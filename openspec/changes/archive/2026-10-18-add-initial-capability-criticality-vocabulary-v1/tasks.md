# Tasks — add-initial-capability-criticality-vocabulary-v1

## 1. Préparation et implémentation

- [x] 1.1 Vérifier component-model, capabilities, absence de vocabulaire existant et valider le périmètre NFDOC.
- [x] 1.2 Créer les quatre artefacts OpenSpec cohérents, sans delta normatif artificiel.
- [x] 1.3 Ajouter CapabilityCriticality sans effet ni modification des consommateurs, façades ou manifests.
- [x] 1.4 Ajouter les tests unitaires et l'import isolé avec gardes d'effets.

## 2. Validation et clôture

- [x] 2.1 Compiler les deux nouveaux fichiers Python et exécuter les tests ciblés et régressions applicables.
- [x] 2.2 Exécuter la validation OpenSpec ciblée stricte, globale standard et stricte ; distinguer échecs et avertissements historiques.
- [x] 2.3 Vérifier contenu, UTF-8/LF, absence d'écriture hors périmètre et conformité aux cadrages.
- [x] 2.4 Présenter toutes les preuves à CGPT et obtenir son autorisation distincte pour l'archivage unique.

Le rapport STATISTIQUES.md est exigé après archivage, sous mandat distinct, avant gate et livraison. Aucun Git autorisé.

## Modules de test

test_modules: ["tests.unit.test_capability_criticality", "tests.unit.test_manifest_models", "tests.unit.test_manifest_schema1", "tests.unit.test_capability_resolution"]

## Preuves examinées par Codex

- Deux fichiers Python compilés séparément : code 0.
- Six modules ciblés : 97 tests réussis, code 0, dont import frais sous gardes positives.
- OpenSpec ciblé strict : code 0, aucun delta normatif requis (skip_specs:true).
- OpenSpec global standard : 187/187, code 0.
- OpenSpec global strict : 185/187, code 1 ; quatre avertissements de longueur préexistants (bulk-operations exigences 6/10/13 ; identity-assurance exigence 4), aucune ERROR ; aucun canon corrigé hors périmètre. Ce résultat ne constitue pas une réussite stricte globale.
- Six fichiers relus et vérifiés UTF-8/LF ; module et tests conformes aux contenus approuvés. Un littéral de test divergent a été corrigé sous mandat neuf avant exécution.
- Empreintes des cadrages, canons component-model/capabilities, façade Kernel, manifest/models.py, capabilities.py et lifecycle/availability.py inchangées.
- Archivage unique explicitement autorisé par Codex après examen des preuves ; STATISTIQUES.md obligatoire sous mandat distinct après archivage.
- PostgreSQL et frontend sans objet pour ce vocabulaire pur ; Git non inspecté et non autorisé. Le cycle global reste incomplet.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 2. Validation et clôture » ; « Preuves examinées par Codex ».

### C88-SL01 — Vérifier component-model, capabilities, absence de vocabulaire existant et valider le périmètre NFDOC.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Préparation et implémentation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C88-SL02 — Créer les quatre artefacts OpenSpec cohérents, sans delta normatif artificiel.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Préparation et implémentation », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C88-SL03 — Ajouter CapabilityCriticality sans effet ni modification des consommateurs, façades ou manifests.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Préparation et implémentation », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C88-SL04 — Ajouter les tests unitaires et l'import isolé avec gardes d'effets.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Préparation et implémentation », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C88-SL05 — Compiler les deux nouveaux fichiers Python et exécuter les tests ciblés et régressions applicables.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Validation et clôture », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C88-SL06 — Exécuter la validation OpenSpec ciblée stricte, globale standard et stricte ; distinguer échecs et avertissements historiques.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Validation et clôture », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C88-SL07 — Vérifier contenu, UTF-8/LF, absence d'écriture hors périmètre et conformité aux cadrages.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Validation et clôture », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C88-SL08 — Présenter toutes les preuves à CGPT et obtenir son autorisation distincte pour l'archivage unique.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Validation et clôture », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
