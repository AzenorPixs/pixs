# Exigences de réalisation — C10

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Les titres, scénarios, lignes et empreintes ci-dessous ont été recoupés avec les trois canons courants le 26 octobre 2026. Les statuts ND/P sont ceux de la matrice de préparation historique ; ils ne sont pas recalculés en verdicts de livraison par cette réconciliation. Une nouvelle dérive impose une relecture avant réalisation. La sélection reste à appliquer par clause et selon le périmètre effectif, sans annoncer que les scénarios ont déjà été exécutés.

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

- `openspec/specs/backup-disaster-recovery/spec.md` : `f65f7a5bcc30a42d99453e8675c4cca16eb902b8f5b5127b43864e88828e683e`.
- `openspec/specs/data-governance/spec.md` : `85c5176f49270a9eb45a51329fc200f8d1cb293bfa6bc93e62eb7fe88999ddfe`.
- `openspec/specs/data-lifecycle/spec.md` : `a3498cc4d3622d569fc9e3f8251a5c5324a9b3d1c612fe014618146297083426`.

Ces empreintes portent sur les octets des fichiers canoniques au relevé documentaire du 26 octobre 2026. L'empreinte backup-disaster-recovery de préparation était périmée ; sa correction suit la relecture du texte courant, sans modification du canon ni qualification d'une restauration.

## Traçabilité des objectifs, scénarios, contrats et tâches

Les identifiants R-01 à R-08 relient les obligations existantes aux [contrats CP-01 à CP-08](design.md#matrice-des-contrats-propriétaires) et aux tâches conservées. Ils n'ajoutent aucune exigence ni scénario OpenSpec. Les critères indiquent les preuves futures attendues ; aucun résultat applicatif n'est acquis par cette table.

| Réf. / objectif | Exigences et scénarios canoniques | Contrats propriétaires | Tâches existantes | Critère observable et limite actuelle |
|---|---|---|---|---|
| R-01 — profils publiés et données classifiées | data-governance : Profil de gouvernance versionné par composant / Flux sortant sans consommateur refusé ; Classification restrictive par défaut / Export non classifié refusé | CP-01, CP-02, CP-06, CP-07 ; CP-08 pour le raccord initial | 1.1–1.2, 2.1 ; 2.4 et 3.1–3.2 pour consolidation | Profil de chaque propriétaire effectivement livré, consommateur et garanties documentés, exposition non classifiée refusée avec diagnostic/audit selon le canon. Catalogue, ponts et reçus initiaux présents ; publication autorisée et qualification intégrée non établies ici. |
| R-02 — demandes ACCESS/EXPORT/RECTIFY/ERASE/RESTRICT | data-governance : Demandes relatives aux données tracées / Effacement propagé | CP-01 à CP-07 selon propriétaire et dérivés présents | 1.2, 2.2 ; 2.3 pour propagation ; 2.4 et 3.1–3.2 | Command autorisée et auditée, rejeu sans double effet, décision appliquée par les services propriétaires à la source et aux dérivés déclarés avec holds/rétention. DataSubjectRequest reste une représentation déclarative ; son traitement effectif n'est pas démontré. |
| R-03 — suppression logique et rétention distinctes | data-lifecycle : Dimensions et états distincts / Suppression logique tracée ; Vocabulaire commun de rétention fermé | CP-01, CP-03, CP-04, CP-07 | 1.1–1.2, 2.2, 2.4, 3.1–3.2 | État de persistance séparé de l'état métier et de rétention, transition propriétaire avec version/contexte courants. Le fournisseur initial refuse les transitions ; les mutations propriétaires déjà présentes ne qualifient pas leur intégration C10. |
| R-04 — purge explicite idempotente | data-lifecycle : Purge autorisée, auditée et idempotente / Purge prématurée refusée | CP-01, CP-03 à CP-07 selon données concernées | 1.2, 2.3–2.4, 3.1–3.2 | Job autorisé, vérifications courantes rétention/holds/références/projections, audit, reprise sans double effet et refus ordinaire motivé. La maintenance audit C05 est réutilisée chez son propriétaire ; elle ne fournit pas une purge générale C10. |
| R-05 — tombstones et restauration sans résurrection | data-lifecycle : Tombstones contre la résurrection / Restauration sans résurrection ; backup-disaster-recovery : Restauration cohérente et réapplication des gouvernances / Objet restauré après suppression validée | CP-01, CP-04, CP-06 à CP-08 | 1.2, 2.3–2.4, 3.2 | Source des effacements et holds applicables, y compris postérieurs au snapshot, définie et vérifiable ; réapplication avant exposition, divergence bloquée ou rendue explicite et auditable. Le seul tombstone mémoire ou présent dans le snapshot ne prouve pas cette garantie. |
| R-06 — dérogation Super Admin bornée | data-governance : Application de l'exception Super Admin / Dérogation de gouvernance dans un tenant accordé ; data-lifecycle : Application de l'exception Super Admin / Purge demandée malgré un legal hold | CP-01, CP-03, CP-04 et autres points d'application concernés | 1.1–1.2, 2.1–2.4, 3.2 | Dérogation courante du seul compte canonique dans son périmètre accordé, contrôles ordinaires et refus intertenant préservés ; aucune autorité anticipée du futur compte initial. Les profils préparatoires restent sans droit. |
| R-07 — conservation des structures préparatoires | data-lifecycle : Vocabulaire commun des stratégies de suppression et exigences du profil structurel tombstone-v1, avec tous leurs scénarios | CP-01 à CP-08 selon structures consommées | 1.1–1.2, 2.1–2.3, 3.2 | Réutilisation des vocabulaires et validateurs existants sans défaut, transition ou garantie runtime ajoutés à ces structures ; les détails de leurs scénarios canoniques restent applicables. Aucune modification de ces sources par la réconciliation. |
| R-08 — reprise déclarée, isolée et autorisée | backup-disaster-recovery : Stratégie déclarée par déploiement / Procédure sans objectifs déclarés ; Périmètres de sauvegarde distincts / Sauvegarde partielle ; Tests de restauration isolés et preuves / Démarrage après restauration ; Restauration destructive autorisée et auditée / Suppression implicite refusée | CP-08 avec faits courants des propriétaires CP-01 à CP-07 concernés | 1.2, 2.4, 3.2 | C16/N05 conservent objectifs/périmètres, environnement isolé, audit et autorisation de restauration ; C10 apporte ses faits et décisions de gouvernance/effacement. Aucune réémission automatique ni purge implicite pour faciliter la reprise ; contrat concret et preuve à qualifier ensemble. |

Les tâches 1.1/1.2 recoupent l'ensemble des lignes avant leur réalisation dépendante. Les tâches 3.1/3.2 consolident les contrôles déjà requis dans chaque unité ; 3.3 relit portée/impacts et 3.4 conserve les autorisations de clôture distinctes. Cette correspondance inverse couvre les dix tâches sans les cocher ni transformer les contrôles futurs en résultats présents.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
