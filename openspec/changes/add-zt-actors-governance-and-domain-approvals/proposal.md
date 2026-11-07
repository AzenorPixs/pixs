# Z30 — Acteurs ZT, gouvernance et approbations entre domaines

## Pourquoi

Z02/Z25 couvrent exécution des autorisations et admission technique. Ils ne couvrent pas l’ensemble des acteurs humains/organisationnels, de la gouvernance et des approbations entre domaines.

Le plan ACL-PIXS-2026-10-31-E3-R1 est validé. La couverture cumulée des changes actifs et des archives a été examinée ; ce dossier porte seulement le besoin résiduel ci-dessous. La présence de code ou une archive ne démontre pas la conformité de la nouvelle version cible.

## Modifications proposées

Préparer la réalisation future de : Acteurs ZT, participations, gouvernance, délégations, approbations et représentation sous les droits propres aux Domaines.

- Acteurs et participations.
- Gouvernance et délégations.
- Approbations directionnelles et transitivité.
- Représentation mandats et états Core Auth.
- Domaines partagés et conformité.

## Capacités et source de vérité

Les spécifications cibles existent déjà et sont validées à l'étape 2. Ce change ne crée aucun comportement normatif supplémentaire. `requirements.md` conserve les exigences, scénarios et empreintes ; `skip_specs: true` évite de réappliquer le référentiel ou de fabriquer des deltas identiques.

- [zt-instances](../../specs/zt-instances/spec.md).
- [pixs-domains](../../specs/pixs-domains/spec.md).

## Frontières et exclusions

Z03 conserve le stockage et service CZT ; Z25 l’enrôlement technique ; Z02 l’application réseau. Les modèles publics d’acteurs doivent précéder leur intégration CZT, sans exiger la gouvernance complète pour les seuls contrats initiaux.

Aucun code, modèle exécutable, migration, test produit, configuration runtime, dépendance, installation, service, publication ou opération Git n'est produit par cette préparation. Les nouvelles tâches restent non cochées. Les quatre composants PBO/PFO/PA/PZT et leurs propriétaires restent distincts.

## Dépendances et phases

- [C97](../add-pixs-instance-and-domain-foundations/proposal.md).
- [Z03](../add-pzt-authoritative-control-and-signed-receipts/proposal.md).
- [Z02](../add-pzt-network-mandates-and-fail-closed-revocation/proposal.md).
- [Z25](../add-pzt-pa-admission-and-ephemeral-peer-generation/proposal.md).

Ces liens indiquent des contrats/prérequis à préciser par unité, pas une disponibilité démontrée. Les phases sont détaillées dans design.md ; aucun cycle de réalisation n'est résolu par une autorité ou un provider fictif.

## Critères d'acceptation de la réalisation future

Approche directionnelle, portée et profondeur bornées ; appartenance non humaine unique ; participations humaines indépendantes ; aucun droit issu de la seule reconnaissance ou d’un mandat expiré.

Chaque unité devra satisfaire ses cas nominaux et refus, sa persistance, son autorisation, sa reprise et les scénarios sources applicables avant d'être cochée. Les mocks ou une compilation ne qualifient pas l'exécutant ou son fournisseur réel.

## Impacts et risques

Les contrats, schémas, versions, interfaces et migrations devront être explicités avant réalisation ; aucun nom d'endpoint, de paquet ou seuil absent du cadrage n'est choisi ici. Les bases indépendantes ne promettent pas de transaction distribuée. Les preuves antérieures restent datées et bornées.

## Statut documentaire

Préparation documentaire selon ACL-PIXS-2026-10-31-E3-R1. Aucune implémentation, qualification produit, livraison ou activation n'est déduite de cette ouverture. Les choix de fournisseurs et preuves manquants restent des barrières avant code.
