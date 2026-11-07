# Z31 — Sorties EZT et groupes de priorisation

## Pourquoi

Z08 couvre des passerelles vers ressources sans PZT, pas des politiques de sorties EZT groupées. Aucun change actif ne couvre ce rôle distinct.

Le plan ACL-PIXS-2026-10-31-E3-R1 est validé. La couverture cumulée des changes actifs et des archives a été examinée ; ce dossier porte seulement le besoin résiduel ci-dessous. La présence de code ou une archive ne démontre pas la conformité de la nouvelle version cible.

## Modifications proposées

Préparer la réalisation future de : Sorties EZT, groupes, priorités, poids, santé par chemin/famille IP, bascule et maintien des connexions.

- Rôle et politiques de sortie.
- Groupes priorités et poids.
- Santé bascule et réadmission.
- Connexions et absence de fuite.

## Capacités et source de vérité

Les spécifications cibles existent déjà et sont validées à l'étape 2. Ce change ne crée aucun comportement normatif supplémentaire. `requirements.md` conserve les exigences, scénarios et empreintes ; `skip_specs: true` évite de réappliquer le référentiel ou de fabriquer des deltas identiques.

- [zt-network-services](../../specs/zt-network-services/spec.md).

## Frontières et exclusions

Ne pas absorber GZT, le moteur de filtrage Z01 ou la gouvernance Z30 ; la configuration de référence reste CZT et l’état opérationnel RAM.

Aucun code, modèle exécutable, migration, test produit, configuration runtime, dépendance, installation, service, publication ou opération Git n'est produit par cette préparation. Les nouvelles tâches restent non cochées. Les quatre composants PBO/PFO/PA/PZT et leurs propriétaires restent distincts.

## Dépendances et phases

- [Z01](../add-pzt-wireguard-local-transport-and-filtering/proposal.md).
- [Z02](../add-pzt-network-mandates-and-fail-closed-revocation/proposal.md).
- [Z03](../add-pzt-authoritative-control-and-signed-receipts/proposal.md).

Ces liens indiquent des contrats/prérequis à préciser par unité, pas une disponibilité démontrée. Les phases sont détaillées dans design.md ; aucun cycle de réalisation n'est résolu par une autorité ou un provider fictif.

## Critères d'acceptation de la réalisation future

Aucun EZT admissible signifie trafic bloqué ; les poids ne concernent que le meilleur niveau admissible ; la santé IPv4 ne prouve pas IPv6 ; un EZT externe reste dans son ZT.

Chaque unité devra satisfaire ses cas nominaux et refus, sa persistance, son autorisation, sa reprise et les scénarios sources applicables avant d'être cochée. Les mocks ou une compilation ne qualifient pas l'exécutant ou son fournisseur réel.

## Impacts et risques

Les contrats, schémas, versions, interfaces et migrations devront être explicités avant réalisation ; aucun nom d'endpoint, de paquet ou seuil absent du cadrage n'est choisi ici. Les bases indépendantes ne promettent pas de transaction distribuée. Les preuves antérieures restent datées et bornées.

## Statut documentaire

Préparation documentaire selon ACL-PIXS-2026-10-31-E3-R1. Aucune implémentation, qualification produit, livraison ou activation n'est déduite de cette ouverture. Les choix de fournisseurs et preuves manquants restent des barrières avant code.
