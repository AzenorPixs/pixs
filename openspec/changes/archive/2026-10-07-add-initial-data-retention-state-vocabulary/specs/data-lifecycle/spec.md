# data-lifecycle

## MODIFIED Requirements

### Requirement: Dimensions et états distincts

Les dimensions métier, persistance (ACTIVE, ARCHIVED, SOFT_DELETED, PURGE_PENDING), rétention (RETAINED, LEGAL_HOLD, ELIGIBLE_FOR_PURGE) et projection MUST NOT être confondues ; la suppression logique est la stratégie par défaut des ressources métier.

#### Scenario: Suppression logique tracée

- **WHEN** une ressource métier est supprimée
- **THEN** elle passe en SOFT_DELETED avec métadonnées de cycle de vie, sans purge physique

#### Scenario: Vocabulaire commun de rétention fermé

- **WHEN** un consommateur utilise le vocabulaire commun de la dimension rétention d'une donnée
- **THEN** les valeurs communes sont exactement RETAINED, LEGAL_HOLD et ELIGIBLE_FOR_PURGE, sans défaut, transition, calcul d'éligibilité ni politique ajoutés par ce vocabulaire
- **AND** aucun de ces états ne vaut à lui seul autorisation de purge

