# Tasks

## 1. Préparation

- [x] 1.1 Prouver périmètre CGPT, absence de change actif et baseline byte-à-byte des symboles R1, C1a, C2, R3 et de la composition bornée de `src/pixs/kernel/feature_flags.py`, des deux suites bornées et des quatre-vingt-trois tests existants, et rappeler la norme R3 profil A déjà canonique.
- [x] 1.2 Créer les cinq artefacts autorisés en UTF-8/LF et réussir `openspec validate add-initial-feature-flag-definition-expiry --strict` et `openspec validate feature-flags --type spec --strict` avant tout code.

## 2. Gate et composition

- [x] 2.1 Étendre `src/pixs/kernel/feature_flags.py` par `validate_feature_flag_assignment_expiry(definition, context)` : types exacts avant tout accès, délégation à `validate_feature_flag_definitions` et `_validate_context`, refus de `expires_at <= as_of` par un diagnostic constant `feature_flags.expiry.expires_at` trié, dédupliqué et non échoé, comparaison par `datetime.fromisoformat` des horodatages déjà validés, aucun objet ni grammaire nouvelle et aucune horloge ; la consommer dans `evaluate_feature_flag_assignments_bounded` après les refus terminaux et le résolveur, sans jamais restituer la valeur d'un `SELECTED` sur définition expirée, en déléguant à `resolve_feature_flag_fallback(definition, use_kind, "STALE")` avec diagnostic d'expiration fusionné même sous `DEFAULT`, en forçant la cause `STALE` d'un `NO_MATCH` expiré et en utilisant `STALE` et le diagnostic d'expiration au lieu de `INVALID` lorsque la définition est expirée ; conserver terminal tout refus de types, validateurs, cohorte, prérequis, politique inconnue et ambiguïté même sur définition expirée ; corriger les docstrings de l'en-tête du module, de `FeatureFlagEvaluation` et de la fonction bornée, sans refactor, les autres primitives inchangées et `__all__` reçoit le seul export ajouté dans le même mandat du module.

## 3. Tests

- [x] 3.1 Étendre `tests/unit/test_feature_flag_evaluation_bounded.py` : bornes `expires_at` avant, égal et après l'instant injecté, équivalence `Z` et `+00:00` avec fractions de secondes, gate autonome retournant seulement des diagnostics et refusant sans décider une entrée invalide, matrice deux politiques par cinq usages sur définition expirée avec `False` et jeton `VARIANT` conservés par le repli `DEFAULT` et refus sans valeur ailleurs, refus terminal préservé pour cohorte, prérequis, politique héritée et candidats ambigus même expirés, objets hôtes et à hooks sans aucun callback, diagnostics triés, dédupliqués, stables sous permutation et double appel, sans écho et sans mutation des entrées, et les onze méthodes de test existantes inchangées.
- [x] 3.2 Étendre `tests/integration/test_feature_flag_evaluation_bounded_integration.py` : un nouvel enfant frais sous les douze gardes causales d'E/S et le finder bloquant Django/PostgreSQL réellement éprouvés avant import puis remis à zéro, appel réel de la gate et d'une évaluation bornée sur définition expirée constatant `SELECTED` refusé, repli `DEFAULT` sur `NON_SENSITIVE` et refus sensible, aucune horloge, base, réseau, environnement métier ni secret, marqueur final dédié.

## 4. Preuves

- [x] 4.1 Vérifier syntaxe minimum 3.12 et compilation des trois fichiers sous l'interpréteur DEVOPS, puis réussir les deux suites étendues et la régression des quatre-vingt-trois tests existants dans un environnement isolé explicite.
- [x] 4.2 Vérifier relecture byte-à-byte des classes, constantes, helpers, validateurs, résolveurs, repli et exports antérieurs, exactitude des seules docstrings locales corrigées, absence de modification hors de ces trois fichiers, UTF-8/LF et delta R3 MOTAMOT, en explicitant que l'admission complète, la provenance, la persistance, l'administration, l'audit, le cache, le cycle de vie, la purge, la cohorte et les prérequis restent non livrés.
- [x] 4.3 Réussir `openspec validate add-initial-feature-flag-definition-expiry --strict` et `openspec validate feature-flags --type spec --strict` après les preuves avant tout cochage, cocher uniquement les tâches réellement prouvées sous mandat distinct et vérifier les critères d'archivage sous contrôle CGPT.

Après achèvement prouvé des tâches : revalider le change en strict après cochage, puis archivage et `STATISTIQUES.md` sous deux mandats distincts. Le parent CISMP reste OPEN.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 4. Preuves ».

### O48-SL01 — Prouver périmètre CGPT, absence de change actif et baseline byte-à-byte des symboles R1, C1a, C2, R3 et de la composition bornée de `src/pixs/kernel/feature_flags.py`, des deux suites bornées et des quatre-vingt-trois tests existants, et rappeler la norme R3 profil A déjà canonique.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Préparation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O48-SL02 — Créer les cinq artefacts autorisés en UTF-8/LF et réussir `openspec validate add-initial-feature-flag-definition-expiry --strict` et `openspec validate feature-flags --type spec --strict` avant tout code.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Préparation », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O48-SL03 — Étendre `src/pixs/kernel/feature_flags.py` par `validate_feature_flag_assignment_expiry(definition, context)` : types exacts avant tout accès, délégation à `validate_feature_flag_definitions` et `_validate_context`, refus de `expires_at <= as_of` par un diagnostic constant `feature_flags.expiry.expires_at` trié, dédupliqué et non échoé, comparaison par `datetime.fromisoformat` des horodatages déjà validés, aucun objet ni grammaire nouvelle et aucune horloge ; la consommer dans `evaluate_feature_flag_assignments_bounded` après les refus terminaux et le résolveur, sans jamais restituer la valeur d'un `SELECTED` sur définition expirée, en déléguant à `resolve_feature_flag_fallback(definition, use_kind, "STALE")` avec diagnostic d'expiration fusionné même sous `DEFAULT`, en forçant la cause `STALE` d'un `NO_MATCH` expiré et en utilisant `STALE` et le diagnostic d'expiration au lieu de `INVALID` lorsque la définition est expirée ; conserver terminal tout refus de types, validateurs, cohorte, prérequis, politique inconnue et ambiguïté même sur définition expirée ; corriger les docstrings de l'en-tête du module, de `FeatureFlagEvaluation` et de la fonction bornée, sans refactor, les autres primitives inchangées et `__all__` reçoit le seul export ajouté dans le même mandat du module.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Gate et composition », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O48-SL04 — Étendre `tests/unit/test_feature_flag_evaluation_bounded.py` : bornes `expires_at` avant, égal et après l'instant injecté, équivalence `Z` et `+00:00` avec fractions de secondes, gate autonome retournant seulement des diagnostics et refusant sans décider une entrée invalide, matrice deux politiques par cinq usages sur définition expirée avec `False` et jeton `VARIANT` conservés par le repli `DEFAULT` et refus sans valeur ailleurs, refus terminal préservé pour cohorte, prérequis, politique héritée et candidats ambigus même expirés, objets hôtes et à hooks sans aucun callback, diagnostics triés, dédupliqués, stables sous permutation et double appel, sans écho et sans mutation des entrées, et les onze méthodes de test existantes inchangées.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Tests », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O48-SL05 — Étendre `tests/integration/test_feature_flag_evaluation_bounded_integration.py` : un nouvel enfant frais sous les douze gardes causales d'E/S et le finder bloquant Django/PostgreSQL réellement éprouvés avant import puis remis à zéro, appel réel de la gate et d'une évaluation bornée sur définition expirée constatant `SELECTED` refusé, repli `DEFAULT` sur `NON_SENSITIVE` et refus sensible, aucune horloge, base, réseau, environnement métier ni secret, marqueur final dédié.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Tests », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O48-SL06 — Vérifier syntaxe minimum 3.12 et compilation des trois fichiers sous l'interpréteur DEVOPS, puis réussir les deux suites étendues et la régression des quatre-vingt-trois tests existants dans un environnement isolé explicite.

- Ancien repère et tâche rattachée : tâche 4.1 ; section « 4. Preuves », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O48-SL07 — Vérifier relecture byte-à-byte des classes, constantes, helpers, validateurs, résolveurs, repli et exports antérieurs, exactitude des seules docstrings locales corrigées, absence de modification hors de ces trois fichiers, UTF-8/LF et delta R3 MOTAMOT, en explicitant que l'admission complète, la provenance, la persistance, l'administration, l'audit, le cache, le cycle de vie, la purge, la cohorte et les prérequis restent non livrés.

- Ancien repère et tâche rattachée : tâche 4.2 ; section « 4. Preuves », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O48-SL08 — Réussir `openspec validate add-initial-feature-flag-definition-expiry --strict` et `openspec validate feature-flags --type spec --strict` après les preuves avant tout cochage, cocher uniquement les tâches réellement prouvées sous mandat distinct et vérifier les critères d'archivage sous contrôle CGPT.

- Ancien repère et tâche rattachée : tâche 4.3 ; section « 4. Preuves », ligne 21 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
