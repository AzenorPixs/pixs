# Corrections et vérifications de la baseline du 16 septembre 2026

Lot réalisé sur validation explicite du développeur le 26 octobre 2026,
incluant la consultation de l'historique Git. Il complète le
[rapport RCAMP initial](../../../../output/rcamp/rcamp2-pixs-01a1794bbc21/REVALIDATION.md).
Les sept artefacts de l'archive cible et les artefacts du RCAMP initial sont
préservés. Les corrections documentaires se trouvent dans ce nouveau dossier.
Une modification concurrente de l'archive auxiliaire du bootstrap est
documentée au §5 ; les preuves historiques proviennent du commit H1 immuable.

## 1. Sources retrouvées et portée des preuves

| Source | Référence | Fait observé |
| --- | --- | --- |
| H0, canon avant | `1d96ece501606330b45c6819054ba6e581b824bd`, 16 septembre 2026, 20:05:16 +02:00 | 74 capacités, 287 exigences, 290 scénarios ; change documentaire encore actif |
| H1, canon et archive | `b83f9de8827f94fe930972a6abf6663fca7a1c29`, 16 septembre 2026, 22:52:47 +02:00 | 76 capacités, 300 exigences, 305 scénarios ; six artefacts de l'archive présents |
| Filiation | H0 est le parent direct de H1 ; H1 est ancêtre du HEAD consulté | Comparaison de deux états successifs d'une même lignée |
| Autre lignée accessible | `05917cd94febc6702be79cb4f1fa0a4540a178c1` et `61543ea2ebb27fb0fa6e6026293f5784348cf816` | Canons respectivement identiques à H0 et H1 ; ces commits ne sont pas des ancêtres du HEAD consulté |
| Canon courant capturé | HEAD `21f8b9beae4d85c4891da5cf075f06df418e0236`, fichiers de travail empreintés | 78 capacités, 859 exigences, 1 064 scénarios |
| Outil déclaré dans le DEVOPS historique H1 | OpenSpec `v1.13` | Métadonnée d'environnement, pas preuve d'exécution de cette version |
| Outil des contrôles du lot | OpenSpec `1.15.0`, chemin déclaré dans le DEVOPS courant | Validations actuelles seulement |

Les empreintes de canons H0/H1, les chemins, lignes et empreintes de chaque
élément sont dans [evidence.json](evidence.json). Les bornes de recherche
Git sont conservées dans
[historical-research.json](../../../../output/baseline-traceability/20261026-consolidate-initial-specification-baseline/historical-research.json).

Les blocs sont délimités par leurs titres, avec retrait du seul espacement
blanc de séparation en bordure. Leurs empreintes ne sont pas les empreintes
de fichiers entiers ; ces dernières sont conservées séparément.

Git réunit dans H1 l'intégration du bootstrap et la présence de l'archive de
consolidation. Il ne fournit pas l'ordre fin des commandes, leur sortie,
ni une autorisation humaine d'archivage. Une date de commit ou un dossier
daté ne remplace pas ces preuves.

## 2. Corrections des deux écarts

### E1 — Couverture élément par élément

La [nouvelle matrice](conservation-matrix.md) contient une ligne pour chacun
des **605 éléments** de H1 : **300 exigences et 305 scénarios**. Chaque ligne
porte un repère d'audit, le titre exact, le rattachement du scénario, les
lignes source et cible, le statut de conservation, les dépendances explicites
et le repère courant. Les chemins complets et empreintes sont dans le JSON
associé. Les repères B ne remplacent aucun identifiant du canon.

Les dépendances correspondent aux références de capacités nommées dans les
blocs et aux cinq dépendances déclarées pour le bootstrap. L'absence de
référence explicite ne prouve pas une indépendance sémantique.

Le contrôle établit :

- **72 fichiers de capacité identiques octet pour octet** entre H0 et H1 ;
- **577 éléments anciens** conservés, dont ceux d'audit et d'operations ;
- **28 éléments provenant des quatre deltas du bootstrap** : 13 exigences
  et 15 scénarios ;
- **603 blocs identiques** à leur source ;
- deux exigences conservées après repliement des lignes de prose :
  `operations / Maintenance hiérarchisée` et
  `initial-administration / Panneau d'administration contrôlé`.

Pour ces deux exigences, les empreintes brutes sont différentes et conservées
comme telles. Les paragraphes et la séquence textuelle restent identiques
après repliement ; aucune identité brute n'est annoncée pour ces blocs.

**Résultat E1 : correction documentaire réalisée dans le nouveau lot.**

### E2 — Réconciliation de l'arithmétique et registre des écarts

M-001 était correcte pour les 72 capacités qu'elle couvre. L'omission vient
des éléments **anciens d'audit et d'operations**, tandis que M-002 et M-003
ne comptaient que leurs nouveaux deltas.

| Groupe reconstitué | Exigences | Scénarios |
| --- | ---: | ---: |
| 72 capacités stables | 277 | 280 |
| audit, contenu ancien | 5 | 5 |
| operations, contenu ancien | 5 | 5 |
| audit, delta du bootstrap | 1 | 1 |
| operations, delta du bootstrap | 1 | 1 |
| initial-application-bootstrap, delta | 4 | 4 |
| initial-administration, delta | 7 | 9 |
| **Total** | **300** | **305** |

Les capacités sont dédupliquées par chemin : 72 + audit + operations + les
deux nouvelles capacités = **76**. Les dix exigences et dix scénarios ne
sont donc ni perdus dans le canon H1 ni à inventer : leurs vingt lignes sont
désormais présentes dans la matrice détaillée.

**Résultat E2 : cause établie et agrégation corrigée dans le nouveau lot.**
La matrice archivée est préservée avec son erreur historique.

### Registre des décisions et limites

| Référence | Nature | Conclusion |
| --- | --- | --- |
| D01 | Autorisation actuelle du développeur | Réaliser ce lot et consulter Git, en préservant l'archive ; elle ne prouve aucun accord de septembre |
| D02 | Choix méthodologique vérifié | Utiliser H0/H1 dans la lignée du HEAD et qualifier séparément l'autre lignée accessible |
| D03 | Correction d'agrégation | Ajouter les contenus anciens audit 5/5 et operations 5/5 à la reconstitution ; conserver les totaux prouvés 300/305 |
| L01 | Validation humaine historique | Accord de septembre sur la matrice et les lots non retrouvé dans les sources consultées |
| L02 | Présentation et archivage historiques | Compte rendu présenté et autorisation d'archivage non retrouvés |
| L03 | Qualification stricte historique | Sortie d'époque non retrouvée ; les contrôles 1.15.0 ne reproduisent pas l'exécution de l'outil déclaré v1.13 |
| L04 | Évolution du Super Admin | Remplacement d'un scénario constaté dans Git ; référence d'arbitrage humain ou de change distinct non établie par cette recherche |

## 3. Résultat des sept vérifications

« Levé sur le contenu historique » signifie que les objets documentaires
de septembre sont maintenant comparés et expliqués. Cela ne vaut ni
validation fonctionnelle du runtime actuel ni preuve d'un accord humain.

| Point du change archivé | Vérification réalisée | Résultat et limite |
| --- | --- | --- |
| **1.3 — Validation de la matrice et des lots** | Recherche des artefacts du change dans quatre versions Git accessibles, de leurs métadonnées et des documents associés ; lecture des prescriptions et cases cochées | **NON VÉRIFIABLE historiquement.** Aucun accord explicite daté portant sur une version identifiable de la matrice et des lots n'a été retrouvé. La validation du lot actuel ne le reconstitue pas. |
| **2.1 — Aucun delta nécessaire à la consolidation** | Union contrôlée des 577 éléments de H0 et des 28 éléments des deltas du bootstrap ; comparaison des 605 éléments de H1 ; vérification de `skip_specs: true` dans le change documentaire | **LEVÉ sur le contenu historique.** Aucun ajout, retrait ou remplacement normatif résiduel n'est attribuable à la consolidation. Les seuls ajouts canoniques sont ceux des quatre deltas du bootstrap. L'ordre exact des commandes au sein du commit n'est pas établi. |
| **2.2 — Relations de bootstrap, opérateur et SecretProvider** | Comparaison des 13 exigences et 15 scénarios des quatre deltas avec H1 ; vérification des cinq capacités de dépendance, du maintien des blocs anciens et de l'absence de résidu normatif | **LEVÉ pour le portage dans H1.** La consolidation n'ajoute aucun transfert, duplication ou changement fonctionnel de ces blocs. Le canon actuel a ensuite évolué, notamment pour le compte fonctionnel Super Admin ; aucune identité fonctionnelle entre septembre et aujourd'hui n'est prétendue. |
| **3.1 — Validation stricte et revue** | Revue de la matrice exhaustive ; validations du nouveau lot et d'une copie isolée H1 avec l'outil actuel ; contrôles courants standard et strict ; recherche de la sortie d'époque | **PARTIEL.** La preuve documentaire et les résultats actuels sont établis. La sortie de validation historique n'est pas retrouvée, le binaire déclaré v1.13 n'a pas été réexécuté et les résultats stricts actuels comportent les refus détaillés ci-dessous. |
| **3.2 — Aucune synchronisation supplémentaire** | Comparaison des ensembles de repères et textes des quatre deltas aux capacités H1, avec distinction explicite des deux repliements de prose | **LEVÉ pour cette archive.** Aucun élément du bootstrap attendu par la matrice ne manque dans H1 et aucune autre clause de consolidation n'attend une synchronisation. Aucun `opsx-sync` n'a été exécuté ; les autres changes actifs restent hors conclusion. |
| **4.1 — Identifiants préservés ou arbitrés** | Inventaire exhaustif H0/H1 et recherche de chacun des 605 repères dans le canon actuel, avec vérification du commit des cinq changements de rattachement ou titre | **PARTIEL au sens historique + courant.** La conservation dans H1 est établie. Aujourd'hui, 600 repères sont inchangés, quatre scénarios ont changé de rattachement et un a été remplacé. Ce dernier a une preuve Git, mais pas de référence d'arbitrage humain ou de change distinct retrouvée dans ce lot. |
| **4.2 — Présentation avant archivage** | Recherche du compte rendu présenté et de la décision dans les quatre versions documentaires et métadonnées Git ; distinction entre présence de l'archive et décision d'archiver | **NON VÉRIFIABLE historiquement.** La présence de l'archive dans H1 est prouvée ; la présentation et l'autorisation préalable ne sont pas attestées par une trace retrouvée. |

Bilan : **sept points examinés**, dont **trois levés sur le contenu
historique**, **deux partiellement établis** et **deux sans preuve humaine
historique retrouvée**. Aucun statut non applicable n'est inventé.

La recherche documentaire dans les sorties projet nommant la cible retrouve
le RCAMP courant et une référence dans le checkpoint GSCM d'octobre. Ces
éléments ne constituent pas des accords de septembre. Les stockages privés
OpenCode, journaux exclus et secrets n'ont pas été lus. L'absence constatée
est limitée à ce périmètre ; elle n'affirme pas qu'aucune preuve n'existe ailleurs.

### Évolutions identifiées dans le canon actuel

Les cinq différences de repère sont corroborées dans le commit
`6ac22961c242a8da709ec1801b7021410d18b479` du 14 octobre 2026 à
21:28:55 +02:00. Le vérificateur contrôle la présence de l'ancien rattachement
dans son parent et du nouveau rattachement dans ce commit.

| Repère | Scénario historique | Situation actuelle |
| --- | --- | --- |
| B0275 | Fanion d'autorisation indisponible | Déplacé de `Échec fermé pour le sensible` vers `Repli DEFAULT réservé au non sensible` ; texte du scénario identique |
| B0296 | Référence de secret après provisionnement | Déplacé vers `Reprise et références de secrets après provisionnement` ; texte identique |
| B0299 | Opérateur initial vérifié | Remplacé par `Compte fonctionnel créé explicitement` ; texte et règle du compte Super Admin modifiés |
| B0303 | Ancienne route d'administration | Déplacé vers `Changement contrôlé de la route d'administration` ; texte identique |
| B0535 | Élargissement implicite refusé | Déplacé vers `Propagation et frontière d'autorisation du ScopeContext` ; texte identique |

Au total, 561 des 605 corps de blocs historiques sont encore identiques au
canon courant, et 44 diffèrent. La présence d'un titre ne prouve donc pas
l'identité de son comportement. Le lot n'autorise aucune restauration du
canon de septembre ni aucune correction de ces évolutions postérieures.

## 4. Contrôles exécutés et limites

Cette section conserve les résultats de la réalisation initiale, avec les
sources et dates de leurs preuves. Les résultats ultérieurs de la phase
d'archivage sont distingués au §6 et dans `STATISTIQUES.md`.

Les preuves horodatées des contrôles OpenSpec et de reproduction, avec
commandes, sorties et codes de retour, sont
dans [le dossier de contrôles](../../../../output/baseline-traceability/20261026-consolidate-initial-specification-baseline/controls-index.json).

| Contrôle | Résultat observé | Portée |
| --- | --- | --- |
| Syntaxe Python du vérificateur | Succès de `python3 -m py_compile` avec Python DevOps 3.14.10, observé dans les sorties natives de réalisation | Borne déclarée Python >= 3.12 conservée ; aucune dépendance ajoutée ; l'exécution sous un interpréteur 3.12 n'est pas prétendue |
| Génération et reproduction de la matrice | 605 éléments ; 603 identiques et deux repliements documentés | Contrôle des sources Git, des ensembles, des textes et des empreintes protégées |
| Première relecture finale | Arrêt explicite, code 1, sur une modification de l'archive auxiliaire | Échec conservé ; aucune restauration ni remise à zéro des empreintes initiales ; voir la réconciliation du §5 |
| Nouveau lot, validation ciblée stricte | **1/1**, code 0 | Shape OpenSpec du nouveau change documentaire, sans delta normatif |
| Copie isolée H1, validation standard | **77/77**, code 0 | 76 capacités et le seul change documentaire de consolidation |
| Copie isolée H1, validation stricte | **75/77**, code 1 | Le change documentaire passe ; `initial-administration` a quatre avertissements de longueur et `initial-application-bootstrap` en a un |
| Projet courant, validation standard | **186/186**, code 0 | 78 capacités et 108 changes actifs au moment du contrôle |
| Projet courant, validation stricte | **185/186**, code 1 | Les 78 capacités passent ; seul `add-pa-system-session-lifecycle` est refusé à cause des sept avertissements de longueur déjà extérieurs au lot |

Les empreintes des entrées des deux contrôles globaux sont stables pendant
leur exécution. La copie historique contient seulement les sources
empreintées de H1 et un dossier temporaire de validation ; elle a été
nettoyée sans déplacer l'archive réelle. Ses résultats ne sont pas ceux d'une
exécution en septembre avec OpenSpec v1.13.

Les avertissements ne sont ni masqués ni corrigés hors périmètre. Un
contrôle strict actuellement refusé n'est pas annoncé réussi. Les tests
Django, PostgreSQL, frontend, navigateur et les constructions de binaires sont
sans objet pour ces seules corrections documentaires ; aucun n'a été exécuté.

## 5. Préservation, réalisation et suites

[preservation.json](preservation.json) conserve les empreintes initiales de
**17 fichiers d'archives** et **78 spécifications canoniques**, sans les
remplacer. Le contrôle final exige l'identité des **sept fichiers de l'archive
cible**, dont `STATISTIQUES.md`, et des **78 spécifications canoniques**,
ainsi que leurs inventaires. Aucun des sept fichiers cibles n'est amendé.

### Modification concurrente de l'archive auxiliaire

Le premier contrôle final s'est arrêté sur une modification de la métadonnée
`.openspec.yaml` du bootstrap. L'observation suivante, à
`2026-10-26T19:32:44Z`, relève quatre documents modifiés (`README.md`,
`proposal.md`, `design.md`, `tasks.md`) et trois fichiers absents
(`specs/audit/spec.md`, `specs/operations/spec.md`,
`specs/initial-administration/spec.md`) dans
`2026-09-16-specify-initial-application-bootstrap`. La métadonnée est alors
de nouveau identique à l'empreinte initiale. Ces changements ne sont pas
des écritures de ce lot ; ils sont postérieurs aux contrôles globaux.

Les anciennes et nouvelles empreintes, présences et dates de fichiers sont
conservées dans [source-drift.json](../../../../output/baseline-traceability/20261026-consolidate-initial-specification-baseline/source-drift.json).
Aucune restauration, suppression ou réécriture n'est effectuée dans cette
archive auxiliaire. Sa préservation globale n'est pas annoncée.

La matrice et ses 605 preuves normatives lisent déjà les quatre deltas
**dans Git H1**, et non dans la copie de travail de l'annexe. La réconciliation
consiste à rendre cette frontière explicite : le contrôle bloquant protège
l'archive cible et le canon, tandis que les sources auxiliaires sont
vérifiées dans le commit immuable. Les 605 enregistrements sont comparés
avant et après cette clarification ; leurs contenus restent identiques.
Les différences concurrentes restent visibles dans le rapport et les preuves.

### Périmètre de réalisation

Les écritures de la réalisation initiale sont limitées au présent nouveau dossier et aux
preuves sous `output/baseline-traceability/`. Git a été consulté en lecture
seule. L'exception de propriétaire requise pour sa lecture est passée par
`git -c safe.directory=…` pour chaque commande, sans modification persistante
de configuration. Aucun commit, push, changement de branche, synchronisation
ou archivage n'a été réalisé pendant cette première phase.

Pour achever les preuves encore partielles, il faut retrouver les accords
de septembre, la sortie de validation d'époque et la référence d'arbitrage
du remplacement du scénario du Super Admin. Une approbation actuelle peut
valider le référentiel reconstruit pour l'avenir, mais ne transforme aucune
de ces traces manquantes en fait historique établi.

Les deux écarts documentaires sont corrigés dans ce lot. Il a été laissé
actif pour revue ; les limites historiques et les refus stricts ont été
conservés pour la décision du développeur.

## 6. Validation actuelle et autorisation d'archivage

Le 26 octobre 2026, le développeur valide le lot
`reconstruct-initial-specification-baseline-traceability` et demande
explicitement son archivage avec statistiques, en conservant les réserves
historiques et les points partiels.

Cette décision actuelle autorise l'archivage du présent lot documentaire.
Elle ne prouve aucun accord humain de septembre et ne lève ni les deux
points partiels (3.1 et 4.1), ni les deux points historiquement non vérifiables
(1.3 et 4.2). Le bilan reste trois points levés sur le contenu historique,
deux partiels et deux non vérifiables historiquement. Les refus stricts et
la dérive concurrente de l'annexe restent également documentés.

La preuve du déplacement natif et les statistiques sont rattachées à cette
phase après constat du résultat d'OpenSpec. Aucun réarchivage de la baseline
historique ni synchronisation normative n'est autorisé par cette opération.

OpenSpec a confirmé le déplacement vers
`2026-10-26-reconstruct-initial-specification-baseline-traceability`, avec
`specsUpdated: false`. Le vérificateur a ensuite reproduit les 605 éléments
depuis son emplacement archivé. Les contrôles globaux de cette phase donnent
185/185 en mode standard et 185/185 en mode strict, avec codes de retour 0.
Ces résultats datés n'annulent ni les refus observés pendant la réalisation
initiale, ni l'absence de sortie d'exécution de septembre avec l'outil
déclaré v1.13. Les statuts des sept points restent inchangés.

La preuve native et les relevés de cette phase sont dans
[les preuves d'archivage](../../../../output/baseline-traceability/20261026-consolidate-initial-specification-baseline/archivage/state.json).
Le rapport [STATISTIQUES.md](STATISTIQUES.md) sépare la réalisation documentaire
et la phase d'archivage, conserve les données absentes en `N/A` et reprend
explicitement les deux points partiels et les deux réserves historiques.
