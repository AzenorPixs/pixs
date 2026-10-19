# Coffre indépendant pour les secrets d’exploitation distribués

## Why

Le canon exige déjà les références opaques, l’identité de workload, les credentials courts compatibles, la rotation, la révocation et l’échec fermé. Il ne sélectionne pas de séparation explicite entre secrets d’amorçage locaux et secrets d’exploitation d’une composition distribuée. Le développeur a retenu cette séparation le 19 octobre 2026, avec un coffre indépendant de la base métier Pixs.

## What Changes

- Limiter les secrets locaux au minimum d’amorçage déclaré ; confier les secrets d’exploitation partagés ou distribués à un coffre dédié.
- Séparer le coffre et sa chaîne de déverrouillage de la base métier Pixs, sans dépendance circulaire de démarrage ou de récupération.
- Préciser les identités par service, les droits minimaux, les durées de vie, le renouvellement, la révocation, l’audit et le refus des replis non déclarés.
- Préparer la qualification de disponibilité et de reprise propre au coffre avant sélection d’une composition distribuée.

## Capabilities

### New Capabilities

Aucune : le contrat `SecretProvider` reste indépendant du produit et le coffre est un provider sélectionné hors Kernel.

### Modified Capabilities

- `secrets-providers` : séparation amorçage/exploitation et garanties d’un coffre indépendant pour les compositions distribuées.
- `reference-composition` : sélection explicite et preuve du coffre avant admission du profil distribué concerné.

Les deltas restent proposés dans ce change ; aucune synchronisation du canon courant pendant cette préparation.

## Impact

Préparation documentaire uniquement, sans code, dépendance, serveur, coffre réel, clé, secret, migration ou déploiement. OpenBao est une référence de comparaison, pas un produit sélectionné ni installé. LDAP et Kerberos conservent leurs rôles d’identité/authentification ; PostgreSQL reste l’autorité métier, sans devenir le coffre des secrets nécessaires à sa propre ouverture.

Le profil initial local et C01 restent inchangés. La protection de son amorçage est complétée par [qualify-pbo-bootstrap-secrets-host-tpm2](../qualify-pbo-bootstrap-secrets-host-tpm2/proposal.md). Le présent coffre est conditionnel à la sélection d’une composition distribuée et n’est pas ajouté comme dépendance obligatoire du P0 local.
