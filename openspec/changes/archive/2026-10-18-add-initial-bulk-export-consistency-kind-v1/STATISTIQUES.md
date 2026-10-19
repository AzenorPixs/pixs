# Statistiques — add-initial-bulk-export-consistency-kind-v1

RUN `cismp2-pixs-16f90fb95c0c4d9b`, contexte CAB `326`, projet `/home/devops/datas/pixs`. Rapport par archive. Intervalle de production : 18/10/2026 20:47:13 Europe/Paris → 18/10/2026 21:10:52 Europe/Paris.

Sources : historique HTTP natif des sessions `ses_eafa6950cffeWS6jcYpN4ytKcA`, `ses_eafa09ec1ffeXHkZvaq2bMSCt6` borné à la fin de collecte, agrégats CAB filtrés du contexte 326, relevés natifs Codex et deux sondes dédiées. La sélection et les sondes sont identifiées séparément ; aucun contenu de secret n’est utilisé. La rédaction de ce rapport, la publication technique et la clôture ultérieures sont hors des compteurs de production ci-dessous.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version exacte non fournie | OpenCode Go / opencode-go | high | 4.412 s | 525.349 | N/A — temps complet non mesurable |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex (GPT-6) | N/A — version exacte non exposée | OpenAI | N/A — non exposé | N/A — orchestrateur non sondé | N/A — orchestrateur non sondé | N/A — télémétrie non exposée |

Temps de service : seules 28.311 s d’intervalles de fragments textuels/raisonnement sont disponibles ; elles ne mesurent pas le temps actif complet. Dénominateur cumulé de tous les agents N/A, parts N/A. Ni attente, outils ni durée calendaire ne sont assimilés à la génération. Les deux sessions de production de cet agent se succèdent ; aucune somme de durées parallèles n’est utilisée.

## 1. Statistiques générales et décisions

Résultat : 123/123 tests réussis (100.0 %), 3/3 compilations exit 0 (100.0 %), ciblé OpenSpec strict exit 0, global standard 186/186 (100.0 %). Strict global avant archive : exit 1, 184/186 (98.9 %) ; après archive : exit 1, 183/185 (98.9 %). Quatre WARNING historiques de longueur : bulk-operations requirements[6], [10], [13] et identity-assurance requirements[4] ; zéro ERROR. Ces deux canons sont inchangés par ce RUN.

| Décision CAB enregistrée | Nombre | Part |
|---|---|---|
| approved | 20 | 95.2 % |
| rejected | 1 | 4.8 % |
| needs_clarification | 0 | 0.0 % |
| pending | 0 | 0.0 % |
| Total | 21 | 100.0 % |

19 permissions natives once observées : 8 écritures et 11 commandes. Sur les 20 décisions approved, une validation est restée sans effet puis annulée à révision périmée. Une seule décision rejected concerne proposal.md avant effet. Le mandat initial de .openspec.yaml avec mode read divergent a été annulé avant effet, après un appel interrompu ; il ne devient pas une deuxième décision CAB rejected. Un autre appel prévol -32602 est une erreur technique avant admission.

Convention : « approuvé et exécuté » signifie appel natif terminé et autorisé dans son mécanisme ; il ne prouve pas une approbation manuelle pour les lectures. « Refusé » désigne un refus de permission explicite. « Erreur technique » désigne un échec d’appel, interruption ou abandon ; les deux validations strictes exit 1 restent des commandes autorisées terminées dont le contrôle a échoué. Aucun refus natif de permission observé.

| Mesure de production native | Valeur |
|---|---|
| Messages | 188 |
| Appels terminés | 110 |
| Appels terminés sans erreur d’outil | 108 (98.2 %) |
| Erreurs d’outil MCP | 2 (1.8 %) |
| Tokens entrée (champ natif) | 464058 |
| Tokens sortie (champ natif) | 34458 |
| Tokens raisonnement séparés | 17134 |
| Cache lecture | 10380799 |
| Cache écriture | 0 |
| Coût numérique natif | 0.077485798 ; devise N/A dans ces métadonnées |
| Compactions observées | 0 |

Les champs tokens sont conservés séparément sans supposer leur caractère additif. Quotas, coûts et performances de l’orchestrateur N/A au-delà des relevés de compte ; coût des requêtes PLLM N/A.

### Sondes de l’agent de codage

Prompt fixe : « Sonde de télémétrie. Sans outil, fichier, réseau ou raisonnement métier. Écris exactement les nombres décimaux de 1 à 400, dans cet ordre, séparés par un espace, sans autre texte. » Même modèle/fournisseur/high, session dédiée sans outils, fichiers ou réseau, une requête par relève.

| Relève | Session | Envoi | Premier texte | Dernier texte | Sortie / raisonnement | TTMT | Tokens/s visibles |
|---|---|---|---|---|---|---|---|
| début | ses_eafa7f37cffebfWlcRcUDKOkRd | 18/10/2026 20:48:30 Europe/Paris | 18/10/2026 20:48:36 Europe/Paris | 18/10/2026 20:48:38 Europe/Paris | 839 / 1549 | 6.911 s | 432.474 |
| fin | ses_eaf943c61ffeeFoyZpefCH5R8O | 18/10/2026 21:10:02 Europe/Paris | 18/10/2026 21:10:04 Europe/Paris | 18/10/2026 21:10:05 Europe/Paris | 821 / 413 | 1.913 s | 618.223 |

Débit = tokens de sortie natifs / durée premier–dernier événement texte. Moyennes arithmétiques : TTMT 4.412 s ; débit 525.349 tokens/s. TTMT min/max 1.913 / 6.911 s ; débit min/max 432.474 / 618.223.

Relèves prévues 2 (100.0 %), réussies 2 (100.0 %), échouées 0 (0.0 %), manquées 0 (0.0 %). Aucune échéance +30 minutes pendant l’activité de production bornée. Surcharge séparée : entrée 24546 tokens, sortie 1660, raisonnement 1962, cache lecture 113 ; durée calendaire cumulée des deux sondes 12.114 s ; coût numérique natif 0.003179226 (devise non fournie). Le benchmark PLLM est distinct : mode1/high valide au palier 2048, TTFT 7.4764 s et débit global 4574.064 tokens/s selon sa formule ; un essai 1024 sans réussite est conservé, aucune ancienne mesure réutilisée. Quotas fournisseur utilisés 0 % / 67 % / 98 % (5 h / semaine / mois).

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---|---|
| user | 74 | 39.4 % |
| assistant | 114 | 60.6 % |
| Total | 188 | 100.0 % |

| Type de partie | Nombre | Part |
|---|---|---|
| text | 163 | 26.5 % |
| step-start | 114 | 18.5 % |
| reasoning | 116 | 18.8 % |
| tool | 110 | 17.9 % |
| step-finish | 113 | 18.3 % |
| Total | 616 | 100.0 % |

| Terminaison assistant | Nombre | Part |
|---|---|---|
| tool-calls | 80 | 70.2 % |
| stop | 33 | 28.9 % |
| inconnue | 1 | 0.9 % |
| Total | 114 | 100.0 % |

La terminaison inconnue correspond à un message interrompu ; aucun succès n’en est déduit.

| Outil | Total | Part globale | Terminé / taux | Refus natif / taux | Erreur / taux |
|---|---|---|---|---|---|
| cgpt-validation_broker_readiness | 9 | 8.2 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 3 | 2.7 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 23 | 20.9 % | 21 (91.3 %) | 0 (0.0 %) | 2 (8.7 %) |
| bash | 11 | 10.0 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 35 | 31.8 % | 35 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 8 | 7.3 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 10 | 9.1 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 1 | 0.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_cancel_approval | 1 | 0.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 1 | 0.9 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 | 7.3 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 110 | 100.0 % | 108 (98.2 %) | 0 (0.0 %) | 2 (1.8 %) |

Les décisions CAB par famille portent 9 éditions (8 approved, 1 rejected) et 12 commandes (12 approved, dont 1 non exécutée) : 21 décisions. Une demande d’édition annulée et un prévol -32602 sont distincts de ce tableau des décisions admises.

## 3. Fichiers modifiés

Les écritures ci-dessous sont les 8 tentatives natives effectivement autorisées et terminées, pas des lignes de code ni une garantie de comportement runtime.

| Chemin absolu complet au moment de l’écriture | Écritures approuvées | Part des 8 | Refus natifs | Erreurs natives |
|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-export-consistency-kind-v1/.openspec.yaml | 1 (100.0 %) | 12.5 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-export-consistency-kind-v1/proposal.md | 1 (100.0 %) | 12.5 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-export-consistency-kind-v1/design.md | 1 (100.0 %) | 12.5 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-export-consistency-kind-v1/tasks.md | 2 (100.0 %) | 25.0 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_export_consistency_kind.py | 1 (100.0 %) | 12.5 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_export_consistency_kind.py | 1 (100.0 %) | 12.5 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_export_consistency_kind_integration.py | 1 (100.0 %) | 12.5 % | 0 (0.0 %) | 0 (0.0 %) |
| Total | 8 (100.0 %) | 100.0 % | 0 (0.0 %) | 0 (0.0 %) |

Avant outil d’écriture : une tentative CAB sur proposal.md a été refusée, une tentative .openspec.yaml a été annulée après écart de manifeste. Elles n’ont produit aucune écriture. Le rapport courant est une livraison distincte, exclue de cet intervalle.

Déplacement autorisé unique : /home/devops/datas/pixs/openspec/changes/add-initial-bulk-export-consistency-kind-v1 → /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-bulk-export-consistency-kind-v1. Les 4 contenus sont conservés exactement ; 7 fichiers attendus en UTF-8/LF, 16 fichiers préexistants contrôlés par empreinte inchangés. Aucun canon, consommateur, façade ou migration modifié. Les fichiers .pyc régénérables produits par les compilations ne sont pas lus comme sources et ne constituent pas une livraison.

## 4. Commandes

| Famille | Nombre | Part | Exit 0 | Exit non nul |
|---|---|---|---|---|
| Prévol /usr/bin/true | 2 | 18.2 % | 2 (100.0 %) | 0 (0.0 %) |
| py_compile | 3 | 27.3 % | 3 (100.0 %) | 0 (0.0 %) |
| unittest ciblé et régressions | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) |
| OpenSpec validate | 4 | 36.4 % | 2 (50.0 %) | 2 (50.0 %) |
| OpenSpec archive | 1 | 9.1 % | 1 (100.0 %) | 0 (0.0 %) |
| Total | 11 | 100.0 % | 9 (81.8 %) | 2 (18.2 %) |

Libellés tronqués à 100 caractères maximum ; toutes les commandes natives exécutées sont recensées par occurrences.

| Commande exécutée | Occurrences | Part |
|---|---|---|
| /usr/bin/true | 2 | 18.2 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_export_consistency_ki… | 1 | 9.1 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_export_consistency_kin… | 1 | 9.1 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_export_consiste… | 1 | 9.1 % |
| /usr/bin/env PYTHONPATH=src:tests:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unitte… | 1 | 9.1 % |
| /home/devops/.local/npm/bin/openspec validate add-initial-bulk-export-consistency-kind-v1 --strict | 1 | 9.1 % |
| /home/devops/.local/npm/bin/openspec validate --all | 1 | 9.1 % |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 | 18.2 % |
| /home/devops/.local/npm/bin/openspec archive add-initial-bulk-export-consistency-kind-v1 --skip-spe… | 1 | 9.1 % |

Commandes refusées : aucune décision rejected sur une commande (0/12, 0.0 %) ; le seul refus CAB est une édition. Une demande de validation ciblée approved a été annulée avant effet pour révision STALE, puis remplacée sous identifiants neufs. L’archivage n’a été exécuté qu’une fois. Les erreurs de contrôle HTTP restent distinctes des commandes exécutées.

## 5. Accès web

| Statut des outils web dans les sessions de production | Nombre | Part |
|---|---|---|
| Approuvé et exécuté | 0 | N/A — dénominateur zéro |
| Refusé | 0 | N/A — dénominateur zéro |
| Erreur | 0 | N/A — dénominateur zéro |
| Total | 0 | N/A — dénominateur zéro |

Aucun outil web ni URL visitée par l’agent de codage dans l’intervalle. Les appels techniques du processus PLLM sont séparés : accès authentifiés approuvés à https://opencode.ai/zen/go/v1/usage, https://opencode.ai/zen/go/v1/models et https://opencode.ai/zen/go/v1/responses. Les deux sondes utilisent l’API OpenCode locale ; elles n’autorisent aucun outil réseau au modèle. Aucun contenu sensible n’est reproduit.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 18/10/2026 20:47:13 Europe/Paris |
| Fin — après archivage | 18/10/2026 21:10:52 Europe/Paris |
| Durée globale (pauses et attentes incluses) | 00 h 23 min 38 s |

La durée comprend tests, attentes et archivage ; elle exclut la rédaction ultérieure du rapport et la clôture.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 18/10/2026 20:47:13 Europe/Paris | 19 % | 25/10/2026 01:23:28 Europe/Paris |
| Après — après archivage de la spécification | 18/10/2026 21:10:52 Europe/Paris | 27 % | 25/10/2026 01:23:28 Europe/Paris |
| Différence après − avant | — | 8 points de pourcentage | — |

Source native mcp__codex_app__get_usage_limits, quota codex, fenêtre 10080 minutes ; compte et réinitialisation identiques. Quota partagé par le compte : cette variation peut inclure d’autres tâches simultanées et n’est pas attribuée exclusivement à ce RUN.

| Domaine des outils natifs | Total | Part globale | Terminé autorisé / taux | Refus natif / taux | Erreur / taux |
|---|---|---|---|---|---|
| Fichiers écrits | 8 | 7.3 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 11 | 10.0 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres : CAB et lectures/recherches | 91 | 82.7 % | 89 (97.8 %) | 0 (0.0 %) | 2 (2.2 %) |
| Total | 110 | 100.0 % | 108 (98.2 %) | 0 (0.0 %) | 2 (1.8 %) |

Le total global 110 se recoupe avec la somme par outil et par domaine ; le refus CAB pré-natif reste compté dans ses 21 décisions, sans doubler les outils. Les 2 sorties strictes non nulles ne sont pas masquées dans les 11 commandes terminées.

CAB : publication technique reçue `publish-77dbb4ccf3554e3f9ef5`, référence 42, passage REPORT limité à ce seul STATISTIQUES.md. Brouillon CAB consulté en lecture seule puis complété depuis l’historique natif borné : ses 105 outils observés SSE sont partiels face aux 110 appels HTTP natifs terminés ; les sources ne sont pas additionnées. Attente ressource observée 31.653 s, détention partagée 433.989 s, aucun gel global ; ces durées peuvent se recouvrir. Les erreurs HTTP de coordination et les métriques busy/idle ne prouvent ni échec métier ni temps productif.

Tests et syntaxe prouvés ; archive unique prouvée ; strict global limité par les quatre WARNING historiques. Git non inspecté et aucune action Git autorisée. Aucun secret n’a été affiché, journalisé ou copié dans les fichiers livrés ; l’accès PLLM reste dans le processus sécurisé. Le vocabulaire est une représentation seule et ne réalise aucun export ni résolution de consistance. Le cycle global Pixs reste incomplet. Gate et arrêt ciblé sont à vérifier après l’écriture et la revue du présent rapport ; leur réussite n’est pas anticipée ici.
