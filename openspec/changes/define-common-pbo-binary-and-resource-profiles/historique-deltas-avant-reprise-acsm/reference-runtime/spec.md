## MODIFIED Requirements

### Requirement: Couche exécutable PA séparée

Les trois binaires PA définis par pixs-agent et le binaire indépendant PZT
défini par pzt MUST rester distincts du runtime applicatif. Ils MUST NOT
remplacer Django, PostgreSQL ou TanStack ni devenir un backend métier
alternatif. Les trois binaires PA et PZT MUST suivre Cython,
avec chaînes et plateformes qualifiées avant construction.

#### Scenario: Exécutants distincts du backend

- **WHEN** une release décrit PA et PZT
- **THEN** elle distingue trois binaires PA et un binaire PZT sans autorité métier alternative

### Requirement: Verrouillage exact de Nuitka pendant la campagne PBO

La version exacte sélectionnée MUST être verrouillée dans `toolchain.nuitka` des métadonnées de campagne PBO pendant la campagne et pour la reproduction de ses artefacts. Les déclarations, métadonnées et contrôles de construction MUST vérifier cette version ; une contrainte ouverte MUST NOT remplacer le verrou. Une nouvelle publication MUST NOT modifier automatiquement la campagne ou ses preuves. La seule reproduction MUST NOT imposer une nouvelle sélection de la dernière stable.

#### Scenario: Publication pendant une campagne et reproduction des artefacts

- **WHEN** une nouvelle stable est publiée après le verrouillage d'une campagne ou qu'un artefact de cette campagne doit être reproduit
- **THEN** la version verrouillée est conservée et une version effective différente est refusée par les contrôles de construction, sans actualisation automatique ni nouvelle sélection pour la seule reproduction

#### Scenario: Version effective différente du verrou

- **WHEN** la construction PBO utilise une version Nuitka différente de celle verrouillée pour la campagne
- **THEN** le contrôle de construction refuse cet écart avant qualification, même si cette version est une stable plus récente

## ADDED Requirements

### Requirement: Binaire PBO commun et socle modulaire

PBO MUST être livré comme un binaire applicatif commun regroupant le Kernel, pixs.core, pixs.auth, pixs.agent et pixs.pzt dans une même application modulaire. Les modules MUST conserver contrats publics, données et permissions propres ; leur présence MUST NOT imposer un démon par module. Les profils de processus MUST suivre runtime sans remplacer Django ni embarquer les exécutants PA/PZT.

#### Scenario: Socle partagé par plusieurs rôles

- **WHEN** la même release démarre des processus PBO web et worker
- **THEN** ils utilisent le même binaire et le même graphe de composition, avec une activation de rôle explicite

#### Scenario: Contrats conservés dans un processus

- **WHEN** Auth ou un module de gestion consomme une primitive Core dans le même processus
- **THEN** il utilise son contrat public sans accès aux données privées ni canal IPC imposé entre ces modules

### Requirement: Compilation PBO Nuitka standalone

PBO MUST être compilé avec Nuitka en mode standalone. Les livraisons Debian/Docker MUST contenir l'exécutable PBO commun, ses bibliothèques, runtime et ressources déclarés, sans imposer un fichier autoextractible unique. Le mode onefile MUST NOT remplacer standalone sans évolution approuvée. Les versions, options, imports dynamiques Django et données de package MUST être qualifiés explicitement.

#### Scenario: Distribution autonome complète

- **WHEN** une distribution du binaire PBO est qualifiée
- **THEN** les rôles web, worker et scheduler, imports Django, migrations, catalogues et ressources nécessaires fonctionnent avec les dépendances livrées et la configuration externe déclarée

#### Scenario: Mode onefile substitué

- **WHEN** un build utilise onefile à la place du mode standalone retenu sans évolution approuvée
- **THEN** il ne satisfait pas le profil de construction PBO

### Requirement: Cython ciblé et mesuré dans PBO

Dans PBO, Cython MUST être réservé aux optimisations ciblées dont le profilage identifie le coût et dont des mesures comparables démontrent un gain selon des critères définis avant recette. La qualification MUST vérifier ressources, contrats, sécurité, maintenabilité et non-régression ; Cython MUST NOT remplacer la chaîne Nuitka du PBO complet. Les exécutants indépendants PA/PZT MUST suivre leurs chaînes Cython distinctes.

#### Scenario: Optimisation sans preuve

- **WHEN** un module Cython est proposé dans PBO sans profilage ni comparaison mesurée du périmètre optimisé
- **THEN** il n'est pas admis dans une composition qualifiée sur cette seule proposition

#### Scenario: Gain ciblé qualifié

- **WHEN** une optimisation Cython est évaluée à code fonctionnel, données, environnement, configuration et charge comparables
- **THEN** les mesures mémoire, CPU, latence ou débit pertinents et les contrôles de non-régression justifient son admission sans affaiblir les contrats ou la sécurité

### Requirement: Qualification du binaire PBO

La construction du binaire PBO MUST qualifier versions de Nuitka, Python, dépendances, compilateur C, ABI, plateformes et options du profil standalone avant distribution. Le nom du fichier et les options CLI MUST être documentés explicitement. Un binaire compilé MUST NOT prouver à lui seul une réduction mémoire, un gain de débit ou une exécution Python parallèle sur plusieurs cœurs.

#### Scenario: Compilation sans mesure de performance

- **WHEN** un binaire PBO est construit sans recette de charge ni de ressources
- **THEN** aucun gain de performance ni support multicœur effectif n'est annoncé sur cette seule base

### Requirement: Dernière stable Nuitka au début de chaque campagne PBO

Au début de chaque campagne de qualification PBO, la chaîne MUST sélectionner la dernière version stable de Nuitka publiée et non retirée sur la source officielle PyPI à la date de vérification. Les préversions et versions de développement MUST NOT être sélectionnées comme dernière stable. La sélection MUST être réévaluée à chaque nouvelle campagne.

#### Scenario: Sélection de la dernière stable au début de la campagne

- **WHEN** une nouvelle campagne PBO commence et PyPI publie une version stable plus récente que le verrou précédent, ainsi qu'une préversion encore plus récente
- **THEN** la version stable publiée et non retirée la plus récente est sélectionnée, la préversion est exclue et la vérification datée, la source, la version et les éléments de provenance et d'intégrité sont enregistrés avec le verrou de la campagne

### Requirement: Traçabilité de la chaîne Nuitka PBO

La date de vérification, la source officielle, la version exacte sélectionnée, la provenance et les empreintes des distributions utilisées MUST être enregistrées avec la chaîne de la campagne. Les preuves historiques MUST rester rattachées à leurs versions et artefacts ; elles MUST NOT être attribuées automatiquement à une nouvelle chaîne.

#### Scenario: Conservation des preuves après changement de version

- **WHEN** une campagne utilise une version Nuitka différente d'une campagne antérieure
- **THEN** chaque campagne conserve sa vérification datée, sa source, sa version, sa provenance et ses empreintes, et les anciennes preuves restent liées à leurs versions et artefacts d'origine

### Requirement: Actualisation coordonnée de Nuitka pour PBO

Tout changement de version Nuitka MUST entraîner la mise à jour coordonnée de `pyproject.toml`, des métadonnées de chaîne, des contrôles PBO, des tests concernés et de la documentation courante, puis la qualification de la nouvelle chaîne. La sélection ou l'inscription documentaire d'une version MUST NOT tenir lieu de qualification.

#### Scenario: Actualisation lors de la campagne suivante

- **WHEN** une campagne suivante sélectionne une nouvelle stable Nuitka
- **THEN** les déclarations, métadonnées de chaîne, contrôles PBO, tests concernés et documentation courante sont alignés avant la qualification de la nouvelle chaîne, tandis que les preuves historiques restent liées à leurs anciens artefacts et versions

### Requirement: Préservation des autres choix de chaîne PBO

La sélection d'une version Nuitka MUST NOT modifier implicitement CPython, le mode GIL, le compilateur C, l'ABI, les cibles, les dépendances, les rôles ou les choix Cython adoptés. Le profil Nuitka standalone et les modes d'exploitation Standalone/ZT MUST être conservés. La politique de dernière stable MUST NOT valoir autorisation d'installation.

#### Scenario: Nouvelle version Nuitka avec autres choix conservés

- **WHEN** une nouvelle stable Nuitka est sélectionnée pour PBO
- **THEN** CPython, le GIL, le compilateur C, l'ABI, les cibles, les dépendances, les rôles, les choix Cython, le profil standalone et les modes Standalone/ZT restent conservés, et aucune installation n'est autorisée par la seule sélection

### Requirement: Blocage si la dernière stable Nuitka ne peut pas être qualifiée

Si la dernière stable ne peut pas être vérifiée ou si sa compatibilité ne peut pas être qualifiée, la sélection ou la qualification concernée MUST rester bloquée. Une ancienne version MUST NOT être choisie implicitement pour contourner ce blocage.

#### Scenario: Dernière stable non vérifiable ou incompatible

- **WHEN** la source officielle ne permet pas de vérifier la dernière stable ou que cette version ne peut pas être qualifiée avec la chaîne et les cibles adoptées
- **THEN** la sélection ou la qualification reste bloquée, sans repli implicite vers une ancienne version ni modification implicite des autres choix de chaîne adoptés

### Requirement: Métadonnées fermées et identité de campagne PBO

Le document TOML de campagne PBO MUST avoir les seules racines `schema_version`, `campaign`, `toolchain`, `selection`, `distributions`. Le schéma MUST être `1.0.0` ; campaign MUST contenir seulement un `id` unique non vide et `component=pbo`, toolchain seulement `nuitka`, version stable exacte normalisée. Les tables MUST être fermées ; champs inconnus, absents, dupliqués ou mal typés MUST être refusés. L'identité et les entrées figées MUST être conservées pour reproduire la campagne.

#### Scenario: Métadonnées valides et reproduction

- **WHEN** une campagne fournit les métadonnées fermées valides et qu'une reproduction est ensuite demandée
- **THEN** le même identifiant, le verrou et les preuves figées sont conservés, sans nouvelle sélection de version ni réécriture des métadonnées historiques

#### Scenario: Métadonnées invalides

- **WHEN** un champ est absent, inconnu, dupliqué ou mal typé, ou que le verrou contient une contrainte ouverte, une préversion, une version de développement, locale ou non normalisée
- **THEN** les métadonnées sont refusées avant compilation avec PBO_CAMPAIGN_METADATA_INVALID, sans valeur implicite ni correction automatique

### Requirement: Preuve de sélection Nuitka dans la campagne PBO

La table selection MUST contenir seulement `verified_at` UTC textuel, `source_url` PyPI officiel, `snapshot` relatif au document et `snapshot_sha256`. Le relevé JSON conservé MUST prouver la dernière stable non retirée à cette date ; son empreinte MUST être vérifiée sur ses octets. Un chemin sortant ou symbolique MUST être refusé. Une empreinte seule MUST NOT prouver l'origine officielle. Le constructeur MUST utiliser la sélection vérifiée, sans consulter PyPI ni choisir une version.

#### Scenario: Relevé absent ou preuve non concluante

- **WHEN** la date ou la source est invalide, le relevé est absent, sortant, symbolique ou altéré, ou qu'il ne démontre pas la sélection officielle de la dernière stable non retirée
- **THEN** la sélection ou la construction reste bloquée avec PBO_CAMPAIGN_EVIDENCE_INVALID pour une preuve inexploitable, sans ancien compilateur choisi implicitement ; un schéma invalide conserve PBO_CAMPAIGN_METADATA_INVALID

### Requirement: Distributions Nuitka tracées par campagne PBO

distributions MUST être une liste non vide de tables contenant seulement `filename`, `url`, `sha256`. Les noms simples MUST être uniques, les URL HTTPS sans authentification et les SHA-256 en hexadécimal minuscule sur 64 caractères. Chaque fichier utilisé MUST correspondre au nom, à l'URL et au condensat d'une distribution non retirée de la version verrouillée dans le relevé officiel. Une distribution absente ou altérée MUST être refusée avant compilation.

#### Scenario: Distribution non déclarée ou altérée

- **WHEN** un fichier utilisé ne figure pas dans les métadonnées ou que son nom, son URL, son empreinte réelle ou son état dans le relevé officiel ne correspond pas à la distribution autorisée
- **THEN** le contrôle refuse la construction avec PBO_CAMPAIGN_EVIDENCE_INVALID avant compilation, sans téléchargement ou installation implicite

### Requirement: Rapport de construction lié au verrou Nuitka PBO

Avant compilation, le constructeur MUST comparer strictement la déclaration Nuitka exacte de `pyproject.toml`, `toolchain.nuitka` et une sonde structurée du compilateur réellement appelé. `build-report.json` MUST lier `campaign_id`, `campaign_metadata_sha256`, `profile_sha256` et `nuitka_version` avec `locked` et `observed`, et tracer distributions vérifiées et issue du contrôle. Les empreintes MUST porter sur les entrées réelles indépendantes du rapport, sans auto-condensat.

#### Scenario: Sonde conforme et rapport lié aux entrées

- **WHEN** la déclaration, le verrou et la version observée concordent et que les entrées et distributions ont été vérifiées
- **THEN** le rapport lie l'identifiant, les empreintes des métadonnées et du profil effectifs, les versions verrouillée et observée ainsi que les distributions vérifiées, sans que ce contrôle seul qualifie le binaire

#### Scenario: Sonde inexploitable ou divergence de version

- **WHEN** la sonde est absente, mal typée ou ambiguë, ou qu'une version déclarée ou observée diffère du verrou
- **THEN** le constructeur refuse avant compilation avec PBO_BUILD_NUITKA_METADATA_INVALID pour la sonde ou PBO_BUILD_NUITKA_MISMATCH pour l'écart ; le rapport conserve les valeurs vérifiées et observed vaut null si aucune version exploitable n'est obtenue

### Requirement: Admission indépendante de la sélection officielle Nuitka PBO

La sélection Nuitka PBO MUST provenir d'une observation directe HTTPS vérifiée et datée en UTC, suivie d'une revue explicitement autorisée du dossier figé. L'admission MUST lier le manifeste exact et la campagne dans un registre protégé distinct du candidat, non modifiable par le constructeur ou son appelant. Un booléen, un relevé auto-déclaré ou son empreinte seule MUST NOT établir cette autorité. Le constructeur MUST vérifier l'admission hors ligne.

#### Scenario: Observation et revue du manifeste exact

- **WHEN** une nouvelle campagne dispose d'une observation officielle exploitable, d'une sélection de la dernière stable non retirée, d'entrées figées vérifiées et d'une revue explicitement autorisée
- **THEN** une admission liée à l'identité de campagne et au manifeste exact est conservée dans le registre protégé, sans que cette décision seule autorise installation, compilation ou qualification

#### Scenario: Preuve auto-déclarée ou registre substitué

- **WHEN** le demandeur fournit un booléen de validation, une admission dans son candidat, une identité de responsable non autorisée ou un registre de remplacement
- **THEN** ces éléments ne valent pas admission et le contrôle refuse avant outils avec PBO_CAMPAIGN_EVIDENCE_INVALID, sans repli implicite ni compilation

#### Scenario: Observation officielle impossible ou non concluante

- **WHEN** HTTPS ou la date n'est pas vérifiable, la source est indisponible ou différente, ou que les données ne permettent pas d'établir la dernière stable non retirée
- **THEN** aucune sélection n'est admise, aucune preuve rétroactive n'est inventée et aucune ancienne version n'est choisie implicitement

### Requirement: Conservation et rattachement des preuves de sélection PBO

Le dossier figé MUST conserver entrées, manifeste, autorisation et admission sans réécriture. Le registre MUST préserver retraits et état courant ; une admission absente, retirée ou invérifiable MUST bloquer la construction. Le rapport MUST lier `selection_admission_ref`, `selection_admission_sha256` et `selection_manifest_sha256` aux preuves vérifiées, sans cycle d'empreintes. La reproduction MUST conserver dates et entrées sans nouvelle sélection.

#### Scenario: Altération ou échange après admission

- **WHEN** un fichier ou le manifeste est altéré, ou qu'une admission est présentée pour une autre campagne ou d'autres octets
- **THEN** les empreintes ou l'identité divergent, la construction est refusée avec PBO_CAMPAIGN_EVIDENCE_INVALID et les preuves d'origine restent conservées

#### Scenario: Retrait ou état courant non vérifiable

- **WHEN** l'admission est absente, retirée, inaccessible ou que son état courant est ambigu, y compris après restauration
- **THEN** la construction reste bloquée avec PBO_CAMPAIGN_EVIDENCE_INVALID, sans réactivation depuis une ancienne copie favorable

#### Scenario: Reproduction avec admission et rapport liés

- **WHEN** les entrées et l'admission de la campagne d'origine restent vérifiées et utilisables pour une reproduction
- **THEN** dates et versions d'origine sont conservées, le rapport lie les références et empreintes vérifiées d'admission et de manifeste, et le constructeur ne consulte pas PyPI pour sélectionner une autre version
