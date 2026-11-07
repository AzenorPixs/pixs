# Références normatives — Z32

Plan ACL-PIXS-2026-10-31-E3-R1, validé ; relevé du 31 octobre 2026. Les blocs ci-dessous sont des copies de référence, jamais des deltas ADDED/MODIFIED ni une autorité indépendante du canon. Leur présence ne prouve aucune réalisation.

## Traçabilité des exigences et scénarios

| Capacité | Exigence cible | Scénarios | Référence |
|---|---|---:|---|
| zt-network-services | RPZT facultatif et actifs multiples | 1 | zt-network-services-c666104b77f7 |
| zt-network-services | Authentification au service cible | 1 | zt-network-services-9f7d4b5d9913 |
| zt-network-services | TLS par publication et distribution PKIZT | 1 | zt-network-services-4da2c1ae43f4 |
| zt-pki | Remise TLS ciblée aux RPZT | 1 | zt-pki-790b4d1f8594 |

## Blocs sources complets

### Référence zt-network-services-c666104b77f7

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 92. SHA-256 du bloc : `c666104b77f7521618077500dde9c139d7352afdcbec9a9190616d99b921a34e`.

Scénarios sources : Deux RPZT.

~~~~text
### Requirement: RPZT facultatif et actifs multiples

RPZT MUST publier les services HTTP/HTTPS/WebSocket explicitement autorisés, être optionnel et désactivé par défaut, avec référence CZT et RAM sans PG propre. Plusieurs RPZT MAY être actifs pour une publication ; l'orientation des clients et ses effets MUST être qualifiés.

#### Scenario: Deux RPZT

- **WHEN** deux exécutants portent une publication
- **THEN** la présence des deux ne prouve pas à elle seule une orientation ou bascule fonctionnelle.
~~~~

### Référence zt-network-services-9f7d4b5d9913

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 101. SHA-256 du bloc : `9f7d4b5d99131170e79e5cfaa72940a0b9120e84066bb8b149276257501ab287`.

Scénarios sources : Service public non déclaré.

~~~~text
### Requirement: Authentification au service cible

RPZT MUST assurer publication, acheminement et restrictions techniques sans authentifier les utilisateurs. Le service cible MUST assurer l'authentification et les droits applicatifs par défaut ; une publication publique MUST être déclarée et autorisée explicitement.

#### Scenario: Service public non déclaré

- **WHEN** une publication vise un service sans authentification sans autorisation publique
- **THEN** elle n’est pas admise comme publication protégée par le seul RPZT.
~~~~

### Référence zt-network-services-4da2c1ae43f4

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 110. SHA-256 du bloc : `4da2c1ae43f4daf05a06f9d630468a2fd057857830ff776838fc7952e91a13e6`.

Scénarios sources : TLS passthrough.

~~~~text
### Requirement: TLS par publication et distribution PKIZT

Chaque publication MUST choisir terminaison TLS au RPZT ou passage chiffré jusqu'au service. En terminaison, PKIZT MUST assurer le cycle des certificats et la remise ciblée/protégée selon zt-pki. Un mode TLS MUST NOT créer une responsabilité d'authentification utilisateur au RPZT.

#### Scenario: TLS passthrough

- **WHEN** une publication transmet TLS jusqu’au service
- **THEN** le service termine TLS et RPZT ne prétend pas authentifier l’utilisateur.
~~~~

### Référence zt-pki-790b4d1f8594

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 74. SHA-256 du bloc : `790b4d1f85949dec88a03d074756efcd37cc36d11652e4dc9e2449f12c9ee58e`.

Scénarios sources : Publication partagée explicitement.

~~~~text
### Requirement: Remise TLS ciblée aux RPZT

Les éléments TLS MUST être distribués uniquement aux RPZT habilités, avec protection individualisée. Un certificat/clé distinct par RPZT MUST être le défaut ; un partage MAY être choisi explicitement par publication. Les secrets MUST NOT être exposés dans les consultations, diagnostics ou artefacts.

#### Scenario: Publication partagée explicitement

- **WHEN** un profil choisit la même clé pour plusieurs RPZT
- **THEN** chaque destinataire habilité reçoit sa propre protection sans rendre la clé lisible aux autres acteurs.
~~~~
