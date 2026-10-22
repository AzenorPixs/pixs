# pixs.core identity — TenantMembership structurel

`TenantMembership` est une paire frozen `(identity_id UUIDv7 exact, tenant_id str exact non vide)`, compatible avec `TopologySnapshot.tenants` et `ScopeContext`. Le projet requiert Python ≥3.12, conformément à `pyproject.toml` ; aucun service applicatif ne démarre à l’import.

`validate_tenant_memberships(identities, tenants, memberships)` exige trois tuples exacts : des `DigitalIdentity` exactes et valides, des identifiants tenant str exacts non vides et des `TenantMembership` exactes. Les références doivent exister ; les identités, tenants et paires dupliqués sont refusés. La relation est N-N ; une identité SERVICE sans User est admise. Les identifiants tenant restent opaques, sans conversion UUID ni trim.

```python
import uuid
from pixs.core.identity import (
    DigitalIdentity, IdentityState, IdentityType,
    TenantMembership, validate_tenant_memberships,
)

# UUIDv7 déterministe pour l’exemple, sans générateur ni effet externe.
identity = DigitalIdentity(
    uuid.UUID(int=(7 << 76) | (2 << 62) | 1),
    IdentityType.SERVICE,
    IdentityState.ACTIVE,
)
membership = TenantMembership(identity.identity_id, "tenant-01")
assert validate_tenant_memberships(
    (identity,), ("tenant-01",), (membership,),
) is True
```

Cette validation porte uniquement sur la structure. Elle accepte tous les états d’identité structurellement valides et ne prouve aucune appartenance ACTIVE au runtime. Activation, révocation, assurance, persistance PostgreSQL, authentification, autorisation, audit, propagation runtime et CRUD tenant restent à implémenter dans leurs périmètres spécifiés. Aucun droit, lien User, identifiant généré ou Tenant autonome n’est ajouté.

Les erreurs exposent exclusivement un message et des attributs constants, sans valeur d’entrée brute. Les sous-types et objets invalides sont rejetés avant leurs protocoles de comparaison, de hachage ou de représentation.
