# Références normatives — O14

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| feature-flags / 18 | [Définition versionnée et bornée](../../specs/feature-flags/spec.md#L18) | P | INTEGRER_EXISTANT_SI_SELECTION |
| feature-flags / 27 | [Ciblage et cohorte déterministes](../../specs/feature-flags/spec.md#L27) | P | INTEGRER_EXISTANT_SI_SELECTION |
| feature-flags / 36 | [Déclaration serveur de la cohorte progressive](../../specs/feature-flags/spec.md#L36) | P | INTEGRER_EXISTANT_SI_SELECTION |
| feature-flags / 45 | [Bucket stable et seuil de cohorte](../../specs/feature-flags/spec.md#L45) | P | INTEGRER_EXISTANT_SI_SELECTION |
| feature-flags / 54 | [Validation préalable de la cohorte](../../specs/feature-flags/spec.md#L54) | P | INTEGRER_EXISTANT_SI_SELECTION |
| feature-flags / 63 | [Repli hors cohorte et fanion sans cohorte](../../specs/feature-flags/spec.md#L63) | P | INTEGRER_EXISTANT_SI_SELECTION |
| feature-flags / 72 | [Échec fermé pour le sensible](../../specs/feature-flags/spec.md#L72) | P | INTEGRER_EXISTANT_SI_SELECTION |
| feature-flags / 81 | [Repli DEFAULT réservé au non sensible](../../specs/feature-flags/spec.md#L81) | P | INTEGRER_EXISTANT_SI_SELECTION |
| feature-flags / 95 | [Repli inconnu et classification serveur](../../specs/feature-flags/spec.md#L95) | P | INTEGRER_EXISTANT_SI_SELECTION |
| feature-flags / 104 | [Expiration serveur des valeurs et affectations](../../specs/feature-flags/spec.md#L104) | P | INTEGRER_EXISTANT_SI_SELECTION |
| feature-flags / 113 | [Affectations hors artefacts](../../specs/feature-flags/spec.md#L113) | P | INTEGRER_EXISTANT_SI_SELECTION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence feature-flags--51b8b1a1de

Source : `openspec/specs/feature-flags/spec.md`, ligne 18. SHA-256 du bloc : `82a107406d149fcb7224c81e7ab699d8816c0b22633fc8b6e1f88d3f7db2f1e4`.

~~~~text
### Requirement: Définition versionnée et bornée

Chaque fanion MUST déclarer identifiant, version, propriétaire, finalité, type BOOLEAN ou VARIANT, défaut, dimensions, cohorte éventuelle, prérequis, repli, expiration et audit ; les règles sont déclaratives, bornées et déterministes, sans code arbitraire.

#### Scenario: Règle à expression rejetée

- **WHEN** une règle embarque du code ou une expression distante
- **THEN** la définition est refusée avant activation
~~~~

### Référence feature-flags--5738221737

Source : `openspec/specs/feature-flags/spec.md`, ligne 27. SHA-256 du bloc : `3680ca65af3e228e03863ef2548fa844425195b85b1c36e545e687df8d59826f`.

~~~~text
### Requirement: Ciblage et cohorte déterministes

Le système MUST respecter les garanties suivantes. L'évaluation utilise uniquement les dimensions déclarées (installation, environnement, tenant, scope enfant) avec priorité du général au spécifique et cohorte stable sans tirage par requête.

#### Scenario: Même contexte même décision

- **WHEN** le même contexte est évalué deux fois
- **THEN** le résultat est identique
~~~~

### Référence feature-flags--6606358021

Source : `openspec/specs/feature-flags/spec.md`, ligne 36. SHA-256 du bloc : `a9bd957e9f287c029adc73ba1582c47251b8f6120da5d498273f13e54eaf19fe`.

~~~~text
### Requirement: Déclaration serveur de la cohorte progressive

Une cohorte progressive MUST être résolue par une règle déclarative côté serveur, distincte de la définition du fanion, contenant cohort_key, subject_dimension, threshold_basis_points et configuration_version. subject_dimension MUST être l'une des dimensions déclarées du fanion parmi INSTALLATION, ENVIRONMENT, TENANT ou SCOPE ; son identité MUST provenir du contexte applicatif canonique côté serveur, sans ciblage individuel ni élargissement implicite de tenant ou de scope.

#### Scenario: Dimension de cohorte déclarée

- **WHEN** une règle de cohorte progressive est résolue côté serveur
- **THEN** elle contient les quatre champs déclarés et son sujet provient d'une dimension du fanion et du contexte canonique sans élargissement de périmètre
~~~~

### Référence feature-flags--4d3be71aff

Source : `openspec/specs/feature-flags/spec.md`, ligne 45. SHA-256 du bloc : `d833e100bec7ea0dbef8405a168fd5466042a0bf5299ba8a3844761740b592e6`.

~~~~text
### Requirement: Bucket stable et seuil de cohorte

threshold_basis_points MUST être un entier compris entre 0 et 10000 inclus. Pour une même clé, une même dimension et une même identité canonique, le calcul MUST fournir le même bucket compris entre 0 et 9999 ; il MUST NOT dépendre de l'instant de requête, du seuil ou d'un tirage aléatoire. Le sujet MUST appartenir à la cohorte exactement lorsque bucket est strictement inférieur à threshold_basis_points.

#### Scenario: Bornes du déploiement progressif

- **WHEN** une règle de cohorte valide est évaluée sur une identité canonique avec un seuil de 0 ou de 10000 points de base
- **THEN** respectivement aucun sujet ou tout sujet valide appartient à la cohorte, sans décision d'autorisation implicite
~~~~

### Référence feature-flags--5dac000c72

Source : `openspec/specs/feature-flags/spec.md`, ligne 54. SHA-256 du bloc : `e3de1982843426b2d36a9814a5dd34bfa30dc261880baede0a7858981fdca0ef`.

~~~~text
### Requirement: Validation préalable de la cohorte

Avant toute évaluation d'affectation soumise à une cohorte, la configuration et l'identité du sujet MUST être validées. Une clé non résolue, une règle invalide, une identité absente ou une version incompatible avec la configuration canonique attendue MUST refuser cette évaluation avant la sélection de valeur et MUST NOT introduire un défaut implicite de configuration.

#### Scenario: Configuration de cohorte indisponible

- **WHEN** la clé ne se résout pas, la règle est invalide, l'identité manque ou la version est incompatible avec la configuration canonique attendue
- **THEN** l'évaluation est refusée sans valeur et sans défaut implicite
~~~~

### Référence feature-flags--5c5ec22a72

Source : `openspec/specs/feature-flags/spec.md`, ligne 63. SHA-256 du bloc : `746d54374f7d4d41545ddd3e27b4ae87b2c112348a60e3dd8b473e62d9683a1e`.

~~~~text
### Requirement: Repli hors cohorte et fanion sans cohorte

Pour une règle valide, un sujet hors cohorte MUST exclure la valeur affectée et appliquer le repli R3 pour la cause ABSENT ; cette décision MUST NOT constituer une permission. Un fanion sans cohort_key MUST conserver son évaluation sans cohorte.

#### Scenario: Sujet hors cohorte

- **WHEN** le bucket stable d'un sujet valide est supérieur ou égal au seuil déclaré
- **THEN** la valeur affectée n'est pas exposée et le repli R3 pour ABSENT s'applique, avec refus pour le sensible
~~~~

### Référence feature-flags--a18ee5957f

Source : `openspec/specs/feature-flags/spec.md`, ligne 72. SHA-256 du bloc : `6c42fe754bda46ff76ce759e8d51d875cdaede02fddffe7a3b5b1feb66fc13cd`.

~~~~text
### Requirement: Échec fermé pour le sensible

Le système MUST respecter les garanties suivantes. Une valeur absente, invalide ou périmée MUST appliquer la politique de repli déclarée. À l'exécution, seules les politiques déclaratives DENY et DEFAULT MUST être reconnues. DENY MUST refuser l'opération sans exposer de valeur de fanion.

#### Scenario: Repli DENY sans valeur

- **WHEN** une valeur absente, invalide ou périmée relève d'une politique DENY
- **THEN** l'opération est refusée sans exposition de valeur de fanion
~~~~

### Référence feature-flags--b84826e079

Source : `openspec/specs/feature-flags/spec.md`, ligne 81. SHA-256 du bloc : `0bf5318d5a5885d1a0e45baea8ce7477f7d1f7a60b1d413a2579df1f3f6dd90f`.

~~~~text
### Requirement: Repli DEFAULT réservé au non sensible

DEFAULT MUST appliquer la valeur par défaut validée de la définition uniquement pour une fonctionnalité non sensible ; DEFAULT MUST NOT être appliqué à une permission, une mutation, une donnée protégée ou un contrat. Une permission, une mutation, une donnée protégée ou un contrat MUST être refusé sur valeur absente, invalide ou périmée, quelle que soit la politique déclarée.

#### Scenario: Fanion d'autorisation indisponible

- **WHEN** le fanion requis pour une mutation est indisponible
- **THEN** l'opération est refusée au lieu d'un repli permissif

#### Scenario: Repli par défaut sur fonctionnalité non sensible

- **WHEN** une valeur absente, invalide ou périmée concerne une fonctionnalité non sensible déclarée avec le repli DEFAULT
- **THEN** la valeur par défaut validée de la définition est appliquée et aucune décision d'autorisation n'en découle
~~~~

### Référence feature-flags--31945a2a93

Source : `openspec/specs/feature-flags/spec.md`, ligne 95. SHA-256 du bloc : `b291e75925acdb7af11ad2b2221ff7b2faafc233f065144e9e2e909e134d516e`.

~~~~text
### Requirement: Repli inconnu et classification serveur

Une référence de repli inconnue ou incompatible MUST produire un refus sans valeur et MUST NOT être convertie en alias implicite. La classification sensible ou non sensible MUST provenir du contexte applicatif canonique côté serveur ; le client et le frontal MUST NOT fournir cette classification. Le frontal MUST faire réévaluer le fanion côté applicatif avant toute exposition protégée.

#### Scenario: Référence de repli inconnue refusée

- **WHEN** un fanion déclare une référence de repli hors du vocabulaire d'exécution borné
- **THEN** l'évaluation est refusée sans exposition de valeur
~~~~

### Référence feature-flags--453d7055b7

Source : `openspec/specs/feature-flags/spec.md`, ligne 104. SHA-256 du bloc : `4a1ad3065067ce6b40d398f0cee2c7d494962fcd7c4c8027bc321584f6012b5c`.

~~~~text
### Requirement: Expiration serveur des valeurs et affectations

À l'instant de référence UTC fourni par le contexte applicatif canonique côté serveur, une définition dont expires_at est inférieur ou égal à cet instant MUST rendre périmées ses valeurs déjà affectées, même lorsque la fenêtre de l'affectation est encore valide ; la politique de repli déclarée MUST alors s'appliquer. L'expiration MUST bloquer les nouvelles affectations et produire un diagnostic, sans suppression implicite de code, données ou contrats.

#### Scenario: Affectation active sous définition expirée

- **WHEN** une affectation encore dans sa fenêtre est évaluée alors que expires_at de la définition est atteint à l'instant de référence serveur
- **THEN** la valeur affectée n'est pas exposée et la politique de repli déclarée s'applique ; toute nouvelle affectation est refusée avec un diagnostic
~~~~

### Référence feature-flags--a29810cb32

Source : `openspec/specs/feature-flags/spec.md`, ligne 113. SHA-256 du bloc : `d502472158a077c9bfc22db194c232cd1fd73cafd61f3603657c6387da27b9c6`.

~~~~text
### Requirement: Affectations hors artefacts

Le système MUST respecter les garanties suivantes.

Les affectations runtime proviennent d'une source persistante versionnée ; aucun paquet, image ni bundle n'embarque d'affectation ; les changements sont administrés, corrélés et audités.

#### Scenario: Affectation embarquée rejetée

- **WHEN** un artefact contient une affectation d'installation ou de production
- **THEN** le build refuse la composition
~~~~

