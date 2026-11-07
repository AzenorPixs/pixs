## 1. Preparation

- [x] 1.1 Prouver perimetre, absence de change actif et perimetre CGPT.
- [x] 1.2 Preparer les cinq artefacts et reussir la validation OpenSpec stricte avant code.

## 2. Gate de disponibilite

- [x] 2.1 Creer src/pixs/kernel/lifecycle/availability.py seul : types figes exacts (CapabilityObservation, CapabilityFallback, CapabilityState, ConsumedCapabilityState, GatedLifecycleResult avec warnings obligatoire), compute_capability_availability retournant quatre tuples (etats, etats consommes, diagnostics FATAUX, warnings NONFATAUX) et run_gated_hooks purs, validation fermee et PROJECTION des faits deja resolus (trois filtres successifs : descripteurs LIES filtres sur l'identite de cible de l'exigence, couple (consumer_id, provider_id) associe par arete de composition.edges — aretes NON typees par capacite, une arete multiple inter-cibles n'est jamais un refus —, matches du parseur partage sur la version exacte declaree par le descripteur lie, verifier des faits deja resolus n'etant pas une nouvelle resolution ; zero fait compatible : OPTIONAL = cas normal d'absence/incompatibilite deja tolere par compose avec activated True, DEGRADED warning NONFATAL avec repli declare sinon FATAL declaration manquante, REQUIRED = BLOCKED fatal, plusieurs faits compatibles = ambiguite fatale sans choix arbitraire ; aretes et observations d'autres cibles ignorees ; jamais par capability_id seul ; aucun candidat non lie) avant tout effet, etats VALIDES restitues memes avec diagnostics fatals lorsque la classification fermee demeure possible, precedence des six etats avec BLOCKED explicite (operable False) distinct de DISABLED, fallback exige seulement pour OPTIONAL non AVAILABLE, provenance hote (RuntimeProfile valide par l'hote, jamais importe), sans IO ni seconde resolution ni parsing de diagnostics.
- [x] 2.2 Creer tests/unit/test_capability_availability_gate.py : six etats et precedence, separation FATAL/warnings, refus fermes avant effet (required non AVAILABLE, optional non AVAILABLE sans repli declare, doublons, observations incoherentes), projection des faits resolus (deux consommateurs/meme capacite/contraintes disjointes, observation AVAILABLE du mauvais fournisseur jamais autorisante, arete multiple inter-cibles jamais refusee, REQUIRED zero fait compatible apres projection = BLOCKED fatal, plusieurs faits compatibles = ambiguite fatale, OPTIONAL zero fait compatible = cas normal absente/incompatible : DEGRADED warning avec repli declare sinon FATAL declaration manquante), BLOCKED explicite (operable False) distinct de DISABLED, OPTIONAL AVAILABLE sans fallback autorisee, types exacts, determinisme, sans echo de valeur brute.
- [x] 2.3 Creer tests/integration/test_capability_availability_gate_integration.py : subprocess frais, gardes IO causales avant import, callbacks passes et comptes, preuve ZERO appel quand FATAL avant tout depart (compteur de callbacks, jamais un rollback simule) avec etats VALIDES inspectables restitues (y compris BLOCKED et warnings OPTIONAL conserves), warnings seuls executant reellement run_hooks, permutations d'ordre d'entree a etats identiques, succes puis refus par etat, exception callback hote propagee conformement a run_hooks (limite hote explicite), chemin lifecycle reel via run_hooks, sans Django/PG/reseau.

## 3. Preuves

- [x] 3.1 Reussir tests unitaires puis integration sur l'executable DEVOPS actuel sous mandats distincts, sans assertion de temps ni fake hard deadline.
- [x] 3.2 Verifier AST 3.11 UTF-8 LF, perimetre availability.py+2 suites, relecture byteexact, diagnostics sans valeur brute, regression ciblee suites lifecycle/descripteurs/composition existantes sous runtime actuel, strict apres preuves, avant tout cochage.
- [x] 3.3 Prouver criteres precedents et delta normatif MOTAMOT de R2 sans nouveau scenario ; aucun etat fabrique depuis une liaison seule, aucune pretention R1/R3/R4, pas de disponibilite operationnelle de production ni P0 global ; archivage et statistiques distincts apres controle.

Archivage et statistiques distincts apres preuves, conserves dans le RUN parent.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Preuves ».

### C53-SL01 — Prouver perimetre, absence de change actif et perimetre CGPT.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Preparation », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C53-SL02 — Preparer les cinq artefacts et reussir la validation OpenSpec stricte avant code.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Preparation », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C53-SL03 — Creer src/pixs/kernel/lifecycle/availability.py seul : types figes exacts (CapabilityObservation, CapabilityFallback, CapabilityState, ConsumedCapabilityState, GatedLifecycleResult avec warnings obligatoire), compute_capability_availability retournant quatre tuples (etats, etats consommes, diagnostics FATAUX, warnings NONFATAUX) et run_gated_hooks purs, validation fermee et PROJECTION des faits deja resolus (trois filtres successifs : descripteurs LIES filtres sur l'identite de cible de l'exigence, couple (consumer_id, provider_id) associe par arete de composition.edges — aretes NON typees par capacite, une arete multiple inter-cibles n'est jamais un refus —, matches du parseur partage sur la version exacte declaree par le descripteur lie, verifier des faits deja resolus n'etant pas une nouvelle resolution ; zero fait compatible : OPTIONAL = cas normal d'absence/incompatibilite deja tolere par compose avec activated True, DEGRADED warning NONFATAL avec repli declare sinon FATAL declaration manquante, REQUIRED = BLOCKED fatal, plusieurs faits compatibles = ambiguite fatale sans choix arbitraire ; aretes et observations d'autres cibles ignorees ; jamais par capability_id seul ; aucun candidat non lie) avant tout effet, etats VALIDES restitues memes avec diagnostics fatals lorsque la classification fermee demeure possible, precedence des six etats avec BLOCKED explicite (operable False) distinct de DISABLED, fallback exige seulement pour OPTIONAL non AVAILABLE, provenance hote (RuntimeProfile valide par l'hote, jamais importe), sans IO ni seconde resolution ni parsing de diagnostics.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Gate de disponibilite », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C53-SL04 — Creer tests/unit/test_capability_availability_gate.py : six etats et precedence, separation FATAL/warnings, refus fermes avant effet (required non AVAILABLE, optional non AVAILABLE sans repli declare, doublons, observations incoherentes), projection des faits resolus (deux consommateurs/meme capacite/contraintes disjointes, observation AVAILABLE du mauvais fournisseur jamais autorisante, arete multiple inter-cibles jamais refusee, REQUIRED zero fait compatible apres projection = BLOCKED fatal, plusieurs faits compatibles = ambiguite fatale, OPTIONAL zero fait compatible = cas normal absente/incompatible : DEGRADED warning avec repli declare sinon FATAL declaration manquante), BLOCKED explicite (operable False) distinct de DISABLED, OPTIONAL AVAILABLE sans fallback autorisee, types exacts, determinisme, sans echo de valeur brute.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Gate de disponibilite », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C53-SL05 — Creer tests/integration/test_capability_availability_gate_integration.py : subprocess frais, gardes IO causales avant import, callbacks passes et comptes, preuve ZERO appel quand FATAL avant tout depart (compteur de callbacks, jamais un rollback simule) avec etats VALIDES inspectables restitues (y compris BLOCKED et warnings OPTIONAL conserves), warnings seuls executant reellement run_hooks, permutations d'ordre d'entree a etats identiques, succes puis refus par etat, exception callback hote propagee conformement a run_hooks (limite hote explicite), chemin lifecycle reel via run_hooks, sans Django/PG/reseau.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Gate de disponibilite », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C53-SL06 — Reussir tests unitaires puis integration sur l'executable DEVOPS actuel sous mandats distincts, sans assertion de temps ni fake hard deadline.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C53-SL07 — Verifier AST 3.11 UTF-8 LF, perimetre availability.py+2 suites, relecture byteexact, diagnostics sans valeur brute, regression ciblee suites lifecycle/descripteurs/composition existantes sous runtime actuel, strict apres preuves, avant tout cochage.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C53-SL08 — Prouver criteres precedents et delta normatif MOTAMOT de R2 sans nouveau scenario ; aucun etat fabrique depuis une liaison seule, aucune pretention R1/R3/R4, pas de disponibilite operationnelle de production ni P0 global ; archivage et statistiques distincts apres controle.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
