# data-lifecycle

## MODIFIED Requirements

### Requirement: Dimensions et états distincts

Les dimensions métier, persistance (ACTIVE, ARCHIVED, SOFT_DELETED, PURGE_PENDING), rétention et projection MUST NOT être confondues ; la suppression logique est la stratégie par défaut des ressources métier.

#### Scenario: Suppression logique tracée

- **WHEN** une ressource métier est supprimée
- **THEN** elle passe en SOFT_DELETED avec métadonnées de cycle de vie, sans purge physique
