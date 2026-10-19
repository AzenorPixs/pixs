# initial-administration Specification

## Purpose

L'administration initiale encadre le provisionnement, les modes de démarrage,
le compte fonctionnel Super Admin, son exception explicite et le panneau
d'administration, avec préservation du régime des Administrateurs ordinaires.

## Requirements

### Requirement: Compte Super Admin unique de paramétrage et de secours

Chaque installation MUST disposer d'un seul compte Super Admin non nominatif, réservé au paramétrage et au secours. Ce compte MUST NOT être utilisé comme compte de service ni déléguer son exception à un autre compte. Son identité numérique MUST être explicitement distinguée des Administrateurs ordinaires.

#### Scenario: Compte fonctionnel non nominatif

- **WHEN** une installation provisionne son Super Admin
- **THEN** elle crée ou réutilise le compte fonctionnel unique sans exiger son rattachement nominatif à un utilisateur

#### Scenario: Second compte et transfert refusés

- **WHEN** une demande veut créer un second Super Admin, déléguer son exception ou utiliser ce compte comme compte de service
- **THEN** la demande est refusée même si elle provient du Super Admin

### Requirement: Exception liée au compte actif

L'exception du Super Admin MUST rester attachée à ce compte tant qu'il est actif ; elle MUST NOT exiger une élévation temporaire par opération. Son périmètre et sa priorité MUST suivre `authorization`. Les contrôles applicatifs de la présente capacité, audit compris, MUST être dérogeables selon cette exception.

#### Scenario: Privilège permanent du compte actif

- **WHEN** le Super Admin actif réalise une opération dans son périmètre autorisé
- **THEN** son exception est disponible sans activation d'une élévation temporaire

### Requirement: Absence de MFA obligatoire au démarrage et au secours

Le MFA MUST NOT être un prérequis au premier démarrage du Super Admin ni à sa réactivation de secours. Le compte MUST conserver une authentification propre ; l'exemption de MFA MUST NOT être présentée comme une authentification multifacteur effectivement réalisée.

#### Scenario: Premier démarrage sans MFA

- **WHEN** le compte Super Admin s'authentifie au premier démarrage sans MFA
- **THEN** l'absence de MFA ne bloque pas sa configuration initiale
- **AND** aucune assurance multifacteur non obtenue n'est annoncée

#### Scenario: Réactivation de secours sans MFA

- **WHEN** le compte Super Admin s'authentifie pour sa réactivation de secours sans MFA
- **THEN** l'absence de MFA ne bloque pas la réactivation

### Requirement: Modes de démarrage explicites

Pixs MUST distinguer les modes INSTALLER, FIRST_CONFIGURATION, NORMAL et
MAINTENANCE. Le mode INSTALLER MUST être lancé explicitement et son éligibilité
MUST dépendre d'un marqueur externe à PostgreSQL. Un marqueur externe absent,
inaccessible, invalide ou incohérent MUST empêcher le démarrage NORMAL.

#### Scenario: Marqueur externe indisponible

- **WHEN** Pixs ne peut pas valider le marqueur externe nécessaire au
  démarrage
- **THEN** il refuse le démarrage NORMAL sans relancer implicitement
  l'installateur

### Requirement: Première configuration et transitions de mode

Le
mode FIRST_CONFIGURATION MUST être déterminé par un état de configuration
initiale persisté en base, distinct du marqueur externe. Les transitions entre
modes MUST être explicites, autorisées et auditées.

#### Scenario: État initial en base distinct du marqueur

- **WHEN** Pixs détermine le mode FIRST_CONFIGURATION
- **THEN** il utilise l'état de configuration initiale persisté en base et les transitions de modes restent explicites, autorisées et auditées

### Requirement: Provisionnement interactif de la base

Le mode INSTALLER MUST demander l'hôte ou IP PostgreSQL, le port avec `5432`
par défaut, l'identifiant, le mot de passe et le nom de base. Il MUST vérifier
la connectivité avant toute opération et MUST traiter la base demandée selon
son état : création confirmée si elle est absente, conservation si elle est
conforme, plan de migration confirmé si elle est migrable, ou suppression et
recréation confirmées si elle est incompatible.

#### Scenario: Base migrable

- **WHEN** la base demandée nécessite une migration compatible
- **THEN** Pixs affiche le plan et n'applique la migration qu'après
  confirmation explicite

### Requirement: Reprise et références de secrets après provisionnement

Les interruptions MUST être
reprenables sans état ambigu ni effet dupliqué. Après le provisionnement, les
valeurs de connexion PostgreSQL MUST être remplacées par des références
externes résolues par un `SecretProvider` autorisé ; elles MUST NOT être
persistées dans une configuration distribuée, un artefact, un diagnostic ou un
audit.

#### Scenario: Référence de secret après provisionnement

- **WHEN** le provisionnement PostgreSQL est terminé
- **THEN** le démarrage ultérieur utilise des références `SecretProvider` sans
  exposer ni persister les valeurs de connexion saisies

### Requirement: Création conditionnelle du Super Admin

Si le mode INSTALLER crée ou recrée une base, Pixs MUST demander un identifiant
de Super Admin et deux saisies identiques de son mot de passe. Il MUST créer le
compte fonctionnel non nominatif dans la base avec une identité numérique
explicite et l'exception définie par `authorization`, et stocker uniquement une
empreinte sécurisée du mot de passe. Il MUST NOT exposer ni journaliser les
valeurs saisies.

#### Scenario: Mots de passe différents

- **WHEN** les deux saisies du mot de passe Super Admin diffèrent
- **THEN** le compte n'est pas créé et aucune valeur de mot de passe n'est
  exposée

#### Scenario: Compte fonctionnel créé explicitement

- **WHEN** le mode INSTALLER crée un Super Admin
- **THEN** il crée ou rattache l'identité numérique explicite du compte fonctionnel
  et applique son exception déclarée sans exiger un compte nominatif

### Requirement: Réutilisation du Super Admin d'une base conservée

Si une base conforme est conservée, Pixs MUST réutiliser le
Super Admin existant sans créer un second compte Super Admin.

#### Scenario: Base conforme conservée

- **WHEN** le mode INSTALLER conserve une base conforme
- **THEN** Pixs réutilise les comptes existants sans créer un second Super Admin

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
Le Super Admin, ou root, MUST y disposer du contrôle total défini par
`authorization`, avec accès explicite préalable à chaque tenant. Les
Administrateurs ordinaires MUST être soumis aux ACL et permissions, et les
éléments non autorisés MUST NOT être visibles ou exécutables.

#### Scenario: Administrateur ordinaire soumis aux ACL

- **WHEN** un Administrateur ordinaire utilise le panneau
- **THEN** ses accès restent soumis aux ACL et permissions et les éléments non autorisés ne sont ni visibles ni exécutables

### Requirement: Changement contrôlé de la route d'administration

Le Super Admin
MUST pouvoir modifier la route du panneau ; la nouvelle route MUST être
interne à Pixs, unique et sans collision. L'ancienne route MUST être refusée
dès le changement et sa tentative d'accès MUST être auditée.

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
Super Admin. Ce marqueur MUST être dérogeable par ce compte pour sa réactivation
de secours. Sans dérogation, les nouvelles connexions, actions et exécutions
différées MUST être refusées ; une transaction déjà engagée MUST pouvoir se
terminer. Les Administrateurs ordinaires MUST NOT contourner ou réactiver
cette désactivation.

#### Scenario: Connexion root désactivée

- **WHEN** le Super Admin est désactivé par le marqueur externe sans dérogation de désactivation ni d'audit
- **THEN** sa connexion est refusée et l'événement est audité sans information
  sensible

#### Scenario: Secours malgré le marqueur de désactivation

- **WHEN** le compte Super Admin s'authentifie et utilise sa dérogation au marqueur externe pour se réactiver en secours
- **THEN** le marqueur ne bloque pas cette réactivation et aucun MFA n'est exigé

#### Scenario: Transaction engagée lors de la désactivation

- **WHEN** une désactivation non dérogée intervient pendant une transaction du Super Admin
- **THEN** la transaction engagée peut se terminer
- **AND** les nouvelles actions et exécutions différées sont refusées tant que la désactivation s'applique sans dérogation

### Requirement: Opérateur technique INSTALLER avant base et sessions

La phase technique C01 MUST être lancée explicitement en mode INSTALLER et MUST authentifier son opérateur par identité OS et rattachement réel à l’unité autorisée, indépendamment de la base et des sessions Pixs. Elle MUST appliquer une politique de confiance versionnée à actions, références et finalités fermées, avec contexte PLATFORM et audit explicites. Une politique ou preuve manquante MUST refuser l’opération.

#### Scenario: Opérateur non vérifiable

- **WHEN** le processus ne peut pas démontrer son identité native ou la politique d’amorçage applicable
- **THEN** l’opération est refusée avant remise de secret et aucune mise en service n’est annoncée

#### Scenario: Root OS sans privilège applicatif implicite

- **WHEN** l’opérateur technique autorisé est root OS
- **THEN** cette identité reste technique et ne crée ni session ni exception Super Admin

### Requirement: Limites et refus de la phase technique INSTALLER

Cette phase MUST NOT provisionner de base, créer de DigitalIdentity, session ou compte Super Admin ni présumer les privilèges de ce compte ; ces réalisations restent du ressort de leurs contrats propriétaires.

#### Scenario: Opérateur non vérifiable

- **WHEN** le processus ne peut pas démontrer son identité native ou la politique d’amorçage applicable
- **THEN** l’opération est refusée avant remise de secret et aucune mise en service n’est annoncée

#### Scenario: Root OS sans privilège applicatif implicite

- **WHEN** l’opérateur technique autorisé est root OS
- **THEN** cette identité reste technique et ne crée ni session ni exception Super Admin
