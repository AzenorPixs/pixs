// Contrat pur de présentation, sans exécution d’action ni autorité d’identité.
// Les références locales viennent du build/shell de confiance ; copie JSON bornée avant validation.
export const PRESENTATION_SCHEMA = 'pixs.presentation/1.0.0';

export const PRESENTATION_CODES = Object.freeze([
  'PRESENTATION_CONTEXT_INVALID',
  'PRESENTATION_LIMITS_INVALID',
  'PRESENTATION_CATALOG_INVALID',
  'PRESENTATION_ROUTE_INVALID',
  'PRESENTATION_SLOT_INVALID',
  'PRESENTATION_COMPONENT_INVALID',
  'PRESENTATION_TREE_INVALID',
  'PRESENTATION_KIND_INVALID',
  'PRESENTATION_VARIANT_INVALID',
  'PRESENTATION_PROPS_INVALID',
  'PRESENTATION_CHILDREN_INVALID',
  'PRESENTATION_PARENT_INVALID',
  'PRESENTATION_LABEL_INVALID',
  'PRESENTATION_PARAMS_INVALID',
  'PRESENTATION_LINK_INVALID',
  'PRESENTATION_FIELD_INVALID',
  'PRESENTATION_FORM_INVALID',
  'PRESENTATION_INTENT_INVALID',
  'PRESENTATION_COMMAND_INVALID',
  'PRESENTATION_BODY_INVALID',
  'PRESENTATION_BINDING_INVALID',
  'PRESENTATION_BUTTON_INVALID',
  'PRESENTATION_STATUS_INVALID',
  'PRESENTATION_TEXT_INVALID',
  'PRESENTATION_ACTION_INVALID',
  'PRESENTATION_MODEL_INVALID',
  'PRESENTATION_COLUMNS_INVALID',
  'PRESENTATION_RECORD_INVALID',
  'PRESENTATION_LIMIT_EXCEEDED',
  'PRESENTATION_CYCLE_INVALID',
]);

export class PresentationContractError extends Error {
  constructor(code, options) {
    super(code, options);
    this.name = 'PresentationContractError';
    this.code = code;
  }
}

function fail(code) {
  throw new PresentationContractError(code);
}

function isPlainRecord(value) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) return false;
  const proto = Object.getPrototypeOf(value);
  return proto === Object.prototype || proto === null;
}

function closedRecord(value, required, code) {
  if (!isPlainRecord(value)) fail(code);
  const keys = Reflect.ownKeys(value);
  if (keys.length !== required.length) fail(code);
  for (const key of keys) {
    if (typeof key !== 'string' || !required.includes(key)) fail(code);
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') fail(code);
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail(code);
  }
  for (const name of required) if (!Object.hasOwn(value, name)) fail(code);
  return value;
}

function denseArray(value, max, code) {
  if (!Array.isArray(value)) fail(code);
  if (Object.getPrototypeOf(value) !== Array.prototype) fail(code);
  if (value.length > max) fail('PRESENTATION_LIMIT_EXCEEDED');
  if (Reflect.ownKeys(value).length !== value.length + 1) fail(code);
  for (let index = 0; index < value.length; index += 1) {
    const descriptor = Object.getOwnPropertyDescriptor(value, String(index));
    if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail(code);
  }
  return value;
}

function safePositiveInt(value) {
  if (typeof value !== 'number' || !Number.isSafeInteger(value) || value <= 0) fail('PRESENTATION_LIMITS_INVALID');
  return value;
}

function checkSurrogates(value, code) {
  for (let index = 0; index < value.length; index += 1) {
    const unit = value.charCodeAt(index);
    if (unit >= 0xd800 && unit <= 0xdbff) {
      const next = value.charCodeAt(index + 1);
      if (!(next >= 0xdc00 && next <= 0xdfff)) fail(code);
      index += 1;
    } else if (unit >= 0xdc00 && unit <= 0xdfff) {
      fail(code);
    }
    if (unit === 0 || unit === 13) fail(code);
    if (unit < 32 && unit !== 10) fail(code);
    if (unit === 127) fail(code);
  }
}

// Texte strict monocarte : identifiants, chemins, noms (LF refusé, sous-ensemble sûr).
function strictLine(value, max, code) {
  if (typeof value !== 'string' || value.length === 0 || value.length > max) fail(code);
  checkSurrogates(value, code);
  if (value.includes('\n')) fail(code);
  return value;
}

// Texte affichable : LF autorisé, NUL/CR refusés.
function displayText(value, max, code, allowEmpty) {
  if (typeof value !== 'string') fail(code);
  if ((!allowEmpty && value.length === 0) || value.length > max) fail(code);
  if (allowEmpty && value.length === 0) return value;
  checkSurrogates(value, code);
  return value;
}

const POINT_RE = /^[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+$/;
const FIELD_RE = /^[a-z][a-z0-9_]*$/;
const COMMAND_RE = /^[A-Za-z][A-Za-z0-9_-]*(?:\.[A-Za-z0-9_-]+)*$/;
const COMMAND_BLOCKED = new Set(['auth', 'csrf', 'shell', 'shell-context']);
const SEGMENT_RE = /^[A-Za-z0-9_-]+$/;
const PARAM_SEGMENT_RE = /^[a-z][a-z0-9_]*$/;
const PROP_SEGMENT_RE = /^[A-Za-z][A-Za-z0-9_]*$/;
const ACTION_ID_RE = /^[A-Za-z][A-Za-z0-9_-]*$/;
const DANGEROUS_KEYS = new Set(['__proto__', 'constructor', 'prototype']);

const KINDS = Object.freeze([
  'section', 'heading', 'text', 'link', 'button', 'field', 'form', 'slot', 'status', 'component',
]);

const VARIANTS = Object.freeze({
  section: Object.freeze(['panel', 'stack', 'row']),
  heading: Object.freeze(['page', 'section']),
  text: Object.freeze(['body', 'muted']),
  link: Object.freeze(['default']),
  button: Object.freeze(['primary', 'secondary']),
  field: Object.freeze(['text', 'boolean', 'integer', 'string-list', 'record-list']),
  form: Object.freeze(['stack']),
  slot: Object.freeze(['append']),
  status: Object.freeze(['command', 'query']),
  component: Object.freeze(['public']),
});

const PROPS = Object.freeze({
  section: Object.freeze([]),
  heading: Object.freeze(['key', 'params']),
  text: Object.freeze(['key', 'params']),
  link: Object.freeze(['key', 'params', 'route', 'routeParams']),
  button: Object.freeze(['id', 'key', 'params', 'submit', 'intent']),
  field: Object.freeze(['name', 'key', 'params', 'required', 'initial']),
  form: Object.freeze(['id', 'key', 'params', 'intent']),
  slot: Object.freeze(['point']),
  status: Object.freeze(['for']),
  component: Object.freeze(['owner', 'id']),
});
const FIELD_BASE_PROPS = Object.freeze(['name', 'key', 'params', 'required', 'initial']);
const FIELD_RECORD_PROPS = Object.freeze(['name', 'key', 'params', 'required', 'initial', 'minItems', 'maxItems', 'columns']);
const COMMAND_INTENT_PROPS = Object.freeze(['command', 'body', 'bindings']);
const QUERY_INTENT_PROPS = Object.freeze(['query', 'params', 'bindings']);
const FIELD_COLUMN_PROPS = Object.freeze(['name', 'key', 'params', 'required']);

const LIMIT_NAMES = Object.freeze([
  'maxNodes', 'maxDepth', 'maxChildren', 'maxTextLength', 'maxParams',
  'maxFields', 'maxBindings', 'maxDataNodes', 'maxBodyDepth', 'maxBodyNodes',
]);

const SECTION_CHILDREN = new Set(['section', 'form', 'heading', 'text', 'link', 'slot', 'component']);
const FORM_CHILDREN = new Set(['section', 'heading', 'text', 'field', 'button', 'status']);
const LEAF_KINDS = new Set(['heading', 'text', 'link', 'button', 'field', 'slot', 'status', 'component']);

function validateLimits(limits) {
  closedRecord(limits, [...LIMIT_NAMES], 'PRESENTATION_LIMITS_INVALID');
  for (const name of LIMIT_NAMES) safePositiveInt(limits[name]);
  return limits;
}

function catalogParamNames(text) {
  const names = new Set();
  for (let index = 0; index < text.length; index += 1) {
    if (text[index] === '}') fail('PRESENTATION_CATALOG_INVALID');
    if (text[index] !== '{') continue;
    const end = text.indexOf('}', index + 1);
    if (end < 0) fail('PRESENTATION_CATALOG_INVALID');
    const name = text.slice(index + 1, end);
    if (!PROP_SEGMENT_RE.test(name)) fail('PRESENTATION_CATALOG_INVALID');
    names.add(name);
    index = end;
  }
  return names;
}

function validateContext(context) {
  closedRecord(context, ['owner', 'id', 'catalogs', 'routes', 'slots', 'components', 'limits'], 'PRESENTATION_CONTEXT_INVALID');
  const limits = validateLimits(context.limits);
  const maxText = limits.maxTextLength;
  strictLine(context.owner, maxText, 'PRESENTATION_CONTEXT_INVALID');
  strictLine(context.id, maxText, 'PRESENTATION_CONTEXT_INVALID');
  if (!POINT_RE.test(context.owner) && !SEGMENT_RE.test(context.owner)) fail('PRESENTATION_CONTEXT_INVALID');
  if(!POINT_RE.test(context.id)||!(context.id===context.owner||context.id.startsWith(context.owner+'.')))fail('PRESENTATION_CONTEXT_INVALID');

  closedRecord(context.catalogs, ['en', 'fr'], 'PRESENTATION_CATALOG_INVALID');
  for (const locale of ['en', 'fr']) {
    const table = context.catalogs[locale];
    if (!isPlainRecord(table)) fail('PRESENTATION_CATALOG_INVALID');
    for (const key of Reflect.ownKeys(table)) {
      if (typeof key !== 'string' || DANGEROUS_KEYS.has(key)) fail('PRESENTATION_CATALOG_INVALID');
      const descriptor = Object.getOwnPropertyDescriptor(table, key);
      if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail('PRESENTATION_CATALOG_INVALID');
    }
  }
  const enKeys = Reflect.ownKeys(context.catalogs.en);
  const frKeys = Reflect.ownKeys(context.catalogs.fr);
  if (enKeys.length !== frKeys.length) fail('PRESENTATION_CATALOG_INVALID');
  const keyParams = new Map();
  for (const key of enKeys) {
    if (typeof key !== 'string') fail('PRESENTATION_CATALOG_INVALID');
    strictLine(key, maxText, 'PRESENTATION_CATALOG_INVALID');
    if(!POINT_RE.test(key))fail('PRESENTATION_CATALOG_INVALID');
    if (!(key === context.owner || key.startsWith(context.owner + '.'))) fail('PRESENTATION_CATALOG_INVALID');
    if (!Object.hasOwn(context.catalogs.fr, key)) fail('PRESENTATION_CATALOG_INVALID');
    const enText = context.catalogs.en[key];
    const frText = context.catalogs.fr[key];
    displayText(enText, maxText, 'PRESENTATION_CATALOG_INVALID', false);
    displayText(frText, maxText, 'PRESENTATION_CATALOG_INVALID', false);
    const expected = catalogParamNames(enText);
    const actual = catalogParamNames(frText);
    if (expected.size !== actual.size || [...expected].some((name) => !actual.has(name))) fail('PRESENTATION_CATALOG_INVALID');
    keyParams.set(key, expected);
  }

  denseArray(context.routes, limits.maxDataNodes, 'PRESENTATION_ROUTE_INVALID');
  const routeParams = new Map();
  const seenRoutes = new Set();
  for (const route of context.routes) {
    strictLine(route, maxText, 'PRESENTATION_ROUTE_INVALID');
    if (!route.startsWith('/')) fail('PRESENTATION_ROUTE_INVALID');
    if (route.length > 1 && route.endsWith('/')) fail('PRESENTATION_ROUTE_INVALID');
    if (route.includes('//') || route.includes('\\') || route.includes('%') || route.includes('?') || route.includes('#') || route.includes(':') || route.includes(' ')) {
      fail('PRESENTATION_ROUTE_INVALID');
    }
    if (seenRoutes.has(route)) fail('PRESENTATION_ROUTE_INVALID');
    seenRoutes.add(route);
    if (route !== '/') {
      const parts = route.slice(1).split('/');
      const params = [];
      for (const part of parts) {
        if (part === '' || part === '.' || part === '..') fail('PRESENTATION_ROUTE_INVALID');
        if (SEGMENT_RE.test(part)) continue;
        if (part.length >= 3 && part.startsWith('{') && part.endsWith('}')) {
          const name = part.slice(1, -1);
          if (!PARAM_SEGMENT_RE.test(name)) fail('PRESENTATION_ROUTE_INVALID');
          if (params.includes(name)) fail('PRESENTATION_ROUTE_INVALID');
          params.push(name);
          continue;
        }
        fail('PRESENTATION_ROUTE_INVALID');
      }
      routeParams.set(route, params);
    } else {
      routeParams.set(route, []);
    }
  }

  denseArray(context.slots, limits.maxDataNodes, 'PRESENTATION_SLOT_INVALID');
  const slots = new Set();
  for (const point of context.slots) {
    strictLine(point, maxText, 'PRESENTATION_SLOT_INVALID');
    if (!POINT_RE.test(point)||!(point===context.owner||point.startsWith(context.owner+'.'))) fail('PRESENTATION_SLOT_INVALID');
    if (slots.has(point)) fail('PRESENTATION_SLOT_INVALID');
    slots.add(point);
  }

  denseArray(context.components, limits.maxDataNodes, 'PRESENTATION_COMPONENT_INVALID');
  const components = new Map();
  for (const entry of context.components) {
    closedRecord(entry, ['owner', 'id'], 'PRESENTATION_COMPONENT_INVALID');
    strictLine(entry.owner, maxText, 'PRESENTATION_COMPONENT_INVALID');
    strictLine(entry.id, maxText, 'PRESENTATION_COMPONENT_INVALID');
    if(!POINT_RE.test(entry.id)||!(entry.id===entry.owner||entry.id.startsWith(entry.owner+'.')))fail('PRESENTATION_COMPONENT_INVALID');
    const key = JSON.stringify([entry.owner, entry.id]);
    if (components.has(key)) fail('PRESENTATION_COMPONENT_INVALID');
    components.set(key, { owner: entry.owner, id: entry.id });
  }

  return { owner: context.owner, id: context.id, limits, keyParams, routeParams, slots, components };
}

function validateLabel(key, params, ctx, maxText, maxParams) {
  strictLine(key, maxText, 'PRESENTATION_LABEL_INVALID');
  if (!ctx.keyParams.has(key)) fail('PRESENTATION_LABEL_INVALID');
  if (!isPlainRecord(params)) fail('PRESENTATION_PARAMS_INVALID');
  const keys = Reflect.ownKeys(params);
  if (keys.length > maxParams) fail('PRESENTATION_LIMIT_EXCEEDED');
  const expected = ctx.keyParams.get(key);
  if (keys.length !== expected.size) fail('PRESENTATION_PARAMS_INVALID');
  for (const name of keys) {
    if (typeof name !== 'string' || DANGEROUS_KEYS.has(name)) fail('PRESENTATION_PARAMS_INVALID');
    if (!expected.has(name)) fail('PRESENTATION_PARAMS_INVALID');
    const descriptor = Object.getOwnPropertyDescriptor(params, name);
    if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail('PRESENTATION_PARAMS_INVALID');
    const value = descriptor.value;
    if (typeof value === 'string') {
      displayText(value, maxText, 'PRESENTATION_PARAMS_INVALID', true);
    } else if (typeof value === 'number') {
      if (!Number.isFinite(value)) fail('PRESENTATION_PARAMS_INVALID');
    } else if (typeof value !== 'boolean') {
      fail('PRESENTATION_PARAMS_INVALID');
    }
  }
  return true;
}

function validateRouteParams(route, routeParams, ctx, maxText) {
  strictLine(route, maxText, 'PRESENTATION_LINK_INVALID');
  if (!ctx.routeParams.has(route)) fail('PRESENTATION_LINK_INVALID');
  if (!isPlainRecord(routeParams)) fail('PRESENTATION_LINK_INVALID');
  const expected = ctx.routeParams.get(route);
  const keys = Reflect.ownKeys(routeParams);
  if (keys.length !== expected.length) fail('PRESENTATION_LINK_INVALID');
  for (const name of keys) {
    if (typeof name !== 'string' || !expected.includes(name)) fail('PRESENTATION_LINK_INVALID');
    const descriptor = Object.getOwnPropertyDescriptor(routeParams, name);
    if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail('PRESENTATION_LINK_INVALID');
    const value = descriptor.value;
    if (typeof value !== 'string' || value.length === 0 || value.length > maxText) fail('PRESENTATION_LINK_INVALID');
    checkSurrogates(value, 'PRESENTATION_LINK_INVALID');
    if (value === '.' || value === '..') fail('PRESENTATION_LINK_INVALID');
    for (let index = 0; index < value.length; index += 1) {
      const unit = value.charCodeAt(index);
      if (unit < 32 || unit === 127) fail('PRESENTATION_LINK_INVALID');
      const character = value[index];
      if (character === '/' || character === '\\' || character === '%' || character === '?' || character === '#' || character === ':') {
        fail('PRESENTATION_LINK_INVALID');
      }
    }
  }
  return true;
}

// Clone JSON générique itératif : quotas avant allocation, alias recopiés,
// cycles/accèsseurs/symboles/exotiques refusés, aucune récursion.
function cloneJson(root,counters,limits,code){
  const holder={},active=new Set();
  const pending=[{source:root,parent:holder,key:'value',depth:0}],max=limits.maxDataNodes;
  let scheduled=1;
  while(pending.length){
    const frame=pending.pop();
    if(frame.exit){active.delete(frame.source);Object.freeze(frame.target);continue;}
    scheduled--;
    if(++counters.data>max)fail('PRESENTATION_LIMIT_EXCEEDED');
    if(code==='PRESENTATION_BODY_INVALID'&&frame.depth>limits.maxBodyDepth)fail('PRESENTATION_LIMIT_EXCEEDED');
    const value=frame.source;
    if(value===null||typeof value==='string'||typeof value==='boolean'||typeof value==='number'){
      if(typeof value==='number'&&!Number.isFinite(value))fail(code);
      if(typeof value==='string')displayText(value,limits.maxTextLength,code,true);
      Object.defineProperty(frame.parent,frame.key,{value,enumerable:true});continue;
    }
    if(typeof value!=='object')fail(code);
    if(active.has(value))fail('PRESENTATION_CYCLE_INVALID');
    const array=Array.isArray(value);
    let keys;
    const available=max-counters.data-scheduled;
    if(array){
      if(value.length>available)fail('PRESENTATION_LIMIT_EXCEEDED');
      denseArray(value,available,code);
      keys=Array.from({length:value.length},(_,i)=>String(i));
    }else{
      if(!isPlainRecord(value))fail(code);
      keys=Reflect.ownKeys(value);
      if(keys.length>available)fail('PRESENTATION_LIMIT_EXCEEDED');
      for(const key of keys){
        if(typeof key!=='string'||DANGEROUS_KEYS.has(key))fail(code);
        displayText(key,limits.maxTextLength,code,true);
        const d=Object.getOwnPropertyDescriptor(value,key);
        if(!d||!Object.hasOwn(d,'value'))fail(code);
      }
    }
    const target=array?new Array(keys.length):{};
    Object.defineProperty(frame.parent,frame.key,{value:target,enumerable:true});
    active.add(value);pending.push({exit:true,source:value,target});
    scheduled+=keys.length;
    for(let i=keys.length-1;i>=0;i--){
      const key=keys[i],d=Object.getOwnPropertyDescriptor(value,key);
      pending.push({source:d.value,parent:target,key,depth:frame.depth+1});
    }
  }
  return holder.value;
}

function validateBody(body,limits){
  if(!isPlainRecord(body))fail('PRESENTATION_BODY_INVALID');
  return cloneJson(body,{data:0},{maxTextLength:limits.maxTextLength,maxDataNodes:limits.maxBodyNodes,maxBodyDepth:limits.maxBodyDepth},'PRESENTATION_BODY_INVALID');
}
function fieldPropsFor(variant) {
  if (variant === 'integer') return [...FIELD_BASE_PROPS, 'minimum', 'maximum'];
  if (variant === 'string-list') return [...FIELD_BASE_PROPS, 'minItems', 'maxItems', 'itemRequired'];
  if (variant === 'record-list') return FIELD_RECORD_PROPS;
  return FIELD_BASE_PROPS;
}
function validateFieldNameRequired(p, limits) {
  strictLine(p.name, limits.maxTextLength, 'PRESENTATION_FIELD_INVALID');
  if (!FIELD_RE.test(p.name)) fail('PRESENTATION_FIELD_INVALID');
  if (typeof p.required !== 'boolean') fail('PRESENTATION_FIELD_INVALID');
}
function validateFieldColumnsShape(columns, limits) {
  denseArray(columns, limits.maxFields, 'PRESENTATION_COLUMNS_INVALID');
  if (columns.length === 0) fail('PRESENTATION_COLUMNS_INVALID');
  const names = new Set();
  for (const col of columns) {
    closedRecord(col, FIELD_COLUMN_PROPS, 'PRESENTATION_COLUMNS_INVALID');
    strictLine(col.name, limits.maxTextLength, 'PRESENTATION_COLUMNS_INVALID');
    if (!FIELD_RE.test(col.name) || DANGEROUS_KEYS.has(col.name)) fail('PRESENTATION_COLUMNS_INVALID');
    if (names.has(col.name)) fail('PRESENTATION_COLUMNS_INVALID');
    names.add(col.name);
    if (typeof col.required !== 'boolean') fail('PRESENTATION_COLUMNS_INVALID');
    strictLine(col.key, limits.maxTextLength, 'PRESENTATION_COLUMNS_INVALID');
    if (!isPlainRecord(col.params)) fail('PRESENTATION_COLUMNS_INVALID');
    const params = Reflect.ownKeys(col.params);
    if (params.length > limits.maxParams) fail('PRESENTATION_LIMIT_EXCEEDED');
    for (const name of params) {
      if (typeof name !== 'string' || !PROP_SEGMENT_RE.test(name) || DANGEROUS_KEYS.has(name)) fail('PRESENTATION_PARAMS_INVALID');
      const value = col.params[name];
      if (!(typeof value === 'string' || typeof value === 'boolean' || typeof value === 'number' && Number.isFinite(value))) fail('PRESENTATION_PARAMS_INVALID');
    }
  }
  return names;
}
function validateFieldMinMax(p) {
  if (typeof p.minItems !== 'number' || !Number.isSafeInteger(p.minItems) || p.minItems < 0) fail('PRESENTATION_FIELD_INVALID');
  if (!(p.maxItems === null || (typeof p.maxItems === 'number' && Number.isSafeInteger(p.maxItems) && p.maxItems >= p.minItems))) fail('PRESENTATION_FIELD_INVALID');
}
function validateFieldInitialShape(p, variant, limits, columnNames) {
  const maxText = limits.maxTextLength;
  if (variant === 'text') {
    displayText(p.initial, maxText, 'PRESENTATION_FIELD_INVALID', true);
    if (p.initial.includes('\n')) fail('PRESENTATION_FIELD_INVALID');
    return;
  }
  if (variant === 'boolean') {
    if (typeof p.initial !== 'boolean') fail('PRESENTATION_FIELD_INVALID');
    return;
  }
  if (variant === 'integer') {
    if (p.initial !== null && !Number.isSafeInteger(p.initial)) fail('PRESENTATION_FIELD_INVALID');
    return;
  }
  if (variant === 'string-list') {
    denseArray(p.initial, limits.maxDataNodes, 'PRESENTATION_FIELD_INVALID');
    for (const value of p.initial) {
      displayText(value, maxText, 'PRESENTATION_FIELD_INVALID', true);
    }
    return;
  }
  if (variant === 'record-list') {
    denseArray(p.initial, limits.maxDataNodes, 'PRESENTATION_RECORD_INVALID');
    for (const record of p.initial) {
      if (!isPlainRecord(record)) fail('PRESENTATION_RECORD_INVALID');
      const keys = Reflect.ownKeys(record);
      if (keys.length !== columnNames.size) fail('PRESENTATION_RECORD_INVALID');
      for (const key of keys) {
        if (typeof key !== 'string' || !columnNames.has(key)) fail('PRESENTATION_RECORD_INVALID');
        if (DANGEROUS_KEYS.has(key)) fail('PRESENTATION_RECORD_INVALID');
        const descriptor = Object.getOwnPropertyDescriptor(record, key);
        if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail('PRESENTATION_RECORD_INVALID');
        displayText(descriptor.value, maxText, 'PRESENTATION_RECORD_INVALID', true);
      }
      for (const name of columnNames) {
        if (!Object.hasOwn(record, name)) fail('PRESENTATION_RECORD_INVALID');
      }
    }
    return;
  }
  fail('PRESENTATION_VARIANT_INVALID');
}
function validateFieldTreeLabels(p, variant, ctx, limits) {
  validateLabel(p.key, p.params, ctx, limits.maxTextLength, limits.maxParams);
  if (variant === 'record-list') {
    for (const col of p.columns) {
      validateLabel(col.key, col.params, ctx, limits.maxTextLength, limits.maxParams);
    }
  }
}
function validateFieldMetadata(p, variant, limits) {
  validateFieldNameRequired(p, limits);
  strictLine(p.key, limits.maxTextLength, 'PRESENTATION_FIELD_INVALID');
  if (!isPlainRecord(p.params)) fail('PRESENTATION_FIELD_INVALID');
  const names = Reflect.ownKeys(p.params);
  if (names.length > limits.maxParams) fail('PRESENTATION_LIMIT_EXCEEDED');
  for (const name of names) {
    if (typeof name !== 'string' || !PROP_SEGMENT_RE.test(name) || DANGEROUS_KEYS.has(name)) fail('PRESENTATION_PARAMS_INVALID');
    const value = p.params[name];
    if (!(typeof value === 'string' || typeof value === 'boolean' || typeof value === 'number' && Number.isFinite(value))) fail('PRESENTATION_PARAMS_INVALID');
  }
  if (variant === 'integer') {
    if (!(p.minimum === null || Number.isSafeInteger(p.minimum))) fail('PRESENTATION_FIELD_INVALID');
    if (!(p.maximum === null || Number.isSafeInteger(p.maximum))) fail('PRESENTATION_FIELD_INVALID');
    if (p.minimum !== null && p.maximum !== null && p.minimum > p.maximum) fail('PRESENTATION_FIELD_INVALID');
  }
  if (variant === 'string-list' || variant === 'record-list') validateFieldMinMax(p);
  if (variant === 'string-list' && typeof p.itemRequired !== 'boolean') fail('PRESENTATION_FIELD_INVALID');
  return variant === 'record-list' ? validateFieldColumnsShape(p.columns, limits) : null;
}
function validateFieldSubmitConstraints(p, variant) {
  const value = p.initial;
  if (variant === 'text') {
    if (p.required && value.trim() === '') fail('PRESENTATION_FIELD_INVALID');
    return;
  }
  if (variant === 'boolean') return;
  if (variant === 'integer') {
    if (value === null) {
      if (p.required) fail('PRESENTATION_FIELD_INVALID');
      return;
    }
    if (p.minimum !== null && value < p.minimum) fail('PRESENTATION_FIELD_INVALID');
    if (p.maximum !== null && value > p.maximum) fail('PRESENTATION_FIELD_INVALID');
    return;
  }
  if (value.length < p.minItems || p.maxItems !== null && value.length > p.maxItems) fail('PRESENTATION_FIELD_INVALID');
  if (variant === 'string-list') {
    if (p.itemRequired && value.some(item => item === '')) fail('PRESENTATION_FIELD_INVALID');
    return;
  }
  for (const record of value) {
    for (const col of p.columns) {
      if (col.required && record[col.name] === '') fail('PRESENTATION_FIELD_INVALID');
    }
  }
}

function resolveBodyPath(body, path) {
  let current = body;
  for (let index = 0; index < path.length - 1; index += 1) {
    if (!isPlainRecord(current)) return { ok: false };
    if (!Object.hasOwn(current, path[index])) return { ok: false };
    current = current[path[index]];
  }
  if (!isPlainRecord(current)) return { ok: false };
  const last = path[path.length - 1];
  if (!Object.hasOwn(current, last)) return { ok: false };
  const slot = current[last];
  if (!(slot === null || typeof slot === 'string')) return { ok: false };
  return { ok: true };
}

function validateIntentBodyAndBindings(rawBody, rawBindings, ctx, counters) {
  const body = validateBody(rawBody, ctx.limits);
  denseArray(rawBindings, ctx.limits.maxBindings, 'PRESENTATION_BINDING_INVALID');
  const fields = new Set();
  const targets = new Set();
  const bindings = [];
  for (const binding of rawBindings) {
    closedRecord(binding, ['field', 'path'], 'PRESENTATION_BINDING_INVALID');
    strictLine(binding.field, ctx.limits.maxTextLength, 'PRESENTATION_BINDING_INVALID');
    if (!FIELD_RE.test(binding.field)) fail('PRESENTATION_BINDING_INVALID');
    if (fields.has(binding.field)) fail('PRESENTATION_BINDING_INVALID');
    fields.add(binding.field);
    denseArray(binding.path, ctx.limits.maxDataNodes, 'PRESENTATION_BINDING_INVALID');
    if (binding.path.length === 0) fail('PRESENTATION_BINDING_INVALID');
    for (const segment of binding.path) {
      if (typeof segment !== 'string' || !PROP_SEGMENT_RE.test(segment)) fail('PRESENTATION_BINDING_INVALID');
      if (DANGEROUS_KEYS.has(segment)) fail('PRESENTATION_BINDING_INVALID');
    }
    const key = JSON.stringify(binding.path);
    if (targets.has(key)) fail('PRESENTATION_BINDING_INVALID');
    targets.add(key);
    if (!resolveBodyPath(body, binding.path).ok) fail('PRESENTATION_BINDING_INVALID');
    bindings.push({ field: binding.field, path: [...binding.path] });
  }
  if (counters.bindings + bindings.length > ctx.limits.maxBindings) fail('PRESENTATION_LIMIT_EXCEEDED');
  counters.bindings += bindings.length;
  return { body, bindings, fields, targets };
}
function validateCommandIntent(intent, ctx, formScope, counters) {
  closedRecord(intent, COMMAND_INTENT_PROPS, 'PRESENTATION_INTENT_INVALID');
  strictLine(intent.command, ctx.limits.maxTextLength, 'PRESENTATION_COMMAND_INVALID');
  if (!COMMAND_RE.test(intent.command)) fail('PRESENTATION_COMMAND_INVALID');
  if (COMMAND_BLOCKED.has(intent.command)) fail('PRESENTATION_COMMAND_INVALID');
  const checked = validateIntentBodyAndBindings(intent.body, intent.bindings, ctx, counters);
  if (formScope) {
    formScope.intentBindings = { fields: checked.fields, targets: checked.targets, body: checked.body };
    formScope.intentKind = 'COMMAND';
  }
  return { kind: 'COMMAND', command: intent.command, body: checked.body, bindings: checked.bindings };
}
function validateQueryIntent(intent, ctx, formScope, counters) {
  closedRecord(intent, QUERY_INTENT_PROPS, 'PRESENTATION_INTENT_INVALID');
  strictLine(intent.query, ctx.limits.maxTextLength, 'PRESENTATION_COMMAND_INVALID');
  if (!COMMAND_RE.test(intent.query) || COMMAND_BLOCKED.has(intent.query)) fail('PRESENTATION_COMMAND_INVALID');
  const checked = validateIntentBodyAndBindings(intent.params, intent.bindings, ctx, counters);
  if (formScope) {
    formScope.intentBindings = { fields: checked.fields, targets: checked.targets, body: checked.body };
    formScope.intentKind = 'QUERY';
  }
  return { kind: 'QUERY', query: intent.query, params: checked.body, bindings: checked.bindings };
}
function validateActionIntent(intent, ctx, formScope, counters) {
  if (!isPlainRecord(intent)) fail('PRESENTATION_INTENT_INVALID');
  const keys = Reflect.ownKeys(intent);
  if (keys.includes('command')) {
    return validateCommandIntent(intent, ctx, formScope, counters);
  }
  if (keys.includes('query')) {
    return validateQueryIntent(intent, ctx, formScope, counters);
  }
  fail('PRESENTATION_INTENT_INVALID');
}
function validateIntent(intent, ctx, formScope, counters) {
  return validateActionIntent(intent, ctx, formScope, counters);
}


export function validatePresentationTree(tree,context){
  closedRecord(context,['owner','id','catalogs','routes','slots','components','limits'],'PRESENTATION_CONTEXT_INVALID');
  const limits=validateLimits(context.limits),data={data:0};
  const copiedContext=cloneJson(context,data,limits,'PRESENTATION_CONTEXT_INVALID');
  const ctx=validateContext(copiedContext);
  const result=cloneJson(tree,data,limits,'PRESENTATION_TREE_INVALID');
  const counters={nodes:0,fields:0,bindings:0},ids=new Set(),actions=new Map(),statuses=[],forms=[];
  const pending=[{node:result,depth:0,form:null,parent:null}];
  const registerId=(id,kind)=>{
    strictLine(id,limits.maxTextLength,'PRESENTATION_FORM_INVALID');
    if(!ACTION_ID_RE.test(id)||ids.has(id))fail('PRESENTATION_FORM_INVALID');
    ids.add(id);
    if(kind)actions.set(id,kind);
  };
  while(pending.length){
    const frame=pending.pop(),n=frame.node;
    closedRecord(n,['kind','variant','props','children'],'PRESENTATION_TREE_INVALID');
    if(!KINDS.includes(n.kind))fail('PRESENTATION_KIND_INVALID');
    if(!VARIANTS[n.kind].includes(n.variant))fail('PRESENTATION_VARIANT_INVALID');
    if(++counters.nodes>limits.maxNodes||frame.depth>limits.maxDepth)fail('PRESENTATION_LIMIT_EXCEEDED');
    if(n.kind==='field'){
      closedRecord(n.props,fieldPropsFor(n.variant),'PRESENTATION_PROPS_INVALID');
    }else if(n.kind==='form' && Object.hasOwn(n.props,'modelKey')){
      closedRecord(n.props,[...PROPS.form,'modelKey'],'PRESENTATION_PROPS_INVALID');
      strictLine(n.props.modelKey,limits.maxTextLength,'PRESENTATION_MODEL_INVALID');
    }else{
      closedRecord(n.props,PROPS[n.kind],'PRESENTATION_PROPS_INVALID');
    }
    denseArray(n.children,limits.maxChildren,'PRESENTATION_CHILDREN_INVALID');
    if(counters.nodes+pending.length+n.children.length>limits.maxNodes)fail('PRESENTATION_LIMIT_EXCEEDED');
    if(LEAF_KINDS.has(n.kind)&&n.children.length)fail('PRESENTATION_CHILDREN_INVALID');
    if(frame.parent==='form'&&!FORM_CHILDREN.has(n.kind))fail('PRESENTATION_PARENT_INVALID');
    if(frame.parent==='section'){
      const allowed=frame.form?FORM_CHILDREN:new Set([...SECTION_CHILDREN,'button','status']);
      if(!allowed.has(n.kind))fail('PRESENTATION_PARENT_INVALID');
    }
    const p=n.props;
    let form=frame.form;
    if(['heading','text','link','button','form'].includes(n.kind))validateLabel(p.key,p.params,ctx,limits.maxTextLength,limits.maxParams);
    if(n.kind==='link')validateRouteParams(p.route,p.routeParams,ctx,limits.maxTextLength);
    if(n.kind==='slot'){
      strictLine(p.point,limits.maxTextLength,'PRESENTATION_SLOT_INVALID');
      if(!ctx.slots.has(p.point))fail('PRESENTATION_SLOT_INVALID');
    }
    if(n.kind==='component'){
      strictLine(p.owner,limits.maxTextLength,'PRESENTATION_COMPONENT_INVALID');
      strictLine(p.id,limits.maxTextLength,'PRESENTATION_COMPONENT_INVALID');
      if(!ctx.components.has(JSON.stringify([p.owner,p.id])))fail('PRESENTATION_COMPONENT_INVALID');
    }
    if(n.kind==='form'){
      if(form)fail('PRESENTATION_PARENT_INVALID');
      const scope={id:p.id,fields:new Set(),intentBindings:null,intentKind:null};forms.push(scope);form=scope;
      const checked=validateActionIntent(p.intent,ctx,form,counters);
      registerId(p.id,checked.kind);
    }
    if(n.kind==='field'){
      if(!form)fail('PRESENTATION_PARENT_INVALID');
      const columnNames=validateFieldMetadata(p, n.variant, limits);
      if(form.fields.has(p.name))fail('PRESENTATION_FIELD_INVALID');
      validateFieldInitialShape(p, n.variant, limits, columnNames);
      validateFieldTreeLabels(p, n.variant, ctx, limits);
      if(++counters.fields>limits.maxFields)fail('PRESENTATION_LIMIT_EXCEEDED');
      form.fields.add(p.name);
    }
    if(n.kind==='button'){
      if(typeof p.submit!=='boolean')fail('PRESENTATION_BUTTON_INVALID');
      if(p.submit){
        if(!form||p.intent!==null)fail('PRESENTATION_BUTTON_INVALID');
        registerId(p.id,null);
      }else{
        const checked=validateActionIntent(p.intent,ctx,null,counters);
        if(checked.bindings.length)fail('PRESENTATION_BINDING_INVALID');
        registerId(p.id,checked.kind);
      }
    }
    if(n.kind==='status'){
      strictLine(p.for,limits.maxTextLength,'PRESENTATION_STATUS_INVALID');
      if(!ACTION_ID_RE.test(p.for))fail('PRESENTATION_STATUS_INVALID');
      if(n.variant!=='command'&&n.variant!=='query')fail('PRESENTATION_VARIANT_INVALID');
      statuses.push({for:p.for,variant:n.variant});
    }
    for(let i=n.children.length-1;i>=0;i--)pending.push({node:n.children[i],depth:frame.depth+1,form,parent:n.kind});
  }
  for(const form of forms){
    const bindings=form.intentBindings;
    if(!bindings||bindings.fields.size!==form.fields.size||[...form.fields].some(name=>!bindings.fields.has(name)))fail('PRESENTATION_BINDING_INVALID');
  }
  for(const item of statuses){
    const kind=actions.get(item.for);
    if(!kind)fail('PRESENTATION_STATUS_INVALID');
    if(item.variant==='command'&&kind!=='COMMAND')fail('PRESENTATION_STATUS_INVALID');
    if(item.variant==='query'&&kind!=='QUERY')fail('PRESENTATION_STATUS_INVALID');
  }
  return result;
}
export function validatePresentationFieldInput(fieldNode, value, limitsInput) {
  const limits = validateLimits(limitsInput);
  const snapshot = cloneJson({ node: fieldNode, value }, { data: 0 }, limits, 'PRESENTATION_FIELD_INVALID');
  const node = snapshot.node;
  closedRecord(node, ['kind', 'variant', 'props', 'children'], 'PRESENTATION_TREE_INVALID');
  if (node.kind !== 'field') fail('PRESENTATION_KIND_INVALID');
  if (!VARIANTS.field.includes(node.variant)) fail('PRESENTATION_VARIANT_INVALID');
  denseArray(node.children, limits.maxChildren, 'PRESENTATION_CHILDREN_INVALID');
  if (node.children.length !== 0) fail('PRESENTATION_CHILDREN_INVALID');
  closedRecord(node.props, fieldPropsFor(node.variant), 'PRESENTATION_PROPS_INVALID');
  const names = validateFieldMetadata(node.props, node.variant, limits);
  validateFieldInitialShape(node.props, node.variant, limits, names);
  const submitted = { ...node.props, initial: snapshot.value };
  validateFieldInitialShape(submitted, node.variant, limits, names);
  validateFieldSubmitConstraints(submitted, node.variant);
  return snapshot.value;
}
