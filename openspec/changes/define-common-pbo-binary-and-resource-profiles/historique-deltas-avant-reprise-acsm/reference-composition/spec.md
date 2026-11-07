## ADDED Requirements

### Requirement: Qualification du binaire commun et des profils de ressources P0

Le profil initial PBO MUST qualifier le binaire commun Kernel/Core/Auth/Agent/PZT et ses ressources selon reference-runtime et runtime. Il MUST sélectionner et qualifier PA système/PZT local pour préparer PostgreSQL, sans activation déduite de la présence des modules ni confusion avec le réseau distant. La preuve MUST respecter les garanties détaillées du scénario ci-dessous.

#### Scenario: Garanties de qualification du parcours initial PA PZT

- **WHEN** le profil initial PBO et son parcours de préparation PostgreSQL sont évalués
- **THEN** Le profil initial PBO MUST qualifier le binaire commun Kernel/Core/Auth/Agent/PZT et son plan de processus selon reference-runtime et runtime. La preuve MUST relier budgets accordés, configuration demandée, état appliqué, mesures et scénarios de panne. Les modules essentiels MUST rester composés et leur présence MUST NOT valoir activation. Le parcours initial de préparation PostgreSQL par PA MUST sélectionner explicitement les exécutants PA système et PZT local avec leurs profils propres à qualifier ; une absence de réseau distant MUST NOT être confondue avec l'absence de ce transport local obligatoire.

#### Scenario: P0 sans exécution réseau

- **WHEN** le profil initial conserve le réseau désactivé
- **THEN** les modules essentiels restent présents dans le binaire PBO et aucun exécutant PA/PZT ni résultat réseau n'est inventé
- **AND** l’absence de PZT local empêche de qualifier le parcours de préparation PostgreSQL par PA

#### Scenario: P0 sans réseau distant

- **WHEN** le profil initial sélectionne la préparation PostgreSQL par PA sans réseau distant
- **THEN** les modules essentiels et les exécutants PA système/PZT local nécessaires sont explicitement sélectionnés et qualifiés sans revendiquer de résultat de réseau distant

#### Scenario: Plan de ressources sans preuve sur cible

- **WHEN** une composition P0 possède un plan mais pas de recette sur l'environnement distribué
- **THEN** elle ne revendique pas un binaire ou un dimensionnement qualifié sur cette seule déclaration
