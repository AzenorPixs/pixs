# Exigences de réalisation — C06

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 proposé ajoute les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| api / 8 | [Application de l'exception Super Admin](../../specs/api/spec.md#L8) | P | API tenant-scoped du Super Admin |
| api / 18 | [Contrats OpenAPI versionnés par majeure](../../specs/api/spec.md#L18) | P | Rupture sans nouvelle majeure bloquée |
| api / 27 | [Enveloppes stables et erreurs typées](../../specs/api/spec.md#L27) | P | Rejou identique restitué |
| api / 38 | [Périmètre canonique et autorisation à la frontière](../../specs/api/spec.md#L38) | P | Tenant d'en-tête non canonique rejeté |
| authorization / 8 | [Portée du contrôle total du Super Admin](../../specs/authorization/spec.md#L8) | P | Tenant non accordé au Super Admin ; Tenant accordé malgré un refus ACL |
| authorization / 23 | [Exception Super Admin dans toutes les interfaces](../../specs/authorization/spec.md#L23) | P | Même exception selon la façade |
| authorization / 33 | [Contrôles applicatifs dérogeables par le Super Admin](../../specs/authorization/spec.md#L33) | P | Contrôle applicatif dérogé |
| authorization / 43 | [Priorité transversale de l'exception Super Admin](../../specs/authorization/spec.md#L43) | P | Compte ordinaire sans exception ; Contrat structurel sans privilège |
| authorization / 57 | [Modèle Subject Resource Action Context](../../specs/authorization/spec.md#L57) | P | Propriété sans politique refusée |
| authorization / 66 | [Priorité DENY puis ALLOW puis refus](../../specs/authorization/spec.md#L66) | P | Conflit DENY contre ALLOW |
| authorization / 77 | [Évaluation applicative avant exposition](../../specs/authorization/spec.md#L77) | P | Liste filtrée à la source |
| authorization-engine / 8 | [Exception Super Admin distincte des profils préparatoires](../../specs/authorization-engine/spec.md#L8) | P | Profils préparatoires sans privilège ajouté |
| authorization-engine / 17 | [Politiques déclaratives versionnées](../../specs/authorization-engine/spec.md#L17) | P | Politique à code rejetée |
| authorization-engine / 26 | [Décisions et filtrage tracés](../../specs/authorization-engine/spec.md#L26) | P | Décision périmée non réutilisée |
| authorization-engine / 37 | [Groupes bornés et délégation auditée](../../specs/authorization-engine/spec.md#L37) | P | Moteur indisponible |
| authorization-engine / 48 | [Profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L48) | P | Sélecteur générique refusé |
| authorization-engine / 57 | [Conditions typées du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L57) | P | Booléen distinct d'un entier |
| authorization-engine / 68 | [Assurances et faits du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L68) | P | Fait inconnu refusé fermé ; Assurances non substituables |
| authorization-engine / 82 | [Limites et obligations du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L82) | P | Obligation inconnue rejetée |
| authorization-engine / 91 | [Obligations honorées par le PEP du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L91) | P | ALLOW minimal avec obligation honorée |
| authorization-engine / 100 | [Snapshot et priorité du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L100) | P | DENY prévaut sur ALLOW mêmes cibles |
| authorization-engine / 109 | [Calcul d'expiration du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L109) | P | Auth expirée malgré TTL |
| authorization-engine / 120 | [Transitions temporelles et réévaluation du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L120) | P | ALLOW expire à activation future DENY |
| authorization-engine / 129 | [Confiance backend et diagnostics du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L129) | P | Booléen client insuffisant |
| authorization-engine / 140 | [Plateforme et intertenant du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L140) | P | Intertenant minimal refusé ; Plateforme ALLOW explicite ; Plateforme sans explicite refusée |
| contracts / 17 | [Versionnement SemVer indépendant](../../specs/contracts/spec.md#L17) | P | Champ obligatoire ajouté |
| contracts / 26 | [Dépréciation et retrait encadrés](../../specs/contracts/spec.md#L26) | P | Suppression anticipée bloquée |
| core / 8 | [Module obligatoire au-dessus du noyau](../../specs/core/spec.md#L8) | P | Composition sans core refusée |
| core / 17 | [Primitives minimales communes](../../specs/core/spec.md#L17) | P | Primitive consommée par contrat |
| core / 31 | [Aucun fournisseur concret imposé](../../specs/core/spec.md#L31) | P | Substitution de fournisseur |
| core / 102 | [Autorités et limites du profil identité structurel](../../specs/core/spec.md#L102) | P | Identité structurelle sans assurance implicite |
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
| scope-context / 8 | [Périmètre explicite du Super Admin](../../specs/scope-context/spec.md#L8) | P | Accord tenant sans changement de propriété |
| scope-context / 18 | [Tenant racine et parenté unique](../../specs/scope-context/spec.md#L18) | P | Cycle de scopes refusé |
| scope-context / 29 | [Propriété canonique unique](../../specs/scope-context/spec.md#L29) | P | Scope sans tenant cohérent refusé |
| scope-context / 40 | [Contexte immuable propagé avant autorisation](../../specs/scope-context/spec.md#L40) | P | Contexte TENANT sans tenant refusé ; Contexte PLATFORM avec identifiants refusé ; Scope orphelin refusé |
| scope-context / 59 | [Propagation et frontière d'autorisation du ScopeContext](../../specs/scope-context/spec.md#L59) | P | Élargissement implicite refusé ; Contexte PLATFORM sans identifiants accepté sans octroyer permission ; Accès plateforme sans permission refusé et audité |
| security / 8 | [Exception applicative réservée au Super Admin](../../specs/security/spec.md#L8) | P | Revendication root sans authentification propre |
| security / 17 | [Profil de sécurité déclaré par composant](../../specs/security/spec.md#L17) | P | Vulnérabilité critique bloquante |
| security / 26 | [Échec fermé sans mode permissif](../../specs/security/spec.md#L26) | P | Contexte non vérifiable refusé |
| security / 37 | [Diagnostics sans exposition sensible](../../specs/security/spec.md#L37) | P | Secret hors journaux |

## Empreintes SHA-256 du canon

- `openspec/specs/api/spec.md` : `58abd35620d8a6e9c65b0f525e8afda12a2291b9a531bba9248643be3afd3152`.
- `openspec/specs/authorization-engine/spec.md` : `bd9de765f72d4700da314f81dbce9d3d0ee532f3bcc5be319f005ffbfd18b20b`.
- `openspec/specs/authorization/spec.md` : `87c9799579008033f39e47a579b8bf536f0d9c8973d678750a540a02ea63166f`.
- `openspec/specs/contracts/spec.md` : `ad08fabc8ff78db8678ec873c9c50235b57fdf2554111d48adf57f274e4a3897`.
- `openspec/specs/core/spec.md` : `d0eb213fa2fbb3ccca042133d910166b35f4a3e8e60178ad02b12420034bada3`.
- `openspec/specs/events/spec.md` : `31af2e0a1ae55bc575b9f0edb906e73d0b707e8c68458d680155251ea587bf14`.
- `openspec/specs/interactions/spec.md` : `9a2e9186b51c70c17781e2395da3e42f83dd2cc90da36bab624d90397d4ab9a0`.
- `openspec/specs/jobs/spec.md` : `6e5c0e3a2dbef7670a6a129821d110188fc2efb283334b1a4ebfda74a80ed421`.
- `openspec/specs/scope-context/spec.md` : `4a8df881b08f5b4e3c302b9966bff199276350cab9a236a9f8ff2330d28d1270`.
- `openspec/specs/security/spec.md` : `c033c6fa6a6fc43d6e7e3295cd7dc7f554bbcbe0c12cb9baf0431acd6f7a685f`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
