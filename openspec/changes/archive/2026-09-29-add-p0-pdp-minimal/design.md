# Design — add-p0-pdp-minimal

## 1. Catalogue, sélecteurs et conditions

- `Catalog(subject_ids: tuple[str], resource_ids: tuple[str], action_ids: tuple[str], scope_contexts: tuple[ScopeContext], attribute_types: tuple[(nom, STR|INT)])` frozen : identifiants canoniques déclarés, duplications refusées ; aucune liste partielle oubliant action ou scope.
- `Selector(kind: str, values: tuple[str])` frozen pour subject, resource et action : `kind` déclaré au catalogue, valeurs `str` exactes non vides dédupliquées et triées ; wildcard, préfixe et vide refusés. `ScopeSelector(contexts: tuple[ScopeContext])` frozen pour le périmètre.
- `Condition(attr: str, op: str, value: object)` frozen : `attr` déclaré, `op` fermé `eq|in` ; `eq` valeur unique `str|int` exact (`type(x) is int`, bool refusé) ; `in` tuple homogène non vide ; memberships fournis uniquement comme faits vérifiés du port, sans octroi autonome.
- `Obligation(kind: str)` frozen : seule variante `AUDIT` normalisée.

## 2. Politiques, limites et snapshot

- `Policy(policy_id, policy_version, owner, effect: Effect, subject, resource, action, scope: ScopeSelector, conditions, obligations, valid_from, valid_until, min_identity_assurance|None, min_authentication_assurance|None, min_federation_trust|None, max_auth_age_seconds: int|None)` frozen : seuils stockés réellement et séparés, fenêtres UTC aware `[from,until)`, obligation inconnue ou politique mal formée rejetée avant activation.
- `Limits(max_policies, max_selector_values, max_conditions_per_policy, max_set_values, max_attributes, max_memberships, max_id_length, max_value_length, max_cost, ttl_seconds, max_freshness_seconds)` frozen : entiers stricts positifs, explicitement requis, sans défaut inventé. Bornent catalogue, chaînes et entiers (`bit_length <= max_value_length`), faits du port, méthodes auth, snapshots et boucles avant tri et copie. Coût conservateur cumulatif en unités d'éléments visités et comparés, contrôlé pendant l'évaluation, dépassement produisant DENY.
- `Snapshot(epoch, catalog: Catalog, limits: Limits, policies: tuple[Policy])` immuable : factory `build_snapshot(epoch, policies, catalog, limits)` validant bornes AVANT normalisation ; politiques normalisées triées ; `policy_id` dupliqué rejeté même à versions différentes (une version active par snapshot) ; `policy_version` d'une décision = `(epoch, tuple((policy_id, version)))`.

## 3. Requête, faits et ports

- `Request(decision_id: str, subject_id: str, resource_id: str, action_id: str, context: ScopeContext, correlation_id: str)` frozen : `str` exacts non vides plus ScopeContext réel, sans auth embarquée ni secret.
- `AuthenticationContext` : types exacts §4.1, trois enums séparées, datetimes UTC aware ; aucun booléen verified.
- `TrustedFacts(subject_id, resource_id, action_id, auth: AuthenticationContext, memberships: tuple[str], attributes: tuple[(nom, valeur)], ownership: ResourceOwnership, context: ScopeContext, revocation_status: ACTIVE|REVOKED|UNKNOWN)` frozen. `TrustedFactsProvider.resolve(request) -> TrustedFacts` dont l'instance vient uniquement de la composition de confiance.
- Appariement strict : `subject_id == auth.digital_identity_id == request.subject_id`, `resource_id == ownership.resource_id == request.resource_id`, `action_id == request.action_id`, `auth.context == facts.context == request.context`, contexte ownership exactement même ScopeContext (partage et héritage non fournis implicitement) ; topologie validée via snapshot `core.scope`.
- `Clock.now() -> datetime` UTC aware lu une seule fois ; si impossible, `evaluated_at=None`, `expires_at=None` et DENY. Snapshot invalide donne `policy_version=None` sans faux identifiant ; exception du provider produit DENY audité.
- `AuditEvent(decision_id, subject_id, resource_id, action_id, context, correlation_id, effect, reason_code, policy_version, evaluated_at)` : champs sûrs validés, valeurs invalides représentées None sans repr ; enrichissement composant, version et causalité réservé à un adapter futur. `AuditSink.record(event) -> ack` strict `True` ; `False` ou exception maintient DENY. ALLOW plateforme porte AUDIT requis et reste non exécutable avant PEP.

## 4. Décision et algorithme

- `Decision(decision_id, effect, reason_code, policy_version, obligations, evaluated_at, expires_at)` frozen ; codes publics `ALLOWED|DENIED`.
- Signature sans doublon : `authorize(request, snapshot, provider, clock, audit, topology) -> Decision` (catalogue et limites portés par le snapshot, topologie passée une fois).
1. Valider snapshot, faits, bornes et types exacts sans repr des entrées.
2. Apparier strictement puis valider topologie ; condition requise absente sur candidate DENY produit DENY, jamais ignorée ; bool et int ne correspondent pas.
3. Retenir politiques actives et horizons `valid_from|valid_until` futurs des politiques aux cibles correspondantes, y compris inactives et conditions susceptibles d'évoluer ; borne conservatrice raccourcissant sans augmenter les droits.
4. Appliquer DENY puis ALLOW puis refus ; unir obligations ALLOW applicables.
5. Calculer `expires_at` comme minimum de now+TTL, expiration auth, auth_time+fraîcheur, prochaine transition ; aucun ALLOW à échéance <= now.
6. Auditer tout refus via le port, échec jamais ALLOW ; plateforme auditée, cross-tenant refusé dans le profil ; recalculer réellement à chaque appel.

## 5. Tests et exclusions

- `tests/unit/test_pdp_policy.py` : catalogue, sélecteurs, conditions, obligations, limites, doublons policy_id, normalisation.
- `tests/unit/test_pdp_decision.py` : appariement strict, DENY>ALLOW, bool/int, opérateur inconnu, absence DENY conservée, périmètres, assurances.
- `tests/unit/test_pdp_time.py` : UTC, TTL, fraîcheur, transitions futures dont DENY futur, fuseaux, déterminisme et non-mutation.
- `tests/integration/test_pdp_audit.py` : refus audités une fois, échec audit fermé, plateforme et cross-tenant, doubles sans preuve de persistance.
- Cinq sources : `src/pixs/core/authz/__init__.py`, `policy.py`, `snapshot.py`, `decision.py`, `ports.py`. Aucune dépendance nouvelle, aucun comportement général non prétendu implémenté.
