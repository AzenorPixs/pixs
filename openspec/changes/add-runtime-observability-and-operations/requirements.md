# Exigences de réalisation — C15

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 proposé ajoute les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| observability / 8 | [Signaux structurés et corrélés](../../specs/observability/spec.md#L8) | P | Corrélation bout en bout |
| observability / 17 | [Santé distinguée et sondes bornées](../../specs/observability/spec.md#L17) | P | Dépendance optionnelle dégradée |
| observability / 26 | [Objectifs de service déclarés](../../specs/observability/spec.md#L26) | P | Objectif sans méthode de mesure |
| observability / 38 | [Rétention et minimisation séparées](../../specs/observability/spec.md#L38) | P | Accès inter-tenant tracé |
| operations / 8 | [Application de l'exception Super Admin](../../specs/operations/spec.md#L8) | P | Intervention de secours pendant une maintenance |
| operations / 17 | [Interface de management distincte et non publique](../../specs/operations/spec.md#L17) | P | Façades convergeant sur le même contrat |
| operations / 26 | [Opérations persistantes avec plan et idempotence](../../specs/operations/spec.md#L26) | P | Rejeu d'une opération annulée |
| operations / 35 | [Sorties sans secret et codes stables](../../specs/operations/spec.md#L35) | P | Commande non autorisée |
| operations / 44 | [État de maintenance avec drainage borné](../../specs/operations/spec.md#L44) | P | Requête reçue pendant le drainage |
| operations / 53 | [Health, diagnostic et audit opérateur](../../specs/operations/spec.md#L53) | P | Réparation via le diagnostic |
| operations / 62 | [Maintenance hiérarchisée](../../specs/operations/spec.md#L62) | P | Maintenance d'une route |
| resilience / 8 | [Isolation des défaillances optionnelles](../../specs/resilience/spec.md#L8) | NE | Fournisseur optionnel en panne isolé |
| resilience / 17 | [Dégradation sans affaiblissement sécurité](../../specs/resilience/spec.md#L17) | NE | Dégradé sans permissivité |
| resilience / 26 | [Révocation et diagnostic des compromissions](../../specs/resilience/spec.md#L26) | NE | Composant compromis bloqué |
| runtime / 8 | [Profils distincts d'un même artefact](../../specs/runtime/spec.md#L8) | P | Profil activé par configuration |
| runtime / 17 | [Profils de déploiement déclarés](../../specs/runtime/spec.md#L17) | P | Capacité absente dans un profil local |
| runtime / 29 | [Exposition minimale par défaut](../../specs/runtime/spec.md#L29) | P | Endpoint de management publiquement joignable |
| runtime / 38 | [Processus stateless et coordination persistante](../../specs/runtime/spec.md#L38) | P | Redémarrage d'un worker ; État technique PA requis en conteneur |
| runtime / 52 | [Lease du scheduler avec clôture de péremption](../../specs/runtime/spec.md#L52) | P | Ancien détenteur toujours actif |
| runtime / 61 | [Arrêt, drain et reprise contrôlés](../../specs/runtime/spec.md#L61) | P | Arrêt pendant traitement |
| runtime / 70 | [États techniques PA distincts du runtime PBO](../../specs/runtime/spec.md#L70) | P | États techniques PA distincts du runtime PBO |

## Empreintes SHA-256 du canon

- `openspec/specs/observability/spec.md` : `4793cf6252768ea2673a4eb843caf027fb850b586a8fcfee877b5d37d1e6ff98`.
- `openspec/specs/operations/spec.md` : `13835ff9b1d97cf4196a66f2f991f25f0d5c0357ccc54c7bcd1d56dffe38d5f1`.
- `openspec/specs/resilience/spec.md` : `b32b0eff946a12be7ee217c5bc2ffe19b763fe015b0dcb4b46c9e8254f43d1f3`.
- `openspec/specs/runtime/spec.md` : `0eb07f4494b590fdd845cfe90143a34dc331717b5b38b293dee4b45c100cee11`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
