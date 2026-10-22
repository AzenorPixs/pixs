## ADDED Requirements


### Requirement: PostgreSQL fourni et initialisation PA du profil Docker Pixs

L’image Docker Pixs MUST fournir le logiciel PostgreSQL sans cluster, secret ou données effectives embarqués. Le profil MUST sélectionner explicitement PA système, PZT local et PostgreSQL avec stockage persistant hors image et hors couche éphémère. PA MUST initialiser seulement les ressources manquantes, conserver l’existant et respecter les garanties de supervision, reprise et réplication ci-dessous.

#### Scenario: Garanties du profil Docker PostgreSQL

- **WHEN** le profil sélectionne cette capacité pour le parcours de préparation PostgreSQL
- **THEN** L'image Docker Pixs MUST fournir le logiciel PostgreSQL, sans cluster préinitialisé, configuration effective ni données métier intégrés aux couches. Le profil d'exécution MUST sélectionner explicitement PA système, PZT local et le service PostgreSQL cohébergé, avec supervision, ordre de démarrage, arrêt contrôlé et budgets de ressources communs déclarés ; la simple présence des binaires MUST NOT les activer. Les données PostgreSQL MUST résider dans un stockage persistant déclaré hors de l'image et de la couche éphémère du conteneur. PA MUST vérifier l'état réel de ce stockage, initialiser uniquement ce qui manque, puis préparer et contrôler le service avant les opérations propriétaires PBO. Un stockage existant MUST être conservé et une incompatibilité MUST rester non prête sans effacement automatique. L'image, un redémarrage ou une réplication MUST NOT créer de nouveau propriétaire de base, cloner une identité PA/PZT ou réinitialiser le cluster. Les réplicas MUST déclarer leur cible de persistance et un propriétaire admissible unique pour la préparation. Tous échanges PBO–PA MUST rester via PZT ; les permissions du conteneur MUST NOT être étendues implicitement à l'hôte.

#### Scenario: Premier démarrage Docker

- **WHEN** un conteneur reçoit un stockage persistant vide et un profil PA/PZT/PostgreSQL explicitement admis
- **THEN** PA prépare le cluster avec le logiciel déjà fourni et PBO conserve seul ses migrations et initialisations applicatives ; aucun secret n’est ajouté à l’image

#### Scenario: Redémarrage et réplication Docker

- **WHEN** un conteneur redémarre ou un réplica cible une base déjà initialisée
- **THEN** le stockage et ses données sont conservés, les identités et le propriétaire de préparation restent distincts et aucun second cluster n’est créé implicitement
