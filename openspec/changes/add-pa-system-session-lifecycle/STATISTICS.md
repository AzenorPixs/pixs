# Statistiques PA03 add-pa-system-session-lifecycle

Ce rapport couvre la création déclarée 17 OCTOBRE 2026 sans heure connue, avec lacune du 17 OCTOBRE au 25 et 26 OCTOBRE classée N/A. Premier checkpoint le 25 à 23:16:13.790491Z. Mesures natives depuis le 26 à 09:53:21.591Z. Nouvelle coupe source 2026-10-30T05:50:53.259Z juste avant cette production, les éditions du rapport et liaisons et clôture ultérieures sont hors snapshot. Date de consignation du relevé 73 pourcent 2026-10-30T05:50:53.515Z, heure exacte de lecture non fournie par l outil. Le cumul remplace l ancien et porte sur les 3 sessions connues PA03 dédupliquées, sans ancien frontend CISMP3 ni sondes. Change ouvert—dépendances manquantes—archivage en attente, 1 tâche sur 10 audit seul validé et 9 ouvertes. Voir [BLOCKERS.md](./BLOCKERS.md), .openspec.yaml et [checkpoint](../../../output/cismp/cismp3-pixs-01a17557c728/state.json), clés resume_20261030.nativeChangeStatistics et resume_20261030.all_change_contexts et resume_20261030.statsComputedTables. Les 9 fichiers et tentatives incluent désormais BLOCKERS écrit le 30 oct. Fin du change toujours EN ATTENTE, sans durée finale. Les mesures sont prises avant son enregistrement, preuve de publication et gate viendront du checkpoint. Technique CAB à la coupe actuelle 2.1.15 RÉTABLI ET VÉRIFIÉ, prévol neuf true avec 0 effectué.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Muse Spark 1.3 Contributor | OC 1.19.4 historique, version exacte du modèle N/A au delà de l id API | opencode-go | high historique | N/A historique | N/A historique | N/A, ensemble non mesurable |
| Muse Spark 1.3 Contributor | OC 2.2.0 reprise, version exacte du modèle N/A au delà de l id API, DEVOPS 2.2.1 non affirmé comme runtime avec divergence d inventaire explicitée | opencode-go | medium reprise | 1.427 secondes, moyenne de 1 sonde valide sans outil | 1130.2 tokens par seconde, moyenne de 1 sonde valide sans outil, sans gain causal ni qualification produit | N/A, ensemble non mesurable |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex moteur exact non exposé | version exacte non exposée N/A | fournisseur API exact non exposé N/A | raisonnement exact non exposé N/A | N/A | N/A | N/A, dénominateur indisponible |

## 1. Statistiques générales et décisions

Ce qui a été mesuré : rôles natifs 481, parties 906, outils natifs 270 dont 244 completed et 26 error, cibles fichier 9 pour 22 tentatives dont 21 completed et 1 error. Les décisions CAB sont strictement disjointes par contexte. Un completed natif ne vaut pas validation produit et les erreurs natives ne sont pas des refus.

| Contexte | Approuvées | Refusées | Total décisions | Once |
|---|---|---|---|---|
| CAB 1225 | 38 | 1 | 39 | 37 |
| CAB 1371 | 3 | 0 | 3 | 3 |
| Total | 41 | 1 | 42 | 40 |

| Décisions | Part |
|---|---|
| approved 41 | 97.6 % |
| rejected 1 | 2.4 % |
| Total 42 | 100 % |

| Usage natif sur 294 réponses | Valeur |
|---|---|
| input | 4565936 |
| output | 214055 |
| raisonnement | 42428 |
| cache read | 57606710 |
| cache write | 0 |
| coût observé | 0.53586598 unité non exposée |

Le cache lu ne s ajoute pas aux entrées comme une consommation calculée, et aucune devise n est inventée. Currency du coût NON EXPOSÉE.

| Session | Messages | Part des 481 | Outils | Part des 270 |
|---|---|---|---|---|
| ses_e885f9c74ffeY3CgYSRt08BP9W | 8 | 1.7 % | 13 | 4.8 % |
| ses_e885ddb30ffe1QQG9mU6kv4QtR | 29 | 6.0 % | 25 | 9.3 % |
| ses_e88532cdcffeUt80NL4PSM1isd | 444 | 92.3 % | 232 | 85.9 % |
| Total | 481 | 100 % | 270 | 100 % |

Les enregistrements et validations et la clôture postérieurs à la coupe ne sont pas inclus, et les résultats finaux relèvent du checkpoint sans fausse livraison. Aucun produit qualifié, 1 sur 10 inchangé.

## 2. Types de messages et d’outils

| Catégorie | Effectif | Part |
|---|---|---|
| user | 160 | 33.3 % |
| assistant | 294 | 61.1 % |
| system | 4 | 0.8 % |
| compaction | 2 | 0.4 % |
| model-switched | 1 | 0.2 % |
| idle | 20 | 4.2 % |
| Total | 481 | 100 % |

| Catégorie | Effectif | Part |
|---|---|---|
| text | 322 | 35.5 % |
| reasoning | 314 | 34.7 % |
| tool | 270 | 29.8 % |
| Total | 906 | 100 % |

| Catégorie | Effectif | Part |
|---|---|---|
| tool-calls | 180 | 61.2 % |
| absent | 2 | 0.7 % |
| stop | 112 | 38.1 % |
| Total | 294 | 100 % |

| Catégorie | Effectif | Part |
|---|---|---|
| opencode-go/muse-spark-1.3-contributor/high | 258 | 87.8 % |
| opencode-go/muse-spark-1.3-contributor/medium | 36 | 12.2 % |
| Total | 294 | 100 % |

| Outil | Total | Part globale | Terminés | Erreurs | Taux terminés | Taux erreurs |
|---|---|---|---|---|---|---|
| read | 99 | 36.7 % | 97 | 2 | 98.0 % | 2.0 % |
| glob | 14 | 5.2 % | 14 | 0 | 100.0 % | 0.0 % |
| cgpt-validation_broker_health | 1 | 0.4 % | 1 | 0 | 100.0 % | 0.0 % |
| cgpt-validation_broker_readiness | 22 | 8.1 % | 22 | 0 | 100.0 % | 0.0 % |
| cgpt-validation_broker_remediation_registry | 1 | 0.4 % | 1 | 0 | 100.0 % | 0.0 % |
| bash | 42 | 15.6 % | 40 | 2 | 95.2 % | 4.8 % |
| cgpt-validation_list_pending | 1 | 0.4 % | 1 | 0 | 100.0 % | 0.0 % |
| cgpt-validation_request_validation | 45 | 16.7 % | 24 | 21 | 53.3 % | 46.7 % |
| grep | 7 | 2.6 % | 7 | 0 | 100.0 % | 0.0 % |
| cgpt-validation_get_approval | 20 | 7.4 % | 20 | 0 | 100.0 % | 0.0 % |
| cgpt-validation_poll_approval | 16 | 5.9 % | 15 | 1 | 93.8 % | 6.3 % |
| cgpt-validation_cancel_approval | 1 | 0.4 % | 1 | 0 | 100.0 % | 0.0 % |
| execute | 1 | 0.4 % | 1 | 0 | 100.0 % | 0.0 % |
| Total | 270 | 100 % | 244 | 26 | 90.4 % | 9.6 % |

Un completed ne prouve pas une approbation manuelle, une erreur native ne signifie pas un refus, et les arrondis peuvent donner 99.9 ou 100.1.

## 3. Fichiers modifiés

| Chemin absolu | Tentatives | Part des 22 tentatives | Terminées | Erreurs | Taux terminées | Taux erreurs |
|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-pa-system-session-lifecycle/requirements.md | 2 | 9.1 % | 1 | 1 | 50.0 % | 50.0 % |
| /home/devops/datas/pixs/openspec/changes/add-pa-system-session-lifecycle/proposal.md | 2 | 9.1 % | 2 | 0 | 100.0 % | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-pa-system-session-lifecycle/design.md | 3 | 13.6 % | 3 | 0 | 100.0 % | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-pa-system-session-lifecycle/tasks.md | 4 | 18.2 % | 4 | 0 | 100.0 % | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-pa-system-session-lifecycle/contracts.md | 3 | 13.6 % | 3 | 0 | 100.0 % | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-pa-system-session-lifecycle/session-integration.md | 2 | 9.1 % | 2 | 0 | 100.0 % | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-pa-system-session-lifecycle/specs/pixs-agent/spec.md | 2 | 9.1 % | 2 | 0 | 100.0 % | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-pa-system-session-lifecycle/.openspec.yaml | 1 | 4.5 % | 1 | 0 | 100.0 % | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-pa-system-session-lifecycle/BLOCKERS.md | 3 | 13.6 % | 3 | 0 | 100.0 % | 0.0 % |
| Total | 22 | 100 % | 21 | 1 | 95.5 % | 4.5 % |

Ces tentatives ne prouvent pas une livraison. Elles sont déjà incluses dans les 42 commandes ; mkdir est compté séparément. La production du rapport postérieure à la coupe est exclue de ces compteurs.

## 4. Commandes

| Famille | Effectif | Part |
|---|---|---|
| curl | 1 | 2.4 % |
| true | 7 | 16.7 % |
| python3 | 23 | 54.8 % |
| openspec validate | 11 | 26.2 % |
| Total | 42 | 100 % |

| ID natif | Libellé <=100 caractères | Statut outil | Code retour | Occurrences | Part des 42 |
|---|---|---|---|---|---|
| call_01a177a1429b755c96afcb078484cda4 | curl status SUP via echo | error | N/A | 1 | 2.4 % |
| call_01a177ab223775efafef8e8e094635c9 | python base64 hashlib os pathlib | error | N/A | 1 | 2.4 % |
| call_01a178ac32f477bd9ef84c0153dec5ec | openspec validate change strict | completed | 1 | 1 | 2.4 % |
| call_01a178ae572c75b498d9ac2a0125c962 | openspec validate all strict json no-interactive | completed | 1 | 1 | 2.4 % |

Les 2 cas error sont des erreurs natives avec exit inconnu, pas des refus prouvés et sans explication de leur cause, et les 2 cas completed exit 1 sont deux mandats distincts avec la même cause des sept warnings de longueur, tandis que les contrôles du 26 octobre restent historiques car aucun test produit ni contrôle documentaire du 30 n était encore exécuté à la coupe.

## 5. Accès web

| Domaine | Mesure | Cause |
|---|---|---|
| web historique | N/A | traces non collectées |
| URL Microsoft et PAM citées dans les docs | N/A | pas de preuve de visites |
| interne CAB | contrôle | pas du web métier |

## 6. Synthèse globale

| Durée du change | Valeur |
|---|---|
| création déclarée | 17 oct 2026 heure N/A |
| premier checkpoint | 25 oct 23:16:13.790491Z |
| coupe | 30 oct 05:50:53.259Z |
| fin du change et archivage | EN ATTENTE |
| durée globale du change | N/A |
| durée provisoire checkpoint vers coupe | 102 h 34 min 39 s calculée 369279 secondes entre 25 oct 23:16:13.790491Z et 30 oct 05:50:53.259Z, provisoire pas fin du change |

| Quota Codex 7 jours | Horodatage | Utilisé | Reset |
|---|---|---|---|
| historique | N/A | 14 % | 1793599315 soit 2026-11-02T06:01:55.000Z |
| reprise historique | 26 oct 11:08:30 UTC | 26 % | 1793599315 soit 2026-11-02T06:01:55.000Z |
| reprise actuelle avant production | 30 oct avant production, heure exacte du relevé 63 non capturée | 63 % | 1793774753 soit 2026-11-04T06:45:53.000Z |
| reprise actuelle fin | consignation 2026-10-30T05:50:53.515Z, heure exacte de lecture non fournie | 73 % | 1793774753 soit 2026-11-04T06:45:53.000Z |
| différence reprise seule | même compte et même fenêtre | 10 points de pourcentage uniquement reprise | partage avec autres tâches sans imputation exclusive |
| différence depuis création | N/A fenêtres différentes et début non capturé | N/A | N/A |

| Domaine | Total | Part globale | Terminés | Erreurs | Taux terminés | Taux erreurs |
|---|---|---|---|---|---|---|
| Lectures et recherches | 120 | 44.4 % | 118 | 2 | 98.3 % | 1.7 % |
| Commandes shell | 42 | 15.6 % | 40 | 2 | 95.2 % | 4.8 % |
| MCP | 107 | 39.6 % | 85 | 22 | 79.4 % | 20.6 % |
| CodeMode execute | 1 | 0.4 % | 1 | 0 | 100 % | 0 % |
| Total | 270 | 100 % | 244 | 26 | 90.4 % | 9.6 % |

Les 22 tentatives fichier sont un sous-ensemble des commandes, sans addition. Les 42 décisions des 2 contextes CAB restent distinctes et ne s additionnent pas aux outils natifs, sans mesures exhaustives depuis le 17. Surcharge des sondes distincte de la production : initiale du 30 input 12370 output 419 reasoning 561 coût 0 TTMT et débit N/A, finale du 30 input 8466 output 408 reasoning 186 coût 0 TTMT 1427 ms flux 361 ms avec modèle medium exact et cgpt connected après, sonde isolée shared deleted true. Sondes historiques incomplètes N/A sans invention, currency du coût NON EXPOSÉE. Compteurs figés à la coupe 05:50, les opérations d édition du rapport et les contrôles et la clôture postérieurs sont exclus, et les résultats d enregistrement et de clôture relèvent du checkpoint. Aucune confirmation métier du module ni test produit ni archive ni livraison, le prévol CAB seul inoffensif ne vaut pas produit. Les tests CLI du 26 restent historiques avec 1 sur 1 ciblé standard et 185 sur 185 global standard et 0 sur 1 puis 184 sur 185 en strict avec sept warnings de longueur, non rejoués au 30 au point de coupe, et 9 cases restent ouvertes. À la coupe du 04:59 UTC, le raccord CAB restait en maintenance en attente, sans prétendre qu il l est encore après restauration 15, aucun secret lu dans ce calcul, sans Git ni activation hôte.

### Sondes techniques hors production

| Position | Entrée | Sortie | Raisonnement | Coût natif | TTMT | Débit | Couverture |
|---|---|---|---|---|---|---|---|
| initiale 30 | 12370 | 419 | 561 | 0 | N/A sans SSE | N/A sans SSE | N/A |
| finale 30 | 8466 | 408 | 186 | 0 | 1427 ms | 1130.2 toks par seconde | 1 sonde valide flux 361 ms supprimée et MCP connected |

### Rapprochement documentaire post coupe 05:50

Nouvelle entrée post coupe 05:50 de rapprochement documentaire, sans toucher aux 6 H2. Les compteurs 270 outils restent la coupe historique dédupliquée, sans addition aux compteurs futurs et sans télémétrie supplémentaire inventée. Couverture des comptages messages et outils et tokens : OpenCode 3 sessions. Activité détaillée historique de l orchestrateur hors relevés quotas non mesurée N/A par sources manquantes, sans conclure à une absence. Sondes distinguées déjà présentes, sans pourcentage attribué exclusivement. Pas de réécriture d ancienne entrée ni nouveau code.

