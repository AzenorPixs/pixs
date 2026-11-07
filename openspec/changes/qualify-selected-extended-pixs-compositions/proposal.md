# Q01 — Recette des compositions étendues

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Recettes transversales des compositions Domaine/ZT partagé/reprise/politiques, sans répéter les réalisations ou recettes locales.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [reference-composition](../../specs/reference-composition/spec.md).
- [pixs-domains](../../specs/pixs-domains/spec.md).
- [organization-charts](../../specs/organization-charts/spec.md).
- [brick-redundancy](../../specs/brick-redundancy/spec.md).
- [managed-device-policies](../../specs/managed-device-policies/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Pourquoi

Le kit local et les contrôles structurels d’attestation ne prouvent pas une composition étendue ; ce dossier prépare les recettes des seuls profils effectivement sélectionnés.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

Scénarios transversaux des compositions étendues, compatibilité/publication corrélées ; preuves regroupées sans recréer contrats locaux.

## Capacités

### Capacités nouvelles

Aucun comportement normatif nouveau n’est prévu. Ce dossier prépare la réalisation ou la qualification des contrats déjà présents dans le canon.

### Capacités modifiées

Aucune modification de texte canonique. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios ; `skip_specs: true` évite un delta identique artificiel. Si un audit ou une décision exige une évolution normative, présenter son delta avant réalisation, sans considérer cette métadonnée comme une dispense de conformité.

## Sélection et périmètre autorisé

Hors premier P0 proposé ; obligation du profil/capacité sélectionné, applicabilité à confirmer. La préparation demandée ne sélectionne, n’active et ne qualifie pas cette capacité dans le premier profil P0.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [publish-first-qualified-pbo-release](../publish-first-qualified-pbo-release/proposal.md).
- [build-and-publish-independent-pa-debian-package](../build-and-publish-independent-pa-debian-package/proposal.md).
- [qualify-active-pzt-contracts-and-profiles](../qualify-active-pzt-contracts-and-profiles/proposal.md).
- [qualify-complete-bulk-runtime](../qualify-complete-bulk-runtime/proposal.md).
- [build-and-qualify-pixs-docker-image](../build-and-qualify-pixs-docker-image/proposal.md).
- [add-selected-object-storage-provider](../add-selected-object-storage-provider/proposal.md).
- [add-governed-document-repository-adapter](../add-governed-document-repository-adapter/proposal.md).
- [add-authorized-search-projections](../add-authorized-search-projections/proposal.md).
- [add-derived-distributed-cache-provider](../add-derived-distributed-cache-provider/proposal.md).
- [add-versioned-workflow-execution](../add-versioned-workflow-execution/proposal.md).
- [add-bounded-business-rule-evaluation](../archive/2026-10-23-add-bounded-business-rule-evaluation/proposal.md).
- [add-external-synchronization-provider](../add-external-synchronization-provider/proposal.md).
- [add-ldap-outbound-directory-projections](../add-ldap-outbound-directory-projections/proposal.md).
- [add-directory-read-freshness-and-postgres-fallback](../add-directory-read-freshness-and-postgres-fallback/proposal.md).
- [add-scim-provisioning-through-owner-commands](../add-scim-provisioning-through-owner-commands/proposal.md).
- [add-notification-preferences-and-selected-channels](../add-notification-preferences-and-selected-channels/proposal.md).
- [add-durable-notification-delivery-and-deduplication](../add-durable-notification-delivery-and-deduplication/proposal.md).
- [add-feature-flag-administration-and-audit](../add-feature-flag-administration-and-audit/proposal.md).
- [integrate-feature-flag-runtime-convergence](../integrate-feature-flag-runtime-convergence/proposal.md).
- [add-entitlements-and-atomic-quota-reservations](../add-entitlements-and-atomic-quota-reservations/proposal.md).
- [add-selected-reactive-synchronization](../add-selected-reactive-synchronization/proposal.md).
- [add-offline-eligible-local-projections](../add-offline-eligible-local-projections/proposal.md).
- [add-offline-intents-and-server-reconciliation](../add-offline-intents-and-server-reconciliation/proposal.md).
- [add-authorized-realtime-collaboration](../add-authorized-realtime-collaboration/proposal.md).
- [add-governed-reporting-analytics](../add-governed-reporting-analytics/proposal.md).
- [generate-typescript-python-public-sdks](../generate-typescript-python-public-sdks/proposal.md).
- [complete-developer-kit-and-cli-workflows](../complete-developer-kit-and-cli-workflows/proposal.md).
- [add-native-client-contract-and-session-support](../add-native-client-contract-and-session-support/proposal.md).
- [add-declared-ai-provider-and-governed-retrieval](../add-declared-ai-provider-and-governed-retrieval/proposal.md).
- [add-mediated-ai-tools-evaluations-and-budgets](../add-mediated-ai-tools-evaluations-and-budgets/proposal.md).
- [add-audit-integrity-and-verifiable-exports](../add-audit-integrity-and-verifiable-exports/proposal.md).
- [add-tenant-regional-placement-and-routing](../add-tenant-regional-placement-and-routing/proposal.md).
- [add-regional-authority-failover](../add-regional-authority-failover/proposal.md).
- [add-verified-component-registry](../add-verified-component-registry/proposal.md).
- [add-health-gated-progressive-deployment](../add-health-gated-progressive-deployment/proposal.md).
- [qualify-selected-performance-budgets](../qualify-selected-performance-budgets/proposal.md).
- [complete-extension-trust-and-isolation-adapters](../complete-extension-trust-and-isolation-adapters/proposal.md).

La liste complète représente la cible globale de l’inventaire ; chaque recette réduite ne retient que ses options et leurs dépendances obligatoires. Aucun profil n’est forcé d’activer toutes les capacités.

## Impact de réalisation future

Assembler les preuves des compositions explicitement sélectionnées, sans exiger toutes les options dans chaque installation. Lier tests, attestations authentifiées, source, versions et artefact réellement exécuté ; distinguer niveaux de test et non-applicabilité motivée. Aucun PASS, support plateforme ni gain de performance n’est déduit de la seule présence d’un dossier.

## Critère de sortie de réalisation future

Preuves actuelles de chaque scénario applicable ; absences motivées ; niveaux de tests distincts ; aucun taux produit tiré du nombre de changes.

## Décisions restant à valider

Profils sélectionnés, critères d’applicabilité et versions exactes ; les dépendances de cible globale ne forcent pas toutes les options dans un profil réduit.
