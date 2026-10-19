## RENAMED Requirements

- FROM: `### Requirement: Composition image PBO PFO et trois binaires PA`
- TO: `### Requirement: Composition image PBO PFO deux binaires PA et PZT`

## MODIFIED Requirements

### Requirement: Composition reproductible corrélée à la release

La construction MUST être reproductible et l’image MUST identifier sa release, ses manifests, contrats et garanties dans le profil déclaré. Les capacités communes MUST rester corrélables aux autres artefacts. Les exclusions de fonctions de session décrites par cette capacité MUST NOT créer de divergence métier cachée ; base et outillage restent à qualifier.

#### Scenario: Deux constructions d'une même release

- **WHEN** la même release est construite deux fois dans des environnements conformes
- **THEN** l’identité vérifiable et les métadonnées restent cohérentes et corrélables

#### Scenario: Binaire utilisateur dans l’image

- **WHEN** la composition Docker inclut le binaire PA de sessions utilisateur
- **THEN** cette composition est refusée selon l’exigence des deux binaires PA système/événements et de PZT indépendant

### Requirement: Composition image PBO PFO deux binaires PA et PZT

L'image Pixs MUST toujours contenir PBO/PFO, pixs.agent, le module essentiel
pixs.pzt, deux binaires PA — démon système et événements du conteneur — et le
binaire indépendant PZT. Elle MUST NOT contenir le binaire utilisateur PA ni
ses modes session-start, session-stop et session-daemon. La séparation PA/PZT
MUST conserver trois exécutables hors PBO/PFO dans l'image.

#### Scenario: Inspection de l’image PA PZT

- **WHEN** le contenu de l’image est inspecté
- **THEN** PBO/PFO, pixs.agent, pixs.pzt, deux binaires PA et PZT sont présents et le binaire utilisateur PA est absent
