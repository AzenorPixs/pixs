// Doubles explicites : transport/server simulés, sans réseau ni secret.
// Ces fixtures ne qualifient ni C03/C04 ni TLS.
import test from 'node:test';
import assert from 'node:assert/strict';
import { createSessionRuntime } from '../src/shell/session-runtime-v1.js';

const ORIGIN = 'https://app.example/';
const HTTP_ORIGIN = 'http://app.example/';
const SESSION_ID = '0193f2a1-7b3c-7d4e-8a5f-123456789abc';
const PLATFORM = Object.freeze({ scope_type: 'PLATFORM', tenant_id: null, scope_id: null });
const TENANT = Object.freeze({ scope_type: 'TENANT', tenant_id: 'tenant-alpha', scope_id: null });
const FULL = Object.freeze({ scope_type: 'TENANT', tenant_id: 'tenant-alpha', scope_id: 'scope-beta' });

function makeClock(start = 1700000000000) {
  let nowValue = start;
  let nextId = 1;
  const tasks = new Map();
  return {
    now: () => nowValue,
    setTime: (v) => { nowValue = v; },
    advance: (d) => { nowValue += d; },
    pendingCount: () => tasks.size,
    setTimeout: (cb, delay) => { const id = nextId++; tasks.set(id, { cb, at: nowValue + delay, delay }); return id; },
    clearTimeout: (id) => { tasks.delete(id); },
    runDue: () => {
      const due = [...tasks.entries()].filter(([, x]) => x.at <= nowValue).map(([id]) => id);
      for (const id of due) { const x = tasks.get(id); tasks.delete(id); x.cb(); }
    },
  };
}

const clockPort = clock => ({ now: clock.now, setTimeout: clock.setTimeout, clearTimeout: clock.clearTimeout });
const deferred = () => { let resolve; const promise = new Promise(done => { resolve = done; }); return { promise, resolve }; };

function makeChannel() {
  const posted = [];
  const listeners = new Map();
  const channel = {
    posted, listeners, shouldThrow: false, closed: false, removeThrows: false, closeThrows: false,
    postMessage(m) { if (channel.shouldThrow) throw new Error('canal-hs'); posted.push(m); },
    addEventListener(t, fn) { if (!listeners.has(t)) listeners.set(t, []); listeners.get(t).push(fn); },
    removeEventListener(t, fn) {
      if (channel.removeThrows) throw new Error('retrait-hs');
      const a = listeners.get(t) || [];
      const i = a.indexOf(fn);
      if (i >= 0) a.splice(i, 1);
    },
    close() { if (channel.closeThrows) throw new Error('fermeture-hs'); channel.closed = true; },
    emit(msg) { for (const fn of [...(listeners.get('message') || [])]) fn({ data: msg }); },
  };
  return channel;
}

function fingerprintDouble() {
  const known = new Map();
  return async value => {
    if (!known.has(value)) known.set(value, (known.size + 1).toString(16).padStart(64, '0'));
    return known.get(value);
  };
}

function activeData(scope, clock, sessionId = SESSION_ID, extra = {}) {
  return {
    identity_ref: 'ident-1', scope, session_id: sessionId, category: 'compte',
    facade: 'WEB', authentication_time: new Date(clock.now() - 1000).toISOString(),
    expires_at: new Date(clock.now() + 60000).toISOString(),
    identity_assurance: 'VERIFIED', authentication_assurance: 'SINGLE_FACTOR',
    ui_permissions: { status: 'UNAVAILABLE', items: [] }, ...extra,
  };
}

function contextEnvelope(correlation, scope, clock, resolverOps = []) {
  return {
    status: 200,
    body: {
      data: activeData(scope, clock),
      meta: { correlation_id: correlation, context: scope, transport_resolver: { version: '1.0.0', operations: resolverOps } },
      links: {},
    },
  };
}

function makeRuntime({ origin = ORIGIN, handler, channel = null, clock = makeClock(), locale = 'en' } = {}) {
  const fetchCalls = [];
  let counter = 0;
  const fetchImpl = async (url, init) => {
    fetchCalls.push({ url, init });
    return handler({ url, init, calls: fetchCalls });
  };
  const rt = createSessionRuntime({
    fetchImpl, origin, clock: clockPort(clock), channel, getLocale: () => locale,
    createId: () => 'corr-' + (++counter),
    fingerprint: fingerprintDouble(),
  });
  return { rt, clock, fetchCalls, channel };
}

function csrfBody(correlation) {
  return { status: 200, body: { data: { csrf_token: 'jeton-csrf-1' }, meta: { correlation_id: correlation, context: PLATFORM }, links: {} } };
}

async function rejectsCode(fn, code) {
  try { await fn(); } catch (e) { assert.equal(String(e && e.code || e && e.message), code); return; }
  assert.fail('rejet attendu ' + code);
}

function throwsCode(fn, code) {
  try { fn(); } catch (e) { assert.equal(String(e && e.code || e && e.message), code); return; }
  assert.fail('rejet attendu ' + code);
}

test('construction sans reseau et ports fermes sans appel accesseur', () => {
  const clock = makeClock();
  const { rt, fetchCalls } = makeRuntime({ clock, handler: async () => { throw new Error('ne-doit-pas-appeler'); } });
  assert.equal(rt.getState().state, 'ANONYMOUS');
  assert.equal(rt.getTargetScope(), null);
  assert.deepEqual(rt.getAuthStatus(), { phase: 'IDLE' });
  assert.deepEqual(rt.getConnectionState(), { online: true, crossTab: 'UNAVAILABLE', transport: 'HTTPS' });
  assert.equal(fetchCalls.length, 0);
  let getterCalls = 0;
  const bad = { fetchImpl: async () => 0, origin: ORIGIN, clock: clockPort(clock), createId: () => 'x',
    fingerprint: fingerprintDouble(), channel: null, getLocale: () => 'en' };
  Object.defineProperty(bad, 'fetchImpl', { get() { getterCalls += 1; return async () => 0; } });
  throwsCode(() => createSessionRuntime(bad), 'SESSION_SHAPE_INVALID');
  assert.equal(getterCalls, 0);
  throwsCode(() => createSessionRuntime({ fetchImpl: async () => 0, origin: ORIGIN, clock: clockPort(clock), createId: () => 'x', fingerprint: fingerprintDouble(), channel: null, getLocale: () => 'en', extra: 1 }), 'SESSION_SHAPE_INVALID');
  throwsCode(() => createSessionRuntime({ fetchImpl: 'x', origin: ORIGIN, clock: clockPort(clock), createId: () => 'x', fingerprint: fingerprintDouble(), channel: null, getLocale: () => 'en' }), 'SESSION_OPTIONS_INVALID');
  throwsCode(() => createSessionRuntime({ fetchImpl: async () => 0, origin: 'https://app.example/?x=1', clock: clockPort(clock), createId: () => 'x', fingerprint: fingerprintDouble(), channel: null, getLocale: () => 'en' }), 'SESSION_ORIGIN_INVALID');
});

test('origine http bloque transport avant tout envoi reseau', async () => {
  const clock = makeClock();
  const { rt, fetchCalls } = makeRuntime({ origin: HTTP_ORIGIN, clock, handler: async () => { throw new Error('ne-doit-pas-appeler'); } });
  assert.equal(rt.getConnectionState().transport, 'HTTP_BLOCKED');
  await rejectsCode(() => rt.load(PLATFORM), 'SESSION_TRANSPORT_REQUIRED');
  await rejectsCode(() => rt.login(PLATFORM, { external_subject: 'u', password: 'p' }), 'SESSION_TRANSPORT_REQUIRED');
  assert.equal(fetchCalls.length, 0);
});

test('contexte actif verifie scope opaque session et meta separes', async () => {
  const clock = makeClock();
  const scope = Object.freeze({ scope_type: 'TENANT', tenant_id: 'tenant-opaque', scope_id: 'portee/opaque' });
  const { rt } = makeRuntime({
    clock,
    handler: async ({ url, init }) => {
      const correlation = init.headers['X-Correlation-ID'];
      assert.ok(!('X-Shell-Session-ID' in init.headers));
      return { status: 200, json: async () => contextEnvelope(correlation, scope, clock).body };
    },
  });
  const state = await rt.load(scope);
  assert.equal(state.state, 'ACTIVE');
  assert.equal(state.scope.tenant_id, 'tenant-opaque');
  assert.equal(state.session_id, SESSION_ID);
  assert.equal(Object.hasOwn(state, 'transport_resolver'), false);
  assert.equal(state.facade, 'WEB');
  assert.ok(Object.isFrozen(state));
  const snap = rt.getContextSnapshot();
  assert.deepEqual(snap.scope, scope);
  assert.equal(rt.isCurrentSnapshot(snap), true);
  assert.equal(rt.isCurrentSnapshot({ scope, epoch: snap.epoch + 1 }), false);
  const resolver = rt.getResolver();
  assert.equal(resolver.version, '1.0.0');
  assert.ok(Object.isFrozen(resolver));
});

test('correlation meta payload temps session invalides refuses sans partiel', async () => {
  async function loadWith(mutate, code = 'SESSION_RESPONSE_INVALID') {
    const clock = makeClock();
    const { rt } = makeRuntime({
      clock,
      handler: async ({ init }) => {
        const correlation = init.headers['X-Correlation-ID'];
        const good = contextEnvelope(correlation, TENANT, clock).body;
        const bad = mutate({ body: good, correlation, clock });
        return { status: 200, json: async () => bad };
      },
    });
    await rejectsCode(() => rt.load(TENANT), code);
    assert.notEqual(rt.getState().state, 'ACTIVE');
  }
  await loadWith(({ body, correlation }) => ({ ...body, meta: { ...body.meta, correlation_id: correlation + '-x' } }));
  await loadWith(({ body }) => ({ ...body, meta: { ...body.meta, context: PLATFORM } }));
  await loadWith(({ body }) => ({ ...body, data: { ...body.data, facade: 'BEARER' } }));
  await loadWith(({ body, clock }) => ({ ...body, data: { ...body.data, expires_at: new Date(clock.now() - 1).toISOString() } }), 'SESSION_CONTEXT_EXPIRED');
  await loadWith(({ body }) => ({ ...body, data: { ...body.data, session_id: '0193f2a1-7b3c-4d4e-8a5f-123456789abc' } }), 'SHELL_CONTEXT_INVALID');
});

test('liaison proprietaire injectee fige sinon refus sans invention', async () => {
  const clock = makeClock();
  const binding = { kind: 'QUERY', name: 'mes-objets', owner: 'pixs.demo', contractVersion: '1.0.0', scopes: ['T'], segments: ['objets'] };
  const { rt } = makeRuntime({
    clock,
    handler: async ({ init }) => {
      const correlation = init.headers['X-Correlation-ID'];
      return { status: 200, json: async () => contextEnvelope(correlation, TENANT, clock, [binding]).body };
    },
  });
  await rt.load(TENANT);
  assert.deepEqual([...rt.getResolver().operations].pop(), binding);
  const clock2 = makeClock();
  const { rt: rt2 } = makeRuntime({
    clock: clock2,
    handler: async ({ init }) => {
      const correlation = init.headers['X-Correlation-ID'];
      const body = contextEnvelope(correlation, TENANT, clock2, [{ kind: 'QUERY', name: 'x', owner: 'pixs.demo', contractVersion: 'pas-semver', scopes: ['T'], segments: ['x'] }]).body;
      return { status: 200, json: async () => body };
    },
  });
  await rejectsCode(() => rt2.load(TENANT), 'SHELL_ROUTE_INVALID');
  assert.equal(rt2.getResolver().operations.length, 37);
});

test('csrf amorce puis post protege porte session idempotence', async () => {
  const clock = makeClock();
  const env = makeRuntime({ clock, handler: async ({ url, init }) => {
    const correlation = init.headers['X-Correlation-ID'];
    assert.equal(init.credentials, 'same-origin'); assert.equal(init.redirect, 'error');
    assert.equal(init.cache, 'no-store'); assert.equal(Object.hasOwn(init.headers, 'Authorization'), false);
    if (url.endsWith('/shell/context')) {
      assert.equal(Object.hasOwn(init.headers, 'X-Shell-Session-ID'), false);
      return { status: 200, json: async () => contextEnvelope(correlation, FULL, clock).body };
    }
    if (url.endsWith('/auth/csrf')) {
      assert.equal(Object.hasOwn(init.headers, 'X-Shell-Session-ID'), false);
      return { status: 200, json: async () => csrfBody(correlation).body };
    }
    assert.equal(init.headers['X-Shell-Session-ID'], SESSION_ID);
    if (init.method === 'POST') {
      assert.equal(init.headers['Content-Type'], 'application/json');
      assert.equal(init.headers['Idempotency-Key'], 'cle-1');
      assert.equal(init.headers['X-CSRFToken'], 'jeton-csrf-1');
      assert.deepEqual(JSON.parse(init.body), { name: 'g' });
    }
    return { status: 200, json: async () => ({ data: [], meta: { correlation_id: correlation, context: FULL }, links: {} }) };
  } });
  await env.rt.load(FULL);
  const snapshot = env.rt.getContextSnapshot();
  await env.rt.fetchJson('/api/v1/web/tenants/tenant-alpha/scopes/scope-beta/groups', { snapshot, params: {} });
  await env.rt.postJson('/api/v1/web/tenants/tenant-alpha/scopes/scope-beta/commands/create-group', { name: 'g' }, { snapshot, idempotencyKey: 'cle-1' });
  assert.deepEqual(env.fetchCalls.map(call => call.init.method), ['GET', 'GET', 'GET', 'POST']);
  env.rt.dispose();
});
test('params requete gardent ordre doublons encodent scopes invalides refuses', async () => {
  const clock = makeClock();
  const scope = { scope_type: 'TENANT', tenant_id: 'tenant/%' + String.fromCharCode(10), scope_id: 'scope/%' };
  const basePath = '/api/v1/web/tenants/tenant%2F%25%0A/scopes/scope%2F%25';
  let seen;
  const env = makeRuntime({ clock, handler: async ({ url, init }) => {
    seen = url;
    const correlation = init.headers['X-Correlation-ID'];
    return { status: 200, json: async () => url.endsWith('/shell/context')
      ? contextEnvelope(correlation, scope, clock).body
      : { data: [], meta: { correlation_id: correlation, context: scope }, links: {} } };
  } });
  await env.rt.load(scope);
  assert.equal(seen, 'https://app.example' + basePath + '/shell/context');
  const snapshot = env.rt.getContextSnapshot(), values = ['b' + String.fromCharCode(10), 'a', 'b' + String.fromCharCode(10)];
  await env.rt.fetchJson(basePath + '/demo_read', { snapshot, params: { tag: values, flag: true, n: 3 } });
  assert.deepEqual(new URL(seen).searchParams.getAll('tag'), values);
  const before = env.fetchCalls.length;
  await rejectsCode(() => env.rt.fetchJson('/api/v1/web/x?y=1', { snapshot, params: {} }), 'SESSION_PATH_INVALID');
  await rejectsCode(() => env.rt.fetchJson(basePath + '/demo_read', { snapshot, params: { bad: 'a' + String.fromCharCode(0) } }), 'SESSION_QUERY_INVALID');
  assert.equal(env.fetchCalls.length, before);
  env.rt.dispose();
});
test('reponse retardee ignoree epoque changee abort observe', async () => {
  const clock = makeClock(), ready = deferred(), content = deferred();
  let signal;
  const env = makeRuntime({ clock, handler: async ({ url, init }) => {
    const correlation = init.headers['X-Correlation-ID'];
    if (url.endsWith('/shell/context')) return { status: 200, json: async () => contextEnvelope(correlation, TENANT, clock).body };
    signal = init.signal; ready.resolve(correlation);
    return { status: 200, json: async () => content.promise };
  } });
  await env.rt.load(TENANT);
  const snapshot = env.rt.getContextSnapshot();
  const pending = env.rt.fetchJson('/api/v1/web/tenants/tenant-alpha/groups', { snapshot, params: {} });
  const refused = rejectsCode(() => pending, 'SESSION_SNAPSHOT_STALE');
  const correlation = await ready.promise;
  env.rt.invalidateScope();
  assert.equal(signal.aborted, true);
  content.resolve({ data: ['ancienne'], meta: { correlation_id: correlation, context: TENANT }, links: {} });
  await refused;
  const before = env.fetchCalls.length;
  await rejectsCode(() => env.rt.fetchJson('/api/v1/web/tenants/tenant-alpha/groups', { snapshot, params: {} }), 'SESSION_SNAPSHOT_STALE');
  assert.equal(env.fetchCalls.length, before);
  env.rt.dispose();
});
test('expiration serveur purge delai technique sans vrai sommeil', async () => {
  const clock = makeClock(), duration = 2147483647 + 40;
  const env = makeRuntime({ clock, handler: async ({ init }) => {
    const body = contextEnvelope(init.headers['X-Correlation-ID'], TENANT, clock).body;
    body.data.expires_at = new Date(clock.now() + duration).toISOString();
    return { status: 200, json: async () => body };
  } });
  await env.rt.load(TENANT);
  assert.equal(clock.pendingCount(), 1);
  clock.advance(2147483647); clock.runDue();
  assert.equal(env.rt.getState().state, 'ACTIVE'); assert.equal(clock.pendingCount(), 1);
  clock.advance(40); clock.runDue();
  assert.equal(env.rt.getState().state, 'EXPIRED');
  assert.equal(env.rt.getState().scope, null); assert.equal(clock.pendingCount(), 0);
  env.rt.dispose();
});
test('401 mismatch purge differee 403 invalide sans revoque inventee', async () => {
  const clock = makeClock();
  const env = makeRuntime({
    clock,
    handler: async ({ url, init }) => {
      const correlation = init.headers['X-Correlation-ID'];
      if (url.endsWith('/shell/context')) return { status: 200, json: async () => contextEnvelope(correlation, TENANT, clock).body };
      return { status: 401, json: async () => ({ error_code: 'pixs.core.api.v1.CONTEXT_MISMATCH', message: 'ecart', details: {}, correlation_id: correlation }) };
    },
  });
  await env.rt.load(TENANT);
  const s = env.rt.getContextSnapshot();
  const res = await env.rt.fetchJson('/api/v1/web/tenants/tenant-alpha/groups', { snapshot: s, params: {} });
  assert.equal(res.status, 401);
  assert.equal(env.rt.getState().state, 'ACTIVE');
  clock.runDue();
  assert.equal(env.rt.getState().state, 'ANONYMOUS');
  const clock2 = makeClock();
  const env2 = makeRuntime({
    clock: clock2,
    handler: async ({ url, init }) => {
      const correlation = init.headers['X-Correlation-ID'];
      if (url.endsWith('/shell/context')) return { status: 200, json: async () => contextEnvelope(correlation, TENANT, clock2).body };
      return { status: 403, json: async () => ({ error_code: 'REFUS', message: 'non', details: {}, correlation_id: correlation }) };
    },
  });
  await env2.rt.load(TENANT);
  const epochBefore = env2.rt.getContextSnapshot().epoch;
  const s2 = env2.rt.getContextSnapshot();
  await env2.rt.fetchJson('/api/v1/web/tenants/tenant-alpha/groups', { snapshot: s2, params: {} });
  clock2.runDue();
  assert.ok(env2.rt.getContextSnapshot().epoch > epochBefore);
  assert.equal(env2.rt.getState().state, 'ACTIVE');
});

test('hors ligne bloque avant reseau retour ne rejoue rien', async () => {
  const clock = makeClock();
  let calls = 0;
  const env = makeRuntime({
    clock,
    handler: async ({ url, init }) => {
      calls++;
      const correlation = init.headers['X-Correlation-ID'];
      return { status: 200, json: async () => contextEnvelope(correlation, TENANT, clock).body };
    },
  });
  await env.rt.load(TENANT);
  const before = calls;
  env.rt.setOnline(false);
  assert.equal(env.rt.getState().state, 'ERROR');
  await rejectsCode(() => env.rt.load(TENANT), 'SESSION_OFFLINE');
  assert.equal(calls, before);
  env.rt.setOnline(true);
  assert.equal(calls, before);
  assert.equal(env.rt.getState().state, 'ERROR');
});

test('canal ne transporte que invalidation sans secret ignore reste', async () => {
  const clock = makeClock();
  const channel = makeChannel();
  const env = makeRuntime({
    clock, channel,
    handler: async ({ url, init }) => {
      const correlation = init.headers['X-Correlation-ID'];
      return { status: 200, json: async () => contextEnvelope(correlation, TENANT, clock).body };
    },
  });
  await env.rt.load(TENANT);
  env.rt.invalidateScope();
  assert.deepEqual(channel.posted, [{ type: 'DATA_INVALIDATE' }]);
  channel.emit({ type: 'DATA_INVALIDATE' });
  assert.ok(env.rt.getContextSnapshot().epoch >= 1);
  channel.emit({ type: 'AUTH_INVALIDATE' });
  assert.equal(env.rt.getState().state, 'ANONYMOUS');
  const epoch = env.rt.getState().epoch;
  channel.emit(null);
  channel.emit({ type: 'AUTH_INVALIDATE', extra: 1 });
  channel.emit({ type: 'INCONNU' });
  assert.equal(env.rt.getState().epoch, epoch);
  assert.ok(channel.posted.every((m) => Object.keys(m).length === 1 && typeof m.type === 'string'));
  assert.ok(!JSON.stringify(channel.posted).includes('mot-de-passe'));
});

test('panne canal rend indisponible et notifie purge avant propagation', async () => {
  const clock = makeClock();
  const channel = makeChannel();
  const env = makeRuntime({
    clock, channel,
    handler: async ({ url, init }) => {
      const correlation = init.headers['X-Correlation-ID'];
      return { status: 200, json: async () => contextEnvelope(correlation, TENANT, clock).body };
    },
  });
  await env.rt.load(TENANT);
  const kinds = [], snapshot = env.rt.getContextSnapshot();
  env.rt.subscribe((e) => { kinds.push(e.kind); if (e.kind === 'CHANNEL_ERROR') assert.equal(env.rt.isCurrentSnapshot(snapshot), false); });
  channel.shouldThrow = true;
  throwsCode(() => env.rt.invalidateScope(), 'SESSION_CHANNEL_UNAVAILABLE');
  assert.equal(env.rt.getConnectionState().crossTab, 'UNAVAILABLE');
  assert.ok(kinds.includes('CHANNEL_ERROR'));
  env.rt.invalidateScope();
  assert.equal(env.rt.getConnectionState().crossTab, 'UNAVAILABLE');
});

test('connexion emet load verifie puis active sans fuite mot de passe', async () => {
  const clock = makeClock();
  const channel = makeChannel();
  const seen = [];
  const env = makeRuntime({
    clock, channel,
    handler: async ({ url, init }) => {
      const correlation = init.headers['X-Correlation-ID'];
      seen.push({ url, headers: { ...init.headers }, method: init.method, body: init.body });
      if (url.endsWith('/auth/csrf')) return { status: 200, json: async () => csrfBody(correlation).body };
      if (url.endsWith('/auth/login')) return { status: 200, json: async () => ({ data: { outcome: 'ISSUED' }, meta: { correlation_id: correlation, context: TENANT }, links: {} }) };
      if (url.endsWith('/shell/context')) return { status: 200, json: async () => contextEnvelope(correlation, TENANT, clock).body };
      throw new Error('route-inattendue ' + url);
    },
  });
  const auth = await env.rt.login(TENANT, { external_subject: 'operatrice', password: 'secret-temporaire' });
  assert.equal(auth.phase, 'CONFIRMED');
  assert.equal(env.rt.getState().state, 'ACTIVE');
  assert.ok(!JSON.stringify(env.rt.getState()).includes('secret-temporaire'));
  assert.ok(!JSON.stringify(env.rt.getAuthStatus()).includes('secret-temporaire'));
  assert.ok(!JSON.stringify(channel.posted).includes('secret-temporaire'));
  assert.ok(seen.filter((c) => c.url.endsWith('/auth/login')).every((c) => !('X-Shell-Session-ID' in c.headers)));
});

test('reprise identique garde cle empreinte divergent refuse sans post', async () => {
  const clock = makeClock(), keys = [];
  const env = makeRuntime({ clock, handler: async ({ url, init }) => {
    const correlation = init.headers['X-Correlation-ID'];
    if (url.endsWith('/auth/csrf')) return { status: 200, json: async () => csrfBody(correlation).body };
    if (!url.endsWith('/auth/login')) throw new Error('route-inattendue');
    keys.push(init.headers['Idempotency-Key']);
    if (keys.length === 1) throw new Error('panne-reseau-synthetique');
    return { status: 400, json: async () => ({ error_code: 'REFUS', message: 'non', details: {}, correlation_id: correlation }) };
  } });
  await rejectsCode(() => env.rt.login(TENANT, { external_subject: 'synthetique', password: 'fixture' }), 'SESSION_NETWORK_FAILED');
  assert.equal(env.rt.getAuthStatus().phase, 'UNKNOWN');
  const before = env.fetchCalls.length;
  await rejectsCode(() => env.rt.login(TENANT, { external_subject: 'synthetique', password: 'autre-fixture' }), 'SESSION_RETRY_MISMATCH');
  await rejectsCode(() => env.rt.login(PLATFORM, { external_subject: 'synthetique', password: 'fixture' }), 'SESSION_RETRY_MISMATCH');
  assert.equal(env.fetchCalls.length, before);
  const retry = await env.rt.login(TENANT, { external_subject: 'synthetique', password: 'fixture' });
  assert.equal(retry.phase, 'UNKNOWN');
  assert.equal(keys.length, 2); assert.equal(keys[0], keys[1]);
  assert.equal(env.rt.getState().state, 'ERROR');
  env.rt.dispose();
});
test('deconnexion distinguee rejouable garde cle entete corps', async () => {
  async function logoutWith(outcome) {
    const clock = makeClock();
    const posts = [];
    const env = makeRuntime({
      clock,
      handler: async ({ url, init }) => {
        const correlation = init.headers['X-Correlation-ID'];
        if (url.endsWith('/shell/context')) return { status: 200, json: async () => contextEnvelope(correlation, TENANT, clock).body };
        if (url.endsWith('/auth/csrf')) return { status: 200, json: async () => csrfBody(correlation).body };
        if (url.endsWith('/auth/logout')) {
          posts.push({ key: init.headers['Idempotency-Key'], session: init.headers['X-Shell-Session-ID'], body: init.body });
          return { status: 200, json: async () => ({ data: { outcome }, meta: { correlation_id: correlation, context: TENANT }, links: {} }) };
        }
        throw new Error('route-inattendue');
      },
    });
    await env.rt.load(TENANT);
    const session = env.rt.getState().session_id;
    const auth = await env.rt.logout();
    assert.equal(env.rt.getState().state, 'ANONYMOUS');
    assert.equal(posts[0].session, session);
    return { auth, posts };
  }
  const w = await logoutWith('WITHDRAWN');
  assert.equal(w.auth.phase, 'CONFIRMED');
  const p = await logoutWith('WITHDRAWN_AUDIT_PENDING');
  assert.equal(p.auth.error_code, 'SESSION_AUDIT_PENDING');
  const clock = makeClock();
  let n = 0;
  const keys = [], sessions = [], bodies = [];
  const env = makeRuntime({
    clock,
    handler: async ({ url, init }) => {
      const correlation = init.headers['X-Correlation-ID'];
      if (url.endsWith('/shell/context')) return { status: 200, json: async () => contextEnvelope(correlation, TENANT, clock).body };
      if (url.endsWith('/auth/csrf')) return { status: 200, json: async () => csrfBody(correlation).body };
      n++;
      keys.push(init.headers['Idempotency-Key']);
      sessions.push(init.headers['X-Shell-Session-ID']); bodies.push(init.body);
      if (n === 1) throw new Error('panne-simulee');
      return { status: 200, json: async () => ({ data: { outcome: 'WITHDRAWN' }, meta: { correlation_id: correlation, context: TENANT }, links: {} }) };
    },
  });
  await env.rt.load(TENANT);
  await rejectsCode(() => env.rt.logout(), 'SESSION_NETWORK_FAILED');
  await env.rt.logout();
  assert.equal(keys[0], keys[1]);
  assert.deepEqual(sessions, [SESSION_ID, SESSION_ID]);
  assert.deepEqual(bodies.map(JSON.parse), [{}, {}]);
  env.rt.dispose();
});

test('mutation pendante refuse double et ignore resultat obsolete', async () => {
  const clock = makeClock(), ready = deferred(), content = deferred();
  let signal;
  const env = makeRuntime({ clock, handler: async ({ url, init }) => {
    const correlation = init.headers['X-Correlation-ID'];
    if (url.endsWith('/auth/csrf')) return { status: 200, json: async () => csrfBody(correlation).body };
    if (url.endsWith('/auth/login')) {
      signal = init.signal; ready.resolve(correlation);
      return { status: 200, json: async () => content.promise };
    }
    if (url.endsWith('/shell/context')) return { status: 200, json: async () => contextEnvelope(correlation, PLATFORM, clock).body };
    throw new Error('route-inattendue');
  } });
  const pending = env.rt.login(TENANT, { external_subject: 'synthetique', password: 'fixture' });
  const refused = rejectsCode(() => pending, 'SESSION_SNAPSHOT_STALE');
  const correlation = await ready.promise;
  await rejectsCode(() => env.rt.login(TENANT, { external_subject: 'synthetique', password: 'fixture' }), 'SESSION_AUTH_PENDING');
  await rejectsCode(() => env.rt.logout(), 'SESSION_AUTH_PENDING');
  await env.rt.load(PLATFORM);
  assert.equal(signal.aborted, true);
  content.resolve({ data: { outcome: 'ISSUED' }, meta: { correlation_id: correlation, context: TENANT }, links: {} });
  await refused;
  assert.deepEqual(env.rt.getState().scope, PLATFORM);
  assert.equal(env.rt.getState().state, 'ACTIVE');
  assert.equal(env.rt.getAuthStatus().phase, 'UNKNOWN');
  env.rt.dispose();
});
test('arret nettoie timers requetes ecoutes remonte echec', async () => {
  const clock = makeClock(), channel = makeChannel(), ready = deferred(), content = deferred();
  let signal;
  const env = makeRuntime({ clock, channel, handler: async ({ url, init }) => {
    const correlation = init.headers['X-Correlation-ID'];
    if (url.endsWith('/shell/context')) return { status: 200, json: async () => contextEnvelope(correlation, TENANT, clock).body };
    signal = init.signal; ready.resolve(correlation);
    return { status: 200, json: async () => content.promise };
  } });
  await env.rt.load(TENANT);
  let notifications = 0;
  const stop = env.rt.subscribe(() => { notifications += 1; });
  assert.equal(typeof stop, 'function');
  const snapshot = env.rt.getContextSnapshot();
  const pending = env.rt.fetchJson('/api/v1/web/tenants/tenant-alpha/groups', { snapshot, params: {} });
  const refused = rejectsCode(() => pending, 'SESSION_SNAPSHOT_STALE');
  const correlation = await ready.promise;
  env.rt.dispose(); const afterFirst = notifications; env.rt.dispose();
  assert.equal(notifications, afterFirst); assert.equal(clock.pendingCount(), 0);
  assert.equal(signal.aborted, true); assert.equal(channel.closed, true);
  assert.equal(channel.listeners.get('message').length, 0);
  content.resolve({ data: [], meta: { correlation_id: correlation, context: TENANT }, links: {} });
  await refused;
  await rejectsCode(() => env.rt.load(TENANT), 'SESSION_DISPOSED');
  const clock2 = makeClock(), bad = makeChannel();
  bad.removeThrows = true;
  const other = makeRuntime({ clock: clock2, channel: bad, handler: async ({ init }) => ({
    status: 200, json: async () => contextEnvelope(init.headers['X-Correlation-ID'], TENANT, clock2).body,
  }) });
  await other.rt.load(TENANT);
  throwsCode(() => other.rt.dispose(), 'SESSION_DISPOSE_FAILED');
  assert.equal(clock2.pendingCount(), 0); assert.equal(bad.closed, true);
});
