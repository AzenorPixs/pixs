## MODIFIED Requirements

### Requirement: Composition reproductible corrélée à la release

La construction MUST être reproductible et l’image MUST identifier sa release, ses manifests, contrats et garanties dans le profil déclaré. Les capacités communes MUST rester corrélables aux autres artefacts. Les exclusions de fonctions de session décrites par cette capacité MUST NOT créer de divergence métier cachée ; base et outillage restent à qualifier.

#### Scenario: Deux constructions d'une même release

- **WHEN** la même release est construite deux fois dans des environnements conformes
- **THEN** l’identité vérifiable et les métadonnées restent cohérentes et corrélables

#### Scenario: Binaire utilisateur dans l’image

- **WHEN** la composition Docker inclut le binaire PA de sessions utilisateur
- **THEN** cette composition est refusée selon l’exigence des trois binaires système PZT

## ADDED Requirements

### Requirement: Composition image PBO PFO et trois binaires PA

L’image Pixs MUST toujours contenir PBO, PFO, le module essentiel PZT côté PBO et exactement trois binaires PA : démon système, événements système du conteneur et exécution PZT. Elle MUST NOT contenir le binaire utilisateur PA ni ses modes session-start, session-stop et session-daemon.

#### Scenario: Composition image PBO PFO et trois binaires PA

- **WHEN** le contenu de l’image est inspecté
- **THEN** PBO/PFO et trois binaires PA sont présents et le binaire utilisateur est absent

### Requirement: Événements PA limités au conteneur

Le binaire d’événements système dans Docker MUST traiter le démarrage et l’arrêt contrôlés du conteneur, sans gestion implicite de l’hôte. Présence des exécutables MUST NOT valoir activation du réseau, lancement implicite de tous les processus ou octroi de droits ; rôles, supervision et signaux MUST suivre le profil déclaré.

#### Scenario: Événements PA limités au conteneur

- **WHEN** le conteneur reçoit un arrêt
- **THEN** son événement PA reste borné au conteneur sans opération implicite sur l’hôte
