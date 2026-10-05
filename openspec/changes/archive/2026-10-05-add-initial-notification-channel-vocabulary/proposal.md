# Proposition — Représentation Enum du vocabulaire de canaux Notification

## Pourquoi

Le vocabulaire fermé des cinq canaux est imposé par les cadrages validés : PROJECT.md ligne 1889 et TECHNICAL.md lignes 1238–1246 énumèrent `IN_APP`, `EMAIL`, `PUSH`, `SMS` et `WEBHOOK` comme capacités indépendantes, sans provider concret imposé (TECHNICAL.md ligne 1248). La spécification canonique notifications interdit tout canal implicite (« Contrats et préférences déclarés », scénario « Canal non déclaré refusé »). Aucune représentation structurelle de ce vocabulaire n'existe dans le code.

## Changements

- Ajouter `src/pixs/kernel/notifications.py` : `NotificationChannel(Enum)` stdlib à cinq membres nom=valeur dans l'ordre des cadrages, seul export de `__all__` ;
- Ajouter un test unitaire et un test d'intégration borné ;
- Delta `specs/notifications/spec.md` MODIFIED reproduisant mot pour mot l'exigence et le scénario canoniques cités, sans addition normative.

## Impacts

- Aucun comportement runtime existant modifié ; aucun provider, envoi, état de livraison, préférence, consentement ou persistance introduits ;
- Effet d'archive attendu nul (+0/~0/-0/→0) ; cette unité partielle ne livre pas les exigences runtime complètes de notifications.
