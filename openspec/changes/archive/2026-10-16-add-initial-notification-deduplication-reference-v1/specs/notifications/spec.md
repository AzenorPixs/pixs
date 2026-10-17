## MODIFIED Requirements

### Requirement: Profil structurel NotificationDeduplicationReferenceV1

Le système MUST fournir un profil structurel immuable `NotificationDeduplicationReferenceV1` à exactement deux champs `deduplication_key` et `perimeter_reference`, chacun de type `str` exact, non vide, opaque et conservé sans normalisation. La validation MUST contrôler le type exact du candidat et de chaque champ avant toute méthode sur une valeur étrangère. Les refus MUST utiliser des diagnostics statiques, triés et dédupliqués, sans écho des valeurs.

#### Scenario: Type étranger refusé sans effet

- **WHEN** le candidat ou un champ présente un type étranger, notamment une sous-classe de `str`
- **THEN** la validation refuse le candidat sans invoquer de méthode de cette valeur et sans divulguer son contenu

#### Scenario: Référence vide refusée

- **WHEN** l'un des deux champs est une chaîne vide
- **THEN** la validation produit un diagnostic statique désignant le champ concerné

#### Scenario: Références conservées exactement

- **WHEN** les deux champs sont des chaînes exactes non vides, y compris avec des espaces
- **THEN** le profil conserve leurs valeurs sans suppression d'espaces, conversion de casse ni autre normalisation

### Requirement: Limites du profil préparatoire de déduplication

Le profil et sa validation MUST NOT comparer l'unicité, résoudre le périmètre, stocker des données, fixer une rétention, envoyer une notification, lier un Job ni garantir un effet unique. Ils MUST NOT être présentés comme une implémentation de la déduplication persistante. Les contrats et contrôles existants MUST rester inchangés.

#### Scenario: Validation sans effet de déduplication

- **WHEN** deux profils structurellement valides portent les mêmes références
- **THEN** leur validation ne produit aucun envoi, stockage ou effet de déduplication et ne prouve aucune unicité persistante
