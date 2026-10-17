## RENAMED Requirements

- FROM: `### Requirement: États techniques PA distincts du runtime PBO`
- TO: `### Requirement: États techniques PA et PZT distincts du runtime PBO`

## MODIFIED Requirements

### Requirement: États techniques PA et PZT distincts du runtime PBO

PA et PZT MUST conserver des états techniques locaux distincts selon leurs
contrats, bornés, protégés et durables lorsque requis, sans autorité métier ni
stockage implicite du runtime PBO. Leurs états de reprise MUST NOT dépendre
du filesystem éphémère d'un conteneur. Leurs profils MUST déclarer propriétaires,
comptes, signaux, préconditions et séquencement d'arrêt sans lancer de rôle implicite.

#### Scenario: Recréation du conteneur PA PZT

- **WHEN** un conteneur PA/PZT est recréé
- **THEN** les exécutants reprennent depuis leurs stockages déclarés sans fusion des états ou autorité métier locale

## ADDED Requirements

### Requirement: Topologies locales et distantes PA PZT

Les profils MUST permettre la colivraison PA/PZT avec ou sans PBO/PFO locaux.
Un hôte distant MAY héberger aussi PBO/PFO ; cette présence MUST NOT accorder
un droit sur un autre exécutant. Chaque relation PBO–PA/PZT MUST déclarer
périmètre, autorité et contrats. Les échanges PBO–PA MUST toujours utiliser
PZT ; le contrôle PBO–PZT MUST conserver ses interfaces sécurisées.

#### Scenario: Hôte local avec tous les composants

- **WHEN** PBO/PFO, PA et PZT partagent un environnement d'exécution
- **THEN** pixs.agent gère PA hors PZT, pixs.pzt gère PZT et le profil local conserve les contrôles PZT

#### Scenario: Hôte distant sans backend local

- **WHEN** PA/PZT est déployé sur un hôte sans PBO/PFO
- **THEN** le PBO distant autorisé gère les exécutants par les contrats de pixs.agent et pixs.pzt via PZT

#### Scenario: Hôte distant avec backend local

- **WHEN** un hôte distant comprend PBO/PFO, PA et PZT
- **THEN** son PBO peut gérer les exécutants locaux ou distants dans ses seuls périmètres autorisés, sans priorité implicite sur un autre PBO
