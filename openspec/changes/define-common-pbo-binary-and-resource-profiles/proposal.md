# Binaire PBO commun et profils de processus selon les ressources

## Pourquoi

La décision du 21 octobre 2026 retient une même application PBO regroupant
Kernel, Core, Auth, Agent et module PZT, distribuée par un binaire commun.
Les profils web, worker et scheduler existent au canon ; leur dimensionnement
et celui des exécutants PA/PZT doivent être explicitement liés aux ressources
réellement accordées à chaque environnement.

La décision du développeur du 26 octobre 2026 complète ce cadrage : sélectionner
la dernière version stable publiée de Nuitka au début de chaque campagne de
qualification PBO, puis verrouiller sa version exacte pendant cette campagne
et pour reproduire ses artefacts, selon la même politique que Cython dans PA01.

Le complément validé ensuite le 26 octobre 2026 définit les métadonnées TOML
de campagne PBO et leur verrou `toolchain.nuitka`, la preuve de sélection,
les distributions tracées et le contrôle de version avant compilation.

## Ce qui change

- Définir le binaire PBO commun Nuitka standalone et préserver les contrats des modules.
- Sélectionner la dernière stable Nuitka publiée et non retirée sur PyPI à chaque nouvelle campagne PBO ; tracer et verrouiller la version exacte, coordonner son actualisation et qualifier la chaîne, sans repli implicite en cas de blocage.
- Définir le schéma fermé de campagne PBO, `toolchain.nuitka`, les preuves de sélection et de distribution, ainsi que le rapport et les refus du contrôle de version.
- Distinguer compilation standalone et exploitation Standalone ou ZT du même binaire.
- Réserver Cython dans PBO aux optimisations ciblées justifiées par profilage, mesures de gain et non-régression ; retenir Cython pour les trois binaires PA et le binaire PZT indépendant.
- Configurer rôles, processus, concurrence et budgets PBO selon l'environnement.
- Conserver les trois binaires/six modes PA et le binaire indépendant PZT,
  avec leurs propres plans de processus et ressources locales ou distantes.
- Distinguer ressources détectées, budget accordé, configuration demandée,
  configuration effective et état appliqué ; encadrer toute adaptation.
- Préserver sécurité, reprise, sessions, baux scheduler et propriétaire réseau
  unique PZT par périmètre, sous supervision déclarée.
- Harmoniser cadrages, README, schémas et distributions Debian/Docker.

## Capacités

### Capacités modifiées

- reference-runtime : binaire PBO commun, qualification de sa construction, politique Nuitka par campagne et métadonnées/verrou associés.
- runtime : rôles, dimensionnement, supervision et qualification des ressources.
- pixs-agent : compilation Cython, processus par rôle/session et coordination des opérations PA.
- pzt : processus configurables avec propriétaire réseau unique et garanties.
- deb-package : livraison du binaire PBO et configuration externe des profils.
- docker-image : même binaire, quotas effectifs et réplication contrôlée.
- reference-composition : preuve du binaire et du plan de ressources du P0.

Aucune nouvelle capacité. Les deltas de la décision du 21 octobre 2026 sont
adoptés et synchronisés au canon ; ils ne doivent pas être comptés ou rejoués
comme des ajouts encore proposés. Le complément Nuitka par campagne du
26 octobre 2026 ajoute six exigences dans le delta reference-runtime ; il est
adopté et synchronisé au canon sur validation explicite du développeur le
26 octobre 2026. Cette synchronisation ne réapplique aucun delta antérieur.
Le complément de métadonnées précise l'exigence de verrouillage déjà
synchronisée et ajoute quatre exigences et six scénarios au delta ; cette
nouvelle précision et ces ajouts sont synchronisés au canon sur validation
explicite du développeur le 26 octobre 2026, sans réapplication des autres
deltas ni réalisation du constructeur.

Le complément du 27 octobre 2026 définit une [preuve officielle datée Nuitka](PREUVE_SELECTION_PBO.md)
équivalente à PA01 : collecte contrôlée, dossier figé, revue autorisée,
admission dans un registre protégé distinct du candidat et vérification hors
ligne. Deux exigences et six scénarios sont ajoutés au delta reference-runtime,
sans synchronisation du canon, code, implémentation ni preuve réelle produite.

## Impact

La réalisation produit, les builds, l'installation, les mesures de performance,
le déploiement et la publication restent à engager sous mandat distinct.
Nuitka en mode standalone est retenu pour PBO ; versions/options, schémas/CLI,
nombres de processus et seuils restent à qualifier. La dernière stable Nuitka
est réévaluée au début de chaque campagne, puis sa version exacte est figée ;
une version invérifiable ou incompatible bloque la sélection ou la qualification
sans retour implicite à une ancienne version ni modification des autres choix
de chaîne. La sélection documentaire ne qualifie pas la chaîne. Aucun outil ni
dépendance n'est installé. Les trois binaires PA et le binaire PZT utilisent Cython.
Le profil P0 conserve ses autres exigences ; aucune qualification n'est déduite
de cette adoption. Aucun archivage n'est effectué.
