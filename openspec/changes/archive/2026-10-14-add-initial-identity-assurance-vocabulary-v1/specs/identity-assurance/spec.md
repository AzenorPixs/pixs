## MODIFIED Requirements

### Requirement: Vocabulaire structurel préparatoire IdentityAssurance v1

Le vocabulaire structurel préparatoire IdentityAssurance v1 MUST admettre exactement CLAIMED, VERIFIED et PROOFED. Toute autre valeur MUST être refusée. Sa représentation MUST NOT fournir de valeur par défaut, de classement ordinal, de mapping fournisseur ou de transition. Elle MUST NOT établir une preuve, calculer ou augmenter une assurance, authentifier, créer une session, accorder un accès, produire un audit ou persister une donnée. Les garanties existantes de séparation des dimensions et de non-surclassement MUST rester applicables.

#### Scenario: Valeurs fermées sans effet

- **WHEN** Une des valeurs CLAIMED, VERIFIED ou PROOFED est représentée
- **THEN** Seul ce vocabulaire structurel est produit, sans preuve, droit, session, audit ni persistance

#### Scenario: Valeur étrangère refusée

- **WHEN** Une valeur étrangère au vocabulaire est présentée
- **THEN** La représentation est refusée sans augmentation implicite du niveau

#### Scenario: Absence sans défaut implicite

- **WHEN** Aucune valeur n’est fournie
- **THEN** Le profil ne choisit aucun niveau par défaut
