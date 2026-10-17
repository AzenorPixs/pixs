# notifications Specification

## Purpose
Les notifications acheminent les informations aux destinataires via des canaux déclarés, de façon asynchrone, dédupliquée et confidentielle.

## Requirements

### Requirement: Contrats et préférences déclarés

Chaque notification MUST suivre un contrat versionné avec destinataires, canaux, préférences et périmètre ; aucun canal implicite ni destinataire élargi sans règle déclarée.

#### Scenario: Canal non déclaré refusé

- **WHEN** un envoi vise un canal non déclaré par le contrat
- **THEN** l'envoi est refusé avec une erreur explicite

#### Scenario: Destinataire élargi refusé

- **WHEN** un envoi vise un destinataire non déclaré par le contrat
- **THEN** l'envoi est refusé avec une erreur explicite

### Requirement: Asynchronisme avec réessais bornés

Le système MUST respecter les garanties suivantes.

Les envois utilisent des travaux persistants avec réessais bornés, déduplication et lettres mortes ; l'épuisement produit un état diagnostiquable sans perte silencieuse.

#### Scenario: Échec persistant tracé

- **WHEN** les réessais sont épuisés
- **THEN** la notification passe en lettre morte avec audit et sans divulgation de contenu sensible

### Requirement: Confidentialité et audit

Les notifications MUST respecter la classification et la gouvernance, minimiser le contenu, ne jamais exposer de secret, et tracer acteur, action et cible sans journaliser les données sensibles.

#### Scenario: Donnée protégée minimisée

- **WHEN** une notification concerne une donnée classifiée
- **THEN** seuls les champs nécessaires sont transmis et l'envoi est audité

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
