## Why
Le canon Bulk v1 et ses validateurs mémoire sont livrés. Les données d'exécution, checkpoints, liaisons Jobs et scheduling ne sont pas encore persistés avec CAS et baux.

## What Changes
- Ajouter quatre modèles runtime et une migration 0004, sans modifier les profils préparatoires Record et JobRecord.
- Ajouter des primitives transactionnelles PostgreSQL pour révisions, transitions, checkpoints et baux.
- Prouver concurrence, rollback, reprise et nettoyage dans un schéma de test isolé.

## Capabilities
### New Capabilities
Aucune.

### Modified Capabilities
- bulk-operations : couverture persistante de B02/B06/B13 déjà normatifs.
- jobs : liaisons et baux B08/B09 déjà normatifs.

## Impact
Six fichiers Python proposés, dont une seule registration minimale dans models.py. Aucun HTTP, provider concret, admission complète, parsing, worker, outbox, PA/PZT, dépendance ou déploiement.
