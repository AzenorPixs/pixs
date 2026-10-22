## MODIFIED Requirements

### Requirement: Autorité métier et état de contrôle cohérents

Django MUST porter autorisations et mutations applicatives ; PostgreSQL MUST faire autorité par périmètre pour les états de contrôle applicatifs et le management ordinaire. Avant sa disponibilité, seule la branche locale de préparation technique PA/PZT définie dans cette capacité MAY utiliser sa source protégée indépendante ; elle MUST NOT décider un droit métier ou une mutation applicative. PBO et autorités MUST NOT décider indépendamment de la validité d'un même mandat. Un seul primaire admissible MUST écrire ; redondance critique MUST utiliser durabilité synchrone et promotion après exclusion vérifiée. PA MUST NOT accéder directement aux tables ni déduire un commit PostgreSQL d'une signature reçue.

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
