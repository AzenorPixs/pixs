// Plugin Vite de composition : virtuel stable, sans decouverte ni activation au build.
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { types as utilTypes } from 'node:util';
import { isPreparedFrontendComposition } from './prepare_frontend_composition.mjs';

const VIRTUAL_ID = 'virtual:pixs-composition/v1';
const RESOLVED_VIRTUAL_ID = '\0virtual:pixs-composition/v1';
const CAPTURED_PREFIX = 'virtual:pixs-captured/';
const RESOLVED_CAPTURED_PREFIX = '\0virtual:pixs-captured/';
const SHELL_ALIAS = 'pixs-shell/v1';
const RENDER_TYPES = new Set(['ROUTE', 'PAGE', 'FORM', 'COMPONENT', 'UI_SLOT']);
const FREEZE_SOURCE = "const __freeze = value => { const pending = [value]; while (pending.length) { const item = pending.pop(); if (item === null || typeof item !== 'object' || Object.isFrozen(item)) continue; for (const child of Object.values(item)) pending.push(child); Object.freeze(item); } return value; };";

export class CompositionPluginError extends Error {
  constructor(code, options) {
    super(code, options);
    this.name = 'CompositionPluginError';
    this.code = code;
    this.stack = this.name + ': ' + code;
  }
}
function fail(code, cause) {
  throw new CompositionPluginError(code, cause === undefined ? undefined : { cause });
}
function exportNameOf(contribution) {
  if (contribution.type === 'ROUTE') return contribution.payload?.page ?? null;
  if (['PAGE', 'FORM', 'COMPONENT', 'UI_SLOT'].includes(contribution.type)) return contribution.payload?.export ?? null;
  return null;
}
function safeHash(text, expected) {
  const digest = createHash('sha256').update(Buffer.from(text, 'utf-8')).digest('hex');
  if (digest !== expected) fail('COMPOSITION_HASH_DRIFT');
}

export function createPixsCompositionPlugin(options) {
  if (options === null || typeof options !== 'object' || Array.isArray(options) || utilTypes.isProxy(options)) fail('PLUGIN_OPTIONS_INVALID');
  if (![Object.prototype, null].includes(Object.getPrototypeOf(options)) || Reflect.ownKeys(options).length !== 2) fail('PLUGIN_OPTIONS_INVALID');
  const values = {};
  for (const name of ['mode', 'composition']) {
    const descriptor = Object.getOwnPropertyDescriptor(options, name);
    if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail('PLUGIN_OPTIONS_INVALID');
    Object.defineProperty(values, name, { value: descriptor.value, enumerable: true });
  }
  const { mode, composition } = values;
  if (mode !== 'STANDALONE' && mode !== 'COMPOSED') fail('PLUGIN_MODE_INVALID');
  if (mode === 'STANDALONE') {
    if (composition !== null) fail('PLUGIN_OPTIONS_INVALID');
  } else {
    if (!isPreparedFrontendComposition(composition)) fail('PLUGIN_COMPOSITION_INVALID');
    if (composition.graph?.blocked === true) fail('GRAPH_BLOCKED');
  }
  const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
  let command = 'serve';
  let drifted = false;
  let cleanupServer = () => {};
  let stopped = false;
  let watchedFiles = [];
  const fileToModule = new Map();
  if (mode === 'COMPOSED') {
    composition.imports.modules.forEach((module, index) => {
      safeHash(module.text, module.hash);
      const virtual = `${CAPTURED_PREFIX}${index}.js`;
      fileToModule.set(module.file, { module, index, virtual, resolved: `${RESOLVED_CAPTURED_PREFIX}${index}.js` });
    });
  }
  function verifiedOrFail() {
    try {
      composition.verifyBeforePublish();
    } catch (cause) {
      drifted = true;
      fail('COMPOSITION_DRIFT', cause);
    }
  }
  function watchedAbsoluteFiles() {
    const files = [];
    for (const owner of composition.envelope.capture.owners) {
      files.push(path.join(root, owner.manifest.path));
      for (const source of owner.sources) files.push(path.join(root, source.path));
    }
    return files;
  }
  function buildVirtualSource() {
    if (mode === 'STANDALONE') {
      return [
        FREEZE_SOURCE,
        `export const mode = ${JSON.stringify('STANDALONE')};`,
        `export const graph = __freeze(${JSON.stringify({ schema: 'pixs.frontend.contribution-graph/1.0.0', order: [], contributionEdges: [], contributions: [], diagnostics: [], blocked: false })});`,
        `export const report = __freeze(${JSON.stringify({ schema: 'pixs.frontend.composition-report/1.0.0', order: [], edges: [], blocked: false })});`,
        `export const points = __freeze(${JSON.stringify({})});`,
        `export const locales = __freeze(${JSON.stringify([])});`,
        `export const admission = __freeze(${JSON.stringify([])});`,
        `export const presentationLimits = __freeze(${JSON.stringify(null)});`,
        `export const factories = Object.freeze(${JSON.stringify({})});`,
        '',
      ].join('\n');
    }
    const active = composition.graph.contributions.filter((contribution) => RENDER_TYPES.has(contribution.type));
    const facetEntry = new Map();
    for (const facet of composition.preflight.facets) facetEntry.set(JSON.stringify([facet.owner, facet.id]), facet.entry);
    const ownerRoot = new Map();
    for (const owner of composition.envelope.capture.owners) ownerRoot.set(owner.owner, owner.root);
    const needed = new Map();
    const links = [];
    active.forEach((contribution, position) => {
      const name = exportNameOf(contribution);
      if (typeof name !== 'string' || !name) fail('PLUGIN_EXPORT_UNKNOWN');
      const entry = facetEntry.get(JSON.stringify([contribution.owner, contribution.id]));
      if (typeof entry !== 'string') fail('PLUGIN_EXPORT_UNKNOWN');
      const file = `${ownerRoot.get(contribution.owner)}/${entry}`;
      const record = fileToModule.get(file);
      if (!record) fail('PLUGIN_EXPORT_UNKNOWN');
      if (!needed.has(record.index)) needed.set(record.index, record);
      links.push({ key: JSON.stringify([contribution.owner, contribution.id]), index: record.index, name });
    });
    const lines = [FREEZE_SOURCE];
    for (const record of [...needed.values()].sort((a, b) => a.index - b.index)) {
      lines.push(`import * as __mod${record.index} from ${JSON.stringify(record.virtual)};`);
    }
    lines.push(`export const mode = ${JSON.stringify('COMPOSED')};`);
    lines.push(`export const graph = __freeze(${JSON.stringify(composition.graph)});`);
    lines.push(`export const report = __freeze(${JSON.stringify(composition.report)});`);
    lines.push(`export const points = __freeze(${JSON.stringify(composition.preflight.points)});`);
    lines.push(`export const locales = __freeze(${JSON.stringify(composition.preflight.locales)});`);
    lines.push(`export const admission = __freeze(${JSON.stringify(composition.preflight.admission)});`);
    lines.push(`export const presentationLimits = __freeze(${JSON.stringify(composition.limits.presentation)});`);
    lines.push('export const factories = Object.freeze({');
    links.forEach(({ key, index, name }, position) => {
      const comma = position + 1 < links.length ? ',' : '';
      lines.push(`  ${JSON.stringify(key)}: __mod${index}[${JSON.stringify(name)}]${comma}`);
    });
    lines.push('});');
    lines.push('');
    return lines.join('\n');
  }
  return {
    name: 'pixs-composition',
    config() {
      return { build: { sourcemap: false, rolldownOptions: { output: { codeSplitting: false } } } };
    },
    configResolved(config) {
      command = config.command ?? command;
    },
    buildStart() {
      if (mode !== 'COMPOSED') return;
      verifiedOrFail();
      for (const { module } of fileToModule.values()) safeHash(module.text, module.hash);
    },
    resolveId(source, importer) {
      if (mode === 'COMPOSED' && typeof importer === 'string' && importer.startsWith(RESOLVED_CAPTURED_PREFIX)) {
        const importerFile = [...fileToModule.entries()].find(([, record]) => record.resolved === importer)?.[0];
        if (!importerFile) fail('PLUGIN_RESOLUTION_UNKNOWN');
        const resolution = composition.imports.resolutions.find(candidate => candidate.from === importerFile && candidate.source === source);
        if (!resolution) fail('PLUGIN_RESOLUTION_UNKNOWN');
        if (resolution.source === SHELL_ALIAS) return path.join(root, 'frontend', 'src', 'shell', 'api-v1.js');
        if (resolution.source.startsWith('.')) {
          const record = fileToModule.get(resolution.target);
          if (!record) fail('PLUGIN_RESOLUTION_UNKNOWN');
          return record.resolved;
        }
        const facade = composition.policy.imports.foreignFacades[resolution.source];
        if (!facade) fail('PLUGIN_RESOLUTION_UNKNOWN');
        const targetRoot = composition.envelope.capture.owners.find(owner => owner.owner === facade.owner)?.root;
        const record = fileToModule.get(targetRoot + '/' + facade.entry);
        if (!record) fail('PLUGIN_RESOLUTION_UNKNOWN');
        return record.resolved;
      }
      if (source === VIRTUAL_ID || source === RESOLVED_VIRTUAL_ID) return RESOLVED_VIRTUAL_ID;
      if (mode === 'COMPOSED' && typeof source === 'string' && source.startsWith(RESOLVED_CAPTURED_PREFIX)) {
        for (const record of fileToModule.values()) if (record.resolved === source) return source;
        fail('PLUGIN_RESOLUTION_UNKNOWN');
      }
      if (mode !== 'COMPOSED') return null;
      if (typeof source === 'string' && source.startsWith(CAPTURED_PREFIX)) {
        if (importer !== RESOLVED_VIRTUAL_ID) fail('PLUGIN_RESOLUTION_UNKNOWN');
        const resolved = source.replace(CAPTURED_PREFIX, RESOLVED_CAPTURED_PREFIX);
        for (const record of fileToModule.values()) if (record.resolved === resolved) return resolved;
        fail('PLUGIN_RESOLUTION_UNKNOWN');
      }
      return null;
    },
    load(id) {
      const captured = typeof id === 'string' && id.startsWith(RESOLVED_CAPTURED_PREFIX);
      if (mode === 'COMPOSED' && (id === RESOLVED_VIRTUAL_ID || captured)) {
        if (drifted) fail('COMPOSITION_DRIFT');
        if (command !== 'build') verifiedOrFail();
      }
      if (id === RESOLVED_VIRTUAL_ID) return buildVirtualSource();
      if (mode !== 'COMPOSED' || !captured) return null;
      const record = [...fileToModule.values()].find(candidate => candidate.resolved === id);
      if (!record) fail('PLUGIN_RESOLUTION_UNKNOWN');
      safeHash(record.module.text, record.module.hash);
      return record.module.text;
    },
    generateBundle() {
      if (mode !== 'COMPOSED') return;
      verifiedOrFail();
      this.emitFile({ type: 'asset', fileName: 'composition.json', source: JSON.stringify(composition.report) });
    },
    configureServer(server) {
      if (mode !== 'COMPOSED') return;
      watchedFiles = watchedAbsoluteFiles();
      const watcher = server.watcher;
      let pending = false;
      const onChange = file => {
        if (stopped || !watchedFiles.includes(file) || pending) return;
        pending = true;
        queueMicrotask(() => {
          pending = false;
          if (stopped || drifted) return;
          try { verifiedOrFail(); }
          catch (cause) {
            // Le prochain accès reçoit un refus fixe ; aucun code ni chemin n'est projeté.
            drifted = true;
            server.config.logger.error('COMPOSITION_DRIFT');
          }
        });
      };
      watcher.add(watchedFiles);
      for (const event of ['change', 'add', 'unlink']) watcher.on(event, onChange);
      cleanupServer = () => {
        if (stopped) return;
        stopped = true;
        for (const event of ['change', 'add', 'unlink']) watcher.off(event, onChange);
        server.httpServer?.off('close', cleanupServer);
      };
      server.httpServer?.once('close', cleanupServer);
      server.middlewares.use((request, response, next) => {
        if (!drifted) return next();
        response.statusCode = 503;
        response.setHeader('Content-Type', 'text/plain; charset=utf-8');
        response.setHeader('Cache-Control', 'no-store');
        response.setHeader('X-Content-Type-Options', 'nosniff');
        response.end('COMPOSITION_DRIFT');
      });
    },
    closeBundle() { cleanupServer(); },

  };
}
