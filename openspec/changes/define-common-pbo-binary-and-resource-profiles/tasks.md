# Tâches — binaire PBO commun et ressources

## Critères courants — reprise ACSM du 31 octobre 2026

Les libellés, cases et sous-lots ci-dessous sont conservés comme repères historiques. Les tâches 2.1 à 2.5 restent ouvertes. Leur réalisation suit les trois modes d'Instance Standalone/ZT/Domaine du canon, distincts de Nuitka standalone et du transport PZT ; les anciennes formulations à deux modes ne restreignent pas cette cible.

Le [contrôle de couverture](COUVERTURE_DELTAS_ACSM.md) rattache les 37 anciennes exigences aux contrats courants et aux tâches restantes. Les 34 blocs déjà au canon et le modèle de modes remplacé ne sont pas à adopter de nouveau. Les deux exigences du [delta actif Nuitka](specs/reference-runtime/spec.md) restent proposées, sans synchronisation implicite ; les critères du 27 octobre et les recettes P01–P06 restent applicables à leur périmètre.

Les rattachements précis sont 2.1/C20-SL07 pour la sélection et l'admission indépendante ; 2.2–2.4/C20-SL08 à SL10 pour le raccordement, les refus et le rapport ; 2.5/C20-SL11 pour la conservation, le retrait, la restauration et la reproduction. Chaque tâche exige ses contrôles propres avant validation. La présente reprise ne coche ni ne réalise aucune de ces unités.

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
et les six exigences déjà adoptées dans le [canon reference-runtime](../../specs/reference-runtime/spec.md)
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

## Sous-lots normalisés

Relevé documentaire du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026 » ; « Périmètre et cas de contrôle propres au lot » ; « Critères et contrôles par tâche future » ; « Preuve officielle datée Nuitka — préparation documentaire du 27 octobre 2026 ».

### C20-SL01 — Relire cadrages, canon, séparation PA/PZT et baseline OpenSpec strict.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Formalisation documentaire », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C20-SL02 — Aligner les cadrages, README et schémas sur le binaire commun et les plans de ressources.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Formalisation documentaire », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C20-SL03 — Synchroniser les sept capacités canoniques et produire les deltas de traçabilité.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Formalisation documentaire », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C20-SL04 — Vérifier cohérence, compteurs, liens, UTF-8/LF, schémas et strict global incluant les capacités ciblées ; consigner les résultats.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Formalisation documentaire », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C20-SL05 — Intégrer Nuitka standalone pour PBO, distinguer les deux modes d'exploitation et Cython ciblé dans PBO des chaînes Cython PA/PZT ; vérifier canon, deltas, compteurs et contrôles documentaires.

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Formalisation documentaire », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C20-SL06 — Vérifier la cohérence finale : nommer les modes Standalone/ZT, distinguer autonomie de gouvernance et activation PZT, ajouter le scénario Standalone avec PA, harmoniser les schémas et contrôler canon/deltas et strict global.

- Ancien repère et tâche rattachée : tâche 1.6 ; section « 1. Formalisation documentaire », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C20-SL07 — Sélectionner et tracer la dernière stable Nuitka publiée et non retirée sur PyPI au début de chaque campagne PBO, verrouiller sa version exacte, aligner déclarations et contrôles puis qualifier la chaîne standalone, ses versions/options, dépendances et ressources, chargement des extensions, noms/CLI, schémas et valeurs des profils ; distinguer exploitation Standalone/ZT sans nouvelle dépendance implicite.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Réalisation future — non engagée », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 39 du texte conservé.
  - Prérequis immédiat : Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Dépendances, critères et contrôles sourcés : tableau « Critères Nuitka par campagne — décision du développeur du 26 octobre 2026 », ligne 60 du texte conservé.
  - Critères complémentaires : Vérifier la dernière stable Nuitka publiée et non retirée sur PyPI au début de la campagne ; exclure préversions et développement ; enregistrer date, source, version exacte, provenance et empreintes. Verrouiller la version et aligner `pyproject.toml`, métadonnées, contrôles de construction, tests concernés et documentation, puis qualifier Python, Django, dépendances, compilateur C, ABI, cibles, options standalone, rôles et ressources embarquées. Une vérification impossible ou une incompatibilité bloque sans repli implicite ni modification des autres choix de chaîne.
- Dépendances, critères et contrôles sourcés : tableau « Critères des métadonnées PBO et de `toolchain.nuitka` — complément du 26 octobre 2026 », ligne 74 du texte conservé.
  - Critères et recettes à réaliser : Valider le schéma TOML fermé v1 et `toolchain.nuitka` : nominal ; champs inconnus, absents, dupliqués ou mal typés ; contrainte ouverte, préversion, développement, version locale ou non normalisée ; date invalide/sans UTC ; relevé absent, sortant ou symbolique ; empreinte erronée ; distribution retirée, non déclarée ou altérée ; preuve officielle ne démontrant pas la dernière stable. Rapprocher le verrou de la déclaration exacte dans `pyproject.toml`, sans installation ni correction implicite.
- Dépendances, critères et contrôles sourcés : tableau « Preuve officielle datée Nuitka — préparation documentaire du 27 octobre 2026 », ligne 87 du texte conservé.
  - Critères de réalisation et preuves futures : Établir observation officielle HTTPS/UTC de Nuitka, sélection de la dernière stable non retirée, manifeste figé et revue autorisée. Déclarer puis qualifier registre, lecteur de confiance, propriétaire et permissions ; aucun booléen du candidat ne crée l'autorité. Vérifier l'identité PBO et refuser une admission PA01. Couvrir P01–P03.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C20-SL08 — Réaliser le binaire PBO et ses rôles/processus configurables avec les propriétaires existants et la persistance de référence.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Réalisation future — non engagée », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 40 du texte conservé.
  - Prérequis immédiat : Tâche 2.1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C20-SL09 — Réaliser plans et suivi de ressources PA/PZT avec sessions, idempotence, propriétaire réseau et garanties de sécurité conservés.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Réalisation future — non engagée », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 41 du texte conservé.
  - Prérequis immédiat : Tâche 2.2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C20-SL10 — Adapter et qualifier superviseurs, paquets et image, limites effectives et états demandé/appliqué sans élargissement des privilèges.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Réalisation future — non engagée », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 42 du texte conservé.
  - Prérequis immédiat : Tâche 2.3 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C20-SL11 — Qualifier mémoire, CPU, latence, débit, saturation, reconfiguration, révocation et reprise par cible ; n'admettre Cython dans PBO que pour des optimisations ciblées mesurées, avec non-régression ; conserver les preuves avant publication.

- Ancien repère et tâche rattachée : tâche 2.5 ; section « 2. Réalisation future — non engagée », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 43 du texte conservé.
  - Prérequis immédiat : Tâche 2.4 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Dépendances, critères et contrôles sourcés : tableau « Critères Nuitka par campagne — décision du développeur du 26 octobre 2026 », ligne 62 du texte conservé.
  - Critères complémentaires : Relier recettes, mesures et artefacts à la version exacte de leur campagne ; conserver les anciennes preuves sous leurs versions et artefacts d'origine. Réévaluer la dernière stable à la campagne suivante ; une sélection ou déclaration seule ne qualifie pas la nouvelle chaîne et n'autorise aucune installation.
- Dépendances, critères et contrôles sourcés : tableau « Critères des métadonnées PBO et de `toolchain.nuitka` — complément du 26 octobre 2026 », ligne 76 du texte conservé.
  - Critères et recettes à réaliser : Qualifier la nouvelle chaîne sur les entrées réelles ; reproduire avec le même identifiant, verrou et preuves sans nouvelle sélection ; vérifier qu'une campagne suivante ne réécrit pas les métadonnées, rapports et artefacts historiques. Les fixtures structurelles et sondes simulées restent distinctes des recettes de compilation et de qualification réelles.
- Dépendances, critères et contrôles sourcés : tableau « Preuve officielle datée Nuitka — préparation documentaire du 27 octobre 2026 », ligne 89 du texte conservé.
  - Critères de réalisation et preuves futures : Vérifier conservation, restauration sans réactivation d'un retrait et reproduction sans nouvelle sélection. Relier les preuves réelles au dossier, à l'admission et au rapport ; couvrir P06 sans présenter une fixture comme collecte officielle ou qualification de la chaîne.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
