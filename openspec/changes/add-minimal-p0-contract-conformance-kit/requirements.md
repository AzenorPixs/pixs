# Références normatives — N06

Les références ci-dessous restent canoniques. Les blocs sont des sources de traçabilité, sans synchronisation ou copie normative concurrente. Les deltas propres au dossier, s’il en contient, restent proposés.

## testing #1

[Source canonique](../../specs/testing/spec.md#L8) ; SHA-256 source `5e0c976821f8623c976d43125c7d5738fbf100b9fae1a112d45894e9fdc7a148`.

### Requirement: Trois niveaux de vérification distincts

Le projet MUST distinguer les tests unitaires des comportements internes, les tests d'intégration des compositions et des dépendances réelles de référence, et les tests de conformité des contrats publiés ; le succès d'un niveau MUST NOT tenir lieu de preuve pour un autre.

#### Scenario: Unitaires verts, intégration rouge

- **WHEN** des tests unitaires réussissent alors qu'un test d'intégration de composition échoue
- **THEN** la release est considérée non valide et l'échec d'intégration est rapporté explicitement

## testing #2

[Source canonique](../../specs/testing/spec.md#L17) ; SHA-256 source `5e0c976821f8623c976d43125c7d5738fbf100b9fae1a112d45894e9fdc7a148`.

### Requirement: Kit de conformité et composant d'exemple

Le Developer Kit MUST fournir des validateurs et suites de conformité
versionnés pour les manifests, contrats et composants déclarés compatibles. Un
composant d'exemple P0 MUST démontrer la composition par contrats, le contexte
tenant/scope et l'autorisation ; il MUST NOT devenir une dépendance de
production.

#### Scenario: Exemple P0 validé

- **WHEN** le composant d'exemple est validé par le Developer Kit
- **THEN** les preuves indiquent les versions de contrats et les contrôles P0 exécutés

## testing #3

[Source canonique](../../specs/testing/spec.md#L30) ; SHA-256 source `5e0c976821f8623c976d43125c7d5738fbf100b9fae1a112d45894e9fdc7a148`.

### Requirement: Suites de conformité versionnées par contrat

Chaque contrat de fournisseur MUST disposer d'une suite de conformité versionnée, indépendante de la technologie implémentée ; le runtime MUST NOT déclarer compatible un provider dont la conformité obligatoire est absente, expirée ou échouée.

#### Scenario: Certification expirée

- **WHEN** un provider présente une preuve de conformité expirée pour sa version déclarée
- **THEN** il est exclu de la sélection tant qu'une nouvelle exécution de la suite ne réussit pas

## testing #4

[Source canonique](../../specs/testing/spec.md#L39) ; SHA-256 source `5e0c976821f8623c976d43125c7d5738fbf100b9fae1a112d45894e9fdc7a148`.

### Requirement: Garanties obligatoires séparées des capacités optionnelles

Les tests MUST distinguer les garanties obligatoires des capacités optionnelles : une capacité optionnelle absente ou indisponible peut produire un état dégradé ou désactivé si elle reste isolée ; une incompatibilité de contrat, une ambiguïté de fournisseur, un défaut d'isolation de tenant ou une violation de sécurité MUST bloquer l'activation.

#### Scenario: Isolement acceptable

- **WHEN** une capacité optionnelle tombe sans fuite d'accès ni perte de donnée
- **THEN** l'état dégradé est accepté et diagnostiqué alors que le socle reste actif

## testing #5

[Source canonique](../../specs/testing/spec.md#L48) ; SHA-256 source `5e0c976821f8623c976d43125c7d5738fbf100b9fae1a112d45894e9fdc7a148`.

### Requirement: Reproductibilité sur la topologie de référence

Les tests MUST être exécutables sur la topologie de référence du projet et sur toute topologie isolée déclarée compatible ; une différence de topologie MUST NOT modifier silencieusement les règles d'autorisation, de partage, de projection ou de suppression.

#### Scenario: Divergence de topologie

- **WHEN** un test d'invariant de périmètre produit un résultat différent selon la topologie
- **THEN** l'écart est bloquant et la topologie concernée perd sa mention de compatibilité

## testing #6

[Source canonique](../../specs/testing/spec.md#L57) ; SHA-256 source `5e0c976821f8623c976d43125c7d5738fbf100b9fae1a112d45894e9fdc7a148`.

### Requirement: Preuves sans secret ni donnée de production

Les fixtures, exemples et rapports produits par les tests MUST être synthétiques et reproductibles, sans secret, sans token et sans donnée de production ; les rapports MUST NOT exposer de détail exploitable.

#### Scenario: Secret détecté dans un rapport

- **WHEN** un artefact de test contient une valeur sensible réelle ou apparentée
- **THEN** le rapport est invalidé, la fuite est signalée et l'exécution est bloquante pour la publication

## testing #7

[Source canonique](../../specs/testing/spec.md#L66) ; SHA-256 source `5e0c976821f8623c976d43125c7d5738fbf100b9fae1a112d45894e9fdc7a148`.

### Requirement: Conformité de la composition frontend récursive

Les suites de conformité MUST vérifier la résolution récursive des modules et sous-modules frontend, la propriété des contributions, les dépendances publiques, les contraintes SemVer, les collisions, les modes obligatoire et optionnel, ainsi que l'équivalence de composition entre développement et artefacts distribués. Une résolution frontend MUST NOT dépendre de l'ordre des imports, du filesystem ou d'un code distant runtime.

#### Scenario: Composition reproductible avec sous-module

- **WHEN** la même composition incluant un module et un sous-module frontend est construite deux fois
- **THEN** les contributions actives, l'ordre de chargement et les diagnostics produits sont identiques

## testing #9

[Source canonique](../../specs/testing/spec.md#L89) ; SHA-256 source `5e0c976821f8623c976d43125c7d5738fbf100b9fae1a112d45894e9fdc7a148`.

### Requirement: Exécution navigateur headless des unités frontend web

Les tests unitaires de la partie frontend web MUST être exécutés dans tous les
navigateurs déclarés par DEVOPS.md, en mode headless ; le succès de ces tests
uniquement sous Node MUST NOT tenir lieu de preuve de cette exigence.

#### Scenario: Les deux moteurs déclarent les cas

- **WHEN** `npm --prefix frontend test` s'exécute sur un environnement
  déclarant Chromium et Firefox headless
- **THEN** chaque cas unitaire frontend reçoit une preuve d'exécution issue de
  chaque navigateur déclaré et le résultat global n'est vert qu'avec les deux
  moteurs

#### Scenario: Moteur manquant ou cas non exécuté

- **WHEN** un navigateur déclaré est indisponible, ne répond pas dans les
  bornes, ou n'exécute pas l'intégralité des cas
- **THEN** l'exécution est en échec diagnostiqué, sans substitution par le
  seul résultat Node ou par la réussite du build

## developer-experience #1

[Source canonique](../../specs/developer-experience/spec.md#L10) ; SHA-256 source `9008a4c9affc2e6dc13c7247fd375c349a8d85fa2733878756dd27373ad8e4b1`.

### Requirement: Parcours local reproductible

Le Developer Kit MUST fournir un parcours local reproductible pour créer et
valider un composant d'exemple compatible P0. Ce parcours MUST utiliser les
contrats et validateurs publiés et MUST NOT exiger de secret ou donnée de production.

#### Scenario: Premier composant local

- **WHEN** un développeur initialise le composant d'exemple P0
- **THEN** il obtient un manifest valide et des diagnostics reproductibles

## developer-experience #2

[Source canonique](../../specs/developer-experience/spec.md#L21) ; SHA-256 source `9008a4c9affc2e6dc13c7247fd375c349a8d85fa2733878756dd27373ad8e4b1`.

### Requirement: Génération sans activation implicite

Le scaffolding MAY générer des fichiers déclaratifs et exemples. Il MUST NOT
enregistrer, activer, provisionner ou publier un composant, provider, tenant ou
secret sans opération explicite autorisée.

#### Scenario: Scaffolding d'un provider

- **WHEN** le Developer Kit génère un squelette de provider
- **THEN** le provider reste non installé et non sélectionné

## developer-experience #3

[Source canonique](../../specs/developer-experience/spec.md#L32) ; SHA-256 source `9008a4c9affc2e6dc13c7247fd375c349a8d85fa2733878756dd27373ad8e4b1`.

### Requirement: Diagnostics sans fuite

Les validateurs et exemples MUST associer les erreurs à la règle ou au champ.
Leurs diagnostics MUST NOT révéler de secret, credential, donnée de production
ou détail privé non nécessaire.

#### Scenario: Manifest incomplet

- **WHEN** un manifest omet un champ obligatoire
- **THEN** le validateur indique le champ et la règle attendue sans donnée sensible

## compatibility #4

[Source canonique](../../specs/compatibility/spec.md#L35) ; SHA-256 source `aee6de57607e95e8442b59155cf893f4ef7454db6a0ba60fbfbd9abe360eb544`.

### Requirement: Compatibilité déclarative distincte de la conformité comportementale

La compatibilité déclarative par contraintes de version et la conformité comportementale par suites de tests MUST être évaluées séparément et toutes deux satisfaites avant de déclarer une composition valide.

#### Scenario: Déclaration sans conformité

- **WHEN** un composant déclare une plage compatible sans preuve de conformité comportementale à cette version
- **THEN** la composition est incomplète et l'activation reste refusée

## compatibility #7

[Source canonique](../../specs/compatibility/spec.md#L66) ; SHA-256 source `aee6de57607e95e8442b59155cf893f4ef7454db6a0ba60fbfbd9abe360eb544`.

### Requirement: Preuve de conformité externe

La conformité comportementale MUST être établie par des
`ConformityAttestation` fournies en mémoire par l'appelant de confiance,
extérieures au manifest, de la forme `{ component_id: string non vide,
component_version: SemVer complète, scope: COMPONENT|CAPABILITY|CONTRACT,
target_id: string non vide, target_version: SemVer complète exacte,
suite_id: string non vide, suite_version: SemVer complète, verdict: PASS,
proof_ref: string non vide }`, sans secret ni contenu de rapport.

#### Scenario: Attestation externe sans contenu de rapport

- **WHEN** l'appelant de confiance fournit une ConformityAttestation
- **THEN** elle porte les champs et versions déclarés sans secret ni contenu de rapport, hors du manifest

## compatibility #8

[Source canonique](../../specs/compatibility/spec.md#L81) ; SHA-256 source `aee6de57607e95e8442b59155cf893f4ef7454db6a0ba60fbfbd9abe360eb544`.

### Requirement: Liaison exacte des attestations de conformité

Le système MUST respecter les garanties suivantes.

La liaison
exacte porte sur `component_version` et `target_version` des attestations et
inclut l'identité textuelle déclarée, métadonnées de build comprises ; les
comparateurs restent évalués selon la spécification `dependencies`. Pour le
scope `COMPONENT`, `target_id` et `target_version` sont l'identifiant et la
version du composant. Une chaîne auto-déclarée du manifest n'est JAMAIS une
preuve.

#### Scenario: Métadonnées de build dans la liaison de preuve

- **WHEN** une attestation est liée à un composant et une cible
- **THEN** la liaison conserve leur identité textuelle exacte, métadonnées de build comprises, et une chaîne du manifest ne vaut pas preuve

## compatibility #9

[Source canonique](../../specs/compatibility/spec.md#L98) ; SHA-256 source `aee6de57607e95e8442b59155cf893f4ef7454db6a0ba60fbfbd9abe360eb544`.

### Requirement: Couverture des attestations avant activation

La couverture suivante est exigée avant activation : chaque composant activé
MUST être couvert par une preuve de portée `COMPONENT` de son fournisseur
(id et version exacts) ; chaque capacité ou contrat résolu MUST être couvert
par une preuve ciblée de son fournisseur (cible et version exactes). Toute
preuve absente, contradictoire, en échec, en mismatch de version, ambiguë ou
malformée MUST refuser l'activation avec un diagnostic non sensible nommant
la preuve manquante ou en cause.

#### Scenario: Activation sans preuve refusée

- **WHEN** une composition résout ses dépendances mais aucune attestation ne couvre un composant activé
- **THEN** l'activation est refusée avec un diagnostic nommant la preuve manquante

#### Scenario: Preuve d'un autre fournisseur ou d'une autre version refusée

- **WHEN** la seule attestation couvre le même identifiant de capacité fourni par un autre composant ou en une autre version exacte
- **THEN** l'activation est refusée avec un diagnostic nommant le mismatch de fournisseur ou de version

#### Scenario: Preuves concordantes autorisant l'activation

- **WHEN** chaque composant activé et chaque capacité ou contrat résolu est couvert par une attestation PASS de version exacte de son fournisseur
- **THEN** la couverture est satisfaite et ne bloque pas l'activation pour ce motif

## compatibility #10

[Source canonique](../../specs/compatibility/spec.md#L123) ; SHA-256 source `aee6de57607e95e8442b59155cf893f4ef7454db6a0ba60fbfbd9abe360eb544`.

### Requirement: Responsabilités de l'appelant et du noyau pour les preuves

Le système MUST respecter les garanties suivantes.

L'appelant authentifie les preuves et atteste
la réalisation des tests ; le noyau valide seulement leur structure et leur
couverture sans prétendre exécuter de suites. La bibliothèque P0 reste
utilisable par tout appelant réel externe fournissant des preuves vérifiées ; les doubles de tests sont clairement nommés et limités aux fixtures.

#### Scenario: Preuve authentifiée par l'appelant

- **WHEN** un appelant réel externe fournit des preuves vérifiées
- **THEN** le noyau en vérifie la structure et la couverture sans prétendre avoir exécuté les suites

## compatibility #11

[Source canonique](../../specs/compatibility/spec.md#L137) ; SHA-256 source `aee6de57607e95e8442b59155cf893f4ef7454db6a0ba60fbfbd9abe360eb544`.

### Requirement: Matrice P0 limitée aux dimensions connues

Les exigences de matrice de compatibilité globale et d'états minimum sont
préservées ; P0 MUST évaluer seulement les dimensions qu'il connaît
(composants, capacités et contrats déclarés, preuves fournies) et MUST NOT
déclarer de matrice globale complète ni de compatible global si des
dimensions restent hors périmètre ou inconnues.

#### Scenario: Dimension inconnue non évaluée

- **WHEN** une dimension de compatibilité (schéma, migration, événement, provider, client) n'est pas évaluable en P0
- **THEN** P0 expose la dimension comme non évaluée et ne délivre pas de validation globale

## providers #3

[Source canonique](../../specs/providers/spec.md#L26) ; SHA-256 source `5aceaa82194cfc9802dcf6ef1bd9e4fc35b18b5156d1b29685e41d23689a7fd7`.

### Requirement: Conformité contractuelle vérifiable

Un fournisseur MUST satisfaire le contrat déclaré à sa version revendiquée ; toute violation constatée MUST entraîner l'isolement du fournisseur et un échec fermé des appels concernés.

#### Scenario: Fournisseur non conforme activé

- **WHEN** un fournisseur échoue à une vérification de conformité de son contrat
- **THEN** il est retiré de la sélection et les appels correspondants échouent avec un code d'erreur stable

## reference-composition #1

[Source canonique](../../specs/reference-composition/spec.md#L10) ; SHA-256 source `7c4d7b603f35f02f6d2ba0eb10dd202793ec288fee0c65a5ff15d244446233ff`.

### Requirement: Capacités obligatoires du P0

Une composition P0 MUST inclure les mécanismes de composition, `pixs.core`, le
contexte tenant/scope, l'autorisation, les API et contrats publics, migrations,
runtime, provisionnement, sécurité, secrets, audit, observabilité, gouvernance,
cycle de vie des données, conformité et un composant d'exemple.

#### Scenario: Capacité P0 absente

- **WHEN** une composition se présente comme P0 mais omet une capacité obligatoire
- **THEN** sa validation échoue avant activation ou publication

## reference-composition #3

[Source canonique](../../specs/reference-composition/spec.md#L33) ; SHA-256 source `7c4d7b603f35f02f6d2ba0eb10dd202793ec288fee0c65a5ff15d244446233ff`.

### Requirement: Preuve reproductible

La validation P0 MUST produire une preuve versionnée du graphe de composants,
contrats, profils et contrôles exécutés. Cette preuve MUST NOT contenir de secret,
credential ou donnée de production.

#### Scenario: Deux validations identiques

- **WHEN** la même composition P0 est validée avec les mêmes entrées
- **THEN** elle produit le même graphe et des contrôles équivalents

