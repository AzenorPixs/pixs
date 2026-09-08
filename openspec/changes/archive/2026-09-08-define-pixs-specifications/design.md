## Context

Voir `proposal.md` pour la motivation. État actuel : `openspec/specs/` vide ; PROJECT.md §34 liste 56 capacités, §35 impose l'ordre de conception, §36 laisse ouverts les détails d'implémentation (schéma TOML exact, APIs, protocoles). Contraintes : mise en place achevée ou suspendue proprement avant 06:00, specs avant code, déterminisme, `deny by default`, PostgreSQL comme source de vérité, Django comme autorité métier.

## Goals / Non-Goals

**Goals:**

- Fournir un socle de 56 spécifications traçables vers PROJECT.md §34 / §35, TECHNICAL.md et BUILD.md.
- Découper en lots A-G revus par CGPT dans l'ordre §35.
- Zéro code, zéro manifest, zéro config dans ce change.

**Non-Goals:**

- Aucune implémentation, aucun schéma `component.toml` final, aucun provider concret figé.
- Aucune spec de capacité écrite avant validation explicite de son lot.

## Decisions

1. **Un change unique `define-pixs-specifications` avec 56 deltas `specs/<kebab>/spec.md`.** Alternative rejetée : N changes séparés (bruit de revue, perte de traçabilité §35).
2. **Ordre des lots = §35 strict :**
   - A socle : `kernel`, `component-model`, `contracts`, `extension-contracts`, `capabilities`, `feature-flags`, `dependencies`, `lifecycle`.
   - B : `migrations`, `modules`, `providers`, `services`, `interactions`, `events`, `jobs`, `notifications`.
   - C : `configuration`, `security`, `core`, `scope-context`, `data-lifecycle`, `data-governance`, `object-storage`, `document-repositories`.
   - D : `search`, `workflows`, `external-synchronization`, `bulk-operations`, `authorization`, `authorization-engine`, `quotas-entitlements`, `authentication`.
   - E : `identity-assurance`, `internationalization`, `themes`, `frontend`, `synchronization`, `offline-first`, `regional-residency`, `api`.
   - F : `sdk-ecosystem`, `observability`, `resilience`, `audit`, `accessibility`, `design-system`, `compatibility`, `testing`.
   - G : `performance`, `runtime`, `operations`, `backup-disaster-recovery`, `deb-package`, `docker-image`, `artifact-publication`, `release-management`.
3. **Format des specs : `Requirement` + `Scenario` par invariant PROJECT/TECHNICAL/BUILD**, identifiants stables, sans implémentation.
4. **Validation par lot via `openspec validate --change` ; suspension propre si 06:00** (lots non validés restent `blocked`, change non archivé).
5. **Convention normative française.** Les spécifications emploient `DOIT` / `NE DOIT PAS`, hérités des sources PROJECT/TECHNICAL/AGENTS ; les WARNING RFC 2119 d'`openspec validate` (« should contain SHALL or MUST ») sont un artefact attendu de cette convention, acceptés et documentés ici, sans réécriture des 56 deltas (arbitrage CGPT approuvé, NQCMOC `mcp-8`, session pixs-define-specs-s002).

## Risks / Trade-offs

- [Dérive §36, ex. TOML exact] → Mitigation : marquer en Open Questions, rien de normatif sans décision.
- [56 specs illisibles d'un coup] → Mitigation : lots A-G + revue CGPT par lot.
- [Conflit Kernel / core / scopes] → Mitigation : ordre §35 + relecture croisée C/D.
