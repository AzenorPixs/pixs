## Why

Le requirement validé « Profil structurel préparatoire d'occultation de champ d'audit v1 » ne dispose pas encore de représentation mémoire ni de validation structurelle.

## What Changes

- Ajouter le module interne audit_field_redaction : Enum RedactionMode, AuditFieldRedaction immuable à trois champs explicites et validateur pur.
- Vérifier les types exacts, les références opaques et la cohérence mode/référence par des tests unitaires et un processus frais instrumenté.
- Préserver les exigences d'audit effectif et la façade publique.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- audit : implémentation du profil préparatoire déjà défini par le canon, sans modification normative.

## Impact

Trois nouveaux fichiers Python : src/pixs/kernel/audit_field_redaction.py, tests/unit/test_audit_field_redaction.py et tests/integration/test_audit_field_redaction_integration.py. Aucun payload, I/O, horloge, classification, résolution de référence, persistance, configuration, provider, façade ni dépendance. Aucune garantie d'occultation effective. Archivage avec --skip-specs et rapport STATISTIQUES.md sous mandats distincts.
