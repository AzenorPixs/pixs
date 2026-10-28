# Tâches — C14

Les coches distinguent les réalisations et validations techniques effectivement prouvées. La préparation du dossier et son strict syntaxique ne valent pas réalisation ; les tâches restantes conservent leurs critères propres.

## 1. Revue de conception

- [x] 1.1 Revoir les exigences/scénarios de requirements.md et l’adoption du profil C00 ; recouper les sources actuelles avant réalisation.
- [x] 1.2 Lever les barrières de conception énoncées dans design.md, présenter les fichiers/contrats et tout delta nécessaire avant écriture de code.

## 2. Réalisation

- [x] 2.1 Définir identifiants, manifests, propriétés de données et contrats publics PZT/DNS, sous revue d’architecture.
- [x] 2.2 Implémenter les modules essentiels et leur intégration au lifecycle commun.
- [x] 2.3 Implémenter configuration/visualisation/supervision honnêtes pour le profil réseau et service DNS non sélectionnés.
- [x] 2.4 Tester absence essentielle bloquante, état non appliqué/non mesuré, refus d’opération exigeant PA et conservation des obligations de gestion.

## 3. Preuves et clôture

- [x] 3.1 Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, avec résultats natifs et preuves.
- [x] 3.2 Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.
- [x] 3.3 Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.
- [x] 3.4 N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.

## Phasage demandé par le développeur le 23 octobre 2026

Le développeur a demandé de réaliser toutes les tâches de réalisation restantes,
puis de procéder aux tests et à la validation dans un second temps. Cette
instruction explicite prévaut sur l'ordre d'exécution immédiate du contrat
historique ci-dessous. Les critères, dépendances et contrôles restent requis.

La réalisation a précédé la phase de tests, selon cette instruction. Les
tâches 2.3/2.4 et 3.1/3.2 disposent désormais des preuves natives exposées
dans VALIDATION.md. Les contrôles de revue et de clôture 3.3/3.4 restent
non cochés jusqu’à leurs propres preuves ; aucun test non exécuté n’est
présenté comme réussi.

Le raccord serveur utilise les exports publics ModuleHttp de C11. La recette
du frontend composé attend son pipeline/runtime effectivement disponible ;
aucun double de transport ou d'exécutant ne vaut cette preuve.

## Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026

Les identifiants et cases ci-dessus sont conservés. Ce contrat précise les critères et contrôles à réaliser **dans chaque tâche**, avant de commencer la suivante. Les tâches de test ou de preuve placées plus loin consolident la couverture et ne reportent jamais les vérifications nécessaires à une tâche antérieure. Une tâche de réalisation comprend donc ses unités, refus et intégrations indispensables dès sa propre exécution ; elle ne peut être validée en attendant qu’une tâche suivante la rende testable.

Les tâches cochées conservent leur statut historique ; leurs preuves doivent être recoupées avant réutilisation si les sources ont changé. Pour les tâches futures, les prérequis externes sont ceux de design.md et des exigences applicables ; un propriétaire, provider, exécutant, contrat adopté ou environnement requis manquant bloque la tâche concernée. La préparation du dossier ne les déclare pas livrés. Les choix ouverts restent à décider avant leur réalisation ; les deltas déjà adoptés ne sont pas réappliqués.

### Périmètre et cas de contrôle propres au lot

- Objet : Périmètre des tâches ci-dessus, sous les contrats publics et propriétaires de design.md.
- Résultat de référence : Les sorties et refus attendus des scénarios applicables au périmètre de cette tâche sont observés ; aucun niveau de garantie ni support non exécuté n’est annoncé.
- Cas de contrôle du profil : Tester absence essentielle bloquante, état non appliqué/non mesuré, refus d’opération exigeant PA et conservation des obligations de gestion. ; Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.

Chaque contrôle est relié au texte complet de l’exigence et à son scénario, dans requirements.md lorsqu’il existe, sinon dans les deltas et le canon référencés par la proposition. Une simple égalité de titre ne prouve pas la couverture. Les cas conditionnels sont appliqués selon le rôle effectivement sélectionné ; une non-applicabilité est motivée sans remplacer une preuve obligatoire. Aucun paramètre numérique ou provider nouveau n’est déduit de ce contrat.

### Critères et contrôles par tâche future

| Tâche existante | Prérequis immédiat | Critère observable de validation | Contrôles exigés dans cette tâche et preuve |
|---|---|---|---|
| 1.1 | Sources, décisions et prérequis externes accessibles ; références et tâches historiques pertinentes recoupées | Inventaire documenté des exigences/scénarios, entrées, sorties, propriétaires, invariants, refus, dépendances et écarts ; les décisions restantes sont identifiées pour 1.2, sans les présumer résolues. | Vérifier les titres, scénarios, liens et empreintes du canon courant ; recouper C00 historique et la sélection locale C08 ; distinguer faits, déductions, choix acquis, modalités à qualifier et preuves manquantes. Aucun code ni test produit nécessaire pour cet inventaire documentaire. |
| 1.2 | Tâche 1.1 techniquement validée avec ses propres preuves | Conception documentée des fichiers, contrats et limites de C14 ; les décisions obligatoires pour 2.1 sont résolues dans le canon adopté ou explicitement validées avant réalisation, et les dépendances d’intégration restent identifiées. | Revue des scénarios et refus concernés, cohérence des propriétaires et frontières C08/PA10, contrôle version/liens/structure ; présenter tout delta nécessaire avant écriture de code. Les arbitrages impactants restent soumis au développeur. Une preuve obligatoire manquante interdit 2.1. |
| 2.1 | Tâche 1.2 techniquement validée avec ses propres preuves | Livrable de conception/profil explicitant les entrées, sorties, propriétaires, invariants, refus et dépendances de cette tâche ; aucun choix obligatoire ouvert pour son exécution dépendante. | Revue ciblée des scénarios du lot affectés par cette tâche, des cas de refus et des décisions ; vérifier version/liens/structure. Si la définition produit des modèles ou contrats exécutables, ajouter immédiatement syntaxe et unités de validation/limites sans attendre la tâche suivante. |
| 2.2 | Tâche 2.1 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.3 | Tâche 2.2 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.4 | Tâche 2.3 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 3.1 | Tâche 2.4 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 3.2 | Tâche 3.1 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 3.3 | Tâche 3.2 techniquement validée avec ses propres preuves | Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée. | Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée. |
| 3.4 | Tâche 3.3 techniquement validée avec ses propres preuves | Périmètre, preuves et limites relus ; autorisations finales séparées et identité de l’artefact préservée ; aucune archive ou publication anticipée. | Comparer fichiers et preuves, vérifier les seules autorisations effectivement acquises et contrôles de clôture applicables ; conserver l’état actif si l’opération finale n’est pas autorisée. |

Les vérifications utilisent les outils et versions du projet selon [AGENTS.md](../../../../AGENTS.md) et [DEVOPS.md](../../../../DEVOPS.md). Pour un changement Python, inclure la compilation syntaxique et les suites configurées ; pour une interface web, inclure tests et build frontend ainsi que Chromium et Firefox headless, et les contrôles visuels/manuels applicables. Les tests matériels, réseau, stockage, packaging et restauration exigent leur environnement autorisé. La syntaxe seule ne valide aucun comportement. Aucun de ces contrôles n’est exécuté par la présente préparation documentaire.

Pour chaque tâche, conserver identifiant, prérequis, fichiers, commandes, résultats natifs, critère/scénario, versions/artefact, limites et prochaine action ; cocher uniquement après validation technique. Un échec ou une preuve obligatoire indisponible interdit la tâche suivante. Une modification concurrente invalide seulement les preuves affectées et impose leur réconciliation avant reprise.

### Incidence du parcours C08 adopté

Le [parcours C08](../../add-installation-and-first-configuration/proposal.md) impose la sélection explicite de PA système et PZT local pour préparer PostgreSQL et initier sa première connexion technique. Le réseau distant et les sessions utilisateur PA ne sont pas activés par ce choix. Dans Docker Pixs, le logiciel PostgreSQL est fourni sans données/cluster/secret dans les couches ; le profil conserve les données persistantes et un propriétaire de préparation admissible unique. L’image contient deux binaires PA système/événements et PZT indépendant, sans binaire utilisateur. Le paquet PA reste distinct du paquet PBO/PFO ; sélectionner l’exécutant ne l’incorpore pas à PBO.

Les qualifications de l’ancien profil sans ces exécutants ne prouvent pas le parcours révisé. Les tests locaux de chaque tâche concernée et la recette finale doivent recouper C08 P01–P10, la politique native pré-base, les secrets et l’audit indépendants, les droits ordinaires après PostgreSQL, la reprise et les budgets réellement accordés. Aucun acteur technique ne réalise l’acte métier R01 ; tous échanges PBO–PA restent via PZT. Le mécanisme de secrets Docker et ses versions/paramètres restent à qualifier, sans équivalence systemd supposée.


### Validation technique 2.3

La tâche 2.3 est validée après le build COMPOSED réel et ses deux campagnes
Chromium/Firefox, quinze critères vrais chacune sur HTTPS loopback et
PostgreSQL isolé : call_01a169bcf17272ebbf540c33af2640d7 et
call_01a169be739c77e89e8bd39453f4b0ad. Les preuves, versions, empreintes,
échecs conservés et limites sont détaillés dans VALIDATION.md. Les tests
de contrats et du domaine restent distingués du renderer réel. La chaîne
TLS/PKI, les exécutants, le DNS actif, les artefacts installés et le P0
global ne sont pas qualifiés. Les validations ultérieures restent distinctes de cette preuve 2.3.


### Validation technique 2.4

La tâche 2.4 est validée sur les quatre gardes de composition réelles
(call_01a169c577dc7195ade8870a436c4511) puis la réexécution 38 + 104
de gestion/lifecycle PostgreSQL (call_01a169c8761370ce909c7c20f0ef5508).
Les critères, plateformes, effets, échecs attendus et limites sont conservés
dans VALIDATION.md. Les contrôles de revue et de clôture conservent leurs preuves distinctes.

### Validation technique 3.1 et 3.2

Le contrôle call_01a16aa836db737c844a192dad35611c prouve syntaxe Python/JS,
145 cas configurés dans chacun des deux navigateurs et build STANDALONE.
Les recettes visuelles call_01a16aaaba3d774e93a80f78cac802ba et
call_01a16aab9467709fbc1a3dc63e7dff23 confirment le renderer composé,
HTTPS loopback, PostgreSQL, nettoyage, deux largeurs et champs étiquetés.
Les huit captures ont été relues. La matrice de VALIDATION.md conserve les
preuves d’isolation/refus et les non-exécutions motivées, dont accessibilité
manuelle exhaustive, PKI, transport PA/PZT, installation et DNS actif.
La revue et la clôture 3.3/3.4 ne sont pas déduites de ces résultats.

### Revue finale et admission de clôture 3.3/3.4

La revue native call_01a16ab5067576c79dd11e3df009124f a contrôlé 373
sources/dépendances, le périmètre de 75 fichiers C14, 21 références et
38 liens relatifs, les empreintes canoniques et UTF-8/LF. OpenSpec strict
valide le change puis 187 éléments globaux, zéro échec. Les messages INFO
sur des dossiers tiers ne sont pas une autorisation d'archiver ces dossiers.
Le diff est examiné depuis les contenus et mandats conservés, sans commande
Git ; les apports préexistants et concurrents restent préservés.

L'invocation 1CISMP4 autorise l'archivage unique C14, la génération de ses
statistiques et la publication/clôture CAB ciblées. La coche 3.4 atteste
cette revue des autorisations et limites ; elle ne prétend pas que l'archive,
STATISTIQUES.md, la publication ou le gate sont déjà exécutés. Le RUN reste
ouvert jusqu'à leurs preuves distinctes. Aucun Git, déploiement, activation
BIND 9, second change ou arrêt des services partagés n'est autorisé par
cette admission. Les liens du dossier déplacé et ses références entrantes
actives sont rétablis mécaniquement lors de l'archivage ; les archives
historiques et les contenus fonctionnels tiers sont conservés.
