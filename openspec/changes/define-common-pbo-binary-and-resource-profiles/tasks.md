# Tâches — binaire PBO commun et ressources

## 1. Formalisation documentaire

- [x] 1.1 Relire cadrages, canon, séparation PA/PZT et baseline OpenSpec strict.
- [x] 1.2 Aligner les cadrages, README et schémas sur le binaire commun et les plans de ressources.
- [x] 1.3 Synchroniser les sept capacités canoniques et produire les deltas de traçabilité.
- [x] 1.4 Vérifier cohérence, compteurs, liens, UTF-8/LF, schémas et strict global incluant les capacités ciblées ; consigner les résultats.

- [x] 1.5 Intégrer Nuitka standalone pour PBO, distinguer les deux modes d'exploitation et Cython ciblé dans PBO des chaînes Cython PA/PZT ; vérifier canon, deltas, compteurs et contrôles documentaires.
- [x] 1.6 Vérifier la cohérence finale : nommer les modes Standalone/ZT, distinguer autonomie de gouvernance et activation PZT, ajouter le scénario Standalone avec PA, harmoniser les schémas et contrôler canon/deltas et strict global.

## 2. Réalisation future — non engagée

- [ ] 2.1 Sélectionner et tracer la dernière stable Nuitka publiée et non retirée sur PyPI au début de chaque campagne PBO, verrouiller sa version exacte, aligner déclarations et contrôles puis qualifier la chaîne standalone, ses versions/options, dépendances et ressources, chargement des extensions, noms/CLI, schémas et valeurs des profils ; distinguer exploitation Standalone/ZT sans nouvelle dépendance implicite.
- [ ] 2.2 Réaliser le binaire PBO et ses rôles/processus configurables avec les propriétaires existants et la persistance de référence.
- [ ] 2.3 Réaliser plans et suivi de ressources PA/PZT avec sessions, idempotence, propriétaire réseau et garanties de sécurité conservés.
- [ ] 2.4 Adapter et qualifier superviseurs, paquets et image, limites effectives et états demandé/appliqué sans élargissement des privilèges.
- [ ] 2.5 Qualifier mémoire, CPU, latence, débit, saturation, reconfiguration, révocation et reprise par cible ; n'admettre Cython dans PBO que pour des optimisations ciblées mesurées, avec non-régression ; conserver les preuves avant publication.

## Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026

Les identifiants et cases ci-dessus sont conservés. Ce contrat précise les critères et contrôles à réaliser **dans chaque tâche**, avant de commencer la suivante. Les tâches de test ou de preuve placées plus loin consolident la couverture et ne reportent jamais les vérifications nécessaires à une tâche antérieure. Une tâche de réalisation comprend donc ses unités, refus et intégrations indispensables dès sa propre exécution ; elle ne peut être validée en attendant qu’une tâche suivante la rende testable.

Les tâches cochées conservent leur statut historique ; leurs preuves doivent être recoupées avant réutilisation si les sources ont changé. Pour les tâches futures, les prérequis externes sont ceux de design.md et des exigences applicables ; un propriétaire, provider, exécutant, contrat adopté ou environnement requis manquant bloque la tâche concernée. La préparation du dossier ne les déclare pas livrés. Les choix ouverts restent à décider avant leur réalisation ; les deltas déjà synchronisés ne sont pas réappliqués. Les six exigences du complément Nuitka par campagne du 26 octobre 2026 sont synchronisées au canon sur validation explicite du développeur, sans nouvelle coche produit.

### Périmètre et cas de contrôle propres au lot

- Objet : Périmètre des tâches ci-dessus, sous les contrats publics et propriétaires de design.md.
- Résultat de référence : Les sorties et refus attendus des scénarios applicables au périmètre de cette tâche sont observés ; aucun niveau de garantie ni support non exécuté n’est annoncé.
- Cas de contrôle du profil : Qualifier la chaîne Nuitka standalone PBO, ses versions/options, dépendances et ressources, chargement des extensions, noms/CLI, schémas et valeurs des profils ; distinguer exploitation Standalone/ZT sans nouvelle dépendance implicite. ; Qualifier mémoire, CPU, latence, débit, saturation, reconfiguration, révocation et reprise par cible ; n'admettre Cython dans PBO que pour des optimisations ciblées mesurées, avec non-régression ; conserver les preuves avant publication.

Chaque contrôle est relié au texte complet de l’exigence et à son scénario, dans requirements.md lorsqu’il existe, sinon dans les deltas et le canon référencés par la proposition. Une simple égalité de titre ne prouve pas la couverture. Les cas conditionnels sont appliqués selon le rôle effectivement sélectionné ; une non-applicabilité est motivée sans remplacer une preuve obligatoire. Aucun paramètre numérique ou provider nouveau n’est déduit de ce contrat.

### Critères et contrôles par tâche future

| Tâche existante | Prérequis immédiat | Critère observable de validation | Contrôles exigés dans cette tâche et preuve |
|---|---|---|---|
| 2.1 | Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |
| 2.2 | Tâche 2.1 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.3 | Tâche 2.2 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.4 | Tâche 2.3 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.5 | Tâche 2.4 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |

Les vérifications utilisent les outils et versions du projet selon [AGENTS.md](../../../AGENTS.md) et [DEVOPS.md](../../../DEVOPS.md). Pour un changement Python, inclure la compilation syntaxique et les suites configurées ; pour une interface web, inclure tests et build frontend ainsi que Chromium et Firefox headless, et les contrôles visuels/manuels applicables. Les tests matériels, réseau, stockage, packaging et restauration exigent leur environnement autorisé. La syntaxe seule ne valide aucun comportement. Aucun de ces contrôles n’est exécuté par la présente préparation documentaire.

Pour chaque tâche, conserver identifiant, prérequis, fichiers, commandes, résultats natifs, critère/scénario, versions/artefact, limites et prochaine action ; cocher uniquement après validation technique. Un échec ou une preuve obligatoire indisponible interdit la tâche suivante. Une modification concurrente invalide seulement les preuves affectées et impose leur réconciliation avant reprise.

## Critères Nuitka par campagne — décision du développeur du 26 octobre 2026

La [politique de conception](design.md#politique-nuitka-par-campagne--décision-du-développeur-du-26-octobre-2026)
et les six exigences ajoutées au [delta reference-runtime](specs/reference-runtime/spec.md)
complètent les tâches existantes, sans nouvelle coche ni réécriture des preuves
historiques. Les tâches de réalisation 2.1 à 2.5 restent non engagées ; ce
complément documentaire est synchronisé au canon sur validation explicite du
développeur le 26 octobre 2026, sans réapplication des deltas antérieurs.

| Tâche existante | Critères complémentaires |
|---|---|
| 2.1 | Vérifier la dernière stable Nuitka publiée et non retirée sur PyPI au début de la campagne ; exclure préversions et développement ; enregistrer date, source, version exacte, provenance et empreintes. Verrouiller la version et aligner `pyproject.toml`, métadonnées, contrôles de construction, tests concernés et documentation, puis qualifier Python, Django, dépendances, compilateur C, ABI, cibles, options standalone, rôles et ressources embarquées. Une vérification impossible ou une incompatibilité bloque sans repli implicite ni modification des autres choix de chaîne. |
| 2.2–2.4 | Contrôler que la version Nuitka effective correspond exactement au verrou et refuser les écarts ; conserver le verrou pendant la campagne et les reproductions, y compris si une nouvelle stable paraît. Préserver les autres choix adoptés, les modes Standalone/ZT et les chaînes Cython distinctes. |
| 2.5 | Relier recettes, mesures et artefacts à la version exacte de leur campagne ; conserver les anciennes preuves sous leurs versions et artefacts d'origine. Réévaluer la dernière stable à la campagne suivante ; une sélection ou déclaration seule ne qualifie pas la nouvelle chaîne et n'autorise aucune installation. |

## Critères des métadonnées PBO et de `toolchain.nuitka` — complément du 26 octobre 2026

Le [contrat de métadonnées](design.md#métadonnées-de-campagne-pbo-et-verrou-nuitka--complément-du-26-octobre-2026)
et le delta reference-runtime précisent le verrou et ajoutent quatre exigences
et six scénarios. Ce complément est synchronisé au canon sur validation
explicite du développeur le 26 octobre 2026, sans réapplication des autres
deltas, réalisation du constructeur ni modification des états des tâches.

| Tâche existante | Critères et recettes à réaliser |
| --- | --- |
| 2.1 | Valider le schéma TOML fermé v1 et `toolchain.nuitka` : nominal ; champs inconnus, absents, dupliqués ou mal typés ; contrainte ouverte, préversion, développement, version locale ou non normalisée ; date invalide/sans UTC ; relevé absent, sortant ou symbolique ; empreinte erronée ; distribution retirée, non déclarée ou altérée ; preuve officielle ne démontrant pas la dernière stable. Rapprocher le verrou de la déclaration exacte dans `pyproject.toml`, sans installation ni correction implicite. |
| 2.2–2.4 | Réaliser la sonde du Nuitka effectivement appelé et son contrôle avant compilation ; vérifier version conforme, sortie inexploitable, compilateur absent et écart, y compris stable plus récente. Relier `build-report.json` à l'identifiant, aux empreintes du document de campagne et du profil, aux distributions et aux versions verrouillée/observée ; vérifier les quatre codes de refus et l'absence de compilation après refus. |
| 2.5 | Qualifier la nouvelle chaîne sur les entrées réelles ; reproduire avec le même identifiant, verrou et preuves sans nouvelle sélection ; vérifier qu'une campagne suivante ne réécrit pas les métadonnées, rapports et artefacts historiques. Les fixtures structurelles et sondes simulées restent distinctes des recettes de compilation et de qualification réelles. |

## Preuve officielle datée Nuitka — préparation documentaire du 27 octobre 2026

La [procédure PBO](PREUVE_SELECTION_PBO.md) complète le delta reference-runtime
avec deux exigences et six scénarios, sans synchronisation du canon ni
implémentation. Le verrou reste `toolchain.nuitka` des métadonnées de campagne.
Les six groupes P01–P06 restent NON EXÉCUTÉS ; aucune coche n'est ajoutée.

| Tâche existante | Critères de réalisation et preuves futures |
| --- | --- |
| 2.1 | Établir observation officielle HTTPS/UTC de Nuitka, sélection de la dernière stable non retirée, manifeste figé et revue autorisée. Déclarer puis qualifier registre, lecteur de confiance, propriétaire et permissions ; aucun booléen du candidat ne crée l'autorité. Vérifier l'identité PBO et refuser une admission PA01. Couvrir P01–P03. |
| 2.2–2.4 | Raccorder la lecture indépendante de l'admission et son état courant, vérifier identité et empreintes avant outils, puis tracer admission et manifeste dans le rapport. Refuser substitution, altération, retrait ou registre inaccessible avec les codes PBO appropriés. Couvrir P02/P04/P05. |
| 2.5 | Vérifier conservation, restauration sans réactivation d'un retrait et reproduction sans nouvelle sélection. Relier les preuves réelles au dossier, à l'admission et au rapport ; couvrir P06 sans présenter une fixture comme collecte officielle ou qualification de la chaîne. |

Aucun registre, collecte, admission, code, installation ou test produit n'est
réalisé par cette inscription documentaire ; les états des tâches sont conservés.
