# Références normatives — N03

Les références ci-dessous restent canoniques. Les blocs sont des sources de traçabilité, sans synchronisation ou copie normative concurrente. Les deltas propres au dossier, s’il en contient, restent proposés.

## artifact-publication #1

[Source canonique](../../../specs/artifact-publication/spec.md#L8) ; SHA-256 source `7888cada73c3beff836fe2bd6dd6a62b166af317e7036680fb6a1f9e248a5b1f`.

### Requirement: Canaux comme contextes de confiance distincts

Les canaux de publication MUST être des contextes de confiance distincts, notamment stable, security et experimental ; un artefact d'un canal non autorisé pour l'environnement MUST être refusé avant activation, et un étiquette mutable ou un canal expérimental MUST NOT être traité comme équivalent à une release stable.

#### Scenario: Artefact du mauvais canal

- **WHEN** un artefact issu d'un canal non autorisé atteint une installation
- **THEN** il est refusé avant activation avec le canal constaté et le canal attendu dans le diagnostic

## artifact-publication #2

[Source canonique](../../../specs/artifact-publication/spec.md#L17) ; SHA-256 source `7888cada73c3beff836fe2bd6dd6a62b166af317e7036680fb6a1f9e248a5b1f`.

### Requirement: Immuabilité et corrélation des corrections

Les artefacts publiés MUST être immuables ; une correction MUST produire une nouvelle version ou un nouvel artefact explicitement corrélé à l'original, jamais une réécriture sur place.

#### Scenario: Écrasement d'un artefact publié

- **WHEN** une tentative de publication remplace un artefact existant sous la même identité
- **THEN** elle est refusée et la correction MUST passer par une nouvelle version corrélée

## artifact-publication #3

[Source canonique](../../../specs/artifact-publication/spec.md#L26) ; SHA-256 source `7888cada73c3beff836fe2bd6dd6a62b166af317e7036680fb6a1f9e248a5b1f`.

### Requirement: Identité vérifiable avant installation

Le canal, la version, la source, la composition et, lorsqu'il s'applique, l'empreinte de l'artefact MUST être vérifiables avant installation, démarrage et mise à niveau.

#### Scenario: Emprunte discordante

- **WHEN** l'empreinte constatée d'un artefact diffère de l'identité annoncée
- **THEN** l'opération est bloquée avec un diagnostic ne exposant aucun élément exploitable

## artifact-publication #4

[Source canonique](../../../specs/artifact-publication/spec.md#L35) ; SHA-256 source `7888cada73c3beff836fe2bd6dd6a62b166af317e7036680fb6a1f9e248a5b1f`.

### Requirement: Signature, provenance et inventaire bloquants

La signature, la provenance et l'inventaire des dépendances font partie de l'identité de distribution ; une signature invalide, absente, expirée ou révoquée MUST bloquer l'opération et produire un diagnostic sans secret.

#### Scenario: Signature révoquée

- **WHEN** un artefact est présenté avec une clé révoquée
- **THEN** l'installation et la mise à niveau sont refusées et l'événement est auditable

## artifact-publication #5

[Source canonique](../../../specs/artifact-publication/spec.md#L44) ; SHA-256 source `7888cada73c3beff836fe2bd6dd6a62b166af317e7036680fb6a1f9e248a5b1f`.

### Requirement: Autorités distinctes et gestion des clés

L'autorité de signature des canaux stables et de sécurité MUST être distincte de celle des artefacts expérimentaux sauf décision de confiance explicitement documentée ; la rotation MUST permettre un chevauchement contrôlé, la révocation MUST rester vérifiable même si un dépôt ou un service de publication est indisponible, et les clés privées MUST NOT apparaître dans aucun artefact, journal, manifest ou fixture.

#### Scenario: Dépôt de publication indisponible

- **WHEN** une vérification de révocation MUST être effectuée alors que le dépôt distant est injoignable
- **THEN** la vérification s'appuie sur les matériaux distribués localement et reste démontrable

## security #2

[Source canonique](../../../specs/security/spec.md#L17) ; SHA-256 source `c033c6fa6a6fc43d6e7e3295cd7dc7f554bbcbe0c12cb9baf0431acd6f7a685f`.

### Requirement: Profil de sécurité déclaré par composant

Chaque composant MUST déclarer données manipulées, permissions, secrets consommés, frontières réseau, dépendances externes et niveau de confiance ; une vulnérabilité critique connue bloque la distribution sauf dérogation limitée, documentée et auditée.

#### Scenario: Vulnérabilité critique bloquante

- **WHEN** un composant présente une vulnérabilité critique sans dérogation valide
- **THEN** sa distribution est refusée

## security #3

[Source canonique](../../../specs/security/spec.md#L26) ; SHA-256 source `c033c6fa6a6fc43d6e7e3295cd7dc7f554bbcbe0c12cb9baf0431acd6f7a685f`.

### Requirement: Échec fermé sans mode permissif

Le système MUST respecter les garanties suivantes.

Toute authentification, autorisation, signature, secret ou contexte non vérifiable produit un échec fermé ; aucun bascule automatique vers un mode permissif pour préserver la disponibilité.

#### Scenario: Contexte non vérifiable refusé

- **WHEN** un contrôle de sécurité ne peut être vérifié
- **THEN** l'opération est refusée et l'événement est diagnostiqué et audité

## security #4

[Source canonique](../../../specs/security/spec.md#L37) ; SHA-256 source `c033c6fa6a6fc43d6e7e3295cd7dc7f554bbcbe0c12cb9baf0431acd6f7a685f`.

### Requirement: Diagnostics sans exposition sensible

Les journaux, diagnostics et inventaires MUST NOT exposer de secret, de jeton ni de donnée personnelle ; révocations, blocages et réactivations restent diagnostiquables et auditables.

#### Scenario: Secret hors journaux

- **WHEN** un diagnostic est produit après un échec de sécurité
- **THEN** il identifie le composant et la cause sans divulguer de valeur sensible

## deb-package #1

[Source canonique](../../../specs/deb-package/spec.md#L8) ; SHA-256 source `46730b2c3505085325539b6ae2386806e5b59bb19aa46adf5f4571335d016e64`.

### Requirement: Paquet corrélé à la release

Chaque paquet MUST identifier sa release, son périmètre de composition, ses manifests, contrats, compatibilités et garanties. Il MUST rester corrélable aux autres artefacts de cette release pour les capacités communes. Cette corrélation MUST NOT imposer un contenu binaire identique entre le paquet PA, le paquet PBO/PFO et l’image sans fonctions de session ; les noms et versions exactes restent à spécifier.

#### Scenario: Version de paquet incohérente

- **WHEN** un paquet revendique une release différente de l’artefact qu’il installe
- **THEN** l’installation signale l’incohérence et bloque l’activation

#### Scenario: Deux paquets indépendants

- **WHEN** la composition Debian cible est vérifiée
- **THEN** le paquet PA et le paquet PBO/PFO restent distincts selon leurs exigences de composition

## deb-package #4

[Source canonique](../../../specs/deb-package/spec.md#L40) ; SHA-256 source `46730b2c3505085325539b6ae2386806e5b59bb19aa46adf5f4571335d016e64`.

### Requirement: Mise à niveau du paquet sous validation

Toute mise à niveau par paquet MUST être une opération explicite soumise à vérification d'identité de distribution, aux contrôles de compatibilité et au plan de migration ; un échec ou un abandon MUST laisser l'ancienne composition ou un état explicitement sûr, sans purge ni activation partielle non diagnostiquée.

#### Scenario: Mise à niveau interrompue

- **WHEN** une mise à niveau de paquet est interrompue après exécution partielle des migrations
- **THEN** le système reste dans un état diagnostiqué et seule une reprise validée ou une restauration autorisée poursuit l'opération

## deb-package #5

[Source canonique](../../../specs/deb-package/spec.md#L49) ; SHA-256 source `46730b2c3505085325539b6ae2386806e5b59bb19aa46adf5f4571335d016e64`.

### Requirement: Aucune installation de code distant implicite

Le paquet MUST NOT, par défaut, télécharger, installer ou activer du code distant pendant l'installation ou l'exécution ; un mécanisme de mise à jour de sécurité peut automatiser le déclenchement sans supprimer les validations requises.

#### Scenario: Téléchargement proposé à l'installation

- **WHEN** une routine d'installation tente de récupérer une dépendance distante non vérifiée
- **THEN** l'installation est refusée sauf procédure explicite conforme aux garanties de publication

