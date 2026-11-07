# Statistiques — add-initial-component-type-vocabulary-v1

RUN `cismp1-pixs-36e5c75c22864406`, contexte CAB 325, racine `/home/devops/datas/pixs`. Agent de codage : sessions `ses_eafa94879ffe6fqK7hIfJbdQso` (sélection) et `ses_eafa718e2ffegGj563L9SW45HT` (change). CAB 1.3.0, OpenCode 1.19.3, PLLM mode 1, Muse high.

Sources : historique natif complet des deux sessions, agrégats JSON/Markdown GET /runs/cismp1-pixs-36e5c75c22864406/statistics, deux sondes dédiées, relevés natifs get_usage_limits avant et après, preuves du checkpoint. Les agrégats CAB portent seulement sur la session réservée ; la sélection antérieure est ajoutée explicitement dans les totaux natifs ci-dessous. Les sondes, le benchmark et la rédaction de ce rapport restent hors production.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor | N/A — version distincte non exposée | opencode-go | high | 1.501 s | 613.823 | 59.323 s (100,0 % des durées connues) |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — configuration exacte non exposée | OpenAI | N/A — non exposé | N/A — non sondé | N/A — non sondé | N/A — non mesurable |

Le temps de service est la somme des intervalles natifs text/reasoning mesurables, fusionnés par réponse ; il ne représente pas la durée calendaire ni l’ensemble du temps de calcul interne. Les durées absentes sont exclues du dénominateur, non estimées. Les sessions de production ont été successives. Le nom Muse 1.3 ne remplace pas une version télémétrique absente.

## 1. Statistiques générales et décisions

Durée calendaire : 00 h 19 min 54 s, pauses, attentes, tests et archivage inclus. Fenêtre achevée avant rédaction du rapport.

| Mesure native, sélection + change | Nombre | Part |
|---|---:|---:|
| Messages utilisateur | 42 | 25.8 % |
| Messages assistant | 121 | 74.2 % |
| Total messages | 163 | 100,0 % |
| Outils terminés | 127 | 98.4 % |
| Outils en erreur technique | 2 | 1.6 % |
| Total outils | 129 | 100,0 % |

| Décisions CAB du contexte 325 | Nombre | Part |
|---|---:|---:|
| Approuvées | 18 | 94.7 % |
| Refusées | 1 | 5.3 % |
| Clarification / attente | 0 | 0,0 % |
| Total | 19 | 100,0 % |

16 permissions natives once, pour 16 effets natifs : 8 écritures et 8 commandes. Les deux autres décisions approuvées ont été annulées avant effet (lecture globale trop large en attente ; archivage STALE). Le refus CAB porte sur un mandat de validation globale devenu périmé avant décision. Deux erreurs MCP de transport/attente restent des erreurs techniques, distinctes du refus et des deux sorties strictes code 1 pour avertissements. Aucun refus de permission native observé. Une réussite d’outil ne prouve pas une approbation manuelle ; les lectures/recherches n’exigeaient pas once.

Télémétrie fournisseur de production : entrées 523 297 ; sorties 34 611 ; raisonnement 16 660 ; cache lu 16 651 384 ; cache écrit 0 ; coût rapporté 0,095886668 $. Les catégories sont conservées séparément sans transformer le quota en tokens ou en euros. Compactions visibles : 0 ; absence de preuve des compactions internes non exposées.

Résultats : trois fichiers Python compilés (code 0), 19/19 tests réussis, ciblé OpenSpec strict code 0 ; global standard 187/187 code 0. Global strict avant archive : 185/187, code 1 ; après archive : 184/186, code 1. Exactement quatre WARNING de longueur (bulk-operations exigences 6/10/13, identity-assurance exigence 4), zéro ERROR. Les avertissements préexistants ne sont pas présentés comme un succès strict. Aucun canon hors périmètre corrigé. Archive unique et publication CAB référence 41 prouvées ; ce vocabulaire passif ne livre pas le profil P0 global.

| Sonde dédiée | TTMT réponse | Tokens/s réponse | Sorties | Résultat |
|---|---:|---:|---:|---|
| début | 1.157 s | 845.361 | 328 | valide |
| fin | 1.846 s | 382.284 | 328 | valide |
| Moyenne des 2 sondes | 1.501 s | 613.823 | 656 au total | 2/2, 100,0 % |

Prévues 2, réussies 2 (100,0 %), échouées 0, manquées 0 ; aucune échéance +30 min n’était atteinte entre sondes. Prompt constant : « Sans outil, sans fichier et sans réseau. Réponds seulement avec les entiers de 1 à 160, séparés par un espace, sans commentaire. ». TTMT mesuré de l’envoi au début du premier texte natif ; débit = tokens de sortie fournis / durée premier-dernier texte. TTMT min/max 1.157/1.846 s ; débit min/max 382.284/845.361. Surcharge distincte : 656 tokens de sortie, 251 de raisonnement et 0,002972 $ ; aucune attribution à la production.

Prévol PLLM frais : quotas 5 h 0 %, semaine 67 %, mois 98 % utilisés ; Muse high disponible ; palier 1 024 réussi, TTFT 2,2409 s et débit global fournisseur 3 495,751 tokens/s (raisonnement inclus). Ce débit global de benchmark ne se confond pas avec le débit de réponse des sondes.

## 2. Types de messages et d’outils

| Parties natives | Nombre | Part |
|---|---:|---:|
| text | 130 | 20.8 % |
| step-start | 120 | 19.2 % |
| reasoning | 127 | 20.3 % |
| tool | 129 | 20.6 % |
| step-finish | 120 | 19.2 % |
| Total | 626 | 100,0 % |

Terminaisons des 121 réponses : tool-calls 81 (66.9 %), stop 39 (32.2 %), terminaison non exposée 1 (0.8 %). Cette lacune n’est pas transformée en réussite.

| Type d’outil | Total | Part globale | Terminé, taux ligne | Refus natif, taux ligne | Erreur, taux ligne |
|---|---:|---:|---:|---:|---:|
| cab-mcp | 28 | 21.7 % | 26 (92.9 %) | 0 (0,0 %) | 2 (7.1 %) |
| todowrite | 7 | 5.4 % | 7 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| read | 55 | 42.6 % | 55 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| glob | 12 | 9.3 % | 12 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| grep | 11 | 8.5 % | 11 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| bash | 8 | 6.2 % | 8 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| write | 8 | 6.2 % | 8 (100.0 %) | 0 (0,0 %) | 0 (0.0 %) |
| Total | 129 | 100,0 % | 127 (98.4 %) | 0 (0,0 %) | 2 (1.6 %) |

## 3. Fichiers modifiés

Tentatives natives d’écriture, et non lignes de diff. Les quatre chemins OpenSpec d’origine ont ensuite été déplacés par l’unique commande d’archivage dans `/home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-component-type-vocabulary-v1`.

| Chemin absolu de la tentative | Approuvé et exécuté, part des 8 écritures | Refus, taux ligne | Erreur, taux ligne |
|---|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-component-type-vocabulary-v1/.openspec.yaml | 1 (12.5 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-component-type-vocabulary-v1/proposal.md | 1 (12.5 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-component-type-vocabulary-v1/design.md | 1 (12.5 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-component-type-vocabulary-v1/tasks.md | 2 (25.0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/component_type.py | 1 (12.5 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_component_type.py | 1 (12.5 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_component_type_integration.py | 1 (12.5 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 8 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

Toutes les tentatives listées sont réussies (100,0 % de chaque ligne). Ce rapport est une neuvième écriture sous mandat distinct, hors fenêtre de production ci-dessus, dans `/home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-component-type-vocabulary-v1/STATISTIQUES.md`. Les sept fichiers produits et les tâches sont relus par contenu/empreinte ; dix fichiers existants de cadrage, canon et façade sont inchangés par SHA-256. Sans inspection Git, la provenance des autres modifications concurrentes n’est pas attribuée à ce RUN.

## 4. Commandes

Les libellés affichés sont bornés à 100 caractères ; les commandes exactes sont conservées dans les mandats et le checkpoint.

| Commande/famille | Occurrences | Part | Approuvé et exécuté, taux ligne | Refus natif | Erreur d’outil |
|---|---:|---:|---:|---:|---:|
| /usr/bin/true | 1 | 12.5 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/component_type.py tests/uni… | 1 | 12.5 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=src:tests/unit:tests/integration /home/d… | 1 | 12.5 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/.local/npm/bin/openspec validate add-initial-component-type-vocabulary-v1 --strict | 1 | 12.5 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/.local/npm/bin/openspec validate --all | 1 | 12.5 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 | 25.0 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-component-type-vocabulary-v1 --yes | 1 | 12.5 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 8 | 100,0 % | 8 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

Deux des huit commandes (25.0 %) retournent code 1 : les contrôles globaux stricts et leurs seuls avertissements historiques. Les six autres retournent code 0 (75.0 %). Une commande refusée par CAB avant exécution : validation globale standard sur révision périmée, 1/19 décisions (5.3 %), sans appel Bash. Autres annulations sans effet : un accès global trop large et un accès d’archivage STALE ; l’archivage effectif n’a eu lieu qu’une fois. Le contrôleur signale aussi une admission decision-run-divergent et deux resource-revision-stale, distinctes des effets natifs.

## 5. Accès web

Aucun outil natif de navigation, recherche web ou webfetch dans la production : 0 accès, refus 0, erreurs 0 ; taux N/A faute de dénominateur. Les appels loopback OpenCode/CAB sont du transport de pilotage, pas des pages visitées.

Les seuls accès HTTPS directs mesurés par l’orchestrateur pour le prévol PLLM sont séparés de la production :

| URL effectivement appelée | Nombre | Part | Approuvé/exécuté | Refus | Erreur |
|---|---:|---:|---:|---:|---:|
| https://opencode.ai/zen/go/v1/usage | 1 | 33,3 % | 1 (100,0 %) | 0 | 0 |
| https://opencode.ai/zen/go/v1/models | 1 | 33,3 % | 1 (100,0 %) | 0 | 0 |
| https://opencode.ai/zen/go/v1/responses | 1 | 33,3 % | 1 (100,0 %) | 0 | 0 |
| Total prévol hors production | 3 | 100,0 % | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

Aucune URL refusée observée. Le transport fournisseur des sessions et sondes n’est pas assimilé à de la navigation web ; ses requêtes internes ne sont pas dénombrées sans télémétrie dédiée. Aucun en-tête d’authentification, identifiant de compte ou secret n’est conservé.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 18/10/2026 20:46:37 Europe/Paris |
| Fin — après archivage | 18/10/2026 21:06:32 Europe/Paris |
| Durée globale, pauses et attentes incluses | 00 h 19 min 54 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé/consignation | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 18/10/2026 20:46:37 Europe/Paris | 19 % | 25/10/2026 01:23:28 Europe/Paris |
| Après — après archivage | 18/10/2026 21:06:32 Europe/Paris | 25 % | 25/10/2026 01:23:28 Europe/Paris |
| Différence après − avant | — | +6 points de pourcentage | — |

Relevés directs get_usage_limits, quota codex, fenêtre 10 080 minutes, même compte et même réinitialisation. Le quota est partagé : sa variation pendant la session peut inclure les autres chats simultanés ; aucune attribution exclusive à ce RUN, aucune conversion en tokens ou en euros. La rédaction ultérieure du rapport est hors intervalle.

| Domaine natif de production | Total | Part globale | Terminé | Refus natif | Erreur |
|---|---:|---:|---:|---:|---:|
| Écritures | 8 | 6.2 % | 8 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Commandes | 8 | 6.2 % | 8 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| CAB MCP | 28 | 21.7 % | 26 (92.9 %) | 0 (0,0 %) | 2 (7.1 %) |
| Lecture/recherche/suivi | 85 | 65.9 % | 85 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Web natif | 0 | 0,0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 129 | 100,0 % | 127 (98.4 %) | 0 (0,0 %) | 2 (1.6 %) |

Totaux croisés : 8 + 8 + 28 + 85 = 129 outils ; 127 terminés + 2 erreurs = 129 ; 18 décisions approuvées + 1 refusée = 19 ; 16 once = 8 écritures + 8 commandes. Les pourcentages arrondis peuvent ne pas sommer exactement 100 %. CAB observe 114,475 s d’attente de ressources et 298,318 s de détention partagée ; ces durées peuvent se recouvrir et ne s’ajoutent pas au temps de génération. Aucune exclusion globale CAB n’a été demandée.

Tests et compilation conformes ; archive unique effective et publication durable référence 41. Le strict global conserve explicitement ses quatre avertissements et son code 1. PostgreSQL/frontend sans objet pour le vocabulaire pur. Git non inspecté et aucune opération Git autorisée. Accès externes limités au fournisseur autorisé ; secrets maintenus dans le processus sécurisé, jamais transmis au modèle ni écrits dans les sources. La vérification de ce rapport précède gate, désarmement et arrêt ciblé ; ces opérations de clôture ne sont pas prétendues achevées par le présent rapport. Le cycle global demeure incomplet.
