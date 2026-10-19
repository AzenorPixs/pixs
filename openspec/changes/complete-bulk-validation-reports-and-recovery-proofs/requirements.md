# Références normatives — B10

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| bulk-operations / 583 | [Runtime Bulk v1 B05 — Parsing et mapping](../../specs/bulk-operations/spec.md#L583) | P | COMPLETER_OU_INTEGRER |
| bulk-operations / 674 | [Runtime Bulk v1 B13 — Diagnostics, checkpoints et preuves](../../specs/bulk-operations/spec.md#L674) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence bulk-operations--2f3a43ac59

Source : `openspec/specs/bulk-operations/spec.md`, ligne 583. SHA-256 du bloc : `c27168072d2c3abc27fff23766ccae292a6422d9eda950e4de2c3aa3b8d106f1`.

~~~~text
### Requirement: Runtime Bulk v1 B05 — Parsing et mapping

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B05 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Mapping déclaré

- **WHEN** un fichier conforme utilise un mapping propriétaire immuable et versionné
- **THEN** seuls les champs déclarés sont transmis au contrat public sans conversion heuristique

#### Scenario: Entrée ambiguë

- **WHEN** un CSV contient un header dupliqué ou un NDJSON une clé dupliquée
- **THEN** le parsing refuse l’entrée et produit un diagnostic statique sans contenu brut
~~~~

### Référence bulk-operations--9315ef8cc6

Source : `openspec/specs/bulk-operations/spec.md`, ligne 674. SHA-256 du bloc : `824db0d9c86d9317145ad3d1d7364003d31fbf811b2444be199777064dcc2511`.

~~~~text
### Requirement: Runtime Bulk v1 B13 — Diagnostics, checkpoints et preuves

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B13 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Checkpoint atomique

- **WHEN** une unité est engagée avec progression, idempotence et événements requis
- **THEN** son checkpoint SQL indique uniquement les effets réellement engagés

#### Scenario: Validation incomplète

- **WHEN** la limite de diagnostics est atteinte
- **THEN** le traitement s’arrête avec complétude fausse et sans diagnostic reproduisant une valeur
~~~~

