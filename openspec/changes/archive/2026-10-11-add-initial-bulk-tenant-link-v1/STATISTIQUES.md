# Statistiques — add-initial-bulk-tenant-link-v1

RUN cismp-pixs-758862ec875d4708 ; job cismp-code-tenant-4c519b515835 ; sessions natives de codage ses_ed5ed2e3affe0WykkSWVqUvWAH, ses_ed5dc9fe9ffe37EWLAY0s63MEi. Historique complet paginé et dédupliqué par identifiant. Les totaux incluent initialisation, prévols et récupérations de ces deux sessions jusqu’à la collecte ; RSMP préalable, sondes dédiées et publication de ce rapport sont hors totaux de production.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen3.8 Flash | N/A : version exacte non exposée | OpenCode Go | xhigh | 1.830 s | 92.079 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex / GPT-6 | N/A : version exacte non exposée | OpenAI | N/A | N/A : aucune sonde orchestrateur | N/A | N/A |

Temps de service N/A : aucun chronométrage de génération active comparable, ni dénominateur fiable. Les durées des messages incluent outils et attentes ; elles ne sont pas assimilées au service modèle. OpenCode 1.18.35 ; broker réel 0.87.1, plugin distribué 0.87.2, versions distinctes. Métadonnées natives : 113 réponses (100 %) avec qwen3.8-flash / opencode-go / xhigh.

## 1. Statistiques générales et décisions

166 messages (100 %), 71 appels d’outils (100 %). Durée calendaire 00 h 40 min 51 s, pauses, récupérations, tests et sondes inclus.

| Décisions CAB terminales uniques | Nombre | Part |
| --- | --- | --- |
| APPROVED | 18 | 85.7 % |
| REJECTED | 3 | 14.3 % |
| Total | 21 | 100 % |

Les décisions sont dédupliquées par approval_id et proviennent uniquement de réponses MCP terminales enregistrées. Les identifiants seulement planifiés ou malformés avant enregistrement sont exclus. Un outil MCP terminé peut transporter REJECTED : son transport est abouti, sa décision est comptée séparément. Abouti signifie terminé sous permission automatique ou manuelle, sans prouver une approbation manuelle à lui seul.

| Compteur natif | Valeur cumulée rapportée | Présent | Absent |
| --- | --- | --- | --- |
| input | 564 | 113 (100.0 %) | 0 (0.0 %) |
| output | 45944 | 113 (100.0 %) | 0 (0.0 %) |
| reasoning | 0 | 113 (100.0 %) | 0 (0.0 %) |
| total | 5242395 (partiel) | 94 (83.2 %) | 19 (16.8 %) |
| cache_read | 3892471 | 113 (100.0 %) | 0 (0.0 %) |
| cache_write | 1303416 | 113 (100.0 %) | 0 (0.0 %) |

Coût natif observé : 0.34464102 USD ; facturation réelle N/A. Compactions dans ces sessions : 0. Messages portant MessageAbortedError : 19 ; un outil déjà terminé conserve son résultat. Aucun total de tokens n’est reconstruit depuis d’autres champs.

Résultat livré : trois compilations exit0, 8/8 tests ciblés (100 %), 103/103 régressions (100 %), soit 111/111 tests (100 %). Strict du change avant et après code exit0, une entrée passée, aucune issue. RSMP antérieur : quatre exigences et une note, ciblée/globale exit1 pour trois WARNING historiques identiques de longueur requirements[6], [10], [13], zéro diagnostic nouveau ; aucune réussite globale n’est revendiquée.

Incidents réconciliés : refus d’une commande OpenSpec modifiée, substitution de la commande ciblée à la régression, demande d’archivage formulée comme édition de dossier ; aucune exécution de ces trois demandes. Un write sans CAB a été interrompu puis sa permission explicitement refusée ; cible absente prouvée avant récupération. Cet appel est classé refus natif, avec interruption concomitante. Les erreurs d’outils indisponibles restent techniques. Nouvelle candidate dans le même job via /job/recover, prévol exact réussi, six fichiers conservés ; aucun rejeu des écritures prouvées. Autorisation et exécution ensuite séparées en deux tours natifs.

| Sonde dédiée | Envoyée | Premier événement | Dernier événement | Tokens sortie | TTMT | Tokens/s | État |
| --- | --- | --- | --- | --- | --- | --- | --- |
| début | 2026-10-11T10:27:19+02:00 | 2026-10-11T10:27:20+02:00 | 2026-10-11T10:27:35+02:00 | 1198 | 1.670 s | 79.926 | success |
| +30 min | 2026-10-11T10:57:25+02:00 | 2026-10-11T10:57:27+02:00 | 2026-10-11T10:57:41+02:00 | 1131 | 1.775 s | 83.342 | success |
| fin | 2026-10-11T11:05:38+02:00 | 2026-10-11T11:05:40+02:00 | 2026-10-11T11:05:50+02:00 | 1123 | 2.046 s | 112.969 | success |

Relèves prévues 3 (100 %), réussies 3 (100.0 %), échouées 0 (0.0 %), manquées 0 (0.0 %). Prompt fixe : « Sans outil, sans fichier ni réseau : écris uniquement la suite des entiers de 1 à 300, séparés par un espace. Aucun commentaire. ». Sessions jetables sans outil, mêmes modèle/fournisseur/xhigh. Moyennes arithmétiques des sondes valides ; TTMT min/max 1.670/2.046 s, débit min/max 79.926/112.969 tokens/s. Chronométrage SSE et compteurs natifs, aucun token remplacé par un fragment de flux. Surcharge de sondes séparée : 3452 tokens sortie ; durée mesurée en SSE 43.991 s. Coût N/A : compteur des sessions jetables non conservé avant leur suppression. La dérogation développeur au benchmark PLLM est conservée ; ces sondes ne fabriquent pas un nouveau benchmark réussi.

## 2. Types de messages et d’outils

Rôles :

| Catégorie | Nombre | Part |
| --- | --- | --- |
| assistant | 113 | 68.1 % |
| user | 53 | 31.9 % |
| Total | 166 | 100 % |

Types de parties :

| Catégorie | Nombre | Part |
| --- | --- | --- |
| reasoning | 95 | 20.3 % |
| step-finish | 94 | 20.0 % |
| step-start | 95 | 20.3 % |
| text | 114 | 24.3 % |
| tool | 71 | 15.1 % |
| Total | 469 | 100 % |

Terminaisons des réponses :

| Catégorie | Nombre | Part |
| --- | --- | --- |
| absent | 19 | 16.8 % |
| stop | 28 | 24.8 % |
| tool-calls | 66 | 58.4 % |
| Total | 113 | 100 % |

| Outil natif | Total | Part | Aboutis | Taux | Refusés | Taux | Erreurs | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bash | 10 | 14.1 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 12 | 16.9 % | 9 | 75.0 % | 0 | 0.0 % | 3 | 25.0 % |
| cgpt-validation_get_approval | 1 | 1.4 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_list_pending | 1 | 1.4 % | 0 | 0.0 % | 0 | 0.0 % | 1 | 100.0 % |
| cgpt-validation_request_validation | 22 | 31.0 % | 21 | 95.5 % | 0 | 0.0 % | 1 | 4.5 % |
| read | 16 | 22.5 % | 15 | 93.8 % | 0 | 0.0 % | 1 | 6.2 % |
| write | 9 | 12.7 % | 8 | 88.9 % | 1 | 11.1 % | 0 | 0.0 % |
| Total | 71 | 100.0 % | 64 | 90.1 % | 1 | 1.4 % | 6 | 8.5 % |

## 3. Fichiers modifiés

Tentatives natives d’écriture, distinctes des intentions CAB non exécutées. Les quatre artefacts ont été déplacés vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-11-add-initial-bulk-tenant-link-v1 ; le tableau conserve les cibles absolues au moment de leurs écritures. Le rapport lui-même est publié après cette collecte et exclu des totaux.

| Chemin absolu complet | Total | Part | Aboutis | Taux | Refusés | Taux | Erreurs | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-tenant-link-v1/design.md | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-tenant-link-v1/proposal.md | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-tenant-link-v1/specs/bulk-operations/spec.md | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-initial-bulk-tenant-link-v1/tasks.md | 2 | 22.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/kernel/bulk_tenant_link.py | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_bulk_tenant_link_integration.py | 2 | 22.2 % | 1 | 50.0 % | 1 | 50.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_bulk_tenant_link.py | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 9 | 100.0 % | 8 | 88.9 % | 1 | 11.1 % | 0 | 0.0 % |

Proposition CAB d’édition refusée, sans outil d’écriture exécuté : /home/devops/datas/pixs/openspec/changes/add-initial-bulk-tenant-link-v1. Elle ne constitue pas un fichier modifié.

## 4. Commandes

Les familles ci-dessous comptent les seuls appels Bash natifs ; les prévols sont explicitement inclus.

| Famille | Total | Part | Aboutis | Taux | Refusés | Taux | Erreurs | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenSpec archive | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec validation | 2 | 20.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Prévol /usr/bin/true | 2 | 20.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python compilation | 3 | 30.0 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Python tests | 2 | 20.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 10 | 100.0 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Propositions de commandes CAB refusées, non exécutées, regroupées séparément des appels Bash :

| Commande refusée (100 caractères maximum) | Occurrences | Part des propositions de commandes refusées |
| --- | --- | --- |
| cd /home/devops/datas/pixs && /home/devops/.local/npm/bin/openspec validate add-initial-bulk-tenant… | 1 | 50.0 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest -v unit.test_bulk_ten… | 1 | 50.0 % |
| Total | 2 | 100.0 % |

La troisième décision REJECTED visait un dossier dans files et aucune commande ; elle figure à la section fichiers. Les commandes exécutées utilisaient les binaires absolus DEVOPS.md, sans regroupement ni substitution. Archivage réussi une fois avec --yes --skip-specs --json ; specsUpdated=false.

## 5. Accès web

| Domaine | Total | Part | Aboutis | Taux | Refusés | Taux | Erreurs | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Outils web | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |
| Total | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucun outil web appelé : aucune URL visitée ou refusée à lister. Le transport du fournisseur LLM, les sondes et les API locales de pilotage ne sont pas présentés comme des visites web de l’agent. Un dénominateur nul reste N/A.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-11T10:27:18+02:00 |
| Fin — après archivage et sonde finale | 2026-10-11T11:08:10+02:00 |
| Durée globale, pauses et attentes incluses | 00 h 40 min 51 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | N/A : outil natif non exposé | N/A | N/A |
| Après — après archivage | 2026-10-11T11:08:10.016305+02:00 ; outil natif non exposé | N/A | N/A |
| Différence après − avant | — | N/A : deux valeurs indisponibles | — |

Outil natif get_usage_limits indisponible aux contrôles initial et final : aucun quota reconstitué ou remplacé par celui d’un autre fournisseur. Les quotas sont partagés par le compte ; une variation observable pourrait inclure d’autres tâches simultanées et ne serait pas exclusivement attribuable à cette session.

| Domaine | Total | Part | Aboutis | Taux | Refusés | Taux | Erreurs | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| autres | 52 | 73.2 % | 46 | 88.5 % | 0 | 0.0 % | 6 | 11.5 % |
| commandes | 10 | 14.1 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| fichiers | 9 | 12.7 % | 8 | 88.9 % | 1 | 11.1 % | 0 | 0.0 % |
| web | 0 | 0.0 % | 0 | N/A | 0 | N/A | 0 | N/A |
| Total | 71 | 100.0 % | 64 | 90.1 % | 1 | 1.4 % | 6 | 8.5 % |

Totaux croisés vérifiés : types = domaines = total outils ; fichiers = somme des tentatives d’écriture ; familles = appels Bash. Tests 111/111 (100 %) ; archive présente avec quatre artefacts exacts, tâches prouvées et aucun changement canonique pendant le code. Trois nouveaux Python seulement, 316 références préservées et ensembles de fichiers Python contrôlés. Aucun Git inspecté ou modifié, aucun secret transmis au modèle, aucun accès web d’agent. Les lectures sécurisées de quotas fournisseur restent hors contexte modèle et hors totaux d’outils OpenCode. Cycle global CISMP non déclaré terminé ; retour SÉLECTION après publication et vérification du présent rapport.
