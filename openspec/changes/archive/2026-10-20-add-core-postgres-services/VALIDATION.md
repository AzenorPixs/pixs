# Validation locale C02 — primitives Core PostgreSQL

Constats du 20 octobre 2026, RUN cismp1-pixs-05379f7c24c9437c, change unique add-core-postgres-services. Les orientations D01–D04 option A et le contrat R01 existants sont conservés. Aucun delta normatif, nouveau fournisseur, Git, déploiement ou change suivant n’est réalisé.

## Périmètre effectivement réalisé

Modèles/migration propriétaires Core, contraintes PostgreSQL, UUIDv7, contrats par domaine, transactions et verrous, services identité/groupes/tenants/scopes/autorisations, QUERY filtrées en SQL et port d’amorçage R01 fermé. Les façades structurelles restent pures. Le manifest déclare cinq capacités core.* et quinze contrats pixs.core.* en 1.0.0 ; le composant reste en 0.1.0. Le registre natif construit vingt ServiceEntry, sans surcouche ni service privé exposé.

QUERY reçoit un kind fermé, CoreQueryInput et CommandEnvelope ; les cinq façades de domaine contrôlent leurs familles. Le plan fourni par le client n’est pas utilisé. C04 recalcule un plan source borné par FilterConfig.max_filter_requests ; C02 applique les références autorisées et le contexte en SQL avant projection. CorePageItem contient données fermées immuables, version et métadonnées de gouvernance. La capacité CoreFactSource reste interne à la composition C03/C04/C08, jamais publiée comme QUERY ou voie client. C10.stage_read et C05 participent à la même transaction lorsque requis ; leurs preuves sont vérifiées avant retour. Une lecture ne crée pas de claim de commande C06 ni d’outbox.

R01 consomme BootstrapActInput et une cible BootstrapTargetSpec vérifiée par C08. L’opérateur, la décision, les références, le plan et les cibles sont liés et recontrôlés. Effets internes fermés : CREATE_IDENTITY, BIND_SUPER_ADMIN, STAMP_CREDENTIAL, CREATE_TENANT, GRANT_SUPER_ADMIN_TENANT, REUSE_EXISTING. Le trio identité/binding/empreinte est requis pour une création ; REUSE_EXISTING s’emploie seul et ne réinitialise rien. Un tenant ne vaut jamais grant implicite. C03 conserve credentials et empreintes privées ; C08 conserve résultat et marqueur. Core n’enregistre ni secret, ni hash de credential. Le compte futur ne fournit aucune dérogation anticipée ; une dérogation actuelle doit venir de C04. Preuve/plan/port absent ou issue inconnue ferme la voie.

## Preuves natives exécutées

Les blocs PostgreSQL utilisent Django 6.1.2 et PostgreSQL 16.14 (server_version_num 160014). Chaque harnais constate real_pg=true, nettoyage réussi et connexions fermées ; les sorties sont confinées et sanitisées. Les participants C03/C04/C05/C06/C08/C09/C10 sont des doubles synthétiques déclarés, avec écritures SQL réelles et vérification connexion physique/PID/xid/nonce quand ils participent. Ce ne sont pas les implémentations de production de ces lots.

| Code | Preuve et portée | Outil natif | Résultat |
|---|---|---|---|
| U | 346 tests de 28 modules purs Core/Kernel/PDP/filtre/cycles/contrats/manifest/registres ; inclut les cinq contrôles du manifest et huit contrats C02 | prt_15817f3fb001ciPHfmtb4zvq58 | exit 0 |
| M | Migration initiale, recorder atomique, exclusion/reprise, schémas indépendants et refus partiel/inconnu/mixte ; douze indicateurs, migration inchangée depuis cette preuve | prt_1576edb4a001K71GrqXYDGnRHA | exit 0 |
| T | 14 cas de transactions PG, rejeu/hash, rollback, audit/outbox/profil refusés, revalidation et vrai commit réconcilié | prt_157ff8331001OAqxRKRsz0T7ZB | 14/14, exit 0 |
| I | 20 cas identité PG, enrichis D04 User/Identity ARCHIVED→SOFT_DELETED, état C10 courant, conservation et non-résurrection | prt_157f7bf4e001zkVEpgHSZluYi1 | 20/20, exit 0 |
| G | 46 cas topologie/groupes/accords/permissions/rôles/Policy ; inclut les 25 cas préparatoires, non additionnés | prt_157b93c14001G1QYTjLfMPYv4f | 46/46, exit 0 |
| Q | 62 cas QUERY : seize projections, SQL avant décodage, plans substitués/périmés, classification/audit, isolation et waivers stricts | prt_157da4d2f001A3eXcYVbT0NEzV | 62/62, exit 0 |
| R | 58 cas R01 : création/réutilisation, effets fermés, confirmations/proofs, rollback participants, commit inconnu, exclusion et rejeu borné | prt_157f2fd64001QXeWo45slpyTe8 | 58/58, exit 0 |
| D | 72 exigences et 89 références de scénarios dans leurs blocs exacts, 18 SHA-256 canoniques, 38 sources UTF-8/LF et empreintes avant ce rapport | prt_15813d66d0018AEnqg8H5jx9T8 | exit 0, aucune erreur |

Compilation finale des 36 fichiers Python alors écrits : prt_15819426a001HGx2iOa3cSx9b7, exit 0. Le test ciblé de 16 contrôles (manifest/contrats/harnais) prt_157fde5bd001Awjh7Tc2PVMO3N est inclus en partie dans U et n’est pas additionné. Il n’existe pas de lint/type checker configuré dans pyproject.toml pour ce périmètre. Aucun frontend n’est modifié ; aucun résultat navigateur/npm n’est revendiqué.

Le strict OpenSpec ciblé prt_1581b68560017cyZCtK3SnzQnJ retourne exit 0, avec la seule INFO skip_specs : zéro delta est accepté. C’est une validation documentaire. Les résultats standard/strict globaux et le strict après archive restent des contrôles distincts de clôture ; leurs résultats natifs sont conservés au checkpoint et au rapport STATISTIQUES.md, sans transformer un avertissement ou une sortie non nulle en succès.

## Traçabilité des 72 lignes

Cette table complète [la matrice source](requirements.md) et ses clauses/scénarios, sans la remplacer ni ajouter d’exigence. Les codes renvoient aux preuves ci-dessus ; une ligne partagée n’ajoute pas de test. « Propriétaire » ou « en attente » signifie que la garantie intégrée reste condition d’activation, jamais une conformité runtime déclarée sur un double.

| Repère | Preuves locales | Portée, limite et condition |
|---|---|---|
| C02-R01 | U,Q | Déclaration MODULE, quinze contrats et vingt entrées réelles ; composition obligatoire finale propriétaire C07. |
| C02-R02 | U,Q | Primitives et seize projections consommables par contrats ; activation C04/C06 distincte. |
| C02-R03 | U,T,R | Ports substituables injectés ; PostgreSQL initial D01, aucun fournisseur Auth/LDAP imposé. |
| C02-R04 | U,I | UUIDv7, vocabulaires exacts et dimensions identité/persistance distinctes. |
| C02-R05 | I | Unicité active des liaisons, références, contention et historique/version. |
| C02-R06 | I | SERVICE sans User persisté ; aucun privilège déduit de ce type. |
| C02-R07 | U | Import frais des façades sans Django, écriture ni réseau ; profils purs conservés. |
| C02-R08 | U,T,I | Faits vérifiés et autorisation requis ; une structure ne vaut pas authentification. |
| C02-R09 | M | Origine/cible explicites et refus des états inconnus ; consommation C08/C16. |
| C02-R10 | M,T | Exclusion PostgreSQL des exécuteurs et ordre stable des verrous. |
| C02-R11 | M | Installation initiale None→0.1.0 seulement ; aucune origine distribuée de coexistence sélectionnée. |
| C02-R12 | M,T | DDL/recorder atomiques, interruption/reprise et avancement persisté. |
| C02-R13 | M | Aucune contraction proposée ni downgrade automatique ; cas conditionnel non applicable. |
| C02-R14 | G,R | Accords tenant explicites stockés ; l’évaluation de leur autorité reste C04. |
| C02-R15 | G | Racines, parenté, refus des cycles et sérialisation par tenant. |
| C02-R16 | G | Cohérence tenant/scope et FK composites ; aucune propriété métier déplacée. |
| C02-R17 | U,G,Q | Contexte exact immuable, topologie active et orphelins refusés. |
| C02-R18 | T,Q | Autorisation actuelle, contexte exact et refus audités ; PLATFORM ne crée aucun droit. |
| C02-T01 | U | Enregistrement natif et refus des services privés/non déclarés. |
| C02-T02 | U | Ordre et collisions des registres communs vérifiés ; résolution runtime finale C07. |
| C02-T03 | T,Q,R | Identité, contexte, corrélation et preuve transactionnelle contrôlés. |
| C02-T04 | U | COMMAND/QUERY/SERVICE restent des catégories séparées. |
| C02-T05 | U | Contrats/capacités 1.0.0 indépendants du composant 0.1.0. |
| C02-T06 | U | Aucun retrait proposé ; mécanismes communs préservés, retrait conditionnel non applicable. |
| C02-T07 | U,D | Manifest unique sans entrée de secret ; source et diagnostics bornés. |
| C02-T08 | U | Cinq capacités schéma 1, quinze implements et contrats associés exacts. |
| C02-T09 | U | Propriétaire dérivé du composant ; injection d’un autre propriétaire refusée. |
| C02-T10 | G,R | Stockage des accords uniquement ; priorité Super Admin/DENY appartient à C04 intégré. |
| C02-T11 | U,Q,R | Profils purs préservés ; waivers de ports stricts, jamais une preuve d’exception C04 réelle. |
| C02-T12 | T,Q,R | Aucune autorité déduite de la propriété, d’un mode ou d’une cible future. |
| C02-T13 | U,T,Q | PDP pur et décisions DENY refusées localement ; C04 runtime reste à intégrer. |
| C02-T14 | Q | SQL restreint aux références C04 avant projection/décodage ; politique interdite non décodée. |
| C02-T15 | R | Port R01 borné ; aucun import ni autorité métier transférée de C01. |
| C02-T16 | R | Preuve opérateur obligatoire ; mode/UID/reçu technique ne sont pas une permission Core. |
| C02-T17 | U | Validateurs préparatoires conservés sans privilège ni IO nouveau. |
| C02-T18 | U,G | Codec Policy fermé et déclarations C04 transactionnelles ; catalogue/limites runtime C04. |
| C02-T19 | T,Q | Revalidation actuelle, versions et plans périmés/substitués refusés. |
| C02-T20 | G,T,Q | Groupes et paires courantes bornés ; imbrication/délégation non sélectionnées pour C02. |
| C02-T21 | T,Q,R | Audit et participants vérifiés sur même connexion/nonce ; False ne vaut pas preuve. |
| C02-T22 | Q | Plan client ignoré, source recalculée et revalidée ; source-filter-plan non traité comme jeton. |
| C02-T23 | T,I,G,R | Mutations propriétaires refusées sans autorisation actuelle. |
| C02-T24 | Q | QUERY sans claim C06 ni outbox ; pagination HTTP appartient à C06, non prétendue livrée. |
| C02-T25 | T,R | Rejeu confirmé, hash divergent refusé et résultat conservé dans la transaction. |
| C02-T26 | T,R | Effet/outbox/résultat atomiques ; aucune publication réseau C09 prétendue. |
| C02-T27 | Q,R | Audit ordinaire obligatoire et dérogations explicites strictes ; aucune preuve fictive si dérogé. |
| C02-T28 | T,I,Q,R | Audit minimal des autorisations/refus ; stockage C05 simulé en SQL, runtime C05 distinct. |
| C02-T29 | T,R | Indisponibilité du sink requis bloque la confirmation ; aucun fallback C01. |
| C02-T30 | I,Q,R | Références minimisées, pas de champ credential/hash dans Core ; redaction HTTP future C06/C05. |
| C02-T31 | Q,R | Profil publié/couverture des références/consommateur exigés ; C10 réel reste propriétaire. |
| C02-T32 | Q | NULL de classification exclu en SQL sauf dérogation actuelle explicite du port C04. |
| C02-T33 | U,I,G | États distincts ; ARCHIVED→SOFT_DELETED avec CAS, état C10 réel et classification conservée. |
| C02-T34 | U,I,G | Suppression physique non exposée et FK PROTECT ; purge C10/C09 non livrée, non déclarée conforme. |
| C02-T35 | U,Q | Tombstone structuré conservé/projeté ; aucun parcours de restauration/résurrection C10/C16 livré. |
| C02-T36 | T,Q,R | Échecs fermés, ports manquants et preuves incorrectes refusés sans effet Core. |
| C02-T37 | D,I,Q,R | Diagnostics fixes, sorties PG confinées/sanitisées et références seules ; interface HTTP C06 distincte. |
| C02-T38 | R | Compte non nominatif DEVICE admis, pas de User implicite, second binding d’installation refusé ; garde SERVICE revue. |
| C02-T39 | U,D | C02 seul ne fournit ni activation P0 C07 ni qualification C17. |
| C02-T40 | Q,R | Recettes C02 sur SQL réel et participants synthétiques ; intégration C03–C10/C17 en attente. |
| C02-T41 | D | Sources contrôlées ; aucun paquet C18 construit ni composition distribuée C17 qualifiée. |
| C02-T42 | T,R | Absence de C05 bloque ; le journal C01 n’est jamais consommé comme audit métier Core. |
| C02-T43 | T,R | Aucune autorité métier locale parallèle ; reprise globale C05/C08/C17 hors livraison C02. |
| C02-T44 | I,G,Q,R | Primitives Core propriétaires PostgreSQL ; aucune projection annuaire écrivaine sélectionnée. |
| C02-T45 | Q | Lecture PostgreSQL disponible ; branche LDAP/repli O09 conditionnelle non sélectionnée. |
| C02-T46 | G,Q | Filtre source et contexte tenant/scope exacts ; consultation O09 reste à intégrer si sélectionnée. |
| C02-T47 | R | Création liée au plan, confirmations vérifiées par le propriétaire synthétique C08 ; mapping réel non prétendu. |
| C02-T48 | R | Réutilisation sans reset/second compte, CAS obsolète refusé et rejeu autorisé actuellement. |
| C02-T49 | R | Opérateur absent/mal typé/périmé/révoqué/contexte divergent refusé ; C01 distinct. |
| C02-T50 | R | Mode NORMAL rejeté structurellement ; aucun reçu C01 ne remplace les ports R01. |
| C02-T51 | R | Identity/Binding sans User ni MFA anticipé ; vrai credential et authentification propres C03/C08 futurs. |
| C02-T52 | R | Acteur distinct de la cible à créer ; égalité admise pour un compte existant réellement vérifié par port. |
| C02-T53 | R | Premier tenant et grant seulement si effets fermés explicites ; CAS et rejeu protégés. |
| C02-T54 | R | Commit réel suivi d’erreur réconcilié, C08 confirmé/C06 perdu fermé, exclusion et rejeu avant marqueur bornés. |

## Vérifications V01–V12 et activation

V01 U/I ; V02 I/G ; V03 G/Q ; V04 T/Q/R ; V05 G/R ; V06 U ; V07 T/Q/R ; V08 M ; V09 M/T/R ; V10 M avec installation initiale seule ; V11 U/I/G/Q/R ; V12 D et interfaces minimisées. Ces rattachements portent sur la part propriétaire C02 décrite dans design.md.

V10 n’introduit pas d’origine distribuée à migrer ni de contraction. Les migrations déclarent None→0.1.0, refusent les origines/états inconnus et ne font aucun downgrade automatique. La contraction et la coexistence de versions publiées non sélectionnées sont des cas conditionnels non applicables ici, avec cette justification ; cela ne vaut pas recette C16.

Les garanties intégrées C03/C04/C05/C06/C08/C09/C10/C16 restent à qualifier par leurs propriétaires puis dans C17 sur le paquet C18, avec identité de distribution C19. R01 B01–B10 a une contribution C02 persistante prouvée ; le mécanisme réel de mapping opérateur, l’éligibilité de base, les confirmations du vrai installateur, le marqueur externe et FIRST_CONFIGURATION ne sont pas livrés par C02. LDAP/O08/O09 ne sont pas sélectionnés comme provider/projection activés. Ni P0 global ni cycle global complet ne sont annoncés.

Les tâches de réalisation sont cochées seulement sur ces preuves. L’obligation conditionnelle de statistiques après archivage reste suivie séparément jusqu’à présence et vérification du rapport ; aucun jalon documentaire ne vaut arrêt du RUN. Le gate, la publication et la libération sont vérifiés après le rapport. Le suivi de clôture est propre à ce seul change, sans fermeture d’OpenCode partagé.
