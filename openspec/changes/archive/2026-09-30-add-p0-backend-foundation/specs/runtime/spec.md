## MODIFIED Requirements

### Requirement: Profils distincts d'un même artefact

Les rôles web, worker et scheduler MUST être des profils d'un même artefact activés par configuration explicite, sans branche fonctionnelle cachée ; le développement peut les regrouper, la production MUST pouvoir les exécuter séparément.

#### Scenario: Profil activé par configuration

- **WHEN** un déploiement produit un worker et un scheduler à partir du même artefact
- **THEN** leurs capacités et limites respectives sont inspectables sans code divergent
