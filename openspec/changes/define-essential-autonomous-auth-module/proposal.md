# Module essentiel pixs.auth et authentification autonome PostgreSQL

## Why

Pixs décrit des providers interchangeables sans garantir une authentification autonome livrée d'origine. Le cadrage du 19 octobre 2026 retient un module essentiel `pixs.auth`, indépendant de `pixs.core`, appuyé par défaut sur PostgreSQL, avec identité fédérée sortante, services propres OpenLDAP/KDC/Active Directory et sources externes installables séparément. Le choix de stockage Core OpenLDAP réversible constitue un complément distinct.

## What Changes

- **BREAKING** : exiger `pixs.auth` et une capacité locale autonome dans les compositions applicatives, dont P0 ; préserver les fixtures structurelles explicitement non applicatives.
- Séparer propriété des identités/droits Core et propriété des justificatifs, politiques, sessions et liaisons d'authentification Auth.
- Livrer le profil local PostgreSQL sans fournisseur externe, OpenLDAP, KDC, cloud ou Internet obligatoire.
- Définir les sous-modules locaux, l'enrôlement, l'émission d'identité, les services gérés et les connecteurs externes.
- Installer les connecteurs vers LDAP/Kerberos/OIDC/SAML externes seulement sur sélection explicite ; ils sont absents de l'installation standard.
- Conserver les trois dimensions d'assurance, les cardinalités Core, les garanties de secrets et l'exception Super Admin.
- Raccorder le choix postinstallation de stockage Core PostgreSQL vers OpenLDAP interne et son retour sans déplacer les sessions/justificatifs Auth ni l'évaluation des ACL.

## Capabilities

### New Capabilities

Aucune dans ce dossier ; les capacités spécialisées ont leurs changes propres, référencés dans design.md.

### Modified Capabilities

- `authentication` : module essentiel autonome, stockage PostgreSQL par défaut, configuration et composition des sous-modules.
- `core` : frontière de propriété et dépendance unidirectionnelle avec Auth.
- `reference-composition` : présence essentielle et profil local standard explicite.

## Impact

Cadrages PROJECT.md, TECHNICAL.md, BUILD.md et synthèse README.md ; raccordement documentaire de C02, C03, C08, C13 et C17. C03 reste propriétaire de la future connexion et des sessions. Aucun manifeste produit, code, dépendance installée, migration, service, secret, Git, déploiement ou publication.

Les trois deltas de ce change sont adoptés et synchronisés le 20 octobre 2026 dans authentication, core et reference-composition : neuf exigences ajoutées, une modifiée et treize scénarios supplémentaires nets. Cette adoption normative n'archive pas le dossier et n'autorise aucun code. Les autres dossiers Auth et le stockage Core réversible conservent leurs deltas proposés. Le catalogue détaillé et les recettes restent à réaliser et qualifier.
