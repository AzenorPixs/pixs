## MODIFIED Requirements

### Requirement: Syntaxe lexicale préparatoire FrontendContributionId v1

Le profil lexical préparatoire FrontendContributionId v1 MUST accepter uniquement une chaîne comportant au moins deux segments non vides séparés par un point ASCII. Chaque segment MUST contenir uniquement les lettres ASCII A–Z et a–z, les chiffres 0–9, le tiret et le soulignement. Toute autre valeur ou tout autre type MUST être refusé.

#### Scenario: Identifiant namespacé reconnu lexicalement

- **WHEN** l'entrée est `acme.crm.contacts` ou `ACME.crm-2.contacts_1`
- **THEN** elle est reconnue dans le seul profil lexical v1 et conservée à l'identique

#### Scenario: Forme hors profil refusée

- **WHEN** l'entrée n'est pas une chaîne, contient moins de deux segments, un segment vide, un espace, un caractère non ASCII ou un caractère hors alphabet autorisé
- **THEN** elle est refusée sans correction, décodage ni changement de casse

### Requirement: Limites du contrôle lexical FrontendContributionId v1

Le contrôle FrontendContributionId v1 MUST conserver l'entrée à l'identique, sans suppression d'espace, normalisation, décodage ou changement de casse. Il MUST rester lexical, sans accès au système de fichiers. Il MUST NOT prouver propriété, provenance, confiance, droit sur `pixs.*` ou unicité, ni définir un champ de manifest, enregistrer, composer, router, charger ou activer une contribution. Les règles générales de namespace réservé et de composition restent applicables.

#### Scenario: Résultat lexical sans effet ni preuve de propriété

- **WHEN** le contrôle v1 accepte un identifiant, y compris un identifiant de forme `pixs.contacts`
- **THEN** son résultat porte uniquement sur la syntaxe et ne prouve aucun droit sur le namespace, aucune unicité, propriété, provenance ou confiance, sans accès aux fichiers ni effet de composition ou d'activation
