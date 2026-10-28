import { parseAst } from 'vite';

export const SYNTAX_VERSION = '1.0.0';
const DESCRIPTOR_EXPORT = 'frontendContributions';
const DANGEROUS_KEYS = new Set(['__proto__', 'constructor', 'prototype']);
const REFUSED_IDENT_CALLS = new Set(['eval', 'Function', 'require']);

export const SYNTAX_CODES = Object.freeze([
  'SYNTAX_LIMITS_INVALID',
  'SYNTAX_TOO_LARGE',
  'SYNTAX_TEXT_INVALID',
  'SYNTAX_INVALID',
  'SYNTAX_AST_TOO_LARGE',
  'SYNTAX_DEPTH_EXCEEDED',
  'SYNTAX_ITEMS_EXCEEDED',
  'SYNTAX_DESCRIPTORS_EXCEEDED',
  'SYNTAX_EXPORT_INVALID',
  'SYNTAX_IMPORT_INVALID',
]);

export class CompositionSyntaxError extends Error {
  constructor(code, options) {
    super(code, options);
    this.name = 'CompositionSyntaxError';
    this.code = code;
  }
}

function fail(code, cause) {
  if (cause === undefined) throw new CompositionSyntaxError(code);
  throw new CompositionSyntaxError(code, { cause });
}

function safeInt(value, code = 'SYNTAX_LIMITS_INVALID') {
  if (typeof value !== 'number' || !Number.isSafeInteger(value) || value <= 0) fail(code);
  return value;
}

function validateLimits(limits) {
  if (limits === null || typeof limits !== 'object' || Array.isArray(limits)) fail('SYNTAX_LIMITS_INVALID');
  const proto = Object.getPrototypeOf(limits);
  if (proto !== Object.prototype && proto !== null) fail('SYNTAX_LIMITS_INVALID');
  const keys = Reflect.ownKeys(limits);
  const required = ['maxSourceBytes', 'maxAstNodes', 'maxDescriptorCount', 'maxTextLength', 'maxLiteralItems', 'maxLiteralDepth'];
  for (const name of required) {
    if (!Object.hasOwn(limits, name)) fail('SYNTAX_LIMITS_INVALID');
  }
  for (const key of keys) {
    if (typeof key !== 'string' || !required.includes(key)) fail('SYNTAX_LIMITS_INVALID');
    const descriptor = Object.getOwnPropertyDescriptor(limits, key);
    if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail('SYNTAX_LIMITS_INVALID');
  }
  for (const name of required) safeInt(limits[name]);
  return limits;
}

function wellFormedSource(text, limits) {
  if (typeof text !== 'string' || text.length === 0) fail('SYNTAX_TEXT_INVALID');
  if (text.length > limits.maxSourceBytes) fail('SYNTAX_TOO_LARGE');
  for (let index = 0; index < text.length; index += 1) {
    const unit = text.charCodeAt(index);
    if (unit >= 0xD800 && unit <= 0xDBFF) {
      const next = text.charCodeAt(index + 1);
      if (!(next >= 0xDC00 && next <= 0xDFFF)) fail('SYNTAX_TEXT_INVALID');
      index += 1;
    } else if (unit >= 0xDC00 && unit <= 0xDFFF) {
      fail('SYNTAX_TEXT_INVALID');
    }
  }
  const bytes = new TextEncoder().encode(text).length;
  if (bytes === 0 || bytes > limits.maxSourceBytes) fail('SYNTAX_TOO_LARGE');
  return text;
}

function boundedMetaText(value, limits, code) {
  if (typeof value !== 'string' || value.length === 0 || value.length > limits.maxTextLength) fail(code);
  for (let index = 0; index < value.length; index += 1) {
    const unit = value.charCodeAt(index);
    if (unit >= 0xD800 && unit <= 0xDBFF) {
      const next = value.charCodeAt(index + 1);
      if (!(next >= 0xDC00 && next <= 0xDFFF)) fail('SYNTAX_TEXT_INVALID');
      index += 1;
    } else if (unit >= 0xDC00 && unit <= 0xDFFF) {
      fail('SYNTAX_TEXT_INVALID');
    }
    if (unit < 32 || unit === 127) fail(code);
  }
  return value;
}

function specName(node, limits) {
  if (!node || typeof node.type !== 'string') fail('SYNTAX_IMPORT_INVALID');
  if (node.type === 'Identifier') {
    if (typeof node.name !== 'string' || node.name.length === 0) fail('SYNTAX_IMPORT_INVALID');
    return boundedMetaText(node.name, limits, 'SYNTAX_IMPORT_INVALID');
  }
  if (node.type === 'Literal') {
    if (typeof node.value !== 'string' || node.value.length === 0) fail('SYNTAX_IMPORT_INVALID');
    return boundedMetaText(node.value, limits, 'SYNTAX_IMPORT_INVALID');
  }
  fail('SYNTAX_IMPORT_INVALID');
}

function literalNode(root, limits, initialDepth) {
  const holder = {};
  const stack = [{ node: root, depth: initialDepth, parent: holder, key: 'value' }];
  while (stack.length > 0) {
    const frame = stack.pop();
    if (frame.finish) {
      Object.freeze(frame.finish);
      continue;
    }
    if (frame.depth > limits.maxLiteralDepth) fail('SYNTAX_DEPTH_EXCEEDED');
    const node = frame.node;
    let value;
    if (node.type === 'Literal') {
      value = node.value;
      if (typeof value === 'string') {
        if (value.length > limits.maxTextLength) fail('SYNTAX_TOO_LARGE');
        for (let index = 0; index < value.length; index += 1) {
          const unit = value.charCodeAt(index);
          if (unit >= 0xD800 && unit <= 0xDBFF) {
            const next = value.charCodeAt(index + 1);
            if (!(next >= 0xDC00 && next <= 0xDFFF)) fail('SYNTAX_TEXT_INVALID');
            index += 1;
          } else if (unit >= 0xDC00 && unit <= 0xDFFF) fail('SYNTAX_TEXT_INVALID');
        }
      } else if (value !== null && typeof value !== 'boolean'
          && !(typeof value === 'number' && Number.isFinite(value))) {
        fail('SYNTAX_EXPORT_INVALID');
      }
    } else if (node.type === 'ObjectExpression') {
      if (node.properties.length > limits.maxLiteralItems) fail('SYNTAX_ITEMS_EXCEEDED');
      value = {};
      const children = [];
      const seen = new Set();
      for (const property of node.properties) {
        if (property.type !== 'Property' || property.computed || property.method
            || property.shorthand || property.kind !== 'init') fail('SYNTAX_EXPORT_INVALID');
        const key = property.key;
        let name;
        if (key.type === 'Identifier') name = key.name;
        else if (key.type === 'Literal' && typeof key.value === 'string') name = key.value;
        else fail('SYNTAX_EXPORT_INVALID');
        boundedMetaText(name, limits, 'SYNTAX_EXPORT_INVALID');
        if (DANGEROUS_KEYS.has(name) || seen.has(name)) fail('SYNTAX_EXPORT_INVALID');
        seen.add(name);
        children.push({ node: property.value, depth: frame.depth + 1, parent: value, key: name });
      }
      stack.push({ finish: value });
      for (let index = children.length - 1; index >= 0; index -= 1) stack.push(children[index]);
    } else if (node.type === 'ArrayExpression') {
      if (node.elements.length > limits.maxLiteralItems) fail('SYNTAX_ITEMS_EXCEEDED');
      value = new Array(node.elements.length);
      stack.push({ finish: value });
      for (let index = node.elements.length - 1; index >= 0; index -= 1) {
        const element = node.elements[index];
        if (element === null || element.type === 'SpreadElement') fail('SYNTAX_EXPORT_INVALID');
        stack.push({ node: element, depth: frame.depth + 1, parent: value, key: String(index) });
      }
    } else {
      fail('SYNTAX_EXPORT_INVALID');
    }
    Object.defineProperty(frame.parent, frame.key, { value, enumerable: true });
  }
  return holder.value;
}

function countNodesIterative(root, limits) {
  let count = 0;
  const stack = [root];
  while (stack.length > 0) {
    const node = stack.pop();
    if (!node || typeof node.type !== 'string') continue;
    count += 1;
    if (count > limits.maxAstNodes) fail('SYNTAX_AST_TOO_LARGE');
    for (const key of Object.keys(node)) {
      if (key === 'type' || key === 'start' || key === 'end' || key === 'loc' || key === 'range') continue;
      const child = node[key];
      if (Array.isArray(child)) {
        for (let index = child.length - 1; index >= 0; index -= 1) {
          const item = child[index];
          if (item && typeof item.type === 'string') {
            if (stack.length + count >= limits.maxAstNodes) fail('SYNTAX_AST_TOO_LARGE');
            stack.push(item);
          }
        }
      } else if (child && typeof child.type === 'string') {
        if (stack.length + count >= limits.maxAstNodes) fail('SYNTAX_AST_TOO_LARGE');
        stack.push(child);
      }
    }
  }
  return count;
}

export function analyzeModuleSource(text, limits) {
  const bounds = validateLimits(limits);
  wellFormedSource(text, bounds);
  let root;
  try {
    root = parseAst(text);
  } catch (error) {
    if (error instanceof CompositionSyntaxError) throw error;
    fail('SYNTAX_INVALID', error);
  }
  if (!root || root.type !== 'Program' || !Array.isArray(root.body)) fail('SYNTAX_INVALID');
  countNodesIterative(root, bounds);
  const imports = [];
  const exportedNames = [];
  let descriptors = null;
  let descriptorSeen = 0;
  const pushImport = (entry) => {
    imports.push(Object.freeze({
      kind: entry.kind,
      source: entry.source,
      bindings: Object.freeze(entry.bindings.map((b) => Object.freeze({ ...b }))),
    }));
  };
  const pushExportName = (name, callable, from, extra = {}) => {
    boundedMetaText(name, bounds, 'SYNTAX_EXPORT_INVALID');
    exportedNames.push(Object.freeze({ name, callable, from, ...extra }));
  };
  for (const node of root.body) {
    if (node.attributes?.length || node.assertions?.length) fail('SYNTAX_IMPORT_INVALID');
    if (node.type === 'ImportDeclaration') {
      if (typeof node.source.value !== 'string') fail('SYNTAX_IMPORT_INVALID');
      boundedMetaText(node.source.value, bounds, 'SYNTAX_IMPORT_INVALID');
      pushImport({
        kind: 'staticImport',
        source: node.source.value,
        bindings: node.specifiers.map((s) => {
          if (s.type === 'ImportSpecifier') return { imported: specName(s.imported, bounds), local: specName(s.local, bounds), exported: null };
          if (s.type === 'ImportDefaultSpecifier') return { imported: 'default', local: specName(s.local, bounds), exported: null };
          if (s.type === 'ImportNamespaceSpecifier') return { imported: '*', local: specName(s.local, bounds), exported: null };
          fail('SYNTAX_IMPORT_INVALID');
        }),
      });
    } else if (node.type === 'ExportAllDeclaration') {
      if (!node.source || typeof node.source.value !== 'string') fail('SYNTAX_IMPORT_INVALID');
      boundedMetaText(node.source.value, bounds, 'SYNTAX_IMPORT_INVALID');
      const bindings = [];
      if (node.exported) bindings.push({ imported: '*', local: null, exported: specName(node.exported, bounds) });
      pushImport({ kind: 'ExportAllFrom', source: node.source.value, bindings });
    } else if (node.type === 'ExportNamedDeclaration') {
      if (node.source) {
        if (typeof node.source.value !== 'string') fail('SYNTAX_IMPORT_INVALID');
        boundedMetaText(node.source.value, bounds, 'SYNTAX_IMPORT_INVALID');
        pushImport({
          kind: 'ExportNamedFrom',
          source: node.source.value,
          bindings: node.specifiers.map((s) => ({ imported: specName(s.local, bounds), local: null, exported: specName(s.exported, bounds) })),
        });
      } else if (node.declaration) {
        const declaration = node.declaration;
        if (declaration.type === 'FunctionDeclaration') {
          if (!declaration.id || declaration.id.type !== 'Identifier') fail('SYNTAX_EXPORT_INVALID');
          pushExportName(declaration.id.name, true, 'local');
        } else if (declaration.type === 'VariableDeclaration') {
          if (declaration.kind !== 'const') fail('SYNTAX_EXPORT_INVALID');
          for (const declarator of declaration.declarations) {
            if (declarator.id.type !== 'Identifier') fail('SYNTAX_EXPORT_INVALID');
            const name = declarator.id.name;
            if (name === DESCRIPTOR_EXPORT) {
              descriptorSeen += 1;
              if (descriptorSeen > 1) fail('SYNTAX_EXPORT_INVALID');
              if (!declarator.init || declarator.init.type !== 'ArrayExpression') fail('SYNTAX_EXPORT_INVALID');
              if (declarator.init.elements.length > bounds.maxDescriptorCount) fail('SYNTAX_DESCRIPTORS_EXCEEDED');
              const items = [];
              for (const element of declarator.init.elements) {
                if (!element || element.type === 'SpreadElement') fail('SYNTAX_EXPORT_INVALID');
                if (element.type !== 'ObjectExpression') fail('SYNTAX_EXPORT_INVALID');
                items.push(literalNode(element, bounds, 1));
              }
              descriptors = items;
              pushExportName(name, false, 'local');
            } else {
              const init = declarator.init;
              const callable = !!init && (init.type === 'ArrowFunctionExpression' || init.type === 'FunctionExpression');
              pushExportName(name, callable, 'local');
            }
          }
        } else if (declaration.type === 'ClassDeclaration') {
          const name = declaration.id ? specName(declaration.id, bounds) : 'default-class';
          pushExportName(name, false, 'local', { class: true });
        } else {
          fail('SYNTAX_EXPORT_INVALID');
        }
      } else if (node.specifiers.length > 0) {
        pushImport({
          kind: 'ExportAlias',
          source: null,
          bindings: node.specifiers.map((s) => ({ imported: null, local: specName(s.local, bounds), exported: specName(s.exported, bounds) })),
        });
        for (const s of node.specifiers) pushExportName(specName(s.exported, bounds), false, 'alias');
      }
    } else if (node.type === 'ExportDefaultDeclaration') {
      pushExportName('default', false, 'default');
    } else if (node.type === 'VariableDeclaration' || node.type === 'FunctionDeclaration' || node.type === 'ClassDeclaration') {
      continue;
    } else if (node.type === 'ExpressionStatement' || node.type === 'EmptyStatement') {
      continue;
    } else {
      fail('SYNTAX_EXPORT_INVALID');
    }
  }
  const stack = [...root.body];
  while (stack.length > 0) {
    const node = stack.pop();
    if (!node || typeof node.type !== 'string') continue;
    if (node.type === 'ImportExpression') {
      const argument = node.source;
      if (!argument || argument.type !== 'Literal' || typeof argument.value !== 'string') fail('SYNTAX_IMPORT_INVALID');
      boundedMetaText(argument.value, bounds, 'SYNTAX_IMPORT_INVALID');
      pushImport({ kind: 'ImportExpression', source: argument.value, bindings: [] });
    }
    if (node.type === 'CallExpression') {
      const callee = node.callee;
      if (callee.type === 'Identifier' && REFUSED_IDENT_CALLS.has(callee.name)) {
        if (callee.name === 'require') {
          const first = node.arguments[0];
          if (!first || first.type !== 'Literal' || typeof first.value !== 'string') fail('SYNTAX_IMPORT_INVALID');
          boundedMetaText(first.value, bounds, 'SYNTAX_IMPORT_INVALID');
          pushImport({ kind: 'requireCall', source: first.value, bindings: [] });
        } else {
          fail('SYNTAX_IMPORT_INVALID');
        }
      }
      if (callee.type === 'Import') fail('SYNTAX_IMPORT_INVALID');
    }
    if (node.type === 'NewExpression') {
      const callee = node.callee;
      if (callee.type === 'Identifier' && callee.name === 'Function') fail('SYNTAX_IMPORT_INVALID');
    }
    for (const key of Object.keys(node)) {
      if (key === 'type' || key === 'start' || key === 'end' || key === 'loc' || key === 'range') continue;
      const child = node[key];
      if (Array.isArray(child)) {
        for (let index = child.length - 1; index >= 0; index -= 1) {
          const item = child[index];
          if (item && typeof item.type === 'string') stack.push(item);
        }
      } else if (child && typeof child.type === 'string') {
        stack.push(child);
      }
    }
  }
  return Object.freeze({
    descriptors: descriptors === null ? null : Object.freeze(descriptors),
    exportedNames: Object.freeze([...exportedNames]),
    imports: Object.freeze([...imports]),
  });
}

export function parseEntrySource(text, limits) {
  const result = analyzeModuleSource(text, limits);
  if (result.descriptors === null) fail('SYNTAX_EXPORT_INVALID');
  for (const entry of result.exportedNames) {
    if (entry.from !== 'local') fail('SYNTAX_EXPORT_INVALID');
    if (entry.name === 'default' || entry.class) fail('SYNTAX_EXPORT_INVALID');
  }
  for (const entry of result.imports) {
    if (entry.kind === 'ExportAlias' || entry.kind === 'ExportAllFrom' || entry.kind === 'ExportNamedFrom') {
      fail('SYNTAX_EXPORT_INVALID');
    }
  }
  return result;
}
