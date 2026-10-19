# Références normatives — X01

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| docker-image / 8 | [Composition reproductible corrélée à la release](../../specs/docker-image/spec.md#L8) | ND | CANDIDAT_DISTRIBUTION |
| docker-image / 22 | [Image sans état ni secret](../../specs/docker-image/spec.md#L22) | ND | CANDIDAT_DISTRIBUTION |
| docker-image / 31 | [Configuration validée à l'exécution](../../specs/docker-image/spec.md#L31) | ND | CANDIDAT_DISTRIBUTION |
| docker-image / 40 | [Sondes alignées sur les états de santé](../../specs/docker-image/spec.md#L40) | ND | CANDIDAT_DISTRIBUTION |
| docker-image / 49 | [Arrêt propre et orchestration sans autorité](../../specs/docker-image/spec.md#L49) | ND | CANDIDAT_DISTRIBUTION |
| docker-image / 58 | [Composition image PBO PFO et trois binaires PA](../../specs/docker-image/spec.md#L58) | ND | CANDIDAT_DISTRIBUTION |
| docker-image / 67 | [Événements PA limités au conteneur](../../specs/docker-image/spec.md#L67) | ND | CANDIDAT_DISTRIBUTION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence docker-image--eccd04c01b

Source : `openspec/specs/docker-image/spec.md`, ligne 8. SHA-256 du bloc : `26a434c02f066ab105de501c3639ec2efad7e21530b71b2df4d6beadfda1496c`.

~~~~text
### Requirement: Composition reproductible corrélée à la release

La construction MUST être reproductible et l’image MUST identifier sa release, ses manifests, contrats et garanties dans le profil déclaré. Les capacités communes MUST rester corrélables aux autres artefacts. Les exclusions de fonctions de session décrites par cette capacité MUST NOT créer de divergence métier cachée ; base et outillage restent à qualifier.

#### Scenario: Deux constructions d'une même release

- **WHEN** la même release est construite deux fois dans des environnements conformes
- **THEN** l’identité vérifiable et les métadonnées restent cohérentes et corrélables

#### Scenario: Binaire utilisateur dans l’image

- **WHEN** la composition Docker inclut le binaire PA de sessions utilisateur
- **THEN** cette composition est refusée selon l’exigence des trois binaires système PZT
~~~~

### Référence docker-image--514331ad94

Source : `openspec/specs/docker-image/spec.md`, ligne 22. SHA-256 du bloc : `5974b07e2b5a54c8239a477d8e7e809fc8d874f12ac5840107a6780c2b22adf2`.

~~~~text
### Requirement: Image sans état ni secret

L'image MUST NOT contenir de secret, de token, de clé privée, de configuration effective ni de données persistantes ; toute persistance MUST rester hors de l'image via les stockages déclarés.

#### Scenario: Valeur sensible dans l'image

- **WHEN** une analyse détecte une valeur sensible dans une couche ou une métadonnée de l'image
- **THEN** la publication est refusée avec un diagnostic n'exposant pas la valeur
~~~~

### Référence docker-image--9fc683d3ec

Source : `openspec/specs/docker-image/spec.md`, ligne 31. SHA-256 du bloc : `a671f2f8947c154811f74235f744614b0dc1b4bd67e70150a3899c65aac1e295`.

~~~~text
### Requirement: Configuration validée à l'exécution

Le conteneur MUST recevoir sa configuration à l'exécution et la valider avant de passer à l'état de service ; il MUST NOT déduire fournisseur, tenant ou identité de l'état accidentel de l'image ou d'un système de fichiers éphémère.

#### Scenario: Démarrage avec configuration invalide

- **WHEN** un conteneur démarre avec une configuration incomplète ou invalide
- **THEN** il reste hors service avec une raison diagnostiquable au lieu de fonctionner dégradé silencieusement
~~~~

### Référence docker-image--67581165b1

Source : `openspec/specs/docker-image/spec.md`, ligne 40. SHA-256 du bloc : `a4efa5dab25ddc0f3cbba7953ebe0681f906e2e005fa399e522be1cfd7b606b6`.

~~~~text
### Requirement: Sondes alignées sur les états de santé

Les contrôles de santé du conteneur MUST être mappés sur les états distincts du socle et MUST NOT confondre vivacité et capacité à servir ; une dépendance optionnelle absente peut donner un état dégradé explicite, jamais une fausse disponibilité.

#### Scenario: Dépendance optionnelle indisponible

- **WHEN** une intégration optionnelle tombe dans un conteneur par ailleurs sain
- **THEN** la sonde d'exposition reflète l'état dégradé déclaré sans masquer une défaillance de sécurité
~~~~

### Référence docker-image--9b574db47f

Source : `openspec/specs/docker-image/spec.md`, ligne 49. SHA-256 du bloc : `82ad41afe40b83351156f395b3d52ddbfa880371520579dad7c624da84e4b516`.

~~~~text
### Requirement: Arrêt propre et orchestration sans autorité

Le conteneur MUST gérer le signal d'arrêt par un drain contrôlé jusqu'à un état final explicite dans une durée bornée ; l'orchestrateur reste un adapter qui ne devient ni autorité métier ni substitut des validations de composition.

#### Scenario: Arrêt demandé pendant un traitement

- **WHEN** l'orchestrateur demande l'arrêt d'une instance en cours de traitement
- **THEN** l'instance draine selon son contrat et l'état persistant permet la reprise sans double effet
~~~~

### Référence docker-image--a25571dc18

Source : `openspec/specs/docker-image/spec.md`, ligne 58. SHA-256 du bloc : `543b7c1ef253e674df6299fae94b3348f7fadf5961ed804581b5afaf3c413b23`.

~~~~text
### Requirement: Composition image PBO PFO et trois binaires PA

L’image Pixs MUST toujours contenir PBO, PFO, le module essentiel PZT côté PBO et exactement trois binaires PA : démon système, événements système du conteneur et exécution PZT. Elle MUST NOT contenir le binaire utilisateur PA ni ses modes session-start, session-stop et session-daemon.

#### Scenario: Composition image PBO PFO et trois binaires PA

- **WHEN** le contenu de l’image est inspecté
- **THEN** PBO/PFO et trois binaires PA sont présents et le binaire utilisateur est absent
~~~~

### Référence docker-image--bd24717e3a

Source : `openspec/specs/docker-image/spec.md`, ligne 67. SHA-256 du bloc : `67e439783126ef0a8a06f6fccd1b23f938cf3c990e477a02c907cfa37598baab`.

~~~~text
### Requirement: Événements PA limités au conteneur

Le binaire d’événements système dans Docker MUST traiter le démarrage et l’arrêt contrôlés du conteneur, sans gestion implicite de l’hôte. Présence des exécutables MUST NOT valoir activation du réseau, lancement implicite de tous les processus ou octroi de droits ; rôles, supervision et signaux MUST suivre le profil déclaré.

#### Scenario: Événements PA limités au conteneur

- **WHEN** le conteneur reçoit un arrêt
- **THEN** son événement PA reste borné au conteneur sans opération implicite sur l’hôte
~~~~

