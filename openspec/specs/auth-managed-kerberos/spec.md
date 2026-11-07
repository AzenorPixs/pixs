# auth-managed-kerberos Specification

## Purpose

KZT fournit MIT Kerberos pour chaque Domaine avec backend OpenLDAP, sous exploitation PA et politiques Auth.

Cible documentaire du cadrage validé du 31 octobre 2026 ; les contrats proposés existants de cette capacité sont à réconcilier avec ce référentiel avant réalisation. Aucun fournisseur ni plateforme n’est réputé qualifié par cette rédaction.

## Requirements

### Requirement: KZT obligatoire et backend OpenLDAP

Chaque Domaine MUST disposer d'au moins un KZT/MIT Kerberos à backend OpenLDAP et MAY avoir plusieurs KZT actifs. En mode normal, l'état opérationnel Kerberos durable MUST résider dans LDAP ; PG MUST garder les références Pixs. PA MUST installer/configurer/exploiter et Auth piloter les politiques. Un backend PG natif MIT ou un engagement PG préalable de chaque écriture KDC MUST NOT être supposé.

#### Scenario: LDAP normal indisponible

- **WHEN** le backend OpenLDAP exigé devient indisponible
- **THEN** les fonctions dépendantes suivent leur dégradation et aucune base Kerberos PG de remplacement n’est activée implicitement.

### Requirement: Realm propre et mappings explicites

Chaque Domaine MUST déclarer un realm propre partagé par ses KZT et unique dans l'Instance. Les principals et identités de service MUST être liés explicitement aux identités Core et périmètres. Realm, nom ou ticket MUST NOT créer d'identité ou permission par simple correspondance.

#### Scenario: Realm en collision

- **WHEN** un second Domaine demande un realm déjà utilisé dans l’Instance
- **THEN** la déclaration est refusée avant activation.

### Requirement: Protection et récupération des clés Kerberos

Clé maîtresse, clés de principals et keytabs MUST être protégées sous identités minimales, sans secret en clair dans tables métier, artefacts ou journaux. Les clés/états Kerberos durables normaux MUST rester dans le backend LDAP. Chaque Domaine MUST déclarer les moyens protégés et procédures de récupération, distincts des seules références PG et sans dépendance circulaire au KZT à reconstruire.

#### Scenario: Moyens locaux perdus

- **WHEN** les moyens d’ouverture KZT sont perdus malgré une sauvegarde LDAP
- **THEN** la procédure de récupération choisie est requise et LDAP seul ne prouve pas l’ouverture possible.

### Requirement: Verrouillage cohérent du realm

Les KZT actifs MUST partager un verrouillage global par realm cohérent par identité. En partition, la cohérence MUST primer sur la disponibilité des authentifications qui en dépendent. Les chemins PG/LDAP/Kerberos concernés MUST coordonner le verrouillage par identité numérique sans verrouiller les autres identités du même individu par déduction.

#### Scenario: Partition de contrôleurs

- **WHEN** un KZT ne peut vérifier l’état global exigé du verrouillage
- **THEN** il ne confirme pas l’authentification dépendante sur une copie possiblement périmée.

### Requirement: Provisionnement progressif par profil

Le provisionnement Kerberos MUST pouvoir être progressif, par administration ou libre-service sous profil explicite. Les identités nécessaires à l'administration globale MUST être prêtes avant activation du premier Domaine. Un compte MUST NOT utiliser Kerberos avant vérification de ses clés ; une session d'enrôlement limitée MUST NOT ouvrir les accès non qualifiés.

#### Scenario: Hash PG seul

- **WHEN** un plan suppose convertir le seul hachage PG en clés Kerberos
- **THEN** il est refusé jusqu’à un parcours de provisionnement compatible et vérifié.

### Requirement: Expiration stricte et état courant

Les tickets MUST être bornés et ne plus être utilisables ni renouvelables après leur échéance. Tous les chemins revendiquant cette garantie MUST être qualifiés, sans la déduire du seul réglage de tolérance d'horloge. Retrait MUST empêcher les nouvelles émissions/renouvellements ; les tickets déjà émis MUST rester soumis aux limites documentées et aux contrôles Pixs courants.

#### Scenario: Ticket expiré dans une tolérance native

- **WHEN** un ticket dépasse son échéance mais un composant permettrait encore une tolérance
- **THEN** le chemin ne doit pas accepter cet usage et reste non qualifié s’il ne peut garantir le refus.

### Requirement: Temps et confiance inter-realms

KZT MUST vérifier les exigences de temps du profil commun, sans imposer un serveur supplémentaire par Domaine. La confiance Kerberos inter-domaines MUST être une composante explicitement autorisée des approbations, avec sens, portée et collision de realms contrôlés. Une approbation ZT seule MUST NOT la créer.

#### Scenario: Approbation sans Kerberos

- **WHEN** deux Domaines ont une approbation réseau sans composante Kerberos
- **THEN** aucune confiance inter-realms n’est déduite.

### Requirement: Restauration sans résurrection

La réadmission KZT MUST vérifier état LDAP, générations de clés, mappings, politiques et retraits courants, en réconciliant les références PG souveraines et les preuves opérationnelles. Une ancienne projection Core MUST NOT remplacer PG ; une restauration LDAP MUST NOT réintroduire un principal retiré. Les garanties de protection, fraîcheur et verrouillage MUST être vérifiées avant readiness.

#### Scenario: Principal retiré restauré

- **WHEN** une ancienne sauvegarde contient un principal retiré depuis sa date
- **THEN** il n’est pas réadmis avant réconciliation courante et vérification du profil.

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

### Requirement: État critique distinct du mode d'exploitation

L'état critique de reconstruction MUST rester distinct des modes Standalone/ZT/Domaine et de la classe réseau Critique d'A05. Il MUST NOT provoquer un changement de mode ou une exemption d'autorisation implicite.

#### Scenario: Reconstruction dans un Domaine

- **WHEN** un Domaine entre en état critique pour reconstruire Kerberos
- **THEN** l'Instance reste en mode Domaine et les autorisations et mandats applicables restent requis
