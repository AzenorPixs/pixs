# Proposition — Représentation déclarative interne d'une déclaration de flux sortant

## Why

L'exigence canonique « Profil de gouvernance versionné par composant »
(openspec/specs/data-governance/spec.md) publie le scénario « Flux sortant sans
consommateur refusé » : « WHEN un transfert déclare une destination sans
consommateur ni garantie documentée THEN le flux est refusé avant activation ».
Le profil versionné est représenté et validé (DataGovernanceProfile, change
archivé 2026-10-06-add-initial-data-governance-profile-representation). Un grep
ciblé de src/pixs/kernel ne montre aucune déclaration de flux sortant ni porte
structurelle correspondant au scénario. TECHNICAL.md §14.5 décrit le besoin en
termes non normatifs ; seul le scénario canonique fonde cette unité.

## What Changes

- Publier `src/pixs/kernel/data_outbound_declaration.py` : dataclass `frozen`
  interne `DataOutboundDeclaration` à trois champs (`destination_reference: str`,
  `consumer_reference: str | None`, `guarantee_reference: str | None`), sans
  défaut, et validateur structurel `validate_data_outbound_declaration` selon
  les patrons `_refusal`/`_pack` prouvés ;
- Le seul refus propre au scénario porte sur l'absence conjointe
  (`consumer_reference` ET `guarantee_reference` à `None` exact) ; aucune
  obligation de présence séparée n'est introduite ;
- Publier un test unitaire d'adhésion et un test d'intégration d'import en
  processus frais `-I -B` sous gardes finies réutilisées ;
- Aucun fichier existant modifié, aucune façade touchée ;
- Delta MODIFIED reproduisant mot pour mot l'exigence R1 et son unique scénario
  canonique, sans aucune norme nouvelle.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `data-governance` : delta identique de la seule exigence « Profil de
  gouvernance versionné par composant », sans changement normatif ; archive
  attendue sans opération sur les specs.

## Impacts

Trois fichiers nouveaux seulement. Refus structurel au niveau déclaration :
cette unité ne prouve ni l'activation refusée, ni la destination autorisée, ni
l'existence réelle d'une garantie ou d'un consommateur, ni l'audit, ni aucun
runtime ; le THEN « refusé avant activation » n'est pas couvert. Pas de
`ConfidentialityLevel` dans le contrat ; aucun lien ajouté au profil ; les
références restent opaques, sans normalisation ni interprétation.
