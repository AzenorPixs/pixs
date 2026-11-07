# Tâches — PA01

Les [orientations A1–A5](DECISIONS_A1_A5.md) et les [détails D-A1/D-A2/D-A3/D-MIG](DETAIL_A1_A2_A3.md) sont VALIDÉS le 26 octobre 2026. Leur inscription couvre uniquement les spécifications et le cadrage. Les quatorze exigences et vingt-cinq scénarios détaillés sont synchronisés à l'identique au canon pixs-agent sur demande explicite complémentaire du développeur le même jour, sans réapplication des autres deltas.

Les [décisions S1/R1/F1](DECISIONS_S1_R1_F1.md) sont VALIDÉES le 27 octobre
2026 et inscrites dans les deltas PA01. Leurs cinq exigences et douze scénarios
sont synchronisés à l'identique aux canons sur demande explicite complémentaire
du développeur du même jour, sans réapplication des autres deltas.
Tables privées Agent, outbox/relais PBO vers PZT et
fournisseurs par domaine sont choisis ; modèles/migrations, intégration, relais,
implémentations/versions et preuves restent manquants. Les cases ci-dessous
et les autorisations propres aux autres sessions restent inchangées ;
aucun code, migration ou test produit n'est réalisé par cette inscription.

Les [détails D-S1/D-R1/D-F1/D-SMIG](DETAIL_S1_R1_F1.md) sont VALIDÉS
DOCUMENTAIREMENT le 27 octobre 2026 et inscrits dans les deltas PA01 :
dix-sept exigences et trente-quatre scénarios NON SYNCHRONISÉS au canon
par cette inscription. Les définitions du schéma physique, du contrat du
relais, des interfaces et de la migration sont acquises ; réalisations,
hébergement/profils opérationnels, versions exécutables et preuves restent
manquants. P-SRF01–P-SRF18 restent NON EXÉCUTÉS, sans nouvelle case cochée.

Le [cadrage documentaire fonctionnel PA/PZT](CADRAGE_FONCTIONNEL.md), demandé le 26 octobre 2026, décrit les interfaces, travaux manquants et recettes futures. Il ne produit aucun code, n'exécute aucun test produit et ne coche aucune tâche ; les conditions de réalisation/exécution des autres sessions restent distinctes.

Le développeur a explicitement autorisé la poursuite du change le 23 octobre 2026 (autorisation conservée). Le cycle par lot adopté le 26 octobre 2026 prévaut pour l'ordre courant : unités testables avec tests ciblés avant écriture suivante. Les cases ne sont cochées que sur preuves techniquement validées.

## Ordre historique — instruction du développeur du 23 octobre 2026 (conservée ; le cycle par lot adopté le 26 octobre 2026 prévaut)

Instruction : « Peux tu réaliser toutes les taches et procéder à la phase de tests et à la validation dans un second lieu ».

1. Réalisation : confirmer la sélection, arrêter les choix réellement ouverts, définir les contrats, produire le code des tâches 4–6 et préparer les tests et recettes de 7–9. Les dépendances de conception et d'autorisation restent obligatoires ; un choix non adopté ne devient pas une hypothèse de réalisation. La préparation des tests n'est pas leur exécution.
2. Tests et validation : exécuter les contrôles documentaires encore différés, la syntaxe, les unités/négatifs, les intégrations et recettes applicables sur les sources finales ; corriger les échecs, réexécuter les preuves invalidées puis valider chaque tâche. Relier les preuves aux scénarios et artefacts avant toute clôture.

Cette instruction remplace uniquement le séquencement temporel des contrôles des sections antérieures ci-dessous : les mentions « avant de commencer la suivante », les prérequis de validation technique immédiate et les interdictions de reporter les tests s'appliquent désormais à la validation finale, pas au passage entre travaux de réalisation autorisés. Les dépendances fonctionnelles, les décisions du développeur, les mandats CAB, les critères observables, les refus de sécurité et les preuves exigées restent conservés. Les prévols de sécurité nécessaires aux opérations CAB restent immédiats.

La tâche 1 conserve sa preuve déjà validée. La sélection de la tâche 2 est préparée dans VALIDATION.md ; son contrôle est différé à la seconde phase et sa case reste vide. Les autres cases restent vides jusqu'à validation sur preuves. Un contrôle différé n'est ni réussi ni dispensé ; un environnement requis indisponible reste explicitement sans preuve et interdit l'achèvement du change.

- [x] 1. Auditer les blocs normatifs et renvois de requirements.md, l’implémentation actuelle et ses preuves ; décider du complément réellement manquant sans recréer l’existant.
- [x] 2. Confirmer la sélection de la capacité, les rôles/plateformes/ressources applicables et les dépendances obligatoires ; ne pas transformer une non-sélection en réussite de test.
- [ ] 3. Lever les barrières de conception de design.md et faire valider les choix encore ouverts avant réalisation ; présenter tout delta normatif ou dépendance supplémentaire nécessaire.
- [ ] 4. Définir les contrats, schémas, propriétaires et adapters du périmètre : Catalogue fermé au build, quatre exécutables, sept modes, Cython pour les trois binaires PA et pour PZT indépendant ; qualifier versions, ABI et runtime avant installation des outils.
- [ ] 5. Réaliser le complément ciblé et son branchement aux dépendances, en conservant les structures déjà livrées.
- [ ] 6. Traiter les échecs, concurrence, limites et interruptions propres au lot ; états incertains explicités et reprise sous autorité/contexte courants.
- [ ] 7. Exécuter syntaxe, contrôles configurés et unités/négatifs applicables, en rapportant les résultats natifs sans données sensibles.
- [ ] 8. Exécuter les intégrations/conformités du profil : Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée.
- [ ] 9. Vérifier la sortie attendue : Contenu et responsabilités exacts ; construction reproductible par cible ; aucune compilation assimilée à une recette fonctionnelle.
- [ ] 10. Relier chaque scénario applicable aux preuves/version/artefact, examiner le diff et les limites ; Git, synchronisation, archive, installation et publication restent soumis à leur autorisation propre.

## Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026

Les identifiants et cases ci-dessus sont conservés. Ce contrat précise les critères et contrôles à réaliser **dans chaque tâche**, avant de commencer la suivante. Les tâches de test ou de preuve placées plus loin consolident la couverture et ne reportent jamais les vérifications nécessaires à une tâche antérieure. Une tâche de réalisation comprend donc ses unités, refus et intégrations indispensables dès sa propre exécution ; elle ne peut être validée en attendant qu’une tâche suivante la rende testable.

Les tâches cochées conservent leur statut historique ; leurs preuves doivent être recoupées avant réutilisation si les sources ont changé. Pour les tâches futures, les prérequis externes sont ceux de design.md et des exigences applicables ; un propriétaire, provider, exécutant, contrat adopté ou environnement requis manquant bloque la tâche concernée. La préparation du dossier ne les déclare pas livrés. Les choix ouverts restent à décider avant leur réalisation ; les deltas déjà adoptés ne sont pas réappliqués.

### Périmètre et cas de contrôle propres au lot

- Objet : Catalogue fermé au build, quatre exécutables, sept modes, Cython pour les trois binaires PA et pour PZT indépendant ; qualifier versions, ABI et runtime avant installation des outils.
- Résultat de référence : Contenu et responsabilités exacts ; construction reproductible par cible ; aucune compilation assimilée à une recette fonctionnelle.
- Cas de contrôle du profil : Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée.

Chaque contrôle est relié au texte complet de l’exigence et à son scénario, dans requirements.md lorsqu’il existe, sinon dans les deltas et le canon référencés par la proposition. Une simple égalité de titre ne prouve pas la couverture. Les cas conditionnels sont appliqués selon le rôle effectivement sélectionné ; une non-applicabilité est motivée sans remplacer une preuve obligatoire. Aucun paramètre numérique ou provider nouveau n’est déduit de ce contrat.

### Critères et contrôles par tâche future

| Tâche existante | Prérequis immédiat | Critère observable de validation | Contrôles exigés dans cette tâche et preuve |
|---|---|---|---|
| 1 | Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées | Inventaire daté des exigences/scénarios et de l’existant ; écarts réels séparés des réalisations historiques et des inconnues. | Recouper les textes complets, leurs versions et preuves ; vérifier liens et absence de doublon, conserver la liste des écarts. |
| 2 | Tâche 1 techniquement validée avec ses propres preuves | Profil, rôles, cibles, ressources, capacités et dépendances obligatoires explicitement sélectionnés ; aucune absence convertie en réussite. | Vérifier manifests/profil et graphe déclaré contre les contrats ; documenter absence, incompatibilité et non-sélection avant effet. |
| 3 | Tâche 2 techniquement validée avec ses propres preuves | Contrats, propriétaires, choix et paramètres nécessaires à la prochaine réalisation arrêtés ; aucun arbitrage bloquant remplacé par une hypothèse. | Revue de conception et des cas nominaux/refus du profil ; validation documentaire requise et preuve des décisions avant code. |
| 4 | Tâche 3 techniquement validée avec ses propres preuves | Contrats et schémas versionnés du seul objet du lot vérifiables indépendamment de la réalisation suivante ; entrées, sorties, refus, limites et propriétaires explicites. | Si contrats documentaires : revue des invariants et structure ; si représentations exécutables : syntaxe et tests de types/versions/champs/bornes et refus sans effets. Aucun adapter futur ne remplace cette preuve. |
| 5 | Tâche 4 techniquement validée avec ses propres preuves | Chemin nominal du complément et branchement public observés ; refus indispensables de types, contexte, droits et dépendances déjà traités ; résultat réel distingué du reçu. | Exécuter syntaxe, unités et intégrations nécessaires au branchement nominal et à ses refus dans le périmètre du lot ; utiliser le propriétaire réel si persistance ou effet réel est requis. Les tests nécessaires de 7/8 sont effectués dès ici. |
| 6 | Tâche 5 techniquement validée avec ses propres preuves | Pannes, concurrence, limites et interruptions du complément traitées avec état inspectable, reprise et absence de double effet ou droit restauré. | Injecter panne, concurrence, expiration/révocation, réponse perdue et interruption/reprise selon les cas du profil ; vérifier état durable et ressources libérées lorsque requis, avant la tâche suivante. |
| 7 | Tâche 6 techniquement validée avec ses propres preuves | Résultats des contrôles exécutés dans les tâches 4–6 disponibles, cohérents avec les fichiers courants et exempts de donnée sensible. | Consolider commandes, résultats et versions déjà prouvés ; réexécuter seulement les contrôles invalidés par modification ou les compléments justifiés sur les fichiers finaux. |
| 8 | Tâche 7 techniquement validée avec ses propres preuves | Scénarios d’intégration/conformité du profil reliés à la dépendance et à l’artefact réels ; garanties et limites mesurées sans extrapolation. | Exécuter les cas du profil listés ci-dessus et les scénarios complets applicables ; comparer résultats, bornes et refus avec le canon. Les mocks ne qualifient pas une dépendance réelle ; rapporter non exécuté/échec séparément. |
| 9 | Tâche 8 techniquement validée avec ses propres preuves | Contenu et responsabilités exacts ; construction reproductible par cible ; aucune compilation assimilée à une recette fonctionnelle. | Revue croisée du résultat de référence ci-dessus, des scénarios et preuves actuelles ; réexécuter seulement les preuves invalidées, pas une recette déjà valide sans motif. |
| 10 | Tâche 9 techniquement validée avec ses propres preuves | Matrice de preuves reliée aux versions/artefacts et périmètre relu ; aucune opération finale sans son autorisation distincte. | Examiner fichiers et preuves, invariance des archives et périmètre ; appliquer les contrôles propres à l’opération finale seulement si elle est ensuite autorisée. |

Les vérifications utilisent les outils et versions du projet selon [AGENTS.md](../../../AGENTS.md) et [DEVOPS.md](../../../DEVOPS.md). Pour un changement Python, inclure la compilation syntaxique et les suites configurées ; pour une interface web, inclure tests et build frontend ainsi que Chromium et Firefox headless, et les contrôles visuels/manuels applicables. Les tests matériels, réseau, stockage, packaging et restauration exigent leur environnement autorisé. La syntaxe seule ne valide aucun comportement. Aucun de ces contrôles n’est exécuté par la présente préparation documentaire.

Pour chaque tâche, conserver identifiant, prérequis, fichiers, commandes, résultats natifs, critère/scénario, versions/artefact, limites et prochaine action ; cocher uniquement après validation technique. Un échec ou une preuve obligatoire indisponible interdit la tâche suivante. Une modification concurrente invalide seulement les preuves affectées et impose leur réconciliation avant reprise.

## Précisions du premier lot validé — 22 octobre 2026

Le développeur a validé D1–D3 dans [design.md](design.md) : CPython 3.14.9 avec GIL/Cython 3.3.0 comme chaîne candidate à qualifier ; distribution en répertoire avec exécutables/runtime/dépendances ; première cible Debian 13 x86_64 physique et VM. Cette reprise documentaire ne coche aucune des dix tâches et ne lance ni installation, ni construction, ni recette.

| Tâche existante | Précision des critères et preuves nécessaires |
| --- | --- |
| 1 | Recouper les six correspondances courantes et leurs scénarios/empreintes dans requirements.md, préserver les copies historiques et distinguer les preuves de source des preuves d’implémentation. |
| 2 | Distinguer la première cible physique/VM des autres profils non qualifiés ; vérifier les dépendances et l’applicabilité sans déclarer PA actif dans P0. |
| 3 | D1–D3 sont acquis et leurs qualifications restent ouvertes ; les noms des fichiers exécutables, l’arborescence relative et la sélection CLI font l’objet de la validation distincte D4–D6 ci-dessous. Les autres paramètres non arrêtés ne sont pas implicitement validés ; seuls les arbitrages encore nécessaires suivent TECHNICAL §45.4. |
| 4 | Déclarer la chaîne Python/Cython, runtime, dépendances et ABI avant sa qualification ; préserver trois binaires/six modes PA et PZT indépendant/pzt-daemon. Aucun choix supplémentaire ni ajout de dépendance par la seule documentation. |
| 8 | Relier les recettes applicables à leurs environnements physique et VM et à leurs artefacts/version exacts ; aucune compilation ne remplace la qualification des modes, responsabilités, refus ou reprises. |

Les autres critères, dépendances, contrôles par tâche et obligations ultérieures des plateformes restent inchangés. Les tests non exécutés et les environnements non qualifiés restent explicitement sans preuve.

## Critères Cython par campagne — décision du développeur du 26 octobre 2026

La [politique de conception](design.md#politique-cython-par-campagne--décision-du-développeur-du-26-octobre-2026) et le [delta normatif](specs/pixs-agent/spec.md) complètent les tâches existantes, sans nouvelle coche ni réécriture des preuves historiques.

Leurs six exigences et six scénarios sont synchronisés au canon pixs-agent
sur demande explicite du développeur le 26 octobre 2026, sans réapplication
des deltas déjà synchronisés. Les états des tâches restent inchangés ; cette
synchronisation documentaire ne qualifie pas la réalisation PA01.

| Tâches existantes | Critères et preuves nécessaires |
| --- | --- |
| 3–4 | Vérifier au début de la campagne la dernière stable Cython publiée et non retirée sur PyPI ; enregistrer date, source, version exacte, provenance et empreintes, puis verrouiller la chaîne. Une vérification impossible ou une incompatibilité reste bloquante, sans ancienne version choisie implicitement. |
| 5–7 | Lors d'un changement de version, aligner `pyproject.toml`, les métadonnées de chaîne, les contrôles PA01, les tests concernés et la documentation courante ; vérifier le refus d'une version différente du verrou et qualifier la nouvelle chaîne. Le constructeur compare désormais la version observée à `toolchain.cython` et trace les deux valeurs ; les sondes simulées ne qualifient aucune compilation native. |
| 8–10 | Relier les recettes et artefacts à la version exacte de leur campagne ; préserver ce verrou pendant la campagne et les reproductions. Réévaluer la dernière stable à la campagne suivante et conserver les anciennes preuves sous leur version d'origine. |

Cette inscription ne modifie ni CPython 3.14.9 avec GIL, ni le code, ni les preuves produit ; elle n'exécute aucune installation ou qualification native.

## Critères de l'enveloppe de campagne PA01 — complément du 26 octobre 2026

Le [contrat d'enveloppe](design.md#enveloppe-de-métadonnées-de-campagne-pa01--complément-du-26-octobre-2026)
et les quatre exigences ajoutées au delta pixs-agent complètent les tâches
existantes, sans nouvelle coche. Ce complément est synchronisé au canon sur
validation explicite du développeur le 26 octobre 2026, sans réapplication
des deltas déjà synchronisés ni modification du constructeur, du validateur
ou de `pyproject.toml`. Le verrou reste `toolchain.cython` du profil de build.

| Tâches existantes | Critères et recettes à réaliser |
| --- | --- |
| 3–4 | Définir et valider l'enveloppe fermée v1 sans modifier le profil de build fermé existant : nominal ; composant PBO refusé ; champs absents, inconnus, dupliqués ou mal typés ; verrou ouvert, préversion, développement, local ou non normalisé ; date invalide/sans UTC ; relevé absent, sortant, symbolique ou altéré ; preuve officielle ne démontrant pas la dernière stable ; distribution retirée, non déclarée ou altérée. |
| 5–7 | Réaliser le raccord entre verrou du profil, copie d'enveloppe, déclaration Cython exacte et sonde réellement utilisée avant compilation. Vérifier toute divergence, sortie inexploitable et stable observée plus récente ; conserver les codes de sonde/version existants et ajouter les deux refus d'enveloppe. Relier le rapport à `campaign_id`, `campaign_metadata_sha256`, `profile_sha256`, aux versions verrouillée/observée et aux distributions vérifiées. Aucun refus n'est suivi de compilation. |
| 8–10 | Qualifier le raccord sur les entrées et outils réels ; reproduire avec identité, verrou, date et preuves conservés, sans nouvelle sélection. Vérifier qu'une nouvelle campagne ne réécrit pas les preuves historiques. Séparer validation structurelle, sonde simulée, chaîne native, exécutables fonctionnels et recette intégrée obligatoire ; aucune fixture ne qualifie l'ensemble PA/PZT. |

## Préparation documentaire du raccord d'enveloppe — 26 octobre 2026

La clarification du développeur retient uniquement le contrat et les recettes,
sans production de code ni implémentation. Le [dossier préparatoire](RACCORD_ENVELOPPE_PA01.md)
raccorde les tâches 3–7 aux groupes V01–V08 et R01–R08, puis les tâches 8–10
aux groupes natifs N01–N03. Tous ces groupes restent NON EXÉCUTÉS.

Les futures réalisations doivent préserver le profil fermé et son verrou,
examiner les appels unitaires et natifs existants, puis fournir leurs preuves
propres. Cette inscription n'ajoute aucune coche, n'exécute aucun test produit
et ne modifie ni code, ni dépendance, ni canon, ni delta OpenSpec.

## Preuve officielle datée — préparation documentaire du 26 octobre 2026

La [procédure de preuve](PREUVE_SELECTION_PA01.md) complète le raccord et le
delta pixs-agent avec deux exigences et six scénarios, synchronisés au canon
sur validation explicite du développeur le 26 octobre 2026, sans réapplication
des autres deltas. Elle conserve le verrou, le profil et l'enveloppe fermés, les états des
tâches et les 19 groupes initiaux ; P01–P06 sont également NON EXÉCUTÉS.

| Tâches existantes | Critères de réalisation et preuves futures |
| --- | --- |
| 3–4 | Établir la collecte HTTPS officielle et UTC, la sélection de la dernière stable non retirée, le manifeste figé et la revue autorisée. Déclarer puis qualifier le registre, son lecteur de confiance, propriétaire et permissions ; aucun identifiant ou booléen du candidat ne crée l'autorité. Couvrir P01–P03. |
| 5–7 | Raccorder la lecture indépendante de l'admission et son état courant, vérifier identité et empreintes de toutes les entrées avant outils, puis tracer admission et manifeste dans le rapport. Refuser substitution, altération, retrait ou registre inaccessible avec les codes appropriés. Couvrir P02/P04/P05. |
| 8–10 | Vérifier conservation, restauration sans réactivation d'un retrait et reproduction sans nouvelle sélection ; relier les preuves réelles au dossier, à son admission et au rapport. Couvrir P06 et les limites de confiance déclarées, sans qualifier une collecte réelle par une fixture. |

Aucun code, stockage protégé, collecte, admission, test produit ou effet système
n'est réalisé par cette inscription documentaire ; aucune coche n'est ajoutée.

## Précisions du second lot validé — 22 octobre 2026

D4–D6 et leur inscription dans design.md/tasks.md sont explicitement validés par le développeur. Ils complètent D1–D3 sans les remplacer. Les dix cases de réalisation restent non cochées ; cette inscription documentaire n’exécute aucune installation, construction ou qualification.

| Décision | Critère à vérifier dans la tâche concernée |
| --- | --- |
| D4 — Fichiers exécutables | Dans les tâches 3/4, déclarer exactement `pixs-pa-system`, `pixs-pa-events`, `pixs-pa-session` et `pzt`, en conservant trois exécutables PA et PZT indépendant. Vérifier la correspondance des rôles avant toute réalisation. |
| D5 — Arborescence relative | Dans les tâches 4/5, décrire puis vérifier le contenu de `bin/`, `runtime/` et `lib/` selon design.md ; ne pas en déduire un chemin absolu d’installation système ni une plateforme supplémentaire. |
| D6 — CLI obligatoire | Dans les tâches 4/5, décrire puis tester `--mode` obligatoire : `system-daemon` pour pixs-pa-system ; `system-start`/`system-stop` pour pixs-pa-events ; `session-start`/`session-stop`/`session-daemon` pour pixs-pa-session ; `pzt-daemon` pour pzt. Vérifier les cas nominaux et le refus de l’absence, d’une valeur inconnue ou d’un mode d’un autre rôle avant de valider la tâche. |

La validation documentaire de ces correspondances ne coche pas la tâche 3 et ne reporte pas les tests nécessaires d’une tâche de réalisation vers les tâches 7/8. Les détails de chaîne, runtime, ABI et dépendances ainsi que les preuves physique/VM restent à qualifier dans le périmètre D1–D3. Les obligations de sécurité, mandats, catalogue fermé et autres critères existants sont conservés.

## Précisions du troisième lot validé — 23 octobre 2026

Le développeur a explicitement validé D7–D9 et leur inscription dans design.md/tasks.md. Ces précisions complètent les critères existants et ne cochent aucune tâche.

| Tâche existante | Précisions validées |
| --- | --- |
| 1–2 | Réconcilier les exigences courantes et distinguer contrats de gestion PBO, mécanismes de composition, chaîne minimale qualifiée et exécutants natifs encore absents. Ne pas transformer une preuve de présence en recette. |
| 3 | D7–D9 sont acquis ; D1–D6 sont conservés. Les qualifications encore manquantes restent à prouver avant réalisation. |
| 4 | Décrire le runtime/ABI/dépendances, l’initialisation isolée et le schéma fermé du profil de build distinct du manifest PBO, avec propriétaires et compatibilité des contrats. Soumettre le catalogue concret avant réalisation. |
| 5 | Réaliser seulement après validation de 1–4 ; vérifier dès cette tâche la fermeture des dépendances et l’exécution après déplacement du répertoire, l’absence de repli hôte et d’influence des chemins Python externes, les refus CLI et catalogue indispensables. |
| 6–9 | Conserver les contrôles de sécurité, erreurs, concurrence, reprise et recettes fonctionnelles ; mesurer taille et ressources du profil réel, sans seuil inventé ni assimilation de compilation à recette. Physique et VM conservent leurs preuves distinctes. |
| 10 | Relier les artefacts, versions, contrats, catalogue généré et preuves courantes ; conserver signature, provenance, SBOM, intégrité et publication selon les contrats existants. |

Les contrôles par tâche restent séquentiels et ne sont pas reportés à une tâche de tests ultérieure. Cette inscription documentaire n’autorise ni code, ni nouvel outil, ni installation ni archivage.

## Journal de validation élémentaire

### Tâche 1 — Audit courant validé le 23 octobre 2026

Inventaire et écarts conservés dans [VALIDATION.md](VALIDATION.md) : six correspondances canoniques et six scénarios, trois blocs liés de préparation/prébase/autorité, 31 sources fingerprintées, 15 sources Python analysées sans exécution et manifests de gestion Agent/PZT présents. L’ancienne absence des modules de gestion n’est pas reconduite ; leur présence ne prouve pas les exécutants natifs.

Le contrôle ciblé `req-2f7957a6c9e347e6a2bbd22ae1ce9b2a` a retourné 0. OpenSpec strict `req-acc32b6344814e0c805a7c47164e8c73` a retourné 0 ; 41 liens locaux et UTF-8/LF sans BOM contrôlés, rapport VM et six artefacts préservés. Validation technique CGPT consignée au checkpoint. Aucun code produit, test métier, recette physique ou qualification fonctionnelle n’est déduit de cet inventaire. Les neuf autres tâches restent non cochées.


## Catalogue initial — choix 1 validé le 23 octobre 2026

Le développeur a adopté le catalogue décrit dans design.md : `inspect_postgresql`, `prepare_postgresql` et `get_postgresql_result`, version `1.0.0`, sous gestion `pixs.agent`, uniquement en `system-daemon`. La préparation est Critique ; les lectures sont Protégé. Cette sélection complète D9 et autorise les contrats détaillés puis leur réalisation dans le périmètre du change.

Pour 3/4, lier chaque opération au propriétaire, au mode, au contrat de paramètres/résultats versionné, aux dépendances, à la configuration et aux permissions. Pour 5/6, conserver le mandat technique vérifié, le plan confirmé, la politique courante, la corrélation et l'idempotence, l'état durable et la réconciliation sans rejeu aveugle. Aucun shell/SQL arbitraire, migration ou mutation de table métier n'entre dans ce catalogue ; tous échanges PBO–PA restent via PZT.

Les contrats, code et tests sont préparés pendant la réalisation ; les contrôles différés et recettes sont exécutés puis validés en seconde phase selon l'instruction courante. Le choix ne prouve aucun exécutant ni transport, ne déclenche aucune installation PostgreSQL hôte et ne sélectionne pas implicitement identité/provider/privilège. Aucun test n'est déclaré réussi et aucune case supplémentaire n'est cochée par cette inscription.


## Quatrième lot adopté — D10–D12, journal technique PA

Réponses explicites du développeur le 23 octobre 2026 : NV_Extend SHA-256 et Cython/ESAPI ; provisionnement hors runtime, PLATFORMCREATE+POLICY_DELETE, maintenance matérielle P-256 distincte et séparation réelle des droits ; autorisation d'usage 256 bits par FD natif protégé et sessions HMAC-SHA-256 liées à l'index, sans mot de passe ni secret Python/journal/agents. D1–D9 et le catalogue non destructif restent conservés.

| Tâches existantes | Critères complémentaires, sans nouvelle coche |
| --- | --- |
| 2–3 | Inventorier la pile TSS et ses ABI/profils ; tracer D10–D12 adoptés, index/TPM explicites et séparation PA/PKI ; distinguer sources et matériel réellement autorisé. |
| 4 | Définir le schéma public d'ancrage, les transitions et le raccord natif avec leurs propriétaires, limites et refus ; un codec, FD ou rapport ne devient pas une autorité. |
| 5–6 | Réaliser lecture/extension autorisées et journal durable ; vérifier garde/remise réellement compétentes, origine native, identité de cible/index/installation, HMAC, état courant, fencing et quiescence ; aucun droit de provisionnement/suppression/Clear/hiérarchie dans PA, aucun rejeu d'extension incertaine. |
| 7–9 | Exécuter ensuite les tests structurels/natifs puis les recettes réelles autorisées : copie/restauration/clonage, panne/response perdue, concurrence, invalidation/retrait et rôle de maintenance ; prouver persistance et séparation réelles sur chaque plateforme sélectionnée, sans remplacer une recette par un mock. |
| 10 | Relier preuves, artefacts, limites et propriétaires exacts ; absence de preuve matérielle ou de propriétaire requis interdit l'achèvement. |

Le présent lot autorise conception/réalisation et sources de tests ; il n'autorise aucune installation, écriture NV, création/utilisation de clé ou modification de hiérarchie actuelle. La qualification exigera un plan matériel exact et distinct, coordonné avec Z12 pour les ressources partagées ; l'index/journal/secret PA ne reprend jamais ceux de PKI. Aucun laboratoire distinct n'est déduit du relevé du TPM de l'hôte Pixs courant.


## Point de réalisation source — consommateur NV, sans validation technique

Dans les tâches4–6, sont maintenant écrits : garde TCTI couplée au lecteur ESAPI, baux réels de journal/lecteur, vérification de toute l'histoire canonique et vrai append/fsync avant intention, consommation unique, nouveau lecteur HMAC et confirmation physique, consommateur NV_Extend opaque avec commit distinct et marquage avant tentative, conservation des inconnus et nettoyage connu avant effet. Le code ne réalise pas encore l'admission/propriétaires courants ni les handlers publics ; le nettoyage/reprise avec nouveaux contexte et autorité après effet incertain reste ouvert.

La composition C du lecteur/consommateur impose les cinq modules nv_secret, nv_anchor, nv_journal, postgresql_contracts et nv_intent, noms/headers explicites, réservés au graphe System pour les sources privées. Les chargeurs de recettes et leurs contrôles de rôle/dépendance sont adaptés. Le modèle ESAPI de TEST suit une valeur NV par contexte, un compteur d'applications et les pannes avant/après effet ; il ne qualifie pas HMAC ou le TPM.

Vingt-six méthodes de recette d'intention sont préparées, dont des scénarios isolés de réponse perdue, refus de rejeu, expiration, erreur RNG et durée de vie, et le drainage/Flush de nos seules ressources avant effet. Elles ne sont pas exécutées. Les neuf cases futures restent non cochées ; cette réalisation n'est ni compilation, ni syntaxe validée, ni réussite de test.

La preuve CT100 f95e57 confirme SSHroot/cismp/UID0 et lecture properties-fixed du TPM2 Intel via /dev/tpmrm0. Elle a été relayée et acquittée dans la session OpenCode existante sans rejeu. Elle ne qualifie pas les scénarios PA/PKI/PZT ou un effet NV/clé ; les tests produit restent en seconde phase et le plan d'effets sur le TPM physique partagé reste distinct.

Les dépendances C08/Z12 sont recoupées : aucun producteur positif C08 de projection/confirmation/mandat E4 signé avantPG, ni propriétaire D14/currentpolicy/UTC ou résolveur TLS/guardian Z12 complet n'est encore livré. Les contrats/DTO et primitives intermédiaires ne les remplacent pas. Le développeur a adopté distinctement le stockage PA par LoadCredentialEncrypted host+tpm2 avec garde/remise dans le lanceur System existant ; aucun cinquième exécutable/mode, secret partagé, repli logiciel ou PCR implicite. L'adoption couvre sources/docs/inventaire et qualification préparée, sans effet actuel sur secret/NV/hôte.


## D13 PA — critère complémentaire adopté pour la garde NV

D13 est validé humainement : stockage PA dédié LoadCredentialEncrypted host+tpm2, garde/remise dans le lanceur System existant, sans cinquième exécutable/mode ni mélange avec PKI/PBO. Pour4–6, réaliser le profil/source/propriétaire natif et le transfert FD avec vérifications courantes positives et refus fermés ; un adaptateur de forme du FD ne les remplace pas. Pour7–9, préparer puis qualifier facteurs réels, provenance, mémoire, rotation/révocation, arrêt et récupération. Aucun PCR/chemin/default de production, secret réel, effet NV ou changement hôte n'est introduit par cette adoption. Aucune case n'est cochée.


## Complément de réalisation source — prêt TLS et observation de reprise NV

Pour4–6, le port privé INITIAL_MATERIAL conserve le couple réel OSSL_LIB_CTX/SSL_CTX et sa référence forte, avec scope et retrait. Le client concret Z12 inclus et sa libération/transfert effectif restent à livrer avant raccord positif. Aucun getter produit public, capsule, clé ou transport n’est ajouté. Dix méthodes et leur conducteur de TEST sont écrits, sans exécution.

L’observation distincte start/step/snapshot/close dans nv_intent relit réellement NV par une nouvelle session HMAC, vérifie toute l’histoire canonique et publie seulement HEAD_MATCH/TAIL_UNANCHORED/DIVERGED après relectures du scope réel. Elle ne fait aucun append/Extend/rejeu et n’autorise ni reprise privilégiée, ni résultat SQL ou ancien contexte déclaré quiescent. Le scanner partagé conserve les refus du prepare existant. Douze méthodes supplémentaires portent test_nv_intent.py à38 méthodes préparées, non exécutées ; les preuves source et limites sont inscrites dans VALIDATION.md.

Les 41 sources suivies ont leurs empreintes rapprochées des écritures autorisées ; aucune syntaxe, compilation, test produit ou qualification n’est déduite. Les cases2–10 restent vides. Le raccord1.1 de production/retour du plan avant signature est porté par la question humaine commune de C08 et reste proposé. Les propriétaires D14/politique/UTC/garde PA, la reprise positive, les handlers et les entrées/lifecycles restent à compléter avant la seconde phase LXC.


## Dernier jalon de réalisation — D14, sans validation technique

Le collecteur SELF/PEER et le client de connexion D14 propre sont écrits dans systemd_observation.pyx, avec familles natives OBS/CONN, budgets/ownership, progression unitaire et refus. Les deux recettes sont fidèles et comportent31 méthodes préparées, non exécutées. Le relevé courant couvre44 sources18réalisation/26tests ; les empreintes et corrections de transcription sont dans VALIDATION.md. Aucune syntaxe, compilation, unité ou qualification produit n’est déclarée, aucune case n’est cochée.

Les primitives RPC readonly/unité proposées ensuite n’ont pas été écrites : leurs lots incomplets ont été refusés avant effet. Restent D14 manager/unité/MainPID/InvocationID, artefacts/politique/UTC/garde D13, client matière et transport PZT, handlers/résultats PostgreSQL, reprise positive et entrées/lifecycles complets. D13NV PA demeure adopté ; cela n’adopte pas D16 des secrets de clés Z12.

La reprise du chemin principal exige le contrat de transport de projection et retour observation/plan avant signature. La projection1.0 existante n’est pas niée ; les trois opérations fermées actuelles et leurs résultats ne fournissent pas ce port. Le lot PA/PZT1.1 est la proposition commune portée par CISMP1, dont la question humaine est déjà posée. Aucun quatrièmeopérateur, partagefichier, DryRunCritique ou adoption par silence n’est ajouté. Les tâches4–6 et le passage aux tests restent non achevés ; la seconde phase LXC suit la réalisation conforme et les décisions requises.


## E5 — Échanges techniques 1.1 et retour du plan avant confirmation

Le lot documentaire commun C08/PA01 a été validé humainement par la réponse
« Valider le lot documentaire commun » à
call_0ef16343f01847f698d3411cb89b5cd3/0. La transcription coordonnée couvre
treize documents C08 et les quatre documents PA01. Son écriture ne livre
aucun codec, handler, transport, autorité, effet PostgreSQL ou recette.

Les profils 1.0.0 existants MUST rester inchangés et explicitement distincts
du profil 1.1.0 ci-dessous. Une enveloppe 1.1 non liée ou invalide MUST NOT
être convertie ou acceptée en 1.0. Le catalogue logique conserve exactement
les trois noms, version 1.0.0 et classes déjà adoptées. TechnicalPlan 1.0.0,
ses octets canoniques et son digest propre MUST rester inchangés.

Pour les tâches 3–4, la décision humaine E5 est reçue ; vérifier la
transcription coordonnée des 17 fichiers et les champs fermés de contracts.md,
les deux profils 1.0/1.1 sans downgrade, la matrice d'invocations et les
propriétaires distincts. L'ancien blocage humain ne décrit plus l'état
actuel du lot documentaire. Les historiques datés restent conservés.

Pour 4–6, les codecs/résolveurs/transport/handlers et vrais propriétaires
courants restent à réaliser après reprise cohérente. Préparer les refus :
preuve absente/périmée, ID/invocation/target/binding divergents, UNOBSERVABLE
pris pour ABSENT, condition différée invalide ou supprimée, CREATE converti
en REUSE, garde ignorée sans effet, réponse perdue/downgrade et cycle de hash.
Ne pas transformer ces textes ou les 44 sources existantes en résultat livré.

Les tâches 7–9 seront exécutées et validées ensuite sur le LXC ; préparation
de recette n'est pas exécution. Task1 conserve sa seule coche historique ;
aucune case, archive, installation, code 1.1, effet PostgreSQL/clé/NV ou
preuve d'identité/fraîcheur n'est ajouté par cette transcription.


## D14 lookup — sources écrites, recettes préparées, sans validation technique

Écrits exacts RELEASED : `src/pixs/pa_native/systemd_observation.pyx` 2990f13493271c9e78301732978814fcb09b175b9a24a8663b2e6603f2db62fe prt_1706d563e001wzfYDDvEhGdWUg ; `tests/native/fixtures/systemd_observation_driver.c` be08c88696a5eac6cc5570491dff5fefd19c18c61bff86d63bd99ca07742908d prt_1706dc643001zphAqvkzDAjzrl ; `tests/native/test_systemd_observation.py` 0e497cd25b92b3c8e94f0d95439b31b82dc1ebefc2968a00b674f202dfaa5acf prt_1706e511d001kSO16rpUE4xvCn. 44 fichiers suivis sans dérive. 45 méthodes au total dans ce test, dont 14 nouvelles lookup, nominal inclus. Aucun test/syntaxe/compilation/import produit exécuté, aucun import produit, aucune exécution/réussite de ces recettes revendiquée, aucune coche/qualification.

Tâches 4-6 et 7-9 restent non achevées ; tests ensuite LXC, zéro nouvelle coche. Faits unité/InvocationID du contrat seuls, manager/MainPID/artefacts/politique/UTC/gardien D13/autorité toujours absents.


## Lot B — réalisation ouverte
Réalisation B ouverte dans tâches 4-6, dépendances à terminer après contrat B fermé. Tests 7-9 ensuite LXC, aucun test, coche ou qualification maintenant. Les raccords indépendants D14 déjà adoptés peuvent continuer sans attendre B.


## Retrait adopté — travaux à fermer avant code
- Fermer avec les propriétaires : ordre PA, D8, D6 et PZT, mapping PZT, contrôle admin distinct et inspection Protégée, preuve d'ancrage.
- Réaliser ensuite seulement : garde, quiescence, intention, ancrage, vérification positive, retrait irréversible, inspection et réconciliation du même intent.
- Refuser : préparation initiale après retrait, changement et migration d'époque et génération, second `Extend` automatique, gestion ordinaire avant preuves, `RETIRED` comme preuve.
- Ordre Z12 interne : `adopt_initial_trust` puis `ADOPTED_FENCED` avec commit et audit PG courants et admission PKI ordinaire fermée, puis `retire_initial_authority` avec tombstone ancrée vers `INITIAL_AUTHORITY_RETIRED`, puis vérification indépendante ordinaire vers `ORDINARY_READY`. D8 est RÉSOLVEUR TLS, pas adoption. Avant D6 : seuls usages INITIAUX explicitement mandatés sous fencing ; après D6 : seul le propriétaire ordinaire Django, A07 et A12 courant fournit le matériel. Même certificat ne vaut pas permission ordinaire. Aucun ordre total PA et PKI imposé : chaque étape et inspection prouve droits, matériaux et libctx courants ; préparer la continuation avant de fermer la voie ; aucune grâce, survie ou changement d'identité implicite. Preuves des DEUX retraits PA et Z12 avant management global.
- D14 MainPID : sources puis recettes à ÉCRIRE en réalisation, puis exécuter et valider en phase2 LXC ; ne jamais reporter l'écriture à la phase2 ni confondre candidats et tests réussis.


## D14 MainPID — sources écrites, recettes préparées, sans validation technique

Écrits exacts RELEASED le 25 octobre 2026, étape IMPLEMENTATION : `src/pixs/pa_native/systemd_observation.pyx` `5eab03f5db581f66814911f933458d14bba329d01119c5d5335781a147e1d787` req-34effb5ff9e2453f8ee08a884cf3c9a5 prt_174c9aa16001ZtiSNi4I5kW0Td ; `tests/native/fixtures/systemd_observation_driver.c` `b3c21cc93d0d0a35e43b12203934a5d82b9e2e69ac3330b61a482feb4fb9d562` req-3941e5af71d049e797a9f38fa92bcd41 prt_174d52c90001Go22aqfrJwftFr ; `tests/native/test_systemd_observation.py` `7511e5082aa32a3d5fb05e8fdaa6e3793efaa92064b86f5b9e96c7c9569edf14` req-e7ca6f0e4ed9476086c37f08e4181c81 prt_174e508dd0017FJKcldAis2c0j.

Total 46 sources suivies sans dérive, dont 19 réalisation / 27 tests ; contrôle de fidélité d'écriture seul, PAS syntaxe/compilation/import/test. Le test conserve 45 méthodes et ajoute 9 méthodes MainPID avec sous-cas : 5 RPC readonly, baux parents, correctif variant, historique d'ordre 1,2,2,1,3, enfant PID vivant/mort, erreurs SDK/types/temps/propriétaire, cleanup sans reset aveugle. Mocks sans qualification manager/identité/artefacts/politique/UTC/garde D13 ni effets SQL/NV. Raccords, handlers/transport/bootstrap B et lifecycle complets restent à finir ; codecs admin mandat/retrait/résultats écrits séparément sans autorité ni qualification. Reprise CAB 1.10.1 même SID/job/version 1200, prévol true exit 0 released. D18 décision humaine vérifiée dans le chat Z12, pas une source UTC extérieure qualifiée ; strict Z12 seulement annoncé par son RUN, sans disponibilité UTC/matière déduite. Seule coche historique 1 conservée, 2-10 vides ; phase 2 LXC après réalisation, archive non faite.


## Composition admin/import — sources et tests préparés, sans validation technique

Graphe codec admin optionnel mais fermé quand présent, PG canonique couvrant les rôles déclarés, garde avant outils, import package/builtin explicite sans repli, aucun System-only ajouté au codec, garde `_api.h` privée SysD du linker alignée. Sources/tests préparés ÉCRIT_NON_TESTÉ, pas de compilation/import positif/test/succès/qualification ; positif builtin réellement compilé en phase2 LXC. 7 nouvelles méthodes (generator 2, builder 2, import admin 3) ; linker étend une méthode existante. 46 fichiers (19 réalisation, 27 tests), aucune coche 2-10 ; D14 54 préparés inchangés. Reste bootstrap B, D14/artefacts/politique/UTC/garde D13, PZT, handlers/résultats/reprise, lifecycle. Contrats humains conservés, aucun nouveau choix/canon.


### 2026-10-25 — E5 Observation+graphe ÉCRIT_NON_TESTÉ
- Codec 12 champs/4 profils/5 ressources/UTC6 forme+octets ; ContentBinding
  PG réel, limites JSON/ref, UTF8 nonASCII accepté octets bornés, binding
  fixe 1.0.0 recontrôlé. 13 méthodes codec, aucun PASS.
- Graphe optionnel quand absent, fermé avec PG canonique unique couvrant
  rôles exécutables ; coexistence admin sans System-only ajouté. 4 méthodes graph.
- Lot 48 fichiers suivis SHA rapprochés (20 réalisation/28 tests), histoires
  datées conservées. Aucune syntaxe/import/compilation/test exécuté.
- Reste : PZT transport/handlers/temps/autorité/propriétaires/SQL/NV/lifecycle ;
  pas de coche 2–10 ni archive. Enveloppe E5 objets vs chaînes en coord C08.


### 2026-10-26 — E5 Préconditions + graphe de construction ÉCRIT_NON_TESTÉ
- Codec `src/pixs/pa_native/postgresql_preconditions.py` SHA `27d290b104f3f723a4f8f96fb38665a91d131b9da23b5c1b3040d7d3120a44fb` req `req-060d9c9760744b5f8fac963e5db914d3` preuve `prt_175b6fc65001MPtiBPyFu1O5sP` RELEASED.
- Recettes `tests/unit/test_pa_postgresql_preconditions.py` SHA `576350010b416d646fca110412b91657bed0e8d1c30f5061c9f55e45e53d01b1` req `req-1de0fd45d1eb4c96ac8af0291c13a55b` preuve `prt_175b8b3c1001vQ2fooBoGy4ALO`, 17 méthodes préparées.
- Contrat `E5-PRE` inclus dans `contracts.md` final SHA `4904de66f1d8f8e29e7ef6349b8ff247dad5c7c464507d1110aa56c11d2b4bbc` (étape `80b53ed5a86e2be38ff17e16642fd686487b6264bb6407e2bd01e1986f4af8aa` req `req-54cfc88cf8b14b5e9dcb942a9fca007c` preuve `prt_175bbf346001TdpjOdmmHKV2ey`), req final `req-5e4c3fd6dcf64283afc847e11bbc2fe0` preuve `prt_175c3a730001Q1ycD2fZ4evEP9`.
- Graphe de construction : `src/pixs/pa_native/generator.py` SHA `c66d621e15386525fc6e2e2a345f802e55eeba46d02d0a44afa386b0a02bd720` req `req-c0ebcaaeff15440988b281896c818e7f` preuve `prt_175c0c6080013cVuajCDmN9AkC` ; `src/pixs/pa_native/builder.py` SHA `bce843dec35f91b8c0b5afbccc4c9fcc032dbe9ed76b79d8fd9199f6214257eb` req `req-b7333b0938714bfe996da56d9b61c26c` preuve `prt_175c16d98001fV4oy1inyxF7xa`.
- Recettes graphe : `tests/unit/test_pa_native_generator.py` SHA `ce474712818fc278f9f688eea999b7832cbd4869a7c8acb8a0ddd88c281484a0` req `req-124d718c9c1945408b1af711111cdb2b` preuve `prt_175c22d300017p92byGX4Yviu5` ; `tests/unit/test_pa_native_builder.py` SHA `664864eb6224d8817965b8223b3adc86eef5060444e7659f9a865fb74c543a11` req `req-94493356c52d4ee881edde3f359a9830` preuve `prt_175c2c3a4001JDdgmMcC1HrBOb`.
- 23 nouvelles méthodes préparées (17 codec + 3 generator + 3 builder) : nominaux vide/ordre préservé/null étroit/digest, refus versions/guards/conditions/doublons/bornes/bool/null/JSON/nombres/seuils UTF8/limites, composition `PA01_PRECONDITIONS_COMPOSITION_INCOMPLETE`, module erroné, PG non couvrant, coexistence admin System + observation PZT + préconditions PZT sous PG union.
- 52 fichiers suivis dont 22 réalisation / 30 tests, histoires datées conservées. Aucun test/import/syntaxe/build/exécution produit. Reste administratif B/owners/transport/handlers/lifecycles ; pas de coche 2-10 ni archive ni qualification.


### Suivi tâches — lot documentaire adopté par le développeur le 26 octobre 2026

Seule la coche historique 1 est conservée, sans nouvelle coche de 2 à 10. Les formes sont adoptées par le développeur le 26 octobre 2026 pour le lot et l’option INIT A, sans travail de code achevé, sans réalisation ni qualification.

Sources suivies au nombre de cinquante-deux, dont vingt-deux de réalisation et trente de tests. Vingt-trois méthodes E5 préparées, soit dix-sept plus trois plus trois. aucun test, import, contrôle de syntaxe ou build produit exécuté dans cette phase, sans succès implicite de tout le code.

Étapes futures après validation : réaliser les codecs, le scanner, l’admission et le retrait, ainsi que les vrais producteurs et raccords D13, D14, temps, PZT, handlers, résultats et lifecycles ; ensuite campagne LXC autorisée, avec effets TPM réels seulement sur plan exact distinct. Rien n’est coché sur la base des textes. Aucun archivage éligible à ce stade.

## Annexe du 26 octobre 2026 — fondations B écrites, non testées

Le lot documentaire B/retrait + INIT A reste adopté sans modification ni revalidation. Progression de réalisation et préparation seulement, sans coche nouvelle : trois codecs publics écrits (Context8 43 méthodes, NV7 37, INIT12 33), trois gardes de composition ajoutées (Context8, NV7, INIT12) avec leurs appels dans les deux chemins (générateur et constructeur), et dix-huit méthodes de recette préparées non exécutées (9 générateur + 9 constructeur). État : 58 fichiers, 25 réalisation (23 src + 2 native), 33 tests, 131 méthodes préparées (43+37+33+18), aucune coche nouvelle ; seule la coche historique 1 subsiste, tâches 2 à 10 non cochées ; aucune syntaxe, import, compilation, unité ou qualification produit. Preuves exactes des dix fichiers : voir l'annexe VALIDATION.md du même jour.

Reste dû : Base8, Resource24, Policy14, PUB/FIN, recette et R0, provenance, scanner mixte, admission et retrait effectifs ; vrais producteurs et résolveurs D11/D13/D14/temps/PZT/handlers/résultats/lifecycles, puis campagne LXC et effets matériels sous plan exact distinct. Aucun port livré, admission, NV/SQL, installation, secret, Git ou archive.

## Nouveau cycle par lot — 26/10/2026

Rechargement CISMP `90a59d5c6468ba30e06fcfd010a91c263e9fbd3ce22e5dad74f86d563171a2f8` et ACSP `53e2a75c5f9032870bc813e55e07ba64a1fac85fab85b5b37622bb5f4f5f81de` relus. Consigne développeur « Appliquer le nouveau cycle par lot, avec tests ciblés avant toute nouvelle écriture Base8 » (`call_ccfc187ff27c48c0a618bae69e89fd1d/0`) : remplace le report antérieur des tests, historiques datés conservés.

Unités validées FORME PYTHON et composition de métadonnées seulement : Context8 43 OK ; graphe 63 OK après échec initial 62/63 corrigé par seule assertion (`^objet : source hors noyau natif autorisé$`, garde produit intacte, Popen non appelé) ; NV7 37 OK ; INIT12 33 OK. Total 176 tests distincts sur 5 modules, 4 commandes finales OK sans redoubler l'essai en échec ; syntaxe 10 fichiers OK ; venv Python 3.14.10 réel.

58 sources (25 réal/33 tests) ; aucune coche 2-10 ; Base8 non écrite, reprise après ces unités ; autres réalisations incomplètes. Détail preuves en VALIDATION.md, sans clore tâches 4-9. PAS Cython/link/import builtin positif, LXC/TPM/SQL/PZT, install, secret, Git, archive, qualification globale.

## Unité Base8 validée scope Python — 26/10/2026

Base8 validée FORME/COMPOSITION PYTHON seulement : 37 tests codec, 69 graphes, syntaxe 2+4 fichiers PASS, contrôle documentaire à réexécuter après ces annexes ; le précédent strict est une preuve antérieure, pas leur validation actuelle. Total courant 219 tests distincts sur 6 modules (43+37+33+37+69) en 5 commandes finales, sans additionner l'ancien graphe 63 ; 60 sources (26 réal/34 tests), aucune coche 2-10. Ordre par lot humain conservé ; reste Resource24/Policy14/PUBFIN/recette R0/provenance/scanner/admission/retrait/owners D11 D13 D14/temps PZT/handlers/résultats/lifecycles puis validations globales. Aucun port opérationnel livré.


## Annexe Resource24 validée scope Python — 26/10/2026

Resource24 validée FORME/COMPOSITION PYTHON seulement : source/recettes/composition Python validées Root ; syntaxe 2 fichiers PASS, 55 unités PASS, syntaxe 4 graphes PASS, 75 unités graphe PASS. Total courant 280 méthodes distinctes sur 7 modules en 6 commandes finales (43+37+33+37+55+75), 14 fichiers syntaxe, 62 fichiers (27 réal/35 tests), aucune coche 2-10. Rechargement CISMP 851 lignes SHA a2af8da0b88331d97501806515c3406b8515386b9db8a7b78d25788f7856441b et ACSP 663 lignes SHA 088cebc3bf3fdbc0c9f1bca41c144c7fc7628253f5a7e191389d40fe740f7a96, même RUN cismp7-pixs-023c11510a274b19 / SID ses_e8feae9d2ffewjQVKDYnpy3qLW. Dépendances de développement vs incidents techniques : poursuivre les unités indépendantes autorisées testables ; seulement à épuisement, clôturer ce RUN en BLOQUÉ delivered=false, change ouvert non archivé avec pour chaque tâche restante la dépendance manquante, le fait preuve, la phase bloquée et la condition exacte de reprise ; pas d'attente/surveillance/réessais automatiques des dépendances de développement, sans supprimer la récupération des incidents opérationnels CAB ; pas d'arrêt partagé/redémarrage OC/archive forcée. Ce jalon NE clôture pas le RUN : restent recettes de codecs préexistants et unités B fermées Policy14/PUBFIN/recette R0/provenance/scanner ; dépendances opérationnelles plus loin. Correction : l'ancienne formule « seule Resource24 indépendante » est abandonnée ; aucun épuisement actuel inféré.


## Annexe Policy14 validée scope Python — 26/10/2026

Policy14 validée FORME/COMPOSITION PYTHON seulement : source/recettes/composition Python validées Root ; syntaxe 2 PASS, 13 unités PASS, syntaxe 4 graphes PASS, 81 unités graphe PASS (37+44). Total courant 481 méthodes distinctes sur 19 modules en 17 commandes finales (475+6, graphe 81 remplace 75), 50 fichiers syntaxe, 64 fichiers (28 réal/36 tests), aucune coche 2-10. Rechargement CISMP 1080 et ACSP 880 en snapshot cohérent, même RUN cismp7-pixs-023c11510a274b19 / SID ses_e8feae9d2ffewjQVKDYnpy3qLW. Méthodes distinctes courantes, pas tous execs historiques. Reste PUB/FIN/recette R0/plan extérieur/provenance/scanner/admission/retrait et providers D11/D13/D14/temps/PZT/handlers/résultats/lifecycles puis validations globales. Dépendances vs incidents : poursuivre indépendants autorisés ; seulement à épuisement clôturer BLOQUÉ delivered=false avec BLOCKERS.md, change ouvert non archivé ; pas d'attente/surveillance/réessais automatiques des dépendances de développement, récupération incidents CAB conservée. Ce jalon NE clôture pas le RUN. Nettoyage BLOCKERS après archive+stats, puis commit GLOBAL Root seul à 3 clés filtrées et branche stable/quiescence ; aucun Git actuel ni par OC. LXC SSH confirmé, DEVOPS humain à jour ; conserver outils LXC, sudo pct non retenté ; sur ce lot aucune valeur d'accès LXC ni project.env lue, sans remettre en cause l'extraction filtrée d'identité initiale autorisée.

Détail preuves en [VALIDATION.md](VALIDATION.md), sans clore tâches 4-9.

## Sous-lots normalisés

Relevé complémentaire du 31 octobre 2026. Plan ACL-PIXS-2026-10-31-CHECK-R1, validé après rapport. PA01-SL01 à SL07 et leurs textes sont conservés intégralement avec leurs alias, dates, preuves, limites et états documentaires. SL07 reste une unité future distincte ; aucune recette 38/38 n’est annoncée par ce complément.

Les tâches 1, 2, 3, 8, 9 et 10 sont rattachées à SL08 à SL13. Les compléments résiduels des tâches 4 à 7 sont rattachés à SL14 à SL17, exclusivement hors des périmètres SL01 à SL07, qu’ils soient acquis ou encore à faire. Avant toute réalisation résiduelle, relier chaque obligation et scénario de la tâche source à l’un de ces périmètres, conserver les preuves valides et signaler les lacunes ; aucune nouvelle exigence, tâche ou duplication de recette n’est créée. La somme des unités partielles ne clôt pas une tâche globale incomplète.

Les critères et prérequis repris du tableau « Critères et contrôles par tâche future » se lisent avec le cycle par lot adopté le 26 octobre et les décisions versionnées courantes. Le sous-lot identifie l’unité, sans imposer son ordre par son numéro. Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE ; une qualification exige ses preuves datées et bornées. La normalisation ne requalifie ni ne retire aucun acquis.

Sources du complément : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md), [CADRAGE_FONCTIONNEL.md](CADRAGE_FONCTIONNEL.md) et [VALIDATION.md](VALIDATION.md), complétées par les décisions et détails déjà référencés au début de ce fichier. Les fichiers et versions de réalisation restent ceux des contrats effectivement sélectionnés, sans squelette de code produit ici.

### PA01-SL01 — Graphe Intent7 composition métadonnées seules (alias Intent7 graph)
- Tâches concernées : 4 (contrats/ABI fermés), 5 (réalisation complément ciblé), 6 (échecs/concurrence/limites), 7 (syntaxe/unités/négatifs) — cases inchangées, aucune coche ajoutée.
- Objectif/périmètre : garde optionnelle `_check_withdrawal_intent_composition` source OU module `withdrawal_intent`, identité canonique unique/ops vides, PG canonique unique couvrant seuls rôles utilisés, appels avant outils après Proofs18 ; 4 fichiers seuls : `src/pixs/pa_native/generator.py` 730l, `src/pixs/pa_native/builder.py` 603l, `tests/unit/test_pa_native_generator.py` 1570l, `tests/unit/test_pa_native_builder.py` 1129l ; codec `withdrawal_intent.py` 7 champs/54 PASS déjà clos, distinct de `nv_intent.pyx` natif.
- Dépendances/prérequis : codec Intent7 54 PASS forme seule 2026-10-30 ; graphe Proofs18 149 PASS 2026-10-30 ; PG `postgresql_contracts` seul import réel ; six effets natifs HELD/once/completed/libérés ; aucune autorité C08/4-rôles/System-only/nv_intent 5 modules imposée.
- Critères/contrôles : syntaxe 4 fichiers exit 0 le 2026-10-30 ; unité 156 PASS 0 fail/error/skip en 1.164s (74 générateur + 82 constructeur), 149 anciens + 7 nouveaux 4+3 datés 2026-10-30 ; cleanup 4 pyc exit 0 absences 4 vérifiées ; docs VALIDATION + Map ; strict ciblé APRÈS docs ; anciens tests/gardes conservés, `_checked_records`/`_sources` seuls appels ajoutés.
- État documentaire : VALIDÉ scope composition Python le 2026-10-30 — six effets code terminés/libérés, 156 PASS prouvés en 1.164s (74 générateur + 82 constructeur, 149 anciens + 7 nouveaux 4+3), syntaxe 4 exit 0, cleanup 4 vérifiés, docs VALIDATION/Map/tasks relus ; voir [VALIDATION.md § Graphe Intent7 156 PASS](VALIDATION.md) ; strict ciblé final exécuté exit 0, preuve `/home/devops/datas/cab/output/scm-discovery-ack/pa01-intent7-graph21121-final-strict-native-proof.json` référencée au checkpoint ; alias Intent7 graph explicite ; cases 4-7 inchangées, aucune tâche globale achevée.

### PA01-SL02 — Recette native nv_secret17 fixtures publiques seules (alias nv_secret17)
- Tâches concernées : 4 (contrats/ABI fermés), 5 (réalisation complément ciblé), 6 (échecs/concurrence/limites), 7 (syntaxe/unités/négatifs) — cases inchangées, aucune coche ajoutée.
- Objectif/périmètre : recette existante `tests/native/test_nv_secret.py` 17 méthodes sur `src/pixs/pa_native/nv_secret.pyx` ; D12 lecteur `pa01_nv_secret_read32` + adaptateur D13 `pa01_nv_credential_open32` formes seules, sans API Python/capsule ; `nv_secret.h` déclaré inventorié SHA/taille, `nv_secret_api.h`/capsules refusés, aucun C/header généré édité ; exclusivement fixtures publiques pipe/fichiers/FD, jamais credential actuel/TPM/service host ; ABI/symboles/FD publics seuls, sans confinement/protection vrai secret ni ABI binaire PA ; System-only restriction produit.
- Dépendances/prérequis : campagne `CPython 3.14.9 GIL activé (Py_GIL_DISABLED=0), shared 0 / Cython 3.3.0 / C11 cc Debian 14.2.0-19 / OpenSSL 3.5.7` observée LXC ; lease `tests-pa01-nvsecret17-9be92571d7704f07a76ec65435dfd5d0` acquise sur `lxc:hvp1/100`, réconciliée CAB 2.1.22/2.1.23, puis RELEASED fencing 12040 ; SL01 VALIDÉ conservé ; bibliothèques/binaires installés et rapports CAB conservés.
- Critères/contrôles : compilation `C11/OpenSSL3` exit 0 ; import `nv_secret` OK ; unité 17 PASS 0 fail/error/skip ; cleanup complet namespace neuf (copies sources/tests, C/h/o/so, rapports temporaires, `fd-*`, inventaire/pins) + vérification d'absence distincte ; bibliothèques/binaires installés conservés, rapports durables/checkpoint CAB conservés ; docs VALIDATION + Map ; strict ciblé APRÈS docs ; aucune qualification binaire PA/credential/autorité/HMAC/NV/SQL/PZT/produit.
- État documentaire : VALIDÉ scope 17 publics le 2026-10-30 — réalisation 17 PASS / restauration LXC+locale prouvées, strict final APRÈS docs exécuté exit 0 ; premier essai 16 OK/1 FAIL conservé, retest 17 PASS.

### PA01-SL03 — Inspection libpq11 sans connexion SQL (alias libpq11)
- Tâches concernées : 4 (contrats/ABI fermés), 5 (réalisation complément ciblé), 6 (échecs/concurrence/limites), 7 (syntaxe/unités/négatifs) — cases inchangées, aucune coche ajoutée.
- Objectif/périmètre : suite existante `tests/native/test_libpq_inspection.py` 11 méthodes sur `src/pixs/pa_native/libpq_inspection.pyx`, aucun appel connect ; source sans cdef public/api, aucun header C exporté attendu ; connexion/inspection lecture seule non réalisée ; vrais headers installés 17.11 PG_VERSION_NUM 170011 et libversion 170011 exigés, aucun faux header ; fixtures publiques/construction/validation/close/owner-thread/env PG* seuls (dont os.putenv), jamais SQL réel/service/DB/TPM/production ; pas de qualification connexion/SELECT/DDL/peer HBA/autorité/server 17.11/transport/PZT/binaire PA ; fixture expected 160015 non observée, ne qualifie pas server 17.11.
- Dépendances/prérequis : campagne `CPython 3.14.9 GIL activé (Py_GIL_DISABLED=0) shared 0 / Cython 3.3.0 / C11` ; inventaire LXC lecture seule sous nouvelle lease, namespace encore absent puis pins à préparation ; headers installés `libpq-fe.h`/`pg_config.h` distincts des produits locaux, conservés ; nouvelle lease `test-resources/acquire` inédite avant préparation, HELD avant commandes CAB distinctes ; SL01/SL02 VALIDÉ conservés ; si headers/lib absents version exacte, installation biblios/binaires autorisée par développeur et conservée, plan exact à examiner avant commande.
- Critères/contrôles : inventaire LXC séparé ; compilation/link réel module exit 0 ; import `libpq_inspection` OK ; unité 11 PASS 0 fail/error/skip sans connect ; produits attendus C/.o/.so + logs seuls, absence `libpq_inspection.h`/`_api.h`/capsules/export inattendu vérifiée ; cleanup complet namespace neuf + vérification absence distincte, headers installés conservés ; docs VALIDATION + Map ; strict ciblé APRÈS docs ; aucune qualification connexion/SQL réelle/autorité/HBA/transport/PZT/binaire PA/produit.
- État documentaire : VALIDÉ scope 11 publics sans connexion SQL le 2026-10-30 — premier 10/1 FAIL conservé log 6225 c9b215... (marqueur public réimprimé traceback 3.14, garde C correcte), retest 11/11 PASS 0.08838s log 4497 1fab618c..., cleanup LXC 17/11 exit 0 + verify OK, lease RELEASED12413 20:09:45.831Z, local 28 objets + VERIFY_OK ; strict ciblé APRÈS docs exécuté le 2026-10-30 `Change 'add-pa-native-build-and-component-composition' is valid` exit 0 ; preuves `pa01-libpq11-{compile,retest,cleanup,verify-cleanup,local-cleanup,local-verify}-native-proof.json` + `libpq11-test-release-result.json` + `pa01-libpq11-doc-strict-native-proof.json`.

### PA01-SL04 — Recette native nv_anchor34 ESAPI simulé seul (alias nv_anchor34)
- Tâches concernées : 4 (contrats/ABI fermés), 5 (réalisation complément ciblé), 6 (échecs/concurrence/limites), 7 (syntaxe/unités/négatifs) — cases inchangées, aucune coche ajoutée.
- Objectif et périmètre : 34 méthodes anchor et 26 méthodes tcti en deux essais séparés, quatre fichiers .pyx et postgresql_contracts.py soit cinq modules inchangés, ESAPI et TCTI simulés seuls, vrais en-têtes TSS version 4.1.3 paquet libtss2-dev 4.1.3-1.2, sans TPM, HMAC, SQL, admission, autorité, PZT, binaire PA ou produit. Correctif C fixture deux locales seul, 8 sources finales manifest 20f2c65f 261197o, premier échec CC 2499o conservé.
- Mesures : compilation 17 étapes exit 0, 5C 4H 6O 1SO f3f0fcd7 1059800o, 107 exports, 5 imports sans capsule. Premiers essais : anchor34 2 échecs et tcti26 3 échecs, 0 erreur et 0 saut. Correctifs des essais seuls : valeur publique standard TCTI, nettoyage start 9 puis Finish 0 avec erreur primaire 6 et compteurs de Flush 14 et 15. Nouveaux essais PASS séparés : anchor34 34/34 pid 1055 environ 0,32s, tcti26 26/26 pid 1089 environ 0,39s, même SO avant et après, aucune somme globale.
- Restitution : nettoyage Root1 36 fichiers et Root2 51 fichiers, vérification distincte des deux racines absentes avec 11 gardes, release bail 12645, local VERIFY_OK 34 fichiers 9 répertoires. Limites : pas de qualification HMAC, TPM, SQL, HBA, PZT, binaire PA ou produit, pas de free-threaded.
- État documentaire : VALIDÉ scope 34/26 le 2026-10-31 — recettes natives 34/34 et 26/26 PASS séparées et environnements restitués ; strict ciblé APRÈS ajouts docs exécuté le 2026-10-31 `Change 'add-pa-native-build-and-component-composition' is valid` exit 0, preuve `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvanchor34-doc-strict-native-proof.json`.

### PA01-SL05 — Prêt privé TLS INITIAL_MATERIAL, 10 recettes réelles (VALIDÉ scope 10)
- Tâches concernées : 4 (contrats/ABI fermés), 5 (réalisation complément ciblé), 6 (échecs/concurrence/limites), 7 (syntaxe/unités/négatifs) — cases inchangées, aucune coche ajoutée.
- Code produit inchangé : les 3 sources publiques totalisent 30968 octets, manifest `258d8430e92df1f6a68d79e073f266cc5c19c514d09a8116c1fc8bd2ca623a11` (`tls_context.pyx` 18685o `b7e23d60`, `tls_lease_driver.pyx` 2456o `7b7022c0`, `test_tls_lease.py` 9827o `c6d86218`), Root TLS dev 1792 ino 262790, campagne CPython 3.14.9 GIL activé shared0, Cython 3.3.0, cc C11 14.2.0, OpenSSL 3.5.7.
- Recettes réelles distinctes : 10/10, 0 échec, 0 erreur, 0 ignoré, durée 0.011263032 s, pid 1460, SO 186408o `5d6c3e39380ee98a91ebd29af933927acb960c00efe07c0c1eb3a693c3d21da8`. Première commande 7 étapes exit 1 conservé, sans blanchiment : la sonde inventait l'attribut `ready_for_transport`, la vraie API est `configuration()["ready_for_transport"]`. Import corrigé séparé exit 0 sans recompiler, 0.068126606 s, pid 1402, `ready_for_transport` False, fonctions privées absentes de la surface Python, capsule absente.
- Artefacts constatés sans recompilation : C 658583o, H 2534o, O 207736o, SO 186408o, 8 symboles `PyInit_tls_lease_driver`, drapeau Cython optionnel, `__wrap_clock_gettime`, `pa01_tls_test_clock/new/get/withdraw/close`, NEEDED `libssl.so.3, libcrypto.so.3, libc.so.6`, transitives `libz.so.1.3.1` et `libzstd.so.1.5.7` normalisées depuis `/lib` vers `/usr` et épinglées, 13 gardes initiales + 2 extra = 15 et 2 liens conservés. Les 4 artefacts et les 8 anciens journaux sont inchangés avant et après les dix essais. Premier journal durable `fea8ef9b34e3ddbe28709d2fcdb371cd7faa9130f52241fa63a0cbb945fd19fb` (1647o) conservé.
- Restitution : nettoyage LXC 16 fichiers 12 répertoires 1097797o digest `f0c5f814c3e8528bb09f91a271ebf694e983ee9df5b98e6fb93f948a86220377`, vérification distincte `verified_absent` pids [], 15 gardes et 2 liens, release lease 12874, nettoyage local 16 fichiers 2 répertoires 18 objets et parent propre absent, `VERIFY_OK` avec 3 sources intactes.
- Limites : horloge de test, couple OpenSSL réel et port privé de test seuls ; aucun PKI, clé, certificat, socket, client Z12, destruction ou transfert intégré, transport, PID interprocessus, autorité, SQL, TPM, PZT, binaire PA produit, livraison ou archive ne sont qualifiés. Les dix cas ne qualifient pas le D13 complet.
- État documentaire : VALIDÉ scope 10 le 2026-10-31 — recettes 10/10 et restitutions prouvées, strict ciblé APRÈS ajouts exécuté `Change 'add-pa-native-build-and-component-composition' is valid` exit 0, preuve `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlslease10-doc-strict-native-proof.json` ; SL01 à SL04 VALIDÉS et 1/10 PARTIELLEMENT RÉALISABLE conservés.

### PA01-SL06 — Contexte TLS13 E3 + primitive Ed25519 E4, 13/13 PASS
- Tâches concernées : 4 (contrats/ABI fermés), 5 (réalisation complément ciblé), 6 (échecs/concurrence/limites), 7 (syntaxe/unités/négatifs) — cases inchangées, aucune coche ajoutée.
- Code et périmètre : 2 sources totalisant 27285 octets (`src/pixs/pa_native/tls_context.pyx` 18685o `b7e23d60f9576d418f2c4b28b6298bcbd288c486e17b91f54cc4b0c5ab2a3933`, `tests/native/test_tls_context.py` 8600o `816b7611c5723dac26dfa04137013b9780d3f34b441060b1a4778ff88e8f567c`), manifest `695d7c94837bff35191a6f67ea4f68f59eebe2bd36f83f409c6d8a517d7057b7`, 13 méthodes AST (8 TLS + 5 Ed25519), campagne CPython 3.14.9 GIL activé shared0, Cython 3.3.0, cc C11 14.2.0, OpenSSL 3.5.7 ; sans PKI, clé privée, certificat, socket, handshake, transport, client Z12, autorité C08, SQL, TPM, PZT, binaire PA produit. Les 13 cas qualifient le contexte et la primitive Ed25519 seuls.
- Compilation 7 étapes exit 0 : C 638253o `38bbe7dd8dd7ed8fe30268a20c5149bcf44c70ed95c54dc35d1c811bead65569`, O 205368o `1bd0e3a50891028a8158e761d0843f21635ad01721ed6909a6b437c83c24a0dc`, SO 185824o `bfcb2cf8582995488eeef1e036dedd523d880d50fc4b38e5bf92defe07c8fe68`, 2 exports `PyInit_tls_context` et drapeau Cython optionnel, NEEDED `libssl.so.3, libcrypto.so.3, libc.so.6`, transitives `libz.so.1.3.1` et `libzstd.so.1.5.7` épinglées avant et après, import `configuration()["ready_for_transport"]` False, fonctions privées absentes de la surface Python, capsule absente, pid 1658.
- Recette 13/13 : 13 run, 0 échec, 0 erreur, 0 ignoré, durée 0.012543340009870008 s, pid 1690, SO inchangé `bfcb2cf8582995488eeef1e036dedd523d880d50fc4b38e5bf92defe07c8fe68`, journal 8002o `9c891f3602c03cf22a6ac6b3a65b130ade322a0a5991e21bcc8fb80cfd32eff6`.
- Restitution : nettoyage LXC 13 fichiers 12 répertoires 1069391o digest `9b071311e21ccaa9f617962ce8690a6b94b2ee6668504baaf7b5ad8bdf42acc3`, vérification distincte `verified_absent` pids [], 15 gardes et 2 liens conservés, release lease 13000 à 03:07:37.744Z, vérification locale `VERIFY_OK` namespace jamais créé et parent absent, 2 sources intactes. Preuves : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-inventory-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-copy-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-compile-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-unit-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-final-inventory-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-cleanup-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-verify-cleanup-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-local-verify-native-proof.json` et `/home/devops/datas/cab/output/scm-discovery-ack/tlscontext13-test-release-result.json`.
- État documentaire : faits SL06 13/13 consignés, revue et strict documentaire finaux tracés dans le checkpoint du RUN, aucun résultat futur affirmé ; SL01 à SL05 VALIDÉS conservés, dont SL03 libpq11, 1/10 PARTIELLEMENT RÉALISABLE non livré non archivé conservé, sans somme.

### PA01-SL07 — Reçu d'intention IO nv_intent, 38 recettes réelles (EN COURS)
- Tâches concernées : 4 (contrats/ABI fermés), 5 (réalisation complément ciblé), 6 (échecs/concurrence/limites), 7 (syntaxe/unités/négatifs) — cases inchangées, aucune coche ajoutée.
- Code et périmètre : 9 sources totalisant 262141 octets (`src/pixs/pa_native/nv_secret.pyx` 14723o `05bb3224`, `src/pixs/pa_native/nv_anchor.pyx` 70328o `c283e562`, `src/pixs/pa_native/nv_journal.pyx` 26409o `a97f9782`, `src/pixs/pa_native/postgresql_contracts.py` 39675o `137e6c11`, `src/pixs/pa_native/nv_intent.pyx` 33269o `11f062c3`, `tests/native/fixtures/nv_intent_driver.c` 1654o `49beb0b4`, `tests/native/fixtures/nv_public_driver.c` 23961o `bfb10819`, `tests/native/fixtures/nv_journal_driver.c` 3493o `44c48f87`, `tests/native/test_nv_intent.py` 48629o `f39a8a55`), 38 méthodes AST existantes, 5 modules `nv_secret/nv_anchor/nv_journal/postgresql_contracts/nv_intent` et driver C `nv_intent` incluant `nv_public_driver` + `nv_journal_driver` ; IO de fixtures publiques réelles, ESAPI/TCTI simulés seuls, wrappers `clock_gettime/write/fsync/close/RAND_bytes_ex/pa01_nv_secret_read32`, C11 + crypto + `-Bsymbolic-functions`, aucune `libtss2-esys`/TCTI réel à lier.
- Objectifs et critères : syntaxe Cython/C/link/import des 5 modules, `nm`/`NEEDED`, puis 38/38 réelles, 0 échec, 0 erreur et 0 saut ; epochs, contextes, intention, reçu, observation, cancel et cleanup selon contrats.
- Limites : aucun HMAC/TPM matériel, credential réel, source positive, SQL, autorité PZT ou produit qualifié.
- Dépendances et campagne : fresh lease LXC100 hvp1 avant inventaire ; deux répertoires neufs ; chaque opération CAB unitaire ; gardes campagne CPython 3.14.9 GIL activé shared0, Cython 3.3.0, cc 14.2.0, OpenSSL 3.5.7, TSS 4.1.3 ; sources de production inchangées au relevé actuel. Campagne native publique 38/38 PASS réalisée le 2026-11-01T12:38:47.234Z et consignée dans VALIDATION.md. Prochain build frais — inventaire, génération/compilation Cython/C, linkage/import des 5 modules, nm/NEEDED et ABI — à exécuter sous un nouveau bail LXC après adoption du plan. Copie 9 sources grosse : réutilise transport OC qualifié NVanchor34, ne pas mettre 262k dans un argv Linux max128k ; aucune augmentation limite CAB16384. Nettoyer seuls fichiers test propres, verify distincte, release, garder installs et preuves toutes périodes.
- État documentaire : EN COURS — campagne native publique 38/38 PASS le 2026-11-01T12:38:47.234Z (0 échec, 0 erreur, 0 saut ; exit 0), preuve détaillée dans VALIDATION.md ; build frais, ABI/link/import, nm/NEEDED non prouvés ; SL01 à SL06 VALIDÉS conservés, 1/10 inchangé. Pas d'implémentation programme avant plan adopté strict. Note à part pour global ultérieur : régressions constructeur10 (new GNU, 9 avant) et liaison5 (builder/generator ont changé depuis preuve 26oct), non mélangées aux 38 ni étendues à cet ajout.

### PA01-SL08 — Audit courant du périmètre

- Ancien repère et tâche rattachée : tâche 1 ; numéro, libellé et case source conservés ci-dessus.
- Objectif et périmètre : Auditer les blocs normatifs et renvois de requirements.md, l’implémentation actuelle et ses preuves ; décider du complément réellement manquant sans recréer l’existant.
- Composants visés : Composition/catalogue PA, exécutables PA et binaire PZT distinct, contrats/adapters et chaîne native du profil sélectionné ; fichiers effectifs selon design.md et la tâche source.
- Dépendances et prérequis sourcés : Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées
- Critères de validation sourcés : Inventaire daté des exigences/scénarios et de l’existant ; écarts réels séparés des réalisations historiques et des inconnues.
- Contrôles prévus sourcés : Recouper les textes complets, leurs versions et preuves ; vérifier liens et absence de doublon, conserver la liste des écarts.
- Limite de couverture : Les unités partielles des autres sous-lots ne remplacent pas la preuve propre de cette tâche.
- Preuves à recouper : tableau de critères et paragraphes propres à la tâche 1, [VALIDATION.md](VALIDATION.md) et décisions référencées par [design.md](design.md). Les recettes et intégrations du profil restent celles de requirements.md ; aucune disponibilité ni garantie produit n’est déduite d’une recette partielle.
- Case source observée le 31 octobre 2026 : cochée ; audit du 23 octobre 2026 conservé avec sa seule portée documentaire.
- État documentaire : NON VÉRIFIABLE pour une nouvelle qualification ; validation historique de l’audit conservée.

### PA01-SL09 — Sélection des capacités et profils

- Ancien repère et tâche rattachée : tâche 2 ; numéro, libellé et case source conservés ci-dessus.
- Objectif et périmètre : Confirmer la sélection de la capacité, les rôles/plateformes/ressources applicables et les dépendances obligatoires ; ne pas transformer une non-sélection en réussite de test.
- Composants visés : Composition/catalogue PA, exécutables PA et binaire PZT distinct, contrats/adapters et chaîne native du profil sélectionné ; fichiers effectifs selon design.md et la tâche source.
- Dépendances et prérequis sourcés : Tâche 1 techniquement validée avec ses propres preuves
- Critères de validation sourcés : Profil, rôles, cibles, ressources, capacités et dépendances obligatoires explicitement sélectionnés ; aucune absence convertie en réussite.
- Contrôles prévus sourcés : Vérifier manifests/profil et graphe déclaré contre les contrats ; documenter absence, incompatibilité et non-sélection avant effet.
- Limite de couverture : Les unités partielles des autres sous-lots ne remplacent pas la preuve propre de cette tâche.
- Preuves à recouper : tableau de critères et paragraphes propres à la tâche 2, [VALIDATION.md](VALIDATION.md) et décisions référencées par [design.md](design.md). Les recettes et intégrations du profil restent celles de requirements.md ; aucune disponibilité ni garantie produit n’est déduite d’une recette partielle.
- Case source observée le 31 octobre 2026 : non cochée ; aucun achèvement de la tâche globale déduit.
- État documentaire au 4 novembre 2026 : VALIDÉ pour la sélection documentaire D1–D9 et le choix catalogue 1, conformément à VALIDATION.md §PA01-SL09 et aux décisions de design.md ; validation OpenSpec stricte ciblée exit 0. Cette validation porte sur la sélection documentaire uniquement : elle ne qualifie ni runtime/ABI, ni physique/VM/Docker, ni recette ou effet PostgreSQL. La case de tâche globale demeure inchangée ; les formats détaillés B et leurs raccords restent NON ADOPTÉS.

### PA01-SL10 — Fermeture des barrières de conception

- Ancien repère et tâche rattachée : tâche 3 ; numéro, libellé et case source conservés ci-dessus.
- Objectif et périmètre : Lever les barrières de conception de design.md et faire valider les choix encore ouverts avant réalisation ; présenter tout delta normatif ou dépendance supplémentaire nécessaire.
- Composants visés : Composition/catalogue PA, exécutables PA et binaire PZT distinct, contrats/adapters et chaîne native du profil sélectionné ; fichiers effectifs selon design.md et la tâche source.
- Dépendances et prérequis sourcés : Tâche 2 techniquement validée avec ses propres preuves
- Critères de validation sourcés : Contrats, propriétaires, choix et paramètres nécessaires à la prochaine réalisation arrêtés ; aucun arbitrage bloquant remplacé par une hypothèse.
- Contrôles prévus sourcés : Revue de conception et des cas nominaux/refus du profil ; validation documentaire requise et preuve des décisions avant code.
- Limite de couverture : Les unités partielles des autres sous-lots ne remplacent pas la preuve propre de cette tâche.
- Preuves à recouper : tableau de critères et paragraphes propres à la tâche 3, [VALIDATION.md](VALIDATION.md) et décisions référencées par [design.md](design.md). Les recettes et intégrations du profil restent celles de requirements.md ; aucune disponibilité ni garantie produit n’est déduite d’une recette partielle.
- Case source observée le 31 octobre 2026 : non cochée ; aucun achèvement de la tâche globale déduit.
- État documentaire au 4 novembre 2026 : VALIDÉ pour le verrou de conception non-B nécessaire à SL14/T4 en rédaction conditionnelle. Revue des critères SL10 établie sur les choix développeur D1–D9, le catalogue 1 et SL09/T2 VALIDÉ (strict ciblé exit 0) ; la section historique des barrières reste une garde sur les preuves.
- Limites T4 : ABI/runtime/dépendances, versions/licences/empreintes, absence Python hôte, isolation/échec fermé, registre, schémas/raccord et qualifications distinctes physique/VM/Docker restent à produire ; Docker non qualifié, LXC non assimilé à Docker. Formats B, plan extérieur, INIT_A12, JournalTransition, séquences et retrait détaillé NON ADOPTÉS ; aucun code B, effet TPM/SQL, adoption C08/Z12 ni qualification n’est acquis. La tâche globale 3 reste non cochée hors périmètre non-B.

### PA01-SL11 — Intégrations et conformité du profil

- Ancien repère et tâche rattachée : tâche 8 ; numéro, libellé et case source conservés ci-dessus.
- Objectif et périmètre : Exécuter les intégrations/conformités du profil : Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée.
- Composants visés : Composition/catalogue PA, exécutables PA et binaire PZT distinct, contrats/adapters et chaîne native du profil sélectionné ; fichiers effectifs selon design.md et la tâche source.
- Dépendances et prérequis sourcés : Tâche 7 techniquement validée avec ses propres preuves
- Critères de validation sourcés : Scénarios d’intégration/conformité du profil reliés à la dépendance et à l’artefact réels ; garanties et limites mesurées sans extrapolation.
- Contrôles prévus sourcés : Exécuter les cas du profil listés ci-dessus et les scénarios complets applicables ; comparer résultats, bornes et refus avec le canon. Les mocks ne qualifient pas une dépendance réelle ; rapporter non exécuté/échec séparément.
- Limite de couverture : Les unités partielles des autres sous-lots ne remplacent pas la preuve propre de cette tâche.
- Preuves à recouper : tableau de critères et paragraphes propres à la tâche 8, [VALIDATION.md](VALIDATION.md) et décisions référencées par [design.md](design.md). Les recettes et intégrations du profil restent celles de requirements.md ; aucune disponibilité ni garantie produit n’est déduite d’une recette partielle.
- Case source observée le 31 octobre 2026 : non cochée ; aucun achèvement de la tâche globale déduit.
- État documentaire : À FAIRE pour le complément non prouvé ; état de réalisation réel à recouper avant reprise, sans nouvelle validation par ce relevé.

### PA01-SL12 — Vérification du résultat attendu

- Ancien repère et tâche rattachée : tâche 9 ; numéro, libellé et case source conservés ci-dessus.
- Objectif et périmètre : Vérifier la sortie attendue : Contenu et responsabilités exacts ; construction reproductible par cible ; aucune compilation assimilée à une recette fonctionnelle.
- Composants visés : Composition/catalogue PA, exécutables PA et binaire PZT distinct, contrats/adapters et chaîne native du profil sélectionné ; fichiers effectifs selon design.md et la tâche source.
- Dépendances et prérequis sourcés : Tâche 8 techniquement validée avec ses propres preuves
- Critères de validation sourcés : Contenu et responsabilités exacts ; construction reproductible par cible ; aucune compilation assimilée à une recette fonctionnelle.
- Contrôles prévus sourcés : Revue croisée du résultat de référence ci-dessus, des scénarios et preuves actuelles ; réexécuter seulement les preuves invalidées, pas une recette déjà valide sans motif.
- Limite de couverture : Les unités partielles des autres sous-lots ne remplacent pas la preuve propre de cette tâche.
- Preuves à recouper : tableau de critères et paragraphes propres à la tâche 9, [VALIDATION.md](VALIDATION.md) et décisions référencées par [design.md](design.md). Les recettes et intégrations du profil restent celles de requirements.md ; aucune disponibilité ni garantie produit n’est déduite d’une recette partielle.
- Case source observée le 31 octobre 2026 : non cochée ; aucun achèvement de la tâche globale déduit.
- État documentaire : À FAIRE pour le complément non prouvé ; état de réalisation réel à recouper avant reprise, sans nouvelle validation par ce relevé.

### PA01-SL13 — Traçabilité finale et opérations autorisées

- Ancien repère et tâche rattachée : tâche 10 ; numéro, libellé et case source conservés ci-dessus.
- Objectif et périmètre : Relier chaque scénario applicable aux preuves/version/artefact, examiner le diff et les limites ; Git, synchronisation, archive, installation et publication restent soumis à leur autorisation propre.
- Composants visés : Composition/catalogue PA, exécutables PA et binaire PZT distinct, contrats/adapters et chaîne native du profil sélectionné ; fichiers effectifs selon design.md et la tâche source.
- Dépendances et prérequis sourcés : Tâche 9 techniquement validée avec ses propres preuves
- Critères de validation sourcés : Matrice de preuves reliée aux versions/artefacts et périmètre relu ; aucune opération finale sans son autorisation distincte.
- Contrôles prévus sourcés : Examiner fichiers et preuves, invariance des archives et périmètre ; appliquer les contrôles propres à l’opération finale seulement si elle est ensuite autorisée.
- Limite de couverture : Les unités partielles des autres sous-lots ne remplacent pas la preuve propre de cette tâche.
- Preuves à recouper : tableau de critères et paragraphes propres à la tâche 10, [VALIDATION.md](VALIDATION.md) et décisions référencées par [design.md](design.md). Les recettes et intégrations du profil restent celles de requirements.md ; aucune disponibilité ni garantie produit n’est déduite d’une recette partielle.
- Case source observée le 31 octobre 2026 : non cochée ; aucun achèvement de la tâche globale déduit.
- État documentaire : À FAIRE pour le complément non prouvé ; état de réalisation réel à recouper avant reprise, sans nouvelle validation par ce relevé.

### PA01-SL14 — Contrats et adapters restant à qualifier

- Ancien repère et tâche rattachée : tâche 4 ; numéro, libellé et case source conservés ci-dessus.
- Objectif et périmètre : Partie restante de la tâche source, hors périmètres SL01 à SL07 : Définir les contrats, schémas, propriétaires et adapters du périmètre : Catalogue fermé au build, quatre exécutables, sept modes, Cython pour les trois binaires PA et pour PZT indépendant ; qualifier versions, ABI et runtime avant installation des outils.
- Composants visés : Composition/catalogue PA, exécutables PA et binaire PZT distinct, contrats/adapters et chaîne native du profil sélectionné ; fichiers effectifs selon design.md et la tâche source.
- Dépendances et prérequis sourcés : Tâche 3 techniquement validée avec ses propres preuves
- Critères de validation sourcés : Contrats et schémas versionnés du seul objet du lot vérifiables indépendamment de la réalisation suivante ; entrées, sorties, refus, limites et propriétaires explicites.
- Contrôles prévus sourcés : Si contrats documentaires : revue des invariants et structure ; si représentations exécutables : syntaxe et tests de types/versions/champs/bornes et refus sans effets. Aucun adapter futur ne remplace cette preuve.
- Limite de couverture : Chaque preuve des SL01 à SL07 est réutilisable seulement pour son périmètre et sa version. Les critères ci-dessous portent sur les obligations résiduelles non couvertes ; un manque de preuve n’est pas remplacé par une fixture ou une répétition d’un acquis.
- Preuves à recouper : tableau de critères et paragraphes propres à la tâche 4, [VALIDATION.md](VALIDATION.md) et décisions référencées par [design.md](design.md). Les recettes et intégrations du profil restent celles de requirements.md ; aucune disponibilité ni garantie produit n’est déduite d’une recette partielle.
- Case source observée le 31 octobre 2026 : non cochée ; aucun achèvement de la tâche globale déduit.
- État documentaire au 4 novembre 2026 : EN COURS. Le delta D9 Docker est aligné entre code et fixture ; tests ciblés 13/13 PASS, py_compile exit 0 et strict ciblé exit 0 (preuves dans VALIDATION.md §PA01-SL14). Contrats PostgreSQL non-B vérifiés : PostgresqlContractsTest seul (NativeRequest/NativeResult/TechnicalPlan), 12 tests PASS, 0 échec/erreur/saut, 0.004 s, exit 0 ; commande PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_native_postgresql_contracts.PostgresqlContractsTest -v ; requestId 0953067e-39b4-48e6-9841-9132ce3f72e3, accès RELEASED/COMPLETED fencing 14081 ; empreintes VALIDATION.md §PA01-SL14. ObservationTest seul (codec Observation PostgreSQL 1.0.0) exécuté : 12 tests PASS, 0 échec/erreur/saut, 0.006 s, exit 0 ; commande PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_postgresql_observation.ObservationTest -v ; requestId 4de29b67-1ba9-4419-a438-e63d2185063f, operationId op-cismp7-pa01-sl14-observation-test-9f382808-1d91-4860-9f17-60cbe6458973, accès RELEASED/COMPLETED fencing 14106 ; empreintes VALIDATION.md §PA01-SL14. PreconditionsFormTest seul (codec PostgreSQL E5-PRE 1.0.0) exécuté : 17 tests PASS, 0 échec/erreur/saut, 0.009 s, exit 0 ; commande PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_postgresql_preconditions.PreconditionsFormTest -v ; requestId 42931c78-6d7d-4639-a050-769d788864bf, operationId op-cismp7-pa01-sl14-preconditions-test-59c62df3-702d-47c5-b1ac-9d8510b44597, accès RELEASED/COMPLETED fencing 14126 ; empreintes VALIDATION.md §PA01-SL14. Strict VALIDATION.md après E5-PRE : exit 0, requestId 1e6fdd03-b692-490b-a535-2cfbf2f644dd, operationId op-cismp7-pa01-sl14-preconditions-strict-6f2085e3-2912-408a-a2d9-339eed56105a, accès RELEASED/COMPLETED fencing 14131. EffectsTest seul (codec PostgreSQL E5-EFF 1.0.0) exécuté : 10 tests PASS, 0 échec/erreur/saut, 0.002 s, exit 0 ; commande PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_postgresql_effects.EffectsTest -v ; requestId 84f19eed-2e22-4385-a69d-4af263da1f4a, operationId op-cismp7-pa01-sl14-effects-test-fa8dc8ab-8394-45ab-89e4-71305c8d5f2f, accès RELEASED/COMPLETED fencing 14143 ; empreintes VALIDATION.md §PA01-SL14. Strict VALIDATION.md après E5-EFF : exit 0, « Change add-pa-native-build-and-component-composition is valid » ; commande /home/devops/.local/npm/bin/openspec validate add-pa-native-build-and-component-composition --strict ; requestId 3901f055-0a0b-4d47-b120-5ad7cee9281f, operationId op-cismp7-pa01-sl14-effects-validation-strict-5b4b7008-d8ba-4135-9ca7-255609d43782, accès RELEASED/COMPLETED fencing 14148. InitialMandateContractsTest seul (mandat initial PostgreSQL E4 1.0.0, codec de forme/octets) exécuté : 10 tests PASS, 0 échec/erreur/saut, 0.008 s, exit 0 ; commande PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_native_postgresql_contracts.InitialMandateContractsTest -v ; requestId deb5ad0a-f3c0-407b-9d93-36eb2c9c6c75, operationId op-cismp7-pa01-sl14-initial-mandate-test-retry-50ee05c2-f408-4521-8350-e448130d2388, accès RELEASED/COMPLETED fencing 14160 ; empreintes VALIDATION.md §PA01-SL14. Strict VALIDATION.md après E4 : exit 0, « Change add-pa-native-build-and-component-composition is valid » ; commande /home/devops/.local/npm/bin/openspec validate add-pa-native-build-and-component-composition --strict ; requestId f2b80cf5-6f0a-4fda-bacb-642498b1c176, operationId op-cismp7-pa01-sl14-initial-mandate-validation-strict-c72e4b1a-0df2-4d09-8bff-b7494a8dd371, accès RELEASED/COMPLETED fencing 14165. AnchorSnapshotContractsTest seul (codec public synthétique D10–D12) exécuté : 10 tests PASS, 0 échec/erreur/saut, 0.003 s, exit 0 ; commande PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_native_postgresql_contracts.AnchorSnapshotContractsTest -v ; requestId 8bb49b24-3797-4d20-b313-713bec6e3e87, operationId op-cismp7-pa01-sl14-anchor-snapshot-test-aedb58cd-4b81-4fb0-93b4-9959381ecc76, accès RELEASED/COMPLETED fencing 14176 ; empreintes VALIDATION.md §PA01-SL14. Strict VALIDATION.md après AnchorSnapshot : exit 0, « Change add-pa-native-build-and-component-composition is valid » ; commande /home/devops/.local/npm/bin/openspec validate add-pa-native-build-and-component-composition --strict ; requestId 9f1a5177-1129-493a-915b-aeaefc904fe0, operationId op-cismp7-pa01-sl14-anchor-validation-strict-cf79bee3-b9f8-478b-a02e-ff8e756c1a6c, accès RELEASED/COMPLETED fencing 14181. Le test ne qualifie aucune vraie ancre, TPM/HMAC, autorité ni format B. Les tests JournalTransition restent non lancés. Le complément reste incomplet : schémas/adapters résiduels, ABI/runtime/dépendances et qualifications non établis. Aucun Docker ou runtime qualifiant, aucun code B/effet TPM/SQL/C08/Z12. La case globale de la tâche 4 reste non cochée.
- Preuve ciblée supplémentaire au 4 novembre 2026 : le test `PeerProfileTest` du profil PostgreSQL Unix/peer a passé 8/8 (0 échec, 0 erreur, 0 saut, 0.002 s, exit 0). Reçu CAB : requestId `fe6712ab-4f77-4cf9-8d3f-9e7062a4fc9b`, operationId `op-cismp7-pa01-sl14-peer-profile-test-ef2c9605-9be4-40b1-901d-7d541134dedd`, accès RELEASED/COMPLETED, fencing 14188 ; empreintes et limites dans `VALIDATION.md` §PA01-SL14. Cette preuve de parseur n’implique aucune connexion PostgreSQL, qualification Docker/runtime, TPM/SQL ou adoption ; T4 reste non cochée.

### PA01-SL15 — Réalisation et branchements restants

- Ancien repère et tâche rattachée : tâche 5 ; numéro, libellé et case source conservés ci-dessus.
- Objectif et périmètre : Partie restante de la tâche source, hors périmètres SL01 à SL07 : Réaliser le complément ciblé et son branchement aux dépendances, en conservant les structures déjà livrées.
- Composants visés : Composition/catalogue PA, exécutables PA et binaire PZT distinct, contrats/adapters et chaîne native du profil sélectionné ; fichiers effectifs selon design.md et la tâche source.
- Dépendances et prérequis sourcés : Tâche 4 techniquement validée avec ses propres preuves
- Critères de validation sourcés : Chemin nominal du complément et branchement public observés ; refus indispensables de types, contexte, droits et dépendances déjà traités ; résultat réel distingué du reçu.
- Contrôles prévus sourcés : Exécuter syntaxe, unités et intégrations nécessaires au branchement nominal et à ses refus dans le périmètre du lot ; utiliser le propriétaire réel si persistance ou effet réel est requis. Les tests nécessaires de 7/8 sont effectués dès ici.
- Limite de couverture : Chaque preuve des SL01 à SL07 est réutilisable seulement pour son périmètre et sa version. Les critères ci-dessous portent sur les obligations résiduelles non couvertes ; un manque de preuve n’est pas remplacé par une fixture ou une répétition d’un acquis.
- Preuves à recouper : tableau de critères et paragraphes propres à la tâche 5, [VALIDATION.md](VALIDATION.md) et décisions référencées par [design.md](design.md). Les recettes et intégrations du profil restent celles de requirements.md ; aucune disponibilité ni garantie produit n’est déduite d’une recette partielle.
- Case source observée le 31 octobre 2026 : non cochée ; aucun achèvement de la tâche globale déduit.
- État documentaire : À FAIRE pour le complément non prouvé ; état de réalisation réel à recouper avant reprise, sans nouvelle validation par ce relevé.

### PA01-SL16 — Robustesse et reprise restantes

- Ancien repère et tâche rattachée : tâche 6 ; numéro, libellé et case source conservés ci-dessus.
- Objectif et périmètre : Partie restante de la tâche source, hors périmètres SL01 à SL07 : Traiter les échecs, concurrence, limites et interruptions propres au lot ; états incertains explicités et reprise sous autorité/contexte courants.
- Composants visés : Composition/catalogue PA, exécutables PA et binaire PZT distinct, contrats/adapters et chaîne native du profil sélectionné ; fichiers effectifs selon design.md et la tâche source.
- Dépendances et prérequis sourcés : Tâche 5 techniquement validée avec ses propres preuves
- Critères de validation sourcés : Pannes, concurrence, limites et interruptions du complément traitées avec état inspectable, reprise et absence de double effet ou droit restauré.
- Contrôles prévus sourcés : Injecter panne, concurrence, expiration/révocation, réponse perdue et interruption/reprise selon les cas du profil ; vérifier état durable et ressources libérées lorsque requis, avant la tâche suivante.
- Limite de couverture : Chaque preuve des SL01 à SL07 est réutilisable seulement pour son périmètre et sa version. Les critères ci-dessous portent sur les obligations résiduelles non couvertes ; un manque de preuve n’est pas remplacé par une fixture ou une répétition d’un acquis.
- Preuves à recouper : tableau de critères et paragraphes propres à la tâche 6, [VALIDATION.md](VALIDATION.md) et décisions référencées par [design.md](design.md). Les recettes et intégrations du profil restent celles de requirements.md ; aucune disponibilité ni garantie produit n’est déduite d’une recette partielle.
- Case source observée le 31 octobre 2026 : non cochée ; aucun achèvement de la tâche globale déduit.
- État documentaire : À FAIRE pour le complément non prouvé ; état de réalisation réel à recouper avant reprise, sans nouvelle validation par ce relevé.

### PA01-SL17 — Consolidation des contrôles locaux restants

- Ancien repère et tâche rattachée : tâche 7 ; numéro, libellé et case source conservés ci-dessus.
- Objectif et périmètre : Partie restante de la tâche source, hors périmètres SL01 à SL07 : Exécuter syntaxe, contrôles configurés et unités/négatifs applicables, en rapportant les résultats natifs sans données sensibles.
- Composants visés : Composition/catalogue PA, exécutables PA et binaire PZT distinct, contrats/adapters et chaîne native du profil sélectionné ; fichiers effectifs selon design.md et la tâche source.
- Dépendances et prérequis sourcés : Tâche 6 techniquement validée avec ses propres preuves
- Critères de validation sourcés : Résultats des contrôles exécutés dans les tâches 4–6 disponibles, cohérents avec les fichiers courants et exempts de donnée sensible.
- Contrôles prévus sourcés : Consolider commandes, résultats et versions déjà prouvés ; réexécuter seulement les contrôles invalidés par modification ou les compléments justifiés sur les fichiers finaux.
- Limite de couverture : Chaque preuve des SL01 à SL07 est réutilisable seulement pour son périmètre et sa version. Les critères ci-dessous portent sur les obligations résiduelles non couvertes ; un manque de preuve n’est pas remplacé par une fixture ou une répétition d’un acquis.
- Preuves à recouper : tableau de critères et paragraphes propres à la tâche 7, [VALIDATION.md](VALIDATION.md) et décisions référencées par [design.md](design.md). Les recettes et intégrations du profil restent celles de requirements.md ; aucune disponibilité ni garantie produit n’est déduite d’une recette partielle.
- Case source observée le 31 octobre 2026 : non cochée ; aucun achèvement de la tâche globale déduit.
- État documentaire : À FAIRE pour le complément non prouvé ; état de réalisation réel à recouper avant reprise, sans nouvelle validation par ce relevé.


## Statut courant des décisions B et du retrait — directive développeur du 3 novembre 2026

Le principe B reste acquis. Les formats détaillés B et leur raccord au journal restent NON ADOPTÉS ; la présente directive supersède les mentions antérieures de ce fichier qui qualifiaient le lot ou ses formes d’adoptés. Le choix opérationnel INIT A acquis séparément demeure distinct : il n’adopte pas le format INIT_A12, le plan, le mapping du journal ni les séquences B.

Les principes de retrait déjà adoptés concernant le signataire, le domaine et le droit courant restent distincts des formats détaillés de retrait, qui restent proposés sans adoption. C08 a jugé la proposition recevable, sans l’adopter ; aucune adoption Z12 n’est déduite.

Les codecs et tests de forme historiques conservent leur portée limitée et ne constituent ni adoption des formats ni qualification runtime. Les cases des tâches restent inchangées : tâche 3 ouverte, aucune coche ou validation nouvelle portée par ce statut. Aucun code B ni effet TPM/SQL n’est autorisé.

## Statut des tâches après validation documentaire PA01 — 3 novembre 2026

Le développeur a validé le lot documentaire présenté le 3 novembre 2026. Les formats détaillés énumérés dans design.md, les séquences et le raccord au journal, ainsi que les formats de retrait correspondants sont adoptés documentairement par PA01 dans leur contenu existant ; cette décision supersède les mentions antérieures de non-adoption. Le format INIT_A12 est adopté au plan documentaire, séparément du choix opérationnel INIT A.

Cette adoption ne coche aucune tâche : les cases et preuves de réalisation restent inchangées, la tâche 3 demeure ouverte et aucune qualification runtime n’est déduite. La revue C08 reste sans adoption formelle par C08, aucune adoption Z12 n’est déduite et aucun code B ou effet TPM/SQL n’est autorisé.

## Statut courant des tâches — mise à jour de reprise du 4 novembre 2026

Conformément à la décision développeur courante du 4 novembre 2026, le principe B reste acquis. Les formats détaillés B, le raccord au journal, le plan extérieur, INIT_A12 et les séquences B restent NON ADOPTÉS ; le choix opérationnel INIT A demeure distinct et ne vaut pas adoption d’INIT_A12, du plan, du mapping journal ou des séquences B.

Les formats détaillés du retrait restent proposés sans adoption. L’avis C08 confirme la recevabilité de la proposition sans adoption formelle ; aucune adoption Z12 n’est déduite.

Cette directive courante supersède, sans l’effacer, l’affirmation antérieure d’adoption documentaire du lot et des formats cités dans l’historique de ce fichier ; cet historique est conservé pour la traçabilité. Les cases restent inchangées, aucune tâche n’est cochée et la tâche 3 reste ouverte. Aucun code B, effet TPM/SQL, qualification runtime/Docker, livraison ou activation ne découle de cette décision.

## D14 MainPID — phase 2 LXC : 54/54 recettes simulées réussies — 5 novembre 2026

Le premier passage a mis en évidence une valeur d’attendu erronée dans le sous-cas main0 : le code retourne le stade 10 pour le refus MainPID=0, alors que le test attendait 8. Seul l’attendu du test a été corrigé ; le code produit n’a pas changé. La campagne LXC suivante a exécuté 54 tests, 54 réussites, 0 échec, 0 erreur, 0 saut, exit 0. Le détail des appels, empreintes, versions et nettoyage figure dans VALIDATION.md à la section « PA01-SL14 — D14 MainPID : recettes exécutées sur LXC ».

La campagne de 54 recettes simulées porte sur le module compilé et le conducteur à SDK sd_bus simulé avec sockets/pidfds locaux. Elle ne qualifie aucun manager systemd réel, unité, identité forte, politique, UTC, garde D13, TPM/NV, SQL ou transport PZT. Les étapes D14 hors de ces recettes et la tâche globale 4 restent ouvertes ; aucune case ni livraison n’est déclarée.

### Recette live MainPID réelle — 5 novembre 2026

Une recette réelle unique SystemdManagerLiveMainPIDTest.test_live_transient_mainpid_self_and_invocation_id a réussi sur CT100/hvp1 dans l’unité pixs-pa01-d14-mainpid-9ab1fd14-33.service (bus /run/systemd/private, CPython 3.14.9 avec -I -B, systemd-run --wait --collect --pipe, RuntimeMaxSec=60s). Résultat : 1 test, 0 échec, 0 erreur, 0 saut, code 0 ; systemd SUCCESS, MainProcess exit 0, runtime 217 ms. Source tests/native/test_systemd_observation.py ; readelf -d a rapporté les dépendances directes libsystemd.so.0 et libc.so.6. Limites : cette seule recette ne qualifie pas identité forte, politique, cycle UTC, D13, TPM/NV, SQL, Docker, C08/Z12, formats B, JournalTransition, livraison ou activation. La tâche globale 4 reste non cochée.

### Inventaire runtime libsystemd0 — 6 novembre 2026

Le contrôle en lecture seule `dpkg-query -W -f='${Package} ${Version} ${Status}\n' libsystemd0` via SSH (`StrictHostKeyChecking=yes`) sur CT100/hvp1 a renvoyé `libsystemd0 257.13-1~deb13u1 install ok installed` (SSH exit 0, commande native exit 0). Stage `stage-cismp7-pa01-libsystemd-c3c768192a8f46c8` : 3352 octets, SHA-256 `4ba3fbd4d4a73078f6edfe1ffdd138032dd22e56cbd5ef0f6c898583a7cc05c4` ; request `req-cismp7-pa01-libsystemd-c3c768192a8f46c8`, operation `op-cismp7-pa01-libsystemd-c3c768192a8f46c8`, call `call_01a1ae1e4f88771f927f4cca25164e12`, permission `per_1ae1e56ad001Ckijz0ctYe9xtz`, `onceAcknowledged=true`, résultat `COMPLETED/exit 0`, accès `RELEASED fencing 14602`. Bail de test LXC conservé `HELD fencing 13953`. `libsystemd0` est distinct de `libsystemd-dev` ; ce constat n’établit ni ABI, ni linkage, ni runtime complet. Tâche 4 non cochée.

### Test ciblé du codec JournalTransition — 6 novembre 2026

La classe `JournalContractTest` de `tests/unit/test_pa_native_journal_contracts.py` a passé seule : 24 tests, 24 réussites, 0 échec, 0 erreur, 0 saut, 0.006 s, exit 0. Commande : `PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_native_journal_contracts.JournalContractTest -v`. Sources relues : `tests/unit/test_pa_native_journal_contracts.py` SHA-256 `f0d506b563ed4bd503685947b6fd015a484804835993da6c8795371dd22c82bf` et `src/pixs/pa_native/postgresql_contracts.py` SHA-256 `137e6c110659a3fc1d85a72f499777bab2a15003fe06218552d0f54acae307fd`. Reçu CAB : request `req-cismp7-pa01-sl14-journal-test-ca86596730e44128`, operation `op-cismp7-pa01-sl14-journal-test-ca86596730e44128`, call `call_01a1ae42514e76d693fdef233c6d1e00`, permission `per_1ae42547e001fq64CeKrgvyPIV`, once acquittée, operation `COMPLETED/exit 0`, access `RELEASED/COMPLETED fencing 14622`. Test de codec synthétique en mémoire seulement ; aucune connexion/requête PostgreSQL, aucun effet SQL, TPM/NV ou runtime. Aucune nouvelle coche ; tâche globale 4 reste non cochée.

### Recettes live D14 positives et refus MainPID=0 — 6 novembre 2026

Le test positif SystemdManagerLiveMainPIDTest.test_live_transient_mainpid_self_and_invocation_id a passé 1/1 sur CT100/hvp1 en transient Type=exec. Le test live MainPID nul SystemdManagerLiveMainPIDTest.test_live_mainpid_zero_refused_state a passé 1/1 sous Type=forking/GuessMainPID=no, avec le processus de test enfant dans le même cgroup. Il vérifie le refus rc4/stage10/errno.ESRCH/cleanup0, la fermeture avec le même diagnostic et l’absence de snapshot après le refus. Les deux résultats, reçus CAB, empreintes, préparation CPython 3.14.9 et limites sont détaillés dans VALIDATION.md, section « Recettes live D14 MainPID positive et refus MainPID=0 ».

Aucune case de tâche n’a changé : la tâche globale 4 reste non cochée et PA01 reste à 2/10. Ces recettes ciblées ne terminent pas le manager D14 ni les raccords et qualifications restants ; aucun code B, effet TPM/SQL, livraison ou activation n’est déduit.

6 novembre 2026 : NativeLinkerRefusalTest 21 tests, 21 PASS, 0 échec, 0 erreur, 0 saut, 0.409 s, exit 0 ; fixtures synthétiques/mocks, aucun sous-processus ni liaison réelle ; voir VALIDATION.md. Aucune coche et aucun avancement PA01 ne changent.

6 novembre 2026 : inventaire LXC de libsystemd-dev sur CT100/hvp1 : `/usr/bin/dpkg-query -W -f='${Package} ${Version} ${Status}' libsystemd-dev` a retourné `libsystemd-dev 257.13-1~deb13u1 install ok installed`, exit 0 (SSH et distant) ; request `req-cismp7-pa01-sl14-lxc-libsystemd-dev-inventory-20261106-02`, operation `op-cismp7-pa01-sl14-lxc-libsystemd-dev-inventory-20261106-02`, call `call_01a1afc6f87175bab2d208b4757b026a`, permission `per_1afc6fc05001bsIobOARoILeU2`, once acquittée, accès `RELEASED/COMPLETED fencing14711` ; helper temporaire supprimé, absence vérifiée. Limites : inventaire dpkg seulement, sans inspection d’en-têtes, compilation, lien, ABI, runtime ou qualification produit ; voir VALIDATION.md. Aucune coche ; tâche 4 ouverte, PA01 2/10.

6 novembre 2026, PA01-SL14 : l’inventaire distant en lecture seule de libsystemd-dev sur CT100/hvp1 a réussi (SSH et helper exit 0). Observés : architecture x86_64 ; sd-bus.h 30 597 octets, sd-id128.h 8 657 octets ; libsystemd.pc 560 octets ; pkg-config version 257, libdir /usr/lib/x86_64-linux-gnu, libs -lsystemd ; libsystemd.so.0 -> libsystemd.so.0.40.0, SONAME libsystemd.so.0 et DT_NEEDED directs relevés. Reçu CAB : req-cismp7-pa01-sl14-lxc-systemd-dev-files-20261106-03 / op-cismp7-pa01-sl14-lxc-systemd-dev-files-20261106-03 / call call_01a1b0b54d92729e8a7068e06258e662, once acquittée, accès RELEASED/COMPLETED fencing 14761. Le helper corrigé a passé py_compile exit 0 ; cache et helper temporaires supprimés, absence vérifiée. Aucun fichier distant ni paquet n’a été modifié. Limites : pas de compilation/liaison réelle, contrôle du linker dev libsystemd.so, ABI ou runtime complet ; tâche 4 reste ouverte, aucune coche nouvelle, PA01 2/10 ; bail LXC reste HELD fencing 13953.

6 novembre 2026, PA01-SL14 : revue PyPI du verrou Cython. La campagne a commencé le 22 octobre ; PyPI date Cython 3.3.0 du 22 août et 3.3.1 du 1er novembre, ce qui permet d’inférer que 3.3.0 était la dernière stable au démarrage (revue rétrospective, sans instantané archivé au 22/10). 3.3.0 reste le verrou D1 de la campagne en cours ; la 3.3.1 publiée ensuite sera réévaluée à la prochaine campagne. Hashes et provenance PyPI consignés dans VALIDATION.md ; aucun téléchargement, installation, changement de version ou coche. Tâche 4 reste ouverte, PA01 2/10. Test unitaire ciblé du constructeur PA01 exécuté le 6 novembre : `PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_native_builder -v` a donné `Ran 82 tests in 0.663s OK`, exit 0 ; reçu CAB `req-cismp7-pa01-sl14-builder-unit-rev-20261106-02` / `op-cismp7-pa01-sl14-builder-unit-rev-20261106-02`, once acquittée, accès RELEASED fencing 14830. Le répertoire de fixtures est vide après exécution. Cette suite unitaire ne prouve pas la génération Cython, la compilation/liaison réelle, l’ABI ni le runtime ; la tâche 4 reste ouverte.