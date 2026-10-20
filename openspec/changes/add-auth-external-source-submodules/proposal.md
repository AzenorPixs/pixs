# Sous-modules installables de sources d'authentification externes

## Why

Les sources externes LDAP, Kerberos ou fédérées doivent être ajoutées à la demande. Elles ne doivent être confondues ni avec le provider local ni avec les propres services annuaire/KDC de Pixs.

## What Changes

- Prévoir des sous-modules LDAP, Kerberos, OIDC, SAML et autres sources sous contrats extensibles.
- Les exclure de l'installation standard, puis séparer installation, configuration de confiance et activation.
- Définir liaison canonique multi-source, assurance, indisponibilité et déprovisionnement sans repli implicite.

## Capabilities

### New Capabilities

- `auth-external-sources` : sous-modules installables de sources d'authentification externes.

### Modified Capabilities

Aucune ; les exigences transversales restent celles du canon et du change d'architecture.

## Impact

Proposition documentaire du 19 octobre 2026, dépendante de [l'architecture Auth](../define-essential-autonomous-auth-module/proposal.md). Deltas proposés uniquement, sans synchronisation du canon. Aucun code, migration, dépendance installée, secret, service, Git, déploiement ou publication. Les identifiants proposés ne créent aucun manifest.
