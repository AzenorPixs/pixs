# Conception — Contrôle déclaratif du canal de notification

## Choix

Module interne séparé `src/pixs/kernel/notification_channel_declaration.py`, stdlib seule, sans I/O ni mutation, sans dataclass ni contrat notification complet. Erreur `NotificationChannelDeclarationError(ValueError)`. Helper `require_declared_notification_channel(channel, declared_channels)` retournant exactement le membre existant `NotificationChannel` si déclaré, sinon levant l'erreur. `declared_channels` : type exact `frozenset`, chaque élément vérifié comme membre canonique de `NotificationChannel` par identité (`is`), sans `str`, alias, coercition ni normalisation ; l'ensemble vide refuse tout canal. `__all__ = ["NotificationChannelDeclarationError", "require_declared_notification_channel"]`. Docstring de frontière ; messages fixes dans le patron de `src/pixs/kernel/contracts/models.py`.

## Justifications

- Scénario canonique « Canal non déclaré refusé » : refus par erreur explicite, sans envoi ni provider ;
- Validation intégrale de `declared_channels` avant tout contrôle et de `channel` par identité avant toute comparaison : aucun appel à `__eq__`, `__hash__`, `__str__` ou `__repr__` d'un objet non validé ; l'appartenance est établie par itération en identité sur l'ensemble validé, jamais par `in` sur une entrée brute ;
- Vocabulaire `NotificationChannel` déjà livré et faisant autorité ; modules `notifications.py` et `notification_delivery.py`, leurs tests et les façades restent intacts.

## Décisions et limites

- Aucune autorité backend, règle d'autorisation, version de contrat, destinataires, préférences, consentement ou périmètre n'est importé ni remplacé ; le contrôle reste déclaratif ;
- Messages fixes sans reflet des entrées ; les erreurs de signature Python (nombre ou absence d'arguments) restent des `TypeError` standard ;
- Intégration : processus frais borné 10 s, gardes constructives bornées aux surfaces d'effets (écriture, réseau, processus, environnement, bases) sur les seules surfaces importées, marqueur distinct ;
- Delta strictement verbatim canonique ; tout résultat d'archive autre que +0/~0/-0/→0 est un écart à rapporter, non à corriger par code.

## Critères observables

- Canal déclaré : retour du membre strictement identique (`is`) ; canal canonique non déclaré, objet hors membres, `declared_channels` de type inexact ou contenant un objet hors membres canoniques : `NotificationChannelDeclarationError` avec message fixe ;
- `frozenset()` vide : refus pour tout canal ; export limité aux deux noms ;
- `py_compile` exit0 par source ; tests unitaires OK ; 1 intégration OK ; régression complète existante OK dans le venv temporaire aux pins déclarés ;
- UTF-8/LF ; empreintes de `notifications.py`, `notification_delivery.py`, de leurs tests et des façades inchangées ; baseline 172 fichiers et 76 spécifications canoniques inchangées ;
- Stricts du change, des spécifications et de l'ensemble valides avant et après code.
