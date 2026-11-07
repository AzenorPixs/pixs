## ADDED Requirements

### Requirement: Logiciel BIND 9 fourni dans Docker Pixs sans activation implicite

L'image Docker Pixs MUST fournir BIND 9 issu de Debian et ses dépendances identifiées. Cette présence MUST NOT activer le serveur sans application et supervision autorisées par le PA désigné. Version et image MUST être corrélées à la release et aux preuves de qualification. Les couches MUST NOT contenir de secret, clé privée ou état DNS propre à une instance.

#### Scenario: Image fournie avec service non sélectionné

- **WHEN** une image Pixs contenant BIND 9 est construite ou démarrée sans rôle serveur DNS sélectionné et admis
- **THEN** la présence du logiciel est vérifiable sans lancement ou disponibilité DNS implicites
- **AND** le choix BIND 9 MUST NOT autoriser implicitement un port, montage, utilisateur ou privilège supplémentaire

#### Scenario: État et secrets hors des couches

- **WHEN** la composition de l'image et les effets de l'installation du paquet sont contrôlés
- **THEN** aucune couche ne contient de clé privée, secret ou état DNS d'instance
- **AND** l'effacement dans une couche ultérieure n'est pas assimilé à l'absence de la donnée dans l'image

#### Scenario: Activation ultérieure contrôlée

- **WHEN** le rôle serveur DNS est ultérieurement sélectionné et admis dans le conteneur
- **THEN** le PA désigné applique et supervise le processus BIND 9 distinct avec les configurations et ressources effectivement autorisées
- **AND** configuration d'instance, données persistantes et références de secrets MUST suivre les plans et propriétaires du profil
- **AND** seul un résultat réel vérifié permet de déclarer état appliqué ou disponibilité
