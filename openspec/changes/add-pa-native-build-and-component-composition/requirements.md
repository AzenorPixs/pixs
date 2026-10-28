# Références normatives — PA01

> Instantané historique des exigences reproduites lors de la préparation. La décision du 21 octobre 2026 retient désormais Cython pour les trois binaires PA et pour PZT indépendant ; les mentions Nuitka dans les blocs et empreintes ci-dessous conservent leur valeur de trace historique et ne sont plus le choix de compilation PA. Le canon et les deltas du change [binaire PBO et profils](../define-common-pbo-binary-and-resource-profiles/design.md) font référence avant réalisation. Aucune empreinte ni preuve de qualification antérieure n'est régénérée ici.

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 11 | [Quatre binaires et sept modes explicitement répartis](../../specs/pixs-agent/spec.md#L11) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 20 | [Compilation différenciée validée](../../specs/pixs-agent/spec.md#L20) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 47 | [Composition au build et catalogue fermé](../../specs/pixs-agent/spec.md#L47) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 218 | [Paramètres ouverts et absence d'implémentation implicite](../../specs/pixs-agent/spec.md#L218) | ND | CANDIDAT_PROFIL_PA |
| pzt / 21 | [Module essentiel PBO et binaire PZT dédié](../../specs/pzt/spec.md#L21) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| reference-runtime / 168 | [Couche exécutable PA séparée](../../specs/reference-runtime/spec.md#L168) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--24f2ceb983

Source : `openspec/specs/pixs-agent/spec.md`, ligne 11. SHA-256 du bloc : `7d77582c9257ea14c361d203416f60c56bc861c3552acc98a217d029ad22e615`.

~~~~text
### Requirement: Quatre binaires et sept modes explicitement répartis

PA MUST comporter exactement quatre binaires dédiés : démon système pour system-daemon ; événements système pour system-start et system-stop ; sessions utilisateur pour session-start, session-stop et session-daemon ; exécution PZT pour pzt-daemon. Les noms d'exécutables, chemins et options CLI restent à spécifier. Le découpage MUST NOT créer un cinquième binaire pour le démon de session.

#### Scenario: Quatre binaires et sept modes explicitement répartis

- **WHEN** une distribution PA complète décrit ses exécutables
- **THEN** elle identifie les quatre responsabilités et les sept modes sans les confondre
~~~~

### Référence pixs-agent--5711267e47

Source : `openspec/specs/pixs-agent/spec.md`, ligne 20. SHA-256 du bloc : `9132f06dab01d6d49af23b44e279820ce119057bed453909df089ea538f12990`.

~~~~text
### Requirement: Compilation différenciée validée

Les binaires démon système, événements système et sessions utilisateur MUST être compilés avec Nuitka ; le binaire PZT MUST être compilé avec Cython. La chaîne MUST partir des sources Python, générer du C puis des exécutables natifs avec runtime et dépendances déclarés. Versions exactes et compatibilité MUST être qualifiées avant construction ; cette décision MUST NOT installer une dépendance ni prouver un gain de performance.

#### Scenario: Compilation différenciée validée

- **WHEN** la matrice de compilation est déclarée
- **THEN** les trois premiers binaires utilisent Nuitka et celui de PZT utilise Cython
~~~~

### Référence pixs-agent--bd3940f601

Source : `openspec/specs/pixs-agent/spec.md`, ligne 47. SHA-256 du bloc : `2cde976931df9e6c3f72460dd263b37705129586eb38a9efc3be6b7269446983`.

~~~~text
### Requirement: Composition au build et catalogue fermé

Chaque capacité PA MUST déclarer identité, version, propriétaire, contrats, dépendances, configuration, sécurité et permissions selon le modèle de composants. La composition initiale MUST se faire au build ; instructions et mandats MUST sélectionner seulement des opérations déjà livrées. PA MUST NOT télécharger ou charger implicitement du code, évaluer du Python ou ouvrir un shell privilégié à partir d'une instruction réseau.

#### Scenario: Composition au build et catalogue fermé

- **WHEN** une instruction demande une opération absente du catalogue livré
- **THEN** elle est refusée sans téléchargement ou exécution de code arbitraire
~~~~

### Référence pixs-agent--3d7a2be5b3

Source : `openspec/specs/pixs-agent/spec.md`, ligne 218. SHA-256 du bloc : `2f7e9ceaff587eaeb6b5bc4691e3df6dd5cf2b52f849c4932d465059d8e0433e`.

~~~~text
### Requirement: Paramètres ouverts et absence d'implémentation implicite

Les noms/versions de paquets et exécutables, bibliothèques, formats non arrêtés, topologies, comptes, quotas manquants et seuils à mesurer MUST rester explicitement ouverts jusqu'à décision ou qualification appropriée. Les versions de Nuitka/Cython et leur graphe MUST être qualifiés avant installation. La rédaction de ces spécifications MUST NOT être présentée comme du code, un test runtime, une plateforme supportée ou un artefact livré.

#### Scenario: Paramètres ouverts et absence d'implémentation implicite

- **WHEN** seules les spécifications sont déclarées
- **THEN** les états d'implémentation, qualification et publication restent explicitement non réalisés
~~~~

### Référence pzt--73016f3d2e

Source : `openspec/specs/pzt/spec.md`, ligne 21. SHA-256 du bloc : `050ae5dc06f898c93bf7624d680e4352ef1525bffe2dbb46b7c66870d5c021d5`.

~~~~text
### Requirement: Module essentiel PBO et binaire PZT dédié

Toute composition cible PBO MUST inclure le module officiel essentiel PZT, au-dessus du Kernel et de pixs.core, par les mécanismes génériques de modules. Le réseau activé/configuré MUST toujours être exécuté par le binaire PZT de PA compilé avec Cython ; PBO MUST assurer configuration, visualisation, supervision et monitoring. Désactiver le réseau MUST NOT retirer le module essentiel de PBO.

#### Scenario: Module essentiel PBO et binaire PZT dédié

- **WHEN** PZT est désactivé dans un PBO
- **THEN** le binaire réseau se ferme mais le module PBO de gestion reste composé
~~~~

### Référence reference-runtime--eb2f9f2af9

Source : `openspec/specs/reference-runtime/spec.md`, ligne 168. SHA-256 du bloc : `37e910ca3a63eaa93c85bf35594c6ee0857b63ec5c280bd47537f3a655ed89bd`.

~~~~text
### Requirement: Couche exécutable PA séparée

Les binaires PA définis par pixs-agent MUST constituer une couche d’exécution locale distincte et MUST NOT remplacer Django, PostgreSQL ou TanStack ni devenir un backend métier alternatif. Leur compilation MUST suivre le choix Nuitka pour trois binaires et Cython pour PZT.

#### Scenario: Couche exécutable PA séparée

- **WHEN** un binaire PA est décrit
- **THEN** il ne devient pas une implémentation alternative de l’autorité métier PBO
~~~~


## Rapprochement avec le canon courant — reprise CISMP7 du 22 octobre 2026

Les six copies et empreintes historiques ci-dessus restent intactes. La table suivante repère leurs exigences correspondantes dans le canon relu sous accès de lecture CAB ; elle ne régénère aucune preuve historique et ne constitue aucun delta normatif. Les titres, lignes et empreintes ci-dessous décrivent cette relecture datée et devront être recontrôlés si le canon évolue.

| Bloc historique | Source actuelle et ligne | Exigence courante | Scénarios du bloc | SHA-256 du bloc courant |
| --- | --- | --- | ---: | --- |
| pixs-agent / 11 | [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md), ligne 64 | Trois binaires PA et six modes distincts de PZT | 1 | `5cd5cae10cd478a8ffb30c4e15180dfdc341506019583f78882f62ec99106408` |
| pixs-agent / 20 | [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md), ligne 78 | Compilation différenciée validée | 1 | `49d91499d8f83f1c794a0c59612a178648ad502a5b43f2965eba5f1f79a072e6` |
| pixs-agent / 47 | [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md), ligne 108 | Composition au build et catalogue fermé | 1 | `0ed896227fd4520562a556c15ca86d634e059dc29313794ff743d8324201c20b` |
| pixs-agent / 218 | [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md), ligne 296 | Paramètres ouverts et absence d'implémentation implicite | 1 | `2fe8f8e831ff5c8809f75a824394b629f715e43baab2b850615835c04c39ba78` |
| pzt / 21 | [openspec/specs/pzt/spec.md](../../specs/pzt/spec.md), ligne 77 | Module essentiel pixs.pzt et exécutable PZT indépendant | 1 | `1063497b290fd7bb8e8abad2dad81ac19bb67f139b4c911c98be000279df7b7c` |
| reference-runtime / 168 | [openspec/specs/reference-runtime/spec.md](../../specs/reference-runtime/spec.md), ligne 221 | Couche exécutable PA séparée | 1 | `409ab89f825b092bd0b952bce1b1e35b9f4b326cd4c20d55d333a5a993bb892f` |

Méthode d’empreinte : bloc UTF-8 depuis son titre `### Requirement:` jusqu’au titre suivant de même niveau exclu, blancs terminaux retirés, puis un unique LF final ajouté ; tous les scénarios du bloc sont inclus. Six exigences et six scénarios sont repérés. Une empreinte n’est pas une preuve d’implémentation.

La correspondance actuelle retient trois binaires et six modes PA, plus PZT indépendant et son mode `pzt-daemon`, avec Cython pour les deux chaînes distinctes. Elle conserve le catalogue fermé, les paramètres non décidés, les responsabilités de `pixs.agent`/`pixs.pzt` et l’absence d’autorité métier des exécutants. Les copies Nuitka ou du quatrième binaire rattaché à PA restent uniquement historiques.

Les candidats CPython 3.14.9 avec GIL/Cython 3.3.0, la distribution en répertoire et la première cible Debian 13 x86_64 physique/VM sont consignés dans [le premier lot validé](design.md). Leur validation ne qualifie pas la chaîne ni une plateforme et ne modifie pas les exigences canoniques.
