# docker-image Specification

## Purpose
L'image de conteneur est un mode de livraison corrélé à la release Pixs : reproductible, stateless, configurée à l'exécution et alignée sur les contrôles de santé et de cycle de vie du socle.

## Requirements

### Requirement: Composition reproductible corrélée à la release

La construction MUST être reproductible et l’image MUST identifier sa release, ses manifests, contrats et garanties dans le profil déclaré. Les capacités communes MUST rester corrélables aux autres artefacts. Les exclusions de fonctions de session décrites par cette capacité MUST NOT créer de divergence métier cachée ; base et outillage restent à qualifier.

#### Scenario: Deux constructions d'une même release

- **WHEN** la même release est construite deux fois dans des environnements conformes
- **THEN** l’identité vérifiable et les métadonnées restent cohérentes et corrélables

#### Scenario: Binaire utilisateur dans l’image

- **WHEN** la composition Docker inclut le binaire PA de sessions utilisateur
- **THEN** cette composition est refusée selon l’exigence des deux binaires PA système/événements et de PZT indépendant

### Requirement: Image sans état ni secret

L'image MUST NOT contenir de secret, de token, de clé privée, de configuration effective ni de données persistantes ; toute persistance MUST rester hors de l'image via les stockages déclarés.

#### Scenario: Valeur sensible dans l'image

- **WHEN** une analyse détecte une valeur sensible dans une couche ou une métadonnée de l'image
- **THEN** la publication est refusée avec un diagnostic n'exposant pas la valeur

### Requirement: Configuration validée à l'exécution

Le conteneur MUST recevoir sa configuration à l'exécution et la valider avant de passer à l'état de service ; il MUST NOT déduire fournisseur, tenant ou identité de l'état accidentel de l'image ou d'un système de fichiers éphémère.

#### Scenario: Démarrage avec configuration invalide

- **WHEN** un conteneur démarre avec une configuration incomplète ou invalide
- **THEN** il reste hors service avec une raison diagnostiquable au lieu de fonctionner dégradé silencieusement

### Requirement: Sondes alignées sur les états de santé

Les contrôles de santé du conteneur MUST être mappés sur les états distincts du socle et MUST NOT confondre vivacité et capacité à servir ; une dépendance optionnelle absente peut donner un état dégradé explicite, jamais une fausse disponibilité.

#### Scenario: Dépendance optionnelle indisponible

- **WHEN** une intégration optionnelle tombe dans un conteneur par ailleurs sain
- **THEN** la sonde d'exposition reflète l'état dégradé déclaré sans masquer une défaillance de sécurité

### Requirement: Arrêt propre et orchestration sans autorité

Le conteneur MUST gérer le signal d'arrêt par un drain contrôlé jusqu'à un état final explicite dans une durée bornée ; l'orchestrateur reste un adapter qui ne devient ni autorité métier ni substitut des validations de composition.

#### Scenario: Arrêt demandé pendant un traitement

- **WHEN** l'orchestrateur demande l'arrêt d'une instance en cours de traitement
- **THEN** l'instance draine selon son contrat et l'état persistant permet la reprise sans double effet

### Requirement: Composition image PBO PFO deux binaires PA et PZT

L'image Pixs MUST toujours contenir PBO/PFO, pixs.agent, le module essentiel
pixs.pzt, deux binaires PA — démon système et événements du conteneur — et le
binaire indépendant PZT. Elle MUST NOT contenir le binaire utilisateur PA ni
ses modes session-start, session-stop et session-daemon. La séparation PA/PZT
MUST conserver trois exécutables hors PBO/PFO dans l'image.

#### Scenario: Inspection de l’image PA PZT

- **WHEN** le contenu de l’image est inspecté
- **THEN** PBO/PFO, pixs.agent, pixs.pzt, deux binaires PA et PZT sont présents et le binaire utilisateur PA est absent

### Requirement: Événements PA limités au conteneur

Le binaire d’événements système dans Docker MUST traiter le démarrage et l’arrêt contrôlés du conteneur, sans gestion implicite de l’hôte. Présence des exécutables MUST NOT valoir activation du réseau, lancement implicite de tous les processus ou octroi de droits ; rôles, supervision et signaux MUST suivre le profil déclaré.

#### Scenario: Événements PA limités au conteneur

- **WHEN** le conteneur reçoit un arrêt
- **THEN** son événement PA reste borné au conteneur sans opération implicite sur l’hôte
