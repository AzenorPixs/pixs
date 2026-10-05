# Proposal: add-initial-health-classifier

## Why

L'exigence « Santé distinguée et sondes bornées » de la capacité `observability` exige des contrôles qui distinguent vivacité, disponibilité, démarrage et diagnostic. Le backend expose une vue de vivacité isolée et des contrôles préparatoires purs (`checks.py`), mais aucun classificateur de snapshots santé n'existe : absence prouvée par lecture native et recherche ciblée dans `src/pixs`.

## What Changes

Ajout d'un classificateur pur de snapshots santé fournis par le caller, avec l'API interne exacte :

- `classify_health(*, alive, startup_complete, pg_available, required=(), optional=())` ; noms anglais pour les nouveaux paramètres conformément à `AGENTS.md` section 14.
- `pg_available` reste un opérande OBLIGATOIRE de la disponibilité ; il n'est jamais classé optionnel.
- Quatre types de contrôles séparés : vivacité = `alive` seul, indépendante de PG ; démarrage = `startup_complete` du snapshot ; disponibilité = vivacité ET démarrage ET `pg_available` ET tous `required` vrais ; diagnostic = booléens, comptes et primitives fixes uniquement.
- `degraded` signale indépendamment les seuls `optional` en échec ; `availability` demeure explicitement `false` quand une dépendance obligatoire, le démarrage ou la vivacité échoue ; aucun statut global `DEGRADED` ne masque la panne.
- Limite interne de 256 booléens par tuple, constante privée garde interne sans configuration ni norme publique ; refus `ValueError("Invalid health snapshot") from None`, sans valeur brute.
- Déterminisme total : aucun IO, aucun import Django, aucune fonction ou callback de sonde, aucun retest PG, aucun paramètre d'environnement ou de configuration, aucune route.

Le helper `src/pixs/backend/health_classifier.py`, deux suites de tests nouvelles ciblées sur l'exécutable Python déclaré dans `DEVOPS.md` et un append unique de `src/pixs/backend/README.md` accompagnent ce change.

## Impact

- Affected specs: `observability`
- Affected code:
  - `src/pixs/backend/health_classifier.py` (création)
  - `tests/unit/test_health_classifier.py` (création)
  - `tests/integration/test_health_classifier_integration.py` (création)
  - `src/pixs/backend/README.md` (append seul)

Aucun comportement existant n'est modifié : les suites historiques 612/180 ne sont pas rejouées, les anciens codes et archives restent préservés, la sonde PG archivée reste inchangée. Aucune prétention de P0, readiness, disponibilité globale, serveur, Git, installation ou mutation PG.
