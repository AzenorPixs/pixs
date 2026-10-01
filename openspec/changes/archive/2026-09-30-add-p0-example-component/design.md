# Design — add-p0-example-component

## 1. Architecture isolée

- `src/pixs/example/` est un MODULE démonstratif synthétique, jamais importé par `pixs.core` ni `pixs.kernel`, sans effet à l'import ni auto-activation. Namespace `example.*` uniquement (jamais `pixs.*`, jamais contrat de production). Fixture `example.hello.contract 1.0.0` démonstrative.
- `component.toml` (schéma 1) est la source unique du provider ; `demo.py` ne contient aucune seconde copie inline et ne lit rien à l'import. `example_texts(provider_text: str) -> tuple[str, str]` reçoit le TOML provider explicitement chargé par l'appelant/test et retourne `(provider_text, consumer_text)`, le consommateur étant une constante namespace `example.client` dépendant de `example.hello.contract ==1.0.0`.
- `example_scope() -> tuple[ScopeContext, TopologySnapshot]` fournit la fixture immuable synthétique (TENANT `t1`, topologie `("t1",)`) ; l'exemple ne fabrique ni faits de confiance, ni politiques, ni audit : snapshot, provider, horloge et audit sont injectés par l'appelant/test.
- `example_plan(snapshot, provider, clock, audit, topology, config, context: ScopeContext) -> FilterPlan` construit ses demandes avec ce même `context` explicite (au lieu de figer `t1`) ; les validateurs existants garantissent contexte/topologie/cross-tenant. Refus politique normal DENY exclut la ressource (plan possiblement vide) ; inconnue/malformée/cross-tenant/audit-échoué → `FilterPlanError`, sans confusion.
- `example_compose(texts, attestations=()) -> CompositionResult` consomme UNIQUEMENT les attestations données par l'appelant et n'en fabrique JAMAIS. Doubles `PASS` (`synthetic_attestations`) cantonnés aux tests et explicitement non preuves de conformité réelle.

## 2. Séparation et réutilisation

- Validation/résolution : `parse_manifest_text`, `discover/validate/resolve/compose`, `SemVer`, `guards`, diagnostics typés. PDP : `build_snapshot/validate_snapshot`, `authorize`, `plan_filter` + ports (`Request/AuthenticationContext/TrustedFactsProvider/Clock/AuditSink`) + policy (`Catalog/Limits/Effect/Selector/ScopeSelector/Condition/Obligation/Policy`). Scope : `ScopeContext/ScopeType/validate_structure`, `TopologySnapshot/validate_context`, `ResourceOwnership`. Aucune logique noyau/core copiée.
- Intégration mémoire distincte de toute référence : `compose()` + `plan_filter()` sur doubles, audit mémoire, sans persistance/DB/réseau/frontend.

## 3. Tests utiles et documentation

- Unitaires (wiring démonstratif seul) : manifests fournisseur/consommateur, résolution versionnée déterministe (ordre/edges), attestations absentes refusent, synthétiques explicitement doubles, contexte TENANT propagé/cross-tenant refusé, ALLOW/DENY prioritaire, audit refusant, horloge/provider injectés, non-mutation, import sans side-effect. NE PAS recopier la matrice filter_plan (coût, bool/révocation, canon-freeze déjà prouvés ; régressions globales couvriront).
- Intégration (mémoire, distincte référence) : `compose()` + `plan_filter()` via doubles, attestations test-only, audit mémoire. Commandes exactes DEVOPS : `/usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/unit -p test_example_component.py -v` et `/usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/integration -p test_example_composition.py -v`.
- `README.md` : parcours reproductible via validateurs existants avec ces deux commandes exactes et limitations explicites (pas de P0 global, pas de Developer Kit complet, pas de backend réel).
- Cohérence ciblée AGENTS/PROJECT/TECHNICAL/BUILD/DEVOPS/README/specs/testing : états inchangés, aucune garantie globale.
