# STATISTIQUES — add-initial-frontend-contribution-type-vocabulary

RUN cismp-pixs-3a9c9fd778064da4 ; session maîtresse ses_ec9186603ffeDtp4nnnTFNV6oT ; job cismp2-frontend-types-ca0b6cb8c88c4f38. Intervalle fermé avant rédaction et écriture du présent rapport ; ces dernières opérations et les gates ultérieurs sont exclus. Source : historique natif complet de cette seule session, checkpoint parent, observations CAB/SSE, sondes jetables et quotas natifs. Aucun autre RUN n’est agrégé.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | Modèle N/A (non exposée) ; OpenCode 1.19.0 | opencode-go | high | 5.079 s | 243.244 | N/A — durée active de génération non isolable de façon fiable |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — modèle exact N/A | N/A — télémétrie exacte absente | OpenAI | N/A — non exposé | N/A — non sondé | N/A — non sondé | N/A — durée active non exposée |

Aucun temps de service complet n’est calculable : aucun dénominateur fiable, aucun pourcentage inventé. Les durées natives des réponses incluent outils et attentes et ne sont pas assimilées au service du modèle. Aucune délégation à un sous-agent. Moyennes TTMT et débit : moyenne arithmétique des 3 sondes valides uniquement.

## 1. Statistiques générales et décisions

Durée calendaire : 00 h 50 min 27 s, pauses, attentes, prévol, tests et archivage inclus. 173 messages (100,0 %), 677 parties (100,0 %), 120 appels d’outils (100,0 %). 25 mandats CAB unitaires exécutés et vérifiés (100,0 % des mandats clôturés de ce change), 0 refus de permission observé.

Un appel terminé est classé réussi autorisé ; cela ne prouve pas à lui seul une approbation manuelle. Les opérations mutables sont rapprochées des décisions CAB corrélées et des preuves natives ; les lectures autorisées par politique restent distinctes. Les délais MCP et rejets de schéma sans dispatch sont des erreurs techniques, jamais des refus de permission ni des exécutions.

| Type | Total | Part | Réussis autorisés | Refus explicites | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Tous outils | 120 | 100.0 % | 113 (94.2 %) | 0 (0.0 %) | 7 (5.8 %) |

| Compteur de tokens natif | Nombre | Part du total catégorisé |
| --- | --- | --- |
| input | 1226220 | 7.1 % |
| output | 38764 | 0.2 % |
| reasoning | 15527 | 0.1 % |
| cache_read | 16027015 | 92.6 % |
| cache_write | 0 | 0.0 % |
| Total catégorisé | 17307526 | 100,0 % |

Input, output, reasoning et cache sont les compteurs distincts exposés par OpenCode, sans conversion en consommation facturée. Coût natif cumulé des réponses : 0.165534230, unité monétaire non exposée donc conversion en euros N/A. Compactages dans cette session : 0. Les cycles parent antérieurs ne sont pas imputés à ce change.

Sondes prévues : début, +30 min, fin ; 3/3 réussies (100,0 %), 0/3 échouées (0,0 %), 0/3 manquées (0,0 %). La sonde +30 min a été relevée avec environ 41 s de retard, sans reconstruction rétroactive. Le quota et la sonde initiaux ont été collectés après prévol/inventaire, avant la première écriture ; ils ne couvrent pas rétrospectivement le prévol.

| Position UTC | Horodatage | TTMT | Débit réel | Sortie tokens | Durée sonde |
| --- | --- | --- | --- | --- | --- |
| début | 2026-10-13T20:24:37.956826+00:00 | 10.440 s | 297.047 t/s | 822 | 13.236 s |
| +30 min | 2026-10-13T20:55:17.987570+00:00 | 2.336 s | 238.676 t/s | 834 | 5.852 s |
| fin | 2026-10-13T21:04:44.442222+00:00 | 2.461 s | 194.010 t/s | 827 | 6.878 s |

TTMT min/max : 2.336/10.440 s ; débit min/max : 194.010/297.047 t/s. Surcharge télémétrie séparée de la production : 2483 tokens de sortie, 25.966 s de durée calendaire cumulée. Coût initial/intermédiaire N/A (non collecté), coût final natif 0.0011748 ; coût total des sondes N/A.

Prompt identique des trois sondes, sans outil/fichier/réseau dans leurs sessions dédiées : Sans outil, fichier, réseau ni commentaire : répète exactement 80 fois la phrase suivante, une phrase par ligne : Le contrôle mesure une sortie fixe sans action métier.

Les identifiants des sessions et messages, les mesures et les horodatages disponibles sont conservés dans statistics.probes du checkpoint. Les instants absolus envoi/premier/dernier token des deux premières sondes ne sont pas conservés (N/A), leurs deltas mesurés restent disponibles ; la sonde finale conserve les trois instants. Version exacte du modèle N/A, non déduite de son nom.

Résultats : 3/3 compilations réussies (100,0 %), 16/16 tests ciblés réussis (100,0 %), 8/8 tâches prouvées cochées (100,0 %), validation stricte du change avant et après code sans issue, canon 78/78 et base combinée 80/80 valides. Trois WARNING bulk historiques identiques ; validation globale non stricte, ne pas confondre avec une validation globale strict réussie.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 45 | 26.0 % |
| assistant | 128 | 74.0 % |
| Total | 173 | 100,0 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 166 | 24.5 % |
| step-start | 128 | 18.9 % |
| reasoning | 135 | 19.9 % |
| tool | 120 | 17.7 % |
| step-finish | 128 | 18.9 % |
| Total | 677 | 100,0 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 86 | 67.2 % |
| stop | 42 | 32.8 % |
| Total | 128 | 100,0 % |

| Type | Total | Part | Réussis autorisés | Refus explicites | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| bash | 18 | 15.0 % | 17 (94.4 %) | 0 (0.0 %) | 1 (5.6 %) |
| cgpt-validation_broker_health | 2 | 1.7 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 18 | 15.0 % | 18 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 13 | 10.8 % | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 4 | 3.3 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 25 | 20.8 % | 22 (88.0 %) | 0 (0.0 %) | 3 (12.0 %) |
| default.write | 1 | 0.8 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| glob | 5 | 4.2 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 1 | 0.8 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 25 | 20.8 % | 23 (92.0 %) | 0 (0.0 %) | 2 (8.0 %) |
| write | 8 | 6.7 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 120 | 100.0 % | 113 (94.2 %) | 0 (0.0 %) | 7 (5.8 %) |

Les erreurs comprennent trois timeouts request_validation récupérés par polling corrélé, deux échecs read (outil indisponible, schéma), un default.write indisponible et un bash sans command rejeté avant dispatch. Aucune de ces erreurs n’est présentée comme un effet exécuté. Une rectification CGPT de clé resources avant décision n’a changé ni la commande ni sa cible.

## 3. Fichiers modifiés

| Type | Total | Part | Réussis autorisés | Refus explicites | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-contribution-type-vocabulary/design.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-contribution-type-vocabulary/proposal.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-contribution-type-vocabulary/specs/frontend/spec.md | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-frontend-contribution-type-vocabulary/tasks.md | 2 | 22.2 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/frontend_contribution_types.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_frontend_contribution_type_integration.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_frontend_contribution_type.py | 1 | 11.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| N/A — appel indisponible avant dispatch | 1 | 11.1 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| Total tentatives fichiers | 9 | 100.0 % | 8 (88.9 %) | 0 (0.0 %) | 1 (11.1 %) |

Ce tableau compte les tentatives d’outils, pas les fichiers uniques. Le fichier de tâches a été écrit à la création puis coché après preuves. Quatre artefacts OpenSpec ont été déplacés par l’archivage unique vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-initial-frontend-contribution-type-vocabulary ; les trois fichiers Python restent à leur emplacement. Les quatre contenus archivés, les trois contenus Python et UTF-8/LF sont prouvés. Le présent STATISTIQUES.md est produit après l’intervalle par un mandat distinct et n’est pas ajouté rétroactivement à ces compteurs. Façade kernel, cadrages et 78 empreintes canoniques inchangés.

## 4. Commandes

| Type | Total | Part | Réussis autorisés | Refus explicites | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Compilation Python | 3 | 16.7 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Erreur avant dispatch | 1 | 5.6 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| OpenSpec | 5 | 27.8 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Prévol CAB /usr/bin/true | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 8 | 44.4 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total tentatives commandes | 18 | 100.0 % | 17 (94.4 %) | 0 (0.0 %) | 1 (5.6 %) |

Libellés limités à 100 caractères ; les commandes intégrales et callID sont dans les mandats et preuves du checkpoint.

| Type | Total | Part | Réussis autorisés | Refus explicites | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| /usr/bin/true | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| N/A — SchemaError avant dispatch, aucune commande | 1 | 5.6 % | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| /home/devops/.local/npm/bin/openspec validate add-initial-frontend-contribution-type-vocabulary --s… | 2 | 11.1 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/kernel/frontend_contribution_types… | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_frontend_contribution_type.… | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_frontend_contributio… | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/devops… | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/devops… | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/devops… | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/devops… | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/devops… | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/devops… | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/devops… | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src /home/devops… | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --specs --json | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec validate --all --json | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/.local/npm/bin/openspec archive add-initial-frontend-contribution-type-vocabulary --sk… | 1 | 5.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 18 | 100.0 % | 17 (94.4 %) | 0 (0.0 %) | 1 (5.6 %) |

Commandes refusées regroupées : aucune (0 occurrence ; part 0,0 % des tentatives). Une tentative bash invalide sans commande est une erreur technique préalable au dispatch. Toutes les commandes effectivement exécutées ont exit0. L’archivage --skip-specs --yes a réussi une fois, avec avertissement non bloquant : titres « Pourquoi/Quoi » du proposal plutôt que « Why/What Changes » attendus par son contrôle documentaire ; le change reste strict valide et le canon est inchangé.

## 5. Accès web

| Type | Total | Part | Réussis autorisés | Refus explicites | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Web | 0 | N/A | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucun outil web ni URL externe visitée dans l’historique de production (0). Taux web N/A car dénominateur nul. Les appels de pilotage HTTP locaux OpenCode/CAB ne sont pas des visites web externes. Aucune URL refusée observée. L’orchestrateur lit les quotas par l’outil natif ; les sondes n’utilisent aucun outil ni réseau.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-13T20:15:10.332000+00:00 |
| Fin — après archivage | 2026-10-13T21:05:37.874054+00:00 |
| Durée globale (pauses et attentes incluses) | 00 h 50 min 27 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — avant première écriture | 2026-10-13T20:24:37.950829+00:00 | 9 % | 2026-10-20T04:59:31+00:00 |
| Après — après archivage et sonde finale | 2026-10-13T21:05:37.874043+00:00 | 9 % | 2026-10-20T04:59:31+00:00 |
| Différence après − avant | — | 0 points de pourcentage | — |

Même quota codex, fenêtre 10080 minutes et même réinitialisation. Quotas partagés par le compte ; la variation peut inclure d’autres tâches simultanées. Une variation nulle peut refléter la précision ou le délai du compteur ; aucune attribution exclusive ni conversion en tokens/euros.

| Type | Total | Part | Réussis autorisés | Refus explicites | Erreurs techniques |
| --- | --- | --- | --- | --- | --- |
| Fichiers | 9 | 7.5 % | 8 (88.9 %) | 0 (0.0 %) | 1 (11.1 %) |
| Commandes | 18 | 15.0 % | 17 (94.4 %) | 0 (0.0 %) | 1 (5.6 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 93 | 77.5 % | 88 (94.6 %) | 0 (0.0 %) | 5 (5.4 %) |
| Total global | 120 | 100.0 % | 113 (94.2 %) | 0 (0.0 %) | 7 (5.8 %) |

Totaux croisés vérifiés : outils par type = domaines = 120 ; réussites + refus + erreurs = 120. Tests et compilations passés, archivage réussi, rapport distinct en cours de production à la fin de cet intervalle. Publication et gate ne sont pas revendiqués rétroactivement. Git non inspecté et aucune opération Git mandatée ; aucun effet externe mandaté, aucun secret dans les fichiers créés ni dans ce rapport. Les vérifications navigateur, npm et PostgreSQL sont non applicables à cette seule Enum Python structurelle. Aucun changement de dépendance. Le parent CISMP reprend SÉLECTION après publication, gate, désarmement et libération vérifiés.
