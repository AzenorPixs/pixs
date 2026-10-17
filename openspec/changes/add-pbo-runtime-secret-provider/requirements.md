# Exigences de réalisation — C01

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 proposé ajoute les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| configuration / 8 | [Schémas typés validés avant activation](../../specs/configuration/spec.md#L8) | P | Configuration invalide bloquée |
| configuration / 17 | [Priorité déterministe des sources](../../specs/configuration/spec.md#L17) | P | Surcharge déterministe |
| configuration / 28 | [Secrets par référence hors artefacts](../../specs/configuration/spec.md#L28) | P | Secret embarqué refusé |
| secrets-providers / 11 | [Références externes sans valeur persistée](../../specs/secrets-providers/spec.md#L11) | P | Diagnostic de référence indisponible |
| secrets-providers / 22 | [Accès runtime associé à une identité de workload](../../specs/secrets-providers/spec.md#L22) | P | Worker non autorisé |
| secrets-providers / 33 | [Rotation, durée de vie et révocation contrôlées](../../specs/secrets-providers/spec.md#L33) | P | Secret tourné |
| secrets-providers / 47 | [Audit minimisé et échec fermé](../../specs/secrets-providers/spec.md#L47) | P | Provider indisponible |

## Empreintes SHA-256 du canon

- `openspec/specs/configuration/spec.md` : `8e710a2390f044b0d5f78ddf68546e3310eddbb878eea29171ea5608dd425904`.
- `openspec/specs/secrets-providers/spec.md` : `8e134d9117ca775984f14c91fb75e042fdf7612b8f6f81a336be93b8673b1dff`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
