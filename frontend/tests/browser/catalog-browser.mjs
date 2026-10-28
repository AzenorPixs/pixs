#!/usr/bin/env node
import http from 'node:http';
import fsp from 'node:fs/promises';
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import crypto from 'node:crypto';
import { build as buildVendor } from 'vite';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FRONTEND = path.resolve(HERE, '..', '..');
const CACHE_ROOT = path.join(FRONTEND, '.cache');
const SESSION_ID = crypto.randomUUID();
const DEADLINE_MS = 90000;
const MAX_BODY = 64 * 1024;
const LOG_CAP = 8 * 1024;
const GRACE_MS = 2000;
const VERSION_CAP_MS = 5000;
const CLOSE_CAP_MS = 2000;
const CASE_COUNT = 145;
const EXPECTED_CASES = Object.freeze(["canonical and French catalogues are complete, immutable and namespaced", "catalogue rejects duplicate, missing and invalid translations", "locale follows the first supported preference, then explicit fallback", "façade : exports appelables et délégation des ports", "ports fermés : types, champs secrets et accesseurs refusés", "périmètres canoniques : plateforme, tenant, scope opaques et session UUIDv7", "snapshots : copies profondes immuables sans alias", "provider : époque et réponse courante contrôlées", "contexte actif : assurances et hints explicites", "contexte inactif : purge des faits et refus des secrets", "routes web : URL externe, traversée et Auth refusées", "queries : contexte du provider et enveloppe C06", "commands : attente serveur, idempotence et copie de l’entrée", "réponse retardée : aucun fait de l’ancien contexte exposé", "résultat connu, refus, panne et issue inconnue distingués", "descripteur : huit types nominaux gelés et concordants", "descripteur : onze points uniques, metadata gelée et catégorie concordante", "descripteur : concordance huit champs, owner_version et requires ordre-multiplicité", "descripteur : limits obligatoires et budgets avant boucles, creux et très grands refusés", "descripteur : facette entry Kernel non normalisée, point et garanties refusés", "descripteur : payload fermé, CSR et exports nommés, chemins privés refusés", "descripteur : chemins fermés, traversée et param canonique", "descripteur : permissions déclaratives, trust et slot modulaire public", "descripteur : catalogues namespacés, LF accepté et sans alias", "descripteur : accesseurs non appelés, exotiques et gelé accepté", "descripteur : tous les champs de facette et limites de volume sont contrôlés", "descripteur : accesseurs de chaque frontière refusés et copies profondes", "transport opaque : slash pourcent espace unicode encodes par segment", "transport : point point NUL surrogate isole refuses avant envoi", "resolveur proprietaire fictif acme.demo : snake namespace semver prerelease", "resolveur : absent collision version scopes secrets getters segments reserves refuses", "resolveur : kind name hostiles sans coercition ni getter, immuable sans alias", "core P T S et 22 15 : memberships refuse, create-group nominal, usurpation refusee", "bindShellApi second param utilise par query et command", "params core sous params : limit cursor ref types, ordre conserve, gele", "params proprietaires transmis sans tri core, snapshot gele", "préflight et graphe purs immuables, sans mutation des entrées", "owner et version du descripteur ne sont jamais réécrits pour concorder", "descripteur surnuméraire retire le propriétaire, pas son voisin", "descripteur absent obligatoire bloque même sans contribution conservée", "doublons sans arbitre et mandatory contradictoire ne devient pas optionnel", "empreinte module/capture et diagnostic owner sont recoupés", "exports réellement callable requis avant graphe", "SANDBOXED sans adapter et DEVELOPMENT en production refusés", "namespace réservé exige owner officiel et propriété concordante", "intersections avec routes protégées refusées, pas uniquement égalité", "paramètres répétés refusés dans une seule route", "deux routes en intersection sont toutes deux retirées, indépendant conservé", "paramètres de même nom sur deux routes ne provoquent pas erreur globale", "slots APPEND gardés dans ordre déclaré ; REJECT retire toutes les collisions", "catalogues en/fr complets et mêmes paramètres nommés", "catalogue appartient au namespace du composant", "clés de traduction en collision retirent les deux contributions", "navigation exige une route et son libellé de catalogue disponibles", "collision des clés UI_PERMISSION refuse les deux, sans créer un droit", "dépendance intra-composant prime sur tri alphabétique des identifiants", "cycles exacts, dépendants diagnostiqués séparément et indépendants gardés", "composante cyclique complète avec arête vers sommet déjà visité", "faits incomplets, index, candidats, edges et agrégat falsifiés refusés", "exigence manquante optionnelle isolée, obligatoire bloque", "refus après collision propagé vers dépendant obligatoire", "point public parent consommé avec dépendances commune et contribution prouvées", "point public sans dépendance frontend vers son fournisseur refusé", "fournisseur de point invalide retire aussi les consommateurs", "erreur de capture recoupée par owner_index et admission hors capture", "points privés ou sans relation commune ne sont pas consommables", "politique, version, budgets et accès de données stricts", "ordre de découverte des facettes et descripteurs sans effet sur résultat", "chaîne de 512 contributions résolue sans récursion du graphe", "navigation sans paramètres explicites ne consomme pas un libellé paramétré", "présentation : arbre fermé copié, profondément gelé et sans mutation", "présentation : alias autorisés copiés sans partager, cycles refusés", "présentation : styles, HTML, composants bruts et variantes inconnues refusés", "présentation : catalogue propriétaire et paramètres exacts des deux langues", "présentation : liens déclarés avec paramètres URL complets et sûrs", "présentation : seuls slots et composants publics admis par le contexte", "présentation : formulaire, liaison de champ et statut de commande sans exécution", "présentation : statut ne référence pas un id action absent", "présentation : champs ou cibles de liaison dupliqués refusés", "présentation : chemins de corps déclarés, pas prototype ni cible arbitraire", "présentation : formulaire imbriqué et champs ou submit sans formulaire refusés", "présentation : accesseurs jamais invoqués et tableaux creux refusés", "présentation : quotas explicites de nœuds, profondeur, données et corps", "présentation : bouton autonome et statut avant déclaration d’action", "présentation : bouton submit ne crée pas un faux id de résultat autonome", "présentation : section de formulaire conserve portée des champs et liaisons", "adapter : classes sémantiques et heading associé sans style ou HTML brut", "adapter : headings distincts ne partagent pas une clé objet convertie en chaîne", "adapter : Link injecté et segment URI encodé", "adapter : tous champs imbriqués rendus et submit hérite du formulaire", "adapter : submit conserve événement privé, valeurs copiées et gelées", "adapter : champ requis vide refusé avant appel commande", "adapter : bouton autonome a statut automatique sans confirmer retour du port", "adapter : rejet asynchrone signalé sans recopier le message privé", "adapter : PENDING empêche une deuxième commande même si port incohérent", "adapter : plusieurs statuts explicites ont ids uniques, sans statut auto doublé", "adapter : slots et composants restent des ports privés injectés", "adapter : ports fermés, états invalides, ids dupliqués et labels non textuels refusés", "construction sans reseau et ports fermes sans appel accesseur", "origine http bloque transport avant tout envoi reseau", "contexte actif verifie scope opaque session et meta separes", "correlation meta payload temps session invalides refuses sans partiel", "liaison proprietaire injectee fige sinon refus sans invention", "csrf amorce puis post protege porte session idempotence", "params requete gardent ordre doublons encodent scopes invalides refuses", "reponse retardee ignoree epoque changee abort observe", "expiration serveur purge delai technique sans vrai sommeil", "401 mismatch purge differee 403 invalide sans revoque inventee", "hors ligne bloque avant reseau retour ne rejoue rien", "canal ne transporte que invalidation sans secret ignore reste", "panne canal rend indisponible et notifie purge avant propagation", "connexion emet load verifie puis active sans fuite mot de passe", "reprise identique garde cle empreinte divergent refuse sans post", "deconnexion distinguee rejouable garde cle entete corps", "mutation pendante refuse double et ignore resultat obsolete", "arret nettoie timers requetes ecoutes remonte echec", "construction : options, graphe, fabriques et points invalides refusés", "visibilite : PUBLIC, AUTH, PLATEFORME, TENANT et permissions sans droit", "isolation : deux proprietaires avec meme action locale", "requete : PENDING puis LOADED, fabrique voit reponse gelee et cache actualise", "commande : CONFIRMED a 200 et REJECTED a 4xx", "commande : panne et 5xx donnent UNKNOWN rejouable a cle identique", "rejeu : autre contenu ou session bloque, query et 4xx ne resolvent pas UNKNOWN", "double soumission PENDING refusee", "champs : false, entier, null, listes, enregistrements, LF et ordre valides", "champs invalides refuses avant tout envoi", "INVALID via reportError sans ecraser PENDING ou UNKNOWN", "purge : avant notification, reponses anciennes ignorees et barrieres gardees", "resolution : resolver courant change, liaison absente refuse sans envoi", "actions retirees inexecutable, composants et slots seulement declares", "fabrique sans effets reseau navigation ou invalidation, vrai cycle refuse", "chaine 512 admise, version numerique, ecoutes et dispose", "champs DOM : ports fermes et accesseurs jamais invoques", "champs DOM : texte natif libelle borne et valeur courante", "champs DOM : booleen false conserve puis true lu sans chaine", "champs DOM : entier facultatif null et nombre avec bornes", "champs DOM : liste preserve LF ordre doublons et copie", "champs DOM : enregistrements conservent colonnes LF et doublons", "champs DOM : ajout retrait respectent minimum maximum et disabled", "champs DOM : focus apres ajout retrait et retour au bouton", "champs DOM : modele stable garde brouillon puis nouvelle cle le purge", "champs DOM : deux proprietaires et modeles restent isoles", "champs DOM : lecteur refuse absent doublon colonne et budget", "champs DOM : variantes fermees et signal badInput refuse explicitement", "adapter runtime : contexte lie authentique, copies et perimes refuses"]);

const ROUTES = new Map([
  ['/', [path.join(HERE, 'runner.html'), 'text/html; charset=utf-8']],
  ['/tests/shell.test.mjs', [path.resolve(FRONTEND, 'tests', 'shell.test.mjs'), 'text/javascript; charset=utf-8']],
  ['/tests/shell-contracts.test.mjs', [path.resolve(FRONTEND, 'tests', 'shell-contracts.test.mjs'), 'text/javascript; charset=utf-8']],
  ['/src/shell/composition-descriptor-v1.js', [path.resolve(FRONTEND, 'src', 'shell', 'composition-descriptor-v1.js'), 'text/javascript; charset=utf-8']],
  ['/tests/composition-graph.test.mjs', [path.resolve(FRONTEND, 'tests', 'composition-graph.test.mjs'), 'text/javascript; charset=utf-8']],
  ['/src/shell/composition-graph-v1.js', [path.resolve(FRONTEND, 'src', 'shell', 'composition-graph-v1.js'), 'text/javascript; charset=utf-8']],
  ['/tests/presentation-contract.test.mjs', [path.resolve(FRONTEND, 'tests', 'presentation-contract.test.mjs'), 'text/javascript; charset=utf-8']],
  ['/src/shell/presentation-contract-v1.js', [path.resolve(FRONTEND, 'src', 'shell', 'presentation-contract-v1.js'), 'text/javascript; charset=utf-8']],
  ['/tests/presentation-adapter.test.mjs', [path.resolve(FRONTEND, 'tests', 'presentation-adapter.test.mjs'), 'text/javascript; charset=utf-8']],
  ['/src/shell/presentation-adapter-v1.js', [path.resolve(FRONTEND, 'src', 'shell', 'presentation-adapter-v1.js'), 'text/javascript; charset=utf-8']],
  ['/src/shell/api-v1.js', [path.resolve(FRONTEND, 'src', 'shell', 'api-v1.js'), 'text/javascript; charset=utf-8']],
  ['/src/catalogs.js', [path.resolve(FRONTEND, 'src', 'catalogs.js'), 'text/javascript; charset=utf-8']],
  ['/tests/session-runtime.test.mjs', [path.resolve(FRONTEND, 'tests/session-runtime.test.mjs'), 'text/javascript; charset=utf-8']],
  ['/tests/composition-runtime.test.mjs', [path.resolve(FRONTEND, 'tests/composition-runtime.test.mjs'), 'text/javascript; charset=utf-8']],
  ['/tests/presentation-fields.test.mjs', [path.resolve(FRONTEND, 'tests/presentation-fields.test.mjs'), 'text/javascript; charset=utf-8']],
  ['/src/shell/session-runtime-v1.js', [path.resolve(FRONTEND, 'src/shell/session-runtime-v1.js'), 'text/javascript; charset=utf-8']],
  ['/src/shell/composition-runtime-v1.js', [path.resolve(FRONTEND, 'src/shell/composition-runtime-v1.js'), 'text/javascript; charset=utf-8']],
  ['/src/shell/presentation-fields-v1.js', [path.resolve(FRONTEND, 'src/shell/presentation-fields-v1.js'), 'text/javascript; charset=utf-8']],
  ['/t/test-adapter.mjs', [path.join(HERE, 'test-adapter.mjs'), 'text/javascript; charset=utf-8']],
  ['/t/assert-adapter.mjs', [path.join(HERE, 'assert-adapter.mjs'), 'text/javascript; charset=utf-8']],
]);

const BROWSERS = [
  {
    id: 'chromium',
    bin: '/usr/bin/chromium',
    args: (url, profile) => ['--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
      '--disable-crash-reporter', `--user-data-dir=${profile}`, url],
  },
  {
    id: 'firefox',
    bin: '/usr/bin/firefox',
    args: (url, profile) => ['-headless', '-no-remote', '-profile', profile, url],
  },
];

const deadlineAt = Date.now() + DEADLINE_MS;
const remaining = () => Math.max(0, deadlineAt - Date.now());
const violations = [];
const posts = new Map();
const runIds = new Map();
const waiters = new Map();
let ORIGIN = null;
let HOST = null;

const withTimeout = async (promise, ms) => {
  let timer;
  try {
    return await Promise.race([promise, new Promise((resolve) => { timer = setTimeout(() => resolve(false), ms); })]);
  } finally {
    clearTimeout(timer);
  }
};

function makeLog() {
  const chunks = []; let bytes = 0; let truncated = false;
  return {
    append(chunk) {
      const room = LOG_CAP - bytes;
      if (chunk.length > room) truncated = true;
      if (room > 0) { const part = chunk.subarray(0, room); chunks.push(part); bytes += part.length; }
    },
    get value() { return Buffer.concat(chunks).toString('utf8') + (truncated ? '…[borné]' : ''); },
  };
}

const cleanEnv = (d) => ({
  PATH: '/usr/bin:/bin',
  LANG: 'C.UTF-8',
  HOME: d.h,
  TMPDIR: d.t,
  XDG_CACHE_HOME: d.c,
  XDG_CONFIG_HOME: d.g,
  XDG_DATA_HOME: d.u,
});

async function makeDirs() {
  const root = await fsp.mkdtemp(path.join(CACHE_ROOT, 'u-'));
  const d = { root, p: path.join(root, 'p'), h: path.join(root, 'h'), t: path.join(root, 't'), c: path.join(root, 'c'), g: path.join(root, 'g'), u: path.join(root, 'u') };
  try {
    for (const x of [d.p, d.h, d.t, d.c, d.g, d.u]) await fsp.mkdir(x, { recursive: true });
    return d;
  } catch (error) {
    await fsp.rm(root, { recursive: true, force: true });
    throw error;
  }
}

function send(res, code, type, body) {
  res.writeHead(code, { 'Content-Type': type, 'Cache-Control': 'no-store' });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    if (Number(req.headers['content-length'] || '0') > MAX_BODY) {
      req.destroy();
      reject(new Error('body_trop_grand'));
      return;
    }
    const chunks = [];
    let size = 0;
    req.on('data', (c) => {
      size += c.length;
      if (size > MAX_BODY) {
        req.destroy();
        reject(new Error('body_trop_grand'));
        return;
      }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

function validateCase(c, i) {
  const e = [];
  if (c === null || typeof c !== 'object' || Array.isArray(c)) return [`cas_${i}_non_objet`];
  if (typeof c.name !== 'string' || c.name.length === 0 || c.name.length > 128) e.push(`nom_${i}_invalide`);
  if (c.status !== 'pass' && c.status !== 'fail') e.push(`statut_${i}_invalide`);
  if (c.status === 'fail' && (typeof c.error !== 'string' || c.error.length > 512)) e.push(`erreur_${i}_invalide`);
  if (c.status === 'pass' && 'error' in c && c.error !== null && c.error !== '') e.push(`erreur_${i}_invalide`);
  return e;
}

function validatePost(body, browserId, runId) {
  const e = [];
  if (body === null || typeof body !== 'object' || Array.isArray(body)) return ['payload_non_objet'];
  if (body.run_id !== runId) e.push('run_id_divergent');
  if (body.browser !== browserId) e.push('browser_divergent');
  if (body.phase !== 'result' && body.phase !== 'init_error') e.push('phase_invalide');
  if (body.phase === 'result') {
    if (!Array.isArray(body.cases) || body.cases.length !== CASE_COUNT) {
      e.push('nombre_cas_invalide');
    } else {
      for (let i = 0; i < CASE_COUNT; i += 1) e.push(...validateCase(body.cases[i], i));
      const names = body.cases.map((c) => (c && typeof c.name === 'string' ? c.name : ''));
      if (new Set(names).size !== CASE_COUNT) e.push('noms_dupliques');
      if (EXPECTED_CASES.length === CASE_COUNT
        && names.slice().sort().join('\u0000') !== EXPECTED_CASES.slice().sort().join('\u0000')) e.push('noms_attendus');
      if (typeof body.ok !== 'boolean' || body.ok !== body.cases.every((c) => c && c.status === 'pass')) e.push('ok_incoherent');
    }
  }
  if (body.phase === 'init_error' && (body.ok !== false || typeof body.error !== 'string' || body.error.length > 512)) e.push('init_error_invalide');
  return e;
}

const server = http.createServer(async (req, res) => {
  try {
    if (req.headers.host !== HOST) {
      violations.push('host_divergent');
      send(res, 400, 'text/plain; charset=utf-8', 'host_divergent');
      return;
    }
    const pathname = decodeURIComponent(new URL(req.url, ORIGIN).pathname);
    if (req.method === 'POST' && pathname === '/result') {
      if (req.headers.origin !== ORIGIN) {
        violations.push('origine_divergente');
        send(res, 403, 'text/plain; charset=utf-8', 'origine_divergente');
        return;
      }
      let raw;
      try {
        raw = await readBody(req);
      } catch {
        violations.push('body_trop_grand');
        send(res, 413, 'application/json; charset=utf-8', '{"error":"body_trop_grand"}');
        return;
      }
      let body = null;
      try {
        body = JSON.parse(raw.toString('utf8'));
      } catch {
        violations.push('json_corrompu');
        send(res, 400, 'application/json; charset=utf-8', '{"error":"json_corrompu"}');
        return;
      }
      const bid = body !== null && typeof body === 'object' ? body.browser : null;
      if (!runIds.has(bid) || remaining() === 0) {
        violations.push('browser_inconnu');
        send(res, 404, 'application/json; charset=utf-8', '{"error":"browser_inconnu"}');
        return;
      }
      if (posts.has(bid)) {
        violations.push(`duplicata_ou_tardif_${bid}`);
        send(res, 409, 'application/json; charset=utf-8', '{"error":"duplicata_ou_tardif"}');
        return;
      }
      const errors = validatePost(body, bid, runIds.get(bid));
      if (errors.length > 0) {
        violations.push(...errors.map((x) => `${x}:${bid}`));
        send(res, 400, 'application/json; charset=utf-8', `{"errors":${JSON.stringify(errors)}}`);
        return;
      }
      posts.set(bid, body);
      if (body.phase === 'init_error') violations.push(`init_recu_${bid}`);
      const wake = waiters.get(bid);
      if (wake) wake();
      send(res, 200, 'application/json; charset=utf-8', '{"status":"accepted"}');
      return;
    }
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      send(res, 405, 'text/plain; charset=utf-8', 'methode_interdite');
      return;
    }
    const route = ROUTES.get(pathname);
    if (!route) {
      send(res, 404, 'text/plain; charset=utf-8', 'non_autorise');
      return;
    }
    const data = await fsp.readFile(route[0]);
    res.writeHead(200, { 'Content-Type': route[1], 'Cache-Control': 'no-store' });
    res.end(req.method === 'HEAD' ? undefined : data);
  } catch (err) {
    violations.push(`serveur_${String(err && err.message).slice(0, 150)}`);
    if (!res.headersSent) send(res, 500, 'text/plain; charset=utf-8', 'erreur');
    else res.destroy();
  }
});

server.on('error', (error) => { violations.push(`http_${String(error.message).slice(0, 150)}`); });

function waitBrowser(id, procClosed) {
  return new Promise((resolve) => {
    let done = false;
    const finish = (why) => {
      if (done) return;
      done = true;
      clearTimeout(timer);
      waiters.delete(id);
      resolve(why);
    };
    const timer = setTimeout(() => finish('deadline'), Math.max(1, remaining() - 2 * GRACE_MS - CLOSE_CAP_MS));
    procClosed.then(() => finish('exit'));
    waiters.set(id, () => finish('post'));
  });
}

function killGroup(child, closed) {
  return (async () => {
    if (child.exitCode !== null || child.signalCode !== null) return (await withTimeout(closed, GRACE_MS)) ? 'dej_termine' : 'process_vivant';
    try {
      process.kill(-child.pid, 'SIGTERM');
    } catch (err) {
      if (err.code !== 'ESRCH') { try { child.kill('SIGTERM'); } catch { violations.push(`sigterm_${child.pid}`); } }
    }
    if (await withTimeout(closed, GRACE_MS)) return 'sigterm';
    try {
      process.kill(-child.pid, 'SIGKILL');
    } catch (err) {
      if (err.code !== 'ESRCH') { try { child.kill('SIGKILL'); } catch { violations.push(`sigkill_${child.pid}`); } }
    }
    return (await withTimeout(closed, GRACE_MS)) ? 'sigkill' : 'process_vivant';
  })();
}

async function removeProfile(root) {
  await fsp.rm(root, { recursive: true, force: true });
  try {
    await fsp.access(root);
    return false;
  } catch {
    return true;
  }
}

function startProcess(browser, args, dirs) {
  const child = spawn(browser.bin, args, { env: cleanEnv(dirs), detached: true, stdio: ['ignore', 'pipe', 'pipe'] });
  const stdout = makeLog(); const stderr = makeLog();
  const state = { child, stdout, stderr, isClosed: false, exit: null, error: null };
  state.closed = new Promise((resolve) => {
    child.once('error', (error) => { state.error = String(error.message).slice(0, 150); });
    child.once('exit', (code, signal) => { state.exit = { code, signal }; });
    child.once('close', () => { state.isClosed = true; resolve(true); });
  });
  child.stdout.on('data', (part) => stdout.append(part));
  child.stderr.on('data', (part) => stderr.append(part));
  return state;
}

async function stopProcess(state) {
  if (state.isClosed) return true;
  await killGroup(state.child, state.closed);
  return state.isClosed;
}

async function captureVersion(browser, dirs) {
  const state = startProcess(browser, ['--version'], dirs);
  const completed = await withTimeout(state.closed, Math.max(1, Math.min(VERSION_CAP_MS, remaining())));
  if (!completed) violations.push(`version_deadline_${browser.id}`);
  const closed = await stopProcess(state);
  const text = state.stdout.value.trim().split('\n').find((line) => /Chromium|Firefox/.test(line)) || '';
  return { ok: completed && closed && !state.error && state.exit?.code === 0 && text.length > 0,
    text, failed: state.error, closed };
}

async function runBrowser(browser) {
  const rec = { id: browser.id, bin: browser.bin, version: null, post: null, exit: null,
    stderr: '', killed: 'none', processClosed: false, profileRemoved: false, runId: crypto.randomUUID() };
  let dirs = null; let state = null; let versionClosed = true;
  try {
    dirs = await makeDirs(); runIds.set(browser.id, rec.runId);
    const ver = await captureVersion(browser, dirs); versionClosed = ver.closed; rec.version = ver.text;
    if (!ver.ok) { violations.push(`version_echouee_${browser.id}`); return rec; }
    if (remaining() <= 2 * GRACE_MS + CLOSE_CAP_MS) { violations.push('deadline_avant_demarrage'); return rec; }
    const url = `${ORIGIN}/?run_id=${rec.runId}&browser=${browser.id}`;
    state = startProcess(browser, browser.args(url, dirs.p), dirs);
    const outcome = await waitBrowser(browser.id, state.closed);
    rec.post = posts.get(browser.id) || null;
    if (outcome === 'deadline') violations.push(`deadline_${browser.id}`);
    else if (outcome === 'exit' && !rec.post) violations.push(`process_sorti_sans_post_${browser.id}`);
    if (state.error) violations.push(`process_${browser.id}`);
  } catch (error) {
    violations.push(`browser_${browser.id}_${String(error.message).slice(0, 150)}`);
  } finally {
    runIds.delete(browser.id); waiters.delete(browser.id);
    if (state) { rec.processClosed = await stopProcess(state); rec.exit = state.exit; rec.stderr = state.stderr.value; }
    else rec.processClosed = versionClosed;
    rec.killed = rec.processClosed ? 'closed_observed' : 'process_vivant';
    if (dirs && rec.processClosed) rec.profileRemoved = await removeProfile(dirs.root);
    if (!rec.processClosed || !rec.profileRemoved) violations.push(`nettoyage_incomplet_${browser.id}`);
  }
  return rec;
}

async function listen() {
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => {
      server.removeListener('error', reject);
      resolve();
    });
  });
  ORIGIN = `http://127.0.0.1:${server.address().port}`;
  HOST = `127.0.0.1:${server.address().port}`;
}

async function closeServer() {
  const closing = new Promise((resolve) => server.close(() => resolve(true)));
  if (typeof server.closeIdleConnections === 'function') server.closeIdleConnections();
  if (typeof server.closeAllConnections === 'function') server.closeAllConnections();
  return withTimeout(closing, CLOSE_CAP_MS);
}

function finalize(records, serverClosed, errors) {
  const browsers = {};
  for (const r of records) {
    browsers[r.id] = {
      version: r.version,
      post: r.post,
      exit: r.exit,
      killed: r.killed,
      process_closed: r.processClosed,
      profile_removed: r.profileRemoved,
      stderr: r.stderr,
    };
  }
  const ok = errors.length === 0 && violations.length === 0 && serverClosed
    && records.length === BROWSERS.length
    && records.every((r) => r.post && r.post.phase === 'result' && r.post.ok === true
      && Array.isArray(r.post.cases) && r.post.cases.length === CASE_COUNT
      && r.post.cases.every((c) => c.status === 'pass')
      && r.version && r.processClosed && r.profileRemoved);
  return {
    schema: 'catalog-browser/2',
    ok,
    code: ok ? 0 : 1,
    session_id: SESSION_ID,
    deadline_ms: DEADLINE_MS,
    elapsed_ms: Date.now() + 0 - (deadlineAt - DEADLINE_MS),
    server_closed: serverClosed,
    browsers,
    violations,
    errors,
  };
}


async function prepareReactVendor() {
  const directory = await fsp.mkdtemp(path.join(CACHE_ROOT, 'react-'));
  const entry = path.join(FRONTEND, '__pixs_c11_test_react__.mjs');
  try {
    await buildVendor({
      configFile: false, root: FRONTEND, envDir: false, envPrefix: [], publicDir: false,
      logLevel: 'error',
      define: { 'process.env.NODE_ENV': JSON.stringify('production') },
      plugins: [{
        name: 'pixs-c11-test-react', enforce: 'pre',
        resolveId(id) { return id === entry ? entry : null; },
        load(id) {
          return id === entry
            ? "export {createElement,useState,useRef,useEffect} from 'react'; export {createRoot} from 'react-dom/client'; export {flushSync} from 'react-dom';"
            : null;
        },
      }],
      build: { outDir: directory, emptyOutDir: false, sourcemap: false, minify: false,
        lib: { entry, formats: ['es'], fileName: () => 'react.mjs' } },
    });
    ROUTES.set('/vendor/react.mjs', [path.join(directory, 'react.mjs'), 'text/javascript; charset=utf-8']);
    return directory;
  } catch (error) {
    await fsp.rm(directory, { recursive: true, force: true });
    throw error;
  }
}

async function main() {
  if (process.argv.length !== 2) throw new Error("Unsupported runner arguments");
  const errors = [];
  const records = [];
  let serverClosed = false;
  let vendorDirectory = null;
  let vendorRemoved = false;
  try {
    vendorDirectory = await prepareReactVendor();
    await listen();
    for (const browser of BROWSERS) {
      if (remaining() === 0) {
        violations.push('deadline_avant_demarrage');
        break;
      }
      records.push(await runBrowser(browser));
    }
  } catch (err) {
    errors.push(String(err && err.message).slice(0, 300));
  }
  serverClosed = await closeServer();
  if (!serverClosed) violations.push('serveur_non_ferme');
  if (vendorDirectory !== null && serverClosed && records.every(r => r.processClosed)) {
    try { await fsp.rm(vendorDirectory, { recursive: true, force: true }); vendorRemoved = true; }
    catch (error) { violations.push('nettoyage_vendor_' + String(error.message).slice(0, 150)); }
  } else if (vendorDirectory !== null) violations.push('vendor_conserve_processus_ou_serveur_actif');
  const output = finalize(records, serverClosed, errors);
  output.react_vendor_removed = vendorRemoved;
  process.stdout.write(JSON.stringify(output, null, 2) + '\n');
  process.exitCode = output.code;
}

await main();
