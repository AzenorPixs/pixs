# Tâches — séparation PA/PZT et gestion PBO

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
