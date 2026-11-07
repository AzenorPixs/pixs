# Z32 — Publications RPZT et gestion TLS ciblée

## Pourquoi

Aucun change actif ne porte la publication RPZT. Les autres rôles réseau ne fournissent pas ce service par simple réutilisation de transport.

Le plan ACL-PIXS-2026-10-31-E3-R1 est validé. La couverture cumulée des changes actifs et des archives a été examinée ; ce dossier porte seulement le besoin résiduel ci-dessous. La présence de code ou une archive ne démontre pas la conformité de la nouvelle version cible.

## Modifications proposées

Préparer la réalisation future de : Publications HTTP/HTTPS/WebSocket par RPZT, modes TLS et remise protégée des éléments nécessaires à chaque exécutant.

- Publications et autorisations.
- HTTP HTTPS WebSocket et modes TLS.
- Remise protégée des éléments TLS.
- Actifs multiples et orientation.
- Conformité sans authentification utilisateur au proxy.

## Capacités et source de vérité

Les spécifications cibles existent déjà et sont validées à l'étape 2. Ce change ne crée aucun comportement normatif supplémentaire. `requirements.md` conserve les exigences, scénarios et empreintes ; `skip_specs: true` évite de réappliquer le référentiel ou de fabriquer des deltas identiques.

- [zt-network-services](../../specs/zt-network-services/spec.md).
- [zt-pki](../../specs/zt-pki/spec.md).

## Frontières et exclusions

L’authentification utilisateur reste au service cible ; Z12/Z29 conservent la production et le cycle des certificats. Une publication publique est un choix explicite.

Aucun code, modèle exécutable, migration, test produit, configuration runtime, dépendance, installation, service, publication ou opération Git n'est produit par cette préparation. Les nouvelles tâches restent non cochées. Les quatre composants PBO/PFO/PA/PZT et leurs propriétaires restent distincts.

## Dépendances et phases

- [Z01](../add-pzt-wireguard-local-transport-and-filtering/proposal.md).
- [Z02](../add-pzt-network-mandates-and-fail-closed-revocation/proposal.md).
- [Z03](../add-pzt-authoritative-control-and-signed-receipts/proposal.md).
- [Z12](../add-pzt-ca-hierarchy-rotation-and-recovery/proposal.md).

Ces liens indiquent des contrats/prérequis à préciser par unité, pas une disponibilité démontrée. Les phases sont détaillées dans design.md ; aucun cycle de réalisation n'est résolu par une autorité ou un provider fictif.

## Critères d'acceptation de la réalisation future

RPZT reste désactivé par défaut ; plusieurs actifs n’impliquent pas une orientation fonctionnelle ; les modes TLS sont explicites et seuls les destinataires habilités reçoivent les éléments TLS.

Chaque unité devra satisfaire ses cas nominaux et refus, sa persistance, son autorisation, sa reprise et les scénarios sources applicables avant d'être cochée. Les mocks ou une compilation ne qualifient pas l'exécutant ou son fournisseur réel.

## Impacts et risques

Les contrats, schémas, versions, interfaces et migrations devront être explicités avant réalisation ; aucun nom d'endpoint, de paquet ou seuil absent du cadrage n'est choisi ici. Les bases indépendantes ne promettent pas de transaction distribuée. Les preuves antérieures restent datées et bornées.

## Statut documentaire

Préparation documentaire selon ACL-PIXS-2026-10-31-E3-R1. Aucune implémentation, qualification produit, livraison ou activation n'est déduite de cette ouverture. Les choix de fournisseurs et preuves manquants restent des barrières avant code.
