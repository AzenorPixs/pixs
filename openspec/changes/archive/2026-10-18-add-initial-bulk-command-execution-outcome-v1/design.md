# Design — add-initial-bulk-command-execution-outcome-v1

## Context

Source normative : openspec/specs/bulk-operations/spec.md, schéma CommandExecutionV1 et clauses B07. Les conventions de bulk_job_handler.py et bulk_job_phase.py fournissent le patron Enum pur. Les littéraux str de bulk_runtime_contracts.py et bulk_server_apply.py restent inchangés.

## Goals / Non-Goals

Représenter les trois noms exacts APPLIED, REPLAYED, REJECTED. Aucun dispatcher, couplage outcome/diagnostics, transition, validation métier, droit, persistance, worker, idempotence ou exécution. Pas de nouvelle dépendance ni configuration.

## Decisions

BulkCommandExecutionOutcome(Enum) dans src/pixs/backend/bulk_command_execution_outcome.py, sans mixin str, membres APPLIED/REPLAYED/REJECTED dans l’ordre canonique. __all__ expose uniquement ce symbole. Le choix des noms Python a été validé explicitement par CGPT après NFDOC. Aucun changement du canon requis.

## Risks / Trade-offs

Fondation structurelle partielle : ce vocabulaire ne prouve ni exécution ni qualification du runtime. L’Enum suit les garanties standard, sans promesse d’immutabilité profonde. Aucun remplacement des validateurs ou littéraux str existants.

## Validation

Compilation distincte des trois fichiers Python ; tests du vocabulaire exact, du rejet sans normalisation et d’import frais avec gardes d’effets et contrôles positifs. Régressions bulk_runtime_contracts proches. Validation OpenSpec ciblée stricte et globale standard/stricte, avec résultats natifs séparés et éventuels avertissements historiques rapportés sans correction hors périmètre. UTF-8/LF, contenu et empreintes vérifiés avant archive.
