# STATISTIQUES — add-bulk-runtime-admission-identity-persistence-v1

Archive : `openspec/changes/archive/2026-10-12-add-bulk-runtime-admission-identity-persistence-v1`. Session : `ses_ed1394509ffeTDOu37OW4Rf18W`. RUN : `cismp-pixs-8a57078ff4d44bde`.

Périmètre : historique natif OpenCode du début de cette session au relevé final après archivage, hors sondes jetables, rédaction de ce rapport et second compactage postérieur. Les métriques internes Codex non exposées restent N/A.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.0 ; modèle N/A | opencode-go | high | 3.666 s | 326.408 | N/A |
| muse-spark-1.3-contributor — compactage | OpenCode 1.19.0 ; modèle N/A | opencode-go | N/A non exposé | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-6 (famille déclarée), orchestrateur Codex | N/A version native non exposée | OpenAI | N/A | N/A | N/A | N/A |

Version du modèle non publiée par la télémétrie ; aucune déduction depuis son nom. TTMT et débit sont les moyennes arithmétiques des sondes valides, sortie textuelle visible. Temps de génération actif et dénominateur cumulé tous agents : N/A ; durée calendaire, outils et attentes ne sont pas assimilés au service. Des activités ont pu se chevaucher.

## 1. Statistiques générales et décisions

Durée calendaire : **02 h 46 min 14 s**, pauses et attentes incluses. 582 messages, 255 appels d’outils : 253 succès (99.2 %), 0 refus (0.0 %), 2 erreurs techniques (0.8 %). 36 décisions CAB uniques approved (100 %), 0 rejected/needs_clarification ; 36 permissions natives once corrélées, consommées une seule fois.

Convention : un appel réussi peut être autorisé automatiquement ; il ne prouve pas une approbation manuelle. Les 36 opérations mutantes/commandes sont, elles, corrélées à des décisions explicites CGPT. Un code 1 global OpenSpec est qualifié uniquement par les trois WARNING historiques exacts ; il n’est pas présenté comme une validation globale verte.

Résultat : 377 tests sans échec ni test ignoré, 22 contrôles PostgreSQL réels, 8 compilations. Archive unique --skip-specs réussie, canon préservé. Fondation de persistance B10 seulement : aucune admission publique, autorité, rétention active ou déduplication/rejeu complet ajouté.

Deux erreurs natives réconciliées : timeout MCP repris par poll_approval sur le même approval_id ; lecture préalable de proposal.md absent avant sa création. Un brouillon après compactage a été rejeté avant écriture pour API inventées, puis contexte relu et brouillon corrigé ; ce rejet de revue ne constitue pas un refus de permission CAB.

Un compactage natif OpenCode dans les bornes ; le second après les bornes est exclu des compteurs de production. API native de compactage du thread Codex non exposée : cycle conjoint incomplet, sans arrêt de travail.

Sondes : 7 prévues/mesurées valides (100 %), 0 échouée ; les cinq échéances périodiques ont été relevées en retard, toutes datées à l’heure réelle, aucune reconstruction rétroactive. Retards détaillés ci-dessous.

| Position | Envoi réel | Échéance | Retard (s) | TTMT (s) | Tokens/s | Tokens sortie |
| --- | --- | --- | --- | --- | --- | --- |
| début identité durable | 2026-10-12T08:27:10.693260+02:00 | — | — | 9.248 | 347.213 | 949 |
| périodique — heure réelle | 2026-10-12T09:00:13.495331+02:00 | 2026-10-12T08:57:22.858900+02:00 | 170.6 | 3.413 | 265.869 | 890 |
| périodique — heure réelle | 2026-10-12T09:27:43.814111+02:00 | 2026-10-12T09:27:22.858900+02:00 | 21.0 | 2.639 | 277.404 | 890 |
| périodique — heure réelle | 2026-10-12T09:58:07.462532+02:00 | 2026-10-12T09:57:22.858900+02:00 | 44.6 | 2.659 | 376.211 | 913 |
| périodique — heure réelle | 2026-10-12T10:38:35.860449+02:00 | 2026-10-12T10:27:22.858900+02:00 | 673.0 | 2.453 | 331.684 | 890 |
| périodique — heure réelle | 2026-10-12T11:02:48.949988+02:00 | 2026-10-12T10:57:22.858900+02:00 | 326.1 | 3.24 | 305.24 | 906 |
| fin après archive identité B10 | 2026-10-12T11:08:26.702055+02:00 | — | — | 2.012 | 381.233 | 890 |

TTMT min/max : 2.012/9.248 s. Débit min/max : 265.869/381.233 tokens/s. Prompt identique : « Sans outil, fichier ni réseau. Écris exactement 80 lignes identiques : Mesure de débit de la session de codage. ». Surcharge des sondes : 6328 tokens de sortie ; coût natif 0.010199152, hors production.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 181 | 31.1 % |
| assistant | 401 | 68.9 % |
| Total | 582 | 100 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 534 | 26.6 % |
| step-start | 401 | 20.0 % |
| reasoning | 414 | 20.6 % |
| tool | 255 | 12.7 % |
| step-finish | 401 | 20.0 % |
| compaction | 1 | 0.0 % |
| Total | 2006 | 100 % |

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 133 | 52.2 % | 133 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 36 | 14.1 % | 35 (97.2 %) | 0 (0.0 %) | 1 (2.8 %) |
| bash | 23 | 9.0 % | 23 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 2 | 0.8 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 40 | 15.7 % | 39 (97.5 %) | 0 (0.0 %) | 1 (2.5 %) |
| glob | 6 | 2.4 % | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 1 | 0.4 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 | 0.4 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 13 | 5.1 % | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 255 | 100 % | 253 (99.2 %) | 0 (0.0 %) | 2 (0.8 %) |

| Fin de réponse | Nombre | Part |
| --- | --- | --- |
| tool-calls | 222 | 55.4 % |
| stop | 179 | 44.6 % |
| Total | 401 | 100 % |

| Tokens natifs | Nombre | Part des composantes |
| --- | --- | --- |
| entrée | 4411585 | 7.6 % |
| sortie | 108653 | 0.2 % |
| raisonnement | 22107 | 0.0 % |
| cache lecture | 53653496 | 92.2 % |
| cache écriture | 0 | 0.0 % |
| Total composantes | 58195841 | 100 % |

Composantes tokens issues de la télémétrie native ; cohérence avec tokens.total pour chaque réponse : True. Coût natif production cumulé : 0.574617492 (unité/devise non exposée par cette API, aucune conversion).

## 3. Fichiers modifiés

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-runtime-admission-identity-persistence-v1/proposal.md | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-runtime-admission-identity-persistence-v1/design.md | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-runtime-admission-identity-persistence-v1/tasks.md | 2 | 15.4 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-runtime-admission-identity-persistence-v1/specs/interactions/spec.md | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_admission_identity_values.py | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_admission_identity_record.py | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/bulk_admission_identity_repository.py | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/migrations/0005_bulk_admission_identity.py | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/models.py | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_bulk_admission_identity_values.py | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_admission_identity_integration.py | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_bulk_admission_identity_postgres_integration.py | 1 | 7.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 13 | 100 % | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Ces nombres sont des tentatives write/edit, non des lignes de code. 12 cibles distinctes, 13 écritures réussies : tasks.md écrit puis coché après preuves. Les quatre artefacts OpenSpec ont été déplacés par la commande d’archivage ; chemins actuels ci-dessus. La commande new a aussi créé /home/devops/datas/pixs/openspec/changes/archive/2026-10-12-add-bulk-runtime-admission-identity-persistence-v1/.openspec.yaml (hors compteur write). Ce STATISTIQUES.md est publié après la fin de l’intervalle, sous mandat distinct, et exclu des compteurs pour éviter l’auto-comptage. Aucun autre fichier de cadrage/canon modifié.

## 4. Commandes

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| Prévol true | 1 | 4.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec | 5 | 21.7 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Compilation Python | 8 | 34.8 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| unittest | 8 | 34.8 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| PostgreSQL réel isolé | 1 | 4.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 23 | 100 % | 23 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

| Commande (100 caractères max) | Nombre | Part |
| --- | --- | --- |
| /usr/bin/true | 1 | 4.3 % |
| /home/devops/.local/npm/bin/openspec new change add-bulk-runtime-admission-identity-persistence-v1 | 1 | 4.3 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate add-bulk-runtime-… | 2 | 8.7 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_admission_identity_va… | 1 | 4.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_admission_identity_re… | 1 | 4.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_admission_identity_re… | 1 | 4.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/migrations/0005_bulk_admis… | 1 | 4.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/models.py | 1 | 4.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_admission_identity_val… | 1 | 4.3 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_admiss… | 1 | 4.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_admission_ident… | 1 | 4.3 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_bulk… | 1 | 4.3 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_runtim… | 1 | 4.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/integration/test_bulk_admission_ident… | 1 | 4.3 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_bulk… | 1 | 4.3 % |
| /home/devops/datas/pixs/.venv/bin/python3 -B tests/integration/test_bulk_admission_identity_postgre… | 1 | 4.3 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_operat… | 1 | 4.3 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest integration.test_bulk… | 1 | 4.3 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_semver_cons… | 1 | 4.3 % |
| PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest unit.test_bulk_runtim… | 1 | 4.3 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate --all --strict --… | 1 | 4.3 % |
| OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec archive add-bulk-runtime-a… | 1 | 4.3 % |
| Total | 23 | 100 % |

Aucune commande refusée : 0 (0.0 %). Les libellés longs sont tronqués à 100 caractères, indicateur inclus ; les commandes complètes et requestId restent dans l’historique natif et le checkpoint. Le global strict a rendu code 1 pour les seuls trois WARNING historiques de longueur ; les deux validations strictes du change ont rendu code 0 sans issue.

## 5. Accès web

Aucun webfetch/websearch : 0 succès, 0 refus, 0 erreur ; parts N/A (dénominateur nul), aucune URL visitée/refusée à lister. Les communications fournisseur LLM/quotas et API locales de pilotage autorisées sont hors de ce domaine et hors des compteurs d’outils web natifs. Aucun déploiement ou appel de service métier externe observé.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-12T08:22:18.358000+02:00 |
| Fin — après archivage | 2026-10-12T11:08:32.531185+02:00 |
| Durée globale (pauses et attentes incluses) | 02 h 46 min 14 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-10-12T08:27:10.693260+02:00 | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-12T11:08:32.531254+02:00 | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé : identité du quota codex, fenêtre 10080 minutes, usedPercent et resetsAt indisponibles ; aucune source externe substituée. Quotas partagés par le compte : une variation éventuelle pourrait inclure des tâches simultanées, aucune attribution exclusive ni conversion en tokens/euros.

| Catégorie | Total | Part | Succès | Refus | Erreurs |
| --- | --- | --- | --- | --- | --- |
| autres | 219 | 85.9 % | 217 (99.1 %) | 0 (0.0 %) | 2 (0.9 %) |
| commandes | 23 | 9.0 % | 23 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| fichiers | 13 | 5.1 % | 13 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 255 | 100 % | 253 (99.2 %) | 0 (0.0 %) | 2 (0.8 %) |

Totaux croisés : 219 autres + 23 commandes + 13 éditions + 0 web = 255 outils ; 253 succès + 0 refus + 2 erreurs = 255. Pourcentages à une décimale, écarts d’arrondi possibles. Les tableaux de fichiers comptent les tentatives write/edit ; les déplacements d’archive et métadonnées CLI ne sont pas comptés deux fois.

377 tests réussis sans ignoré, 22 contrôles PG réels sur PostgreSQL 16.15 ; forward/reverse 0005, sept tables existantes et tables publiques stables, schéma test supprimé, connexions principales et threads fermées. Huit compilations et strict change code0 sans issue. Global strict code1, uniquement trois WARNING historiques identiques, sans correction hors périmètre.

Archive unique openspec/changes/archive/2026-10-12-add-bulk-runtime-admission-identity-persistence-v1 ; rapport publié après les bornes par mandat distinct. Fondation de persistance identité B10 livrée, aucune preuve de runtime Bulk ou admission complète revendiquée. Le parent CISMP reprend la sélection après vérification de ce rapport ; aucun état TERMINÉ global n’est affirmé.

Git non inspecté et aucune commande Git, commit ou push mandatés. Aucun déploiement ; pas de navigateur/front-end concerné. Tests PG dans le seul schéma synthétique possédé ; accès fournisseurs/PLLM et API locales autorisés. Secrets confinés aux processus autorisés et stockage natif d’authentification, aucune valeur transmise au modèle, au rapport ou aux sources. Copie Syncthing conflictuelle de bulk_runtime_repository signalée et laissée intacte ; canonique conforme à son empreinte antérieure.
