# Plan global de préparation — 102 changes

Relevé du 17 octobre 2026 : 100 dossiers de l’inventaire initial, complétés par les deux changes validés après audit. **Préparation documentaire achevée ; aucune implémentation autorisée.**

## Périmètre et comptes

| Famille | Changes préparés |
|---|---:|
| Premier P0 : C00–C19 et N01 | 21 |
| Pixs Agent | 9 |
| PZT et contrats techniques | 26 |
| Compléments Bulk | 11 |
| Capacités supplémentaires sélectionnables | 32 |
| Clarification native/hors ligne N02 | 1 |
| Docker | 1 |
| Recette étendue | 1 |
| **Total** | **102** |

Les 1 012 tâches sont non cochées. Les options ne sont pas sélectionnées par la création de leur dossier. N01 ajoute la procédure d’urgence au premier P0 ; N02 clarifie une frontière normative pour les profils natifs hors ligne, sans les imposer au P0.

N01 complète le canon existant avec skip_specs explicite. N02 contient des deltas MODIFIED natifs ; C00 garde ses deltas de profil proposés. Aucun delta n’a été synchronisé. Tous les autres dossiers restent des préparations de réalisation du canon ; aucune copie normative identique créée pour satisfaire l’outil.

## Audit et preuves

- [Audit individuel durable des 94 exigences](audit-ne-94.json) : 10 P, 84 ND ; aucun verdict de qualification intégré.
- [Couverture des 717 exigences](couverture-preparation-globale.md), [dépendances structurées](preparation-globale.json), [arbitrages](arbitrages-preparation-globale.md).
- [Rapport actuel et contrôles](../../../reports/audit-ne-94-2026-10-17/RAPPORT.md).
- [Validation historique des 100 dossiers](validation-globale.md) : preuve antérieure, ne valide pas les modifications de cet audit.

## Ordre possible selon les dépendances fermes

Les conditions de profil et d’activation sont séparées du graphe acyclique. Cet ordre est une aide de planification et n’autorise aucune réalisation.

| Ordre | Lot | Change | Dépendances fermes |
|---:|---|---|---|
| 1 | C00 | [define-first-installable-pbo-profile](../define-first-installable-pbo-profile/proposal.md) | Aucune |
| 2 | C01 | [add-pbo-runtime-secret-provider](../add-pbo-runtime-secret-provider/proposal.md) | C00 |
| 3 | C02 | [add-core-postgres-services](../add-core-postgres-services/proposal.md) | C00 |
| 4 | C05 | [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md) | C00, C02 |
| 5 | C03 | [add-initial-authentication-and-sessions](../add-initial-authentication-and-sessions/proposal.md) | C01, C02, C05 |
| 6 | C07 | [activate-reference-runtime-composition](../activate-reference-runtime-composition/proposal.md) | C01, C02, C05 |
| 7 | Z12 | [add-pzt-ca-hierarchy-rotation-and-recovery](../add-pzt-ca-hierarchy-rotation-and-recovery/proposal.md) | C01, C02, C05 |
| 8 | C04 | [integrate-runtime-authorization-and-super-admin](../integrate-runtime-authorization-and-super-admin/proposal.md) | C02, C03, C05 |
| 9 | N02 | [clarify-native-credentials-and-offline-storage-boundary](../clarify-native-credentials-and-offline-storage-boundary/proposal.md) | C03 |
| 10 | PA01 | [add-pa-native-build-and-component-composition](../add-pa-native-build-and-component-composition/proposal.md) | C00, C07 |
| 11 | PA02 | [add-pa-bootstrap-and-authority-binding](../add-pa-bootstrap-and-authority-binding/proposal.md) | C01, C02, C03 |
| 12 | Z03 | [add-pzt-authoritative-control-and-signed-receipts](../add-pzt-authoritative-control-and-signed-receipts/proposal.md) | C02, C05, Z12 |
| 13 | Z13 | [add-pzt-offline-root-backup-and-recovery](../add-pzt-offline-root-backup-and-recovery/proposal.md) | Z12 |
| 14 | C06 | [add-protected-core-http-commands-and-queries](../add-protected-core-http-commands-and-queries/proposal.md) | C02, C03, C04, C05 |
| 15 | C08 | [add-installation-and-first-configuration](../add-installation-and-first-configuration/proposal.md) | C01, C02, C03, C04, C05, C07 |
| 16 | PA03 | [add-pa-system-session-lifecycle](../add-pa-system-session-lifecycle/proposal.md) | PA01, PA02 |
| 17 | Z02 | [add-pzt-network-mandates-and-fail-closed-revocation](../add-pzt-network-mandates-and-fail-closed-revocation/proposal.md) | C04, C05, Z03 |
| 18 | Z09 | [add-pzt-service-identities-and-tpm-attestation](../add-pzt-service-identities-and-tpm-attestation/proposal.md) | PA02, Z12, C04 |
| 19 | C09 | [add-reference-worker-scheduler-and-event-delivery](../add-reference-worker-scheduler-and-event-delivery/proposal.md) | C04, C05, C06, C07 |
| 20 | C11 | [compose-modular-frontend-with-core-api](../compose-modular-frontend-with-core-api/proposal.md) | C06, C07 |
| 21 | O06 | [add-bounded-business-rule-evaluation](../add-bounded-business-rule-evaluation/proposal.md) | C04, C05, C06 |
| 22 | Z06 | [add-pzt-public-control-contracts-and-state-streams](../add-pzt-public-control-contracts-and-state-streams/proposal.md) | C06, Z02, Z03 |
| 23 | Z18 | [add-pzt-isolated-time-helper-and-ipc](../add-pzt-isolated-time-helper-and-ipc/proposal.md) | PA01, PA03 |
| 24 | C10 | [enforce-core-data-governance-and-lifecycle](../enforce-core-data-governance-and-lifecycle/proposal.md) | C02, C04, C05, C09 |
| 25 | C12 | [complete-shared-ui-i18n-and-accessibility](../complete-shared-ui-i18n-and-accessibility/proposal.md) | C06, C11 |
| 26 | C14 | [add-essential-pbo-pzt-and-dns-modules](../add-essential-pbo-pzt-and-dns-modules/proposal.md) | C00, C02, C04, C05, C06, C11 |
| 27 | C15 | [add-runtime-observability-and-operations](../add-runtime-observability-and-operations/proposal.md) | C04, C05, C07, C09 |
| 28 | O05 | [add-versioned-workflow-execution](../add-versioned-workflow-execution/proposal.md) | C04, C05, C09 |
| 29 | O10 | [add-scim-provisioning-through-owner-commands](../add-scim-provisioning-through-owner-commands/proposal.md) | C03, C04, C06, C09 |
| 30 | O15 | [add-entitlements-and-atomic-quota-reservations](../add-entitlements-and-atomic-quota-reservations/proposal.md) | C04, C05, C06, C09 |
| 31 | O21 | [generate-typescript-python-public-sdks](../generate-typescript-python-public-sdks/proposal.md) | C06, C09 |
| 32 | Z11 | [add-pzt-operational-certificate-renewal](../add-pzt-operational-certificate-renewal/proposal.md) | Z09, Z12, Z06 |
| 33 | Z25 | [add-pzt-pa-admission-and-ephemeral-peer-generation](../add-pzt-pa-admission-and-ephemeral-peer-generation/proposal.md) | PA02, Z02, Z09, C09 |
| 34 | B01 | [complete-bulk-owner-admission-and-import-mapping](../complete-bulk-owner-admission-and-import-mapping/proposal.md) | C04, C06, C10 |
| 35 | C13 | [add-initial-administration-panel](../add-initial-administration-panel/proposal.md) | C08, C10, C11, C12 |
| 36 | C16 | [add-upgrade-backup-and-restore-contracts](../add-upgrade-backup-and-restore-contracts/proposal.md) | C08, C09, C10, C15 |
| 37 | N01 | [add-pbo-security-quarantine-and-revocation](../add-pbo-security-quarantine-and-revocation/proposal.md) | C03, C04, C05, C07, C09, C15 |
| 38 | O01 | [add-selected-object-storage-provider](../add-selected-object-storage-provider/proposal.md) | C01, C04, C05, C10 |
| 39 | O02 | [add-governed-document-repository-adapter](../add-governed-document-repository-adapter/proposal.md) | C04, C05, C10 |
| 40 | O03 | [add-authorized-search-projections](../add-authorized-search-projections/proposal.md) | C04, C09, C10 |
| 41 | O04 | [add-derived-distributed-cache-provider](../add-derived-distributed-cache-provider/proposal.md) | C04, C09, C10 |
| 42 | O07 | [add-external-synchronization-provider](../add-external-synchronization-provider/proposal.md) | C04, C05, C09, C10 |
| 43 | O08 | [add-ldap-outbound-directory-projections](../add-ldap-outbound-directory-projections/proposal.md) | C02, C04, C05, C09, C10 |
| 44 | O11 | [add-notification-preferences-and-selected-channels](../add-notification-preferences-and-selected-channels/proposal.md) | C04, C05, C10, C12 |
| 45 | O16 | [add-selected-reactive-synchronization](../add-selected-reactive-synchronization/proposal.md) | C04, C06, C09, C10 |
| 46 | O17 | [add-offline-eligible-local-projections](../add-offline-eligible-local-projections/proposal.md) | C04, C06, C10 |
| 47 | O19 | [add-authorized-realtime-collaboration](../add-authorized-realtime-collaboration/proposal.md) | C04, C06, C09, C10 |
| 48 | O20 | [add-governed-reporting-analytics](../add-governed-reporting-analytics/proposal.md) | C04, C09, C10 |
| 49 | O23 | [add-native-client-contract-and-session-support](../add-native-client-contract-and-session-support/proposal.md) | O21, C03, C04 |
| 50 | O24 | [add-declared-ai-provider-and-governed-retrieval](../add-declared-ai-provider-and-governed-retrieval/proposal.md) | C01, C04, C06, C10 |
| 51 | O27 | [add-tenant-regional-placement-and-routing](../add-tenant-regional-placement-and-routing/proposal.md) | C04, C06, C10 |
| 52 | Z01 | [add-pzt-wireguard-local-transport-and-filtering](../add-pzt-wireguard-local-transport-and-filtering/proposal.md) | C14, PA01, PA02, Z02, Z09, Z25 |
| 53 | Z04 | [add-pzt-private-address-plan-and-ipv6-lifecycle](../add-pzt-private-address-plan-and-ipv6-lifecycle/proposal.md) | C14, Z03 |
| 54 | B04 | [complete-bulk-owner-conflict-strategies](../complete-bulk-owner-conflict-strategies/proposal.md) | B01 |
| 55 | B05 | [integrate-bulk-private-object-storage](../integrate-bulk-private-object-storage/proposal.md) | O01, B01 |
| 56 | B06 | [add-bulk-authorized-export-and-revocable-results](../add-bulk-authorized-export-and-revocable-results/proposal.md) | B01, O01, C10 |
| 57 | B07 | [integrate-bulk-inbox-outbox-and-publication](../integrate-bulk-inbox-outbox-and-publication/proposal.md) | C09, B01 |
| 58 | C18 | [build-first-pbo-pfo-debian-package](../build-first-pbo-pfo-debian-package/proposal.md) | C07, C08, C09, C11, C13, C14, C15, C16, N01 |
| 59 | O09 | [add-directory-read-freshness-and-postgres-fallback](../add-directory-read-freshness-and-postgres-fallback/proposal.md) | O08 |
| 60 | O12 | [add-durable-notification-delivery-and-deduplication](../add-durable-notification-delivery-and-deduplication/proposal.md) | O11, C09 |
| 61 | O13 | [add-feature-flag-administration-and-audit](../add-feature-flag-administration-and-audit/proposal.md) | C04, C05, C06, C13 |
| 62 | O18 | [add-offline-intents-and-server-reconciliation](../add-offline-intents-and-server-reconciliation/proposal.md) | O17, C06 |
| 63 | O25 | [add-mediated-ai-tools-evaluations-and-budgets](../add-mediated-ai-tools-evaluations-and-budgets/proposal.md) | O24, C05, C09, O15 |
| 64 | O26 | [add-audit-integrity-and-verifiable-exports](../add-audit-integrity-and-verifiable-exports/proposal.md) | C05, C10, C16 |
| 65 | O28 | [add-regional-authority-failover](../add-regional-authority-failover/proposal.md) | O27, C16 |
| 66 | PA04 | [add-pa-authorized-instruction-execution](../add-pa-authorized-instruction-execution/proposal.md) | PA03, Z01, Z02, Z06, Z25, C04, C05 |
| 67 | Z07 | [add-pzt-path-discovery-and-encrypted-relays](../add-pzt-path-discovery-and-encrypted-relays/proposal.md) | Z01, Z02, Z06 |
| 68 | Z10 | [add-pzt-tls-policy-and-bounded-cipher-migration](../add-pzt-tls-policy-and-bounded-cipher-migration/proposal.md) | Z01, Z06, Z12 |
| 69 | B02 | [add-bulk-atomic-import-execution](../add-bulk-atomic-import-execution/proposal.md) | B01, B05 |
| 70 | B03 | [add-bulk-best-effort-import-execution](../add-bulk-best-effort-import-execution/proposal.md) | B01, B05 |
| 71 | B08 | [integrate-bulk-worker-jobs-and-cancellation](../integrate-bulk-worker-jobs-and-cancellation/proposal.md) | C09, B01, B07 |
| 72 | C17 | [qualify-first-pbo-composition](../qualify-first-pbo-composition/proposal.md) | C04, C06, C08, C09, C10, C12, C13, C14, C15, C16, C18, N01 |
| 73 | O14 | [integrate-feature-flag-runtime-convergence](../integrate-feature-flag-runtime-convergence/proposal.md) | O13, C07, C09 |
| 74 | PA05 | [add-pa-desired-applied-configuration-and-drift](../add-pa-desired-applied-configuration-and-drift/proposal.md) | PA04, C09 |
| 75 | PA06 | [add-pa-durable-technical-state-and-offline-recovery](../add-pa-durable-technical-state-and-offline-recovery/proposal.md) | PA04, C09 |
| 76 | Z05 | [add-pzt-managed-dns-service-and-pa-adapters](../add-pzt-managed-dns-service-and-pa-adapters/proposal.md) | C14, PA04, Z04, Z06 |
| 77 | Z08 | [add-pzt-gateway-and-controlled-failover-profile](../add-pzt-gateway-and-controlled-failover-profile/proposal.md) | Z01, Z03, Z07 |
| 78 | B09 | [expose-bulk-versioned-http-api](../expose-bulk-versioned-http-api/proposal.md) | C06, B01, B08 |
| 79 | B10 | [complete-bulk-validation-reports-and-recovery-proofs](../complete-bulk-validation-reports-and-recovery-proofs/proposal.md) | B01, B08, C10 |
| 80 | C19 | [publish-first-qualified-pbo-release](../publish-first-qualified-pbo-release/proposal.md) | C17, C18 |
| 81 | O22 | [complete-developer-kit-and-cli-workflows](../complete-developer-kit-and-cli-workflows/proposal.md) | C07, C17, O21 |
| 82 | O31 | [qualify-selected-performance-budgets](../qualify-selected-performance-budgets/proposal.md) | C00, C15, C17 |
| 83 | O32 | [complete-extension-trust-and-isolation-adapters](../complete-extension-trust-and-isolation-adapters/proposal.md) | C07, C11, C17 |
| 84 | PA07 | [add-pa-supervision-maintenance-and-quarantine](../add-pa-supervision-maintenance-and-quarantine/proposal.md) | PA05, PA06, C12, C15 |
| 85 | Z14 | [add-pzt-monotonic-witness-and-key-sanitation](../add-pzt-monotonic-witness-and-key-sanitation/proposal.md) | Z13, PA06 |
| 86 | Z19 | [add-pzt-durable-helper-state-and-writer-exclusion](../add-pzt-durable-helper-state-and-writer-exclusion/proposal.md) | PA06, Z18 |
| 87 | B11 | [qualify-complete-bulk-runtime](../qualify-complete-bulk-runtime/proposal.md) | B02, B03, B04, B06, B07, B08, B09, B10 |
| 88 | O29 | [add-verified-component-registry](../add-verified-component-registry/proposal.md) | C07, C19 |
| 89 | O30 | [add-health-gated-progressive-deployment](../add-health-gated-progressive-deployment/proposal.md) | C15, C16, C19 |
| 90 | PA08 | [qualify-pa-platforms-and-r01-r68-matrix](../qualify-pa-platforms-and-r01-r68-matrix/proposal.md) | PA07, Z01, Z05, Z06, Z09, Z25 |
| 91 | Z15 | [add-pzt-evidence-dossier-and-bounded-validation](../add-pzt-evidence-dossier-and-bounded-validation/proposal.md) | Z03, Z13, Z14 |
| 92 | Z17 | [add-pzt-qualified-time-and-freshness-decisions](../add-pzt-qualified-time-and-freshness-decisions/proposal.md) | Z18, Z19 |
| 93 | Z20 | [add-pzt-bounded-telemetry-export-and-retention](../add-pzt-bounded-telemetry-export-and-retention/proposal.md) | Z19, C15 |
| 94 | Z16 | [add-pzt-proof-admission-and-attempt-reconciliation](../add-pzt-proof-admission-and-attempt-reconciliation/proposal.md) | Z15, Z17, C09 |
| 95 | Z21 | [add-pzt-telemetry-purge-jobs-and-leases](../add-pzt-telemetry-purge-jobs-and-leases/proposal.md) | Z20, C09, C10 |
| 96 | Z22 | [add-pzt-canonical-purge-manifests-and-integrity](../add-pzt-canonical-purge-manifests-and-integrity/proposal.md) | Z21, C05 |
| 97 | Z23 | [add-pzt-controlled-manifest-incident-rearm](../add-pzt-controlled-manifest-incident-rearm/proposal.md) | Z22, Z15, Z16, C04 |
| 98 | Z24 | [add-pzt-rearm-status-stream-and-reconciliation](../add-pzt-rearm-status-stream-and-reconciliation/proposal.md) | Z23, Z06 |
| 99 | Z26 | [qualify-active-pzt-contracts-and-profiles](../qualify-active-pzt-contracts-and-profiles/proposal.md) | PA08, C17, C19, Z01, Z02, Z03, Z04, Z05, Z06, Z07, Z09, Z10, Z11, Z12, Z13, Z14, Z15, Z16, Z17, Z18, Z19, Z20, Z21, Z22, Z23, Z24, Z25 |
| 100 | PA09 | [build-and-publish-independent-pa-debian-package](../build-and-publish-independent-pa-debian-package/proposal.md) | PA08, Z26, C19 |
| 101 | X01 | [build-and-qualify-pixs-docker-image](../build-and-qualify-pixs-docker-image/proposal.md) | C19, PA09, Z26 |
| 102 | Q01 | [qualify-selected-extended-pixs-compositions](../qualify-selected-extended-pixs-compositions/proposal.md) | C19, PA09, Z26, B11, X01, O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12, O13, O14, O15, O16, O17, O18, O19, O20, O21, O22, O23, O24, O25, O26, O27, O28, O29, O30, O31, O32 |

## Conditions de profil et d’activation

- O02 exige O01 seulement pour le stockage objet Pixs ; un référentiel externe/projeté autonome reste possible.
- O19 exige O18 pour les intentions hors ligne ; reconnexion et révocation restent obligatoires aussi en ligne.
- O20 exige O01 si les résultats sont stockés en objet Pixs.
- O17/O18/O23 : adoption des deltas N02 avant réalisation d’un profil combinant client natif et données hors ligne.
- O24 : aucun appel fournisseur réel avant O15 et O25 ; adapter testable isolément sur doubles, sans cycle de préparation. O25 dépend fermement d’O15.
- N01 doit être intégré avant construction C18 puis qualification C17 ; il ne dépend ni du catalogue O29 ni d’un PA actif.
- Z08 reste soumis à qualification Z26 du socle hors passerelle avant première activation. Q01 décrit une cible de catalogue ; seuls options retenues et prérequis applicables sont exigés d’un profil réduit.
- C14 conserve les modules PZT/DNS essentiels au PBO même sans PA. X01 conserve son périmètre PBO/PFO/PZT et trois binaires PA.

## Barrières avant réalisation

Providers, plateformes, modèles persistants, protocoles publics, valeurs non arrêtées de budget et objectifs demandent encore revue et validation lorsqu’un lot est choisi. Les conceptions détaillent refus, reprise, autorité et preuve de sortie ; leur présence ne signifie pas prêt à coder. Les décisions PA/PZT suivent TECHNICAL §45.4.

Les 94 NE ont été analysées dans les seules sources consultées. ND signifie couverture non démontrée, sans prouver une absence sur une installation externe. Aucun code produit, service, migration, secret, configuration système, publication ou archive n’a été modifié par cet audit.
