# Références normatives — Z28

Plan ACL-PIXS-2026-10-31-E3-R1, validé ; relevé du 31 octobre 2026. Les blocs ci-dessous sont des copies de référence, jamais des deltas ADDED/MODIFIED ni une autorité indépendante du canon. Leur présence ne prouve aucune réalisation.

## Traçabilité des exigences et scénarios

| Capacité | Exigence cible | Scénarios | Référence |
|---|---|---:|---|
| zt-dns-dhcp | DZT obligatoire et base commune indépendante | 1 | zt-dns-dhcp-a6e4d4b82a23 |
| zt-dns-dhcp | Préparation et mise à jour PA configuration PZT | 1 | zt-dns-dhcp-2b6ce945e38b |
| zt-dns-dhcp | Configuration entièrement régénérable | 1 | zt-dns-dhcp-7ead14a72e9a |
| zt-dns-dhcp | Activation DHCP indépendante et désactivée par défaut | 1 | zt-dns-dhcp-43c426b9d645 |
| zt-dns-dhcp | Adressage coordonné et propriétaire par pool | 1 | zt-dns-dhcp-a3fa9a562107 |
| zt-dns-dhcp | Liaison DHCP DNS configurable | 1 | zt-dns-dhcp-17080b1aed7c |

## Blocs sources complets

### Référence zt-dns-dhcp-a6e4d4b82a23

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 11. SHA-256 du bloc : `a6e4d4b82a23d0d4194faa5e5bc977d55dd4e10d2015293d1cdb5dad391f56d3`.

Scénarios sources : Plusieurs DZT.

~~~~text
### Requirement: DZT obligatoire et base commune indépendante

Chaque ZT MUST disposer d'au moins un DZT exécuté par PZT. BIND 9 MUST fournir DNS v4/v6 et ISC DHCP MUST fournir DHCPv4 et DHCPv6 par processus distincts. Une PG DZT MUST conserver la référence commune à ces fonctions, indépendante de CZT, PKIZT et PBO, avec réplication synchrone et primaire unique selon zt-controller et brick-redundancy.

#### Scenario: Plusieurs DZT

- **WHEN** une réplique DZT est ajoutée
- **THEN** elle rejoint le même référentiel logique sans source de configuration concurrente.
~~~~

### Référence zt-dns-dhcp-2b6ce945e38b

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 20. SHA-256 du bloc : `2b6ce945e38b1456b0c994124e8b62d091fd1a2c036cf2d5bfd22940c5cff008`.

Scénarios sources : Mise à jour BIND.

~~~~text
### Requirement: Préparation et mise à jour PA configuration PZT

PA MUST assurer préparation, installation, maintenance système et mise à jour des logiciels DNS/DHCP. PZT/DZT MUST assurer configuration et maintenance logicielle du fonctionnement, validation, application et contrôle des services. PBO MUST administrer séparément les périmètres. Ces interventions MUST être coordonnées et leurs résultats distingués.

#### Scenario: Mise à jour BIND

- **WHEN** PA termine une mise à jour autorisée
- **THEN** DZT revalide la compatibilité, réapplique si nécessaire la configuration et vérifie le fonctionnement avant succès du service.
~~~~

### Référence zt-dns-dhcp-7ead14a72e9a

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 29. SHA-256 du bloc : `7ead14a72e9af3424f562f2087ddbb48654a73f7b60db2fd1fadd8dc6fde5968`.

Scénarios sources : Régénération après panne.

~~~~text
### Requirement: Configuration entièrement régénérable

DZT MUST produire et pouvoir rejouer intégralement les configurations depuis une révision cohérente de sa PG, sans traiter les modifications manuelles des fichiers comme vérité. Baux, mises à jour dynamiques, journaux nécessaires et clés DNSSEC MUST être préservés par des contrats de durabilité/reprise explicites.

#### Scenario: Régénération après panne

- **WHEN** les fichiers générés sont reconstruits
- **THEN** l’état natif durable n’est ni effacé ni supposé recréé par la configuration seule.
~~~~

### Référence zt-dns-dhcp-43c426b9d645

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 65. SHA-256 du bloc : `43c426b9d6456cb755fb4972337fd0e477a48d4d20272893874aad0ed48c3f5b`.

Scénarios sources : DZT initialisé.

~~~~text
### Requirement: Activation DHCP indépendante et désactivée par défaut

DHCPv4 et DHCPv6 MUST être désactivés par défaut et activés explicitement, indépendamment par réseau, depuis PBO. La présence obligatoire du DZT MUST NOT démarrer l'attribution DHCP sur un réseau non autorisé.

#### Scenario: DZT initialisé

- **WHEN** un DZT est initialisé sans réseau DHCP activé
- **THEN** aucun bail DHCPv4 ou DHCPv6 n’est attribué.
~~~~

### Référence zt-dns-dhcp-a3fa9a562107

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 74. SHA-256 du bloc : `a3fa9a56210702924906d9035b25f98c9f643efb265199f0158abe66ec74dd1f`.

Scénarios sources : Reprise sans baux fiables.

~~~~text
### Requirement: Adressage coordonné et propriétaire par pool

CZT MUST gérer l'adressage des pairs PZT ; DZT MUST gérer les réseaux DHCP avec coordination des préfixes/pools. Un pool MUST avoir un seul DZT autorisé à attribuer ou renouveler ses baux à un instant donné ; les pools MAY être répartis. La reprise MUST vérifier les baux et exclure l'ancien propriétaire.

#### Scenario: Reprise sans baux fiables

- **WHEN** un secours ne peut vérifier l’état des baux du pool
- **THEN** il ne devient pas allocateur actif sur la seule panne de l’ancien DZT.
~~~~

### Référence zt-dns-dhcp-17080b1aed7c

Source : [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md), ligne 83. SHA-256 du bloc : `17080b1aed7cd6b13ddd795989aa792216bef304a46a3306be0f2b2a1db8ded7`.

Scénarios sources : Publication échouée.

~~~~text
### Requirement: Liaison DHCP DNS configurable

Le lien DHCP–DNS MUST pouvoir être automatique et configurable par périmètre. Le bail et son état de publication DNS MUST être suivis séparément, avec idempotence, retrait et reprise selon leurs politiques ; la réussite de l'un MUST NOT prouver celle de l'autre.

#### Scenario: Publication échouée

- **WHEN** un bail est accordé mais sa publication DNS échoue
- **THEN** les deux états sont visibles et la reprise ne réattribue pas aveuglément le bail.
~~~~
