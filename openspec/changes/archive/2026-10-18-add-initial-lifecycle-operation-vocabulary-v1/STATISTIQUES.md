# Statistiques — add-initial-lifecycle-operation-vocabulary-v1

RUN : cismp1-pixs-ebdf111060144304 ; contexte CAB : 307 ; session native principale : ses_eb078dd0dffeTYYhVByMoTRd7h.

Fenêtre figée du début effectif de ce RUN au relevé final après archivage. Source principale : historique HTTP natif complet de la session, confronté aux agrégats CAB 1.3.0 filtrés par RUN/contexte et à leurs brouillons JSON/Markdown. La rédaction du présent rapport et la clôture ultérieure sont hors fenêtre ; aucune opération ultérieure ne complète rétroactivement les comptes. Les sessions techniques de sélection et de sondes sont identifiées séparément. Aucun historique exclu ni secret lu par le modèle.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A — version exacte non exposée | OpenCode Go (opencode-go) | high | 2.643 s | 736.131 (sondes) | N/A — temps de génération complet non isolable |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex / GPT-6 | N/A — version exacte non exposée | OpenAI | N/A — réglage non exposé | N/A — non sondé | N/A — non sondé | N/A — télémétrie de service indisponible |

Le dénominateur du temps de service cumulé est indisponible ; durée calendaire, busy, attente CAB et durée des outils ne sont pas convertis en service LLM. Les métadonnées natives confirment le fournisseur, le modèle et high pour toutes les réponses de codage. Aucun modèle de repli utilisé.

## 1. Statistiques générales et décisions

Durée globale : 00 h 20 min 05 s, pauses, attente de permission, tests et archivage inclus. Nouveau vocabulaire LifecycleOperation : onze valeurs canoniques, sans modification de la machine existante.

| Résultat observé | Valeur | Part ou limite |
| --- | --- | --- |
| Tests ciblés et régressions | 25 réussis / 25 | 100.0 % ; 0 échec, 0 ignoré |
| Fichiers compilés | 3 / 3 | 100.0 % ; code 0 |
| OpenSpec ciblé strict | 1 / 1 | 100.0 % ; code 0 |
| OpenSpec global standard avant archive | 186 / 186 | 100.0 % ; code 0 |
| OpenSpec global strict avant archive | 184 / 186 | 98.9 % ; code 1 |
| OpenSpec global strict après archive | 183 / 185 | 98.9 % ; code 1 |
| Archive unique | 1 / 1 | 100.0 % ; code 0 |
| Outils natifs terminés sans erreur technique | 75 / 76 | 98.7 % |
| Erreurs techniques natives | 1 / 76 | 1.3 % |

Les deux sorties strictes globales conservent exactement quatre WARNING historiques de longueur (bulk-operations exigences 6/10/13 ; identity-assurance exigence 4), zéro ERROR. Le strict global reste en échec ; aucune réussite stricte globale revendiquée ni correction hors périmètre. L’unique erreur technique native est une lecture du dossier du change avant sa création, sans effet. Aucun échec de test.

| Décision CAB | Nombre | Part des décisions |
| --- | --- | --- |
| Approuvé | 16 | 100.0 % |
| Refusé | 0 | 0.0 % |
| Clarification | 0 | 0.0 % |
| En attente | 0 | 0.0 % |
| Total | 16 | 100 % |

16 permissions natives once correspondent aux 16 opérations exécutées. Un outil terminé signifie exécuté avec succès technique, sans prouver à lui seul une approbation manuelle ; les lectures/recherches ne reçoivent pas de permission manuelle. Les écritures et commandes disposent de décisions explicites CGPT corrélées. Un code de commande non nul est distingué d’un refus et d’une erreur technique de l’outil.

| Compteur natif cumulé de production | Valeur |
| --- | --- |
| total | 9462434 |
| input | 330150 |
| output | 27502 |
| reasoning | 8202 |
| cache.read | 9096580 |
| cache.write | 0 |

Ces compteurs sont cumulés par réponse, avec répétition du contexte ; le total natif inclut le cache et ne mesure pas des tokens uniques. Coût déclaré natif : 0.05834896 (devise/valorisation abonnement N/A). Coût réel fournisseur et coût orchestrateur : N/A. Compactions natives dans la fenêtre : 0 ; échéance de 1 h 30 non atteinte.

### Sondes et contrôle PLLM

| Relève | Session | TTMT (s) | Tokens/s | Sortie / raisonnement | Statut |
| --- | --- | --- | --- | --- | --- |
| début | ses_eb07b9f8bffeKoauZujUyQwPr7 | 3.377 | 933.673 | 366 / 819 | réussie |
| fin | ses_eb06ab848ffelXAVryMFFWd4m3 | 1.910 | 538.588 | 328 / 199 | réussie |

2 relèves prévues, 2 réussies (100.0 %), 0 échouée (0.0 %), 0 manquée (0.0 %). Aucune échéance +30 min avant la fin. Prompt identique : « Écris exactement les nombres de 1 à 160 séparés par un espace, sans autre texte. » Sessions dédiées sans outil, fichier ni réseau. TTMT min/max : 1.910 / 3.377 s ; débit min/max : 538.588 / 933.673.
Instants d’envoi, premier texte et dernier texte issus des horodatages natifs OpenCode conservés au checkpoint. Précision et buffering du transport inconnus, sans chronométrie monotone indépendante du premier delta SSE ; ces débits de sortie observés ne sont pas une mesure matérielle du modèle. Aucune sonde orchestrateur.
Surcharge des deux sondes : 29627 tokens natifs cumulés, dont 694 de sortie et 1018 de raisonnement ; coût/durée active isolée N/A. Cette surcharge est exclue de la production ci-dessus.
PLLM mode 1 imposée, high : quotas Go initiaux utilisés 2 % / 66 % / 98 % (5 h / semaine / mois). Deux requêtes de benchmark : flux incomplet à 1024, puis succès à 2048 après nouveau contrôle des quotas. TTFT de contenu 7.271 s ; débit global convention PLLM 3977.648 tokens/s (raisonnement et réponse, fenêtre de génération 0.4095 s, fortement dépendant du buffering) ; 1630 tokens de sortie natifs dont 1431 de raisonnement. Surcharge benchmark séparée ; pas de substitution à une sonde statistique. Authentification utilisée uniquement dans le processus sécurisé, jamais transmise au modèle.
Session de sélection technique distincte : ses_eb07b6ec4ffea2N3m9vBAleS3x (lecture seule, exclue de la fenêtre native principale de production et des agrégats CAB du contexte). Ses tokens/service ne sont pas répartis arbitrairement sur le change.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| assistant | 68 | 76.4 % |
| user | 21 | 23.6 % |
| Total | 89 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| reasoning | 66 | 18.6 % |
| step-finish | 68 | 19.2 % |
| step-start | 68 | 19.2 % |
| text | 76 | 21.5 % |
| tool | 76 | 21.5 % |
| Total | 354 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| stop | 19 | 27.9 % |
| tool-calls | 49 | 72.1 % |
| Total | 68 | 100 % |

| Outil | Total | Part | Terminé | Taux terminé | Refusé | Taux refus | Erreur | Taux erreur |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bash | 8 | 10.5 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_health | 1 | 1.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 3 | 3.9 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_list_pending | 1 | 1.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 16 | 21.1 % | 16 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 13 | 17.1 % | 13 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 1 | 1.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 25 | 32.9 % | 24 | 96.0 % | 0 | 0.0 % | 1 | 4.0 % |
| write | 8 | 10.5 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 76 | 100 % | 75 | 98.7 % | 0 | 0.0 % | 1 | 1.3 % |

Le brouillon CAB initial avait une observation cab-mcp encore en cours ; la relecture native et l’agrégat final concordent désormais : 76 appels, 75 terminés, 1 erreur, zéro pending/running. Les métriques antérieures ne sont pas transformées en effets inconnus actuels.

## 3. Fichiers modifiés

Comptes de tentatives d’écriture natives dans la fenêtre ; déplacements par archive détaillés séparément. Les écritures de bytecode dues à py_compile sont un effet de commande connu, pas des appels write supplémentaires.
| Chemin absolu actuel | Tentatives | Part | Approuvées | Taux | Refusées | Taux refus | Erreurs | Taux erreur |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-lifecycle-operation-vocabulary-v1/.openspec.yaml | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-lifecycle-operation-vocabulary-v1/design.md | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-lifecycle-operation-vocabulary-v1/proposal.md | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-lifecycle-operation-vocabulary-v1/tasks.md | 2 | 25.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/kernel/lifecycle/operation.py | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_lifecycle_operation_integration.py | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_lifecycle_operation.py | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 8 | 100 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les quatre artefacts ont été déplacés une seule fois de /home/devops/datas/pixs/openspec/changes/add-initial-lifecycle-operation-vocabulary-v1 vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-lifecycle-operation-vocabulary-v1. Les empreintes avant/après déplacement sont identiques. Trois nouveaux fichiers Python ; aucune modification des fichiers existants de cycle de vie, façades, cadrages ou canon contrôlés. /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-lifecycle-operation-vocabulary-v1/STATISTIQUES.md est rédigé ensuite sous mandat distinct et son écriture est hors fenêtre.

## 4. Commandes

| Famille | Occurrences | Part | Autorisées/exécutées | Taux refus | Taux erreur outil |
| --- | --- | --- | --- | --- | --- |
| Compilation Python | 1 | 12.5 % | 1 (100.0 %) | 0.0 % | 0.0 % |
| OpenSpec | 5 | 62.5 % | 5 (100.0 %) | 0.0 % | 0.0 % |
| Prévol sans effet | 1 | 12.5 % | 1 (100.0 %) | 0.0 % | 0.0 % |
| Tests Python | 1 | 12.5 % | 1 (100.0 %) | 0.0 % | 0.0 % |
| Total | 8 | 100 % | 8 (100.0 %) | 0.0 % | 0.0 % |

| Commande (100 caractères maximum) | Occurrences | Part | Code natif |
| --- | --- | --- | --- |
| /usr/bin/true | 1 | 12.5 % | 0 × 1 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/lifecycle/operation.py test… | 1 | 12.5 % | 0 × 1 |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /home/devops/datas/pixs/.venv/bin/python3 -… | 1 | 12.5 % | 0 × 1 |
| /home/devops/.local/npm/bin/openspec validate add-initial-lifecycle-operation-vocabulary-v1 --strict | 1 | 12.5 % | 0 × 1 |
| /home/devops/.local/npm/bin/openspec validate --all | 1 | 12.5 % | 0 × 1 |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 | 25.0 % | 1 × 2 |
| /home/devops/.local/npm/bin/openspec archive add-initial-lifecycle-operation-vocabulary-v1 --yes --… | 1 | 12.5 % | 0 × 1 |
| Total | 8 | 100 % | 6 × 0 ; 2 × 1 |

Commandes refusées : aucune (0 / 8, 0.0 %). Six commandes retournent 0 (75.0 %), deux contrôles stricts globaux retournent 1 (25.0 %) pour les seuls WARNING décrits ; aucun échec de test ni erreur technique de Bash. Les commandes exactes complètes et leurs requestId sont conservés dans le checkpoint, sans wrapper ni regroupement.

## 5. Accès web

| Accès web de production par l’agent | Nombre | Part ou taux |
| --- | --- | --- |
| Approuvé et visité | 0 | N/A — dénominateur nul |
| Refusé | 0 | N/A — dénominateur nul |
| Erreur | 0 | N/A — dénominateur nul |
| Total | 0 | N/A — dénominateur nul |

Aucun outil web ni URL visité/refusé dans la session de production. Les API techniques de pilotage locales (OpenCode/CAB) sont distinctes de la navigation web.
Accès fournisseur de prévol hors production, approuvés : https://opencode.ai/zen/go/v1/usage (2 consultations), https://opencode.ai/zen/go/v1/models (1 consultation), https://opencode.ai/zen/go/v1/responses (2 requêtes : 1 flux incomplet puis 1 réussite). Aucune URL refusée ; aucun accès à un autre fournisseur. Ces 5 requêtes techniques autorisées sont séparées des 0 accès web de production. Le contenu de code nécessaire à la session est transmis à OpenCode Go selon l’accord Pixs ; aucune donnée secrète dans les prompts.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-18T14:56:24.959385+00:00 |
| Fin — après archivage | 2026-10-18T15:16:30.853797+00:00 |
| Durée globale (pauses et attentes incluses) | 00 h 20 min 05 s |

Horodatages UTC, consignés localement ; la fin correspond au relevé final du quota et précède la rédaction du rapport.
| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-18T14:56:24.959395+00:00 | 13 % | 2026-10-24T23:23:28+00:00 |
| Après — après archivage de la spécification | 2026-10-18T15:16:30.853797+00:00 | 14 % | 2026-10-24T23:23:28+00:00 |
| Différence après − avant | — | 1 point de pourcentage | — |

Source des deux relevés : mcp__codex_app__get_usage_limits, rateLimitsByLimitId.codex, fenêtre 10080 minutes, même compte et même resetsAt. Le compteur est partagé : la différence peut inclure d’autres tâches simultanées et ne mesure pas une consommation exclusive de ce RUN. Aucune conversion en tokens ou en euros.
| Domaine | Total | Part globale | Terminé | Taux terminé | Refusé | Taux refus | Erreur | Taux erreur |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Fichiers | 8 | 10.5 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 8 | 10.5 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| Autres outils | 60 | 78.9 % | 59 | 98.3 % | 0 | 0.0 % | 1 | 1.7 % |
| Global | 76 | 100 % | 75 | 98.7 % | 0 | 0.0 % | 1 | 1.3 % |

Coordination CAB finale filtrée : 16 décisions approuvées et 16 once ; zéro validation indécise, active ou permission native parasite. Publication durable publish-2236d735b8f84cae ; référence 38. Les durées de détention, busy, attente et effets de CAB peuvent se recouvrir et ne s’additionnent pas comme temps productif.
Résultat du change : onze opérations canoniques passives ; 25 tests et trois compilations réussis ; OpenSpec ciblé strict et global standard réussis. Strict global avant/après archive en échec uniquement pour quatre WARNING historiques, zéro ERROR. Archivage unique exécuté et contrôlé. Git non inspecté, aucun commit/push autorisé ni exécuté. Aucun effet externe métier ; pas de PostgreSQL/frontend nécessaires à ce vocabulaire. Les contenus écrits et relus sont statiques, sans secret ; la clé PLLM reste dans son processus sécurisé.
La publication technique est prouvée ; la validation du présent rapport, le gate, le désarmement, la libération et l’arrêt ciblé suivent hors fenêtre et sont tracés au checkpoint /home/devops/datas/pixs/output/cismp/cismp1-pixs-ebdf111060144304/state.json. Ce rapport ne prétend pas prouver une fin globale du projet : cycle_global_complete=false.
