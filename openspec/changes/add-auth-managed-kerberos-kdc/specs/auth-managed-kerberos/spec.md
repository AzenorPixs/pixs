## ADDED Requirements

### Requirement: KDC propre indépendant des sources externes

pixs.auth MUST pouvoir provisionner, configurer, démarrer, arrêter et superviser son propre KDC Kerberos par sous-module déclaré. L'activation MUST être explicite, possible sans OpenLDAP et indépendante d'un connecteur externe. Une dépendance LDAP MUST être déclarée seulement si le backend sélectionné l'exige.

#### Scenario: KDC sans annuaire

- **WHEN** une composition autorisée sélectionne un backend KDC sans LDAP
- **THEN** le KDC propre peut être activé sans OpenLDAP ni realm externe

#### Scenario: Backend LDAP sans annuaire

- **WHEN** le backend choisi exige LDAP mais sa dépendance n'est pas satisfaite
- **THEN** l'activation concernée est refusée sans changer de backend implicitement

### Requirement: Principals liés aux identités canoniques

Chaque principal ou identité de service géré MUST être rattaché explicitement au référentiel Core et à son périmètre par mapping Auth persistant, PostgreSQL par défaut. Realm, principal et validité d'un ticket MUST NOT créer une identité, une appartenance ou une permission Pixs par simple correspondance de nom.

#### Scenario: Principal au nom d'un administrateur

- **WHEN** un ticket valide contient un nom similaire à un administrateur Pixs sans liaison approuvée
- **THEN** aucun droit ni lien automatique n'est accordé

### Requirement: Protection et amorçage des clés Kerberos

Le KDC MUST protéger clés maîtresses, clés de principals et keytabs sous identités techniques minimales, avec rotation et récupération déclarées. Ces secrets MUST NOT être en clair dans les tables métier, artefacts ou journaux. L'amorçage MUST NOT dépendre circulairement d'une authentification par le KDC à ouvrir.

#### Scenario: Keytab demandée hors périmètre

- **WHEN** un service demande la keytab d'un autre service sans autorisation
- **THEN** la remise est refusée et aucune clé n'est exposée

#### Scenario: Conversion d'une empreinte locale

- **WHEN** un plan suppose de produire une clé Kerberos depuis le seul hash du mot de passe Pixs
- **THEN** le plan est refusé jusqu'à définition d'un enrôlement cryptographique compatible

### Requirement: Tickets bornés et limites de révocation explicites

Le KDC MUST déclarer confiance des realms, prérequis temporels, durées et renouvellement. Un retrait MUST empêcher nouvelles émissions et renouvellements selon la borne déclarée. Pixs MUST vérifier son état courant avant opération sensible ; l'effet sur les tickets déjà délivrés aux tiers MUST être explicite sans révocation instantanée supposée.

#### Scenario: Ticket encore valide après retrait

- **WHEN** une identité révoquée présente à Pixs un ticket non expiré
- **THEN** le ticket ne contourne pas le contrôle courant et aucun droit sensible n'est accordé

#### Scenario: Service tiers sans garantie suffisante

- **WHEN** un client ne peut respecter la borne de révocation exigée
- **THEN** la composition ne qualifie pas ce client pour l'usage sensible concerné

### Requirement: Reprise du KDC sans résurrection des accès

Avant réadmission d'un KDC restauré, le service MUST réconcilier générations de clés, mappings, retraits et politiques courants. Les dépendances temporelles ou de secrets non vérifiables MUST empêcher sa readiness. La restauration MUST NOT réactiver implicitement un principal retiré.

#### Scenario: Ancienne base de principals restaurée

- **WHEN** un snapshot contient un principal retiré après sa date
- **THEN** l'émission reste bloquée pour ce principal jusqu'à réconciliation de l'état courant
