## Why

Pixs ne dispose d'aucune spécification OpenSpec exploitable (`openspec/specs/` vide). PROJECT.md §34, TECHNICAL.md et BUILD.md définissent le cap mais ne sont pas des comportements vérifiables. Il faut un socle de spécifications par capacité avant tout code, à achever ou suspendre proprement avant 06:00.

## What Changes

- Crée le change `define-pixs-specifications` (schéma `spec-driven`).
- Fournit `proposal.md`, `design.md`, `tasks.md` comme base de revue CGPT.
- Prépare 56 capacités issues de PROJECT.md §34 pour spécification par lots (ordre §35), sans écrire leurs `spec.md` dans ce lot.
- Ne modifie aucun code, aucun manifest, aucune config existante.

## Capabilities

### New Capabilities

- `kernel`: mécanismes fondamentaux, registre, découverte, orchestration générique.
- `component-model`: identité stable, types, propriétés et états communs.
- `contracts`: catégories, versions, garanties, compatibilité et dépréciation.
- `extension-contracts`: points d'extension, contributions, collisions, confiance et isolation.
- `providers`: déclaration, sélection explicite, conformité, dégradation et diagnostic.
- `modules`: manifest, API publique/privée, propriété données et migrations, chargement.
- `capabilities`: capacités fournies/requises, résolution, sélection déterministe.
- `feature-flags`: définitions, affectations runtime, ciblage, évaluation, expiration et audit.
- `dependencies`: dépendances déclarées, résolution, ordre, cycles.
- `lifecycle`: validation, chargement, activation, désactivation, états distincts.
- `migrations`: contrats, planification, compatibilité, reprise et contraction.
- `services`: contrats, registre, providers.
- `interactions`: commands, queries, frontières transactionnelles.
- `events`: événements, hooks, handlers.
- `jobs`: exécution persistante, leases, retries, dead-letters, reprise.
- `notifications`: contrats, préférences, asynchronisme, audit et confidentialité.
- `configuration`: configuration globale/par composant, schémas, défauts, secrets.
- `security`: secrets, frontières de confiance, SBOM, diagnostics sans fuite.
- `core`: capacités communes obligatoires (`pixs.core`).
- `scope-context`: Tenant racine, scopes enfants, ScopeContext, propriété canonique.
- `data-lifecycle`: persistance, rétention, suppression, purge, tombstones.
- `data-governance`: profils, classification, finalités, demandes, propagation.
- `object-storage`: contrat ObjectStorageProvider, isolation, conformité.
- `document-repositories`: contrat DocumentRepositoryProvider, modes, Nextcloud.
- `search`: contrat SearchProvider, indexation, filtrage autorisé.
- `workflows`: définitions, transitions, reprise, compatibilité instances.
- `external-synchronization`: contrat SynchronizationProvider, mappings, conflits.
- `bulk-operations`: contrat BulkOperation, staging, reprise, quotas, audit.
- `authorization`: sujets, Subject/Resource/Action, ACL, évaluation.
- `authorization-engine`: PDP/PEP, politiques, décisions, filtrage, cache.
- `quotas-entitlements`: entitlements, quotas, réservations, échec fermé.
- `authentication`: AuthenticationProvider, Local, OIDC, SAML.
- `identity-assurance`: AuthenticationContext, assurance, step-up, révocation.
- `internationalization`: catalogues, résolution, composition.
- `themes`: thèmes, branding, surcharges.
- `frontend`: TanStack, routes, contributions UI.
- `synchronization`: Electric, réactivité, sync frontend.
- `offline-first`: capacité opt-in, réplicas locaux, conflits, purge.
- `regional-residency`: placement par tenant, régions logiques, bascule.
- `api`: contrats HTTP, versionnement, documentation (OpenAPI).
- `sdk-ecosystem`: SDK TS/Python, génération, Developer Kit, CLI.
- `observability`: logs, métriques, traces, health, diagnostics.
- `resilience`: isolation défaillances, santé, dégradé.
- `audit`: événements métier, acteur/action/cible, traçabilité.
- `accessibility`: clavier, focus, sémantique, assistance (WCAG 2.2 AA).
- `design-system`: tokens, primitives, Light/Dark.
- `compatibility`: versions, contraintes, matrice de validation.
- `testing`: unitaires, intégration, conformité contrats.
- `performance`: mesure, optimisation, budgets.
- `runtime`: profils web/worker/scheduler, coordination, leases.
- `operations`: interface management, maintenance, drainage, audit opérateur.
- `backup-disaster-recovery`: RPO/RTO, restauration, tombstones.
- `deb-package`: composition Debian, services, lifecycle, validation.
- `docker-image`: composition OCI/Docker, base, health, persistance.
- `artifact-publication`: canaux, immutabilité, signature, SBOM.
- `release-management`: versions, support, upgrade, coexistence N/N+1.

### Modified Capabilities

- Aucune (référentiel `openspec/specs/` vide).

## Impact

- Ajout uniquement dans `openspec/changes/define-pixs-specifications/`.
- Aucun impact code, API, dépendance ou runtime.
- Les `specs/*/spec.md` seront proposés par lots ultérieurs après revue CGPT de ce lot.
