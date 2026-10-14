# Conception — Représentation déclarative interne du DataGovernanceProfile

## Forme livrée

Module interne séparé `src/pixs/kernel/data_governance_profile.py`, stdlib seule, sans I/O ni mutation. `DataGovernanceProfile` : dataclass `frozen=True` à quinze champs obligatoires dans l'ordre de TECHNICAL §14.5 — `profile_version`, `data_asset_id`, `owner_component`, `source_of_truth`, `data_classes`, `confidentiality`, `personal_data`, `purpose_refs`, `retention_policy`, `deletion_policy`, `residency_constraints`, `authorized_consumers`, `processor_refs`, `export_policy`, `lineage` — sans défaut, sans `__post_init__`, sans méthode applicative ; constructeur structurellement permissif, validateur `validate_data_governance_profile(candidate)` seul point fermé, retournant une liste de `Diagnostic` (`VALIDATE`, patron `notification_contract.py`) dédupliquée et triée, à messages fixes sans écho. `__all__ = ["DataGovernanceProfile", "validate_data_governance_profile"]`.

## Règles de validation

- `candidate` de type exact différent de `DataGovernanceProfile` : refus unique avant tout `getattr` et sans aucun appel de méthode d'un objet hostile ;
- `profile_version` : `str` de type exact non vide accepté par le `parse_version` SemVer existant (`pixs.kernel.manifest.semver`) ;
- cinq collections `data_classes`, `purpose_refs`, `residency_constraints`, `authorized_consumers`, `processor_refs` : `frozenset` de type exact, chaque élément `str` de type exact non vide ; sous-classes refusées ; **l'ensemble vide est explicitement admis**, sans permission ni obligation déduites ;
- `confidentiality` et `personal_data` : membres canoniques contrôlés par identité `is` (Enum livrés de `data_governance.py`) ;
- sept références opaques `data_asset_id`, `owner_component`, `source_of_truth`, `retention_policy`, `deletion_policy`, `export_policy`, `lineage` : `str` de type exact non vide, références fournies par un caller trusted ; aucune normalisation, résolution, interprétation de région ou de garantie ;
- aucun helper privé de `capabilities` ou `manifest` n'est emprunté pour imposer une grammaire de domaine ; aucune appartenance ou message n'invoque les dunder d'une valeur non validée.

## Décisions

- Décision root explicite : les quinze champs sont obligatoires dans la représentation, aucun défaut, aucun champ omis ; les « éventuelles » de TECHNICAL portent sur l'existence de déclarations (processeurs, contraintes), non sur la présence des champs ; aucune valeur `None` ni sémantique d'absence inventée ;
- `profile_version` validée par SemVer via le parseur existant : choix technique root distinct d'une garantie normative de la spec ;
- Réutilisations sans modification : `ConfidentialityLevel`/`PersonalDataLevel`, `parse_version`, `Diagnostic`/`VALIDATE` ; aucune importation de `pixs.core` ;
- Représentation interne et partielle : ni `ContractDescriptor`, ni contrat enregistré, ni wire format ; fichiers source, tests et façade des changes archivés restent inchangés octet à octet.

## Critères observables

- Instance valide complète : diagnostics vides, ordre de collecte trié déterministe ;
- Chaque champ fautif : un `Diagnostic` à message fixe (`data_governance_profile.<champ>`), sans reproduction d'aucune valeur ;
- Cinq ensembles vides acceptés sans diagnostic ; sous-classes, bool, int et éléments hétérogènes refusés avant tout contrôle d'appartenance ; deux dimensions par identité stricte ;
- Export exactement `["DataGovernanceProfile", "validate_data_governance_profile"]` ;
- Import du module et appels du validateur sans aucun effet observable (écriture, réseau, process, environnement, base).

## Validation prévue (décision technique root explicite pour CE change)

- `openspec validate` strict du change et de la spec `data-governance` : exit 0 obligatoire, avant le code puis après les tests ;
- Globals `--specs --strict` et `--all --strict --json --report findings` : sorties brutes et codes réels consignés ; qualification admise **seulement** si les findings sont exactement les 19 WARNING de longueur de la table validée de l'archive `2026-10-06-add-initial-notification-contract-representation`, mêmes emplacements et textes, et si les 76 specs canoniques restent identiques à leurs empreintes de référence avant code ; toute ERROR, tout autre WARNING, emplacement ou texte, toute couverture incomplète ou divergence d'empreinte bloque ;
- Compilations ciblées des trois nouveaux fichiers, résultats natifs ;
- Tests unitaire et d'intégration (processus frais `-I -B`, environnement réduit, gardes finies d'effets réutilisées, marqueur fixe, aucune nouvelle dépendance) ;
- Régression ciblée : familles vocabulaire (`data_governance`, `job_state`, `notification_channel`, `notification_delivery_state`) et patrons de contrat (`notification_contract`, `event_contract`, `audit_event`), gardes `kernel_purity` et `public_api_facades` ;
- UTF-8/LF des trois nouveaux fichiers et empreintes des fichiers non concernés.

## Non-goal

Aucune politique, provider, autorité, exposition, export, activation, audit, persistance, normalisation, résolution ni exécution ; la façade du Kernel n'est pas modifiée.
