## MODIFIED Requirements

### Requirement: Conteneur préparatoire FrontendManifestFacet v1

Dans un `component.toml` de `schema_version = "1"`, la table optionnelle `frontend` du profil FrontendManifestFacet v1 MUST contenir exactement `schema_version` et `contributions`. `frontend.schema_version` MUST être la chaîne `"1"`, distincte des versions du composant et des contributions. `contributions` MUST être un tableau ordonné de tables, MAY vide. Toute clé supplémentaire, version inconnue ou valeur d'un autre type MUST être refusée sans correction ni écho de valeur brute.

#### Scenario: Facette v1 structurée reconnue

- **WHEN** un manifest de schéma 1 porte une table frontend avec schema_version égal à la chaîne "1" et contributions vide
- **THEN** la facette est reconnue comme déclaration préparatoire sans activation

#### Scenario: Forme ou version hors profil refusée

- **WHEN** la facette omet une clé obligatoire, ajoute une clé, porte une version autre que la chaîne "1" ou des contributions d'un autre type
- **THEN** elle est refusée sans valeur implicite ni correction

### Requirement: Rattachement de la facette frontend au composant commun

Une facette FrontendManifestFacet v1 présente MUST appartenir à un composant MODULE ou SUBMODULE et rester rattachée à son identité, sa version et son lifecycle communs. L'absence de la table frontend MUST signifier absence de facette, sans modifier la validité des manifests existants. Ce profil MUST NOT créer de type de composant, registre ou lifecycle parallèle.

#### Scenario: Manifest historique sans facette

- **WHEN** un manifest valide ne contient pas de table frontend
- **THEN** sa validation conserve le comportement existant sans créer de facette implicite

#### Scenario: Type de composant hors périmètre

- **WHEN** un composant d'un type autre que MODULE ou SUBMODULE porte une facette frontend
- **THEN** cette facette est refusée dans le profil v1

### Requirement: Déclarations de contribution sérialisées sans transformation

Chaque table de contributions MUST être conforme aux six champs exacts de FrontendContributionDeclaration v1 et à leurs profils existants, sans autre grammaire. La représentation validée de la facette MUST être immuable et préserver les textes, l'ordre et la multiplicité des contributions et de requires, sans normalisation, décodage ni changement de casse. Un diagnostic de refus MUST NOT reproduire les valeurs brutes.

#### Scenario: Déclarations ordonnées préservées

- **WHEN** la facette contient des déclarations v1 valides avec textes, dépendances et contributions ordonnés
- **THEN** ces valeurs et leur multiplicité sont conservées dans une représentation immuable

#### Scenario: Déclaration hors profil refusée

- **WHEN** une contribution manque de requires ou scope, ajoute un champ ou utilise une valeur refusée par FrontendContributionDeclaration v1
- **THEN** la facette est refusée sans correction ni écho de la valeur brute

### Requirement: Limites de la facette préparatoire frontend v1

La reconnaissance FrontendManifestFacet v1 MUST rester structurelle. Elle MUST NOT résoudre les chemins d'entrée, charger du code, composer, router, activer, résoudre les dépendances ou autoriser une action. Elle MUST NOT prouver unicité, propriété, provenance, confiance, droit sur pixs.* ou compatibilité du shell. Les règles communes restent applicables séparément.

#### Scenario: Reconnaissance sans effet runtime

- **WHEN** une facette v1 est reconnue
- **THEN** aucun chargement, routage, résolution, activation ou droit n'en découle
