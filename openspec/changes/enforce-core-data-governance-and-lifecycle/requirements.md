# Exigences de réalisation — C10

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 proposé ajoute les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| backup-disaster-recovery / 8 | [Stratégie déclarée par déploiement](../../specs/backup-disaster-recovery/spec.md#L8) | ND | Procédure sans objectifs déclarés |
| backup-disaster-recovery / 17 | [Périmètres de sauvegarde distincts](../../specs/backup-disaster-recovery/spec.md#L17) | ND | Sauvegarde partielle |
| backup-disaster-recovery / 26 | [Restauration cohérente et réapplication des gouvernances](../../specs/backup-disaster-recovery/spec.md#L26) | ND | Objet restauré après suppression validée |
| backup-disaster-recovery / 35 | [Tests de restauration isolés et preuves](../../specs/backup-disaster-recovery/spec.md#L35) | ND | Démarrage après restauration |
| backup-disaster-recovery / 44 | [Restauration destructive autorisée et auditée](../../specs/backup-disaster-recovery/spec.md#L44) | ND | Suppression implicite refusée |
| data-governance / 8 | [Application de l'exception Super Admin](../../specs/data-governance/spec.md#L8) | P | Dérogation de gouvernance dans un tenant accordé |
| data-governance / 18 | [Profil de gouvernance versionné par composant](../../specs/data-governance/spec.md#L18) | P | Flux sortant sans consommateur refusé |
| data-governance / 27 | [Classification restrictive par défaut](../../specs/data-governance/spec.md#L27) | P | Export non classifié refusé |
| data-governance / 38 | [Demandes relatives aux données tracées](../../specs/data-governance/spec.md#L38) | P | Effacement propagé |
| data-lifecycle / 8 | [Application de l'exception Super Admin](../../specs/data-lifecycle/spec.md#L8) | P | Purge demandée malgré un legal hold |
| data-lifecycle / 18 | [Dimensions et états distincts](../../specs/data-lifecycle/spec.md#L18) | P | Suppression logique tracée ; Vocabulaire commun de rétention fermé |
| data-lifecycle / 43 | [Purge autorisée, auditée et idempotente](../../specs/data-lifecycle/spec.md#L43) | P | Purge prématurée refusée |
| data-lifecycle / 52 | [Tombstones contre la résurrection](../../specs/data-lifecycle/spec.md#L52) | P | Restauration sans résurrection |

## Empreintes SHA-256 du canon

- `openspec/specs/backup-disaster-recovery/spec.md` : `3b129f2e8fd899d2e1992296d7c5c6a93b2336873335584fa837270ce4545954`.
- `openspec/specs/data-governance/spec.md` : `85c5176f49270a9eb45a51329fc200f8d1cb293bfa6bc93e62eb7fe88999ddfe`.
- `openspec/specs/data-lifecycle/spec.md` : `a3498cc4d3622d569fc9e3f8251a5c5324a9b3d1c612fe014618146297083426`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
