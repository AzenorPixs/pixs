# Design — add-initial-capability-criticality-vocabulary-v1

## Context

Source normative : openspec/specs/component-model/spec.md, exigences schéma 1 capacités et contrats versionnés, corroborée par openspec/specs/capabilities/spec.md (descripteur et disponibilité) et TECHNICAL.md §7.1. Les conventions de component_type.py, bulk_job_phase.py et architecture_decision_state.py fournissent le patron Enum pur à valeurs égales aux noms. CRITICALITIES reste le frozenset de référence dans src/pixs/kernel/manifest/models.py ; parse_manifest n'accepte que des chaînes.

## Goals / Non-Goals

Représenter les deux noms exacts dans l'ordre canonique REQUIRED, OPTIONAL. Aucun dispatcher, registre, résolution, transition, validation métier, droit, persistance, worker ou exécution. Pas de nouvelle dépendance ni configuration. Aucune modification de manifest, composition, descripteurs, fallback, availability, façades ou littéraux existants.

## Decisions

CapabilityCriticality(Enum), sans mixin str, membres dans l'ordre canonique à valeurs identiques aux noms. __all__ expose uniquement CapabilityCriticality, sans constante de version. Le choix des noms Python et l'absence de version ont été validés explicitement par CGPT après NFDOC. Aucun changement du canon requis.

## Risks / Trade-offs

Fondation structurelle partielle : ce vocabulaire ne prouve ni enregistrement, ni résolution, ni qualification du runtime. L'Enum suit les garanties standard, sans promesse d'immutabilité profonde. Aucun remplacement des validateurs ou littéraux existants.

## Validation

Compilation distincte des deux fichiers Python ; tests du vocabulaire exact, du rejet sans normalisation, de la cohérence avec CRITICALITIES sans accepter les membres Enum dans parse_manifest, de la préservation criticality str et règles fallback REQUIRED/OPTIONAL, et d'import frais sans Django ni réseau/commandes. Régressions manifest_models, manifest_schema1 et capability_resolution proches. Validation OpenSpec ciblée stricte et globale standard/stricte, avec résultats natifs séparés et éventuels avertissements historiques rapportés sans correction hors périmètre. UTF-8/LF, contenu et empreintes vérifiés avant archive.
