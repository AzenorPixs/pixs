# Exigences de réalisation — C09

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 proposé ajoute les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| events / 8 | [Événements immuables versionnés](../../specs/events/spec.md#L8) | P | Contrat d'intégration séparé |
| events / 17 | [Publication après validation transactionnelle](../../specs/events/spec.md#L17) | P | Transaction échouée sans événement |
| events / 26 | [Consommateurs idempotents et ordonnés](../../specs/events/spec.md#L26) | P | Rejou sans double effet |
| events / 35 | [Profil préparatoire de déclaration d'enregistrement d'événement v1](../../specs/events/spec.md#L35) | P | Déclaration passive de contrat de domaine ; Contrat d'intégration distinct |
| events / 49 | [Validation fermée de la déclaration d'enregistrement v1](../../specs/events/spec.md#L49) | P | Référence ou type étranger refusé ; Contrat porté invalide |
| events / 63 | [Frontière préparatoire de la déclaration d'enregistrement v1](../../specs/events/spec.md#L63) | P | Validité structurelle sans admission runtime |
| events / 72 | [Runtime Bulk v1 B11 — Outbox et publication](../../specs/events/spec.md#L72) | P | Rollback sans publication ; Livraison répétée |
| interactions / 8 | [Application de l'exception Super Admin](../../specs/interactions/spec.md#L8) | P | Command propriétaire avec dérogation métier |
| interactions / 18 | [Commandes validées et autorisées](../../specs/interactions/spec.md#L18) | P | Mutation sans autorisation refusée |
| interactions / 27 | [Requêtes sans mutation implicite](../../specs/interactions/spec.md#L27) | P | Lecture filtrée à la source |
| interactions / 36 | [Idempotence et traçabilité des commandes](../../specs/interactions/spec.md#L36) | P | Rejou divergent |
| interactions / 45 | [Runtime Bulk v1 B10 — Idempotence durable](../../specs/interactions/spec.md#L45) | P | Rejeu identique ; Rejeu divergent |
| jobs / 8 | [Exécution asynchrone demandée par le Super Admin](../../specs/jobs/spec.md#L8) | P | Worker sans compte de service Super Admin ; Nouvelle exécution après désactivation |
| jobs / 22 | [Contrôles applicatifs des Jobs et exception](../../specs/jobs/spec.md#L22) | P | Dérogation portée par la demande initiale |
| jobs / 31 | [Persistance et états explicites](../../specs/jobs/spec.md#L31) | P | Reprise après interruption |
| jobs / 40 | [Autorisation réévaluée à l'exécution](../../specs/jobs/spec.md#L40) | P | Contexte expiré refusé |
| jobs / 49 | [Idempotence et corrélation des travaux](../../specs/jobs/spec.md#L49) | P | Double déclenchement dédupliqué |
| jobs / 58 | [Runtime Bulk v1 B08 — Jobs et liaison persistante](../../specs/jobs/spec.md#L58) | P | Phase persistante ; Liaison multiple |
| jobs / 72 | [Runtime Bulk v1 B09 — Baux, reprise et configuration](../../specs/jobs/spec.md#L72) | P | Reprise sous bail ; Bail périmé |
| runtime / 8 | [Profils distincts d'un même artefact](../../specs/runtime/spec.md#L8) | P | Profil activé par configuration |
| runtime / 17 | [Profils de déploiement déclarés](../../specs/runtime/spec.md#L17) | P | Capacité absente dans un profil local |
| runtime / 29 | [Exposition minimale par défaut](../../specs/runtime/spec.md#L29) | P | Endpoint de management publiquement joignable |
| runtime / 38 | [Processus stateless et coordination persistante](../../specs/runtime/spec.md#L38) | P | Redémarrage d'un worker ; État technique PA requis en conteneur |
| runtime / 52 | [Lease du scheduler avec clôture de péremption](../../specs/runtime/spec.md#L52) | P | Ancien détenteur toujours actif |
| runtime / 61 | [Arrêt, drain et reprise contrôlés](../../specs/runtime/spec.md#L61) | P | Arrêt pendant traitement |
| runtime / 70 | [États techniques PA distincts du runtime PBO](../../specs/runtime/spec.md#L70) | P | États techniques PA distincts du runtime PBO |

## Empreintes SHA-256 du canon

- `openspec/specs/events/spec.md` : `31af2e0a1ae55bc575b9f0edb906e73d0b707e8c68458d680155251ea587bf14`.
- `openspec/specs/interactions/spec.md` : `9a2e9186b51c70c17781e2395da3e42f83dd2cc90da36bab624d90397d4ab9a0`.
- `openspec/specs/jobs/spec.md` : `6e5c0e3a2dbef7670a6a129821d110188fc2efb283334b1a4ebfda74a80ed421`.
- `openspec/specs/runtime/spec.md` : `0eb07f4494b590fdd845cfe90143a34dc331717b5b38b293dee4b45c100cee11`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
