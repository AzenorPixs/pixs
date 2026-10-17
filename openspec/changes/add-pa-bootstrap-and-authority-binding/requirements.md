# Références normatives — PA02

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 38 | [Indépendance d'installation et autorité applicative](../../specs/pixs-agent/spec.md#L38) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 65 | [Provisionnement distinct du canal de contrôle](../../specs/pixs-agent/spec.md#L65) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 101 | [Plusieurs PBO et conflits explicites](../../specs/pixs-agent/spec.md#L101) | ND | CANDIDAT_PROFIL_PA |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--5c3c0eb52d

Source : `openspec/specs/pixs-agent/spec.md`, ligne 38. SHA-256 du bloc : `db38cd6d3d6d07cd9b02dc070c47ce83fa1ac4262c41dbefc28ef736d48ebac0`.

~~~~text
### Requirement: Indépendance d'installation et autorité applicative

Les binaires PA MUST pouvoir être installés sans PBO, PFO ou navigateur locaux et joindre un PBO distant autorisé. PA MUST NOT embarquer Django/PostgreSQL comme autorité métier, accéder directement aux tables métier ni confirmer une mutation de sa propre initiative. PBO/Django MUST conserver les décisions applicatives et PostgreSQL leur persistance de référence.

#### Scenario: Indépendance d'installation et autorité applicative

- **WHEN** PA est installé seul sur une cible
- **THEN** ses opérations restent liées à leurs mandats et à l'autorité PBO compétente
~~~~

### Référence pixs-agent--a5d47c79ad

Source : `openspec/specs/pixs-agent/spec.md`, ligne 65. SHA-256 du bloc : `f6d65845a37f027ce02981a8cd2727d7b6aacd2d3591e0d1e5c321d56b497db0`.

~~~~text
### Requirement: Provisionnement distinct du canal de contrôle

Le provisionnement MUST établir configuration minimale, identité, ancrages et références de secrets avant le premier échange PBO–PA, avec états inspectables non provisionné, en cours, prêt ou échoué. L'origine et l'autorisation MUST être vérifiées ; le premier PBO rencontré MUST NOT être approuvé automatiquement. La reprise MUST éviter de dupliquer identité ou autorisation ; des fichiers de provisionnement MUST NOT devenir un canal continu hors PZT.

#### Scenario: Provisionnement distinct du canal de contrôle

- **WHEN** l'ancrage requis est absent au premier démarrage
- **THEN** les échanges dépendants restent bloqués avec un état de provisionnement explicite
~~~~

### Référence pixs-agent--81ad04f3f7

Source : `openspec/specs/pixs-agent/spec.md`, ligne 101. SHA-256 du bloc : `ba18660550aea4c031e646bba39b2b2cfa1772e2ab93aa12780c3665c753f4c5`.

~~~~text
### Requirement: Plusieurs PBO et conflits explicites

Chaque relation PBO–PA MUST déclarer son périmètre et ses versions ; plusieurs connexions MUST NOT permettre l'administration libre d'une même ressource. Les autorités, délégations et priorités MUST être définies avant activation ; des commandes incompatibles MUST être bloquées sans règle du dernier message reçu. Les résultats, identités et configurations d'une relation MUST NOT être exposés à une autre sans accord explicite.

#### Scenario: Plusieurs PBO et conflits explicites

- **WHEN** deux instructions incompatibles ciblent la même ressource
- **THEN** le conflit est déclaré et aucune autorité n'est choisie implicitement
~~~~

