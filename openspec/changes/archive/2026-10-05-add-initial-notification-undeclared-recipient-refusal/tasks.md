# Tâches — Refus déclaratif explicite du destinataire élargi non déclaré

## 1. Contrôle déclaratif pur

- [x] 1.1 Exécuter les stricts du change, des spécifications et de tous les éléments avant tout code, avec résultat natif contrôlé.
- [x] 1.2 Publier `src/pixs/kernel/notification_recipient_declaration.py` : `NotificationRecipientDeclarationError(ValueError)`, helper `require_declared_notification_recipient(recipient_key, declared_recipient_keys)`, validation de type exact `str` non vide pour la clé et de `frozenset` exact de `str` exacts non vides intégralement validée avant toute appartenance, comparaison par valeur exacte après validation seulement, retour de la clé entrée inchangée sans normalisation, messages fixes sans reflet des entrées, `__all__` limité à l'erreur et au helper, sans modification de `notifications.py`, de `notification_delivery.py`, de `notification_channel_declaration.py`, de leurs tests ni des façades.
- [x] 1.3 Publier et exécuter le test unitaire : clé déclarée retournée inchangée ; même valeur sous objet distinct accepté ; clé vide, non-`str`, `None`, `bool`, `int` ou sous-classe de `str` refusée avant tout dunder ; `declared_recipient_keys` de type inexact, sous-classe de `frozenset`, ou contenant `None`, `bool`, `int`, sous-classe de `str` ou chaîne vide refusée avant appartenance ; `frozenset` vide refusant toute clé ; messages ne reproduisant aucune entrée ; export exactement `["NotificationRecipientDeclarationError", "require_declared_notification_recipient"]`.
- [x] 1.4 Publier et exécuter le test d'intégration : import et comportement contrôlé dans un processus frais borné 10 s, marqueur d'intégration distinct, gardes d'effets positives incluses, snapshots distinguant le `__hash__` déclenché par le constructeur `frozenset` de l'appelant avant le helper du refus du helper après validation intégrale, aucun effet observable.
- [x] 1.5 Exécuter les trois compilations ciblées et la régression complète existante dans le venv temporaire aux cinq pins déjà déclarés, sans toucher aucun environnement existant, contrôler les résultats natifs, UTF-8/LF et les empreintes des sources livrées et des cadrages non concernés, puis nettoyer le venv temporaire.
- [x] 1.6 Exécuter les stricts du change, des spécifications et de tous les éléments après code, résultats natifs contrôlés.

Aucune tâche d'archivage ni de rapport de statistiques ; l'archivage et le rapport STATISTIQUES.md relèvent de décisions et mandats CGPT distincts après preuve des tâches et validation stricte finale.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 1. Contrôle déclaratif pur ».

### O58-SL01 — Exécuter les stricts du change, des spécifications et de tous les éléments avant tout code, avec résultat natif contrôlé.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Contrôle déclaratif pur », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O58-SL02 — Publier `src/pixs/kernel/notification_recipient_declaration.py` : `NotificationRecipientDeclarationError(ValueError)`, helper `require_declared_notification_recipient(recipient_key, declared_recipient_keys)`, validation de type exact `str` non vide pour la clé et de `frozenset` exact de `str` exacts non vides intégralement validée avant toute appartenance, comparaison par valeur exacte après validation seulement, retour de la clé entrée inchangée sans normalisation, messages fixes sans reflet des entrées, `__all__` limité à l'erreur et au helper, sans modification de `notifications.py`, de `notification_delivery.py`, de `notification_channel_declaration.py`, de leurs tests ni des façades.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Contrôle déclaratif pur », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O58-SL03 — Publier et exécuter le test unitaire : clé déclarée retournée inchangée ; même valeur sous objet distinct accepté ; clé vide, non-`str`, `None`, `bool`, `int` ou sous-classe de `str` refusée avant tout dunder ; `declared_recipient_keys` de type inexact, sous-classe de `frozenset`, ou contenant `None`, `bool`, `int`, sous-classe de `str` ou chaîne vide refusée avant appartenance ; `frozenset` vide refusant toute clé ; messages ne reproduisant aucune entrée ; export exactement `["NotificationRecipientDeclarationError", "require_declared_notification_recipient"]`.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Contrôle déclaratif pur », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O58-SL04 — Publier et exécuter le test d'intégration : import et comportement contrôlé dans un processus frais borné 10 s, marqueur d'intégration distinct, gardes d'effets positives incluses, snapshots distinguant le `__hash__` déclenché par le constructeur `frozenset` de l'appelant avant le helper du refus du helper après validation intégrale, aucun effet observable.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Contrôle déclaratif pur », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O58-SL05 — Exécuter les trois compilations ciblées et la régression complète existante dans le venv temporaire aux cinq pins déjà déclarés, sans toucher aucun environnement existant, contrôler les résultats natifs, UTF-8/LF et les empreintes des sources livrées et des cadrages non concernés, puis nettoyer le venv temporaire.

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Contrôle déclaratif pur », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O58-SL06 — Exécuter les stricts du change, des spécifications et de tous les éléments après code, résultats natifs contrôlés.

- Ancien repère et tâche rattachée : tâche 1.6 ; section « 1. Contrôle déclaratif pur », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
