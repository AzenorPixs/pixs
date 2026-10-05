# Conception — NotificationDeliveryState

## Choix

`NotificationDeliveryState(Enum)` standard dans `src/pixs/kernel/notification_delivery.py`, six membres nom=valeur : `QUEUED`, `SENDING`, `SENT`, `DELIVERED`, `FAILED`, `CANCELLED`, dans cet ordre ; docstring de frontière ; `__all__ = ["NotificationDeliveryState"]`. Patron identique à `src/pixs/kernel/notifications.py` ; module indépendant, `NotificationChannel`, son `__all__` et ses tests inchangés.

## Justifications

- Vocabulaire fermé déjà énoncé par les cadrages d'autorité (TECHNICAL.md l.1254–1263 ; PROJECT.md l.1891) ;
- Enum stdlib, aucune dépendance, aucun effet observable à l'import ;
- Envoi, réessais, lettres mortes, transitions et persistance relèvent d'exigences non couvertes par cette unité.

## Décisions et limites

- Aucune machine à états, transition, factory, validation, diagnostic, catégorie, service, préférence, portée ou persistance promis ;
- Aucune équivalence future entre `FAILED` et l'état de lettre morte du scénario canonique n'est spécifiée par cette unité ;
- Intégration : processus frais borné 10 s, gardes de construction bornées aux surfaces finies d'effets (écriture, réseau, processus, environnement, bases) sur le seul vocabulaire importé — garde constructive bornée, pas une sandbox universelle ;
- Delta strictement verbatim canonique ; tout résultat d'archive autre que +0/~0/-0/→0 est un écart à rapporter, non à corriger par code.

## Critères observables

- Six noms/valeurs exacts et ordre des cadrages, absence d'alias et de membre supplémentaire, export unique ;
- `py_compile` exit0 par source ; 3 tests unitaires OK ; 1 intégration OK ; régression complète existante OK ;
- UTF-8/LF, empreintes des sources et cadrages non concernés inchangés, dont `src/pixs/kernel/notifications.py` et ses deux tests ;
- Stricts du change, des spécifications et de l'ensemble valides avant et après code.
