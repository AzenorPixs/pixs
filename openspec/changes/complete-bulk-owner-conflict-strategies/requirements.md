# Références normatives — B04

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| bulk-operations / 631 | [Runtime Bulk v1 B07 — Modes et conflits](../../specs/bulk-operations/spec.md#L631) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence bulk-operations--22c5156a47

Source : `openspec/specs/bulk-operations/spec.md`, ligne 631. SHA-256 du bloc : `075ef50c5d9591f1601f29d011fe82ee3e5ec01efba7e9ba8773182327b71b07`.

~~~~text
### Requirement: Runtime Bulk v1 B07 — Modes et conflits

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B07 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Unité engagée

- **WHEN** un import autorisé applique un mode supporté par le propriétaire
- **THEN** ses engagements, rejets et checkpoints respectent les garanties propres à ce mode

#### Scenario: Garantie absente

- **WHEN** un module ne garantit pas la transaction requise pour ATOMIC
- **THEN** le mode est refusé avant mutation sans fallback vers BEST_EFFORT

#### Scenario: Validation seule après flux complet prouvé

- **WHEN** un import VALIDATE_ONLY présente un flux qualifié complet avec intégrité vérifiée et fermeture réussie avant tout appel propriétaire
- **THEN** le rapport, la progression et le checkpoint finaux sont établis sous gardes actuelles avec applied_rows à zéro et sans exécution propriétaire

#### Scenario: Interruption sans validation complète prétendue

- **WHEN** une limite, une annulation ou une perte de bail interrompt la validation
- **THEN** aucune validation complète ni mutation ni persistance forcée n'est prétendue et l'état reste explicite à réconcilier

#### Scenario: Chunk ATOMIC_PER_CHUNK REJECT engagé sans rejou

- **WHEN** une opération IMPORT ATOMIC_PER_CHUNK REJECT à validation complète prouvée applique un chunk sous autorité EXECUTE et gouvernance RESOLVED actuelles, avec participation propriétaire PostgreSQL déclarée au même alias et unité protégée même thread et même transaction
- **THEN** le chunk est engagé avec checkpoint et outbox requise dans la même transaction, les chunks déjà engagés sont conservés, aucun rejou n'est compté comme nouvel effet et un rejet propriétaire ou conflit REJECT annule le chunk courant entier sans mutation partielle
~~~~

