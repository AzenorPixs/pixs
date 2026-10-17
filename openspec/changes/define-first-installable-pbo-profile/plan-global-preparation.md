# Plan global de préparation — 100 changes

Date : 17 octobre 2026. Le développeur a demandé les 80 dossiers restants après la préparation C00–C19. **Les 100 candidats de l’inventaire sont maintenant des changes actifs préparés, sans implémentation.**

## Périmètre et statut

La création documentaire n’active aucune capacité dans une installation et ne vaut pas approbation de décisions encore ouvertes. Le premier profil PBO/PFO de C00 reste distinct des profils PA/PZT actif, Docker et des capacités optionnelles. Les dossiers sont conditionnels à leur sélection et à leurs clauses applicables.

Tous les changes contiennent proposition, conception et tâches non cochées. Les 80 nouveaux dossiers incluent les blocs normatifs complets de leurs références dans requirements.md : les valeurs et conditions validées y sont conservées sans fabriquer de delta normatif identique. Leur métadonnée skip_specs indique uniquement l’absence d’évolution normative prévue ; tout comportement nouveau exige son delta avant réalisation.

Le statut natif de planification terminée constate les fichiers présents. Il ne lève ni barrière de conception ni interdiction d’implémenter dans la demande actuelle.

## Comptes

| Famille | Dossiers préparés |
|---|---:|
| Premier P0 | 20 |
| PZT et contrats techniques | 26 |
| Pixs Agent | 9 |
| Capacités supplémentaires | 32 |
| Compléments Bulk | 11 |
| Docker | 1 |
| Recette étendue | 1 |
| **Total** | **100** |

Les 996 tâches de réalisation restent non cochées. Aucune création supplémentaire n’est nécessaire pour matérialiser le catalogue actuel de 100 candidats ; audits, profils et revue de conception peuvent ultérieurement conduire à fusionner ou découper certains lots sur demande appropriée.

## Accès aux preuves et décisions

- [Vérifications globales](validation-globale.md) et [sorties OpenSpec natives](validation-globale.json).
- [État structuré, empreintes et références](preparation-globale.json).
- [Couverture des 717 exigences canoniques](couverture-preparation-globale.md).
- [Registre des décisions et qualifications](arbitrages-preparation-globale.md).

## Dépendances de préparation

Les ajustements C05 vers C03/C04 de la revue P0 sont conservés. Le graphe global est sans cycle ; les dépendances d’un profil réduit ne comprennent que ses options sélectionnées et leurs obligations. L’ordre ci-dessous est un ordre possible de traitement, pas une autorisation de réalisation.

| Ordre | Lot | Change | Dépendances |
|---:|---|---|---|
| 1 | C00 | [define-first-installable-pbo-profile](../define-first-installable-pbo-profile/proposal.md) | Aucune |
| 2 | C01 | [add-pbo-runtime-secret-provider](../add-pbo-runtime-secret-provider/proposal.md) | C00 |
| 3 | C02 | [add-core-postgres-services](../add-core-postgres-services/proposal.md) | C00 |
| 4 | C05 | [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md) | C00, C02 |
| 5 | C03 | [add-initial-authentication-and-sessions](../add-initial-authentication-and-sessions/proposal.md) | C01, C02, C05 |
| 6 | C07 | [activate-reference-runtime-composition](../activate-reference-runtime-composition/proposal.md) | C01, C02, C05 |
| 7 | Z12 | [add-pzt-ca-hierarchy-rotation-and-recovery](../add-pzt-ca-hierarchy-rotation-and-recovery/proposal.md) | C01, C02, C05 |
| 8 | C04 | [integrate-runtime-authorization-and-super-admin](../integrate-runtime-authorization-and-super-admin/proposal.md) | C02, C03, C05 |
| 9 | PA01 | [add-pa-native-build-and-component-composition](../add-pa-native-build-and-component-composition/proposal.md) | C00, C07 |
| 10 | PA02 | [add-pa-bootstrap-and-authority-binding](../add-pa-bootstrap-and-authority-binding/proposal.md) | C01, C02, C03 |
| 11 | Z03 | [add-pzt-authoritative-control-and-signed-receipts](../add-pzt-authoritative-control-and-signed-receipts/proposal.md) | C02, C05, Z12 |
| 12 | Z13 | [add-pzt-offline-root-backup-and-recovery](../add-pzt-offline-root-backup-and-recovery/proposal.md) | Z12 |
| 13 | C06 | [add-protected-core-http-commands-and-queries](../add-protected-core-http-commands-and-queries/proposal.md) | C02, C03, C04, C05 |
| 14 | C08 | [add-installation-and-first-configuration](../add-installation-and-first-configuration/proposal.md) | C01, C02, C03, C04, C05, C07 |
| 15 | PA03 | [add-pa-system-session-lifecycle](../add-pa-system-session-lifecycle/proposal.md) | PA01, PA02 |
| 16 | Z02 | [add-pzt-network-mandates-and-fail-closed-revocation](../add-pzt-network-mandates-and-fail-closed-revocation/proposal.md) | C04, C05, Z03 |
| 17 | Z09 | [add-pzt-service-identities-and-tpm-attestation](../add-pzt-service-identities-and-tpm-attestation/proposal.md) | PA02, Z12, C04 |
| 18 | C09 | [add-reference-worker-scheduler-and-event-delivery](../add-reference-worker-scheduler-and-event-delivery/proposal.md) | C04, C05, C06, C07 |
| 19 | C11 | [compose-modular-frontend-with-core-api](../compose-modular-frontend-with-core-api/proposal.md) | C06, C07 |
| 20 | O06 | [add-bounded-business-rule-evaluation](../add-bounded-business-rule-evaluation/proposal.md) | C04, C05, C06 |
| 21 | Z06 | [add-pzt-public-control-contracts-and-state-streams](../add-pzt-public-control-contracts-and-state-streams/proposal.md) | C06, Z02, Z03 |
| 22 | Z18 | [add-pzt-isolated-time-helper-and-ipc](../add-pzt-isolated-time-helper-and-ipc/proposal.md) | PA01, PA03 |
| 23 | C10 | [enforce-core-data-governance-and-lifecycle](../enforce-core-data-governance-and-lifecycle/proposal.md) | C02, C04, C05, C09 |
| 24 | C12 | [complete-shared-ui-i18n-and-accessibility](../complete-shared-ui-i18n-and-accessibility/proposal.md) | C06, C11 |
| 25 | C14 | [add-essential-pbo-pzt-and-dns-modules](../add-essential-pbo-pzt-and-dns-modules/proposal.md) | C00, C02, C04, C05, C06, C11 |
| 26 | C15 | [add-runtime-observability-and-operations](../add-runtime-observability-and-operations/proposal.md) | C04, C05, C07, C09 |
| 27 | O05 | [add-versioned-workflow-execution](../add-versioned-workflow-execution/proposal.md) | C04, C05, C09 |
| 28 | O10 | [add-scim-provisioning-through-owner-commands](../add-scim-provisioning-through-owner-commands/proposal.md) | C03, C04, C06, C09 |
| 29 | O15 | [add-entitlements-and-atomic-quota-reservations](../add-entitlements-and-atomic-quota-reservations/proposal.md) | C04, C05, C06, C09 |
| 30 | O21 | [generate-typescript-python-public-sdks](../generate-typescript-python-public-sdks/proposal.md) | C06, C09 |
| 31 | Z11 | [add-pzt-operational-certificate-renewal](../add-pzt-operational-certificate-renewal/proposal.md) | Z09, Z12, Z06 |
| 32 | Z25 | [add-pzt-pa-admission-and-ephemeral-peer-generation](../add-pzt-pa-admission-and-ephemeral-peer-generation/proposal.md) | PA02, Z02, Z09, C09 |
| 33 | B01 | [complete-bulk-owner-admission-and-import-mapping](../complete-bulk-owner-admission-and-import-mapping/proposal.md) | C04, C06, C10 |
| 34 | C13 | [add-initial-administration-panel](../add-initial-administration-panel/proposal.md) | C08, C10, C11, C12 |
| 35 | C16 | [add-upgrade-backup-and-restore-contracts](../add-upgrade-backup-and-restore-contracts/proposal.md) | C08, C09, C10, C15 |
| 36 | O01 | [add-selected-object-storage-provider](../add-selected-object-storage-provider/proposal.md) | C01, C04, C05, C10 |
| 37 | O03 | [add-authorized-search-projections](../add-authorized-search-projections/proposal.md) | C04, C09, C10 |
| 38 | O04 | [add-derived-distributed-cache-provider](../add-derived-distributed-cache-provider/proposal.md) | C04, C09, C10 |
| 39 | O07 | [add-external-synchronization-provider](../add-external-synchronization-provider/proposal.md) | C04, C05, C09, C10 |
| 40 | O08 | [add-ldap-outbound-directory-projections](../add-ldap-outbound-directory-projections/proposal.md) | C02, C04, C05, C09, C10 |
| 41 | O11 | [add-notification-preferences-and-selected-channels](../add-notification-preferences-and-selected-channels/proposal.md) | C04, C05, C10, C12 |
| 42 | O16 | [add-selected-reactive-synchronization](../add-selected-reactive-synchronization/proposal.md) | C04, C06, C09, C10 |
| 43 | O17 | [add-offline-eligible-local-projections](../add-offline-eligible-local-projections/proposal.md) | C04, C06, C10 |
| 44 | O20 | [add-governed-reporting-analytics](../add-governed-reporting-analytics/proposal.md) | C04, C09, C10 |
| 45 | O23 | [add-native-client-contract-and-session-support](../add-native-client-contract-and-session-support/proposal.md) | O21, C03, C04 |
| 46 | O24 | [add-declared-ai-provider-and-governed-retrieval](../add-declared-ai-provider-and-governed-retrieval/proposal.md) | C01, C04, C06, C10 |
| 47 | O27 | [add-tenant-regional-placement-and-routing](../add-tenant-regional-placement-and-routing/proposal.md) | C04, C06, C10 |
| 48 | Z01 | [add-pzt-wireguard-local-transport-and-filtering](../add-pzt-wireguard-local-transport-and-filtering/proposal.md) | C14, PA01, PA02, Z02, Z09, Z25 |
| 49 | Z04 | [add-pzt-private-address-plan-and-ipv6-lifecycle](../add-pzt-private-address-plan-and-ipv6-lifecycle/proposal.md) | C14, Z03 |
| 50 | B04 | [complete-bulk-owner-conflict-strategies](../complete-bulk-owner-conflict-strategies/proposal.md) | B01 |
| 51 | B05 | [integrate-bulk-private-object-storage](../integrate-bulk-private-object-storage/proposal.md) | O01, B01 |
| 52 | B06 | [add-bulk-authorized-export-and-revocable-results](../add-bulk-authorized-export-and-revocable-results/proposal.md) | B01, O01, C10 |
| 53 | B07 | [integrate-bulk-inbox-outbox-and-publication](../integrate-bulk-inbox-outbox-and-publication/proposal.md) | C09, B01 |
| 54 | C18 | [build-first-pbo-pfo-debian-package](../build-first-pbo-pfo-debian-package/proposal.md) | C07, C08, C09, C11, C13, C14, C15, C16 |
| 55 | O02 | [add-governed-document-repository-adapter](../add-governed-document-repository-adapter/proposal.md) | O01, C04, C05, C10 |
| 56 | O09 | [add-directory-read-freshness-and-postgres-fallback](../add-directory-read-freshness-and-postgres-fallback/proposal.md) | O08 |
| 57 | O12 | [add-durable-notification-delivery-and-deduplication](../add-durable-notification-delivery-and-deduplication/proposal.md) | O11, C09 |
| 58 | O13 | [add-feature-flag-administration-and-audit](../add-feature-flag-administration-and-audit/proposal.md) | C04, C05, C06, C13 |
| 59 | O18 | [add-offline-intents-and-server-reconciliation](../add-offline-intents-and-server-reconciliation/proposal.md) | O17, C06 |
| 60 | O25 | [add-mediated-ai-tools-evaluations-and-budgets](../add-mediated-ai-tools-evaluations-and-budgets/proposal.md) | O24, C05, C09 |
| 61 | O26 | [add-audit-integrity-and-verifiable-exports](../add-audit-integrity-and-verifiable-exports/proposal.md) | C05, C10, C16 |
| 62 | O28 | [add-regional-authority-failover](../add-regional-authority-failover/proposal.md) | O27, C16 |
| 63 | PA04 | [add-pa-authorized-instruction-execution](../add-pa-authorized-instruction-execution/proposal.md) | PA03, Z01, Z02, Z06, Z25, C04, C05 |
| 64 | Z07 | [add-pzt-path-discovery-and-encrypted-relays](../add-pzt-path-discovery-and-encrypted-relays/proposal.md) | Z01, Z02, Z06 |
| 65 | Z10 | [add-pzt-tls-policy-and-bounded-cipher-migration](../add-pzt-tls-policy-and-bounded-cipher-migration/proposal.md) | Z01, Z06, Z12 |
| 66 | B02 | [add-bulk-atomic-import-execution](../add-bulk-atomic-import-execution/proposal.md) | B01, B05 |
| 67 | B03 | [add-bulk-best-effort-import-execution](../add-bulk-best-effort-import-execution/proposal.md) | B01, B05 |
| 68 | B08 | [integrate-bulk-worker-jobs-and-cancellation](../integrate-bulk-worker-jobs-and-cancellation/proposal.md) | C09, B01, B07 |
| 69 | C17 | [qualify-first-pbo-composition](../qualify-first-pbo-composition/proposal.md) | C04, C06, C08, C09, C10, C12, C13, C14, C15, C16, C18 |
| 70 | O14 | [integrate-feature-flag-runtime-convergence](../integrate-feature-flag-runtime-convergence/proposal.md) | O13, C07, C09 |
| 71 | O19 | [add-authorized-realtime-collaboration](../add-authorized-realtime-collaboration/proposal.md) | C04, C06, C09, C10, O18 |
| 72 | PA05 | [add-pa-desired-applied-configuration-and-drift](../add-pa-desired-applied-configuration-and-drift/proposal.md) | PA04, C09 |
| 73 | PA06 | [add-pa-durable-technical-state-and-offline-recovery](../add-pa-durable-technical-state-and-offline-recovery/proposal.md) | PA04, C09 |
| 74 | Z05 | [add-pzt-managed-dns-service-and-pa-adapters](../add-pzt-managed-dns-service-and-pa-adapters/proposal.md) | C14, PA04, Z04, Z06 |
| 75 | Z08 | [add-pzt-gateway-and-controlled-failover-profile](../add-pzt-gateway-and-controlled-failover-profile/proposal.md) | Z01, Z03, Z07 |
| 76 | B09 | [expose-bulk-versioned-http-api](../expose-bulk-versioned-http-api/proposal.md) | C06, B01, B08 |
| 77 | B10 | [complete-bulk-validation-reports-and-recovery-proofs](../complete-bulk-validation-reports-and-recovery-proofs/proposal.md) | B01, B08, C10 |
| 78 | C19 | [publish-first-qualified-pbo-release](../publish-first-qualified-pbo-release/proposal.md) | C17, C18 |
| 79 | O22 | [complete-developer-kit-and-cli-workflows](../complete-developer-kit-and-cli-workflows/proposal.md) | C07, C17, O21 |
| 80 | O31 | [qualify-selected-performance-budgets](../qualify-selected-performance-budgets/proposal.md) | C00, C15, C17 |
| 81 | O32 | [complete-extension-trust-and-isolation-adapters](../complete-extension-trust-and-isolation-adapters/proposal.md) | C07, C11, C17 |
| 82 | PA07 | [add-pa-supervision-maintenance-and-quarantine](../add-pa-supervision-maintenance-and-quarantine/proposal.md) | PA05, PA06, C12, C15 |
| 83 | Z14 | [add-pzt-monotonic-witness-and-key-sanitation](../add-pzt-monotonic-witness-and-key-sanitation/proposal.md) | Z13, PA06 |
| 84 | Z19 | [add-pzt-durable-helper-state-and-writer-exclusion](../add-pzt-durable-helper-state-and-writer-exclusion/proposal.md) | PA06, Z18 |
| 85 | B11 | [qualify-complete-bulk-runtime](../qualify-complete-bulk-runtime/proposal.md) | B02, B03, B04, B06, B07, B08, B09, B10 |
| 86 | O29 | [add-verified-component-registry](../add-verified-component-registry/proposal.md) | C07, C19 |
| 87 | O30 | [add-health-gated-progressive-deployment](../add-health-gated-progressive-deployment/proposal.md) | C15, C16, C19 |
| 88 | PA08 | [qualify-pa-platforms-and-r01-r68-matrix](../qualify-pa-platforms-and-r01-r68-matrix/proposal.md) | PA07, Z01, Z05, Z06, Z09, Z25 |
| 89 | Z15 | [add-pzt-evidence-dossier-and-bounded-validation](../add-pzt-evidence-dossier-and-bounded-validation/proposal.md) | Z03, Z13, Z14 |
| 90 | Z17 | [add-pzt-qualified-time-and-freshness-decisions](../add-pzt-qualified-time-and-freshness-decisions/proposal.md) | Z18, Z19 |
| 91 | Z20 | [add-pzt-bounded-telemetry-export-and-retention](../add-pzt-bounded-telemetry-export-and-retention/proposal.md) | Z19, C15 |
| 92 | Z16 | [add-pzt-proof-admission-and-attempt-reconciliation](../add-pzt-proof-admission-and-attempt-reconciliation/proposal.md) | Z15, Z17, C09 |
| 93 | Z21 | [add-pzt-telemetry-purge-jobs-and-leases](../add-pzt-telemetry-purge-jobs-and-leases/proposal.md) | Z20, C09, C10 |
| 94 | Z22 | [add-pzt-canonical-purge-manifests-and-integrity](../add-pzt-canonical-purge-manifests-and-integrity/proposal.md) | Z21, C05 |
| 95 | Z23 | [add-pzt-controlled-manifest-incident-rearm](../add-pzt-controlled-manifest-incident-rearm/proposal.md) | Z22, Z15, Z16, C04 |
| 96 | Z24 | [add-pzt-rearm-status-stream-and-reconciliation](../add-pzt-rearm-status-stream-and-reconciliation/proposal.md) | Z23, Z06 |
| 97 | Z26 | [qualify-active-pzt-contracts-and-profiles](../qualify-active-pzt-contracts-and-profiles/proposal.md) | PA08, C17, C19, Z01, Z02, Z03, Z04, Z05, Z06, Z07, Z09, Z10, Z11, Z12, Z13, Z14, Z15, Z16, Z17, Z18, Z19, Z20, Z21, Z22, Z23, Z24, Z25 |
| 98 | PA09 | [build-and-publish-independent-pa-debian-package](../build-and-publish-independent-pa-debian-package/proposal.md) | PA08, Z26, C19 |
| 99 | X01 | [build-and-qualify-pixs-docker-image](../build-and-qualify-pixs-docker-image/proposal.md) | C19, PA09, Z26 |
| 100 | Q01 | [qualify-selected-extended-pixs-compositions](../qualify-selected-extended-pixs-compositions/proposal.md) | C19, PA09, Z26, B11, X01, O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12, O13, O14, O15, O16, O17, O18, O19, O20, O21, O22, O23, O24, O25, O26, O27, O28, O29, O30, O31, O32 |

## Conditions distinctes du graphe de création

- Z08 : préparer le profil passerelle ne l’active pas ; sa première activation exige une qualification Z26 préalable du socle hors passerelle. Z26 peut ensuite qualifier la passerelle dans une recette ultérieure.
- O23 : un client natif en ligne n’hérite pas implicitement du mode offline ; la sélection offline ajoute ses contrats et dépendances.
- Q01 : les dépendances listées décrivent la cible globale du catalogue ; une recette d’un profil réduit n’impose pas d’activer les 32 options.
- C14 : les modules PZT/DNS restent essentiels dans le premier PBO, même sans exécution PA/réseau ; une clause obligatoire de gestion n’est pas écartée par le classement conditionnel de son contrat.
- X01 : l’image Pixs contient PBO/PFO/PZT et trois binaires PA, jamais le binaire utilisateur ; un conteneur PBO seul n’est pas présenté comme cette image conforme.

## Limites de validation

La matrice conserve 94 lignes non évaluées : la demande autorise leurs propositions de préparation conditionnelle, pas une déclaration automatique de manque ni une création de code. Les structures déjà livrées demeurent à réutiliser et qualifier. Les arbitrages de sécurité, providers, plateformes et exploitation seront soumis au moment où la réalisation concernée sera choisie ; les valeurs déjà décidées ne sont pas rouvertes.

Aucun compte connecté, secret, processus OpenCode, CAB, service système, montage, permission, dépendance, migration, API fournisseur ou publication n’a été actionné pour cette préparation.

