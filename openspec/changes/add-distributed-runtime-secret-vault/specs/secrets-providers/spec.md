## ADDED Requirements

### Requirement: Séparation des secrets d’amorçage et d’exploitation distribuée

Une composition distribuée sélectionnée MUST distinguer le minimum local d’amorçage des secrets d’exploitation résolus par un coffre dédié indépendant de la base métier Pixs. L’ouverture et la récupération du coffre MUST NOT dépendre d’un secret détenu seulement dans la base qu’il doit permettre d’ouvrir. Une panne MUST NOT provoquer la copie durable implicite des secrets du coffre sur les hôtes.

#### Scenario: Credential nécessaire à la connexion PostgreSQL

- **WHEN** un service demande au coffre le credential nécessaire à sa connexion à la base métier Pixs
- **THEN** l’authentification initiale, l’ouverture et la récupération de ce coffre restent possibles sans lire préalablement cette base

#### Scenario: Réseau indisponible au démarrage

- **WHEN** le coffre n’est pas joignable pour une nouvelle résolution obligatoire
- **THEN** le service n’invente pas de stockage local de remplacement et reste non prêt pour la capacité concernée

### Requirement: Accès au coffre limité par service et périmètre

Le coffre MUST authentifier chaque workload et limiter son accès aux références, rôles, finalités et périmètres déclarés. Les services MUST NOT partager un credential d’administration global. Une identité d’amorçage MUST recevoir seulement les droits nécessaires à sa fonction et MUST NOT conférer une identité ou une autorité métier implicite.

#### Scenario: Worker demandant un secret réservé au web

- **WHEN** un worker authentifié demande une référence autorisée uniquement au rôle web
- **THEN** le coffre ou le provider refuse et audite la demande avant remise d’une valeur

#### Scenario: Jeton administrateur utilisé comme identité ordinaire

- **WHEN** la configuration propose le même jeton administrateur global pour les services applicatifs
- **THEN** la composition refuse cette configuration comme identité d’exploitation conforme

### Requirement: Baux courts et révocation des secrets du coffre

Le provider de coffre MUST utiliser des credentials courts lorsqu’ils sont compatibles et déclarer durée de vie, renouvellement, délai de révocation et traitement des copies consommées. Un renouvellement MUST revalider identité et politique courantes. Un cache ou une copie locale MUST NOT prolonger un bail, retarder la révocation au-delà du délai déclaré ou conserver un accès révoqué.

#### Scenario: Bail expiré sans renouvellement autorisé

- **WHEN** un credential arrive à expiration et que le coffre ne permet pas un renouvellement conforme
- **THEN** les nouvelles utilisations sont refusées et les consommateurs traitent les copies chargées selon leurs obligations de révocation et d’arrêt

#### Scenario: Révocation pendant une exécution

- **WHEN** un accès est révoqué alors qu’un service détient une copie de credential
- **THEN** le provider et le consommateur appliquent la borne de révocation prouvée sans la prolonger par leur cache ou un redémarrage non contrôlé

### Requirement: Protection du transport et des clés du coffre

Les communications réseau avec le coffre MUST vérifier son identité et protéger confidentialité et intégrité. Son stockage, ses sauvegardes et ses clés de déverrouillage MUST disposer de protections et d’accès explicitement déclarés et séparés. Les clés de déverrouillage MUST NOT être placées dans la base métier Pixs, les artefacts ou les journaux.

#### Scenario: Identité du coffre non vérifiable

- **WHEN** l’identité du serveur présenté ne correspond pas à la confiance déclarée ou ne peut pas être vérifiée
- **THEN** aucune valeur ni identité d’accès secrète n’est transmise à ce serveur et la résolution échoue fermée

#### Scenario: Sauvegarde du coffre sans mécanisme de récupération des clés

- **WHEN** la stratégie sauvegarde le stockage chiffré mais ne démontre pas la récupération protégée des clés nécessaires
- **THEN** elle ne revendique pas une capacité de restauration conforme du coffre

### Requirement: Indisponibilité du coffre sans repli implicite

Une nouvelle résolution obligatoire MUST échouer fermée si le coffre est indisponible. Un credential déjà délivré MAY rester utilisé uniquement dans ses bornes et sous les garanties de révocation démontrées. LDAP, la base métier Pixs, un fichier en clair ou un cache durable MUST NOT devenir un provider de remplacement implicite. Une garantie non tenue MUST empêcher la readiness concernée.

#### Scenario: Coupure avec bail encore valide

- **WHEN** une coupure interrompt l’accès au coffre alors qu’un service dispose d’un credential non expiré
- **THEN** son usage ne continue que si la politique et les garanties de révocation le permettent, sans renouvellement supposé ni prolongation de validité

#### Scenario: Limite de validité atteinte pendant la panne

- **WHEN** le délai applicable expire sans preuve permettant le maintien de l’accès
- **THEN** la capacité protégée cesse ses usages selon son contrat et ne bascule pas vers une copie locale ou une table métier

### Requirement: Audit minimisé des accès au coffre distribué

Les résolutions, refus, rotations et révocations du coffre MUST être corrélés à une identité de workload et à une référence selon les contrats d’audit applicables. Les preuves MUST NOT contenir de valeur, jeton ou clé. Un succès technique du coffre MUST NOT remplacer un reçu persistant requis avant remise au consommateur.

#### Scenario: Réponse du coffre sans preuve d’audit requise

- **WHEN** le coffre répond mais que le provider ne peut pas vérifier l’audit persistant imposé à cette résolution
- **THEN** aucune résolution conforme ni remise autorisée n’est annoncée par le provider

#### Scenario: Rapport d’exploitation du coffre

- **WHEN** un opérateur consulte les accès et rotations réalisés
- **THEN** il peut relier workload, référence et résultat sans obtenir les valeurs ni les credentials d’accès du coffre
