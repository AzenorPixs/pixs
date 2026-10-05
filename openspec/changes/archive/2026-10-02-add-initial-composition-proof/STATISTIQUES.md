# STATISTIQUES — add-initial-composition-proof

Périmètre : /home/devops/datas/pixs. Début 2026-10-02T02:19:28.403492+00:00 ; fin après archivage et sonde finale 2026-10-02T03:19:47.691340+00:00. Bornes fixées avant rédaction : la publication de ce rapport et sa vérification sont exclues des comptages de production. Historique API complet de toutes les sessions de travail listées ci-dessous ; sondes jetables exclues. Aucun journal ni source sensible utilisé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version modèle non exposée | opencode-go | high | 5.013 s | 185.668 | 907.076 s mesurables ; part N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex | N/A — télémétrie non exposée | OpenAI | N/A — télémétrie non exposée | N/A — aucune sonde orchestrateur | N/A | N/A |

Temps de service limité aux intervalles text/reasoning horodatés et fusionnés par réponse ; outils, attentes et durée calendaire exclus. Service orchestrateur absent : dénominateur global indisponible, parts N/A. Les sondes seules fondent TTMT et débit moyens ; version non déduite du nom. Activités de production et sondes peuvent se chevaucher ; leurs durées ne sont pas additionnées au calendrier.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part/taux |
|---|---|---|
| Messages | 120 | 100 % |
| Appels outils | 97 | 100 % |
| Approuvé et exécuté | 97 | 100.0 % |
| Refusés explicites | 0 | 0.0 % |
| Erreurs techniques/protocole | 0 | 0.0 % |
| Durée calendaire avec pauses | 01 h 00 min 19 s | 100 % de l’intervalle |

| Erreur de réponse fournisseur hors outil | Nombre | Part des réponses assistants |
|---|---|---|
| Réponses avec erreur API native | 1 | 1.1 % |
| Dont HTTP 503 | 1 | 1.1 % |

Convention : « approuvé et exécuté » signifie appel terminé avec succès, autorisé automatiquement ou manuellement. Ce résultat ne prouve pas une approbation manuelle. Une réponse MCP terminale indique une décision distincte de l’exécution native. Seuls les refus explicitement enregistrés sont des refus ; interruption, invalid tool, test échoué et écart de protocole sont des erreurs. Une réussite native hors cible resterait une erreur de protocole, jamais une exécution autorisée.

| Télémétrie production | Valeur | Part |
|---|---|---|
| cache_read | 11755194 | 90.9 % |
| cache_write | 0 | 0.0 % |
| input | 1092460 | 8.4 % |
| output | 48656 | 0.4 % |
| reasoning | 41129 | 0.3 % |
| total | 12937439 | 100 % du total API |

Coût agrégé API : 0.150713388 (100 % du coût de production observé ; unité native API). Total API, cache et tokens input/output/reasoning sont conservés tels quels et ne sont pas recomposés lorsqu’ils se recouvrent. Compactions : 0 (part 0.0 % des parties).

| Décision MCP unique par requestId | Nombre | Part |
|---|---|---|
| APPROVED | 18 | 100.0 % |
| TOTAL | 18 | 100 % |

Résultats finaux : 605 tests unitaires et 174 tests d’intégration réels sous mandats distincts exit 0. Import helper pur Django bloqué sans tentative, dix gardes FS/PG2/socket2 zéro ; appels valides/négatifs FS6/PG3/socket2/setup/configure zéro, settings.configured et apps.ready faux. Pipeline discover/validate/resolve réellement instrumenté, double appels et six permutations byte-identiques, données minimales/JSON canonique/omission metadata vérifiés ; type exact et pièges de subclasses non invoqués, négatifs UTF8/taille/schema/identités/rôles/dépendance/cycle avec erreurs génériques sans raw, resolve atteint pour dépendance et cycle. Caller intégration a lu seulement les trois manifests réels avant gardes FS et a comparé ordre/arêtes à resolve public réel. AST Python 3.11 trois sources et quatre snippets, UTF8/LF, 65 empreintes et dist3 intacts. Validation stricte avant/après cochage valid true 0 issues ; huit tâches prouvées et archivage skip-specs exit 0, delta Preuve reproductible exactement canonique. Pas de preuve conformité/profil/activation/P0/readiness globale ; aucun serveur/browser nécessaire pour ce helper pur.

## 2. Types de messages et d’outils

Rôles :

| Type | Nombre | Part |
|---|---|---|
| assistant | 91 | 75.8 % |
| user | 29 | 24.2 % |
| TOTAL | 120 | 100 % |

Types de parties :

| Type | Nombre | Part |
|---|---|---|
| reasoning | 170 | 33.7 % |
| step-finish | 90 | 17.9 % |
| step-start | 90 | 17.9 % |
| text | 57 | 11.3 % |
| tool | 97 | 19.2 % |
| TOTAL | 504 | 100 % |

Terminaisons assistants :

| Type | Nombre | Part |
|---|---|---|
| absent | 1 | 1.1 % |
| stop | 28 | 30.8 % |
| tool-calls | 62 | 68.1 % |
| TOTAL | 91 | 100 % |

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| bash | 8 | 8.2 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 3 | 3.1 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 18 | 18.6 % | 18 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 1 | 1.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| glob | 3 | 3.1 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 55 | 56.7 % | 55 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 9 | 9.3 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 97 | 100 % | 97 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Couverture historique :

| Session OpenCode | Messages dans bornes | Historique complet demandé |
|---|---|---|
| ses_f05b5f016ffezu6AlQZxDwC27H | 24 | oui |
| ses_f0585b3f8ffemDsCc37O0oMydP | 96 | oui |

## 3. Fichiers modifiés

| Chemin absolu complet | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-initial-composition-proof/.openspec.yaml | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-composition-proof/design.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-composition-proof/proposal.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-composition-proof/specs/reference-composition/spec.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-composition-proof/tasks.md | 2 | 20.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/README.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/composition_proof.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_initial_composition_proof_integration.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_initial_composition_proof.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 10 | 100 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les chiffres comptent les tentatives natives d’écriture, pas des fichiers distincts. 9 chemins distincts (100.0 %). Archivage distinct par commande : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-initial-composition-proof. Aucun déplacement manuel. STATISTIQUES.md est publié après ces bornes sous son propre mandat ; il ne se compte pas lui-même.

## 4. Commandes

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| OpenSpec | 4 | 50.0 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Prévol true | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python vérification | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests intégration | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unitaires | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 8 | 100 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes observées, libellés bornés à 100 caractères :

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| [1] /usr/bin/true | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [2] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 3 | 37.5 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [3] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [4] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src TMPDIR=/… | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [5] /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/de… | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| [6] /usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETR… | 1 | 12.5 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| TOTAL | 8 | 100 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes refusées explicitement :

Aucune commande explicitement refusée dans l’état natif final de ce périmètre. Un outil interrompu sans résultat reste une erreur technique, distincte des refus explicitement enregistrés.

## 5. Accès web

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| TOTAL | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Preuve pure en mémoire : aucun serveur HTTP ni navigateur nécessaire ou lancé par ce change. Aucune URL visitée par l’agent de codage dans cet intervalle, aucun outil web exécuté. Les recherches techniques de l’orchestrateur et l’évaluation fournisseur PLLM restent hors de la télémétrie de production OpenCode ; elles sont déclarées séparément et ne sont pas attribuées au codeur. Volumes d’outils orchestrateur non exposés dans cette télémétrie : N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-02T02:19:28.403492+00:00 |
| Fin — après archivage | 2026-10-02T03:19:47.691340+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 00 min 19 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-02T02:27:01.710950+00:00 | N/A — outil natif non exposé | N/A |
| Après — après archivage de la spécification | 2026-10-02T03:21:25.964278+00:00 | N/A — outil natif non exposé | N/A |
| Différence après − avant | — | N/A — deux relevés comparables absents | — |

Quota codex, fenêtre10080 minutes : tool mcp__codex_app__get_usage_limits non exposé ; aucun quota Spark ou quota restant substitué. Les quotas sont partagés par le compte ; une variation peut inclure d’autres tâches simultanées. Exclusivité non vérifiée.

| Catégorie | Total | Part | Approuvé et exécuté | Taux | Refusé | Taux refus | Erreur technique/protocole | Taux erreur |
|---|---|---|---|---|---|---|---|---|
| Autres outils | 79 | 81.4 % | 79 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Commandes | 8 | 8.2 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Fichiers | 10 | 10.3 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| TOTAL | 97 | 100 % | 97 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Sondes dédiées de l’agent de codage, hors production :

| Position | Envoi UTC | Premier token UTC | Dernier token UTC | TTMT s | Débit tok/s | Sortie tokens | Statut |
|---|---|---|---|---|---|---|---|
| initiale — préparation preuve de composition | 2026-10-02T02:27:38.800300+00:00 | 2026-10-02T02:27:48.190515+00:00 | 2026-10-02T02:28:01.519635+00:00 | 9.390209 | 39.987618 | 533 | réussie |
| périodique — créneau 2026-10-02T02:57:38.800300+00:00 | 2026-10-02T02:59:26.535117+00:00 | 2026-10-02T02:59:28.944768+00:00 | 2026-10-02T02:59:30.479220+00:00 | 2.409649 | 318.679955 | 489 | réussie |
| finale — après archivage preuve initiale | 2026-10-02T03:19:37.609749+00:00 | 2026-10-02T03:19:40.847873+00:00 | 2026-10-02T03:19:43.313379+00:00 | 3.238119 | 198.336231 | 489 | réussie |

Relèves prévues : 3 (100 %) ; réussies 3 (100.0 %), échouées 0 (0.0 %), manquées 0 (0.0 %). Les horaires réels sont conservés ; aucune relève manquée n’est recréée rétroactivement.

TTMT min/moy/max : 2.409649/5.012659/9.390209 s ; débit min/moy/max : 39.987618/185.667935/318.679955 tok/s.

Surcharge sondes : 27710 tokens total API, 1511 tokens sortie, coût API 0.003049900, durées stream mesurées 17.329091 s ; hors statistiques de production. Prompt constant conservé dans cismp-state.json, modèle/fournisseur/HIGH identiques ; aucune sonde orchestrateur.

Incidents du périmètre : Surcharge fournisseur HTTP503 service_overloaded avant MCP sur le mandat design 21a23f847697 : erreur API hors outil, aucune cible écrite ni décision persistée (GET404), aucune permission, 65 empreintes/dist3/README intacts. Mandat clos sans exécution, ancien dispatch clôturé seulement, nouvelle session persistante avec readiness réel avant accès projet, test true unique 3a5b4b6dfef2 exit0 puis readiness final READY0IDLE ; deux fichiers déjà prouvés non rejoués. Brouillons corrigés AVANT toute écriture : isinstance permissif, spies visant mauvais symboles, fixtures manquante/schema/cycle/opaque invalidement définies, assertion Django incohérente, TMPDIR hors racine, couverture gardes incomplète et compteurs ; JSON initial incomplet et append absent corrigés dans proposition CGPT, snippets rendus lisibles et AST vérifiée. NDOC de revue a confondu import pur PG2 et appels instrumentés PG3 et cité des constantes déjà supprimées du brouillon : clarifié dans la même session, NFDOC final confirmé. Aucun échec des tests runtime finaux, aucune source SDK/exclue lue par read/glob/grep dans ce périmètre. Réponses décision HTTP400 avant stockage rapprochées GET404 puis décision unique, cause non établie. Les incidents de l’orchestrateur (chemin de lecture inexistant, assertions de cadrage/parse/rendu corrigées) restent dans le checkpoint ; aucune exécution de source par CGPT. Publication future exclue des comptages fixés.

Archivage : /home/devops/datas/pixs/openspec/changes/archive/2026-10-02-add-initial-composition-proof, preuves dans le RUN parent. Git non inspecté, aucun commit/push autorisé ou effectué. Aucun secret lu, aucune installation, aucune connexion PostgreSQL ni réseau applicatif dans les tests observés. Preuve JSON interne déterministe des étapes pures initiales discover/validate/resolve, sans conformité, profil, activation ou P0. Ce change ne prouve ni disponibilité globale ni cycle CISMP complet.
