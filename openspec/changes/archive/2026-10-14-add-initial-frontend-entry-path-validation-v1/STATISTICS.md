# STATISTIQUES — add-initial-frontend-entry-path-validation-v1

RUN cismp-pixs-3a9c9fd778064da4 ; session maîtresse ses_ec73f1346ffezXtrZGqWqry2X6 ; job cismp2-entry-validation-62cb0ab518df45a5. Intervalle fermé avant rédaction et écriture du présent rapport ; ces dernières opérations et les gates ultérieurs sont exclus. Source : historique natif complet de cette seule session, checkpoint parent, observations CAB/SSE, sondes jetables et quotas natifs. Aucun autre RUN n’est agrégé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | Modèle N/A (non exposée) ; OpenCode 1.19.0 | opencode-go | high | 2.409 s | 167.706 | N/A — durée active de génération non isolable de façon fiable |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — modèle exact N/A | N/A — télémétrie exacte absente | OpenAI | N/A — non exposé | N/A — non sondé | N/A — non sondé | N/A — durée active non exposée |

Aucun temps de service complet n’est calculable : aucun dénominateur fiable, aucun pourcentage inventé. Les durées natives des réponses incluent outils et attentes et ne sont pas assimilées au service du modèle. Aucune délégation à un sous-agent. Moyennes TTMT et débit : moyenne arithmétique des 4 sondes valides uniquement.

## 1. Statistiques générales et décisions

Durée calendaire : 01 h 37 min 59 s, pauses, attentes, prévol, tests et archivage inclus. 251 messages (100,0 %), 924 parties (100,0 %), 132 appels d’outils (100,0 %). 23 mandats CAB unitaires exécutés et vérifiés (100,0 % des mandats clôturés de ce change), 0 refus de permission observé.

Un appel terminé est classé réussi autorisé ; cela ne prouve pas à lui seul une approbation manuelle. Les opérations mutables sont rapprochées des décisions CAB corrélées et des preuves natives ; les lectures autorisées par politique restent distinctes. Les délais MCP et rejets de schéma sans dispatch sont des erreurs techniques, jamais des refus de permission ni des exécutions.

| Type | Total | Part | Réussis autorisés | Refus explicites | Erreurs techniques ou validation |
| --- | --- | --- | --- | --- | --- |
| Tous outils | 132 | 100.0 % | 128 (97.0 %) | 0 (0.0 %) | 4 (3.0 %) |

| Compteur de tokens natif | Nombre | Part du total catégorisé |
| --- | --- | --- |
| input | 2064401 | 5.9 % |
| output | 58383 | 0.2 % |
| reasoning | 20858 | 0.1 % |
| cache_read | 33129143 | 93.9 % |
| cache_write | 0 | 0.0 % |
| Total catégorisé | 35272785 | 100,0 % |

Input, output, reasoning et cache sont les compteurs distincts exposés par OpenCode, sans conversion en consommation facturée. Coût natif cumulé des réponses : 0.288546586, unité monétaire non exposée donc conversion en euros N/A. Compactages dans cette session : 0. Les cycles parent antérieurs ne sont pas imputés à ce change.

Sondes réelles : 4 ; valides 4 (100.0 %), échecs 0 (0.0 %). Échéances manquées consignées : 1 ; chaque mesure tardive est datée réellement, sans reconstruction. Début et fin présents, quotas initiaux conservés indépendamment.

Échéance 2026-10-14T05:24:37.848373+00:00 non mesurée à temps ; constat 2026-10-14T05:46:46.933694+00:00 : Sonde périodique non exécutée à échéance pendant revue et jalon stable ; aucune mesure rétroactive.

| Position UTC | Horodatage | TTMT | Débit réel | Sortie tokens | Durée sonde |
| --- | --- | --- | --- | --- | --- |
| début | 2026-10-14T04:54:31.436150+00:00 | 2.773 s | 227.612 t/s | 823 | 6.396 s |
| périodique tardive | 2026-10-14T05:46:46.944662+00:00 | 2.248 s | 188.184 t/s | 829 | 6.754 s |
| périodique +30 min après relève réelle | 2026-10-14T06:17:10.374699+00:00 | 2.446 s | 163.328 t/s | 853 | 7.787 s |
| fin | 2026-10-14T06:28:01.610906+00:00 | 2.168 s | 91.699 t/s | 873 | 11.711 s |

TTMT min/max : 2.168/2.773 s ; débit min/max : 91.699/227.612 t/s. Surcharge séparée de la production : 3378 tokens de sortie, 32.648 s, coût natif 0.004816000, unité monétaire non exposée.

Prompt constant dans chaque session jetable sans outils : Sans outil, fichier, réseau ni commentaire : répète exactement 80 fois la phrase suivante, une phrase par ligne : Le contrôle mesure une sortie fixe sans action métier.

Les identifiants, instants envoi/premier/dernier token et compteurs réellement exposés sont conservés dans statistics.probes. Version exacte du modèle N/A, non déduite de son nom. Cadence attendue : initiale, toutes les 30 minutes, finale ; les échéances manquées restent visibles séparément des mesures réelles.

Résultats : 3/3 compilations réussies (100,0 %), 10/10 méthodes de test ciblées réussies (100,0 %), dont 132 sous-cas de contrôles C0/DEL distincts des méthodes ; 8/8 tâches cochées après preuves (100,0 %). Strict du change avant/après code sans issue. Validation globale avant archive et contrôle global strict après archive : codes natifs et quatre WARNING de longueur conservés (3 Bulk historiques, 1 IdentityAssurance publiée par un autre RUN en référence6), aucun ERROR ni nouvelle issue Frontend. Un code nonzero du global strict reste un échec CLI qualifié ; il n’est jamais présenté comme strict sans issue. Le critère longueur est explicitement exclu par CISMP.

| Contrôle natif | Code sortie | Items | Valides CLI | Invalides CLI |
| --- | --- | --- | --- | --- |
| Strict du change avant code | 0 | 1 | 1 | 0 |
| Strict du change après code | 0 | 1 | 1 | 0 |
| Diagnostic élargi --all | 1 | 80 | 79 | 1 |
| Canon requis --specs | 0 | 78 | 78 | 0 |
| Canon strict après archive | 1 | 78 | 76 | 2 |

Le code1 du diagnostic élargi provient du delta B01 absent dans un autre RUN. Le code1 du canon strict provient uniquement des quatre WARNING de longueur ; la longueur est explicitement exclue du critère qualité par CISMP. Ces sorties restent des échecs CLI qualifiés ; aucune réussite globale stricte ni terminaison du projet n’est revendiquée.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 72 | 28.7 % |
| assistant | 179 | 71.3 % |
| Total | 251 | 100,0 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 240 | 26.0 % |
| step-start | 179 | 19.4 % |
| reasoning | 194 | 21.0 % |
| tool | 132 | 14.3 % |
| step-finish | 179 | 19.4 % |
| Total | 924 | 100,0 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 108 | 60.3 % |
| stop | 71 | 39.7 % |
| Total | 179 | 100,0 % |

| Type | Total | Part | Réussis autorisés | Refus explicites | Erreurs techniques ou validation |
| --- | --- | --- | --- | --- | --- |
| bash | 15 | 11.4 % | 13 (86.7 %) | 0 (0.0 %) | 2 (13.3 %) |
| cgpt-validation_broker_health | 2 | 1.5 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 46 | 34.8 % | 46 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_remediation_registry | 1 | 0.8 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 3 | 2.3 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 | 0.8 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 | 0.8 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| cgpt-validation_request_validation | 23 | 17.4 % | 22 (95.7 %) | 0 (0.0 %) | 1 (4.3 %) |
| glob | 5 | 3.8 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 2 | 1.5 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 25 | 18.9 % | 25 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 | 6.1 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 132 | 100.0 % | 128 (97.0 %) | 0 (0.0 %) | 4 (3.0 %) |

Les erreurs et sorties CLI nonzero ci-dessus restent distinctes des refus. Le diagnostic --all avant archive a échoué sur le B01 concurrent sans delta (79/80 valides, canon78/78 et change Frontend valide), sans correction par ce RUN. La validation canon requise --specs reste séparée ; le contrôle global strict après archive conserve quatre WARNING externes, code CLI nonzero préservé. Le parent ne déclare pas le projet global terminé. Un timeout MCP est repris par le même approval_id ; un outil indisponible avant dispatch ne prouve aucun effet. Toute écriture exécutée est rapprochée de son mandat et du contenu exact.

## 3. Fichiers modifiés

| Type | Total | Part | Réussis autorisés | Refus explicites | Erreurs techniques ou validation |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-entry-path-validation-v1/design.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-entry-path-validation-v1/proposal.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-entry-path-validation-v1/specs/frontend/spec.md | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-entry-path-validation-v1/tasks.md | 2 | 25.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/frontend_entry_paths.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_frontend_entry_path_integration.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_frontend_entry_path.py | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total tentatives fichiers | 8 | 100.0 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Ce tableau compte les tentatives d’outils, pas les fichiers uniques. Le fichier de tâches a été écrit à la création puis coché après preuves. Quatre artefacts OpenSpec ont été déplacés par l’archivage unique vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-14-add-initial-frontend-entry-path-validation-v1 ; les trois fichiers Python restent à leur emplacement. Les quatre contenus archivés, les trois contenus Python et UTF-8/LF sont prouvés. Le présent STATISTIQUES.md est produit après l’intervalle par un mandat distinct et n’est pas ajouté rétroactivement à ces compteurs. Façade kernel et canon frontend inchangés. Les cadrages externes et publications d’autres RUNs sont réconciliés séparément dans le checkpoint et ne sont pas attribués à ce lot.

## 4. Commandes

| Type | Total | Part | Réussis autorisés | Refus explicites | Erreurs techniques ou validation |
| --- | --- | --- | --- | --- | --- |
| Compilation Python | 3 | 20.0 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 6 | 40.0 % | 4 (66.7 %) | 0 (0.0 %) | 2 (33.3 %) |
| Prévol CAB /usr/bin/true | 2 | 13.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 4 | 26.7 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total tentatives commandes | 15 | 100.0 % | 13 (86.7 %) | 0 (0.0 %) | 2 (13.3 %) |

Libellés limités à 100 caractères ; les commandes intégrales et callID sont dans les mandats et preuves du checkpoint.

| Type | Total | Part | Réussis autorisés | Refus explicites | Erreurs techniques ou validation |
| --- | --- | --- | --- | --- | --- |
| /usr/bin/true | 2 | 13.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate add-initial-frontend-entry-path-validation-v1 --stric… | 2 | 13.3 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/frontend_entry_paths.py | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_frontend_entry_path.py | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_frontend_entry_path_… | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/devops… | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/devops… | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/devops… | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/devops… | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --all --json | 1 | 6.7 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| /home/devops/.local/npm/bin/openspec validate --specs --json | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-frontend-entry-path-validation-v1 --skip-s… | 1 | 6.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --specs --strict --json | 1 | 6.7 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| Total | 15 | 100.0 % | 13 (86.7 %) | 0 (0.0 %) | 2 (13.3 %) |

Commandes refusées regroupées : 0 occurrence(s), 0.0 %. Les erreurs pré-dispatch restent techniques. Chaque commande réussie possède son code de sortie natif 0. Archivage --skip-specs --yes exécuté une seule fois, canon frontend préservé.

## 5. Accès web

| Type | Total | Part | Réussis autorisés | Refus explicites | Erreurs techniques ou validation |
| --- | --- | --- | --- | --- | --- |
| Web | 0 | N/A | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucun outil web ni URL externe visitée dans l’historique de production (0). Taux web N/A car dénominateur nul. Les appels de pilotage HTTP locaux OpenCode/CAB ne sont pas des visites web externes. Aucune URL refusée observée. L’orchestrateur lit les quotas par l’outil natif ; les sondes n’utilisent aucun outil ni réseau.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-14T04:52:10.041000+00:00 |
| Fin — après archivage | 2026-10-14T06:30:10+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 37 min 59 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — avant première écriture | 2026-10-14T04:52:10.068275+00:00 | 12 % | 2026-10-20T04:59:31+00:00 |
| Après — après archivage et sonde finale | 2026-10-14T06:30:10+00:00 | 15 % | 2026-10-20T04:59:31+00:00 |
| Différence après − avant | — | N/A — identité du compte initial non conservée | — |

Quota codex, fenêtre 10080 minutes et même réinitialisation observés. Identité du compte absente du relevé initial : différence non calculée, comparaison du même compte non prouvée. Les quotas sont partagés par le compte et toute variation peut inclure d’autres tâches simultanées. Une variation nulle peut refléter la précision ou le délai du compteur ; aucune attribution exclusive ni conversion en tokens/euros.

| Type | Total | Part | Réussis autorisés | Refus explicites | Erreurs techniques ou validation |
| --- | --- | --- | --- | --- | --- |
| Fichiers | 8 | 6.1 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 15 | 11.4 % | 13 (86.7 %) | 0 (0.0 %) | 2 (13.3 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 109 | 82.6 % | 107 (98.2 %) | 0 (0.0 %) | 2 (1.8 %) |
| Total global | 132 | 100.0 % | 128 (97.0 %) | 0 (0.0 %) | 4 (3.0 %) |

Totaux croisés vérifiés : outils par type = domaines = 132 ; réussites + refus + erreurs = 132. Tests et compilations passés, archivage réussi, rapport distinct en cours de production à la fin de cet intervalle. Publication et gate ne sont pas revendiqués rétroactivement. Git non inspecté et aucune opération Git mandatée ; aucun effet externe mandaté, aucun secret dans les fichiers créés ni dans ce rapport. Les vérifications navigateur, npm et PostgreSQL sont non applicables à ce seul validateur lexical pur Python. Aucun changement de dépendance. Le parent CISMP reprend SÉLECTION après publication, gate, désarmement et libération vérifiés.
