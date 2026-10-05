# Conception — NotificationChannel

## Choix

`NotificationChannel(Enum)` standard dans `src/pixs/kernel/notifications.py`, cinq membres nom=valeur : `IN_APP`, `EMAIL`, `PUSH`, `SMS`, `WEBHOOK`, dans cet ordre ; docstring de frontière ; `__all__ = ["NotificationChannel"]`. Patron identique à `src/pixs/kernel/jobs.py`.

## Justifications

- Vocabulaire fermé déjà énoncé par les cadrages d'autorité (PROJECT.md l.1889 ; TECHNICAL.md l.1238–1246) ;
- Enum stdlib, aucune dépendance, aucun effet observable à l'import ;
- Sélection de providers et refus runtime des canaux non déclarés relèvent d'exigences non couvertes par cette unité.

## Décisions et limites

- Aucune immuabilité profonde, factory, validation, diagnostic, catégorie, état de livraison, service, préférence, portée ou persistance promis ;
- Intégration : processus frais borné 10 s, gardes de construction bornées aux surfaces finies d'effets (écriture, réseau, processus, environnement, bases) sur le seul vocabulaire importé — garde constructive bornée, pas une sandbox universelle ;
- Delta strictement verbatim canonique ; tout résultat d'archive autre que +0/~0/-0/→0 est un écart à rapporter, non à corriger par code.

## Critères observables

- Cinq noms/valeurs exacts et ordre des cadrages, absence d'alias et de membre supplémentaire, export unique ;
- `py_compile` exit0 par source ; 3 tests unitaires OK ; 1 intégration OK ; régression complète existante OK ;
- UTF-8/LF, empreintes des sources et cadrages non concernés inchangées ;
- Stricts du change, des spécifications et de l'ensemble valides avant et après code.
