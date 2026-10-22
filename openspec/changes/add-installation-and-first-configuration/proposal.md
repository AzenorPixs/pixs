# C08 — Installateur et première configuration

## Pourquoi

Le canon impose un parcours INSTALLER explicite puis FIRST_CONFIGURATION et NORMAL, sans secret distribué ni compte implicite. Le raccord complet n’est pas livré : le résolveur C01 actuel refuse hors INSTALLER et le port Core de gouvernance initiale ne dispose que de producteurs de test dans les recettes consultées.

## Statut et décisions du 22 octobre 2026

Le développeur a validé la reprise documentaire initiale, puis la correction distincte de .openspec.yaml. La métadonnée conserve schema et created et ne déclare plus skip_specs. La validation OpenSpec ciblée stricte a réussi avant adoption, sans constituer une recette produit.

Le développeur a ensuite validé l’intégration exacte des quatre exigences et huit scénarios des deux deltas C08 dans les canons secrets-providers et installation-provisioning, avec alignement des quatre documents C08. Le présent lot ne produit ni code, migration, installation de service, déploiement ou archive. Les tâches de réalisation restent non cochées.

R01 du 19 octobre et D15/D16 du 20 octobre sont conservés : clé Ed25519 personnelle préautorisée, sujet opérateur pré-session explicite, autorisation finale de 600 secondes, consommation liée au commit et effets fermés. Aucune autorité métier n’est transférée de C01 au futur Super Admin.

## Comportements adoptés et réalisation future

- [secrets-providers](../../specs/secrets-providers/spec.md) : résolution technique post-INSTALLER explicitement autorisée par mode/workload et continuité d’audit avant PostgreSQL puis relais C05 idempotent.
- [installation-provisioning](../../specs/installation-provisioning/spec.md) : source protégée de gouvernance initiale et publication externe des références de connexion effectivement vérifiées.

Les deux deltas locaux secrets-providers et installation-provisioning conservent les quatre ajouts déjà adoptés. Le nouveau complément PA/PZT ci-dessous ajoute des propositions distinctes ; il ne vaut pas adoption de ces nouveaux textes. Les validations après intégration sont des contrôles documentaires distincts des recettes d’implémentation futures.

La conception décrit le plan privé et ses confirmations, l’empreinte sans auto-référence, la source de confiance, le marqueur externe, l’état FIRST_CONFIGURATION et le résultat C08 participant à la transaction Core/Auth/audit.

## Dépendances

Les contrats déjà livrés de C01, C02, C03, C04, C05 et C07 restent nécessaires : secrets techniques, Core PostgreSQL, Auth locale, autorisation, audit et composition de référence.

C08 dépend aussi d’une source de gouvernance initiale de confiance satisfaisant GovernanceProvider et le profil canonique data-governance. Ce contrat minimal est à coordonner avec [C10](../enforce-core-data-governance-and-lifecycle/design.md). La présence de son protocole ou d’une fixture n’est pas une réalisation ; C08 n’implémente pas implicitement tout C10.

## Impact

Le lot d’adoption porte sur les deux canons et les quatre documents C08 autorisés. Aucun Kernel, code, modèle, migration, gabarit pur, paramètre d’exploitation, secret ou état Git n’est modifié. Aucun nouveau provider ou writer de secrets n’est sélectionné. Le raccord du provider existant et le fournisseur de gouvernance doivent être réalisés et qualifiés après vérification des dépendances et cadrage des mandats.

## Critères de sortie de la réalisation future

Recette R01 B01–B10, quatre états de base, confirmations fraîches, refus de mots de passe différents, conservation du compte unique, reprise sans doublon et marqueur invalide interdisant NORMAL sans relancer INSTALLER. Ajouter S01–S04 et G01–G03 de requirements.md ; leur adoption ne prouve aucune exécution.

## Conditions de retour au cycle CISMP

Après validation documentaire de l’intégration, reprendre l’inventaire du premier jalon C08 non prouvé. Vérifier la source de gouvernance, la procédure externe de publication des credentials et les paramètres de confiance et de stockage, sans transformer des valeurs de fixtures en paramètres d’exploitation. L’adoption ne constitue ni une livraison C08 ni une disponibilité P0.


## Parcours validé PA/PZT → PostgreSQL → PBO — complément documentaire

Le développeur valide le parcours suivant : le PA système de l’hôte initie la première connexion technique PostgreSQL et prépare le service sur hôte physique ou VM ; dans Docker Pixs, PostgreSQL est fourni dans l’image et PA initialise seulement la configuration et le stockage persistants manquants. Les données existantes sont conservées. PBO reste propriétaire des migrations et de l’initialisation Core/Auth/Super Admin/premier tenant. Tous échanges PBO–PA passent par PZT, y compris sur le même hôte ou conteneur.

Une procédure opérateur locale provisionne la confiance et les seuls droits techniques PA/PZT indépendamment de la base Pixs à préparer. Le profil PZT local mTLS n’autorise que les opérations techniques déclarées ; il ne donne aucun droit métier ni ouverture réseau distante. Le management ordinaire attend l’autorité applicative PostgreSQL. Aux démarrages suivants, la remise du seul secret de connexion au workload PBO vérifié est évaluée sous politique native protégée indépendante d’Auth PostgreSQL ; les autres décisions restent applicatives. R01 Ed25519/600 secondes et C01 INSTALLER restent distincts et inchangés.

Huit deltas sont proposés dans ce même change, sans nouveau change : [administration initiale](specs/initial-administration/spec.md), [provisionnement](specs/installation-provisioning/spec.md), [PA](specs/pixs-agent/spec.md), [PZT](specs/pzt/spec.md), [Docker](specs/docker-image/spec.md), [composition](specs/reference-composition/spec.md), [autorisation](specs/authorization/spec.md) et [secrets](specs/secrets-providers/spec.md). Les modifications de clauses existantes y sont explicites. Les quatre exigences déjà adoptées restent acquises ; les nouveaux ajouts et modifications PA/PZT restent proposés à l’intégration canonique, sans adoption silencieuse.

Le présent complément modifie seulement ces huit deltas, les quatre documents C08 et le commentaire de .openspec.yaml (schema/created conservés). Il ne change aucun canon, cadrage racine, code, migration, service, volume, permission ou état Git et ne réalise aucune recette produit. Les futurs alignements de BUILD §14/§23 (PostgreSQL dans l’image, données hors image), PROJECT et TECHNICAL devront suivre les contrats adoptés. La qualification historique sans exécutants PA/PZT ne prouve pas le profil révisé ; le provider et le mode de livraison des secrets Docker restent à déclarer et qualifier, sans nouveau choix implicite.

Les critères de sortie documentaires sont : cohérence des huit deltas et de leurs clauses canoniques ciblées, maintien des quatre ajouts acquis et de R01/C01, validation OpenSpec stricte, UTF-8/LF, liens valides, tâches de réalisation non cochées et empreintes des canons inchangées. L’adoption précise et la réalisation future restent distinctes de ce jalon.
