# pixs-instance Specification

## Purpose

L'Instance Pixs est l'ensemble logique commun aux PBO, aux individus Core et aux domaines, indépendant de leur déploiement.

Cible documentaire du cadrage validé du 31 octobre 2026 (PROJECT.md §45, TECHNICAL.md §46 et BUILD.md §49). Cette spécification ne constitue pas une implémentation ni une qualification de plateforme.

## Requirements

### Requirement: Identité logique et référentiel commun

L'Instance Pixs MUST posséder une identité stable distincte de ses PBO, processus, hôtes et ZT. Tous ses PBO MUST utiliser le même référentiel d'individus Core ; un nouveau PBO MUST NOT créer une liste concurrente d'individus.

#### Scenario: Ajout de PBO

- **WHEN** un second PBO est admis dans la même Instance
- **THEN** il référence les individus communs tout en conservant les données et responsabilités de ses modules.

### Requirement: Modes Standalone ZT et Domaine

L'Instance MUST distinguer Standalone sans Domaine et avec une application PBO logique éventuellement redondée, ZT sans Domaine avec un ZT d'Instance, et Domaine avec un ou plusieurs Domaines utilisant ZT. Plusieurs PBO fonctionnellement distincts MAY exister en ZT et Domaine. Ces modes MUST rester distincts de Nuitka standalone et de l'activation du transport PZT.

#### Scenario: Transport pré-domaine

- **WHEN** Standalone utilise PZT pour joindre PA
- **THEN** le mode reste Standalone et les contrôles réseau et applicatifs restent nécessaires.

#### Scenario: Mode ZT

- **WHEN** ZT est initialisé sans création de Domaine
- **THEN** le référentiel des individus et les données pré-domaine restent au niveau Instance.

### Requirement: ZT entièrement initialisé avant Domaine

La création du premier Domaine MUST exiger un mode ZT complètement initialisé, avec rôles essentiels opérationnels, identités, stockage et politiques vérifiés. Un état administratif créé ou un processus vivant MUST NOT suffire. La transition MUST être explicite et suivie durablement.

#### Scenario: ZT incomplet

- **WHEN** le rôle PKIZT essentiel manque lors de la demande du premier Domaine
- **THEN** la transition reste bloquée avec les capacités manquantes identifiées.

#### Scenario: Préconditions vérifiées

- **WHEN** le ZT et les autres préconditions de transition sont vérifiés
- **THEN** la procédure autorisée peut préparer puis activer le premier Domaine.

### Requirement: Minima et contrôleurs distincts

Chaque Instance MUST disposer d'au moins un PBO et un PA, déployés selon les environnements à administrer. Les contrôleurs d'Instance et de Domaine MUST être distingués du CZT. Leur regroupement ou séparation sur des PBO MUST être configurable sans fusion de bases ni habilitations.

#### Scenario: Contrôleurs regroupés

- **WHEN** un PBO assure les fonctions Instance et Domaine
- **THEN** les propriétaires des bases, identités et autorisations restent distincts.

### Requirement: Références PG avant et après Domaine

Avant le premier Domaine, PG Instance MUST porter individus, identités numériques, organigrammes Core, groupes, ACL et données métier pré-domaine. Après activation, PG Instance MUST conserver les individus et données communes sans identité numérique d'Instance ; les identités et données reprises MUST appartenir à PG du premier Domaine, avec identifiants et relations préservés.

#### Scenario: Activation du premier Domaine

- **WHEN** le transfert pré-domaine est confirmé
- **THEN** l’identité de Domaine devient utilisable selon son profil et l’ancienne identité d’Instance ne reste pas une autre voie de connexion.

### Requirement: Maintenance des écritures pour la transition

La transition pré-domaine vers Domaine MUST planifier une maintenance des écritures, vérifier données, relations et authentification cible et traiter toute issue inconnue avant reprise. Elle MUST NOT déclarer la bascule réussie sur un accusé de réception ou un seul effet technique PA.

#### Scenario: Interruption de transfert

- **WHEN** le résultat du transfert ou de son engagement est inconnu
- **THEN** la procédure réconcilie les états propriétaires avant toute répétition ou reprise des écritures.

### Requirement: Administration globale par identités habilitées

Après activation du premier Domaine, l'administration globale MUST utiliser des identités de Domaines explicitement habilitées. Plusieurs Domaines d'authentification MAY être autorisés. Une panne LDAP/Kerberos MAY être traitée par un profil PG Domaine explicitement autorisé et qualifié ; elle MUST NOT recréer d'identité numérique d'Instance ni réduire l'assurance exigée.

#### Scenario: Domaine d’authentification non habilité

- **WHEN** un utilisateur authentifié par un Domaine non habilité demande l’administration globale
- **THEN** la demande est refusée malgré la validité de son authentification.

### Requirement: Absence de retour Domaine Standalone V1

Après activation du premier Domaine, l'Instance MUST rester en mode Domaine en V1. Panne, restauration, retrait de domaine ou révocation MUST NOT provoquer un retour Standalone ou réactiver les anciennes identités. Les autres transitions inverses non spécifiées MUST NOT être introduites implicitement.

#### Scenario: Ancienne sauvegarde

- **WHEN** une reprise utilise des données antérieures à la transition
- **THEN** les contrôles empêchent de rétablir le mode et les identités Standalone devenus caducs.

### Requirement: Habilitations Instance et domaines

Les habilitations globales Instance et celles de chaque Domaine MUST être séparées et vérifiées. Le partage d'un PBO, PA, stockage physique ou réseau MUST NOT les transmettre implicitement.

#### Scenario: PBO mutualisé

- **WHEN** un administrateur d’un Domaine utilise un PBO servant plusieurs Domaines
- **THEN** son action reste limitée aux périmètres explicitement autorisés.
