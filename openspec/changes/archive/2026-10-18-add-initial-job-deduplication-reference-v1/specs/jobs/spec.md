## MODIFIED Requirements

### Requirement: Structure de JobDeduplicationReferenceV1

Le système MUST fournir un profil structurel immuable `JobDeduplicationReferenceV1` contenant exactement `deduplication_key` et `perimeter_reference`. Chaque champ MUST être une chaîne `str` exacte non vide, opaque et conservée sans normalisation.

#### Scenario: Références conservées exactement

- **WHEN** les deux champs sont des chaînes exactes non vides, y compris des espaces, de l'Unicode ou des différences de casse
- **THEN** le profil conserve exactement les valeurs fournies

### Requirement: Validation fermée de JobDeduplicationReferenceV1

La validation MUST contrôler le type exact du candidat et de chaque champ avant toute méthode sur une valeur étrangère. Les refus MUST utiliser les diagnostics `VALIDATE` existants, statiques, triés et dédupliqués, sans écho des valeurs.

#### Scenario: Type étranger refusé sans effet

- **WHEN** le candidat ou un champ est de type étranger, notamment une sous-classe de `str`
- **THEN** la validation refuse sans invoquer de méthode de cette valeur ni divulguer son contenu

#### Scenario: Référence vide refusée

- **WHEN** l'un des deux champs est une chaîne vide
- **THEN** la validation produit un diagnostic statique désignant le champ concerné

### Requirement: Limites de JobDeduplicationReferenceV1

Le profil et sa validation MUST NOT comparer l'unicité, résoudre le périmètre, stocker, fixer une rétention, lier ou exécuter un Job runtime, envoyer, réessayer, autoriser ni garantir un effet unique. Leur réussite MUST NOT être présentée comme une déduplication persistante. Les contrats et contrôles existants MUST rester inchangés.

#### Scenario: Validation sans effet de déduplication

- **WHEN** deux profils structurellement valides portent les mêmes références
- **THEN** leur validation ne produit aucun stockage, Job, envoi ni effet de déduplication et ne prouve aucune unicité persistante
