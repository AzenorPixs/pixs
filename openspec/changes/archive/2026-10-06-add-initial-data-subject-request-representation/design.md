# Conception — Représentation déclarative interne du DataSubjectRequest

## Contexte

Source canonique de la légitimité : `openspec/specs/data-governance/spec.md`, exigence « Demandes relatives aux données tracées ». Structure descriptive : TECHNICAL.md §14.6 (arborescence à onze entrées après séparation de `tenant_id / scope_id`), sans force normative RFC 2119. Dépendance prouvée : `DataSubjectOperation` de `src/pixs/kernel/data_subject_operations.py` (cinq membres canoniques, testés). Patron de validateur : `src/pixs/kernel/data_governance_profile.py` (garde de type exact, diagnostics `VALIDATE` fixes, `_pack` trié/dédupliqué). Décision CGPT : `src/pixs/kernel/data_subject_request.py`, sans modification de façade.

## Forme livrée

Dataclass `frozen=True` à onze champs obligatoires au constructeur, dans l'ordre de §14.6 : `request_id: str`, `operation: DataSubjectOperation`, `subject_reference: str`, `tenant_id: str | None`, `scope_id: str | None`, `requested_by: str`, `status: str`, `policy_version: str`, `operation_id: str | None`, `legal_hold_decision: str | None`, `result_reference: str | None`. Aucun défaut, sans `__post_init__`, sans méthode ; constructeur structurellement permissif, `validate_data_subject_request(candidate)` seul point fermé, retournant une liste de `Diagnostic` (`VALIDATE`, patron `data_governance_profile.py`) dédupliquée et triée, à messages fixes sans écho. `__all__ = ["DataSubjectRequest", "validate_data_subject_request"]`.

## Règles de validation

- `candidate` de type exact différent de `DataSubjectRequest` : refus unique avant tout `getattr` et sans aucun appel de méthode d'un objet hostile ;
- six champs requis : `operation` contrôlée comme membre canonique `DataSubjectOperation` par identité `is` ; `request_id`, `subject_reference`, `requested_by`, `status`, `policy_version` : `str` de type exact non vide, chaînes opaques, conservées sans normalisation, strip ni grammaire ; `policy_version` sans contrainte SemVer ;
- cinq champs éventuels (`tenant_id`, `scope_id`, `operation_id`, `legal_hold_decision`, `result_reference`) : `None` exact (signifie uniquement « champ non fourni » — jamais l'absence d'un hold, d'une obligation ou d'une autorisation) ou `str` de type exact non vide ; sous-classes, bool, int refusés ;
- aucune appartenance, comparaison ou message n'invoque les dunder d'une valeur non validée.

## Décisions

- Décision CGPT explicite (choix B) : onze champs présents, les cinq « éventuels » typés `str | None`, aucun défaut, absence fournie explicitement par `None` ;
- Correction consignée : la règle « quinze champs obligatoires, aucun None » du change archivé `2026-10-06-add-initial-data-governance-profile-representation` était propre à l'exigence de profil, qui impose la publication de chaque item ; elle ne constitue pas une interdiction générale de `None` et ne s'applique pas aux champs que §14.6 déclare éventuels ;
- `None` n'est jamais interprété : aucune lecture de sens (« aucun hold », « non autorisé », etc.) ne peut en être déduite par cette unité ;
- Réutilisations sans modification : `DataSubjectOperation`, `Diagnostic`/`VALIDATE` ; aucune importation de `pixs.core`, aucune dépendance nouvelle ;
- Représentation interne et partielle : ni contrat enregistré, ni wire format, ni exécution ; fichiers et façade des changes archivés inchangés octet à octet ;
- Régression bornée justifiée (module isolé, importé par aucun existant) : dépendance directe et patrons voisins, pas de liste étendue sans lien.

## Critères observables

Instance valide complète (éventuels à `None` explicites) : liste de diagnostics vide, ordre trié déterministe ; chaque refus : un `Diagnostic` par champ fautif (`data_subject_request.<champ>`), message fixe, sans reproduction d'aucune valeur ; `None` admis exactement pour les cinq éventuels, refusé pour les six requis ; sous-classes de `str`, bool, int, éléments hostiles refusés sans invocation de dunder ; export exactement `["DataSubjectRequest", "validate_data_subject_request"]` ; import et appels du validateur sans aucun effet observable sur les surfaces gardées ; ces gardes finies ne constituent pas une preuve universelle d'absence d'effets.

## Validation prévue (décision technique root explicite pour CE change)

- `openspec validate` strict du change et de la spec `data-governance` : exit 0 obligatoire, avant le code puis après les tests ;
- Contrôles globaux `--specs --strict --json --report findings` et `--all --strict --json --report findings` : sorties brutes et codes réels consignés à chaque passe ; qualification admise seulement si exit natif réellement 1, couverture complète (76 specs / 77 items), identité exacte des issues de la table validée de l'archive `2026-10-06-add-initial-notification-contract-representation` (19 WARNING de longueur, mêmes emplacements et textes), zéro ERROR et aucun autre texte ou emplacement, et baseline de référence inchangée ; toute ERROR, tout autre WARNING, emplacement ou texte, toute divergence d'empreinte ou couverture incomplète suspend le mandat et déclenche la reprise obligatoire CISMP, sans clôture terminale automatique ;
- Compilations ciblées des trois nouveaux fichiers, résultats natifs ;
- Tests unitaire et d'intégration (processus frais `-I -B`, environnement réduit, gardes finies d'effets réutilisées, marqueur `DATA_SUBJECT_REQUEST_SAFE_INTEGRATION_OK` seul sur stdout, quatre assertions finales hors `with`, sans nouvelle dépendance) ;
- Régression bornée : `tests/unit/test_data_subject_operations_vocabulary.py` (dépendance directe), `tests/unit/test_data_governance_profile.py` (patron de validateur et spec partagés), `tests/integration/test_kernel_purity.py` et `tests/integration/test_public_api_facades.py` (garde de pureté et de façade bornée pour tout module ajouté au Kernel) ;
- UTF-8/LF des trois nouveaux fichiers et empreintes des fichiers non concernés.

## Non-goal

Aucune exécution, file, autorisation, audit, idempotence, propagation, hold, rétention, politique juridique, région, base, runtime ni immutabilité profonde ; aucune interprétation de `None`, du `status`, de `policy_version` ou de `legal_hold_decision`.
