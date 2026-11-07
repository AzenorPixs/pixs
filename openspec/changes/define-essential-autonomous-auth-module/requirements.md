# Registre consolidé des déclarations Auth et stockage Core

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| authentication | Fournisseurs déclarés et confiance explicite | 1 | authentication-19f40b972c78 |
| authentication | Identifiant externe canonique et liaison explicite | 1 | authentication-cf3b90403a1e |
| authentication | Sessions bornées et révocation propagée | 2 | authentication-bba360459f9c |
| authentication | Module essentiel autonome pixs.auth | 2 | authentication-2cd9fc78aed8 |
| authentication | Autonomie locale et PostgreSQL par défaut | 3 | authentication-7deab703128c |
| authentication | Propriété des données Auth et protection des justificatifs | 2 | authentication-5af8eb52988f |
| authentication | Sous-modules Auth composés par les mécanismes communs | 1 | authentication-f8a9e9da127b |
| authentication | Politiques Auth déclaratives et contextualisées | 1 | authentication-2a10fbff7239 |
| authentication | Absence de repli implicite entre méthodes et sources | 2 | authentication-64ed6a16a8f6 |
| authentication | Interfaces spécialisées du profil Auth local | 1 | authentication-ca439766ea7f |
| authentication | Justificatifs opaques et stockage serveur par empreinte | 1 | authentication-c43dd24e0955 |
| authentication | État Auth courant requis | 1 | authentication-fb37fa48763a |
| authentication | Durées des sessions locales ordinaires | 2 | authentication-f58a4b2bf783 |
| authentication | Durée des accès et fraîcheur sensible | 2 | authentication-81737f3de29d |
| authentication | Politique configurable et exceptions canoniques | 1 | authentication-f87c04c0556b |
| authentication | Renouvellement rotatif à usage unique | 1 | authentication-9f0d9b2938e0 |
| authentication | Activité utilisateur et renouvellement | 1 | authentication-c668081af427 |
| authentication | Concurrence et réponse perdue de rotation | 2 | authentication-d9131b3941bf |
| authentication | Réutilisation suspecte et révocation de session | 1 | authentication-4cc4a81801fe |
| authentication | Plafond et remplacement explicite des sessions | 2 | authentication-42558d8e901e |
| authentication | Onglets et renouvellements sans nouvelle session | 1 | authentication-3f508363903c |
| authentication | Changement de mot de passe sans reconnexion automatique | 2 | authentication-1f281505aa1c |
| authentication | Récupération et compromission du mot de passe | 2 | authentication-7e9531288ce6 |
| authentication | Argon2id via les outils Django | 1 | authentication-2e7a00ac3949 |
| authentication | Réutilisation Argon2id dans un profil OpenLDAP qualifié | 2 | authentication-82591f961338 |
| authentication | Limites de la compatibilité des empreintes | 1 | authentication-882a416b3157 |
| authentication | Conservation du renouvellement de la CLI interactive | 1 | authentication-38870e5fe1b2 |
| authentication | Mot de passe commun par identité numérique | 1 | authentication-c423b942ab64 |
| authentication | Changement uniquement depuis PBO | 1 | authentication-29ea6c6bc11d |
| authentication | Récupération configurable et désactivée par défaut | 1 | authentication-7507cdda1859 |
| authentication | MFA choisie par profil et chemins qualifiés | 1 | authentication-d40c9ae62ea3 |
| authentication | Changements effectifs et contrôleurs à jour | 1 | authentication-d30f23cea222 |
| authentication | Verrouillage commun et états dépendants | 1 | authentication-19aff870d368 |
| core | Module obligatoire au-dessus du noyau | 1 | core-fc5c17b85882 |
| core | Primitives minimales communes | 1 | core-a15db0a0e874 |
| core | Aucun fournisseur concret imposé | 1 | core-71fb8ebb9b15 |
| core | Profil minimal des utilisateurs et identités numériques v1 | 2 | core-cad742eb1a6c |
| core | Liaison utilisateur identité explicite et unique | 2 | core-5be4341f9029 |
| core | Représentation minimale des comptes de service | 1 | core-1ec1c0295927 |
| core | Frontière des validateurs du profil identité | 1 | core-9641b83b4301 |
| core | Autorités et limites du profil identité structurel | 1 | core-0b6602b1da05 |
| core | Frontière Core Auth et dépendance unidirectionnelle | 1 | core-fe32af48f650 |
| core | Moyens multiples sans multiplication implicite des identités | 1 | core-7d3a8ec34441 |
| core | Évolution versionnée du lien individu identités | 1 | core-810ca819ba83 |
| reference-composition | Qualification du binaire commun et des profils de ressources P0 | 4 | reference-composition-7131b276f78e |
| reference-composition | Capacités obligatoires du P0 | 1 | reference-composition-0af0b6011293 |
| reference-composition | Capacités hors P0 explicites | 1 | reference-composition-986398c06367 |
| reference-composition | Preuve reproductible | 1 | reference-composition-ab553efe6c54 |
| reference-composition | Profil initial PBO PFO Debian local v1 | 2 | reference-composition-5f1322f3cd28 |
| reference-composition | Garanties du socle conservées dans le profil initial | 1 | reference-composition-70063af8e7b7 |
| reference-composition | Parcours installable et utilisable du profil initial | 1 | reference-composition-2614801b7609 |
| reference-composition | Capacités non sélectionnées du profil initial | 1 | reference-composition-ef9b2d25c156 |
| reference-composition | Preuve de la composition effectivement distribuée | 1 | reference-composition-7961b985d4cc |
| reference-composition | Choix C01 systemd et exception d’amorçage du profil Debian local | 2 | reference-composition-80e3d17e557d |
| reference-composition | Qualification et source de vérité après amorçage | 2 | reference-composition-b86766ab642e |
| reference-composition | Profil Auth standard sans connecteur externe installé | 2 | reference-composition-fa2727180f3d |
| reference-composition | Composition ZT initiale et Domaines | 1 | reference-composition-4f43b97aaed5 |
| pixs-instance | Identité logique et référentiel commun | 1 | pixs-instance-b9b134df059f |
| pixs-instance | Modes Standalone ZT et Domaine | 2 | pixs-instance-18485b8d2051 |
| pixs-instance | ZT entièrement initialisé avant Domaine | 2 | pixs-instance-81a8ae9c0556 |
| pixs-instance | Minima et contrôleurs distincts | 1 | pixs-instance-b189f9cd6424 |
| pixs-instance | Références PG avant et après Domaine | 1 | pixs-instance-9baefb0c5ae7 |
| pixs-instance | Maintenance des écritures pour la transition | 1 | pixs-instance-ebdd233f14af |
| pixs-instance | Administration globale par identités habilitées | 1 | pixs-instance-8c964dc84f92 |
| pixs-instance | Absence de retour Domaine Standalone V1 | 1 | pixs-instance-c159a59d2125 |
| pixs-instance | Habilitations Instance et domaines | 1 | pixs-instance-b7a2b5d23968 |
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

### Référence courante authentication-19f40b972c78

Source : [authentication](../../specs/authentication/spec.md), ligne 8. SHA-256 : `19f40b972c7847934dfd3652c5fc9dc435a200f49ca6ba0194190f7e8f0a7b14`.

Scénarios : Émetteur non approuvé refusé.

~~~~text
### Requirement: Fournisseurs déclarés et confiance explicite

Chaque fournisseur (local, OIDC, SAML) MUST déclarer protocole, émetteurs, audiences, algorithmes, clés, claims obligatoires et mappings ; la seule validité cryptographique MUST NOT suffire sans confiance applicative configurée.

#### Scenario: Émetteur non approuvé refusé

- **WHEN** un jeton valide émane d'un émetteur non approuvé
- **THEN** l'authentification est refusée avec une erreur stable et un audit
~~~~

### Référence courante authentication-cf3b90403a1e

Source : [authentication](../../specs/authentication/spec.md), ligne 17. SHA-256 : `cf3b90403a1e4309fe5f284e5b5d57dc277f4951d68d4dfd85a8a122409fedea`.

Scénarios : Courriel seul non rapproché.

~~~~text
### Requirement: Identifiant externe canonique et liaison explicite

Le système MUST respecter les garanties suivantes.

L'identifiant externe canonique est le triplet fournisseur, émetteur, sujet ; toute liaison à une identité existante est explicite, vérifiée des deux côtés, idempotente et auditée ; aucun rapprochement par courriel seul.

#### Scenario: Courriel seul non rapproché

- **WHEN** deux comptes partagent la même adresse sans preuve bilatérale
- **THEN** aucune fusion n'a lieu et une liaison explicite reste exigée
~~~~

### Référence courante authentication-bba360459f9c

Source : [authentication](../../specs/authentication/spec.md), ligne 28. SHA-256 : `bba360459f9c54d5266d275f5e1cc8690b32e4ca5436162d1d01e8fc54f75db5`.

Scénarios : Révocation propagée; Retrait sans audit confirmé.

~~~~text
### Requirement: Sessions bornées et révocation propagée

Sessions, jetons et renouvellements MUST être bornés et rotatifs, avec détection de réutilisation. Toute révocation d’identité, justificatif, session ou confiance MUST invalider les contextes concernés sans supprimer les données métier. L’audit MUST suivre audit, sans secret, avec son exception limitée au retrait d’accès Auth. Révocation persistante et audit réussi MUST NOT être annoncés sans leur preuve.

#### Scenario: Révocation propagée
- **WHEN** une identité ou une session est révoquée
- **THEN** les contextes dérivés sont invalidés avant toute nouvelle opération sensible

#### Scenario: Retrait sans audit confirmé
- **WHEN** seul l’audit est indisponible et qu’un retrait d’accès Auth autorisé est persisté selon l’exception dédiée
- **THEN** les contextes concernés sont invalidés et l’échec d’audit reste signalé pour réconciliation sans audit fictif
~~~~

### Référence courante authentication-2cd9fc78aed8

Source : [authentication](../../specs/authentication/spec.md), ligne 40. SHA-256 : `2cd9fc78aed8a023b789605bbbbd7de954d34a3dd3addaa5bf144945f18e405a`.

Scénarios : Composition applicative sans Auth; Fixture structurelle isolée.

~~~~text
### Requirement: Module essentiel autonome pixs.auth

Toute composition applicative Pixs MUST inclure `pixs.auth`, module essentiel indépendant de `pixs.core`, avec une capacité locale autonome sélectionnée explicitement par le profil. Son absence MUST empêcher l'activation applicative. Les fixtures structurelles non applicatives MUST rester distinguées de ce profil.

#### Scenario: Composition applicative sans Auth
- **WHEN** une composition applicative omet pixs.auth ou sa capacité locale requise
- **THEN** sa validation échoue avant activation sans annoncer d'authentification disponible

#### Scenario: Fixture structurelle isolée
- **WHEN** un test manipule seulement un contrat pur Core sans runtime applicatif
- **THEN** il reste possible sans Auth et ne constitue pas une composition applicative qualifiée
~~~~

### Référence courante authentication-7deab703128c

Source : [authentication](../../specs/authentication/spec.md), ligne 52. SHA-256 : `7deab703128c58f53bf986cc8aa083c34d13801b0c7b28ec2dfbcc7702a73096`.

Scénarios : Installation autonome; Authentification PG Domaine; État PG courant absent.

~~~~text
### Requirement: Autonomie locale et PostgreSQL par défaut

Avant le premier Domaine, Auth MUST pouvoir authentifier sur PG Instance sans fournisseur externe, LDAP/KDC ni Internet. Après activation, les identités MUST appartenir aux Domaines et PG Instance MUST NOT conserver d'identité numérique d'Instance. Auth MAY authentifier directement sur PG Domaine sous profil explicite et qualifié ; LZT/KZT MUST rester obligatoires par Domaine sans imposer leur disponibilité à ce chemin PG autorisé.

#### Scenario: Installation autonome

- **WHEN** le profil pré-domaine local est sélectionné
- **THEN** l’authentification PG Instance reste possible selon ses moyens et politiques.

#### Scenario: Authentification PG Domaine

- **WHEN** un profil permet explicitement PG Domaine avec ses garanties
- **THEN** Auth utilise l’identité de Domaine sans réactiver son ancienne identité d’Instance.

#### Scenario: État PG courant absent

- **WHEN** l’opération exige une PG actuelle indisponible
- **THEN** elle échoue fermée sans fichier ou session supposée valide.
~~~~

### Référence courante authentication-5af8eb52988f

Source : [authentication](../../specs/authentication/spec.md), ligne 71. SHA-256 : `5af8eb52988f703d72691a1d8e5a01544fea517f7e2333a79cc63b9d612d8747`.

Scénarios : Session persistée; Liaison avec Core.

~~~~text
### Requirement: Propriété des données Auth et protection des justificatifs

pixs.auth MUST posséder ses justificatifs, liaisons d'authentification, politiques et sessions, rattachés aux identités Core par contrat public. Les mots de passe MUST être stockés uniquement sous empreinte sécurisée ; les jetons réutilisables, clés privées et secrets MFA MUST NOT être stockés en clair dans les tables métier, manifests ou journaux. Les secrets réversibles MUST suivre les contrats de protection et de secrets applicables.

#### Scenario: Session persistée
- **WHEN** Auth conserve une session ou un renouvellement
- **THEN** l'enregistrement permet expiration et révocation sans exposer le jeton brut réutilisable

#### Scenario: Liaison avec Core
- **WHEN** Auth rattache un moyen à une DigitalIdentity
- **THEN** la référence est vérifiée par contrat public sans écriture directe dans les tables Core
~~~~

### Référence courante authentication-f8a9e9da127b

Source : [authentication](../../specs/authentication/spec.md), ligne 83. SHA-256 : `f8a9e9da127b784472c0fc7d7aa9fd8ec4115e59069299b27a283b0d935580f4`.

Scénarios : Source installée sans confiance.

~~~~text
### Requirement: Sous-modules Auth composés par les mécanismes communs

Les méthodes locales, l'enrôlement, l'émission d'identité, les services gérés et les sources externes MUST être extensibles par composants déclarés et contrats versionnés. Les sous-modules MUST utiliser le manifest et le lifecycle communs sans registre parallèle. L'installation d'un sous-module MUST NOT suffire à activer une confiance ou un service.

#### Scenario: Source installée sans confiance
- **WHEN** un sous-module de source est installé sans configuration de confiance validée
- **THEN** il ne peut authentifier aucune identité
~~~~

### Référence courante authentication-2a10fbff7239

Source : [authentication](../../specs/authentication/spec.md), ligne 91. SHA-256 : `2a10fbff7239d37dc777e2035ab2d9daeed141895d618b15f1f822f95a53fb49`.

Scénarios : Politique contradictoire.

~~~~text
### Requirement: Politiques Auth déclaratives et contextualisées

Les politiques Auth MUST être typées, versionnées et résolues déterministiquement selon Instance, Domaine, profil et contexte tenant/scope applicable. Méthodes, MFA, fraîcheur, sessions, récupération et confiance MUST exposer origine et valeur effective sans secret. Une règle contradictoire MUST bloquer l'opération sans sélection opportuniste de la moins exigeante.

#### Scenario: Politique contradictoire

- **WHEN** les règles ne permettent pas de déterminer l’assurance applicable
- **THEN** Auth refuse avec diagnostic sans réduire implicitement les exigences.
~~~~

### Référence courante authentication-64ed6a16a8f6

Source : [authentication](../../specs/authentication/spec.md), ligne 100. SHA-256 : `64ed6a16a8f6769d91ff1f258024246cb9de57963ce0c74565c58c91b30d91bc`.

Scénarios : IdP externe indisponible; Secours propre du Super Admin.

~~~~text
### Requirement: Absence de repli implicite entre méthodes et sources

Une indisponibilité externe MUST NOT activer une authentification locale ou diminuer l'assurance requise. La coexistence des sources et méthodes MUST suivre une politique explicite et préserver la liaison canonique. Le compte de secours MUST conserver son authentification propre et son exception selon authorization et initial-administration, sans extension aux comptes ordinaires.

#### Scenario: IdP externe indisponible
- **WHEN** une politique impose un IdP externe indisponible pour un compte ordinaire
- **THEN** un mot de passe local ne devient pas un repli autorisé par cette seule panne

#### Scenario: Secours propre du Super Admin
- **WHEN** le Super Admin utilise son parcours canonique de secours sans MFA
- **THEN** son exception reste applicable sans attribuer un niveau MULTI_FACTOR non obtenu
~~~~

### Référence courante authentication-ca439766ea7f

Source : [authentication](../../specs/authentication/spec.md), ligne 112. SHA-256 : `ca439766ea7fc07ebcabc2de93893796ead6e0a27c17ef7207c249d3de383b4a`.

Scénarios : Session liée à Core.

~~~~text
### Requirement: Interfaces spécialisées du profil Auth local

Le profil local MUST exposer des interfaces spécialisées d’authentification, de sessions et de justificatifs, typées et versionnées dans le même module pixs.auth. Les façades web, API et CLI MUST réutiliser ces contrats. Auth MUST référencer les identités Core par UUID et ports publics, posséder ses écritures et MUST NOT exposer de modèle Django privé ni écrire dans les tables privées d’un autre module.

#### Scenario: Session liée à Core
- **WHEN** une façade demande une session
- **THEN** Auth vérifie la référence et l’état Core par port public puis possède ses écritures, sans modèle privé exposé
~~~~

### Référence courante authentication-c43dd24e0955

Source : [authentication](../../specs/authentication/spec.md), ligne 120. SHA-256 : `c43dd24e0955878cdc29c3245ac9db762b0718920b26954272409fcda6fa5958`.

Scénarios : Justificatif brut absent.

~~~~text
### Requirement: Justificatifs opaques et stockage serveur par empreinte

Le profil local MUST utiliser des identifiants de session et jetons API/CLI opaques issus d’un générateur aléatoire cryptographiquement sûr. Les justificatifs remis au client MUST être conservés côté serveur uniquement sous empreinte de vérification, avec état, expiration et révocation dans PostgreSQL. Un backend conservant leur valeur brute MUST NOT être repris sans adaptation conforme.

#### Scenario: Justificatif brut absent
- **WHEN** Auth persiste une session ou un jeton
- **THEN** la vérification par empreinte et la révocation sont possibles sans stocker ni journaliser le justificatif brut réutilisable
~~~~

### Référence courante authentication-fb37fa48763a

Source : [authentication](../../specs/authentication/spec.md), ligne 128. SHA-256 : `fb37fa48763ac16ec2a80b11378e43f8da96b332bedb0e4a771f6fec35bda3b2`.

Scénarios : État inaccessible.

~~~~text
### Requirement: État Auth courant requis

Un contrôle nécessitant l’état Auth courant MUST échouer fermé si cet état ne peut pas être vérifié. PostgreSQL indisponible MUST NOT entraîner un repli vers un fichier ou un jeton supposé valide.

#### Scenario: État inaccessible
- **WHEN** PostgreSQL Auth ne permet pas de vérifier l’état courant requis
- **THEN** l’accès est refusé sans repli implicite
~~~~

### Référence courante authentication-f58a4b2bf783

Source : [authentication](../../specs/authentication/spec.md), ligne 136. SHA-256 : `f58a4b2bf78334507b530cf4d14f24b8b5ea14d5d6518292fa31f7c19ce74bfc`.

Scénarios : Inactivité ordinaire; Plafond administratif.

~~~~text
### Requirement: Durées des sessions locales ordinaires

Par défaut, les sessions ordinaires MUST expirer après 60 minutes d’inactivité ou 12 heures au total et les sessions d’administration ordinaires après 15 minutes d’inactivité ou 2 heures au total, selon la première échéance atteinte.

#### Scenario: Inactivité ordinaire
- **WHEN** une session ordinaire atteint 60 minutes sans activité admissible sous politique par défaut
- **THEN** elle expire même si son plafond absolu de 12 heures n’est pas atteint

#### Scenario: Plafond administratif
- **WHEN** une session d’administration ordinaire atteint 2 heures sous politique par défaut malgré une activité récente
- **THEN** elle expire sans prolongation par activité ou renouvellement
~~~~

### Référence courante authentication-81737f3de29d

Source : [authentication](../../specs/authentication/spec.md), ligne 148. SHA-256 : `81737f3de29d72442f51ae6348d6bb37f1f9c77ad8a1e8be88a48c9ee92c864c`.

Scénarios : Validité restante courte; Fraîcheur insuffisante.

~~~~text
### Requirement: Durée des accès et fraîcheur sensible

Le profil local MUST limiter par défaut les jetons d’accès API/CLI à 15 minutes et à la validité restante applicable. Une opération sensible MUST exiger par défaut une authentification datant de moins de 5 minutes et les niveaux d’assurance réellement requis, sans assurance inventée.

#### Scenario: Validité restante courte
- **WHEN** la session expire dans moins de 15 minutes lors d’une émission
- **THEN** le jeton n’est utilisable que pendant cette validité restante ou moins

#### Scenario: Fraîcheur insuffisante
- **WHEN** un compte ordinaire demande une action sensible avec une authentification datant de 5 minutes ou davantage sous politique par défaut
- **THEN** une réauthentification conforme est exigée avant l’effet sensible
~~~~

### Référence courante authentication-f87c04c0556b

Source : [authentication](../../specs/authentication/spec.md), ligne 160. SHA-256 : `f87c04c0556b341cb92597841c34d9e807d1f8c22616297f4d9c080786d16c21`.

Scénarios : Politique résolue.

~~~~text
### Requirement: Politique configurable et exceptions canoniques

Durées, fraîcheur et plafonds de sessions MUST être configurables par politique typée/versionnée exposant valeur effective et origine. Les exceptions canoniques du seul Super Admin MUST rester préservées sans s’étendre aux administrateurs ordinaires ni fabriquer d’assurance. Une invalidation courante MUST pouvoir écourter la validité annoncée.

#### Scenario: Politique résolue
- **WHEN** une politique qualifiée remplace une valeur par défaut pour un compte ordinaire
- **THEN** la valeur effective et son origine sont connues et les invalidations courantes restent applicables
~~~~

### Référence courante authentication-9f0d9b2938e0

Source : [authentication](../../specs/authentication/spec.md), ligne 168. SHA-256 : `9f0d9b2938e0078c3c7651c6b233cd9389a05e53f520757d3abfe7bc3c47b82e`.

Scénarios : Rotation réussie.

~~~~text
### Requirement: Renouvellement rotatif à usage unique

Le renouvellement API/CLI MUST employer un jeton à usage unique remplacé atomiquement à chaque renouvellement réussi. Il MUST NOT repousser le plafond absolu de session ni la date réelle d’authentification. Les secrets de renouvellement MUST rester soumis au stockage serveur par empreinte.

#### Scenario: Rotation réussie
- **WHEN** un renouvellement valide est confirmé
- **THEN** le jeton consommé ne peut plus produire de rotation et ni plafond absolu ni date réelle d’authentification ne changent
~~~~

### Référence courante authentication-c668081af427

Source : [authentication](../../specs/authentication/spec.md), ligne 176. SHA-256 : `c668081af427760a2493d4ef49fcd94f345856622ce643611155d404409b2b7f`.

Scénarios : Renouvellements seuls.

~~~~text
### Requirement: Activité utilisateur et renouvellement

Les activités repoussant l’inactivité MUST être déclarées et contrôlées côté serveur. Le renouvellement seul MUST NOT compter comme activité utilisateur. Les appels d’arrière-plan et répétitions automatiques MUST NOT être assimilés implicitement à une action utilisateur.

#### Scenario: Renouvellements seuls
- **WHEN** un client renouvelle périodiquement sans activité utilisateur admissible
- **THEN** la session expire à son échéance d’inactivité sans prolonger son plafond absolu
~~~~

### Référence courante authentication-d9131b3941bf

Source : [authentication](../../specs/authentication/spec.md), ligne 184. SHA-256 : `d9131b3941bf08793306fab4517439636b39bd5ecd125aa4447132d5fe02a079`.

Scénarios : Deux appels concurrents; Réponse perdue.

~~~~text
### Requirement: Concurrence et réponse perdue de rotation

Les concurrences et répétitions reconnues MUST NOT émettre un second renouvellement pour un jeton consommé. La perte d’une réponse MAY imposer une nouvelle authentification ; le système MUST NOT promettre la restitution d’un nouveau secret conservé seulement sous empreinte.

#### Scenario: Deux appels concurrents
- **WHEN** deux requêtes consomment le même jeton de renouvellement
- **THEN** au plus une rotation est confirmée, sans seconde émission

#### Scenario: Réponse perdue
- **WHEN** une rotation est committée mais sa réponse contenant le nouveau secret est perdue
- **THEN** la reprise ne produit pas de second renouvellement et peut imposer une nouvelle authentification
~~~~

### Référence courante authentication-4cc4a81801fe

Source : [authentication](../../specs/authentication/spec.md), ligne 196. SHA-256 : `4cc4a81801fed7394b154b348da874c29516d322e8e5288aea33f7ff7c2971b4`.

Scénarios : Réutilisation suspecte.

~~~~text
### Requirement: Réutilisation suspecte et révocation de session

Une réutilisation suspecte d’un jeton consommé MUST révoquer la session concernée et tous ses jetons dérivés, sans fermeture automatique des autres sessions du compte. Une déconnexion globale MAY être décidée par traitement d’incident autorisé. La détection MUST distinguer répétitions reconnues et concurrences légitimes d’une réutilisation suspecte selon un contrat explicite, sans seconde émission.

#### Scenario: Réutilisation suspecte
- **WHEN** le mécanisme qualifié classe une réutilisation comme suspecte
- **THEN** la session et ses dérivés sont invalidés, les autres sessions restant ouvertes sauf révocation globale autorisée
~~~~

### Référence courante authentication-42558d8e901e

Source : [authentication](../../specs/authentication/spec.md), ligne 204. SHA-256 : `42558d8e901e94ebdf8e0abd69aaa8e9830c307de5ec9bde97ba1bad0887be8a`.

Scénarios : Limite atteinte; Admissions concurrentes.

~~~~text
### Requirement: Plafond et remplacement explicite des sessions

La politique par défaut MUST limiter un compte à 5 sessions ordinaires et 2 sessions d’administration ordinaires selon leur catégorie, avec admission contrôlée atomiquement. À la limite atteinte, une admission MUST exiger le choix explicite d’une session à fermer ou être refusée ; elle MUST NOT déconnecter silencieusement une session existante.

#### Scenario: Limite atteinte
- **WHEN** une sixième session ordinaire est demandée sous politique par défaut sans remplacement choisi
- **THEN** l’admission est refusée sans fermeture silencieuse

#### Scenario: Admissions concurrentes
- **WHEN** plusieurs admissions tentent de consommer le dernier emplacement autorisé
- **THEN** le contrôle atomique empêche de dépasser le plafond effectif
~~~~

### Référence courante authentication-3f508363903c

Source : [authentication](../../specs/authentication/spec.md), ligne 216. SHA-256 : `3f508363903c83e248e623634a98c7e2d622c21b85c8404ba0c2265194c4e43e`.

Scénarios : Même cookie.

~~~~text
### Requirement: Onglets et renouvellements sans nouvelle session

Les onglets partageant le même cookie et le renouvellement de jetons MUST NOT compter comme de nouvelles sessions.

#### Scenario: Même cookie
- **WHEN** plusieurs onglets partagent une session ou un client renouvelle ses jetons
- **THEN** aucun emplacement supplémentaire n’est consommé par cette seule opération
~~~~

### Référence courante authentication-1f281505aa1c

Source : [authentication](../../specs/authentication/spec.md), ligne 224. SHA-256 : `1f281505aa1cbeb35700a343e55f4d6701cf68afde6319018d2213d14c7fff2b`.

Scénarios : Changement authentifié par défaut; Autre identité du même individu.

~~~~text
### Requirement: Changement de mot de passe sans reconnexion automatique

Le changement de mot de passe MUST être piloté par Auth depuis un PBO habilité. Le profil MUST distinguer les contextes : changement authentifié révoquant par défaut les autres sessions avec conservation possible de la session courante après vérification ; récupération/réinitialisation révoquant toutes les sessions de l'identité par défaut. La politique MAY être ajustée explicitement ; une reconnexion ou assurance supérieure MUST NOT être déduite du changement.

#### Scenario: Changement authentifié par défaut

- **WHEN** une identité change son mot de passe depuis sa session vérifiée
- **THEN** les autres sessions sont révoquées et seule la session courante peut être conservée après vérification.

#### Scenario: Autre identité du même individu

- **WHEN** le mot de passe d’une identité courante change
- **THEN** les sessions de son identité administrative suivent leur politique propre.
~~~~

### Référence courante authentication-7e9531288ce6

Source : [authentication](../../specs/authentication/spec.md), ligne 238. SHA-256 : `7e9531288ce64316cfddf0506c1d9975462ae617e35a8fbf9c4242863ba99af3`.

Scénarios : Récupération sans MFA; Changement non confirmé.

~~~~text
### Requirement: Récupération et compromission du mot de passe

Récupération et réinitialisation MUST suivre leur profil et révoquer toutes les sessions de l'identité par défaut ; une compromission suspectée MUST déclencher le retrait prévu sans assurance restaurée implicitement. Un retrait d'accès malgré panne d'audit MUST suivre audit et MUST NOT confirmer un justificatif non committé. Les tickets Kerberos déjà délivrés MUST être traités séparément des sessions Pixs.

#### Scenario: Récupération sans MFA

- **WHEN** une récupération autorisée ne fournit pas de nouvelle preuve MFA
- **THEN** les sessions sont révoquées selon le profil sans assurance multifacteur inventée.

#### Scenario: Changement non confirmé

- **WHEN** seul le retrait est confirmé après échec de mutation
- **THEN** aucun nouveau mot de passe n’est annoncé committé.
~~~~

### Référence courante authentication-2e7a00ac3949

Source : [authentication](../../specs/authentication/spec.md), ligne 252. SHA-256 : `2e7a00ac394982673813c45e4cd841e62718a07c313e0f34c219259c623bc201`.

Scénarios : Paramètres qualifiés.

~~~~text
### Requirement: Argon2id via les outils Django

Le profil local MUST protéger les mots de passe avec Argon2id via Django et argon2-cffi, avec versions stables épinglées et paramètres qualifiés pour les versions Python supportées. Il MUST NOT implémenter d’algorithme de hachage personnalisé ni abaisser sa protection pour une intégration.

#### Scenario: Paramètres qualifiés
- **WHEN** une version du profil local est préparée pour réalisation
- **THEN** la compatibilité des versions et les coûts mémoire/calcul sont qualifiés sans dépendance installée par la seule spécification
~~~~

### Référence courante authentication-82591f961338

Source : [authentication](../../specs/authentication/spec.md), ligne 260. SHA-256 : `82591f961338092914e2d8de89cb0b6bbbbce1dd8dc62dcefd49c3e3b5fcafaa`.

Scénarios : Vérification croisée; Profil incompatible.

~~~~text
### Requirement: Réutilisation Argon2id dans un profil OpenLDAP qualifié

La réutilisation d’une empreinte Argon2id par un futur profil OpenLDAP sélectionné MUST être qualifiée avec son module Argon2 et une adaptation d’enveloppe préservant variante, version, paramètres, sel et résultat. Un format ou paramètre incompatible MUST être refusé explicitement, sans repli vers un hachage plus faible.

#### Scenario: Vérification croisée
- **WHEN** un profil OpenLDAP sélectionné est qualifié pour l’empreinte produite par Django
- **THEN** la même empreinte adaptée accepte le bon mot de passe et refuse le mauvais sans réhachage ni affaiblissement

#### Scenario: Profil incompatible
- **WHEN** une variante, version, enveloppe ou un paramètre n’est pas accepté
- **THEN** la compatibilité est refusée sans hachage affaibli ni succès de qualification annoncé
~~~~

### Référence courante authentication-882a416b3157

Source : [authentication](../../specs/authentication/spec.md), ligne 272. SHA-256 : `882a416b3157563873d5b14a3e5b0eed2f5c221c9d1a0dae4b428cb3aa0b76bf`.

Scénarios : Compatibilité documentaire seule.

~~~~text
### Requirement: Limites de la compatibilité des empreintes

L’adaptation d’enveloppe MUST NOT être présentée comme récupération du mot de passe ou conversion en clé Kerberos ou Active Directory. Elle MUST NOT activer un annuaire ni dupliquer des justificatifs implicitement. PostgreSQL MUST rester distingué comme stockage applicatif de l’empreinte, sans assimilation à l’authentification de ses comptes techniques.

#### Scenario: Compatibilité documentaire seule
- **WHEN** la possibilité de réutilisation est documentée
- **THEN** aucun service LDAP, copie de justificatif, conversion de clé ou changement d’authentification PostgreSQL n’est engagé
~~~~

### Référence courante authentication-38870e5fe1b2

Source : [authentication](../../specs/authentication/spec.md), ligne 280. SHA-256 : `38870e5fe1b2ac82daab211930be3664bb27d3741bf88ae5d3d3cf87696cbda9`.

Scénarios : Trousseau indisponible.

~~~~text
### Requirement: Conservation du renouvellement de la CLI interactive

La CLI interactive MUST conserver le jeton entre lancements uniquement dans un trousseau système disponible et qualifié. Sinon, elle MUST le garder en mémoire jusqu’à la fin du processus et MUST NOT se rabattre automatiquement sur un fichier en clair. Cette conservation MUST respecter expiration, révocation et plafonds ; elle MUST NOT créer de session permanente ni de compte de service.

#### Scenario: Trousseau indisponible
- **WHEN** aucun trousseau qualifié n’est utilisable
- **THEN** le jeton reste en mémoire du processus et le lancement suivant demande une nouvelle connexion sans fichier de repli clair
~~~~

### Référence courante authentication-c423b942ab64

Source : [authentication](../../specs/authentication/spec.md), ligne 288. SHA-256 : `c423b942ab644a30f93169d10aa6bd81b22d954b9e68c9d3daca9602915a6c12`.

Scénarios : Deux identités.

~~~~text
### Requirement: Mot de passe commun par identité numérique

Une identité numérique MUST utiliser un mot de passe commun pour ses méthodes PG/LDAP/Kerberos qui en emploient un. Auth MUST coordonner les représentations de vérification et clés propres à ces méthodes, sans supposer une conversion depuis un hash PG. Les identités distinctes d'un individu MUST garder leurs propres moyens et profils.

#### Scenario: Deux identités

- **WHEN** un individu possède des comptes courant et administratif
- **THEN** le mot de passe commun concerne les méthodes de chaque identité sans imposer un secret unique à l’individu.
~~~~

### Référence courante authentication-29ea6c6bc11d

Source : [authentication](../../specs/authentication/spec.md), ligne 297. SHA-256 : `29ea6c6bc11d3ae5e1875c9a8e241f44fbfdfe8ec3d56da3a7e99f56657bd2f3`.

Scénarios : Changement natif non prévu.

~~~~text
### Requirement: Changement uniquement depuis PBO

Les mots de passe des individus MUST être changés depuis PBO sous pilotage Auth. Le PBO logique Standalone MUST pouvoir porter cette fonction ; en Domaine elle MAY être sur le contrôleur ou un autre PBO habilité. Les rotations de secrets machine et services MUST rester distinctes de cette règle.

#### Scenario: Changement natif non prévu

- **WHEN** une application tente d’utiliser une voie native non autorisée pour changer le mot de passe individuel
- **THEN** la voie est refusée ou non proposée sans contourner PBO.
~~~~

### Référence courante authentication-7507cdda1859

Source : [authentication](../../specs/authentication/spec.md), ligne 306. SHA-256 : `7507cdda1859125274e06238f7d348ba6c33cd46ad35ee7dcca99d5c58883259`.

Scénarios : Récupération non activée.

~~~~text
### Requirement: Récupération configurable et désactivée par défaut

Auth MUST proposer changement individuel, réinitialisation par administrateur habilité et récupération autonome configurable/débrayable. La récupération autonome MUST être désactivée par défaut et ses moyens activés explicitement par profil. Les politiques de mot de passe MUST pouvoir se décliner Instance/Domaine/profil, les domaines et profils ajoutant leurs contraintes au socle.

#### Scenario: Récupération non activée

- **WHEN** un individu demande le parcours autonome avec le profil par défaut
- **THEN** ce parcours reste désactivé sans créer de moyen de récupération implicite.
~~~~

### Référence courante authentication-d40c9ae62ea3

Source : [authentication](../../specs/authentication/spec.md), ligne 315. SHA-256 : `d40c9ae62ea3f70ab8ef2d36d2825a4ecb4325fa03070ff893dfa97e3b1a5af0`.

Scénarios : Chemin non qualifié.

~~~~text
### Requirement: MFA choisie par profil et chemins qualifiés

La MFA MUST être configurable par profil, y compris administratif, sans obligation générale Pixs. TOTP et clés/passkeys MUST être sélectionnables sur les chemins qualifiés ; un profil exigeant MFA MUST refuser un chemin incapable de fournir l'assurance. Gestion des facteurs MUST pouvoir être individuelle ou administrative sous habilitations et profil.

#### Scenario: Chemin non qualifié

- **WHEN** un profil exige MFA sur un chemin non qualifié
- **THEN** l’authentification est refusée sans annoncer la MFA depuis un seul facteur.
~~~~

### Référence courante authentication-d30f23cea222

Source : [authentication](../../specs/authentication/spec.md), ligne 324. SHA-256 : `d30f23cea2223420259e854f754eb651f4a3fa985cd87a85e72a01913ae10ea9`.

Scénarios : Contrôleur isolé encore actif.

~~~~text
### Requirement: Changements effectifs et contrôleurs à jour

Chaque profil MUST choisir entre confirmation de tous les contrôleurs déclarés ou de ceux maintenus en service après exclusion effective vérifiée des autres. Un défaut général MUST NOT être déduit. Le simple défaut de joignabilité MUST NOT prouver l'exclusion ni diminuer le minimum synchrone PG. La réadmission MUST être manuelle ou automatique selon profil après vérification identité, habilitations et révisions.

#### Scenario: Contrôleur isolé encore actif

- **WHEN** un contrôleur non à jour reste susceptible d’authentifier sur un réseau isolé
- **THEN** le changement n’est pas déclaré effectif tant que sa mise à jour ou son exclusion exigée n’est pas prouvée.
~~~~

### Référence courante authentication-19aff870d368

Source : [authentication](../../specs/authentication/spec.md), ligne 333. SHA-256 : `19aff870d36851592c71fafd88873fdc25c0e118a6ae19c842f1789d5090f6a7`.

Scénarios : Échecs sur LDAP.

~~~~text
### Requirement: Verrouillage commun et états dépendants

Les méthodes PG/LDAP/Kerberos concernées MUST coordonner un verrouillage par identité numérique. Les autres identités de l'individu MUST garder leurs états, sauf suspension globale Core. Les accès et mandats dépendants MUST suivre les révocations et continuités de zt-instances sans repli permissif.

#### Scenario: Échecs sur LDAP

- **WHEN** les échecs atteignent la limite applicable à l’identité via LDAP
- **THEN** le même état de verrouillage s’applique aux autres méthodes concernées sans verrouiller une autre identité par déduction.
~~~~

### Référence courante core-fc5c17b85882

Source : [core](../../specs/core/spec.md), ligne 8. SHA-256 : `fc5c17b85882a8ba45a10882c27301127360d7d338acfed61ae555f474e99776`.

Scénarios : Composition sans core refusée.

~~~~text
### Requirement: Module obligatoire au-dessus du noyau

Toute composition Pixs MUST inclure pixs.core comme module requis ; une composition sans pixs.core est invalide.

#### Scenario: Composition sans core refusée

- **WHEN** une composition omet pixs.core
- **THEN** l'activation est refusée avant tout chargement
~~~~

### Référence courante core-a15db0a0e874

Source : [core](../../specs/core/spec.md), ligne 17. SHA-256 : `a15db0a0e874b998aae0d3883b0347bb0489c0e07ef375e39225258e613241f9`.

Scénarios : Primitive consommée par contrat.

~~~~text
### Requirement: Primitives minimales communes

pixs.core MUST exposer individus, identités numériques, groupes, appartenances, tenants, rôles, ACL et permissions via contrats publics. Le référentiel d'individus MUST être commun à l'Instance. PG Instance/Domaine MUST conserver leur vérité selon pixs-instance ; la publication LDAP MUST suivre directory-projections et auth-managed-directory sans remplacer PG.

#### Scenario: Primitive consommée par contrat

- **WHEN** un module demande une identité ou une appartenance
- **THEN** il utilise le contrat propriétaire sans accès direct aux tables privées.
~~~~

### Référence courante core-71fb8ebb9b15

Source : [core](../../specs/core/spec.md), ligne 26. SHA-256 : `71fb8ebb9b15814ee30b4a4c0ce5c9bb1ddb832abf1cc4559300abf76d76eeb6`.

Scénarios : Fournisseur compatible.

~~~~text
### Requirement: Aucun fournisseur concret imposé

Le noyau et les contrats génériques Core MUST rester agnostiques des implémentations. Les profils MUST déclarer leurs fournisseurs requis, dont PG source Core et OpenLDAP/MIT Kerberos en mode Domaine, sans intégrer leur code au noyau ni activer implicitement un service.

#### Scenario: Fournisseur compatible

- **WHEN** un fournisseur compatible est sélectionné dans les limites du profil
- **THEN** les consommateurs gardent leurs contrats sans dépendre de son implémentation privée.
~~~~

### Référence courante core-cad742eb1a6c

Source : [core](../../specs/core/spec.md), ligne 35. SHA-256 : `cad742eb1a6c4eb163ea45410ed7ee9c86448a3e4be1a3f079032d8fe403f16d`.

Scénarios : Identité minimale valide; Identifiant ou vocabulaire invalide.

~~~~text
### Requirement: Profil minimal des utilisateurs et identités numériques v1

Les identifiants internes stables de `User` et `DigitalIdentity` MUST être
des UUIDv7. Le profil v1 de `DigitalIdentity` MUST porter un type explicite
parmi `HUMAN`, `SERVICE`, `DEVICE` et `FEDERATED`, et un état explicite
parmi `ACTIVE`, `SUSPENDED`, `REVOKED` et `EXPIRED`. Les validateurs
MUST rejeter un identifiant non UUIDv7, un type inconnu ou un état inconnu ;
ils MUST NOT déduire un état, un type ou une assurance d'un provider.

#### Scenario: Identité minimale valide

- **WHEN** un utilisateur et une identité HUMAN à l'état ACTIVE portent chacun un UUIDv7 valide
- **THEN** leurs représentations minimales sont acceptées sans exiger une authentification ou une liaison entre eux

#### Scenario: Identifiant ou vocabulaire invalide

- **WHEN** un identifiant n'est pas un UUIDv7 ou le type ou l'état n'appartient pas au vocabulaire fermé du profil v1
- **THEN** la validation refuse la représentation concernée
~~~~

### Référence courante core-5be4341f9029

Source : [core](../../specs/core/spec.md), ligne 54. SHA-256 : `5be4341f90297f703e132f31ac54e36f7b95b9eeee07f1115391e4b32f8fce64`.

Scénarios : Plusieurs identités du même individu; Identité liée à deux individus.

~~~~text
### Requirement: Liaison utilisateur identité explicite et unique

Un individu User MUST pouvoir exister sans DigitalIdentity et une identité technique MUST pouvoir exister sans individu. Chaque identité MUST être liée à au plus un individu ; un individu MUST pouvoir posséder plusieurs identités par Domaine selon pixs-domains. Les références MUST être existantes, explicites et cohérentes avec leur périmètre ; elles MUST NOT être déduites d'un nom, email ou identifiant externe.

#### Scenario: Plusieurs identités du même individu

- **WHEN** un individu possède une identité courante et une identité administrative dans le même Domaine
- **THEN** les deux liaisons sont admises avec profils et droits distincts.

#### Scenario: Identité liée à deux individus

- **WHEN** la même identité est liée à deux individus ou à une référence absente
- **THEN** la liaison est refusée.
~~~~

### Référence courante core-1ec1c0295927

Source : [core](../../specs/core/spec.md), ligne 68. SHA-256 : `1ec1c0295927e8168d6acb338b99c9f7f50340b776ac6c536f89a61c164fde51`.

Scénarios : Compte de service sans utilisateur.

~~~~text
### Requirement: Représentation minimale des comptes de service

Dans le profil v1, un compte de service MUST être représenté par une
`DigitalIdentity` de type `SERVICE`. Cette représentation MUST pouvoir
exister sans utilisateur lié et MUST NOT conférer par elle-même de droit
d'accès ni de niveau d'assurance.

#### Scenario: Compte de service sans utilisateur

- **WHEN** une identité SERVICE possède un UUIDv7 et un état valides sans utilisateur lié
- **THEN** sa représentation de compte de service est acceptée sans établir une authentification ni une autorisation
~~~~

### Référence courante core-9641b83b4301

Source : [core](../../specs/core/spec.md), ligne 80. SHA-256 : `9641b83b4301530600349bf2b779a1cd8a2a59ab86a38aa7588ecea6a9c5f4f0`.

Scénarios : Validation structurelle sans effet applicatif.

~~~~text
### Requirement: Frontière des validateurs du profil identité

La validation structurelle du profil v1 MUST pouvoir être exercée sur des
modèles sans authentification réelle, provider concret ni persistance. Elle MUST NOT être présentée comme une authentification, une autorisation,
une mutation persistante ou une preuve d'audit durable.

#### Scenario: Validation structurelle sans effet applicatif

- **WHEN** un modèle d'identité satisfait le profil structurel
- **THEN** cette validation ne crée aucune session, ne persiste aucune entité et n'accorde aucun accès
~~~~

### Référence courante core-0b6602b1da05

Source : [core](../../specs/core/spec.md), ligne 91. SHA-256 : `0b6602b1da05f941115747a0bdac11582bcc6db4d887493bf0dd87144a80674b`.

Scénarios : Identité structurelle sans assurance implicite.

~~~~text
### Requirement: Autorités et limites du profil identité structurel

Le backend Django
MUST rester l'autorité métier et transactionnelle ; PostgreSQL MUST rester
la source de vérité applicative. Les mutations réelles MUST conserver les
exigences applicables de persistance, d'autorisation et d'audit. Le profil structurel MUST NOT définir implicitement des transitions d'état,
des règles temporelles ou des niveaux d'assurance à partir du seul type
ou état de l'identité.

#### Scenario: Identité structurelle sans assurance implicite

- **WHEN** un modèle satisfait le profil structurel d'identité
- **THEN** son type ou son état ne définit pas implicitement de transition, règle temporelle ou niveau d'assurance, et les mutations restent sous l'autorité backend
~~~~

### Référence courante core-fe32af48f650

Source : [core](../../specs/core/spec.md), ligne 105. SHA-256 : `fe32af48f650fc38400dc2d1f8a081762b649f6c3cbc693b8a33d669fd95e370`.

Scénarios : Révocation canonique.

~~~~text
### Requirement: Frontière Core Auth et dépendance unidirectionnelle

pixs.core MUST rester propriétaire de User, DigitalIdentity, liens, groupes, appartenances, tenants, rôles, ACL et permissions. pixs.auth MUST consommer ses contrats publics pour ces données. Core MUST NOT dépendre d'une implémentation Auth ni héberger ses protocoles, sessions ou secrets. Les contrats purs partagés existants MUST rester réutilisables sans déplacement imposé.

#### Scenario: Révocation canonique
- **WHEN** Core confirme la révocation d'une DigitalIdentity
- **THEN** Auth invalide les accès concernés selon son contrat sans écriture Core dans une table privée Auth ni cycle de dépendances
~~~~

### Référence courante core-7d3a8ec34441

Source : [core](../../specs/core/spec.md), ligne 113. SHA-256 : `7d3a8ec344411de2b477f833bcfefc4790f600c535142cce6aaedbbed958e266`.

Scénarios : Passkey et principal pour une identité.

~~~~text
### Requirement: Moyens multiples sans multiplication implicite des identités

Une DigitalIdentity MUST pouvoir avoir plusieurs moyens et sources sous propriété Auth. Ajouter une méthode MUST NOT créer une identité, une appartenance ou un droit implicite. La cardinalité des identités par individu MUST suivre la liaison explicite ci-dessus, sans fusion d'identités distinctes par partage d'un moyen ou nom.

#### Scenario: Passkey et principal pour une identité

- **WHEN** une passkey et un principal Kerberos sont liés à une identité
- **THEN** son UUID et ses habilitations restent inchangés sans compte supplémentaire.
~~~~

### Référence courante core-810ca819ba83

Source : [core](../../specs/core/spec.md), ligne 123. SHA-256 : `810ca819ba83be9240790e2382bfa67eb864a7839821bd925e3ca212adaa0f80`.

Scénarios : Contrat v1 existant.

~~~~text
### Requirement: Évolution versionnée du lien individu identités

Les contrats et modèles v1 MUST conserver leurs références de preuve et être distingués du modèle à plusieurs identités par individu et Domaine. Le nouveau modèle MUST suivre une évolution versionnée et des migrations préservant identités et relations ; une ancienne recette v1 MUST NOT qualifier automatiquement le nouveau lien.

#### Scenario: Contrat v1 existant

- **WHEN** un modèle validé pour la liaison unique v1 est examiné
- **THEN** sa preuve reste bornée à cette version et ne démontre pas la nouvelle cardinalité Domaine
~~~~

### Référence courante reference-composition-7131b276f78e

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 10. SHA-256 : `7131b276f78ec528ebd8d3dc65dca30cc41d7a9b3f3ae193754cb02b3e8ea9e6`.

Scénarios : Garanties de qualification du parcours initial PA PZT; P0 sans exécution réseau; P0 sans réseau distant; Plan de ressources sans preuve sur cible.

~~~~text
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
~~~~

### Référence courante reference-composition-0af0b6011293

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 35. SHA-256 : `0af0b601129367e64eba64554f480dd9d5a1b93ee2348a0ba66ad4ac964e8671`.

Scénarios : Capacité P0 absente.

~~~~text
### Requirement: Capacités obligatoires du P0

Une composition P0 MUST inclure les mécanismes de composition, `pixs.core`, `pixs.auth` essentiel avec son authentification locale autonome et PostgreSQL par défaut, le contexte tenant/scope, l'autorisation, les API et contrats publics, migrations, runtime, provisionnement, sécurité, secrets, audit, observabilité, gouvernance, cycle de vie des données, conformité et un composant d'exemple.

#### Scenario: Capacité P0 absente

- **WHEN** une composition se présente comme P0 mais omet une capacité obligatoire
- **THEN** sa validation échoue avant activation ou publication
~~~~

### Référence courante reference-composition-986398c06367

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 44. SHA-256 : `986398c063671a966f8bc20f7e0d7706fe89595ff960a233fa8fbc266c49ad03`.

Scénarios : Synchronisation non sélectionnée.

~~~~text
### Requirement: Capacités hors P0 explicites

Toute capacité hors P0 MAY être ajoutée par sélection explicite. Son absence
MUST être déclarée ou représentée par un état compatible et MUST NOT affaiblir
les garanties du P0.

#### Scenario: Synchronisation non sélectionnée

- **WHEN** une composition P0 n'inclut aucun provider de synchronisation
- **THEN** elle reste valide sans annoncer de capacité réactive
~~~~

### Référence courante reference-composition-ab553efe6c54

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 55. SHA-256 : `ab553efe6c54a415ee9b8e42bbb9e9d009d3681dce99c2210ada04af4ef236b4`.

Scénarios : Deux validations identiques.

~~~~text
### Requirement: Preuve reproductible

La validation P0 MUST produire une preuve versionnée du graphe de composants,
contrats, profils et contrôles exécutés. Cette preuve MUST NOT contenir de secret,
credential ou donnée de production.

#### Scenario: Deux validations identiques

- **WHEN** la même composition P0 est validée avec les mêmes entrées
- **THEN** elle produit le même graphe et des contrôles équivalents
~~~~

### Référence courante reference-composition-5f1322f3cd28

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 66. SHA-256 : `5f1322f3cd28af91090d23c44e81cab453f1e264e606a48d7fbaa4ea3853d90e`.

Scénarios : Garanties du profil Debian local avec préparation PA; Architecture seulement observée.

~~~~text
### Requirement: Profil initial PBO PFO Debian local v1

Le profil pbo-p0-debian-local-v1 MUST identifier PBO/PFO, Debian 13 local, Django/TanStack et PostgreSQL distinct de PBO, préparé par PA système via PZT local. Il MUST déclarer et qualifier ses versions, architectures et exécutants selon le scénario ci-dessous ; un relevé de développement ou une preuve sans ces exécutants MUST NOT qualifier ce profil révisé.

#### Scenario: Garanties du profil Debian local avec préparation PA

- **WHEN** la première livraison du profil pbo-p0-debian-local-v1 est évaluée
- **THEN** La première livraison de profil `pbo-p0-debian-local-v1` MUST identifier PBO/PFO, Debian 13 local, Django, TanStack et PostgreSQL comme service distinct du processus PBO, préparé par le PA système de cet hôte via le parcours PA/PZT déclaré. Le profil MUST sélectionner les exécutants PA système et PZT local nécessaires à ce parcours ; une qualification historique sans ces exécutants MUST NOT prouver ce profil révisé. Elle MUST déclarer ses architectures et versions qualifiées avant distribution ; le relevé de développement MUST NOT tenir lieu de qualification.

#### Scenario: Architecture seulement observée

- **WHEN** une architecture apparaît dans l’environnement de développement sans recette correspondante
- **THEN** elle n’est pas annoncée comme supportée par le profil livré
~~~~

### Référence courante reference-composition-70063af8e7b7

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 80. SHA-256 : `70063af8e7b7f3ec61cbf3a60e111e20b60fcc09b6574df183ec392d1f1dce56`.

Scénarios : Module essentiel absent.

~~~~text
### Requirement: Garanties du socle conservées dans le profil initial

Le profil initial MUST satisfaire les capacités obligatoires P0 et composer les modules de gestion `pixs.agent` (PA hors PZT) et `pixs.pzt` (PZT), ainsi que le module DNS essentiel côté PBO. La désactivation réseau MUST NOT retirer ces modules ni affaiblir identité, périmètre, autorisation, audit, gouvernance ou reprise applicables.

#### Scenario: Module essentiel absent

- **WHEN** le réseau est désactivé mais `pixs.agent`, `pixs.pzt` ou le module DNS essentiel manque à la composition PBO
- **THEN** la qualification du profil échoue avant publication
~~~~

### Référence courante reference-composition-2614801b7609

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 89. SHA-256 : `2614801b7609ab3d7e337158b1a189846ac07b7308a13f21974f0e532efc17de`.

Scénarios : Démonstration mémoire seule.

~~~~text
### Requirement: Parcours installable et utilisable du profil initial

Le profil MUST permettre installation, première configuration, authentification, administration et opérations Core via contrats publics. Les rôles web, worker et scheduler MUST utiliser le même artefact et la persistance de référence ; une composition de test seule MUST NOT prouver ces parcours.

#### Scenario: Démonstration mémoire seule

- **WHEN** les seuls contrôles réussis utilisent des fixtures mémoire sans installation ni dépendance réelle
- **THEN** le profil ne revendique pas un parcours installable et utilisable qualifié
~~~~

### Référence courante reference-composition-ef9b2d25c156

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 98. SHA-256 : `ef9b2d25c1563c4766241a4a4b0e5df4f4188397774c38481e8c1f9e7bd395ab`.

Scénarios : Option absente sans dépendance obligatoire.

~~~~text
### Requirement: Capacités non sélectionnées du profil initial

Le profil MUST déclarer les capacités non sélectionnées et leurs limites sans annoncer leurs garanties. Une dépendance obligatoire d’une capacité sélectionnée MUST NOT être exclue sous prétexte d’option ; son absence bloque la qualification concernée.

#### Scenario: Option absente sans dépendance obligatoire

- **WHEN** aucun provider de synchronisation n’est sélectionné et aucune capacité retenue ne l’exige
- **THEN** son absence est déclarée sans annoncer de synchronisation ni affaiblir le P0
~~~~

### Référence courante reference-composition-7961b985d4cc

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 107. SHA-256 : `7961b985d4cc6e4533276d182585f4d018bce58499a8d3ce46b8b3ae71f2da57`.

Scénarios : Sources et paquet divergents.

~~~~text
### Requirement: Preuve de la composition effectivement distribuée

La preuve initiale MUST relier exigences applicables, scénarios exécutés, composants, versions et artefact installé. Elle MUST distinguer code présent, déclarations, dimensions non évaluées et verdicts observés, sans secret ni compatibilité globale supposée.

#### Scenario: Sources et paquet divergents

- **WHEN** la recette porte sur des sources différentes de celles du paquet proposé
- **THEN** elle ne suffit pas à qualifier la composition distribuée
~~~~

### Référence courante reference-composition-80e3d17e557d

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 116. SHA-256 : `80e3d17e557db39ab0b1f163e3b9be60f18df6f7f0cdd4ef4555404d6256b8c9`.

Scénarios : Hôte intermédiaire conservé non prêt; Source locale hors phase autorisée.

~~~~text
### Requirement: Choix C01 systemd et exception d’amorçage du profil Debian local

Le profil pbo-p0-debian-local-v1 MUST sélectionner le transport C01 LoadCredentialEncrypted systemd avec rotation par arrêt attesté et redémarrage contrôlé. Avant disponibilité de la base Pixs et du sink C05, il MUST déclarer explicitement l’exception limitée du journal fonctionnel local d’amorçage, ses politiques et son autorisation INSTALLER.

#### Scenario: Hôte intermédiaire conservé non prêt

- **WHEN** le provider est configuré mais qu’une preuve d’identité, d’audit, de reprise ou de qualification requise manque
- **THEN** la composition reste non prête sans affaiblir les obligations C17/C18/C19

#### Scenario: Source locale hors phase autorisée

- **WHEN** le journal local est proposé comme autorité applicative après reprise complète ou pour des opérations métier ordinaires
- **THEN** la composition refuse cet usage hors de l’exception d’amorçage
~~~~

### Référence courante reference-composition-b86766ab642e

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 130. SHA-256 : `b86766ab642ec0550cf7661ba1d162a50901d633d9bb6948cc548c4cb0225c3e`.

Scénarios : Hôte intermédiaire conservé non prêt; Source locale hors phase autorisée.

~~~~text
### Requirement: Qualification et source de vérité après amorçage

Cette exception MUST NOT devenir une source de vérité métier parallèle après reprise dans PostgreSQL. Les architectures, versions, capacités de stockage et politiques MUST être qualifiées avant distribution ; DEVOPS.md, un test isolé ou un reçu mémoire MUST NOT valoir qualification du paquet.

#### Scenario: Hôte intermédiaire conservé non prêt

- **WHEN** le provider est configuré mais qu’une preuve d’identité, d’audit, de reprise ou de qualification requise manque
- **THEN** la composition reste non prête sans affaiblir les obligations C17/C18/C19

#### Scenario: Source locale hors phase autorisée

- **WHEN** le journal local est proposé comme autorité applicative après reprise complète ou pour des opérations métier ordinaires
- **THEN** la composition refuse cet usage hors de l’exception d’amorçage
~~~~

### Référence courante reference-composition-fa2727180f3d

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 144. SHA-256 : `fa2727180f3d824fbb7e3619a5b0196d02d52df210f1022887c5b3578875e857`.

Scénarios : Profil livré sans connecteurs externes; Profil Domaine.

~~~~text
### Requirement: Profil Auth standard sans connecteur externe installé

Le profil pré-domaine MUST sélectionner Auth local PG et garder les connecteurs externes absents sauf sélection explicite. Le mode Domaine MUST composer les capacités LZT/OpenLDAP et KZT/MIT Kerberos requises par Domaine ; IdP sortant et connecteurs externes MUST rester distincts et non activés implicitement. Présence de logiciel et service opérationnel MUST rester séparés.

#### Scenario: Profil livré sans connecteurs externes

- **WHEN** un profil Standalone standard est installé
- **THEN** Auth PG fonctionne selon sa politique sans service LDAP/KDC ou émission sortante implicite.

#### Scenario: Profil Domaine

- **WHEN** une composition revendique un Domaine opérationnel
- **THEN** ses LZT/KZT et son ZT admissible doivent être vérifiés, même si aucune source externe n’est installée.
~~~~

### Référence courante reference-composition-4f43b97aaed5

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 158. SHA-256 : `4f43b97aaed55b2b87629f7cc9dfae67e927a01213a4051882f1cc89c67f335e`.

Scénarios : PBO seul disponible.

~~~~text
### Requirement: Composition ZT initiale et Domaines

La qualification MUST distinguer PBO composé, PA/PZT disponibles, ZT entièrement initialisé et Domaine opérationnel. Les minima MUST suivre pixs-instance, pixs-domains et zt-instances ; un contrat pur ou artefact présent MUST NOT prouver ces états. Le premier PZT complet MUST cibler Debian/Linux et les autres profils MUST déclarer leurs rôles qualifiés.

#### Scenario: PBO seul disponible

- **WHEN** PBO est qualifié mais aucun exécutant CZT/DZT/PKIZT n’est admissible
- **THEN** la composition ne revendique pas ZT initialisé ni création de Domaine admissible.
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

## Statut au 20 octobre 2026

Neuf changes restent ouverts. Les seuls deltas de define-essential-autonomous-auth-module sont adoptés le 20 octobre 2026 dans authentication, core et reference-composition : neuf exigences ajoutées, une modifiée et treize scénarios supplémentaires nets. Les huit autres dossiers conservent leurs deltas proposés. Les 83 tâches restent non cochées ; aucun code, manifest produit, dépendance, service ou migration n'est produit par cette adoption documentaire.

Les clauses canoniques continuent à s'appliquer tant que leurs modifications proposées ne sont pas adoptées. Les décisions du présent registre définissent le périmètre documentaire, sans prétendre que les choix détaillés, paramètres et preuves de compatibilité sont déjà arrêtés.

## Déclarations et dossiers propriétaires

| Déclaration retenue | Change ouvert | Deltas et état d'adoption |
| --- | --- | --- |
| pixs.auth essentiel indépendant ; dépendance publique vers Core ; local PostgreSQL par défaut ; politiques et sous-modules | [Architecture](proposal.md) | [authentication](historique-deltas-avant-e3/authentication/spec.md), [core](historique-deltas-avant-e3/core/spec.md), [reference-composition](historique-deltas-avant-e3/reference-composition/spec.md) — adoptés au canon le 20 octobre 2026 |
| Mot de passe, passkeys/WebAuthn, TOTP, MFA et récupération locaux ; moyens matériels extensibles | [Méthodes locales](../add-auth-local-authenticators-and-mfa/proposal.md) | [auth-authenticators](../add-auth-local-authenticators-and-mfa/specs/auth-authenticators/spec.md) |
| Forge/enrôlement, preuves et liaison des moyens sans second référentiel | [Enrôlement](../add-auth-identity-enrollment/proposal.md) | [auth-identity-enrollment](../add-auth-identity-enrollment/specs/auth-identity-enrollment/spec.md) |
| Pixs fournisseur d'identité vers clients approuvés OIDC/SAML | [Émission d'identité](../add-auth-identity-provider/proposal.md) | [auth-identity-provider](../add-auth-identity-provider/specs/auth-identity-provider/spec.md) |
| Annuaire OpenLDAP propre activable ; projection, authentification et stockage Core déclarés séparément | [OpenLDAP géré](../add-auth-managed-openldap/proposal.md) | [auth-managed-directory](../add-auth-managed-openldap/historique-deltas-avant-e3/auth-managed-directory/spec.md), [directory-projections](../add-auth-managed-openldap/historique-deltas-avant-e3/directory-projections/spec.md) |
| KDC propre activable seul ou avec backend LDAP explicitement sélectionné | [KDC géré](../add-auth-managed-kerberos-kdc/proposal.md) | [auth-managed-kerberos](../add-auth-managed-kerberos-kdc/historique-deltas-avant-e3/auth-managed-kerberos/spec.md) |
| Sources externes LDAP/Kerberos/OIDC/SAML installables, absentes du profil standard | [Connecteurs externes](../add-auth-external-source-submodules/proposal.md) | [auth-external-sources](../add-auth-external-source-submodules/specs/auth-external-sources/spec.md) |
| pixs.auth.directory.ad pour un domaine Active Directory propre, non activé par défaut | [Active Directory géré](../add-auth-managed-active-directory/proposal.md) | [auth-managed-active-directory](../add-auth-managed-active-directory/historique-deltas-avant-e3/auth-managed-active-directory/spec.md) |
| Utilisateurs/groupes/ACL initialement dans PostgreSQL ; migration postinstallation vers OpenLDAP interne ; retour depuis les données LDAP courantes | [Stockage Core réversible](../add-reversible-core-directory-storage/proposal.md) | [core-storage](../add-reversible-core-directory-storage/specs/core-storage/spec.md), [core](../add-reversible-core-directory-storage/specs/core/spec.md), [directory-projections](../add-reversible-core-directory-storage/specs/directory-projections/spec.md), [reference-runtime](../add-reversible-core-directory-storage/specs/reference-runtime/spec.md) |

## Frontières communes à appliquer

- Core garde les identités canoniques, relations, groupes et droits ; Auth gère l'authentification, ses moyens, politiques et sessions, et le contrôle de ses services propres.
- PostgreSQL est le stockage par défaut ; la seule exception Core de ces dossiers est l'OpenLDAP interne engagé par migration réversible. Les autres domaines restent sur leur stockage déclaré.
- La projection LDAP reste une copie de consultation sans ACL Pixs. Le stockage Core LDAP peut conserver les ACL applicatives, dont l'évaluation reste dans Pixs. Les ACL techniques slapd ne les remplacent pas.
- L'activation d'OpenLDAP, du KDC, d'AD ou d'un émetteur IdP n'installe aucun connecteur externe et ne migre aucune donnée Core par effet de bord.
- L'aller et le retour Core conservent UUID, relations, états, versions, révocations et tombstones ; le retour ne réactive pas une ancienne copie PostgreSQL et la panne ne vaut pas migration.
- L'exception Super Admin reste celle du canon dans son seul périmètre, sans création de preuve MFA, de conformité cryptographique ou de résultat de migration absent.

## Raccordements existants et limites

[C03](../archive/2026-10-21-add-initial-authentication-and-sessions/design.md) conserve connexion et sessions ; [C02](../archive/2026-10-20-add-core-postgres-services/design.md) conserve le provider PostgreSQL initial. [C08](../add-installation-and-first-configuration/design.md) porte le provisionnement, [C13](../add-initial-administration-panel/design.md) l'administration, [C17](../qualify-first-pbo-composition/design.md) la qualification de l'artefact sélectionné. Les dossiers de projection [O08](../add-ldap-outbound-directory-projections/design.md) et de lecture fraîche [O09](../add-directory-read-freshness-and-postgres-fallback/design.md) restent limités à leur rôle de projection.

Les produits, versions, paramètres, schémas physiques, profils de protocole, garanties LDAP multi-objets et mécanismes de bascule restent à préciser et qualifier avant code. DEVOPS.md reste un inventaire d'environnement ; la présence d'un outil n'y prouve ni installation d'une capacité proposée ni qualification de celle-ci.

## Statut des deltas antérieurs après contrôle E3

Les anciens fichiers sous specs/ ont été déplacés, avec empreintes conservées, vers [l’historique interne](historique-deltas-avant-e3/README.md). Le [contrôle de couverture](COUVERTURE_DELTAS_E3.md) relie chaque ancienne exigence au contrat courant et aux tâches ouvertes. Le dossier reste actif ; skip_specs évite seulement la réapplication des anciennes prescriptions. Il ne termine ni la réalisation, ni les tests, ni les 49 tâches encore ouvertes dans les sept dossiers concernés.
