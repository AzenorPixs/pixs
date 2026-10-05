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
