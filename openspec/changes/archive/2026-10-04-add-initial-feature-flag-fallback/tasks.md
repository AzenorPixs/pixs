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
