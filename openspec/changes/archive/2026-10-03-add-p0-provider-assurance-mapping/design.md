# Design : add-p0-provider-assurance-mapping

## Modèle (frozen, tous champs obligatoires sans défaut)

- `AssuranceDimension(Enum)` : `IDENTITY`, `AUTHENTICATION`, `FEDERATION` ; chacune liée à son enum et minimum (`CLAIMED`, `SINGLE_FACTOR`, `UNTRUSTED`).
- `AssuranceRule` : `dimension: AssuranceDimension`, `method: str` (jeton opaque non vide), `level: IdentityAssurance | AuthenticationAssurance | FederationTrust` — identité de membre constante du seul enum de cette dimension avant hachage ou ordinal ; `type(x) in (classes)` est proscrit (métaclasse étrangère).
- `ProviderAssuranceMapping` : `provider_id: str`, `max_identity_assurance: IdentityAssurance`, `max_authentication_assurance: AuthenticationAssurance`, `max_federation_trust: FederationTrust`, `accepted_rules: tuple[AssuranceRule, ...]`, `valid_from: datetime`, `valid_until: datetime`.
- `ProofObservation` : `observation_id: str`, `provider_id: str`, `method: str`, `status: str` dans `{ABSENT, AMBIGUOUS, EXPIRED, UNVERIFIED, VERIFIED}`, `attested_at: datetime`, `expires_at: datetime` fini strict. `ABSENT` reste un constat inactif ; l'absence canonique est le tuple vide.
- `AssuranceResult` : exactement `identity_assurance: IdentityAssurance`, `authentication_assurance: AuthenticationAssurance`, `federation_trust: FederationTrust`, tous obligatoires ; trois champs séparés, jamais fusionnés.

## Signature et contrat

`evaluate_assurance(mapping: ProviderAssuranceMapping, observations: tuple[ProofObservation, ...], reference_time: datetime) -> AssuranceResult` ; lève `AssuranceMappingError` (constante, `code="PDP_MAPPING_INVALID"`, `element="pdp_mapping"`, `step="validate_mapping"`, sans écho de valeur). Les erreurs structurelles (types/valeurs/identifiants dupliqués/règles dupliquées/plafond violé) lèvent cette erreur constante ; les permutations donnent mêmes code, element, step et message. La divergence de niveaux issus de preuves bien formées donne le minimum par dimension comme précisé ci-dessous, sans exception. Aucun retour de liste de diagnostics.

## Ordre des gardes

1. identité de type exacte (`type(x) is`) du mapping, du conteneur (`tuple`) et de chaque observation avant tout accès d'attribut étranger ;
2. scalaires : `str` non vides opaques (alignés sur la grammaire d'identifiants du contexte PDP existant, aucune grammaire neuve) ;
3. temps : `_is_utc_aware` (helper privé de `policy`, seule réutilisation privée admise et validée CGPT, lecture seule) sur chaque datetime, `valid_from < valid_until`, `attested_at < expires_at`, `reference_time` UTC ;
4. règles : unicité `(dimension, method)` ; `level` ∈ enum de la dimension ; ordinal issu de l'ordre de déclaration des enums existantes (`tuple(Enum)`, sans invocation de `decision._rank`) ; `level <= plafond` de la dimension ; unicité des `observation_id` du lot. Identité de membre des enums avant tout ordinal ou hachage.

## Validité et sémantique

Fenêtres demi-ouvertes partout : le mapping contribue si `valid_from <= reference_time < valid_until` ; l'observation si `attested_at <= reference_time < expires_at`. Par dimension, ne contribue qu'une observation du même `provider_id`, `status == VERIFIED`, dont la `method` est référencée par une règle `(dimension, method)` ; le niveau retenu est celui **déclaré de la règle**, plafonné validé ; `ABSENT`/`AMBIGUOUS`/`EXPIRED`/`UNVERIFIED` ou hors fenêtre ne contribuent jamais.

## Résolu par dimension

Aucun contributeur ⇒ minimum de la dimension ; niveau distinct unique ⇒ ce niveau ; niveaux divergents ⇒ **minimum de la dimension** (politique conservatrice : seul le minimum évite toute hausse implicite sous preuve contradictoire).

## Frontière de confiance

Les statuts sont des constats normalisés non secrets d'un hôte déjà authentifié : aucune authentification, vérification cryptographique ni permission n'en est déduite ; aucun `AuthenticationContext` produit ; `ports.py` et PDP inchangés.

## Preuves

3 × `py_compile` réellement exécutés sous DEVOPS Python 3.14.8 ; syntaxe minimale 3.11 contrôlée par AST seulement, aucune exécution Python 3.11 revendiquée, unitaires (plafonds, unicité, fenêtres, divergence, hostiles sans invocation, absence vide), intégration enfant frais sous gardes IO/finder causales avant import, régressions PDP (`test_pdp_policy`, `test_pdp_decision`, `test_pdp_time`) et tests identité/périmètre liés aux imports réutilisés ; les 200 tests du change précédent restent déjà prouvés, sans interaction nouvelle, baseline 168, stricts avant code puis avant/après cochage, archivage et statistiques distincts.
