# Proposal — add-bulk-event-envelope-persistence-v1

## Why
Fondation partielle de persistance pour le runtime Bulk v1, liée à B11 Outbox et publication. Les profils préparatoires livrés restent inchangés. Aucune publication, aucune séquence, aucun publisher.

## What Changes
Fournir une primitive append-only des treize clés EventEnvelopeV1, avec codec privé texte JSON, écriture dans la transaction propriétaire active et copies owned en lecture. Sans publication.

## Périmètre source
Six fichiers ciblés, cinq nouveaux plus un import minimal :
- src/pixs/backend/bulk_event_envelope_record.py (nouveau)
- src/pixs/backend/bulk_event_envelope_repository.py (nouveau)
- src/pixs/backend/migrations/0007_bulk_event_envelope.py (nouveau, dépend 0006, réversible)
- src/pixs/backend/models.py (import minimal existant)
- tests/unit/test_bulk_event_envelope_persistence.py (nouveau)
- tests/integration/test_bulk_event_envelope_persistence_integration.py (nouveau)

## Principes
- Treize clés exactes sans défaut, event_id clé primaire explicite de sa table.
- Codec JSON TEXT privé de persistance, distinct de tout wire format ou canonique.
- Limites explicites existantes fournies par l'appelant, payload NUL échappé et préservé, scalaires JSON exacts, refus technique de capacité avant toute entrée/sortie.
- Capture frozen owned, exports owned, UTC strict, garde type-hostile avant callbacks.
- Modèle et repository insert-only, sans update, replay ou upsert.
- Insert avec force_insert dans la transaction active de l'appelant, alias unique validé. Seul le duplicata SQL23505 sur la clé primaire donne un refus stable, avec rollback du propriétaire même lorsque l'erreur est capturée.
- Aucun appel aux ports de confiance, aucune autorité nouvelle : seules les préconditions documentées de l'appelant, sans garantie métier ajoutée.

## Tests et validations
- Types hostiles, diagnostics sans écho, import inerte, processus frais offline.
- NUL, scalaires limites, refus de capacité avant entrée/sortie, UTC et copies, gel.
- Co-transaction commit et rollback, race à une création unique et un refus de duplicata sans second effet, rollback même capturé, contraintes persistantes.
- Migration isolée, nettoyage du schéma de test, connexions fermées, régressions pertinentes.
- Exécution avec l'interpréteur et l'environnement du projet et OpenSpec selon DEVOPS.md, PostgreSQL isolé autorisé dans le seul processus de test.

## Non-objectifs
Outbox, inbox, publisher, sequence. Norme, champ, port, callback ou autorité nouveaux. Mutation des modules purs, du runtime ou de command-idempotency existants. Schéma propriétaire, minimisation ou absence de secrets. Provider de production, HTTP, frontend, PA, PZT, purge, holds, Git, infra, secrets.

## Archive et rapport
Procédure distincte après preuves, hors tâches ci-dessous.
