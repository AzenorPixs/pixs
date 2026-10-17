# Plan de préparation — première livraison P0

Date : 17 octobre 2026. Inventaire validé par le développeur ; vingt dossiers initiaux préparés, complétés depuis par N01 validé après audit, sans réalisation. C00 formalise le profil et ses deltas proposés. C01–C19 réalisent le canon existant : pas de delta identique artificiel, exigences référencées et skip_specs explicite.

## Ordre de dépendances conseillé après revue

| Lot | Change | Dépendances vérifiées | État |
|---|---|---|---|
| C00 | [define-first-installable-pbo-profile](../define-first-installable-pbo-profile/proposal.md) | Aucune | Documents préparés ; tâches non cochées |
| C02 | [add-core-postgres-services](../add-core-postgres-services/proposal.md) | C00 | Documents préparés ; tâches non cochées |
| C01 | [add-pbo-runtime-secret-provider](../add-pbo-runtime-secret-provider/proposal.md) | C00 | Documents préparés ; tâches non cochées |
| C05 | [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md) | C00, C02 | Documents préparés ; tâches non cochées |
| C07 | [activate-reference-runtime-composition](../activate-reference-runtime-composition/proposal.md) | C01, C02, C05 | Documents préparés ; tâches non cochées |
| C03 | [add-initial-authentication-and-sessions](../add-initial-authentication-and-sessions/proposal.md) | C01, C02, C05 | Documents préparés ; tâches non cochées |
| C04 | [integrate-runtime-authorization-and-super-admin](../integrate-runtime-authorization-and-super-admin/proposal.md) | C02, C03, C05 | Documents préparés ; tâches non cochées |
| C08 | [add-installation-and-first-configuration](../add-installation-and-first-configuration/proposal.md) | C01, C02, C03, C04, C05, C07 | Documents préparés ; tâches non cochées |
| C06 | [add-protected-core-http-commands-and-queries](../add-protected-core-http-commands-and-queries/proposal.md) | C02, C03, C04, C05 | Documents préparés ; tâches non cochées |
| C09 | [add-reference-worker-scheduler-and-event-delivery](../add-reference-worker-scheduler-and-event-delivery/proposal.md) | C04, C05, C06, C07 | Documents préparés ; tâches non cochées |
| C11 | [compose-modular-frontend-with-core-api](../compose-modular-frontend-with-core-api/proposal.md) | C06, C07 | Documents préparés ; tâches non cochées |
| C14 | [add-essential-pbo-pzt-and-dns-modules](../add-essential-pbo-pzt-and-dns-modules/proposal.md) | C00, C02, C04, C05, C06, C11 | Documents préparés ; tâches non cochées |
| C15 | [add-runtime-observability-and-operations](../add-runtime-observability-and-operations/proposal.md) | C04, C05, C07, C09 | Documents préparés ; tâches non cochées |
| C12 | [complete-shared-ui-i18n-and-accessibility](../complete-shared-ui-i18n-and-accessibility/proposal.md) | C06, C11 | Documents préparés ; tâches non cochées |
| C10 | [enforce-core-data-governance-and-lifecycle](../enforce-core-data-governance-and-lifecycle/proposal.md) | C02, C04, C05, C09 | Documents préparés ; tâches non cochées |
| C13 | [add-initial-administration-panel](../add-initial-administration-panel/proposal.md) | C08, C10, C11, C12 | Documents préparés ; tâches non cochées |
| C16 | [add-upgrade-backup-and-restore-contracts](../add-upgrade-backup-and-restore-contracts/proposal.md) | C08, C09, C10, C15 | Documents préparés ; tâches non cochées |
| N01 | [add-pbo-security-quarantine-and-revocation](../add-pbo-security-quarantine-and-revocation/proposal.md) | C03, C04, C05, C07, C09, C15 | Urgence PBO dédiée validée ; documents préparés, tâches non cochées |
| C18 | [build-first-pbo-pfo-debian-package](../build-first-pbo-pfo-debian-package/proposal.md) | C07, C08, C09, C11, C13, C14, C15, C16, N01 | Documents préparés ; tâches non cochées |
| C17 | [qualify-first-pbo-composition](../qualify-first-pbo-composition/proposal.md) | C04, C06, C08, C09, C10, C12, C13, C14, C15, C16, C18, N01 | Documents préparés ; tâches non cochées |
| C19 | [publish-first-qualified-pbo-release](../publish-first-qualified-pbo-release/proposal.md) | C17, C18 | Documents préparés ; tâches non cochées |

La revue a ajouté C05 comme dépendance explicite de C03 et C04 : authentification et autorisation runtime nécessitent l’audit durable. L’ordre matériel de création initial et l’ordre final de dépendances sont conservés séparément dans preparation.json.

## Frontière de validation

L’autorisation de création ne vaut pas approbation de tous les choix de sécurité ou autorisation d’implémenter. Les textes normatifs C00 restent dans ses deltas ; aucune synchronisation ou archive. Les barrières de conception propres à chaque change restent visibles. La validation stricte porte sur les documents, pas sur le service.

## Périmètre préparé séparément

Après la demande explicite complémentaire du développeur, les 80 autres candidats sont préparés sans implémentation dans le [plan global](plan-global-preparation.md). Ils restent distincts du premier profil P0 : PA/réseau actif, Bulk, options, Docker et recette étendue ne sont pas activés par leur création. Si une obligation conditionnelle devient active, ses dépendances doivent être sélectionnées avant qualification.

## Référence du canon

Les empreintes de 206 entrées sont conservées dans preparation.json pour détecter une dérive ; elles ne prouvent ni une exécution ni une conformité de ces fichiers. Les modifications Git préexistantes ne sont pas reprises ou supprimées.



## Révision après audit des 94 NE

Le premier P0 compte désormais 21 changes préparés. [N02](../clarify-native-credentials-and-offline-storage-boundary/proposal.md) reste une clarification optionnelle transverse pour les profils natifs hors ligne. Le [plan global actuel](plan-global-preparation.md) compte 102 dossiers ; les anciennes validations C00–C19 et globales de 100 dossiers restent datées et historiques.
