# Références normatives — add-auth-managed-active-directory

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| auth-managed-active-directory | Domaine Pixs commun et objectif Windows V1 | 1 | auth-managed-active-directory-df29a2bbb73e |
| auth-managed-active-directory | Produit et capacité démontrés avant activation | 1 | auth-managed-active-directory-a0f224bdebf5 |
| auth-managed-active-directory | Jonction et politiques depuis PBO | 1 | auth-managed-active-directory-ded2fecd67fd |
| auth-managed-active-directory | Éditions et périmètre Windows | 1 | auth-managed-active-directory-4179bcdbc8da |
| managed-device-policies | Cibles V1 et exécutants locaux | 1 | managed-device-policies-8a43d725b9c8 |
| managed-device-policies | Gestion ZT et jonction d’authentification distinctes | 1 | managed-device-policies-f3d868c20f8b |
| managed-device-policies | Politiques communes et spécifiques | 1 | managed-device-policies-0fc04bee903f |
| managed-device-policies | Priorités et contradictions | 1 | managed-device-policies-a7f801c0bbd9 |
| managed-device-policies | Application par PA et état vérifié | 1 | managed-device-policies-fc87e0db8071 |
| managed-device-policies | Session hors ligne bornée | 1 | managed-device-policies-53ac3cf3063d |
| managed-device-policies | Rotation des secrets machine et services | 1 | managed-device-policies-0e3d3ee17150 |
| managed-device-policies | Redémarrage par profil et conclusion après reprise | 1 | managed-device-policies-0a228d3c9bf5 |
| pixs-domains | Identité et FQDN explicites | 1 | pixs-domains-02f0f83aed5e |
| pixs-domains | ZT obligatoire dédié ou partagé | 2 | pixs-domains-686f4e13ff70 |
| pixs-domains | Isolation dans un ZT partagé | 1 | pixs-domains-bd2991264b73 |
| pixs-domains | Services minimaux par Domaine | 1 | pixs-domains-c9ce061e2b23 |
| pixs-domains | Tenants et propriété des ressources | 2 | pixs-domains-784b3416b755 |
| pixs-domains | Individus et identités multiples | 1 | pixs-domains-8e5157150f7c |
| pixs-domains | Transferts fonctionnels contrôlés V1 | 1 | pixs-domains-ba4dfa97bf7d |
| pixs-domains | Structures organisationnelles non transférables V1 | 1 | pixs-domains-2d4b91559aa3 |
| pixs-domains | Retrait du premier Domaine | 1 | pixs-domains-f9d0dad1d882 |
| pixs-domains | Approbations internes et externes | 1 | pixs-domains-94814997f512 |
| pixs-domains | Références PG et services de Domaine en mode normal ou critique | 1 | pixs-domains-d8fce09ab784 |

### Référence courante auth-managed-active-directory-df29a2bbb73e

Source : [auth-managed-active-directory](../../specs/auth-managed-active-directory/spec.md), ligne 11. SHA-256 : `df29a2bbb73ebcf5444a43e3578cd23f2af0bf64cdd76e245af93d07404ec2a4`.

Scénarios : Fournisseur compatible AD proposé.

~~~~text
### Requirement: Domaine Pixs commun et objectif Windows V1

La V1 MUST prévoir la jonction native des postes Windows et les politiques de type GPO dans le même Domaine Pixs. La compatibilité MUST être démontrée avec PG source Core, LZT/OpenLDAP et KZT/MIT Kerberos ; une seconde autorité incompatible pour le même realm MUST NOT être introduite par déduction.

#### Scenario: Fournisseur compatible AD proposé

- **WHEN** un fournisseur utilise un autre annuaire ou mécanisme Kerberos
- **THEN** son articulation doit être qualifiée avant toute sélection sans déclarer automatiquement l’assemblage conforme.
~~~~

### Référence courante auth-managed-active-directory-a0f224bdebf5

Source : [auth-managed-active-directory](../../specs/auth-managed-active-directory/spec.md), ligne 20. SHA-256 : `a0f224bdebf5e4f389cebf63f8f8e9f0627176e19ffe12e054e9aa00aa696cf9`.

Scénarios : Paquet disponible seul.

~~~~text
### Requirement: Produit et capacité démontrés avant activation

Le fournisseur compatible AD, ses dépendances et ses garanties MUST être explicitement sélectionnés et qualifiés avant activation. La présence d'un paquet ou une documentation de protocole MUST NOT prouver sa compatibilité avec les autorités Pixs. Une capacité non démontrée MUST rester indisponible sans changement silencieux du modèle.

#### Scenario: Paquet disponible seul

- **WHEN** un paquet de contrôleur est disponible mais aucune recette de l’assemblage n’existe
- **THEN** la jonction native n’est pas déclarée disponible.
~~~~

### Référence courante auth-managed-active-directory-ded2fecd67fd

Source : [auth-managed-active-directory](../../specs/auth-managed-active-directory/spec.md), ligne 29. SHA-256 : `ded2fecd67fdb8fa7558967ec6773b24671fdbbc22509f3565d4d3afd6a4bcc8`.

Scénarios : Jonction sans ZT.

~~~~text
### Requirement: Jonction et politiques depuis PBO

La jonction Windows MUST être orchestrée depuis PBO avec préparation et exécution autorisées PA et intégration ZT préalable. L'administration des GPO MUST passer par PBO en V1. Les politiques MUST suivre managed-device-policies sans déléguer les décisions métier au contrôleur natif.

#### Scenario: Jonction sans ZT

- **WHEN** un poste tente une jonction avant intégration ZT
- **THEN** le parcours est bloqué jusqu’à satisfaction du prérequis.
~~~~

### Référence courante auth-managed-active-directory-4179bcdbc8da

Source : [auth-managed-active-directory](../../specs/auth-managed-active-directory/spec.md), ligne 38. SHA-256 : `4179bcdbc8dae48cec7f948f132059b8044543a5d1d7b0010c4f7fc7bb1f2869`.

Scénarios : PA sur serveur Windows.

~~~~text
### Requirement: Éditions et périmètre Windows

Le profil V1 MUST qualifier Windows 10/11 dans les éditions autorisant la jonction native ; Home MUST NOT être déclarée admissible à cette jonction. Windows Server MUST rester hors périmètre des membres natifs V1 ; son éventuel déploiement PA/PZT MUST être évalué séparément.

#### Scenario: PA sur serveur Windows

- **WHEN** un profil PA/PZT pour Windows Server est examiné
- **THEN** il ne confère pas la jonction native V1 et n’est pas exclu par cette seule décision.
~~~~

### Référence courante managed-device-policies-8a43d725b9c8

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 11. SHA-256 : `8a43d725b9c8f9f725eb22c048e5e91d1ee208d3af98a44e61ea75cfae643633`.

Scénarios : Poste administré.

~~~~text
### Requirement: Cibles V1 et exécutants locaux

Les profils V1 MUST couvrir postes Linux/Windows et serveurs Linux membres, avec Debian stable et Windows 10/11 admissibles à qualifier. Les postes administrés et serveurs Linux soumis aux politiques MUST disposer de PA/PZT locaux. Les rôles serveur de domaine MUST NOT être imposés sur chaque poste.

#### Scenario: Poste administré

- **WHEN** un poste reçoit une politique Pixs
- **THEN** les exécutants locaux sont vérifiés sans le transformer en LZT ou KZT.
~~~~

### Référence courante managed-device-policies-f3d868c20f8b

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 20. SHA-256 : `f3d868c20f8b51c27e721a1df72180c8508e9cfdf1ff06948b8294b817119a29`.

Scénarios : Hôte tiers géré.

~~~~text
### Requirement: Gestion ZT et jonction d’authentification distinctes

Un hôte MAY être intégré à ZT et administré sans jonction de domaine pour l'authentification de ses utilisateurs. Cette jonction MUST rester facultative mais exiger l'intégration ZT préalable lorsqu'elle est demandée. Le passage du PA en mode Domaine MUST NOT joindre automatiquement l'hôte au domaine d'authentification.

#### Scenario: Hôte tiers géré

- **WHEN** un hôte rejoint ZT sans jonction d’authentification
- **THEN** PA peut gérer ses capacités autorisées tandis que les utilisateurs conservent l’authentification configurée sur l’hôte.
~~~~

### Référence courante managed-device-policies-0fc04bee903f

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 29. SHA-256 : `0fc04bee903fa7c526db55656c40db141fc78bd93e1a2f658507d54be92da507`.

Scénarios : Règle propre à Windows.

~~~~text
### Requirement: Politiques communes et spécifiques

Les politiques MUST permettre des intentions communes Windows/Linux et des règles propres aux plateformes, avec politiques de poste et d'utilisateur et ciblage explicite. Les capacités non qualifiées MUST être déclarées non applicables ou indisponibles, sans simulation de succès.

#### Scenario: Règle propre à Windows

- **WHEN** une politique commune comporte une règle GPO Windows
- **THEN** l’application Linux ne prétend pas avoir appliqué cette règle native.
~~~~

### Référence courante managed-device-policies-a7f801c0bbd9

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 38. SHA-256 : `a7f801c0bbd9d9343d1e85e137ebc5eb30e56d499daabeba1006d7fe6d26ebbe`.

Scénarios : Deux valeurs au même niveau.

~~~~text
### Requirement: Priorités et contradictions

Les politiques de configuration MUST avoir des priorités explicites ; les contradictions à priorité égale MUST être signalées sans règle implicite du dernier reçu. La résolution MUST respecter les contrats de propriété et autorisations de chaque périmètre.

#### Scenario: Deux valeurs au même niveau

- **WHEN** deux politiques de même priorité imposent des valeurs incompatibles
- **THEN** l’écart est signalé et aucune valeur n’est choisie par ordre d’arrivée.
~~~~

### Référence courante managed-device-policies-fc87e0db8071

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 47. SHA-256 : `fc87e0db80717cda5b2c979b05d5045ee0bf334a5dd2cf6559bb9d13857e9c0e`.

Scénarios : Configuration reçue sans effet.

~~~~text
### Requirement: Application par PA et état vérifié

PA MUST appliquer les opérations livrées et autorisées dans le contexte système ou utilisateur approprié via pixs.agent. Réception, application, dérive et résultat confirmé MUST rester distincts. Les corrections automatiques MUST posséder leur propre politique et mandat.

#### Scenario: Configuration reçue sans effet

- **WHEN** PA reçoit une politique mais échoue à la mettre en place
- **THEN** PBO affiche l’échec sans état appliqué fictif.
~~~~

### Référence courante managed-device-policies-53ac3cf3063d

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 56. SHA-256 : `53ac3cf3063d580b57f56441ca276f52645441d643d76c41f8e4077b7e5882e7`.

Scénarios : Pas de profil hors ligne.

~~~~text
### Requirement: Session hors ligne bornée

L'ouverture de session hors ligne MAY être permise par profil explicite et borné. Elle MUST conserver les exigences de validité, protection locale et retraits connus ; une panne MUST NOT activer ce profil ni repousser ses échéances.

#### Scenario: Pas de profil hors ligne

- **WHEN** le contrôleur est indisponible sans profil hors ligne autorisé
- **THEN** aucune nouvelle permission de connexion locale n’est déduite de la panne.
~~~~

### Référence courante managed-device-policies-0e3d3ee17150

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 65. SHA-256 : `0e3d3ee171504e6660c5650982a199dc41378de37affda7cbe83cb40f3506336`.

Scénarios : Rotation native autorisée.

~~~~text
### Requirement: Rotation des secrets machine et services

La rotation des secrets machine MUST être sélectionnable par profil entre pilotage Pixs/PBO/PA et rotation native qualifiée. Les services techniques MUST pouvoir utiliser un moyen propre ou une représentation habilitée selon profil. Ces secrets MUST rester distincts du mot de passe des individus changé depuis PBO.

#### Scenario: Rotation native autorisée

- **WHEN** un poste utilise la rotation machine native qualifiée
- **THEN** elle suit son profil et sa cohérence contrôleurs sans autoriser un changement natif du mot de passe individuel.
~~~~

### Référence courante managed-device-policies-0a228d3c9bf5

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 74. SHA-256 : `0a228d3c9bf5969235d9a1b17bf8161742513eb0cd8bfd88e93f3901641b2177`.

Scénarios : Jonction exigeant redémarrage.

~~~~text
### Requirement: Redémarrage par profil et conclusion après reprise

Le profil MUST choisir redémarrage manuel ou automatique sous fenêtre autorisée, avec manuel par défaut. PBO MUST distinguer redémarrage requis et opération terminée ; les vérifications après redémarrage MUST précéder la conclusion de jonction ou de politique.

#### Scenario: Jonction exigeant redémarrage

- **WHEN** la configuration est appliquée mais le poste n’a pas redémarré
- **THEN** l’opération reste à terminer jusqu’aux contrôles après reprise.
~~~~

### Référence courante pixs-domains-02f0f83aed5e

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 11. SHA-256 : `02f0f83aed5e7e038716c3f91cc0b8f31edb2c5ea812cd6dbe8b37b700589e39`.

Scénarios : Racine déjà utilisée.

~~~~text
### Requirement: Identité et FQDN explicites

Chaque Domaine MUST posséder une identité stable et un FQDN DNS explicitement choisi. Deux Domaines d'une même Instance MUST NOT déclarer le même FQDN exact. La position DNS MUST NOT créer d'approbation ni d'autorisation implicite.

#### Scenario: Racine déjà utilisée

- **WHEN** un Domaine demande le FQDN exact d’un autre Domaine de l’Instance
- **THEN** la déclaration est refusée avant activation.
~~~~

### Référence courante pixs-domains-686f4e13ff70

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 20. SHA-256 : `686f4e13ff70e8af073de2ac6f80d25d553a84feb6cec9fec11dc0f13c5d93cc`.

Scénarios : Deux sous-domaines; Faux suffixe.

~~~~text
### Requirement: ZT obligatoire dédié ou partagé

Chaque Domaine MUST utiliser une instance ZT. Il MAY créer son ZT ou utiliser celui de l'Instance lorsque son FQDN est égal au FQDN ZT ou en est un sous-domaine par labels DNS. Plusieurs Domaines admissibles MAY utiliser ce même ZT ; le partage MUST rester explicitement déclaré.

#### Scenario: Deux sous-domaines

- **WHEN** association.pixs.fr et recherche.pixs.fr choisissent le ZT pixs.fr
- **THEN** ils peuvent être rattachés avec des périmètres distincts.

#### Scenario: Faux suffixe

- **WHEN** association-autrepixs.fr demande le ZT pixs.fr en invoquant un suffixe de caractères
- **THEN** la condition hiérarchique DNS est refusée.
~~~~

### Référence courante pixs-domains-bd2991264b73

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 34. SHA-256 : `bd2991264b73d60314f90b7bb3d936bee405c507992fe50e7ff2e06fb1da6fc6`.

Scénarios : Même ZT sans politique.

~~~~text
### Requirement: Isolation dans un ZT partagé

Les politiques MUST pouvoir être propres à un Domaine ou partagées explicitement. Les communications inter-domaines MUST être refusées par défaut et nécessiter une politique explicite. Le partage du ZT MUST NOT fusionner les identités, ACL applicatives, annuaires ou realms.

#### Scenario: Même ZT sans politique

- **WHEN** deux acteurs de Domaines différents partagent ZT sans autorisation de communication
- **THEN** l’initiation inter-domaines est refusée.
~~~~

### Référence courante pixs-domains-c9ce061e2b23

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 43. SHA-256 : `c9ce061e2b23d3859a4cb92e01635334908d63f103ce5c9db7b2b2c1d5a053c5`.

Scénarios : ZT partagé et KZT manquant.

~~~~text
### Requirement: Services minimaux par Domaine

Chaque Domaine MUST disposer de sa PG indépendante, de ses organigrammes organisationnel/fonctionnel, d'au moins un LZT/OpenLDAP et d'un KZT/MIT Kerberos. Chaque Domaine MUST déclarer son realm, unique dans l'Instance. Les minima CZT/SZT/RZT/STZT/DZT/PKIZT MUST être évalués par ZT réel, pas dupliqués par déduction pour un ZT partagé.

#### Scenario: ZT partagé et KZT manquant

- **WHEN** un nouveau Domaine partage un ZT opérationnel mais ne possède aucun KZT
- **THEN** ses services de Domaine restent non opérationnels tant que ce minimum manque.
~~~~

### Référence courante pixs-domains-784b3416b755

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 52. SHA-256 : `784b3416b7559266c7a1b38d15a475ebd8b05a90e2f00eb976a8bf198703e0f4`.

Scénarios : Domaine sans tenant; Tenant rattaché deux fois.

~~~~text
### Requirement: Tenants et propriété des ressources

Un Domaine MUST accepter zéro, un ou plusieurs tenants ; chaque tenant MUST appartenir à un seul Domaine après transition. Les scopes enfants MUST rester rattachés à leur tenant sans cycles. Les propriétés Instance, Domaine et Tenant MUST être distinctes et n'accorder aucun droit implicite.

#### Scenario: Domaine sans tenant

- **WHEN** un Domaine opérationnel ne contient aucun tenant
- **THEN** ses services et son rattachement ZT restent valides.

#### Scenario: Tenant rattaché deux fois

- **WHEN** une mutation rattache simultanément un tenant à deux Domaines
- **THEN** elle est refusée sans ambiguïté de propriétaire.
~~~~

### Référence courante pixs-domains-8e5157150f7c

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 66. SHA-256 : `8e5157150f7c0a1801085b1c19bdd9c69fe4c345dcba246bb25ed2aba4727793`.

Scénarios : Affiliation sans admission.

~~~~text
### Requirement: Individus et identités multiples

Un individu Core MUST pouvoir être affilié à plusieurs Domaines et tenants et posséder plusieurs identités par Domaine. Chaque participation MUST conserver ses admissions, profils et habilitations. Une affiliation Core MUST NOT valoir admission ZT, sauf politique automatique explicite.

#### Scenario: Affiliation sans admission

- **WHEN** un individu est affilié à Recherche sans politique d’admission automatique
- **THEN** son appartenance ZT n’est pas créée par cette seule affiliation.
~~~~

### Référence courante pixs-domains-ba4dfa97bf7d

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 75. SHA-256 : `ba4dfa97bf7dfe8389d5a8f4597671aa9630b9e24d13f8a2ea071bc82dc36b12`.

Scénarios : Tenant transféré.

~~~~text
### Requirement: Transferts fonctionnels contrôlés V1

La V1 MUST prévoir les transferts autorisés d'identités numériques, données métier et tenants entre Domaines de la même Instance, avec vérification des dépendances, continuité des références et réévaluation des droits cibles. Le transfert MUST NOT copier implicitement des autorisations ni être présenté comme déplacement d'une brique exécutable.

#### Scenario: Tenant transféré

- **WHEN** un transfert de tenant est engagé entre deux Domaines
- **THEN** son identité est conservée, son propriétaire est unique et les habilitations de destination sont réévaluées.
~~~~

### Référence courante pixs-domains-2d4b91559aa3

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 84. SHA-256 : `2d4b91559aa387da2cb8be333d66674748a755850567e45bba8b742811112985`.

Scénarios : Transfert de département.

~~~~text
### Requirement: Structures organisationnelles non transférables V1

La V1 MUST NOT proposer le transfert fonctionnel de structures organisationnelles entre Domaines. Miroitage autorisé et réorganisation interne MUST rester distincts d'un tel transfert.

#### Scenario: Transfert de département

- **WHEN** une demande V1 vise à transférer un département entre Domaines
- **THEN** elle est refusée comme hors périmètre sans modifier les structures source ou cible.
~~~~

### Référence courante pixs-domains-f9d0dad1d882

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 93. SHA-256 : `f9d0dad1d882e815cf4d5b665b2037e6591dcb271ed3dd1e9f7605fcd4759334`.

Scénarios : Dernier Domaine.

~~~~text
### Requirement: Retrait du premier Domaine

Le premier Domaine MAY être retiré par procédure explicite si au moins un autre Domaine est opérationnel et si données, identités, authentification globale et dépendances sont traitées. Le retrait MUST NOT rétablir Standalone, laisser l'administration sans identité admissible ou retirer un ZT partagé encore requis.

#### Scenario: Dernier Domaine

- **WHEN** le retrait vise le seul Domaine opérationnel
- **THEN** il est refusé sans retour implicite en Standalone.
~~~~

### Référence courante pixs-domains-94814997f512

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 102. SHA-256 : `94814997f512912fbd83b186f7db3bf2f0771d0e37c0e5ecfc7fe81a41c5562f`.

Scénarios : Individu externe reconnu.

~~~~text
### Requirement: Approbations internes et externes

Les Domaines MUST pouvoir établir des approbations dans une même Instance ou entre Instances selon zt-instances. Un individu externe MUST conserver son identité d'origine ; la cible MUST conserver une référence et décider séparément de ses admissions et droits. Les composantes DNS et Kerberos MUST être explicites.

#### Scenario: Individu externe reconnu

- **WHEN** une approbation permet de reconnaître l’identité externe
- **THEN** la reconnaissance ne crée pas d’identité locale indépendante ou de droits automatiques.
~~~~

### Référence courante pixs-domains-d8fce09ab784

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 111. SHA-256 : `d8fce09ab78488325720197abff25a3f229a41ca7f6e38dac7da16c02df7b924`.

Scénarios : Reconstruction de Domaine.

~~~~text
### Requirement: Références PG et services de Domaine en mode normal ou critique

LZT et KZT MUST être obligatoires par Domaine. PG MUST rester souveraine pour les données de référence Pixs ; LDAP MUST porter l'état opérationnel Kerberos durable en mode normal. Une reconstruction complète depuis PG MUST suivre le mode critique autorisé, avec restauration protégée ou recréation/reprovisionnement selon profil et sauvegardes disponibles. La réplication LDAP MUST NOT remplacer la référence Core PG.

#### Scenario: Reconstruction de Domaine

- **WHEN** tous les annuaires du Domaine sont perdus
- **THEN** le Domaine applique sa procédure critique, distingue données de référence et clés récupérées/recréées, puis vérifie la remise en service.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Statut des deltas antérieurs après contrôle E3

Les anciens fichiers sous specs/ ont été déplacés, avec empreintes conservées, vers [l’historique interne](historique-deltas-avant-e3/README.md). Le [contrôle de couverture](COUVERTURE_DELTAS_E3.md) relie chaque ancienne exigence au contrat courant et aux tâches ouvertes. Le dossier reste actif ; skip_specs évite seulement la réapplication des anciennes prescriptions. Il ne termine ni la réalisation, ni les tests, ni les 49 tâches encore ouvertes dans les sept dossiers concernés.
