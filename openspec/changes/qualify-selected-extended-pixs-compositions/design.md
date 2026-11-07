# Conception — Q01

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

## Statut

PRÉPARATION_DOCUMENTAIRE_CONDITIONNELLE. Le dossier est demandé ; ses choix encore ouverts et son implémentation ne sont pas approuvés implicitement. La présence des fichiers ne signifie pas prêt à coder.

## Contexte actuel

Le kit local et les contrôles structurels d’attestation ne prouvent pas une composition étendue ; ce dossier prépare les recettes des seuls profils effectivement sélectionnés.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

Sources et périmètres consultés :

- [src/pixs/developer_kit/README.md](../../../src/pixs/developer_kit/README.md).
- [src/pixs/kernel/conformity.py](../../../src/pixs/kernel/conformity.py).
- [openspec/specs/testing/spec.md](../../specs/testing/spec.md).
- [src/pixs/developer_kit/validators.py](../../../src/pixs/developer_kit/validators.py).
- [src/pixs/kernel/contracts/README.md](../../../src/pixs/kernel/contracts/README.md).
- [src/pixs/kernel/contracts/models.py](../../../src/pixs/kernel/contracts/models.py).
- [src/pixs/example/__init__.py](../../../src/pixs/example/__init__.py).
- [src/pixs/backend/README.md](../../../src/pixs/backend/README.md).
- [src/pixs/backend/composition_initial.py](../../../src/pixs/backend/composition_initial.py).
- [src/pixs/backend/composition_proof.py](../../../src/pixs/backend/composition_proof.py).
- [src/pixs/backend/local_test_composition.py](../../../src/pixs/backend/local_test_composition.py).
- [src/pixs/backend/liveness_view.py](../../../src/pixs/backend/liveness_view.py).
- [frontend/README.md](../../../frontend/README.md).
- [frontend/package.json](../../../frontend/package.json).

## Architecture et frontières

Assembler les preuves des compositions explicitement sélectionnées, sans exiger toutes les options dans chaque installation. Lier tests, attestations authentifiées, source, versions et artefact réellement exécuté ; distinguer niveaux de test et non-applicabilité motivée. Aucun PASS, support plateforme ni gain de performance n’est déduit de la seule présence d’un dossier.

Périmètre propre à ce lot : Scénarios transversaux des compositions étendues, compatibilité/publication corrélées ; preuves regroupées sans recréer contrats locaux.

## Choix déjà fixés et alternatives

Les décisions validées dans les contrats sources sont conservées, y compris formats, algorithmes, valeurs, rôles et alternatives rejetées. Elles ne sont pas rouvertes sous prétexte d’un nouveau dossier. Les plafonds d’un auxiliaire, collecteur, validateur ou travail ne deviennent pas un budget général du PA/PBO.

Les modalités concrètes encore ouvertes ne reçoivent pas de valeur de défaut inventée. Une bibliothèque, un provider ou une dépendance présent dans DEVOPS n’est ni sélectionné ni qualifié. Les références normatives complètes sont dans requirements.md ; les mentions historiques qu’elles contiennent ne décrivent pas des effets réalisés pendant cette préparation.

## Barrières de conception avant réalisation

Profils sélectionnés, critères d’applicabilité et versions exactes ; les dépendances de cible globale ne forcent pas toutes les options dans un profil réduit.

Ces barrières n’empêchent pas la rédaction conditionnelle du dossier. Avant tout code, les choix ayant un impact réel sur sécurité, périmètre, compatibilité, exploitation ou ressources devront être soumis avec conséquences et recommandation ; pour PA/PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages. Les paramètres déjà décidés sont à qualifier, pas à remplacer par une nouvelle décision supposée.

## Dépendances et interfaces

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

Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent explicitement incomplètes tant que les obligations manquent.

## Vérification future

Unités, intégrations réelles, conformité versionnée, navigateurs headless et manuel selon profil ; cohérence des versions et preuves négatives, scénarios absents/échoués explicites, verdict natif OpenSpec conservé.

Sortie du lot : Preuves actuelles de chaque scénario applicable ; absences motivées ; niveaux de tests distincts ; aucun taux produit tiré du nombre de changes.

Exercer tous les scénarios et clauses applicables des blocs sources, y compris renvois normatifs ; un scénario non applicable doit être motivé par le profil réel. Les contrôles applicatifs suivent l’exception Super Admin du canon dans son seul périmètre, sans fabriquer audit, mesure, signature ou effet absent.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données/états doit préciser propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation/restauration. Aucun retour arrière destructeur, remise à zéro, arrêt de service ou changement de droits implicites.

## Limites du dossier

Pas de PASS actuel ni d’achèvement produit revendiqué. L’autorisation de préparation ne permet ni d’activer la capacité dans P0 ni d’utiliser un compte connecté, publier un artefact ou envoyer une notification réelle.
