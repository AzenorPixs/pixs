# feature-flags — Delta

## MODIFIED Requirements

### Requirement: Ciblage et cohorte déterministes

Le système MUST respecter les garanties suivantes.

L'évaluation utilise uniquement les dimensions déclarées (installation, environnement, tenant, scope enfant) avec priorité du général au spécifique et cohorte stable sans tirage par requête.

#### Scenario: Même contexte même décision

- **WHEN** le même contexte est évalué deux fois
- **THEN** le résultat est identique
