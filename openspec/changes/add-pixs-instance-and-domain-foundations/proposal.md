# C97 — Fondations Instance Pixs et Domaines et modes d’exploitation

## Pourquoi

Les modes PBO historiques et le parcours initial C08 ne couvrent pas la nouvelle Instance logique, les Domaines et les contrôleurs répartis. C08 reste propriétaire de son installation initiale et C96 des transformations d’identités.

Le plan ACL-PIXS-2026-10-31-E3-R1 est validé. La couverture cumulée des changes actifs et des archives a été examinée ; ce dossier porte seulement le besoin résiduel ci-dessous. La présence de code ou une archive ne démontre pas la conformité de la nouvelle version cible.

## Modifications proposées

Préparer la réalisation future de : Identité logique d’Instance, Domaines/FQDN, trois modes, bases et contrôleurs séparés et transition après ZT entièrement initialisé.

- Identité Instance et données pré-domaine.
- Domaines FQDN et rattachement ZT.
- Bases et contrôleurs séparés.
- Transition après ZT initialisé.
- Continuité et conformité.

## Capacités et source de vérité

Les spécifications cibles existent déjà et sont validées à l'étape 2. Ce change ne crée aucun comportement normatif supplémentaire. `requirements.md` conserve les exigences, scénarios et empreintes ; `skip_specs: true` évite de réappliquer le référentiel ou de fabriquer des deltas identiques.

- [pixs-instance](../../specs/pixs-instance/spec.md).
- [pixs-domains](../../specs/pixs-domains/spec.md).

## Frontières et exclusions

Les fondations pré-domaine ne dépendent pas d’un Domaine déjà activé. Les rôles ZT, LDAP et Kerberos restent réalisés dans leurs changes propriétaires.

Aucun code, modèle exécutable, migration, test produit, configuration runtime, dépendance, installation, service, publication ou opération Git n'est produit par cette préparation. Les nouvelles tâches restent non cochées. Les quatre composants PBO/PFO/PA/PZT et leurs propriétaires restent distincts.

## Dépendances et phases

- [C08](../add-installation-and-first-configuration/proposal.md).
- [C96](../add-domain-scoped-identities-and-controlled-transfers/proposal.md).
- [Z03](../add-pzt-authoritative-control-and-signed-receipts/proposal.md).
- [Z05](../add-pzt-managed-dns-service-and-pa-adapters/proposal.md).
- [Z07](../add-pzt-path-discovery-and-encrypted-relays/proposal.md).
- [Z12](../add-pzt-ca-hierarchy-rotation-and-recovery/proposal.md).
- [O38](../add-auth-managed-kerberos-kdc/proposal.md).
- [O39](../add-auth-managed-openldap/proposal.md).

Ces liens indiquent des contrats/prérequis à préciser par unité, pas une disponibilité démontrée. Les phases sont détaillées dans design.md ; aucun cycle de réalisation n'est résolu par une autorité ou un provider fictif.

## Critères d'acceptation de la réalisation future

Un ZT incomplet bloque le premier Domaine ; le partage ZT respecte les labels DNS ; les bases restent séparées et aucun retour Domaine vers Standalone n’est introduit.

Chaque unité devra satisfaire ses cas nominaux et refus, sa persistance, son autorisation, sa reprise et les scénarios sources applicables avant d'être cochée. Les mocks ou une compilation ne qualifient pas l'exécutant ou son fournisseur réel.

## Impacts et risques

Les contrats, schémas, versions, interfaces et migrations devront être explicités avant réalisation ; aucun nom d'endpoint, de paquet ou seuil absent du cadrage n'est choisi ici. Les bases indépendantes ne promettent pas de transaction distribuée. Les preuves antérieures restent datées et bornées.

## Statut documentaire

Préparation documentaire selon ACL-PIXS-2026-10-31-E3-R1. Aucune implémentation, qualification produit, livraison ou activation n'est déduite de cette ouverture. Les choix de fournisseurs et preuves manquants restent des barrières avant code.
