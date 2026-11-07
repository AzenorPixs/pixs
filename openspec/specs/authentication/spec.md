# authentication Specification

## Purpose
L'authentification vérifie les identités via des fournisseurs déclarés et approuvés, sans déplacer la source de vérité des utilisateurs, groupes et appartenances hors de Pixs.

## Requirements

### Requirement: Fournisseurs déclarés et confiance explicite

Chaque fournisseur (local, OIDC, SAML) MUST déclarer protocole, émetteurs, audiences, algorithmes, clés, claims obligatoires et mappings ; la seule validité cryptographique MUST NOT suffire sans confiance applicative configurée.

#### Scenario: Émetteur non approuvé refusé

- **WHEN** un jeton valide émane d'un émetteur non approuvé
- **THEN** l'authentification est refusée avec une erreur stable et un audit

### Requirement: Identifiant externe canonique et liaison explicite

Le système MUST respecter les garanties suivantes.

L'identifiant externe canonique est le triplet fournisseur, émetteur, sujet ; toute liaison à une identité existante est explicite, vérifiée des deux côtés, idempotente et auditée ; aucun rapprochement par courriel seul.

#### Scenario: Courriel seul non rapproché

- **WHEN** deux comptes partagent la même adresse sans preuve bilatérale
- **THEN** aucune fusion n'a lieu et une liaison explicite reste exigée

### Requirement: Sessions bornées et révocation propagée

Sessions, jetons et renouvellements MUST être bornés et rotatifs, avec détection de réutilisation. Toute révocation d’identité, justificatif, session ou confiance MUST invalider les contextes concernés sans supprimer les données métier. L’audit MUST suivre audit, sans secret, avec son exception limitée au retrait d’accès Auth. Révocation persistante et audit réussi MUST NOT être annoncés sans leur preuve.

#### Scenario: Révocation propagée
- **WHEN** une identité ou une session est révoquée
- **THEN** les contextes dérivés sont invalidés avant toute nouvelle opération sensible

#### Scenario: Retrait sans audit confirmé
- **WHEN** seul l’audit est indisponible et qu’un retrait d’accès Auth autorisé est persisté selon l’exception dédiée
- **THEN** les contextes concernés sont invalidés et l’échec d’audit reste signalé pour réconciliation sans audit fictif

### Requirement: Module essentiel autonome pixs.auth

Toute composition applicative Pixs MUST inclure `pixs.auth`, module essentiel indépendant de `pixs.core`, avec une capacité locale autonome sélectionnée explicitement par le profil. Son absence MUST empêcher l'activation applicative. Les fixtures structurelles non applicatives MUST rester distinguées de ce profil.

#### Scenario: Composition applicative sans Auth
- **WHEN** une composition applicative omet pixs.auth ou sa capacité locale requise
- **THEN** sa validation échoue avant activation sans annoncer d'authentification disponible

#### Scenario: Fixture structurelle isolée
- **WHEN** un test manipule seulement un contrat pur Core sans runtime applicatif
- **THEN** il reste possible sans Auth et ne constitue pas une composition applicative qualifiée

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

### Requirement: Propriété des données Auth et protection des justificatifs

pixs.auth MUST posséder ses justificatifs, liaisons d'authentification, politiques et sessions, rattachés aux identités Core par contrat public. Les mots de passe MUST être stockés uniquement sous empreinte sécurisée ; les jetons réutilisables, clés privées et secrets MFA MUST NOT être stockés en clair dans les tables métier, manifests ou journaux. Les secrets réversibles MUST suivre les contrats de protection et de secrets applicables.

#### Scenario: Session persistée
- **WHEN** Auth conserve une session ou un renouvellement
- **THEN** l'enregistrement permet expiration et révocation sans exposer le jeton brut réutilisable

#### Scenario: Liaison avec Core
- **WHEN** Auth rattache un moyen à une DigitalIdentity
- **THEN** la référence est vérifiée par contrat public sans écriture directe dans les tables Core

### Requirement: Sous-modules Auth composés par les mécanismes communs

Les méthodes locales, l'enrôlement, l'émission d'identité, les services gérés et les sources externes MUST être extensibles par composants déclarés et contrats versionnés. Les sous-modules MUST utiliser le manifest et le lifecycle communs sans registre parallèle. L'installation d'un sous-module MUST NOT suffire à activer une confiance ou un service.

#### Scenario: Source installée sans confiance
- **WHEN** un sous-module de source est installé sans configuration de confiance validée
- **THEN** il ne peut authentifier aucune identité

### Requirement: Politiques Auth déclaratives et contextualisées

Les politiques Auth MUST être typées, versionnées et résolues déterministiquement selon Instance, Domaine, profil et contexte tenant/scope applicable. Méthodes, MFA, fraîcheur, sessions, récupération et confiance MUST exposer origine et valeur effective sans secret. Une règle contradictoire MUST bloquer l'opération sans sélection opportuniste de la moins exigeante.

#### Scenario: Politique contradictoire

- **WHEN** les règles ne permettent pas de déterminer l’assurance applicable
- **THEN** Auth refuse avec diagnostic sans réduire implicitement les exigences.

### Requirement: Absence de repli implicite entre méthodes et sources

Une indisponibilité externe MUST NOT activer une authentification locale ou diminuer l'assurance requise. La coexistence des sources et méthodes MUST suivre une politique explicite et préserver la liaison canonique. Le compte de secours MUST conserver son authentification propre et son exception selon authorization et initial-administration, sans extension aux comptes ordinaires.

#### Scenario: IdP externe indisponible
- **WHEN** une politique impose un IdP externe indisponible pour un compte ordinaire
- **THEN** un mot de passe local ne devient pas un repli autorisé par cette seule panne

#### Scenario: Secours propre du Super Admin
- **WHEN** le Super Admin utilise son parcours canonique de secours sans MFA
- **THEN** son exception reste applicable sans attribuer un niveau MULTI_FACTOR non obtenu

### Requirement: Interfaces spécialisées du profil Auth local

Le profil local MUST exposer des interfaces spécialisées d’authentification, de sessions et de justificatifs, typées et versionnées dans le même module pixs.auth. Les façades web, API et CLI MUST réutiliser ces contrats. Auth MUST référencer les identités Core par UUID et ports publics, posséder ses écritures et MUST NOT exposer de modèle Django privé ni écrire dans les tables privées d’un autre module.

#### Scenario: Session liée à Core
- **WHEN** une façade demande une session
- **THEN** Auth vérifie la référence et l’état Core par port public puis possède ses écritures, sans modèle privé exposé

### Requirement: Justificatifs opaques et stockage serveur par empreinte

Le profil local MUST utiliser des identifiants de session et jetons API/CLI opaques issus d’un générateur aléatoire cryptographiquement sûr. Les justificatifs remis au client MUST être conservés côté serveur uniquement sous empreinte de vérification, avec état, expiration et révocation dans PostgreSQL. Un backend conservant leur valeur brute MUST NOT être repris sans adaptation conforme.

#### Scenario: Justificatif brut absent
- **WHEN** Auth persiste une session ou un jeton
- **THEN** la vérification par empreinte et la révocation sont possibles sans stocker ni journaliser le justificatif brut réutilisable

### Requirement: État Auth courant requis

Un contrôle nécessitant l’état Auth courant MUST échouer fermé si cet état ne peut pas être vérifié. PostgreSQL indisponible MUST NOT entraîner un repli vers un fichier ou un jeton supposé valide.

#### Scenario: État inaccessible
- **WHEN** PostgreSQL Auth ne permet pas de vérifier l’état courant requis
- **THEN** l’accès est refusé sans repli implicite

### Requirement: Durées des sessions locales ordinaires

Par défaut, les sessions ordinaires MUST expirer après 60 minutes d’inactivité ou 12 heures au total et les sessions d’administration ordinaires après 15 minutes d’inactivité ou 2 heures au total, selon la première échéance atteinte.

#### Scenario: Inactivité ordinaire
- **WHEN** une session ordinaire atteint 60 minutes sans activité admissible sous politique par défaut
- **THEN** elle expire même si son plafond absolu de 12 heures n’est pas atteint

#### Scenario: Plafond administratif
- **WHEN** une session d’administration ordinaire atteint 2 heures sous politique par défaut malgré une activité récente
- **THEN** elle expire sans prolongation par activité ou renouvellement

### Requirement: Durée des accès et fraîcheur sensible

Le profil local MUST limiter par défaut les jetons d’accès API/CLI à 15 minutes et à la validité restante applicable. Une opération sensible MUST exiger par défaut une authentification datant de moins de 5 minutes et les niveaux d’assurance réellement requis, sans assurance inventée.

#### Scenario: Validité restante courte
- **WHEN** la session expire dans moins de 15 minutes lors d’une émission
- **THEN** le jeton n’est utilisable que pendant cette validité restante ou moins

#### Scenario: Fraîcheur insuffisante
- **WHEN** un compte ordinaire demande une action sensible avec une authentification datant de 5 minutes ou davantage sous politique par défaut
- **THEN** une réauthentification conforme est exigée avant l’effet sensible

### Requirement: Politique configurable et exceptions canoniques

Durées, fraîcheur et plafonds de sessions MUST être configurables par politique typée/versionnée exposant valeur effective et origine. Les exceptions canoniques du seul Super Admin MUST rester préservées sans s’étendre aux administrateurs ordinaires ni fabriquer d’assurance. Une invalidation courante MUST pouvoir écourter la validité annoncée.

#### Scenario: Politique résolue
- **WHEN** une politique qualifiée remplace une valeur par défaut pour un compte ordinaire
- **THEN** la valeur effective et son origine sont connues et les invalidations courantes restent applicables

### Requirement: Renouvellement rotatif à usage unique

Le renouvellement API/CLI MUST employer un jeton à usage unique remplacé atomiquement à chaque renouvellement réussi. Il MUST NOT repousser le plafond absolu de session ni la date réelle d’authentification. Les secrets de renouvellement MUST rester soumis au stockage serveur par empreinte.

#### Scenario: Rotation réussie
- **WHEN** un renouvellement valide est confirmé
- **THEN** le jeton consommé ne peut plus produire de rotation et ni plafond absolu ni date réelle d’authentification ne changent

### Requirement: Activité utilisateur et renouvellement

Les activités repoussant l’inactivité MUST être déclarées et contrôlées côté serveur. Le renouvellement seul MUST NOT compter comme activité utilisateur. Les appels d’arrière-plan et répétitions automatiques MUST NOT être assimilés implicitement à une action utilisateur.

#### Scenario: Renouvellements seuls
- **WHEN** un client renouvelle périodiquement sans activité utilisateur admissible
- **THEN** la session expire à son échéance d’inactivité sans prolonger son plafond absolu

### Requirement: Concurrence et réponse perdue de rotation

Les concurrences et répétitions reconnues MUST NOT émettre un second renouvellement pour un jeton consommé. La perte d’une réponse MAY imposer une nouvelle authentification ; le système MUST NOT promettre la restitution d’un nouveau secret conservé seulement sous empreinte.

#### Scenario: Deux appels concurrents
- **WHEN** deux requêtes consomment le même jeton de renouvellement
- **THEN** au plus une rotation est confirmée, sans seconde émission

#### Scenario: Réponse perdue
- **WHEN** une rotation est committée mais sa réponse contenant le nouveau secret est perdue
- **THEN** la reprise ne produit pas de second renouvellement et peut imposer une nouvelle authentification

### Requirement: Réutilisation suspecte et révocation de session

Une réutilisation suspecte d’un jeton consommé MUST révoquer la session concernée et tous ses jetons dérivés, sans fermeture automatique des autres sessions du compte. Une déconnexion globale MAY être décidée par traitement d’incident autorisé. La détection MUST distinguer répétitions reconnues et concurrences légitimes d’une réutilisation suspecte selon un contrat explicite, sans seconde émission.

#### Scenario: Réutilisation suspecte
- **WHEN** le mécanisme qualifié classe une réutilisation comme suspecte
- **THEN** la session et ses dérivés sont invalidés, les autres sessions restant ouvertes sauf révocation globale autorisée

### Requirement: Plafond et remplacement explicite des sessions

La politique par défaut MUST limiter un compte à 5 sessions ordinaires et 2 sessions d’administration ordinaires selon leur catégorie, avec admission contrôlée atomiquement. À la limite atteinte, une admission MUST exiger le choix explicite d’une session à fermer ou être refusée ; elle MUST NOT déconnecter silencieusement une session existante.

#### Scenario: Limite atteinte
- **WHEN** une sixième session ordinaire est demandée sous politique par défaut sans remplacement choisi
- **THEN** l’admission est refusée sans fermeture silencieuse

#### Scenario: Admissions concurrentes
- **WHEN** plusieurs admissions tentent de consommer le dernier emplacement autorisé
- **THEN** le contrôle atomique empêche de dépasser le plafond effectif

### Requirement: Onglets et renouvellements sans nouvelle session

Les onglets partageant le même cookie et le renouvellement de jetons MUST NOT compter comme de nouvelles sessions.

#### Scenario: Même cookie
- **WHEN** plusieurs onglets partagent une session ou un client renouvelle ses jetons
- **THEN** aucun emplacement supplémentaire n’est consommé par cette seule opération

### Requirement: Changement de mot de passe sans reconnexion automatique

Le changement de mot de passe MUST être piloté par Auth depuis un PBO habilité. Le profil MUST distinguer les contextes : changement authentifié révoquant par défaut les autres sessions avec conservation possible de la session courante après vérification ; récupération/réinitialisation révoquant toutes les sessions de l'identité par défaut. La politique MAY être ajustée explicitement ; une reconnexion ou assurance supérieure MUST NOT être déduite du changement.

#### Scenario: Changement authentifié par défaut

- **WHEN** une identité change son mot de passe depuis sa session vérifiée
- **THEN** les autres sessions sont révoquées et seule la session courante peut être conservée après vérification.

#### Scenario: Autre identité du même individu

- **WHEN** le mot de passe d’une identité courante change
- **THEN** les sessions de son identité administrative suivent leur politique propre.

### Requirement: Récupération et compromission du mot de passe

Récupération et réinitialisation MUST suivre leur profil et révoquer toutes les sessions de l'identité par défaut ; une compromission suspectée MUST déclencher le retrait prévu sans assurance restaurée implicitement. Un retrait d'accès malgré panne d'audit MUST suivre audit et MUST NOT confirmer un justificatif non committé. Les tickets Kerberos déjà délivrés MUST être traités séparément des sessions Pixs.

#### Scenario: Récupération sans MFA

- **WHEN** une récupération autorisée ne fournit pas de nouvelle preuve MFA
- **THEN** les sessions sont révoquées selon le profil sans assurance multifacteur inventée.

#### Scenario: Changement non confirmé

- **WHEN** seul le retrait est confirmé après échec de mutation
- **THEN** aucun nouveau mot de passe n’est annoncé committé.

### Requirement: Argon2id via les outils Django

Le profil local MUST protéger les mots de passe avec Argon2id via Django et argon2-cffi, avec versions stables épinglées et paramètres qualifiés pour les versions Python supportées. Il MUST NOT implémenter d’algorithme de hachage personnalisé ni abaisser sa protection pour une intégration.

#### Scenario: Paramètres qualifiés
- **WHEN** une version du profil local est préparée pour réalisation
- **THEN** la compatibilité des versions et les coûts mémoire/calcul sont qualifiés sans dépendance installée par la seule spécification

### Requirement: Réutilisation Argon2id dans un profil OpenLDAP qualifié

La réutilisation d’une empreinte Argon2id par un futur profil OpenLDAP sélectionné MUST être qualifiée avec son module Argon2 et une adaptation d’enveloppe préservant variante, version, paramètres, sel et résultat. Un format ou paramètre incompatible MUST être refusé explicitement, sans repli vers un hachage plus faible.

#### Scenario: Vérification croisée
- **WHEN** un profil OpenLDAP sélectionné est qualifié pour l’empreinte produite par Django
- **THEN** la même empreinte adaptée accepte le bon mot de passe et refuse le mauvais sans réhachage ni affaiblissement

#### Scenario: Profil incompatible
- **WHEN** une variante, version, enveloppe ou un paramètre n’est pas accepté
- **THEN** la compatibilité est refusée sans hachage affaibli ni succès de qualification annoncé

### Requirement: Limites de la compatibilité des empreintes

L’adaptation d’enveloppe MUST NOT être présentée comme récupération du mot de passe ou conversion en clé Kerberos ou Active Directory. Elle MUST NOT activer un annuaire ni dupliquer des justificatifs implicitement. PostgreSQL MUST rester distingué comme stockage applicatif de l’empreinte, sans assimilation à l’authentification de ses comptes techniques.

#### Scenario: Compatibilité documentaire seule
- **WHEN** la possibilité de réutilisation est documentée
- **THEN** aucun service LDAP, copie de justificatif, conversion de clé ou changement d’authentification PostgreSQL n’est engagé

### Requirement: Conservation du renouvellement de la CLI interactive

La CLI interactive MUST conserver le jeton entre lancements uniquement dans un trousseau système disponible et qualifié. Sinon, elle MUST le garder en mémoire jusqu’à la fin du processus et MUST NOT se rabattre automatiquement sur un fichier en clair. Cette conservation MUST respecter expiration, révocation et plafonds ; elle MUST NOT créer de session permanente ni de compte de service.

#### Scenario: Trousseau indisponible
- **WHEN** aucun trousseau qualifié n’est utilisable
- **THEN** le jeton reste en mémoire du processus et le lancement suivant demande une nouvelle connexion sans fichier de repli clair

### Requirement: Mot de passe commun par identité numérique

Une identité numérique MUST utiliser un mot de passe commun pour ses méthodes PG/LDAP/Kerberos qui en emploient un. Auth MUST coordonner les représentations de vérification et clés propres à ces méthodes, sans supposer une conversion depuis un hash PG. Les identités distinctes d'un individu MUST garder leurs propres moyens et profils.

#### Scenario: Deux identités

- **WHEN** un individu possède des comptes courant et administratif
- **THEN** le mot de passe commun concerne les méthodes de chaque identité sans imposer un secret unique à l’individu.

### Requirement: Changement uniquement depuis PBO

Les mots de passe des individus MUST être changés depuis PBO sous pilotage Auth. Le PBO logique Standalone MUST pouvoir porter cette fonction ; en Domaine elle MAY être sur le contrôleur ou un autre PBO habilité. Les rotations de secrets machine et services MUST rester distinctes de cette règle.

#### Scenario: Changement natif non prévu

- **WHEN** une application tente d’utiliser une voie native non autorisée pour changer le mot de passe individuel
- **THEN** la voie est refusée ou non proposée sans contourner PBO.

### Requirement: Récupération configurable et désactivée par défaut

Auth MUST proposer changement individuel, réinitialisation par administrateur habilité et récupération autonome configurable/débrayable. La récupération autonome MUST être désactivée par défaut et ses moyens activés explicitement par profil. Les politiques de mot de passe MUST pouvoir se décliner Instance/Domaine/profil, les domaines et profils ajoutant leurs contraintes au socle.

#### Scenario: Récupération non activée

- **WHEN** un individu demande le parcours autonome avec le profil par défaut
- **THEN** ce parcours reste désactivé sans créer de moyen de récupération implicite.

### Requirement: MFA choisie par profil et chemins qualifiés

La MFA MUST être configurable par profil, y compris administratif, sans obligation générale Pixs. TOTP et clés/passkeys MUST être sélectionnables sur les chemins qualifiés ; un profil exigeant MFA MUST refuser un chemin incapable de fournir l'assurance. Gestion des facteurs MUST pouvoir être individuelle ou administrative sous habilitations et profil.

#### Scenario: Chemin non qualifié

- **WHEN** un profil exige MFA sur un chemin non qualifié
- **THEN** l’authentification est refusée sans annoncer la MFA depuis un seul facteur.

### Requirement: Changements effectifs et contrôleurs à jour

Chaque profil MUST choisir entre confirmation de tous les contrôleurs déclarés ou de ceux maintenus en service après exclusion effective vérifiée des autres. Un défaut général MUST NOT être déduit. Le simple défaut de joignabilité MUST NOT prouver l'exclusion ni diminuer le minimum synchrone PG. La réadmission MUST être manuelle ou automatique selon profil après vérification identité, habilitations et révisions.

#### Scenario: Contrôleur isolé encore actif

- **WHEN** un contrôleur non à jour reste susceptible d’authentifier sur un réseau isolé
- **THEN** le changement n’est pas déclaré effectif tant que sa mise à jour ou son exclusion exigée n’est pas prouvée.

### Requirement: Verrouillage commun et états dépendants

Les méthodes PG/LDAP/Kerberos concernées MUST coordonner un verrouillage par identité numérique. Les autres identités de l'individu MUST garder leurs états, sauf suspension globale Core. Les accès et mandats dépendants MUST suivre les révocations et continuités de zt-instances sans repli permissif.

#### Scenario: Échecs sur LDAP

- **WHEN** les échecs atteignent la limite applicable à l’identité via LDAP
- **THEN** le même état de verrouillage s’applique aux autres méthodes concernées sans verrouiller une autre identité par déduction.
