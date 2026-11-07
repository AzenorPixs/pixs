# C95 — Organigrammes Core et ZT et miroitage gouverné

## Pourquoi

Aucun change actif ne porte l’ensemble des trois référentiels, de leurs sources de miroitage et de leurs affiliations. C13 consommera les vues ; Z30 conserve les acteurs et structures ZT.

Le plan ACL-PIXS-2026-10-31-E3-R1 est validé. La couverture cumulée des changes actifs et des archives a été examinée ; ce dossier porte seulement le besoin résiduel ci-dessous. La présence de code ou une archive ne démontre pas la conformité de la nouvelle version cible.

## Modifications proposées

Préparer la réalisation future de : Organigrammes organisationnel et fonctionnel Core, structure ZT et miroitage gouverné, présentés en trois volets distincts.

- Référentiels et hiérarchies.
- Source et périmètres des miroirs.
- Affiliations et réévaluation des droits.
- Trois volets PBO et conformité.

## Capacités et source de vérité

Les spécifications cibles existent déjà et sont validées à l'étape 2. Ce change ne crée aucun comportement normatif supplémentaire. `requirements.md` conserve les exigences, scénarios et empreintes ; `skip_specs: true` évite de réappliquer le référentiel ou de fabriquer des deltas identiques.

- [organization-charts](../../specs/organization-charts/spec.md).

## Frontières et exclusions

Ne pas réimplémenter le registre des acteurs Z30, le moteur de politiques Z02 ou les primitives génériques Core ; aucun transfert de structure inter-domaines en V1.

Aucun code, modèle exécutable, migration, test produit, configuration runtime, dépendance, installation, service, publication ou opération Git n'est produit par cette préparation. Les nouvelles tâches restent non cochées. Les quatre composants PBO/PFO/PA/PZT et leurs propriétaires restent distincts.

## Dépendances et phases

- [C96](../add-domain-scoped-identities-and-controlled-transfers/proposal.md).
- [Z30](../add-zt-actors-governance-and-domain-approvals/proposal.md).

Ces liens indiquent des contrats/prérequis à préciser par unité, pas une disponibilité démontrée. Les phases sont détaillées dans design.md ; aucun cycle de réalisation n'est résolu par une autorité ou un provider fictif.

## Critères d'acceptation de la réalisation future

Une source explicite est vérifiée par périmètre de miroir ; les cycles et parents multiples sont refusés ; structure seule est le défaut ; aucun droit ou admission n’est copié implicitement.

Chaque unité devra satisfaire ses cas nominaux et refus, sa persistance, son autorisation, sa reprise et les scénarios sources applicables avant d'être cochée. Les mocks ou une compilation ne qualifient pas l'exécutant ou son fournisseur réel.

## Impacts et risques

Les contrats, schémas, versions, interfaces et migrations devront être explicités avant réalisation ; aucun nom d'endpoint, de paquet ou seuil absent du cadrage n'est choisi ici. Les bases indépendantes ne promettent pas de transaction distribuée. Les preuves antérieures restent datées et bornées.

## Statut documentaire

Préparation documentaire selon ACL-PIXS-2026-10-31-E3-R1. Aucune implémentation, qualification produit, livraison ou activation n'est déduite de cette ouverture. Les choix de fournisseurs et preuves manquants restent des barrières avant code.
