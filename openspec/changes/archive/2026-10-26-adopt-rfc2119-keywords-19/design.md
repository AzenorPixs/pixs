## Context

Ce lot 19 est issu de 2026-09-10-adopt-rfc2119-keywords. Le découpage en 21 lots a été explicitement validé par le développeur le 2026-10-26.

## Goals / Non-Goals

- Respecter la limite de dix deltas sans fractionner les fichiers normatifs.
- Préserver leurs octets, les 205 exigences et les 206 scénarios de la collection.
- Ne modifier ni le canon ni le contenu des exigences et scénarios.
- Ne pas confondre ce découpage documentaire avec une implémentation nouvelle ou la résolution de 2.1.

## Decisions

Chaque fichier specs/<capacité>/spec.md appartient à un seul lot. Les modifications concernent uniquement le cadrage, les tâches de validation et la traçabilité. L'archive d'origine complète est sauvegardée avant publication. Aucun marqueur skip_specs n'est utilisé pour dispenser les deltas de validation.

## Validation

Valider strictement la proposition et les deltas avant archivage, vérifier les empreintes et utiliser archive --skip-specs sans --no-validate. Revalider les archives résultantes et vérifier que le canon réel reste inchangé.
