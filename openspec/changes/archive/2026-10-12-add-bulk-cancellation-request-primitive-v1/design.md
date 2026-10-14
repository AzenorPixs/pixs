## Context
B02 et B06 avec annexes BulkExecutionExtensionV1, ProgressV1 et matrice import/export sont approuvés. `apply_transition` exige déjà `cancellation_requested is True` pour CANCELLED et les baux refusent si flag non False. Ce lot ajoute la pose interne du flag, après autorisation de la couche supérieure ; il ne constitue pas une action CANCEL sécurisée de bout en bout.

## Goals / Non-Goals
Signature interne `request_cancellation(*, operation_id: object, expected_revision: object) -> int`, choix Python définitif au niveau interne permis par la Frontière du contrat, sans champ ni sémantique ajouté. Objectif : poser uniquement `cancellation_requested=True` et `revision+1` sous CAS. Non-objectifs : aucun argument `now`, aucune lecture d'horloge, aucune priorité expiration/annulation, aucun statut/progrès/checkpoint/bail/date/champ additionnel, aucune idempotence Command annoncée, aucun ALLOW fabriqué, aucune décision d'autorisation.

## Decisions
Réutiliser gardes `_is_text` et `_require_incrementable_revision`, verrous opération puis extension, `transaction.atomic(using)` existant. Refuser terminal Bulk et CAS obsolète par `TransitionRefused` et `CasConflict` existants. Mise à jour filtrée sur `(operation_id, revision=expected_revision)` puis contrôle une ligne, sans écho de valeur. Répétition avec révision obsolète refusée ; aucune promesse de rejou identique. Autorisation supérieure reste précondition distincte vérifiée par l'appelant.

## Validation
Syntaxe via Python projet `/home/devops/datas/pixs/.venv/bin/python3`. Unitaires : types hostiles avant I/O avec zéro requête, terminaux refusés, CAS valide puis stale refusé, flag persisté et autres champs inchangés. PG isolés : rollback sans trace, concurrence une seule gagnante, persistance du flag, checkpoints/progrès/baux/échéances conservés. Régressions repository existantes par groupes exacts. Secrets PG chargés seul processus test. Strict change, UTF-8/LF, fichiers attendus seuls. Archive unique `--skip-specs` car deltas MODIFIED verbatim, puis STATISTIQUES distinct à six sections.

## Risks / Trade-offs
Une primitive persistante n'est ni autorisation ni preuve d'effet métier. Les tests PG avec providers synthétiques ne prouvent pas une composition de production. Les refus CAS/terminal restent explicites ; une double demande sans révision fraîche échoue au lieu d'être absorbée.

## Rollback
Aucune migration ni donnée de production. Retrait du code et tests du lot, sans toucher modèles, migrations antérieures ou canon.
