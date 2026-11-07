# N08 — Profils d’autorité et remplacement contrôlé des briques

## Pourquoi

Z03/Z12/C16 décrivent des mécanismes propres à leurs rôles. Ils ne couvrent pas le modèle transversal de mode par famille, dérogations, statut de l’ancienne brique et compatibilité de versions.

Le plan ACL-PIXS-2026-10-31-E3-R1 est validé. La couverture cumulée des changes actifs et des archives a été examinée ; ce dossier porte seulement le besoin résiduel ci-dessous. La présence de code ou une archive ne démontre pas la conformité de la nouvelle version cible.

## Modifications proposées

Préparer la réalisation future de : Contrats transversaux des familles d’autorité, synchronisation, compatibilité et remplacement d’une brique par une nouvelle installation vérifiée.

- Modes par famille et dérogations.
- Synchronisation et prise d’autorité.
- Observation secours et démantèlement.
- Versions compatibles et conformité.

## Capacités et source de vérité

Les spécifications cibles existent déjà et sont validées à l'étape 2. Ce change ne crée aucun comportement normatif supplémentaire. `requirements.md` conserve les exigences, scénarios et empreintes ; `skip_specs: true` évite de réappliquer le référentiel ou de fabriquer des deltas identiques.

- [brick-redundancy](../../specs/brick-redundancy/spec.md).

## Frontières et exclusions

Ne pas réimplémenter la réplication native PG/LDAP ni les signataires ; chaque rôle conserve son fournisseur et ses garanties spécifiques.

Aucun code, modèle exécutable, migration, test produit, configuration runtime, dépendance, installation, service, publication ou opération Git n'est produit par cette préparation. Les nouvelles tâches restent non cochées. Les quatre composants PBO/PFO/PA/PZT et leurs propriétaires restent distincts.

## Dépendances et phases

- [C97](../add-pixs-instance-and-domain-foundations/proposal.md).

Ces liens indiquent des contrats/prérequis à préciser par unité, pas une disponibilité démontrée. Les phases sont détaillées dans design.md ; aucun cycle de réalisation n'est résolu par une autorité ou un provider fictif.

## Critères d'acceptation de la réalisation future

Une exception est explicite et tracée ; un maître non exclu ne peut pas être doublé ; une règle générique n’abaisse pas les confirmations PG ; le démantèlement respecte les critères déclarés.

Chaque unité devra satisfaire ses cas nominaux et refus, sa persistance, son autorisation, sa reprise et les scénarios sources applicables avant d'être cochée. Les mocks ou une compilation ne qualifient pas l'exécutant ou son fournisseur réel.

## Impacts et risques

Les contrats, schémas, versions, interfaces et migrations devront être explicités avant réalisation ; aucun nom d'endpoint, de paquet ou seuil absent du cadrage n'est choisi ici. Les bases indépendantes ne promettent pas de transaction distribuée. Les preuves antérieures restent datées et bornées.

## Statut documentaire

Préparation documentaire selon ACL-PIXS-2026-10-31-E3-R1. Aucune implémentation, qualification produit, livraison ou activation n'est déduite de cette ouverture. Les choix de fournisseurs et preuves manquants restent des barrières avant code.
