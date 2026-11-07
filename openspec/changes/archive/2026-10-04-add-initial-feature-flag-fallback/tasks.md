# Tasks

## 1. Préparation

- [x] 1.1 Prouver périmètre CGPT, absence de change actif et baseline byte à byte des éléments R1, C1a et C2 du module `src/pixs/kernel/feature_flags.py` ainsi que des suites existantes, puis consigner la collecte initiale.
- [x] 1.2 Créer les cinq artefacts autorisés en UTF-8/LF et réussir `openspec validate add-initial-feature-flag-fallback --strict` et `openspec validate feature-flags --type spec --strict` avant tout code.

## 2. Appendice du module

- [x] 2.1 Étendre seulement `src/pixs/kernel/feature_flags.py` par un appendice isolé : `FeatureFlagFallback` frozen à trois champs obligatoires sans défaut, domaines privés fermés `use_kind` et `failure_kind`, fonction pure `resolve_feature_flag_fallback` réutilisant `validate_feature_flag_definitions`, `_is_bare_reference` et `_evaluation_diagnostics`, sans duplication de grammaire, sans horloge, sans E/S, sans persistance, sans résolution de candidat, sans cohorte ni prérequis ; conserver les classes, constantes, helpers, validateurs et exports antérieurs, `__all__` relevant d'un mandat distinct.

## 3. Tests

- [x] 3.1 Créer `tests/unit/test_feature_flag_fallback.py` : matrice des usages et des échecs reconnus, `DENY` refusé sans valeur avec diagnostics pouvant rester vides, `DEFAULT` sur `NON_SENSITIVE` appliquant la `default_value` avec `False` et jeton `VARIANT` conservés, usage sensible refusé quelle que soit la politique, référence opaque héritée inconnue ou incompatible refusée sans alias, valeurs et types hostiles fermés sans callback ni écho, diagnostics triés, dédupliqués et indépendants de l'ordre, champs obligatoires et immutabilité, absence de défaut et de champ inconnu accepté.
- [x] 3.2 Créer `tests/integration/test_feature_flag_fallback_integration.py` : import d'un enfant frais sous gardes causales d'E/S et finder bloquant Django/PostgreSQL réellement éprouvés avant import puis remis à zéro, exécution réelle de la primitive sur une définition témoin, refus d'un usage et d'un échec inconnus avant tout effet, marqueur final dédié, périmètre sans Django, PostgreSQL, réseau, environnement métier ni secret.

## 4. Preuves

- [x] 4.1 Vérifier syntaxe minimum 3.12 et compilation des trois fichiers sous l'interpréteur DEVOPS, puis réussir les deux suites nouvelles et la régression des soixante et un tests existants dans un environnement explicite isolé.
- [x] 4.2 Vérifier relecture byte-exacte des classes, constantes, helpers, validateurs et exports antérieurs, conservation du validateur structurel R1 sans restriction nouvelle, absence de modification hors de ces trois fichiers, UTF-8/LF et delta R3 MOTAMOT, en explicitant que la détection d'échec, la classification, la réévaluation par le frontal, la cohorte, les prérequis, la persistance, l'administration, l'audit et le cycle de vie restent non livrés.
- [x] 4.3 Réussir `openspec validate add-initial-feature-flag-fallback --strict` et `openspec validate feature-flags --type spec --strict` après les preuves avant tout cochage, cocher uniquement les tâches réellement prouvées sous mandat distinct et vérifier les critères d'archivage sous contrôle CGPT.

Après achèvement prouvé des tâches : archivage puis `STATISTIQUES.md` sous deux mandats distincts. Le parent CISMP reste OPEN.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 4. Preuves ».

### O50-SL01 — Prouver périmètre CGPT, absence de change actif et baseline byte à byte des éléments R1, C1a et C2 du module `src/pixs/kernel/feature_flags.py` ainsi que des suites existantes, puis consigner la collecte initiale.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Préparation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O50-SL02 — Créer les cinq artefacts autorisés en UTF-8/LF et réussir `openspec validate add-initial-feature-flag-fallback --strict` et `openspec validate feature-flags --type spec --strict` avant tout code.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Préparation », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O50-SL03 — Étendre seulement `src/pixs/kernel/feature_flags.py` par un appendice isolé : `FeatureFlagFallback` frozen à trois champs obligatoires sans défaut, domaines privés fermés `use_kind` et `failure_kind`, fonction pure `resolve_feature_flag_fallback` réutilisant `validate_feature_flag_definitions`, `_is_bare_reference` et `_evaluation_diagnostics`, sans duplication de grammaire, sans horloge, sans E/S, sans persistance, sans résolution de candidat, sans cohorte ni prérequis ; conserver les classes, constantes, helpers, validateurs et exports antérieurs, `__all__` relevant d'un mandat distinct.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Appendice du module », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O50-SL04 — Créer `tests/unit/test_feature_flag_fallback.py` : matrice des usages et des échecs reconnus, `DENY` refusé sans valeur avec diagnostics pouvant rester vides, `DEFAULT` sur `NON_SENSITIVE` appliquant la `default_value` avec `False` et jeton `VARIANT` conservés, usage sensible refusé quelle que soit la politique, référence opaque héritée inconnue ou incompatible refusée sans alias, valeurs et types hostiles fermés sans callback ni écho, diagnostics triés, dédupliqués et indépendants de l'ordre, champs obligatoires et immutabilité, absence de défaut et de champ inconnu accepté.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Tests », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O50-SL05 — Créer `tests/integration/test_feature_flag_fallback_integration.py` : import d'un enfant frais sous gardes causales d'E/S et finder bloquant Django/PostgreSQL réellement éprouvés avant import puis remis à zéro, exécution réelle de la primitive sur une définition témoin, refus d'un usage et d'un échec inconnus avant tout effet, marqueur final dédié, périmètre sans Django, PostgreSQL, réseau, environnement métier ni secret.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Tests », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O50-SL06 — Vérifier syntaxe minimum 3.12 et compilation des trois fichiers sous l'interpréteur DEVOPS, puis réussir les deux suites nouvelles et la régression des soixante et un tests existants dans un environnement explicite isolé.

- Ancien repère et tâche rattachée : tâche 4.1 ; section « 4. Preuves », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O50-SL07 — Vérifier relecture byte-exacte des classes, constantes, helpers, validateurs et exports antérieurs, conservation du validateur structurel R1 sans restriction nouvelle, absence de modification hors de ces trois fichiers, UTF-8/LF et delta R3 MOTAMOT, en explicitant que la détection d'échec, la classification, la réévaluation par le frontal, la cohorte, les prérequis, la persistance, l'administration, l'audit et le cycle de vie restent non livrés.

- Ancien repère et tâche rattachée : tâche 4.2 ; section « 4. Preuves », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O50-SL08 — Réussir `openspec validate add-initial-feature-flag-fallback --strict` et `openspec validate feature-flags --type spec --strict` après les preuves avant tout cochage, cocher uniquement les tâches réellement prouvées sous mandat distinct et vérifier les critères d'archivage sous contrôle CGPT.

- Ancien repère et tâche rattachée : tâche 4.3 ; section « 4. Preuves », ligne 21 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
