// Session privée du shell : contexte vérifié, époques et transport WEB uniquement.
import { validateScope, validateSnapshot, validateShellContext, validateTransportResolver, defaultTransportResolver } from './api-v1.js';

const NUL = String.fromCharCode(0);
const SAME_KEYS = ['scope_type', 'tenant_id', 'scope_id'];
const UUID7 = /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;

export class SessionRuntimeError extends Error {
  constructor(code, options) { super(code, options); this.name = 'SessionRuntimeError'; this.code = code; }
}
const fail = (code, cause) => { throw new SessionRuntimeError(code, cause === undefined ? undefined : { cause }); };
function fields(value, required, optional = []) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) fail('SESSION_SHAPE_INVALID');
  if (![Object.prototype, null].includes(Object.getPrototypeOf(value))) fail('SESSION_SHAPE_INVALID');
  const names = Reflect.ownKeys(value);
  if (names.some(name => typeof name !== 'string' || !required.includes(name) && !optional.includes(name))) fail('SESSION_SHAPE_INVALID');
  for (const name of [...required, ...optional]) {
    const descriptor = Object.getOwnPropertyDescriptor(value, name);
    if (!descriptor) { if (required.includes(name)) fail('SESSION_SHAPE_INVALID'); else continue; }
    if (!Object.hasOwn(descriptor, 'value')) fail('SESSION_SHAPE_INVALID');
  }
  return value;
}
function text(value, code) {
  if (typeof value !== 'string' || !value || value.includes(NUL) || value.includes(String.fromCharCode(10)) || value.includes(String.fromCharCode(13))) fail(code);
  try { encodeURIComponent(value); } catch (cause) { fail(code, cause); }
  return value;
}
function clone(value, active = new Set()) {
  if (value === null || ['string', 'boolean'].includes(typeof value)) return value;
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value !== 'object' || active.has(value)) fail('SESSION_JSON_INVALID');
  active.add(value);
  const array = Array.isArray(value);
  if (![array ? Array.prototype : Object.prototype, ...(array ? [] : [null])].includes(Object.getPrototypeOf(value))) fail('SESSION_JSON_INVALID');
  const keys = Reflect.ownKeys(value).filter(key => !(array && key === 'length'));
  if (array && keys.length !== value.length) fail('SESSION_JSON_INVALID');
  const result = array ? [] : {};
  for (let index = 0; index < keys.length; index += 1) {
    const key = array ? String(index) : keys[index];
    if (typeof key !== 'string' || ['__proto__', 'constructor', 'prototype'].includes(key)) fail('SESSION_JSON_INVALID');
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail('SESSION_JSON_INVALID');
    Object.defineProperty(result, key, { value: clone(descriptor.value, active), enumerable: true });
  }
  active.delete(value);
  return Object.freeze(result);
}
const sameScope = (a, b) => SAME_KEYS.every(key => a[key] === b[key]);
function base(scope) {
  const checked = validateScope(scope);
  if (checked.scope_type === 'PLATFORM') return '/api/v1/web/platform';
  const segment = value => {
    if (typeof value !== 'string' || !value || value.includes(NUL)) fail('SESSION_SCOPE_INVALID');
    try { encodeURIComponent(value); } catch (cause) { fail('SESSION_SCOPE_INVALID', cause); }
    if (value === '.' || value === '..') fail('SESSION_SCOPE_INVALID');
    return encodeURIComponent(value);
  };
  return '/api/v1/web/tenants/' + segment(checked.tenant_id)
    + (checked.scope_id === null ? '' : '/scopes/' + segment(checked.scope_id));
}
function queryString(params) {
  if (params === undefined) return '';
  if (params === null || typeof params !== 'object' || Array.isArray(params)) fail('SESSION_QUERY_INVALID');
  fields(params, [], Object.keys(params));
  const output = new URLSearchParams();
  for (const key of Object.keys(params)) {
    const values = Array.isArray(params[key]) ? params[key] : [params[key]];
    for (const value of values) {
      if (typeof value !== 'string' && typeof value !== 'boolean'
          && !(typeof value === 'number' && Number.isSafeInteger(value))) fail('SESSION_QUERY_INVALID');
      if (typeof value === 'string') {
        if (value.includes(NUL)) fail('SESSION_QUERY_INVALID');
        try { encodeURIComponent(value); } catch (cause) { fail('SESSION_QUERY_INVALID', cause); }
      }
      output.append(key, String(value));
    }
  }
  const encoded = output.toString();
  return encoded ? '?' + encoded : '';
}

export function createSessionRuntime(options) {
  const names = ['fetchImpl', 'origin', 'clock', 'createId', 'fingerprint', 'channel', 'getLocale'];
  const checkedOptions = fields(options, names);
  const p = Object.freeze(Object.fromEntries(names.map(name => [name, Object.getOwnPropertyDescriptor(checkedOptions, name).value])));
  for (const name of ['fetchImpl', 'createId', 'fingerprint', 'getLocale']) if (typeof p[name] !== 'function') fail('SESSION_OPTIONS_INVALID');
  const clockNames = ['now', 'setTimeout', 'clearTimeout'];
  const checkedClock = fields(p.clock, clockNames);
  const clock = Object.freeze(Object.fromEntries(clockNames.map(name => [name, Object.getOwnPropertyDescriptor(checkedClock, name).value])));
  if (Object.values(clock).some(value => typeof value !== 'function')) fail('SESSION_OPTIONS_INVALID');
  let origin;
  try { origin = new URL(p.origin); } catch (cause) { fail('SESSION_ORIGIN_INVALID', cause); }
  if (!['http:', 'https:'].includes(origin.protocol) || origin.username || origin.password || origin.search || origin.hash || origin.pathname !== '/') fail('SESSION_ORIGIN_INVALID');
  if (p.channel !== null && ['postMessage', 'addEventListener', 'removeEventListener', 'close'].some(name => typeof p.channel?.[name] !== 'function')) fail('SESSION_OPTIONS_INVALID');
  let epoch = 0;
  let state = validateShellContext({ state: 'ANONYMOUS', epoch, scope: null });
  let resolver = defaultTransportResolver();
  let targetScope = null;
  let online = true;
  let disposed = false;
  let csrf = null;
  let auth = Object.freeze({ phase: 'IDLE' });
  let pendingAuth = null;
  let activeAuth = null;
  let expiry = null;
  const controllers = new Set(), timers = new Set(), listeners = new Set();
  const now = () => {
    const value = clock.now();
    if (!Number.isSafeInteger(value) || value < 0) fail('SESSION_CLOCK_INVALID');
    return value;
  };
  const id = () => {
    const value = text(p.createId(), 'SESSION_CORRELATION_INVALID');
    if (value.length > 128) fail('SESSION_CORRELATION_INVALID');
    return value;
  };
  const notify = (kind, previous = state) => {
    const event = Object.freeze({ kind, previous, current: state });
    for (const listener of [...listeners]) listener(event);
  };
  const tick = () => {
    if (epoch === Number.MAX_SAFE_INTEGER) fail('SESSION_EPOCH_EXHAUSTED');
    return ++epoch;
  };
  const cancel = token => { if (token !== null) { clock.clearTimeout(token); timers.delete(token); } };
  const schedule = (callback, delay) => {
    let token;
    token = clock.setTimeout(() => { timers.delete(token); if (!disposed) callback(); }, delay);
    timers.add(token);
    return token;
  };
  const abort = () => { for (const controller of controllers) controller.abort(); controllers.clear(); };
  const current = snapshot => {
    try {
      const checked = validateSnapshot(snapshot);
      return !disposed && state.state === 'ACTIVE' && checked.epoch === epoch && sameScope(checked.scope, state.scope);
    } catch { return false; }
  };
  let channelAvailable = p.channel !== null;
  const signal = type => {
    if (!channelAvailable) return;
    try { p.channel.postMessage(Object.freeze({ type })); }
    catch (cause) {
      channelAvailable = false;
      notify('CHANNEL_ERROR');
      fail('SESSION_CHANNEL_UNAVAILABLE', cause);
    }
  };
  function reset(nextState, kind = 'CONTEXT', broadcast = false) {
    const previous = state;
    tick(); abort(); cancel(expiry); expiry = null; csrf = null;
    state = validateShellContext({ state: nextState, epoch, scope: null });
    resolver = defaultTransportResolver();
    if (broadcast) signal('AUTH_INVALIDATE');
    notify(kind, previous);
  }
  function armExpiry() {
    cancel(expiry);
    const deadline = Date.parse(state.expires_at);
    const remaining = deadline - now();
    if (remaining <= 0) { reset('EXPIRED'); return; }
    expiry = schedule(() => {
      expiry = null;
      if (state.state === 'ACTIVE') armExpiry();
    }, Math.min(remaining, 2147483647));
  }
  const requireTransport = () => {
    if (disposed) fail('SESSION_DISPOSED');
    if (origin.protocol !== 'https:') fail('SESSION_TRANSPORT_REQUIRED');
    if (!online) fail('SESSION_OFFLINE');
  };
  const pathOf = value => {
    if (typeof value !== 'string' || !value.startsWith('/api/v1/web/') || value.includes(NUL)) fail('SESSION_PATH_INVALID');
    const url = new URL(value, origin.origin);
    if (url.origin !== origin.origin || url.hash || value !== url.pathname + url.search) fail('SESSION_PATH_INVALID');
    return url.pathname + url.search;
  };
  async function request(method, path, expectedScope, body, key, csrfValue, expectedSession) {
    requireTransport();
    const correlation = id(), locale = p.getLocale();
    if (!['en', 'fr'].includes(locale)) fail('SESSION_LOCALE_INVALID');
    const headers = { 'Accept-Language': locale, 'X-Correlation-ID': correlation };
    if (expectedSession !== undefined) headers['X-Shell-Session-ID'] = expectedSession;
    if (method === 'POST') {
      headers['Content-Type'] = 'application/json';
      headers['Idempotency-Key'] = text(key, 'SESSION_IDEMPOTENCY_REQUIRED');
      headers['X-CSRFToken'] = text(csrfValue, 'SESSION_CSRF_INVALID');
    }
    const controller = new AbortController(); controllers.add(controller);
    try {
      const response = await p.fetchImpl(origin.origin + pathOf(path), {
        method, headers, credentials: 'same-origin', cache: 'no-store', redirect: 'error',
        signal: controller.signal, ...(method === 'POST' ? { body: JSON.stringify(body) } : {}),
      });
      if (!Number.isInteger(response.status) || response.status < 100 || response.status > 599) fail('SESSION_RESPONSE_INVALID');
      let result;
      try { result = clone(await response.json()); } catch (cause) { fail('SESSION_RESPONSE_INVALID', cause); }
      if (response.status === 200 || response.status === 202) {
        fields(result, ['data', 'meta', 'links']);
        if (result.meta === null || typeof result.meta !== 'object' || Array.isArray(result.meta)) fail('SESSION_RESPONSE_INVALID');
        fields(result.meta, ['correlation_id', 'context'], Object.keys(result.meta).filter(name => !['correlation_id', 'context'].includes(name)));
        if (result.meta.correlation_id !== correlation || !sameScope(validateScope(result.meta.context), expectedScope)) fail('SESSION_RESPONSE_INVALID');
        if (result.links === null || typeof result.links !== 'object' || Array.isArray(result.links)) fail('SESSION_RESPONSE_INVALID');
      } else if (response.status >= 400) {
        fields(result, ['error_code', 'message', 'details', 'correlation_id'], ['field_errors']);
        if (typeof result.error_code !== 'string' || !result.error_code || typeof result.message !== 'string' || result.correlation_id !== correlation) fail('SESSION_RESPONSE_INVALID');
      } else fail('SESSION_RESPONSE_INVALID');
      return Object.freeze({ status: response.status, body: result });
    } catch (cause) {
      if (cause instanceof SessionRuntimeError) throw cause;
      fail('SESSION_NETWORK_FAILED', cause);
    } finally { controllers.delete(controller); }
  }
  async function csrfToken(generation) {
    if (csrf !== null) return csrf;
    const response = await request('GET', '/api/v1/web/auth/csrf',
      { scope_type: 'PLATFORM', tenant_id: null, scope_id: null });
    if (generation !== epoch) fail('SESSION_SNAPSHOT_STALE');
    if (response.status !== 200) fail('SESSION_CSRF_FAILED');
    fields(response.body.data, ['csrf_token']);
    csrf = text(response.body.data.csrf_token, 'SESSION_CSRF_INVALID');
    return csrf;
  }
  function invalidateScope(broadcast = true) {
    if (disposed) fail('SESSION_DISPOSED');
    if (state.state !== 'ACTIVE') return state;
    const previous = state;
    state = validateShellContext({ ...state, epoch: tick() });
    abort();
    if (broadcast) signal('DATA_INVALIDATE');
    notify('DATA', previous);
    return state;
  }
  function processRejection(response, snapshot) {
    if (response.status === 401 || response.body?.error_code?.endsWith('.CONTEXT_MISMATCH')) schedule(() => { if (current(snapshot)) reset('ANONYMOUS'); }, 0);
    else if (response.status === 403) {
      schedule(() => { if (current(snapshot)) invalidateScope(); }, 0);
    }
  }
  async function fetchJson(path, options) {
    fields(options, ['snapshot', 'params']);
    const snapshot = validateSnapshot(options.snapshot);
    if (!current(snapshot)) fail('SESSION_SNAPSHOT_STALE');
    const session = state.session_id;
    if (typeof path !== 'string' || path.includes('?')) fail('SESSION_PATH_INVALID');
    const response = await request('GET', path + queryString(options.params), snapshot.scope, undefined, undefined, undefined, session);
    if (!current(snapshot)) fail('SESSION_SNAPSHOT_STALE');
    processRejection(response, snapshot);
    return response;
  }
  async function postJson(path, body, options) {
    fields(options, ['snapshot', 'idempotencyKey']);
    const snapshot = validateSnapshot(options.snapshot);
    if (!current(snapshot)) fail('SESSION_SNAPSHOT_STALE');
    const session = state.session_id;
    const token = await csrfToken(snapshot.epoch);
    if (!current(snapshot)) fail('SESSION_SNAPSHOT_STALE');
    const response = await request('POST', path, snapshot.scope, clone(body), options.idempotencyKey, token, session);
    if (!current(snapshot)) fail('SESSION_SNAPSHOT_STALE');
    processRejection(response, snapshot);
    return response;
  }
  async function load(scope) {
    if (disposed) fail('SESSION_DISPOSED');
    const candidate = validateScope(scope); const target = base(candidate);
    reset('INITIALIZING');
    targetScope = candidate;
    const generation = epoch;
    try {
      const response = await request('GET', target + '/shell/context', candidate);
      if (generation !== epoch || disposed) fail('SESSION_SNAPSHOT_STALE');
      if (response.status !== 200) {
        reset(response.status === 401 || response.status === 403 ? 'ANONYMOUS' : 'ERROR');
        fail('SESSION_CONTEXT_REFUSED');
      }
      fields(response.body.meta, ['correlation_id', 'context', 'transport_resolver']);
      const data = fields(response.body.data, ['identity_ref', 'scope', 'session_id', 'category', 'facade', 'authentication_time', 'expires_at', 'identity_assurance', 'authentication_assurance', 'ui_permissions']);
      if (!sameScope(validateScope(data.scope), candidate) || data.facade !== 'WEB') fail('SESSION_RESPONSE_INVALID');
      const next = validateShellContext({ ...data, state: 'ACTIVE', epoch, scope: candidate });
      if (!(Date.parse(next.authentication_time) <= now() && now() < Date.parse(next.expires_at))) fail('SESSION_CONTEXT_EXPIRED');
      const nextResolver = validateTransportResolver(response.body.meta.transport_resolver);
      const previous = state;
      resolver = nextResolver; state = next;
      armExpiry(); notify('CONTEXT', previous);
      return state;
    } catch (cause) {
      if (generation === epoch && !disposed) reset('ERROR');
      throw cause;
    }
  }
  async function mutateAuth(kind, scope, body) {
    requireTransport();
    if (auth.phase === 'PENDING') fail('SESSION_AUTH_PENDING');
    const target = validateScope(scope), route = base(target);
    const priorSession = kind === 'logout' ? (pendingAuth?.session ?? (state.state === 'ACTIVE' ? state.session_id : undefined)) : undefined;
    if (kind === 'logout' && priorSession === undefined) fail('SESSION_NOT_ACTIVE');
    const serialized = JSON.stringify(body);
    const digest = await p.fingerprint(JSON.stringify({ kind, scope: target, body: serialized, ...(priorSession === undefined ? {} : { session: priorSession }) }));
    if (disposed) fail('SESSION_DISPOSED');
    if (auth.phase === 'PENDING') fail('SESSION_AUTH_PENDING');
    if (typeof digest !== 'string' || !/^[0-9a-f]{64}$/.test(digest)) fail('SESSION_FINGERPRINT_INVALID');
    if (pendingAuth !== null && pendingAuth.digest !== digest) fail('SESSION_RETRY_MISMATCH');
    const key = pendingAuth === null ? id() : pendingAuth.key;
    const marker = {};
    activeAuth = marker;
    reset('INITIALIZING', 'AUTH', true);
    targetScope = target;
    const generation = epoch;
    auth = Object.freeze({ phase: 'PENDING' }); notify('AUTH');
    let sent = false;
    try {
      const token = await csrfToken(generation);
      if (generation !== epoch) fail('SESSION_SNAPSHOT_STALE');
      sent = true;
      const response = await request('POST', route + '/auth/' + kind, target, body, key, token,
        kind === 'logout' ? priorSession : undefined);
      if (generation !== epoch || disposed) fail('SESSION_SNAPSHOT_STALE');
      if (response.status === 200) {
        const outcome = response.body.data?.outcome;
        if (kind === 'login' && outcome === 'ISSUED') {
          activeAuth = null; pendingAuth = null; auth = Object.freeze({ phase: 'CONFIRMED' }); signal('AUTH_INVALIDATE');
          await load(target);
          notify('AUTH'); return auth;
        }
        if (kind === 'logout' && ['WITHDRAWN', 'WITHDRAWN_AUDIT_PENDING'].includes(outcome)) {
          activeAuth = null; pendingAuth = null; auth = Object.freeze({ phase: 'CONFIRMED', ...(outcome === 'WITHDRAWN_AUDIT_PENDING' ? { error_code: 'SESSION_AUDIT_PENDING' } : {}) });
          reset('ANONYMOUS', 'AUTH', true); return auth;
        }
        fail('SESSION_AUTH_UNKNOWN');
      }
      if (response.status >= 400 && response.status < 500 && pendingAuth !== null) {
        activeAuth = null;
        auth = Object.freeze({ phase: 'UNKNOWN', error_code: response.body.error_code });
        reset('ERROR', 'AUTH'); return auth;
      }
      if (response.status >= 400 && response.status < 500) {
        activeAuth = null; pendingAuth = null;
        auth = Object.freeze({ phase: 'REJECTED', error_code: response.body.error_code });
        reset('ANONYMOUS', 'AUTH'); return auth;
      }
      fail('SESSION_AUTH_UNKNOWN');
    } catch (cause) {
      if (activeAuth === marker && !disposed) {
        activeAuth = null;
        if (sent) pendingAuth = Object.freeze({ key, digest, ...(priorSession === undefined ? {} : { session: priorSession }) });
        auth = Object.freeze({ phase: sent || pendingAuth !== null ? 'UNKNOWN' : 'REJECTED', error_code: cause instanceof SessionRuntimeError ? cause.code : 'SESSION_NETWORK_FAILED' });
        if (generation === epoch) reset('ERROR', 'AUTH');
        else notify('AUTH');
      }
      throw cause;
    }
  }
  function login(scope, credentials) {
    const input = fields(credentials, ['external_subject', 'password'], ['replace_session_id']);
    if (typeof input.external_subject !== 'string' || !input.external_subject || input.external_subject.includes(NUL)) fail('SESSION_CREDENTIALS_INVALID');
    if (typeof input.password !== 'string' || !input.password) fail('SESSION_CREDENTIALS_INVALID');
    if (input.replace_session_id !== undefined && (typeof input.replace_session_id !== 'string' || !UUID7.test(input.replace_session_id))) fail('SESSION_CREDENTIALS_INVALID');
    return mutateAuth('login', scope, clone(input));
  }
  function logout() {
    if (targetScope === null && state.state !== 'ACTIVE') fail('SESSION_NOT_ACTIVE');
    return mutateAuth('logout', state.state === 'ACTIVE' ? state.scope : targetScope, {});
  }
  function onMessage(event) {
    const message = event.data;
    if (message === null || typeof message !== 'object' || Array.isArray(message)
        || Reflect.ownKeys(message).length !== 1) return;
    const descriptor = Object.getOwnPropertyDescriptor(message, 'type');
    if (!descriptor || !Object.hasOwn(descriptor, 'value')) return;
    if (descriptor.value === 'AUTH_INVALIDATE') reset('ANONYMOUS');
    else if (descriptor.value === 'DATA_INVALIDATE') invalidateScope(false);
  }
  if (p.channel !== null) p.channel.addEventListener('message', onMessage);
  return Object.freeze({
    getState: () => state, getResolver: () => resolver, getTargetScope: () => targetScope,
    getConnectionState: () => Object.freeze({ online, crossTab: channelAvailable ? 'AVAILABLE' : 'UNAVAILABLE', transport: origin.protocol === 'https:' ? 'HTTPS' : 'HTTP_BLOCKED' }),
    getAuthStatus: () => auth,
    getContextSnapshot: () => { if (state.state !== 'ACTIVE') fail('SESSION_NOT_ACTIVE'); return validateSnapshot({ scope: state.scope, epoch }); },
    isCurrentSnapshot: current,
    subscribe: listener => { if (typeof listener !== 'function') fail('SESSION_LISTENER_INVALID'); listeners.add(listener); return () => listeners.delete(listener); },
    load, login, logout, invalidateScope, fetchJson, postJson,
    setOnline: value => {
      if (disposed) fail('SESSION_DISPOSED');
      if (typeof value !== 'boolean') fail('SESSION_ONLINE_INVALID');
      online = value;
      if (!value) reset('ERROR', 'NETWORK');
      else notify('NETWORK');
    },
    dispose: () => {
      if (disposed) return;
      const errors = [];
      try { reset('ANONYMOUS'); } catch (cause) { errors.push(cause); }
      disposed = true; activeAuth = null; pendingAuth = null; csrf = null; targetScope = null;
      for (const token of [...timers]) { try { cancel(token); } catch (cause) { errors.push(cause); } }
      listeners.clear();
      if (p.channel !== null) {
        try { p.channel.removeEventListener('message', onMessage); } catch (cause) { errors.push(cause); }
        try { p.channel.close(); } catch (cause) { errors.push(cause); }
      }
      if (errors.length) fail('SESSION_DISPOSE_FAILED', new AggregateError(errors));
    },
  });
}
