# Références normatives — add-auth-local-authenticators-and-mfa

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
| identity-assurance | Assurance et exception Super Admin | 1 | identity-assurance-f8c3e9f871f6 |
| identity-assurance | Contexte vérifié et dimensions distinctes | 1 | identity-assurance-912c1b51e780 |
| identity-assurance | Seuil sensible et élévation explicite | 1 | identity-assurance-46750cd438c9 |
| identity-assurance | Fraîcheur, révocation et récupération sans élévation implicite | 1 | identity-assurance-c1320e1ca2ef |
| identity-assurance | Vocabulaire structurel préparatoire IdentityAssurance v1 | 3 | identity-assurance-67e754b2229c |
| identity-assurance | Absence d'effets du vocabulaire IdentityAssurance v1 | 1 | identity-assurance-d0b09e6d213b |
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

### Référence courante identity-assurance-f8c3e9f871f6

Source : [identity-assurance](../../specs/identity-assurance/spec.md), ligne 8. SHA-256 : `f8c3e9f871f618ebc643c4e7fff45c0503cd5d403758e7322ef938cb783f8c57`.

Scénarios : Secours avec assurance réellement obtenue.

~~~~text
### Requirement: Assurance et exception Super Admin

Les contrôles d'assurance MUST s'appliquer sous réserve de l'exception Super Admin de `authorization`. Au premier démarrage et à la réactivation de secours de ce compte, le MFA MUST NOT être exigé, conformément à `initial-administration`. Les niveaux d'assurance MUST décrire les preuves réellement obtenues ; une dérogation MUST NOT augmenter artificiellement un niveau.

#### Scenario: Secours avec assurance réellement obtenue

- **WHEN** le Super Admin se réactive en secours avec son authentification propre sans MFA
- **THEN** l'absence de MFA ne bloque pas l'accès de secours et le contexte ne déclare pas MULTI_FACTOR sans preuve
~~~~

### Référence courante identity-assurance-912c1b51e780

Source : [identity-assurance](../../specs/identity-assurance/spec.md), ligne 17. SHA-256 : `912c1b51e7803f60984ba1a1d0f3dd85f23cc10b75e6b09bd7eb005530b07762`.

Scénarios : Claim absent sans surclassement.

~~~~text
### Requirement: Contexte vérifié et dimensions distinctes

Le système MUST respecter les garanties suivantes.

Toute authentification réussie produit un contexte vérifié, limité dans le temps, rattaché à une identité numérique et au périmètre applicable, avec assurance d'identité, assurance d'authentification et confiance fédérée évaluées séparément selon le mapping déclaré du fournisseur.

#### Scenario: Claim absent sans surclassement

- **WHEN** une preuve ou un claim est absent, ambigu ou expiré
- **THEN** le niveau d'assurance n'est jamais augmenté implicitement
~~~~

### Référence courante identity-assurance-46750cd438c9

Source : [identity-assurance](../../specs/identity-assurance/spec.md), ligne 28. SHA-256 : `46750cd438c9bf9f52268c2d2ba212737e6b896fb7988fae6f7673afc04f982e`.

Scénarios : Élévation exigée.

~~~~text
### Requirement: Seuil sensible et élévation explicite

Le profil MUST définir l'assurance requise pour ses opérations, y compris administratives, avec MFA configurable sans obligation générale Pixs. L'opération MUST vérifier le seuil effectivement sélectionné et refuser ou demander un step-up si nécessaire. Le frontal MUST NOT simuler cette élévation et un profil MUST NOT annoncer une assurance que son chemin ne peut qualifier.

#### Scenario: Élévation exigée

- **WHEN** le profil exige une assurance supérieure à celle effectivement obtenue
- **THEN** le système refuse ou engage une élévation explicite selon le contrat.
~~~~

### Référence courante identity-assurance-c1320e1ca2ef

Source : [identity-assurance](../../specs/identity-assurance/spec.md), ligne 37. SHA-256 : `c1320e1ca2efcf467e810c31230e1e75d56186164cf5f2ca93eaaae1f172ef2c`.

Scénarios : Récupération sans restauration d'assurance.

~~~~text
### Requirement: Fraîcheur, révocation et récupération sans élévation implicite

Le système MUST respecter les garanties suivantes.

Expiration, fraîcheur maximale, rotation et révocation sont vérifiées avant toute décision sensible ; une récupération invalide les sessions concernées sans restaurer implicitement un niveau élevé.

#### Scenario: Récupération sans restauration d'assurance

- **WHEN** un compte est récupéré après compromission
- **THEN** les niveaux élevés restent perdus jusqu'à nouvelle preuve ou intervention autorisée
~~~~

### Référence courante identity-assurance-67e754b2229c

Source : [identity-assurance](../../specs/identity-assurance/spec.md), ligne 48. SHA-256 : `67e754b2229cff83359d5f7d1fd315e9ae7e41038eeb2e9129df0ced4ca80dbf`.

Scénarios : Valeurs fermées sans effet; Valeur étrangère refusée; Absence sans défaut implicite.

~~~~text
### Requirement: Vocabulaire structurel préparatoire IdentityAssurance v1

Le vocabulaire structurel préparatoire IdentityAssurance v1 MUST admettre exactement CLAIMED, VERIFIED et PROOFED. Toute autre valeur MUST être refusée. Sa représentation MUST NOT fournir de valeur par défaut, de classement ordinal, de mapping fournisseur ou de transition.

#### Scenario: Valeurs fermées sans effet

- **WHEN** Une des valeurs CLAIMED, VERIFIED ou PROOFED est représentée
- **THEN** Seul ce vocabulaire structurel est produit, sans preuve, droit, session, audit ni persistance

#### Scenario: Valeur étrangère refusée

- **WHEN** Une valeur étrangère au vocabulaire est présentée
- **THEN** La représentation est refusée sans augmentation implicite du niveau

#### Scenario: Absence sans défaut implicite

- **WHEN** Aucune valeur n’est fournie
- **THEN** Le profil ne choisit aucun niveau par défaut
~~~~

### Référence courante identity-assurance-d0b09e6d213b

Source : [identity-assurance](../../specs/identity-assurance/spec.md), ligne 67. SHA-256 : `d0b09e6d213b294370690dea58af6c2083ecd7b8d7275e87755d4d39991694b4`.

Scénarios : Valeur représentée sans assurance calculée.

~~~~text
### Requirement: Absence d'effets du vocabulaire IdentityAssurance v1

La représentation IdentityAssurance v1 MUST NOT établir une preuve, calculer ou augmenter une assurance, authentifier, créer une session, accorder un accès, produire un audit ou persister une donnée. Les garanties existantes de séparation des dimensions et de non-surclassement MUST rester applicables.

#### Scenario: Valeur représentée sans assurance calculée

- **WHEN** une valeur du vocabulaire IdentityAssurance v1 est représentée
- **THEN** aucune preuve, assurance calculée, authentification, session, permission, écriture d'audit ou persistance n'en découle
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
