# Statistiques — adoption documentaire C00

Archive : `2026-10-18-define-first-installable-pbo-profile`. Profil : `pbo-p0-debian-local-v1`.

RUN : `cismp3-pixs-f39cdc809e674373`, contexte CAB 280. Sessions de production : `ses_eb3bd0cfeffew3L5MkDJcToqLJ` puis `ses_eb3b77417ffeAMRjAtqfMAcYHi`. Collecte arrêtée avant la rédaction de ce rapport. La durée comprend les attentes d’authentification et de validation humaine ; elle ne représente pas un temps de génération.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.3 ; version du modèle N/A | OpenCode Go / opencode-go | high | 1.302 s | 564.8 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex, famille GPT-6 (identité système) | N/A — version précise non exposée | OpenAI | N/A — métadonnée native non exposée | N/A | N/A | N/A |

Les moyennes du codage proviennent de trois sondes valides, avec le même modèle/fournisseur/high. Elles utilisent l’envoi côté orchestrateur et les bornes natives de la partie texte ; ce ne sont pas des mesures SSE client. Le débit porte sur les tokens de réponse exposés par OpenCode. Aucun sondage de l’orchestrateur. Le dénominateur du temps de service n’est pas mesurable : les bornes disponibles mêlent appels, attentes et génération ; aucune durée busy ou calendaire n’y est substituée.

## 1. Statistiques générales et décisions

| Mesure | Valeur | Part / précision |
| --- | --- | --- |
| Messages de production | 202 | 100 % des messages des deux sessions |
| Appels d’outils | 129 | 100 % de l’historique natif |
| Exécutés / terminés avec succès | 117 | 90.7 % |
| Refus natifs de permission | 0 | 0.0 % |
| Erreurs ou sorties non nulles | 12 | 9.3 % |
| Décisions CAB approuvées / once observées | 22 / 22 | 100 % des décisions approuvées ont une once |
| Mandats annulés avant effet | 3 | 12,0 % des 25 demandes request_validation |
| Compactages natifs observés | 0 | Aucune réussite conjointe de compactage revendiquée |

Convention : « exécuté » désigne un appel natif terminé, avec autorisation automatique de lecture ou décision CAB unitaire selon son type. Un succès de lecture ne prouve pas une approbation manuelle. Les sorties 1 des trois validations globales comptent comme contrôles en erreur, avec leurs avertissements ; elles ne sont ni refus de permission ni tests produit échoués. Les autres erreurs sont des délais, interruptions MCP ou une erreur de lecture.

| Décision des 25 demandes natives | Nombre | Part |
| --- | --- | --- |
| Approuvées | 22 | 88.0 % |
| Annulées sans effet | 3 | 12.0 % |
| Refusées | 0 | 0.0 % |
| En attente | 0 | 0.0 % |
| Total | 25 | 100 % |

Incidents préservés : démarrage lent du broker et délai MCP, interruption d’un prévol sans effet puis récupération dans le même RUN, commande JSON préparée par CGPT dépassant la limite de 2 000 caractères, et révision de destination à relever après déplacement. Les trois mandats annulés n’ont exécuté aucune mutation. Les reprises ont utilisé des identités inédites ; aucun archivage ni effet prouvé n’a été rejoué.

| Tokens natifs de production | Nombre | Part du total exposé |
| --- | --- | --- |
| Entrée hors cache | 1154565 | 2.5 % |
| Réponse | 46679 | 0.1 % |
| Raisonnement | 11440 | 0.0 % |
| Cache lu | 44230589 | 97.3 % |
| Cache écrit | 0 | 0.0 % |
| Total | 45443273 | 100 % |

Coût cumulé exposé par OpenCode : 0.215541478 en unité native non précisée par la réponse API ; aucune conversion monétaire. Les valeurs absentes des tours interrompus ne sont pas reconstituées. Le coût et les tokens des sondes sont séparés ci-dessous.

| Sonde | Horodatage d’envoi | TTMT | Tokens/s | Tokens de réponse | Résultat |
| --- | --- | --- | --- | --- | --- |
| début | 18/10/2026 01:45:42 CEST | 1.380 s | 449.3 | 368 | Valide |
| +30 minutes après reprise | 18/10/2026 18:34:46 CEST | 1.410 s | 510.4 | 368 | Valide |
| fin après archivage | 18/10/2026 18:44:13 CEST | 1.116 s | 734.5 | 368 | Valide |

Relèves : 3 prévues, 3 valides, 0 échouée, 0 manquée pendant l’activité. La pause d’attente humaine ne donne lieu à aucune sonde reconstruite. La relève après reprise a été envoyée environ 37 s après son échéance. TTMT min/max : 1.116/1.410 s ; débit min/max : 449.3/734.5.

Surcharge des sondes : 1104 tokens de réponse, coût natif 0.003968952, exclus des compteurs de production. Prompt constant : nombres 0001 à 0120, un par ligne, sans outil ni autre texte ; sortie vérifiée identique. Le benchmark PLLM est distinct des sondes et n’est pas utilisé pour leur moyenne.

PLLM conservée : mode 1, Muse high ; benchmark frais à la reprise valide, palier 2 048, TTFT 3,9935 s. Quotas OpenCode Go au relevé de reprise : 3 % utilisés sur 5 h, 66 % sur la semaine, 98 % sur le mois. Ces valeurs datées ne sont pas des quotas Codex et n’établissent pas une consommation exclusive de ce RUN.

Couverture CAB : le collecteur expose 124 observations de latence terminale, contre 129 appels dans l’historique natif complet. Ces périmètres ne sont pas additionnés et leur écart n’est pas attribué à une cause non prouvée. Les compteurs d’appels de ce rapport proviennent de l’historique natif.

| Latence CAB | Moyenne | Médiane | P95 | Observations |
| --- | --- | --- | --- | --- |
| Demande → décision | 32.139 s | 15.651 s | 102.553 s | 22 |
| Décision → once | 5.050 s | 5.329 s | 6.973 s | 22 |

Échecs HTTP de garde observés, sans les confondre avec des permissions refusées : run-pause = 1, native-validation-not-correlated = 8, request-reconciliation-required = 3, resource-revision-stale = 3.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| assistant | 144 | 71.3 % |
| user | 58 | 28.7 % |
| Total | 202 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| reasoning | 148 | 21.1 % |
| step-finish | 141 | 20.1 % |
| step-start | 143 | 20.4 % |
| text | 141 | 20.1 % |
| tool | 129 | 18.4 % |
| Total | 702 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| N/A | 3 | 2.1 % |
| stop | 39 | 27.1 % |
| tool-calls | 102 | 70.8 % |
| Total | 144 | 100 % |

| Outil | Total | Part globale | Exécuté | Refusé | Erreur / sortie non nulle |
| --- | --- | --- | --- | --- | --- |
| bash | 22 | 17.1 % | 19 (86.4 %) | 0 (0.0 %) | 3 (13.6 %) |
| cgpt-validation_broker_health | 1 | 0.8 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 15 | 11.6 % | 14 (93.3 %) | 0 (0.0 %) | 1 (6.7 %) |
| cgpt-validation_cancel_approval | 3 | 2.3 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 9 | 7.0 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 7 | 5.4 % | 7 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 4 | 3.1 % | 2 (50.0 %) | 0 (0.0 %) | 2 (50.0 %) |
| cgpt-validation_request_validation | 25 | 19.4 % | 20 (80.0 %) | 0 (0.0 %) | 5 (20.0 %) |
| glob | 4 | 3.1 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 4 | 3.1 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 35 | 27.1 % | 34 (97.1 %) | 0 (0.0 %) | 1 (2.9 %) |
| Total | 129 | 100 % | 117 (90.7 %) | 0 (0,0 %) | 12 (9.3 %) |

Les réponses de décision, messages, parties, tokens et step-finish ne sont pas additionnés entre eux. Les tokens sont pris une fois par message assistant ; les parties step-finish ne sont pas recomptées.

## 3. Fichiers modifiés

Comptage des tentatives natives d’écriture effectivement exécutées, rebasé sur les chemins finaux. Les demandes annulées avant permission n’y deviennent pas des écritures en erreur.

| Chemin absolu | Écritures | Part | Approuvées/exécutées | Refusées | En erreur |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile/applicabilite-pzt-dns.json | 1 | 8.3 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile/applicabilite-pzt-dns.md | 2 | 16.7 % | 2 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile/design.md | 2 | 16.7 % | 2 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile/specs/deb-package/spec.md | 1 | 8.3 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile/specs/pzt/spec.md | 1 | 8.3 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile/specs/reference-composition/spec.md | 1 | 8.3 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile/tasks.md | 1 | 8.3 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/specs/deb-package/spec.md | 1 | 8.3 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/specs/pzt/spec.md | 1 | 8.3 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| /home/devops/datas/pixs/openspec/specs/reference-composition/spec.md | 1 | 8.3 % | 1 (100 %) | 0 (0 %) | 0 (0 %) |
| Total : 10 fichiers | 12 | 100 % | 12 (100 %) | 0 (0 %) | 0 (0 %) |

Archivage natif : 25 pièces ont été déplacées ensemble vers `/home/devops/datas/pixs/openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile`. Parmi elles, sept fichiers de C00 ont un contenu modifié — les six fichiers RSMP et tasks.md — et 18 pièces historiques restent identiques. Les trois canons sont hors de ce dossier. La matrice Markdown et design.md ont chacun une seconde écriture pour préserver leurs liens après déplacement.

Le présent `/home/devops/datas/pixs/openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile/STATISTIQUES.md` est écrit après la borne de collecte par un mandat distinct ; son écriture est exclue de ces 12 tentatives afin d’éviter une statistique autoréférente.

## 4. Commandes

| Famille | Total | Part | Exécuté | Refusé | Erreur / sortie non nulle |
| --- | --- | --- | --- | --- | --- |
| OpenSpec | 6 | 27.3 % | 3 (50.0 %) | 0 (0.0 %) | 3 (50.0 %) |
| Prévol /usr/bin/true | 2 | 9.1 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Python | 14 | 63.6 % | 14 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 22 | 100 % | 19 (86,4 %) | 0 (0 %) | 3 (13,6 %) |

| Libellé (100 caractères maximum) | Occurrences | Part | Exécuté | Refusé | Erreur |
| --- | --- | --- | --- | --- | --- |
| /usr/bin/true | 2 | 9.1 % | 2 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 3 | 13.6 % | 0 | 0 | 3 |
| Python — RSMP C00 1/6 : applicabilite-pzt-dns.json | 1 | 4.5 % | 1 | 0 | 0 |
| Python — RSMP C00 2/6 : applicabilite-pzt-dns.md | 1 | 4.5 % | 1 | 0 | 0 |
| Python — RSMP C00 3/6 : spec.md | 1 | 4.5 % | 1 | 0 | 0 |
| Python — RSMP C00 4/6 : spec.md | 1 | 4.5 % | 1 | 0 | 0 |
| Python — RSMP C00 5/6 : spec.md | 1 | 4.5 % | 1 | 0 | 0 |
| Python — RSMP C00 6/6 : design.md | 1 | 4.5 % | 1 | 0 | 0 |
| Python — Vérifier les six fichiers RSMP et la matrice complète | 1 | 4.5 % | 1 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec validate define-first-installable-pbo-profile --strict | 1 | 4.5 % | 1 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec archive --help | 1 | 4.5 % | 1 | 0 | 0 |
| Python — Synchroniser le canon reference-composition depuis C00 | 1 | 4.5 % | 1 | 0 | 0 |
| Python — Synchroniser le canon pzt depuis C00 | 1 | 4.5 % | 1 | 0 | 0 |
| Python — Synchroniser le canon deb-package depuis C00 | 1 | 4.5 % | 1 | 0 | 0 |
| Python — Cocher les six tâches C00 après les preuves d’adoption | 1 | 4.5 % | 1 | 0 | 0 |
| /home/devops/.local/npm/bin/openspec archive define-first-installable-pbo-profile --yes --skip-specs | 1 | 4.5 % | 1 | 0 | 0 |
| Python — Conserver les liens de applicabilite-pzt-dns.md après archivage | 1 | 4.5 % | 1 | 0 | 0 |
| Python — Conserver les liens de design.md après archivage | 1 | 4.5 % | 1 | 0 | 0 |
| Python — Vérifier l’archive C00 et son adoption canonique | 1 | 4.5 % | 1 | 0 | 0 |
| Total | 22 | 100 % | 19 | 0 | 3 |

Les scripts Python sont identifiés par le titre du mandat approuvé ; la commande exacte et son empreinte sont conservées dans l’historique natif et le checkpoint du RUN. Commandes refusées : aucune, 0/22 (0 %). Les trois sorties 1 correspondent exclusivement aux validations globales strictes avec les quatre avertissements préexistants.

## 5. Accès web

| Accès web par outils de la session | Total | Approuvés/exécutés | Refusés | Erreur | Part |
| --- | --- | --- | --- | --- | --- |
| webfetch / websearch | 0 | 0 (N/A) | 0 (N/A) | 0 (N/A) | N/A |
| Total | 0 | 0 (N/A) | 0 (N/A) | 0 (N/A) | N/A |

Aucune URL visitée par un outil web et aucune requête web de recherche. Les communications API nécessaires au fournisseur et à CAB ne sont pas des pages consultées. Le nombre complet de requêtes de transport et de leurs reprises n’est pas exposé : N/A, sans reconstruction.

| Endpoint observé hors outils web | Statut et portée |
| --- | --- |
| https://opencode.ai/zen/go/v1/usage | Contrôle de quota autorisé ; HTTP 401 initialement, puis réussite après rétablissement de l’authentification. Aucun secret exposé. |
| https://opencode.ai/zen/go/v1/responses | Tests de génération PLLM autorisés, mode 1/high ; distincts des visites web et des sondes OpenCode. |
| http://127.0.0.1:4096/ | API native locale OpenCode, répertoire Pixs explicite. |
| http://127.0.0.1:8788/ | API locale CAB ; décisions unitaires de CGPT, ressources et publication. |

Un HTTP 401 fournisseur est un échec d’authentification, pas un refus de permission native. Aucun accès fournisseur ou contenu exclu supplémentaire n’a été déduit de ce diagnostic.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début — checkpoint du RUN, avant sondes | 18/10/2026 01:28:07 CEST |
| Fin — après archivage, sondes et collecte | 18/10/2026 18:47:03 CEST |
| Durée globale (pauses et attentes incluses) | 17 h 18 min 56 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 18/10/2026 01:28:07 CEST | N/A | N/A |
| Après — après archivage de la spécification | 18/10/2026 18:47:03 CEST | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif mcp__codex_app__get_usage_limits non exposé : aucun quota Codex de fenêtre 10080 minutes ni identité de compte/réinitialisation vérifiable. Ni un quota Spark, ni les quotas OpenCode Go, ni une ancienne valeur ne sont substitués. Le quota est partagé par le compte ; une différence éventuelle pourrait inclure d’autres tâches et ne serait pas attribuée exclusivement à CISMP3.

| Domaine sans double comptage | Total | Part globale | Exécuté | Refusé | Erreur |
| --- | --- | --- | --- | --- | --- |
| Fichiers : lectures/recherches | 43 | 33.3 % | 42 (97.7 %) | 0 (0.0 %) | 1 (2.3 %) |
| Commandes | 22 | 17.1 % | 19 (86.4 %) | 0 (0.0 %) | 3 (13.6 %) |
| Autres outils MCP | 64 | 49.6 % | 56 (87.5 %) | 0 (0.0 %) | 8 (12.5 %) |
| Web | 0 | 0,0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 129 | 100 % | 117 (90.7 %) | 0 (0,0 %) | 12 (9.3 %) |

Les 12 écritures documentaires sont déjà incluses dans les commandes Python, pas ajoutées une seconde fois aux 129 outils. Les totaux par rôles, parties, outils, familles, fichiers et domaines sont vérifiés séparément. Les arrondis à une décimale peuvent empêcher l’addition des pourcentages d’afficher exactement 100 %.

Résultat : profil documentaire adopté, neuf exigences et dix scénarios synchronisés sur trois canons ; six tâches closes sur preuves ; 197 références et 213 liens locaux vérifiés, 18 pièces historiques conservées. Validation ciblée C00 : 0. Validation globale finale : 1, 182/184 éléments, les mêmes quatre avertissements de longueur, aucun ERROR. Archivage unique : 0 ; avertissement non bloquant sur les titres français de proposal.md conservé sans modification de ce fichier.

Publication technique CAB : référence 39, reçu `publish-c3-2ed949dbc45d`. Aucune installation, activation, recette PostgreSQL/navigateur ou build produit n’est attesté par C00. Aucune opération Git, commit ou push. Les secrets de la PLLM ont été utilisés uniquement par le processus sécurisé, sans valeur dans les prompts, sorties ou sources. Les bornes et preuves du rapport précèdent le gate, le désarmement et la libération contrôlée du seul RUN ; leur résultat terminal sera consigné dans le checkpoint.
