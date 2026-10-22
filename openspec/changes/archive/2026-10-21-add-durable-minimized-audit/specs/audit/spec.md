## ADDED Requirements

### Requirement: Transaction commune des sessions et de leur audit requis

Dans le profil local PostgreSQL, création et renouvellement de session MUST confirmer l’état Auth et l’événement C05 requis dans une transaction commune par interfaces propriétaires participantes. Un module MUST NOT accéder directement aux tables privées d’un autre.

#### Scenario: Création et audit liés
- **WHEN** une session ordinaire est créée
- **THEN** état Auth et événement requis sont confirmés dans la même transaction propriétaire

### Requirement: Audit requis avant tout nouvel accès ordinaire

Sans preuve du commit commun requis, une nouvelle session ou un nouveau jeton MUST NOT être rendu utilisable ni annoncé confirmé. Connexions, renouvellements et élévations ordinaires MUST rester refusés si l’audit durable requis manque. Les exceptions canoniques du Super Admin MUST rester distinctes sans preuve persistante inventée.

#### Scenario: Audit échoué à la création
- **WHEN** l’événement requis ne peut pas être persisté avec une création ordinaire
- **THEN** aucune nouvelle session utilisable n’est confirmée

#### Scenario: Réponse perdue après renouvellement
- **WHEN** le commit commun est confirmé mais sa réponse perdue
- **THEN** la reprise inspecte les états sans double effet ni promesse de restituer un secret conservé seulement sous empreinte

### Requirement: Retrait d’accès Auth prioritaire lors d’une panne d’audit

Si seul l’audit requis échoue et qu’Auth reste accessible, une déconnexion ou révocation Auth vérifiée et autorisée, ou une invalidation prévue par une politique de confiance vérifiée, MUST retirer l’accès et ses dérivés sans annulation due à cette seule panne. L’exception MUST rester limitée à la diminution d’accès Auth.

#### Scenario: Déconnexion malgré panne audit
- **WHEN** l’acteur et le retrait sont vérifiés, Auth disponible et seul l’audit échoue
- **THEN** le retrait confirmé invalide la session et ses jetons dérivés

### Requirement: Contrôles et exclusions du retrait prioritaire

Le retrait prioritaire MUST conserver les contrôles d’identité, d’autorisation, de cible et de périmètre. Il MUST NOT autoriser connexion, renouvellement, élévation, réactivation, changement de justificatif ou autre mutation métier sans ses garanties.

#### Scenario: Nouvel accès refusé
- **WHEN** un compte ordinaire invoque une panne d’audit pour une connexion, un renouvellement ou une élévation
- **THEN** l’exception est refusée sans nouvel accès

#### Scenario: Auteur non vérifiable
- **WHEN** le retrait demandé manque de preuve ou d’autorisation et n’est pas une invalidation de confiance prévue
- **THEN** la panne d’audit ne donne aucun droit de révoquer autrui

### Requirement: Retrait durable et réconciliation de son audit manquant

Le propriétaire Auth MUST persister le retrait et les références minimales de réconciliation, sans secret. Ces références MUST NOT valoir audit C05 réussi ni journal de secours général. L’échec d’audit MUST être signalé puis réconcilié via C05 sans reconstitution implicite depuis les logs techniques.

#### Scenario: Audit manquant signalé
- **WHEN** un retrait est committé sans son audit C05 disponible
- **THEN** la réponse distingue retrait confirmé et audit manquant, avec références durables de réconciliation

### Requirement: Frontière transactionnelle et preuve du retrait

Une transaction PostgreSQL en erreur MUST NOT être poursuivie en ignorant l’échec. La reprise du retrait MUST avoir une frontière définie et une revalidation courante. Si Auth est indisponible ou son commit incertain, une révocation persistante MUST NOT être annoncée sans preuve ; l’accès exigeant un état courant vérifiable MUST rester refusé.

#### Scenario: Auth ou commit non vérifiable
- **WHEN** Auth est indisponible ou le commit du retrait incertain
- **THEN** aucune révocation persistante n’est annoncée et l’accès exigeant l’état courant reste refusé

#### Scenario: Opération composée
- **WHEN** une panne interrompt retrait et mutation de justificatif
- **THEN** seul le retrait peut être repris sous revalidation, sans continuer la transaction en erreur ni confirmer la mutation non committée

## MODIFIED Requirements

### Requirement: Audit dérogeable du Super Admin

Le Super Admin MUST pouvoir déroger à l’audit dans son périmètre autorisé. L’absence d’audit persistant MUST NOT bloquer son opération sous cette dérogation ni être présentée comme un audit réalisé. Les autres comptes MUST conserver leurs obligations, sauf le seul retrait d’accès Auth défini dans cette capacité ; cette réserve MUST NOT leur transférer l’exception Super Admin.

#### Scenario: Opération Super Admin sans audit persistant

- **WHEN** le Super Admin utilise sa dérogation d'audit pour une opération dans son périmètre autorisé et l'audit est indisponible
- **THEN** l'absence d'audit ne bloque pas l'opération
- **AND** aucune preuve d'audit réalisée n'est annoncée

#### Scenario: Audit ordinaire toujours obligatoire

- **WHEN** un Administrateur ordinaire demande une opération soumise à audit hors retrait d’accès Auth admissible alors que cet audit ne peut pas être persisté
- **THEN** l'opération est refusée selon les exigences ordinaires

### Requirement: Portée de l'exception dans les exigences d'audit

Les exigences et scénarios de contrôle applicatif de cette capacité MUST s'appliquer sous réserve de l'exception définie par `authorization`, dans le périmètre du seul compte décrit par `initial-administration`. Les comptes ordinaires MUST conserver leurs contrôles, sous réserve de la seule exception limitée au retrait d’accès Auth définie dans cette capacité. Les profils structurels préparatoires MUST rester inchangés.

#### Scenario: Profil d'occultation inchangé

- **WHEN** un profil structurel d'occultation de champ est validé
- **THEN** ses types, modes et limites restent inchangés et sa validation ne vaut ni audit réalisé ni dérogation

### Requirement: Périmètre obligatoire d'audit

Authentifications, changements d’identité, autorisations sensibles, accès inter-tenants, mutations métier significatives, modifications de configuration et opérations destructives MUST produire un audit persistant contrôlé soumis à rétention. Seul le retrait d’accès Auth admissible selon l’exception dédiée MAY être confirmé sans audit C05 disponible ; son échec MUST être signalé et réconcilié, sans extension aux autres opérations.

#### Scenario: Opération destructive sans audit

- **WHEN** une opération destructive ne peut pas enregistrer son événement d'audit
- **THEN** l'opération est refusée en échec fermé avec un diagnostic explicite

### Requirement: Audit exhaustif du panneau d'administration

Toute activité du panneau (connexion, déconnexion, lecture, navigation, création, modification, suppression, refus, configuration, route ou marqueur externe) MUST produire un audit persistant, sinon être refusée, sauf retrait d’accès Auth admissible selon l’exception dédiée. La politique MUST déclarer événement minimal, rétention, intégrité, droits de consultation et capacité adaptée à cette volumétrie.

#### Scenario: Navigation non auditable

- **WHEN** le panneau ne peut pas persister l'événement de navigation demandé
- **THEN** il refuse l'accès à l'affichage concerné sans exposer de donnée
  sensible
