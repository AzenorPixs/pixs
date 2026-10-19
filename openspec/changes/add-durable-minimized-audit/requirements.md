# Exigences de réalisation — C05

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| audit / 8 | [Audit dérogeable du Super Admin](../../specs/audit/spec.md#L8) | P | Opération Super Admin sans audit persistant ; Audit ordinaire toujours obligatoire |
| audit / 23 | [Portée de l'exception dans les exigences d'audit](../../specs/audit/spec.md#L23) | P | Profil d'occultation inchangé |
| audit / 32 | [Audit fonctionnel distinct des logs techniques](../../specs/audit/spec.md#L32) | P | Perte de télémétrie technique |
| audit / 41 | [Contenu minimal d'un événement d'audit](../../specs/audit/spec.md#L41) | P | Refus d'autorisation tracé |
| audit / 50 | [Périmètre obligatoire d'audit](../../specs/audit/spec.md#L50) | P | Opération destructive sans audit |
| audit / 59 | [Append-only et réécriture contrôlée](../../specs/audit/spec.md#L59) | P | Obligation d'effacement |
| audit / 68 | [Minimisation et non-duplication des données](../../specs/audit/spec.md#L68) | P | Payload sensible détecté |
| audit / 77 | [Audit exhaustif du panneau d'administration](../../specs/audit/spec.md#L77) | P | Navigation non auditable |
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
| data-governance / 8 | [Application de l'exception Super Admin](../../specs/data-governance/spec.md#L8) | P | Dérogation de gouvernance dans un tenant accordé |
| data-governance / 18 | [Profil de gouvernance versionné par composant](../../specs/data-governance/spec.md#L18) | P | Flux sortant sans consommateur refusé |
| data-governance / 27 | [Classification restrictive par défaut](../../specs/data-governance/spec.md#L27) | P | Export non classifié refusé |
| data-governance / 38 | [Demandes relatives aux données tracées](../../specs/data-governance/spec.md#L38) | P | Effacement propagé |
| data-lifecycle / 8 | [Application de l'exception Super Admin](../../specs/data-lifecycle/spec.md#L8) | P | Purge demandée malgré un legal hold |
| data-lifecycle / 18 | [Dimensions et états distincts](../../specs/data-lifecycle/spec.md#L18) | P | Suppression logique tracée ; Vocabulaire commun de rétention fermé |
| data-lifecycle / 43 | [Purge autorisée, auditée et idempotente](../../specs/data-lifecycle/spec.md#L43) | P | Purge prématurée refusée |
| data-lifecycle / 52 | [Tombstones contre la résurrection](../../specs/data-lifecycle/spec.md#L52) | P | Restauration sans résurrection |
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
| secrets-providers / 11 | [Références externes sans valeur persistée](../../specs/secrets-providers/spec.md#L11) | P | Diagnostic de référence indisponible |
| secrets-providers / 22 | [Accès runtime associé à une identité de workload](../../specs/secrets-providers/spec.md#L22) | P | Worker non autorisé |
| secrets-providers / 33 | [Rotation, durée de vie et révocation contrôlées](../../specs/secrets-providers/spec.md#L33) | P | Secret tourné |
| secrets-providers / 47 | [Audit minimisé et échec fermé](../../specs/secrets-providers/spec.md#L47) | P | Provider indisponible |
| security / 8 | [Exception applicative réservée au Super Admin](../../specs/security/spec.md#L8) | P | Revendication root sans authentification propre |
| security / 17 | [Profil de sécurité déclaré par composant](../../specs/security/spec.md#L17) | P | Vulnérabilité critique bloquante |
| security / 26 | [Échec fermé sans mode permissif](../../specs/security/spec.md#L26) | P | Contexte non vérifiable refusé |
| security / 37 | [Diagnostics sans exposition sensible](../../specs/security/spec.md#L37) | P | Secret hors journaux |

## Empreintes SHA-256 du canon

- `openspec/specs/audit/spec.md` : `43d8dd9947fbac84c5decbf829825db577276853f5224e5bacc021c22bf4f513`.
- `openspec/specs/authorization-engine/spec.md` : `bd9de765f72d4700da314f81dbce9d3d0ee532f3bcc5be319f005ffbfd18b20b`.
- `openspec/specs/authorization/spec.md` : `87c9799579008033f39e47a579b8bf536f0d9c8973d678750a540a02ea63166f`.
- `openspec/specs/data-governance/spec.md` : `85c5176f49270a9eb45a51329fc200f8d1cb293bfa6bc93e62eb7fe88999ddfe`.
- `openspec/specs/data-lifecycle/spec.md` : `a3498cc4d3622d569fc9e3f8251a5c5324a9b3d1c612fe014618146297083426`.
- `openspec/specs/observability/spec.md` : `4793cf6252768ea2673a4eb843caf027fb850b586a8fcfee877b5d37d1e6ff98`.
- `openspec/specs/operations/spec.md` : `13835ff9b1d97cf4196a66f2f991f25f0d5c0357ccc54c7bcd1d56dffe38d5f1`.
- `openspec/specs/secrets-providers/spec.md` : `8e134d9117ca775984f14c91fb75e042fdf7612b8f6f81a336be93b8673b1dff`.
- `openspec/specs/security/spec.md` : `c033c6fa6a6fc43d6e7e3295cd7dc7f554bbcbe0c12cb9baf0431acd6f7a685f`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
