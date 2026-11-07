# Z28 — DHCPv4 et DHCPv6 DZT et liaison DNS

## Pourquoi

Z05 et Z27 portent DNS/BIND 9. Aucun change actif ne prépare les mécanismes d’allocation DHCP et de reprise cohérente des baux.

Le plan ACL-PIXS-2026-10-31-E3-R1 est validé. La couverture cumulée des changes actifs et des archives a été examinée ; ce dossier porte seulement le besoin résiduel ci-dessous. La présence de code ou une archive ne démontre pas la conformité de la nouvelle version cible.

## Modifications proposées

Préparer la réalisation future de : DHCPv4/v6 du DZT, référence commune DNS/DHCP, conservation des baux, propriétaire par pool et liaison DHCP–DNS.

- Référence DZT et génération DHCP.
- Baux et propriétaire unique par pool.
- Publication DNS liée aux baux.
- Activation et reprise qualifiées.

## Capacités et source de vérité

Les spécifications cibles existent déjà et sont validées à l'étape 2. Ce change ne crée aucun comportement normatif supplémentaire. `requirements.md` conserve les exigences, scénarios et empreintes ; `skip_specs: true` évite de réappliquer le référentiel ou de fabriquer des deltas identiques.

- [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md).

## Frontières et exclusions

Z05 conserve les vues et la configuration DNS ; PA conserve installation, maintenance système et mise à jour des logiciels ; DZT conserve configuration et fonctionnement logiciel.

Aucun code, modèle exécutable, migration, test produit, configuration runtime, dépendance, installation, service, publication ou opération Git n'est produit par cette préparation. Les nouvelles tâches restent non cochées. Les quatre composants PBO/PFO/PA/PZT et leurs propriétaires restent distincts.

## Dépendances et phases

- [Z05](../add-pzt-managed-dns-service-and-pa-adapters/proposal.md).
- [Z03](../add-pzt-authoritative-control-and-signed-receipts/proposal.md).
- [PA04](../add-pa-authorized-instruction-execution/proposal.md).

Ces liens indiquent des contrats/prérequis à préciser par unité, pas une disponibilité démontrée. Les phases sont détaillées dans design.md ; aucun cycle de réalisation n'est résolu par une autorité ou un provider fictif.

## Critères d'acceptation de la réalisation future

DHCP est désactivé par défaut ; un pool n’a qu’un allocateur actif ; une reprise sans baux fiables est refusée ; réussite du bail et publication DNS restent distinctes.

Chaque unité devra satisfaire ses cas nominaux et refus, sa persistance, son autorisation, sa reprise et les scénarios sources applicables avant d'être cochée. Les mocks ou une compilation ne qualifient pas l'exécutant ou son fournisseur réel.

## Impacts et risques

Les contrats, schémas, versions, interfaces et migrations devront être explicités avant réalisation ; aucun nom d'endpoint, de paquet ou seuil absent du cadrage n'est choisi ici. Les bases indépendantes ne promettent pas de transaction distribuée. Les preuves antérieures restent datées et bornées.

## Statut documentaire

Préparation documentaire selon ACL-PIXS-2026-10-31-E3-R1. Aucune implémentation, qualification produit, livraison ou activation n'est déduite de cette ouverture. Les choix de fournisseurs et preuves manquants restent des barrières avant code.
