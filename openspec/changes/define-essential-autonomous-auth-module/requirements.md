# Registre consolidé des déclarations Auth et stockage Core

## Statut au 20 octobre 2026

Neuf changes restent ouverts. Les seuls deltas de define-essential-autonomous-auth-module sont adoptés le 20 octobre 2026 dans authentication, core et reference-composition : neuf exigences ajoutées, une modifiée et treize scénarios supplémentaires nets. Les huit autres dossiers conservent leurs deltas proposés. Les 83 tâches restent non cochées ; aucun code, manifest produit, dépendance, service ou migration n'est produit par cette adoption documentaire.

Les clauses canoniques continuent à s'appliquer tant que leurs modifications proposées ne sont pas adoptées. Les décisions du présent registre définissent le périmètre documentaire, sans prétendre que les choix détaillés, paramètres et preuves de compatibilité sont déjà arrêtés.

## Déclarations et dossiers propriétaires

| Déclaration retenue | Change ouvert | Deltas et état d'adoption |
| --- | --- | --- |
| pixs.auth essentiel indépendant ; dépendance publique vers Core ; local PostgreSQL par défaut ; politiques et sous-modules | [Architecture](proposal.md) | [authentication](specs/authentication/spec.md), [core](specs/core/spec.md), [reference-composition](specs/reference-composition/spec.md) — adoptés au canon le 20 octobre 2026 |
| Mot de passe, passkeys/WebAuthn, TOTP, MFA et récupération locaux ; moyens matériels extensibles | [Méthodes locales](../add-auth-local-authenticators-and-mfa/proposal.md) | [auth-authenticators](../add-auth-local-authenticators-and-mfa/specs/auth-authenticators/spec.md) |
| Forge/enrôlement, preuves et liaison des moyens sans second référentiel | [Enrôlement](../add-auth-identity-enrollment/proposal.md) | [auth-identity-enrollment](../add-auth-identity-enrollment/specs/auth-identity-enrollment/spec.md) |
| Pixs fournisseur d'identité vers clients approuvés OIDC/SAML | [Émission d'identité](../add-auth-identity-provider/proposal.md) | [auth-identity-provider](../add-auth-identity-provider/specs/auth-identity-provider/spec.md) |
| Annuaire OpenLDAP propre activable ; projection, authentification et stockage Core déclarés séparément | [OpenLDAP géré](../add-auth-managed-openldap/proposal.md) | [auth-managed-directory](../add-auth-managed-openldap/specs/auth-managed-directory/spec.md), [directory-projections](../add-auth-managed-openldap/specs/directory-projections/spec.md) |
| KDC propre activable seul ou avec backend LDAP explicitement sélectionné | [KDC géré](../add-auth-managed-kerberos-kdc/proposal.md) | [auth-managed-kerberos](../add-auth-managed-kerberos-kdc/specs/auth-managed-kerberos/spec.md) |
| Sources externes LDAP/Kerberos/OIDC/SAML installables, absentes du profil standard | [Connecteurs externes](../add-auth-external-source-submodules/proposal.md) | [auth-external-sources](../add-auth-external-source-submodules/specs/auth-external-sources/spec.md) |
| pixs.auth.directory.ad pour un domaine Active Directory propre, non activé par défaut | [Active Directory géré](../add-auth-managed-active-directory/proposal.md) | [auth-managed-active-directory](../add-auth-managed-active-directory/specs/auth-managed-active-directory/spec.md) |
| Utilisateurs/groupes/ACL initialement dans PostgreSQL ; migration postinstallation vers OpenLDAP interne ; retour depuis les données LDAP courantes | [Stockage Core réversible](../add-reversible-core-directory-storage/proposal.md) | [core-storage](../add-reversible-core-directory-storage/specs/core-storage/spec.md), [core](../add-reversible-core-directory-storage/specs/core/spec.md), [directory-projections](../add-reversible-core-directory-storage/specs/directory-projections/spec.md), [reference-runtime](../add-reversible-core-directory-storage/specs/reference-runtime/spec.md) |

## Frontières communes à appliquer

- Core garde les identités canoniques, relations, groupes et droits ; Auth gère l'authentification, ses moyens, politiques et sessions, et le contrôle de ses services propres.
- PostgreSQL est le stockage par défaut ; la seule exception Core de ces dossiers est l'OpenLDAP interne engagé par migration réversible. Les autres domaines restent sur leur stockage déclaré.
- La projection LDAP reste une copie de consultation sans ACL Pixs. Le stockage Core LDAP peut conserver les ACL applicatives, dont l'évaluation reste dans Pixs. Les ACL techniques slapd ne les remplacent pas.
- L'activation d'OpenLDAP, du KDC, d'AD ou d'un émetteur IdP n'installe aucun connecteur externe et ne migre aucune donnée Core par effet de bord.
- L'aller et le retour Core conservent UUID, relations, états, versions, révocations et tombstones ; le retour ne réactive pas une ancienne copie PostgreSQL et la panne ne vaut pas migration.
- L'exception Super Admin reste celle du canon dans son seul périmètre, sans création de preuve MFA, de conformité cryptographique ou de résultat de migration absent.

## Raccordements existants et limites

[C03](../add-initial-authentication-and-sessions/design.md) conserve connexion et sessions ; [C02](../archive/2026-10-20-add-core-postgres-services/design.md) conserve le provider PostgreSQL initial. [C08](../add-installation-and-first-configuration/design.md) porte le provisionnement, [C13](../add-initial-administration-panel/design.md) l'administration, [C17](../qualify-first-pbo-composition/design.md) la qualification de l'artefact sélectionné. Les dossiers de projection [O08](../add-ldap-outbound-directory-projections/design.md) et de lecture fraîche [O09](../add-directory-read-freshness-and-postgres-fallback/design.md) restent limités à leur rôle de projection.

Les produits, versions, paramètres, schémas physiques, profils de protocole, garanties LDAP multi-objets et mécanismes de bascule restent à préciser et qualifier avant code. DEVOPS.md reste un inventaire d'environnement ; la présence d'un outil n'y prouve ni installation d'une capacité proposée ni qualification de celle-ci.
