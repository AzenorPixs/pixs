# Design — add-initial-component-type-vocabulary-v1

## Context

Source normative : openspec/specs/component-model/spec.md, exigence « Types de composants unifiés », corroborée par TECHNICAL.md §5 et PROJECT.md §2.25. Les conventions de bulk_job_phase.py, architecture_decision_state.py et data_persistence_states.py fournissent le patron Enum pur à valeurs égales aux noms. COMPONENT_TYPES reste le frozenset de référence dans src/pixs/kernel/manifest/models.py ; parse_manifest n’accepte que des chaînes.

## Goals / Non-Goals

Représenter les six noms exacts dans l’ordre canonique KERNEL, MODULE, SUBMODULE, PROVIDER, EXTENSION, THEME. Aucun dispatcher, registre, résolution, transition, validation métier, droit, persistance, worker ou exécution. Pas de nouvelle dépendance ni configuration. Aucune modification de manifest, composition, façades ou littéraux existants.

## Decisions

ComponentType(Enum), sans mixin str, membres dans l’ordre canonique à valeurs identiques aux noms. __all__ expose uniquement ComponentType, sans constante de version. Le choix des noms Python et l’absence de version ont été validés explicitement par CGPT après NFDOC. Aucun changement du canon requis.

## Risks / Trade-offs

Fondation structurelle partielle : ce vocabulaire ne prouve ni enregistrement, ni résolution, ni qualification du runtime ou du profil P0. L’Enum suit les garanties standard, sans promesse d’immutabilité profonde. Aucun remplacement des validateurs ou littéraux existants.

## Validation

Compilation distincte des trois fichiers Python ; tests du vocabulaire exact, du rejet sans normalisation, de la cohérence avec COMPONENT_TYPES sans accepter les membres Enum dans parse_manifest, et d’import frais avec gardes d’effets et contrôles positifs. Régressions manifest_models proches. Validation OpenSpec ciblée stricte et globale standard/stricte, avec résultats natifs séparés et éventuels avertissements historiques rapportés sans correction hors périmètre. UTF-8/LF, contenu et empreintes vérifiés avant archive.
