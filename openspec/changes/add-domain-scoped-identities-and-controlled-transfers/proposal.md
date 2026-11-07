# C96 — Identités de domaine, périmètres et transferts contrôlés

## Pourquoi

Les archives C02/C03 et les dossiers Auth ne réalisent pas la nouvelle cardinalité, les contextes Domaine ni les transferts de tenants/identités. C21/O34/O36 seront raccordés à ces contrats, sans réouvrir les archives.

Le plan ACL-PIXS-2026-10-31-E3-R1 est validé. La couverture cumulée des changes actifs et des archives a été examinée ; ce dossier porte seulement le besoin résiduel ci-dessous. La présence de code ou une archive ne démontre pas la conformité de la nouvelle version cible.

## Modifications proposées

Préparer la réalisation future de : Individu commun, identités multiples par Domaine, contextes propriétaires, habilitations et transferts fonctionnels contrôlés.

- Individus et identités multiples.
- Contextes Instance Domaine Tenant.
- Habilitations globales et locales.
- Transferts et retrait de domaine.
- Migration et conformité.

## Capacités et source de vérité

Les spécifications cibles existent déjà et sont validées à l'étape 2. Ce change ne crée aucun comportement normatif supplémentaire. `requirements.md` conserve les exigences, scénarios et empreintes ; `skip_specs: true` évite de réappliquer le référentiel ou de fabriquer des deltas identiques.

- [core](../../specs/core/spec.md).
- [scope-context](../../specs/scope-context/spec.md).
- [pixs-domains](../../specs/pixs-domains/spec.md).
- [pixs-instance](../../specs/pixs-instance/spec.md).

## Frontières et exclusions

C97 conserve l’orchestration des modes et contrôleurs ; les modules métier restent propriétaires de leurs écritures pendant un transfert ; aucun déplacement de brique exécutable ni transfert organisationnel V1.

Aucun code, modèle exécutable, migration, test produit, configuration runtime, dépendance, installation, service, publication ou opération Git n'est produit par cette préparation. Les nouvelles tâches restent non cochées. Les quatre composants PBO/PFO/PA/PZT et leurs propriétaires restent distincts.

## Dépendances et phases

- [C97](../add-pixs-instance-and-domain-foundations/proposal.md).
- [C21](../define-essential-autonomous-auth-module/proposal.md).

Ces liens indiquent des contrats/prérequis à préciser par unité, pas une disponibilité démontrée. Les phases sont détaillées dans design.md ; aucun cycle de réalisation n'est résolu par une autorité ou un provider fictif.

## Critères d'acceptation de la réalisation future

Plusieurs identités du même individu restent indépendantes ; une identité n’est pas liée à deux individus ; le propriétaire est unique et aucune permission n’est copiée automatiquement.

Chaque unité devra satisfaire ses cas nominaux et refus, sa persistance, son autorisation, sa reprise et les scénarios sources applicables avant d'être cochée. Les mocks ou une compilation ne qualifient pas l'exécutant ou son fournisseur réel.

## Impacts et risques

Les contrats, schémas, versions, interfaces et migrations devront être explicités avant réalisation ; aucun nom d'endpoint, de paquet ou seuil absent du cadrage n'est choisi ici. Les bases indépendantes ne promettent pas de transaction distribuée. Les preuves antérieures restent datées et bornées.

## Statut documentaire

Préparation documentaire selon ACL-PIXS-2026-10-31-E3-R1. Aucune implémentation, qualification produit, livraison ou activation n'est déduite de cette ouverture. Les choix de fournisseurs et preuves manquants restent des barrières avant code.
