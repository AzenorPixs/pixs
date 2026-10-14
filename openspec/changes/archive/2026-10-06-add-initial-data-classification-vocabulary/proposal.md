# Proposition — Vocabulaire Enum des classifications de gouvernance des données

## Why

L'exigence canonique « Classification restrictive par défaut » (openspec/specs/data-governance/spec.md) énonce deux dimensions fermées et orthogonales : confidentialité `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` et données personnelles `NONE`, `PERSONAL`, `SENSITIVE_PERSONAL`. Le grep ciblé de `src/pixs/kernel` (`governance|confidentiality|personal_data`) n'expose aucune représentation. Sans source unique, chaque consommateur reproduirait ces valeurs par chaînes libres, source de divergences silencieuses.

## What Changes

- Publier `src/pixs/kernel/data_governance.py` : deux `Enum` standards, `ConfidentialityLevel` (quatre membres) et `PersonalDataLevel` (trois membres), noms et valeurs textuels exacts dans l'ordre de la source canonique, sur le patron observé de `JobState(Enum)` de `kernel/jobs.py` ;
- Publier un test unitaire d'adhésion du vocabulaire et un test d'intégration d'import en processus frais `-I -B` sans effet ;
- Aucun fichier existant modifié, aucune façade ni `__init__` touché ; aucune logique d'export, de refus ou de classification dans ce change ;
- Delta MODIFIED reproduisant mot pour mot la requirement et son scénario canoniques, sans changement normatif.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `data-governance` : delta identique de la seule exigence « Classification restrictive par défaut », sans changement normatif ; archive attendue sans opération sur les specs.

## Impacts

Fondation partielle : représente les deux dimensions de classification, ne clôture pas l'exigence « Classification restrictive par défaut ». Aucun défaut, alias, seuil ou ordre de sévérité, factory, convertisseur, validateur, donnée métier, ni prétention à une immutabilité profonde.
