// Lancement frontend capture : CLI bornee, sans env ni decouverte.
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { prepareFrontendComposition } from './prepare_frontend_composition.mjs';
import { createFrontendViteConfig } from '../vite.config.js';
import { build, createServer } from 'vite';

const COMPOSED_OPTIONS = ['selection', 'selection-sha256', 'policy', 'policy-sha256', 'max-policy-bytes', 'max-wire-bytes', 'python'];
const KNOWN_OPTIONS = new Set(['mode', 'command', ...COMPOSED_OPTIONS]);
const EXCLUDED_PARTS = new Set([
  '.git', '.opencode', 'node_modules', '.cache', '.venv', 'venv', 'env', 'logs',
  'tmp', '__pycache__', '.idea', '.mypy_cache', '.npm', '.pytest_cache', '.ruff_cache',
  '.stfolder', '.stignore', '.vscode', '.python-version', 'credentials.json',
  'credentials.yaml', 'secrets.json', 'secrets.yaml', 'id_rsa', 'id_ed25519',
]);
const EXCLUDED_SUFFIXES = ['.pem', '.key', '.p12', '.pfx', '.crt', '.cer', '.der'];

export class CliError extends Error {
  constructor(code, options) {
    super(code, options);
    this.name = 'CliError';
    this.code = code;
  }
}
function fail(code, cause) { throw new CliError(code, cause === undefined ? undefined : { cause }); }
function assertHex64(value) {
  if (typeof value !== 'string' || value.length !== 64 || !/^[0-9a-f]{64}$/.test(value)) fail('CLI_PIN_INVALID');
}
function assertSafeInt(value) {
  if (typeof value !== 'number' || !Number.isSafeInteger(value) || value <= 0) fail('CLI_BOUNDS_INVALID');
}
function parsePositiveInt(text) {
  if (typeof text !== 'string' || !/^[0-9]+$/.test(text)) fail('CLI_BOUNDS_INVALID');
  const value = Number(text);
  assertSafeInt(value);
  return value;
}

export function parseCliArgs(argv) {
  const seen = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (typeof token !== 'string' || !token.startsWith('--')) fail('CLI_OPTION_UNKNOWN');
    const cut = token.indexOf('=');
    let name;
    let value;
    if (cut === -1) {
      name = token.slice(2);
      value = argv[i + 1];
      i += 1;
    } else {
      name = token.slice(2, cut);
      value = token.slice(cut + 1);
    }
    if (!KNOWN_OPTIONS.has(name)) fail('CLI_OPTION_UNKNOWN');
    if (typeof value !== 'string' || !value) fail('CLI_OPTION_MISSING');
    if (value.startsWith('--')) fail('CLI_OPTION_MISSING');
    if (seen.has(name)) fail('CLI_OPTION_DUPLICATE');
    seen.set(name, value);
  }
  const mode = seen.get('mode');
  const command = seen.get('command');
  if (mode !== 'STANDALONE' && mode !== 'COMPOSED') fail('CLI_MODE_INVALID');
  if (command !== 'build' && command !== 'serve') fail('CLI_COMMAND_INVALID');
  if (mode === 'STANDALONE') {
    for (const name of COMPOSED_OPTIONS) if (seen.has(name)) fail('CLI_OPTION_UNUSED');
    return { mode, command };
  }
  for (const name of COMPOSED_OPTIONS) if (!seen.has(name)) fail('CLI_OPTION_MISSING');
  const selection = seen.get('selection');
  const selectionSha256 = seen.get('selection-sha256');
  const policy = seen.get('policy');
  const policySha256 = seen.get('policy-sha256');
  assertHex64(selectionSha256);
  assertHex64(policySha256);
  const maxPolicyBytes = parsePositiveInt(seen.get('max-policy-bytes'));
  const maxWireBytes = parsePositiveInt(seen.get('max-wire-bytes'));
  const python = seen.get('python');
  if (typeof python !== 'string' || !path.isAbsolute(python) || (/[\r\n]/.test(python) || python.includes(String.fromCharCode(0)))) fail('CLI_PYTHON_INVALID');
  return { mode, command, selection, selectionSha256, policy, policySha256, maxPolicyBytes, maxWireBytes, python };
}

export function projectRootFromScript() {
  return path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
}
function assertRelativePosix(rel) {
  if (typeof rel !== 'string' || !rel) fail('CLI_PATH_INVALID');
  if (rel.includes('\\') || rel.includes(String.fromCharCode(0)) || rel.includes('\r') || rel.includes('\n')) fail('CLI_PATH_INVALID');
  if (rel.startsWith('/') || rel.startsWith('./') || rel === '.' || rel === '..') fail('CLI_PATH_INVALID');
  if (rel.endsWith('/')) fail('CLI_PATH_INVALID');
  const parts = rel.split('/');
  for (const part of parts) {
    if (!part || part === '.' || part === '..') fail('CLI_PATH_INVALID');
  }
  return rel;
}
function assertNotExcluded(rel) {
  if (!rel.endsWith('.json')) fail('CLI_PATH_INVALID');
  for (const part of rel.split('/')) {
    const lower = part.toLowerCase();
    if (EXCLUDED_PARTS.has(lower) || lower.endsWith('.env') || lower.includes('.env.')
        || EXCLUDED_SUFFIXES.some(suffix => lower.endsWith(suffix))) fail('CLI_PATH_EXCLUDED');
  }
}

export function readOperatorFile(rootReal, rel, maxBytes) {
  assertRelativePosix(rel);
  assertNotExcluded(rel);
  assertSafeInt(maxBytes);
  let rootCanonical;
  try { rootCanonical = fs.realpathSync(rootReal); } catch { fail('CLI_ROOT_INVALID'); }
  const target = path.join(rootCanonical, rel);
  if (target !== rootCanonical && !target.startsWith(rootCanonical + path.sep)) fail('CLI_PATH_INVALID');
  const dir = path.dirname(target);
  const relDir = path.relative(rootCanonical, dir);
  if (relDir && relDir !== '') {
    const steps = relDir.split(path.sep);
    let current = rootCanonical;
    for (const step of steps) {
      current = path.join(current, step);
      let stat;
      try { stat = fs.lstatSync(current); } catch { fail('CLI_PATH_INVALID'); }
      if (stat.isSymbolicLink()) fail('CLI_PATH_INVALID');
      if (!stat.isDirectory()) fail('CLI_PATH_INVALID');
    }
  }
  let fd = -1;
  try {
    fd = fs.openSync(target, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
    const before = fs.fstatSync(fd, { bigint: true });
    if (!before.isFile()) fail('CLI_PATH_INVALID');
    if (before.size <= 0n || before.size > BigInt(maxBytes)) fail('CLI_BYTES_INVALID');
    let canonical;
    try { canonical = fs.realpathSync('/proc/self/fd/' + String(fd)); } catch { fail('CLI_PATH_INVALID'); }
    if (canonical !== target || (!canonical.startsWith(rootCanonical + path.sep))) fail('CLI_PATH_INVALID');
    const chunks = [];
    let total = 0;
    const block = 65536;
    for (;;) {
      const buf = Buffer.alloc(Math.min(block, maxBytes + 1 - total));
      const read = fs.readSync(fd, buf, 0, buf.length, null);
      if (read === 0) break;
      total += read;
      if (total > maxBytes) fail('CLI_BYTES_INVALID');
      chunks.push(buf.subarray(0, read));
    }
    const after = fs.fstatSync(fd, { bigint: true });
    if (after.dev !== before.dev || after.ino !== before.ino || after.size !== before.size || after.mtimeNs !== before.mtimeNs || after.ctimeNs !== before.ctimeNs) fail('CLI_PATH_CHANGED');
    if (total === 0 || BigInt(total) !== before.size) fail('CLI_BYTES_INVALID');
    return Buffer.concat(chunks, total);
  } finally {
    if (fd !== -1) fs.closeSync(fd);
  }
}

export function loadOperatorBytes(rootCanonical, parsed) {
  const selectionBytes = readOperatorFile(rootCanonical, parsed.selection, parsed.maxWireBytes);
  const policyBytes = readOperatorFile(rootCanonical, parsed.policy, parsed.maxPolicyBytes);
  if (createHash('sha256').update(selectionBytes).digest('hex') !== parsed.selectionSha256) fail('CLI_PIN_MISMATCH');
  if (createHash('sha256').update(policyBytes).digest('hex') !== parsed.policySha256) fail('CLI_PIN_MISMATCH');
  return { selectionBytes, policyBytes };
}

export function createCompositionFromOptions(parsed, bytes) {
  return prepareFrontendComposition({
    selectionBytes: Buffer.from(bytes.selectionBytes),
    expectedSelectionSha256: parsed.selectionSha256,
    policyBytes: Buffer.from(bytes.policyBytes),
    expectedPolicySha256: parsed.policySha256,
    maxPolicyBytes: parsed.maxPolicyBytes,
    maxWireBytes: parsed.maxWireBytes,
    pythonExecutable: parsed.python,
  });
}
export function verifyOperatorAndComposition(rootCanonical, parsed, bytes, composition) {
  const freshSelection = readOperatorFile(rootCanonical, parsed.selection, parsed.maxWireBytes);
  const freshPolicy = readOperatorFile(rootCanonical, parsed.policy, parsed.maxPolicyBytes);
  if (freshSelection.length !== bytes.selectionBytes.length || freshPolicy.length !== bytes.policyBytes.length) fail('CLI_VERIFY_FAILED');
  if (!freshSelection.equals(bytes.selectionBytes) || !freshPolicy.equals(bytes.policyBytes)) fail('CLI_VERIFY_FAILED');
  if (createHash('sha256').update(freshSelection).digest('hex') !== parsed.selectionSha256) fail('CLI_VERIFY_FAILED');
  if (createHash('sha256').update(freshPolicy).digest('hex') !== parsed.policySha256) fail('CLI_VERIFY_FAILED');
  try { composition.verifyBeforePublish(); } catch (cause) { fail('CLI_VERIFY_FAILED', cause); }
}

export async function runBuildWithComposition(mode, composition) {
  const config = createFrontendViteConfig({ mode, composition });
  await build({ ...config, configFile: false });
}
export async function runServeWithComposition(mode, composition, watchOptions) {
  const config = createFrontendViteConfig({ mode, composition });
  const server = await createServer({ ...config, configFile: false });
  let drifted = false;
  let closed = false;
  let closePromise;
  let pending = false;
  const watched = watchOptions?.paths ?? [];
  const verify = watchOptions?.verify;
  if (mode === 'COMPOSED' && (typeof verify !== 'function' || watched.length !== 2)) {
    await server.close();
    fail('CLI_WATCH_INVALID');
  }
  const onChange = file => {
    if (closed || drifted || pending || !watched.includes(file)) return;
    pending = true;
    queueMicrotask(() => {
      pending = false;
      if (closed || drifted) return;
      try { verify(); }
      catch (cause) {
        drifted = true;
        server.config.logger.error('CLI_VERIFY_FAILED');
      }
    });
  };
  const cleanup = () => {
    if (closePromise) return closePromise;
    closed = true;
    closePromise = (async () => {
      for (const event of ['change', 'add', 'unlink']) server.watcher.off(event, onChange);
      await server.close();
    })();
    return closePromise;
  };
  const onSignal = () => {
    cleanup().catch(() => {
      process.stderr.write('CLI_CLOSE_FAILED\n');
      process.exitCode = 1;
    });
  };
  process.once('SIGINT', onSignal);
  process.once('SIGTERM', onSignal);
  try {
    if (mode === 'COMPOSED') {
      server.watcher.add(watched);
      for (const event of ['change', 'add', 'unlink']) server.watcher.on(event, onChange);
      server.middlewares.use((request, response, next) => {
        if (!drifted) return next();
        response.statusCode = 503;
        response.setHeader('Content-Type', 'text/plain; charset=utf-8');
        response.setHeader('Cache-Control', 'no-store');
        response.setHeader('X-Content-Type-Options', 'nosniff');
        response.end('CLI_VERIFY_FAILED');
      });
      verify();
    }
    const finished = new Promise(resolve => {
      server.httpServer?.once('close', resolve);
    });
    await server.listen();
    server.printUrls();
    await finished;
  } finally {
    process.off('SIGINT', onSignal);
    process.off('SIGTERM', onSignal);
    await cleanup();
  }
}
async function main() {
  const parsed = parseCliArgs(process.argv.slice(2));
  const rootCanonical = fs.realpathSync(projectRootFromScript());
  if (parsed.mode === 'STANDALONE') {
    if (parsed.command === 'build') await runBuildWithComposition('STANDALONE', null);
    else await runServeWithComposition('STANDALONE', null, null);
    return;
  }
  const bytes = loadOperatorBytes(rootCanonical, parsed);
  const composition = createCompositionFromOptions(parsed, bytes);
  verifyOperatorAndComposition(rootCanonical, parsed, bytes, composition);
  if (parsed.command === 'build') {
    await runBuildWithComposition('COMPOSED', composition);
    verifyOperatorAndComposition(rootCanonical, parsed, bytes, composition);
    return;
  }
  const watched = [path.join(rootCanonical, parsed.selection), path.join(rootCanonical, parsed.policy)];
  await runServeWithComposition('COMPOSED', composition, { paths: watched, verify: () => verifyOperatorAndComposition(rootCanonical, parsed, bytes, composition) });
}
function isCliEntry() {
  try {
    const entry = process.argv[1] ? fs.realpathSync(path.resolve(process.argv[1])) : '';
    return entry === fs.realpathSync(fileURLToPath(import.meta.url));
  } catch { return false; }
}
if (isCliEntry()) {
  main().catch((error) => {
    const code = typeof error?.code === 'string' && /^[A-Z][A-Z0-9_]{0,63}$/.test(error.code) ? error.code : 'CLI_FAILED';
    process.stderr.write(code + '\n');
    process.exitCode = 1;
  });
}
