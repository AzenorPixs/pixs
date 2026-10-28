// Tests composition-runtime : doubles explicites, vrais Query/CommandClient, aucun réseau en fabrique.
import test from 'node:test';
import { createPresentationAdapter } from '../src/shell/presentation-adapter-v1.js';
import assert from 'node:assert/strict';
import { createCompositionRuntime } from '../src/shell/composition-runtime-v1.js';
import { defaultTransportResolver, validateShellContext } from '../src/shell/api-v1.js';
import { createShellExtensionPoints } from '../src/shell/composition-descriptor-v1.js';

const UUID7 = '0193f5e2-7a1b-7c3d-8e4f-9a0b1c2d3e4f';
const keyOf = (owner, id) => JSON.stringify([owner, id]);
const clone = (v) => JSON.parse(JSON.stringify(v));

function limits() {
  return {
    maxNodes: 1024, maxDepth: 64, maxChildren: 32, maxTextLength: 1024,
    maxParams: 16, maxFields: 32, maxBindings: 64, maxDataNodes: 100000,
    maxBodyDepth: 16, maxBodyNodes: 1024,
  };
}

function catalogFor(owner) {
  const t = (s) => `${owner}.${s}`;
  return {
    en: {
      [t('title')]: 'Title', [t('msg')]: 'Hello {name}', [t('form')]: 'Form',
      [t('username')]: 'Username', [t('submit')]: 'Submit', [t('flag')]: 'Flag',
      [t('count')]: 'Count', [t('tags')]: 'Tags', [t('rows')]: 'Rows',
    },
    fr: {
      [t('title')]: 'Titre', [t('msg')]: 'Bonjour {name}', [t('form')]: 'Formulaire',
      [t('username')]: 'Identifiant', [t('submit')]: 'Envoyer', [t('flag')]: 'Drapeau',
      [t('count')]: 'Compteur', [t('tags')]: 'Etiquettes', [t('rows')]: 'Lignes',
    },
  };
}

function makeFixture(scope) {
  let base = clone(scope ?? { scope_type: 'PLATFORM', tenant_id: null, scope_id: null });
  let epoch = 0, sessionId = UUID7, stateName = 'ACTIVE', unsubscribeThrows = false;
  const listeners = new Set(), fetchCalls = [], postCalls = [], fetchQueue = [], postQueue = [];
  const fetchWaiters = [], postWaiters = [];
  let fetchIndex = 0, postIndex = 0;
  let resolver = { version: '1.0.0', operations: [
    ...defaultTransportResolver().operations.map(clone),
    { kind: 'QUERY', name: 'demo-items', owner: 'acme.demo', contractVersion: '1.0.0', scopes: ['P', 'T', 'S'], segments: ['demo', 'items'] },
    { kind: 'COMMAND', name: 'demo-create', owner: 'acme.demo', contractVersion: '1.0.0', scopes: ['P', 'T', 'S'], segments: ['demo', 'create'] },
  ] };
  const state = () => validateShellContext(stateName === 'ACTIVE' ? {
    state: 'ACTIVE', epoch, scope: clone(base), identity_ref: 'fixture-identity', session_id: sessionId,
    category: 'ADMIN', facade: 'WEB', authentication_time: '2026-01-01T00:00:00Z', expires_at: '2026-12-31T00:00:00Z',
    identity_assurance: 'VERIFIED', authentication_assurance: 'MULTI_FACTOR',
    ui_permissions: { status: 'VERIFIED', policy_version: '1', evaluated_at: '2026-01-01T00:00:00Z',
      items: [{ action_id: 'voir', resource_id: 'fixture-resource', allowed: true }] },
  } : { state: stateName, epoch, scope: null });
  const emit = kind => { epoch += 1; for (const fn of [...listeners]) fn({ kind }); };
  const notifyWaiters = (waiters, count) => {
    for (const waiter of [...waiters]) if (count >= waiter.count) {
      waiters.splice(waiters.indexOf(waiter), 1); waiter.resolve();
    }
  };
  const wait = (waiters, count, current) => current >= count ? Promise.resolve() : new Promise(resolve => waiters.push({ count, resolve }));
  const session = {
    getState: state, getResolver: () => resolver,
    getContextSnapshot: () => {
      if (stateName !== 'ACTIVE') throw Object.assign(new Error('SESSION_NOT_ACTIVE'), { code: 'SESSION_NOT_ACTIVE' });
      return { scope: clone(base), epoch };
    },
    isCurrentSnapshot: snapshot => stateName === 'ACTIVE' && snapshot?.epoch === epoch && JSON.stringify(snapshot.scope) === JSON.stringify(base),
    subscribe: fn => { listeners.add(fn); return () => { if (unsubscribeThrows) throw new Error('fixture-unsubscribe'); listeners.delete(fn); }; },
    fetchJson: (path, opts) => {
      fetchCalls.push({ path, opts: clone(opts) });
      return new Promise((resolve, reject) => { fetchQueue.push({ resolve, reject }); notifyWaiters(fetchWaiters, fetchCalls.length); });
    },
    postJson: (path, body, opts) => {
      postCalls.push({ path, body: clone(body), opts: clone(opts) });
      return new Promise((resolve, reject) => { postQueue.push({ resolve, reject }); notifyWaiters(postWaiters, postCalls.length); });
    },
    invalidateScope: () => emit('DATA'),
  };
  return {
    session, fetchCalls, postCalls,
    waitForFetch: () => wait(fetchWaiters, ++fetchIndex, fetchCalls.length),
    waitForPost: () => wait(postWaiters, ++postIndex, postCalls.length),
    resolveFetchNext: value => fetchQueue.shift().resolve(clone(value)),
    rejectFetchNext: error => fetchQueue.shift().reject(error),
    resolvePostNext: value => postQueue.shift().resolve(clone(value)),
    rejectPostNext: error => postQueue.shift().reject(error),
    advance: (kind = 'DATA') => emit(kind),
    setSession: value => { sessionId = value; emit('CONTEXT'); },
    setScope: value => { base = clone(value); emit('CONTEXT'); },
    setState: value => { stateName = value; emit('CONTEXT'); },
    setResolver: value => { resolver = clone(value); },
    failUnsubscribe: () => { unsubscribeThrows = true; },
    listenerCount: () => listeners.size,
  };
}

function spy() {
  const prints = new Map();
  let n = 0;
  let ids = 0;
  return {
    translated: [],
    navigated: [],
    errors: [],
    translate: function (k) { this.translated.push(k); return String(k); },
    navigate: function (path, params) { this.navigated.push({ path, params: clone(params ?? {}) }); return null; },
    onError: function (c) { this.errors.push(c); },
    createId: () => `id-${++ids}`,
    fingerprint: async (s) => {
      const k = String(s);
      if (!prints.has(k)) { n += 1; prints.set(k, n.toString(16).padStart(64, '0')); }
      return prints.get(k);
    },
  };
}

function okData(scope, data) {
  return { status: 200, body: { data: data ?? { items: [] }, meta: { correlation_id: 'corr-1', context: clone(scope) }, links: { self: '/x' } } };
}
function errBody(scope, status, code) {
  return { status, body: { error_code: code, message: 'refuse', details: {}, correlation_id: 'c-1' } };
}

function contrib(owner, id, type, point, payload, scope = 'PUBLIC', perms = []) {
  return { owner, id, type, activation_scope: scope, display_permissions: [...perms], point, payload: clone(payload) };
}
function graphOf(contributions, edges = []) {
  return { schema: 'pixs.frontend.contribution-graph/1.0.0', blocked: false, contributions: clone(contributions), contributionEdges: clone(edges) };
}
function i18n(owner) {
  return contrib(owner, `${owner}.i18n`, 'TRANSLATION', 'pixs.shell.translations', { catalog: catalogFor(owner) });
}
function page(owner, local = 'page') {
  return contrib(owner, `${owner}.${local}`, 'PAGE', 'pixs.shell.pages', { export: 'Page' });
}
function factoryFor(root) {
  return () => ({ schema: 'pixs.presentation/1.0.0', root: clone(root) });
}
function simpleRoot(owner) {
  return {
    kind: 'section', variant: 'panel', props: {}, children: [
      { kind: 'heading', variant: 'page', props: { key: `${owner}.title`, params: {} }, children: [] },
      { kind: 'text', variant: 'body', props: { key: `${owner}.msg`, params: { name: 'A' } }, children: [] },
    ],
  };
}
function formRoot(owner) {
  return {
    kind: 'form', variant: 'stack',
    props: { id: 'create', key: `${owner}.form`, params: {}, intent: { command: 'demo-create', body: { payload: { username: null } }, bindings: [{ field: 'username', path: ['payload', 'username'] }] } },
    children: [
      { kind: 'field', variant: 'text', props: { name: 'username', key: `${owner}.username`, params: {}, required: true, initial: '' }, children: [] },
      { kind: 'button', variant: 'primary', props: { id: 'submit', key: `${owner}.submit`, params: {}, submit: true, intent: null }, children: [] },
      { kind: 'status', variant: 'command', props: { for: 'create' }, children: [] },
    ],
  };
}
function queryRoot(owner) {
  return {
    kind: 'section', variant: 'stack', props: {}, children: [
      { kind: 'button', variant: 'secondary', props: { id: 'run', key: `${owner}.submit`, params: {}, submit: false, intent: { query: 'demo-items', params: {}, bindings: [] } }, children: [] },
      { kind: 'status', variant: 'query', props: { for: 'run' }, children: [] },
    ],
  };
}
function makeRuntime(fixture, graph, factories, sp) {
  const s = sp ?? spy();
  const rt = createCompositionRuntime({
    graph, factories, session: fixture.session,
    translate: s.translate.bind(s), navigate: s.navigate.bind(s),
    presentationLimits: limits(), points: createShellExtensionPoints(),
    createId: s.createId, fingerprint: s.fingerprint, onError: s.onError.bind(s),
  });
  return { rt, spies: s };
}
function refused(fn) {
  let e;
  try { fn(); } catch (cause) { e = cause; }
  assert.ok(e instanceof Error);
  assert.equal(typeof e.code, 'string');
  return e;
}

async function rejected(promise, code) {
  let error;
  try { await promise; } catch (cause) { error = cause; }
  assert.ok(error instanceof Error);
  if (code !== undefined) assert.equal(error.code, code);
  return error;
}

test('construction : options, graphe, fabriques et points invalides refusés', () => {
  const fx = makeFixture();
  const g = graphOf([i18n('acme.demo'), page('acme.demo')]);
  let factoryCalls = 0;
  const fac = { [keyOf('acme.demo', 'acme.demo.page')]: () => { factoryCalls += 1; return { schema: 'pixs.presentation/1.0.0', root: simpleRoot('acme.demo') }; } };
  const good = makeRuntime(fx, g, fac); assert.equal(factoryCalls, 0); good.rt.dispose();
  refused(() => createCompositionRuntime({}));
  let getters = 0;
  const badOptions = {};
  Object.defineProperty(badOptions, 'graph', { get() { getters += 1; return g; } });
  refused(() => createCompositionRuntime(badOptions));
  assert.equal(getters, 0);
  refused(() => makeRuntime(fx, { ...g, blocked: true }, fac));
  const empty = makeRuntime(fx, graphOf([]), {}); empty.rt.dispose();
  refused(() => makeRuntime(fx, g, {}));
  refused(() => makeRuntime(fx, g, { [keyOf('acme.demo', 'acme.demo.page')]: 'non-fonction' }));
  refused(() => createCompositionRuntime({
    graph: g, factories: fac, session: fx.session, translate: () => 'x', navigate: () => null,
    presentationLimits: limits(), points: { points: {}, metadata: { version: '1.0.0', schema: 'x' } },
    createId: () => 'a', fingerprint: async () => '0'.repeat(64), onError: () => {},
  }));
});

test('visibilite : PUBLIC, AUTH, PLATEFORME, TENANT et permissions sans droit', () => {
  for (const [scope, vis, hidden] of [
    [{ scope_type: 'PLATFORM', tenant_id: null, scope_id: null }, ['pub', 'auth', 'plat'], ['ten', 'tenScope']],
    [{ scope_type: 'TENANT', tenant_id: 't1', scope_id: null }, ['pub', 'auth', 'ten', 'tenScope'], ['plat']],
    [{ scope_type: 'TENANT', tenant_id: 't1', scope_id: 's1' }, ['pub', 'auth', 'ten', 'tenScope'], ['plat']],
  ]) {
    const fx = makeFixture(scope);
    const mk = (local, act, perms = []) => contrib('acme.demo', `acme.demo.${local}`, 'PAGE', 'pixs.shell.pages', { export: 'P' }, act, perms);
    const parts = [i18n('acme.demo'), mk('pub', 'PUBLIC'), mk('auth', 'AUTHENTICATED'), mk('plat', 'PLATFORM_SCOPED'), mk('ten', 'TENANT_SCOPED'), mk('tenScope', 'TENANT_SCOPED'), mk('gated', 'PUBLIC', ['voir'])];
    const g = graphOf(parts);
    const fac = Object.fromEntries(parts.filter((c) => c.type === 'PAGE').map((c) => [keyOf(c.owner, c.id), factoryFor(simpleRoot('acme.demo'))]));
    const { rt } = makeRuntime(fx, g, fac);
    assert.deepEqual(rt.visibleNavigation(), []);
    for (const local of vis) assert.ok(rt.renderContribution('acme.demo', `acme.demo.${local}`));
    for (const local of hidden) assert.equal(refused(() => rt.renderContribution('acme.demo', `acme.demo.${local}`)).code, 'COMPOSITION_UNAVAILABLE');
    assert.equal(refused(() => rt.renderContribution('acme.demo', 'acme.demo.gated')).code, 'COMPOSITION_UNAVAILABLE');
    fx.setState('ANONYMOUS');
    assert.ok(rt.renderContribution('acme.demo', 'acme.demo.pub'));
    assert.equal(refused(() => rt.renderContribution('acme.demo', 'acme.demo.auth')).code, 'COMPOSITION_UNAVAILABLE');
    rt.dispose();
  }
});

test('isolation : deux proprietaires avec meme action locale', async () => {
  const fx = makeFixture(), owners = ['acme.a', 'acme.b'];
  const g = graphOf(owners.flatMap(owner => [i18n(owner), contrib(owner, owner + '.form', 'FORM', 'pixs.shell.forms', { export: 'F' })]));
  const fac = Object.fromEntries(owners.map(owner => [keyOf(owner, owner + '.form'), factoryFor(formRoot(owner))]));
  const { rt } = makeRuntime(fx, g, fac);
  const a = rt.renderContribution('acme.a', 'acme.a.form'), b = rt.renderContribution('acme.b', 'acme.b.form');
  const intent = formRoot('acme.a').props.intent;
  const pending = rt.submit('create', intent, { username: 'alice' }, a.context);
  await fx.waitForPost();
  assert.equal(rt.getState('acme.a', 'acme.a.form').actions.create.phase, 'PENDING');
  assert.deepEqual(rt.getState('acme.b', 'acme.b.form'), { actions: {}, fields: {} });
  fx.resolvePostNext(okData(fx.session.getState().scope, { created: 'alice' }));
  await pending;
  assert.equal(rt.getState('acme.a', 'acme.a.form').actions.create.response.data.created, 'alice');
  assert.equal(rt.getState('acme.a', 'acme.a.form').fields.create.username, 'alice');
  assert.deepEqual(rt.getState('acme.b', 'acme.b.form'), { actions: {}, fields: {} });
  assert.equal(rt.actionState('create', b.context).state, 'IDLE');
  rt.dispose();
});
test('requete : PENDING puis LOADED, fabrique voit reponse gelee et cache actualise', async () => {
  const fx = makeFixture();
  const owner = 'acme.demo';
  const g = graphOf([i18n(owner), page(owner)]);
  let seen = null;
  const fac = {
    [keyOf(owner, `${owner}.page`)]: (input) => { seen = input.state; return { schema: 'pixs.presentation/1.0.0', root: queryRoot(owner) }; },
  };
  const { rt } = makeRuntime(fx, g, fac);
  const first = rt.renderContribution(owner, `${owner}.page`);
  assert.equal(rt.actionState('run', first.context).state, 'IDLE');
  const scope = fx.session.getState().scope;
  const pending = rt.submit('run', { query: 'demo-items', params: {}, bindings: [] }, {}, first.context);
  await fx.waitForFetch();
  assert.equal(rt.actionState('run', first.context).state, 'PENDING');
  assert.equal(fx.fetchCalls.length, 1);
  fx.resolveFetchNext(okData(scope, { items: [{ n: 1 }] }));
  const done = await pending;
  assert.equal(done.phase, 'LOADED');
  assert.deepEqual(done.response.data, { items: [{ n: 1 }] });
  const second = rt.renderContribution(owner, `${owner}.page`);
  assert.equal(second.context.owner, owner);
  assert.equal(seen.actions.run.phase, 'LOADED');
  assert.deepEqual(seen.actions.run.response.data, { items: [{ n: 1 }] });
  assert.equal(Object.isFrozen(seen.actions.run.response.data.items[0]), true);
  rt.dispose();
});

test('commande : CONFIRMED a 200 et REJECTED a 4xx', async () => {
  const fx = makeFixture();
  const owner = 'acme.demo';
  const g = graphOf([i18n(owner), contrib(owner, `${owner}.form`, 'FORM', 'pixs.shell.forms', { export: 'F' })]);
  const fac = { [keyOf(owner, `${owner}.form`)]: factoryFor(formRoot(owner)) };
  const { rt } = makeRuntime(fx, g, fac);
  const view = rt.renderContribution(owner, `${owner}.form`);
  const scope = fx.session.getState().scope;
  const p1 = rt.submit('create', { command: 'demo-create', body: { payload: { username: null } }, bindings: [{ field: 'username', path: ['payload', 'username'] }] }, { username: 'alice' }, view.context);
  await fx.waitForPost();
  fx.resolvePostNext(okData(scope, { created: true }));
  assert.equal((await p1).phase, 'CONFIRMED');
  const view2 = rt.renderContribution(owner, `${owner}.form`);
  const p2 = rt.submit('create', { command: 'demo-create', body: { payload: { username: null } }, bindings: [{ field: 'username', path: ['payload', 'username'] }] }, { username: 'bob' }, view2.context);
  await fx.waitForPost();
  fx.resolvePostNext(errBody(scope, 400, 'E_BAD'));
  assert.equal((await p2).phase, 'REJECTED');
  assert.equal(rt.getState(owner, `${owner}.form`).actions.create.error_code, 'E_BAD');
  rt.dispose();
});

test('commande : panne et 5xx donnent UNKNOWN rejouable a cle identique', async () => {
  for (const failure of ['network', '503']) {
    const fx = makeFixture(), owner = 'acme.demo';
    const g = graphOf([i18n(owner), contrib(owner, owner + '.form', 'FORM', 'pixs.shell.forms', { export: 'F' })]);
    const { rt } = makeRuntime(fx, g, { [keyOf(owner, owner + '.form')]: factoryFor(formRoot(owner)) });
    const view = rt.renderContribution(owner, owner + '.form'), intent = formRoot(owner).props.intent;
    const pending = rt.submit('create', intent, { username: 'alice' }, view.context);
    const classified = failure === 'network' ? rejected(pending, 'SHELL_COMMAND_UNKNOWN') : pending;
    await fx.waitForPost();
    const key = fx.postCalls[0].opts.idempotencyKey;
    if (failure === 'network') fx.rejectPostNext(new Error('fixture-network'));
    else fx.resolvePostNext(errBody(fx.session.getState().scope, 503, 'acme.demo.UNAVAILABLE'));
    await classified;
    assert.equal(rt.getState(owner, owner + '.form').actions.create.phase, 'UNKNOWN');
    const retry = rt.submit('create', intent, { username: 'alice' }, view.context);
    await fx.waitForPost();
    assert.equal(fx.postCalls[1].opts.idempotencyKey, key);
    assert.deepEqual(fx.postCalls[1].body, fx.postCalls[0].body);
    fx.resolvePostNext(okData(fx.session.getState().scope, { created: true }));
    assert.equal((await retry).phase, 'CONFIRMED');
    rt.dispose();
  }
});
test('rejeu : autre contenu ou session bloque, query et 4xx ne resolvent pas UNKNOWN', async () => {
  const fx = makeFixture(), owner = 'acme.demo', tree = formRoot(owner);
  tree.children.push(...queryRoot(owner).children);
  const g = graphOf([i18n(owner), contrib(owner, owner + '.form', 'FORM', 'pixs.shell.forms', { export: 'F' })]);
  const { rt } = makeRuntime(fx, g, { [keyOf(owner, owner + '.form')]: factoryFor(tree) });
  const view = rt.renderContribution(owner, owner + '.form'), intent = tree.props.intent;
  const first = rt.submit('create', intent, { username: 'alice' }, view.context);
  await fx.waitForPost();
  fx.resolvePostNext(errBody(fx.session.getState().scope, 503, 'acme.demo.UNKNOWN'));
  assert.equal((await first).phase, 'UNKNOWN');
  await rejected(rt.submit('create', intent, { username: 'bob' }, view.context), 'COMPOSITION_RETRY_MISMATCH');
  assert.equal(fx.postCalls.length, 1);
  const read = rt.submit('run', queryRoot(owner).children[0].props.intent, {}, view.context);
  await fx.waitForFetch(); fx.resolveFetchNext(okData(fx.session.getState().scope, { items: [] }));
  assert.equal((await read).phase, 'LOADED');
  assert.equal(rt.getState(owner, owner + '.form').actions.create.phase, 'UNKNOWN');
  const retry = rt.submit('create', intent, { username: 'alice' }, view.context);
  await fx.waitForPost();
  fx.resolvePostNext(errBody(fx.session.getState().scope, 400, 'acme.demo.REFUSED'));
  assert.equal((await retry).phase, 'UNKNOWN');
  assert.equal(fx.postCalls[0].opts.idempotencyKey, fx.postCalls[1].opts.idempotencyKey);
  fx.setSession('0193f5e2-7a1b-7c3d-8e4f-9a0b1c2d3e40');
  const fresh = rt.renderContribution(owner, owner + '.form');
  await rejected(rt.submit('create', intent, { username: 'alice' }, fresh.context), 'COMPOSITION_RETRY_CONTEXT_MISMATCH');
  assert.equal(fx.postCalls.length, 2);
  rt.dispose();
});
test('double soumission PENDING refusee', async () => {
  const fx = makeFixture();
  const owner = 'acme.demo';
  const g = graphOf([i18n(owner), contrib(owner, `${owner}.form`, 'FORM', 'pixs.shell.forms', { export: 'F' })]);
  const fac = { [keyOf(owner, `${owner}.form`)]: factoryFor(formRoot(owner)) };
  const { rt } = makeRuntime(fx, g, fac);
  const view = rt.renderContribution(owner, `${owner}.form`);
  const intent = { command: 'demo-create', body: { payload: { username: null } }, bindings: [{ field: 'username', path: ['payload', 'username'] }] };
  const p1 = rt.submit('create', clone(intent), { username: 'alice' }, view.context);
  await fx.waitForPost();
  await assert.rejects(rt.submit('create', clone(intent), { username: 'alice' }, view.context), /COMPOSITION_PENDING/);
  fx.resolvePostNext(okData(fx.session.getState().scope, {}));
  await p1;
  rt.dispose();
});

test('champs : false, entier, null, listes, enregistrements, LF et ordre valides', async () => {
  const fx = makeFixture();
  const owner = 'acme.demo';
  const cols = [
    { name: 'label', key: `${owner}.username`, params: {}, required: true },
    { name: 'note', key: `${owner}.submit`, params: {}, required: false },
  ];
  const root = {
    kind: 'form', variant: 'stack',
    props: {
      id: 'big', key: `${owner}.form`, params: {},
      intent: {
        command: 'demo-create',
        body: { payload: { a: null, b: null, c: null, d: null, e: null } },
        bindings: [
          { field: 'flag', path: ['payload', 'a'] }, { field: 'count', path: ['payload', 'b'] },
          { field: 'alias', path: ['payload', 'c'] }, { field: 'tags', path: ['payload', 'd'] },
          { field: 'rows', path: ['payload', 'e'] },
        ],
      },
    },
    children: [
      { kind: 'field', variant: 'boolean', props: { name: 'flag', key: `${owner}.flag`, params: {}, required: true, initial: false }, children: [] },
      { kind: 'field', variant: 'integer', props: { name: 'count', key: `${owner}.count`, params: {}, required: false, initial: null, minimum: 1, maximum: 9 }, children: [] },
      { kind: 'field', variant: 'text', props: { name: 'alias', key: `${owner}.username`, params: {}, required: false, initial: '' }, children: [] },
      { kind: 'field', variant: 'string-list', props: { name: 'tags', key: `${owner}.tags`, params: {}, required: false, initial: [], minItems: 0, maxItems: 3, itemRequired: false }, children: [] },
      { kind: 'field', variant: 'record-list', props: { name: 'rows', key: `${owner}.rows`, params: {}, required: false, initial: [], minItems: 0, maxItems: 2, columns: cols }, children: [] },
      { kind: 'button', variant: 'primary', props: { id: 'go', key: `${owner}.submit`, params: {}, submit: true, intent: null }, children: [] },
      { kind: 'status', variant: 'command', props: { for: 'big' }, children: [] },
    ],
  };
  const g = graphOf([i18n(owner), contrib(owner, `${owner}.form`, 'FORM', 'pixs.shell.forms', { export: 'F' })]);
  const fac = { [keyOf(owner, `${owner}.form`)]: factoryFor(root) };
  const { rt } = makeRuntime(fx, g, fac);
  const view = rt.renderContribution(owner, `${owner}.form`);
  assert.ok(view.tree);
  const values = { flag: false, count: 7, alias: '', tags: ['b' + String.fromCharCode(10), 'a', 'b' + String.fromCharCode(10)],
    rows: [{ label: 'x', note: 'n' + String.fromCharCode(10) }, { label: 'x', note: 'n' + String.fromCharCode(10) }] };
  const expected = clone(values);
  const pending = rt.submit('big', root.props.intent, values, view.context);
  values.tags.push('changed'); values.rows[0].note = 'changed';
  await fx.waitForPost();
  assert.deepEqual(fx.postCalls[0].body.payload, { a: false, b: 7, c: '', d: expected.tags, e: expected.rows });
  fx.resolvePostNext(okData(fx.session.getState().scope, {})); await pending;
  const second = rt.submit('big', root.props.intent, { flag: false, count: null, alias: '', tags: [], rows: [] }, view.context);
  await fx.waitForPost();
  assert.equal(fx.postCalls[1].body.payload.b, null);
  fx.resolvePostNext(okData(fx.session.getState().scope, {})); await second;
  rt.dispose();
});

test('champs invalides refuses avant tout envoi', async () => {
  const fx = makeFixture();
  const owner = 'acme.demo';
  const g = graphOf([i18n(owner), contrib(owner, `${owner}.form`, 'FORM', 'pixs.shell.forms', { export: 'F' })]);
  const fac = { [keyOf(owner, `${owner}.form`)]: factoryFor(formRoot(owner)) };
  const { rt } = makeRuntime(fx, g, fac);
  const view = rt.renderContribution(owner, `${owner}.form`);
  const intent = { command: 'demo-create', body: { payload: { username: null } }, bindings: [{ field: 'username', path: ['payload', 'username'] }] };
  await rejected(rt.submit('create', clone(intent), { username: '' }, view.context), 'PRESENTATION_FIELD_INVALID');
  await assert.rejects(rt.submit('create', { command: 'demo-create', body: {}, bindings: [] }, {}, view.context), /COMPOSITION_INTENT_STALE/);
  let read = 0;
  const fields = {};
  Object.defineProperty(fields, 'username', { get() { read += 1; return 'bad'; }, enumerable: true });
  await rejected(rt.submit('create', intent, fields, view.context), 'COMPOSITION_DATA_INVALID');
  assert.equal(read, 0); assert.equal(fx.postCalls.length, 0);
  rt.dispose();
});

test('INVALID via reportError sans ecraser PENDING ou UNKNOWN', async () => {
  const fx = makeFixture(), owner = 'acme.demo', id = owner + '.form';
  const g = graphOf([i18n(owner), contrib(owner, id, 'FORM', 'pixs.shell.forms', { export: 'F' })]);
  const { rt, spies } = makeRuntime(fx, g, { [keyOf(owner, id)]: factoryFor(formRoot(owner)) });
  const view = rt.renderContribution(owner, id), intent = formRoot(owner).props.intent;
  rt.reportError('create', 'fixture.INPUT', view.context);
  assert.equal(rt.actionState('create', view.context).state, 'INVALID');
  const pending = rt.submit('create', intent, { username: 'alice' }, view.context);
  await fx.waitForPost();
  rt.reportError('create', 'fixture.PENDING', view.context);
  assert.equal(rt.actionState('create', view.context).state, 'PENDING');
  fx.resolvePostNext(errBody(fx.session.getState().scope, 503, 'fixture.UNKNOWN'));
  assert.equal((await pending).phase, 'UNKNOWN');
  rt.reportError('create', 'fixture.UNKNOWN', view.context);
  assert.equal(rt.actionState('create', view.context).state, 'UNKNOWN');
  assert.deepEqual(spies.errors, ['fixture.INPUT', 'fixture.PENDING', 'fixture.UNKNOWN']);
  rt.dispose();
});
test('purge : avant notification, reponses anciennes ignorees et barrieres gardees', async () => {
  const fx = makeFixture(), owner = 'acme.demo', id = owner + '.page', routeId = owner + '.route';
  const tree = { kind: 'section', variant: 'stack', props: {}, children: [formRoot(owner), queryRoot(owner)] };
  const g = graphOf([i18n(owner), page(owner), contrib(owner, routeId, 'ROUTE', 'pixs.shell.routes', { path: '/demo', mode: 'CSR', page: 'P' })]);
  const { rt } = makeRuntime(fx, g, { [keyOf(owner, id)]: factoryFor(tree), [keyOf(owner, routeId)]: factoryFor(tree) });
  const view = rt.renderContribution(owner, id), queryIntent = queryRoot(owner).children[0].props.intent;
  const pendingQuery = rt.submit('run', queryIntent, {}, view.context);
  await fx.waitForFetch();
  let purgedBeforeNotify = false;
  const off = rt.subscribe(event => {
    if (event.kind === 'SESSION') {
      assert.equal(Object.hasOwn(rt.getState(owner, id).actions, 'run'), false);
      assert.deepEqual(rt.getState(owner, id).fields, {});
      purgedBeforeNotify = true;
    }
  });
  fx.advance('DATA');
  assert.equal(purgedBeforeNotify, true); off();
  fx.resolveFetchNext(okData(fx.session.getState().scope, { items: ['old'] }));
  assert.equal(await pendingQuery, null);
  const fresh = rt.renderContribution(owner, id);
  const pendingCommand = rt.submit('create', formRoot(owner).props.intent, { username: 'alice' }, fresh.context);
  await fx.waitForPost(); fx.advance('CONTEXT');
  fx.resolvePostNext(okData(fx.session.getState().scope, { created: true }));
  assert.equal((await pendingCommand).phase, 'UNKNOWN');
  assert.equal(Object.hasOwn(rt.getState(owner, id).actions.create, 'response'), false);
  assert.deepEqual(rt.getState(owner, id).fields, {});
  rt.openRoute(owner, routeId, {}); rt.leaveRoute();
  assert.equal(rt.getState(owner, id).actions.create.phase, 'UNKNOWN');
  rt.dispose();
});
test('resolution : resolver courant change, liaison absente refuse sans envoi', async () => {
  const fx = makeFixture(), owner = 'acme.demo', id = owner + '.page';
  const g = graphOf([i18n(owner), page(owner)]);
  const { rt } = makeRuntime(fx, g, { [keyOf(owner, id)]: factoryFor(queryRoot(owner)) });
  const view = rt.renderContribution(owner, id), intent = queryRoot(owner).children[0].props.intent;
  const first = rt.submit('run', intent, {}, view.context);
  await fx.waitForFetch();
  assert.equal(fx.fetchCalls[0].path, '/api/v1/web/platform/demo/items');
  fx.resolveFetchNext(okData(fx.session.getState().scope, {})); await first;
  const changed = clone(fx.session.getResolver());
  changed.operations.find(binding => binding.name === 'demo-items').segments = ['demo', 'v2-items'];
  fx.setResolver(changed);
  const second = rt.submit('run', intent, {}, view.context);
  await fx.waitForFetch();
  assert.equal(fx.fetchCalls[1].path, '/api/v1/web/platform/demo/v2-items');
  fx.resolveFetchNext(okData(fx.session.getState().scope, {})); await second;
  fx.setResolver({ version: '1.0.0', operations: defaultTransportResolver().operations });
  await rejected(rt.submit('run', intent, {}, view.context), 'SHELL_ROUTE_INVALID');
  assert.equal(fx.fetchCalls.length, 2); assert.equal(fx.postCalls.length, 0);
  rt.dispose();
});
test('actions retirees inexecutable, composants et slots seulement declares', async () => {
  const fx = makeFixture(), owner = 'acme.demo', id = owner + '.page';
  let withAction = true;
  const card = contrib(owner, owner + '.card', 'COMPONENT', 'pixs.shell.components', { export: 'C' });
  const slot = contrib(owner, owner + '.zone', 'UI_SLOT', 'pixs.shell.main', { slot: 'pixs.shell.main', export: 'S' });
  const g = graphOf([i18n(owner), page(owner), card, slot], [[owner, id, owner, card.id]]);
  const { rt } = makeRuntime(fx, g, {
    [keyOf(owner, id)]: () => ({ schema: 'pixs.presentation/1.0.0', root: withAction ? queryRoot(owner) : simpleRoot(owner) }),
    [keyOf(owner, card.id)]: factoryFor(simpleRoot(owner)),
    [keyOf(owner, slot.id)]: factoryFor(simpleRoot(owner)),
  });
  const view = rt.renderContribution(owner, id);
  assert.deepEqual(rt.slotContributions('pixs.shell.main').map(item => item.id), [slot.id]);
  assert.ok(rt.renderComponent(view.context, owner, card.id).tree);
  assert.equal(refused(() => rt.renderComponent(view.context, owner, 'acme.demo.absent')).code, 'COMPOSITION_COMPONENT_UNAVAILABLE');
  assert.equal(refused(() => rt.slotContributions('pixs.shell.main', view.context)).code, 'COMPOSITION_SLOT_UNAVAILABLE');
  assert.equal(refused(() => rt.slotContributions('pixs.shell.inconnu')).code, 'COMPOSITION_POINT_UNKNOWN');
  withAction = false; rt.refreshPresentation(); rt.renderContribution(owner, id);
  await rejected(rt.submit('run', queryRoot(owner).children[0].props.intent, {}, view.context), 'COMPOSITION_ACTION_UNAVAILABLE');
  assert.equal(fx.fetchCalls.length, 0);
  rt.dispose();
});
test('fabrique sans effets reseau navigation ou invalidation, vrai cycle refuse', () => {
  const owner = 'acme.demo', id = owner + '.page', g = graphOf([i18n(owner), page(owner)]);
  for (const effect of [
    api => api.QueryClient.query('demo-items', { params: {} }),
    api => api.CommandClient.intent('demo-create', {}, { idempotencyKey: 'fixture' }),
    api => api.navigate('/login'),
    api => api.invalidateScope(),
  ]) {
    const fx = makeFixture();
    const { rt, spies } = makeRuntime(fx, g, { [keyOf(owner, id)]: input => {
      effect(input.api); return { schema: 'pixs.presentation/1.0.0', root: simpleRoot(owner) };
    } });
    const error = refused(() => rt.renderContribution(owner, id));
    assert.equal(error.code, 'COMPOSITION_FACTORY_FAILED');
    assert.equal(error.cause.code, 'COMPOSITION_RENDER_EFFECT');
    assert.equal(fx.fetchCalls.length, 0); assert.equal(fx.postCalls.length, 0);
    assert.deepEqual(spies.navigated, []); assert.equal(rt.getVersion(), 0);
    rt.dispose();
  }
  const cyc = graphOf([i18n(owner), page(owner, 'a'), page(owner, 'b')], [
    [owner, owner + '.a', owner, owner + '.b'], [owner, owner + '.b', owner, owner + '.a'],
  ]);
  assert.equal(refused(() => makeRuntime(makeFixture(), cyc, {
    [keyOf(owner, owner + '.a')]: factoryFor(simpleRoot(owner)), [keyOf(owner, owner + '.b')]: factoryFor(simpleRoot(owner)),
  })).code, 'COMPOSITION_GRAPH_CYCLE');
});
test('chaine 512 admise, version numerique, ecoutes et dispose', () => {
  const fx = makeFixture();
  const owner = 'acme.demo';
  const parts = [i18n(owner)];
  const edges = [];
  let prev = null;
  for (let i = 0; i < 512; i += 1) {
    const id = `${owner}.n${i}`;
    parts.push(contrib(owner, id, 'PAGE', 'pixs.shell.pages', { export: 'P' }));
    if (prev) edges.push([owner, prev, owner, id]);
    prev = id;
  }
  const g = graphOf(parts, edges);
  const fac = Object.fromEntries(parts.filter((c) => c.type === 'PAGE').map((c) => [keyOf(c.owner, c.id), factoryFor(simpleRoot(owner))]));
  const { rt } = makeRuntime(fx, g, fac);
  assert.equal(typeof rt.getVersion(), 'number');
  assert.equal(fx.listenerCount(), 1);
  const initialVersion = rt.getVersion();
  let calls = 0;
  const off = rt.subscribe(() => { calls += 1; });
  rt.refreshPresentation();
  assert.equal(calls, 1);
  assert.equal(rt.getVersion(), initialVersion + 1);
  off();
  rt.refreshPresentation();
  assert.equal(calls, 1);
  const first = parts.find((c) => c.type === 'PAGE');
  assert.ok(rt.renderContribution(first.owner, first.id));
  rt.dispose(); rt.dispose();
  assert.equal(fx.listenerCount(), 0);
  assert.equal(refused(() => rt.renderContribution(first.owner, first.id)).code, 'COMPOSITION_DISPOSED');
  const broken = makeFixture(), other = makeRuntime(broken, graphOf([]), {}).rt;
  broken.failUnsubscribe();
  assert.throws(() => other.dispose(), /fixture-unsubscribe/);
});

test('adapter runtime : contexte lie authentique, copies et perimes refuses', async () => {
  const fx = makeFixture(), owner = 'acme.demo', id = owner + '.form';
  const g = graphOf([i18n(owner), contrib(owner, id, 'FORM', 'pixs.shell.forms', { export: 'F' })]);
  const { rt } = makeRuntime(fx, g, { [keyOf(owner, id)]: factoryFor(formRoot(owner)) });
  try {
    const produced = rt.renderContribution(owner, id), authentic = produced.context;
    const copied = clone(authentic);
    assert.equal(refused(() => rt.actionState('create', copied)).code, 'COMPOSITION_CONTEXT_STALE');
    await rejected(rt.submit('create', formRoot(owner).props.intent, { username: 'alice' }, copied),
      'COMPOSITION_CONTEXT_STALE');
    assert.equal(refused(() => rt.reportError('create', 'E_COPY', copied)).code, 'COMPOSITION_CONTEXT_STALE');
    const h = (type, props, ...children) => ({ type, props: props ?? {}, children });
    const ports = state => ({
      h, Link() {}, label: key => key,
      id: (() => { let next = 0; return () => 'ui' + (++next); })(),
      state,
      submit: (action, intent, values) => rt.submit(action, intent, values, authentic),
      readFields: (element, names) => Object.fromEntries(names.map(name => [name, 'alice'])),
      slot: point => rt.slotContributions(point, authentic),
      component: (childOwner, childId) => rt.renderComponent(authentic, childOwner, childId),
      onError: (action, code) => rt.reportError(action, code, authentic),
    });
    const unbound = createPresentationAdapter(ports((action, copy) => rt.actionState(action, copy)));
    assert.equal(refused(() => unbound.render(produced.tree, authentic)).code,
      'COMPOSITION_CONTEXT_STALE');
    assert.equal(fx.postCalls.length, 0);
    let copiedPortContext = null;
    const bound = createPresentationAdapter(ports((action, copy) => {
      copiedPortContext = copy;
      return rt.actionState(action, authentic);
    }));
    const view = bound.render(produced.tree, authentic);
    assert.equal(view.type, 'form');
    assert.notEqual(copiedPortContext, authentic);
    assert.deepEqual(copiedPortContext, authentic);
    assert.equal(Object.isFrozen(copiedPortContext), true);
    const pending = view.props.onSubmit({ preventDefault() {}, currentTarget: {} });
    await fx.waitForPost();
    assert.equal(rt.getState(owner, id).actions.create.phase, 'PENDING');
    assert.equal(fx.postCalls[0].body.payload.username, 'alice');
    fx.resolvePostNext(okData(fx.session.getState().scope, { created: true }));
    await pending;
    assert.equal(rt.getState(owner, id).actions.create.phase, 'CONFIRMED');
    fx.advance('DATA');
    assert.equal(refused(() => rt.actionState('create', authentic)).code, 'COMPOSITION_CONTEXT_STALE');
    await rejected(rt.submit('create', formRoot(owner).props.intent, { username: 'alice' }, authentic),
      'COMPOSITION_CONTEXT_STALE');
    assert.equal(refused(() => rt.reportError('create', 'E_STALE', authentic)).code,
      'COMPOSITION_CONTEXT_STALE');
    assert.equal(fx.postCalls.length, 1);
  } finally { rt.dispose(); }
});
