## MODIFIED Requirements

### Requirement: Composition image PBO PFO deux binaires PA et PZT

L'image Pixs MUST toujours contenir le binaire PBO commun, les ressources PFO,
pixs.core, pixs.auth, pixs.agent, pixs.pzt, deux binaires PA — démon système et
événements du conteneur — et le
binaire indépendant PZT. Elle MUST NOT contenir le binaire utilisateur PA ni
ses modes session-start, session-stop et session-daemon. La séparation PA/PZT
MUST conserver trois exécutables hors PBO/PFO dans l'image.

#### Scenario: Inspection de l’image PA PZT

- **WHEN** le contenu de l’image est inspecté
- **THEN** PBO/PFO, pixs.agent, pixs.pzt, deux binaires PA et PZT sont présents et le binaire utilisateur PA est absent

## ADDED Requirements

### Requirement: Réplication des profils sous quotas du conteneur

L'image MUST livrer le binaire PBO commun Nuitka standalone avec ses ressources frontend et conserver les exécutants PA/PZT indépendants prévus. Chaque conteneur MUST sélectionner un rôle applicatif PBO explicite, avec processus et concurrence bornés selon runtime ; les réplicas et exécutants cohébergés MUST partager un budget contrôlé. La réplication MUST NOT cloner un propriétaire réseau ni une identité d'exécutant implicitement.

#### Scenario: Plusieurs conteneurs web

- **WHEN** plusieurs conteneurs lancent le rôle web depuis la même image
- **THEN** leurs budgets cumulés et connexions sont contrôlés, sans activation implicite des binaires PA/PZT présents dans l'image

#### Scenario: Ressources de l'hôte non accordées

- **WHEN** le serveur possède plus de CPU ou mémoire que le quota du conteneur
- **THEN** le dimensionnement respecte les limites accordées et les modes de session PA restent exclus
