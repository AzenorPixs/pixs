# Références normatives — O12

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| notifications / 22 | [Asynchronisme avec réessais bornés](../../specs/notifications/spec.md#L22) | P | COMPLETER_OU_INTEGRER |
| notifications / 33 | [Confidentialité et audit](../../specs/notifications/spec.md#L33) | P | COMPLETER_OU_INTEGRER |
| notifications / 42 | [Profil structurel NotificationDeduplicationReferenceV1](../../specs/notifications/spec.md#L42) | P | REUTILISATION_A_QUALIFIER |
| notifications / 61 | [Limites du profil préparatoire de déduplication](../../specs/notifications/spec.md#L61) | P | REUTILISATION_A_QUALIFIER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence notifications--1b1f603c33

Source : `openspec/specs/notifications/spec.md`, ligne 22. SHA-256 du bloc : `2f09248b570dd711b1dec13c631e8a2be63102ac78e637c4e18b5d7f8ad3bb2b`.

~~~~text
### Requirement: Asynchronisme avec réessais bornés

Le système MUST respecter les garanties suivantes.

Les envois utilisent des travaux persistants avec réessais bornés, déduplication et lettres mortes ; l'épuisement produit un état diagnostiquable sans perte silencieuse.

#### Scenario: Échec persistant tracé

- **WHEN** les réessais sont épuisés
- **THEN** la notification passe en lettre morte avec audit et sans divulgation de contenu sensible
~~~~

### Référence notifications--a6ae2139c1

Source : `openspec/specs/notifications/spec.md`, ligne 33. SHA-256 du bloc : `142476ae3177fec08cedf4d18057140b40f68ea4bb38d94a29c795d6f0c858c6`.

~~~~text
### Requirement: Confidentialité et audit

Les notifications MUST respecter la classification et la gouvernance, minimiser le contenu, ne jamais exposer de secret, et tracer acteur, action et cible sans journaliser les données sensibles.

#### Scenario: Donnée protégée minimisée

- **WHEN** une notification concerne une donnée classifiée
- **THEN** seuls les champs nécessaires sont transmis et l'envoi est audité
~~~~

### Référence notifications--78391a5fdd

Source : `openspec/specs/notifications/spec.md`, ligne 42. SHA-256 du bloc : `46b8b435abc5009ba4e7525e3b0722b53f376012d67c6a55604d223a8701a8fd`.

~~~~text
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
~~~~

### Référence notifications--971d595c91

Source : `openspec/specs/notifications/spec.md`, ligne 61. SHA-256 du bloc : `8de7e58f7b1ba59c381396acbc7438be26c3a2703cdd736bb585007d8a5e2352`.

~~~~text
### Requirement: Limites du profil préparatoire de déduplication

Le profil et sa validation MUST NOT comparer l'unicité, résoudre le périmètre, stocker des données, fixer une rétention, envoyer une notification, lier un Job ni garantir un effet unique. Ils MUST NOT être présentés comme une implémentation de la déduplication persistante. Les contrats et contrôles existants MUST rester inchangés.

#### Scenario: Validation sans effet de déduplication

- **WHEN** deux profils structurellement valides portent les mêmes références
- **THEN** leur validation ne produit aucun envoi, stockage ou effet de déduplication et ne prouve aucune unicité persistante
~~~~

