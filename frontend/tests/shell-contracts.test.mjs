// Doubles explicites de ports/transport : ces tests ne qualifient ni C03/C04 ni un rendu.
import test from 'node:test';
import assert from 'node:assert/strict';
import {
  SHELL_API_VERSION,
  TRANSPORT_RESOLVER_VERSION,
  validateScope,
  validateSnapshot,
  buildWebPath,
  resolveTransport,
  validateTransportResolver,
  defaultTransportResolver,
  createContextProvider,
  createQueryClient,
  createCommandClient,
  validateShellContext,
  createShellPorts,
  bindShellApi,
  shellSlots,
  ShellContextProvider, useShellContext, QueryClient, CommandClient, navigate, invalidateScope,
} from '../src/shell/api-v1.js';
import {
  validateCompositionDescriptor,
  createShellExtensionPoints,
  COMPOSITION_DESCRIPTOR_VERSION,
} from '../src/shell/composition-descriptor-v1.js';

const TENANT = '0193f2a1-7b3c-7d4e-8a5f-123456789abc';
const SCOPE_ID = '0193f2a2-7b3c-7d4e-9a5f-123456789abd';
const PLATFORM = Object.freeze({ scope_type: 'PLATFORM', tenant_id: null, scope_id: null });
const TENANT_SCOPE = Object.freeze({ scope_type: 'TENANT', tenant_id: TENANT, scope_id: null });
const FULL_SCOPE = Object.freeze({ scope_type: 'TENANT', tenant_id: TENANT, scope_id: SCOPE_ID });

function snap(scope, epoch = 7) {
  return Object.freeze({ scope, epoch });
}
function okEnvelope(scope, correlation_id = 'c-1') {
  return Object.freeze({ status: 200, body: Object.freeze({ data: Object.freeze([]), meta: Object.freeze({ correlation_id, context: scope }), links: Object.freeze({}) }) });
}
function errEnvelope(code = 'ACCESS_DENIED', correlation_id = 'c-1') {
  return Object.freeze({ status: 403, body: Object.freeze({ error_code: code, message: 'refusé', details: Object.freeze({}), correlation_id }) });
}
async function rejectsWith(fn, code) {
  let threw = false;
  try { await fn(); } catch (e) { threw = true; assert.equal(String(e && e.message), code); }
  assert.ok(threw, 'rejet attendu ' + code);
}
function contextDouble(scope, current = true) {
  const s = snap(scope);
  return {
    snapshot: () => s,
    isCurrent: (v) => { assert.equal(v.epoch, s.epoch); return current; },
  };
}

test('façade : exports appelables et délégation des ports', () => {
  assert.equal(SHELL_API_VERSION, '1.0.0');
  assert.deepEqual(shellSlots(), ['pixs.shell.header', 'pixs.shell.navigation', 'pixs.shell.main', 'pixs.shell.footer']);
  let navArgs = null;
  const ports = {
    ShellContextProvider: (...a) => 'p', useShellContext: () => ({ state: 'ANONYMOUS', epoch: 0, scope: null }), getContextSnapshot: () => snap(PLATFORM),
    isCurrentSnapshot: () => true, fetchJson: async () => okEnvelope(PLATFORM), postJson: async () => okEnvelope(PLATFORM),
    navigate: (...a) => { navArgs = a; return 'n'; }, invalidateScope: () => 'i', translate: (k) => k, present: (v) => v,
  };
  const api = bindShellApi(ports);
  assert.equal(api.version, '1.0.0');
  for (const fn of [ShellContextProvider, useShellContext, QueryClient, CommandClient, navigate, invalidateScope]) assert.equal(typeof fn, 'function');
  assert.equal(ShellContextProvider(api, 'enfant'), 'p');
  assert.equal(useShellContext(api).state, 'ANONYMOUS');
  assert.equal(invalidateScope(api), 'i');
  assert.equal(api.navigate('x'), 'n');
  assert.deepEqual(navArgs, ['x']);
});

test('ports fermés : types, champs secrets et accesseurs refusés', () => {
  const good = { ShellContextProvider: () => 0, useShellContext: () => 0, getContextSnapshot: () => snap(PLATFORM), isCurrentSnapshot: () => true, fetchJson: async () => 0, postJson: async () => 0, navigate: () => 0, invalidateScope: () => 0, translate: () => 0, present: () => 0 };
  assert.ok(createShellPorts(Object.freeze({ ...good })));
  assert.throws(() => createShellPorts(undefined), { message: 'SHELL_PORTS_INVALID' });
  assert.throws(() => createShellPorts({ ...good, fetchJson: 1 }), { message: 'SHELL_PORT_MISSING' });
  assert.throws(() => createShellPorts(null), { message: 'SHELL_PORTS_INVALID' });
  assert.throws(() => createShellPorts([]), { message: 'SHELL_PORTS_INVALID' });
  assert.throws(() => createShellPorts({ ...good, token: 't' }), { message: 'SHELL_PORTS_INVALID' });
  const noFetch = { ...good };
  delete noFetch.fetchJson;
  assert.throws(() => createShellPorts(noFetch), { message: 'SHELL_PORTS_INVALID' });
  let invoked = false;
  const evil = {};
  Object.defineProperty(evil, 'fetchJson', { get() { invoked = true; return async () => 0; }, enumerable: true, configurable: true });
  for (const k of ['ShellContextProvider', 'useShellContext', 'getContextSnapshot', 'isCurrentSnapshot', 'postJson', 'navigate', 'invalidateScope', 'translate', 'present']) evil[k] = good[k];
  assert.throws(() => createShellPorts(evil), { message: 'SHELL_PORTS_INVALID' });
  assert.equal(invoked, false);
});

test('périmètres canoniques : plateforme, tenant, scope opaques et session UUIDv7', () => {
  assert.ok(Object.isFrozen(validateScope(PLATFORM)));
  assert.ok(Object.isFrozen(validateScope(TENANT_SCOPE)));
  assert.ok(Object.isFrozen(validateScope(FULL_SCOPE)));
  assert.ok(Object.isFrozen(validateScope({ scope_type: 'TENANT', tenant_id: 'not-uuid', scope_id: null })));
  assert.ok(Object.isFrozen(validateScope({ scope_type: 'TENANT', tenant_id: 'toto', scope_id: null })));
  assert.ok(Object.isFrozen(validateScope({ scope_type: 'TENANT', tenant_id: '.', scope_id: null })));
  assert.ok(Object.isFrozen(validateScope({ scope_type: 'TENANT', tenant_id: '..', scope_id: null })));
  assert.ok(Object.isFrozen(validateScope({ scope_type: 'TENANT', tenant_id: '\0', scope_id: null })));
  assert.ok(Object.isFrozen(validateScope({ scope_type: 'TENANT', tenant_id: '\uD800', scope_id: null })));
  assert.throws(() => validateScope({ scope_type: 'PLATFORM', tenant_id: TENANT, scope_id: null }), { message: 'SHELL_SCOPE_INVALID' });
  assert.throws(() => validateScope({ scope_type: 'TENANT', tenant_id: '', scope_id: null }), { message: 'SHELL_SCOPE_INVALID' });
  assert.throws(() => validateScope({ scope_type: 'TENANT', tenant_id: TENANT }), { message: 'SHELL_SCOPE_INVALID' });
  assert.throws(() => validateScope({ scope_type: 'TENANT', tenant_id: null, scope_id: null }), { message: 'SHELL_SCOPE_INVALID' });
  assert.throws(() => validateScope({ scope_type: 'X', tenant_id: null, scope_id: null }), { message: 'SHELL_SCOPE_INVALID' });
});

test('snapshots : copies profondes immuables sans alias', () => {
  const s = validateSnapshot({ scope: TENANT_SCOPE, epoch: 3 });
  assert.ok(Object.isFrozen(s));
  assert.ok(Object.isFrozen(s.scope));
  assert.equal(s.epoch, 3);
  const provider = createContextProvider({ getContextSnapshot: () => ({ scope: TENANT_SCOPE, epoch: 3 }), isCurrentSnapshot: () => true });
  const a = provider.snapshot();
  const b = provider.snapshot();
  assert.ok(a !== b);
  assert.equal(a.epoch, b.epoch);
  const original = { scope: { scope_type: 'PLATFORM', tenant_id: null, scope_id: null }, epoch: 2 };
  const copy = validateSnapshot(original);
  original.scope.scope_type = 'TENANT'; original.epoch = 99;
  assert.equal(copy.scope.scope_type, 'PLATFORM'); assert.equal(copy.epoch, 2);
  assert.equal(Object.isFrozen(original), false);
});

test('provider : époque et réponse courante contrôlées', () => {
  const provider = createContextProvider({ getContextSnapshot: () => ({ scope: PLATFORM, epoch: 1 }), isCurrentSnapshot: (v) => v.epoch === 1 });
  assert.ok(provider.snapshot().epoch === 1);
  assert.equal(provider.isCurrent(snap(PLATFORM, 1)), true);
  assert.equal(provider.isCurrent(snap(PLATFORM, 2)), false);
  assert.throws(() => createContextProvider({ getContextSnapshot: null, isCurrentSnapshot: () => true }), { message: 'SHELL_PORT_MISSING' });
});

test('contexte actif : assurances et hints explicites', () => {
  const active = {
    state: 'ACTIVE', epoch: 9, scope: FULL_SCOPE, identity_ref: 'id:1', session_id: '0193f2a1-7b3c-7d4e-8a5f-123456789abc',
    category: 'ADMIN', facade: 'WEB', authentication_time: '2026-10-22T19:00:00Z', expires_at: '2026-10-22T20:00:00Z',
    identity_assurance: 'VERIFIED', authentication_assurance: 'MULTI_FACTOR',
    ui_permissions: { status: 'VERIFIED', items: [{ action_id: 'pixs.core.groups.read', resource_id: 'pixs.core.group:g1', allowed: true }], policy_version: '1', evaluated_at: '2026-10-22T19:00:00Z' },
  };
  const frozen = validateShellContext(active);
  assert.ok(Object.isFrozen(frozen));
  assert.ok(Object.isFrozen(frozen.ui_permissions));
  assert.ok(Object.isFrozen(frozen.ui_permissions.items[0]));
  active.ui_permissions.items[0].allowed = false;
  assert.equal(frozen.ui_permissions.items[0].allowed, true);
  const unavailable = { ...active, ui_permissions: { status: 'UNAVAILABLE', items: [] } };
  assert.ok(validateShellContext(unavailable));
});

test('contexte inactif : purge des faits et refus des secrets', () => {
  const anon = Object.freeze({ state: 'ANONYMOUS', epoch: 0, scope: null });
  assert.ok(validateShellContext(anon));
  assert.throws(() => validateShellContext({ state: 'ANONYMOUS', epoch: 0, scope: null, identity_ref: 'id:1' }), { message: 'SHELL_CONTEXT_INVALID' });
  const active = {
    state: 'ACTIVE', epoch: 1, scope: TENANT_SCOPE, identity_ref: 'id:1', session_id: TENANT, category: 'ADMIN', facade: 'WEB',
    authentication_time: '2026-10-22T19:00:00Z', expires_at: '2026-10-22T20:00:00Z',
    identity_assurance: 'VERIFIED', authentication_assurance: 'MULTI_FACTOR',
    ui_permissions: { status: 'UNAVAILABLE', items: [] },
  };
  assert.throws(() => validateShellContext({ ...active, provider: 'p' }), { message: 'SHELL_CONTEXT_INVALID' });
  assert.throws(() => validateShellContext({ ...active, cookie: 'c' }), { message: 'SHELL_CONTEXT_INVALID' });
  assert.throws(() => validateShellContext({ ...active, facade: 'API' }), { message: 'SHELL_CONTEXT_INVALID' });
  assert.throws(() => validateShellContext({ ...active, session_id: 'opaque-invalid-session' }), { message: 'SHELL_CONTEXT_INVALID' });
  for (const key of ['token', 'issuer', 'external_subject', 'credential_id']) assert.throws(() => validateShellContext({ ...active, [key]: 'fixture' }), { message: 'SHELL_CONTEXT_INVALID' });
  assert.throws(() => validateShellContext({ ...active, identity_assurance: 'ADMIN' }), { message: 'SHELL_CONTEXT_INVALID' });
});

test('routes web : URL externe, traversée et Auth refusées', async () => {
  let called = false;
  const provider = contextDouble(PLATFORM);
  const client = createQueryClient({ fetchJson: async () => { called = true; return okEnvelope(PLATFORM); }, contextProvider: provider });
  await rejectsWith(() => client.query('../x'), 'SHELL_ROUTE_INVALID');
  await rejectsWith(() => client.query('auth'), 'SHELL_ROUTE_INVALID');
  await rejectsWith(() => createCommandClient({ postJson: async () => okEnvelope(PLATFORM), contextProvider: provider }).intent('auth', {}, { idempotencyKey: 'k' }), 'SHELL_ROUTE_INVALID');
  await rejectsWith(() => createCommandClient({ postJson: async () => okEnvelope(PLATFORM), contextProvider: provider }).intent('https://evil/x', {}, { idempotencyKey: 'k' }), 'SHELL_ROUTE_INVALID');
  assert.equal(called, false);
});

test('queries : contexte du provider et enveloppe C06', async () => {
  let seen = null;
  const provider = contextDouble(FULL_SCOPE);
  const client = createQueryClient({ fetchJson: async (path, { snapshot }) => { seen = { path, snapshot }; return okEnvelope(FULL_SCOPE); }, contextProvider: provider });
  const body = await client.query('groups');
  assert.ok(body.meta.correlation_id === 'c-1');
  assert.equal(seen.path, '/api/v1/web/tenants/' + TENANT + '/scopes/' + SCOPE_ID + '/groups');
  await rejectsWith(() => client.query('groups', { scope: FULL_SCOPE }), 'SHELL_QUERY_INVALID');
});

test('commands : attente serveur, idempotence et copie de l’entrée', async () => {
  let release;
  const gate = new Promise((resolve) => { release = resolve; });
  let seen = null;
  const provider = contextDouble(PLATFORM);
  const client = createCommandClient({ postJson: async (path, input, { idempotencyKey, snapshot }) => { seen = { path, input, idempotencyKey }; await gate; return okEnvelope(PLATFORM); }, contextProvider: provider });
  const source = { name: 'g' };
  const pending = client.intent('create-group', source, { idempotencyKey: 'k-1' });
  source.name = 'modifié';
  let settled = false;
  pending.then(() => { settled = true; }, () => { settled = true; });
  await Promise.resolve();
  assert.equal(settled, false);
  release();
  const out = await pending;
  assert.equal(out.state, 'CONFIRMED');
  assert.equal(seen.idempotencyKey, 'k-1');
  assert.equal(seen.input.name, 'g');
  assert.ok(Object.isFrozen(seen.input));
  assert.equal(seen.path, '/api/v1/web/platform/commands/create-group');
  await rejectsWith(() => client.intent('create-group', {}, { }), 'SHELL_IDEMPOTENCY_REQUIRED');
});

test('réponse retardée : aucun fait de l’ancien contexte exposé', async () => {
  const provider = { snapshot: () => snap(PLATFORM, 1), isCurrent: () => false };
  const client = createQueryClient({ fetchJson: async () => okEnvelope(PLATFORM), contextProvider: provider });
  await rejectsWith(() => client.query('users'), 'SHELL_SNAPSHOT_STALE');
  const cmd = createCommandClient({ postJson: async () => okEnvelope(PLATFORM), contextProvider: provider });
  await rejectsWith(() => cmd.intent('create-group', {}, { idempotencyKey: 'k' }), 'SHELL_SNAPSHOT_STALE');
});

test('résultat connu, refus, panne et issue inconnue distingués', async () => {
  const provider = contextDouble(PLATFORM);
  const okClient = createCommandClient({ postJson: async () => okEnvelope(PLATFORM), contextProvider: provider });
  assert.equal((await okClient.intent('create-group', {}, { idempotencyKey: 'k' })).state, 'CONFIRMED');
  const rejClient = createCommandClient({ postJson: async () => errEnvelope(), contextProvider: provider });
  assert.equal((await rejClient.intent('create-group', {}, { idempotencyKey: 'k' })).state, 'REJECTED');
  const unknownClient = createCommandClient({ postJson: async () => ({ status: 500, body: { error_code: 'E', message: 'm', details: {}, correlation_id: 'c' } }), contextProvider: provider });
  assert.equal((await unknownClient.intent('create-group', {}, { idempotencyKey: 'k' })).state, 'UNKNOWN');
  const acceptedClient = createCommandClient({ postJson: async () => ({ status: 202, body: {} }), contextProvider: provider });
  assert.equal((await acceptedClient.intent('create-group', {}, { idempotencyKey: 'k' })).state, 'UNKNOWN');
  const badClient = createQueryClient({ fetchJson: async () => ({ status: 200, body: {} }), contextProvider: provider });
  await rejectsWith(() => badClient.query('users'), 'SHELL_RESPONSE_INVALID');
  const downClient = createQueryClient({ fetchJson: async () => { throw new Error('down'); }, contextProvider: provider });
  await rejectsWith(() => downClient.query('users'), 'SHELL_QUERY_UNAVAILABLE');
});

const DLIMITS = Object.freeze({
  maxTextLength: 256,
  maxRequires: 8,
  maxPermissions: 8,
  maxPoints: 32,
  maxLocales: 8,
  maxCatalogKeys: 32,
});
function dfacet(over = {}) {
  return {
    owner: 'acme.app',
    owner_version: '1.0.0',
    type: 'ROUTE',
    id: 'acme.app.home',
    entry: 'frontend/routes/home',
    version: '1.0.0',
    requires: [],
    scope: 'TENANT_SCOPED',
    ...over,
  };
}
function dpoints() {
  return createShellExtensionPoints();
}
function dcontext(facet, over = {}) {
  return { facet, extensionPoints: dpoints(), limits: DLIMITS, ...over };
}
function ddescriptor(facet, point, payload, over = {}) {
  return {
    descriptor_version: '1.0.0',
    owner: facet.owner,
    owner_version: facet.owner_version,
    type: facet.type,
    id: facet.id,
    entry: facet.entry,
    version: facet.version,
    requires: [...facet.requires],
    scope: facet.scope,
    point,
    point_version: '1.0.0',
    display_permissions: [],
    trust: 'TRUSTED',
    mandatory: true,
    activation_scope: facet.scope,
    payload,
    ...over,
  };
}
function rejectsCode(fn, code) {
  try { fn(); } catch (e) { assert.equal(e.code, code); assert.equal(e.message, code); return; }
  throw new Error('rejet attendu ' + code);
}
function payloadFor(type) {
  if (type === 'ROUTE') return { path: '/home', mode: 'CSR', page: 'Home' };
  if (type === 'PAGE') return { export: 'HomePage' };
  if (type === 'NAVIGATION') return { route: '/home', labelKey: 'acme.app.home' };
  if (type === 'COMPONENT') return { export: 'HomeView' };
  if (type === 'FORM') return { export: 'HomeForm' };
  if (type === 'TRANSLATION') return { catalog: { fr: { 'acme.app.title': 'Accueil' } } };
  if (type === 'UI_PERMISSION') return { key: 'acme.app.view', fallback: 'Voir' };
  return { slot: 'pixs.shell.main', export: 'MainSlot' };
}
function pointFor(type) {
  if (type === 'ROUTE') return 'pixs.shell.routes';
  if (type === 'PAGE') return 'pixs.shell.pages';
  if (type === 'NAVIGATION') return 'pixs.shell.navigation-items';
  if (type === 'COMPONENT') return 'pixs.shell.components';
  if (type === 'FORM') return 'pixs.shell.forms';
  if (type === 'TRANSLATION') return 'pixs.shell.translations';
  if (type === 'UI_PERMISSION') return 'pixs.shell.ui-permissions';
  return 'pixs.shell.main';
}

test('descripteur : huit types nominaux gelés et concordants', () => {
  for (const type of ['ROUTE','PAGE','NAVIGATION','COMPONENT','FORM','TRANSLATION','UI_PERMISSION','UI_SLOT']) {
    const facet = dfacet({ type, id: `acme.app.${type.toLowerCase()}` });
    const out = validateCompositionDescriptor(
      ddescriptor(facet, pointFor(type), payloadFor(type)),
      dcontext(facet),
    );
    assert.ok(Object.isFrozen(out));
    assert.ok(Object.isFrozen(out.requires));
    assert.ok(Object.isFrozen(out.payload));
    assert.equal(out.type, type);
    assert.equal(COMPOSITION_DESCRIPTOR_VERSION, '1.0.0');
  }
});

test('descripteur : onze points uniques, metadata gelée et catégorie concordante', () => {
  const registry = dpoints();
  const ids = Object.keys(registry.points);
  assert.deepEqual(ids.sort(), [...new Set(ids)].sort());
  assert.equal(ids.length, 11);
  assert.ok(Object.isFrozen(registry));
  assert.ok(Object.isFrozen(registry.points));
  assert.ok(Object.isFrozen(registry.metadata));
  assert.equal(registry.metadata.version, '1.0.0');
  const facet = dfacet({ type: 'PAGE', id: 'acme.app.page' });
  const bad = ddescriptor(facet, 'pixs.shell.routes', { export: 'HomePage' });
  rejectsCode(() => validateCompositionDescriptor(bad, dcontext(facet)), 'DESCRIPTOR_CATEGORY_MISMATCH');
});

test('descripteur : concordance huit champs, owner_version et requires ordre-multiplicité', () => {
  const facet = dfacet({ owner_version: '1.0.1', requires: ['audit >=1.0.0 <2.0.0','acme.other ==2.0.0','audit >=1.0.0 <2.0.0'] });
  const good = ddescriptor(facet, 'pixs.shell.routes', { path: '/a', mode: 'CSR', page: 'Home' });
  assert.deepEqual(validateCompositionDescriptor(good, dcontext(facet)).requires, facet.requires);
  const swapped = ddescriptor(facet, 'pixs.shell.routes', { path: '/a', mode: 'CSR', page: 'Home' });
  swapped.requires = [facet.requires[1], facet.requires[0], facet.requires[2]];
  rejectsCode(() => validateCompositionDescriptor(swapped, dcontext(facet)), 'DESCRIPTOR_FACET_MISMATCH');
  const badOwner = ddescriptor({ ...facet }, 'pixs.shell.routes', { path: '/a', mode: 'CSR', page: 'Home' });
  badOwner.owner_version = '9.9.9';
  rejectsCode(() => validateCompositionDescriptor(badOwner, dcontext(facet)), 'DESCRIPTOR_FACET_MISMATCH');
});

test('descripteur : limits obligatoires et budgets avant boucles, creux et très grands refusés', () => {
  const facet = dfacet();
  const good = ddescriptor(facet, 'pixs.shell.routes', { path: '/a', mode: 'CSR', page: 'Home' });
  rejectsCode(() => validateCompositionDescriptor(good, { facet, extensionPoints: dpoints() }), 'DESCRIPTOR_CONTEXT_INVALID');
  for (const badLimits of [{ ...DLIMITS, maxTextLength: 0 }, { ...DLIMITS, maxRequires: NaN }, { ...DLIMITS, maxPoints: true }]) {
    rejectsCode(() => validateCompositionDescriptor(good, { facet, extensionPoints: dpoints(), limits: badLimits }), 'DESCRIPTOR_LIMITS_INVALID');
  }
  const huge = new Array(2 ** 32 - 1);
  huge[0] = 'x';
  const badRequires = ddescriptor(facet, 'pixs.shell.routes', { path: '/a', mode: 'CSR', page: 'Home' });
  badRequires.requires = huge;
  rejectsCode(() => validateCompositionDescriptor(badRequires, dcontext(facet)), 'DESCRIPTOR_INVALID');
  const sparsePerms = [];
  sparsePerms[2] = 'voir';
  const badPerms = ddescriptor(facet, 'pixs.shell.routes', { path: '/a', mode: 'CSR', page: 'Home' });
  badPerms.display_permissions = sparsePerms;
  rejectsCode(() => validateCompositionDescriptor(badPerms, dcontext(facet)), 'DESCRIPTOR_PERMISSIONS_INVALID');
});

test('descripteur : facette entry Kernel non normalisée, point et garanties refusés', () => {
  const facet = dfacet({ entry: 'frontend/routes/MixedCase_Entry-1' });
  const good = ddescriptor(facet, 'pixs.shell.routes', { path: '/a', mode: 'CSR', page: 'Home' });
  assert.equal(validateCompositionDescriptor(good, dcontext(facet)).entry, 'frontend/routes/MixedCase_Entry-1');
  rejectsCode(() => validateCompositionDescriptor({ ...good, point: 'pixs.shell.unknown' }, dcontext(facet)), 'DESCRIPTOR_POINT_UNKNOWN');
  const registry = dpoints();
  const wrongVersion = { ...registry.points['pixs.shell.routes'], version: '2.0.0' };
  const badRegistry = { points: { ...registry.points, 'pixs.shell.routes': wrongVersion }, metadata: registry.metadata };
  rejectsCode(() => validateCompositionDescriptor(good, { facet, extensionPoints: badRegistry, limits: DLIMITS }), 'DESCRIPTOR_POINT_VERSION_INVALID');
  const badSchema = { ...registry.points['pixs.shell.routes'], schema: 'autre/schema' };
  const badRegistry2 = { points: { ...registry.points, 'pixs.shell.routes': badSchema }, metadata: registry.metadata };
  rejectsCode(() => validateCompositionDescriptor(good, { facet, extensionPoints: badRegistry2, limits: DLIMITS }), 'DESCRIPTOR_SCHEMA_INVALID');
  const badOwner = { ...registry.points['pixs.shell.routes'], owner: '' };
  const badRegistry3 = { points: { ...registry.points, 'pixs.shell.routes': badOwner }, metadata: registry.metadata };
  rejectsCode(() => validateCompositionDescriptor(good, { facet, extensionPoints: badRegistry3, limits: DLIMITS }), 'DESCRIPTOR_POINTS_INVALID');
  const badGuarantees = { ...registry.points['pixs.shell.routes'], guarantees: ['DATA_ONLY_DESCRIPTOR'] };
  const badRegistry4 = { points: { ...registry.points, 'pixs.shell.routes': badGuarantees }, metadata: registry.metadata };
  rejectsCode(() => validateCompositionDescriptor(good, { facet, extensionPoints: badRegistry4, limits: DLIMITS }), 'DESCRIPTOR_GUARANTEES_INVALID');
});

test('descripteur : payload fermé, CSR et exports nommés, chemins privés refusés', () => {
  const facet = dfacet();
  const noCsr = ddescriptor(facet, 'pixs.shell.routes', { path: '/a', mode: 'SSR', page: 'Home' });
  rejectsCode(() => validateCompositionDescriptor(noCsr, dcontext(facet)), 'DESCRIPTOR_PAYLOAD_INVALID');
  for (const badExport of ['frontend/Home', './Home', 'Home/Page', '_Private', 'constructor', 'prototype', 'a-b']) {
    const bad = ddescriptor(dfacet({ type: 'PAGE', id: 'acme.app.page' }), 'pixs.shell.pages', { export: badExport });
    const f = dfacet({ type: 'PAGE', id: 'acme.app.page' });
    rejectsCode(() => validateCompositionDescriptor(bad, dcontext(f)), 'DESCRIPTOR_EXPORT_INVALID');
  }
  const extra = ddescriptor(facet, 'pixs.shell.routes', { path: '/a', mode: 'CSR', page: 'Home', autre: 1 });
  rejectsCode(() => validateCompositionDescriptor(extra, dcontext(facet)), 'DESCRIPTOR_PAYLOAD_INVALID');
});

test('descripteur : chemins fermés, traversée et param canonique', () => {
  const facet = dfacet();
  assert.equal(validateCompositionDescriptor(ddescriptor(facet, 'pixs.shell.routes', { path: '/{tenant_id}', mode: 'CSR', page: 'Home' }), dcontext(facet)).payload.path, '/{tenant_id}');
  assert.equal(validateCompositionDescriptor(ddescriptor(facet, 'pixs.shell.routes', { path: '/', mode: 'CSR', page: 'Home' }), dcontext(facet)).payload.path, '/');
  for (const badPath of ['/a/../b', '/a/./b', '/a//b', '/a/', '/a%20b', '/a?x=1', '/a#frag', '/a:b', '/a b', 'a/b', '/a\\b', '/{Bad}', '/{a b}', '/..', '/.']) {
    const bad = ddescriptor(facet, 'pixs.shell.routes', { path: badPath, mode: 'CSR', page: 'Home' });
    rejectsCode(() => validateCompositionDescriptor(bad, dcontext(facet)), 'DESCRIPTOR_PATH_INVALID');
  }
});

test('descripteur : permissions déclaratives, trust et slot modulaire public', () => {
  const facet = dfacet({ scope: 'PUBLIC', type: 'UI_SLOT', id: 'acme.app.slot' });
  const registry = dpoints();
  const modularPoint = 'acme.mod.slot';
  const modularRegistry = {
    points: { ...registry.points, [modularPoint]: { owner: 'acme.mod', category: 'UI_SLOT', version: '1.0.0', schema: 'pixs.frontend.composition-descriptor/1.0.0', guarantees: ['DATA_ONLY_DESCRIPTOR', 'EXPLICIT_ENTRY_EXPORTS'] } },
    metadata: registry.metadata,
  };
  const good = ddescriptor(facet, modularPoint, { slot: modularPoint, export: 'SlotView' }, { display_permissions: ['voir-accueil'], trust: 'SANDBOXED', mandatory: false });
  assert.equal(validateCompositionDescriptor(good, { facet, extensionPoints: modularRegistry, limits: DLIMITS }).trust, 'SANDBOXED');
  for (const trust of ['PLATFORM', 'TRUSTED', 'DEVELOPMENT']) {
    const candidate = ddescriptor(facet, modularPoint, { slot: modularPoint, export: 'SlotView' }, { trust });
    assert.equal(validateCompositionDescriptor(candidate, { facet, extensionPoints: modularRegistry, limits: DLIMITS }).trust, trust);
  }
  rejectsCode(() => validateCompositionDescriptor(ddescriptor(facet, modularPoint, { slot: modularPoint, export: 'SlotView' }, { trust: 'FAUX' }), { facet, extensionPoints: modularRegistry, limits: DLIMITS }), 'DESCRIPTOR_TRUST_INVALID');
  const mismatch = ddescriptor(facet, modularPoint, { slot: 'pixs.shell.main', export: 'SlotView' });
  rejectsCode(() => validateCompositionDescriptor(mismatch, { facet, extensionPoints: modularRegistry, limits: DLIMITS }), 'DESCRIPTOR_PAYLOAD_INVALID');
});

test('descripteur : catalogues namespacés, LF accepté et sans alias', () => {
  const facet = dfacet({ type: 'TRANSLATION', id: 'acme.app.i18n' });
  const catalog = { fr: { 'acme.app.title': 'Bonjour\nSuite' }, 'fr-FR': { 'acme.app.title': 'Bonjour' } };
  const good = ddescriptor(facet, 'pixs.shell.translations', { catalog });
  const out = validateCompositionDescriptor(good, dcontext(facet));
  assert.equal(out.payload.catalog.fr['acme.app.title'], 'Bonjour\nSuite');
  catalog.fr['acme.app.title'] = 'modifié';
  assert.equal(out.payload.catalog.fr['acme.app.title'], 'Bonjour\nSuite');
  const badControl = { fr: { 'acme.app.title': 'a\x01b' } };
  rejectsCode(() => validateCompositionDescriptor(ddescriptor(facet, 'pixs.shell.translations', { catalog: badControl }), dcontext(facet)), 'DESCRIPTOR_PAYLOAD_INVALID');
  const badSurrogate = { fr: { 'acme.app.title': '\uD800' } };
  rejectsCode(() => validateCompositionDescriptor(ddescriptor(facet, 'pixs.shell.translations', { catalog: badSurrogate }), dcontext(facet)), 'DESCRIPTOR_PAYLOAD_INVALID');
  const badLocale = { fr_fr: { 'acme.app.title': 'x' } };
  rejectsCode(() => validateCompositionDescriptor(ddescriptor(facet, 'pixs.shell.translations', { catalog: badLocale }), dcontext(facet)), 'DESCRIPTOR_PAYLOAD_INVALID');
});

test('descripteur : accesseurs non appelés, exotiques et gelé accepté', () => {
  const facet = dfacet();
  const good = ddescriptor(facet, 'pixs.shell.routes', { path: '/a', mode: 'CSR', page: 'Home' });
  let calls = 0;
  const evilGetter = {};
  Object.defineProperty(evilGetter, 'path', { get() { calls += 1; return '/a'; }, enumerable: true });
  evilGetter.mode = 'CSR';
  evilGetter.page = 'Home';
  const badPayload = ddescriptor(facet, 'pixs.shell.routes', evilGetter);
  rejectsCode(() => validateCompositionDescriptor(badPayload, dcontext(facet)), 'DESCRIPTOR_PAYLOAD_INVALID');
  assert.equal(calls, 0);
  let contextCalls = 0;
  const evilContext = {};
  Object.defineProperty(evilContext, 'facet', { get() { contextCalls += 1; return facet; }, enumerable: true });
  evilContext.extensionPoints = dpoints();
  evilContext.limits = DLIMITS;
  rejectsCode(() => validateCompositionDescriptor(good, evilContext), 'DESCRIPTOR_CONTEXT_INVALID');
  assert.equal(contextCalls, 0);
  const withSymbol = ddescriptor(facet, 'pixs.shell.routes', { path: '/a', mode: 'CSR', page: 'Home' });
  withSymbol[Symbol('extra')] = 1;
  rejectsCode(() => validateCompositionDescriptor(withSymbol, dcontext(facet)), 'DESCRIPTOR_INVALID');
  const protoKey = ddescriptor(facet, 'pixs.shell.routes', { path: '/a', mode: 'CSR', page: 'Home' });
  Object.defineProperty(protoKey.payload, '__proto__', { value: 1, enumerable: true });
  rejectsCode(() => validateCompositionDescriptor(protoKey, dcontext(facet)), 'DESCRIPTOR_PAYLOAD_INVALID');
  const frozenGood = Object.freeze({ ...good, requires: Object.freeze([...good.requires]), display_permissions: Object.freeze([]), payload: Object.freeze({ ...good.payload }) });
  const frozenContext = Object.freeze({ facet: Object.freeze({ ...facet, requires: Object.freeze([...facet.requires]) }), extensionPoints: dpoints(), limits: DLIMITS });
  assert.ok(validateCompositionDescriptor(frozenGood, frozenContext));
});

test('descripteur : tous les champs de facette et limites de volume sont contrôlés', () => {
  const f = dfacet();
  const good = ddescriptor(f, 'pixs.shell.routes', payloadFor('ROUTE'));
  for (const key of ['owner', 'owner_version', 'type', 'id', 'entry', 'version', 'scope']) {
    rejectsCode(() => validateCompositionDescriptor({ ...good, [key]: 'autre' }, dcontext(f)), 'DESCRIPTOR_FACET_MISMATCH');
  }
  rejectsCode(() => validateCompositionDescriptor({ ...good, requires: ['audit'] }, dcontext(f)), 'DESCRIPTOR_FACET_MISMATCH');
  rejectsCode(() => validateCompositionDescriptor({ ...good, descriptor_version: '2.0.0' }, dcontext(f)), 'DESCRIPTOR_VERSION_INVALID');
  rejectsCode(() => validateCompositionDescriptor({ ...good, activation_scope: 'PUBLIC' }, dcontext(f)), 'DESCRIPTOR_SCOPE_MISMATCH');
  rejectsCode(() => validateCompositionDescriptor({ ...good, mandatory: 'true' }, dcontext(f)), 'DESCRIPTOR_INVALID');
  rejectsCode(() => validateCompositionDescriptor({ ...good, token: 'interdit' }, dcontext(f)), 'DESCRIPTOR_INVALID');
  rejectsCode(() => validateCompositionDescriptor({ ...good, display_permissions: ['a','b'] }, dcontext(f, { limits: { ...DLIMITS, maxPermissions: 1 } })), 'DESCRIPTOR_PERMISSIONS_INVALID');
  rejectsCode(() => validateCompositionDescriptor(good, dcontext(f, { limits: { ...DLIMITS, maxPoints: 1 } })), 'DESCRIPTOR_POINTS_INVALID');
  const tf = dfacet({ type: 'TRANSLATION' });
  const trans = catalog => ddescriptor(tf, 'pixs.shell.translations', { catalog });
  rejectsCode(() => validateCompositionDescriptor(trans({ fr: { 'acme.x': 'x' }, en: { 'acme.x': 'x' } }), dcontext(tf, { limits: { ...DLIMITS, maxLocales: 1 } })), 'DESCRIPTOR_PAYLOAD_INVALID');
  rejectsCode(() => validateCompositionDescriptor(trans({ fr: { 'acme.x': 'x', 'acme.y': 'y' } }), dcontext(tf, { limits: { ...DLIMITS, maxCatalogKeys: 1 } })), 'DESCRIPTOR_PAYLOAD_INVALID');
  rejectsCode(() => validateCompositionDescriptor(trans({ fr: { 'acme.x': 'x'.repeat(257) } }), dcontext(tf)), 'DESCRIPTOR_PAYLOAD_INVALID');
  rejectsCode(() => validateCompositionDescriptor(trans({ fr: { x: 'x' } }), dcontext(tf)), 'DESCRIPTOR_PAYLOAD_INVALID');
  const perms = [];
  perms.extra = 'x';
  rejectsCode(() => validateCompositionDescriptor({ ...good, display_permissions: perms }, dcontext(f)), 'DESCRIPTOR_PERMISSIONS_INVALID');
  rejectsCode(() => validateCompositionDescriptor(good, dcontext(f, { limits: new Map() })), 'DESCRIPTOR_LIMITS_INVALID');
});

test('descripteur : accesseurs de chaque frontière refusés et copies profondes', () => {
  const f = dfacet({ requires: ['audit >=1.0.0'] });
  const good = ddescriptor(f, 'pixs.shell.routes', payloadFor('ROUTE'), { display_permissions: ['acme.view'] });
  let calls = 0;
  const getter = (obj, key, value) => Object.defineProperty(obj, key, { get() { calls += 1; return value; }, enumerable: true, configurable: true });
  const badValue = getter({ ...good }, 'owner', good.owner);
  rejectsCode(() => validateCompositionDescriptor(badValue, dcontext(f)), 'DESCRIPTOR_INVALID');
  const badFacet = getter({ ...f }, 'owner', f.owner);
  rejectsCode(() => validateCompositionDescriptor(good, dcontext(badFacet)), 'DESCRIPTOR_FACET_INVALID');
  const reg = dpoints();
  const badPoints = getter({ ...reg.points }, 'pixs.shell.routes', reg.points['pixs.shell.routes']);
  rejectsCode(() => validateCompositionDescriptor(good, dcontext(f, { extensionPoints: { ...reg, points: badPoints } })), 'DESCRIPTOR_POINTS_INVALID');
  const tf = dfacet({ type: 'TRANSLATION' });
  const evilCatalog = getter({}, 'fr', { 'acme.x': 'x' });
  rejectsCode(() => validateCompositionDescriptor(ddescriptor(tf, 'pixs.shell.translations', { catalog: evilCatalog }), dcontext(tf)), 'DESCRIPTOR_PAYLOAD_INVALID');
  const evilTable = getter({}, 'acme.x', 'x');
  rejectsCode(() => validateCompositionDescriptor(ddescriptor(tf, 'pixs.shell.translations', { catalog: { fr: evilTable } }), dcontext(tf)), 'DESCRIPTOR_PAYLOAD_INVALID');
  assert.equal(calls, 0);
  const snap = validateCompositionDescriptor(good, dcontext(f));
  good.requires.push('acme.new');
  good.display_permissions.push('acme.edit');
  good.payload.path = '/changed';
  assert.deepEqual(snap.requires, ['audit >=1.0.0']);
  assert.deepEqual(snap.display_permissions, ['acme.view']);
  assert.equal(snap.payload.path, '/home');
  assert.ok(Object.isFrozen(snap.display_permissions));
  const catalogSnap = validateCompositionDescriptor(ddescriptor(tf, 'pixs.shell.translations', payloadFor('TRANSLATION')), dcontext(tf));
  assert.ok(Object.isFrozen(catalogSnap.payload.catalog));
  assert.ok(Object.isFrozen(catalogSnap.payload.catalog.fr));
});

function acmeResolver() {
  return validateTransportResolver({ version: '1.0.0', operations: [{ kind: 'QUERY', name: 'get_demo_state', owner: 'acme.demo', contractVersion: '2.1.0-rc.1+build.7', scopes: ['P'], segments: ['demo', 'state'] }, { kind: 'QUERY', name: 'acme.demo.views', owner: 'acme.demo', contractVersion: '1.0.0', scopes: ['T', 'S'], segments: ['demo', 'views'] }, { kind: 'COMMAND', name: 'declare_name', owner: 'acme.demo', contractVersion: '1.0.0', scopes: ['P', 'T', 'S'], segments: ['demo', 'declare'] }, { kind: 'QUERY', name: 'demo.repeat', owner: 'acme.demo', contractVersion: '1.0.0', scopes: ['P'], segments: ['demo', 'demo'] }] });
}
function op2(kind, name) { return Object.freeze({ kind, name }); }

test('transport opaque : slash pourcent espace unicode encodes par segment', () => {
  assert.equal(TRANSPORT_RESOLVER_VERSION, '1.0.0');
  const r = defaultTransportResolver();
  assert.equal(resolveTransport(r, PLATFORM, op2('QUERY', 'users')), '/api/v1/web/platform/users');
  assert.equal(resolveTransport(r, { scope_type: 'TENANT', tenant_id: 'a/b', scope_id: null }, op2('QUERY', 'groups')), '/api/v1/web/tenants/a%2Fb/groups');
  assert.equal(resolveTransport(r, { scope_type: 'TENANT', tenant_id: 'a%b c', scope_id: null }, op2('QUERY', 'groups')), '/api/v1/web/tenants/a%25b%20c/groups');
  assert.equal(resolveTransport(r, { scope_type: 'TENANT', tenant_id: 't\u00e9\u4e2d', scope_id: null }, op2('QUERY', 'groups')), '/api/v1/web/tenants/t%C3%A9%E4%B8%AD/groups');
  assert.equal(resolveTransport(r, { scope_type: 'TENANT', tenant_id: 'x'.repeat(2000), scope_id: null }, op2('QUERY', 'groups')), '/api/v1/web/tenants/' + 'x'.repeat(2000) + '/groups');
});

test('transport : point point NUL surrogate isole refuses avant envoi', async () => {
  for (const bad of ['.', '..', '\0', '\uD800']) {
    let called = false;
    const provider = contextDouble({ scope_type: 'TENANT', tenant_id: bad, scope_id: null });
    const client = createQueryClient({ fetchJson: async () => { called = true; return okEnvelope(PLATFORM); }, contextProvider: provider });
    await rejectsWith(() => client.query('groups'), 'SHELL_ROUTE_INVALID');
    assert.equal(called, false);
  }
});

test('resolveur proprietaire fictif acme.demo : snake namespace semver prerelease', () => {
  const r = acmeResolver();
  assert.ok(Object.isFrozen(r));
  assert.ok(Object.isFrozen(r.operations));
  assert.equal(resolveTransport(r, PLATFORM, op2('QUERY', 'get_demo_state')), '/api/v1/web/platform/demo/state');
  assert.equal(resolveTransport(r, FULL_SCOPE, op2('QUERY', 'acme.demo.views')), '/api/v1/web/tenants/' + TENANT + '/scopes/' + SCOPE_ID + '/demo/views');
  assert.equal(resolveTransport(r, PLATFORM, op2('QUERY', 'demo.repeat')), '/api/v1/web/platform/demo/demo');
  assert.throws(() => validateTransportResolver({ version: '1.0.0', operations: [{ kind: 'QUERY', name: 'x', owner: 'acme.demo', contractVersion: '01.0.0', scopes: ['P'], segments: ['x'] }] }), { message: 'SHELL_ROUTE_INVALID' });
  assert.throws(() => validateTransportResolver({ version: '1.0.0', operations: [{ kind: 'QUERY', name: 'x', owner: 'acme.demo', contractVersion: '1.0.0-01', scopes: ['P'], segments: ['x'] }] }), { message: 'SHELL_ROUTE_INVALID' });
});

test('resolveur : absent collision version scopes secrets getters segments reserves refuses', async () => {
  const r = defaultTransportResolver();
  let called = false;
  const provider = contextDouble(PLATFORM);
  const client = createQueryClient({ fetchJson: async () => { called = true; return okEnvelope(PLATFORM); }, contextProvider: provider });
  await rejectsWith(() => client.query('missing_demo_state'), 'SHELL_ROUTE_INVALID');
  assert.equal(called, false);
  assert.throws(() => resolveTransport(r, PLATFORM, op2('QUERY', 'missing_demo_state')), { message: 'SHELL_ROUTE_INVALID' });
  assert.throws(() => validateTransportResolver({ version: '1.0.0', operations: [{ kind: 'QUERY', name: 'groups', owner: 'pixs.core', contractVersion: '1.0.0', scopes: ['P', 'T', 'S'], segments: ['groups'] }, { kind: 'QUERY', name: 'groups', owner: 'acme.demo', contractVersion: '1.0.0', scopes: ['P'], segments: ['demo'] }] }), { message: 'SHELL_ROUTE_INVALID' });
  assert.throws(() => validateTransportResolver({ version: '2.0.0', operations: [] }), { message: 'SHELL_ROUTE_INVALID' });
  assert.throws(() => validateTransportResolver({ version: '1.0.0', operations: [{ kind: 'QUERY', name: 'x', owner: 'acme.demo', contractVersion: 'bad', scopes: ['P'], segments: ['x'] }] }), { message: 'SHELL_ROUTE_INVALID' });
  assert.throws(() => validateTransportResolver({ version: '1.0.0', operations: [{ kind: 'QUERY', name: 'x', owner: 'acme.demo', contractVersion: '1.0.0', scopes: [], segments: ['x'] }] }), { message: 'SHELL_ROUTE_INVALID' });
  assert.throws(() => validateTransportResolver({ version: '1.0.0', operations: [{ kind: 'QUERY', name: 'x', owner: 'acme.demo', contractVersion: '1.0.0', scopes: ['P', 'P'], segments: ['x'] }] }), { message: 'SHELL_ROUTE_INVALID' });
  assert.throws(() => validateTransportResolver({ version: '1.0.0', operations: [{ kind: 'QUERY', name: 'x', owner: 'acme.demo', contractVersion: '1.0.0', scopes: ['P'], segments: ['x'], token: 't' }] }), { message: 'SHELL_ROUTE_INVALID' });
  const evil = {};
  Object.defineProperty(evil, 'kind', { get() { throw new Error('getter'); }, enumerable: true });
  evil.name = 'x'; evil.owner = 'acme.demo'; evil.contractVersion = '1.0.0'; evil.scopes = ['P']; evil.segments = ['x'];
  assert.throws(() => validateTransportResolver({ version: '1.0.0', operations: [evil] }), { message: 'SHELL_ROUTE_INVALID' });
  for (const segs of [['.'], ['..'], ['a/b'], ['a\\b'], ['a%b'], ['a?b'], ['a#b'], ['a:b'], ['a b'], ['a\u0001b'], ['auth'], ['csrf'], ['shell'], ['shell-context']]) assert.throws(() => validateTransportResolver({ version: '1.0.0', operations: [{ kind: 'QUERY', name: 'x', owner: 'acme.demo', contractVersion: '1.0.0', scopes: ['P'], segments: segs }] }), { message: 'SHELL_ROUTE_INVALID' });
});

test('resolveur : kind name hostiles sans coercition ni getter, immuable sans alias', async () => {
  const r = defaultTransportResolver();
  for (const badOp of [{ kind: 'query', name: 'users' }, { kind: 'QUERY', name: '' }, { kind: 'QUERY', name: 42 }, { kind: 42, name: 'users' }, { kind: 'QUERY' }, { name: 'users' }]) assert.throws(() => resolveTransport(r, PLATFORM, badOp), { message: 'SHELL_ROUTE_INVALID' });
  const evil = {};
  Object.defineProperty(evil, 'kind', { get() { return 'QUERY'; }, enumerable: true });
  evil.name = 'users';
  assert.throws(() => resolveTransport(r, PLATFORM, evil), { message: 'SHELL_ROUTE_INVALID' });
  let coercionCalls = 0;
  const hostile = { toString() { coercionCalls += 1; throw new Error('coercition interdite'); } };
  assert.throws(() => resolveTransport(r, PLATFORM, { kind: hostile, name: 'users' }), { message: 'SHELL_ROUTE_INVALID' });
  assert.throws(() => resolveTransport(r, PLATFORM, { kind: 'QUERY', name: hostile }), { message: 'SHELL_ROUTE_INVALID' });
  assert.equal(coercionCalls, 0);
  const frozen = defaultTransportResolver();
  assert.ok(Object.isFrozen(frozen.operations));
  assert.ok(Object.isFrozen(frozen.operations[0]));
  let mutationError = null;
  try { frozen.operations[0].segments[0] = 'mutated'; }
  catch (error) { mutationError = error; }
  assert.equal(mutationError instanceof TypeError, true);
  const src = { version: '1.0.0', operations: [{ kind: 'QUERY', name: 'get_demo_state', owner: 'acme.demo', contractVersion: '1.0.0', scopes: ['P'], segments: ['demo', 'state'] }] };
  const built = validateTransportResolver(src);
  src.operations.push({ kind: 'QUERY', name: 'evil', owner: 'acme.demo', contractVersion: '1.0.0', scopes: ['P'], segments: ['evil'] });
  src.operations[0].segments.push('mutated');
  src.operations[0].scopes.push('S');
  assert.equal(built.operations.length, 1);
  assert.deepEqual([...built.operations[0].segments], ['demo', 'state']);
  assert.deepEqual([...built.operations[0].scopes], ['P']);
  let seenPath = null;
  const provider = contextDouble(PLATFORM);
  const client = createQueryClient({ fetchJson: async (path) => { seenPath = path; return okEnvelope(PLATFORM); }, contextProvider: provider, resolver: built });
  await client.query('get_demo_state');
  assert.equal(seenPath, '/api/v1/web/platform/demo/state');
  await rejectsWith(() => client.query('evil'), 'SHELL_ROUTE_INVALID');
});

test('core P T S et 22 15 : memberships refuse, create-group nominal, usurpation refusee', async () => {
  const r = defaultTransportResolver();
  const cmds = r.operations.filter((b) => b.kind === 'COMMAND');
  const queries = r.operations.filter((b) => b.kind === 'QUERY');
  assert.equal(cmds.length, 22);
  assert.equal(queries.length, 15);
  assert.equal(resolveTransport(r, PLATFORM, op2('COMMAND', 'create-group')), '/api/v1/web/platform/commands/create-group');
  assert.equal(resolveTransport(r, TENANT_SCOPE, op2('COMMAND', 'create-group')), '/api/v1/web/tenants/' + TENANT + '/commands/create-group');
  assert.equal(resolveTransport(r, FULL_SCOPE, op2('COMMAND', 'create-group')), '/api/v1/web/tenants/' + TENANT + '/scopes/' + SCOPE_ID + '/commands/create-group');
  let called = false;
  const pPlat = contextDouble(PLATFORM);
  const cNo = createQueryClient({ fetchJson: async () => { called = true; return okEnvelope(PLATFORM); }, contextProvider: pPlat });
  await rejectsWith(() => cNo.query('memberships'), 'SHELL_ROUTE_INVALID');
  assert.equal(called, false);
  assert.throws(() => validateTransportResolver({ version: '1.0.0', operations: [{ kind: 'QUERY', name: 'groups', owner: 'pixs.core', contractVersion: '1.0.0', scopes: ['P'], segments: ['groups'] }] }), { message: 'SHELL_ROUTE_INVALID' });
  assert.throws(() => validateTransportResolver({ version: '1.0.0', operations: [{ kind: 'QUERY', name: 'groups', owner: 'pixs.core', contractVersion: '1.0.0', scopes: ['P', 'T', 'S'], segments: ['renamed'] }] }), { message: 'SHELL_ROUTE_INVALID' });
  assert.throws(() => validateTransportResolver({ version: '1.0.0', operations: [{ kind: 'QUERY', name: 'groups', owner: 'pixs.core', contractVersion: '2.0.0', scopes: ['P', 'T', 'S'], segments: ['groups'] }] }), { message: 'SHELL_ROUTE_INVALID' });
  assert.throws(() => validateTransportResolver({ version: '1.0.0', operations: [{ kind: 'QUERY', name: 'users', owner: 'acme.demo', contractVersion: '1.0.0', scopes: ['P'], segments: ['demo'] }] }), { message: 'SHELL_ROUTE_INVALID' });
});

test('bindShellApi second param utilise par query et command', async () => {
  const ports = { ShellContextProvider: (...a) => 'p', useShellContext: () => ({ state: 'ANONYMOUS', epoch: 0, scope: null }), getContextSnapshot: () => snap(PLATFORM), isCurrentSnapshot: () => true, fetchJson: async () => okEnvelope(PLATFORM), postJson: async () => okEnvelope(PLATFORM), navigate: () => 'n', invalidateScope: () => 'i', translate: (k) => k, present: (v) => v };
  const api = bindShellApi(ports, acmeResolver());
  let qPath = null;
  let cPath = null;
  const qPorts = { ShellContextProvider: () => 'p', useShellContext: () => ({ state: 'ANONYMOUS', epoch: 0, scope: null }), getContextSnapshot: () => snap(PLATFORM), isCurrentSnapshot: () => true, fetchJson: async (p) => { qPath = p; return okEnvelope(PLATFORM); }, postJson: async () => okEnvelope(PLATFORM), navigate: () => 'n', invalidateScope: () => 'i', translate: (k) => k, present: (v) => v };
  const api2 = bindShellApi(qPorts, acmeResolver());
  await api2.QueryClient.query('get_demo_state');
  assert.equal(qPath, '/api/v1/web/platform/demo/state');
  const cPorts = { ShellContextProvider: () => 'p', useShellContext: () => ({ state: 'ANONYMOUS', epoch: 0, scope: null }), getContextSnapshot: () => snap(PLATFORM), isCurrentSnapshot: () => true, fetchJson: async () => okEnvelope(PLATFORM), postJson: async (p) => { cPath = p; return okEnvelope(PLATFORM); }, navigate: () => 'n', invalidateScope: () => 'i', translate: (k) => k, present: (v) => v };
  const api3 = bindShellApi(cPorts, acmeResolver());
  const out = await api3.CommandClient.intent('declare_name', {}, { idempotencyKey: 'k-1' });
  assert.equal(out.state, 'CONFIRMED');
  assert.equal(cPath, '/api/v1/web/platform/demo/declare');
  assert.equal(api.version, '1.0.0');
});

test('params core sous params : limit cursor ref types, ordre conserve, gele', async () => {
  const provider = contextDouble(PLATFORM);
  let sent = null;
  const client = createQueryClient({ fetchJson: async (path, { snapshot, params }) => { sent = params; return okEnvelope(PLATFORM); }, contextProvider: provider });
  await client.query('users', { params: { limit: 10 } });
  assert.equal(sent.limit, 10);
  assert.ok(Object.isFrozen(sent));
  sent = null;
  await client.query('users', { params: { cursor: 'abc' } });
  assert.equal(sent.cursor, 'abc');
  assert.ok(Object.isFrozen(sent));
  sent = null;
  await client.query('users', { params: { ref: ['b', 'a'] } });
  assert.deepEqual([...sent.ref], ['b', 'a']);
  assert.ok(Object.isFrozen(sent));
  assert.ok(Object.isFrozen(sent.ref));
  for (const bad of [{ limit: 0 }, { limit: true }, { limit: '10' }, { limit: 1.5 }, { limit: Number.MAX_SAFE_INTEGER + 1 }, { cursor: '' }, { cursor: 42 }, { ref: ['a', 'a'] }, { ref: [''] }, { ref: 'a' }, { ref: ['a', 1] }, { limit: 1, unknown: 1 }]) {
    let called = false;
    const c = createQueryClient({ fetchJson: async () => { called = true; return okEnvelope(PLATFORM); }, contextProvider: provider });
    await rejectsWith(() => c.query('users', { params: bad }), 'SHELL_QUERY_INVALID');
    assert.equal(called, false);
  }
  await rejectsWith(() => client.query('users', { params: { limit: 1 }, extra: 1 }), 'SHELL_QUERY_INVALID');
  for (const badData of [{ limit: NaN }, { limit: Infinity }]) {
    let called = false;
    const c = createQueryClient({ fetchJson: async () => { called = true; return okEnvelope(PLATFORM); }, contextProvider: provider });
    await rejectsWith(() => c.query('users', { params: badData }), 'SHELL_DATA_INVALID');
    assert.equal(called, false);
  }
  const sparse = []; sparse[2] = 'x';
  {
    let called = false;
    const c = createQueryClient({ fetchJson: async () => { called = true; return okEnvelope(PLATFORM); }, contextProvider: provider });
    await rejectsWith(() => c.query('users', { params: { ref: sparse } }), 'SHELL_DATA_INVALID');
    assert.equal(called, false);
  }
  {
    let getterCalls = 0;
    const evil = {};
    Object.defineProperty(evil, 'limit', { get() { getterCalls += 1; return 1; }, enumerable: true });
    let called = false;
    const c = createQueryClient({ fetchJson: async () => { called = true; return okEnvelope(PLATFORM); }, contextProvider: provider });
    await rejectsWith(() => c.query('users', { params: evil }), 'SHELL_DATA_INVALID');
    assert.equal(called, false);
    assert.equal(getterCalls, 0);
  }
  {
    const sym = {}; sym[Symbol('s')] = 1;
    let called = false;
    const c = createQueryClient({ fetchJson: async () => { called = true; return okEnvelope(PLATFORM); }, contextProvider: provider });
    await rejectsWith(() => c.query('users', { params: sym }), 'SHELL_DATA_INVALID');
    assert.equal(called, false);
  }
});

test('params proprietaires transmis sans tri core, snapshot gele', async () => {
  let seen = null;
  const provider = contextDouble(FULL_SCOPE);
  const r = acmeResolver();
  const client = createQueryClient({ fetchJson: async (path, { snapshot, params }) => { seen = { path, params, snapshot }; return { status: 200, body: { data: [], meta: { correlation_id: 'c-1', context: FULL_SCOPE }, links: {} } }; }, contextProvider: provider, resolver: r });
  const input = { view: 'v2', name: 'n', views: ['z', 'a', 'z'] };
  const body = await client.query('acme.demo.views', { params: input });
  assert.ok(body !== undefined);
  assert.equal(seen.path, '/api/v1/web/tenants/' + TENANT + '/scopes/' + SCOPE_ID + '/demo/views');
  assert.deepEqual([...seen.params.views], ['z', 'a', 'z']);
  assert.ok(Object.isFrozen(seen.snapshot));
  assert.ok(Object.isFrozen(seen.params));
  assert.deepEqual(input.views, ['z', 'a', 'z']);
  assert.ok(Object.isFrozen(seen.params.views));
  assert.ok(seen.params.views !== input.views);
  input.views.push('plus-tard');
  assert.deepEqual([...seen.params.views], ['z', 'a', 'z']);
});

