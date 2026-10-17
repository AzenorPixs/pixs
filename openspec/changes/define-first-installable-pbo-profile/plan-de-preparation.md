# Plan de préparation — première livraison P0

Relevé du 17 octobre 2026 : 25 dossiers P0 préparés, C00–C19 puis N01 et N03–N06 validés après audits. Réalisation non autorisée ; tâches non cochées. C00/N04/N05 portent des deltas proposés, sans synchronisation. Les autres lots réalisent le canon existant avec skip_specs explicite.

## Dépendances fermes dans le profil

| Lot | Change | Dépendances | État |
|---|---|---|---|
| C00 | [define-first-installable-pbo-profile](../define-first-installable-pbo-profile/proposal.md) | Aucune | Préparé ; réalisation non lancée |
| C01 | [add-pbo-runtime-secret-provider](../add-pbo-runtime-secret-provider/proposal.md) | C00 | Préparé ; réalisation non lancée |
| C02 | [add-core-postgres-services](../add-core-postgres-services/proposal.md) | C00 | Préparé ; réalisation non lancée |
| N03 | [add-p0-artifact-trust-and-preinstallation-verification](../add-p0-artifact-trust-and-preinstallation-verification/proposal.md) | C00 | Préparé ; réalisation non lancée |
| C05 | [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md) | C00, C02 | Préparé ; réalisation non lancée |
| C03 | [add-initial-authentication-and-sessions](../add-initial-authentication-and-sessions/proposal.md) | C01, C02, C05 | Préparé ; réalisation non lancée |
| C07 | [activate-reference-runtime-composition](../activate-reference-runtime-composition/proposal.md) | C01, C02, C05 | Préparé ; réalisation non lancée |
| C04 | [integrate-runtime-authorization-and-super-admin](../integrate-runtime-authorization-and-super-admin/proposal.md) | C02, C03, C05 | Préparé ; réalisation non lancée |
| C06 | [add-protected-core-http-commands-and-queries](../add-protected-core-http-commands-and-queries/proposal.md) | C02, C03, C04, C05 | Préparé ; réalisation non lancée |
| C08 | [add-installation-and-first-configuration](../add-installation-and-first-configuration/proposal.md) | C01, C02, C03, C04, C05, C07 | Préparé ; réalisation non lancée |
| C09 | [add-reference-worker-scheduler-and-event-delivery](../add-reference-worker-scheduler-and-event-delivery/proposal.md) | C04, C05, C06, C07 | Préparé ; réalisation non lancée |
| C11 | [compose-modular-frontend-with-core-api](../compose-modular-frontend-with-core-api/proposal.md) | C06, C07 | Préparé ; réalisation non lancée |
| C10 | [enforce-core-data-governance-and-lifecycle](../enforce-core-data-governance-and-lifecycle/proposal.md) | C02, C04, C05, C09 | Préparé ; réalisation non lancée |
| C12 | [complete-shared-ui-i18n-and-accessibility](../complete-shared-ui-i18n-and-accessibility/proposal.md) | C06, C11 | Préparé ; réalisation non lancée |
| C14 | [add-essential-pbo-pzt-and-dns-modules](../add-essential-pbo-pzt-and-dns-modules/proposal.md) | C00, C02, C04, C05, C06, C11 | Préparé ; réalisation non lancée |
| C15 | [add-runtime-observability-and-operations](../add-runtime-observability-and-operations/proposal.md) | C04, C05, C07, C09 | Préparé ; réalisation non lancée |
| C13 | [add-initial-administration-panel](../add-initial-administration-panel/proposal.md) | C08, C10, C11, C12 | Préparé ; réalisation non lancée |
| C16 | [add-upgrade-backup-and-restore-contracts](../add-upgrade-backup-and-restore-contracts/proposal.md) | C08, C09, C10, C15 | Préparé ; réalisation non lancée |
| N01 | [add-pbo-security-quarantine-and-revocation](../add-pbo-security-quarantine-and-revocation/proposal.md) | C03, C04, C05, C07, C09, C15 | Préparé ; réalisation non lancée |
| N04 | [define-p0-web-serving-and-security-boundary](../define-p0-web-serving-and-security-boundary/proposal.md) | C03, C06, C07, C11, C15 | Préparé ; réalisation non lancée |
| N05 | [add-p0-post-restore-reconciliation-and-readmission](../add-p0-post-restore-reconciliation-and-readmission/proposal.md) | C01, C03, C04, C05, C08, C09, C10, C15, C16, N01 | Préparé ; réalisation non lancée |
| N06 | [add-minimal-p0-contract-conformance-kit](../add-minimal-p0-contract-conformance-kit/proposal.md) | C06, C07, C09, C10, C11, C14, N01 | Préparé ; réalisation non lancée |
| C18 | [build-first-pbo-pfo-debian-package](../build-first-pbo-pfo-debian-package/proposal.md) | C07, C08, C09, C11, C13, C14, C15, C16, N01, N03, N04, N05 | Préparé ; réalisation non lancée |
| C17 | [qualify-first-pbo-composition](../qualify-first-pbo-composition/proposal.md) | C04, C06, C08, C09, C10, C12, C13, C14, C15, C16, C18, N01, N03, N04, N05, N06 | Préparé ; réalisation non lancée |
| C19 | [publish-first-qualified-pbo-release](../publish-first-qualified-pbo-release/proposal.md) | C17, C18, N03 | Préparé ; réalisation non lancée |

## Conditions de fermeture du parcours

N03 rend les contrôles de confiance disponibles avant installation. N04 assemble l’entrée web. N05 assure la réadmission après restauration. N06 produit le kit minimal avant la recette C17 ; il ne rend pas les SDK/CLI complets obligatoires. C07 reste un hôte intermédiaire tant que ses obligations/proofs manquent. C18 produit le paquet à qualifier puis C19 conserve l’identité qualifiée et prépare sa publication sur instruction distincte.

[Audit transversal](audit-transversal-p0.md), [plan global 106 dossiers](plan-global-preparation.md) et [registre des validations](arbitrages-preparation-globale.md). N02 reste hors premier profil, applicable aux combinaisons natives/hors ligne. Aucun compteur canonique n’inclut les deltas proposés. Les preuves antérieures de 20/100/102 dossiers restent datées et historiques.
