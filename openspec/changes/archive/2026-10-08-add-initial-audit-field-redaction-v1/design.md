## Context

Sources : openspec/specs/audit/spec.md, requirement « Profil structurel préparatoire d'occultation de champ d'audit v1 », et TECHNICAL.md §29. Patrons : data_tombstone_profile.py, audit_event.py et diagnostics.

## Goals / Non-Goals

Implémenter uniquement la représentation et sa validation structurelle. Aucun audit effectif, payload avant/après, classification, pseudonymisation effective, résolution, horloge, I/O, persistance, wire format, façade, configuration ou dépendance.

## Decisions

- Module interne audit_field_redaction.py : RedactionMode(Enum) fermé à REDACTED et PSEUDONYMIZED_REFERENCE ; AuditFieldRedaction dataclass frozen, exactement field_reference: str, mode: RedactionMode, replacement_reference: str | None, sans défaut.
- Surface locale __all__ limitée à RedactionMode, AuditFieldRedaction et validate_audit_field_redaction ; façade kernel inchangée.
- Types exacts ; membres Enum par identité. Références str exactes non vides, opaques, sans normalisation. REDACTED exige None explicite ; PSEUDONYMIZED_REFERENCE exige une référence str exacte non vide. Les valeurs proviennent de l'appelant de confiance ou de fixtures synthétiques.
- Diagnostics VALIDATE statiques, préfixe audit_field_redaction., triés et dédupliqués selon les conventions existantes, sans écho de valeurs. Le validateur ne décide aucune autorisation ou applicabilité.
- Tests unitaires puis intégration dans un processus frais -I -B, environnement réduit, gardes positivement vérifiés puis compteurs remis à zéro. Contrôler filesystem, environnement, réseau, subprocess, DB et horloge sans patcher directement les méthodes C immuables.
- Delta MODIFIED reprenant exactement le requirement canonique et ses deux scénarios ; archive --skip-specs.

## Risks / Trade-offs

Le profil pourrait être confondu avec une occultation effective : le contrat et les tests ne certifient que sa structure. Aucun payload ni fusion avec AuditEvent. L'Enum fermé implique une évolution explicite pour tout futur mode.

## Validation

Compilation des trois fichiers ; tests unitaires et intégration fraîche ; régressions audit_event, diagnostics, façades et pureté Kernel ; validation stricte du change, validation canonique et globale. Qualifier séparément les seuls WARNING de longueur exclus par le développeur. Vérifier UTF-8/LF, cohérence du delta et absence de modification hors périmètre.

## Migration Plan

Aucune migration. Aucun changement d'intégration publique. Trois fichiers nouveaux et indépendants.

## Open Questions

Aucune question fonctionnelle ouverte dans le périmètre validé.
