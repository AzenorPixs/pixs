## Purpose

Le stockage objet conserve les octets via des fournisseurs interchangeables, tandis que Pixs garde l'autorité sur métadonnées, permissions et cycle de vie.

## ADDED Requirements

### Requirement: Contrat fournisseur objet et métadonnées Pixs

Le contenu binaire est confié à un ObjectStorageProvider compatible ; identité, tenant, permissions, audit et cycle de vie restent gérés par Pixs via la métadonnée, indépendamment de la durée technique des octets.

#### Scenario: Suppression propagée au fournisseur

- **WHEN** une métadonnée est supprimée ou purgée
- **THEN** un marqueur et une décision d'effacement sont propagés au fournisseur sans exposer l'autorité métier

### Requirement: Isolation tenant et périmètre

Chaque objet DOIT porter le tenant racine et le scope applicable ; aucun partage direct avec un espace exclusif tiers ; toute suppression respecte rétention, holds et révocation.

#### Scenario: Accès inter-tenant refusé

- **WHEN** une identité demande un objet hors de son périmètre autorisé
- **THEN** l'accès est refusé avec un audit, sans fuite d'existence

### Requirement: Conformité des adaptateurs

Chaque adaptateur DOIT déclarer transport, chiffrement, localisation, rétention, suppression, restitution et révocation ; les clés et identifiants restent fournis par référence externe.

#### Scenario: Adaptateur non conforme bloqué

- **WHEN** un adaptateur ne démontre pas la suppression ou la révocation déclarée
- **THEN** sa composition est refusée
