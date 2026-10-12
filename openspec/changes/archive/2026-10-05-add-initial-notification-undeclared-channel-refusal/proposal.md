# Proposition — Refus déclaratif explicite du canal de notification non déclaré

## Why

L'exigence canonique « Contrats et préférences déclarés » impose : « Chaque notification MUST suivre un contrat versionné avec destinataires, canaux, préférences et périmètre ; aucun canal implicite ni destinataire élargi sans règle déclarée. » Son scénario « Canal non déclaré refusé » exige : « WHEN un envoi vise un canal non déclaré par le contrat / THEN l'envoi est refusé avec une erreur explicite » (openspec/specs/notifications/spec.md). Le vocabulaire `NotificationChannel` est livré dans le Kernel ; aucun contrôle structurel de la déclaration des canaux n'existe dans le code.

## What Changes

- Ajouter `src/pixs/kernel/notification_channel_declaration.py` : `NotificationChannelDeclarationError(ValueError)` et helper `require_declared_notification_channel(channel, declared_channels)` retournant exactement le membre déclaré, stdlib seule, sans I/O ni mutation, `__all__` limité à ces deux noms, module indépendant de `notifications.py` et `notification_delivery.py` ;
- Ajouter un test unitaire et un test d'intégration borné ;
- Delta `specs/notifications/spec.md` MODIFIED reproduisant mot pour mot l'exigence et le scénario canoniques cités, sans addition normative.

## Impacts

- Aucun comportement runtime existant modifié ; aucun envoi, provider, file, persistance, préférence, consentement, destinataire, version de contrat, périmètre ni autorité backend introduits ou remplacés ; `declared_channels` est un `frozenset` exact de membres canoniques, l'ensemble vide refusant tout canal ; les messages d'erreur sont fixes et ne reproduisent aucune entrée ;
- Effet d'archive attendu nul (+0/~0/-0/→0), baseline de 172 fichiers et 76 spécifications canoniques inchangées ; cette unité partielle ne livre que le refus déclaratif du canal non déclaré : contrat versionné complet, destinataires, préférences, périmètre et envoi réel relèvent d'exigences non couvertes par cette unité.
