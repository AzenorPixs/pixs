## MODIFIED Requirements

### Requirement: Déclaration lisible des fournisseurs

Chaque fournisseur MUST déclarer par manifest lisible les contrats qu'il implémente, leurs versions, ses capacités et ses contraintes ; une implémentation non déclarée MUST NOT pouvoir être sélectionnée.

#### Scenario: Implémentation non déclarée

- **WHEN** une implémentation existe sans déclaration de contrat
- **THEN** elle ne peut être sélectionnée par aucune composition et reste inactive

### Requirement: Sélection explicite sans choix implicite

La sélection d'un fournisseur MUST suivre le fournisseur configuré, sinon le candidat compatible unique, sinon refuser la composition ; la sélection MUST NOT dépendre de l'ordre de découverte.

#### Scenario: Deux candidats sans configuration

- **WHEN** deux fournisseurs compatibles satisfont le même contrat sans fournisseur configuré
- **THEN** la composition est refusée avec un diagnostic d'ambiguïté explicite

### Requirement: Conformité contractuelle vérifiable

Un fournisseur MUST satisfaire le contrat déclaré à sa version revendiquée ; toute violation constatée MUST entraîner l'isolement du fournisseur et un échec fermé des appels concernés.

#### Scenario: Fournisseur non conforme activé

- **WHEN** un fournisseur échoue à une vérification de conformité de son contrat
- **THEN** il est retiré de la sélection et les appels correspondants échouent avec un code d'erreur stable

### Requirement: Dégradation contrôlée et diagnostic

Le système MUST offrir un mode dégradé explicite quand un fournisseur devient indisponible, avec diagnostic utile, sans exposer de secret ni masquer l'échec.

#### Scenario: Indisponibilité d'un fournisseur

- **WHEN** le fournisseur sélectionné devient injoignable
- **THEN** la capacité est déclarée dégradée, l'état est diagnostiquable et l'incident est tracé sans fuite d'information sensible
