# Design — ExportManifest persistence

## 17 noms canoniques

manifest_version, operation_id, format, mapping_reference, mapping_version, tenant_context_reference, scope_context_reference, consistency_kind, consistency_reference, row_count, size_bytes, sha256, classification_reference, expires_at, object_reference, object_version, complete. Tous 17 explicites, sans default, sans clé additionnelle, sans FK operation, sans Unique operation, sans latest/CAS, sans format public.

## 18 colonnes physiques

PK technique id BigAuto hors17 + 17 colonnes logiques. Types : 13 TEXT scalaires ( manifest_version, operation_id, format, mapping_reference, mapping_version, tenant_context_reference, scope_context_reference null, consistency_kind, consistency_reference, sha256, classification_reference, object_reference, object_version), soit 15 TEXT au total avec les 2 TEXT privés row_count/size_bytes décimal canonique ASCII `0|[1-9][0-9]*` (pas wire format public), 1 _TrustedUtcDateTimeField réutilisé pour expires_at (trusted DB, astimezone utc, naïf/étranger refusé), 1 Boolean exact complete. Pas int64 cap sauf id technique. Capacité str/int stdlib refusée avant I/O sans modifier int global (str pour encoder, int pour décoder, après types exacts et fullmatch décimal privé ASCII ; aucune conversion JSON, aucun réglage global).

## Record

- from_values pur avant ORM : capture_bulk_export_manifest_values puis freeze, aucune I/O.
- _current_values via __dict__ contre deferred ; champ absent = invalide.
- as_values retourne un dict neuf des 17 valeurs logiques ; repository get retourne la capture pure existante gelée 17, sans modèle lazy ni type normatif ajouté.
- full_clean : même exclude ne saute pas logique, validate_unique False et validate_constraints False, pas de query unique.
- save insert-only : args interdits, force_insert True exigé, force_update False, update_fields None, using str runtime non vide, adding True, alias owner explicite, transaction propriétaire active exigée, puis super save insert-only.
- Factory from_values encode les deux compteurs après capture pure ; le constructeur Django conserve son contrat de stockage, sans override. as_values/full_clean/save revalident tous attributs stockés avant effet et refusent les compteurs privés non TEXT, malformés ou hors capacité réelle. Aucun défaut logique.
- complete/hash/versions/références/consistance/classification/expiry = PRECONDITIONS producteur trusted et DONNEES structurelles, pas preuve production/finalisation/READY/READ_RESULT/gouvernance/clock.
- signedURL jamais champ et aucun générateur ; object_reference opaque privé, pas heuristique URL nouvelle.
- Pur Manifest actuel inchangé.

## Repository

- insert/get seuls, join atomic False (rejoint transaction propriétaire, savepoint False).
- insert : from_values pur, vérifie atomic owner, save insert-only alias owner, retourne id technique ; DBError propagée, rollback owner même capture.
- get : valide id int 1..INT64MAX avant query, query par PK seule, None si absent, sinon capture pure existante gelée 17 ; context pas requis pur Manifest (pas de policy/catalogue).
- insert/get ne prouvent pas finalisation/projection/consistance/classification/gouvernance/READ_RESULT/READY ; préconditions producteur explicites.
- Multiple mêmes operation_id : stockage interne seul, sans latest ni unicité publique.

## Migration 0010

- Après 0009 seule, 12 tables préexistantes stables et préservées. CreateModel seul, CHECKs dérivés des types et valeurs déjà validés (noms et nombre à figer après revue du modèle), miroir exact modèle, aucune FK, aucune Unique operation, forward/reverse 0010 seuls.

## Tests

- Gardes réelles offline avant setup (PG connect, socket, subprocess bloqués, compteurs 0).
- PG isolé helpers inchangés job_record_16hex : safe_schema, managed_pg, quote_search_path, table_identity, public preserves 12.
- 18 colonnes/contraintes correspondantes, no unique/fk operation.
- Cas : roundtrip 17, None scope, False complete, UTC min/max et identité timezone.utc, grands int >int64 (2**63+123, 10**600 persistance si capacité disponible ; 10**1000 valide en pur mais refus stockage si limite stdlib640), stdlib capacity refusée, compteurs TEXT malformés (vide, signe, espace, zéro initial, chiffre non ASCII, type étranger), clés/types hostiles et refus capacité réelle, no owner, hydrate refusé, alias autre refusé, prequery refusée avant I/O.
- Observateur indépendant, co-effects co-commit/rollback, vrai CHECK 23514 propagation propriétaire invalide, forward/reverse 0010 cleanup conns.

## Préconditions et limites

Les références opaques ne deviennent pas un nouveau format public ; la couche conserve les valeurs déjà validées. Elle ne vérifie pas qu’une chaîne opaque est un objet finalisé et ne déduit aucune autorisation, disponibilité READY ou gouvernance. Aucun signedURL ne constitue une donnée attendue du producteur. Pas de contrainte de cohérence row_count/size_bytes/complete ajoutée au pur. Toute capacité physique ou erreur SQL inattendue est propagée, sans faux succès.
