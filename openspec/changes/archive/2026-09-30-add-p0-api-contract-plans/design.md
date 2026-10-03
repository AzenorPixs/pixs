# Design — add-p0-api-contract-plans

## Modèle
- `ApiContractPlan` : dataclass frozen, EXACTEMENT 2 champs :
  `contract: ContractDescriptor` (catégorie API stricte) et
  `openapi_document_ref: str` (référence LOGIQUE publique du document).
- Le constructeur valide les 2 champs dans `__post_init__` ; toute
  entrée invalide lève `ApiContractPlanError`.
- `ApiContractPlanError(ValueError)` : diagnostics constants, sans écho
  de valeurs brutes, levée avec `from None`.
- Les gardes revalident les types exacts des 2 champs via
  `object.__getattribute__` APRÈS contrôle de type (`type(x) is Y`) :
  forgeries, sous-classes hostiles, getters/`__repr__`/coercitions
  hostiles et champs manquants (enveloppés en constante, `from None`)
  sont rejetés. Aucune coercition, aucun accès par attribut direct
  avant typecheck.
- Les erreurs publiques de `ContractDescriptor`, `require_category` et
  `check_evolution` sont encapsulées en `ApiContractPlanError`
  (`from None`) ; le `TypeError` standard de signature reste natif.
- `openapi_document_ref` : `str` exact, identifiant nu vérifié par
  `parse_requirement` publique avec contraintes VIDES et
  `target_id == valeur` (aucune conversion, aucune regex privée).
  Référence LOGIQUE publique : ne prouve aucun fichier, schéma ou
  publication. Ni fichier, ni URL, ni I/O.

## Gardes (pure metadata, sans I/O)
- `api_major_prefix(plan: object) -> str` : revalide le plan
  (types exacts des 2 champs), parse le texte de version SemVer
  COMPLET via `parse_version` partagée (majeure 0 permise,
  préversions et build valides selon SemVer), retourne
  `/api/v{major}`. La version API est SemVer et indépendante des
  versions runtime et de toute version de schéma OpenAPI ; les
  préfixes `/api/v0...` sont valables, préversions/builds inclus.
- `check_api_evolution(previous: object, proposed: object, *,
  breaking: bool, coexistence_doc: object) -> str` : revalide les
  deux plans et leurs descripteurs (types exacts, forgeries
  rejetées) ; `breaking` doit être `type is bool`.
- Ordre/rupture/précédence égale : réutilise UNIQUEMENT
  `check_evolution` et `compare` publics, sans dupliquer ces règles.
- Majeure CROISSANTE signifie STRICTEMENT
  `proposed.version.major > previous.version.major` (entiers issus
  de `parse_version`), JAMAIS `compare > 0` : une mineure ou
  corrective ne déclenche pas les exigences doc/coexistence.
- Les refs doc PEUVENT changer à majeure égale. Seule une majeure
  strictement supérieure EXIGE refs doc LOGIQUES distinctes
  (`!=` textuel validé) ET `coexistence_doc` str non blanche
  (après strip, sans écho). Sinon `coexistence_doc` est `None`
  exact ou str non blanche exacte.
- Retour EXACT `DECLARATIVE_API_EVOLUTION_VALID`. N'atteste JAMAIS
  la publication réelle, la coexistence réelle, le schéma ni la
  compatibilité comportementale : validité déclarative seule.

## Interdits
Ni I/O, ni HTTP, ni génération OpenAPI, ni sécurité, ni idempotence,
ni garde tenant, ni nouvelles normes, ni dépendances, ni changement
de source existante.

## Tests futurs meaningful
Plans forgés/hostiles, contract non-API, doc ref invalide (vide,
avec contraintes, `target_id != valeur`, non identifiant), préfixe
majeures dont 0/pré/build, rupture même majeure bloquée, baisse
bloquée, précédence égale OK, nouvelle majeure sans doc distincte /
sans coexistence / blanche bloquées, mineure avec doc changée OK
sans coexistence, même majeure `None` OK et doc non blanche OK,
`breaking` non-bool rejeté, `TypeError` signature natif,
diagnostics constants sans écho. Comptes observés aux exécutions
dédiées puis régressions UNIT/INTEGRATION séparées via .venv
existant (exécution seule).
