# Proposition — Représentation Enum du vocabulaire des états de livraison Notification

## Why

Le vocabulaire fermé des six états de livraison est imposé par les cadrages validés : TECHNICAL.md lignes 1254–1263 énumèrent `QUEUED`, `SENDING`, `SENT`, `DELIVERED`, `FAILED` et `CANCELLED` ; PROJECT.md ligne 1891 exige que les notifications « conservent un état de livraison ». La spécification canonique notifications déclare des travaux persistants avec réessais bornés et lettres mortes produisant « un état diagnostiquable » (exigence « Asynchronisme avec réessais bornés », scénario « Échec persistant tracé »). Aucune représentation structurelle de ce vocabulaire n'existe dans le code.

## What Changes

- Ajouter `src/pixs/kernel/notification_delivery.py` : `NotificationDeliveryState(Enum)` stdlib à six membres nom=valeur dans l'ordre des cadrages, seul export de `__all__`, module indépendant de `notifications.py` ;
- Ajouter un test unitaire et un test d'intégration borné ;
- Delta `specs/notifications/spec.md` MODIFIED reproduisant mot pour mot l'exigence et le scénario canoniques cités, sans addition normative.

## Impacts

- Aucun comportement runtime existant modifié ; aucun envoi, retry, lettre morte, machine à états, transition, provider, préférence, consentement ou persistance introduits ; aucune correspondance future entre `FAILED` et la lettre morte n'est revendiquée ni inventée ;
- Effet d'archive attendu nul (+0/~0/-0/→0) ; cette unité partielle ne livre pas les exigences runtime complètes de notifications.
