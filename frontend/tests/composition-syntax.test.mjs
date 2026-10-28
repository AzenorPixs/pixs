import test from 'node:test';
import assert from 'node:assert/strict';
import { TextEncoder } from 'node:util';
import {
  analyzeModuleSource,
  parseEntrySource,
  SYNTAX_VERSION,
} from '../scripts/composition-syntax-v1.mjs';
import {
  validateCompositionDescriptor,
  createShellExtensionPoints,
} from '../src/shell/composition-descriptor-v1.js';

const LIMITS = Object.freeze({
  maxSourceBytes: 8192,
  maxAstNodes: 800,
  maxDescriptorCount: 4,
  maxTextLength: 256,
  maxLiteralItems: 16,
  maxLiteralDepth: 5,
});

const DESCRIPTOR = Object.freeze({
  descriptor_version: '1.0.0',
  owner: 'acme.app',
  owner_version: '1.0.0',
  type: 'ROUTE',
  id: 'acme.app.home',
  entry: 'frontend/routes/home',
  version: '1.0.0',
  requires: [],
  scope: 'TENANT_SCOPED',
  point: 'pixs.shell.routes',
  point_version: '1.0.0',
  display_permissions: [],
  trust: 'TRUSTED',
  mandatory: true,
  activation_scope: 'TENANT_SCOPED',
  payload: { path: '/home', mode: 'CSR', page: 'Home' },
});

const FACET = Object.freeze({
  owner: 'acme.app',
  owner_version: '1.0.0',
  type: 'ROUTE',
  id: 'acme.app.home',
  entry: 'frontend/routes/home',
  version: '1.0.0',
  requires: [],
  scope: 'TENANT_SCOPED',
});

function limits(over = {}) {
  return { ...LIMITS, ...over };
}

function rejectsCode(fn, code) {
  try {
    fn();
  } catch (error) {
    assert.equal(error.code, code);
    assert.equal(error.message, code);
    assert.equal(String(error), 'CompositionSyntaxError: ' + code);
    return error;
  }
  throw new Error('rejet attendu ' + code);
}

function entrySource(descriptorLiteral = JSON.stringify(DESCRIPTOR)) {
  return `import { useShellContext } from "pixs-shell/v1";\nexport const frontendContributions = [${descriptorLiteral}];\nexport function Home() { return null; }\n`;
}

test('syntaxe : nominal plein compatible descripteur reel', () => {
  const source = entrySource();
  const parsed = parseEntrySource(source, limits());
  assert.equal(parsed.descriptors.length, 1);
  assert.deepEqual(parsed.descriptors[0], DESCRIPTOR);
  assert.ok(parsed.exportedNames.some((e) => e.name === 'Home' && e.callable === true && e.from === 'local'));
  assert.ok(parsed.imports.some((i) => i.kind === 'staticImport' && i.source === 'pixs-shell/v1'));
  const registry = createShellExtensionPoints();
  const out = validateCompositionDescriptor(parsed.descriptors[0], {
    facet: FACET,
    extensionPoints: registry,
    limits: { maxTextLength: 256, maxRequires: 8, maxPermissions: 8, maxPoints: 32, maxLocales: 8, maxCatalogKeys: 32 },
  });
  assert.equal(out.id, 'acme.app.home');
  assert.ok(Object.isFrozen(parsed));
  assert.equal(SYNTAX_VERSION, '1.0.0');
});

test('syntaxe : helper interne sans descripteur accepte analyze refuse entry', () => {
  const source = `export function helper() { return 1; }\n`;
  const analyzed = analyzeModuleSource(source, limits());
  assert.equal(analyzed.descriptors, null);
  assert.ok(analyzed.exportedNames.some((e) => e.name === 'helper' && e.callable === true));
  rejectsCode(() => parseEntrySource(source, limits()), 'SYNTAX_EXPORT_INVALID');
});

test('syntaxe : exports fonction et const flechee callable', () => {
  const source = `export function Foo() {}\nexport const Bar = () => 1;\nexport const Data = 1;\nexport const frontendContributions = [];`;
  const analyzed = analyzeModuleSource(source, limits());
  const byName = Object.fromEntries(analyzed.exportedNames.map((e) => [e.name, e]));
  assert.equal(byName.Foo.callable, true);
  assert.equal(byName.Bar.callable, true);
  assert.equal(byName.Data.callable, false);
});

test('syntaxe : bindings import default namespace named et string-literal', () => {
  const source = `import d, { a as b, c } from "mod-a";\nimport * as ns from "mod-b";\nimport { "a-b" as c2 } from "mod-c";\nexport const frontendContributions = [];`;
  const analyzed = analyzeModuleSource(source, limits());
  const first = analyzed.imports.find((i) => i.source === 'mod-a');
  assert.deepEqual(first.bindings, [
    { imported: 'default', local: 'd', exported: null },
    { imported: 'a', local: 'b', exported: null },
    { imported: 'c', local: 'c', exported: null },
  ]);
  const second = analyzed.imports.find((i) => i.source === 'mod-b');
  assert.deepEqual(second.bindings, [{ imported: '*', local: 'ns', exported: null }]);
  const third = analyzed.imports.find((i) => i.source === 'mod-c');
  assert.deepEqual(third.bindings, [{ imported: 'a-b', local: 'c2', exported: null }]);
});

test('syntaxe : reexport private as Public preserve distinct', () => {
  const source = `export { privateName as PublicName } from "mod-x";\nexport const frontendContributions = [];`;
  const analyzed = analyzeModuleSource(source, limits());
  const reexport = analyzed.imports.find((i) => i.kind === 'ExportNamedFrom');
  assert.deepEqual(reexport.bindings, [{ imported: 'privateName', local: null, exported: 'PublicName' }]);
  rejectsCode(() => parseEntrySource(source, limits()), 'SYNTAX_EXPORT_INVALID');
});

test('syntaxe : alias local default class structures par analyze refuses par entry', () => {
  const base = entrySource();
  assert.ok(parseEntrySource(base, limits()));
  const aliasSource = base + `export { Home as HomeAlias };\n`;
  const analyzedAlias = analyzeModuleSource(aliasSource, limits());
  assert.ok(analyzedAlias.imports.some((i) => i.kind === 'ExportAlias'));
  rejectsCode(() => parseEntrySource(aliasSource, limits()), 'SYNTAX_EXPORT_INVALID');
  const defaultSource = `export default 1;\n` + base;
  const analyzedDefault = analyzeModuleSource(defaultSource, limits());
  assert.ok(analyzedDefault.exportedNames.some((e) => e.name === 'default' && e.from === 'default'));
  rejectsCode(() => parseEntrySource(defaultSource, limits()), 'SYNTAX_EXPORT_INVALID');
  const classSource = base + `export class Widget {}\n`;
  const analyzedClass = analyzeModuleSource(classSource, limits());
  assert.ok(analyzedClass.exportedNames.some((e) => e.name === 'Widget' && e.class === true));
  rejectsCode(() => parseEntrySource(classSource, limits()), 'SYNTAX_EXPORT_INVALID');
});

test('syntaxe : import dynamique dans fleche collecte non-litteral refuse', () => {
  const source = `export const later = () => import("https://example.invalid/x.js");\nexport const frontendContributions = [];`;
  const analyzed = analyzeModuleSource(source, limits());
  assert.ok(analyzed.imports.some((i) => i.kind === 'ImportExpression' && i.source === 'https://example.invalid/x.js'));
  const bad = `export const later = (x) => import(x);\nexport const frontendContributions = [];`;
  rejectsCode(() => analyzeModuleSource(bad, limits()), 'SYNTAX_IMPORT_INVALID');
});

test('syntaxe : require litteral collecte non-litteral eval Function refuses', () => {
  const good = `export const frontendContributions = [];\nconst x = require("node:fs");\n`;
  const analyzed = analyzeModuleSource(good, limits());
  assert.ok(analyzed.imports.some((i) => i.kind === 'requireCall' && i.source === 'node:fs'));
  const badRequire = `export const frontendContributions = [];\nconst x = require(y);\n`;
  rejectsCode(() => analyzeModuleSource(badRequire, limits()), 'SYNTAX_IMPORT_INVALID');
  for (const bad of [
    `export const frontendContributions = [];\neval("1");\n`,
    `export const frontendContributions = [];\nFunction("return 1");\n`,
    `export const frontendContributions = [];\nnew Function("return 1");\n`,
  ]) {
    rejectsCode(() => analyzeModuleSource(bad, limits()), 'SYNTAX_IMPORT_INVALID');
  }
});

test('syntaxe : commentaires strings regexp ressemblant import sans faux import sentinel non execute', () => {
  assert.equal(globalThis.__C11_SYNTAX_SENTINEL, undefined);
  const source = `// import x from "fake";\nconst s = "import y from 'fake2'";\nconst re = /import\\s+x/;\nglobalThis.__C11_SYNTAX_SENTINEL = true;\nexport const frontendContributions = [];\n`;
  const analyzed = analyzeModuleSource(source, limits());
  assert.equal(analyzed.imports.length, 0);
  assert.equal(globalThis.__C11_SYNTAX_SENTINEL, undefined);
});

test('syntaxe : limits obligatoires zero bool extra getters non appeles', () => {
  const source = entrySource();
  rejectsCode(() => analyzeModuleSource(source, null), 'SYNTAX_LIMITS_INVALID');
  for (const bad of [{ ...LIMITS, maxAstNodes: 0 }, { ...LIMITS, maxTextLength: true }, { ...LIMITS, extra: 1 }]) {
    rejectsCode(() => analyzeModuleSource(source, bad), 'SYNTAX_LIMITS_INVALID');
  }
  let calls = 0;
  const evil = {};
  Object.defineProperty(evil, 'maxAstNodes', { get() { calls += 1; return 800; }, enumerable: true });
  for (const key of ['maxSourceBytes', 'maxDescriptorCount', 'maxTextLength', 'maxLiteralItems', 'maxLiteralDepth']) evil[key] = LIMITS[key];
  rejectsCode(() => analyzeModuleSource(source, evil), 'SYNTAX_LIMITS_INVALID');
  assert.equal(calls, 0);
});

test('syntaxe : maxSourceBytes UTF8 exact depassement multioctets', () => {
  const text = 'é'.repeat(10);
  const bytes = new TextEncoder().encode(`export const frontendContributions = []; // ${text}`).length;
  const okLimits = limits({ maxSourceBytes: bytes });
  assert.ok(analyzeModuleSource(`export const frontendContributions = []; // ${text}`, okLimits));
  rejectsCode(() => analyzeModuleSource(`export const frontendContributions = []; // ${text}`, limits({ maxSourceBytes: bytes - 1 })), 'SYNTAX_TOO_LARGE');
});

test('syntaxe : source longue metadata courte distingue maxTextLength', () => {
  const longComment = `// ${'x'.repeat(500)}\n`;
  const source = longComment + `export const frontendContributions = [];`;
  assert.ok(analyzeModuleSource(source, limits({ maxSourceBytes: 4096, maxTextLength: 32 })));
  const badMeta = `import { ${'y'.repeat(64)} } from "m";\nexport const frontendContributions = [];`;
  rejectsCode(() => analyzeModuleSource(badMeta, limits({ maxSourceBytes: 4096, maxTextLength: 10 })), 'SYNTAX_IMPORT_INVALID');
});

test('syntaxe : volume AST et profondeur reelle typee sans RangeError simule', () => {
  let big = '';
  for (let index = 0; index < 60; index += 1) big += `export const v${index} = ${index};\n`;
  big += `export const frontendContributions = [];\n`;
  rejectsCode(() => analyzeModuleSource(big, limits({ maxAstNodes: 10 })), 'SYNTAX_AST_TOO_LARGE');
  let deep = 'export const frontendContributions = [{a:';
  for (let index = 0; index < 10; index += 1) deep += '{a:';
  deep += '1';
  for (let index = 0; index < 10; index += 1) deep += '}';
  deep += '}];';
  rejectsCode(() => analyzeModuleSource(deep, limits({ maxLiteralDepth: 3 })), 'SYNTAX_DEPTH_EXCEEDED');
});

test('syntaxe : maxDescriptorCount maxLiteralItems racine descripteur', () => {
  const two = `export const frontendContributions = [{},{}];`;
  rejectsCode(() => parseEntrySource(two, limits({ maxDescriptorCount: 1 })), 'SYNTAX_DESCRIPTORS_EXCEEDED');
  const many = `export const frontendContributions = [{${Array.from({ length: 20 }, (_, i) => `k${i}:1`).join(',')}}];`;
  rejectsCode(() => parseEntrySource(many, limits({ maxLiteralItems: 5 })), 'SYNTAX_ITEMS_EXCEEDED');
  assert.ok(parseEntrySource('export const frontendContributions = [];', limits()));
  for (const bad of [
    'export const frontendContributions = [null];',
    'export const frontendContributions = ["x"];',
    'export const frontendContributions = [[]];',
    'export const frontendContributions = null;',
    'export const frontendContributions = "x";',
  ]) {
    rejectsCode(() => parseEntrySource(bad, limits()), 'SYNTAX_EXPORT_INVALID');
  }
});

test('syntaxe : donnees gelees sans alias', () => {
  const parsed = parseEntrySource(entrySource(), limits());
  assert.ok(Object.isFrozen(parsed));
  assert.ok(Object.isFrozen(parsed.descriptors));
  assert.ok(Object.isFrozen(parsed.exportedNames));
  assert.ok(Object.isFrozen(parsed.imports));
  assert.throws(() => { parsed.descriptors[0].payload.path = '/modifie'; }, TypeError);
  assert.ok(Object.isFrozen(parsed.descriptors[0].payload));
  const again = parseEntrySource(entrySource(), limits());
  assert.equal(again.descriptors[0].payload.path, '/home');
});

test('syntaxe : LF catalogue et surrogate valide conservés, invalides refusés', () => {
  const translated = { ...DESCRIPTOR, type: 'TRANSLATION', id: 'acme.app.i18n',
    point: 'pixs.shell.translations', payload: {
      catalog: { en: { 'acme.app.title': 'Line\nTwo' }, fr: { 'acme.app.title': 'Ligne\nDeux' } },
    } };
  const parsed = parseEntrySource(entrySource(JSON.stringify(translated)), limits());
  assert.equal(parsed.descriptors[0].payload.catalog.en['acme.app.title'], 'Line\nTwo');
  validateCompositionDescriptor(parsed.descriptors[0], {
    facet: { ...FACET, type: 'TRANSLATION', id: 'acme.app.i18n' },
    extensionPoints: createShellExtensionPoints(),
    limits: { maxTextLength: 256, maxRequires: 8, maxPermissions: 8, maxPoints: 32, maxLocales: 8, maxCatalogKeys: 32 },
  });
  const emoji = '𝌆';
  assert.equal(parseEntrySource('export const frontendContributions = [{t:"' + emoji + '"}];', limits()).descriptors[0].t, emoji);
  rejectsCode(() => analyzeModuleSource('export const frontendContributions = [{t:"\uD800"}];', limits()), 'SYNTAX_TEXT_INVALID');
  rejectsCode(() => analyzeModuleSource('export const frontendContributions = [{t:"\\uD800"}];', limits()), 'SYNTAX_TEXT_INVALID');
});

test('syntaxe : spread method getter shorthand computed numeric doublon proto call identifier hole refuses', () => {
  const base = (inner) => `export const frontendContributions = [${inner}];`;
  for (const bad of [
    base('{...{a:1}}'),
    base('{m(){}}'),
    base('{get a(){return 1}}'),
    base('{a}'),
    base('{["a"+1]:1}'),
    base('{1:1}'),
    base('{a:1,a:2}'),
    base('{__proto__:1}'),
    base('{a:call()}'),
    base('{a:someIdent}'),
    base('{a:[,]}'),
  ]) {
    rejectsCode(() => parseEntrySource(bad, limits()), 'SYNTAX_EXPORT_INVALID');
  }
  assert.ok(parseEntrySource(base('{a:1,b:"x",c:true,d:null,e:1}'), limits()));
});

test('syntaxe : regexp bigint infini comme valeur refuses', () => {
  rejectsCode(() => parseEntrySource(`export const frontendContributions = [{a:/ab+c/}];`, limits()), 'SYNTAX_EXPORT_INVALID');
  rejectsCode(() => parseEntrySource(`export const frontendContributions = [{a:10n}];`, limits()), 'SYNTAX_EXPORT_INVALID');
  rejectsCode(() => parseEntrySource(`export const frontendContributions = [{a:Infinity}];`, limits()), 'SYNTAX_EXPORT_INVALID');
  rejectsCode(() => parseEntrySource(`export const frontendContributions = [{a:1e999}];`, limits()), 'SYNTAX_EXPORT_INVALID');
});

test('syntaxe : malforme code stable sans echo cause conservee', () => {
  const bad = `export const = ["C11_PRIVATE_SENTINEL";`;
  let caught;
  try {
    parseEntrySource(bad, limits());
  } catch (error) {
    caught = error;
  }
  assert.ok(caught);
  assert.equal(caught.code, 'SYNTAX_INVALID');
  assert.equal(caught.message, 'SYNTAX_INVALID');
  assert.equal(String(caught), 'CompositionSyntaxError: SYNTAX_INVALID');
  assert.ok(caught.cause);
  assert.ok(!String(caught).includes('C11_PRIVATE_SENTINEL'));
  assert.ok(!String(caught).includes('export const'));
});

test('syntaxe : restrictions entry distinctes JS interne sans sandbox generale', () => {
  const internal = `export function helper() { return import("x"); }\n`;
  const analyzed = analyzeModuleSource(internal, limits());
  assert.ok(analyzed.imports.some((i) => i.kind === 'ImportExpression'));
  rejectsCode(() => parseEntrySource(internal, limits()), 'SYNTAX_EXPORT_INVALID');
});
