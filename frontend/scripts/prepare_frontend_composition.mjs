// Pont build Node vers le pont Python borne, sans ecriture ni activation.
// Ordre impose : pins/bornes, policy, prepare, imports, profil, preflight, facts, graph, report.
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { types as utilTypes } from 'node:util';
import { collectFrontendImports } from './composition-imports-v1.mjs';
import { analyzePresentationSource, PresentationSourceError } from './presentation-profile-v1.mjs';
import { preflightContributions, composeContributionGraph } from '../src/shell/composition-graph-v1.js';

export const BRIDGE_SCHEMA = 'pixs.frontend.bridge/1.0.0';
export const REPORT_SCHEMA = 'pixs.frontend.composition-report/1.0.0';
const SHELL_ALIAS = 'pixs-shell/v1';
const preparedCompositions = new WeakSet();
const GLOBAL_PROFILE_CODES = new Set([
  'PROFILE_AST_LIMIT',
  'PROFILE_BINDINGS_LIMIT',
  'PROFILE_SCOPE_LIMIT',
  'PROFILE_TEXT_LIMIT',
  'PROFILE_SOURCE_INVALID',
  'PROFILE_LIMITS_INVALID',
]);
const STRUCTURAL_PROFILE_CODES = new Set([
  'PROFILE_NODE_REFUSED', 'PROFILE_MEMBER_REFUSED', 'PROFILE_PARSE_INVALID',
  'PROFILE_BINDING_INVALID', 'PROFILE_ASSIGNMENT_REFUSED',
  'PROFILE_FREE_IDENTIFIER', 'PROFILE_TOP_LEVEL_EFFECT',
]);

export class CompositionBuildError extends Error {
  constructor(code, options) {
    super(code, options);
    this.name = 'CompositionBuildError';
    this.code = code;
  }
}
function fail(code, cause) {
  if (cause === undefined) throw new CompositionBuildError(code);
  throw new CompositionBuildError(code, { cause });
}
function assertHex64(value, code) {
  if (typeof value !== 'string' || value.length !== 64 || !/^[0-9a-f]{64}$/.test(value)) fail(code);
  return value;
}
function assertSafeInt(value, code) {
  if (typeof value !== 'number' || !Number.isSafeInteger(value) || value <= 0) fail(code);
  return value;
}
function freezeJson(value, seen = new Set()) {
  if (value === null || typeof value !== 'object' || seen.has(value)) return value;
  if (typeof Buffer !== 'undefined' && Buffer.isBuffer(value)) return value;
  if (value instanceof Uint8Array || value instanceof DataView) return value;
  seen.add(value);
  for (const key of Reflect.ownKeys(value)) {
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail('BUILD_SHAPE_INVALID');
    freezeJson(descriptor.value, seen);
  }
  return Object.freeze(value);
}
function rootFromScript() {
  return path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
}
function bridgeScriptFor(root) {
  return path.join(root, 'frontend', 'scripts', 'frontend_composition_bridge.py');
}
function closedRecord(value, names, code) {
  if (value === null || typeof value !== 'object' || Array.isArray(value) || utilTypes.isProxy(value)) fail(code);
  const proto = Object.getPrototypeOf(value);
  if (proto !== Object.prototype && proto !== null) fail(code);
  const keys = Reflect.ownKeys(value);
  if (keys.length !== names.length) fail(code);
  const copy = {};
  for (const name of names) {
    const descriptor = Object.getOwnPropertyDescriptor(value, name);
    if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail(code);
    Object.defineProperty(copy, name, { value: descriptor.value, enumerable: true });
  }
  return copy;
}
function decodeBridgeResponse(stdout, maxWireBytes) {
  if (!Buffer.isBuffer(stdout) || !stdout.length || stdout.length > maxWireBytes) fail('BRIDGE_RESPONSE_INVALID');
  let envelope;
  try {
    envelope = JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(stdout));
  } catch (cause) {
    fail('BRIDGE_RESPONSE_INVALID', cause);
  }
  if (envelope?.ok === true) {
    envelope = closedRecord(envelope, ['schema', 'ok', 'result'], 'BRIDGE_RESPONSE_INVALID');
  } else if (envelope?.ok === false) {
    envelope = closedRecord(envelope, ['schema', 'ok', 'error_code'], 'BRIDGE_RESPONSE_INVALID');
    if (typeof envelope.error_code !== 'string' || !/^[A-Z][A-Z0-9_]{0,63}$/.test(envelope.error_code)) fail('BRIDGE_RESPONSE_INVALID');
  } else fail('BRIDGE_RESPONSE_INVALID');
  if (envelope.schema !== BRIDGE_SCHEMA) fail('BRIDGE_RESPONSE_INVALID');
  return envelope;
}
function callBridge({ pythonExecutable, bridgeScript, root, maxWireBytes, maxPolicyBytes, request }) {
  let payload;
  try {
    payload = Buffer.from(JSON.stringify(request), 'utf-8');
  } catch (cause) {
    fail('BRIDGE_REQUEST_INVALID', cause);
  }
  if (payload.length > maxWireBytes) fail('BRIDGE_WIRE_TOO_LARGE');
  let spawned;
  try {
    spawned = spawnSync(pythonExecutable, [
      '-B', bridgeScript, '--max-wire-bytes', String(maxWireBytes),
      '--max-policy-bytes', String(maxPolicyBytes),
    ], {
      input: payload, cwd: root, shell: false, encoding: null, maxBuffer: maxWireBytes,
      env: {
        LANG: 'C.UTF-8', PYTHONDONTWRITEBYTECODE: '1',
        PYTHONPATH: path.join(root, 'src') + ':' + path.join(root, 'frontend', 'scripts'),
        PATH: path.dirname(pythonExecutable) + ':/usr/bin:/bin',
      },
    });
  } catch (cause) {
    fail('BRIDGE_SPAWN_FAILED', cause);
  }
  if (spawned.error) fail('BRIDGE_SPAWN_FAILED', spawned.error);
  if (spawned.signal || spawned.status === null) fail('BRIDGE_PROCESS_FAILED');
  const envelope = decodeBridgeResponse(spawned.stdout, maxWireBytes);
  if (spawned.status !== 0 || envelope.ok !== true) {
    fail(envelope.ok === false ? envelope.error_code : 'BRIDGE_PROCESS_FAILED');
  }
  return envelope.result;
}
// Propagation a point fixe des owners refuses vers leurs importeurs.
// Cible relative exacte, facades etrangeres via policy, alias shell sans owner externe.
function propagateProfileRefusals(imports, policy, refusedOwners, envelope) {
  const fileToOwner = new Map();
  for (const owner of envelope.capture.owners) {
    for (const source of owner.sources) fileToOwner.set(source.path, owner.owner);
  }
  const diagnostics = [...imports.diagnostics];
  const recorded = new Set(diagnostics.map(item => JSON.stringify([item.owner, item.path, item.code])));
  let changed = true;
  while (changed) {
    changed = false;
    for (const resolution of imports.resolutions) {
      const fromOwner = fileToOwner.get(resolution.from);
      if (!fromOwner) fail('BUILD_RESOLUTION_INVALID');
      if (refusedOwners.has(fromOwner) || resolution.source === SHELL_ALIAS) continue;
      let targetOwner;
      if (resolution.source.startsWith('.')) targetOwner = fileToOwner.get(resolution.target);
      else if (Object.hasOwn(policy.imports.foreignFacades, resolution.source)) {
        targetOwner = policy.imports.foreignFacades[resolution.source].owner;
      } else fail('BUILD_RESOLUTION_INVALID');
      if (!targetOwner) fail('BUILD_RESOLUTION_INVALID');
      if (refusedOwners.has(targetOwner)) {
        refusedOwners.add(fromOwner);
        changed = true;
        const diagnostic = { owner: fromOwner, path: resolution.from, code: 'IMPORT_DEPENDENCY_UNAVAILABLE' };
        const key = JSON.stringify([diagnostic.owner, diagnostic.path, diagnostic.code]);
        if (!recorded.has(key)) { recorded.add(key); diagnostics.push(diagnostic); }
      }
    }
  }
  return {
    modules: imports.modules.filter(module => !refusedOwners.has(module.owner)),
    resolutions: imports.resolutions.filter(resolution => !refusedOwners.has(fileToOwner.get(resolution.from))),
    diagnostics,
  };
}

export function isPreparedFrontendComposition(value) {
  return value !== null && typeof value === 'object' && preparedCompositions.has(value);
}

export function prepareFrontendComposition(options) {
  const checked = closedRecord(options, [
    'selectionBytes', 'expectedSelectionSha256', 'policyBytes', 'expectedPolicySha256',
    'maxPolicyBytes', 'maxWireBytes', 'pythonExecutable',
  ], 'BUILD_OPTIONS_INVALID');
  const { selectionBytes, expectedSelectionSha256, policyBytes, expectedPolicySha256, maxPolicyBytes, maxWireBytes, pythonExecutable } = checked;
  if (utilTypes.isProxy(selectionBytes) || utilTypes.isProxy(policyBytes) || !Buffer.isBuffer(selectionBytes) || !Buffer.isBuffer(policyBytes)) fail('BUILD_BYTES_INVALID');
  if (typeof pythonExecutable !== 'string' || !path.isAbsolute(pythonExecutable) || /[\0\r\n]/.test(pythonExecutable)) fail('BUILD_PYTHON_INVALID');
  assertHex64(expectedSelectionSha256, 'BUILD_PIN_INVALID');
  assertHex64(expectedPolicySha256, 'BUILD_PIN_INVALID');
  assertSafeInt(maxPolicyBytes, 'BUILD_BOUNDS_INVALID');
  assertSafeInt(maxWireBytes, 'BUILD_BOUNDS_INVALID');
  const root = rootFromScript();
  const bridgeScript = bridgeScriptFor(root);
  const initialSelection = Buffer.from(selectionBytes);
  const initialPolicy = Buffer.from(policyBytes);
  if (initialSelection.length === 0 || initialPolicy.length === 0) fail('BUILD_BYTES_INVALID');
  if (initialSelection.length > maxWireBytes || initialPolicy.length > maxPolicyBytes) fail('BUILD_BOUNDS_INVALID');
  if (createHash('sha256').update(initialSelection).digest('hex') !== expectedSelectionSha256) fail('BUILD_PIN_MISMATCH');
  if (createHash('sha256').update(initialPolicy).digest('hex') !== expectedPolicySha256) fail('BUILD_PIN_MISMATCH');
  // 1. Politique via pont : JSON strict, sept groupes fermes, wire concordant.
  const document = callBridge({
    pythonExecutable, bridgeScript, root, maxWireBytes, maxPolicyBytes,
    request: { operation: 'policy', policy_b64: initialPolicy.toString('base64'), expected_policy_sha256: expectedPolicySha256 },
  });
  const checkedDocument = closedRecord(document, ['schema', 'policy', 'limits'], 'BRIDGE_RESPONSE_INVALID');
  if (checkedDocument.schema !== 'pixs.frontend.build-policy/1.0.0') fail('BRIDGE_RESPONSE_INVALID');
  const policy = freezeJson(checkedDocument.policy);
  const limits = freezeJson(checkedDocument.limits);
  // 2. Vrai PlanEnvelope via pont prepare.
  const envelope = freezeJson(callBridge({
    pythonExecutable, bridgeScript, root, maxWireBytes, maxPolicyBytes,
    request: {
      operation: 'prepare',
      selection_b64: initialSelection.toString('base64'),
      expected_selection_sha256: expectedSelectionSha256,
      selection_limits: { ...limits.selection },
    },
  }));
  if (envelope?.capture?.selection_sha256 !== expectedSelectionSha256) fail('BUILD_CAPTURE_MISMATCH');
  // 3. Imports existants, sans champ invente.
  const rawImports = collectFrontendImports(envelope, policy.imports, limits.imports);
  const sourceLimits = { ...limits.sourceProfile };
  const refusedOwners = new Set();
  const structureDiagnostics = [];
  // 4. Profil pour TOUS les modules survivants, avant preflight.
  for (const module of rawImports.modules) {
    try {
      analyzePresentationSource(module.text, sourceLimits);
    } catch (error) {
      if (!(error instanceof PresentationSourceError)) fail('PROFILE_INVARIANT_FAILED', error);
      if (GLOBAL_PROFILE_CODES.has(error.code)) fail(error.code, error);
      if (!STRUCTURAL_PROFILE_CODES.has(error.code)) fail('PROFILE_INVARIANT_FAILED', error);
      structureDiagnostics.push({ owner: module.owner, path: module.file, code: error.code });
      refusedOwners.add(module.owner);
    }
  }
  let imports = rawImports;
  if (refusedOwners.size > 0 || structureDiagnostics.length > 0) {
    const merged = { modules: rawImports.modules, resolutions: rawImports.resolutions, diagnostics: [...rawImports.diagnostics, ...structureDiagnostics] };
    const filtered = propagateProfileRefusals(merged, policy, refusedOwners, envelope);
    imports = freezeJson(filtered);
  } else {
    imports = freezeJson({ modules: rawImports.modules, resolutions: rawImports.resolutions, diagnostics: [...rawImports.diagnostics] });
  }
  // 5. Preflight puis faits puis graphe, sur survivants seuls.
  const preflight = freezeJson(preflightContributions(envelope, imports, policy, limits.graph));
  const facts = freezeJson(callBridge({
    pythonExecutable, bridgeScript, root, maxWireBytes, maxPolicyBytes,
    request: {
      operation: 'facts',
      facets: preflight.facets.map((facet) => ({ ...facet })),
      component_order: [...preflight.componentOrder],
      component_edges: preflight.componentEdges.map((edge) => [...edge]),
      requirements_limits: { ...limits.requirements },
    },
  }));
  const graph = freezeJson(composeContributionGraph(preflight, facts, limits.graph));
  // 6. Blocage global avant Vite/artefact, jamais faux READY.
  if (graph.blocked === true) {
    const error = new CompositionBuildError('GRAPH_BLOCKED');
    error.diagnostics = [...graph.diagnostics];
    throw error;
  }
  // 7. Rapport public sur, sans code ni capture.
  const report = freezeJson({
    schema: REPORT_SCHEMA,
    order: graph.order.map((entry) => ({ ...entry })),
    edges: graph.contributionEdges.map((edge) => [...edge]),
    points: JSON.parse(JSON.stringify(preflight.points)),
    locales: [...preflight.locales],
    diagnostics: graph.diagnostics.map((entry) => ({ ...entry })),
    blocked: false,
    context_fingerprint: envelope.capture.context_fingerprint,
    selection_sha256: envelope.capture.selection_sha256,
    policy_sha256: expectedPolicySha256,
  });
  const build = {
    envelope,
    policy,
    limits,
    imports,
    preflight,
    graph,
    report,
    verifyBeforePublish() {
      if (createHash('sha256').update(initialSelection).digest('hex') !== expectedSelectionSha256) fail('BUILD_PIN_MISMATCH');
      if (createHash('sha256').update(initialPolicy).digest('hex') !== expectedPolicySha256) fail('BUILD_PIN_MISMATCH');
      const verified = callBridge({
        pythonExecutable, bridgeScript, root, maxWireBytes, maxPolicyBytes,
        request: {
          operation: 'verify',
          capture: JSON.parse(JSON.stringify(envelope.capture)),
          selection_b64: initialSelection.toString('base64'),
          expected_selection_sha256: expectedSelectionSha256,
          selection_limits: { ...limits.selection },
        },
      });
      const checkedVerified = closedRecord(verified, [
        'verified', 'selection_sha256', 'context_fingerprint',
      ], 'BRIDGE_VERIFY_FAILED');
      if (checkedVerified.verified !== true
          || checkedVerified.selection_sha256 !== expectedSelectionSha256
          || checkedVerified.context_fingerprint !== envelope.capture.context_fingerprint) fail('BRIDGE_VERIFY_FAILED');
      return freezeJson(verified);
    },
  };
  const prepared = freezeJson(build);
  preparedCompositions.add(prepared);
  return prepared;
}
