# Proposition — Unité de persistance JobRecord pour les travaux

## Why

L'exigence canonique « Persistance et états explicites » (openspec/specs/jobs/spec.md) impose que chaque travail soit persisté avant exécution avec les neuf états nommés, un bail persistant et une politique de réessai bornée. Le backend ne dispose d'aucune table de travaux : seul le modèle des fanions est persisté. Cette unité ajoute seule le modèle Django `JobRecord` borné à la persistance, sans worker, sans transition, sans politique de bail ou de réessai, et sans prétendre au contrat `Job` complet de TECHNICAL.md §23.

## What Changes

- Éditer `src/pixs/backend/models.py` : ajouter `JobRecord` à treize champs bornés (job_id, job_type, job_version, payload, subject, tenant_context, correlation_id, causation_id, perimeter_reference, state, attempt_count, lease_owner, lease_expires_at), le wrapper `_validate_job_version` branché aux validators du champ, et les CheckConstraints d'intégrité ; `__all__` étendu à `["FeatureFlagSourceSnapshotRecord", "JobRecord"]` ; classe `FeatureFlagSourceSnapshotRecord` préservée octet pour octet ;
- Ajouter `src/pixs/backend/migrations/0002_job_record.py` : `CreateModel` réversible dépendant de `("backend", "0001_feature_flag_source_snapshot")`, PK `TextField(primary_key=True, serialize=False)` (convention Django pour PK non auto) ;
- Ajouter `tests/unit/test_job_record.py` (offline, cas ciblés, zéro connexion) et `tests/integration/test_job_record_postgres_integration.py` (PostgreSQL réel, schéma d'essai unique) ;
- Adapter uniquement l'assertion d'inventaire de `tests/integration/test_feature_flag_postgres_source_integration.py` pour les deux modèles désormais présents, en conservant tous les contrôles des fanions ;
- Delta `specs/jobs/spec.md` MODIFIED reproduisant mot pour mot l'exigence canonique « Persistance et états explicites » et son scénario, sans exigence nouvelle ni règle normative.

## Impacts

- `settings.py`, `apps.py`, la migration 0001 et le modèle des fanions inchangés ; `pixs.backend` n'est installé que par les harnais de test (label `backend`), sans activation de configuration production ;
- `state` sans défaut : fourni explicitement ; `attempt_count` défaut 0 ; références opaques sans FK ni preuve d'existence ; `payload`/`subject`/`tenant_context` JSONField opaques (`null=False` SQL, `blank=True` pour `full_clean`, conteneurs vides tolérés sans choix de forme) ; leases facultatifs `null=True`/`blank=True` sans sémantique ;
- `save()` n'appelle pas `full_clean` ; les contraintes DB ne prouvent pas SemVer, validé seulement par le chemin `full_clean`/`clean_fields` via `_validate_job_version` réutilisant `pixs.kernel.manifest.semver.parse_version` (ValueError converti en ValidationError à message fixe sans écho) ;
- Effet canonique effectif attendu nul (+0/~0/-0/→0) ; les exigences « Autorisation réévaluée à l'exécution » et « Idempotence et corrélation des travaux » et le scénario « Reprise après interruption » restent non couverts : aucune exécution, reprise, bail actif, réessai ni déduplication ne sont implémentés.
