# Design — add-p0-tenant-membership

## Choix d'implémentation

Module `src/pixs/core/identity/tenant_membership.py` : `TenantMembership` frozen slots repr=False avec `identity_id` UUIDv7 EXACT du profil existant et `tenant_id` str EXACT opaque non vide compatible `TopologySnapshot.tenants` et `ScopeContext`.

`validate_tenant_membership(value)` exige type exact `TenantMembership`, lecture via `object.__getattribute__`, `_check_uuid` réutilisé comme `groups.py` pour `identity_id`, `tenant_id` str exact non vide, sans normalisation trim, sans défaut, sans identifiant généré.

`validate_tenant_memberships(identities, tenants, memberships)` exige trois tuples EXACTS obligatoires. Identités `DigitalIdentity` EXACTES via `validate_identity`. Tenants : str exacts non vides. Rejette identités dupliquées par entier UUID, tenants dupliqués par valeur, références absentes, paire identité/tenant dupliquée. Cardinalité N-N. `SERVICE` sans `User` admis. Tous états structurellement valides acceptés SANS donner droit ni activation.

Identifiant tenant non converti en UUID. Aucun `Tenant` autonome inventé. Erreur `TenantMembershipError(ValueError)` message constant, attributs `code`, `element`, `step` constants, sans valeur brute, `from None` lors traduction `IdentityError` ou structurelle.

Gardes `type(x) is` exclusives, aucune comparaison de types par égalité ni protocole d'objet inconnu. Aucun `hash`, `getattr`, `__repr__` hostile avant types exacts. Modèles corrompus refusés au validate.

## Limites

Pure référence tenant : contextualise la relation mais ne prouve aucune appartenance ACTIVE au runtime ni lecture ou mutation permise. Aucun état, transition, contexte d'assurance ajouté.

Activation, révocation, Django, PostgreSQL vérité, Bearer, autorisation, audit, propagation, CRUD tenant restent REQUIS ultérieurement. Validation structurelle ne vaut ni authentification ni autorisation ni persistance ni audit durable.

## Ressources futures prévues

Module, façade `src/pixs/core/identity/__init__.py` par append original inchangé, nouveau `src/pixs/core/identity/README.md`, `tests/unit/test_tenant_membership.py`, `tests/integration/test_tenant_membership_integration.py`. AST Python 3.11, UTF-8 LF, tests dédiés puis régressions en DEUX commandes séparées, exemples README, non-import Django, PDP ou service tant que pure.
