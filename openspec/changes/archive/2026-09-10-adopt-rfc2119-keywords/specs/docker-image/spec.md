## MODIFIED Requirements

### Requirement: Composition reproductible corrélée à la release

La construction MUST être reproductible et l'image MUST identifier la release qu'elle livre, corrélable aux autres artefacts avec les mêmes composants, manifests, contrats et garanties ; la base et l'outillage de construction restent des détails non normatifs.

#### Scenario: Deux constructions d'une même release

- **WHEN** la même release est construite deux fois dans des environnements conformes
- **THEN** l'identité vérifiable de la livraison et ses métadonnées de release restent cohérentes et corrélables

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
