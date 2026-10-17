# Références normatives — O16

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| synchronization / 8 | [Mécanisme réactif optionnel sous autorité applicative](../../specs/synchronization/spec.md#L8) | NE | AUDIT_AVANT_CREATION |
| synchronization / 17 | [Périmètre et autorisation propagés aux projections](../../specs/synchronization/spec.md#L17) | NE | AUDIT_AVANT_CREATION |
| synchronization / 26 | [Cohérence déclarée et échec contrôlé](../../specs/synchronization/spec.md#L26) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence synchronization--0387583c83

Source : `openspec/specs/synchronization/spec.md`, ligne 8. SHA-256 du bloc : `de95f3f8486241b5c491e5f290f7d204903fa245093c39cf634f922e23aa8c27`.

~~~~text
### Requirement: Mécanisme réactif optionnel sous autorité applicative

Toute mutation MUST être validée et transactionnée par l'applicatif avant propagation réactive ; un module sans besoin réactif MUST NOT dépendre du mécanisme de synchronisation.

#### Scenario: Mutation non validée non propagée

- **WHEN** une mutation n'a pas été validée par l'applicatif
- **THEN** elle n'est jamais diffusée comme état de référence
~~~~

### Référence synchronization--594b70b7fb

Source : `openspec/specs/synchronization/spec.md`, ligne 17. SHA-256 du bloc : `5bf2c3295093206c881c3022a7f7f708717a721686c5ae336d2494f26de7858c`.

~~~~text
### Requirement: Périmètre et autorisation propagés aux projections

Chaque projection synchronisée MUST porter tenant, scope, version et corrélation, respecter le filtrage autorisé et invalider les données révoquées, supprimées ou purgées via marqueurs.

#### Scenario: Donnée révoquée invalidée

- **WHEN** une révocation ou suppression survient à la source
- **THEN** les projections clientes concernées sont invalidées avant tout nouvel affichage
~~~~

### Référence synchronization--7b38a4bde2

Source : `openspec/specs/synchronization/spec.md`, ligne 26. SHA-256 du bloc : `9371aa9c06cafd06743cfa9df82443340e3703d4c0a980a86625fc0f4b3a94d9`.

~~~~text
### Requirement: Cohérence déclarée et échec contrôlé

Le système MUST respecter les garanties suivantes.

Cohérence éventuelle, fraîcheur maximale et dégradation sont déclarées par capacité et ressource ; toute incohérence ou perte de fournisseur produit un état contrôlé au lieu d'un succès implicite.

#### Scenario: Fournisseur perdu diagnostiqué

- **WHEN** le mécanisme de synchronisation devient indisponible
- **THEN** le client signale un état périmé ou hors ligne sans valider de mutation locale
~~~~

