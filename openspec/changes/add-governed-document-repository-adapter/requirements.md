# Références normatives — O02

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| document-repositories / 8 | [Contrat référentiel et modes déclarés](../../specs/document-repositories/spec.md#L8) | NE | AUDIT_AVANT_CREATION |
| document-repositories / 17 | [Autorisation et audit préservés](../../specs/document-repositories/spec.md#L17) | NE | AUDIT_AVANT_CREATION |
| document-repositories / 28 | [Mappings, conflits et reprises](../../specs/document-repositories/spec.md#L28) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence document-repositories--50a836c42c

Source : `openspec/specs/document-repositories/spec.md`, ligne 8. SHA-256 du bloc : `65be7cbf145735ca65b2894d1d098ac1045b4525ab99781ae2ee4c6d7fcc6765`.

~~~~text
### Requirement: Contrat référentiel et modes déclarés

Chaque intégration MUST déclarer le mode piloté par Pixs ou externe, la source d'autorité, le sens de synchronisation, la gestion des conflits et les règles de suppression par espace.

#### Scenario: Mode ambigu refusé

- **WHEN** un espace ne déclare ni autorité ni sens de synchronisation
- **THEN** son activation est refusée
~~~~

### Référence document-repositories--4bf78554ca

Source : `openspec/specs/document-repositories/spec.md`, ligne 17. SHA-256 du bloc : `63c9fe8397cdf1e84d6f044e2e412da11a66e24c1cd576e91e4da3c30ad189d1`.

~~~~text
### Requirement: Autorisation et audit préservés

Le système MUST respecter les garanties suivantes.

Aucun accès direct au stockage interne d'un référentiel externe ; toute opération passe par l'identité numérique, le contexte tenant, l'autorisation applicative et l'audit Pixs, via les interfaces publiques configurables.

#### Scenario: Contournement refusé

- **WHEN** une opération tente d'accéder au répertoire interne du référentiel
- **THEN** elle est refusée et tracée
~~~~

### Référence document-repositories--f9f2629c30

Source : `openspec/specs/document-repositories/spec.md`, ligne 28. SHA-256 du bloc : `6ab3cf03887716f2f7ac2eb60cea3c837f40f88d8754a8caa763e146319bca82`.

~~~~text
### Requirement: Mappings, conflits et reprises

Le système MUST respecter les garanties suivantes.

Mappings, points de reprise et états de synchronisation sont versionnés, persistants et idempotents ; une modification externe en mode piloté vaut divergence traitée, en mode externe elle alimente la projection.

#### Scenario: Divergence traitée explicitement

- **WHEN** une modification externe survient en mode piloté
- **THEN** elle est signalée comme divergence avec un état diagnostiqué, sans mutation silencieuse
~~~~

