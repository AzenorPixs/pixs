# Exigences de réalisation — C16

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| backup-disaster-recovery | Stratégie déclarée par déploiement | 1 | backup-disaster-recovery-ce55a3a23d95 |
| backup-disaster-recovery | Périmètres de sauvegarde distincts | 1 | backup-disaster-recovery-789b1b8e93e1 |
| backup-disaster-recovery | Restauration cohérente et réapplication des gouvernances | 1 | backup-disaster-recovery-66c296260a74 |
| backup-disaster-recovery | Tests de restauration isolés et preuves | 1 | backup-disaster-recovery-b161a98dd98c |
| backup-disaster-recovery | Restauration destructive autorisée et auditée | 1 | backup-disaster-recovery-d53211ddf75b |
| backup-disaster-recovery | Déclenchement et périmètres de restauration | 1 | backup-disaster-recovery-48771dfc3645 |
| backup-disaster-recovery | État PG LDAP Kerberos et clés de reprise | 2 | backup-disaster-recovery-29ed52b25f69 |
| brick-redundancy | Remplacement sans déplacement direct | 1 | brick-redundancy-ce67ff7e1fde |
| brick-redundancy | Mode par famille et exceptions | 1 | brick-redundancy-78e23fa4ab8f |
| brick-redundancy | Conditions de reprise propres à la brique | 1 | brick-redundancy-29e8a1e997e2 |
| brick-redundancy | Unicité de l’autorité et automatisation | 1 | brick-redundancy-b7eb34bb70c2 |
| brick-redundancy | Observation et démantèlement | 1 | brick-redundancy-8df77aef5446 |
| brick-redundancy | Compatibilité de versions par famille | 1 | brick-redundancy-73cbc72a8e34 |
| brick-redundancy | Références PostgreSQL répliquées et garanties conservées | 1 | brick-redundancy-9c403ec6ed51 |
| pixs-instance | Identité logique et référentiel commun | 1 | pixs-instance-b9b134df059f |
| pixs-instance | Modes Standalone ZT et Domaine | 2 | pixs-instance-18485b8d2051 |
| pixs-instance | ZT entièrement initialisé avant Domaine | 2 | pixs-instance-81a8ae9c0556 |
| pixs-instance | Minima et contrôleurs distincts | 1 | pixs-instance-b189f9cd6424 |
| pixs-instance | Références PG avant et après Domaine | 1 | pixs-instance-9baefb0c5ae7 |
| pixs-instance | Maintenance des écritures pour la transition | 1 | pixs-instance-ebdd233f14af |
| pixs-instance | Administration globale par identités habilitées | 1 | pixs-instance-8c964dc84f92 |
| pixs-instance | Absence de retour Domaine Standalone V1 | 1 | pixs-instance-c159a59d2125 |
| pixs-instance | Habilitations Instance et domaines | 1 | pixs-instance-b7a2b5d23968 |
| auth-managed-kerberos | KZT obligatoire et backend OpenLDAP | 1 | auth-managed-kerberos-050d7fe34c83 |
| auth-managed-kerberos | Realm propre et mappings explicites | 1 | auth-managed-kerberos-7bb78778c4c7 |
| auth-managed-kerberos | Protection et récupération des clés Kerberos | 1 | auth-managed-kerberos-1760917ff34e |
| auth-managed-kerberos | Verrouillage cohérent du realm | 1 | auth-managed-kerberos-255d8bbfe611 |
| auth-managed-kerberos | Provisionnement progressif par profil | 1 | auth-managed-kerberos-1c0f0ee90eed |
| auth-managed-kerberos | Expiration stricte et état courant | 1 | auth-managed-kerberos-551806d8cd3f |
| auth-managed-kerberos | Temps et confiance inter-realms | 1 | auth-managed-kerberos-72a422092c18 |
| auth-managed-kerberos | Restauration sans résurrection | 1 | auth-managed-kerberos-2916ffe1ae32 |
| auth-managed-kerberos | Reconstruction complète en urgence critique | 3 | auth-managed-kerberos-9dec834a75dd |
| auth-managed-kerberos | État critique distinct du mode d'exploitation | 1 | auth-managed-kerberos-3ea4c587f7b3 |

### Référence courante backup-disaster-recovery-ce55a3a23d95

Source : [backup-disaster-recovery](../../specs/backup-disaster-recovery/spec.md), ligne 8. SHA-256 : `ce55a3a23d959aed0c1c5aa20ea3b289997878f1302cf872ee5fd012423f360c`.

Scénarios : Procédure sans objectifs déclarés.

~~~~text
### Requirement: Stratégie déclarée par déploiement

Le déploiement MUST définir ses objectifs de perte et de délai de reprise acceptables, son périmètre, ses durées de conservation, ses contrôles d'accès, ses procédures de restauration et la preuve attendue après restauration ; le socle n'impose aucun outil particulier.

#### Scenario: Procédure sans objectifs déclarés

- **WHEN** une procédure de restauration est demandée sur un déploiement sans objectifs déclarés
- **THEN** l'écart est signalé et la couverture de reprise ne peut être certifiée
~~~~

### Référence courante backup-disaster-recovery-789b1b8e93e1

Source : [backup-disaster-recovery](../../specs/backup-disaster-recovery/spec.md), ligne 17. SHA-256 : `789b1b8e93e13ea6ce6fe80c0ab8fd4e2d428341bbcb3df5fa360a5a75c0d09b`.

Scénarios : Sauvegarde partielle.

~~~~text
### Requirement: Périmètres de sauvegarde distincts

La stratégie MUST couvrir séparément les données persistantes avec leurs états de traitement, les objets et fichiers avec versions, rétentions et sommes de contrôle, et la configuration avec les références de secrets et leurs mécanismes de rotation ; une sauvegarde MUST NOT devenir une nouvelle source d'autorité.

#### Scenario: Sauvegarde partielle

- **WHEN** un périmètre n'est pas couvert par la sauvegarde invoquée
- **THEN** la reprise est déclarée incomplète avec le périmètre manquant identifié
~~~~

### Référence courante backup-disaster-recovery-66c296260a74

Source : [backup-disaster-recovery](../../specs/backup-disaster-recovery/spec.md), ligne 26. SHA-256 : `66c296260a74a7b49c28ce9f95b38d60b6e93f02802bc9b5e67f1bdd13b928a2`.

Scénarios : Objet restauré après suppression validée.

~~~~text
### Requirement: Restauration cohérente et réapplication des gouvernances

Une restauration MUST vérifier la cohérence entre métadonnées, objets, événements non publiés, travaux, points de contrôle, mappings externes et versions de composants, et réappliquer les marqueurs de suppression, le journal d'effacement, les restrictions légales et les états de rétention avant toute exposition aux utilisateurs ou aux synchronisations.

#### Scenario: Objet restauré après suppression validée

- **WHEN** un objet restauré contredit une suppression déjà validée
- **THEN** la divergence est bloquée ou rendue explicite et auditable, sans annulation silencieuse
~~~~

### Référence courante backup-disaster-recovery-b161a98dd98c

Source : [backup-disaster-recovery](../../specs/backup-disaster-recovery/spec.md), ligne 35. SHA-256 : `b161a98dd98c06e8604e1a941ced0c458daa2ccf67e5510a5f4b2970a99271f0`.

Scénarios : Démarrage après restauration.

~~~~text
### Requirement: Tests de restauration isolés et preuves

Les restaurations MUST être exécutables dans un environnement isolé, testées régulièrement, et produire une preuve conservée ; après restauration le système MUST démarrer en état contrôlé, détecter les écarts de composition ou de version et reprendre les traitements idempotents.

#### Scenario: Démarrage après restauration

- **WHEN** une instance démarre depuis une restauration testée
- **THEN** les traitements non confirmés restent dans un état diagnostiquable sans réémission automatique
~~~~

### Référence courante backup-disaster-recovery-d53211ddf75b

Source : [backup-disaster-recovery](../../specs/backup-disaster-recovery/spec.md), ligne 44. SHA-256 : `d53211ddf75b4ac08d27cd6f4a1390fd6c093fc96632b022c8e6d69c8568e878`.

Scénarios : Suppression implicite refusée.

~~~~text
### Requirement: Restauration destructive autorisée et auditée

Une restauration destructive ou un retour à un point antérieur MUST être une opération explicitement autorisée, confirmée et auditée ; une purge implicite d'identités, tenants, autorisations, secrets ou données métier MUST NOT être tolérée pour rendre la restauration possible.

#### Scenario: Suppression implicite refusée

- **WHEN** une procédure propose de réinitialiser des données pour faciliter la restauration
- **THEN** elle est refusée hors opération autorisée distincte avec audit propre
~~~~

### Référence courante backup-disaster-recovery-48771dfc3645

Source : [backup-disaster-recovery](../../specs/backup-disaster-recovery/spec.md), ligne 53. SHA-256 : `48771dfc3645fb2cdd82d04e9c02debf3cc25038f8d69d71567ed09fb679f9d2`.

Scénarios : Restauration de Domaine.

~~~~text
### Requirement: Déclenchement et périmètres de restauration

Les sauvegardes MUST pouvoir être manuelles ou automatiques selon les profils et toutes MUST être chiffrées. Les restaurations MUST être déclenchées manuellement par un acteur habilité et MAY cibler Instance, Domaine ou composant après vérification des dépendances. Leur lieu ou nombre de copies MUST suivre les protections déjà applicables, sans nouvelle règle déduite de cette consolidation.

#### Scenario: Restauration de Domaine

- **WHEN** une restauration ciblée est demandée
- **THEN** les références Instance, le ZT utilisé et les dépendances des composants sont contrôlés avant réadmission.
~~~~

### Référence courante backup-disaster-recovery-29ed52b25f69

Source : [backup-disaster-recovery](../../specs/backup-disaster-recovery/spec.md), ligne 62. SHA-256 : `29ed52b25f6910cc032f78951614de97c2acc02b821c7d086aca9b1ae8a9e85d`.

Scénarios : Sauvegarde complète exploitable; PG seule disponible.

~~~~text
### Requirement: État PG LDAP Kerberos et clés de reprise

Les sauvegardes MUST couvrir PG souveraine pour les références Pixs et l'état Kerberos durable normal dans LDAP, avec ses moyens protégés de reprise. Le mode critique MUST prévoir restauration LDAP/Kerberos puis réconciliation, ou reconstruction depuis PG avec clés/reprovisionnement selon profil et copies disponibles. La reprise MUST NOT réintroduire un droit retiré ni rétablir Standalone après Domaine.

#### Scenario: Sauvegarde complète exploitable

- **WHEN** le profil critique dispose des sauvegardes protégées et moyens requis
- **THEN** il restaure les états puis vérifie leur cohérence avec les références et retraits courants.

#### Scenario: PG seule disponible

- **WHEN** l’état Kerberos normal est perdu sans sauvegarde exploitable
- **THEN** le profil critique peut reconstruire les références depuis PG mais recrée les clés et reprovisionne les accès nécessaires sans continuité fictive des anciens moyens.
~~~~

### Référence courante brick-redundancy-ce67ff7e1fde

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 11. SHA-256 : `ce67ff7e1fde4ca9f4b7ad0badf7054c4e1fe46c1db73b174b19e30bd470ee1a`.

Scénarios : Second PZT.

~~~~text
### Requirement: Remplacement sans déplacement direct

Une brique MUST être remplacée par initialisation d'une seconde brique identifiée, synchronisation, vérification puis activation/reprise avant démantèlement selon ses critères. La procédure MUST NOT déplacer implicitement le processus ou copier l'identité d'un nouveau membre.

#### Scenario: Second PZT

- **WHEN** un PZT supplémentaire est initialisé pour remplacer un rôle
- **THEN** il reçoit son identité et son admission propres avant de reprendre le rôle autorisé.
~~~~

### Référence courante brick-redundancy-78e23fa4ab8f

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 20. SHA-256 : `78e23fa4ab8fa0bb63d03ef7d2eed6192c067b88caebb136646f31b66c88d7e2`.

Scénarios : Exception au mode.

~~~~text
### Requirement: Mode par famille et exceptions

Chaque famille MUST définir son mode d'autorité et de synchronisation par défaut. Une brique MAY y déroger par configuration explicite ; une exception incompatible avec le mode de famille MUST être justifiée et tracée. La dérogation MUST NOT supprimer une garantie spécifique obligatoire du rôle.

#### Scenario: Exception au mode

- **WHEN** un administrateur propose une exception de mode
- **THEN** sa justification, sa portée et ses contrôles sont enregistrés avant admission.
~~~~

### Référence courante brick-redundancy-29e8a1e997e2

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 29. SHA-256 : `29e8a1e997e28be127916e1f936f38f70b6562b68b46d5dab57cff4629b3a465`.

Scénarios : Copies requises absentes.

~~~~text
### Requirement: Conditions de reprise propres à la brique

Chaque brique MUST déclarer ses exigences de synchronisation et l'éventuel état partiel admissible avec limites explicites. La procédure MUST vérifier les critères courants avant activation. La règle générale MUST NOT abaisser le minimum PG synchrone ni permettre la perte d'une écriture confirmée dans un profil qui la protège.

#### Scenario: Copies requises absentes

- **WHEN** une reprise CZT ne satisfait pas son minimum synchrone configuré
- **THEN** la règle générale d’état partiel ne permet pas de la confirmer.
~~~~

### Référence courante brick-redundancy-b7eb34bb70c2

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 38. SHA-256 : `b7eb34bb70c29f74664bbd69e8874a6819b8e6ecf8a60cc8c2626164191d7f65`.

Scénarios : Ancien maître isolé.

~~~~text
### Requirement: Unicité de l’autorité et automatisation

Un rôle à maître unique MUST empêcher l'ancien et le nouveau maître d'exercer simultanément. La reprise MAY être automatique sous politique et mandat préalablement autorisés ; sinon un administrateur MUST confirmer. Une injoignabilité seule MUST NOT prouver l'exclusion.

#### Scenario: Ancien maître isolé

- **WHEN** l’ancien maître est injoignable mais son exclusion n’est pas démontrée
- **THEN** la prise d’autorité reste bloquée selon le contrat du rôle.
~~~~

### Référence courante brick-redundancy-8df77aef5446

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 47. SHA-256 : `8df77aef54469a86d9737a29a58a9b52c8f4fc211a4ac422a8bb6a1a5f8b9175`.

Scénarios : Nouvel actif non vérifié.

~~~~text
### Requirement: Observation et démantèlement

Chaque brique MUST définir la vérification du nouvel actif, l'éventuelle période d'observation, le statut de l'ancienne et ses critères de démantèlement. L'ancienne MAY rester secours passif, copie de retrait ou autre état déclaré ; elle MUST NOT reprendre des droits expirés ou révoqués.

#### Scenario: Nouvel actif non vérifié

- **WHEN** le service de remplacement n’a pas satisfait les contrôles
- **THEN** le démantèlement n’est pas autorisé sur sa seule activation administrative.
~~~~

### Référence courante brick-redundancy-73cbc72a8e34

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 56. SHA-256 : `73cbc72a8e34d14d7ef69dc78d17ffb7d5f3c0e0fcfd1898d8a241e4867f752c`.

Scénarios : Versions hors plage.

~~~~text
### Requirement: Compatibilité de versions par famille

Chaque famille MUST déclarer si des versions identiques sont requises ou si une plage de compatibilité est admise. Une paire non qualifiée MUST être refusée pour synchronisation/reprise ; la présence des binaires MUST NOT prouver la compatibilité.

#### Scenario: Versions hors plage

- **WHEN** une réplique est installée dans une version non admise
- **THEN** la synchronisation protégée ou la reprise concernée reste bloquée avec diagnostic.
~~~~

### Référence courante brick-redundancy-9c403ec6ed51

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 65. SHA-256 : `9c403ec6ed51a5c3ebdc3db0b60ff70c1382311adacdd6a3fc42fdc997c6fd23`.

Scénarios : Copies distinctes.

~~~~text
### Requirement: Références PostgreSQL répliquées et garanties conservées

Les bases PG Instance, Domaine, CZT, DZT et PKIZT MUST pouvoir disposer de répliques synchrones avec un primaire d'écriture unique. Leur minimum de confirmations MUST être configurable sans réduction automatique en panne ; promotion MUST exclure l'ancien primaire et préserver les écritures confirmées. Une réplication MUST rester celle d'une même base logique sans fusion de Domaines.

#### Scenario: Copies distinctes

- **WHEN** deux PG de Domaines différents sont déclarées
- **THEN** elles ne deviennent pas répliques d’une même base par partage de serveur ou de ZT.
~~~~

### Référence courante pixs-instance-b9b134df059f

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 11. SHA-256 : `b9b134df059f8bf6661d4623bae95e040e6f1461c35dd19d5d91ec4cd68c99bc`.

Scénarios : Ajout de PBO.

~~~~text
### Requirement: Identité logique et référentiel commun

L'Instance Pixs MUST posséder une identité stable distincte de ses PBO, processus, hôtes et ZT. Tous ses PBO MUST utiliser le même référentiel d'individus Core ; un nouveau PBO MUST NOT créer une liste concurrente d'individus.

#### Scenario: Ajout de PBO

- **WHEN** un second PBO est admis dans la même Instance
- **THEN** il référence les individus communs tout en conservant les données et responsabilités de ses modules.
~~~~

### Référence courante pixs-instance-18485b8d2051

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 20. SHA-256 : `18485b8d20510d544246b6d9c7efd51c9479aedb4fd4f839499c3e12bed5f82b`.

Scénarios : Transport pré-domaine; Mode ZT.

~~~~text
### Requirement: Modes Standalone ZT et Domaine

L'Instance MUST distinguer Standalone sans Domaine et avec une application PBO logique éventuellement redondée, ZT sans Domaine avec un ZT d'Instance, et Domaine avec un ou plusieurs Domaines utilisant ZT. Plusieurs PBO fonctionnellement distincts MAY exister en ZT et Domaine. Ces modes MUST rester distincts de Nuitka standalone et de l'activation du transport PZT.

#### Scenario: Transport pré-domaine

- **WHEN** Standalone utilise PZT pour joindre PA
- **THEN** le mode reste Standalone et les contrôles réseau et applicatifs restent nécessaires.

#### Scenario: Mode ZT

- **WHEN** ZT est initialisé sans création de Domaine
- **THEN** le référentiel des individus et les données pré-domaine restent au niveau Instance.
~~~~

### Référence courante pixs-instance-81a8ae9c0556

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 34. SHA-256 : `81a8ae9c0556560bcabef991ba7a8b2259c107021aadecec007049cbc2a8898f`.

Scénarios : ZT incomplet; Préconditions vérifiées.

~~~~text
### Requirement: ZT entièrement initialisé avant Domaine

La création du premier Domaine MUST exiger un mode ZT complètement initialisé, avec rôles essentiels opérationnels, identités, stockage et politiques vérifiés. Un état administratif créé ou un processus vivant MUST NOT suffire. La transition MUST être explicite et suivie durablement.

#### Scenario: ZT incomplet

- **WHEN** le rôle PKIZT essentiel manque lors de la demande du premier Domaine
- **THEN** la transition reste bloquée avec les capacités manquantes identifiées.

#### Scenario: Préconditions vérifiées

- **WHEN** le ZT et les autres préconditions de transition sont vérifiés
- **THEN** la procédure autorisée peut préparer puis activer le premier Domaine.
~~~~

### Référence courante pixs-instance-b189f9cd6424

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 48. SHA-256 : `b189f9cd6424f6b3127b840e6d069becb563c5a7942465fed2bd469482045888`.

Scénarios : Contrôleurs regroupés.

~~~~text
### Requirement: Minima et contrôleurs distincts

Chaque Instance MUST disposer d'au moins un PBO et un PA, déployés selon les environnements à administrer. Les contrôleurs d'Instance et de Domaine MUST être distingués du CZT. Leur regroupement ou séparation sur des PBO MUST être configurable sans fusion de bases ni habilitations.

#### Scenario: Contrôleurs regroupés

- **WHEN** un PBO assure les fonctions Instance et Domaine
- **THEN** les propriétaires des bases, identités et autorisations restent distincts.
~~~~

### Référence courante pixs-instance-9baefb0c5ae7

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 57. SHA-256 : `9baefb0c5ae783cb168944c78c34b6f7bc7814b244f9c8888e21389eef0e6e37`.

Scénarios : Activation du premier Domaine.

~~~~text
### Requirement: Références PG avant et après Domaine

Avant le premier Domaine, PG Instance MUST porter individus, identités numériques, organigrammes Core, groupes, ACL et données métier pré-domaine. Après activation, PG Instance MUST conserver les individus et données communes sans identité numérique d'Instance ; les identités et données reprises MUST appartenir à PG du premier Domaine, avec identifiants et relations préservés.

#### Scenario: Activation du premier Domaine

- **WHEN** le transfert pré-domaine est confirmé
- **THEN** l’identité de Domaine devient utilisable selon son profil et l’ancienne identité d’Instance ne reste pas une autre voie de connexion.
~~~~

### Référence courante pixs-instance-ebdd233f14af

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 66. SHA-256 : `ebdd233f14afcc75b3a6a94757dd20a6eb5ec1c9e93b692f109025695c0b8e33`.

Scénarios : Interruption de transfert.

~~~~text
### Requirement: Maintenance des écritures pour la transition

La transition pré-domaine vers Domaine MUST planifier une maintenance des écritures, vérifier données, relations et authentification cible et traiter toute issue inconnue avant reprise. Elle MUST NOT déclarer la bascule réussie sur un accusé de réception ou un seul effet technique PA.

#### Scenario: Interruption de transfert

- **WHEN** le résultat du transfert ou de son engagement est inconnu
- **THEN** la procédure réconcilie les états propriétaires avant toute répétition ou reprise des écritures.
~~~~

### Référence courante pixs-instance-8c964dc84f92

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 75. SHA-256 : `8c964dc84f92c940b5c3ba094d124ffaeb003db84c0f5617cc9487e8d70c38e3`.

Scénarios : Domaine d’authentification non habilité.

~~~~text
### Requirement: Administration globale par identités habilitées

Après activation du premier Domaine, l'administration globale MUST utiliser des identités de Domaines explicitement habilitées. Plusieurs Domaines d'authentification MAY être autorisés. Une panne LDAP/Kerberos MAY être traitée par un profil PG Domaine explicitement autorisé et qualifié ; elle MUST NOT recréer d'identité numérique d'Instance ni réduire l'assurance exigée.

#### Scenario: Domaine d’authentification non habilité

- **WHEN** un utilisateur authentifié par un Domaine non habilité demande l’administration globale
- **THEN** la demande est refusée malgré la validité de son authentification.
~~~~

### Référence courante pixs-instance-c159a59d2125

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 84. SHA-256 : `c159a59d212509364156279d995f289887b68dc5fde0e1bc12244c0f317d5cfa`.

Scénarios : Ancienne sauvegarde.

~~~~text
### Requirement: Absence de retour Domaine Standalone V1

Après activation du premier Domaine, l'Instance MUST rester en mode Domaine en V1. Panne, restauration, retrait de domaine ou révocation MUST NOT provoquer un retour Standalone ou réactiver les anciennes identités. Les autres transitions inverses non spécifiées MUST NOT être introduites implicitement.

#### Scenario: Ancienne sauvegarde

- **WHEN** une reprise utilise des données antérieures à la transition
- **THEN** les contrôles empêchent de rétablir le mode et les identités Standalone devenus caducs.
~~~~

### Référence courante pixs-instance-b7a2b5d23968

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 93. SHA-256 : `b7a2b5d2396839fee82af4ccc545e2c2c542dcbef6458888992a032fce8e929f`.

Scénarios : PBO mutualisé.

~~~~text
### Requirement: Habilitations Instance et domaines

Les habilitations globales Instance et celles de chaque Domaine MUST être séparées et vérifiées. Le partage d'un PBO, PA, stockage physique ou réseau MUST NOT les transmettre implicitement.

#### Scenario: PBO mutualisé

- **WHEN** un administrateur d’un Domaine utilise un PBO servant plusieurs Domaines
- **THEN** son action reste limitée aux périmètres explicitement autorisés.
~~~~

### Référence courante auth-managed-kerberos-050d7fe34c83

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 11. SHA-256 : `050d7fe34c83001e92768a1d227ad8e8df7e5412165840403ab7355727a71698`.

Scénarios : LDAP normal indisponible.

~~~~text
### Requirement: KZT obligatoire et backend OpenLDAP

Chaque Domaine MUST disposer d'au moins un KZT/MIT Kerberos à backend OpenLDAP et MAY avoir plusieurs KZT actifs. En mode normal, l'état opérationnel Kerberos durable MUST résider dans LDAP ; PG MUST garder les références Pixs. PA MUST installer/configurer/exploiter et Auth piloter les politiques. Un backend PG natif MIT ou un engagement PG préalable de chaque écriture KDC MUST NOT être supposé.

#### Scenario: LDAP normal indisponible

- **WHEN** le backend OpenLDAP exigé devient indisponible
- **THEN** les fonctions dépendantes suivent leur dégradation et aucune base Kerberos PG de remplacement n’est activée implicitement.
~~~~

### Référence courante auth-managed-kerberos-7bb78778c4c7

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 20. SHA-256 : `7bb78778c4c7ca79543e71307f9ddf3cd73f22dfd369945dd576583202a146dd`.

Scénarios : Realm en collision.

~~~~text
### Requirement: Realm propre et mappings explicites

Chaque Domaine MUST déclarer un realm propre partagé par ses KZT et unique dans l'Instance. Les principals et identités de service MUST être liés explicitement aux identités Core et périmètres. Realm, nom ou ticket MUST NOT créer d'identité ou permission par simple correspondance.

#### Scenario: Realm en collision

- **WHEN** un second Domaine demande un realm déjà utilisé dans l’Instance
- **THEN** la déclaration est refusée avant activation.
~~~~

### Référence courante auth-managed-kerberos-1760917ff34e

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 29. SHA-256 : `1760917ff34e9206553c315688562ddfa433ed8c35bd55afcfc957337e279434`.

Scénarios : Moyens locaux perdus.

~~~~text
### Requirement: Protection et récupération des clés Kerberos

Clé maîtresse, clés de principals et keytabs MUST être protégées sous identités minimales, sans secret en clair dans tables métier, artefacts ou journaux. Les clés/états Kerberos durables normaux MUST rester dans le backend LDAP. Chaque Domaine MUST déclarer les moyens protégés et procédures de récupération, distincts des seules références PG et sans dépendance circulaire au KZT à reconstruire.

#### Scenario: Moyens locaux perdus

- **WHEN** les moyens d’ouverture KZT sont perdus malgré une sauvegarde LDAP
- **THEN** la procédure de récupération choisie est requise et LDAP seul ne prouve pas l’ouverture possible.
~~~~

### Référence courante auth-managed-kerberos-255d8bbfe611

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 38. SHA-256 : `255d8bbfe611d38f703a6932a1d6f604ae7e1b010acca6e9612d84b3fe964a2b`.

Scénarios : Partition de contrôleurs.

~~~~text
### Requirement: Verrouillage cohérent du realm

Les KZT actifs MUST partager un verrouillage global par realm cohérent par identité. En partition, la cohérence MUST primer sur la disponibilité des authentifications qui en dépendent. Les chemins PG/LDAP/Kerberos concernés MUST coordonner le verrouillage par identité numérique sans verrouiller les autres identités du même individu par déduction.

#### Scenario: Partition de contrôleurs

- **WHEN** un KZT ne peut vérifier l’état global exigé du verrouillage
- **THEN** il ne confirme pas l’authentification dépendante sur une copie possiblement périmée.
~~~~

### Référence courante auth-managed-kerberos-1c0f0ee90eed

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 47. SHA-256 : `1c0f0ee90eed2d250f4a8253654ae6b38aa6c7bf5994c5ada4186924e4865ba7`.

Scénarios : Hash PG seul.

~~~~text
### Requirement: Provisionnement progressif par profil

Le provisionnement Kerberos MUST pouvoir être progressif, par administration ou libre-service sous profil explicite. Les identités nécessaires à l'administration globale MUST être prêtes avant activation du premier Domaine. Un compte MUST NOT utiliser Kerberos avant vérification de ses clés ; une session d'enrôlement limitée MUST NOT ouvrir les accès non qualifiés.

#### Scenario: Hash PG seul

- **WHEN** un plan suppose convertir le seul hachage PG en clés Kerberos
- **THEN** il est refusé jusqu’à un parcours de provisionnement compatible et vérifié.
~~~~

### Référence courante auth-managed-kerberos-551806d8cd3f

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 56. SHA-256 : `551806d8cd3f50d3712a590d122c76918252bf71104a0e70406bd4848c8e6400`.

Scénarios : Ticket expiré dans une tolérance native.

~~~~text
### Requirement: Expiration stricte et état courant

Les tickets MUST être bornés et ne plus être utilisables ni renouvelables après leur échéance. Tous les chemins revendiquant cette garantie MUST être qualifiés, sans la déduire du seul réglage de tolérance d'horloge. Retrait MUST empêcher les nouvelles émissions/renouvellements ; les tickets déjà émis MUST rester soumis aux limites documentées et aux contrôles Pixs courants.

#### Scenario: Ticket expiré dans une tolérance native

- **WHEN** un ticket dépasse son échéance mais un composant permettrait encore une tolérance
- **THEN** le chemin ne doit pas accepter cet usage et reste non qualifié s’il ne peut garantir le refus.
~~~~

### Référence courante auth-managed-kerberos-72a422092c18

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 65. SHA-256 : `72a422092c1852f4c79dad57945cc2553528d0d7027fd62cae147da6dc1fa676`.

Scénarios : Approbation sans Kerberos.

~~~~text
### Requirement: Temps et confiance inter-realms

KZT MUST vérifier les exigences de temps du profil commun, sans imposer un serveur supplémentaire par Domaine. La confiance Kerberos inter-domaines MUST être une composante explicitement autorisée des approbations, avec sens, portée et collision de realms contrôlés. Une approbation ZT seule MUST NOT la créer.

#### Scenario: Approbation sans Kerberos

- **WHEN** deux Domaines ont une approbation réseau sans composante Kerberos
- **THEN** aucune confiance inter-realms n’est déduite.
~~~~

### Référence courante auth-managed-kerberos-2916ffe1ae32

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 74. SHA-256 : `2916ffe1ae32cf40ab19b04097e4086d7096189d0b61e05c7a8ceb4f142b7f64`.

Scénarios : Principal retiré restauré.

~~~~text
### Requirement: Restauration sans résurrection

La réadmission KZT MUST vérifier état LDAP, générations de clés, mappings, politiques et retraits courants, en réconciliant les références PG souveraines et les preuves opérationnelles. Une ancienne projection Core MUST NOT remplacer PG ; une restauration LDAP MUST NOT réintroduire un principal retiré. Les garanties de protection, fraîcheur et verrouillage MUST être vérifiées avant readiness.

#### Scenario: Principal retiré restauré

- **WHEN** une ancienne sauvegarde contient un principal retiré depuis sa date
- **THEN** il n’est pas réadmis avant réconciliation courante et vérification du profil.
~~~~

### Référence courante auth-managed-kerberos-9dec834a75dd

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 83. SHA-256 : `9dec834a75ddda1262373b9a35613ba204475cee37c3158184cabaabca0378bb`.

Scénarios : Sauvegarde exploitable; Sauvegarde absente ou inadmissible; Mode normal.

~~~~text
### Requirement: Reconstruction complète en urgence critique

Une reconstruction complète LDAP/Kerberos depuis PG MUST être réservée à une procédure d'urgence en mode critique, explicitement autorisée et tracée. Le profil MUST prévoir restauration de sauvegarde protégée ou recréation depuis les références PG avec nouvelles clés et reprovisionnement nécessaires, selon les copies disponibles. La reprise MUST vérifier les garanties de sécurité avant admission et MUST NOT promettre les mêmes clés depuis de simples métadonnées PG.

#### Scenario: Sauvegarde exploitable

- **WHEN** le profil critique dispose d’un état LDAP/Kerberos protégé et des moyens requis
- **THEN** il restaure puis réconcilie cet état avec PG et les retraits courants avant réadmission.

#### Scenario: Sauvegarde absente ou inadmissible

- **WHEN** le profil choisit la reconstruction depuis les références PG sans clés récupérables
- **THEN** il recrée les clés/états requis et reprovisionne les utilisateurs/services concernés, sans prétendre conserver leurs anciens justificatifs ou tickets.

#### Scenario: Mode normal

- **WHEN** un KZT effectue une écriture native normale dans LDAP
- **THEN** la règle de reconstruction critique n’impose pas un engagement miroir PG avant chaque écriture.
~~~~

### Référence courante auth-managed-kerberos-3ea4c587f7b3

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 102. SHA-256 : `3ea4c587f7b34899a82cc619ce6206e84c6436a4d92c7bfa5abde2c2eef09069`.

Scénarios : Reconstruction dans un Domaine.

~~~~text
### Requirement: État critique distinct du mode d'exploitation

L'état critique de reconstruction MUST rester distinct des modes Standalone/ZT/Domaine et de la classe réseau Critique d'A05. Il MUST NOT provoquer un changement de mode ou une exemption d'autorisation implicite.

#### Scenario: Reconstruction dans un Domaine

- **WHEN** un Domaine entre en état critique pour reconstruire Kerberos
- **THEN** l'Instance reste en mode Domaine et les autorisations et mandats applicables restent requis
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| artifact-publication / 8 | [Canaux comme contextes de confiance distincts](../../specs/artifact-publication/spec.md#L8) | ND | Artefact du mauvais canal |
| artifact-publication / 17 | [Immuabilité et corrélation des corrections](../../specs/artifact-publication/spec.md#L17) | ND | Écrasement d'un artefact publié |
| artifact-publication / 26 | [Identité vérifiable avant installation](../../specs/artifact-publication/spec.md#L26) | ND | Emprunte discordante |
| artifact-publication / 35 | [Signature, provenance et inventaire bloquants](../../specs/artifact-publication/spec.md#L35) | ND | Signature révoquée |
| artifact-publication / 44 | [Autorités distinctes et gestion des clés](../../specs/artifact-publication/spec.md#L44) | ND | Dépôt de publication indisponible |
| backup-disaster-recovery / 8 | [Stratégie déclarée par déploiement](../../specs/backup-disaster-recovery/spec.md#L8) | ND | Procédure sans objectifs déclarés |
| backup-disaster-recovery / 17 | [Périmètres de sauvegarde distincts](../../specs/backup-disaster-recovery/spec.md#L17) | ND | Sauvegarde partielle |
| backup-disaster-recovery / 26 | [Restauration cohérente et réapplication des gouvernances](../../specs/backup-disaster-recovery/spec.md#L26) | ND | Objet restauré après suppression validée |
| backup-disaster-recovery / 35 | [Tests de restauration isolés et preuves](../../specs/backup-disaster-recovery/spec.md#L35) | ND | Démarrage après restauration |
| backup-disaster-recovery / 44 | [Restauration destructive autorisée et auditée](../../specs/backup-disaster-recovery/spec.md#L44) | ND | Suppression implicite refusée |
| compatibility / 8 | [Contraintes de version déclarées et vérifiées](../../specs/compatibility/spec.md#L8) | P | Contrainte insatisfaite à l'activation |
| compatibility / 17 | [Aucune compatibilité présumée](../../specs/compatibility/spec.md#L17) | P | Version supérieure non testée |
| compatibility / 26 | [Matrice de compatibilité globale](../../specs/compatibility/spec.md#L26) | P | État bloqué déterministe |
| compatibility / 35 | [Compatibilité déclarative distincte de la conformité comportementale](../../specs/compatibility/spec.md#L35) | P | Déclaration sans conformité |
| compatibility / 44 | [Coexistence pendant les montées de version](../../specs/compatibility/spec.md#L44) | P | Suppression prématurée |
| compatibility / 123 | [Responsabilités de l'appelant et du noyau pour les preuves](../../specs/compatibility/spec.md#L123) | P | Preuve authentifiée par l'appelant |
| data-governance / 8 | [Application de l'exception Super Admin](../../specs/data-governance/spec.md#L8) | P | Dérogation de gouvernance dans un tenant accordé |
| data-governance / 18 | [Profil de gouvernance versionné par composant](../../specs/data-governance/spec.md#L18) | P | Flux sortant sans consommateur refusé |
| data-governance / 27 | [Classification restrictive par défaut](../../specs/data-governance/spec.md#L27) | P | Export non classifié refusé |
| data-governance / 38 | [Demandes relatives aux données tracées](../../specs/data-governance/spec.md#L38) | P | Effacement propagé |
| data-lifecycle / 8 | [Application de l'exception Super Admin](../../specs/data-lifecycle/spec.md#L8) | P | Purge demandée malgré un legal hold |
| data-lifecycle / 18 | [Dimensions et états distincts](../../specs/data-lifecycle/spec.md#L18) | P | Suppression logique tracée ; Vocabulaire commun de rétention fermé |
| data-lifecycle / 43 | [Purge autorisée, auditée et idempotente](../../specs/data-lifecycle/spec.md#L43) | P | Purge prématurée refusée |
| data-lifecycle / 52 | [Tombstones contre la résurrection](../../specs/data-lifecycle/spec.md#L52) | P | Restauration sans résurrection |
| deb-package / 8 | [Paquet corrélé à la release](../../specs/deb-package/spec.md#L8) | ND | Version de paquet incohérente ; Deux paquets indépendants |
| deb-package / 22 | [Configuration et secrets hors paquet](../../specs/deb-package/spec.md#L22) | ND | Secret trouvé dans le paquet |
| deb-package / 31 | [Services alignés sur le lifecycle Pixs](../../specs/deb-package/spec.md#L31) | ND | Redémarrage par le gestionnaire de services |
| deb-package / 40 | [Mise à niveau du paquet sous validation](../../specs/deb-package/spec.md#L40) | ND | Mise à niveau interrompue |
| deb-package / 49 | [Aucune installation de code distant implicite](../../specs/deb-package/spec.md#L49) | ND | Téléchargement proposé à l'installation |
| deb-package / 58 | [Distribution Debian indépendante PA et PBO PFO](../../specs/deb-package/spec.md#L58) | ND | Distribution Debian indépendante PA et PBO PFO |
| deb-package / 67 | [Quatre binaires dans le paquet PA](../../specs/deb-package/spec.md#L67) | ND | Quatre binaires dans le paquet PA |
| lifecycle / 8 | [États de cycle de vie distincts](../../specs/lifecycle/spec.md#L8) | P | États non confondus |
| lifecycle / 17 | [Transitions autorisées et refusées](../../specs/lifecycle/spec.md#L17) | P | Désactivation sans perte et purge explicite |
| lifecycle / 26 | [Ordre déterministe des hooks](../../specs/lifecycle/spec.md#L26) | P | Double résolution identique |
| lifecycle / 35 | [Idempotence des opérations](../../specs/lifecycle/spec.md#L35) | P | Rejeu sans double effet |
| lifecycle / 44 | [Diagnostic des échecs](../../specs/lifecycle/spec.md#L44) | P | Activation invalide bloquée |
| migrations / 8 | [Contrat de migration](../../specs/migrations/spec.md#L8) | P | Migration sans version cible |
| migrations / 17 | [Planification et ordre déterministes](../../specs/migrations/spec.md#L17) | P | Deux migrations concurrentes |
| migrations / 26 | [Compatibilité pendant l'application](../../specs/migrations/spec.md#L26) | P | Coexistence pendant migration |
| migrations / 35 | [Reprise idempotente](../../specs/migrations/spec.md#L35) | P | Interruption puis reprise |
| migrations / 44 | [Contraction contrôlée](../../specs/migrations/spec.md#L44) | P | Contraction prématurée |
| modules / 8 | [Manifest lisible obligatoire](../../specs/modules/spec.md#L8) | P | Manifest incomplet |
| modules / 17 | [Frontière API publique et privée](../../specs/modules/spec.md#L17) | P | Accès à une API non déclarée |
| modules / 26 | [Propriété des données et migrations associées](../../specs/modules/spec.md#L26) | P | Changement de schéma non migré |
| modules / 35 | [Chargement contrôlé déterministe](../../specs/modules/spec.md#L35) | P | Cycle de dépendances |
| modules / 44 | [Propriété des contributions frontend modulaires](../../specs/modules/spec.md#L44) | P | Sous-module autonome intégré |
| observability / 8 | [Signaux structurés et corrélés](../../specs/observability/spec.md#L8) | P | Corrélation bout en bout |
| observability / 17 | [Santé distinguée et sondes bornées](../../specs/observability/spec.md#L17) | P | Dépendance optionnelle dégradée |
| observability / 26 | [Objectifs de service déclarés](../../specs/observability/spec.md#L26) | P | Objectif sans méthode de mesure |
| observability / 38 | [Rétention et minimisation séparées](../../specs/observability/spec.md#L38) | P | Accès inter-tenant tracé |
| operations / 8 | [Application de l'exception Super Admin](../../specs/operations/spec.md#L8) | P | Intervention de secours pendant une maintenance |
| operations / 17 | [Interface de management distincte et non publique](../../specs/operations/spec.md#L17) | P | Façades convergeant sur le même contrat |
| operations / 26 | [Opérations persistantes avec plan et idempotence](../../specs/operations/spec.md#L26) | P | Rejeu d'une opération annulée |
| operations / 35 | [Sorties sans secret et codes stables](../../specs/operations/spec.md#L35) | P | Commande non autorisée |
| operations / 44 | [État de maintenance avec drainage borné](../../specs/operations/spec.md#L44) | P | Requête reçue pendant le drainage |
| operations / 53 | [Health, diagnostic et audit opérateur](../../specs/operations/spec.md#L53) | P | Réparation via le diagnostic |
| operations / 62 | [Maintenance hiérarchisée](../../specs/operations/spec.md#L62) | P | Maintenance d'une route |
| release-management / 8 | [Définition et support d'une release](../../specs/release-management/spec.md#L8) | ND | Release sans déclaration de support |
| release-management / 17 | [Chemin de migration vérifiable](../../specs/release-management/spec.md#L17) | ND | Saut non prouvé |
| release-management / 26 | [Mise à niveau orchestrée par prévalidations](../../specs/release-management/spec.md#L26) | ND | Étape de prévalidation échouée |
| release-management / 35 | [Coexistence transitoire N et N+1](../../specs/release-management/spec.md#L35) | ND | Contraction pendant la fenêtre |
| release-management / 44 | [Retour arrière soumis à la matrice](../../specs/release-management/spec.md#L44) | ND | Retour arrière non garanti |
| release-management / 55 | [Activation, retrait et instance non valide](../../specs/release-management/spec.md#L55) | ND | Instance échouant aux contrôles |

## Empreintes SHA-256 du canon

- `openspec/specs/artifact-publication/spec.md` : `7888cada73c3beff836fe2bd6dd6a62b166af317e7036680fb6a1f9e248a5b1f`.
- `openspec/specs/backup-disaster-recovery/spec.md` : `3b129f2e8fd899d2e1992296d7c5c6a93b2336873335584fa837270ce4545954`.
- `openspec/specs/compatibility/spec.md` : `aee6de57607e95e8442b59155cf893f4ef7454db6a0ba60fbfbd9abe360eb544`.
- `openspec/specs/data-governance/spec.md` : `85c5176f49270a9eb45a51329fc200f8d1cb293bfa6bc93e62eb7fe88999ddfe`.
- `openspec/specs/data-lifecycle/spec.md` : `a3498cc4d3622d569fc9e3f8251a5c5324a9b3d1c612fe014618146297083426`.
- `openspec/specs/deb-package/spec.md` : `46730b2c3505085325539b6ae2386806e5b59bb19aa46adf5f4571335d016e64`.
- `openspec/specs/lifecycle/spec.md` : `e4f8fb1bc340000c2fafed0a6d2862b9ad033d668e89691bfdeb3bf6dc8215d3`.
- `openspec/specs/migrations/spec.md` : `9b3ced385afbeaa7414a1d58752078482e57efa242064e21e7fb4b6fde451efe`.
- `openspec/specs/modules/spec.md` : `7ea4899dff68afd31f22a501e587da4dcad9c911d1689583672678cf108ff37b`.
- `openspec/specs/observability/spec.md` : `4793cf6252768ea2673a4eb843caf027fb850b586a8fcfee877b5d37d1e6ff98`.
- `openspec/specs/operations/spec.md` : `13835ff9b1d97cf4196a66f2f991f25f0d5c0357ccc54c7bcd1d56dffe38d5f1`.
- `openspec/specs/release-management/spec.md` : `0fd7fc3720214df3741c8eed94e0db460b2fd67101cee3310c08b952672f6e3f`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
