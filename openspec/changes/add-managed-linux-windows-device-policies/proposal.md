# PA12 — Politiques des postes Linux et Windows et serveurs Linux

## Pourquoi

PA05 porte le mécanisme souhaité/appliqué mais pas le modèle complet de politiques des équipements. O37 porte la compatibilité Windows et les GPO ; ce lot en consomme les capacités qualifiées.

Le plan ACL-PIXS-2026-10-31-E3-R1 est validé. La couverture cumulée des changes actifs et des archives a été examinée ; ce dossier porte seulement le besoin résiduel ci-dessous. La présence de code ou une archive ne démontre pas la conformité de la nouvelle version cible.

## Modifications proposées

Préparer la réalisation future de : Politiques de poste et d’utilisateur pour Linux/Windows, serveurs Linux, gestion ZT distincte de la jonction et parcours hors ligne/redémarrage.

- Résolution et ciblage des politiques.
- Application système et utilisateur.
- Jonction session hors ligne et redémarrage.
- Qualification des profils et conflits.

## Capacités et source de vérité

Les spécifications cibles existent déjà et sont validées à l'étape 2. Ce change ne crée aucun comportement normatif supplémentaire. `requirements.md` conserve les exigences, scénarios et empreintes ; `skip_specs: true` évite de réappliquer le référentiel ou de fabriquer des deltas identiques.

- [managed-device-policies](../../specs/managed-device-policies/spec.md).

## Frontières et exclusions

PA05 conserve l’application générique ; O37 conserve le fournisseur Windows ; les serveurs Windows ne deviennent pas membres natifs V1.

Aucun code, modèle exécutable, migration, test produit, configuration runtime, dépendance, installation, service, publication ou opération Git n'est produit par cette préparation. Les nouvelles tâches restent non cochées. Les quatre composants PBO/PFO/PA/PZT et leurs propriétaires restent distincts.

## Dépendances et phases

- [C96](../add-domain-scoped-identities-and-controlled-transfers/proposal.md).
- [PA04](../add-pa-authorized-instruction-execution/proposal.md).
- [PA05](../add-pa-desired-applied-configuration-and-drift/proposal.md).
- [PA06](../add-pa-durable-technical-state-and-offline-recovery/proposal.md).
- [O37](../add-auth-managed-active-directory/proposal.md).

Ces liens indiquent des contrats/prérequis à préciser par unité, pas une disponibilité démontrée. Les phases sont détaillées dans design.md ; aucun cycle de réalisation n'est résolu par une autorité ou un provider fictif.

## Critères d'acceptation de la réalisation future

Les contradictions à priorité égale sont signalées ; l’hôte géré dans ZT peut rester sans jonction d’authentification ; hors ligne et redémarrage suivent un profil, avec manuel par défaut.

Chaque unité devra satisfaire ses cas nominaux et refus, sa persistance, son autorisation, sa reprise et les scénarios sources applicables avant d'être cochée. Les mocks ou une compilation ne qualifient pas l'exécutant ou son fournisseur réel.

## Impacts et risques

Les contrats, schémas, versions, interfaces et migrations devront être explicités avant réalisation ; aucun nom d'endpoint, de paquet ou seuil absent du cadrage n'est choisi ici. Les bases indépendantes ne promettent pas de transaction distribuée. Les preuves antérieures restent datées et bornées.

## Statut documentaire

Préparation documentaire selon ACL-PIXS-2026-10-31-E3-R1. Aucune implémentation, qualification produit, livraison ou activation n'est déduite de cette ouverture. Les choix de fournisseurs et preuves manquants restent des barrières avant code.
