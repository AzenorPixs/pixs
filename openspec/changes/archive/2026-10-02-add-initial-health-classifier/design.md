# Conception classificateur sante pur

## Context
Vue liveness existante, `checks.py` preparatoire sans classificateur, aucun module equivalent dans `src/pixs` (grep source cible). Django 5.2.17 non installe dans le runtime actuel declare. Ancien `.venv` historique non rerun. Sonde PG `add-pg-connectivity-probe` archivee, inchangee, non retestee.

## Goals / Non-Goals
But : classifier des snapshots sante fournis par le caller en quatre types de controles separes, pur, deterministe, sans IO ni import Django ni execution de sonde. Non-buts : disponibilite globale, P0, readiness, serveur, route, retest PG, nouveaux delais, parametre CFG/env, contrat public, norme ajoutee.

## Decisions
- API interne exacte et unique : `classify_health(*, alive, startup_complete, pg_available, required=(), optional=())` ; noms anglais pour les nouveaux parametres conformement a `AGENTS.md` section 14 ; mot-cle-only obligatoire.
- Types exacts verifies avant toute longueur ou iteration : `alive`, `startup_complete`, `pg_available` doivent etre `bool` exacts (pas d'entier ni objet verique) ; `required` et `optional` doivent etre des `tuple` exacts. Les longueurs des deux tuples sont verifiees avant toute inspection des elements ; chaque element doit etre un `bool` exact.
- Limite interne : au plus 256 booleens par tuple, constante privee garde interne du module ; sans configuration, sans variable d'environnement, sans norme publique ni seuil universel invente.
- Quatre types de controles separes : vivacite = `alive` seul, independante de PG ; demarrage = `startup_complete` ; disponibilite = `alive` ET `startup_complete` ET `pg_available` ET tous `required` vrais ; diagnostic = booleens et comptes uniquement.
- PG opérande toujours OBLIGATOIRE de disponibilite : `required_count` = `1 + len(required)` et `required_ok_count` = `int(pg_available) + sum(required)` incluent PG. `optional_count` et `optional_ok_count` couvrent les autres optionnels seulement.
- `degraded` signale independamment les seuls `optional` en echec ; `availability` demeure explicitement `false` quand une obligatoire, le demarrage ou la vivacite echoue ; aucun statut global `DEGRADED` ne masque la panne.
- Determinisme : meme entree, meme sortie ; aucun IO, aucun import Django, aucune fonction ou callback de sonde, aucun etat global, aucun secret, aucune valeur brute.
- Refus fixe unique : `ValueError("Invalid health snapshot") from None` sur toute entree invalide, sans valeur brute ni nom de champ ; `from None` masque la chaine de contexte, sans supprimer la pile Python.

### Schema de sortie interne
Neuf champs fixes par appel, primitives fixes uniquement, rendus dans un `dict` simple : les comptes constituent le diagnostic ; aucune chaine `DEGRADED` publique n'est ajoutee. Neuf signifie neuf champs ; chaque appel produit un dict nouveau et independant, sans pretention d'immutabilite ni objet partage :
- `"liveness"` : bool, image exacte de `alive`.
- `"startup"` : bool, image exacte de `startup_complete`.
- `"availability"` : bool, conjonction vivacite, demarrage, `pg_available` et tous `required`.
- `"degraded"` : bool, vrai uniquement si au moins un `optional` est faux.
- `"pg_available"` : bool, image exacte de `pg_available`.
- `"required_count"` : int, `1 + len(required)`, incluant PG.
- `"required_ok_count"` : int, `int(pg_available) + sum(required)`, incluant PG.
- `"optional_count"` : int, `len(optional)`, autres optionnels seulement.
- `"optional_ok_count"` : int, `sum(optional)`, autres optionnels seulement.

## Files
`src/pixs/backend/health_classifier.py` ; `tests/unit/test_health_classifier.py` ; `tests/integration/test_health_classifier_integration.py` ; append seul `src/pixs/backend/README.md`.

## Validation
Strict OpenSpec avant code puis apres preuves ; tests nouveaux cibles sur l'executable Python declare dans `DEVOPS.md` (runtime actuel) ; matrices quatre types, PG obligatoire, optionnels, combos startup/alive ; types et `repr` hostile jamais appeles. Les cas grands tuples (longueur 257) et objets hostiles prouvent les refus sans hooks etrangers ; l'ordre des gardes est confirme par lecture AST/code ou par un espion de type comptant les inspections, car le simple objet hostile ne prouve pas a lui seul l'absence de `type(x)` prealable. Subprocess frais avec gardes IO/sockets/connexion SQL et sans import Django necessaire ; aucune assertion de temps fragile. Comptages baseline construits exactement par CGPT avant toute assertion, aucun compte invente ; anciens tests 612/180 historiques non rerun, anciens codes et archives preserves.
