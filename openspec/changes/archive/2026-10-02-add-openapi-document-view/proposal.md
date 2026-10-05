# Document OpenAPI réel servi en HTTP

## Why

La spécification `api` requiert que chaque capacité exposée dispose d'un contrat OpenAPI publié et versionné, majeure dans le chemin. Les plans `ApiContractPlan` (descripteur + référence logique nue, préfixe `/api/v{major}`, évolution déléguée) n'attestent aucune publication réelle : aucun document n'est servi. Il s'agit d'une absence technique implémentable, non d'une incohérence documentaire.

## What Changes

- Fournir `src/pixs/backend/openapi_document_view.py` avec `build_openapi_view(plan, document)` : `plan` `ApiContractPlan` exact validé, `document` `str` JSON exact non vide borné `64KiB` avant parse ; octets préchargés et figés ; aucune URL ni plan ni métier inventé dans la bibliothèque.
- Validation documentaire bornée : UTF-8 invalide/surrogate/clés dupliquées/non-fini/récursion rejetés, diagnostics fixes `from None` ; version format précise `3.1.0` (pas `3.1.x`) ; `info.title`/`info.version` exigés ; `info.version` égale version contrat via plan validé (règle locale du jalon, non obligation OAS globale ; `openapi` = version format, distincte de `info.version` = version document, source officielle `https://spec.openapis.org/oas/v3.1.0.html`) ; `paths` non vide, littéraux ASCII sous préfixe majeur exact avec frontière `/` ; opérations structurées avec `responses` + `description`, types de contenu et schéma inline minimal supportés, anonyme explicite `security: []` ; références externes refusées ; sous-ensemble supporté clairement documenté, sans validation OpenAPI exhaustive ni comportementale.
- `GET` → 200 corps exact préchargé ; `HEAD` → 200 sans corps avec Content-Length identique au GET ; autre méthode → 405 vide avec `Allow: GET, HEAD` ; MIME `application/json; charset=utf-8` et `Cache-Control: no-store`.
- Import module pur (aucun import Django/lecture FS/config/I-O à l'import) ; document public fourni explicitement par caller responsable, aucune détection magique de secrets revendiquée.
- Tous plans/documents/URL/capacités synthétiques en TESTS seuls ; capacité enveloppe existante (`build_success_response`) consistante avec le contrat, sans nouvelle bibliothèque métadonnées probe.
- Intégration vrai Client : `resolve`, checks, PG/socket zéro, public 403 sans handler, 404 sans echo, octets document exacts, cohérence plan majeur/info/chemins TEST déclarés.
- Sources/façades/`frontend/dist` existants immuables (préservés checkpoint) ; aucune installation validateur ni requête réseau.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `api` : premier jalon strict de l'exigence existante « Contrats OpenAPI versionnés par majeure », sous-ensemble service document seul, reprise normative inchangée.

## Impact

Trois nouveaux fichiers code/tests hors artefacts plus un append seul dans `src/pixs/backend/README.md`. Aucune façade/`manage.py`/`frontend/` modifiée, aucun contrat/version/capacité nouveau, aucune URL concrète distribuée, aucun serveur/DB/SQLite, aucun secret, aucun Git, aucun déploiement. Composition P0, readiness/startup/global et production restent non revendiqués.
