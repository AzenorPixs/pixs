// browser-check.mjs — validation navigateur locale Chromium headless ephemere.
// Preuves limitees aux criteres 3.2 : route/refus, langues, themes, clavier, reflow.
// Ne constitue ni un audit WCAG complet ni une preuve P0.
// Exige un serveur Vite deja demarre sur http://127.0.0.1:5173 (mandat CAB distinct).
import { spawn, spawnSync } from 'node:child_process';
import { mkdtemp, readFile, rm, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { catalogs } from '../src/catalogs.js';

const CHROMIUM = '/usr/lib/chromium/chromium';
const VITE_ORIGIN = 'http://127.0.0.1:5173';
const WS_ALLOWED = 'ws://127.0.0.1:5173/';
const GLOBAL_MS = 90000;
const CALL_MS = 12000;

const here = path.dirname(fileURLToPath(import.meta.url));
const frontendRoot = path.resolve(here, '..');
const cacheParent = path.join(frontendRoot, '.cache');

function withTimeout(promise, ms, label) {
  let t;
  const guard = new Promise((_, reject) => {
    t = setTimeout(() => reject(new Error(`timeout ${label} (${ms}ms)`)), ms);
  });
  return Promise.race([promise, guard]).finally(() => clearTimeout(t));
}

function cleanEnv(ephemeral) {
  return {
    PATH: '/usr/bin:/bin',
    LANG: 'C.UTF-8',
    TMPDIR: ephemeral,
    XDG_CACHE_HOME: path.join(ephemeral, 'xdg-cache'),
    XDG_CONFIG_HOME: path.join(ephemeral, 'xdg-config'),
  };
}

function chromiumVersion(env) {
  const r = spawnSync(CHROMIUM, ['--version'], { env, timeout: 10000, encoding: 'utf8' });
  const out = `${r.stdout ?? ''}${r.stderr ?? ''}`.trim();
  if (r.status !== 0 || !out) throw new Error(`chromium --version exit ${r.status}: ${out}`);
  return out;
}

async function httpGetJson(url) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(new Error(`timeout GET ${url}`)), CALL_MS);
  try {
    const { get } = await import('node:http');
    return await new Promise((resolve, reject) => {
      const req = get(url, { signal: ctrl.signal }, (res) => {
        let data = '';
        res.on('data', (c) => { data += c; });
        res.on('end', () => {
          try { resolve(JSON.parse(data)); } catch (e) { reject(new Error(`parse JSON ${url}: ${e.message}`)); }
        });
        res.on('error', (e) => reject(new Error(`reponse ${url}: ${e.message}`)));
      });
      req.on('error', (e) => reject(new Error(`GET ${url}: ${e.message}`)));
    });
  } finally {
    clearTimeout(t);
  }
}

class Cdp {
  constructor(url, deadline, cdpErrors) {
    this.url = url;
    this.deadline = deadline;
    this.cdpErrors = cdpErrors;
    this.id = 0;
    this.pending = new Map();
    this.listeners = new Map();
    this.socket = null;
  }
  connect() {
    return withTimeout(new Promise((resolve, reject) => {
      const ws = new WebSocket(this.url);
      this.socket = ws;
      ws.onopen = () => resolve();
      ws.onerror = () => reject(new Error('CDP connexion erreur'));
      ws.onmessage = (ev) => {
        let msg;
        try {
          msg = JSON.parse(ev.data);
        } catch (e) {
          this.cdpErrors.push(`parse CDP: ${e?.message ?? e}`);
          return;
        }
        if (msg.id !== undefined && this.pending.has(msg.id)) {
          const { resolve, reject } = this.pending.get(msg.id);
          this.pending.delete(msg.id);
          if (msg.error) reject(new Error(`CDP ${msg.error.message ?? JSON.stringify(msg.error)}`));
          else resolve(msg.result ?? {});
        } else if (msg.method) {
          const arr = this.listeners.get(msg.method) ?? [];
          for (const fn of [...arr]) {
            try { fn(msg); } catch (e) { this.cdpErrors.push(`listener ${msg.method}: ${e?.message ?? e}`); }
          }
        }
      };
      ws.onclose = () => {
        if (this.pending.size > 0) this.cdpErrors.push(`CDP close avec ${this.pending.size} appels en vol`);
        for (const { reject } of this.pending.values()) reject(new Error('CDP socket fermee'));
        this.pending.clear();
      };
    }), CALL_MS, 'connexion CDP');
  }
  on(method, fn) {
    const arr = this.listeners.get(method) ?? [];
    arr.push(fn);
    this.listeners.set(method, arr);
  }
  send(method, params = {}, sessionId) {
    if (Date.now() > this.deadline) return Promise.reject(new Error(`delai global 90s depasse avant CDP ${method}`));
    const id = ++this.id;
    const payload = { id, method, params };
    if (sessionId) payload.sessionId = sessionId;
    const p = new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      try { this.socket.send(JSON.stringify(payload)); } catch (e) { this.pending.delete(id); reject(e); }
    });
    return withTimeout(p, CALL_MS, `CDP ${method}`);
  }
  close() {
    try { this.socket?.close(); } catch (e) { this.cdpErrors.push(`close: ${e?.message ?? e}`); }
  }
}

async function main() {
  await mkdir(cacheParent, { recursive: true });
  const ephemeral = await mkdtemp(path.join(cacheParent, 'b-'));
  const profileDir = path.join(ephemeral, 'profil');
  const env = cleanEnv(ephemeral);

  const errors = [];
  const cdpErrors = [];
  const note = (where, e) => errors.push(`${where}: ${e?.message ?? String(e)}`);
  let version = '';
  try { version = chromiumVersion(env); } catch (e) { note('version', e); }

  let child = null;
  let closed = false;
  let cdp = null;
  let stderrHead = '';
  let childPid = null;
  const consoleErrors = [];
  const runtimeErrors = [];
  const fetchErrors = [];
  const httpErrors = [];
  let allowedCount = 0;
  let blockedCount = 0;
  const blockedSample = [];
  const deadline = Date.now() + GLOBAL_MS;

  const cleanup = async () => {
    const out = { profileRemoved: false, processClosed: false, signalCode: null, cleanupErrors: [] };
    try { cdp?.close(); } catch (e) { out.cleanupErrors.push(`cdp.close: ${e?.message ?? e}`); }
    if (child) {
      const alreadyGone = child.exitCode !== null || child.signalCode !== null || closed;
      if (!alreadyGone) {
        const done = new Promise((resolve) => {
          child.once('close', (code, signal) => resolve({ code, signal }));
          child.once('exit', (code, signal) => resolve({ code, signal }));
        });
        try { process.kill(-child.pid, 'SIGTERM'); } catch (e) { out.cleanupErrors.push(`SIGTERM groupe ${child.pid}: ${e?.message ?? e}`); }
        const st = await withTimeout(done, 5000, 'arret chromium').catch((e) => {
          out.cleanupErrors.push(e.message);
          return null;
        });
        if (st) out.signalCode = st.signal ?? null;
        const stillAlive = child.exitCode === null && child.signalCode === null;
        if (stillAlive) {
          try { process.kill(-child.pid, 'SIGKILL'); } catch (e) { out.cleanupErrors.push(`SIGKILL groupe ${child.pid}: ${e?.message ?? e}`); }
          await withTimeout(new Promise((r) => {
            child.once('close', () => r(true));
            child.once('exit', () => r(true));
            setTimeout(() => r(false), 3000);
          }), 4000, 'sigkill').catch((e) => out.cleanupErrors.push(e.message));
        }
      }
      out.signalCode = out.signalCode ?? child.signalCode ?? null;
      out.processClosed = child.exitCode !== null || child.signalCode !== null || closed;
      if (!out.processClosed) out.cleanupErrors.push('processus non termine (preuve manquante)');
    } else {
      out.processClosed = true;
    }
    try {
      await rm(ephemeral, { recursive: true, force: true });
      out.profileRemoved = true;
    } catch (e) { out.cleanupErrors.push(`rm ephemere: ${e?.message ?? e}`); }
    return out;
  };

  const result = {
    ok: false,
    chromiumVersion: version,
    viteOrigin: VITE_ORIGIN,
    pid: null,
    stderr: '',
    checks: {},
    network: { allowed: 0, blockedExternal: 0, blockedSample: [] },
    http: { errors: 0, sample: [] },
    console: { consoleErrors: 0, runtimeErrors: 0, fetchErrors: 0, sample: [] },
    cleanup: null,
    errors,
    cdpErrors,
  };

  try {
    await mkdir(env.XDG_CACHE_HOME, { recursive: true });
    await mkdir(env.XDG_CONFIG_HOME, { recursive: true });
    await mkdir(profileDir, { recursive: true });
    const chromiumSocketPath = path.join(env.TMPDIR, 'org.chromium.Chromium.XXXXXX', 'SingletonSocket');
    if (Buffer.byteLength(chromiumSocketPath, 'utf8') > 107) throw new Error(`chemin socket trop long (${Buffer.byteLength(chromiumSocketPath, 'utf8')}>107)`);
    if (!version) throw new Error('version Chromium indisponible, arret sans contournement');
    const args = [
      '--headless',
      '--disable-gpu',
      '--no-first-run',
      '--no-default-browser-check',
      '--disable-background-networking',
      '--disable-component-update',
      '--disable-sync',
      '--disable-features=Translate,OptimizationHints',
      `--user-data-dir=${profileDir}`,
      '--remote-debugging-port=0',
      '--remote-debugging-address=127.0.0.1',
      'about:blank',
    ];
    child = spawn(CHROMIUM, args, { env, stdio: ['ignore', 'ignore', 'pipe'], detached: true });
    childPid = child.pid ?? null;
    result.pid = childPid;
    child.on('close', () => { closed = true; });
    child.on('exit', () => { closed = true; });
    child.stderr?.on('data', (c) => { if (stderrHead.length < 2000) stderrHead += c.toString().slice(0, 2000 - stderrHead.length); });
    await new Promise((r) => setTimeout(r, 1200));
    const launchFailed = (child.exitCode !== null && child.exitCode !== 0) || child.signalCode !== null;
    if (launchFailed) {
      throw new Error(`Chromium quitte au lancement (code ${child.exitCode} signal ${child.signalCode}) : ${stderrHead.slice(0, 500)}`);
    }
    const portFile = await (async () => {
      const end = Date.now() + 15000;
      for (;;) {
        try {
          const raw = await readFile(path.join(profileDir, 'DevToolsActivePort'), 'utf8');
          const n = Number(raw.split('\n')[0].trim());
          if (Number.isInteger(n) && n > 0 && n < 65536) return n;
        } catch { /* reessaie */ }
        if (Date.now() > end) throw new Error('DevToolsActivePort illisible (timeout 15s)');
        await new Promise((r) => setTimeout(r, 200));
      }
    })();
    const ver = await httpGetJson(`http://127.0.0.1:${portFile}/json/version`);
    if (!ver.webSocketDebuggerUrl || !ver.webSocketDebuggerUrl.startsWith('ws://127.0.0.1:')) {
      throw new Error('endpoint CDP non loopback ou absent');
    }
    const realUA = ver['User-Agent'] ?? ver['user-Agent'] ?? '';
    if (!realUA) throw new Error('User-Agent reel absent de /json/version');
    cdp = new Cdp(ver.webSocketDebuggerUrl, deadline, cdpErrors);
    await cdp.connect();
    const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
    const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
    const S = (m, p = {}) => cdp.send(m, p, sessionId);

    cdp.on('Runtime.consoleAPICalled', (m) => {
      if (m.params?.type === 'error') consoleErrors.push(JSON.stringify((m.params.args ?? []).slice(0, 2)).slice(0, 200));
    });
    cdp.on('Runtime.exceptionThrown', (m) => {
      runtimeErrors.push(String(m.params?.exceptionDetails?.text ?? 'exception').slice(0, 200));
    });
    cdp.on('Log.entryAdded', (m) => {
      const e = m.params?.entry;
      if (e && e.level === 'error') consoleErrors.push(String(e.text ?? e.url ?? '').slice(0, 200));
    });
    cdp.on('Network.responseReceived', (m) => {
      const status = m.params?.response?.status ?? 0;
      const url = m.params?.response?.url ?? '';
      if (status >= 400 && url) httpErrors.push(`${status} ${url.slice(0, 200)}`);
    });
    await S('Fetch.enable', { patterns: [{ urlPattern: '*' }] });
    cdp.on('Fetch.requestPaused', (m) => {
      const p = m.params ?? {};
      const url = p.request?.url ?? '';
      const sid = m.sessionId ?? sessionId;
      const okUrl = url.startsWith(`${VITE_ORIGIN}/`) || url === VITE_ORIGIN || url.startsWith(WS_ALLOWED) || url.startsWith('data:');
      void (async () => {
        try {
          if (okUrl) {
            allowedCount += 1;
            await cdp.send('Fetch.continueRequest', { requestId: p.requestId }, sid);
          } else {
            blockedCount += 1;
            if (blockedSample.length < 5) blockedSample.push(url.slice(0, 200));
            await cdp.send('Fetch.failRequest', { requestId: p.requestId, errorReason: 'BlockedByClient' }, sid);
          }
        } catch (e) { fetchErrors.push(`fetch ${url.slice(0, 80)}: ${e?.message ?? e}`); }
      })();
    });

    await S('Page.enable');
    await S('Runtime.enable');
    await S('Log.enable');
    await S('Network.enable');
    await S('Accessibility.enable');

    const evalJs = async (expression) => {
      const r = await S('Runtime.evaluate', { expression, returnByValue: true });
      if (r.exceptionDetails) throw new Error(`evaluate: ${r.exceptionDetails.text}`);
      return r.result?.value;
    };
    const waitHeading = async (id, label) => {
      const end = Date.now() + 15000;
      for (;;) {
        const present = await evalJs(`document.querySelector("#${id}") !== null`);
        if (present === true) return true;
        if (Date.now() > end) throw new Error(`${label} absent (#${id})`);
        await new Promise((r) => setTimeout(r, 200));
      }
    };
    const navigateAndWait = async (url) => {
      const loaded = new Promise((resolve, reject) => {
        const t = setTimeout(() => reject(new Error(`timeout chargement ${url}`)), 15000);
        cdp.on('Page.loadEventFired', function once() {
          clearTimeout(t);
          const arr = cdp.listeners.get('Page.loadEventFired') ?? [];
          cdp.listeners.set('Page.loadEventFired', arr.filter((f) => f !== once));
          resolve(true);
        });
      });
      await S('Page.navigate', { url });
      await loaded;
      const end = Date.now() + 10000;
      for (;;) {
        const st = await evalJs('({ ready: document.readyState, url: location.href })');
        if (st?.ready === 'complete' && String(st.url).startsWith(VITE_ORIGIN)) return st;
        if (Date.now() > end) throw new Error(`document non complet pour ${url}`);
        await new Promise((r) => setTimeout(r, 200));
      }
    };
    const setSelect = async (want) => {
      await evalJs(`{ const s=[...document.querySelectorAll("select")].find(e=>[...e.options].some(o=>o.value==="${want}")); if(!s) throw new Error("select absent"); s.focus(); s.value="${want}"; s.dispatchEvent(new Event("change",{bubbles:true})); }`);
      await new Promise((r) => setTimeout(r, 350));
    };
    const pressTab = async (withShift) => {
      if (withShift) {
        await S('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Shift', code: 'ShiftLeft', modifiers: 8 });
        await S('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab', code: 'Tab', modifiers: 8, windowsVirtualKeyCode: 9 });
        await S('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab', code: 'Tab', modifiers: 8, windowsVirtualKeyCode: 9 });
        await S('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Shift', code: 'ShiftLeft' });
      } else {
        await S('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
        await S('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab', code: 'Tab' });
      }
      await new Promise((r) => setTimeout(r, 150));
    };

    // Route / exacte canon.
    await navigateAndWait(`${VITE_ORIGIN}/`);
    await waitHeading('home-heading', 'accueil');
    const homeEn = await evalJs('document.querySelector("#home-heading")?.textContent ?? ""');
    result.checks.routeHome = { heading: String(homeEn).slice(0, 80), exactEn: homeEn === catalogs.en['shell.heading'] };

    // Route inconnue : #unavailable-heading + lien retour section.panel a[href='/'].
    await navigateAndWait(`${VITE_ORIGIN}/route-inconnue-xyz`);
    await waitHeading('unavailable-heading', 'introuvable');
    const nf = await evalJs('({ t: document.querySelector("#unavailable-heading")?.textContent ?? "", home: document.querySelector("#home-heading") !== null, back: document.querySelector("section.panel a[href=\'/\']")?.textContent ?? "" })');
    result.checks.routeUnknown = {
      exact: nf.t === catalogs.en['shell.notFound'] || nf.t === catalogs.fr['shell.notFound'],
      backLink: String(nf.back).length > 0,
      noHomeCapacity: nf.home === false,
    };

    // Langue : emulation acceptLanguage AVANT navigation (pas setLocaleOverride).
    await S('Emulation.setUserAgentOverride', { userAgent: realUA, acceptLanguage: 'fr-FR,fr' });
    await navigateAndWait(`${VITE_ORIGIN}/`);
    await waitHeading('home-heading', 'accueil-fr');
    const navLangFr = await evalJs('navigator.languages?.join(",") ?? navigator.language ?? ""');
    const langFr = await evalJs('document.documentElement.lang');
    const headFrFallback = await evalJs('document.querySelector("#home-heading")?.textContent ?? ""');
    const fallbackFr = langFr === 'fr' && headFrFallback === catalogs.fr['shell.heading'];
    // Choix memoire fr puis override en SANS navigation : memoire + timeOrigin conserves.
    await setSelect('fr');
    const tMem0 = await evalJs('performance.timeOrigin');
    const selFr = await evalJs('[...document.querySelectorAll("select")].map(s=>s.value).join("|")');
    await S('Emulation.setUserAgentOverride', { userAgent: realUA, acceptLanguage: 'en-US,en' });
    await new Promise((r) => setTimeout(r, 350));
    const langStillFr = await evalJs('document.documentElement.lang');
    const tMem1 = await evalJs('performance.timeOrigin');
    // Choix en exact.
    await setSelect('en');
    const enHead = await evalJs('document.querySelector("#home-heading")?.textContent ?? ""');
    // Override de-DE,de puis navigation : defaut en AVANT tout setSelect.
    await S('Emulation.setUserAgentOverride', { userAgent: realUA, acceptLanguage: 'de-DE,de' });
    await navigateAndWait(`${VITE_ORIGIN}/`);
    await waitHeading('home-heading', 'accueil-de');
    const langDe = await evalJs('document.documentElement.lang');
    const headDe = await evalJs('document.querySelector("#home-heading")?.textContent ?? ""');
    // AX en francais : forcer fr pour controle nomme.
    await setSelect('fr');
    const axFr = await S('Accessibility.getFullAXTree', {});
    const frNodes = axFr.nodes ?? [];
    const hasName = (role, name) => frNodes.some((n) => n.role?.value === role && n.name?.value === name);
    result.checks.language = {
      navigatorEmulatedFr: navLangFr,
      fallbackFr,
      memoryFrPrevailsNoNav: langStillFr === 'fr' && tMem0 === tMem1,
      selectionsKept: selFr.includes('fr'),
      enExact: enHead === catalogs.en['shell.heading'],
      unsupportedDeDefaultsEn: langDe === 'en' && headDe === catalogs.en['shell.heading'],
      axComboLang: hasName('combobox', catalogs.fr['shell.language']),
      axComboTheme: hasName('combobox', catalogs.fr['shell.theme']),
      axMain: frNodes.some((n) => n.role?.value === 'main'),
      axHeading: frNodes.some((n) => n.role?.value === 'heading' && (n.name?.value === catalogs.fr['shell.heading'])),
      axSkipLink: frNodes.some((n) => n.role?.value === 'link' && n.name?.value === catalogs.fr['shell.skip']),
    };

    // Themes : system reel via setEmulatedMedia, priorite choix, noReload timeOrigin+selections.
    await S('Emulation.setUserAgentOverride', { userAgent: realUA, acceptLanguage: 'en-US,en' });
    await navigateAndWait(`${VITE_ORIGIN}/`);
    await waitHeading('home-heading', 'accueil-theme');
    await setSelect('en');
    const t0 = await evalJs('performance.timeOrigin');
    await setSelect('system');
    await S('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'dark' }] });
    await new Promise((r) => setTimeout(r, 350));
    const sysDark = await evalJs('document.documentElement.dataset.theme ?? ""');
    await S('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'light' }] });
    await new Promise((r) => setTimeout(r, 350));
    const sysLight = await evalJs('document.documentElement.dataset.theme ?? ""');
    const selSys = await evalJs('[...document.querySelectorAll("select")].map(s=>s.value).join("|")');
    await setSelect('dark');
    await S('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'light' }] });
    await new Promise((r) => setTimeout(r, 350));
    const userDarkPrevails = await evalJs('document.documentElement.dataset.theme ?? ""');
    await setSelect('light');
    const userLight = await evalJs('document.documentElement.dataset.theme ?? ""');
    const t1 = await evalJs('performance.timeOrigin');
    const selEnd = await evalJs('[...document.querySelectorAll("select")].map(s=>s.value).join("|")');
    result.checks.themes = {
      systemDark: sysDark === 'dark',
      systemLight: sysLight === 'light',
      userDarkPrevails: userDarkPrevails === 'dark',
      userLight: userLight === 'light',
      noReload: t0 === t1 && selEnd.includes('light') && selSys.includes('system'),
      timeOrigin: [t0, t1],
    };

    // Clavier : 1er Tab -> skip-link mesure, Enter immediat -> #content.
    await navigateAndWait(`${VITE_ORIGIN}/`);
    await waitHeading('home-heading', 'accueil-clavier');
    const initialFocusTag = await evalJs('document.activeElement?.tagName ?? ""');
    await pressTab(false);
    const first = await evalJs('({ cls: document.activeElement?.className ?? "", tag: document.activeElement?.tagName ?? "", rect: (()=>{ const r=document.activeElement?.getBoundingClientRect(); return r ? {x:r.x,y:r.y,w:r.width,h:r.height} : null; })(), outline: getComputedStyle(document.activeElement).outlineWidth || "0" })');
    const firstPx = parseFloat(first.outline) || 0;
    const firstVisible = first.rect && first.rect.w > 0 && first.rect.h > 0 && first.rect.y >= 0;
    const firstIsSkip = String(first.cls).includes('skip-link');
    await S('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 });
    await S('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter' });
    await new Promise((r) => setTimeout(r, 300));
    const afterEnterId = await evalJs('document.activeElement?.id ?? ""');
    // Recharger puis 4 Tab : sequence exacte avec cibles distinctes et focus visibles.
    await navigateAndWait(`${VITE_ORIGIN}/`);
    await waitHeading('home-heading', 'accueil-seq');
    const seq = [];
    for (let i = 0; i < 4; i++) {
      await pressTab(false);
      seq.push(await evalJs('({ tag: document.activeElement?.tagName ?? "", cls: document.activeElement?.className ?? "", val: document.activeElement?.value ?? "", outline: getComputedStyle(document.activeElement).outlineWidth || "0" })'));
    }
    const seqOk =
      String(seq[0]?.cls).includes('skip-link') &&
      seq[1]?.tag === 'A' && String(seq[1]?.cls).includes('brand') &&
      seq[2]?.tag === 'SELECT' && seq[3]?.tag === 'SELECT' &&
      seq[2]?.val !== seq[3]?.val &&
      seq.every((s) => s.outline !== '0px' && s.outline !== '0');
    // Shift+Tab avec modifiers 8 : retour exact theme -> langue.
    const beforeShift = await evalJs('({ val: document.activeElement?.value ?? "", tag: document.activeElement?.tagName ?? "" })');
    await pressTab(true);
    const afterShift = await evalJs('({ val: document.activeElement?.value ?? "", tag: document.activeElement?.tagName ?? "" })');
    result.checks.keyboard = {
      initialFocusTag,
      firstIsSkip,
      firstOutline: first.outline,
      firstOutlineOk: firstPx >= 3,
      firstVisible: Boolean(firstVisible),
      enterToContent: afterEnterId === 'content',
      sequence: seq.map((s) => `${s.tag}:${String(s.cls).slice(0, 12)}:${s.val}`),
      sequenceExact: seqOk,
      beforeShift,
      afterShift,
      shiftBackExact: beforeShift?.val === seq[3]?.val && afterShift?.val === seq[2]?.val && afterShift?.tag === 'SELECT',
    };

    // Reflow 320 CSS px.
    await S('Emulation.setDeviceMetricsOverride', { width: 320, height: 800, deviceScaleFactor: 1, mobile: false });
    await new Promise((r) => setTimeout(r, 300));
    const reflow = await evalJs('({ scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth })');
    result.checks.reflow320 = { ...reflow, ok: reflow.scrollW <= reflow.clientW + 1 };

    // Zoom CSS 200 : proxy supplementaire explicite, pas de zoom natif.
    await S('Emulation.setDeviceMetricsOverride', { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
    await evalJs('document.body.style.zoom = "2"');
    await new Promise((r) => setTimeout(r, 300));
    const z = await evalJs('({ v: String(getComputedStyle(document.body).zoom ?? document.body.style.zoom), scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth, head: document.querySelector("#home-heading")?.textContent?.slice(0,60) ?? "" })');
    await evalJs('document.body.style.zoom = ""');
    result.checks.zoomCSS200 = {
      value: z.v, scrollW: z.scrollW, clientW: z.clientW, textKept: z.head.length > 0,
      explicitProxy: true,
      ok: (z.v === '2' || z.v === '2.0') && z.head.length > 0 && z.scrollW <= z.clientW + 1,
    };

    result.network = { allowed: allowedCount, blockedExternal: blockedCount, blockedSample: [...blockedSample] };
    result.http = { errors: httpErrors.length, sample: [...httpErrors].slice(0, 5) };
    result.console = { consoleErrors: consoleErrors.length, runtimeErrors: runtimeErrors.length, fetchErrors: fetchErrors.length, sample: [...consoleErrors, ...runtimeErrors, ...fetchErrors].slice(0, 5) };
    result.cdpErrors = [...cdpErrors];

    const c = result.checks;
    const allOk =
      c.routeHome?.exactEn === true &&
      c.routeUnknown?.exact === true && c.routeUnknown?.backLink === true && c.routeUnknown?.noHomeCapacity === true &&
      c.language?.fallbackFr === true && c.language?.memoryFrPrevailsNoNav === true &&
      c.language?.enExact === true && c.language?.unsupportedDeDefaultsEn === true &&
      c.language?.axComboLang === true && c.language?.axComboTheme === true &&
      c.language?.axMain === true && c.language?.axHeading === true && c.language?.axSkipLink === true &&
      c.themes?.systemDark === true && c.themes?.systemLight === true &&
      c.themes?.userDarkPrevails === true && c.themes?.userLight === true && c.themes?.noReload === true &&
      c.keyboard?.firstIsSkip === true && c.keyboard?.firstOutlineOk === true && c.keyboard?.firstVisible === true &&
      c.keyboard?.enterToContent === true && c.keyboard?.sequenceExact === true && c.keyboard?.shiftBackExact === true &&
      c.reflow320?.ok === true && c.zoomCSS200?.ok === true &&
      result.console.consoleErrors === 0 && result.console.runtimeErrors === 0 && result.console.fetchErrors === 0 &&
      result.network.blockedExternal === 0 &&
      errors.length === 0 && cdpErrors.length === 0;
    result.ok = allOk;
    result.criticalOk = allOk;
  } catch (e) {
    note('principal', e);
    result.ok = false;
    result.criticalOk = false;
  } finally {
    result.errors = errors;
    result.cdpErrors = [...cdpErrors];
    result.pid = childPid ?? child?.pid ?? result.pid ?? null;
    result.stderr = stderrHead.slice(0, 2000);
    result.http = { errors: httpErrors.length, sample: [...httpErrors].slice(0, 5) };
    result.network = { allowed: allowedCount, blockedExternal: blockedCount, blockedSample: [...blockedSample] };
    result.console = { consoleErrors: consoleErrors.length, runtimeErrors: runtimeErrors.length, fetchErrors: fetchErrors.length, sample: [...consoleErrors, ...runtimeErrors, ...fetchErrors].slice(0, 5) };
    try {
      result.cleanup = await cleanup();
    } catch (e) {
      result.cleanup = { error: e?.message ?? String(e) };
    }
    // Verdict final APRES finally : cleanup et dernieres erreurs exiges.
    const cl = result.cleanup ?? {};
    const cleanOk = cl.profileRemoved === true && cl.processClosed === true && (cl.cleanupErrors ?? []).length === 0;
    if (!cleanOk) { result.ok = false; result.criticalOk = false; }
    if (result.console.runtimeErrors !== 0 || result.console.fetchErrors !== 0) { result.ok = false; result.criticalOk = false; }
    console.log(JSON.stringify(result));
    if (!result.ok) process.exitCode = 1;
  }
}

await main();
