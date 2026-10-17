# Références normatives — PA09

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| deb-package / 58 | [Distribution Debian indépendante PA et PBO PFO](../../specs/deb-package/spec.md#L58) | ND | COMPLETER_OU_INTEGRER |
| deb-package / 67 | [Quatre binaires dans le paquet PA](../../specs/deb-package/spec.md#L67) | ND | COMPLETER_OU_INTEGRER |
| pixs-agent / 11 | [Quatre binaires et sept modes explicitement répartis](../../specs/pixs-agent/spec.md#L11) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 38 | [Indépendance d'installation et autorité applicative](../../specs/pixs-agent/spec.md#L38) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 209 | [Publications locales expérimentales et sécurité de distribution](../../specs/pixs-agent/spec.md#L209) | ND | CANDIDAT_PROFIL_PA |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence deb-package--9112fb78b5

Source : `openspec/specs/deb-package/spec.md`, ligne 58. SHA-256 du bloc : `093f3bb6a9b35ad099decdd39ded1a7a9654a93e094cf52a59d6d33d3c3bb2c3`.

~~~~text
### Requirement: Distribution Debian indépendante PA et PBO PFO

La distribution Debian MUST comporter un paquet PBO/PFO et un paquet PA indépendant. Le paquet PBO/PFO MUST contenir le module essentiel PZT et MUST NOT embarquer les quatre binaires PA. L’installation PA seule MUST NOT requérir PBO/PFO locaux comme contenu embarqué ; les compatibilités et dépendances d’installation restent déclarées.

#### Scenario: Distribution Debian indépendante PA et PBO PFO

- **WHEN** PA est installé seul
- **THEN** son paquet reste indépendant et peut joindre un PBO distant autorisé
~~~~

### Référence deb-package--477adcdbb1

Source : `openspec/specs/deb-package/spec.md`, ligne 67. SHA-256 du bloc : `e049d00b76c48e5d87aed01ad83927a13fa52686eb940213167e99ad4936f6c4`.

~~~~text
### Requirement: Quatre binaires dans le paquet PA

Le paquet PA MUST livrer exactement les quatre exécutables définis par pixs-agent : démon système, événements de démarrage/arrêt de l’hôte, sessions utilisateur et exécution PZT. Il MUST conserver la séparation des modes et permissions ; noms/chemins et versions restent à spécifier.

#### Scenario: Quatre binaires dans le paquet PA

- **WHEN** le paquet PA est vérifié
- **THEN** les quatre binaires et leurs responsabilités sont identifiables sans PBO/PFO embarqués
~~~~

### Référence pixs-agent--24f2ceb983

Source : `openspec/specs/pixs-agent/spec.md`, ligne 11. SHA-256 du bloc : `7d77582c9257ea14c361d203416f60c56bc861c3552acc98a217d029ad22e615`.

~~~~text
### Requirement: Quatre binaires et sept modes explicitement répartis

PA MUST comporter exactement quatre binaires dédiés : démon système pour system-daemon ; événements système pour system-start et system-stop ; sessions utilisateur pour session-start, session-stop et session-daemon ; exécution PZT pour pzt-daemon. Les noms d'exécutables, chemins et options CLI restent à spécifier. Le découpage MUST NOT créer un cinquième binaire pour le démon de session.

#### Scenario: Quatre binaires et sept modes explicitement répartis

- **WHEN** une distribution PA complète décrit ses exécutables
- **THEN** elle identifie les quatre responsabilités et les sept modes sans les confondre
~~~~

### Référence pixs-agent--5c3c0eb52d

Source : `openspec/specs/pixs-agent/spec.md`, ligne 38. SHA-256 du bloc : `db38cd6d3d6d07cd9b02dc070c47ce83fa1ac4262c41dbefc28ef736d48ebac0`.

~~~~text
### Requirement: Indépendance d'installation et autorité applicative

Les binaires PA MUST pouvoir être installés sans PBO, PFO ou navigateur locaux et joindre un PBO distant autorisé. PA MUST NOT embarquer Django/PostgreSQL comme autorité métier, accéder directement aux tables métier ni confirmer une mutation de sa propre initiative. PBO/Django MUST conserver les décisions applicatives et PostgreSQL leur persistance de référence.

#### Scenario: Indépendance d'installation et autorité applicative

- **WHEN** PA est installé seul sur une cible
- **THEN** ses opérations restent liées à leurs mandats et à l'autorité PBO compétente
~~~~

### Référence pixs-agent--2706087935

Source : `openspec/specs/pixs-agent/spec.md`, ligne 209. SHA-256 du bloc : `0375ec260b62cb401a7dbb81be02385cb44193a19105a6bfb3c72b0bfd628d35`.

~~~~text
### Requirement: Publications locales expérimentales et sécurité de distribution

La première livraison envisagée MUST rester locale sur canal expérimental, avec capacités, versions, limites et preuves déclarées. Elle MUST satisfaire artifact-publication, notamment signature, provenance, inventaire, intégrité, immuabilité et révocation ; locale ou expérimentale MUST NOT dispenser de ces garanties ni autoriser une clé secrète dans un artefact. La présente formalisation MUST NOT construire, signer ou publier un artefact.

#### Scenario: Publications locales expérimentales et sécurité de distribution

- **WHEN** un artefact local expérimental ne dispose pas d'une signature admissible
- **THEN** il ne peut pas être déclaré publiable ou installable conformément à artifact-publication
~~~~

