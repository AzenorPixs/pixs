#!/usr/bin/env node
import http from 'node:http';
import fsp from 'node:fs/promises';
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import crypto from 'node:crypto';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FRONTEND = path.resolve(HERE, '..', '..');
const CACHE_ROOT = path.join(FRONTEND, '.cache');
const SESSION_ID = crypto.randomUUID();
const DEADLINE_MS = 90000;
const MAX_BODY = 64 * 1024;
const LOG_CAP = 8 * 1024;
const GRACE_MS = 2000;
const VERSION_CAP_MS = 5000;
const CLOSE_CAP_MS = 2000;
const CASE_COUNT = 3;
const EXPECTED_CASES = Object.freeze(["canonical and French catalogues are complete, immutable and namespaced", "catalogue rejects duplicate, missing and invalid translations", "locale follows the first supported preference, then explicit fallback"]);

const ROUTES = new Map([
  ['/', [path.join(HERE, 'runner.html'), 'text/html; charset=utf-8']],
  ['/tests/shell.test.mjs', [path.resolve(FRONTEND, 'tests', 'shell.test.mjs'), 'text/javascript; charset=utf-8']],
  ['/src/catalogs.js', [path.resolve(FRONTEND, 'src', 'catalogs.js'), 'text/javascript; charset=utf-8']],
  ['/t/test-adapter.mjs', [path.join(HERE, 'test-adapter.mjs'), 'text/javascript; charset=utf-8']],
  ['/t/assert-adapter.mjs', [path.join(HERE, 'assert-adapter.mjs'), 'text/javascript; charset=utf-8']],
]);

const BROWSERS = [
  {
    id: 'chromium',
    bin: '/usr/bin/chromium',
    args: (url, profile) => ['--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
      '--disable-crash-reporter', `--user-data-dir=${profile}`, url],
  },
  {
    id: 'firefox',
    bin: '/usr/bin/firefox',
    args: (url, profile) => ['-headless', '-no-remote', '-profile', profile, url],
  },
];

const deadlineAt = Date.now() + DEADLINE_MS;
const remaining = () => Math.max(0, deadlineAt - Date.now());
const violations = [];
const posts = new Map();
const runIds = new Map();
const waiters = new Map();
let ORIGIN = null;
let HOST = null;

const withTimeout = async (promise, ms) => {
  let timer;
  try {
    return await Promise.race([promise, new Promise((resolve) => { timer = setTimeout(() => resolve(false), ms); })]);
  } finally {
    clearTimeout(timer);
  }
};

function makeLog() {
  const chunks = []; let bytes = 0; let truncated = false;
  return {
    append(chunk) {
      const room = LOG_CAP - bytes;
      if (chunk.length > room) truncated = true;
      if (room > 0) { const part = chunk.subarray(0, room); chunks.push(part); bytes += part.length; }
    },
    get value() { return Buffer.concat(chunks).toString('utf8') + (truncated ? '…[borné]' : ''); },
  };
}

const cleanEnv = (d) => ({
  PATH: '/usr/bin:/bin',
  LANG: 'C.UTF-8',
  HOME: d.h,
  TMPDIR: d.t,
  XDG_CACHE_HOME: d.c,
  XDG_CONFIG_HOME: d.g,
  XDG_DATA_HOME: d.u,
});

async function makeDirs() {
  const root = await fsp.mkdtemp(path.join(CACHE_ROOT, 'u-'));
  const d = { root, p: path.join(root, 'p'), h: path.join(root, 'h'), t: path.join(root, 't'), c: path.join(root, 'c'), g: path.join(root, 'g'), u: path.join(root, 'u') };
  try {
    for (const x of [d.p, d.h, d.t, d.c, d.g, d.u]) await fsp.mkdir(x, { recursive: true });
    return d;
  } catch (error) {
    await fsp.rm(root, { recursive: true, force: true });
    throw error;
  }
}

function send(res, code, type, body) {
  res.writeHead(code, { 'Content-Type': type, 'Cache-Control': 'no-store' });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    if (Number(req.headers['content-length'] || '0') > MAX_BODY) {
      req.destroy();
      reject(new Error('body_trop_grand'));
      return;
    }
    const chunks = [];
    let size = 0;
    req.on('data', (c) => {
      size += c.length;
      if (size > MAX_BODY) {
        req.destroy();
        reject(new Error('body_trop_grand'));
        return;
      }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

function validateCase(c, i) {
  const e = [];
  if (c === null || typeof c !== 'object' || Array.isArray(c)) return [`cas_${i}_non_objet`];
  if (typeof c.name !== 'string' || c.name.length === 0 || c.name.length > 128) e.push(`nom_${i}_invalide`);
  if (c.status !== 'pass' && c.status !== 'fail') e.push(`statut_${i}_invalide`);
  if (c.status === 'fail' && (typeof c.error !== 'string' || c.error.length > 512)) e.push(`erreur_${i}_invalide`);
  if (c.status === 'pass' && 'error' in c && c.error !== null && c.error !== '') e.push(`erreur_${i}_invalide`);
  return e;
}

function validatePost(body, browserId, runId) {
  const e = [];
  if (body === null || typeof body !== 'object' || Array.isArray(body)) return ['payload_non_objet'];
  if (body.run_id !== runId) e.push('run_id_divergent');
  if (body.browser !== browserId) e.push('browser_divergent');
  if (body.phase !== 'result' && body.phase !== 'init_error') e.push('phase_invalide');
  if (body.phase === 'result') {
    if (!Array.isArray(body.cases) || body.cases.length !== CASE_COUNT) {
      e.push('nombre_cas_invalide');
    } else {
      for (let i = 0; i < CASE_COUNT; i += 1) e.push(...validateCase(body.cases[i], i));
      const names = body.cases.map((c) => (c && typeof c.name === 'string' ? c.name : ''));
      if (new Set(names).size !== CASE_COUNT) e.push('noms_dupliques');
      if (EXPECTED_CASES.length === CASE_COUNT
        && names.slice().sort().join('\u0000') !== EXPECTED_CASES.slice().sort().join('\u0000')) e.push('noms_attendus');
      if (typeof body.ok !== 'boolean' || body.ok !== body.cases.every((c) => c && c.status === 'pass')) e.push('ok_incoherent');
    }
  }
  if (body.phase === 'init_error' && (body.ok !== false || typeof body.error !== 'string' || body.error.length > 512)) e.push('init_error_invalide');
  return e;
}

const server = http.createServer(async (req, res) => {
  try {
    if (req.headers.host !== HOST) {
      violations.push('host_divergent');
      send(res, 400, 'text/plain; charset=utf-8', 'host_divergent');
      return;
    }
    const pathname = decodeURIComponent(new URL(req.url, ORIGIN).pathname);
    if (req.method === 'POST' && pathname === '/result') {
      if (req.headers.origin !== ORIGIN) {
        violations.push('origine_divergente');
        send(res, 403, 'text/plain; charset=utf-8', 'origine_divergente');
        return;
      }
      let raw;
      try {
        raw = await readBody(req);
      } catch {
        violations.push('body_trop_grand');
        send(res, 413, 'application/json; charset=utf-8', '{"error":"body_trop_grand"}');
        return;
      }
      let body = null;
      try {
        body = JSON.parse(raw.toString('utf8'));
      } catch {
        violations.push('json_corrompu');
        send(res, 400, 'application/json; charset=utf-8', '{"error":"json_corrompu"}');
        return;
      }
      const bid = body !== null && typeof body === 'object' ? body.browser : null;
      if (!runIds.has(bid) || remaining() === 0) {
        violations.push('browser_inconnu');
        send(res, 404, 'application/json; charset=utf-8', '{"error":"browser_inconnu"}');
        return;
      }
      if (posts.has(bid)) {
        violations.push(`duplicata_ou_tardif_${bid}`);
        send(res, 409, 'application/json; charset=utf-8', '{"error":"duplicata_ou_tardif"}');
        return;
      }
      const errors = validatePost(body, bid, runIds.get(bid));
      if (errors.length > 0) {
        violations.push(...errors.map((x) => `${x}:${bid}`));
        send(res, 400, 'application/json; charset=utf-8', `{"errors":${JSON.stringify(errors)}}`);
        return;
      }
      posts.set(bid, body);
      if (body.phase === 'init_error') violations.push(`init_recu_${bid}`);
      const wake = waiters.get(bid);
      if (wake) wake();
      send(res, 200, 'application/json; charset=utf-8', '{"status":"accepted"}');
      return;
    }
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      send(res, 405, 'text/plain; charset=utf-8', 'methode_interdite');
      return;
    }
    const route = ROUTES.get(pathname);
    if (!route) {
      send(res, 404, 'text/plain; charset=utf-8', 'non_autorise');
      return;
    }
    const data = await fsp.readFile(route[0]);
    res.writeHead(200, { 'Content-Type': route[1], 'Cache-Control': 'no-store' });
    res.end(req.method === 'HEAD' ? undefined : data);
  } catch (err) {
    violations.push(`serveur_${String(err && err.message).slice(0, 150)}`);
    if (!res.headersSent) send(res, 500, 'text/plain; charset=utf-8', 'erreur');
    else res.destroy();
  }
});

server.on('error', (error) => { violations.push(`http_${String(error.message).slice(0, 150)}`); });

function waitBrowser(id, procClosed) {
  return new Promise((resolve) => {
    let done = false;
    const finish = (why) => {
      if (done) return;
      done = true;
      clearTimeout(timer);
      waiters.delete(id);
      resolve(why);
    };
    const timer = setTimeout(() => finish('deadline'), Math.max(1, remaining() - 2 * GRACE_MS - CLOSE_CAP_MS));
    procClosed.then(() => finish('exit'));
    waiters.set(id, () => finish('post'));
  });
}

function killGroup(child, closed) {
  return (async () => {
    if (child.exitCode !== null || child.signalCode !== null) return (await withTimeout(closed, GRACE_MS)) ? 'dej_termine' : 'process_vivant';
    try {
      process.kill(-child.pid, 'SIGTERM');
    } catch (err) {
      if (err.code !== 'ESRCH') { try { child.kill('SIGTERM'); } catch { violations.push(`sigterm_${child.pid}`); } }
    }
    if (await withTimeout(closed, GRACE_MS)) return 'sigterm';
    try {
      process.kill(-child.pid, 'SIGKILL');
    } catch (err) {
      if (err.code !== 'ESRCH') { try { child.kill('SIGKILL'); } catch { violations.push(`sigkill_${child.pid}`); } }
    }
    return (await withTimeout(closed, GRACE_MS)) ? 'sigkill' : 'process_vivant';
  })();
}

async function removeProfile(root) {
  await fsp.rm(root, { recursive: true, force: true });
  try {
    await fsp.access(root);
    return false;
  } catch {
    return true;
  }
}

function startProcess(browser, args, dirs) {
  const child = spawn(browser.bin, args, { env: cleanEnv(dirs), detached: true, stdio: ['ignore', 'pipe', 'pipe'] });
  const stdout = makeLog(); const stderr = makeLog();
  const state = { child, stdout, stderr, isClosed: false, exit: null, error: null };
  state.closed = new Promise((resolve) => {
    child.once('error', (error) => { state.error = String(error.message).slice(0, 150); });
    child.once('exit', (code, signal) => { state.exit = { code, signal }; });
    child.once('close', () => { state.isClosed = true; resolve(true); });
  });
  child.stdout.on('data', (part) => stdout.append(part));
  child.stderr.on('data', (part) => stderr.append(part));
  return state;
}

async function stopProcess(state) {
  if (state.isClosed) return true;
  await killGroup(state.child, state.closed);
  return state.isClosed;
}

async function captureVersion(browser, dirs) {
  const state = startProcess(browser, ['--version'], dirs);
  const completed = await withTimeout(state.closed, Math.max(1, Math.min(VERSION_CAP_MS, remaining())));
  if (!completed) violations.push(`version_deadline_${browser.id}`);
  const closed = await stopProcess(state);
  const text = state.stdout.value.trim().split('\n').find((line) => /Chromium|Firefox/.test(line)) || '';
  return { ok: completed && closed && !state.error && state.exit?.code === 0 && text.length > 0,
    text, failed: state.error, closed };
}

async function runBrowser(browser) {
  const rec = { id: browser.id, bin: browser.bin, version: null, post: null, exit: null,
    stderr: '', killed: 'none', processClosed: false, profileRemoved: false, runId: crypto.randomUUID() };
  let dirs = null; let state = null; let versionClosed = true;
  try {
    dirs = await makeDirs(); runIds.set(browser.id, rec.runId);
    const ver = await captureVersion(browser, dirs); versionClosed = ver.closed; rec.version = ver.text;
    if (!ver.ok) { violations.push(`version_echouee_${browser.id}`); return rec; }
    if (remaining() <= 2 * GRACE_MS + CLOSE_CAP_MS) { violations.push('deadline_avant_demarrage'); return rec; }
    const url = `${ORIGIN}/?run_id=${rec.runId}&browser=${browser.id}`;
    state = startProcess(browser, browser.args(url, dirs.p), dirs);
    const outcome = await waitBrowser(browser.id, state.closed);
    rec.post = posts.get(browser.id) || null;
    if (outcome === 'deadline') violations.push(`deadline_${browser.id}`);
    else if (outcome === 'exit' && !rec.post) violations.push(`process_sorti_sans_post_${browser.id}`);
    if (state.error) violations.push(`process_${browser.id}`);
  } catch (error) {
    violations.push(`browser_${browser.id}_${String(error.message).slice(0, 150)}`);
  } finally {
    runIds.delete(browser.id); waiters.delete(browser.id);
    if (state) { rec.processClosed = await stopProcess(state); rec.exit = state.exit; rec.stderr = state.stderr.value; }
    else rec.processClosed = versionClosed;
    rec.killed = rec.processClosed ? 'closed_observed' : 'process_vivant';
    if (dirs && rec.processClosed) rec.profileRemoved = await removeProfile(dirs.root);
    if (!rec.processClosed || !rec.profileRemoved) violations.push(`nettoyage_incomplet_${browser.id}`);
  }
  return rec;
}

async function listen() {
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => {
      server.removeListener('error', reject);
      resolve();
    });
  });
  ORIGIN = `http://127.0.0.1:${server.address().port}`;
  HOST = `127.0.0.1:${server.address().port}`;
}

async function closeServer() {
  const closing = new Promise((resolve) => server.close(() => resolve(true)));
  if (typeof server.closeIdleConnections === 'function') server.closeIdleConnections();
  if (typeof server.closeAllConnections === 'function') server.closeAllConnections();
  return withTimeout(closing, CLOSE_CAP_MS);
}

function finalize(records, serverClosed, errors) {
  const browsers = {};
  for (const r of records) {
    browsers[r.id] = {
      version: r.version,
      post: r.post,
      exit: r.exit,
      killed: r.killed,
      process_closed: r.processClosed,
      profile_removed: r.profileRemoved,
      stderr: r.stderr,
    };
  }
  const ok = errors.length === 0 && violations.length === 0 && serverClosed
    && records.length === BROWSERS.length
    && records.every((r) => r.post && r.post.phase === 'result' && r.post.ok === true
      && Array.isArray(r.post.cases) && r.post.cases.length === CASE_COUNT
      && r.post.cases.every((c) => c.status === 'pass')
      && r.version && r.processClosed && r.profileRemoved);
  return {
    schema: 'catalog-browser/2',
    ok,
    code: ok ? 0 : 1,
    session_id: SESSION_ID,
    deadline_ms: DEADLINE_MS,
    elapsed_ms: Date.now() + 0 - (deadlineAt - DEADLINE_MS),
    server_closed: serverClosed,
    browsers,
    violations,
    errors,
  };
}

async function main() {
  if (process.argv.length !== 2) throw new Error("Unsupported runner arguments");
  const errors = [];
  const records = [];
  let serverClosed = false;
  try {
    await listen();
    for (const browser of BROWSERS) {
      if (remaining() === 0) {
        violations.push('deadline_avant_demarrage');
        break;
      }
      records.push(await runBrowser(browser));
    }
  } catch (err) {
    errors.push(String(err && err.message).slice(0, 300));
  }
  serverClosed = await closeServer();
  if (!serverClosed) violations.push('serveur_non_ferme');
  const output = finalize(records, serverClosed, errors);
  process.stdout.write(JSON.stringify(output, null, 2) + '\n');
  process.exitCode = output.code;
}

await main();
