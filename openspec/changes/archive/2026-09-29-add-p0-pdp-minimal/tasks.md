# Tasks — add-p0-pdp-minimal

## 1. Modèles, catalogue et limites

- [x] 1.1 Créer `src/pixs/core/authz/policy.py` : Effect, Selector, ScopeSelector, Condition eq/in typés, Obligation AUDIT, Policy avec seuils assurance séparés et fenêtres, rejets avant activation — preuve : tests policy
- [x] 1.2 Créer `src/pixs/core/authz/snapshot.py` : Catalog complet, Limits stricts, factory build_snapshot bornes avant normalisation, triés, duplicata policy_id refusé — preuve : tests policy et temps
- [x] 1.3 Créer `src/pixs/core/authz/ports.py` : Request sans auth, AuthenticationContext §4.1, TrustedFacts, provider backend seul, Clock UTC unique, AuditSink strict — preuve : tests décision et audit

## 2. Évaluation et façade

- [x] 2.1 Créer `src/pixs/core/authz/decision.py` : authorize recalculé chaque appel, appariement strict, DENY>ALLOW>défaut, fait requis inconnu refusé sur candidate pertinente DENY ou ALLOW, assurances §4.1, expires min bornes et DENY futur, audit refus, échec jamais ALLOW — preuve : tests décision, temps et audit
- [x] 2.2 Créer `src/pixs/core/authz/__init__.py` : façade bornée des cinq sources — preuve : import public

## 3. Tests

- [x] 3.1 `tests/unit/test_pdp_policy.py` : construction, normalisation, wildcard/obligation inconnue/doublons/bornes refusés
- [x] 3.2 `tests/unit/test_pdp_decision.py` : appariement, priorité, bool/int, opérateur inconnu, absence conservant DENY, périmètres, assurances non substituables, snapshots invalides refusés
- [x] 3.3 `tests/unit/test_pdp_time.py` : UTC, TTL, fraîcheur, transitions futures, fuseaux, échéance exacte, renouvellement facts et snapshot entre deux appels, déterminisme et non-mutation
- [x] 3.4 `tests/integration/test_pdp_audit.py` : refus audités une fois, callback False et exception jamais ALLOW, plateforme explicite, cross-tenant refusé, doubles sans persistance

## 4. Validations

- [x] 4.1 Suites unit et intégration complètes via chemins DEVOPS — preuve : exits 0
- [x] 4.2 AST mémoire, UTF-8 et LF des sources et tests — preuve : contrôle ciblé
- [x] 4.3 OpenSpec strict via exécutable DEVOPS — preuve : 0 échec
- [x] 4.4 Revue code, specs, cadrages et hors périmètre — preuve : rapport

Limites : persistance, PEP, PostgreSQL et audit durable hors périmètre. Archivage et statistiques par mandats distincts ultérieurs.

## Preuves de validation

- 1.1–3.4 : cinq sources et quatre fichiers de tests relus ; 53 tests PDP unitaires et 10 tests PDP d'intégration mémoire inclus dans les suites complètes.
- 4.1 : 281 tests unitaires, exit 0 (`msg_0ee3beaea001czNs46J3NmnpgH`) ; 96 tests d'intégration, exit 0 (`msg_0ee39d289001fgqoFmAmAH7nKQ`).
- 4.2 : AST des neuf fichiers Python et UTF-8/LF des treize fichiers du change, exit 0 (`msg_0ee3d83ca001at9xHC5T7g96Vx`).
- 4.3 : OpenSpec strict, 77 éléments valides, zéro échec, exit 0 (`msg_0ee3ec6bd001vLtuQPf5kC37BE`).
- 4.4 : revue CGPT des sources et tests, du design, de `authorization-engine`, `TECHNICAL §4.1/12`, `PROJECT §2.31/2.32`, README, BUILD et DEVOPS. Les écritures observées de cette session sont limitées aux treize fichiers autorisés. Aucun Git, nouveau fournisseur, dépendance, build Debian/Docker ou accès de production exécuté.

Les refus d'accès sont testés sur un port d'audit mémoire. Un échec du port conserve DENY sans garantir une persistance ; un ALLOW demeure soumis aux obligations du PEP futur. Les réécritures intermédiaires incomplètes et les deux exécutions policy en échec ont été corrigées avant ces validations ; aucun achèvement intermédiaire n'a été coché.
