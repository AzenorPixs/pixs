# Références normatives — PA01

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| pixs-agent | Processus PA configurables par rôle et session | 2 | pixs-agent-c606e03ee3c7 |
| pixs-agent | Trois binaires PA et six modes distincts de PZT | 1 | pixs-agent-5cd5cae10cd4 |
| pixs-agent | Compilation différenciée validée | 1 | pixs-agent-49d91499d8f8 |
| pixs-agent | Composition au build et catalogue fermé | 1 | pixs-agent-0ed896227fd4 |
| pixs-agent | Paramètres ouverts et absence d'implémentation implicite | 1 | pixs-agent-2fe8f8e831ff |
| pixs-agent | Dernière stable Cython au début de chaque campagne PA01 | 1 | pixs-agent-d4d5a6f7b9a7 |
| pixs-agent | Traçabilité de la chaîne Cython PA01 | 1 | pixs-agent-f866e48a0626 |
| pixs-agent | Verrouillage exact de Cython pendant la campagne PA01 | 1 | pixs-agent-942f9dcf7533 |
| pixs-agent | Actualisation coordonnée de Cython pour PA01 | 1 | pixs-agent-816f0ea9f1cd |
| pixs-agent | Préservation des autres choix de chaîne PA01 | 1 | pixs-agent-fad0558df391 |
| pixs-agent | Blocage si la dernière stable Cython ne peut pas être qualifiée | 1 | pixs-agent-13da3c4b328e |
| pzt | Module essentiel pixs.pzt et exécutable PZT indépendant | 1 | pzt-1063497b290f |
| pzt | Frontières et identités PA PZT explicites | 1 | pzt-0f4a5ba6eba9 |
| reference-runtime | Binaire PBO commun et socle modulaire | 2 | reference-runtime-d579870947ef |
| reference-runtime | Compilation PBO Nuitka standalone | 2 | reference-runtime-442fdc059971 |
| reference-runtime | Cython ciblé et mesuré dans PBO | 2 | reference-runtime-82a60f9e0cf2 |
| reference-runtime | Qualification du binaire PBO | 1 | reference-runtime-be879237fe75 |
| reference-runtime | Pile de référence unique | 2 | reference-runtime-988d3d50a615 |
| reference-runtime | Adapter explicite | 1 | reference-runtime-e21374a24d6f |
| reference-runtime | Absence de sélection cachée | 1 | reference-runtime-2b29bdc3cedc |
| reference-runtime | Version stable actuelle de Django | 1 | reference-runtime-e16d452ba50d |
| reference-runtime | Adaptation complète à la stable Django ciblée | 1 | reference-runtime-8daabca40e5f |
| reference-runtime | Relevé et qualification de la stable courante | 1 | reference-runtime-a858c8bca3ef |
| reference-runtime | Qualification reproductible et politique sans dérogation | 1 | reference-runtime-0b5bbe475406 |
| reference-runtime | Dépendances Python les plus récentes compatibles avec Django | 1 | reference-runtime-6b95b469b3f3 |
| reference-runtime | Versions exactes, plages et bornes minimales Django | 1 | reference-runtime-daa5593d2feb |
| reference-runtime | Qualification du graphe Python et incompatibilités explicites | 1 | reference-runtime-297362616fd0 |
| reference-runtime | Absence d'installation forcée ou de recul Django | 1 | reference-runtime-8b90d25bd99a |
| reference-runtime | Compatibilité avec le Python actuel du projet | 3 | reference-runtime-3dd91a63a9e2 |
| reference-runtime | Couche exécutable PA séparée | 1 | reference-runtime-409ab89f825b |
| reference-runtime | Modules de gestion pixs.agent et pixs.pzt dans PBO | 2 | reference-runtime-9646ae50ea78 |
| reference-runtime | Dernière stable Nuitka au début de chaque campagne PBO | 1 | reference-runtime-dd1c633ba395 |
| reference-runtime | Traçabilité de la chaîne Nuitka PBO | 1 | reference-runtime-6a0ee4bd4bfd |
| reference-runtime | Verrouillage exact de Nuitka pendant la campagne PBO | 2 | reference-runtime-1e6135365491 |
| reference-runtime | Actualisation coordonnée de Nuitka pour PBO | 1 | reference-runtime-e066b66b3fff |
| reference-runtime | Préservation des autres choix de chaîne PBO | 1 | reference-runtime-b9bcba27e82b |
| reference-runtime | Blocage si la dernière stable Nuitka ne peut pas être qualifiée | 1 | reference-runtime-207ac2c394d0 |
| reference-runtime | Métadonnées fermées et identité de campagne PBO | 2 | reference-runtime-35f06de2e0c9 |
| reference-runtime | Preuve de sélection Nuitka dans la campagne PBO | 1 | reference-runtime-ae55e5d2fd56 |
| reference-runtime | Distributions Nuitka tracées par campagne PBO | 1 | reference-runtime-3fe2b116dd44 |
| reference-runtime | Rapport de construction lié au verrou Nuitka PBO | 2 | reference-runtime-6ebe3e0fcd96 |

### Référence courante pixs-agent-c606e03ee3c7

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 41. SHA-256 : `c606e03ee3c7151f6a5c10e84afad50ba736b4315f1879897dad1865334815ea`.

Scénarios : Deux sessions utilisateur; Profil Docker dimensionné.

~~~~text
### Requirement: Processus PA configurables par rôle et session

Les trois binaires et six modes PA MUST conserver leur répartition et permettre un plan de processus et de concurrence selon runtime et les ressources de leur environnement. Le plan MUST distinguer démons permanents, événements bornés et sessions réelles. Il MUST NOT transformer un événement en démon, activer un mode exclu du profil ou partager les privilèges entre système et utilisateur.

#### Scenario: Deux sessions utilisateur

- **WHEN** deux sessions réelles utilisent le binaire utilisateur PA
- **THEN** leurs processus, droits, ressources et arrêts restent isolés dans le budget global déclaré

#### Scenario: Profil Docker dimensionné

- **WHEN** un plan de ressources PA est appliqué dans Docker
- **THEN** seuls les modes système et événements du conteneur admissibles sont sélectionnés, sans mode de session
~~~~

### Référence courante pixs-agent-5cd5cae10cd4

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 64. SHA-256 : `5cd5cae10cd478a8ffb30c4e15180dfdc341506019583f78882f62ec99106408`.

Scénarios : Répartition PA et PZT.

~~~~text
### Requirement: Trois binaires PA et six modes distincts de PZT

PA MUST comporter exactement trois binaires : démon système pour system-daemon ;
événements système pour system-start et system-stop ; sessions utilisateur pour
session-start, session-stop et session-daemon. PZT et son mode pzt-daemon MUST
rester un composant exécutable indépendant, colivré selon deb-package et
docker-image. Le démon de session MUST NOT créer un binaire supplémentaire.
Les chemins et options CLI restent à spécifier.

#### Scenario: Répartition PA et PZT

- **WHEN** la composition complète PA/PZT est décrite
- **THEN** elle distingue trois binaires et six modes PA du binaire indépendant PZT et de son mode pzt-daemon
~~~~

### Référence courante pixs-agent-49d91499d8f8

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 78. SHA-256 : `49d91499d8f83f1c794a0c59612a178648ad502a5b43f2965eba5f1f79a072e6`.

Scénarios : Compilation des composants distincts.

~~~~text
### Requirement: Compilation différenciée validée

Les trois binaires PA MUST être compilés avec Cython ; le binaire indépendant
PZT MUST suivre Cython selon pzt. Les chaînes MUST partir de Python via C avec
runtime, dépendances et ABI déclarés et qualifiés avant construction. Cette
décision MUST NOT installer un outil ni prouver un gain de performance.

#### Scenario: Compilation des composants distincts

- **WHEN** la matrice de compilation PA/PZT est déclarée
- **THEN** les trois binaires PA et PZT indépendant utilisent Cython avec leurs chaînes et qualifications propres
~~~~

### Référence courante pixs-agent-0ed896227fd4

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 108. SHA-256 : `0ed896227fd4520562a556c15ca86d634e059dc29313794ff743d8324201c20b`.

Scénarios : Composition au build et catalogue fermé.

~~~~text
### Requirement: Composition au build et catalogue fermé

Chaque capacité PA MUST déclarer identité, version, propriétaire, contrats, dépendances, configuration, sécurité et permissions selon le modèle de composants. La composition initiale MUST se faire au build ; instructions et mandats MUST sélectionner seulement des opérations déjà livrées. PA MUST NOT télécharger ou charger implicitement du code, évaluer du Python ou ouvrir un shell privilégié à partir d'une instruction réseau.

#### Scenario: Composition au build et catalogue fermé

- **WHEN** une instruction demande une opération absente du catalogue livré
- **THEN** elle est refusée sans téléchargement ou exécution de code arbitraire
~~~~

### Référence courante pixs-agent-2fe8f8e831ff

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 296. SHA-256 : `2fe8f8e831ff5c8809f75a824394b629f715e43baab2b850615835c04c39ba78`.

Scénarios : Paramètres ouverts et absence d'implémentation implicite.

~~~~text
### Requirement: Paramètres ouverts et absence d'implémentation implicite

Les identifiants pixs.agent, pixs.pzt et le nom du composant/binaire PZT MUST
être considérés validés. Noms/versions de paquets, noms de fichiers exécutables,
chemins, CLI, bibliothèques, comptes, formats et valeurs non arrêtés MUST rester
ouverts jusqu'à décision ou qualification. Les versions de Cython MUST
être qualifiées avant installation. Cette rédaction MUST NOT valoir code,
recette runtime, support de plateforme ou artefact livré.

#### Scenario: Paramètres ouverts et absence d'implémentation implicite

- **WHEN** seules les spécifications sont déclarées
- **THEN** les états d'implémentation, qualification et publication restent explicitement non réalisés
~~~~

### Référence courante pixs-agent-d4d5a6f7b9a7

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 467. SHA-256 : `d4d5a6f7b9a721b15560211b17a0ea1ebdd2a56945aab0ce77bcbefbb6d174d1`.

Scénarios : Sélection de la dernière stable au début de la campagne.

~~~~text
### Requirement: Dernière stable Cython au début de chaque campagne PA01

Au début de chaque campagne de qualification PA01, la chaîne MUST sélectionner la dernière version stable de Cython publiée et non retirée sur la source officielle PyPI à la date de vérification. Les préversions et versions de développement MUST NOT être sélectionnées comme dernière stable. La sélection MUST être réévaluée à chaque nouvelle campagne.

#### Scenario: Sélection de la dernière stable au début de la campagne

- **WHEN** une nouvelle campagne PA01 commence et PyPI publie une version stable plus récente que le verrou précédent, ainsi qu'une préversion encore plus récente
- **THEN** la version stable publiée et non retirée la plus récente est sélectionnée, la préversion est exclue et la vérification datée, la source, la version et les éléments de provenance et d'intégrité sont enregistrés avec le verrou de la campagne
~~~~

### Référence courante pixs-agent-f866e48a0626

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 476. SHA-256 : `f866e48a06266cdd1a8f1112713b8e84b3f69b1b3e340a9b7ebc5b803688c0be`.

Scénarios : Conservation des preuves après changement de version.

~~~~text
### Requirement: Traçabilité de la chaîne Cython PA01

La date de vérification, la source officielle, la version exacte sélectionnée, la provenance et les empreintes des distributions utilisées MUST être enregistrées avec la chaîne de la campagne. Les preuves historiques MUST rester rattachées à leurs versions et artefacts ; elles MUST NOT être attribuées automatiquement à une nouvelle chaîne.

#### Scenario: Conservation des preuves après changement de version

- **WHEN** une campagne utilise une version Cython différente d'une campagne antérieure
- **THEN** chaque campagne conserve sa vérification datée, sa source, sa version, sa provenance et ses empreintes, et les anciennes preuves restent liées à leurs versions et artefacts d'origine
~~~~

### Référence courante pixs-agent-942f9dcf7533

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 485. SHA-256 : `942f9dcf75334ddaecd396b0b03888f93dfc6bb94c6687ce5f6ec534aac84077`.

Scénarios : Publication pendant une campagne et reproduction des artefacts.

~~~~text
### Requirement: Verrouillage exact de Cython pendant la campagne PA01

La version exacte sélectionnée MUST être verrouillée dans `toolchain.cython` du profil PA01 pendant la campagne et pour la reproduction de ses artefacts. Les déclarations, métadonnées et contrôles de construction MUST vérifier cette version ; une contrainte ouverte MUST NOT remplacer le verrou. Une nouvelle publication MUST NOT modifier automatiquement la campagne ou ses preuves. La seule reproduction MUST NOT imposer une nouvelle sélection de la dernière stable.

#### Scenario: Publication pendant une campagne et reproduction des artefacts

- **WHEN** une nouvelle stable est publiée après le verrouillage d'une campagne ou qu'un artefact de cette campagne doit être reproduit
- **THEN** la version verrouillée est conservée et une version effective différente est refusée par les contrôles de construction, sans actualisation automatique ni nouvelle sélection pour la seule reproduction
~~~~

### Référence courante pixs-agent-816f0ea9f1cd

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 494. SHA-256 : `816f0ea9f1cdfef3a7d4f9fbe0fd9efebbd39eaa53ac8a39549bc2666b49bc5b`.

Scénarios : Actualisation lors de la campagne suivante.

~~~~text
### Requirement: Actualisation coordonnée de Cython pour PA01

Tout changement de version Cython MUST entraîner la mise à jour coordonnée de `pyproject.toml`, des métadonnées de chaîne, des contrôles PA01, des tests concernés et de la documentation courante, puis la qualification de la nouvelle chaîne. La sélection ou l'inscription documentaire d'une version MUST NOT tenir lieu de qualification.

#### Scenario: Actualisation lors de la campagne suivante

- **WHEN** une campagne suivante sélectionne une nouvelle stable Cython
- **THEN** les déclarations, métadonnées de chaîne, contrôles PA01, tests concernés et documentation courante sont alignés avant la qualification de la nouvelle chaîne, tandis que les preuves historiques restent liées à leurs anciens artefacts et versions
~~~~

### Référence courante pixs-agent-fad0558df391

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 503. SHA-256 : `fad0558df39127bb0415ca588767475bee05083b452ccfe030063ff8b4763271`.

Scénarios : Nouvelle version Cython avec autres choix conservés.

~~~~text
### Requirement: Préservation des autres choix de chaîne PA01

La sélection d'une version Cython MUST NOT modifier implicitement CPython, le mode GIL, l'ABI, les cibles ou les autres choix adoptés. La politique de dernière stable MUST NOT valoir autorisation d'installation.

#### Scenario: Nouvelle version Cython avec autres choix conservés

- **WHEN** une nouvelle stable Cython est sélectionnée pour PA01
- **THEN** CPython, le GIL, l'ABI, les cibles et les autres choix adoptés restent conservés, et aucune installation n'est autorisée par la seule sélection
~~~~

### Référence courante pixs-agent-13da3c4b328e

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 512. SHA-256 : `13da3c4b328e02595debab951d5cc05e55a4eb88952ac21a9570be1323e02745`.

Scénarios : Dernière stable non vérifiable ou incompatible.

~~~~text
### Requirement: Blocage si la dernière stable Cython ne peut pas être qualifiée

Si la dernière stable ne peut pas être vérifiée ou si sa compatibilité ne peut pas être qualifiée, la sélection ou la qualification concernée MUST rester bloquée. Une ancienne version MUST NOT être choisie implicitement pour contourner ce blocage.

#### Scenario: Dernière stable non vérifiable ou incompatible

- **WHEN** la source officielle ne permet pas de vérifier la dernière stable ou que cette version ne peut pas être qualifiée avec la chaîne et les cibles adoptées
- **THEN** la sélection ou la qualification reste bloquée, sans repli implicite vers une ancienne version ni modification implicite de CPython, du GIL, de l'ABI ou des cibles
~~~~

### Référence courante pzt-1063497b290f

Source : [pzt](../../specs/pzt/spec.md), ligne 77. SHA-256 : `1063497b290fd7bb8e8abad2dad81ac19bb67f139b4c911c98be000279df7b7c`.

Scénarios : Réseau désactivé et gestion conservée.

~~~~text
### Requirement: Module essentiel pixs.pzt et exécutable PZT indépendant

Toute composition cible PBO MUST inclure le module officiel essentiel pixs.pzt,
au-dessus du Kernel et de pixs.core, par les mécanismes génériques. pixs.pzt
MUST configurer, administrer, visualiser, superviser et monitorer PZT. Le réseau
activé/configuré MUST être exécuté par le binaire indépendant PZT, compilé avec
Cython. Désactiver le réseau MUST NOT retirer pixs.pzt de PBO.

#### Scenario: Réseau désactivé et gestion conservée

- **WHEN** PZT est désactivé dans un PBO
- **THEN** le binaire réseau se ferme mais pixs.pzt demeure composé avec ses fonctions de gestion
~~~~

### Référence courante pzt-0f4a5ba6eba9

Source : [pzt](../../specs/pzt/spec.md), ligne 270. SHA-256 : `0f4a5ba6eba942fd067ab81877191eb5886e0811f8f2bf48fbd6a02aaa59d610`.

Scénarios : Colivraison sans admission du composant réseau.

~~~~text
### Requirement: Frontières et identités PA PZT explicites

Les profils MUST déclarer les interfaces PA–PZT, appelants, cibles, droits,
isolation et liaisons d'identités et de preuves requises. PA et PZT MUST garder
leurs identités, clés et états distincts. Une colivraison ou une attestation PA
MUST NOT admettre automatiquement PZT, transférer un secret, un privilège ou
supprimer une preuve d'identité, d'hôte ou d'intégrité exigée.

#### Scenario: Colivraison sans admission du composant réseau

- **WHEN** PA et PZT sont installés ensemble mais une preuve requise pour PZT n'est pas vérifiable
- **THEN** le périmètre dépendant est bloqué sans identité partagée ni transfert implicite de droit
~~~~

### Référence courante reference-runtime-d579870947ef

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 12. SHA-256 : `d579870947eff610f89c305f4fe26bc0ff079a1cd45b690104af1f7031d4f233`.

Scénarios : Socle partagé par plusieurs rôles; Contrats conservés dans un processus.

~~~~text
### Requirement: Binaire PBO commun et socle modulaire

PBO MUST être livré comme un binaire applicatif commun regroupant le Kernel, pixs.core, pixs.auth, pixs.agent et pixs.pzt dans une même application modulaire. Les modules MUST conserver contrats publics, données et permissions propres ; leur présence MUST NOT imposer un démon par module. Les profils de processus MUST suivre runtime sans remplacer Django ni embarquer les exécutants PA/PZT.

#### Scenario: Socle partagé par plusieurs rôles

- **WHEN** la même release démarre des processus PBO web et worker
- **THEN** ils utilisent le même binaire et le même graphe de composition, avec une activation de rôle explicite

#### Scenario: Contrats conservés dans un processus

- **WHEN** Auth ou un module de gestion consomme une primitive Core dans le même processus
- **THEN** il utilise son contrat public sans accès aux données privées ni canal IPC imposé entre ces modules
~~~~

### Référence courante reference-runtime-442fdc059971

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 26. SHA-256 : `442fdc0599710868608ebf7425c3412a97fe42afb65fe94fbf794176853ddb7b`.

Scénarios : Distribution autonome complète; Mode onefile substitué.

~~~~text
### Requirement: Compilation PBO Nuitka standalone

PBO MUST être compilé avec Nuitka en mode standalone. Les livraisons Debian/Docker MUST contenir l'exécutable PBO commun, ses bibliothèques, runtime et ressources déclarés, sans imposer un fichier autoextractible unique. Le mode onefile MUST NOT remplacer standalone sans évolution approuvée. Les versions, options, imports dynamiques Django et données de package MUST être qualifiés explicitement.

#### Scenario: Distribution autonome complète

- **WHEN** une distribution du binaire PBO est qualifiée
- **THEN** les rôles web, worker et scheduler, imports Django, migrations, catalogues et ressources nécessaires fonctionnent avec les dépendances livrées et la configuration externe déclarée

#### Scenario: Mode onefile substitué

- **WHEN** un build utilise onefile à la place du mode standalone retenu sans évolution approuvée
- **THEN** il ne satisfait pas le profil de construction PBO
~~~~

### Référence courante reference-runtime-82a60f9e0cf2

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 40. SHA-256 : `82a60f9e0cf268e6575b96a70eb408b159290052eae81067122b86604a96969f`.

Scénarios : Optimisation sans preuve; Gain ciblé qualifié.

~~~~text
### Requirement: Cython ciblé et mesuré dans PBO

Dans PBO, Cython MUST être réservé aux optimisations ciblées dont le profilage identifie le coût et dont des mesures comparables démontrent un gain selon des critères définis avant recette. La qualification MUST vérifier ressources, contrats, sécurité, maintenabilité et non-régression ; Cython MUST NOT remplacer la chaîne Nuitka du PBO complet. Les exécutants indépendants PA/PZT MUST suivre leurs chaînes Cython distinctes.

#### Scenario: Optimisation sans preuve

- **WHEN** un module Cython est proposé dans PBO sans profilage ni comparaison mesurée du périmètre optimisé
- **THEN** il n'est pas admis dans une composition qualifiée sur cette seule proposition

#### Scenario: Gain ciblé qualifié

- **WHEN** une optimisation Cython est évaluée à code fonctionnel, données, environnement, configuration et charge comparables
- **THEN** les mesures mémoire, CPU, latence ou débit pertinents et les contrôles de non-régression justifient son admission sans affaiblir les contrats ou la sécurité
~~~~

### Référence courante reference-runtime-be879237fe75

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 54. SHA-256 : `be879237fe75304b7b62bfafdda63b0928a55cac3f6a28ec1b7d0d320a890cd9`.

Scénarios : Compilation sans mesure de performance.

~~~~text
### Requirement: Qualification du binaire PBO

La construction du binaire PBO MUST qualifier versions de Nuitka, Python, dépendances, compilateur C, ABI, plateformes et options du profil standalone avant distribution. Le nom du fichier et les options CLI MUST être documentés explicitement. Un binaire compilé MUST NOT prouver à lui seul une réduction mémoire, un gain de débit ou une exécution Python parallèle sur plusieurs cœurs.

#### Scenario: Compilation sans mesure de performance

- **WHEN** un binaire PBO est construit sans recette de charge ni de ressources
- **THEN** aucun gain de performance ni support multicœur effectif n'est annoncé sur cette seule base
~~~~

### Référence courante reference-runtime-988d3d50a615

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 63. SHA-256 : `988d3d50a6155de75a88388388e2fbc199a8afde4b78817a6f34633251fab73e`.

Scénarios : Runtime décrit; Réseau désactivé.

~~~~text
### Requirement: Pile de référence unique

Le runtime applicatif PBO/PFO MUST utiliser Django pour l’autorité métier, PostgreSQL comme source de vérité et TanStack comme frontend de référence. L’agnosticisme MUST concerner domaines, contrats, providers et intégrations et MUST NOT promettre l’interchangeabilité immédiate de cette pile. PA, PZT, pixs.agent et pixs.pzt MUST respecter leurs exigences distinctes.

#### Scenario: Runtime décrit

- **WHEN** une release décrit PBO/PFO et les binaires PA
- **THEN** elle identifie Django/PostgreSQL/TanStack pour PBO/PFO et les fonctions locales PA séparément

#### Scenario: Réseau désactivé

- **WHEN** une composition PBO désactive l’exécution réseau PZT
- **THEN** le module essentiel de configuration et de supervision reste composé
~~~~

### Référence courante reference-runtime-e21374a24d6f

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 77. SHA-256 : `e21374a24d6fa7447e275548900870a699c6994b922295ffdc1e765b53610a73`.

Scénarios : Runtime alternatif non déclaré.

~~~~text
### Requirement: Adapter explicite

Un adapter de runtime futur MAY être proposé comme composant distinct. Il MUST
déclarer contrats, compatibilités, limites et preuves de conformité et MUST NOT
modifier implicitement les garanties du runtime de référence.

#### Scenario: Runtime alternatif non déclaré

- **WHEN** un artefact remplace un élément de la pile sans adapter validé
- **THEN** il ne peut pas être déclaré compatible avec le profil de référence
~~~~

### Référence courante reference-runtime-2b29bdc3cedc

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 88. SHA-256 : `2b29bdc3cedcce27c01ab8a9bb8fe76321aea7456fe12c8fcf190d1fab396084`.

Scénarios : Paquet alternatif présent.

~~~~text
### Requirement: Absence de sélection cachée

Le build et le runtime MUST NOT sélectionner une pile alternative selon
l'environnement, l'ordre des imports ou la présence d'un paquet.

#### Scenario: Paquet alternatif présent

- **WHEN** un paquet d'un autre backend est présent dans l'artefact
- **THEN** il ne change pas le runtime effectif sans sélection explicite
~~~~

### Référence courante reference-runtime-e16d452ba50d

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 98. SHA-256 : `e16d452ba50d1a7f65d3db3136851114b1bff08c27a76406ece43d086f1c30dd`.

Scénarios : Nouvelle version stable officielle.

~~~~text
### Requirement: Version stable actuelle de Django

Pixs MUST cibler en permanence la dernière version stable officielle encore
supportée par le projet Django, avec ses correctifs et ses évolutions mineures
ou majeures. Une préversion ou une branche de développement MUST NOT constituer
cette cible ; une ancienne série LTS MUST NOT remplacer la stable courante.

#### Scenario: Nouvelle version stable officielle

- **WHEN** Django publie une nouvelle version stable supportée
- **THEN** Pixs doit actualiser sa cible et adapter le code, le runtime et toutes les dépendances concernés
- **AND** toute incompatibilité restante doit être déclarée comme un travail de migration et ne justifie pas une cible ancienne implicite
~~~~

### Référence courante reference-runtime-8daabca40e5f

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 111. SHA-256 : `8daabca40e5f23ae464c14f2b321ab9ee722f9af26d560bab810179e81d09ff6`.

Scénarios : Migration encore non qualifiée.

~~~~text
### Requirement: Adaptation complète à la stable Django ciblée

Le projet MUST adapter l'intégralité de son code, ses migrations, ses tests,
son runtime Python, ses dépendances directes et transitives et ses déclarations
de compatibilité aux besoins de cette version.

#### Scenario: Migration encore non qualifiée

- **WHEN** les dépendances déclarées ou les validations portent encore sur une version antérieure
- **THEN** le projet doit rendre cet écart explicite et ne peut pas déclarer une conformité à la stable courante sans les preuves de qualification applicables
~~~~

### Référence courante reference-runtime-a858c8bca3ef

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 122. SHA-256 : `a858c8bca3effefea73674d6f4dc3e911a1255a920aebd67438d598c3adce6a2`.

Scénarios : Relevé horodaté.

~~~~text
### Requirement: Relevé et qualification de la stable courante

Pixs MUST vérifier la cible dans les sources officielles Django à chaque
nouvelle stable et avant la qualification d'une nouvelle release. `TECHNICAL.md` MUST rapporter la version stable supportée observée, l'horodatage
de vérification avec son fuseau et les liens officiels. Le relevé MUST
distinguer cible vérifiée, versions déclarées et migration effectivement
qualifiée.

#### Scenario: Relevé horodaté

- **WHEN** la stable officielle est vérifiée
- **THEN** TECHNICAL.md enregistre la version, l'instant de consultation avec fuseau et les sources officielles sans présenter cette consultation comme une installation ou une qualification
~~~~

### Référence courante reference-runtime-0b5bbe475406

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 135. SHA-256 : `0b5bbe475406f48b7975c79a428401397e75402769c959c16b5849a6dce6f520`.

Scénarios : Build reproductible et nouvelle qualification.

~~~~text
### Requirement: Qualification reproductible et politique sans dérogation

La qualification MUST fixer les versions exactes pour préserver la
reproductibilité et MUST vérifier le graphe de dépendances, les tests et les
migrations applicables ; elle MUST NOT procéder par mise à niveau silencieuse. La politique des dépendances Python MUST s'appliquer à toutes les dépendances
sans exception, psycopg compris. Un pin historique MUST NOT constituer une
dérogation à la priorité des contraintes Django et à la cohérence du graphe.

#### Scenario: Build reproductible et nouvelle qualification

- **WHEN** une nouvelle release est qualifiée sur la stable courante
- **THEN** ses versions sont fixées exactement et sa compatibilité complète est validée, tout écart restant empêchant la déclaration de conformité
- **AND** les versions figées des artefacts historiques restent reconstructibles sans constituer une dérogation à la cible de la nouvelle release
~~~~

### Référence courante reference-runtime-6b95b469b3f3

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 149. SHA-256 : `6b95b469b3f38808ab9a4578b656e0e82199ca4c5d67e2576b183fa41995574c`.

Scénarios : Version imposée par Django.

~~~~text
### Requirement: Dépendances Python les plus récentes compatibles avec Django

Les dépendances Python nécessaires au projet, directes et transitives, MUST
utiliser leur dernière version disponible compatible avec la stable Django
ciblée et avec l'ensemble du graphe installé dans l'environnement du projet. Une version exacte ou une plage supportée indiquée par Django MUST prévaloir
sur la dernière version disponible du paquet.

#### Scenario: Version imposée par Django

- **WHEN** la dernière version disponible d'une dépendance ne respecte pas la version exacte ou la plage supportée imposée par Django
- **THEN** la contrainte Django prévaut et la dernière version admissible est retenue sous réserve de la cohérence du graphe complet
~~~~

### Référence courante reference-runtime-daa5593d2feb

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 161. SHA-256 : `daa5593d2febea5e63523776a6f6b8ee28272454a505fa7ecf247cc09102ab57`.

Scénarios : Plage et borne minimale.

~~~~text
### Requirement: Versions exactes, plages et bornes minimales Django

Une version exacte imposée MUST
être respectée ; une plage MUST conduire à la version admissible la plus récente,
sans traiter une borne minimale comme un verrouillage exact.

#### Scenario: Plage et borne minimale

- **WHEN** Django indique une plage supportée contenant plusieurs versions disponibles
- **THEN** la version compatible la plus récente est retenue et une simple borne minimale ne devient pas une version exacte imposée
~~~~

### Référence courante reference-runtime-297362616fd0

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 172. SHA-256 : `297362616fd0baceaf5064ceee717d4210addf8979bedf73e43acc6d7bce6100`.

Scénarios : Graphe incompatible ou contrainte absente.

~~~~text
### Requirement: Qualification du graphe Python et incompatibilités explicites

En l'absence de
contrainte Django explicite, la compatibilité MUST être qualifiée par les
métadonnées et les tests applicables. La qualification MUST conserver les
sources et versions retenues et MUST vérifier ensemble les dépendances directes
et transitives. Toute incompatibilité restante MUST être explicite et conduire
à l'adaptation du code ou de l'environnement.

#### Scenario: Graphe incompatible ou contrainte absente

- **WHEN** une dépendance n'a pas de contrainte Django explicite ou que le graphe complet présente une incompatibilité
- **THEN** les métadonnées et tests applicables doivent qualifier la compatibilité, tout conflit restant empêchant une déclaration de conformité sans forcer l'installation ni rétrograder la cible Django
~~~~

### Référence courante reference-runtime-8b90d25bd99a

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 186. SHA-256 : `8b90d25bd99a691ff079bb841b5c85eba15d60449cf33caa72dc810c41cb3c1d`.

Scénarios : Version de dépendance refusée par Django.

~~~~text
### Requirement: Absence d'installation forcée ou de recul Django

Le projet MUST NOT installer de
force une version refusée par Django ni revenir à un ancien Django pour adopter
une dépendance plus récente.

#### Scenario: Version de dépendance refusée par Django

- **WHEN** une version candidate exige de forcer une dépendance refusée ou de revenir à un ancien Django
- **THEN** le projet ne l'installe pas de force et ne recule pas sa cible Django pour adopter cette dépendance
~~~~

### Référence courante reference-runtime-3dd91a63a9e2

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 197. SHA-256 : `3dd91a63a9e2c157d09b75a4eb21d333d3a46821fe4b762ca08142be28eade67`.

Scénarios : Version compatible; Incompatibilité avec Python actuel; Solution validée par le développeur.

~~~~text
### Requirement: Compatibilité avec le Python actuel du projet

Toute évolution de dépendance Python MUST être supportée par le Python actuel
du projet déclaré dans `DEVOPS.md`. Une incompatibilité MUST suspendre
l'évolution jusqu'à validation ou refus explicite du développeur. Les agents
MUST NOT valider cette exception, changer Python ou masquer le conflit.
La solution retenue MUST être qualifiée avant installation.

#### Scenario: Version compatible

- **WHEN** une évolution de dépendance est proposée
- **THEN** ses contraintes Requires-Python, ses wheels et ses tests doivent confirmer son support du Python actuel, en complément des contraintes Django et du graphe complet

#### Scenario: Incompatibilité avec Python actuel

- **WHEN** la version candidate n'est pas supportée par le Python actuel du projet
- **THEN** l'évolution reste suspendue et seul le développeur peut la valider ou la refuser, y compris tout changement de version Python nécessaire
- **AND** les agents ne forcent pas l'installation et ne modifient pas implicitement la cible pour masquer l'incompatibilité

#### Scenario: Solution validée par le développeur

- **WHEN** le développeur valide une solution après une incompatibilité
- **THEN** la solution choisie doit être qualifiée techniquement avant installation, la validation humaine ne constituant pas en soi une preuve de compatibilité
~~~~

### Référence courante reference-runtime-409ab89f825b

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 221. SHA-256 : `409ab89f825b092bd0b952bce1b1e35b9f4b326cd4c20d55d333a5a993bb892f`.

Scénarios : Exécutants distincts du backend.

~~~~text
### Requirement: Couche exécutable PA séparée

Les trois binaires PA définis par pixs-agent et le binaire indépendant PZT
défini par pzt MUST rester distincts du runtime applicatif. Ils MUST NOT
remplacer Django, PostgreSQL ou TanStack ni devenir un backend métier
alternatif. Les trois binaires PA et PZT MUST suivre Cython,
avec chaînes et plateformes qualifiées avant construction.

#### Scenario: Exécutants distincts du backend

- **WHEN** une release décrit PA et PZT
- **THEN** elle distingue trois binaires PA et un binaire PZT sans autorité métier alternative
~~~~

### Référence courante reference-runtime-9646ae50ea78

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 234. SHA-256 : `9646ae50ea78bd07d9396061cef533def22517a248e283633fcc14763dddaf7e`.

Scénarios : Composition des deux modules de gestion; Réseau désactivé.

~~~~text
### Requirement: Modules de gestion pixs.agent et pixs.pzt dans PBO

La composition cible PBO MUST inclure pixs.agent pour la gestion PA hors PZT
selon pixs-agent et le module essentiel pixs.pzt selon pzt, même réseau
désactivé. Les deux modules MUST utiliser les mécanismes communs et les
primitives pixs.core par contrats publics. La gestion PZT MUST rester dans
pixs.pzt et son exécution dans le binaire indépendant PZT.

#### Scenario: Composition des deux modules de gestion

- **WHEN** la composition PBO est décrite
- **THEN** pixs.agent et pixs.pzt ont des responsabilités et contrats distincts au-dessus du Kernel et de pixs.core

#### Scenario: Réseau désactivé

- **WHEN** l’opérateur désactive le réseau PZT
- **THEN** le binaire réseau se ferme et pixs.pzt demeure dans PBO
~~~~

### Référence courante reference-runtime-dd1c633ba395

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 252. SHA-256 : `dd1c633ba3954ac7f6d2909e5a2f9be6420b934ad7b7c9a3ef991c0876ecc20f`.

Scénarios : Sélection de la dernière stable au début de la campagne.

~~~~text
### Requirement: Dernière stable Nuitka au début de chaque campagne PBO

Au début de chaque campagne de qualification PBO, la chaîne MUST sélectionner la dernière version stable de Nuitka publiée et non retirée sur la source officielle PyPI à la date de vérification. Les préversions et versions de développement MUST NOT être sélectionnées comme dernière stable. La sélection MUST être réévaluée à chaque nouvelle campagne.

#### Scenario: Sélection de la dernière stable au début de la campagne

- **WHEN** une nouvelle campagne PBO commence et PyPI publie une version stable plus récente que le verrou précédent, ainsi qu'une préversion encore plus récente
- **THEN** la version stable publiée et non retirée la plus récente est sélectionnée, la préversion est exclue et la vérification datée, la source, la version et les éléments de provenance et d'intégrité sont enregistrés avec le verrou de la campagne
~~~~

### Référence courante reference-runtime-6a0ee4bd4bfd

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 261. SHA-256 : `6a0ee4bd4bfdf45bf38f9614a31a9a0c7243a768273eae433d13b3d536cc7a9b`.

Scénarios : Conservation des preuves après changement de version.

~~~~text
### Requirement: Traçabilité de la chaîne Nuitka PBO

La date de vérification, la source officielle, la version exacte sélectionnée, la provenance et les empreintes des distributions utilisées MUST être enregistrées avec la chaîne de la campagne. Les preuves historiques MUST rester rattachées à leurs versions et artefacts ; elles MUST NOT être attribuées automatiquement à une nouvelle chaîne.

#### Scenario: Conservation des preuves après changement de version

- **WHEN** une campagne utilise une version Nuitka différente d'une campagne antérieure
- **THEN** chaque campagne conserve sa vérification datée, sa source, sa version, sa provenance et ses empreintes, et les anciennes preuves restent liées à leurs versions et artefacts d'origine
~~~~

### Référence courante reference-runtime-1e6135365491

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 270. SHA-256 : `1e6135365491fa55bb95b1bf0193030b838a707fd624343db1f9e1831d0aeded`.

Scénarios : Publication pendant une campagne et reproduction des artefacts; Version effective différente du verrou.

~~~~text
### Requirement: Verrouillage exact de Nuitka pendant la campagne PBO

La version exacte sélectionnée MUST être verrouillée dans `toolchain.nuitka` des métadonnées de campagne PBO pendant la campagne et pour la reproduction de ses artefacts. Les déclarations, métadonnées et contrôles de construction MUST vérifier cette version ; une contrainte ouverte MUST NOT remplacer le verrou. Une nouvelle publication MUST NOT modifier automatiquement la campagne ou ses preuves. La seule reproduction MUST NOT imposer une nouvelle sélection de la dernière stable.

#### Scenario: Publication pendant une campagne et reproduction des artefacts

- **WHEN** une nouvelle stable est publiée après le verrouillage d'une campagne ou qu'un artefact de cette campagne doit être reproduit
- **THEN** la version verrouillée est conservée et une version effective différente est refusée par les contrôles de construction, sans actualisation automatique ni nouvelle sélection pour la seule reproduction

#### Scenario: Version effective différente du verrou

- **WHEN** la construction PBO utilise une version Nuitka différente de celle verrouillée pour la campagne
- **THEN** le contrôle de construction refuse cet écart avant qualification, même si cette version est une stable plus récente
~~~~

### Référence courante reference-runtime-e066b66b3fff

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 284. SHA-256 : `e066b66b3fff9a39104c825dc6e673c88383b5726556e6a2163a57857216a3d7`.

Scénarios : Actualisation lors de la campagne suivante.

~~~~text
### Requirement: Actualisation coordonnée de Nuitka pour PBO

Tout changement de version Nuitka MUST entraîner la mise à jour coordonnée de `pyproject.toml`, des métadonnées de chaîne, des contrôles PBO, des tests concernés et de la documentation courante, puis la qualification de la nouvelle chaîne. La sélection ou l'inscription documentaire d'une version MUST NOT tenir lieu de qualification.

#### Scenario: Actualisation lors de la campagne suivante

- **WHEN** une campagne suivante sélectionne une nouvelle stable Nuitka
- **THEN** les déclarations, métadonnées de chaîne, contrôles PBO, tests concernés et documentation courante sont alignés avant la qualification de la nouvelle chaîne, tandis que les preuves historiques restent liées à leurs anciens artefacts et versions
~~~~

### Référence courante reference-runtime-b9bcba27e82b

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 293. SHA-256 : `b9bcba27e82bba7e2d125910e0c8be3902266874bb9dea60262b1461e8c60b0e`.

Scénarios : Nouvelle version Nuitka avec autres choix conservés.

~~~~text
### Requirement: Préservation des autres choix de chaîne PBO

La sélection d'une version Nuitka MUST NOT modifier implicitement CPython, le mode GIL, le compilateur C, l'ABI, les cibles, les dépendances, les rôles ou les choix Cython adoptés. Le profil Nuitka standalone et les modes d'exploitation Standalone/ZT MUST être conservés. La politique de dernière stable MUST NOT valoir autorisation d'installation.

#### Scenario: Nouvelle version Nuitka avec autres choix conservés

- **WHEN** une nouvelle stable Nuitka est sélectionnée pour PBO
- **THEN** CPython, le GIL, le compilateur C, l'ABI, les cibles, les dépendances, les rôles, les choix Cython, le profil standalone et les modes Standalone/ZT restent conservés, et aucune installation n'est autorisée par la seule sélection
~~~~

### Référence courante reference-runtime-207ac2c394d0

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 302. SHA-256 : `207ac2c394d020210ae91601ff617976dbd4b63413db24e73321623ac86f109c`.

Scénarios : Dernière stable non vérifiable ou incompatible.

~~~~text
### Requirement: Blocage si la dernière stable Nuitka ne peut pas être qualifiée

Si la dernière stable ne peut pas être vérifiée ou si sa compatibilité ne peut pas être qualifiée, la sélection ou la qualification concernée MUST rester bloquée. Une ancienne version MUST NOT être choisie implicitement pour contourner ce blocage.

#### Scenario: Dernière stable non vérifiable ou incompatible

- **WHEN** la source officielle ne permet pas de vérifier la dernière stable ou que cette version ne peut pas être qualifiée avec la chaîne et les cibles adoptées
- **THEN** la sélection ou la qualification reste bloquée, sans repli implicite vers une ancienne version ni modification implicite des autres choix de chaîne adoptés
~~~~

### Référence courante reference-runtime-35f06de2e0c9

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 311. SHA-256 : `35f06de2e0c913d3b5506072f1063b6b8356324bdf1114a5a834534108c138d9`.

Scénarios : Métadonnées valides et reproduction; Métadonnées invalides.

~~~~text
### Requirement: Métadonnées fermées et identité de campagne PBO

Le document TOML de campagne PBO MUST avoir les seules racines `schema_version`, `campaign`, `toolchain`, `selection`, `distributions`. Le schéma MUST être `1.0.0` ; campaign MUST contenir seulement un `id` unique non vide et `component=pbo`, toolchain seulement `nuitka`, version stable exacte normalisée. Les tables MUST être fermées ; champs inconnus, absents, dupliqués ou mal typés MUST être refusés. L'identité et les entrées figées MUST être conservées pour reproduire la campagne.

#### Scenario: Métadonnées valides et reproduction

- **WHEN** une campagne fournit les métadonnées fermées valides et qu'une reproduction est ensuite demandée
- **THEN** le même identifiant, le verrou et les preuves figées sont conservés, sans nouvelle sélection de version ni réécriture des métadonnées historiques

#### Scenario: Métadonnées invalides

- **WHEN** un champ est absent, inconnu, dupliqué ou mal typé, ou que le verrou contient une contrainte ouverte, une préversion, une version de développement, locale ou non normalisée
- **THEN** les métadonnées sont refusées avant compilation avec PBO_CAMPAIGN_METADATA_INVALID, sans valeur implicite ni correction automatique
~~~~

### Référence courante reference-runtime-ae55e5d2fd56

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 325. SHA-256 : `ae55e5d2fd56b74fc594d02f5a686f3497a8b826110001dd0494a81ab50dc7e5`.

Scénarios : Relevé absent ou preuve non concluante.

~~~~text
### Requirement: Preuve de sélection Nuitka dans la campagne PBO

La table selection MUST contenir seulement `verified_at` UTC textuel, `source_url` PyPI officiel, `snapshot` relatif au document et `snapshot_sha256`. Le relevé JSON conservé MUST prouver la dernière stable non retirée à cette date ; son empreinte MUST être vérifiée sur ses octets. Un chemin sortant ou symbolique MUST être refusé. Une empreinte seule MUST NOT prouver l'origine officielle. Le constructeur MUST utiliser la sélection vérifiée, sans consulter PyPI ni choisir une version.

#### Scenario: Relevé absent ou preuve non concluante

- **WHEN** la date ou la source est invalide, le relevé est absent, sortant, symbolique ou altéré, ou qu'il ne démontre pas la sélection officielle de la dernière stable non retirée
- **THEN** la sélection ou la construction reste bloquée avec PBO_CAMPAIGN_EVIDENCE_INVALID pour une preuve inexploitable, sans ancien compilateur choisi implicitement ; un schéma invalide conserve PBO_CAMPAIGN_METADATA_INVALID
~~~~

### Référence courante reference-runtime-3fe2b116dd44

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 334. SHA-256 : `3fe2b116dd4434a6ca9d1c80a6d9c5575b42597158506aaabef90f06bbdcdd76`.

Scénarios : Distribution non déclarée ou altérée.

~~~~text
### Requirement: Distributions Nuitka tracées par campagne PBO

distributions MUST être une liste non vide de tables contenant seulement `filename`, `url`, `sha256`. Les noms simples MUST être uniques, les URL HTTPS sans authentification et les SHA-256 en hexadécimal minuscule sur 64 caractères. Chaque fichier utilisé MUST correspondre au nom, à l'URL et au condensat d'une distribution non retirée de la version verrouillée dans le relevé officiel. Une distribution absente ou altérée MUST être refusée avant compilation.

#### Scenario: Distribution non déclarée ou altérée

- **WHEN** un fichier utilisé ne figure pas dans les métadonnées ou que son nom, son URL, son empreinte réelle ou son état dans le relevé officiel ne correspond pas à la distribution autorisée
- **THEN** le contrôle refuse la construction avec PBO_CAMPAIGN_EVIDENCE_INVALID avant compilation, sans téléchargement ou installation implicite
~~~~

### Référence courante reference-runtime-6ebe3e0fcd96

Source : [reference-runtime](../../specs/reference-runtime/spec.md), ligne 343. SHA-256 : `6ebe3e0fcd9635da8e25a7ed7da7a616b1a7a1c40fbf011b05e6a481ce3a8d6f`.

Scénarios : Sonde conforme et rapport lié aux entrées; Sonde inexploitable ou divergence de version.

~~~~text
### Requirement: Rapport de construction lié au verrou Nuitka PBO

Avant compilation, le constructeur MUST comparer strictement la déclaration Nuitka exacte de `pyproject.toml`, `toolchain.nuitka` et une sonde structurée du compilateur réellement appelé. `build-report.json` MUST lier `campaign_id`, `campaign_metadata_sha256`, `profile_sha256` et `nuitka_version` avec `locked` et `observed`, et tracer distributions vérifiées et issue du contrôle. Les empreintes MUST porter sur les entrées réelles indépendantes du rapport, sans auto-condensat.

#### Scenario: Sonde conforme et rapport lié aux entrées

- **WHEN** la déclaration, le verrou et la version observée concordent et que les entrées et distributions ont été vérifiées
- **THEN** le rapport lie l'identifiant, les empreintes des métadonnées et du profil effectifs, les versions verrouillée et observée ainsi que les distributions vérifiées, sans que ce contrôle seul qualifie le binaire

#### Scenario: Sonde inexploitable ou divergence de version

- **WHEN** la sonde est absente, mal typée ou ambiguë, ou qu'une version déclarée ou observée diffère du verrou
- **THEN** le constructeur refuse avant compilation avec PBO_BUILD_NUITKA_METADATA_INVALID pour la sonde ou PBO_BUILD_NUITKA_MISMATCH pour l'écart ; le rapport conserve les valeurs vérifiées et observed vaut null si aucune version exploitable n'est obtenue
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

> Instantané historique des exigences reproduites lors de la préparation. La décision du 21 octobre 2026 retient désormais Cython pour les trois binaires PA et pour PZT indépendant ; les mentions Nuitka dans les blocs et empreintes ci-dessous conservent leur valeur de trace historique et ne sont plus le choix de compilation PA. Le canon et les deltas du change [binaire PBO et profils](../define-common-pbo-binary-and-resource-profiles/design.md) font référence avant réalisation. Aucune empreinte ni preuve de qualification antérieure n'est régénérée ici.

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 11 | [Quatre binaires et sept modes explicitement répartis](../../specs/pixs-agent/spec.md#L11) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 20 | [Compilation différenciée validée](../../specs/pixs-agent/spec.md#L20) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 47 | [Composition au build et catalogue fermé](../../specs/pixs-agent/spec.md#L47) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 218 | [Paramètres ouverts et absence d'implémentation implicite](../../specs/pixs-agent/spec.md#L218) | ND | CANDIDAT_PROFIL_PA |
| pzt / 21 | [Module essentiel PBO et binaire PZT dédié](../../specs/pzt/spec.md#L21) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| reference-runtime / 168 | [Couche exécutable PA séparée](../../specs/reference-runtime/spec.md#L168) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--24f2ceb983

Source : `openspec/specs/pixs-agent/spec.md`, ligne 11. SHA-256 du bloc : `7d77582c9257ea14c361d203416f60c56bc861c3552acc98a217d029ad22e615`.

~~~~text
### Requirement: Quatre binaires et sept modes explicitement répartis

PA MUST comporter exactement quatre binaires dédiés : démon système pour system-daemon ; événements système pour system-start et system-stop ; sessions utilisateur pour session-start, session-stop et session-daemon ; exécution PZT pour pzt-daemon. Les noms d'exécutables, chemins et options CLI restent à spécifier. Le découpage MUST NOT créer un cinquième binaire pour le démon de session.

#### Scenario: Quatre binaires et sept modes explicitement répartis

- **WHEN** une distribution PA complète décrit ses exécutables
- **THEN** elle identifie les quatre responsabilités et les sept modes sans les confondre
~~~~

### Référence pixs-agent--5711267e47

Source : `openspec/specs/pixs-agent/spec.md`, ligne 20. SHA-256 du bloc : `9132f06dab01d6d49af23b44e279820ce119057bed453909df089ea538f12990`.

~~~~text
### Requirement: Compilation différenciée validée

Les binaires démon système, événements système et sessions utilisateur MUST être compilés avec Nuitka ; le binaire PZT MUST être compilé avec Cython. La chaîne MUST partir des sources Python, générer du C puis des exécutables natifs avec runtime et dépendances déclarés. Versions exactes et compatibilité MUST être qualifiées avant construction ; cette décision MUST NOT installer une dépendance ni prouver un gain de performance.

#### Scenario: Compilation différenciée validée

- **WHEN** la matrice de compilation est déclarée
- **THEN** les trois premiers binaires utilisent Nuitka et celui de PZT utilise Cython
~~~~

### Référence pixs-agent--bd3940f601

Source : `openspec/specs/pixs-agent/spec.md`, ligne 47. SHA-256 du bloc : `2cde976931df9e6c3f72460dd263b37705129586eb38a9efc3be6b7269446983`.

~~~~text
### Requirement: Composition au build et catalogue fermé

Chaque capacité PA MUST déclarer identité, version, propriétaire, contrats, dépendances, configuration, sécurité et permissions selon le modèle de composants. La composition initiale MUST se faire au build ; instructions et mandats MUST sélectionner seulement des opérations déjà livrées. PA MUST NOT télécharger ou charger implicitement du code, évaluer du Python ou ouvrir un shell privilégié à partir d'une instruction réseau.

#### Scenario: Composition au build et catalogue fermé

- **WHEN** une instruction demande une opération absente du catalogue livré
- **THEN** elle est refusée sans téléchargement ou exécution de code arbitraire
~~~~

### Référence pixs-agent--3d7a2be5b3

Source : `openspec/specs/pixs-agent/spec.md`, ligne 218. SHA-256 du bloc : `2f7e9ceaff587eaeb6b5bc4691e3df6dd5cf2b52f849c4932d465059d8e0433e`.

~~~~text
### Requirement: Paramètres ouverts et absence d'implémentation implicite

Les noms/versions de paquets et exécutables, bibliothèques, formats non arrêtés, topologies, comptes, quotas manquants et seuils à mesurer MUST rester explicitement ouverts jusqu'à décision ou qualification appropriée. Les versions de Nuitka/Cython et leur graphe MUST être qualifiés avant installation. La rédaction de ces spécifications MUST NOT être présentée comme du code, un test runtime, une plateforme supportée ou un artefact livré.

#### Scenario: Paramètres ouverts et absence d'implémentation implicite

- **WHEN** seules les spécifications sont déclarées
- **THEN** les états d'implémentation, qualification et publication restent explicitement non réalisés
~~~~

### Référence pzt--73016f3d2e

Source : `openspec/specs/pzt/spec.md`, ligne 21. SHA-256 du bloc : `050ae5dc06f898c93bf7624d680e4352ef1525bffe2dbb46b7c66870d5c021d5`.

~~~~text
### Requirement: Module essentiel PBO et binaire PZT dédié

Toute composition cible PBO MUST inclure le module officiel essentiel PZT, au-dessus du Kernel et de pixs.core, par les mécanismes génériques de modules. Le réseau activé/configuré MUST toujours être exécuté par le binaire PZT de PA compilé avec Cython ; PBO MUST assurer configuration, visualisation, supervision et monitoring. Désactiver le réseau MUST NOT retirer le module essentiel de PBO.

#### Scenario: Module essentiel PBO et binaire PZT dédié

- **WHEN** PZT est désactivé dans un PBO
- **THEN** le binaire réseau se ferme mais le module PBO de gestion reste composé
~~~~

### Référence reference-runtime--eb2f9f2af9

Source : `openspec/specs/reference-runtime/spec.md`, ligne 168. SHA-256 du bloc : `37e910ca3a63eaa93c85bf35594c6ee0857b63ec5c280bd47537f3a655ed89bd`.

~~~~text
### Requirement: Couche exécutable PA séparée

Les binaires PA définis par pixs-agent MUST constituer une couche d’exécution locale distincte et MUST NOT remplacer Django, PostgreSQL ou TanStack ni devenir un backend métier alternatif. Leur compilation MUST suivre le choix Nuitka pour trois binaires et Cython pour PZT.

#### Scenario: Couche exécutable PA séparée

- **WHEN** un binaire PA est décrit
- **THEN** il ne devient pas une implémentation alternative de l’autorité métier PBO
~~~~


## Rapprochement avec le canon courant — reprise CISMP7 du 22 octobre 2026

Les six copies et empreintes historiques ci-dessus restent intactes. La table suivante repère leurs exigences correspondantes dans le canon relu sous accès de lecture CAB ; elle ne régénère aucune preuve historique et ne constitue aucun delta normatif. Les titres, lignes et empreintes ci-dessous décrivent cette relecture datée et devront être recontrôlés si le canon évolue.

| Bloc historique | Source actuelle et ligne | Exigence courante | Scénarios du bloc | SHA-256 du bloc courant |
| --- | --- | --- | ---: | --- |
| pixs-agent / 11 | [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md), ligne 64 | Trois binaires PA et six modes distincts de PZT | 1 | `5cd5cae10cd478a8ffb30c4e15180dfdc341506019583f78882f62ec99106408` |
| pixs-agent / 20 | [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md), ligne 78 | Compilation différenciée validée | 1 | `49d91499d8f83f1c794a0c59612a178648ad502a5b43f2965eba5f1f79a072e6` |
| pixs-agent / 47 | [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md), ligne 108 | Composition au build et catalogue fermé | 1 | `0ed896227fd4520562a556c15ca86d634e059dc29313794ff743d8324201c20b` |
| pixs-agent / 218 | [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md), ligne 296 | Paramètres ouverts et absence d'implémentation implicite | 1 | `2fe8f8e831ff5c8809f75a824394b629f715e43baab2b850615835c04c39ba78` |
| pzt / 21 | [openspec/specs/pzt/spec.md](../../specs/pzt/spec.md), ligne 77 | Module essentiel pixs.pzt et exécutable PZT indépendant | 1 | `1063497b290fd7bb8e8abad2dad81ac19bb67f139b4c911c98be000279df7b7c` |
| reference-runtime / 168 | [openspec/specs/reference-runtime/spec.md](../../specs/reference-runtime/spec.md), ligne 221 | Couche exécutable PA séparée | 1 | `409ab89f825b092bd0b952bce1b1e35b9f4b326cd4c20d55d333a5a993bb892f` |

Méthode d’empreinte : bloc UTF-8 depuis son titre `### Requirement:` jusqu’au titre suivant de même niveau exclu, blancs terminaux retirés, puis un unique LF final ajouté ; tous les scénarios du bloc sont inclus. Six exigences et six scénarios sont repérés. Une empreinte n’est pas une preuve d’implémentation.

La correspondance actuelle retient trois binaires et six modes PA, plus PZT indépendant et son mode `pzt-daemon`, avec Cython pour les deux chaînes distinctes. Elle conserve le catalogue fermé, les paramètres non décidés, les responsabilités de `pixs.agent`/`pixs.pzt` et l’absence d’autorité métier des exécutants. Les copies Nuitka ou du quatrième binaire rattaché à PA restent uniquement historiques.

Les candidats CPython 3.14.9 avec GIL/Cython 3.3.0, la distribution en répertoire et la première cible Debian 13 x86_64 physique/VM sont consignés dans [le premier lot validé](design.md). Leur validation ne qualifie pas la chaîne ni une plateforme et ne modifie pas les exigences canoniques.
