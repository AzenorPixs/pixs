# STATISTICS.md — add-pzt-ca-hierarchy-rotation-and-recovery

Statut exact : change ouvert — dépendances manquantes — archivage en attente.
Change créé : 2026-10-17, heure absente. Corpus vérifiable depuis 2026-10-22 ; lacune 2026-10-17 → 2026-10-22 N/A.
Gel : 2026-10-30T06:42:53.618Z. Surplus ultérieurs au gel exclus des totaux, suivis au checkpoint.
RUN : cismp6-pixs-9dd1542d4c0542f2. Checkpoint : [output/cismp/cismp6-pixs-9dd1542d4c0542f2/state.json](/home/devops/datas/pixs/output/cismp/cismp6-pixs-9dd1542d4c0542f2/state.json). BLOCKERS : [openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/BLOCKERS.md](/home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/BLOCKERS.md).
Provenance : API native OpenCode V2 via client CAB, collecte OC 2026-10-30T06:42:36.567Z ; 2 logs Codex 01a16513-e281-7832-a135-11cf69735a9a et 01a175ad-4722-7773-8463-3934ef187689, uniquement métadonnées extraites.
Git : commande git diff check a renvoyé 'Not a git repository', aucun commit/push fait ; contrôle comparatif SHA 10 sources et 3 edits documentaires bien observé, ligne MAP C6 conservée malgré modifications des pairs.
Gate BLOQUÉ encore à obtenir après rapport, change ouvert/non livré/non archivé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A | opencode-go | high | 3,25266428025793 s | 230,91217267470262 /s | N/A |
| muse-spark-1.3-contributor | N/A | opencode-go | medium | 1,833851766 s | 476,510860017989 /s | N/A |
| muse-spark-1.3-contributor | N/A | opencode-go | default | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| gpt-6.1-sol | 0.163.0-alpha.10.2 | Codex Desktop | high | N/A | N/A | N/A |
| gpt-6.1-sol | 0.164.0-alpha.11.1 | Codex Desktop | high | N/A | N/A | N/A |

Les versions 0.163.0-alpha.10.2 et 0.164.0-alpha.11.1 sont celles de l agent CLI, modèle exact N/A ; OpenAI via Codex Desktop. Temps de service N/A car durées actives et dénominateur indisponibles.

## 1. Statistiques générales et décisions

**Tableau sessions, base 8390 messages uniques dédupliqués par message.id.**

| Session | Messages | Part / 8390 |
|---|---|---|
| ses_e9ae62ea7ffeV1b8Quq8SrPDcn | 5 | 0,1 % |
| ses_e9ae37b7effeNoaNGZaH496Asf | 1247 | 14,9 % |
| ses_e980d8697ffem5AAHJwzbZxBnS | 2665 | 31,8 % |
| ses_e92e6d566ffevcAeEdMlJdzZO6 | 335 | 4,0 % |
| ses_e923e69ccffe5Q92IfYpuabX5S | 34 | 0,4 % |
| ses_e922b55afffe40Kkvcxa2arNaR | 3857 | 46,0 % |
| ses_e86fbafd4ffea5n3Iw1SpbyDRx | 247 | 2,9 % |
| Total | 8390 | 100,0 % |

**Tableau messages et rôles, base 8390 messages.**

| Rôle | Messages | Part / 8390 |
|---|---|---|
| user | 3109 | 37,1 % |
| assistant | 5221 | 62,2 % |
| system | 9 | 0,1 % |
| compaction | 35 | 0,4 % |
| model-switched | 1 | 0,0 % |
| idle | 15 | 0,2 % |
| Total | 8390 | 100,0 % |

Les messages user incluent les mandats orchestrateur, pas des messages humains.

**Tableau finishes, base 8390 tous rôles.**

| Finish | Messages | Part / 8390 |
|---|---|---|
| absent | 3782 | 45,1 % |
| tool-calls | 2727 | 32,5 % |
| stop | 1881 | 22,4 % |
| Total | 8390 | 100,0 % |

**Tableau décisions MCP dédupliquées, base 367 requêtes.**

| Statut | Requêtes | Part / 367 |
|---|---|---|
| APPROVED | 353 | 96,2 % |
| REJECTED | 4 | 1,1 % |
| CANCELLED | 6 | 1,6 % |
| EXPIRED | 1 | 0,3 % |
| TERMINAL_NON_OBSERVE | 3 | 0,8 % |
| Total | 367 | 100,0 % |

## 2. Types de messages et d’outils

**Tableau résultats outils natifs, base 4091 parties.**

| Famille | Completed | Error | Total | Part total / 4091 | Taux completed / ligne | Taux error / ligne | Refus corrélé |
|---|---|---|---|---|---|---|---|
| read | 544 | 8 | 552 | 13,5 % | 98,6 % | 1,4 % | N/A |
| cab-mcp | 2928 | 81 | 3009 | 73,6 % | 97,3 % | 2,7 % | N/A |
| bash | 283 | 6 | 289 | 7,1 % | 97,9 % | 2,1 % | N/A |
| grep | 89 | 1 | 90 | 2,2 % | 98,9 % | 1,1 % | N/A |
| glob | 80 | 0 | 80 | 2,0 % | 100,0 % | 0,0 % | N/A |
| edit | 39 | 0 | 39 | 1,0 % | 100,0 % | 0,0 % | N/A |
| write | 24 | 0 | 24 | 0,6 % | 100,0 % | 0,0 % | N/A |
| invalid | 6 | 0 | 6 | 0,1 % | 100,0 % | 0,0 % | N/A |
| execute | 2 | 0 | 2 | 0,0 % | 100,0 % | 0,0 % | N/A |
| Total | 3995 | 96 | 4091 | 100,0 % | 97,7 % | 2,3 % | N/A |

**Tableau parties, base 16092 parties.**

| Type | Parties | Part / 16092 |
|---|---|---|
| text | 6518 | 40,5 % |
| reasoning | 5483 | 34,1 % |
| tool | 4091 | 25,4 % |
| Total | 16092 | 100,0 % |

**Tableau jetons natifs OpenCode, base 5221 messages avec jetons.**

| Champ | Valeur |
|---|---|
| input | 66822015 |
| output | 2221137 |
| reasoning | 1023845 |
| cache lecture | 1582917134 |
| cache écriture | 0 |
| messages avec coût | 5221 / 5221 |
| coût API | 10,05765638, devise N/A |

**Tableau Codex, métadonnées seules par rollout, sans mélange OpenCode.**

| Rollout | Lignes | developer / user / assistant | Outer total | exec / sleep / input async / wait | Avec sortie | Input cumulé | Cache cumulé | Output cumulé | Raisonnement cumulé | Total cumulé | Compactions |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01a16513 2026-10-22 | 31147 | 62 / 71 / 590 | 3467 | 2905 / 422 / 24 / 116 | 3467 | 1058328834 | 1043550848 | 3300895 | 2166310 | 1061629729 | 13 |
| 01a175ad 2026-10-26 | 9419 | 32 / 30 / 154 | 953 | 899 / 51 / 2 / 1 | 952 | 328405292 | 323377920 | 1151109 | 727631 | 329556401 | 4 |

**Tableau sondes.**

| Sonde | TTMT | TPS | Sortie | Deltas SSE | Entrée / sortie / raisonnement |
|---|---|---|---|---|---|
| high historique 31 conservées | moyenne 3,25266428025793 s, min 1,6182463270016014 s, max 8,169086408999748 s | moyenne 230,91217267470262 /s, min 91,73157577994714 /s, max 718,8593710316344 /s, sortie totale 25404 hors production | N/A | N/A | N/A |
| medium initiale 2026-10-30T05:46:35.557Z | 2,447225874 s | 247,22328674919305 /s | 809 | 26 | 8460 / 809 / 224 |
| medium finale 2026-10-30T06:41:05.712Z | 1,220477658 s | 705,7984332867842 /s | 809 | 10 | 8460 / 809 / 149 |
| medium moyenne 2 sondes | 1,833851766 s | 476,510860017989 /s | N/A | N/A | N/A |

**Tableau surcharge medium, séparé.**

| Champ | Valeur |
|---|---|
| entrée totale | 16920 |
| sortie totale | 1618 |
| raisonnement total | 373 |
| cache lecture total | 0 |
| cache écriture total | 0 |
| coût total | 0 |

Prévision totale historique N/A. Relève +30 min du 30/10 manquée. Tentative variant default exclue. Autres prévols sans mesure SSE exclus.

## 3. Fichiers modifiés

**Tableau tentatives natives directes, base 63 tentatives, 31 chemins.**

| Chemin complet | Completed | Error | Part / 63 | Taux completed / ligne | Refus par chemin |
|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/tasks.md | 10 | 0 | 15,9 % | 100,0 % | N/A |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/design.md | 8 | 0 | 12,7 % | 100,0 % | N/A |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/contracts.md | 8 | 0 | 12,7 % | 100,0 % | N/A |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/proposal.md | 4 | 0 | 6,3 % | 100,0 % | N/A |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/.openspec.yaml | 3 | 0 | 4,8 % | 100,0 % | N/A |
| /home/devops/datas/pixs/tests/integration/z12/Dockerfile | 2 | 0 | 3,2 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_process_image.pxi | 2 | 0 | 3,2 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_policy_bytes.pxi | 2 | 0 | 3,2 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_owner_context.pxi | 2 | 0 | 3,2 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_systemd_connection.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_manager_unit.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_chrony_protocol.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_chrony_receive.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_chrony_socket.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_chrony_request.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_key_auth_fd.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_chrony_query.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_admin_profile_gen.py | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_admin_profile.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_admin_codec.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_admin_verify.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_admin_values.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_admin_binding.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_admin_time.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_owner_limits_gen.py | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_owner_build_gen.py | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_owner_public_slice.pxi | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/output/cismp/cismp6-pixs-9dd1542d4c0542f2/PROPOSITION_REPRISE_TEMPS.md | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/output/cismp/cismp6-pixs-9dd1542d4c0542f2/PROPOSITION_REALISATION_TEMPS_V2.md | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/BLOCKERS.md | 1 | 0 | 1,6 % | 100,0 % | N/A |
| /home/devops/datas/pixs/DEVELOPMENT_MAP.md | 1 | 0 | 1,6 % | 100,0 % | N/A |
| Total | 63 | 0 | 100,0 % | 100,0 % | N/A |

Completed ne prouve pas une permission manuelle ; erreurs 0 seulement celles de l outil natif. Le rapport lui-même est postérieur au gel et n est pas dans ces 63 tentatives.

**Tableau effets shell JSON distinct, non additif, base 35 effets.**

| Chemin complet | Effets | Part / 35 |
|---|---|---|
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_tcti_deadline.pxi | 2 | 5,7 % |
| /home/devops/datas/pixs/tests/integration/z12/native_deadline.pyx | 2 | 5,7 % |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/design.md | 2 | 5,7 % |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/contracts.md | 2 | 5,7 % |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/tasks.md | 3 | 8,6 % |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/RACCORDS_TEMPS_V2.md | 5 | 14,3 % |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_nv_read_guard.pxi | 1 | 2,9 % |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/.openspec.yaml | 1 | 2,9 % |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/proposal.md | 1 | 2,9 % |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/_launch_obs_sysd.pxi | 1 | 2,9 % |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/RECETTE_TEMPS_V2.md | 1 | 2,9 % |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/specs/runtime/spec.md | 1 | 2,9 % |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/requirements.md | 1 | 2,9 % |
| /home/devops/datas/pixs/openspec/specs/runtime/spec.md | 1 | 2,9 % |
| /home/devops/datas/pixs/src/pixs/kernel/contracts/time.py | 1 | 2,9 % |
| /home/devops/datas/pixs/src/pixs/kernel/contracts/__init__.py | 1 | 2,9 % |
| /home/devops/datas/pixs/tests/unit/test_time_contract.py | 1 | 2,9 % |
| /home/devops/datas/pixs/tests/integration/test_contract_descriptors_integration.py | 1 | 2,9 % |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/z12_time_profile.inc | 1 | 2,9 % |
| /home/devops/datas/pixs/tests/integration/z12/native_time_math.c | 1 | 2,9 % |
| /home/devops/datas/pixs/src/pixs/pzt_ca/native/z12_time_budget.inc | 1 | 2,9 % |
| /home/devops/datas/pixs/tests/integration/z12/native_time_budget_check.c | 1 | 2,9 % |
| /home/devops/datas/pixs/src/pixs/core/time_guard.py | 1 | 2,9 % |
| /home/devops/datas/pixs/tests/unit/test_time_guard_delegation.py | 1 | 2,9 % |
| /home/devops/datas/pixs/openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery/BLOCKERS.md | 1 | 2,9 % |
| Total | 35 | 100,0 % |

## 4. Commandes

**Tableau familles, base 289 exécutions, total absolu 289.**

| Famille | Completed | Error | Total absolu | Part / 289 | Taux completed / ligne | Taux error / ligne | Refus corrélé |
|---|---|---|---|---|---|---|---|
| true | 30 | 0 | 30 | 10,4 % | 100,0 % | 0,0 % | N/A |
| openspec | 40 | 0 | 40 | 13,8 % | 100,0 % | 0,0 % | N/A |
| docker | 12 | 0 | 12 | 4,2 % | 100,0 % | 0,0 % | N/A |
| python3 | 182 | 6 | 188 | 65,1 % | 96,8 % | 3,2 % | N/A |
| rg | 6 | 0 | 6 | 2,1 % | 100,0 % | 0,0 % | N/A |
| cat | 2 | 0 | 2 | 0,7 % | 100,0 % | 0,0 % | N/A |
| sed | 3 | 0 | 3 | 1,0 % | 100,0 % | 0,0 % | N/A |
| mkdir | 2 | 0 | 2 | 0,7 % | 100,0 % | 0,0 % | N/A |
| cc | 2 | 0 | 2 | 0,7 % | 100,0 % | 0,0 % | N/A |
| native_time_math | 1 | 0 | 1 | 0,3 % | 100,0 % | 0,0 % | N/A |
| rmdir | 2 | 0 | 2 | 0,7 % | 100,0 % | 0,0 % | N/A |
| native_time_budget | 1 | 0 | 1 | 0,3 % | 100,0 % | 0,0 % | N/A |
| Total | 283 | 6 | 289 | 100,0 % | 97,9 % | 2,1 % | N/A |

**Tableau commandes refusées, base 4 refus, total 4 / 100,0 %.**

| Identifiant | Commande display exacte | Occurrences | Part / 4 |
|---|---|---|---|
| z12-6ddcce9e174b438abad6fffc4208d30e | /usr/bin/docker --host unix:///var/run/docker.sock run --rm --pull never --network none --read-only… | 1 | 25,0 % |
| z12-b9d971825489453583123617165059c1 | rg --files tests/unit tests/integration -g '*core*.py' -g '*pzt*.py' -g '*test_support.py' -g 'conf… | 1 | 25,0 % |
| cismp6-tcti-source-9ed07a758d4c41eeb4e1c137a224dee7 | /home/devops/python/current/bin/python3 -B -c 'import hashlib, json, os\nfrom pathlib import Path\n… | 1 | 25,0 % |
| cismp6-t0-1b8294dcacec4e9692b8f245db70beac | /home/devops/python/current/bin/python3 -B -c 'import base64,binascii,hashlib,json,sys,lzma\nfrom p… | 1 | 25,0 % |

## 5. Accès web

**Tableau web natif.**

| Outil web natif | Tentatives | Taux | URLs |
|---|---|---|---|
| aucun | 0 | N/A, dénominateur 0 | N/A |

## 6. Synthèse globale

**Tableau domaines exclusifs, base 4091 parties.**

| Domaine | Total absolu | Part / 4091 | Completed | Error | Taux completed / ligne | Taux error / ligne | Refus |
|---|---|---|---|---|---|---|---|
| fichiers edit + write | 63 | 1,5 % | 63 | 0 | 100,0 % | 0,0 % | N/A |
| commandes bash | 289 | 7,1 % | 283 | 6 | 97,9 % | 2,1 % | N/A |
| web | 0 | 0,0 % | 0 | 0 | N/A, dénominateur 0 | N/A, dénominateur 0 | N/A |
| autres tous outils restants | 3739 | 91,4 % | 3649 | 90 | 97,6 % | 2,4 % | N/A |
| Total | 4091 | 100,0 % | 3995 | 96 | 97,7 % | 2,3 % | N/A |

**Tableau quotas, compte partagé.**

| Mesure | Horodatage | Quota utilisé | Réinitialisation |
|---|---|---|---|
| avant début création | N/A, heure absente | N/A | N/A |
| premier historique | 2026-10-22T19:38:14.875692Z | 8 % | 2026-10-29T17:09:38.000Z |
| reprise | 2026-10-30T04:43:53.589Z | 63 % | 2026-11-04T06:45:53.000Z |
| courant | 2026-10-30T06:41:34Z | 78 % | 2026-11-04T06:45:53.000Z |
| après archivage | en attente | N/A | N/A |
| différence change entière | N/A, relevé initial absent et fenêtres différentes | N/A | N/A |
| variation reprise | 63 → 78 vaut 15 points du compte partagé | — | — |

**Tableau durée.**

| Étape | Valeur |
|---|---|
| début | 2026-10-17, heure absente |
| fin et archivage | en attente |
| durée globale | N/A |
| intervalle provisoire 2026-10-22T19:26:14.910Z → gel 2026-10-30T06:42:53.618Z | 645398,708 s soit 179 h 16 min 38,708 s, valeur provisoire distincte de la durée du change |

Limites T1 : 10 SHA inchangés, succès historiques 68/61/52/10 non rejoués, aucun producteur UTC qualifié ni raccord effectif PA/NTS/TCB. Strict change PASS observé 1/1 durationMs 46. 3 documents 30/10 appliqués, aucun nouveau code, installation, activation, Git, archive.
Conditions de reprise : contrôler producteur PA01 effectif, renseigner profils/provenance/continuité, établir composition/liaisons, obtenir autorisation phase, réévaluer preuves. Pointeurs : BLOCKERS.md appendice 2026-10-30T05:56:31.677Z, checkpoint output/cismp/cismp6-pixs-9dd1542d4c0542f2/state.json.

Limites de lecture : completed n est ni une autorisation manuelle ni un test PASS ; les 6 appels invalid terminés ne sont pas des opérations valides ; les 3 demandes sans état terminal observé ne sont pas 3 pending actuels ; le compteur contrôleur rejected 1 pour la demande bfcf et son reçu MCP EXPIRED 1 sont deux niveaux distincts. Durées, tokens et sondes restent séparés : pas d ajout du raisonnement à la sortie, pas de somme des snapshots cumulés, pas de somme des outils OUTER Codex et natifs OC. Historique web Codex N/A car arguments non extraits, HTTP technique OC/CAB hors catégorie web. Temps de service N/A et coût API en unité non documentée, aucune conversion en facture. La version au gel est provisoire, rapport et clôture ultérieurs tracés au checkpoint et à intégrer lors de la prochaine reprise sans remplacer l historique.

Sources : [/home/ade/.codex/archived_sessions/rollout-2026-10-22T21-26-04-01a16513-e281-7832-a135-11cf69735a9a.jsonl](/home/ade/.codex/archived_sessions/rollout-2026-10-22T21-26-04-01a16513-e281-7832-a135-11cf69735a9a.jsonl) et [/home/ade/.codex/sessions/2026/10/26/rollout-2026-10-26T01-47-32-01a175ad-4722-7773-8463-3934ef187689.jsonl](/home/ade/.codex/sessions/2026/10/26/rollout-2026-10-26T01-47-32-01a175ad-4722-7773-8463-3934ef187689.jsonl), métadonnées seules.
