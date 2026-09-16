## ADDED Requirements

### Requirement: Modes de démarrage explicites

Pixs MUST distinguer les modes INSTALLER, FIRST_CONFIGURATION, NORMAL et
MAINTENANCE. Le mode INSTALLER MUST être lancé explicitement et son éligibilité
MUST dépendre d'un marqueur externe à PostgreSQL. Un marqueur externe absent,
inaccessible, invalide ou incohérent MUST empêcher le démarrage NORMAL. Le
mode FIRST_CONFIGURATION MUST être déterminé par un état de configuration
initiale persisté en base, distinct du marqueur externe. Les transitions entre
modes MUST être explicites, autorisées et auditées.

#### Scenario: Marqueur externe indisponible

- **WHEN** Pixs ne peut pas valider le marqueur externe nécessaire au
  démarrage
- **THEN** il refuse le démarrage NORMAL sans relancer implicitement
  l'installateur

### Requirement: Provisionnement interactif de la base

Le mode INSTALLER MUST demander l'hôte ou IP PostgreSQL, le port avec `5432`
par défaut, l'identifiant, le mot de passe et le nom de base. Il MUST vérifier
la connectivité avant toute opération et MUST traiter la base demandée selon
son état : création confirmée si elle est absente, conservation si elle est
conforme, plan de migration confirmé si elle est migrable, ou suppression et
recréation confirmées si elle est incompatible. Les interruptions MUST être
reprenables sans état ambigu ni effet dupliqué. Après le provisionnement, les
valeurs de connexion PostgreSQL MUST être remplacées par des références
externes résolues par un `SecretProvider` autorisé ; elles MUST NOT être
persistées dans une configuration distribuée, un artefact, un diagnostic ou un
audit.

#### Scenario: Base migrable

- **WHEN** la base demandée nécessite une migration compatible
- **THEN** Pixs affiche le plan et n'applique la migration qu'après
  confirmation explicite

#### Scenario: Référence de secret après provisionnement

- **WHEN** le provisionnement PostgreSQL est terminé
- **THEN** le démarrage ultérieur utilise des références `SecretProvider` sans
  exposer ni persister les valeurs de connexion saisies

### Requirement: Création conditionnelle du Super Admin

Si le mode INSTALLER crée ou recrée une base, Pixs MUST demander un identifiant
de Super Admin et deux saisies identiques de son mot de passe. Il MUST créer le
compte dans la base comme identité numérique vérifiée de l'opérateur initial,
soumise à une politique d'autorisation déclarée, et stocker uniquement une
empreinte sécurisée du mot de passe. Il MUST NOT exposer ni journaliser les
valeurs saisies. Si une base conforme est conservée, Pixs MUST réutiliser les
comptes existants sans créer un second Super Admin.

#### Scenario: Mots de passe différents

- **WHEN** les deux saisies du mot de passe Super Admin diffèrent
- **THEN** le compte n'est pas créé et aucune valeur de mot de passe n'est
  exposée

#### Scenario: Opérateur initial vérifié

- **WHEN** le mode INSTALLER crée un Super Admin
- **THEN** il crée ou rattache une identité numérique vérifiée et applique la
  politique d'autorisation déclarée avant la mise en service

### Requirement: Marqueur externe et première configuration

Après un provisionnement réussi, Pixs MUST produire ou faire valider un
marqueur d'installation externe, définitif et indépendant de PostgreSQL. Avec
un marqueur externe valide et une configuration initiale non validée en base,
Pixs MUST démarrer en mode FIRST_CONFIGURATION, demander une connexion Super
Admin et réserver à ce compte la finalisation de la configuration. Une fois
validée, Pixs MUST démarrer en mode NORMAL.

#### Scenario: Configuration initiale inachevée

- **WHEN** le marqueur externe est valide mais la configuration initiale n'est
  pas validée en base
- **THEN** Pixs démarre en mode FIRST_CONFIGURATION et refuse sa finalisation
  par un compte autre que le Super Admin

### Requirement: Panneau d'administration contrôlé

Le panneau d'administration MUST être accessible initialement via `/admin/`.
Le Super Admin, ou root, MUST y disposer d'un accès total hors ACL. Les
Administrateurs ordinaires MUST être soumis aux ACL et permissions, et les
éléments non autorisés MUST NOT être visibles ou exécutables. Le Super Admin
MUST pouvoir modifier la route du panneau ; la nouvelle route MUST être interne
à Pixs, unique et sans collision. L'ancienne route MUST être refusée dès le
changement et sa tentative d'accès MUST être auditée.

#### Scenario: Ancienne route d'administration

- **WHEN** une requête vise l'ancienne route après son remplacement
- **THEN** Pixs la refuse et enregistre un événement d'audit sans credential

### Requirement: Expérience et état du panneau

Le panneau MUST afficher les états d'installation, de configuration et de
santé sans credential. Il MUST distinguer les informations de santé publiques,
celles accessibles aux Administrateurs et celles réservées au Super Admin. Il
MUST prendre en charge les thèmes clair et sombre, les langues configurées,
l'accessibilité, la navigation clavier, le responsive, la gestion de session
et la déconnexion.

#### Scenario: Santé réservée au root

- **WHEN** un Administrateur demande une information de santé réservée au
  Super Admin
- **THEN** l'information n'est pas exposée et la décision est auditée

### Requirement: Désactivation externe du Super Admin

Un marqueur externe, indépendant de PostgreSQL, MUST pouvoir désactiver le
Super Admin. Lorsqu'il est actif, Pixs MUST refuser toute connexion ou action
de ce compte ; les Administrateurs ordinaires MUST NOT pouvoir contourner ou
réactiver cette désactivation. La réactivation MUST relever exclusivement du
mécanisme externe autorisé.

#### Scenario: Connexion root désactivée

- **WHEN** le Super Admin est désactivé par le marqueur externe
- **THEN** sa connexion est refusée et l'événement est audité sans information
  sensible
