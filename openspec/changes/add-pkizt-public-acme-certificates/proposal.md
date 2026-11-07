# Z29 — Certificats ACME publics et renouvellement PKIZT

## Pourquoi

Z11 et Z12 portent certificats opérationnels et PKI privée ; ils ne couvrent pas le cycle ACME public complet ni ses challenges et ARI.

Le plan ACL-PIXS-2026-10-31-E3-R1 est validé. La couverture cumulée des changes actifs et des archives a été examinée ; ce dossier porte seulement le besoin résiduel ci-dessous. La présence de code ou une archive ne démontre pas la conformité de la nouvelle version cible.

## Modifications proposées

Préparer la réalisation future de : Cycle des certificats publics ACME, challenges, coordination unique, reprise et renouvellement anticipé avec preuve de déploiement.

- Comptes certificats et clés protégées.
- Challenges DNS HTTP et TLS.
- Coordonnateur unique et reprise.
- Renouvellement ARI et déploiement vérifié.

## Capacités et source de vérité

Les spécifications cibles existent déjà et sont validées à l'étape 2. Ce change ne crée aucun comportement normatif supplémentaire. `requirements.md` conserve les exigences, scénarios et empreintes ; `skip_specs: true` évite de réappliquer le référentiel ou de fabriquer des deltas identiques.

- [zt-pki](../../specs/zt-pki/spec.md).

## Frontières et exclusions

Z12 conserve autorités privées, protections et habilitations ; Z11 conserve son renouvellement opérationnel. Les profils DNS-01 et HTTP/TLS-ALPN déclarent leurs dépendances DZT/RPZT sans cycle global imposé.

Aucun code, modèle exécutable, migration, test produit, configuration runtime, dépendance, installation, service, publication ou opération Git n'est produit par cette préparation. Les nouvelles tâches restent non cochées. Les quatre composants PBO/PFO/PA/PZT et leurs propriétaires restent distincts.

## Dépendances et phases

- [Z12](../add-pzt-ca-hierarchy-rotation-and-recovery/proposal.md).
- [Z11](../add-pzt-operational-certificate-renewal/proposal.md).
- [Z05](../add-pzt-managed-dns-service-and-pa-adapters/proposal.md).
- [Z32](../add-zt-reverse-proxy-publications/proposal.md).

Ces liens indiquent des contrats/prérequis à préciser par unité, pas une disponibilité démontrée. Les phases sont détaillées dans design.md ; aucun cycle de réalisation n'est résolu par une autorité ou un provider fictif.

## Critères d'acceptation de la réalisation future

Un seul coordonnateur est actif par certificat ; la clé est générée côté PKIZT ; certificat obtenu et certificat effectivement servi sont vérifiés séparément.

Chaque unité devra satisfaire ses cas nominaux et refus, sa persistance, son autorisation, sa reprise et les scénarios sources applicables avant d'être cochée. Les mocks ou une compilation ne qualifient pas l'exécutant ou son fournisseur réel.

## Impacts et risques

Les contrats, schémas, versions, interfaces et migrations devront être explicités avant réalisation ; aucun nom d'endpoint, de paquet ou seuil absent du cadrage n'est choisi ici. Les bases indépendantes ne promettent pas de transaction distribuée. Les preuves antérieures restent datées et bornées.

## Statut documentaire

Préparation documentaire selon ACL-PIXS-2026-10-31-E3-R1. Aucune implémentation, qualification produit, livraison ou activation n'est déduite de cette ouverture. Les choix de fournisseurs et preuves manquants restent des barrières avant code.
