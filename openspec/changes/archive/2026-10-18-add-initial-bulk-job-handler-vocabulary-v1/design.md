# Design — add-initial-bulk-job-handler-vocabulary-v1

## Context

Source normative : openspec/specs/jobs/spec.md, annexe B08, clause « Les handlers déclarés MUST être pixs.bulk.stage, pixs.bulk.validate, pixs.bulk.apply et pixs.bulk.export, version 1.0.0 ». Les conventions de bulk_job_phase.py et jobs.py fournissent le patron Enum pur. Les littéraux de bulk_server_admission.py restent inchangés.

## Goals / Non-Goals

Représenter les quatre noms exacts et leur version canonique. Aucun dispatcher, association automatique phase/handler, résolution, transition, validation métier, droit, persistance, worker ou exécution. Pas de nouvelle dépendance ni configuration.

## Decisions

BulkJobHandler(Enum), sans mixin str, membres STAGE/VALIDATE/APPLY/EXPORT dans l’ordre B08. BULK_JOB_HANDLER_VERSION est la chaîne exacte 1.0.0. __all__ expose uniquement ces deux symboles. Le choix des noms Python a été validé explicitement par CGPT après NFDOC. Aucun changement du canon requis.

## Risks / Trade-offs

Fondation structurelle partielle : ce vocabulaire ne prouve ni implémentation des quatre handlers ni qualification du runtime ou du profil P0. L’Enum suit les garanties standard, sans promesse d’immutabilité profonde. Aucun remplacement des validateurs ou littéraux existants.

## Validation

Compilation distincte des trois fichiers Python ; tests du vocabulaire exact, du rejet sans normalisation et d’import frais avec gardes d’effets et contrôles positifs. Régressions BulkJobPhase et JobState proches. Validation OpenSpec ciblée stricte et globale standard/stricte, avec résultats natifs séparés et éventuels avertissements historiques rapportés sans correction hors périmètre. UTF-8/LF, contenu et empreintes vérifiés avant archive.
