// Runtime privé : données de présentation, actions explicites et isolation par contribution.
import { bindShellApi, validateSnapshot, validateScope } from './api-v1.js';
import { validatePresentationTree, validatePresentationFieldInput, PRESENTATION_SCHEMA } from './presentation-contract-v1.js';

export class CompositionRuntimeError extends Error {
  constructor(code, cause) { super(code, cause === undefined ? undefined : { cause }); this.name = 'CompositionRuntimeError'; this.code = code; }
}
const fail = (code, cause) => { throw new CompositionRuntimeError(code, cause); };
const keyOf = (owner, id) => JSON.stringify([owner, id]);
const dangerous = key => ['__proto__', 'constructor', 'prototype'].includes(key);
function record(value) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)
      || ![Object.prototype, null].includes(Object.getPrototypeOf(value))) fail('COMPOSITION_DATA_INVALID');
  for (const key of Reflect.ownKeys(value)) {
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (typeof key !== 'string' || dangerous(key) || !descriptor || !Object.hasOwn(descriptor, 'value')) fail('COMPOSITION_DATA_INVALID');
  }
  return value;
}
function closed(value, names) {
  record(value);
  if (Reflect.ownKeys(value).length !== names.length || names.some(name => !Object.hasOwn(value, name))) fail('COMPOSITION_OPTIONS_INVALID');
  return value;
}
function copy(value, bounds) {
  let count = 0;
  const active = new Set();
  function visit(node, depth) {
    if (++count > bounds.maxDataNodes || depth > bounds.maxDepth) fail('COMPOSITION_DATA_LIMIT');
    if (node === null || typeof node === 'string' || typeof node === 'boolean') return node;
    if (typeof node === 'number' && Number.isFinite(node)) return node;
    if (typeof node !== 'object' || active.has(node)) fail('COMPOSITION_DATA_INVALID');
    active.add(node);
    let output;
    if (Array.isArray(node)) {
      if (Object.getPrototypeOf(node) !== Array.prototype || Reflect.ownKeys(node).length !== node.length + 1) fail('COMPOSITION_DATA_INVALID');
      output = [];
      for (let index = 0; index < node.length; index += 1) {
        const descriptor = Object.getOwnPropertyDescriptor(node, String(index));
        if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail('COMPOSITION_DATA_INVALID');
        output.push(visit(descriptor.value, depth + 1));
      }
    } else {
      record(node); output = {};
      for (const key of Object.keys(node)) Object.defineProperty(output, key, { value: visit(node[key], depth + 1), enumerable: true });
    }
    active.delete(node);
    return Object.freeze(output);
  }
  return visit(value, 0);
}
function canonical(value) {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
  return '{' + Object.keys(value).sort().map(key => JSON.stringify(key) + ':' + canonical(value[key])).join(',') + '}';
}
function routeParameters(path, values) {
  record(values);
  const expected = path.split('/').filter(part => part.startsWith('{')).map(part => part.slice(1, -1));
  if (Object.keys(values).length !== expected.length || expected.some(name => !Object.hasOwn(values, name))) fail('COMPOSITION_ROUTE_INVALID');
  for (const value of Object.values(values)) {
    if (typeof value !== 'string' || !value || value === '.' || value === '..' || value.includes(String.fromCharCode(0))) fail('COMPOSITION_ROUTE_INVALID');
    try { encodeURIComponent(value); } catch (cause) { fail('COMPOSITION_ROUTE_INVALID', cause); }
  }
}

export function createCompositionRuntime(options) {
  const names = ['graph', 'factories', 'session', 'translate', 'navigate', 'presentationLimits', 'points', 'createId', 'fingerprint', 'onError'];
  const checked = closed(options, names);
  const p = Object.freeze(Object.fromEntries(names.map(name => [name, checked[name]])));
  for (const name of ['translate', 'navigate', 'createId', 'fingerprint', 'onError']) if (typeof p[name] !== 'function') fail('COMPOSITION_OPTIONS_INVALID');
  const limitNames = ['maxNodes', 'maxDepth', 'maxChildren', 'maxTextLength', 'maxParams', 'maxFields', 'maxBindings', 'maxDataNodes', 'maxBodyDepth', 'maxBodyNodes'];
  closed(p.presentationLimits, limitNames);
  for (const value of Object.values(p.presentationLimits)) if (!Number.isSafeInteger(value) || value <= 0) fail('COMPOSITION_OPTIONS_INVALID');
  const limits = Object.freeze({ ...p.presentationLimits });
  const json = value => copy(value, limits);
  const sessionNames = ['getState', 'getResolver', 'getContextSnapshot', 'isCurrentSnapshot', 'subscribe', 'fetchJson', 'postJson', 'invalidateScope'];
  if (!p.session || sessionNames.some(name => typeof p.session[name] !== 'function')) fail('COMPOSITION_OPTIONS_INVALID');
  const session = Object.freeze(Object.fromEntries(sessionNames.map(name => [name, p.session[name].bind(p.session)])));
  const graph = json(p.graph), points = json(p.points);
  if (graph.schema !== 'pixs.frontend.contribution-graph/1.0.0' || graph.blocked !== false
      || !Array.isArray(graph.contributions) || !Array.isArray(graph.contributionEdges)) fail('COMPOSITION_GRAPH_INVALID');
  record(points.points); record(points.metadata);
  const nodes = new Map(), factories = new Map(), edges = new Map();
  const renderable = new Set(['ROUTE', 'PAGE', 'FORM', 'COMPONENT', 'UI_SLOT']);
  for (const contribution of graph.contributions) {
    record(contribution);
    if (typeof contribution.owner !== 'string' || typeof contribution.id !== 'string'
        || !['PUBLIC', 'AUTHENTICATED', 'PLATFORM_SCOPED', 'TENANT_SCOPED'].includes(contribution.activation_scope)
        || !Array.isArray(contribution.display_permissions) || contribution.display_permissions.some(value => typeof value !== 'string')
        || !Object.hasOwn(points.points, contribution.point) || points.points[contribution.point].category !== contribution.type) fail('COMPOSITION_GRAPH_INVALID');
    const key = keyOf(contribution.owner, contribution.id);
    if (nodes.has(key)) fail('COMPOSITION_GRAPH_INVALID');
    nodes.set(key, contribution); edges.set(key, new Set());
  }
  for (const edge of graph.contributionEdges) {
    if (!Array.isArray(edge) || edge.length !== 4) fail('COMPOSITION_GRAPH_INVALID');
    const source = keyOf(edge[0], edge[1]), target = keyOf(edge[2], edge[3]);
    if (!nodes.has(source) || !nodes.has(target)) fail('COMPOSITION_GRAPH_INVALID');
    edges.get(source).add(target);
  }
  // Les dépendances de rendu restent celles du graphe ; aucun registre de lifecycle parallèle.
  // La profondeur du graphe n’est pas celle des arbres de présentation.
  const incoming = new Map([...nodes.keys()].map(key => [key, 0]));
  for (const targets of edges.values()) {
    for (const target of targets) incoming.set(target, incoming.get(target) + 1);
  }
  const ready = [...nodes.keys()].filter(key => incoming.get(key) === 0);
  let visitedCount = 0;
  for (let index = 0; index < ready.length; index += 1) {
    visitedCount += 1;
    for (const target of edges.get(ready[index])) {
      const remaining = incoming.get(target) - 1;
      incoming.set(target, remaining);
      if (remaining === 0) ready.push(target);
    }
  }
  if (visitedCount !== nodes.size) fail('COMPOSITION_GRAPH_CYCLE');
  record(p.factories);
  for (const key of Object.keys(p.factories)) {
    if (!nodes.has(key) || !renderable.has(nodes.get(key).type) || typeof p.factories[key] !== 'function') fail('COMPOSITION_FACTORY_INVALID');
    factories.set(key, p.factories[key]);
  }
  for (const [key, node] of nodes) if (renderable.has(node.type) && !factories.has(key)) fail('COMPOSITION_FACTORY_INVALID');

  let revision = 0, routeRevision = 0, activeRoute = null, disposed = false, rendering = false;
  let contexts = new WeakMap();
  const listeners = new Set(), actions = new Map(), registry = new Map(), formValues = new Map(), trees = new Map();
  const alive = () => { if (disposed) fail('COMPOSITION_DISPOSED'); };
  function bump(kind) {
    if (revision === Number.MAX_SAFE_INTEGER) fail('COMPOSITION_SEQUENCE_EXHAUSTED');
    revision += 1; trees.clear();
    for (const listener of [...listeners]) listener(Object.freeze({ kind, revision }));
  }
  const contribution = (owner, id) => {
    const node = nodes.get(keyOf(owner, id));
    if (!node) fail('COMPOSITION_CONTRIBUTION_UNKNOWN');
    return node;
  };
  function visible(node) {
    const context = session.getState();
    if (node.display_permissions.length) return false;
    if (node.activation_scope === 'PUBLIC') return true;
    if (context.state !== 'ACTIVE') return false;
    if (node.activation_scope === 'AUTHENTICATED') return true;
    return node.activation_scope === 'PLATFORM_SCOPED' ? context.scope.scope_type === 'PLATFORM' : context.scope.scope_type === 'TENANT';
  }
  const sessionTag = () => {
    const context = session.getState();
    return context.state === 'ACTIVE' ? canonical({ session: context.session_id, scope: validateScope(context.scope) }) : null;
  };
  const actionKey = (owner, id, action) => JSON.stringify([owner, id, action]);
  function projected(owner, id) {
    const values = {}, fields = {};
    for (const entry of actions.values()) if (entry.owner === owner && entry.id === id) {
      const value = { kind: entry.kind, phase: entry.phase, sequence: entry.sequence };
      if (entry.error_code) value.error_code = entry.error_code;
      if (entry.response !== undefined) value.response = entry.response;
      Object.defineProperty(values, entry.action, { value: Object.freeze(value), enumerable: true });
    }
    for (const entry of formValues.values()) if (entry.owner === owner && entry.id === id) {
      Object.defineProperty(fields, entry.form, { value: entry.values, enumerable: true });
    }
    return Object.freeze({ actions: Object.freeze(values), fields: Object.freeze(fields) });
  }
  function contextFor(node) {
    const catalogs = { en: {}, fr: {} };
    for (const candidate of nodes.values()) if (candidate.type === 'TRANSLATION' && candidate.owner === node.owner) {
      for (const locale of ['en', 'fr']) for (const [key, value] of Object.entries(candidate.payload.catalog[locale])) {
        if (Object.hasOwn(catalogs[locale], key)) fail('COMPOSITION_CATALOG_COLLISION');
        Object.defineProperty(catalogs[locale], key, { value, enumerable: true });
      }
    }
    const dependencies = edges.get(keyOf(node.owner, node.id));
    return json({
      owner: node.owner, id: node.id, catalogs,
      routes: ['/', '/login', '/platform', '/tenants/{tenant_id}', '/tenants/{tenant_id}/scopes/{scope_id}',
        ...[...nodes.values()].filter(candidate => candidate.type === 'ROUTE').map(candidate => candidate.payload.path)],
      slots: Object.keys(points.points).filter(point => points.points[point].category === 'UI_SLOT'
        && points.points[point].owner === node.owner && (point === node.owner || point.startsWith(node.owner + '.'))),
      components: [...nodes.values()].filter(candidate => ['PAGE', 'FORM', 'COMPONENT'].includes(candidate.type)
        && dependencies.has(keyOf(candidate.owner, candidate.id))).map(candidate => ({ owner: candidate.owner, id: candidate.id })),
      limits,
    });
  }
  function checkedContext(context) {
    const marker = contexts.get(context);
    if (!marker || marker.routeRevision !== routeRevision || marker.epoch !== session.getState().epoch) fail('COMPOSITION_CONTEXT_STALE');
    return marker;
  }
  function forget() {
    for (const [key, entry] of actions) {
      if (entry.kind === 'COMMAND' && (entry.phase === 'UNKNOWN' || entry.phase === 'PENDING' && (entry.dispatched || entry.uncertain))) {
        actions.set(key, { owner: entry.owner, id: entry.id, action: entry.action, kind: 'COMMAND', phase: 'UNKNOWN',
          sequence: entry.sequence, key: entry.key, digest: entry.digest, tag: entry.tag, uncertain: true, error_code: 'COMPOSITION_RESULT_UNKNOWN' });
      } else actions.delete(key);
    }
    formValues.clear(); registry.clear(); trees.clear(); contexts = new WeakMap();
    if (routeRevision === Number.MAX_SAFE_INTEGER) fail('COMPOSITION_SEQUENCE_EXHAUSTED');
    routeRevision += 1;
  }
  function index(tree, node) {
    const pending = [tree];
    while (pending.length) {
      const current = pending.pop();
      if (current.kind === 'form' || current.kind === 'button' && !current.props.submit) {
        const intent = current.props.intent;
        if (intent !== null) {
          const fields = [];
          if (current.kind === 'form') {
            const queue = [...current.children];
            while (queue.length) { const child = queue.pop(); if (child.kind === 'field') fields.push(child); queue.push(...child.children); }
          }
          registry.set(actionKey(node.owner, node.id, current.props.id), { node, intent, fields, form: current.kind === 'form' });
        }
      }
      pending.push(...current.children);
    }
  }
  function apiFor(node, presentationContext) {
    const guard = () => { if (rendering) fail('COMPOSITION_RENDER_EFFECT'); alive(); };
    const api = bindShellApi({
      ShellContextProvider: () => session.getState(), useShellContext: () => session.getState(),
      getContextSnapshot: session.getContextSnapshot, isCurrentSnapshot: session.isCurrentSnapshot,
      fetchJson: session.fetchJson, postJson: session.postJson,
      navigate: (path, params = {}) => { guard(); if (!presentationContext.routes.includes(path)) fail('COMPOSITION_ROUTE_INVALID'); routeParameters(path, params); return p.navigate(path, json(params)); },
      invalidateScope: () => { guard(); return session.invalidateScope(); },
      translate: (key, params = {}) => {
        if (!Object.hasOwn(presentationContext.catalogs.en, key)) fail('COMPOSITION_LABEL_UNKNOWN');
        return p.translate(key, json(params), presentationContext);
      },
      present: tree => validatePresentationTree(tree, presentationContext),
    }, session.getResolver());
    return Object.freeze({ ...api,
      QueryClient: Object.freeze({ query: (...args) => { guard(); return api.QueryClient.query(...args); } }),
      CommandClient: Object.freeze({ intent: (...args) => { guard(); return api.CommandClient.intent(...args); } }),
    });
  }
  function renderContribution(owner, id, routeParams = {}) {
    alive();
    const node = contribution(owner, id);
    if (!renderable.has(node.type) || !visible(node)) fail('COMPOSITION_UNAVAILABLE');
    const params = json(routeParams);
    if (node.type === 'ROUTE') routeParameters(node.payload.path, params);
    const cacheKey = canonical([owner, id, params]);
    if (trees.has(cacheKey)) return trees.get(cacheKey);
    const context = contextFor(node);
    const input = Object.freeze({ api: apiFor(node, context), context: json(session.getState()), routeParams: params, state: projected(owner, id) });
    let result;
    if (rendering) fail('COMPOSITION_RENDER_CYCLE');
    rendering = true;
    try { result = factories.get(keyOf(owner, id))(input); }
    catch (cause) { fail('COMPOSITION_FACTORY_FAILED', cause); }
    finally { rendering = false; }
    closed(result, ['schema', 'root']);
    if (result.schema !== PRESENTATION_SCHEMA) fail('COMPOSITION_PRESENTATION_INVALID');
    const tree = validatePresentationTree(result.root, context);
    for (const [key, registered] of registry) {
      if (registered.node.owner === owner && registered.node.id === id) registry.delete(key);
    }
    contexts.set(context, { owner, id, epoch: session.getState().epoch, routeRevision });
    index(tree, node);
    const output = Object.freeze({ tree, context });
    if (trees.size >= limits.maxDataNodes) fail('COMPOSITION_DATA_LIMIT');
    trees.set(cacheKey, output);
    return output;
  }
  function mergedIntent(registered, intent, fields) {
    if (canonical(json(intent)) !== canonical(registered.intent)) fail('COMPOSITION_INTENT_STALE');
    record(fields);
    if (Object.keys(fields).length !== registered.fields.length) fail('COMPOSITION_FIELD_INVALID');
    const values = {};
    for (const field of registered.fields) {
      const name = field.props.name;
      if (!Object.hasOwn(fields, name)) fail('COMPOSITION_FIELD_INVALID');
      Object.defineProperty(values, name, { value: validatePresentationFieldInput(field, fields[name], limits), enumerable: true });
    }
    const kind = Object.hasOwn(intent, 'query') ? 'QUERY' : 'COMMAND';
    const body = JSON.parse(JSON.stringify(kind === 'QUERY' ? intent.params : intent.body));
    for (const binding of intent.bindings) {
      let target = body;
      for (const name of binding.path.slice(0, -1)) {
        if (!Object.hasOwn(record(target), name)) fail('COMPOSITION_BINDING_INVALID');
        target = target[name];
      }
      const leaf = binding.path.at(-1);
      if (!Object.hasOwn(record(target), leaf) || dangerous(leaf)) fail('COMPOSITION_BINDING_INVALID');
      target[leaf] = values[binding.field];
    }
    return { kind, name: kind === 'QUERY' ? intent.query : intent.command, body: json(body), fields: json(values) };
  }
  function abandon(key, entry) {
    if (actions.get(key) !== entry) return;
    if (entry.kind === 'COMMAND' && (entry.dispatched || entry.uncertain)) {
      actions.set(key, { owner: entry.owner, id: entry.id, action: entry.action, kind: 'COMMAND', phase: 'UNKNOWN', sequence: entry.sequence,
        key: entry.key, digest: entry.digest, tag: entry.tag, uncertain: true, error_code: 'COMPOSITION_RESULT_UNKNOWN' });
    } else actions.delete(key);
    formValues.delete(key); bump('ACTION');
  }
  function resultFor(owner, id, action) { return projected(owner, id).actions[action] ?? null; }
  async function submit(action, intent, fields, context) {
    alive();
    const marker = checkedContext(context), key = actionKey(marker.owner, marker.id, action), registered = registry.get(key);
    if (!registered || !visible(registered.node)) fail('COMPOSITION_ACTION_UNAVAILABLE');
    const known = actions.get(key);
    if (known?.phase === 'PENDING') fail('COMPOSITION_PENDING');
    const request = mergedIntent(registered, intent, fields);
    const snapshot = validateSnapshot(session.getContextSnapshot()), tag = sessionTag();
    if (known?.phase === 'UNKNOWN' && known.tag !== tag) fail('COMPOSITION_RETRY_CONTEXT_MISMATCH');
    const sequence = (known?.sequence ?? 0) + 1;
    if (!Number.isSafeInteger(sequence)) fail('COMPOSITION_SEQUENCE_EXHAUSTED');
    const idempotencyKey = request.kind === 'COMMAND' ? (known?.phase === 'UNKNOWN' ? known.key : p.createId()) : null;
    if (request.kind === 'COMMAND' && (typeof idempotencyKey !== 'string' || !idempotencyKey || idempotencyKey.length > 128)) fail('COMPOSITION_ID_INVALID');
    const entry = { owner: marker.owner, id: marker.id, action, kind: request.kind, phase: 'PENDING', sequence,
      key: idempotencyKey, digest: known?.phase === 'UNKNOWN' ? known.digest : null, tag,
      dispatched: false, uncertain: known?.phase === 'UNKNOWN' };
    actions.set(key, entry);
    formValues.set(key, { owner: marker.owner, id: marker.id, form: action, values: request.fields });
    bump('ACTION');
    try {
      if (request.kind === 'COMMAND') {
        const digest = await p.fingerprint(canonical({ kind: request.kind, name: request.name, body: request.body }));
        if (typeof digest !== 'string' || !/^[0-9a-f]{64}$/.test(digest)) fail('COMPOSITION_FINGERPRINT_INVALID');
        if (entry.uncertain && entry.digest !== digest) fail('COMPOSITION_RETRY_MISMATCH');
        entry.digest = digest;
      }
      if (actions.get(key) !== entry || !session.isCurrentSnapshot(snapshot) || marker.routeRevision !== routeRevision) {
        abandon(key, entry); return resultFor(marker.owner, marker.id, action);
      }
      const api = apiFor(registered.node, context);
      entry.dispatched = true;
      const outcome = request.kind === 'QUERY' ? await api.QueryClient.query(request.name, { params: request.body })
        : await api.CommandClient.intent(request.name, request.body, { idempotencyKey });
      if (actions.get(key) !== entry || !session.isCurrentSnapshot(snapshot) || marker.routeRevision !== routeRevision) {
        abandon(key, entry); return resultFor(marker.owner, marker.id, action);
      }
      if (request.kind === 'QUERY') { entry.phase = 'LOADED'; entry.response = json(outcome); }
      else if (outcome.state === 'CONFIRMED') { entry.phase = 'CONFIRMED'; entry.response = json(outcome.response); entry.uncertain = false; }
      else if (outcome.state === 'REJECTED' && !entry.uncertain) { entry.phase = 'REJECTED'; entry.response = json(outcome.response); entry.error_code = outcome.response.error_code; }
      else { entry.phase = 'UNKNOWN'; entry.uncertain = true; entry.error_code = 'COMPOSITION_RESULT_UNKNOWN'; }
      bump('ACTION');
      return resultFor(marker.owner, marker.id, action);
    } catch (cause) {
      if (actions.get(key) !== entry) return resultFor(marker.owner, marker.id, action);
      const localRefusal = ['SHELL_ROUTE_INVALID', 'SHELL_COMMAND_INVALID', 'SHELL_IDEMPOTENCY_REQUIRED'].includes(cause?.code);
      if (localRefusal) entry.dispatched = false;
      entry.phase = entry.kind === 'COMMAND' ? (entry.dispatched || entry.uncertain ? 'UNKNOWN' : 'REJECTED')
        : ['SHELL_QUERY_REFUSED', 'SHELL_QUERY_INVALID', 'SHELL_ROUTE_INVALID'].includes(cause?.code) ? 'REJECTED' : 'UNAVAILABLE';
      entry.error_code = cause instanceof Error && typeof cause.code === 'string' ? cause.code : 'COMPOSITION_ACTION_FAILED';
      if (entry.phase === 'UNKNOWN') entry.uncertain = true;
      bump('ACTION');
      throw cause;
    }
  }
  const unsubscribe = session.subscribe(() => { if (!disposed) { forget(); bump('SESSION'); } });
  if (typeof unsubscribe !== 'function') fail('COMPOSITION_SESSION_INVALID');
  return Object.freeze({
    subscribe: listener => { alive(); if (typeof listener !== 'function') fail('COMPOSITION_LISTENER_INVALID'); listeners.add(listener); return () => listeners.delete(listener); },
    getVersion: () => revision,
    getState: (owner, id) => { alive(); contribution(owner, id); return projected(owner, id); },
    visibleRoutes: () => Object.freeze([...nodes.values()].filter(node => node.type === 'ROUTE' && visible(node))),
    visibleNavigation: () => Object.freeze([...nodes.values()].filter(node => node.type === 'NAVIGATION' && visible(node))),
    slotContributions: (point, parent = null) => {
      alive();
      if (!Object.hasOwn(points.points, point) || points.points[point].category !== 'UI_SLOT') fail('COMPOSITION_POINT_UNKNOWN');
      if (parent !== null) { checkedContext(parent); if (!parent.slots.includes(point)) fail('COMPOSITION_SLOT_UNAVAILABLE'); }
      return Object.freeze([...nodes.values()].filter(node => node.type === 'UI_SLOT' && node.payload.slot === point && visible(node)));
    },
    renderComponent: (context, owner, id, params = {}) => {
      checkedContext(context);
      if (!context.components.some(item => item.owner === owner && item.id === id)) fail('COMPOSITION_COMPONENT_UNAVAILABLE');
      return renderContribution(owner, id, params);
    },
    openRoute: (owner, id, params = {}) => {
      alive(); const node = contribution(owner, id);
      if (node.type !== 'ROUTE' || !visible(node)) fail('COMPOSITION_ROUTE_UNAVAILABLE');
      routeParameters(node.payload.path, params);
      const next = canonical([owner, id, json(params)]);
      if (next !== activeRoute) { forget(); activeRoute = next; bump('ROUTE'); }
    },
    leaveRoute: () => { alive(); if (activeRoute !== null) { forget(); activeRoute = null; bump('ROUTE'); } },
    refreshPresentation: () => { alive(); bump('PRESENTATION'); },
    renderContribution, submit,
    actionState: (action, context) => {
      alive(); const marker = checkedContext(context), registered = registry.get(actionKey(marker.owner, marker.id, action));
      const entry = actions.get(actionKey(marker.owner, marker.id, action));
      const available = registered && visible(registered.node) && session.getState().state === 'ACTIVE';
      const phase = entry?.phase ?? 'IDLE';
      const canSubmit = Boolean(available && phase !== 'PENDING' && !(phase === 'UNKNOWN' && entry.tag !== sessionTag()));
      return Object.freeze({ state: available ? phase : 'UNAVAILABLE', message: p.translate('shell.state' + (available ? phase : 'UNAVAILABLE'), {}, null),
        canSubmit, fieldsDisabled: !available || phase === 'PENDING' || phase === 'UNKNOWN' && !canSubmit });
    },
    reportError: (action, code, context) => {
      alive(); const marker = checkedContext(context), entry = actions.get(actionKey(marker.owner, marker.id, action));
      if (typeof code !== 'string' || !code) fail('COMPOSITION_ERROR_INVALID');
      if (entry) entry.error_code = code;
      if (!entry || ['IDLE', 'LOADED', 'CONFIRMED', 'INVALID'].includes(entry.phase)) {
        const key = actionKey(marker.owner, marker.id, action), registered = registry.get(key);
        if (registered) actions.set(key, { owner: marker.owner, id: marker.id, action,
          kind: Object.hasOwn(registered.intent, 'query') ? 'QUERY' : 'COMMAND',
          phase: 'INVALID', sequence: entry?.sequence ?? 0, error_code: code });
      }
      p.onError(code); bump('ERROR');
    },
    dispose: () => {
      if (disposed) return;
      disposed = true;
      try { unsubscribe(); }
      finally { actions.clear(); registry.clear(); formValues.clear(); trees.clear(); listeners.clear(); contexts = new WeakMap(); activeRoute = null; }
    },
  });
}
