# Proposition — Refus déclaratif explicite du destinataire élargi non déclaré

## Why

L'exigence canonique « Contrats et préférences déclarés » impose : « Chaque notification MUST suivre un contrat versionné avec destinataires, canaux, préférences et périmètre ; aucun canal implicite ni destinataire élargi sans règle déclarée. » Son scénario « Canal non déclaré refusé » exige : « WHEN un envoi vise un canal non déclaré par le contrat / THEN l'envoi est refusé avec une erreur explicite » (openspec/specs/notifications/spec.md). Le contrôle structurel de la déclaration des canaux est livré dans `src/pixs/kernel/notification_channel_declaration.py` ; la clause résiduelle « aucun ... destinataire élargi sans règle déclarée » ne dispose d'aucun contrôle structurel dans le code.

## What Changes

- Ajouter `src/pixs/kernel/notification_recipient_declaration.py` : `NotificationRecipientDeclarationError(ValueError)` et helper `require_declared_notification_recipient(recipient_key, declared_recipient_keys)` retournant exactement la clé `str` d'entrée quand elle est déclarée, stdlib seule, sans I/O ni mutation, `__all__` limité à ces deux noms, module indépendant des modules notification existants ;
- Fixer la garde : `recipient_key` de type `str` exact et non vide ; `declared_recipient_keys` de type `frozenset` exact dont chaque élément est un `str` exact non vide, validée intégralement avant toute appartenance ; comparaison par valeur exacte après validation seulement ; retour de la clé entrée inchangée ; aucune normalisation, strip, casefold, grammaire d'adresse, identification ni valeur par défaut ; espacement jamais transformé ; objets distincts de même valeur acceptés ;
- Delta `specs/notifications/spec.md` MODIFIED reproduisant mot pour mot l'exigence et le scénario canoniques cités, sans addition d'exigence nouvelle, et ajoutant le seul scénario « Destinataire élargi refusé » qui opérationnalise la même exigence MUST existante.

## Impacts et limites

Aucun dataclass, contrat de notification complet, façade publique, service, provider, envoi, file, persistance, préférence, consentement, destinataire riche, tenant, périmètre, autorité backend ni modification de `notifications.py`, `notification_delivery.py`, `notification_channel_declaration.py`, de leurs tests ou des façades. Les préférences relatives aux événements critiques de sécurité restent sans ancrage canonique validé et ne sont pas traitées ici.
