# Z26 — Recette PZT par contrat et profil

## Pourquoi

Les contrats PZT et leurs décisions sont spécifiés ; le README ne revendique pas de réseau livré. Les clauses de gestion PBO essentielles restent distinctes des rôles réseau activés et des auxiliaires spécialisés.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

Recettes contrat/sécurité/reprise/ressources/isolation/autorité/transport/administration A05b–A12g ; qualification initiale sans passerelle, puis profils suivants.

## Capacités

### Capacités nouvelles

Aucun comportement normatif nouveau n’est prévu. Ce dossier prépare la réalisation ou la qualification des contrats déjà présents dans le canon.

### Capacités modifiées

Aucune modification de texte canonique. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios ; `skip_specs: true` évite un delta identique artificiel. Si un audit ou une décision exige une évolution normative, présenter son delta avant réalisation, sans considérer cette métadonnée comme une dispense de conformité.

## Sélection et périmètre autorisé

Hors premier P0 proposé ; obligation du profil/capacité sélectionné, applicabilité à confirmer. La préparation demandée ne sélectionne, n’active et ne qualifie pas cette capacité dans le premier profil P0.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [qualify-pa-platforms-and-r01-r68-matrix](../qualify-pa-platforms-and-r01-r68-matrix/proposal.md).
- [qualify-first-pbo-composition](../qualify-first-pbo-composition/proposal.md).
- [publish-first-qualified-pbo-release](../publish-first-qualified-pbo-release/proposal.md).
- [add-pzt-wireguard-local-transport-and-filtering](../add-pzt-wireguard-local-transport-and-filtering/proposal.md).
- [add-pzt-network-mandates-and-fail-closed-revocation](../add-pzt-network-mandates-and-fail-closed-revocation/proposal.md).
- [add-pzt-authoritative-control-and-signed-receipts](../add-pzt-authoritative-control-and-signed-receipts/proposal.md).
- [add-pzt-private-address-plan-and-ipv6-lifecycle](../add-pzt-private-address-plan-and-ipv6-lifecycle/proposal.md).
- [add-pzt-managed-dns-service-and-pa-adapters](../add-pzt-managed-dns-service-and-pa-adapters/proposal.md).
- [add-pzt-public-control-contracts-and-state-streams](../add-pzt-public-control-contracts-and-state-streams/proposal.md).
- [add-pzt-path-discovery-and-encrypted-relays](../add-pzt-path-discovery-and-encrypted-relays/proposal.md).
- [add-pzt-service-identities-and-tpm-attestation](../add-pzt-service-identities-and-tpm-attestation/proposal.md).
- [add-pzt-tls-policy-and-bounded-cipher-migration](../add-pzt-tls-policy-and-bounded-cipher-migration/proposal.md).
- [add-pzt-operational-certificate-renewal](../add-pzt-operational-certificate-renewal/proposal.md).
- [add-pzt-ca-hierarchy-rotation-and-recovery](../add-pzt-ca-hierarchy-rotation-and-recovery/proposal.md).
- [add-pzt-offline-root-backup-and-recovery](../add-pzt-offline-root-backup-and-recovery/proposal.md).
- [add-pzt-monotonic-witness-and-key-sanitation](../add-pzt-monotonic-witness-and-key-sanitation/proposal.md).
- [add-pzt-evidence-dossier-and-bounded-validation](../add-pzt-evidence-dossier-and-bounded-validation/proposal.md).
- [add-pzt-proof-admission-and-attempt-reconciliation](../add-pzt-proof-admission-and-attempt-reconciliation/proposal.md).
- [add-pzt-qualified-time-and-freshness-decisions](../add-pzt-qualified-time-and-freshness-decisions/proposal.md).
- [add-pzt-isolated-time-helper-and-ipc](../add-pzt-isolated-time-helper-and-ipc/proposal.md).
- [add-pzt-durable-helper-state-and-writer-exclusion](../add-pzt-durable-helper-state-and-writer-exclusion/proposal.md).
- [add-pzt-bounded-telemetry-export-and-retention](../add-pzt-bounded-telemetry-export-and-retention/proposal.md).
- [add-pzt-telemetry-purge-jobs-and-leases](../add-pzt-telemetry-purge-jobs-and-leases/proposal.md).
- [add-pzt-canonical-purge-manifests-and-integrity](../add-pzt-canonical-purge-manifests-and-integrity/proposal.md).
- [add-pzt-controlled-manifest-incident-rearm](../add-pzt-controlled-manifest-incident-rearm/proposal.md).
- [add-pzt-rearm-status-stream-and-reconciliation](../add-pzt-rearm-status-stream-and-reconciliation/proposal.md).
- [add-pzt-pa-admission-and-ephemeral-peer-generation](../add-pzt-pa-admission-and-ephemeral-peer-generation/proposal.md).

Qualifier d’abord le socle sans passerelle. Z08 est préparé séparément et sa recette vient après cette première preuve ; une seconde recette peut alors intégrer le profil passerelle.

## Impact de réalisation future

Séparer contrôle métier PBO/Django/PostgreSQL, propriétaire réseau pzt-daemon et adapters système. Implémenter le rôle précisément désigné par les contrats sources, avec schémas fermés, versions et contrôles courants ; conserver toutes bornes, unités, conditions de reprise et alternatives rejetées. La cryptographie WireGuard n’est pas réimplémentée. Les bibliothèques de transport, sources de temps et adapters sont qualifiés, sans confiance supposée.

## Critère de sortie de réalisation future

Preuves actuelles par scénario applicable ; valeurs validées conservées ; alternatives rejetées non activées ; pas de recette de passerelle avant socle.

## Décisions restant à valider

Composition de recette, OS/CPU/providers/charges et scénarios applicables ; passage au profil passerelle seulement après première qualification du socle.
