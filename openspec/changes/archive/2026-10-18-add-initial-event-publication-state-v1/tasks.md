# Tâches — vocabulaire initial des états de publication d’événement v1

- [x] 1. Vérifier le canon B11 et OutboxPublicationV1, l’absence du vocabulaire, les limites du change et sa validation OpenSpec ciblée avant code.
- [x] 2. Fournir `src/pixs/backend/event_publication_state.py`, Enum pur aux cinq valeurs canoniques.
- [x] 3. Fournir les tests unitaires de contrat/refus et l’intégration avec import frais sous gardes d’effets vérifiées.
- [x] 4. Compiler séparément les trois fichiers ; exécuter les tests et régressions ciblés ; vérifier UTF-8/LF, conformité, périmètre et empreintes ; rapporter les validations OpenSpec ciblée stricte, globale standard et globale stricte avec leurs codes réels.

Les coches attendent les preuves natives examinées par CGPT. L’archivage puis `STATISTIQUES.md` font l’objet de mandats distincts après les validations ; aucune mesure absente n’est inventée.

## Preuves examinées par CGPT

- Inventaire lecture seule : rapport `msg_14c4afa71001IxQtFYD56arAsY`. Validation ciblée avant code : `req-7e368d4be6c34c9e`, exit 0.
- Module et deux tests : contenus exacts relus ; écritures natives unitaires corrélées.
- Trois compilations séparées : `req-0fa8b603f75b4ee3`, `req-b80cc77c3d98427b`, `req-380ff0d6046e4a86`, chacune exit 0.
- Tests : `req-efe7768ccaea4992`, 54 réussis en 0,982 s, exit 0 ; contrat, import frais sous gardes vérifiées et régressions backend/outbox. Aucun PostgreSQL réel requis.
- Validation ciblée après code : `req-1ee41ba5022448c6`, exit 0. Globale standard : `req-be06a35d088744ae`, 187 valides, 0 échec, exit 0.
- Globale stricte : `req-4bc3d2aa5309403f`, 185 valides et 2 capacités signalées, exit 1 : quatre WARNING de longueur dans bulk-operations requirements[6]/[10]/[13] et identity-assurance requirements[4], zéro ERROR. Ces canons sont inchangés ; ce résultat n’est pas présenté comme un succès strict global.
- Les 16 fichiers existants suivis par empreinte sont inchangés ; sources nouvelles UTF-8/LF, sans changement de façade ou de canon. Matrice cadrages/README revue dans le périmètre du vocabulaire ; aucune mise à jour nécessaire. Git non inspecté, provenance historique non vérifiée.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Preuves examinées par CGPT ».

### C91-SL01 — Vérifier le canon B11 et OutboxPublicationV1, l’absence du vocabulaire, les limites du change et sa validation OpenSpec ciblée avant code.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tâches — vocabulaire initial des états de publication d’événement v1 », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C91-SL02 — Fournir `src/pixs/backend/event_publication_state.py`, Enum pur aux cinq valeurs canoniques.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tâches — vocabulaire initial des états de publication d’événement v1 », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C91-SL03 — Fournir les tests unitaires de contrat/refus et l’intégration avec import frais sous gardes d’effets vérifiées.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tâches — vocabulaire initial des états de publication d’événement v1 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C91-SL04 — Compiler séparément les trois fichiers ; exécuter les tests et régressions ciblés ; vérifier UTF-8/LF, conformité, périmètre et empreintes ; rapporter les validations OpenSpec ciblée stricte, globale standard et globale stricte avec leurs codes réels.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tâches — vocabulaire initial des états de publication d’événement v1 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
