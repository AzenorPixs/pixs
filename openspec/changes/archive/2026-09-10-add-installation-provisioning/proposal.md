## Why

Pixs définit déjà les mécanismes d'identité, de configuration, de périmètre,
d'autorisation et de lifecycle, sans formaliser leur point de départ commun.
Une installation ou un tenant ne doit pas devenir actif par un état implicite,
un secret embarqué ou un compte administrateur par défaut.

## What Changes

- Définir le provisionnement explicite, idempotent et auditable d'une
  installation Pixs avant son exposition au trafic applicatif.
- Définir la validation de la configuration de bootstrap et la résolution
  externe des secrets, sans valeur sensible dans un artefact ou un manifest.
- Définir la création contrôlée de l'identité opérateur initiale et du premier
  tenant, avec périmètre, autorisation et séparation des responsabilités.
- Définir les états, échecs, reprises et diagnostics du provisionnement.

## Capabilities

### New Capabilities

- `installation-provisioning`: provisionnement sécurisé d'une installation,
  de son opérateur initial et de ses tenants avant mise en service.

### Modified Capabilities

Aucune.

## Impact

Cette évolution introduit une spécification de capacité et ses futurs contrats
de provisionnement. Elle n'ajoute ni code, ni provider concret, ni dépendance,
ni secret, ni route API à ce stade.
