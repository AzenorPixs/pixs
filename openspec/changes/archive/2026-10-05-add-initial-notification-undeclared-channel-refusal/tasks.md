# Tâches — Refus déclaratif explicite du canal de notification non déclaré

## 1. Contrôle déclaratif pur

- [x] 1.1 Exécuter les stricts du change, des spécifications et de tous les éléments avant tout code, avec résultat natif contrôlé.
- [x] 1.2 Publier `src/pixs/kernel/notification_channel_declaration.py` : `NotificationChannelDeclarationError(ValueError)`, helper `require_declared_notification_channel(channel, declared_channels)`, validation de type exact et d'appartenance par identité avant tout contrôle, messages fixes sans reflet des entrées, `__all__` limité à l'erreur et au helper, sans modification de `notifications.py`, de `notification_delivery.py`, de leurs tests ni des façades.
- [x] 1.3 Publier et exécuter le test unitaire : canal déclaré retourné à l'identique ; canal canonique non déclaré refusé ; objet hors membres refusé ; `declared_channels` de type inexact ou contenant un objet hors membres canoniques refusé ; `frozenset` vide refusant tout canal ; messages ne reproduisant aucune entrée ; export exactement `["NotificationChannelDeclarationError", "require_declared_notification_channel"]`.
- [x] 1.4 Publier et exécuter le test d'intégration : import et comportement contrôlé dans un processus frais borné 10 s, marqueur d'intégration distinct, gardes d'effets positives incluses, aucun effet observable.
- [x] 1.5 Exécuter les trois compilations ciblées et la régression complète existante dans le venv temporaire aux pins déjà déclarés, sans toucher aucun environnement existant, contrôler les résultats natifs, UTF-8/LF et les empreintes des sources livrées et des cadrages non concernés.
- [x] 1.6 Exécuter les stricts du change, des spécifications et de tous les éléments après code, résultats natifs contrôlés.

Aucune tâche d'archivage ni de rapport de statistiques ; l'archivage et le rapport STATISTIQUES.md relèvent de décisions et mandats CGPT distincts après preuve des tâches et validation stricte finale.
