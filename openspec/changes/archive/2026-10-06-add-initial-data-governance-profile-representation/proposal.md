# Proposition — Représentation déclarative interne du DataGovernanceProfile

## Why

L'exigence canonique « Profil de gouvernance versionné par composant » (openspec/specs/data-governance/spec.md) impose à chaque composant qui introduit, dérive ou transfère des données de publier un profil versionné énumérant propriétaire, source de vérité, classes, confidentialité, données personnelles, finalités, rétention, suppression, consommateurs, processeurs, contraintes de résidence ou transfert, export et lignée. TECHNICAL.md §14.5 en donne la structure à quinze champs. Le Kernel ne contient aucune représentation de ce profil : le grep ciblé de `src/pixs/kernel` (`DataGovernanceProfile|profile_version|source_of_truth`) n'expose que des concepts d'autres domaines (capabilities, contracts, feature flags). Les deux Enum de classification livrées par le change archivé `2026-10-06-add-initial-data-classification-vocabulary` représentent les dimensions de confidentialité et de données personnelles, mais ne fondent aucune structure de profil. Sans représentation unique et fermée, chaque consommateur reproduirait le profil par chaînes libres, source de divergences silencieuses.

## What Changes

- Ajouter `src/pixs/kernel/data_governance_profile.py` : dataclass `frozen` interne `DataGovernanceProfile` aux quinze champs obligatoires de TECHNICAL §14.5 dans l'ordre de la source, et validateur structurel `validate_data_governance_profile` retournant des diagnostics fixes, triés et dédupliqués, sans écho des valeurs, selon le patron `notification_contract.py`/`event_contract.py`/`audit_event.py` ;
- Ajouter un test unitaire et un test d'intégration en processus frais ;
- Delta `specs/data-governance/spec.md` MODIFIED reproduisant mot pour mot l'exigence « Profil de gouvernance versionné par composant » et son scénario canoniques, sans aucune norme nouvelle.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `data-governance` : delta identique de la seule exigence « Profil de gouvernance versionné par composant », sans changement normatif ; archive attendue sans opération sur les specs.

## Impact

Aucun fichier existant ni façade modifiés ; trois fichiers nouveaux seulement. Représentation déclarative interne et partielle : elle ne prouve ni la publication effective du profil par chaque composant, ni activation, politique effective de rétention/suppression/export, autorité de la source de vérité, règle d’exposition/export, DataSubjectRequest, audit ni runtime. Le scénario « Flux sortant sans consommateur refusé » appartient à l’exigence « Profil de gouvernance versionné par composant » et reste hors de cette unité ; l’exigence « Classification restrictive par défaut » reste également non close.
