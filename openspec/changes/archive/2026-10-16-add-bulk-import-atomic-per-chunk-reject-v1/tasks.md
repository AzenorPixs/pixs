# Tasks — add-bulk-import-atomic-per-chunk-reject-v1

Aucune tâche cochée sans preuve. Les déclarations serveur et les tests doivent démontrer un chemin positif, sans inventer de garantie à partir de méthodes présentes.

- [x] 1.1 Implémenter la participation PostgreSQL propriétaire explicite et la façade IMPORT ATOMIC_PER_CHUNK/REJECT, avec validation complète avant APPLY, gardes actuelles et engagement atomique par chunk.
- [x] 1.2 Ajouter les tests unitaires d’import inerte, types hostiles, capacités exactes, refus avant I/O, limites, diagnostics statiques et erreurs inattendues non masquées.
- [x] 1.3 Ajouter le test ordinaire inerte et la qualification PostgreSQL réelle isolée : mutation/idempotence/progression/checkpoint/outbox requis same-tx, rollback, CAS, baux, reprise/rejou, annulation/échéances, nettoyage et connexions fermées.
- [x] 2.1 Compiler tous les fichiers Python autorisés et exécuter les tests ordinaires ciblés avec sorties natives.
- [x] 2.2 Qualifier PostgreSQL réel sans mock de la primitive transactionnelle ni modification des tables publiques, avec chemin positif et finalisation prouvés.
- [x] 2.3 Exécuter les régressions affectées, notamment VALIDATE_ONLY et les gardes runtime/annulation/idempotence/outbox ; vérifier les empreintes, UTF-8/LF, conformité documentaire et absence d’écriture hors périmètre.
- [x] 2.4 Obtenir l’exclusion, valider la base combinée et le strict ciblé/global avec résultats exacts, puis relire toutes les preuves avant les coches et l’archive.

Après les preuves préarchive : archive unique et synchronisation B07 seules sous mandat distinct, contrôle postarchive et publication réelle, libération d’exclusion, rapport STATISTIQUES.md distinct vérifié en phase REPORT, gate individuel, désarmement et libération. Le parent CISMP revient à SÉLECTION ; ces opérations ne sont pas cochées par anticipation.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### B55-SL01 — Implémenter la participation PostgreSQL propriétaire explicite et la façade IMPORT ATOMIC_PER_CHUNK/REJECT, avec validation complète avant APPLY, gardes actuelles et engagement atomique par chunk.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « Tasks — add-bulk-import-atomic-per-chunk-reject-v1 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B55-SL02 — Ajouter les tests unitaires d’import inerte, types hostiles, capacités exactes, refus avant I/O, limites, diagnostics statiques et erreurs inattendues non masquées.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « Tasks — add-bulk-import-atomic-per-chunk-reject-v1 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B55-SL03 — Ajouter le test ordinaire inerte et la qualification PostgreSQL réelle isolée : mutation/idempotence/progression/checkpoint/outbox requis same-tx, rollback, CAS, baux, reprise/rejou, annulation/échéances, nettoyage et connexions fermées.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « Tasks — add-bulk-import-atomic-per-chunk-reject-v1 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B55-SL04 — Compiler tous les fichiers Python autorisés et exécuter les tests ordinaires ciblés avec sorties natives.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « Tasks — add-bulk-import-atomic-per-chunk-reject-v1 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B55-SL05 — Qualifier PostgreSQL réel sans mock de la primitive transactionnelle ni modification des tables publiques, avec chemin positif et finalisation prouvés.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « Tasks — add-bulk-import-atomic-per-chunk-reject-v1 », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B55-SL06 — Exécuter les régressions affectées, notamment VALIDATE_ONLY et les gardes runtime/annulation/idempotence/outbox ; vérifier les empreintes, UTF-8/LF, conformité documentaire et absence d’écriture hors périmètre.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « Tasks — add-bulk-import-atomic-per-chunk-reject-v1 », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### B55-SL07 — Obtenir l’exclusion, valider la base combinée et le strict ciblé/global avec résultats exacts, puis relire toutes les preuves avant les coches et l’archive.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « Tasks — add-bulk-import-atomic-per-chunk-reject-v1 », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
