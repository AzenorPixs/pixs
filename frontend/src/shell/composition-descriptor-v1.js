export const COMPOSITION_DESCRIPTOR_VERSION = '1.0.0';
export const SHELL_CONTRACT_VERSION = '1.0.0';
export const DESCRIPTOR_SCHEMA = 'pixs.frontend.composition-descriptor/1.0.0';

const TYPES = Object.freeze([
  'ROUTE',
  'PAGE',
  'NAVIGATION',
  'COMPONENT',
  'FORM',
  'TRANSLATION',
  'UI_PERMISSION',
  'UI_SLOT',
]);
const TRUST_LEVELS = Object.freeze(['PLATFORM', 'TRUSTED', 'SANDBOXED', 'DEVELOPMENT']);
const SCOPES = Object.freeze(['PUBLIC', 'AUTHENTICATED', 'TENANT_SCOPED', 'PLATFORM_SCOPED']);
const GUARANTEES_REQUIRED = Object.freeze(['DATA_ONLY_DESCRIPTOR', 'EXPLICIT_ENTRY_EXPORTS']);

const POINT_RE = /^[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+$/;
const EXPORT_NAME_RE = /^[A-Za-z$][A-Za-z0-9_$]*$/;
const EXPORT_BLOCKED = new Set(['constructor', 'prototype', '__proto__']);
const SEGMENT_RE = /^[A-Za-z0-9_-]+$/;
const PARAM_RE = /^\{[a-z][a-z0-9_]*\}$/;
const LOCALE_RE = /^[a-z]{2}(?:-[A-Z]{2})?$/;
const DANGEROUS_KEYS = new Set(['__proto__', 'constructor', 'prototype']);

export const DESCRIPTOR_CODES = Object.freeze([
  'DESCRIPTOR_INVALID',
  'DESCRIPTOR_CONTEXT_INVALID',
  'DESCRIPTOR_LIMITS_INVALID',
  'DESCRIPTOR_FACET_INVALID',
  'DESCRIPTOR_POINTS_INVALID',
  'DESCRIPTOR_METADATA_INVALID',
  'DESCRIPTOR_POINT_UNKNOWN',
  'DESCRIPTOR_POINT_VERSION_INVALID',
  'DESCRIPTOR_SCHEMA_INVALID',
  'DESCRIPTOR_CATEGORY_MISMATCH',
  'DESCRIPTOR_GUARANTEES_INVALID',
  'DESCRIPTOR_VERSION_INVALID',
  'DESCRIPTOR_FACET_MISMATCH',
  'DESCRIPTOR_TRUST_INVALID',
  'DESCRIPTOR_SCOPE_INVALID',
  'DESCRIPTOR_SCOPE_MISMATCH',
  'DESCRIPTOR_PERMISSIONS_INVALID',
  'DESCRIPTOR_PATH_INVALID',
  'DESCRIPTOR_EXPORT_INVALID',
  'DESCRIPTOR_PAYLOAD_INVALID',
  'DESCRIPTOR_TYPE_INVALID',
  'DESCRIPTOR_DATA_INVALID',
]);

export class CompositionDescriptorError extends Error {
  constructor(code, options) {
    super(code, options);
    this.name = 'CompositionDescriptorError';
    this.code = code;
  }
}

function fail(code) {
  throw new CompositionDescriptorError(code);
}

function isPlainRecord(value) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) return false;
  const proto = Object.getPrototypeOf(value);
  return proto === Object.prototype || proto === null;
}

function record(value, required, optional = [], code = 'DESCRIPTOR_INVALID') {
  if (!isPlainRecord(value)) fail(code);
  const keys = Reflect.ownKeys(value);
  for (const key of keys) {
    if (typeof key !== 'string') fail(code);
    if (DANGEROUS_KEYS.has(key)) fail(code);
  }
  for (const name of required) {
    if (!Object.hasOwn(value, name)) fail(code);
  }
  for (const key of keys) {
    if (!required.includes(key) && !optional.includes(key)) fail(code);
  }
  for (const key of keys) {
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail(code);
  }
  return value;
}

function denseArray(value, code, max) {
  if (!Array.isArray(value)) fail(code);
  if (Object.getPrototypeOf(value) !== Array.prototype || value.length > max) fail(code);
  if (Reflect.ownKeys(value).length !== value.length + 1) fail(code);
  for (let index = 0; index < value.length; index += 1) {
    const descriptor = Object.getOwnPropertyDescriptor(value, String(index));
    if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail(code);
  }
  return value;
}

function safeInt(value, code) {
  if (typeof value !== 'number' || !Number.isSafeInteger(value) || value <= 0) fail(code);
  return value;
}

function validateLimits(limits) {
  record(
    limits,
    ['maxTextLength', 'maxRequires', 'maxPermissions', 'maxPoints', 'maxLocales', 'maxCatalogKeys'],
    [],
    'DESCRIPTOR_LIMITS_INVALID',
  );
  safeInt(limits.maxTextLength, 'DESCRIPTOR_LIMITS_INVALID');
  safeInt(limits.maxRequires, 'DESCRIPTOR_LIMITS_INVALID');
  safeInt(limits.maxPermissions, 'DESCRIPTOR_LIMITS_INVALID');
  safeInt(limits.maxPoints, 'DESCRIPTOR_LIMITS_INVALID');
  safeInt(limits.maxLocales, 'DESCRIPTOR_LIMITS_INVALID');
  safeInt(limits.maxCatalogKeys, 'DESCRIPTOR_LIMITS_INVALID');
  return limits;
}

function strictText(value, max, code = 'DESCRIPTOR_INVALID') {
  if (typeof value !== 'string' || value.length === 0 || value.length > max) fail(code);
  for (let index = 0; index < value.length; index += 1) {
    const unit = value.charCodeAt(index);
    if (unit >= 0xD800 && unit <= 0xDBFF) {
      const next = value.charCodeAt(index + 1);
      if (!(next >= 0xDC00 && next <= 0xDFFF)) fail(code);
      index += 1;
    } else if (unit >= 0xDC00 && unit <= 0xDFFF) fail(code);
    if (unit < 32 || unit === 127) fail(code);
  }
  return value;
}

function catalogText(value, max, code = 'DESCRIPTOR_PAYLOAD_INVALID') {
  if (typeof value !== 'string' || value.length === 0 || value.length > max) fail(code);
  for (let index = 0; index < value.length; index += 1) {
    const unit = value.charCodeAt(index);
    if (unit >= 0xD800 && unit <= 0xDBFF) {
      const next = value.charCodeAt(index + 1);
      if (!(next >= 0xDC00 && next <= 0xDFFF)) fail(code);
      index += 1;
    } else if (unit >= 0xDC00 && unit <= 0xDFFF) fail(code);
    if (unit === 0) fail(code);
    if (unit < 32 && unit !== 10) fail(code);
    if (unit === 127) fail(code);
  }
  return value;
}

function checkExportName(value, max) {
  strictText(value, max, 'DESCRIPTOR_EXPORT_INVALID');
  if (!EXPORT_NAME_RE.test(value)) fail('DESCRIPTOR_EXPORT_INVALID');
  if (value.startsWith('_')) fail('DESCRIPTOR_EXPORT_INVALID');
  if (EXPORT_BLOCKED.has(value)) fail('DESCRIPTOR_EXPORT_INVALID');
  return value;
}

function checkPath(value, max) {
  strictText(value, max, 'DESCRIPTOR_PATH_INVALID');
  if (!value.startsWith('/')) fail('DESCRIPTOR_PATH_INVALID');
  if (value.length > 1 && value.endsWith('/')) fail('DESCRIPTOR_PATH_INVALID');
  if (value.includes('//')) fail('DESCRIPTOR_PATH_INVALID');
  if (value.includes('\\')) fail('DESCRIPTOR_PATH_INVALID');
  if (value.includes('%') || value.includes('?') || value.includes('#')) fail('DESCRIPTOR_PATH_INVALID');
  if (value.includes(':') || value.includes(' ')) fail('DESCRIPTOR_PATH_INVALID');
  if (value === '/') return value;
  const parts = value.slice(1).split('/');
  for (const part of parts) {
    if (part === '' || part === '.' || part === '..') fail('DESCRIPTOR_PATH_INVALID');
    if (SEGMENT_RE.test(part)) continue;
    if (PARAM_RE.test(part)) continue;
    fail('DESCRIPTOR_PATH_INVALID');
  }
  return value;
}

function validateFacetRef(facet, limits) {
  record(
    facet,
    ['owner', 'owner_version', 'type', 'id', 'entry', 'version', 'requires', 'scope'],
    [],
    'DESCRIPTOR_FACET_INVALID',
  );
  strictText(facet.owner, limits.maxTextLength, 'DESCRIPTOR_FACET_INVALID');
  strictText(facet.owner_version, limits.maxTextLength, 'DESCRIPTOR_FACET_INVALID');
  strictText(facet.type, limits.maxTextLength, 'DESCRIPTOR_FACET_INVALID');
  if (!TYPES.includes(facet.type)) fail('DESCRIPTOR_FACET_INVALID');
  strictText(facet.id, limits.maxTextLength, 'DESCRIPTOR_FACET_INVALID');
  strictText(facet.entry, limits.maxTextLength, 'DESCRIPTOR_FACET_INVALID');
  strictText(facet.version, limits.maxTextLength, 'DESCRIPTOR_FACET_INVALID');
  strictText(facet.scope, limits.maxTextLength, 'DESCRIPTOR_FACET_INVALID');
  if (!SCOPES.includes(facet.scope)) fail('DESCRIPTOR_FACET_INVALID');
  denseArray(facet.requires, 'DESCRIPTOR_FACET_INVALID', limits.maxRequires);
  if (facet.requires.length > limits.maxRequires) fail('DESCRIPTOR_FACET_INVALID');
  for (const item of facet.requires) strictText(item, limits.maxTextLength, 'DESCRIPTOR_FACET_INVALID');
  return facet;
}

function validatePointDef(def, limits) {
  record(def, ['owner', 'category', 'version', 'schema', 'guarantees'], [], 'DESCRIPTOR_POINTS_INVALID');
  strictText(def.owner, limits.maxTextLength, 'DESCRIPTOR_POINTS_INVALID');
  strictText(def.category, limits.maxTextLength, 'DESCRIPTOR_POINTS_INVALID');
  if (!TYPES.includes(def.category)) fail('DESCRIPTOR_POINTS_INVALID');
  if (def.version !== '1.0.0') fail('DESCRIPTOR_POINT_VERSION_INVALID');
  if (def.schema !== DESCRIPTOR_SCHEMA) fail('DESCRIPTOR_SCHEMA_INVALID');
  denseArray(def.guarantees, 'DESCRIPTOR_GUARANTEES_INVALID', GUARANTEES_REQUIRED.length);
  if (def.guarantees.length === 0) fail('DESCRIPTOR_GUARANTEES_INVALID');
  for (const item of def.guarantees) {
    strictText(item, limits.maxTextLength, 'DESCRIPTOR_GUARANTEES_INVALID');
    if (!GUARANTEES_REQUIRED.includes(item)) fail('DESCRIPTOR_GUARANTEES_INVALID');
  }
  if (!GUARANTEES_REQUIRED.every((name) => def.guarantees.includes(name))) {
    fail('DESCRIPTOR_GUARANTEES_INVALID');
  }
  if (new Set(def.guarantees).size !== def.guarantees.length) fail('DESCRIPTOR_GUARANTEES_INVALID');
  return def;
}

function validateExtensionPoints(registry, limits) {
  record(registry, ['points', 'metadata'], [], 'DESCRIPTOR_POINTS_INVALID');
  record(registry.metadata, ['version', 'schema'], [], 'DESCRIPTOR_METADATA_INVALID');
  if (registry.metadata.version !== '1.0.0') fail('DESCRIPTOR_POINT_VERSION_INVALID');
  if (registry.metadata.schema !== DESCRIPTOR_SCHEMA) fail('DESCRIPTOR_SCHEMA_INVALID');
  if (!isPlainRecord(registry.points)) fail('DESCRIPTOR_POINTS_INVALID');
  const ids = Reflect.ownKeys(registry.points);
  if (ids.length === 0 || ids.length > limits.maxPoints) fail('DESCRIPTOR_POINTS_INVALID');
  for (const id of ids) {
    if (typeof id !== 'string') fail('DESCRIPTOR_POINTS_INVALID');
    if (DANGEROUS_KEYS.has(id)) fail('DESCRIPTOR_POINTS_INVALID');
    strictText(id, limits.maxTextLength, 'DESCRIPTOR_POINTS_INVALID');
    if (!POINT_RE.test(id)) fail('DESCRIPTOR_POINTS_INVALID');
    const descriptor = Object.getOwnPropertyDescriptor(registry.points, id);
    if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail('DESCRIPTOR_POINTS_INVALID');
    validatePointDef(descriptor.value, limits);
  }
  return registry;
}

function validateDisplayPermissions(value, limits) {
  denseArray(value, 'DESCRIPTOR_PERMISSIONS_INVALID', limits.maxPermissions);
  if (value.length > limits.maxPermissions) fail('DESCRIPTOR_PERMISSIONS_INVALID');
  for (const item of value) strictText(item, limits.maxTextLength, 'DESCRIPTOR_PERMISSIONS_INVALID');
  return value;
}

function validateCatalog(value, limits) {
  if (!isPlainRecord(value)) fail('DESCRIPTOR_PAYLOAD_INVALID');
  const locales = Reflect.ownKeys(value);
  if (locales.length === 0 || locales.length > limits.maxLocales) fail('DESCRIPTOR_PAYLOAD_INVALID');
  let total = 0;
  for (const locale of locales) {
    if (typeof locale !== 'string') fail('DESCRIPTOR_PAYLOAD_INVALID');
    if (DANGEROUS_KEYS.has(locale)) fail('DESCRIPTOR_PAYLOAD_INVALID');
    strictText(locale, limits.maxTextLength, 'DESCRIPTOR_PAYLOAD_INVALID');
    if (!LOCALE_RE.test(locale)) fail('DESCRIPTOR_PAYLOAD_INVALID');
    const holder = Object.getOwnPropertyDescriptor(value, locale);
    if (!holder || !Object.hasOwn(holder, 'value')) fail('DESCRIPTOR_PAYLOAD_INVALID');
    const table = holder.value;
    if (!isPlainRecord(table)) fail('DESCRIPTOR_PAYLOAD_INVALID');
    const names = Reflect.ownKeys(table);
    if (names.length === 0) fail('DESCRIPTOR_PAYLOAD_INVALID');
    total += names.length;
    if (total > limits.maxCatalogKeys) fail('DESCRIPTOR_PAYLOAD_INVALID');
    for (const name of names) {
      if (typeof name !== 'string') fail('DESCRIPTOR_PAYLOAD_INVALID');
      if (DANGEROUS_KEYS.has(name)) fail('DESCRIPTOR_PAYLOAD_INVALID');
      strictText(name, limits.maxTextLength, 'DESCRIPTOR_PAYLOAD_INVALID');
      if (!POINT_RE.test(name)) fail('DESCRIPTOR_PAYLOAD_INVALID');
      const cell = Object.getOwnPropertyDescriptor(table, name);
      if (!cell || !Object.hasOwn(cell, 'value')) fail('DESCRIPTOR_PAYLOAD_INVALID');
      catalogText(cell.value, limits.maxTextLength, 'DESCRIPTOR_PAYLOAD_INVALID');
    }
  }
  return value;
}

function validatePayload(type, payload, pointId, limits) {
  if (!isPlainRecord(payload)) fail('DESCRIPTOR_PAYLOAD_INVALID');
  if (type === 'ROUTE') {
    record(payload, ['path', 'mode', 'page'], [], 'DESCRIPTOR_PAYLOAD_INVALID');
    checkPath(payload.path, limits.maxTextLength);
    if (payload.mode !== 'CSR') fail('DESCRIPTOR_PAYLOAD_INVALID');
    checkExportName(payload.page, limits.maxTextLength);
    return payload;
  }
  if (type === 'PAGE' || type === 'COMPONENT' || type === 'FORM') {
    record(payload, ['export'], [], 'DESCRIPTOR_PAYLOAD_INVALID');
    checkExportName(payload.export, limits.maxTextLength);
    return payload;
  }
  if (type === 'NAVIGATION') {
    record(payload, ['route', 'labelKey'], [], 'DESCRIPTOR_PAYLOAD_INVALID');
    checkPath(payload.route, limits.maxTextLength);
    strictText(payload.labelKey, limits.maxTextLength, 'DESCRIPTOR_PAYLOAD_INVALID');
    if (!POINT_RE.test(payload.labelKey)) {
      fail('DESCRIPTOR_PAYLOAD_INVALID');
    }
    return payload;
  }
  if (type === 'TRANSLATION') {
    record(payload, ['catalog'], [], 'DESCRIPTOR_PAYLOAD_INVALID');
    validateCatalog(payload.catalog, limits);
    return payload;
  }
  if (type === 'UI_PERMISSION') {
    record(payload, ['key', 'fallback'], [], 'DESCRIPTOR_PAYLOAD_INVALID');
    strictText(payload.key, limits.maxTextLength, 'DESCRIPTOR_PAYLOAD_INVALID');
    if (!POINT_RE.test(payload.key)) fail('DESCRIPTOR_PAYLOAD_INVALID');
    strictText(payload.fallback, limits.maxTextLength, 'DESCRIPTOR_PAYLOAD_INVALID');
    return payload;
  }
  if (type === 'UI_SLOT') {
    record(payload, ['slot', 'export'], [], 'DESCRIPTOR_PAYLOAD_INVALID');
    strictText(payload.slot, limits.maxTextLength, 'DESCRIPTOR_PAYLOAD_INVALID');
    if (payload.slot !== pointId) fail('DESCRIPTOR_PAYLOAD_INVALID');
    checkExportName(payload.export, limits.maxTextLength);
    return payload;
  }
  fail('DESCRIPTOR_TYPE_INVALID');
}

function snapshotDescriptor(value) {
  const out = {};
  Object.defineProperty(out, 'descriptor_version', { value: value.descriptor_version, enumerable: true });
  Object.defineProperty(out, 'owner', { value: value.owner, enumerable: true });
  Object.defineProperty(out, 'owner_version', { value: value.owner_version, enumerable: true });
  Object.defineProperty(out, 'type', { value: value.type, enumerable: true });
  Object.defineProperty(out, 'id', { value: value.id, enumerable: true });
  Object.defineProperty(out, 'entry', { value: value.entry, enumerable: true });
  Object.defineProperty(out, 'version', { value: value.version, enumerable: true });
  const requires = [];
  for (let index = 0; index < value.requires.length; index += 1) {
    requires.push(value.requires[index]);
  }
  Object.defineProperty(out, 'requires', { value: Object.freeze(requires), enumerable: true });
  Object.defineProperty(out, 'scope', { value: value.scope, enumerable: true });
  Object.defineProperty(out, 'point', { value: value.point, enumerable: true });
  Object.defineProperty(out, 'point_version', { value: value.point_version, enumerable: true });
  const permissions = [];
  for (let index = 0; index < value.display_permissions.length; index += 1) {
    permissions.push(value.display_permissions[index]);
  }
  Object.defineProperty(out, 'display_permissions', {
    value: Object.freeze(permissions),
    enumerable: true,
  });
  Object.defineProperty(out, 'trust', { value: value.trust, enumerable: true });
  Object.defineProperty(out, 'mandatory', { value: value.mandatory, enumerable: true });
  Object.defineProperty(out, 'activation_scope', { value: value.activation_scope, enumerable: true });
  const payload = {};
  const source = value.payload;
  for (const key of Reflect.ownKeys(source)) {
    const holder = Object.getOwnPropertyDescriptor(source, key);
    if (key === 'catalog') {
      const catalog = {};
      for (const locale of Reflect.ownKeys(holder.value)) {
        const tableHolder = Object.getOwnPropertyDescriptor(holder.value, locale);
        const table = {};
        for (const name of Reflect.ownKeys(tableHolder.value)) {
          Object.defineProperty(table, name, {
            value: Object.getOwnPropertyDescriptor(tableHolder.value, name).value,
            enumerable: true,
          });
        }
        Object.defineProperty(catalog, locale, { value: Object.freeze(table), enumerable: true });
      }
      Object.defineProperty(payload, 'catalog', { value: Object.freeze(catalog), enumerable: true });
    } else {
      Object.defineProperty(payload, key, { value: holder.value, enumerable: true });
    }
  }
  Object.defineProperty(out, 'payload', { value: Object.freeze(payload), enumerable: true });
  return Object.freeze(out);
}

export function validateCompositionDescriptor(value, context) {
  record(context, ['facet', 'extensionPoints', 'limits'], [], 'DESCRIPTOR_CONTEXT_INVALID');
  const limits = validateLimits(context.limits);
  const facet = validateFacetRef(context.facet, limits);
  const registry = validateExtensionPoints(context.extensionPoints, limits);
  record(
    value,
    [
      'descriptor_version',
      'owner',
      'owner_version',
      'type',
      'id',
      'entry',
      'version',
      'requires',
      'scope',
      'point',
      'point_version',
      'display_permissions',
      'trust',
      'mandatory',
      'activation_scope',
      'payload',
    ],
    [],
    'DESCRIPTOR_INVALID',
  );
  if (value.descriptor_version !== COMPOSITION_DESCRIPTOR_VERSION) fail('DESCRIPTOR_VERSION_INVALID');
  if (value.point_version !== SHELL_CONTRACT_VERSION) fail('DESCRIPTOR_POINT_VERSION_INVALID');
  if (value.point_version !== registry.metadata.version) fail('DESCRIPTOR_POINT_VERSION_INVALID');
  if (
    value.owner !== facet.owner ||
    value.owner_version !== facet.owner_version ||
    value.type !== facet.type ||
    value.id !== facet.id ||
    value.entry !== facet.entry ||
    value.version !== facet.version ||
    value.scope !== facet.scope
  ) {
    fail('DESCRIPTOR_FACET_MISMATCH');
  }
  denseArray(value.requires, 'DESCRIPTOR_INVALID', limits.maxRequires);
  if (value.requires.length !== facet.requires.length) fail('DESCRIPTOR_FACET_MISMATCH');
  if (value.requires.length > limits.maxRequires) fail('DESCRIPTOR_INVALID');
  for (let index = 0; index < value.requires.length; index += 1) {
    if (value.requires[index] !== facet.requires[index]) fail('DESCRIPTOR_FACET_MISMATCH');
  }
  strictText(value.point, limits.maxTextLength, 'DESCRIPTOR_INVALID');
  if (!Object.hasOwn(registry.points, value.point)) fail('DESCRIPTOR_POINT_UNKNOWN');
  const point = registry.points[value.point];
  if (point.category !== value.type) fail('DESCRIPTOR_CATEGORY_MISMATCH');
  if (point.version !== value.point_version) fail('DESCRIPTOR_POINT_VERSION_INVALID');
  if (point.schema !== DESCRIPTOR_SCHEMA) fail('DESCRIPTOR_SCHEMA_INVALID');
  if (typeof value.mandatory !== 'boolean') fail('DESCRIPTOR_INVALID');
  if (!TRUST_LEVELS.includes(value.trust)) fail('DESCRIPTOR_TRUST_INVALID');
  if (!SCOPES.includes(value.activation_scope)) fail('DESCRIPTOR_SCOPE_INVALID');
  if (value.activation_scope !== facet.scope) fail('DESCRIPTOR_SCOPE_MISMATCH');
  validateDisplayPermissions(value.display_permissions, limits);
  validatePayload(value.type, value.payload, value.point, limits);
  return snapshotDescriptor(value);
}

function shellPoint(category) {
  return Object.freeze({
    owner: 'pixs.shell',
    category,
    version: '1.0.0',
    schema: DESCRIPTOR_SCHEMA,
    guarantees: Object.freeze(['DATA_ONLY_DESCRIPTOR', 'EXPLICIT_ENTRY_EXPORTS']),
  });
}

export function createShellExtensionPoints() {
  const entries = [
    ['pixs.shell.routes', shellPoint('ROUTE')],
    ['pixs.shell.pages', shellPoint('PAGE')],
    ['pixs.shell.navigation-items', shellPoint('NAVIGATION')],
    ['pixs.shell.components', shellPoint('COMPONENT')],
    ['pixs.shell.forms', shellPoint('FORM')],
    ['pixs.shell.translations', shellPoint('TRANSLATION')],
    ['pixs.shell.ui-permissions', shellPoint('UI_PERMISSION')],
    ['pixs.shell.header', shellPoint('UI_SLOT')],
    ['pixs.shell.navigation', shellPoint('UI_SLOT')],
    ['pixs.shell.main', shellPoint('UI_SLOT')],
    ['pixs.shell.footer', shellPoint('UI_SLOT')],
  ];
  const seen = new Set();
  for (const [id] of entries) {
    if (seen.has(id)) fail('DESCRIPTOR_POINTS_INVALID');
    seen.add(id);
  }
  return Object.freeze({
    points: Object.freeze(Object.fromEntries(entries)),
    metadata: Object.freeze({ version: '1.0.0', schema: DESCRIPTOR_SCHEMA }),
  });
}
