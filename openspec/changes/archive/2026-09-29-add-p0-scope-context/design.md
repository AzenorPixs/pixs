# Design — add-p0-scope-context

## API concrète

- `ScopeType` : enum strict `TENANT | PLATFORM`, sans conversion silencieuse ; types exacts exigés, aucun cast implicite.
- `ScopeContext(scope_type, tenant_id=None, scope_id=None)` : frozen dataclass, validation structurelle à la construction, aucune mutation ni `freeze()` tardif.
- `ScopeNode` frozen `(scope_id, tenant_id, parent_scope_id=None)` : identifiants opaques `str` non vides, rejet des types invalides sans normalisation cachée.
- `validate_structure(ctx)` : TENANT exige `tenant_id` opaque non vide, `scope_id` facultatif cohérent selon contrat ; PLATFORM exige absence des deux ; `scope_id` sans tenant refusé ; types invalides rejetés.
- `TopologySnapshot(tenants, scopes)` : entrées itérables défensivement copiées, exposition immuable (tuples) ; tenants connus, scopes uniques, parents connus dans le même tenant, acyclique ; refus doublons, référence absente, cycle, inter-tenant.
- `resolve_order(snapshot)` : ordre topologique parent avant enfant avec tie-break lexicographique déterministe, indépendant de l'ordre d'entrée ; parcours itératif borné par taille du snapshot, pas de limite de récursion arbitraire.
- `validate_context(ctx, snapshot)` : vérification du contexte contre snapshot avant toute consommation.
- Propriété canonique représentée simplement par ScopeContext assigné explicitement à la ressource, aucune déduction de droits ni lookup magique : `ResourceOwnership` frozen `(resource_id, context)` minimal ; `canonical_owner` retourne le contexte possédé seulement si utile, sinon supprimer ce wrapper.
- `check_claim(canonical, claim=None, *, snapshot, on_denied)` : valide le contexte canonique réel contre snapshot, puis la prétention optionnelle qui MUST être un ScopeContext strictement égal ; ne jamais élargir parent/enfant/tenant/plateforme ; tout changement explicite refusé ; callback non callable rejeté à l'entrée ; audit obligatoire pour tout refus de frontière y compris canonique invalide ou prétention de mauvais type ; si le callback échoue, ne jamais retourner de contexte, exception enveloppée sans message brut.
- Diagnostics : codes/élément/étape par constantes, sans identifiants bruts ni donnée sensible ; décrire tests de mutation du snapshot après entrée et absence de contenu sensible dans les erreurs.

## Identifiants

Chaînes opaques non vides pour la mémoire ; rejet des types invalides. UUIDv7 réservé aux entités persistées futures, non imposé ici.

## Propagation et autorisation

La validation du contexte canonique contre le snapshot précède toute consommation. Le contexte ne donne jamais droit : l'autorisation, le runtime et l'audit durable restent à intégrer en aval. Les doubles de test du callback prouvent le signalement, pas un audit persistant.

## Fichiers minimaux

- `src/pixs/core/__init__.py` : export façade.
- `src/pixs/core/scope/__init__.py` : façade publique.
- `src/pixs/core/scope/context.py` : ScopeType, ScopeContext, validate_structure.
- `src/pixs/core/scope/topology.py` : snapshot, validation, ordre déterministe.
- `src/pixs/core/scope/ownership.py` : propriété canonique.
- `src/pixs/core/scope/propagation.py` : check_claim + callback audit.
- `tests/unit/test_scope_context_structure.py`, `tests/unit/test_scope_topology.py`, `tests/unit/test_scope_ownership.py`, `tests/integration/test_scope_propagation.py`.

Aucun wrapper identité inutile, aucune API freeze tardif.

## Critères et risques

Critères : constructions frozen, refus exigés, déterminisme par permutation d'entrée, refus élargissement explicite, callback appelé à chaque refus, diagnostics sans secret.
Risques : confusion structure/autorisation (mitigée par séparation stricte), sur-spécification identifiants (mitigée par opacité), dépendance ordre entrée (mitigée par tri canonique).
