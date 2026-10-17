# Références normatives — O32

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| extension-contracts / 8 | [Points d'extension publics versionnés](../../specs/extension-contracts/spec.md#L8) | P | COMPLETER_OU_INTEGRER |
| extension-contracts / 17 | [Contributions déclarées et isolées](../../specs/extension-contracts/spec.md#L17) | P | COMPLETER_OU_INTEGRER |
| extension-contracts / 26 | [Niveau de confiance des extensions](../../specs/extension-contracts/spec.md#L26) | P | COMPLETER_OU_INTEGRER |
| extension-contracts / 38 | [Collisions et composition déterministe](../../specs/extension-contracts/spec.md#L38) | P | COMPLETER_OU_INTEGRER |
| extension-contracts / 47 | [Composition interface au build](../../specs/extension-contracts/spec.md#L47) | P | COMPLETER_OU_INTEGRER |
| extension-contracts / 56 | [Frontières publiques des composants frontend imbriqués](../../specs/extension-contracts/spec.md#L56) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence extension-contracts--9485da6da3

Source : `openspec/specs/extension-contracts/spec.md`, ligne 8. SHA-256 du bloc : `56c61d5033d805ad0e2870cbc39f8a41da383f3730161bdf1df625933c209f40`.

~~~~text
### Requirement: Points d'extension publics versionnés

Chaque point d'extension MUST déclarer identifiant namespacé, catégorie, version, schéma de contribution, propriétaire et garanties documentées.

#### Scenario: Contribution sans point déclaré rejetée

- **WHEN** une contribution vise un point non déclaré ou incompatible
- **THEN** la composition du périmètre concerné est refusée
~~~~

### Référence extension-contracts--24edde55c0

Source : `openspec/specs/extension-contracts/spec.md`, ligne 17. SHA-256 du bloc : `d0a67dc0a70b3171937bbda2dc584f3229af04fa96724cef1174d9da0b065ca6`.

~~~~text
### Requirement: Contributions déclarées et isolées

Chaque contribution MUST déclarer identifiant stable, composant cible, version de contrat, point d'entrée, dépendances, permissions, niveau de confiance et conditions d'activation ; elle MUST NOT importer d'implémentation privée ni modifier directement les données d'un autre composant.

#### Scenario: Accès privé bloqué

- **WHEN** une extension importe un modèle interne ou écrit dans les tables privées d'un autre module
- **THEN** le build ou l'activation bloque avec un diagnostic explicite
~~~~

### Référence extension-contracts--41b22aba68

Source : `openspec/specs/extension-contracts/spec.md`, ligne 26. SHA-256 du bloc : `80a499460a0a4d27935de2b57d47bbe6af06788183e764a008c27624822a96c9`.

~~~~text
### Requirement: Niveau de confiance des extensions

Toute extension MUST déclarer l'un des niveaux `PLATFORM`, `TRUSTED`,
`SANDBOXED` ou `DEVELOPMENT`. `DEVELOPMENT` MUST NOT être activé en production.
`SANDBOXED` MUST limiter ses accès aux APIs, permissions et données explicitement
accordées ; ce niveau MUST NOT contourner les contrats, l'autorisation ou la gouvernance.

#### Scenario: Extension de développement en production

- **WHEN** une composition de production inclut une extension `DEVELOPMENT`
- **THEN** sa validation échoue avant activation
~~~~

### Référence extension-contracts--150474c72f

Source : `openspec/specs/extension-contracts/spec.md`, ligne 38. SHA-256 du bloc : `0479271ff048f1b90c7b3904325a46004ba533c58c2546ae7c7d66e9eaba9bc7`.

~~~~text
### Requirement: Collisions et composition déterministe

Les collisions sont refusées par défaut ; toute composition multi-contributions MUST déclarer politique de fusion, priorité et ordre déterministes ; une contribution obligatoire incompatible bloque, une optionnelle est isolée et diagnostiquée.

#### Scenario: Deux routes en collision

- **WHEN** deux contributions revendiquent le même chemin sans politique déclarée
- **THEN** la composition est refusée au lieu d'un choix arbitraire
~~~~

### Référence extension-contracts--5480b74480

Source : `openspec/specs/extension-contracts/spec.md`, ligne 47. SHA-256 du bloc : `50b213d128a09c34ef6366a8aa083387ce0ccfd5791dff7976493a0931d48107`.

~~~~text
### Requirement: Composition interface au build

Les extensions d'interface de référence MUST être composées au build depuis des sources versionnées ; aucun téléchargement, installation ni évaluation de code distant au runtime ; toute isolation (sandbox, iframe) expose une API explicitement limitée.

#### Scenario: Code distant implicite refusé

- **WHEN** une extension tente de charger du code distant non déclaré au runtime
- **THEN** le chargement est refusé et l'état FAILED est diagnostiqué
~~~~

### Référence extension-contracts--23a0a5ef0e

Source : `openspec/specs/extension-contracts/spec.md`, ligne 56. SHA-256 du bloc : `b6da4b6727e3bd04c337b5ecd52affe386cf8747f447dfe0883e649b13436b68`.

~~~~text
### Requirement: Frontières publiques des composants frontend imbriqués

Un parent, un sous-module et leurs composants frères MUST s'intégrer par des routes, slots, façades, événements UI ou autres points d'extension publics, namespacés et versionnés. Une contribution enfant MUST NOT être activée, fusionnée ou rendue prioritaire par effet de bord du parent ; toute politique de composition reste déclarée et déterministe.

#### Scenario: Slot enfant non déclaré

- **WHEN** un sous-module tente de contribuer à une zone d'interface privée de son parent
- **THEN** le build refuse la contribution au lieu de l'intégrer par convention d'arborescence
~~~~

