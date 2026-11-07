# Exigences de réalisation — C10

État courant : le développeur valide techniquement 1.1 sur sa portée documentaire ; sa case reste non cochée sur instruction explicite. 1.2 reste OUVERTE avec ses barrières. La [validation technique documentaire](design.md#validation-technique-documentaire-de-la-tâche-11) précise cette décision ; les mentions antérieures d’absence de validation complète ou de tâches ouvertes décrivent leurs états historiques, sans annuler cet acquis ni valoir qualification produit.

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

## C10-CONCEPTION-R1 — couverture exhaustive du canon

Relevé du 28 octobre 2026 : empreintes des trois canons ci-dessus inchangées ; 19 exigences et 20 scénarios. Cette table complète la sélection historique, conserve ses statuts ND/P et renvoie au texte intégral de chaque scénario. Aucune recette exécutée ni qualification déduite.

| Capacité / exigence exacte | Scénarios exacts | Traçabilité |
|---|---|---|
| [backup-disaster-recovery — Stratégie déclarée par déploiement](../../specs/backup-disaster-recovery/spec.md) | Procédure sans objectifs déclarés | R-08 |
| [backup-disaster-recovery — Périmètres de sauvegarde distincts](../../specs/backup-disaster-recovery/spec.md) | Sauvegarde partielle | R-08 |
| [backup-disaster-recovery — Restauration cohérente et réapplication des gouvernances](../../specs/backup-disaster-recovery/spec.md) | Objet restauré après suppression validée | R-05 / R-08 |
| [backup-disaster-recovery — Tests de restauration isolés et preuves](../../specs/backup-disaster-recovery/spec.md) | Démarrage après restauration | R-08 |
| [backup-disaster-recovery — Restauration destructive autorisée et auditée](../../specs/backup-disaster-recovery/spec.md) | Suppression implicite refusée | R-08 |
| [data-governance — Application de l'exception Super Admin](../../specs/data-governance/spec.md) | Dérogation de gouvernance dans un tenant accordé | R-06 |
| [data-governance — Profil de gouvernance versionné par composant](../../specs/data-governance/spec.md) | Flux sortant sans consommateur refusé | R-01 |
| [data-governance — Classification restrictive par défaut](../../specs/data-governance/spec.md) | Export non classifié refusé | R-01 |
| [data-governance — Demandes relatives aux données tracées](../../specs/data-governance/spec.md) | Effacement propagé | R-02 |
| [data-lifecycle — Application de l'exception Super Admin](../../specs/data-lifecycle/spec.md) | Purge demandée malgré un legal hold | R-06 |
| [data-lifecycle — Dimensions et états distincts](../../specs/data-lifecycle/spec.md) | Suppression logique tracée ; Vocabulaire commun de rétention fermé | R-03 / R-07 |
| [data-lifecycle — Vocabulaire commun des stratégies de suppression](../../specs/data-lifecycle/spec.md) | Vocabulaire déclaratif distinct de la persistance | R-07 |
| [data-lifecycle — Purge autorisée, auditée et idempotente](../../specs/data-lifecycle/spec.md) | Purge prématurée refusée | R-04 |
| [data-lifecycle — Tombstones contre la résurrection](../../specs/data-lifecycle/spec.md) | Restauration sans résurrection | R-05 |
| [data-lifecycle — Profil structurel préparatoire de tombstone v1](../../specs/data-lifecycle/spec.md) | Structure valide sans effet | R-07 |
| [data-lifecycle — Référence, version et instant du profil tombstone-v1](../../specs/data-lifecycle/spec.md) | Version et instant du tombstone structurel | R-07 |
| [data-lifecycle — Références optionnelles du profil tombstone-v1](../../specs/data-lifecycle/spec.md) | Références opaques sans exemption | R-07 |
| [data-lifecycle — Validation pure du profil tombstone-v1](../../specs/data-lifecycle/spec.md) | Structure invalide refusée sans écho | R-07 |
| [data-lifecycle — Limites des garanties du profil tombstone-v1](../../specs/data-lifecycle/spec.md) | Tombstone structurel distinct d'une preuve d'effacement | R-07 |

### Compléments de traçabilité

- R-01 : D1 couvre les propriétaires des données effectivement persistées, Agent compris via CP-07. Liste exacte des ressources et consommateurs à arrêter ; aucun profil non publié réputé disponible.
- R-05 : D3 couvre les effacements et restrictions post-snapshot ; propriétaire, mécanisme, complétude et fraîcheur restent ouverts. Le profil mémoire tombstone-v1 ne prouve pas cette garantie.
- R-07 : réutiliser les vocabulaires et validateurs par propriétaire, Agent compris, sans nouvelle valeur, transition ni autorité ajoutée aux structures.
- R-08 : C10 fournit les faits, C16 restaure et N05 coordonne la réadmission ; contrats et preuves restent à arrêter, sans journal externe choisi implicitement.

Voir les [décisions et paramètres ouverts](design.md#registre-des-décisions-et-paramètres-ouverts). Q1.4-GOV-SOURCE/Q1.4-C10-PUBLISH et l’exception Super Admin canonique restent acquis. Aucun delta ni changement de canon dans cette édition.

## C10-CONCEPTION-R2 — traçabilité users/PLATFORM

Inventaire D1 et unité users/PLATFORM validés par le développeur, voir [design.md](design.md#c10-conception-r2--inventaire-d1-et-unité-usersplatform). Les 68 modèles recensés sont présents dans les sources, sans disponibilité runtime déduite. Les 13 modèles Bulk ne sélectionnent pas Bulk.

| Référence | Application à la première unité | Limite ou paramètre ouvert |
|---|---|---|
| R-01 / CP-01 et CP-03 à CP-06 applicables | CoreUser, users, USER, PLATFORM, pixs.core.identity.read ; profil publié couvrant explicitement collection/références, classification CONFIDENTIAL/PERSONAL adoptée pour cette unité. | Références du profil et des consommateurs, finalité, politiques, résidence/processeurs et configuration protégée encore ouverts ; aucun profil incomplet ni valeur de fixture admis implicitement. |
| R-06 / CP-03 | Autorisation C04 et exception Super Admin canonique conservées ; lecture métier avec audit/reçus techniques possibles. | Contrôles ordinaires, périmètre et faits techniques non fabriqués par une dérogation ; preuves d’intégration futures. |
| R-07 | Réutilisation des structures, références et contrôles du chemin query_core existant. | Pas de nouvelle valeur structurelle, transition ni permission déduite de l’inventaire ; pas d’ACCESS complet ni export revendiqué. |
| R-05 et R-08 / CP-08 | D3 reste applicable aux futures phases d’effacement/restauration/réadmission. | Aucune source post-snapshot nouvelle réalisée pour ce raccord ; propriétaire, stockage, complétude et fraîcheur restent ouverts, sans garantie post-restauration. |

La couverture des 19 exigences et 20 scénarios de R1 reste entière ; la première unité ne sélectionne pas tous leurs traitements et n’exempte aucune clause applicable. Les preuves futures incluent nominal, profil absent/révoqué/divergent, ressource non couverte, classification divergente, autorisation refusée, rollback et perte de validité avant restitution, avec PostgreSQL réel. Aucun test produit exécuté par cette consignation ; aucun delta normatif nouveau établi.

## D2-USERS-R1 — références adoptées et preuves futures

Les [références, consommateurs, finalité et politiques](design.md#d2-users-r1--profil-consommateurs-et-politiques) sont validés documentairement par le développeur. Profil pixs.core.governance.users.platform.read.v1, version 1.0.0 ; data_asset_id pixs.core.data.users ; propriétaire pixs.core ; source pixs.core.source.postgresql.users.v1 ; classe user_reference ; CONFIDENTIAL/PERSONAL. La finalité pixs.core.purpose.users.administration.v1 couvre la consultation administrative autorisée ; lignée pixs.core.lineage.users.platform.read.v1.

| Traçabilité | Choix documentaire acquis | Contrôle futur et limite |
|---|---|---|
| R-01 / CP-01 | Profil versionné et couverture explicite de la collection USER/PLATFORM et des références individuelles. | Comparer governance_ref persisté et data_asset_id avant exposition ; divergence refusée sans reclassement implicite. Présence d’un nom opaque distincte d’une publication autorisée. |
| R-01 / CP-03 / CP-06 applicables | authorized_consumers : pixs.core.consumer.query.users.platform.v1 et pixs.backend.consumer.http.core.users.v1. | Vérifier liaison aux composants/versions, contexte et autorisation ; destinataire HTTP final ouvert avant qualification de bout en bout. Aucun consommateur supplémentaire implicite. |
| R-01 / R-03 / R-06 | Références pixs.core.retention.users.v1, pixs.core.deletion.users.v1, pixs.core.export.users.v1 ; exception Super Admin canonique conservée. | Lecture sans prolongation de rétention ni purge, mutations et export dédié hors unité ; durées, critères et politiques techniques audit/reçus ouverts. |
| R-01 / R-07 | Résidence pixs.core.residency.users.platform.v1 ; processor_refs vide pour cette unité. | Vérifier emplacements/replications et absence effective de processeur externe avant activation ; toute présence supplémentaire à déclarer. Les références ne modifient pas les validateurs structurels. |
| R-05 / R-08 / CP-08 | D3 et la séparation C10/C16/N05 sont conservés. | Aucun fait de fraîcheur, source post-snapshot ni réadmission démontré par le profil ou sa lignée. |

Les noms sont adoptés ; paramètres opérationnels non arrêtés toujours ouverts selon design.md. Versions et empreintes de publication, autorités, fraîcheur et configuration protégée à fournir et qualifier ; aucun défaut de fixture. Le destinataire HTTP, les emplacements et les liaisons effectives des consommateurs ne sont pas réputés définis par leurs seules références.

La couverture des 19 exigences et 20 scénarios reste inchangée. Les refus de profil absent/révoqué/divergent, ressource non couverte, classification divergente et autorisation refusée, ainsi que rollback et perte de validité avant restitution, restent des preuves futures à produire dans la réalisation. Aucun delta, changement de canon ou test produit exécuté par cette consignation.

## D2-USERS-COMPAT-R1 — traçabilité de la compatibilité

C1–C5 sont adoptées documentairement ; voir les [décisions et conditions ouvertes](design.md#d2-users-compat-r1--compatibilité-des-classifications). Le data_asset_id pixs.core.data.users et la classification CONFIDENTIAL/PERSONAL de D2-USERS-R1 restent acquis.

| Traçabilité | Décision acquise | Preuve future et limite |
|---|---|---|
| R-01 / CP-01 — C1/C2 | Égalité exacte du triplet governance_ref/confidentiality/personal ; réutilisation des lignes compatibles sans modification. | Observer les classifications de la cible puis qualifier couverture du profil, attestation, filtrage et revalidation ; collection vide ou réussite sous dérogation insuffisantes. |
| R-01 / R-03 / R-06 — C3 | Données divergentes ou NULL conservées ; refus ordinaire existant, exception canonique préservée, aucun alias ni conversion implicite. | Tester référence différente, confidentialité/donnée personnelle divergentes, NULL et page contenant un élément divergent ; aucun résultat partiel fabriqué par omission. |
| R-01 / R-07 — C4 | Cohérence nécessaire des profils producteurs et lecteurs ; aucune valeur pixs.core.data.users imposée aux futures lignes par le seul profil de lecture. | Examiner séparément le chemin de création et les cas de dérogation ; aucune adaptation de producteur autorisée par la présente décision. |
| R-01 / R-03 / R-05 / R-08 — C5 | Reclassement éventuel distinct, propriétaire et explicitement autorisé. | Besoin, périmètre, concurrence, audit, dérivés et reprise ouverts ; pas de migration implicite ni preuve post-restauration déduite. |

L’inspection agrégée proposée n’est pas exécutée : cible/méthode autorisées, répartition réelle et besoin de reclassement restent OUVERTS. Prévoir catégories sans double comptage et total de contrôle, ventilation par état de persistance, date et périmètre ; sans UUID, contenu métier ou ancienne référence personnalisée affichés. Une inspection ne prouve ni fonctionnement du raccord ni compatibilité future des créations.

La couverture des 19 exigences et 20 scénarios et les empreintes canoniques restent inchangées. C1–C5 précisent les choix de compatibilité sans nouveau delta normatif établi. Aucun test produit exécuté ni valeur d’exploitation observée par cette consignation.

## C10-INSPECTION-R1 — traçabilité du plan agrégé

Le [plan d’inspection et ses bornes](design.md#c10-inspection-r1--plan-dinspection-agrégée) sont adoptés documentairement par le développeur. Cible et accès restent ouverts ; aucune inspection exécutée, implémentation ou coche.

| Traçabilité | Méthode et contrôle adoptés | Limite |
|---|---|---|
| R-01 / CP-01 / C1–C3 | Classer chaque champ du triplet en CIBLE/ABSENT/AUTRE, croiser les trois catégories et l’état de persistance ; compter dans un snapshot READ ONLY / REPEATABLE READ. | Triplet cible pixs.core.data.users / CONFIDENTIAL / PERSONAL ; aucune valeur persistée constatée par le plan. Sommes disjointes égales au total, sans normalisation. |
| R-01 / R-03 / R-06 | Vérifier identité de cible, structure, droits, visibilité et lecture seule ; minimiser la sortie en catégories/comptes. | Pas d’UUID, contenu utilisateur, ancienne référence personnalisée ou secret restitué. Visibilité partielle = PARTIEL, sans contournement automatique de RLS ni verdict global. |
| R-01 / R-07 | Attente verrou 1 s, instruction 5 s, abandon global après 15 s ; aucun réessai automatique. | Expiration/interruption = NON CONCLUANT ; aucun échantillonnage ni augmentation automatique ; mécanisme effectif non implémenté ici. |
| R-01 / C4 | Inspection complète des états de persistance, total et date/périmètre. | Une table vide ou une inspection historique ne garantit pas les classifications des créations futures. |
| R-05 / R-08 / C5 et CP-08 | Décision de reclassement éventuel séparée après observation, sous propriétaire et autorisation propres. | Ni migration, reclassement ni réadmission post-restauration autorisés par le plan. |

Le serveur déclaré dans DEVOPS n’est qu’un candidat ; base, environnement, schéma, rôle/mécanisme d’accès, preuve de visibilité et périmètre de restitution restent OUVERTS. Aucune lecture de project.env ou configuration privée pour cette édition ; accès local approuvé sans secret transmis requis avant exécution future. La méthode de tests serait distincte de la preuve sur données applicatives.

La couverture des 19 exigences et 20 scénarios et les empreintes canoniques restent inchangées. Ces bornes d’inspection ne modifient pas les budgets produit ni le canon ; aucun delta normatif nouveau établi. Les tests et observations de fonctionnement restent non exécutés.

## C10-INSPECTION-CIBLE-R1 — traçabilité de la cible et des accès

Le [cadrage de cible et d’accès](design.md#c10-inspection-cible-r1--cible-et-accès) est adopté documentairement, avec toutes les valeurs non fournies conservées OUVERTES. Aucun accès à la base, lecture de secrets ou inspection exécutée.

| Traçabilité | Choix acquis | Preuve et limite |
|---|---|---|
| R-01 / CP-01 | Cible identifiée par environnement, déploiement, machine d’exécution, endpoint, base, schéma et relation. | Seuls endpoint candidat, client et table sont déclarés ; cible effective ouverte. Boucle locale ne prouve pas identité du déploiement ; aucun schéma supposé. |
| R-01 / R-06 / CP-03 | Accès existant approuvé, référence non secrète, profil de transport/authentification ; voie opérateur recommandée. | Droits, mécanisme, opérateur et autorisation effective de périmètre à établir ; aucun compte/rôle/privilège créé ni accès implicite. Alternative agent conditionnée à un mécanisme existant gardant les secrets hors de ses lectures/sorties. |
| R-01 / CP-01 / C1–C3 | Preuve explicite de visibilité complète, y compris RLS, filtres et périmètre de connexion. | Sans preuve complète : PARTIEL, même si les lignes visibles correspondent au triplet ; aucun changement de rôle ni contournement RLS automatique. |
| R-01 / R-07 | Restitution agrégée et minimisée selon C10-INSPECTION-R1, avec désignation non secrète de cible. | Autorisation de restitution dans la conversation et responsable de preuve ouverts ; aucune donnée de connexion sensible ou contenu de fichier d’accès demandé. |

La méthode et les bornes C10-INSPECTION-R1 sont conservées ; ce cadrage ne démontre ni classifications réelles, ni fonctionnement de users/PLATFORM, ni besoin de reclassement. D3 demeure ouvert pour ses phases. Couverture des 19 exigences et 20 scénarios et empreintes canoniques inchangées ; aucun delta normatif nouveau établi ni test produit exécuté.

## C10-INSPECTION-VISIBILITE-R1 — traçabilité de la preuve

Le [protocole de visibilité](design.md#c10-inspection-visibilite-r1--preuve-de-visibilité) est validé documentairement. La preuve reste distincte des comptes agrégés et du verdict de classification ; aucune observation de base ou lecture de secrets dans cette édition.

| Traçabilité | Contrôles adoptés | Conditions ouvertes et limite |
|---|---|---|
| R-01 / CP-01 | Identité précise de la table, schéma, absence de vue intermédiaire ; structure inattendue à réexaminer. | Cible et structure effectives OUVERTES ; le seul nom pixs_core_user ne prouve pas le bon objet. |
| R-01 / R-06 / CP-03 | Concordance locale rôle de connexion/rôle effectif/accès approuvé ; droits effectifs de connexion, schéma et colonnes ; contexte sans changement de rôle ni intermédiaire SECURITY DEFINER. | Accès, rôle et droits réels OUVERTS ; aucune élévation ni autorisation déduite d’une exemption technique. |
| R-01 / CP-01 / C1–C3 | Activation/forçage RLS, application effective au rôle, politiques SELECT/ALL, rôles, prédicats, combinaisons et dépendances. | Sans preuve de portée totale : au plus PARTIEL ; absence de déclaration RLS dans les sources examinées distincte d’absence déployée. Aucun contournement automatique. |
| R-01 / R-07 | Même session/transaction pour preuve et agrégats, stabilité administrative documentée, restitution minimale non secrète. | Stabilité, opérateur et preuves restent OUVERTS ; changement de rôle/droits/politiques impose réexamen. Erreur/expiration/mauvaise cible/droits insuffisants : NON CONCLUANT, sans réessai. |

Superutilisateur, BYPASSRLS et propriétaire selon le forçage doivent être constatés sans modification, puis rapprochés de l’accès approuvé. Deux comptes sous le même filtre ou un total nul ne démontrent pas l’exhaustivité. Les références officielles PostgreSQL 16 et les détails de conclusion figurent dans design.md.

Les bornes C10-INSPECTION-R1 restent 1 s / 5 s / 15 s sans réessai. Couverture des 19 exigences et 20 scénarios et empreintes canoniques inchangées ; aucun delta normatif nouveau établi, aucune inspection ni test produit exécuté. Les points D2/D3 non arrêtés restent ouverts.

## C10-INSPECTION-RAPPORT-R1 — traçabilité du format

Le [format Markdown du rapport](design.md#c10-inspection-rapport-r1--format-du-rapport) est validé documentairement. Il décrit une restitution future en six parties, sans créer un rapport de résultats ni préremplir des observations. Inspection actuelle NON EXÉCUTÉE ; aucune donnée ni preuve de visibilité disponible.

| Traçabilité | Format adopté | Limite et contrôle futur |
|---|---|---|
| R-01 / CP-01 / C1–C3 | Agrégats détaillés des combinaisons CIBLE/ABSENT/AUTRE, ventilés par état ; synthèse total/cible/autres. | Combinaisons disjointes ; totaux cohérents dans le même snapshot ; omission = zéro uniquement si agrégation achevée/cohérente dans sa portée. N/A motivé distinct de zéro. |
| R-01 / R-06 / CP-03 | Preuve distincte de visibilité avec résultat unitaire et référence de preuve ; verdict COMPLÈTE DÉMONTRÉE/PARTIELLE/NON DÉMONTRÉE. | NON APPLICABLE justifié, aucune preuve manquante remplacée ; aucun identifiant de connexion ni prédicat sensible exposé. |
| R-01 / R-07 | Séparer exécution, visibilité, cohérence des agrégats, classification et conclusion globale ; six parties avec identité/portée et limites/suites. | Visibilité complète distincte de compatibilité ; table vide distincte de classification compatible ; erreur/expiration/incohérence = NON CONCLUANTE, absence d’exécution = NON EXÉCUTÉE. |
| R-05 / R-08 / C5 et CP-08 | Suites proposées distinguées des faits et interprétations. | Aucun reclassement, producteur futur ou raccord qualifié ; aucune réadmission post-restauration déduite d’un rapport. |

États reconnus ACTIVE/ARCHIVED/SOFT_DELETED/PURGE_PENDING ; valeurs hors vocabulaire ou absentes sous AUTRE sans valeur brute. Pas de pourcentage par défaut, UUID ou contenu utilisateur. Les agrégats partiels décrivent uniquement les lignes visibles ; aucune compatibilité globale sans preuve complète. Les références de cible, accès, dates et périmètre sont à renseigner selon leur autorisation de restitution.

Cible, accès, preuves et paramètres D2/D3 non arrêtés restent ouverts ; bornes 1 s / 5 s / 15 s sans réessai conservées. Couverture des 19 exigences et 20 scénarios et empreintes canoniques inchangées ; aucun delta normatif nouveau établi ni inspection/test produit exécuté.

## C10-INSPECTION-ACCEPTATION-R1 — traçabilité des critères

La [grille documentaire A01–A16](design.md#c10-inspection-acceptation-r1--critères-du-rapport) est adoptée après validation explicite du développeur. Ce sont des cas de vérification future du rapport, tous NON EXÉCUTÉS, sans nouveau scénario normatif canonique. Un rapport recevable peut décrire une inspection non concluante ou partielle.

| Traçabilité | Cas | Critères à vérifier ultérieurement |
|---|---|---|
| R-01 / CP-01 / C1–C3 | A01–A04 | Inspection complète avec triplet cible ou écarts, table vide distinguée de classification compatible, états comptés sans omission. |
| R-01 / R-06 / CP-03 | A05–A08 | Restreindre les conclusions aux lignes visibles ; aucune compatibilité globale, table vide ou extrapolation déduite d’un sous-ensemble. |
| R-01 / R-07 | A09–A12 | Arrêt sur cible/structure/accès incorrects, erreur/expiration, comptes incohérents ou preuves non raccordables ; pas de correction, rôle changé ou réessai automatique. |
| R-01 / R-06 / R-07 | A13–A15 | NON EXÉCUTÉE sans compte inventé ; zéro omis seulement sous conditions de portée/achèvement/cohérence ; NON APPLICABLE justifié sans preuve manquante masquée. |
| R-05 / R-08 / C5 et CP-08 | A16 | Confidentialité et limites de conclusion ; rapport non recevable s’il expose des éléments interdits ou prétend qualifier raccord, producteurs futurs ou restauration par les seuls agrégats. |

Priorité des verdicts : absence d’exécution → NON EXÉCUTÉE ; erreur/incohérence/preuve invalidée → NON CONCLUANTE ; agrégation exploitable mais visibilité limitée/non démontrée → PARTIELLE ; exécution achevée, agrégats cohérents et visibilité complète → CONCLUANTE avec classification distincte. Un résultat d’inspection défavorable n’est pas un échec de recevabilité si le rapport le décrit correctement.

Les six parties et la minimisation du format restent exigées ; N/A motivé distinct de zéro et suites proposées distinctes d’actions autorisées. Points ouverts de cible/accès/visibilité/restitution et D2/D3 conservés, bornes 1 s / 5 s / 15 s sans réessai inchangées. Couverture des 19 exigences et 20 scénarios canoniques et empreintes inchangées ; aucun test produit ni inspection exécuté, aucun delta normatif nouveau établi.

## C10-INSPECTION-SYNTHETIQUES-R1 — traçabilité des maquettes

Les [maquettes SYNTH-A01 à SYNTH-A16](design.md#c10-inspection-synthetiques-r1--maquettes-documentaires) sont adoptées documentairement après validation du développeur. Nombres et preuves sont FICTIFS ; leur exécution réelle reste NON EXÉCUTÉE. Les six parties du format sont reprises par une enveloppe commune, sans preuve réelle ou donnée d’exploitation inventée.

| Traçabilité | Maquettes | Attentes et limites |
|---|---|---|
| R-01 / CP-01 / C1–C3 | SYNTH-A01 à SYNTH-A04 | Comptes cibles, divergents, nuls ou ventilés par état ; verdicts complets sous visibilité complète supposée. A02 : 7+2+1=10 ; A04 : 5+2+1+1+1+2=12, cible 9/autres 3 ; aucune conformité du cycle de vie déduite. |
| R-01 / R-06 / CP-03 | SYNTH-A05 à SYNTH-A08 | Totaux visibles 6, 8, 0 et 6 ; conclusions PARTIELLES, sans totalité extrapolée ni table vide déduite du zéro visible. |
| R-01 / R-07 | SYNTH-A09 à SYNTH-A12 | Cible incorrecte, expiration, incohérence volontaire 7+4≠10, contextes différents ; NON CONCLUANTE, sans correction ou réessai automatique. |
| R-01 / R-06 / R-07 | SYNTH-A13 à SYNTH-A15 | Non-exécution, omission conditionnelle des zéros, non-applicabilité justifiée ; variantes négatives explicites. |
| R-05 / R-08 / C5 et CP-08 | SYNTH-A16 | Décrire sans reproduire de valeur interdite ; rapport non recevable si confidentialité ou limite de qualification violée. Aucun verdict global accepté sur le document incorrect. |

Une synthèse attendue peut être recevable tout en concluant à une inspection partielle ou non concluante. La correction arithmétique ne démontre pas la portée ; les preuves supposées restent fictives. Les valeurs volontairement incohérentes d’A11 sont conservées comme contre-exemple, jamais comme agrégat réel ni résultat corrigé.

Points de cible/accès/visibilité/restitution et D2/D3 non arrêtés toujours ouverts ; bornes 1 s / 5 s / 15 s sans réessai conservées. Couverture des 19 exigences et 20 scénarios canoniques et empreintes inchangées ; aucun nouveau scénario normatif, inspection, test produit ou implémentation dans cette consignation.

## C10-INSPECTION-SYNTHETIQUES-REVUE-R1 — traçabilité des corrections

Les [maquettes complétées et variantes](design.md#c10-inspection-synthetiques-revue-r1--maquettes-complétées) sont adoptées documentairement, toutes NON EXÉCUTÉES réellement. Chaque cas précise six parties, métadonnées/preuves/fenêtre UTC fictives, exécution simulée et verdicts distincts, sans attestation ni résultat produit réel.

| Traçabilité | Correction | Limite |
|---|---|---|
| R-01 / CP-01 / C1–C3 | Ventilations A01=10 ACTIVE cibles, A05=6, A06=8, A08=4 cibles+2 références AUTRE ; A03/A07 vides. A02/A04 conservées. | Sommes synthétiques seulement ; visibilité complète/partielle explicitement supposée, aucune donnée réelle. |
| R-01 / R-06 / CP-03 | A06 : agrégation achevée/cohérente sans erreur, preuve de portée manquante seulement. A15 positive : seul examen détaillé de politiques NON APPLICABLE. | Contrôles de cible, rôle, droits et état RLS toujours nécessaires ; aucune extrapolation. |
| R-01 / R-07 | A12 : somme correcte mais agrégats NON VÉRIFIÉS et classification NON ÉVALUABLE, faute de contextes raccordables ; NON CONCLUANTE. | Arithmétique seule insuffisante ; aucun assemblage artificiel de preuves. |
| R-01 / R-07 | Variantes A09 : cible/droits/structure ; A10 : 1/5/15 s ; A11 : somme/clé dupliquée/négatif/non entier ; A14 : omission positive/négative. | Attentes documentaires non testées ; contre-exemples conservés, aucun réessai, changement de rôle ou correction automatique. |
| R-05 / R-08 / C5 et CP-08 | A15 négative et A16 confidentialité/extrapolation : recevabilité rejetée avec motif, sans donnée interdite reproduite. | Aucun verdict global accepté sur un candidat incorrect ; aucune qualification du raccord/producteur/restauration. |

Les nombres synthétiques adoptés sont conservés ; variantes nouvelles explicitent des défauts déjà couverts par les critères, sans nouveau scénario normatif. Cible/accès/preuves/restitution et paramètres D2/D3 non arrêtés restent ouverts ; bornes 1 s / 5 s / 15 s inchangées. Couverture des 19 exigences et 20 scénarios canoniques et empreintes inchangées. Aucun test produit, inspection ou implémentation.

## Corrections finales des variantes A14 et A15 négatives

Les [corrections finales](design.md#corrections-finales-des-variantes-a14-et-a15-négatives) sont adoptées documentairement après validation du développeur. Elles corrigent l’héritage des hypothèses fictives, sans changer le canon ni exécuter les cas.

| Traçabilité | Substitution adoptée | Résultat attendu et limite |
|---|---|---|
| R-01 / R-07 — A14 négative | Exécution INTERROMPUE et absence d’agrégat complet établies, remplaçant ACHEVÉE/COHÉRENTS du parent positif ; comptes indisponibles N/A. | Candidat complétant par zéro non recevable ; diagnostic attendu NON CONCLUANTE, agrégats NON VÉRIFIÉS, classification NON ÉVALUABLE. Aucun verdict global accepté sur le candidat incorrect. |
| R-01 / R-06 / CP-03 — A15 négative | Preuve de désactivation RLS et visibilité complète du parent retirées ; RLS applicable au rôle et portée non établie ; agrégation achevée/cohérente sans autre erreur. | NON APPLICABLE injustifié : candidat non recevable. Diagnostic correct : visibilité NON DÉMONTRÉE, comptes cohérents dans la portée observée, inspection au plus PARTIELLE, sans compatibilité globale. Aucun verdict global accepté sur le candidat incorrect. |

Variantes positives et nombres initiaux conservés ; contrôles nécessaires de cible/rôle/droits/état RLS maintenus. Toutes les maquettes sont fictives et réellement NON EXÉCUTÉES. Points de cible/accès/preuves/restitution et D2/D3 non arrêtés restent ouverts ; bornes 1 s / 5 s / 15 s sans réessai inchangées. Couverture des 19 exigences et 20 scénarios et empreintes canoniques inchangées ; aucun delta normatif nouveau établi, aucune inspection ni test produit.

## Revue finale validée des maquettes A01–A16

Le développeur valide la [revue documentaire finale](design.md#revue-finale-validée-des-maquettes-a01a16). Les seize maquettes et seize variantes corrigées sont conformes aux critères examinés ; aucune correction supplémentaire nécessaire identifiée dans le périmètre documentaire. Les hypothèses A14/A15 négatives remplacent explicitement celles de leurs parents positifs ; A12 conserve NON VÉRIFIÉS malgré une somme correcte.

| Traçabilité | Conclusion acquise | Limite |
|---|---|---|
| R-01 / CP-01 / C1–C3 | A01–A04 : dénombrement/classification distincts, sommes et combinaisons détaillées cohérentes. | Nombres fictifs ; aucune donnée réelle ni compatibilité d’exploitation constatée. |
| R-01 / R-06 / CP-03 | A05–A08 et A15 : portée limitée, preuve de visibilité et non-applicabilité justifiée correctement distinguées. | Rôle, droits, RLS et politiques effectifs restent à établir. |
| R-01 / R-07 | A09–A14 : arrêts, incohérences, défaut de preuve commune, non-exécution et omission conditionnelle du zéro correctement traités ; priorité des verdicts respectée. | Vérification documentaire seulement, aucun test exécuté ni réussite produit déduite. |
| R-05 / R-08 / C5 et CP-08 | A16 et variantes : confidentialité et limites de conclusion respectées dans les supports ; candidats incorrects non recevables. | Aucun raccord, producteur futur, reclassement ou réadmission qualifié/autorisé par les agrégats. |

Cible, accès, opérateur, droits/RLS/stabilité, preuve de visibilité, restitution, classifications réelles et paramètres D2/D3 non arrêtés restent ouverts ; éventuel reclassement distinct. Les 19 exigences et 20 scénarios canoniques et leurs empreintes restent inchangés. Bornes 1 s / 5 s / 15 s sans réessai conservées, inspection réelle NON EXÉCUTÉE. Cette validation de revue ne clôture pas 1.1/1.2 et n’autorise aucune implémentation ; aucun delta normatif nouveau établi.

## C10-CLOTURE-CONCEPTION-R1 — traçabilité des conditions de clôture

Le [plan de clôture documentaire](design.md#c10-cloture-conception-r1--acquis-et-barrières) est validé pour consignation uniquement. Les conditions de 1.1 et 1.2 sont distinctes ; aucune tâche n’est close ou cochée.

| Traçabilité | Acquis | Travail et preuves restant nécessaires |
|---|---|---|
| R-01 à R-08 / CP-01 à CP-08 — 1.1 | Canon/C00 revus, matrices, inventaire D1, unité users/PLATFORM et décisions documentaires consignés ; maquettes revues. | Bilan consolidé par objectif : applicabilité C10/unité, sources actuelles, preuves réutilisables/fixtures, décisions/écarts/dépendances non vérifiées, travaux C10 et propriétaires C08/C16/N05 ; validation documentaire de ce bilan acquise sous C10-BILAN-1.1-R1, sans clôture de tâche. |
| R-01 / R-06 / R-07 — 1.2 | Références D2-USERS-R1, classification et C1–C5 acquis ; Q1.4-GOV-SOURCE/Q1.4-C10-PUBLISH conservés. | Après validation de 1.1 : politiques opérationnelles utilisateurs/audit/reçus, publication/configuration protégée, consommateurs/HTTP/résidence, producteurs et présentation des fichiers/contrats avant code. |
| R-02 à R-05 / R-08 / CP-08 — 1.2 | Frontières de propriété, distinction phases et orientation D3 documentées. | Droits des demandes, rétention/holds/purge/dérivés ; source post-snapshot et contrats C16/N05 à arrêter ; éventuel delta normatif à déterminer avant réalisation dépendante. |

La revue documentaire doit identifier les inconnues sans les assimiler à des prérequis satisfaits. Inspection et qualification futures ne constituent pas la preuve de la seule revue ; en conception, leur méthode et leurs critères doivent être définis sans résultat anticipé. Le contrat de validation existant et les tests par unité dès réalisation sont conservés.

Les acquis partiels users/PLATFORM ne réduisent pas la portée de 1.2. Bilan C10-BILAN-1.1-R1 désormais consigné et validé documentairement ; dix tâches toujours ouvertes. Paramètres D2/D3, cible/accès/preuves/restitution et reclassement éventuel ouverts, inspection NON EXÉCUTÉE. Couverture des 19 exigences et 20 scénarios et empreintes inchangées ; bornes 1 s / 5 s / 15 s sans réessai conservées ; aucun delta normatif nouveau établi, test produit ou implémentation.

## C10-BILAN-1.1-R1 — traçabilité consolidée validée

Le [bilan consolidé R-01–R-08](design.md#c10-bilan-11-r1--rapprochement-consolidé) est présenté puis validé documentairement par le développeur. Il rapproche chaque objectif des acquis, du canon/C00, des contrats CP, des sources actuelles et des dépendances non vérifiées. Les tableaux antérieurs restent les références détaillées des exigences/scénarios ; aucune exigence ni applicabilité supprimée par l’unité users/PLATFORM.

| Objectif | Acquis de revue | Reste à traiter, sans disponibilité supposée |
|---|---|---|
| R-01 | D1/D2, profils, classification, contrats et sources de catalogue/raccord présents. | Publication/configuration, consommateurs, profils techniques, compatibilité des lignes et raccord ordinaire. |
| R-02 | Cinq demandes et structure DataSubjectRequest à onze champs recensées. | Traitement propriétaire, droits, audit, idempotence et propagation ; lecture users distincte d’ACCESS complet. |
| R-03 | Dimensions distinctes et transitions du fournisseur initial refusées. | Contrats de transition, rétention et raccords propriétaires ; aucun changement d’état dans l’unité. |
| R-04 | Maintenance audit et travaux propriétaires existants identifiés. | Fournisseur des faits courants, mandat Job et propagation ; purge générale non déduite de C05. |
| R-05 | Orientation D3 et tombstone mémoire à huit champs distinct du durable. | Source post-snapshot et preuves avec C16/N05 ; aucune garantie de non-résurrection acquise. |
| R-06 | Décideur et dérogation propriétaires présents, branches canoniques conservées. | Qualification réelle des points d’application ; succès sous dérogation distinct de compatibilité ordinaire. |
| R-07 | Vocabulaires/validateurs et profil à quinze champs conservés. | Relier références et politiques effectives ; aucune nouvelle autorité structurelle. |
| R-08 | Frontières C10/C16/N05 identifiées. | Objectifs, faits courants, réconciliation et recettes de reprise à arrêter/qualifier. |

Les contrats archivés et résultats historiques sont réutilisables seulement dans leur portée et après confrontation aux versions consommées ; participants synthétiques C10 distincts d’une preuve intégrée fraîche. Maquettes documentaires validées distinctes de cas exécutés. Inspection, publications réelles et qualifications restent non prouvées.

Validation documentaire du bilan acquise, sans clôture de tâche ou coche. Les sept barrières de 1.2 et les points de cible/accès/visibilité/restitution/D2/D3 et reclassement éventuel restent ouverts. Canon : 19 exigences et 20 scénarios référencés, empreintes inchangées ; aucun delta normatif nouveau établi. Bornes 1 s / 5 s / 15 s sans réessai conservées ; aucun accès de base, secret lu, recette produit ou implémentation.

## Validation technique documentaire de la tâche 1.1

Le développeur valide techniquement 1.1 sur sa portée documentaire, après bilan consolidé et revue finale. Voir la [portée de validation](design.md#validation-technique-documentaire-de-la-tâche-11). Cet acquis distinct de la seule validation du bilan est consigné sans accès à la base, lecture de secrets, implémentation ou coche.

| Traçabilité | Validation acquise | Limite conservée |
|---|---|---|
| R-01–R-08 / CP-01–CP-08 | Revue documentaire, rapprochement canon/C00/sources/contrats, décisions et limites des preuves historiques et dépendances non vérifiées. | Aucune publication effective, classification réelle ou intégration qualifiée déduite de cette revue. |
| Passage 1.1 vers 1.2 | Validation technique documentaire de 1.1 désormais acquise ; case volontairement non cochée. | 1.2 OUVERTE avec ses sept barrières ; aucun feu vert implicite à 2.1 ou aux autres réalisations. |
| R-05 / R-08 / CP-08 et D2/D3 | Inconnues explicitement conservées dans le bilan validé. | Paramètres opérationnels et dépendances non vérifiées toujours ouverts ; aucune restauration ou réadmission qualifiée. |

Couverture des 19 exigences et 20 scénarios et empreintes canoniques inchangées. Les dix cases restent non cochées par instruction expresse ; la validation de revue n’est pas un résultat de recette produit. Cible/accès/visibilité/restitution et reclassement éventuel ouverts ; bornes 1 s / 5 s / 15 s sans réessai inchangées. Aucun delta normatif nouveau établi ni implémentation.

## C10-POLITIQUES-OPERATIONNELLES-R1 — traçabilité des politiques

Les [politiques et décisions P1–P6](design.md#c10-politiques-operationnelles-r1--utilisateurs-audit-et-reçus) sont adoptées documentairement pour users/PLATFORM, avec paramètres non arrêtés OUVERTS. La validation ne constitue ni publication effective, ni configuration, ni réalisation de maintenance.

| Traçabilité | Règles acquises | Décisions/preuves restant nécessaires |
|---|---|---|
| R-01 / R-03 / R-06 / CP-01 | Politiques utilisateurs existantes conservées ; lecture sans prolongation de rétention ni suppression, transfert ou export supplémentaire implicite ; C1–C5 et exception canonique préservées. | Départ/durée ou critères de fin, états archivés/supprimés et holds de la source utilisateur à arrêter ; aucune classification persistée observée. |
| R-01 / R-04 / R-06 / CP-04 | Audit pixs.core.audit.users.platform.v1, version 1.0.0 ; propriétaire C05, minimisation, contrôle de lecture et append-only en usage normal. | retention_days strictement positif, profil/classification propres, origine/autorité, max_event_bytes/max_query_records et occultations ; évolution de politique historique explicite. |
| R-01 / R-04 / R-05 / R-07 | Reçus : pixs.backend.retention.c10.receipts.v1 et pixs.backend.deletion.c10.receipts.v1, distincts de la politique utilisateur ; prepared_at et stage distincts d’un commit. | Responsable de cycle de vie, consommateurs, classification, durée/départ, dépendances et mécanisme de fin de conservation compatibles avec l’immutabilité. Aucun UPDATE/DELETE ni purge autorisé par une référence. |
| R-02 à R-08 / CP concernés | P1–P6 : séparation, configuration explicite, historique, maintenance distincte, préservation des preuves nécessaires et durées à arrêter. | Aucun défaut permissif, valeur de fixture, suppression rétroactive ou conservation illimitée adoptés implicitement ; faits courants et contrôles requis avant maintenance. |

Le [canon audit](../../specs/audit/spec.md), notamment contenu minimal, minimisation, append-only et portée de dérogation, reste applicable en complément des trois canons comptés dans la couverture historique de 19 exigences/20 scénarios. Cette couverture et ses empreintes restent inchangées ; aucune modification normative nouvelle établie par la présente consignation. Un nouveau comportement normatif éventuel du mécanisme de maintenance nécessiterait son delta préalable approuvé.

Validation technique documentaire 1.1 conservée, case non cochée ; 1.2 ouverte, barrière des politiques non entièrement levée. Paramètres D2/D3 et inspection/reclassement non arrêtés ouverts, bornes d’inspection 1 s / 5 s / 15 s sans réessai inchangées. Aucune durée de conservation chiffrée choisie ; aucune base consultée, secret lu, implémentation ou test produit.

## C10-CONSERVATION-R1 — traçabilité des ancres et durées

Les [événements de départ et DUR1–DUR6](design.md#c10-conservation-r1--événements-durées-et-maintenance) sont adoptés documentairement par le développeur, sans accès à la base, lecture de secrets, implémentation ni coche. Les durées chiffrées et paramètres non arrêtés restent OUVERTS.

| Traçabilité | Décisions acquises | Conditions et preuves encore nécessaires |
|---|---|---|
| R-01 / R-03 / CP-01 | Pas d’expiration utilisateur depuis création/lecture ; période après suppression depuis transition propriétaire durable/confirmée SOFT_DELETED. ARCHIVED ne vaut pas suppression. | Fin de finalité/réexamen, durée/finalité résiduelle, dépendances/holds et preuve stable de suppression ; updated_at seul insuffisant. |
| R-04 / R-06 / CP-04 | Ancre audit created_at avec retention_days historique ; durée/version/origine enregistrées conservées, aucun raccourcissement rétroactif implicite. | Durées par catégorie et finalités à choisir ; entier strictement positif selon AuditPolicy ; faits courants et contrôles de maintenance toujours requis. |
| R-01 / R-04 / R-05 / CP concernés | Reçus : clôture durable avec issue réconciliée comme ancre future, pas prepared_at ni simple présence d’un reçu. | Responsable et preuve de clôture, réconciliation, durée, dépendances consommées et mécanisme compatible avec l’immutabilité ; aucune suppression rendue possible par l’échéance seule. |
| R-03 à R-08 / CP concernés | DUR1–DUR6 : ancre stable, holds/dépendances, éligibilité distincte de purge, historique, ancre manquante explicite, mécanisme non inventé. | Exceptions canoniques préservées ; pas de valeur de fixture, date fabriquée ou conservation illimitée adoptées. Tout effet rétroactif exige décision propre. |

Chaque durée exige une valeur et une justification explicites, indépendantes pour utilisateurs/audits/reçus ; aucune durée commune ou chiffrée sélectionnée ici. Les bornes 1 s / 5 s / 15 s concernent l’inspection seulement. Tout contrat persistant ou comportement nouveau de maintenance doit être examiné pour déterminer un éventuel delta normatif avant réalisation.

Validation technique documentaire de 1.1 conservée, case non cochée ; 1.2 ouverte avec ses barrières et paramètres D2/D3 non arrêtés. Les 19 exigences et 20 scénarios des trois canons comptés et leurs empreintes restent inchangés, canon audit également préservé. Aucune inspection, recette, opération de maintenance ou implémentation.

## C10-DUREES-R1 — traçabilité des valeurs et CH1–CH6

Les [valeurs, justifications et CH1–CH6](design.md#c10-durees-r1--valeurs-justifications-et-décisions) sont adoptés documentairement par le développeur. Les nombres ne sont plus des paramètres indéterminés dans ce périmètre ; déploiement, preuves d’ancrage et mécanismes effectifs restent ouverts. Aucun accès à la base, lecture de secrets, implémentation ni coche.

| Traçabilité | Valeur et décision acquises | Conditions encore nécessaires |
|---|---|---|
| R-01 / R-03 / CP-01 — CH1/CH2 | 30 jours après SOFT_DELETED durable/confirmé ; réexamen de finalité actif/archivé tous les 90 jours sans expiration automatique. | Preuve stable de suppression, responsable et ancre du réexamen, dépendances/holds ; aucune date déduite de updated_at seul. |
| R-04 / R-06 / CP-04 — CH1/CH3 | 186 jours d’audit depuis created_at pour les nouveaux événements du périmètre/version désignés. | Anciennes durées/version/origine préservées ; reprise de l’existant sur décision distincte. Autres paramètres AuditPolicy et faits courants de maintenance à arrêter. |
| R-01 / R-04 / R-05 — CH1/CH5 | 90 jours de reçus après clôture durable avec issue réconciliée ; réexamen des blocages à l’échéance. | Issue inconnue sans ancre calculable, prepared_at insuffisant ; références encore nécessaires et immutabilité opposables, aucune purge rendue possible par la durée. |
| R-01 / R-02 / R-07 — CH4 | Revue de minimisation audits/reçus avant activation ; durées distinctes et UTC, jours de 24 h. | UUID/références non réputés anonymes ; données conservées après suppression de source à justifier et minimiser, sans réécriture historique implicite. |
| R-03 à R-08 — CH6 | Réévaluation après 90 premiers jours d’exploitation effective ou plus tôt si conditions changent. | Départ d’exploitation non constaté ; aucun changement automatique. Raccord, producteurs et restauration non qualifiés par les durées. |

Le repère CNIL est explicité dans design.md ; 186 jours ne vaut ni équivalence réglementaire automatique ni garantie de conformité. Les choix chiffrés sont techniques et soumis à la définition du déploiement/finalité. Toute maintenance conserve autorisations, holds, références et contrôles canoniques ; aucune conservation illimitée ou valeur de fixture adoptée.

Validation technique documentaire 1.1 acquise, case non cochée ; 1.2 ouverte et dix cases inchangées. Déploiement, responsables, ancres, minimisation et mécanismes de maintenance ainsi que D2/D3 non arrêtés restent ouverts. Couverture des 19 exigences et 20 scénarios des trois canons comptés et empreintes inchangées, canon audit préservé ; aucun delta normatif nouveau établi ou test produit. Bornes d’inspection 1 s / 5 s / 15 s sans réessai distinctes et inchangées.

## C10-MINIMISATION-R1 — traçabilité des champs et MIN1–MIN6

Les [champs et décisions MIN1–MIN6](design.md#c10-minimisation-r1--audits-et-reçus-après-suppression) sont adoptés documentairement, sans accès à la base, lecture de secrets, implémentation ni coche. Règles de maintenance d’audit distinctes de restitution de reçus immuables et de minimisation effective de leur conservation.

| Traçabilité | Choix documentaire acquis | Limite et preuve encore nécessaires |
|---|---|---|
| R-01 / R-02 / R-04 / CP-04 | generic.actor_reference/resource_id : pseudonymisation seulement ; generic.reason_or_error : occultation possible ; pdp.subject_id/resource_id : deux modes possibles selon nécessité. | Maintenance propriétaire C05, sélection autorisée par personne et preuves de liens ; aucun remplacement global indistinct. |
| R-01 / R-04 / R-07 | Conserver champs nécessaires d’action/résultat/instant, références techniques et empreintes pour la traçabilité justifiée. | Champs sans règle actuelle non réputés modifiables ; réidentification et nécessité résiduelle à examiner, traitement C01 séparé. |
| R-01 / R-04 / R-05 | Originaux des reçus immuables ; synthèse minimisée avec catégories/comptes et résultat de vérification plutôt qu’identifiants/empreintes lorsque suffisant. | Pas d’occultation persistante en place, de reçu transformé équivalent ou d’intégrité prouvée par la seule synthèse ; fin de conservation encore ouverte. |
| R-02 à R-08 / CP concernés | MIN1–MIN6 : déclenchement, sélection, nécessité résiduelle, pseudonymisation de confiance, intégrité et restitution séparée. | Aucune donnée individuelle affichée pour prouver une minimisation ; mécanisme, périmètre et autorisations effectifs à arrêter. |

Suppression logique, décision d’effacement/minimisation et preuves nécessaires aux opérations/holds/réconciliations restent distinctes. Pseudonyme, UUID ou empreinte non réputés anonymes ; référence publique et limites techniques dans design.md. Aucun nouveau droit ou mode structurel ajouté. Les [obligations audit](../../specs/audit/spec.md) et exceptions canoniques demeurent applicables.

Durées 30/186/90 jours inchangées, sans remise à zéro ni maintenance automatique. Validation technique documentaire 1.1 acquise, case non cochée ; 1.2 ouverte avec paramètres D2/D3 non arrêtés, dix cases inchangées. Sélection/liens d’identité/pseudonymisation/nécessité résiduelle/C01/champs non modifiables et fin de conservation des reçus OUVERTS. Couverture historique des 19 exigences et 20 scénarios et empreintes inchangées, canon audit préservé ; aucun delta normatif nouveau établi ou test produit exécuté. Tout nouveau comportement persistant éventuel à examiner avant réalisation.

## C10-RAPPROCHEMENT-R1 — traçabilité des critères et preuves

Les [critères, statuts et RAP1–RAP6](design.md#c10-rapprochement-r1--sélection-et-preuves-propriétaires) sont adoptés documentairement par le développeur. Aucun accès à la base, lecture de secrets, implémentation ni coche ; absence d’enregistrement d’instance rapproché.

| Traçabilité | Choix acquis | Preuve ou décision restant ouverte |
|---|---|---|
| R-01 / R-02 / CP-01/CP-02 — RAP1/RAP2 | Références exactes, rôles acteur/cible/composite distincts ; identité numérique différente de CoreUser ; attribution historique prouvée. | Interfaces, source/durabilité/version/période des liens et contradictions à établir. Lien actif actuel ou instant seul insuffisant. |
| R-01 / R-04 / CP concernés — RAP3 | Chaîne reçu/opération-demande/acteur/utilisateur ; validation propriétaire du reçu et resource_refs. | Reçu sans acteur direct ; correlation_id/pid/xid/empreinte isolés insuffisants, aucune inversion ou tentative d’identifiants. |
| R-02 à R-08 — RAP4/RAP5 | Statuts distincts, incertitude explicite, visibilité/exhaustivité et déduplication sans perdre les motifs. | Aucun traitement sur candidat indirect/non vérifiable/conflictuel ; absence de résultat incomplet distincte d’absence de lien. |
| R-02 / R-04 / R-05 / R-06 — RAP6 | Sélection établie ouvre l’examen MIN1–MIN6, pas l’autorisation de transformer. | Décisions de champs/nécessité résiduelle distinctes ; autres acteurs, intégrité, C01 et dépendances préservés, reçus immuables. |

La grille de preuve minimale est documentaire : type, rôle, critère, référence propriétaire, version/période, contexte, statut/motif ; aucune API nouvelle ni donnée réelle attestée. Restitution agrégée sans UUID ni contenu personnel. Interfaces/historique/conflits/conservation des preuves/exhaustivité et paramètres D2/D3 non arrêtés restent OUVERTS.

Durées 30/186/90 jours conservées, sans durée inventée pour de nouvelles preuves ; bornes 1 s / 5 s / 15 s sans réessai inchangées. Validation technique documentaire 1.1 acquise, case non cochée ; 1.2 ouverte, dix cases conservées. Couverture historique des 19 exigences et 20 scénarios et empreintes inchangées, canon audit préservé ; aucun delta normatif nouveau établi, inspection ou test produit exécuté.

## C10-HISTORIQUE-LIENS-R1 — traçabilité des sources historiques

Les [sources, contrôles et HIST1–HIST6](design.md#c10-historique-liens-r1--sources-et-contrôles-historiques) sont validés documentairement. État courant et audit isolé restent distincts d’un historique complet ; aucune disponibilité de source ou donnée d’instance attestée par cette édition.

| Traçabilité | Décisions acquises | Preuves ou mécanismes ouverts |
|---|---|---|
| R-01 / R-02 / CP-01/CP-02 — HIST1/HIST3 | Références/couple exacts, preuve propriétaire Core, période ou ordre causal établi. | Interfaces, faits disponibles, source/provenance/version et temporalité à établir ; aucun lien ancien déduit du seul état actif actuel. |
| R-01 / R-04 / CP concernés — HIST2/HIST4 | Effet confirmé distinct d’autorisation/stage/publication/livraison ; rejeu confirmé distinct de nouvelle transition. | Résultat propriétaire et réconciliation d’issue inconnue, déduplication contractuelle ; version de couple non comparée comme séquence globale. |
| R-02 à R-08 — HIST5/HIST6 | Historique manquant/expiré/occulté signalé, conflit non résolu conservé. | Exhaustivité, conflits et conservation/minimisation de preuve à arrêter ; absence de trace ne prouve pas absence de lien. |

Sources candidates : liens conservés, résultats propriétaires/idempotence, audit C05, outbox/preuves C09 et instantanés identifiés ; limites explicites dans design.md. Le besoin d’un nouveau journal n’est examiné qu’en cas d’insuffisance démontrée, sans création ni sélection implicite. Grille de preuve documentaire, restitution agrégée sans UUID/contenu individuel ; faits détaillés chez les propriétaires.

Interfaces/faits/temps/complétude/déduplication/conflits/conservation restent OUVERTS. Durées 30/186/90 jours conservées sans extension automatique à une nouvelle source. Validation technique documentaire 1.1 acquise, case non cochée ; 1.2 ouverte avec paramètres D2/D3 et dépendances non vérifiées, dix cases inchangées. Couverture historique 19 exigences/20 scénarios et empreintes inchangées, canon audit préservé ; aucune inspection ni recette produit, aucun delta normatif nouveau établi. Bornes 1 s / 5 s / 15 s sans réessai inchangées.
