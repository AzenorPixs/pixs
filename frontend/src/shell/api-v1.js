export const SHELL_API_VERSION = '1.0.0';
const SLOT_IDS = Object.freeze(['pixs.shell.header', 'pixs.shell.navigation', 'pixs.shell.main', 'pixs.shell.footer']);
const RESERVED_TOP = new Set(['auth', 'csrf', 'shell', 'shell-context']);
const UUID7 = /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
export const TRANSPORT_RESOLVER_VERSION = '1.0.0';
const CORE_CONTRACT_VERSION = '1.0.0';
const SEMVER_RE = /^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-((?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$/;
function denseNoUniq(v, code) {
  if (!Array.isArray(v)) fail(code);
  if (Object.getPrototypeOf(v) !== Array.prototype) fail(code);
  if (Reflect.ownKeys(v).length !== v.length + 1) fail(code);
  for (let i = 0; i < v.length; i += 1) {
    const d = Object.getOwnPropertyDescriptor(v, String(i));
    if (!d || !Object.hasOwn(d, 'value')) fail(code);
  }
  return v;
}
function checkSegments(segs) {
  denseNoUniq(segs, 'SHELL_ROUTE_INVALID');
  if (segs.length === 0) fail('SHELL_ROUTE_INVALID');
  for (const s of segs) {
    if (typeof s !== 'string' || s.length === 0) fail('SHELL_ROUTE_INVALID');
    if (s === '.' || s === '..') fail('SHELL_ROUTE_INVALID');
    if (s.includes('/') || s.includes('\\') || s.includes('%') || s.includes('?') || s.includes('#') || s.includes(':') || s.includes(' ')) fail('SHELL_ROUTE_INVALID');
    for (let i = 0; i < s.length; i += 1) {
      const u = s.charCodeAt(i);
      if (u < 32 || u === 127 || u === 0 || u === 10 || u === 13) fail('SHELL_ROUTE_INVALID');
    }
  }
  if (RESERVED_TOP.has(segs[0])) fail('SHELL_ROUTE_INVALID');
  return segs;
}
function checkBinding(b) {
  record(b, ['kind', 'name', 'owner', 'contractVersion', 'scopes', 'segments'], [], 'SHELL_ROUTE_INVALID');
  if (b.kind !== 'QUERY' && b.kind !== 'COMMAND') fail('SHELL_ROUTE_INVALID');
  if (typeof b.name !== 'string' || b.name.length === 0) fail('SHELL_ROUTE_INVALID');
  if (typeof b.owner !== 'string' || b.owner.length === 0) fail('SHELL_ROUTE_INVALID');
  if (typeof b.contractVersion !== 'string' || !SEMVER_RE.test(b.contractVersion)) fail('SHELL_ROUTE_INVALID');
  denseNoUniq(b.scopes, 'SHELL_ROUTE_INVALID');
  if (b.scopes.length === 0) fail('SHELL_ROUTE_INVALID');
  for (const m of b.scopes) if (m !== 'P' && m !== 'T' && m !== 'S') fail('SHELL_ROUTE_INVALID');
  if (new Set(b.scopes).size !== b.scopes.length) fail('SHELL_ROUTE_INVALID');
  checkSegments(b.segments);
  return b;
}
const CORE_BINDINGS_SRC = [
  ['COMMAND', 'create-user', ['P'], ['commands', 'create-user']],
  ['COMMAND', 'create-identity', ['P'], ['commands', 'create-identity']],
  ['COMMAND', 'link-identity', ['P'], ['commands', 'link-identity']],
  ['COMMAND', 'unlink-identity', ['P'], ['commands', 'unlink-identity']],
  ['COMMAND', 'set-identity-state', ['P'], ['commands', 'set-identity-state']],
  ['COMMAND', 'logical-delete-identity', ['P'], ['commands', 'logical-delete-identity']],
  ['COMMAND', 'create-group', ['P', 'T', 'S'], ['commands', 'create-group']],
  ['COMMAND', 'change-group-persistence', ['P', 'T', 'S'], ['commands', 'change-group-persistence']],
  ['COMMAND', 'add-user-group', ['P', 'T', 'S'], ['commands', 'add-user-group']],
  ['COMMAND', 'remove-user-group', ['P', 'T', 'S'], ['commands', 'remove-user-group']],
  ['COMMAND', 'activate-tenant-membership', ['T'], ['commands', 'activate-tenant-membership']],
  ['COMMAND', 'revoke-tenant-membership', ['T'], ['commands', 'revoke-tenant-membership']],
  ['COMMAND', 'create-tenant', ['P'], ['commands', 'create-tenant']],
  ['COMMAND', 'create-scope', ['T'], ['commands', 'create-scope']],
  ['COMMAND', 'move-scope', ['T'], ['commands', 'move-scope']],
  ['COMMAND', 'declare-permission', ['P'], ['commands', 'declare-permission']],
  ['COMMAND', 'create-role', ['P', 'T', 'S'], ['commands', 'create-role']],
  ['COMMAND', 'set-role-permissions', ['P', 'T', 'S'], ['commands', 'set-role-permissions']],
  ['COMMAND', 'assign-role', ['P', 'T', 'S'], ['commands', 'assign-role']],
  ['COMMAND', 'unassign-role', ['P', 'T', 'S'], ['commands', 'unassign-role']],
  ['COMMAND', 'persist-policy', ['P'], ['commands', 'persist-policy']],
  ['COMMAND', 'change-authz-persistence', ['P', 'T', 'S'], ['commands', 'change-authz-persistence']],
  ['QUERY', 'users', ['P'], ['users']],
  ['QUERY', 'identities', ['P'], ['identities']],
  ['QUERY', 'links', ['P'], ['links']],
  ['QUERY', 'groups', ['P', 'T', 'S'], ['groups']],
  ['QUERY', 'user-groups', ['P', 'T', 'S'], ['user-groups']],
  ['QUERY', 'memberships', ['T'], ['memberships']],
  ['QUERY', 'tenants', ['P'], ['tenants']],
  ['QUERY', 'scopes', ['T'], ['scopes']],
  ['QUERY', 'permissions', ['P'], ['permissions']],
  ['QUERY', 'roles', ['P', 'T', 'S'], ['roles']],
  ['QUERY', 'role-permissions', ['P', 'T', 'S'], ['role-permissions']],
  ['QUERY', 'assignments', ['P', 'T', 'S'], ['assignments']],
  ['QUERY', 'policies', ['P'], ['policies']],
  ['QUERY', 'bindings', ['P'], ['bindings']],
  ['QUERY', 'grants', ['P'], ['grants']],
];
function coreBindingList() {
  return CORE_BINDINGS_SRC.map((e) => Object.freeze({ kind: e[0], name: e[1], owner: 'pixs.core', contractVersion: CORE_CONTRACT_VERSION, scopes: Object.freeze([...e[2]]), segments: Object.freeze([...e[3]]) }));
}
function isCoreBinding(b) {
  for (const c of coreBindingList()) {
    if (c.kind === b.kind && c.name === b.name && c.contractVersion === b.contractVersion && c.owner === b.owner && c.scopes.length === b.scopes.length && c.scopes.every((x, i) => x === b.scopes[i]) && c.segments.length === b.segments.length && c.segments.every((x, i) => x === b.segments[i])) return true;
  }
  return false;
}
function isKnownCoreKey(kind, name) {
  for (const c of coreBindingList()) if (c.kind === kind && c.name === name) return true;
  return false;
}
export function validateTransportResolver(r) {
  record(r, ['version', 'operations'], [], 'SHELL_ROUTE_INVALID');
  if (r.version !== '1.0.0') fail('SHELL_ROUTE_INVALID');
  denseNoUniq(r.operations, 'SHELL_ROUTE_INVALID');
  const seen = new Set();
  const out = [];
  for (const item of r.operations) {
    const b = checkBinding(item);
    const k = b.kind + '/' + b.name;
    if (seen.has(k)) fail('SHELL_ROUTE_INVALID');
    seen.add(k);
    if (b.owner === 'pixs.core') {
      if (!isCoreBinding(b)) fail('SHELL_ROUTE_INVALID');
    } else if (isKnownCoreKey(b.kind, b.name)) fail('SHELL_ROUTE_INVALID');
    out.push(Object.freeze({ kind: b.kind, name: b.name, owner: b.owner, contractVersion: b.contractVersion, scopes: Object.freeze([...b.scopes]), segments: Object.freeze([...b.segments]) }));
  }
  return Object.freeze({ version: r.version, operations: Object.freeze(out) });
}
export function defaultTransportResolver() {
  return Object.freeze({ version: '1.0.0', operations: Object.freeze(coreBindingList()) });
}
export class ShellContractError extends Error {
  constructor(code, options) { super(code, options); this.name = 'ShellContractError'; this.code = code; }
}
function fail(code) { throw new ShellContractError(code); }
function record(value, required, optional = [], code = 'SHELL_CONTRACT_INVALID') {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) fail(code);
  const proto = Object.getPrototypeOf(value);
  if (proto !== Object.prototype && proto !== null) fail(code);
  const keys = Reflect.ownKeys(value);
  if (keys.some(key => typeof key !== 'string' || !required.includes(key) && !optional.includes(key)) || required.some(key => !Object.hasOwn(value, key))) fail(code);
  for (const key of keys) if (!Object.hasOwn(Object.getOwnPropertyDescriptor(value, key), 'value')) fail(code);
  return value;
}
function jsonSnapshot(value, seen = new Set()) {
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return value;
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value !== 'object' || seen.has(value)) fail('SHELL_DATA_INVALID');
  seen.add(value);
  try {
    if (Array.isArray(value)) {
      if (Object.getPrototypeOf(value) !== Array.prototype || Reflect.ownKeys(value).length !== value.length + 1) fail('SHELL_DATA_INVALID');
      const out = [];
      for (let i = 0; i < value.length; i += 1) {
        const d = Object.getOwnPropertyDescriptor(value, String(i));
        if (!d || !Object.hasOwn(d, 'value')) fail('SHELL_DATA_INVALID');
        out.push(jsonSnapshot(d.value, seen));
      }
      return Object.freeze(out);
    }
    record(value, [], Reflect.ownKeys(value), 'SHELL_DATA_INVALID');
    const out = {};
    for (const key of Reflect.ownKeys(value)) {
      if (typeof key !== 'string') fail('SHELL_DATA_INVALID');
      Object.defineProperty(out, key, { value: jsonSnapshot(Object.getOwnPropertyDescriptor(value, key).value, seen), enumerable: true });
    }
    return Object.freeze(out);
  } finally { seen.delete(value); }
}
export function validateScope(value) {
  record(value, ['scope_type', 'tenant_id', 'scope_id'], [], 'SHELL_SCOPE_INVALID');
  if (value.scope_type === 'PLATFORM') {
    if (value.tenant_id !== null || value.scope_id !== null) fail('SHELL_SCOPE_INVALID');
  } else if (value.scope_type === 'TENANT') {
    if (typeof value.tenant_id !== 'string' || value.tenant_id.length === 0) fail('SHELL_SCOPE_INVALID');
    if (value.scope_id !== null && (typeof value.scope_id !== 'string' || value.scope_id.length === 0)) fail('SHELL_SCOPE_INVALID');
  } else fail('SHELL_SCOPE_INVALID');
  return Object.freeze({ scope_type: value.scope_type, tenant_id: value.tenant_id, scope_id: value.scope_id });
}
export function validateSnapshot(value) {
  record(value, ['scope', 'epoch'], [], 'SHELL_SNAPSHOT_INVALID');
  if (!Number.isSafeInteger(value.epoch) || value.epoch < 0) fail('SHELL_SNAPSHOT_INVALID');
  return Object.freeze({ scope: validateScope(value.scope), epoch: value.epoch });
}
function sameScope(a, b) { return a.scope_type === b.scope_type && a.tenant_id === b.tenant_id && a.scope_id === b.scope_id; }
function functions(value, names) {
  record(value, names, [], 'SHELL_PORTS_INVALID');
  const out = {};
  for (const name of names) { if (typeof value[name] !== 'function') fail('SHELL_PORT_MISSING'); out[name] = value[name]; }
  return Object.freeze(out);
}
export function createContextProvider(ports) {
  const p = functions(ports, ['getContextSnapshot', 'isCurrentSnapshot']);
  return Object.freeze({
    snapshot() { return validateSnapshot(p.getContextSnapshot()); },
    isCurrent(snapshot) {
      const current = p.isCurrentSnapshot(validateSnapshot(snapshot));
      if (typeof current !== 'boolean') fail('SHELL_PORT_RESULT_INVALID');
      return current;
    },
  });
}
export function resolveTransport(resolver, scope, operation) {
  const r = validateTransportResolver(resolver);
  const s = validateScope(scope);
  record(operation, ['kind', 'name'], [], 'SHELL_ROUTE_INVALID');
  if (operation.kind !== 'QUERY' && operation.kind !== 'COMMAND') fail('SHELL_ROUTE_INVALID');
  if (typeof operation.name !== 'string' || operation.name.length === 0) fail('SHELL_ROUTE_INVALID');
  const dk = Object.getOwnPropertyDescriptor(operation, 'kind');
  const dn = Object.getOwnPropertyDescriptor(operation, 'name');
  if (!dk || !Object.hasOwn(dk, 'value') || !dn || !Object.hasOwn(dn, 'value')) fail('SHELL_ROUTE_INVALID');
  let found = null;
  for (const b of r.operations) if (b.kind === operation.kind && b.name === operation.name) { found = b; break; }
  if (!found) fail('SHELL_ROUTE_INVALID');
  const mode = s.scope_type === 'PLATFORM' ? 'P' : s.scope_id === null ? 'T' : 'S';
  if (!found.scopes.includes(mode)) fail('SHELL_ROUTE_INVALID');
  if (s.scope_type === 'TENANT') {
    for (const v of [s.tenant_id, s.scope_id]) {
      if (v === null) continue;
      if (v === '.' || v === '..' || v.includes('\0')) fail('SHELL_ROUTE_INVALID');
    }
  }
  let root = '/api/v1/web/platform';
  try {
    if (s.scope_type === 'TENANT') {
      root = '/api/v1/web/tenants/' + encodeURIComponent(s.tenant_id);
      if (s.scope_id !== null) root += '/scopes/' + encodeURIComponent(s.scope_id);
    }
  } catch (error) {
    if (!(error instanceof URIError)) throw error;
    fail('SHELL_ROUTE_INVALID');
  }
  return root + '/' + found.segments.map((seg) => {
    try {
      return encodeURIComponent(seg);
    } catch (error) {
      if (!(error instanceof URIError)) throw error;
      fail('SHELL_ROUTE_INVALID');
    }
  }).join('/');
}
export function buildWebPath(scope, operation, resolver) {
  return resolveTransport(resolver === undefined ? defaultTransportResolver() : resolver, scope, operation);
}
function response(value, scope) {
  record(value, ['status', 'body'], [], 'SHELL_RESPONSE_INVALID');
  if (!Number.isInteger(value.status) || value.status < 100 || value.status > 599) fail('SHELL_RESPONSE_INVALID');
  const body = jsonSnapshot(value.body);
  if (value.status === 200) {
    record(body, ['data', 'meta', 'links'], [], 'SHELL_RESPONSE_INVALID');
    if (body.meta === null || typeof body.meta !== 'object' || Array.isArray(body.meta) || body.links === null || typeof body.links !== 'object' || Array.isArray(body.links)) fail('SHELL_RESPONSE_INVALID');
    if (typeof body.meta.correlation_id !== 'string' || body.meta.correlation_id.length === 0 || !sameScope(validateScope(body.meta.context), scope)) fail('SHELL_RESPONSE_CONTEXT_MISMATCH');
  }
  if (value.status >= 400) {
    record(body, ['error_code', 'message', 'details', 'correlation_id'], ['field_errors'], 'SHELL_RESPONSE_INVALID');
    if (typeof body.error_code !== 'string' || !body.error_code || typeof body.message !== 'string' || typeof body.correlation_id !== 'string' || !body.correlation_id) fail('SHELL_RESPONSE_INVALID');
  }
  return Object.freeze({ status: value.status, body });
}
function clientPorts(value, method) {
  record(value, [method, 'contextProvider'], ['resolver'], 'SHELL_PORTS_INVALID');
  if (typeof value[method] !== 'function') fail('SHELL_PORT_MISSING');
  const provider = functions(value.contextProvider, ['snapshot', 'isCurrent']);
  let resolver = value.resolver;
  if (resolver === undefined) resolver = defaultTransportResolver();
  resolver = validateTransportResolver(resolver);
  return { send: value[method], provider, resolver };
}
function checkLimitValue(v) {
  if (typeof v !== 'number' || !Number.isSafeInteger(v) || v <= 0) fail('SHELL_QUERY_INVALID');
  return v;
}
function checkCursorValue(v) {
  if (typeof v !== 'string' || v.length === 0 || v.includes('\0')) fail('SHELL_QUERY_INVALID');
  return v;
}
function checkRefList(v) {
  denseNoUniq(v, 'SHELL_QUERY_INVALID');
  const seen = new Set();
  for (const x of v) {
    if (typeof x !== 'string' || x.length === 0 || x.includes('\0')) fail('SHELL_QUERY_INVALID');
    if (seen.has(x)) fail('SHELL_QUERY_INVALID');
    seen.add(x);
  }
  return Object.freeze([...v]);
}
export function createQueryClient(ports) {
  const { send, provider, resolver } = clientPorts(ports, 'fetchJson');
  return Object.freeze({
    async query(collection, options = {}) {
      record(options, [], ['params'], 'SHELL_QUERY_INVALID');
      if (typeof collection !== 'string' || collection.length === 0) fail('SHELL_ROUTE_INVALID');
      const snapshot = validateSnapshot(provider.snapshot());
      const path = resolveTransport(resolver, snapshot.scope, { kind: 'QUERY', name: collection });
      let binding = null;
      for (const b of resolver.operations) if (b.kind === 'QUERY' && b.name === collection) { binding = b; break; }
      if (!binding) fail('SHELL_ROUTE_INVALID');
      let params = options.params === undefined ? Object.freeze({}) : jsonSnapshot(options.params);
      if (params === null || typeof params !== 'object' || Array.isArray(params)) fail('SHELL_QUERY_INVALID');
      if (binding.owner === 'pixs.core') {
        record(params, [], ['limit', 'cursor', 'ref'], 'SHELL_QUERY_INVALID');
        const out = {};
        if (Object.hasOwn(params, 'limit')) out.limit = checkLimitValue(Object.getOwnPropertyDescriptor(params, 'limit').value);
        if (Object.hasOwn(params, 'cursor')) {
          out.cursor = checkCursorValue(Object.getOwnPropertyDescriptor(params, 'cursor').value);
        }
        if (Object.hasOwn(params, 'ref')) out.ref = checkRefList(Object.getOwnPropertyDescriptor(params, 'ref').value);
        params = Object.freeze({ ...out });
      }
      let raw;
      try { raw = await send(path, Object.freeze({ snapshot, params })); }
      catch (cause) { throw new ShellContractError('SHELL_QUERY_UNAVAILABLE', { cause }); }
      if (provider.isCurrent(snapshot) !== true) fail('SHELL_SNAPSHOT_STALE');
      const result = response(raw, snapshot.scope);
      if (result.status !== 200) fail('SHELL_QUERY_REFUSED');
      return result.body;
    },
  });
}
export function createCommandClient(ports) {
  const { send, provider, resolver } = clientPorts(ports, 'postJson');
  return Object.freeze({
    async intent(command, body, options) {
      record(options, ['idempotencyKey'], [], 'SHELL_IDEMPOTENCY_REQUIRED');
      if (typeof options.idempotencyKey !== 'string' || options.idempotencyKey.trim().length === 0) fail('SHELL_IDEMPOTENCY_REQUIRED');
      if (typeof command !== 'string' || command.length === 0) fail('SHELL_ROUTE_INVALID');
      const snapshot = validateSnapshot(provider.snapshot());
      const path = resolveTransport(resolver, snapshot.scope, { kind: 'COMMAND', name: command });
      const input = jsonSnapshot(body);
      if (input === null || typeof input !== 'object' || Array.isArray(input)) fail('SHELL_COMMAND_INVALID');
      let raw;
      try { raw = await send(path, input, Object.freeze({ idempotencyKey: options.idempotencyKey, snapshot })); }
      catch (cause) { throw new ShellContractError('SHELL_COMMAND_UNKNOWN', { cause }); }
      if (provider.isCurrent(snapshot) !== true) fail('SHELL_SNAPSHOT_STALE');
      const result = response(raw, snapshot.scope);
      if (result.status === 200) return Object.freeze({ state: 'CONFIRMED', response: result.body });
      if (result.status >= 400 && result.status < 500) return Object.freeze({ state: 'REJECTED', response: result.body });
      return Object.freeze({ state: 'UNKNOWN' });
    },
  });
}
const CONTEXT_FACTS = Object.freeze(['identity_ref', 'session_id', 'category', 'facade', 'authentication_time', 'expires_at', 'identity_assurance', 'authentication_assurance', 'ui_permissions']);
const SESSION_STATES = new Set(['INITIALIZING', 'ANONYMOUS', 'ACTIVE', 'EXPIRED', 'REVOKED', 'ERROR']);
export function validateShellContext(value) {
  record(value, ['state', 'epoch', 'scope'], CONTEXT_FACTS, 'SHELL_CONTEXT_INVALID');
  if (!SESSION_STATES.has(value.state) || !Number.isSafeInteger(value.epoch) || value.epoch < 0) fail('SHELL_CONTEXT_INVALID');
  if (value.state === 'ACTIVE') {
    validateScope(value.scope);
    for (const key of CONTEXT_FACTS.filter(key => key !== 'ui_permissions')) {
      if (typeof value[key] !== 'string' || value[key].length === 0) fail('SHELL_CONTEXT_INVALID');
    }
    if (!UUID7.test(value.session_id) || value.facade !== 'WEB') fail('SHELL_CONTEXT_INVALID');
    if (!['CLAIMED', 'VERIFIED', 'PROOFED'].includes(value.identity_assurance) || !['SINGLE_FACTOR', 'MULTI_FACTOR', 'PHISHING_RESISTANT'].includes(value.authentication_assurance)) fail('SHELL_CONTEXT_INVALID');
    for (const key of ['authentication_time', 'expires_at']) {
      if (!/(Z|\+00:00)$/.test(value[key]) || !Number.isFinite(Date.parse(value[key]))) fail('SHELL_CONTEXT_INVALID');
    }
  } else if (value.scope !== null || CONTEXT_FACTS.some(key => Object.hasOwn(value, key) && value[key] !== null)) fail('SHELL_CONTEXT_INVALID');
  const snapshot = jsonSnapshot(value);
  if (value.state === 'ACTIVE') {
    const hints = snapshot.ui_permissions;
    record(hints, ['status', 'items'], ['policy_version', 'evaluated_at'], 'SHELL_CONTEXT_INVALID');
    if (!Array.isArray(hints.items) || !['VERIFIED', 'UNAVAILABLE'].includes(hints.status)) fail('SHELL_CONTEXT_INVALID');
    if (hints.status === 'UNAVAILABLE' && (hints.items.length || Object.keys(hints).length !== 2)) fail('SHELL_CONTEXT_INVALID');
    if (hints.status === 'VERIFIED') {
      if (typeof hints.policy_version !== 'string' || !hints.policy_version || typeof hints.evaluated_at !== 'string' || !/(Z|\+00:00)$/.test(hints.evaluated_at) || !Number.isFinite(Date.parse(hints.evaluated_at))) fail('SHELL_CONTEXT_INVALID');
      for (const item of hints.items) {
        record(item, ['action_id', 'resource_id', 'allowed'], [], 'SHELL_CONTEXT_INVALID');
        if (typeof item.action_id !== 'string' || !item.action_id || typeof item.resource_id !== 'string' || !item.resource_id || typeof item.allowed !== 'boolean') fail('SHELL_CONTEXT_INVALID');
      }
    }
  }
  return snapshot;
}
const PUBLIC_PORTS = Object.freeze(['ShellContextProvider', 'useShellContext', 'getContextSnapshot', 'isCurrentSnapshot', 'fetchJson', 'postJson', 'navigate', 'invalidateScope', 'translate', 'present']);
export function createShellPorts(ports) { return functions(ports, PUBLIC_PORTS); }
export function bindShellApi(ports, resolver) {
  const p = createShellPorts(ports);
  const context = createContextProvider({ getContextSnapshot: p.getContextSnapshot, isCurrentSnapshot: p.isCurrentSnapshot });
  const r = resolver === undefined ? defaultTransportResolver() : validateTransportResolver(resolver);
  return Object.freeze({
    version: SHELL_API_VERSION,
    ShellContextProvider: (...args) => p.ShellContextProvider(...args),
    useShellContext: () => validateShellContext(p.useShellContext()),
    QueryClient: createQueryClient({ fetchJson: p.fetchJson, contextProvider: context, resolver: r }),
    CommandClient: createCommandClient({ postJson: p.postJson, contextProvider: context, resolver: r }),
    navigate: (...args) => p.navigate(...args),
    invalidateScope: (...args) => p.invalidateScope(...args),
    translate: (...args) => p.translate(...args),
    present: (...args) => p.present(...args),
  });
}
function boundApi(api) {
  record(api, ['version', 'ShellContextProvider', 'useShellContext', 'QueryClient', 'CommandClient', 'navigate', 'invalidateScope', 'translate', 'present'], [], 'SHELL_API_INVALID');
  if (api.version !== SHELL_API_VERSION) fail('SHELL_API_INVALID');
  for (const name of ['ShellContextProvider', 'useShellContext', 'navigate', 'invalidateScope', 'translate', 'present']) if (typeof api[name] !== 'function') fail('SHELL_API_INVALID');
  functions(api.QueryClient, ['query']);
  functions(api.CommandClient, ['intent']);
  return api;
}
export const QueryClient = createQueryClient;
export const CommandClient = createCommandClient;
export function ShellContextProvider(api, ...args) { return boundApi(api).ShellContextProvider(...args); }
export function useShellContext(api) { return validateShellContext(boundApi(api).useShellContext()); }
export function navigate(api, ...args) { return boundApi(api).navigate(...args); }
export function invalidateScope(api, ...args) { return boundApi(api).invalidateScope(...args); }
export function shellSlots() { return SLOT_IDS; }
