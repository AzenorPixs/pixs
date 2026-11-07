# C21 — Module essentiel pixs.auth et authentification autonome PostgreSQL

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Auth sur PG Instance avant Domaine puis identités de Domaine ; LZT/KZT requis par Domaine ; aucune souveraineté Core transférée vers LDAP.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [authentication](../../specs/authentication/spec.md).
- [core](../../specs/core/spec.md).
- [reference-composition](../../specs/reference-composition/spec.md).
- [pixs-instance](../../specs/pixs-instance/spec.md).
- [pixs-domains](../../specs/pixs-domains/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

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

## Statut des deltas antérieurs après contrôle E3

Les anciens fichiers sous specs/ ont été déplacés, avec empreintes conservées, vers [l’historique interne](historique-deltas-avant-e3/README.md). Le [contrôle de couverture](COUVERTURE_DELTAS_E3.md) relie chaque ancienne exigence au contrat courant et aux tâches ouvertes. Le dossier reste actif ; skip_specs évite seulement la réapplication des anciennes prescriptions. Il ne termine ni la réalisation, ni les tests, ni les 49 tâches encore ouvertes dans les sept dossiers concernés.
