# Proposition — Références préparatoires de déduplication des notifications

## Why

La capacité canonique notifications définit désormais le profil NotificationDeduplicationReferenceV1 et ses limites préparatoires. Sa représentation et sa validation restent à implémenter. Cette unité prépare deux références opaques ; elle ne livre pas la déduplication persistante exigée du futur runtime.

## What Changes

- Ajouter src/pixs/kernel/notification_deduplication.py, avec le profil immuable à exactement deux champs et son validateur défensif.
- Ajouter des tests unitaires et une intégration en processus frais sous gardes d'effets.
- Reprendre exactement les deux exigences canoniques dans un delta MODIFIED, sans norme supplémentaire ni changement du canon.

## Impacts

Trois nouveaux fichiers Python seulement. Réutiliser Diagnostic et VALIDATE sans modifier les modules existants. Aucune nouvelle dépendance, configuration, migration, façade ou modification Git. Aucune unicité, résolution de périmètre, persistance, rétention, notification envoyée ou liaison Job. Archivage prévu avec --skip-specs, le canon étant déjà publié par la RSMP préalable ; STATISTIQUES.md reste obligatoire après archive.
