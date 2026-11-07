# Références normatives — C95

Plan ACL-PIXS-2026-10-31-E3-R1, validé ; relevé du 31 octobre 2026. Les blocs ci-dessous sont des copies de référence, jamais des deltas ADDED/MODIFIED ni une autorité indépendante du canon. Leur présence ne prouve aucune réalisation.

## Traçabilité des exigences et scénarios

| Capacité | Exigence cible | Scénarios | Référence |
|---|---|---:|---|
| organization-charts | Trois référentiels propriétaires | 1 | organization-charts-c0cec12f0548 |
| organization-charts | Hiérarchie structurelle et affiliations | 1 | organization-charts-43a3193484d2 |
| organization-charts | Source explicite de chaque miroir | 1 | organization-charts-8369220fda62 |
| organization-charts | Structure seule par défaut | 1 | organization-charts-3f5fd5146131 |
| organization-charts | Admission et droits séparés du miroir | 1 | organization-charts-a06107e07b95 |

## Blocs sources complets

### Référence organization-charts-c0cec12f0548

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 11. SHA-256 du bloc : `c0cec12f054833f37f9ef4e5d2ae8e89737e329ea5b1f9ce56459b44fffdf241`.

Scénarios sources : ZT partagé.

~~~~text
### Requirement: Trois référentiels propriétaires

Core MUST gérer l'organigramme organisationnel et le fonctionnel, par Domaine après transition. CZT MUST gérer l'organigramme structurel de son ZT. PBO MUST présenter trois volets distincts ; un ZT partagé MUST conserver les périmètres des Domaines sans dupliquer une racine ZT par Domaine.

#### Scenario: ZT partagé

- **WHEN** deux Domaines utilisent le même CZT
- **THEN** leurs volets Core restent propres et les périmètres structurels sont présentés dans le ZT commun.
~~~~

### Référence organization-charts-43a3193484d2

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 20. SHA-256 du bloc : `43a3193484d2bee52ef6f44cfe182b5c6b34e2cfb44d4f63bcd89d3ed21ebcd1`.

Scénarios sources : Deux parents structurels.

~~~~text
### Requirement: Hiérarchie structurelle et affiliations

L'organigramme ZT MUST posséder une racine unique, au plus un parent structurel par structure, aucun cycle et des affiliations multiples possibles. Chaque acteur technique MUST avoir une structure responsable de référence ; chaque individu MUST avoir un rattachement principal par ZT. Ces relations MUST rester distinctes des permissions et de la hiérarchie PKI.

#### Scenario: Deux parents structurels

- **WHEN** une structure ZT reçoit deux parents structurels
- **THEN** la mutation est refusée sans empêcher les affiliations transversales autorisées.
~~~~

### Référence organization-charts-8369220fda62

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 29. SHA-256 du bloc : `8369220fda6234df9ed1556288de294305748cfda265cac54698c3df3fa38184`.

Scénarios sources : Écriture sur miroir.

~~~~text
### Requirement: Source explicite de chaque miroir

Un périmètre de miroitage MUST choisir une source explicite parmi les trois organigrammes, ses données et transformations autorisées. Ses mutations MUST passer par la source et respecter les contraintes cibles. Une modification de la copie MUST NOT devenir silencieusement une deuxième autorité.

#### Scenario: Écriture sur miroir

- **WHEN** un opérateur tente de modifier directement la copie reflétée
- **THEN** l’interface applique le contrat de la source ou refuse l’écriture concurrente.
~~~~

### Référence organization-charts-3f5fd5146131

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 38. SHA-256 du bloc : `3f5fd5146131f61a9cf1d8e9811329be5f7f571d315ad76e8af0231f736a8105`.

Scénarios sources : Miroir standard.

~~~~text
### Requirement: Structure seule par défaut

Le miroir MUST porter sur la structure seule par défaut. La synchronisation des rattachements et affiliations MAY être activée explicitement par périmètre ; les individus MUST rester référencés depuis Core sans duplication d'identité ou de moyen d'authentification.

#### Scenario: Miroir standard

- **WHEN** un miroir est créé sans sélection des affiliations
- **THEN** les seules structures et relations hiérarchiques autorisées sont reprises.
~~~~

### Référence organization-charts-a06107e07b95

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 47. SHA-256 du bloc : `a06107e07b9597bbf983057cb15e8480fd7a774f5e4c3628bc1d29e71ecce71b`.

Scénarios sources : Affiliation vers un ZT.

~~~~text
### Requirement: Admission et droits séparés du miroir

Un miroir MUST NOT créer implicitement admission ZT, compte, permission ou copie d'ACL. Une affiliation vers ZT MUST exiger l'admission applicable et les politiques ZT MUST être réévaluées après modification autorisée.

#### Scenario: Affiliation vers un ZT

- **WHEN** le miroir reçoit l’affiliation d’un individu non admis
- **THEN** aucune participation effective ni autorisation ZT n’est déduite.
~~~~
