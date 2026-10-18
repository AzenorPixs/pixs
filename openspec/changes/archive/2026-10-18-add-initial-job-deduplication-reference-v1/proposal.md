# Proposition — Référence préparatoire de déduplication des Jobs

## Why

La RSMP validée définit le profil structurel `JobDeduplicationReferenceV1`. Sa représentation et sa validation restent à fournir. Ce change livre ce seul profil préparatoire, sans déduplication persistante.

## What Changes

- Ajouter un profil immuable à deux références opaques et son validateur fermé.
- Ajouter des tests unitaires et une intégration en processus frais sous gardes d'effets.
- Reproduire exactement les trois exigences canoniques validées dans le delta jobs.

## Capabilities

### Modified Capabilities

- `jobs` : implémenter le profil structurel et ses limites déjà adoptés par la RSMP.

## Impact

Trois nouveaux fichiers Python : `src/pixs/kernel/job_deduplication_reference.py`, `tests/unit/test_job_deduplication_reference.py` et `tests/integration/test_job_deduplication_reference_integration.py`. Réutilisation des diagnostics existants et de la bibliothèque standard, Python >=3.12. Aucun runtime, stockage, rétention, unicité, migration, provider, dépendance ni opération Git. Archivage avec `--skip-specs` puisque le canon est adopté par la RSMP préalable ; rapport STATISTIQUES.md distinct obligatoire.
