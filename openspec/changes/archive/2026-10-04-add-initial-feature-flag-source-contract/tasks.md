# Tasks

## 1. Préparation

- [x] 1.1 Confirmer périmètre, absence de change actif, 22 baselines, 119 tests et normes R2/R4 ; publier les cinq artefacts puis réussir les stricts avant code.

## 2. Contrat

- [x] 2.1 Ajouter `FeatureFlagSourceSnapshot` à quatre champs figés et son validateur avec les validateurs existants, liaisons exactes, règle unique par clé et refus de toute règle non référencée.
- [x] 2.2 Ajouter `evaluate_feature_flag_source_snapshot` : types et version fermés, lookup exact, extraction complète des affectations, appel réel à `evaluate_feature_flag_assignments_with_cohort` sans projection ni repli inventé.

## 3. Tests

- [x] 3.1 Créer la suite unitaire causale : lot vide valide, définition ou règle manquantes, affectation hors flag, selector non déclaré, versions divergentes, règles hôtes partagées, liaisons incohérentes, entrées hostiles sans callback, non-mutation et absence d'écho.
- [x] 3.2 Créer l'intégration fraîche sans I/O réelle : finder et gardes éprouvés avant import, appel de composition réel, comptes zéro après usages, aucune horloge, base, réseau ou secret.

## 4. Preuves

- [x] 4.1 Réussir les compilations des trois sources, syntaxe minimum 3.12, nouvelles suites et les 119 régressions dans un environnement explicite.
- [x] 4.2 Vérifier les 22 baselines inchangées, le delta R2/R4 recopié mot pour mot, UTF-8/LF, limites de provenance et absence de persistance livrée.
- [x] 4.3 Réussir les stricts du change et canonique après preuves, cocher uniquement les huit tâches sous mandat distinct, puis faire contrôler l'archivage par CGPT.
