# Exigences de réalisation — C02

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| core / 8 | [Module obligatoire au-dessus du noyau](../../specs/core/spec.md#L8) | P | Composition sans core refusée |
| core / 17 | [Primitives minimales communes](../../specs/core/spec.md#L17) | P | Primitive consommée par contrat |
| core / 31 | [Aucun fournisseur concret imposé](../../specs/core/spec.md#L31) | P | Substitution de fournisseur |
| core / 102 | [Autorités et limites du profil identité structurel](../../specs/core/spec.md#L102) | P | Identité structurelle sans assurance implicite |
| migrations / 8 | [Contrat de migration](../../specs/migrations/spec.md#L8) | P | Migration sans version cible |
| migrations / 17 | [Planification et ordre déterministes](../../specs/migrations/spec.md#L17) | P | Deux migrations concurrentes |
| migrations / 26 | [Compatibilité pendant l'application](../../specs/migrations/spec.md#L26) | P | Coexistence pendant migration |
| migrations / 35 | [Reprise idempotente](../../specs/migrations/spec.md#L35) | P | Interruption puis reprise |
| migrations / 44 | [Contraction contrôlée](../../specs/migrations/spec.md#L44) | P | Contraction prématurée |
| scope-context / 8 | [Périmètre explicite du Super Admin](../../specs/scope-context/spec.md#L8) | P | Accord tenant sans changement de propriété |
| scope-context / 18 | [Tenant racine et parenté unique](../../specs/scope-context/spec.md#L18) | P | Cycle de scopes refusé |
| scope-context / 29 | [Propriété canonique unique](../../specs/scope-context/spec.md#L29) | P | Scope sans tenant cohérent refusé |
| scope-context / 40 | [Contexte immuable propagé avant autorisation](../../specs/scope-context/spec.md#L40) | P | Contexte TENANT sans tenant refusé ; Contexte PLATFORM avec identifiants refusé ; Scope orphelin refusé |
| scope-context / 59 | [Propagation et frontière d'autorisation du ScopeContext](../../specs/scope-context/spec.md#L59) | P | Élargissement implicite refusé ; Contexte PLATFORM sans identifiants accepté sans octroyer permission ; Accès plateforme sans permission refusé et audité |

## Empreintes SHA-256 du canon

- `openspec/specs/core/spec.md` : `d0eb213fa2fbb3ccca042133d910166b35f4a3e8e60178ad02b12420034bada3`.
- `openspec/specs/migrations/spec.md` : `9b3ced385afbeaa7414a1d58752078482e57efa242064e21e7fb4b6fde451efe`.
- `openspec/specs/scope-context/spec.md` : `4a8df881b08f5b4e3c302b9966bff199276350cab9a236a9f8ff2330d28d1270`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
