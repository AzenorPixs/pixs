# C08 — Installateur et première configuration

## Cible adoptée le 22 octobre 2026

Le parcours PA/PZT → PostgreSQL → PBO et les huit deltas sont intégrés au canon. Six exigences sont ajoutées, six modifiées et vingt-sept scénarios supplémentaires nets (dont quatre de présentation des garanties) sont conservés, sans doubler les quatre exigences déjà adoptées. PROJECT.md, TECHNICAL.md et BUILD.md sont alignés. Cette adoption est documentaire ; aucune réalisation ni qualification produit n’est déduite. Les étapes antérieures ci-dessous conservent leur portée historique.

## Pourquoi

Le canon impose un parcours INSTALLER explicite puis FIRST_CONFIGURATION et NORMAL, sans secret distribué ni compte implicite. Le raccord complet n’est pas livré : le résolveur C01 actuel refuse hors INSTALLER et le port Core de gouvernance initiale ne dispose que de producteurs de test dans les recettes consultées.

## Statut et décisions du 22 octobre 2026

Le développeur a validé la reprise documentaire initiale, puis la correction distincte de .openspec.yaml. La métadonnée conserve schema et created et ne déclare plus skip_specs. La validation OpenSpec ciblée stricte a réussi avant adoption, sans constituer une recette produit.

Le développeur a ensuite validé l’intégration exacte des quatre exigences et huit scénarios des deux deltas C08 dans les canons secrets-providers et installation-provisioning, avec alignement des quatre documents C08. Le présent lot ne produit ni code, migration, installation de service, déploiement ou archive. Les tâches de réalisation restent non cochées.

R01 du 19 octobre et D15/D16 du 20 octobre sont conservés : clé Ed25519 personnelle préautorisée, sujet opérateur pré-session explicite, autorisation finale de 600 secondes, consommation liée au commit et effets fermés. Aucune autorité métier n’est transférée de C01 au futur Super Admin.

## Comportements adoptés et réalisation future

- [secrets-providers](../../specs/secrets-providers/spec.md) : résolution technique post-INSTALLER explicitement autorisée par mode/workload et continuité d’audit avant PostgreSQL puis relais C05 idempotent.
- [installation-provisioning](../../specs/installation-provisioning/spec.md) : source protégée de gouvernance initiale et publication externe des références de connexion effectivement vérifiées.

Les deux deltas locaux secrets-providers et installation-provisioning conservent les quatre ajouts antérieurs. Le complément PA/PZT est désormais adopté dans les huit canons après revue distincte. Les validations après intégration sont des contrôles documentaires distincts des recettes d’implémentation futures.

La conception décrit le plan privé et ses confirmations, l’empreinte sans auto-référence, la source de confiance, le marqueur externe, l’état FIRST_CONFIGURATION et le résultat C08 participant à la transaction Core/Auth/audit.

## Dépendances

Les contrats déjà livrés de C01, C02, C03, C04, C05 et C07 restent nécessaires : secrets techniques, Core PostgreSQL, Auth locale, autorisation, audit et composition de référence.

C08 dépend aussi d’une source de gouvernance initiale de confiance satisfaisant GovernanceProvider et le profil canonique data-governance. Ce contrat minimal est à coordonner avec [C10](../enforce-core-data-governance-and-lifecycle/design.md). La présence de son protocole ou d’une fixture n’est pas une réalisation ; C08 n’implémente pas implicitement tout C10.

## Impact

Le lot d’adoption porte sur les deux canons et les quatre documents C08 autorisés. Aucun Kernel, code, modèle, migration, gabarit pur, paramètre d’exploitation, secret ou état Git n’est modifié. Ce lot historique ne sélectionnait aucun nouveau provider ou writer de secrets. Le raccord du provider existant et le fournisseur de gouvernance doivent être réalisés et qualifiés après vérification des dépendances et cadrage des mandats.

## Critères de sortie de la réalisation future

Recette R01 B01–B10, quatre états de base, confirmations fraîches, refus de mots de passe différents, conservation du compte unique, reprise sans doublon et marqueur invalide interdisant NORMAL sans relancer INSTALLER. Ajouter S01–S04 et G01–G03 de requirements.md ; leur adoption ne prouve aucune exécution.

## Conditions de retour au cycle CISMP

Après validation documentaire de l’intégration, reprendre l’inventaire du premier jalon C08 non prouvé. Vérifier la source de gouvernance, la procédure externe de publication des credentials et les paramètres de confiance et de stockage, sans transformer des valeurs de fixtures en paramètres d’exploitation. L’adoption ne constitue ni une livraison C08 ni une disponibilité P0.


## Parcours PA/PZT → PostgreSQL → PBO — adoption normative

Le parcours adopté est le suivant : le PA système de l’hôte initie la première connexion technique PostgreSQL et prépare le service sur hôte physique ou VM ; dans Docker Pixs, PostgreSQL est fourni dans l’image et PA initialise seulement la configuration et le stockage persistants manquants. Les données existantes sont conservées. PBO reste propriétaire des migrations et de l’initialisation Core/Auth/Super Admin/premier tenant. Tous échanges PBO–PA passent par PZT, y compris sur le même hôte ou conteneur.

Une procédure opérateur locale provisionne la confiance et les seuls droits techniques PA/PZT indépendamment de la base Pixs à préparer. Le profil PZT local mTLS n’autorise que les opérations techniques déclarées ; il ne donne aucun droit métier ni ouverture réseau distante. Le management ordinaire attend l’autorité applicative PostgreSQL. Aux démarrages suivants, la remise du seul secret de connexion au workload PBO vérifié est évaluée sous politique native protégée indépendante d’Auth PostgreSQL ; les autres décisions restent applicatives. R01 Ed25519/600 secondes et C01 INSTALLER restent distincts et inchangés.

Huit deltas sont adoptés dans ce même change, sans nouveau change : [administration initiale](specs/initial-administration/spec.md), [provisionnement](specs/installation-provisioning/spec.md), [PA](specs/pixs-agent/spec.md), [PZT](specs/pzt/spec.md), [Docker](specs/docker-image/spec.md), [composition](specs/reference-composition/spec.md), [autorisation](specs/authorization/spec.md) et [secrets](specs/secrets-providers/spec.md). Les modifications de clauses existantes y sont explicites. Les quatre exigences précédemment adoptées restent acquises ; les six ajouts et six modifications PA/PZT sont intégrés aux canons après revue.

L’adoption modifie les huit canons et les quatre documents C08, avec alignement de PROJECT, TECHNICAL et BUILD §§14/23 : logiciel PostgreSQL fourni dans l’image, données persistantes hors des couches. Les deltas restent des traces de cette adoption et ne doivent pas être appliqués une seconde fois. La métadonnée conserve schema et created ; son commentaire est aligné sur l’adoption. Le code, les migrations, services, volumes, permissions et Git ne sont pas modifiés. La qualification historique sans exécutants PA/PZT ne prouve pas le profil révisé ; le provider et le mode de livraison des secrets Docker devaient encore être déclarés et qualifiés à cette étape historique, sans nouveau choix implicite.

Les critères de sortie documentaires sont : concordance des huit deltas avec les clauses adoptées, maintien des quatre ajouts acquis et de R01/C01, validation OpenSpec stricte, UTF-8/LF, liens valides, tâches de réalisation non cochées et préservation des autres exigences et des archives. Les empreintes après adoption et les résultats observés sont consignés dans le bilan GSCM ; la réalisation reste future.

## Adoption documentaire D1–D3 du 23 octobre 2026

Le développeur a validé les trois choix du [design, profils 1.5](design.md) et leur lot documentaire de dix fichiers : Debian 13 x86_64 physique/VM et Docker Linux amd64 ; base candidate Docker Official Image postgres:16.15-trixie à verrouiller par digest avant construction ; init Docker et Supervisor 4.2.5-3, nouvelle dépendance de l’image seulement ; fournisseur Docker distinct de C01, par fichiers versionnés montés en lecture seule, avec preuve native du workload, politique courante, arrêt attesté des consommateurs, révocation et audit à réaliser et qualifier.

Les deux exigences et cinq scénarios supplémentaires sont adoptés dans les deltas et canons [docker-image](../../specs/docker-image/spec.md) et [secrets-providers](../../specs/secrets-providers/spec.md). Leur traçabilité figure dans [requirements.md](requirements.md). Les compteurs précédents décrivent les lots historiques ; ces ajouts ne constituent aucune recette exécutée. BUILD reçoit un seul paragraphe de renvoi. La tâche 2.5 couvre désormais les fournisseurs réels systemd et Docker ; aucune case de réalisation n’est anticipée.

L’accord autorise cette adoption documentaire uniquement : aucun code, migration, installation, téléchargement ou construction d’image, Git, changement de service, volume, permissions ou infrastructure. Les paramètres d’exploitation, identités, politiques, budgets, dépendances et artefacts restent à fournir et qualifier avant les réalisations dépendantes. C01 Debian, les gabarits purs, R01 Ed25519/600 secondes, les propriétaires PA/PZT/PBO/Core/Auth/C05 et le raccord minimal C10 validé en 1.4 restent inchangés.

## Première installation totalement autonome — décision du 23 octobre 2026

Le développeur exige : « L’installation première doit être totalement autonome ». Le premier **hôte** ne doit nécessiter ni instance Pixs, ni PostgreSQL Pixs, ni autorité privée PZT déjà opérationnels, ni paquet d’identités ou certificats PZT préémis ailleurs. Une procédure opérateur locale contrôlée doit permettre d’établir la confiance initiale avant PostgreSQL, sans premier PBO auto-approuvé.

Le [design — décision Q1.6-PKI](design.md) conserve les responsabilités : échanges PBO–PA via PZT, préparation PostgreSQL par PA, migrations et initialisation applicative par PBO, rapprochement des preuves puis transfert au contrôle courant. L’exigence couvre physique/VM et le profil Docker sélectionné, avec conservation des données existantes. La création initiale de confiance et son articulation avec la PKI ordinaire restent à préciser avant réalisation.

Seuls proposal/design/requirements C08 sont alignés sur cette décision. Elle ne valide pas implicitement E1/E2/E3, un nouveau provider TLS, une dépendance ou une exception PKI. Les décisions C01/R01, profils 1.5 et propriétaires restent acquis. Aucun canon, delta, tâche cochée, code, certificat, clé, service, installation ou infrastructure n’est produit par cette étape.

## État courant de réalisation — 23 octobre 2026

Le développeur autorise la continuation de C08 jusqu'à sa clôture, réalisations puis phase de tests et validation. Les lots documentaires antérieurs restent historiques et n'annoncent pas une livraison. Les sous-lots privés `installation/marker.py` et `installation/plan.py`, avec leurs deux fichiers unittest, sont écrits sous CAB mais non testés ; 2.1 demeure incomplète, sans stockage protégé du plan/checkpoint ni lecteur propriétaire PostgreSQL.

Les décisions sont désormais acquises : autonomie initiale ; contrat initial Z12 documentaire 1.0.0 §12 publié sous référence 69 ; catalogue PA01 PostgreSQL version 1.0.0 publié sous référence 70 ; choix E3 explicitement validé, adaptateur Cython libssl/libcrypto OpenSSL 3 pour PZT local TLS 1.3/mTLS. C08 reste consommateur de Z12 et du catalogue PA, sans second émetteur PKI. Les API/runtime initiaux, schémas de raccord, plans techniques et exécutants manquants restent à réaliser et qualifier ; un texte publié ne vaut pas API disponible. E3 ne vaut ni installation sur l'hôte actuel ni sélection implicite de versions, ABI, providers, ports ou budgets.

Aucune nouvelle tâche n'est cochée et aucun résultat de test produit n'est anticipé. C01, R01 Ed25519/600 secondes, profils 1.5 et raccord minimal C10 sont conservés. Documentation publique et historique des évolutions seront alignés sur le comportement réellement qualifié avant clôture ; Git et infrastructure restent soumis aux autorisations distinctes.

## Point de reprise du 23 octobre 2026 — adoption documentaire E4

E3 reste adopté. Le développeur a explicitement répondu « Valider le lot E4
proposé » : usage supplémentaire de la clé personnelle Ed25519 préautorisée
pour le mandat technique PA distinct de R01, liaison au plan PostgreSQL et à
sa confirmation, registre durable PA avec ancrage TPM NV dédié distinct Z12.
Les principes et limites sont au [design, section E4](design.md).

L'adoption couvre les trois documents C08 ; aucun canon ni runtime n'est
modifié par ce lot. Schémas conditionnels exacts, résolveurs, protection NV,
machine durable et preuves restent à produire par leurs propriétaires.
Aucune installation ni opération TPM/NV sur l'hôte actuel n'est autorisée.

Les sources privées de plan/marqueur/stockage/contenu d'acte, la source et
l'adaptateur minimal C10 avec migration 0014, puis le modèle de résultat C08
avec migration 0015 et import Django sont écrits, non testés. Aucune migration
SQL ni recette intégrée n'a été exécutée. Écrivain/lecteur de résultat, checkpoint,
modes, CLI et raccords restent à compléter. Les tâches après 1.5 sont ouvertes.
La réalisation précède la phase de tests/validation conformément à la demande ;
le change n'est pas archivé.

## Retrait de la préparation initiale PA — principes adoptés

Le retrait supprime irréversiblement la nouvelle préparation initiale PA, sans supprimer la remise technique minimale canonique de connexion au workload PBO et sans inventer une autorité ordinaire déjà admise. L'action concernée est withdraw_initial_authority, de classe Critique, dans le domaine PA_POSTGRESQL_WITHDRAWAL, sous la permission WITHDRAW_PA_INITIAL.

Le mandat de retrait est un mandat signé nouveau, distinct des mandats R01 et E4. Il est signé par la clé privée personnelle Ed25519 de l'opérateur, conservée hors runtime et hors agents. La clé d'administration PA et les clés de la PKI et du TLS Z12 ne sont jamais réutilisées implicitement pour cet acte.

C08 confirme ce retrait avec les contrats courants C03 et C04 et un mapping explicitement vérifié vers le signataire. Aucun booléen verified fourni par l'appelant et aucun SuperAdmin auto-attribué ne vaut confirmation.

PA vérifie la signature, la clé et la politique courantes, la révocation, la validité et la fraîcheur UTC, les identités natives et la relation PZT, la cible, le plan et le contexte, la consommation anti-rejeu, la quiescence et l'ancrage durable irréversible. Un DTO à l'état RETIRED, un résultat PG_SUCCEEDED, un mode NORMAL ou D6 seul ne prouvent pas le retrait PA.

L'inspection administrative Protégé reste possible sous autorisation courante de son propriétaire. Elle est distincte de get_postgresql_result et ne rouvre ni extension, ni préparation, ni retrait rejoué.

Les contrats de topologie D8/D6, de wire et de résolveurs restent à fermer en revue commune avant leur code, les qualifications réelles en phase 2 après réalisation, sans élargir les accords par ce texte. Le retrait suppose les prérequis applicatifs, les migrations, R01, Core, Auth et les audits rapprochés, sans exiger que l'autorité ordinaire PA soit déjà active pour retirer l'autorité initiale. Les propriétaires PA et Z12 et leurs deux retraits restent distincts. Aucun ordre nouveau n'est adopté ici. L'adoption des principes ne vaut pas réalisation.

E5 est adopté documentairement et reste non réalisé ni qualifié. La séquence est OBSERVE protégé, observation PA reçue et vérifiée, projection C08 immuable liée à cette observation, PREPARE_PLAN avec retour du bundle vérifié, présentation et confirmation C08 seize champs, nouvelle PREPARE critique signée engageant toute l'enveloppe 1.1, puis READ_RESULT distincte. Les enveloppes 1.1, les cinq ressources SOFTWARE, CLUSTER, SERVICE, ROLE, DATABASE, UNOBSERVABLE jamais absence, les préconditions stagiées avant chaque CREATE, effects_binding manifeste entier distinct de effects_digest tableau, et les tableaux A07 complets ordre et doublons de leurs invocations réelles restent définis par PA01. Docker, INITIALIZE_START, RECREATE et DATABASE_DROP restent refusés avant tout effet sans conversion silencieuse. Aucun code, producteur, transport, test ou infrastructure n'est livré ici.
