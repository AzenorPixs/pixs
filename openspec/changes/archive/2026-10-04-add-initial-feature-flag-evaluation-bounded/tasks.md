# Tasks

## 1. Préparation

- [x] 1.1 Prouver périmètre CGPT, absence de change actif et baseline byte à byte des éléments R1, C1a, C2 et R3 de `src/pixs/kernel/feature_flags.py` ainsi que des huit fichiers de suites existantes, puis consigner la collecte initiale.
- [x] 1.2 Créer les cinq artefacts autorisés en UTF-8/LF et réussir `openspec validate add-initial-feature-flag-evaluation-bounded --strict` et `openspec validate feature-flags --type spec --strict` avant tout code.

## 2. Appendice du module

- [x] 2.1 Étendre seulement `src/pixs/kernel/feature_flags.py` par un appendice isolé : `FeatureFlagEvaluation` frozen à trois champs obligatoires sans défaut et fonction pure `evaluate_feature_flag_assignments_bounded` à quatre paramètres requis, fermant les types par identité exacte avant tout accès, itération, comparaison ou hachage, déléguant aux validateurs et helpers existants, refusant une configuration avec `cohort_key` déclarée ou prérequis non vide sans `DEFAULT`, appliquant la gate de politique hors `DENY`/`DEFAULT` avant toute valeur, composant `resolve_feature_flag_assignment` sans le modifier, classant `STALE` seulement sur identité exacte et `valid_until <= as_of`, `ABSENT` sinon, déléguant le repli à `resolve_feature_flag_fallback`, et ne lisant aucun texte de diagnostic humain ; aucune horloge, E/S, persistance, cohorte, prérequis, décision d'expiration ni permission.

## 3. Tests

- [x] 3.1 Créer `tests/unit/test_feature_flag_evaluation_bounded.py` : politique inconnue refusée avant toute valeur même pour un candidat valide, `SELECTED` conservé pour un usage sensible valide avec `False` et jeton `VARIANT` intacts et jamais tenu pour permission, `STALE` sur `valid_until <= as_of`, `ABSENT` sur `as_of < valid_from` et sur absence d'identité, lot mixte expiré et futur traité `STALE` à repli identique, `INVALID` atteint uniquement par le champ machine connu du résolveur et jamais par un contournement, entrées invalides et ambiguïtés en refus terminal sans repli, types hostiles sans callback ni `getattr`, diagnostics triés, dédupliqués, sans écho et indépendants de l'ordre, immutabilité, champs obligatoires et absence de défaut.
- [x] 3.2 Créer `tests/integration/test_feature_flag_evaluation_bounded_integration.py` : import d'un enfant frais sous gardes causales d'E/S et finder bloquant Django/PostgreSQL réellement éprouvés avant import puis remis à zéro, exécution réelle de la composition sur une définition témoin sans cohorte ni prérequis, cas dynamique unique `SELECTED` sensible et `STALE` replié, refus hostile avant tout effet, marqueur final dédié, périmètre sans Django, PostgreSQL, réseau, environnement métier ni secret.

## 4. Preuves

- [x] 4.1 Vérifier syntaxe minimum 3.12 et compilation des trois fichiers sous l'interpréteur DEVOPS, puis réussir les deux suites nouvelles et la régression des soixante et onze tests existants dans un environnement explicite isolé.
- [x] 4.2 Vérifier relecture byte-exacte des classes, constantes, helpers, validateurs, résolveurs et exports antérieurs, absence de modification hors de ces trois fichiers, conservation de l'API du résolveur existant, UTF-8/LF et deltas R2 et R3 MOTAMOT avec les quatre scénarios existants, en explicitant que la cohorte, les prérequis, l'expiration et le cycle de vie de la définition, la persistance, l'administration, le cache, l'audit, la provenance de l'appelant et les garanties globales R2 et R3 restent non livrés.
- [x] 4.3 Réussir `openspec validate add-initial-feature-flag-evaluation-bounded --strict` et `openspec validate feature-flags --type spec --strict` après les preuves avant tout cochage, cocher uniquement les tâches réellement prouvées sous mandat distinct, et vérifier les critères d'archivage sous contrôle CGPT.

Après cochage contrôlé : revalider le change en strict, puis archivage et `STATISTIQUES.md` sous mandats distincts. Le parent CISMP reste OPEN.
