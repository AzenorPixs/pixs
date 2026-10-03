# Conception du service de document OpenAPI

## Context

`ApiContractPlan` + `api_major_prefix` + enveloppes existent et testés ; aucun document servi. `servers` absent vaut défaut `/` ; `security: []` retire l'authentification (source officielle OAS 3.1.0). La garde accepte les littéraux avec points ; `liveness`/`shell` montrent le gabarit fabrique pure + Client réel.

## Goals / Non-Goals

But : servir réellement un document 3.1.0 borné et le prouver. Non-buts : aucune URL distribuée, aucune génération OpenAPI, aucune validation exhaustive/comportementale, aucune coexistence réelle, aucune composition P0, aucun readiness/startup, aucune PG/secrets/dépendance nouvelle.

## Decisions

- Signature `build_openapi_view(plan, document)` : `plan` doit être revalidé par l’API publique `api_major_prefix` existante (type exact, catégorie API, ref nue), sans importer de helper privé ; `document` exact `str` non vide, `longueur de caractères puis d’octets UTF-8 <= 65536` avant parse, sinon erreur fixe.
- Parse : `json.loads` avec refus UTF-8 invalide/surrogate (encode strict), `parse_constant` rejetant non-fini, parcours récursif borné rejetant aussi float débordé (1e999) et surrogate décodé (y compris clés), `object_pairs_hook` rejetant clés dupliquées, limite récursion ; toute anomalie → `OpenapiDocumentError("Invalid OpenAPI document.")` fixe `from None`, sans echo.
- Forme : `openapi == "3.1.0"` exact ; `info` dict avec `title`/`version` `str` exacts non blancs ; `info.version` == version contrat du plan (règle locale jalon) ; `paths` dict non vide ; chaque chemin littéral ASCII commençant par préfixe majeur exact + frontière `/` (au moins un segment après préfixe) ; chaque opération valeur structurée avec `responses` dict non vide dont chaque réponse a `description` `str` ; `content` optionnel limité aux types déclarés avec schéma inline minimal (types JSON exacts finis et schémas inline structurés ; aucune `$ref` acceptée dans ce sous-ensemble inline) ; `servers` absent seulement dans ce sous-ensemble (défaut `/`) ; `security: []` anonyme explicite.
- Construction : octets UTF-8 figés une fois ; handlers ferment sur octets + MIME ; `GET` 200 exact, `HEAD` 200 vide + Content-Length GET, autres 405 vide + `Allow` ; `Cache-Control: no-store` partout.
- En TESTS seuls : plan synthétique (descripteur API `1.0.0`, ref nue), document 3.1.0 minimal cohérent, déclarations garde (`api/v1/openapi.json` et capacité synthétique de document PUBLIC, témoin private 403, inconnues/autre majeure 404) ; `resolve`+Client réels : lire le document et appeler réellement sa capacité synthétique via `build_success_response`, vérifier enveloppe cohérente avec le schéma inline et version/chemins ; `run_checks(databases=[])`, gardes `psycopg`/socket zéro, settings `ENGINE` seul.
- Diagnostics tous fixes `from None`, sans `repr`/comparaison hostile ; identifiants nouveaux anglais.

## Files

`src/pixs/backend/openapi_document_view.py`, `tests/unit/test_openapi_document_view.py`, `tests/integration/test_openapi_document_view_integration.py`, append seul `src/pixs/backend/README.md`.

## Validation

OpenSpec strict avant/après ; unit sous-processus isolés (import pur, hostiles, bornes, incohérences) ; intégration Django synthétique frais, aucun secret ni engine SQLite, `django.setup()`, Client réel, gardes zéro, UTF-8/LF, périmètre strict.

## Risks / Trade-offs

Aucune route utilisable en production issue de ce jalon. Le sous-ensemble documenté ne remplace pas un validateur exhaustif ; toute mise en service de production exigera un change distinct.
