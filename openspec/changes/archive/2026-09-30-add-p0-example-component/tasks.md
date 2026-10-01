# Tasks — add-p0-example-component

## 1. Sources et façade

- [x] 1.1 Source TOML provider : `src/pixs/example/component.toml` schéma 1, MODULE `example.hello` 1.0.0, capacité/contrat `example.hello[.contract]` 1.0.0 — preuve : parse/validate OK
- [x] 1.2 Démo pure : `src/pixs/example/demo.py` (`example_texts/provider_text`, `example_scope`, `example_plan`, `example_compose`), APIs publiques réutilisées, ports injectés — preuve : revue + tests wiring
- [x] 1.3 Façade isolée : `src/pixs/example/__init__.py` sans side-effect, sans import production — preuve : import public
- [x] 1.4 README parcours borné : `src/pixs/example/README.md` commandes DEVOPS exactes + limitations — preuve : relecture

## 2. Tests

- [x] 2.1 Tests unitaires wiring : `tests/unit/test_example_component.py` (manifests, résolution déterministe, attestations, TENANT/cross-tenant, ALLOW/DENY, audit, clock/provider, non-mutation) — preuve : suite verte
- [x] 2.2 Tests intégration mémoire : `tests/integration/test_example_composition.py` (`compose` + `plan_filter`, attestations test-only, audit mémoire) — preuve : suite verte
- [x] 2.3 Tests ciblés exécutés : deux commandes DEVOPS exactes unit + intégration — preuve : exits 0
- [x] 2.4 Régressions globales : suites complètes unit + intégration via chemins DEVOPS — preuve : exits 0

## 3. Validations

- [x] 3.1 AST/UTF-8/LF + delta exact + OpenSpec strict via exécutable DEVOPS — preuve : 0 échec
- [x] 3.2 Revue matrice/nondep/nosecrets/périmètre + preuves CAB — preuve : rapport

Limites : backend Django, PostgreSQL, CLI/Developer Kit complet, providers concrets, frontend, persistance, audit durable, dépendances nouvelles, runtime complet et P0 global hors périmètre. Archivage sur mandat distinct après tout prouvé.
