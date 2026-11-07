// Raccord C11 réel Python/Kernel/Vite ; preuves de composition en DEVELOPMENT.
// Le rendu et les mutations HTTPS restent qualifiés par la recette navigateur distincte.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { build, createServer } from 'vite';
import { prepareFrontendComposition, isPreparedFrontendComposition } from '../scripts/prepare_frontend_composition.mjs';
import { createPixsCompositionPlugin } from '../scripts/pixs-composition-plugin-v1.mjs';
import { createFrontendViteConfig } from '../vite.config.js';
import { readOperatorFile, parseCliArgs } from '../scripts/run_frontend_build.mjs';

const ROOT = fileURLToPath(new URL('../../', import.meta.url));
const WORK_BASE = path.join(ROOT, 'output/cismp/cismp3-pixs-c4b2bfe2c6614f3f/composed-pipeline');
const SELECTION = 'frontend/tests/c14-composed-selection.json';
const POLICY = 'frontend/tests/c14-composed-policy.json';
const SELECTION_PIN = '539ea89ffbe85012ba2f80e180240b8fb08502d781ea4d96bca6db38b7b7ed22';
const POLICY_PIN = 'c1ec66595f72710df7c8d7afb50c3c74e66d9d3fb32a4e432817267380463cd6';
const PYTHON = '/home/devops/datas/pixs/.venv/bin/python3';
const digest = value => crypto.createHash('sha256').update(value).digest('hex');
function nominal() {
  const selectionBytes = readOperatorFile(ROOT, SELECTION, 1048576);
  const policyBytes = readOperatorFile(ROOT, POLICY, 65536);
  assert.equal(digest(selectionBytes), SELECTION_PIN, 'selection approuvee devenue perimee');
  assert.equal(digest(policyBytes), POLICY_PIN, 'profil de recette devenu perime');
  assert.equal(JSON.parse(selectionBytes.toString('utf8')).environment, 'DEVELOPMENT');
  const { maxPolicyBytes, maxWireBytes } = JSON.parse(policyBytes.toString('utf8')).limits.wire;
  return { selectionBytes, policyBytes, maxPolicyBytes, maxWireBytes,
    expectedSelectionSha256: SELECTION_PIN, expectedPolicySha256: POLICY_PIN,
    pythonExecutable: PYTHON };
}
const prepare = () => prepareFrontendComposition(nominal());

test('pipeline : CLI ferme et documents operateur epingles', () => {
  const n = nominal();
  assert.deepEqual(parseCliArgs(['--mode', 'STANDALONE', '--command', 'build']),
    { mode: 'STANDALONE', command: 'build' });
  assert.throws(() => parseCliArgs(['--mode', 'COMPOSED', '--command', 'build']), /CLI_OPTION_MISSING/);
  assert.throws(() => parseCliArgs(['--mode', 'STANDALONE', '--command', 'build',
    '--selection', SELECTION]), /CLI_OPTION_UNUSED/);
  assert.throws(() => parseCliArgs(['--mode', 'STANDALONE', '--mode', 'STANDALONE',
    '--command', 'build']), /CLI_OPTION_DUPLICATE/);
  assert.throws(() => readOperatorFile(ROOT, 'project.env', 1024), /CLI_PATH_INVALID|CLI_PATH_EXCLUDED/);
  assert.equal(n.maxWireBytes, 1048576);
});

test('pipeline : options fermees et pins refuses avant lancement Python', () => {
  const n = nominal();
  assert.throws(() => prepareFrontendComposition({}), /BUILD_OPTIONS_INVALID/);
  assert.throws(() => prepareFrontendComposition({ ...n, extra: true }), /BUILD_OPTIONS_INVALID/);
  const missingPython = path.join(WORK_BASE, 'python-inexistant');
  for (const field of ['selectionBytes', 'policyBytes']) {
    const altered = Buffer.from(n[field]); altered[0] ^= 1;
    assert.throws(() => prepareFrontendComposition({
      ...n, [field]: altered, pythonExecutable: missingPython,
    }), /BUILD_PIN_MISMATCH/);
  }
});

test('pipeline : vrai pont Python Kernel imports profil et graphe', () => {
  const prepared = prepare();
  assert.equal(isPreparedFrontendComposition(prepared), true);
  assert.equal(prepared.graph.blocked, false);
  assert.ok(prepared.graph.order.length > 0);
  for (const owner of ['pixs.pzt', 'pixs.dns']) {
    assert.ok(prepared.graph.contributions.some(item => item.owner === owner));
  }
  assert.equal(prepared.report.selection_sha256, SELECTION_PIN);
  assert.equal(prepared.report.policy_sha256, POLICY_PIN);
  assert.equal(prepared.envelope.capture.selection_sha256, SELECTION_PIN);
  assert.equal(Object.isFrozen(prepared.report), true);
  assert.equal(Object.isFrozen(prepared.graph.contributions), true);
});

test('pipeline : provenance non forgeable et verification avant publication', () => {
  const prepared = prepare();
  let called = 0;
  const forged = { ...prepared, verifyBeforePublish() { called++; return { verified: true }; } };
  assert.equal(isPreparedFrontendComposition(forged), false);
  assert.throws(() => createPixsCompositionPlugin({ mode: 'COMPOSED', composition: forged }),
    /PLUGIN_COMPOSITION_INVALID/);
  assert.equal(called, 0);
  const proxy = new Proxy(prepared, { get() { called++; throw new Error('ACCESSEUR_INTERDIT'); } });
  assert.throws(() => createPixsCompositionPlugin({ mode: 'COMPOSED', composition: proxy }),
    /PLUGIN_COMPOSITION_INVALID/);
  assert.equal(called, 0);
  assert.equal(createPixsCompositionPlugin({ mode: 'COMPOSED', composition: prepared }).name,
    'pixs-composition');
  const verified = prepared.verifyBeforePublish();
  assert.equal(verified.verified, true);
  assert.equal(verified.selection_sha256, SELECTION_PIN);
});

test('pipeline : copies des octets conservees sans alias de l appelant', () => {
  const n = nominal(), prepared = prepareFrontendComposition(n);
  n.selectionBytes.fill(0); n.policyBytes.fill(0);
  assert.equal(prepared.report.selection_sha256, SELECTION_PIN);
  assert.equal(prepared.report.policy_sha256, POLICY_PIN);
  assert.equal(prepared.verifyBeforePublish().verified, true);
});

function rawReport(source) {
  const prefix = 'export const report = __freeze(';
  const lines = source.split(String.fromCharCode(10)).filter(line => line.startsWith(prefix));
  assert.equal(lines.length, 1, 'un seul rapport public dans module virtuel');
  assert.ok(lines[0].endsWith(');'));
  return JSON.parse(lines[0].slice(prefix.length, -2));
}

test('pipeline : rapport dev servi et rapport bundle reel concordent', async () => {
  const prepared = prepare();
  await fsp.mkdir(WORK_BASE, { recursive: true });
  const work = await fsp.mkdtemp(path.join(WORK_BASE, 'run-'));
  const outDir = path.join(work, 'bundle'), cacheDir = path.join(work, 'vite-cache');
  let server = null, problem = null;
  try {
    const dev = createFrontendViteConfig({ mode: 'COMPOSED', composition: prepared });
    server = await createServer({ ...dev, configFile: false, cacheDir, logLevel: 'error',
      server: { ...dev.server, host: '127.0.0.1', port: 0, strictPort: false } });
    await server.listen();
    const address = server.httpServer.address();
    assert.ok(address && typeof address.port === 'number' && address.port > 0);
    const virtual = 'virtual:pixs-composition/v1';
    const resolved = await server.pluginContainer.resolveId(virtual);
    assert.ok(resolved?.id);
    const loaded = await server.pluginContainer.load(resolved.id);
    const raw = typeof loaded === 'string' ? loaded : loaded?.code;
    assert.equal(typeof raw, 'string');
    const devReport = rawReport(raw);
    assert.deepEqual(devReport, JSON.parse(JSON.stringify(prepared.report)));
    const response = await fetch('http://127.0.0.1:' + address.port
      + '/@id/__x00__virtual:pixs-composition/v1');
    assert.equal(response.status, 200);
    const served = await response.text();
    assert.ok(served.includes(SELECTION_PIN));
    assert.ok(served.includes(POLICY_PIN));
    await server.close(); server = null;
    const prod = createFrontendViteConfig({ mode: 'COMPOSED', composition: prepared });
    const result = await build({ ...prod, configFile: false, cacheDir, logLevel: 'error',
      build: { ...prod.build, outDir, emptyOutDir: true } });
    const report = JSON.parse(await fsp.readFile(path.join(outDir, 'composition.json'), 'utf8'));
    assert.deepEqual(report, devReport);
    const outputs = (Array.isArray(result) ? result : [result]).flatMap(item => item.output);
    const chunks = outputs.filter(item => item.type === 'chunk');
    assert.ok(chunks.length > 0);
    let composed = false;
    for (const chunk of chunks) {
      const bytes = await fsp.readFile(path.join(outDir, chunk.fileName), 'utf8');
      assert.equal(bytes, chunk.code);
      if (bytes.includes('COMPOSED')) composed = true;
    }
    assert.equal(composed, true);
    assert.equal(report.blocked, false);
    assert.equal(prepared.verifyBeforePublish().verified, true);
  } catch (error) { problem = error; }
  const cleanupErrors = [];
  if (server) {
    try { await server.close(); } catch (error) { cleanupErrors.push(error); }
  }
  try { await fsp.rm(work, { recursive: true, force: true }); }
  catch (error) { cleanupErrors.push(error); }
  if (cleanupErrors.length) {
    throw new AggregateError([...(problem ? [problem] : []), ...cleanupErrors],
      'PIPELINE_NETTOYAGE_ECHOUE', { cause: problem });
  }
  if (problem) throw problem;
  assert.equal(fs.existsSync(work), false);
});
