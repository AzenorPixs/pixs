## MODIFIED Requirements

### Requirement: Autorité métier et état de contrôle cohérents

Django MUST porter les autorisations et mutations applicatives ; PostgreSQL MUST rester l’autorité du contrôle et du management ordinaires. Avant sa disponibilité, seule la branche locale PA/PZT MAY utiliser sa source technique protégée indépendante. Cette exception MUST NOT créer de droit métier. Les garanties de coordination, de primaire unique, de durabilité et d’accès PA du scénario ci-dessous MUST s’appliquer.

#### Scenario: Garanties de séparation du contrôle technique et applicatif

- **WHEN** l’état de contrôle PZT est évalué avant ou après disponibilité de PostgreSQL
- **THEN** Django MUST porter autorisations et mutations applicatives ; PostgreSQL MUST faire autorité par périmètre pour les états de contrôle applicatifs et le management ordinaire. Avant sa disponibilité, seule la branche locale de préparation technique PA/PZT définie dans cette capacité MAY utiliser sa source protégée indépendante ; elle MUST NOT décider un droit métier ou une mutation applicative. PBO et autorités MUST NOT décider indépendamment de la validité d'un même mandat. Un seul primaire admissible MUST écrire ; redondance critique MUST utiliser durabilité synchrone et promotion après exclusion vérifiée. PA MUST NOT accéder directement aux tables ni déduire un commit PostgreSQL d'une signature reçue.

#### Scenario: Autorité métier et état de contrôle cohérents

- **WHEN** une réponse de commit est perdue
- **THEN** la source autoritative est réconciliée sans nouvelle mutation aveugle

## ADDED Requirements

### Requirement: Amorçage local PA PZT indépendant de PostgreSQL

Le parcours PA/PZT MUST disposer d’un provisionnement opérateur et d’une politique technique protégée indépendants de la base Pixs à préparer. Le profil local mTLS MUST limiter les échanges à la préparation technique autorisée, refuser tout repli PBO–PA hors PZT et rapprocher les résultats avant transfert au contrôle applicatif PostgreSQL selon les garanties ci-dessous.

#### Scenario: Garanties de l’amorçage local PZT

- **WHEN** le profil sélectionne cette capacité pour le parcours de préparation PostgreSQL
- **THEN** Avant le premier échange PBO–PA, une procédure opérateur locale explicite MUST provisionner PA et PZT avec leurs identités propres, ancrages de confiance, configuration minimale, références de secrets et politique technique versionnée protégée, sans dépendre de la base Pixs à préparer ni d'une session future. Cette procédure MUST vérifier l'origine et l'autorisation du provisionnement ; le premier PBO rencontré MUST NOT devenir une autorité de confiance. Elle MUST permettre un profil PZT local mTLS pour les seuls échanges de préparation, d'inspection et de résultats techniques PostgreSQL explicitement autorisés ; elle MUST NOT ouvrir le réseau distant, le management ordinaire, un tenant ou une mutation métier. Les mandats MUST avoir cibles, actions fermées, bornes et validité explicites, anti-rejeu, révocation vérifiable et audit durable indépendant de PostgreSQL. Une politique absente, expirée, révoquée ou dont la fraîcheur ne peut être vérifiée MUST fermer l'admission. Le contrôle applicatif ordinaire MUST attendre PostgreSQL et ses décisions courantes. La transition MUST rapprocher preuves et résultats vers leurs propriétaires persistants puis terminer les mandats temporaires avant admission ordinaire ; des politiques divergentes MUST NOT faire autorité simultanément. Panne ou absence de PZT MUST bloquer les échanges PBO–PA, sans socket, loopback ou fichier de secours hors PZT. Le provisionnement local opérateur MUST NOT devenir un canal continu PBO–PA.

#### Scenario: PZT local avant la base

- **WHEN** la base Pixs est absente mais le provisionnement opérateur et le mandat technique local sont vérifiés
- **THEN** les seuls échanges techniques prévus sont admis via PZT local mTLS ; aucune autorisation métier ou ouverture réseau distante n’est déduite

#### Scenario: Autorité d’amorçage périmée

- **WHEN** un échange présente un mandat expiré ou une politique locale dont la fraîcheur ne peut être vérifiée
- **THEN** PZT refuse l’échange sans consulter une base inexistante ni ouvrir un canal de substitution

#### Scenario: Relais de contrôle incomplet

- **WHEN** PostgreSQL devient disponible mais le rapprochement des résultats et la fin des mandats temporaires ne sont pas confirmés
- **THEN** le management ordinaire reste non prêt sans déclarer deux autorités concurrentes

### Requirement: Fin des mandats temporaires de préparation initiale PZT

Après retrait irréversible PA, PZT MUST refuser tout nouvel échange de préparation initiale sous l'autorité retirée. Les mandats temporaires concernés MUST se terminer, sans supprimer la remise minimale PBO ni inventer d'autorité ordinaire.

#### Scenario: Nouvel échange de préparation initiale après retrait

- **WHEN** un échange demande une nouvelle préparation initiale alors que le retrait PA est ancré pour la cible concernée
- **THEN** PZT refuse l'échange sans ouvrir de canal de substitution
- **AND** les retraits PA et Z12 restent distincts par leurs propriétaires

#### Scenario: Mandat temporaire de préparation initiale périmé ou révoqué

- **WHEN** un mandat temporaire de préparation initiale est périmé, révoqué ou dont la fraîcheur ne peut être vérifiée
- **THEN** PZT refuse l'échange et le parcours reste non prêt pour cette préparation

#### Scenario: Garanties conservées de fin PZT

- **WHEN** la fin des mandats est évaluée pour la cible concernée
- **THEN** la quiescence et l'ancrage du retrait sont vérifiés, sans autorité ordinaire anticipée
- **AND** les contrats de topologie D8/D6, de wire et de résolveurs restent à fermer en revue commune avant leur code, les qualifications réelles en phase 2 après réalisation, et l'adoption des principes ne vaut pas réalisation

## ADDED Requirements

### Requirement: Transport PZT des enveloppes 1.1 et provenance A07

Tous échanges PBO-PA MUST passer par PZT. Pour le profil PostgreSQL initial 1.1 E5 sélectionné, les enveloppes 1.1 fermées avec purposes OBSERVE, PREPARE_PLAN, PREPARE et READ_RESULT sont obligatoires, sans modifier les contrats 1.0 ni fallback. Les tableaux A07 MUST conserver ordre et doublons de leurs invocations réelles. Toute divergence MUST imposer refus ou replanification sans compensation destructive ni rejeu d'issue inconnue.

#### Scenario: A07 complets par invocation réelle

- **WHEN** un appel OBSERVE, PREPARE_PLAN, PREPARE ou READ_RESULT est transporté
- **THEN** invocation, correlation_ids et causation_ids correspondent à l'invocation réelle avec ordre et doublons conservés

#### Scenario: Divergence sans compensation destructive

- **WHEN** une observation, un plan ou une réponse diverge ou est perdue
- **THEN** le parcours ferme la résolution ou impose une nouvelle planification sans supprimer de base ni rejouer un mandat consommé
