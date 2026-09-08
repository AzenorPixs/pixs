## Purpose

La publication des artefacts établit leur identité de distribution : canaux de confiance distincts, immuabilité, signature, provenance et inventaire de dépendances vérifiables avant toute installation ou activation.

## ADDED Requirements

### Requirement: Canaux comme contextes de confiance distincts

Les canaux de publication DOIVENT être des contextes de confiance distincts, notamment stable, security et experimental ; un artefact d'un canal non autorisé pour l'environnement DOIT être refusé avant activation, et un étiquette mutable ou un canal expérimental NE DOIT JAMAIS être traité comme équivalent à une release stable.

#### Scenario: Artefact du mauvais canal

- **WHEN** un artefact issu d'un canal non autorisé atteint une installation
- **THEN** il est refusé avant activation avec le canal constaté et le canal attendu dans le diagnostic

### Requirement: Immuabilité et corrélation des corrections

Les artefacts publiés DOIVENT être immuables ; une correction DOIT produire une nouvelle version ou un nouvel artefact explicitement corrélé à l'original, jamais une réécriture sur place.

#### Scenario: Écrasement d'un artefact publié

- **WHEN** une tentative de publication remplace un artefact existant sous la même identité
- **THEN** elle est refusée et la correction doit passer par une nouvelle version corrélée

### Requirement: Identité vérifiable avant installation

Le canal, la version, la source, la composition et, lorsqu'il s'applique, l'empreinte de l'artefact DOIVENT être vérifiables avant installation, démarrage et mise à niveau.

#### Scenario: Emprunte discordante

- **WHEN** l'empreinte constatée d'un artefact diffère de l'identité annoncée
- **THEN** l'opération est bloquée avec un diagnostic ne exposant aucun élément exploitable

### Requirement: Signature, provenance et inventaire bloquants

La signature, la provenance et l'inventaire des dépendances font partie de l'identité de distribution ; une signature invalide, absente, expirée ou révoquée DOIT bloquer l'opération et produire un diagnostic sans secret.

#### Scenario: Signature révoquée

- **WHEN** un artefact est présenté avec une clé révoquée
- **THEN** l'installation et la mise à niveau sont refusées et l'événement est auditable

### Requirement: Autorités distinctes et gestion des clés

L'autorité de signature des canaux stables et de sécurité DOIT être distincte de celle des artefacts expérimentaux sauf décision de confiance explicitement documentée ; la rotation DOIT permettre un chevauchement contrôlé, la révocation DOIT rester vérifiable même si un dépôt ou un service de publication est indisponible, et les clés privées NE DOIVENT apparaître dans aucun artefact, journal, manifest ou fixture.

#### Scenario: Dépôt de publication indisponible

- **WHEN** une vérification de révocation doit être effectuée alors que le dépôt distant est injoignable
- **THEN** la vérification s'appuie sur les matériaux distribués localement et reste démontrable
