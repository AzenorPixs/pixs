# identity-assurance Specification

## Purpose
L'assurance normalise la force de l'identification, de l'authentification et de la confiance fédérée, et conditionne les opérations sensibles avec élévation explicite.

## Requirements

### Requirement: Contexte vérifié et dimensions distinctes

Toute authentification réussie produit un contexte vérifié, limité dans le temps, rattaché à une identité numérique et au périmètre applicable, avec assurance d'identité, assurance d'authentification et confiance fédérée évaluées séparément selon le mapping déclaré du fournisseur.

#### Scenario: Claim absent sans surclassement

- **WHEN** une preuve ou un claim est absent, ambigu ou expiré
- **THEN** le niveau d'assurance n'est jamais augmenté implicitement

### Requirement: Seuil sensible et élévation explicite

Toute opération sensible exige le niveau requis, au minimum l'authentification multifacteur le cas échéant ; à défaut, l'opération est refusée ou soumise à une élévation explicite que le frontal NE DOIT pas simuler.

#### Scenario: Élévation exigée

- **WHEN** une action sensible est demandée avec une assurance insuffisante
- **THEN** le système refuse ou déclenche une élévation explicite auditée

### Requirement: Fraîcheur, révocation et récupération sans élévation implicite

Expiration, fraîcheur maximale, rotation et révocation sont vérifiées avant toute décision sensible ; une récupération invalide les sessions concernées sans restaurer implicitement un niveau élevé.

#### Scenario: Récupération sans restauration d'assurance

- **WHEN** un compte est récupéré après compromission
- **THEN** les niveaux élevés restent perdus jusqu'à nouvelle preuve ou intervention autorisée
