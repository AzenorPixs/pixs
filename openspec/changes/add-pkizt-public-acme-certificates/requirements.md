# Références normatives — Z29

Plan ACL-PIXS-2026-10-31-E3-R1, validé ; relevé du 31 octobre 2026. Les blocs ci-dessous sont des copies de référence, jamais des deltas ADDED/MODIFIED ni une autorité indépendante du canon. Leur présence ne prouve aucune réalisation.

## Traçabilité des exigences et scénarios

| Capacité | Exigence cible | Scénarios | Référence |
|---|---|---:|---|
| zt-pki | ACME public et génération de clés | 1 | zt-pki-2ae6168f0a0c |
| zt-pki | Challenges et coordination ACME | 1 | zt-pki-e3e8cdbdb3dd |
| zt-pki | Renouvellement anticipé et déploiement vérifié | 1 | zt-pki-ba327c12b293 |
| zt-pki | Remise TLS ciblée aux RPZT | 1 | zt-pki-790b4d1f8594 |

## Blocs sources complets

### Référence zt-pki-2ae6168f0a0c

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 47. SHA-256 du bloc : `2ae6168f0a0c414767a99f8ae8b52c96dcdd3ed4d9b18f73c67870597438d38a`.

Scénarios sources : Demande publique.

~~~~text
### Requirement: ACME public et génération de clés

PKIZT MUST pouvoir gérer des certificats publiquement reconnus via ACME selon les profils autorisés. La clé privée MUST être générée/protégée côté PKIZT ; compte ACME et clés de certificats MUST suivre leurs protections chiffrées et synchronisées. L'autorité publique MUST NOT être présentée comme fournisseur de la clé privée.

#### Scenario: Demande publique

- **WHEN** un profil autorise un certificat ACME
- **THEN** PKIZT conserve la clé privée et soumet la demande contenant la clé publique à signer.
~~~~

### Référence zt-pki-e3e8cdbdb3dd

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 56. SHA-256 du bloc : `e3e8cdbdb3dd1c0442050aed5ee076e3f5eb7d4b33694fe76a9a9458c6fe05ac`.

Scénarios sources : Deux coordonnateurs.

~~~~text
### Requirement: Challenges et coordination ACME

DNS-01, HTTP-01 et TLS-ALPN-01 MUST être sélectionnables par profil avec orchestration autorisée DZT/RPZT. Un certificat MUST avoir un coordonnateur ACME actif unique et un état durable permettant la reprise sans double opération non maîtrisée.

#### Scenario: Deux coordonnateurs

- **WHEN** deux PKIZT tentent de gérer le même certificat
- **THEN** un seul est admissible à coordonner les opérations courantes.
~~~~

### Référence zt-pki-ba327c12b293

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 65. SHA-256 du bloc : `ba327c12b293ee06bbc12a70370bb17386dd700089e7ab0af38230953b5cec06`.

Scénarios sources : Certificat non servi.

~~~~text
### Requirement: Renouvellement anticipé et déploiement vérifié

Le renouvellement MUST être automatique et anticipé selon le profil, avec ARI lorsqu'il est disponible. La réussite MUST distinguer obtention du certificat, distribution et activation réellement vérifiée sur les services ; l'émission MUST NOT prouver le déploiement.

#### Scenario: Certificat non servi

- **WHEN** un certificat renouvelé existe mais RPZT sert encore l’ancien
- **THEN** le déploiement reste incomplet et ne peut être annoncé réussi.
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
