// Recette du bundle C14 : CDP Chromium / WebDriver BiDi Firefox, sans transport simulé.
// Références : developer.mozilla.org/en-US/docs/Web/WebDriver/How_to/Create_BiDi_connection
// et /Reference/BiDi/Modules/session/new ; certificats acceptés dans le seul profil jetable.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const NAMES = ['real_renderer_pzt', 'real_renderer_dns', 'real_http_confirmed_mutations',
  'unknown_unmeasured_honest', 'list_record_lf_order_duplicates', 'retirement_visible',
  'locales_fr_en', 'no_console_errors'];
const cases = Object.fromEntries(NAMES.map(name => [name, false]));
const [engine, origin] = process.argv.slice(2);
const deadline = Date.now() + 90000;
let child, closed, rpc, directory, evaluate, navigate, cleanup = false, consoleErrors = 0;
let phase = 'INPUT', diagnostic = null;
const runtimeCodes = [];
function check(condition) { if (!condition) throw new Error('C14_BROWSER_CHECK_FAILED'); }
async function until(predicate, cap = 10000) {
  const end = Math.min(deadline, Date.now() + cap);
  while (Date.now() < end) {
    const result = await predicate();
    if (result) return result;
    await new Promise(resolve => setTimeout(resolve, 50));
  }
  throw new Error('C14_BROWSER_DEADLINE');
}
async function readInput() {
  let raw = '';
  for await (const chunk of process.stdin) {
    raw += chunk;
    check(Buffer.byteLength(raw) <= 65536);
  }
  return JSON.parse(raw);
}
class Rpc {
  constructor(socket) {
    this.socket = socket; this.next = 0; this.pending = new Map(); this.listeners = [];
    socket.addEventListener('message', event => {
      let message;
      try { message = JSON.parse(String(event.data)); }
      catch { this.rejectAll(); return; }
      if (Number.isSafeInteger(message.id)) {
        const item = this.pending.get(message.id);
        if (!item) return;
        this.pending.delete(message.id); clearTimeout(item.timer);
        if (message.error) item.reject(new Error('C14_BROWSER_PROTOCOL_REFUSED'));
        else item.resolve(message.result);
      } else {
        for (const listener of this.listeners) listener(message);
      }
    });
    socket.addEventListener('close', () => this.rejectAll());
    socket.addEventListener('error', () => this.rejectAll());
  }
  rejectAll() {
    for (const item of this.pending.values()) {
      clearTimeout(item.timer); item.reject(new Error('C14_BROWSER_CONNECTION_CLOSED'));
    }
    this.pending.clear();
  }
  send(method, params = {}, sessionId) {
    const id = ++this.next;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id); reject(new Error('C14_BROWSER_RPC_DEADLINE'));
      }, Math.max(1, Math.min(['Runtime.evaluate','script.evaluate'].includes(method) ? 45000 : ['Page.navigate','browsingContext.navigate'].includes(method) ? 30000 : 12000, deadline - Date.now())));
      this.pending.set(id, { resolve, reject, timer });
      this.socket.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));
    });
  }
  close() { this.rejectAll(); this.socket.close(); }
}
async function connect(url) {
  const parsed = new URL(url);
  check(parsed.protocol === 'ws:' && parsed.hostname === '127.0.0.1');
  const socket = new WebSocket(url);
  await new Promise((resolve, reject) => {
    const timer = setTimeout(() => { socket.close(); reject(new Error('C14_WS_DEADLINE')); }, 5000);
    socket.addEventListener('open', () => { clearTimeout(timer); resolve(); }, { once: true });
    socket.addEventListener('error', () => { clearTimeout(timer); reject(new Error('C14_WS_REFUSED')); }, { once: true });
  });
  return new Rpc(socket);
}

async function domRecipe(v, owner) {
  const wait = async predicate => {
    const end = Date.now() + 8000;
    while (Date.now() < end) {
      if (predicate()) return;
      await new Promise(resolve => setTimeout(resolve, 25));
    }
    throw new Error('C14_DOM_DEADLINE');
  };
  const assert = value => { if (!value) throw new Error('C14_DOM_ASSERTION'); };
  const body = () => document.body.textContent;
  const scalar = (input, value) => {
    assert(input && !input.disabled);
    if (input.type === 'checkbox') { if (input.checked !== value) input.click(); }
    else {
      const proto = input.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
      Object.getOwnPropertyDescriptor(proto, 'value').set.call(input, String(value));
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
    }
  };
  const formWith = name => document.querySelector('input[name="' + name + '"]')?.form;
  const listValues = root => [...root.querySelectorAll('[data-pixs-row]')].map(row => {
    const fields = [...row.querySelectorAll('textarea')];
    return fields.length === 1 && fields[0].dataset.column === 'value'
      ? fields[0].value : Object.fromEntries(fields.map(input => [input.dataset.column, input.value]));
  });
  const fill = async (form, name, value) => {
    assert(form);
    if (Array.isArray(value)) {
      const root = form.querySelector('[data-pixs-list="' + name + '"]'); assert(root);
      while (root.querySelectorAll('[data-pixs-row]').length < value.length) {
        const before = root.querySelectorAll('[data-pixs-row]').length;
        const add = root.querySelector('[data-pixs-add]'); assert(add && !add.disabled); add.click();
        await wait(() => root.querySelectorAll('[data-pixs-row]').length === before + 1);
      }
      assert(root.querySelectorAll('[data-pixs-row]').length === value.length);
      const rows = [...root.querySelectorAll('[data-pixs-row]')];
      for (let index = 0; index < rows.length; index++) {
        const record = typeof value[index] === 'string' ? { value: value[index] } : value[index];
        for (const [column, text] of Object.entries(record)) {
          scalar(rows[index].querySelector('textarea[data-column="' + column + '"]'), text);
        }
      }
      await wait(() => JSON.stringify(listValues(root)) === JSON.stringify(value));
    } else scalar(form.querySelector('input[name="' + name + '"]'), value);
  };
  const setLocale = async locale => {
    const select = [...document.querySelectorAll('select')]
      .find(element => [...element.options].some(option => option.value === 'en')
        && [...element.options].some(option => option.value === 'fr'));
    assert(select);
    Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value').set.call(select, locale);
    select.dispatchEvent(new Event('change', { bubbles: true }));
    await wait(() => select.value === locale && (owner === 'pzt'
      ? body().includes(locale === 'fr' ? 'Gestion réseau PZT' : 'PZT network management')
      : body().includes(locale === 'fr' ? 'Gestion DNS' : 'DNS management')));
  };
  const profile = v[owner + '_ref'], configuration = v[owner + '_configuration'];
  await wait(() => formWith('resource_id'));
  assert(isSecureContext && location.origin === v.origin);
  const expectedTitle = owner === 'pzt' ? 'PZT network management' : 'DNS management';
  await setLocale('en');
  assert([...document.querySelectorAll('h1,h2')].some(node => node.textContent === expectedTitle));
  await setLocale('fr'); await setLocale('en');
  const result = { renderer: true, confirmed: false, observation: false, records: false, retired: false, locales: true };
  const create = formWith('resource_id');
  await fill(create, 'resource_id', profile);
  for (const name of owner === 'pzt' ? ['v6_enabled', 'plan_ref', 'budget_ref'] : ['suffix', 'ttl_positive', 'ttl_negative', 'views']) {
    await fill(create, name, configuration[name]);
  }
  for (const [name, value] of Object.entries(configuration.governance)) {
    if (name !== 'owner_component') await fill(create, 'gov_' + name, value);
  }
  await fill(create, 'secret_refs', configuration.secret_refs);
  assert(create.checkValidity());
  create.requestSubmit();
  await wait(() => document.querySelector('[data-command-state="CONFIRMED"]'));
  const reload = async () => {
    const form = formWith('profile_ref'); assert(form);
    await fill(form, 'profile_ref', profile); form.requestSubmit();
    await wait(() => document.querySelector('[data-query-state="LOADED"]')
      && document.querySelector('form [data-pixs-list="secret_refs"]'));
  };
  await reload();
  await wait(() => body().includes('Desired configuration is declared.'));
  const editors = [...document.querySelectorAll('form [data-pixs-list="secret_refs"]')];
  assert(editors.length === 1);
  assert(JSON.stringify(listValues(editors[0])) === JSON.stringify(configuration.secret_refs));
  assert(configuration.secret_refs.length === 3
    && configuration.secret_refs[0].source.includes('\n')
    && JSON.stringify(configuration.secret_refs[0]) === JSON.stringify(configuration.secret_refs[2])
    && configuration.secret_refs[0].entry_id !== configuration.secret_refs[1].entry_id);
  result.records = true;
  const observed = [...document.querySelectorAll('button')].find(button => button.textContent === 'Read observed state');
  assert(observed && !observed.disabled); observed.click();
  await wait(() => body().includes('Applied state is unknown; measurements are unavailable.'));
  result.observation = true;
  const retire = formWith('reason'); assert(retire);
  await fill(retire, 'reason', 'Retrait explicite de recette navigateur');
  retire.requestSubmit();
  await wait(() => body().includes('The change is confirmed. Reload the desired configuration before another mutation.'));
  await reload();
  await wait(() => body().includes('Desired configuration is retired.'));
  assert([...document.querySelectorAll('button')].some(button => button.textContent === 'Declare the desired configuration again'));
  result.confirmed = true; result.retired = true;
  return result;
}

try {
  check(['chromium', 'firefox'].includes(engine));
  const parsed = new URL(origin);
  check(parsed.protocol === 'https:' && parsed.hostname === '127.0.0.1' && parsed.port
    && parsed.origin === origin && !parsed.username && !parsed.password);
  const vectors = await readInput();
  check(vectors.origin === origin && typeof vectors.pzt_ref === 'string' && typeof vectors.dns_ref === 'string');
  const cache = path.resolve('frontend/.cache');
  check(typeof vectors.browser_directory === 'string');
  directory = path.resolve(vectors.browser_directory);
  check(path.dirname(directory) === cache && /^c4-[cf]-[A-Za-z0-9_-]+$/.test(path.basename(directory))
    && fs.realpathSync(directory) === directory && fs.lstatSync(directory).isDirectory()
    && fs.readdirSync(directory).length === 0);
  const publicVectors = { origin: vectors.origin, pzt_ref: vectors.pzt_ref, dns_ref: vectors.dns_ref,
    pzt_configuration: vectors.pzt_configuration, dns_configuration: vectors.dns_configuration };
  const dirs = Object.fromEntries(['profile', 'home', 'tmp', 'cache', 'config', 'data'].map(name => {
    const names = {profile:'p',home:'h',tmp:'t',cache:'c',config:'g',data:'u'};
    const value = path.join(directory, names[name]); fs.mkdirSync(value, { mode: 0o700 }); return [name, value];
  }));
  const env = { PATH: '/usr/bin:/bin', LANG: 'C.UTF-8', HOME: dirs.home, TMPDIR: dirs.tmp,
    XDG_CACHE_HOME: dirs.cache, XDG_CONFIG_HOME: dirs.config, XDG_DATA_HOME: dirs.data };
  const args = engine === 'chromium'
    ? ['--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--disable-crash-reporter',
      '--disable-background-networking', '--ignore-certificate-errors', '--remote-debugging-address=127.0.0.1',
      '--remote-debugging-port=0', '--user-data-dir=' + dirs.profile, 'about:blank']
    : ['-headless', '-no-remote', '-profile', dirs.profile, '--remote-debugging-port=0', 'about:blank'];
  phase = 'SPAWN';
  if (engine === 'chromium' && Buffer.byteLength(path.join(dirs.tmp, 'org.chromium.Chromium.XXXXXX', 'SingletonSocket')) > 107) throw new Error('C14_BROWSER_SOCKET_PATH_TOO_LONG');
  child = spawn('/usr/bin/' + engine, args, { env, stdio: ['ignore', 'pipe', 'pipe'], detached: false });
  closed = new Promise(resolve => { child.once('close', () => resolve(true)); child.once('error', () => resolve(false)); });
  let output = '', observedEndpoint = null;
  const append = chunk => {
    output = (output + String(chunk)).slice(-8192);
    const match = output.match(/ws:\/\/127\.0\.0\.1:\d+(?:\/[^\s]*)?/);
    if (match) observedEndpoint = match[0];
  };
  child.stdout.on('data', append); child.stderr.on('data', append);
  phase = 'ENDPOINT';
  const endpoint = await until(() => {
    return observedEndpoint;
  }, 12000);
  phase = 'CONNECT';
  rpc = await connect(engine === 'firefox' ? endpoint.replace(/\/$/, '') + '/session' : endpoint);

  if (engine === 'chromium') {
    phase = 'CDP_CREATE_TARGET';
    const { targetId } = await rpc.send('Target.createTarget', { url: 'about:blank' });
    phase = 'CDP_ATTACH';
    const { sessionId } = await rpc.send('Target.attachToTarget', { targetId, flatten: true });
    rpc.listeners.push(message => {
      if (message.sessionId === sessionId && (message.method === 'Runtime.exceptionThrown'
          || message.method === 'Log.entryAdded' && message.params.entry.level === 'error')) consoleErrors++;
    });
    phase = 'CDP_ENABLE';
    await rpc.send('Page.enable', {}, sessionId); await rpc.send('Runtime.enable', {}, sessionId);
    await rpc.send('Log.enable', {}, sessionId);
    evaluate = async expression => {
      const result = await rpc.send('Runtime.evaluate', {
        expression: '(async()=>JSON.stringify(await (' + expression + ')))()',
        awaitPromise: true, returnByValue: true,
      }, sessionId);
      check(!result.exceptionDetails && typeof result.result?.value === 'string');
      return JSON.parse(result.result.value);
    };
    navigate = async url => { const result = await rpc.send('Page.navigate', { url }, sessionId); check(!result.errorText); };
  } else {
    phase = 'BIDI_SESSION';
    const session = await rpc.send('session.new', { capabilities: { alwaysMatch: { acceptInsecureCerts: true } } });
    check(session.capabilities.acceptInsecureCerts === true);
    const { context } = await rpc.send('browsingContext.create', { type: 'tab' });
    await rpc.send('session.subscribe', { events: ['log.entryAdded'], contexts: [context] });
    rpc.listeners.push(message => { if (message.method === 'log.entryAdded' && message.params.level === 'error') consoleErrors++; });
    evaluate = async expression => {
      const result = await rpc.send('script.evaluate', {
        expression: '(async()=>JSON.stringify(await (' + expression + ')))()',
        target: { context }, awaitPromise: true,
      });
      check(result.type === 'success' && result.result?.type === 'string');
      return JSON.parse(result.result.value);
    };
    navigate = async url => { await rpc.send('browsingContext.navigate', { context, url, wait: 'complete' }); };
  }
  phase = 'BOOTSTRAP_NAVIGATE';
  await navigate(origin + '/__c14/bootstrap');
  const results = {};
  for (const owner of ['pzt', 'dns']) {
    phase = owner === 'pzt' ? 'DOM_PZT' : 'NAVIGATE_DNS';
    if (owner === 'dns') await navigate(origin + '/platform/dns');
    phase = owner === 'pzt' ? 'DOM_PZT' : 'DOM_DNS';
    await until(() => evaluate('Boolean(document.querySelector("input[name=resource_id]"))'));
    results[owner] = await evaluate('(' + domRecipe.toString() + ')(' + JSON.stringify(publicVectors) + ',' + JSON.stringify(owner) + ')');
    check(Object.values(results[owner]).every(value => value === true));
    cases['real_renderer_' + owner] = results[owner].renderer;
  }
  cases.real_http_confirmed_mutations = results.pzt.confirmed && results.dns.confirmed;
  cases.unknown_unmeasured_honest = results.pzt.observation && results.dns.observation;
  cases.list_record_lf_order_duplicates = results.pzt.records && results.dns.records;
  cases.retirement_visible = results.pzt.retired && results.dns.retired;
  cases.locales_fr_en = results.pzt.locales && results.dns.locales;
  cases.no_console_errors = consoleErrors === 0;
} catch (error) {
  const candidate = typeof error?.message === 'string' ? error.message : '';
  let view = { route: 'UNKNOWN', field_names: [] };
  if (evaluate) {
    try {
      view = await evaluate("({route:location.pathname==='/platform/pzt'?'PZT':location.pathname==='/platform/dns'?'DNS':location.pathname==='/login'?'LOGIN':location.pathname==='/platform'?'PLATFORM':'OTHER',field_names:[...document.querySelectorAll('input[name]')].map(e=>e.name).filter(n=>/^[a-z][a-z0-9_]{0,63}$/.test(n)).slice(0,64)})");
    } catch { /* Le diagnostic secondaire reste facultatif ; l'échec initial est conservé. */ }
  }
  diagnostic = { phase, code: /^C14_[A-Z_]+$/.test(candidate) ? candidate : 'C14_BROWSER_UNEXPECTED',
    route: view.route, field_names: view.field_names, console_errors: Math.min(consoleErrors, 1000), runtime_codes: [...runtimeCodes] };
  // Les diagnostics restent bornés aux critères fermés, sans données de page ni cookies.
} finally {
  if (rpc && child && child.exitCode === null) {
    try { await rpc.send(engine === 'chromium' ? 'Browser.close' : 'browser.close'); }
    catch { /* La fermeture de connexion est attendue ; le parent vérifiera la quiescence. */ }
  }
  if (rpc) rpc.close();
  let stopped = !child;
  if (child) {
    child.kill('SIGTERM');
    stopped = await Promise.race([closed, new Promise(resolve => setTimeout(() => resolve(false), 2500))]);
    if (!stopped) {
      child.kill('SIGKILL');
      stopped = await Promise.race([closed, new Promise(resolve => setTimeout(() => resolve(false), 2500))]);
    }
  }
  if (directory && stopped) fs.rmSync(directory, { recursive: true, force: true });
  cleanup = stopped && (!directory || !fs.existsSync(directory));
}
process.stdout.write(JSON.stringify({ schema: 'pixs.c14.composed.browser/1.0.0', engine, cases, cleanup, diagnostic }) + '\n');
process.exitCode = cleanup && Object.values(cases).every(value => value === true) ? 0 : 1;
