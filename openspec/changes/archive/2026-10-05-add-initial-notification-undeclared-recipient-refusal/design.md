# Conception — Contrôle déclaratif de la clé de destinataire Notification

## Forme livrée

Module interne séparé `src/pixs/kernel/notification_recipient_declaration.py`, stdlib seule, sans I/O ni mutation, sans dataclass ni contrat notification complet. Erreur `NotificationRecipientDeclarationError(ValueError)`. Helper `require_declared_notification_recipient(recipient_key, declared_recipient_keys)` retournant `str` : `recipient_key` doit être de type `str` exactement et non vide ; `declared_recipient_keys` doit être de type `frozenset` exactement et chaque élément doit être un `str` exact non vide ; validation intégrale des deux entrées avant toute appartenance ; seulement après validation, appartenance par comparaison de valeur exacte ; retourne `recipient_key` inchangée. `__all__ = ["NotificationRecipientDeclarationError", "require_declared_notification_recipient"]`. Docstring de frontière ; messages fixes dans le patron de `src/pixs/kernel/contracts/models.py`, sans reflet des entrées.

## Décisions

- Clé de destinataire `str` opaque validée par valeur : aucun type canon de destinataire inventé, aucune grammaire d'adresse, aucun identifiant, aucune normalisation ; casse, espacement et ponctuation préservés caractère par caractère ; deux objets distincts de même valeur sont acceptés ;
- Sous-classes de `str`, `bool`, `int`, `None`, conteneurs de type inexact et sous-classes de `frozenset` refusés avant toute invocation des dunder de l'objet hostile ;
- Un conteneur construit par l'appelant avec éléments hostiles peut déclencher `__hash__` par le constructeur `frozenset` avant l'appel du helper : ce comportement relève de l'appelant, pas du helper ; les snapshots de test distinguent ce cas du refus du helper après validation ;
- `frozenset` vide refusant toute clé ; l'helper ne définit aucune valeur par défaut ;
- Modules `notifications.py`, `notification_delivery.py`, `notification_channel_declaration.py`, leurs tests et les façades restent intacts ; aucune façade publique n'exporte le helper.

## Critères observables

- Clé déclarée : l'objet `str` d'entrée est retourné, valeur inchangée ; même valeur sous un objet distinct déclaré : acceptée ;
- Clé vide, non `str`, `None`, `bool`, `int` ou sous-classe de `str` : `NotificationRecipientDeclarationError` à message fixe ;
- `declared_recipient_keys` de type inexact ou sous-classe de `frozenset` : refus avant appartenance ; élément `None`, `bool`, `int`, sous-classe de `str` ou `str` vide : refus avant appartenance ;
- `frozenset` vide : toute clé refusée ;
- Messages : ne reproduisent aucune entrée ;
- Export : exactement `["NotificationRecipientDeclarationError", "require_declared_notification_recipient"]` ;
- UTF-8/LF ; empreintes des modules notification existants, de leurs tests et des façades inchangées ; avant archivage, 181 références et 76 spécifications canoniques inchangées ; après archivage, 180 références et 75 spécifications canoniques exactement inchangées, seul notifications/spec.md ajoute le scénario approuvé ;
- Delta canon autorisé +1 scénario maximal : seul ajout du scénario « Destinataire élargi refusé » sous l'exigence existante, exigence et scénario canoniques reproduits mot à mot ; sources et archives des changes précédents, dont le rapport Refusal d'empreinte `5c63c949cf49701e95f69293507ab40183e6b2974de7d37b6f47f137f56fb40c`, préservés.
