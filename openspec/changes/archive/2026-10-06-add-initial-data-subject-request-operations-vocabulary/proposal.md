# Proposition — Vocabulaire Enum des opérations de demande relative aux données

## Why

L'exigence canonique « Demandes relatives aux données tracées » (openspec/specs/data-governance/spec.md) énumère cinq demandes — accès, export, rectification, effacement, restriction — comme commandes autorisées, auditées, idempotentes et propagées. TECHNICAL.md §14.6 fournit les identifiants anglais exacts `ACCESS`, `EXPORT`, `RECTIFY`, `ERASE`, `RESTRICT`. Le grep ciblé de `src/pixs` (`DataSubject|RECTIFY|data_subject`) n'expose aucune représentation. Ce vocabulaire fournira une référence commune aux futurs consommateurs.

## What Changes

- Publier `src/pixs/kernel/data_subject_operations.py` : `DataSubjectOperation(Enum)` à cinq membres, noms et valeurs textuels exacts dans l'ordre canonique `ACCESS`, `EXPORT`, `RECTIFY`, `ERASE`, `RESTRICT`, sur le patron `JobState(Enum)` et celui des classifications livrées ;
- Publier un test unitaire d'adhésion du vocabulaire et un test d'intégration d'import en processus frais `-I -B` sous gardes réutilisées ;
- Aucun fichier existant modifié, aucune façade ni `__init__` touché ;
- Delta MODIFIED reproduisant mot pour mot l'exigence et son scénario canoniques, sans changement normatif.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `data-governance` : delta identique de la seule exigence « Demandes relatives aux données tracées », sans changement normatif ; archive attendue sans opération sur les specs.

## Impacts

Fondation partielle : représente le vocabulaire fermé des opérations, ne clôture pas l'exigence « Demandes relatives aux données tracées ». L'autorisation, l'audit, l'idempotence, la propagation, les holds, la rétention, le `status`, le runtime, la base et le consentement juridique ne sont ni ajoutés ni revendiqués ; le scénario « Effacement propagé » n'est pas transformé en promesse du vocabulaire. Aucune valeur par défaut, alias, constructeur, wrapper, parseur ni export de variante.
