## MODIFIED Requirements

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
