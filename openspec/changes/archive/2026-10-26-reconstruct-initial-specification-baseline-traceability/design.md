## Context

La matrice archivée annonce 76 capacités, 300 exigences et 305 scénarios,
mais ses cinq lignes donnent 290 exigences et 295 scénarios. La recherche
Git autorisée retrouve les sources nécessaires à une reconstruction.

## Goals / Non-Goals

**Goals:** produire une matrice exhaustive, expliquer l'écart, examiner les
sept points et conserver les preuves des contrôles réellement exécutés.

**Non-Goals:** modifier une archive, un comportement, le canon ou un autre
change ; présumer une validation humaine à partir d'un commit ou d'une case
cochée ; effacer une incertitude historique avec une approbation actuelle.

## Decisions

### Références datées et filiation

- H0 : `1d96ece501606330b45c6819054ba6e581b824bd`, 16 septembre
  2026 à 20:05:16 +02:00, parent direct de H1.
- H1 : `b83f9de8827f94fe930972a6abf6663fca7a1c29`, 16 septembre
  2026 à 22:52:47 +02:00, ancêtre du HEAD consulté.
- Le HEAD de départ est `21f8b9beae4d85c4891da5cf075f06df418e0236`.
- Les commits `05917cd94febc6702be79cb4f1fa0a4540a178c1` et
  `61543ea2ebb27fb0fa6e6026293f5784348cf816` appartiennent à une autre
  lignée accessible. Leurs canons corroborent respectivement H0 et H1 ;
  ils ne sont pas présentés comme ancêtres du HEAD.

La date d'un commit prouve la présence d'un contenu dans cet historique,
pas l'heure d'une commande d'archivage ni un accord humain.

### Reconstruction sans correction rétrospective

Les 72 capacités stables donnent 277 exigences et 280 scénarios. Les cinq
exigences et cinq scénarios anciens d'audit et ceux d'operations doivent
également être conservés. Les deltas du bootstrap ajoutent 13 exigences et
15 scénarios. La somme correcte est donc 287 + 13 = 300 exigences et
290 + 15 = 305 scénarios, dans 76 capacités distinctes.

La nouvelle matrice corrige l'agrégation dans ce lot. Le document archivé
reste inchangé et son erreur demeure visible comme fait historique.

### Comparaisons explicites

`verify_traceability.py` distingue identité brute d'un bloc et identité
après simple repliement des lignes de prose. Le repliement conserve les
paragraphes, les titres et les structures Markdown ; il n'est pas appliqué
aux listes ou blocs de code. Deux exigences du bootstrap diffèrent seulement
par leurs retours à la ligne : `Maintenance hiérarchisée` et
`Panneau d'administration contrôlé`. Leurs empreintes brutes restent distinctes.

Un bloc commence à son titre et s'arrête au titre suivant ; l'espacement
blanc de séparation en bordure est retiré avant comparaison et calcul de
l'empreinte du bloc. Les empreintes de fichiers de `preservation.json` et
les empreintes de canons H0/H1 portent, elles, sur les octets complets.

Les repères B0001 et suivants sont des repères d'audit locaux, pas de nouveaux
identifiants normatifs. Chaque scénario conserve son exigence parente dans
la comparaison historique. Une dépendance structurée désigne une référence
explicite à une capacité dans le bloc, complétée pour le bootstrap par les
dépendances déclarées par l'archive ; son absence ne prouve aucune indépendance.

### État actuel séparé

La traçabilité courante compare les 605 éléments de H1 au canon lu lors du
lot. Les déplacements de scénarios sont distingués des disparitions. Le
remplacement d'`Opérateur initial vérifié` par
`Compte fonctionnel créé explicitement` est constaté dans le commit
`6ac22961c242a8da709ec1801b7021410d18b479`, avec modification de la clause
du Super Admin. Cette différence postérieure n'est pas une perte imputée
à la consolidation de septembre. Le commit ne vaut pas preuve d'accord humain.

### Preuves et limites

`evidence.json` et `conservation-matrix.md` sont générés depuis les mêmes
sources. `preservation.json` fixe les empreintes initiales des 17 artefacts
des deux archives et des 78 spécifications courantes. Le contrôle bloquant
porte sur les sept fichiers de la cible et le canon. L'archive auxiliaire du
bootstrap a changé dans le répertoire de travail pendant la réalisation ;
ses dix empreintes initiales restent conservées, sans restauration. La
reconstitution utilise exclusivement ses sources normatives immuables dans
H1, et ne dépend donc pas de cette copie de travail concurrente. Les
différences observées sont exposées dans `VERIFICATIONS.md` et la preuve
`source-drift.json`, sans prétendre à la préservation globale de l'annexe.
`VERIFICATIONS.md` porte les conclusions des sept points et les résultats
des contrôles. Les sorties natives complètes restent dans le dossier de
preuves non versionné indiqué par ce rapport.

Les sources Git et documentaires retrouvées peuvent lever un constat
technique. L'absence d'accord ou de sortie de commande historique reste
qualifiée comme telle, sans reconstruction rétroactive.

## Verification Plan

1. Recalculer et comparer les inventaires H0, H1 et les deltas du bootstrap.
2. Vérifier la couverture des 605 éléments, les totaux et les deux repliements.
3. Vérifier la matrice et ses empreintes par une seconde exécution sans écriture.
4. Valider le lot et une copie isolée des artefacts historiques avec OpenSpec.
5. Distinguer contrôles globaux standard et strict, et leurs défauts extérieurs.
6. Vérifier la préservation des sources et l'absence d'écriture dans les archives.

## Migration Plan

Aucune migration ni activation. Le lot a été laissé actif après sa réalisation
initiale. Le développeur a ensuite validé le lot et expressément demandé son
archivage avec statistiques le 26 octobre 2026, en conservant les réserves.
L'archivage porte uniquement sur ce dossier documentaire, sans mise à jour
du canon ni opération Git mutante. Le vérificateur prend en charge les deux
emplacements du lot, actif et archivé ; les liens vers les preuves sont
ajustés au déplacement. Les points partiels et les preuves historiques
absentes gardent leurs statuts.
