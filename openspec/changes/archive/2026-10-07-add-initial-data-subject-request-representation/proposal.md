# Proposition — Représentation déclarative interne du DataSubjectRequest

## Why

L'exigence canonique « Demandes relatives aux données tracées » (openspec/specs/data-governance/spec.md) qualifie les demandes d'accès, d'export, de rectification, d'effacement et de restriction de commandes autorisées, auditées, idempotentes et propagées. Le vocabulaire des cinq opérations est livré et prouvé (`DataSubjectOperation`, change archivé `2026-10-06-add-initial-data-subject-request-operations-vocabulary`). Le grep ciblé de `src/pixs/kernel` (`DataSubjectRequest|legal_hold`) n'expose aucune représentation de la demande elle-même. TECHNICAL.md §14.6 en fournit la structure en onze champs (après séparation de `tenant_id` et `scope_id`), dont cinq marqués « éventuels » ; cette structure de cadrage n'a pas la force normative RFC 2119, le delta ci-joint restant mot pour mot canonique. Cette unité fournit une forme interne fermée pour les consommateurs futurs ; aucun consommateur de DataSubjectRequest n'est observé actuellement.

## What Changes

- Publier `src/pixs/kernel/data_subject_request.py` : dataclass `frozen` interne `DataSubjectRequest` à onze champs dans l'ordre de TECHNICAL §14.6, tous exigés au constructeur sans défaut, et validateur structurel `validate_data_subject_request` retournant des diagnostics fixes, triés, dédupliqués, sans écho des valeurs, selon le patron `data_governance_profile.py` ;
- Publier un test unitaire d'adhésion et un test d'intégration d'import en processus frais `-I -B` sous gardes finies réutilisées ;
- Aucun fichier existant modifié, aucune façade ni `__init__` touché ;
- Delta MODIFIED reproduisant mot pour mot l'exigence et son scénario canoniques, sans aucune norme nouvelle.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `data-governance` : delta identique de la seule exigence « Demandes relatives aux données tracées », sans changement normatif ; archive attendue sans opération sur les specs.

## Impacts

Aucun fichier existant ni façade modifiés ; trois fichiers nouveaux seulement. Représentation déclarative interne et partielle : elle ne prouve ni la publication de la demande, ni son autorisation, son audit, son idempotence, sa propagation, le respect des holds et de la rétention, ni aucun runtime ; le scénario « Effacement propagé » n'est pas couvert par cette unité. Le type `str | None` des cinq champs éventuels signifie uniquement « champ non fourni », jamais l'absence d'un hold, d'une obligation ou d'une autorisation. Aucun héritage, aucune exécution de Command, aucun comportement d'autorisation, d'audit, de propagation ou de hold ajouté.
