# Tâches — séparation PA/PZT et gestion PBO

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Maintien ciblé des unités — ACL-PIXS-2026-10-31-E3-R1

Périmètre courant : Raccords Agent/PZT et nouveaux contextes ; préserver les versions et preuves anciennes sans qualification nouvelle par héritage.

Les tâches, libellés, cases et sous-lots existants sont conservés. Lorsque leur texte mentionne une orientation remplacée, il reste un repère historique ; la réalisation future suit la cible courante indiquée ci-dessus et ses scénarios. Une ancienne case cochée n'est pas une validation de cette nouvelle version. Chaque unité future vérifie ses contrats, nominal/refus, persistance, autorisation et reprise nécessaires avant sa propre validation ; aucun test produit n'est exécuté par ce maintien.

Sources : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md).

| Unité existante | Correspondance | Critères à relier lors de la réalisation future |
|---|---|---|
| PA10-SL01 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA10, sans nouvelle qualification de la case historique |
| PA10-SL02 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA10, sans nouvelle qualification de la case historique |
| PA10-SL03 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA10, sans nouvelle qualification de la case historique |
| PA10-SL04 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA10, sans nouvelle qualification de la case historique |
| PA10-SL05 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA10, sans nouvelle qualification de la case historique |
| PA10-SL06 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA10, sans nouvelle qualification de la case historique |
| PA10-SL07 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA10, sans nouvelle qualification de la case historique |
| PA10-SL08 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA10, sans nouvelle qualification de la case historique |
| PA10-SL09 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA10, sans nouvelle qualification de la case historique |
| PA10-SL10 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA10, sans nouvelle qualification de la case historique |
| PA10-SL11 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA10, sans nouvelle qualification de la case historique |
| PA10-SL12 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA10, sans nouvelle qualification de la case historique |
| PA10-SL13 | Repère et libellé conservés | Cible et scénarios courants du périmètre PA10, sans nouvelle qualification de la case historique |

La liste ci-dessus n'est pas une nouvelle séquence : les anciens rattachements aux tâches et alias restent ceux des sections conservées. Aucun identifiant n'est attribué à une unité historique absente ou ambiguë.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Les [détails D-A1/D-A2/D-A3/D-MIG](../add-pa-native-build-and-component-composition/DETAIL_A1_A2_A3.md) sont VALIDÉS le 26 octobre 2026, inscrits dans le delta PA01 et synchronisés à l'identique au canon pixs-agent sur demande explicite complémentaire du développeur le même jour. Agent 2.0.0 est adopté mais non livré, la migration non exécutée.

Les [décisions S1/R1/F1](../add-pa-native-build-and-component-composition/DECISIONS_S1_R1_F1.md)
sont VALIDÉES le 27 octobre 2026 : tables privées Agent, outbox/relais PBO
vers PZT et fournisseurs retenus par domaine. Elles sont inscrites dans les
deltas PA01 ; leurs cinq exigences et douze scénarios sont synchronisés à
l'identique aux canons sur demande explicite complémentaire du développeur
du même jour, sans réapplication des autres deltas.
Modèles/migrations, intégration, implémentations/versions, réalisations et preuves
restent manquants. Aucune case ni autorisation de réalisation/exécution
n'est modifiée par cette inscription documentaire.

Les [détails D-S1/D-R1/D-F1/D-SMIG](../add-pa-native-build-and-component-composition/DETAIL_S1_R1_F1.md)
sont VALIDÉS DOCUMENTAIREMENT le 27 octobre 2026 et inscrits dans les deltas
PA01 : dix-sept exigences et trente-quatre scénarios, NON SYNCHRONISÉS au
canon par cette inscription. Huit tables/contraintes, contrat du relais,
interfaces privées et migration détaillée sont adoptés ; code, migrations,
relais/hébergement/profils, fournisseurs versionnés et preuves restent
manquants. Aucune tâche 2.2–2.4 cochée, aucun nouveau cas produit exécuté.

## 1. Formalisation autorisée

- [x] 1.1 Relire les cadrages et capacités applicables et identifier les responsabilités contradictoires.
- [x] 1.2 Reporter la décision validée dans PROJECT.md, TECHNICAL.md, BUILD.md et README.md avec les topologies locales et les deux cas distants.
- [x] 1.3 Aligner les six capacités canoniques et tracer les deltas approuvés.
- [x] 1.4 Signaler l'évolution aux dossiers préparatoires propriétaires sans lancer leurs tâches.
- [x] 1.5 Vérifier UTF-8/LF, liens, schémas, cohérence des responsabilités, OpenSpec strict ciblé/global et absence de changement de code ; consigner les résultats dans design.md.

## 2. Réalisation future — non autorisée par cette session

- [x] 2.1a Réaliser les types et validateurs des trois contrats publics Agent v1.0.0 dédiés (`src/pixs/agent/__init__.py`, `contracts.py`) selon les schémas de design.md. Prouver immédiatement syntaxe, champs/types/versions, catalogue fermé, liaisons acteur/tenant/cible/génération, validité, idempotence et refus sans preuve par unités et tests de frontière ; aucune persistance ou transmission revendiquée.
- [x] 2.1b Fournir le manifest réel `pixs.agent` MODULE 0.1.0 et son enregistrement Django (`component.toml`, `apps.py`) ; dépendances et contrats exacts selon design.md. Prouver syntaxe, découverte, validation, registres et refus des dépendances/versions invalides ; les tests de composition nomment les fixtures externes et ne revendiquent aucune readiness P0.
- [x] 2.1c Réaliser la persistance PostgreSQL propriétaire des états souhaité, observé et confirmé (`models.py`, `migrations/`, dépôt propriétaire). Prouver syntaxe, migrations et aller/retour PostgreSQL réel autorisé, isolation tenant/cible, génération/idempotence concurrentes, crash/perte de réponse et erreurs de stockage sans faux succès ; aucune confirmation exécutant inventée.
- [x] 2.1d Fournir le service de gestion et le `ComponentAdapter` PBO (`service.py`, `adapter.py`) sur contrats Core et port PZT explicites. Prouver immédiatement autorisation/refus et portée Super Admin, liaison id/version du manifest, observation propriétaire, hooks configure/start et libération des ressources sur échec ; aucun démarrage PA/PZT implicite ni migration au chargement.
- [x] 2.1e Prouver la supervision honnête et la continuité de gestion sans exécutant (`supervision.py` et tests applicables) : souhaité/appliqué/dernier connu/confirmé distincts, périmé daté, absence PZT sans substitution, reprise par réconciliation. Vérifier la composition de gestion avec manifests et adaptateur réels ; distinguer refus testés, transport simulé et qualifications réelles restant à 2.2–2.4.
- [ ] 2.2 Coordonner les contrats PA/PZT avec PA01/PA03 et pixs.pzt avec C14 : exécutants, identités, preuves, lifecycle et canaux ; réconcilier les instantanés de préparation avant code.
- [ ] 2.3 Coordonner PA09/X01 pour conserver les contenus Debian/Docker et les frontières de supervision, sans dépendance PBO locale imposée à PA/PZT.
- [ ] 2.4 Qualifier avec les lots propriétaires les scénarios de gestion séparée, transport local/distant, deux topologies distantes, panne, sécurité et compositions ; conserver les preuves avant toute revendication de livraison.

## Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026

Les identifiants et cases ci-dessus sont conservés. Ce contrat précise les critères et contrôles à réaliser **dans chaque tâche**, avant de commencer la suivante. Les tâches de test ou de preuve placées plus loin consolident la couverture et ne reportent jamais les vérifications nécessaires à une tâche antérieure. Une tâche de réalisation comprend donc ses unités, refus et intégrations indispensables dès sa propre exécution ; elle ne peut être validée en attendant qu’une tâche suivante la rende testable.

Les tâches cochées conservent leur statut historique ; leurs preuves doivent être recoupées avant réutilisation si les sources ont changé. Pour les tâches futures, les prérequis externes sont ceux de design.md et des exigences applicables ; un propriétaire, provider, exécutant, contrat adopté ou environnement requis manquant bloque la tâche concernée. La préparation du dossier ne les déclare pas livrés. Les choix ouverts restent à décider avant leur réalisation ; les deltas déjà adoptés ne sont pas réappliqués.

### Périmètre et cas de contrôle propres au lot

- Objet : Périmètre des tâches ci-dessus, sous les contrats publics et propriétaires de design.md.
- Résultat de référence : Les sorties et refus attendus des scénarios applicables au périmètre de cette tâche sont observés ; aucun niveau de garantie ni support non exécuté n’est annoncé.
- Cas de contrôle du profil : Qualifier avec les lots propriétaires les scénarios de gestion séparée, transport local/distant, deux topologies distantes, panne, sécurité et compositions ; conserver les preuves avant toute revendication de livraison.

Chaque contrôle est relié au texte complet de l’exigence et à son scénario, dans requirements.md lorsqu’il existe, sinon dans les deltas et le canon référencés par la proposition. Une simple égalité de titre ne prouve pas la couverture. Les cas conditionnels sont appliqués selon le rôle effectivement sélectionné ; une non-applicabilité est motivée sans remplacer une preuve obligatoire. Aucun paramètre numérique ou provider nouveau n’est déduit de ce contrat.

### Critères et contrôles par tâche future

| Tâche existante | Prérequis immédiat | Critère observable de validation | Contrôles exigés dans cette tâche et preuve |
|---|---|---|---|
| 2.1a | Sources/décisions et formes génériques recoupées | Contrats fermés et leurs refus prouvés, sans effet ni dépendance à la persistance future | Compilation Python et unités/négatifs de chaque frontière, catalogue/version/contexte/mandat/génération/idempotence ; absence de preuve requise refusée. |
| 2.1b | 2.1a validée et cochée | Manifest et registres cohérents, composant déclaré sans fausse disponibilité | Syntaxe Python/TOML, découverte/validation et composition ; dépendance/version inconnue et attestation absente refusées ; fixtures externes identifiées. |
| 2.1c | 2.1b validée et cochée | États propriétaires durables, concurrence et reprise sans double effet démontrés | Compilation, vérifications migrations et intégrations PostgreSQL réelles autorisées : isolation, idempotence/conflit, génération, crash/perte de réponse, erreur stockage. |
| 2.1d | 2.1c validée et cochée | Service et adaptateur contrôlés, observations réelles du producteur et nettoyage sur échec | Compilation, unités/refus et intégration Core/host_runtime ; acteur/tenant/périmètre, manifest/adaptateur divergent, gates, hooks et acquisitions partielles. |
| 2.1e | 2.1d validée et cochée | Gestion composée et observations honnêtes sans inventer un exécutant ou un résultat | Syntaxe et suites applicables, intégrations souhaité/observé/confirmé, péremption, indisponibilité PZT et réconciliation ; distinguer simulation et transport réel. |
| 2.2 | Tâche 2.1e techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.3 | Tâche 2.2 techniquement validée avec ses propres preuves | Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure. | Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux. |
| 2.4 | Tâche 2.3 techniquement validée avec ses propres preuves | Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation. | Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche. |

Les vérifications utilisent les outils et versions du projet selon [AGENTS.md](../../../AGENTS.md) et [DEVOPS.md](../../../DEVOPS.md). Pour un changement Python, inclure la compilation syntaxique et les suites configurées ; pour une interface web, inclure tests et build frontend ainsi que Chromium et Firefox headless, et les contrôles visuels/manuels applicables. Les tests matériels, réseau, stockage, packaging et restauration exigent leur environnement autorisé. La syntaxe seule ne valide aucun comportement. Aucun de ces contrôles n’est exécuté par la présente préparation documentaire.

Pour chaque tâche, conserver identifiant, prérequis, fichiers, commandes, résultats natifs, critère/scénario, versions/artefact, limites et prochaine action ; cocher uniquement après validation technique. Un échec ou une preuve obligatoire indisponible interdit la tâche suivante. Une modification concurrente invalide seulement les preuves affectées et impose leur réconciliation avant reprise.

## Avancement préparatoire du 24 octobre 2026

Les tâches 2.2–2.4 restent ouvertes. La [matrice de raccords](RACCORDS.md)
et les [28 cas de reprise non exécutés](RECETTE_RACCORDS.md) préparent les
interfaces, responsabilités, refus et preuves à consommer dès disponibilité
des propriétaires. C14 livré est pris en compte ; les écarts de générations,
phases natives et dates ne sont pas résolus implicitement. Cette préparation
ne modifie ni les critères des tâches ni leurs prérequis, et ne vaut aucune
qualification de transport, exécutant, matériel ou distribution.

## Sous-lots normalisés

Relevé documentaire du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026 » ; « Périmètre et cas de contrôle propres au lot » ; « Critères et contrôles par tâche future ».

### PA10-SL01 — Relire les cadrages et capacités applicables et identifier les responsabilités contradictoires.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Formalisation autorisée », ligne 25 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA10-SL02 — Reporter la décision validée dans PROJECT.md, TECHNICAL.md, BUILD.md et README.md avec les topologies locales et les deux cas distants.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Formalisation autorisée », ligne 26 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA10-SL03 — Aligner les six capacités canoniques et tracer les deltas approuvés.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Formalisation autorisée », ligne 27 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA10-SL04 — Signaler l'évolution aux dossiers préparatoires propriétaires sans lancer leurs tâches.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Formalisation autorisée », ligne 28 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA10-SL05 — Vérifier UTF-8/LF, liens, schémas, cohérence des responsabilités, OpenSpec strict ciblé/global et absence de changement de code ; consigner les résultats dans design.md.

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Formalisation autorisée », ligne 29 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA10-SL06 — Réaliser les types et validateurs des trois contrats publics Agent v1.0.0 dédiés (`src/pixs/agent/__init__.py`, `contracts.py`) selon les schémas de design.md. Prouver immédiatement syntaxe, champs/types/versions, catalogue fermé, liaisons acteur/tenant/cible/génération, validité, idempotence et refus sans preuve par unités et tests de frontière ; aucune persistance ou transmission revendiquée.

- Ancien repère et tâche rattachée : tâche 2.1a ; section « 2. Réalisation future — non autorisée par cette session », ligne 33 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 60 du texte conservé.
  - Prérequis immédiat : Sources/décisions et formes génériques recoupées
  - Critère observable de validation : Contrats fermés et leurs refus prouvés, sans effet ni dépendance à la persistance future
  - Contrôles exigés dans cette tâche et preuve : Compilation Python et unités/négatifs de chaque frontière, catalogue/version/contexte/mandat/génération/idempotence ; absence de preuve requise refusée.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA10-SL07 — Fournir le manifest réel `pixs.agent` MODULE 0.1.0 et son enregistrement Django (`component.toml`, `apps.py`) ; dépendances et contrats exacts selon design.md. Prouver syntaxe, découverte, validation, registres et refus des dépendances/versions invalides ; les tests de composition nomment les fixtures externes et ne revendiquent aucune readiness P0.

- Ancien repère et tâche rattachée : tâche 2.1b ; section « 2. Réalisation future — non autorisée par cette session », ligne 34 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 61 du texte conservé.
  - Prérequis immédiat : 2.1a validée et cochée
  - Critère observable de validation : Manifest et registres cohérents, composant déclaré sans fausse disponibilité
  - Contrôles exigés dans cette tâche et preuve : Syntaxe Python/TOML, découverte/validation et composition ; dépendance/version inconnue et attestation absente refusées ; fixtures externes identifiées.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA10-SL08 — Réaliser la persistance PostgreSQL propriétaire des états souhaité, observé et confirmé (`models.py`, `migrations/`, dépôt propriétaire). Prouver syntaxe, migrations et aller/retour PostgreSQL réel autorisé, isolation tenant/cible, génération/idempotence concurrentes, crash/perte de réponse et erreurs de stockage sans faux succès ; aucune confirmation exécutant inventée.

- Ancien repère et tâche rattachée : tâche 2.1c ; section « 2. Réalisation future — non autorisée par cette session », ligne 35 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 62 du texte conservé.
  - Prérequis immédiat : 2.1b validée et cochée
  - Critère observable de validation : États propriétaires durables, concurrence et reprise sans double effet démontrés
  - Contrôles exigés dans cette tâche et preuve : Compilation, vérifications migrations et intégrations PostgreSQL réelles autorisées : isolation, idempotence/conflit, génération, crash/perte de réponse, erreur stockage.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA10-SL09 — Fournir le service de gestion et le `ComponentAdapter` PBO (`service.py`, `adapter.py`) sur contrats Core et port PZT explicites. Prouver immédiatement autorisation/refus et portée Super Admin, liaison id/version du manifest, observation propriétaire, hooks configure/start et libération des ressources sur échec ; aucun démarrage PA/PZT implicite ni migration au chargement.

- Ancien repère et tâche rattachée : tâche 2.1d ; section « 2. Réalisation future — non autorisée par cette session », ligne 36 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 63 du texte conservé.
  - Prérequis immédiat : 2.1c validée et cochée
  - Critère observable de validation : Service et adaptateur contrôlés, observations réelles du producteur et nettoyage sur échec
  - Contrôles exigés dans cette tâche et preuve : Compilation, unités/refus et intégration Core/host_runtime ; acteur/tenant/périmètre, manifest/adaptateur divergent, gates, hooks et acquisitions partielles.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA10-SL10 — Prouver la supervision honnête et la continuité de gestion sans exécutant (`supervision.py` et tests applicables) : souhaité/appliqué/dernier connu/confirmé distincts, périmé daté, absence PZT sans substitution, reprise par réconciliation. Vérifier la composition de gestion avec manifests et adaptateur réels ; distinguer refus testés, transport simulé et qualifications réelles restant à 2.2–2.4.

- Ancien repère et tâche rattachée : tâche 2.1e ; section « 2. Réalisation future — non autorisée par cette session », ligne 37 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 64 du texte conservé.
  - Prérequis immédiat : 2.1d validée et cochée
  - Critère observable de validation : Gestion composée et observations honnêtes sans inventer un exécutant ou un résultat
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et suites applicables, intégrations souhaité/observé/confirmé, péremption, indisponibilité PZT et réconciliation ; distinguer simulation et transport réel.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA10-SL11 — Coordonner les contrats PA/PZT avec PA01/PA03 et pixs.pzt avec C14 : exécutants, identités, preuves, lifecycle et canaux ; réconcilier les instantanés de préparation avant code.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Réalisation future — non autorisée par cette session », ligne 38 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 65 du texte conservé.
  - Prérequis immédiat : Tâche 2.1e techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
- Actualisation SL11 du 30/10 : trois unités pures VALIDÉES chacune sur son périmètre — codec UTC6 et agent-content.v2 dans [identifiers.py](../../../src/pixs/agent/identifiers.py) avec [test_agent_identifiers_v2.py](../../../tests/unit/test_agent_identifiers_v2.py) (17 ciblés), descripteurs et validateurs 2.0.0 dans [contracts_v2.py](../../../src/pixs/agent/contracts_v2.py) avec [test_agent_contracts_v2.py](../../../tests/unit/test_agent_contracts_v2.py) (24 ciblés), documents payload traces et observés opaques D-S1 §3.4 dans [documents.py](../../../src/pixs/agent/documents.py) avec [test_agent_documents.py](../../../tests/unit/test_agent_documents.py) (18 ciblés) ; preuves : compilation 0 et régression `PYTHONPATH=src .venv/bin/python3 -B -m unittest discover -s tests/unit -p 'test_agent_*.py'` avec 158 PASS dont 158 inclut 18, 24 et 17 sans les additionner ; limites : ces unités ne qualifient aucune NOUVELLE persistance ou migration S1, aucun transport, autorité ou temps, ni activation métier Agent 2.0.0 ; persistance v1 et preuves historiques 2.1c conservées ; SL11 EN COURS et partiellement réalisé ; 2.2 toujours non cochée.
- Actualisation SL11 du 30/10 (unité S1 document) : quatre unités locales VALIDÉES LOCALES dont trois pures, sur leur seul périmètre — table seule `PayloadDocument` append-only D-S1 §3.4 avec persistance PostgreSQL réelle en schémas jetables dans cinq fichiers : [models.py](../../../src/pixs/agent/models.py), [0002_agent_payload_document.py](../../../src/pixs/agent/migrations/0002_agent_payload_document.py), [lifecycle.py](../../../src/pixs/agent/lifecycle.py), [agent_pg_test_support.py](../../../tests/integration/agent_pg_test_support.py), [test_agent_payload_document_postgres.py](../../../tests/integration/test_agent_payload_document_postgres.py) ; preuves : syntaxe 0, `MigrationAutodetector` sans drift (`AGENT_NO_MIGRATION_DRIFT`), 11 critères PG réels tous vrais, régressions 20 critères stockage v1 et 14 critères adapter/lifecycle v1 tous vrais, 158 unitaires Agent PASS, cache dédié nettoyé, connexions/threads fermés prouvés ; 158 inclut 17+24+18 sans les additionner, ne pas additionner 11/20/14 comme unitaires ; limites : table seule, pas d'application données métier ni profil complet S1/Agent 2, manifest 0.1.0, migration 0001 et migration_lock inchangés, providers/autorité/temps/transport toujours non qualifiés ; persistance v1 et preuves 2.1c conservées ; SL11 EN COURS ; 2.2–2.4 ouvertes.
- Actualisation SL11 du 30/10 (unité U1 inventaire) : cinq unités locales VALIDÉES LOCALES dont quatre pures, sur leur seul périmètre — codec `agent-fact-inventory.v1` D-S1 §3.6 (tableau 17 valeurs, UTF-8 canonique, UUIDv7 en texte, null/textes et précisions de dates préservés, sha256 brut sans nouveau namespace) dans deux fichiers : [fact_inventory.py](../../../src/pixs/agent/fact_inventory.py) avec [test_agent_fact_inventory.py](../../../tests/unit/test_agent_fact_inventory.py) (10 ciblés) ; preuves : compilation 0 et régression `PYTHONPATH=src .venv/bin/python3 -B -m unittest discover -s tests/unit -p 'test_agent_*.py'` avec 168 PASS dont 168 inclut 10 nouveaux et 17/24/18 anciens sans les additionner, cache nettoyé ; dernières preuves PG de l'unité document du 30/10 conservées (11 document, 20 stockage v1, 14 adapter v1) sans les prétendre réexécutées pour ce codec, ne pas additionner 168 avec 10 ni avec PG ; limites : pas de classification, preuve de version, provenance, temps, autorité ou transport ; schéma Agent courant 4 tables (3 historiques + document), sept tables S1 nouvelles restant à réaliser ; persistance v1 et preuves 2.1c conservées ; SL11 EN COURS ; 2.2–2.4 ouvertes.
- Actualisation SL11 du 30/10 (unité U2 provenance structurelle) : six unités locales VALIDÉES LOCALES dont quatre pures et deux unités PG, sur leur seul périmètre — table seule `PayloadProvenance` append-only D-S1 §3.6/§3.7 (structure inerte, preuve limitée aux références de fixture sans authenticité) dans six fichiers : [models.py](../../../src/pixs/agent/models.py), [0003_agent_payload_provenance.py](../../../src/pixs/agent/migrations/0003_agent_payload_provenance.py), [_registry_support.py](../../../src/pixs/agent/_registry_support.py), [lifecycle.py](../../../src/pixs/agent/lifecycle.py), [agent_pg_test_support.py](../../../tests/integration/agent_pg_test_support.py), [test_agent_payload_provenance_postgres.py](../../../tests/integration/test_agent_payload_provenance_postgres.py) ; preuves : compilation 0, drift Django et registre cinq figé valides (`AGENT_NO_MIGRATION_DRIFT_REGISTRY_FIVE_VALID`), 12 critères PG provenance tous vrais avec régressions 11 document, 20 stockage v1 et 14 adapter v1 tous vrais, 168 unitaires Agent PASS sans additionner 168 avec 10 ni avec PG, caches nettoyés et connexions/threads prouvés ; limites : pas de classification M2, provenance authentique, autorité, temps, transport, activation ni schéma S1 complet ; schéma de tests 5 tables (3 historiques + document + provenance), six tables S1 nouvelles restant à réaliser ; 0001/0002, migration_lock et manifest 0.1.0 inchangés ; aucune application de la nouvelle extension sur des données métier ; persistance v1 et preuves 2.1c conservées ; SL11 EN COURS ; 2.2–2.4 ouvertes.
- Actualisation SL11 du 30/10 (unité U3 binding structurel) : sept unités locales VALIDÉES LOCALES dont quatre pures et trois unités PG, sur leur seul périmètre — DDL et primitives privées locales seulement : `PaBinding`/`PaBindingRevision` append-only et `PaBindingState` pointeur courant mutable uniquement par primitive CAS protégée, PK composite vraie, FK composites RunSQL, primitives privées init/CAS, garde `CompositePrimaryKey` corrigée dans [_registry_support.py](../../../src/pixs/agent/_registry_support.py) (test préservé), dans sept fichiers : [models.py](../../../src/pixs/agent/models.py), [0004_agent_pa_binding.py](../../../src/pixs/agent/migrations/0004_agent_pa_binding.py), [_registry_support.py](../../../src/pixs/agent/_registry_support.py), [lifecycle.py](../../../src/pixs/agent/lifecycle.py), [agent_pg_test_support.py](../../../tests/integration/agent_pg_test_support.py), [test_agent_payload_provenance_postgres.py](../../../tests/integration/test_agent_payload_provenance_postgres.py), [test_agent_pa_binding_postgres.py](../../../tests/integration/test_agent_pa_binding_postgres.py) ; preuves neuves : syntaxe 0, drift Django et registre 8 valides, 12 critères PG binding tous vrais avec diagnostics 10/10 dont `pk_ok=true` et `registre_drift=true`, régressions 12 provenance / 11 document / 20 stockage v1 / 14 adapter toutes PG PASS, 168 unitaires Agent PASS sans additionner 168 avec ciblés ni avec PG (17/24/18/10 inclus dans 168, 11/20/14/12 PG non additionnés), cache dédié nettoyé, connexions/threads/schemas fermés prouvés ; limites : ni stage_binding/admission F1/transport/authenticité/temps/autorité/Agent2 opérationnel ni M1/M2/M4 global, pas de nouveau runtime ; schéma test 8 tables (3 historiques + doc + provenance + 3 binding), restent 3 tables S1 nouvelles U4 outbox/attempt/delivery_event ; migrations 0001–0003, manifest 0.1.0, migration_lock inchangés ; persistance v1 et preuves 2.1c conservées ; SL11 EN COURS ; 2.2–2.4 ouvertes ; 10/13 inchangé, toutes preuves historiques ci-dessus préservées.
- Actualisation SL11 du 30/10 (unité U4 relais inerte) : huit unités locales VALIDÉES LOCALES dont quatre pures et quatre unités PG, sur leur seul périmètre — DDL inerte et insert-only seulement : `PaOutbox`/`PaAttempt`/`PaDeliveryEvent` (colonnes 20/18/24 avec BaseAgent 8), PK/FK PROTECT/3 uniques nommés/index partiels/CHECK tableaux CASE 1D/snapshot de forme, aucune réservation/CAS/relais/worker/transport ni R1/F1 opérationnel, dans cinq fichiers : [models.py](../../../src/pixs/agent/models.py), [0005_agent_pa_relay.py](../../../src/pixs/agent/migrations/0005_agent_pa_relay.py), [_registry_support.py](../../../src/pixs/agent/_registry_support.py), [agent_pg_test_support.py](../../../tests/integration/agent_pg_test_support.py), [test_agent_pa_relay_postgres.py](../../../tests/integration/test_agent_pa_relay_postgres.py) ; sources locales désormais 11 tables = 3 historiques + 8 S1 ; les 8 nouvelles tables S1 sont réalisées et qualifiées en schéma TEST SEULEMENT ; preuves neuves : syntaxe 0, drift Django et registre 11 + graphe 5 migrations valides, 14 critères PG relay tous vrais avec 2 PID workers distincts, 4 FK réelles 23503, tableaux NULL/[]/ordre/doublons/Unicode conservés, éléments NULL/vide/2D refusés par `evt_postcond_ck`, NUL refusé par `clean()` Python, 7 refs snapshot chacune NULL + array NULL refusés par `evt_snapshot_shape` avec `response_digest` opaque non-hex accepté, 4 index physiques vérifiés avec prédicats partiels, reverse 0005→0004 refusé `MIGRATION_RELAY_IRREVERSIBLE` avec snapshots DB complets inchangés, régressions 12 binding + 12 provenance + 11 document + 20 stockage v1 + 14 adapter toutes PG PASS, 168 unitaires Agent PASS sans additionner 168 avec ciblés ni avec PG, seul warning observé `models.W045` x1 pour CHECK RawSQL avec zéro erreur (clean Python miroir, contrainte PG testée, non masqué), cache dédié nettoyé, conns/threads/schémas fermés prouvés ; limites : ni déploiement M1 métier, ni classification M2, ni activation M4 ; bornes profil, autorité/temps/transport/provenance authentique non qualifiés ; manifest 0.1.0, migration_lock, lifecycle et 0001–0004 inchangés ; persistance v1 et preuves 2.1c conservées ; SL11 EN COURS ; 2.2–2.4 ouvertes ; 10/13 inchangé, toutes preuves historiques ci-dessus préservées.
- Actualisation SL11 du 30/10 (unité pure observation) : neuf unités locales VALIDÉES LOCALES dont cinq pures et quatre unités PG, sur leur seul périmètre — `TransportObservation` privé 1.0.0 à cinq champs fermés (`attempt_ref/outcome/receipt_ref/native_operation_ref/detail_ref`), immuable `frozen+slots`, validation intrinsèque et construction fermée depuis mapping, 3 outcomes exacts avec `receipt_ref` non-NULL/non-vide requis pour `RECEIPT`, 12 motifs privés D-R1 §4.4 exacts et fermés, dans deux fichiers : [relay_observation.py](../../../src/pixs/agent/relay_observation.py) avec [test_agent_relay_observation.py](../../../tests/unit/test_agent_relay_observation.py) (16 ciblés) ; preuves neuves : syntaxe 0, 16 tests ciblés PASS et 184 unitaires Agent PASS (184 inclut 16, ne pas les additionner), cache nettoyé ; preuves PG relay 14 / binding 12 / provenance 12 / document 11 / stockage 20 / adapter 14 et W045 x1 restant celles de l'unité précédente, NON réexécutées pour ce module pur, source S1 inchangée ; limites : ni reçu authentique, ni non-soumission, ni propriétaire établi, ni qualification depuis une référence ; aucun fournisseur, runtime, DB, réseau, horloge, export `__init__` ou code wire modifié ; schéma de test 11 tables inchangé, manifest 0.1.0 / migration_lock inchangés ; persistance v1 et preuves 2.1c conservées ; SL11 EN COURS ; 2.2–2.4 ouvertes ; 10/13 inchangé, toutes preuves historiques ci-dessus préservées.
- Actualisation SL11 du 30/10 (unité pure composition) : dix unités locales VALIDÉES LOCALES dont six pures et quatre unités PG, sur leur seul périmètre — `RelayComposition` privé 1.0.0 à sept champs fermés exacts (`slot/interface_version/provider_component/implementation_ref/implementation_version/composition_ref/qualification_ref`), `interface_version` exacte 1.0.0, immuable `frozen+slots`, références opaques UTF-8 non-vides sans NUL, construction fermée depuis mapping, sans tri/normalisation/conversion ni types élargis, dans deux fichiers : [relay_composition.py](../../../src/pixs/agent/relay_composition.py) avec [test_agent_relay_composition.py](../../../tests/unit/test_agent_relay_composition.py) (12 ciblés) ; preuves neuves : syntaxe 0, 12 tests ciblés PASS et 196 unitaires Agent PASS (196 inclut 12, ne pas les additionner), cache nettoyé ; preuves PG relay 14 / binding 12 / provenance 12 / document 11 / stockage 20 / adapter 14 et W045 x1 restant celles de l'unité 8, NON réexécutées pour ce module pur, source S1 inchangée ; limites : présence de `qualification_ref` ne prouvant aucune validité, autorisation ou actualité ; aucun provider, registre, runtime, réseau, DB, horloge, export `__init__` ou code wire ajouté ; pas de whitelist slot/provider ni format implementation_version inventés ; schéma de test 11 tables inchangé, manifest 0.1.0 / migration_lock inchangés ; persistance v1 et preuves 2.1c conservées ; SL11 EN COURS ; 2.2–2.4 ouvertes ; 10/13 inchangé, toutes preuves historiques ci-dessus préservées.
- Actualisation SL11 du 30/10 (unité pure reçu résolution) : onze unités locales VALIDÉES LOCALES dont sept pures et quatre unités PG, sur leur seul périmètre — `ResolutionReceipt` privé 1.0.0 à neuf champs fermés exacts (`binding_ref/native_operation_ref/native_result_ref/native_snapshot_ref/native_revision_ref/response_digest/origin_proof_ref/postcondition_refs/time_evidence_ref`), huit références opaques UTF-8 non-vides sans NUL types stricts sans HEX64 imposé pour `response_digest`, `postcondition_refs` tuple immuable ordre/doublons préservés vide accepté sans borne inventée liste refusée, construction fermée depuis mapping, immuable `frozen+slots`, sans tri/normalisation/conversion ni inférence causalité depuis date/phase/numéro/ref, dans deux fichiers : [resolution_receipt.py](../../../src/pixs/agent/resolution_receipt.py) avec [test_agent_resolution_receipt.py](../../../tests/unit/test_agent_resolution_receipt.py) (13 ciblés) ; preuves neuves : syntaxe 0, 13 tests ciblés PASS et 209 unitaires Agent PASS (209 inclut 13, ne pas les additionner), cache nettoyé ; preuves PG relay 14 / binding 12 / provenance 12 / document 11 / stockage 20 / adapter 14 et W045 x1 restant celles de l'unité 8, NON réexécutées pour ce module pur, source S1 inchangée ; limites : ni resolve_result, ni vérification origine/postcondition/snapshot courant, ni causalité/autorisation déduite des références ; aucun fournisseur, DB, réseau, horloge, runtime, export `__init__` ou code wire modifié ; schéma TEST 11 tables inchangé, manifest 0.1.0 / migration_lock inchangés ; persistance v1 et preuves 2.1c conservées ; SL11 EN COURS ; 2.2–2.4 ouvertes ; 10/13 inchangé, toutes preuves historiques ci-dessus préservées.
- Actualisation SL11 du 30/10 (unité PG lecture reconciliation) : douze unités locales VALIDÉES LOCALES dont sept pures et cinq unités PG, sur leur seul périmètre — `read_reconciliation` seule privée/inactive dans [relay_store.py](../../../src/pixs/agent/relay_store.py) avec [test_agent_relay_store_postgres.py](../../../tests/integration/test_agent_relay_store_postgres.py) (14 critères) ; SQL un statement paramétré filtré scope/cible, jointure révision courante, refus divergences révision/état-raison/ref native, UUID7 strict, retour figé tuples avec présentation stable sans ordre causal, postconditions préservées ; aucune mutation/observe_commit/relais/provider/profil/autorité/temps/transport/activation/export `__init__`/wire ajouté, pid/schema provenance seule ; preuves réelles : syntaxe 0, 14 critères PG lecture PASS après correction CaptureQueriesContext (échec initial AttributeError cap.queries conservé), régressions 14 relay / 12 binding / 12 provenance / 11 doc / 20 stockage / 14 adapter toutes PG PASS (97 critères PG distincts 7 suites, pas unitaires), 209 unitaires Agent PASS, cache/conns/threads/schémas nettoyés, W045 x1 inchangé observé par relay zéro erreur ; schéma TEST 11 / 5 migrations et manifest 0.1.0 / migration_lock inchangés ; limites : futures mutations/observe_commit non approuvées faute garanties profil/staging/jeton/preuves propriétaires ; prochain bilan des blocages sourcés, pas de clôture inventée ; persistance v1 et preuves 2.1c conservées ; SL11 EN COURS ; 2.2–2.4 ouvertes ; 10/13 inchangé, toutes preuves historiques ci-dessus préservées.

- Bilan 30/10 : finalisation BLOQUÉE, voir [BLOCKERS.md](BLOCKERS.md) pour 2.2 à 2.4 sourcées ; 12 unités et preuves ci-dessus conservées, aucune case cochée ou renumérotée.

### PA10-SL12 — Coordonner PA09/X01 pour conserver les contenus Debian/Docker et les frontières de supervision, sans dépendance PBO locale imposée à PA/PZT.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Réalisation future — non autorisée par cette session », ligne 39 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 66 du texte conservé.
  - Prérequis immédiat : Tâche 2.2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Comportement nominal de cette étape et refus indispensables observés par son propriétaire ; isolation, intégrité et reprise requises pour cette étape déjà prouvées, sans dépendre d’une réalisation ultérieure.
  - Contrôles exigés dans cette tâche et preuve : Syntaxe et contrôles configurés ; unités/négatifs et intégrations nécessaires aux cas du lot affectés par cette tâche, exécutés immédiatement. Vérifier type/version/contexte invalide, droits/refus, panne et reprise applicables ; persistance, transport, build ou plateforme réels si requis par le critère. Les recettes finales ne remplacent pas ces tests locaux.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### PA10-SL13 — Qualifier avec les lots propriétaires les scénarios de gestion séparée, transport local/distant, deux topologies distantes, panne, sécurité et compositions ; conserver les preuves avant toute revendication de livraison.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Réalisation future — non autorisée par cette session », ligne 40 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 67 du texte conservé.
  - Prérequis immédiat : Tâche 2.3 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats observés des scénarios et cas de contrôle du lot affectés par cette tâche, reliés aux versions, profils et artefacts ; refus et limites explicites, sans support déduit d’une simple compilation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter dès cette tâche les cas propres au lot listés ci-dessus qui prouvent son objet, sur les dépendances/plateformes réelles lorsque leur garantie est revendiquée ; conserver commandes/résultats et distinguer unité, intégration, conformité et contrôles manuels. Une preuve obligatoire manquante bloque la tâche.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
