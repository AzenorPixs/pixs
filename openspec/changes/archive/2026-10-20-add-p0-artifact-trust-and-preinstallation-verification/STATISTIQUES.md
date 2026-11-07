# Statistiques de session — N03

Projet Pixs ; change add-p0-artifact-trust-and-preinstallation-verification ; RUN cismp2-pixs-ac0840c5f4524da9 ; contextId 423 ; session ses_ea7d229efffe8mhOwKaAxc0akA.

Périmètre : historique natif OpenCode/CAB du RUN technique de réalisation, complété par quotas Codex, sondes et deux recherches documentaires connues. Les autres messages/outils/tokens Codex ne sont pas exportés : N/A. La sélection et les attentes du parent historique restent séparées dans son checkpoint.

La borne finale précède la rédaction du rapport et la clôture ; leurs outils ne sont pas inclus. Un appel réussi autorisé automatiquement ne prouve pas une approbation manuelle. Une commande exit non nul est une erreur ; un refus exige une preuve explicite de permission refusée. Les erreurs MCP et les effets de source restent distincts.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor — 226 réponses | OpenCode 1.19.3 ; version LLM N/A | opencode-go | high | 2.1267 s — sondes | 406.430 — sondes | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex — modèle exact non exposé | N/A | OpenAI | N/A | N/A | N/A | N/A |

Les bornes exclusives de génération et le dénominateur de temps de service cumulé ne sont pas exposés. Les durées busy/idle ou de message peuvent contenir des attentes ; elles ne sont pas assimilées au temps de service.

## 1. Statistiques générales et décisions

Durée calendaire : **01 h 22 min 26 s**, pauses et attentes comprises. Résultat : 35 tests finaux OK, six fichiers compilés puis le module corrigé recompilé, strict 193/193 avant archive et 192/192 après archive. Un échec diagnostique initial est corrigé. Une seule archive est exécutée ; aucun P0 global n’est annoncé.

- Messages natifs : 338 ; parties : 1201 ; outils natifs : 202.
- Décisions CAB : 32 approuvées, 0 refusées, 0 clarifications, 0 en attente ; once : 32.
- Tokens natifs bruts : total 97081754, input 1223603, output 147154, reasoning 32693, cache.read 95678304, cache.write 0. Aucune conversion de quota en tokens.
- Champ coût natif cumulé : 0.34968631 sur 226 réponses renseignées ; devise/frais d’abonnement non exposés, coût financier total N/A.
- Compactages dans l’intervalle : aucun appel initié ou observé par ce RUN ; compactages internes non exposés N/A.

Compteurs d’admission HTTP, retries possibles et distincts des commandes : {"resource-revision-stale": 8, "native-validation-not-correlated": 5, "operation-outside-reservation": 4, "request-reconciliation-required": 3}.

Les demandes périmées annulées, erreurs de schéma avant enregistrement et outil indisponible après relance en lecture seule ont été réconciliés sans effet hors périmètre. Aucune archive rejouée. La variation de notation d’un littéral Unicode de test est réconciliée par égalité d’AST.

| Sonde | Horodatage UTC | Statut | TTMT (s) | Tokens/s | Tokens de sortie |
|---|---|---|---:|---:|---:|
| début | 2026-10-20T07:27:01.406096+00:00 | success | 2.8686 | 378.944 | 318 |
| +30 min | 2026-10-20T07:57:50.120652+00:00 | success | 2.4847 | 324.184 | 297 |
| +60 min — retard 95.3 s | 2026-10-20T08:29:28.959215+00:00 | success | 1.6235 | 431.2 | 297 |
| fin | 2026-10-20T08:47:04.084299+00:00 | success | 1.5302 | 491.392 | 297 |

Sondes : 4 prévues/mesurées, 4 valides, 0 invalides, zéro relève manquée ; +60 min explicitement tardive. Même prompt et taille, même modèle/fournisseur/high, aucun outil ni accès projet. Moyennes arithmétiques TTMT 2.1267 s et débit 406.430 tokens/s. Plages TTMT 1.5302–2.8686 s ; débit 324.184–491.392. Surcharge distincte : 1209 tokens de sortie ; coût N/A. Orchestrateur non sondé.

## 2. Types de messages et d’outils

| Rôle natif | Nombre | Part |
|---|---:|---:|
| assistant | 226 | 66.9 % |
| user | 112 | 33.1 % |
| **Total** | **338** | **100 %** |

| Type de partie | Nombre | Part |
|---|---:|---:|
| reasoning | 249 | 20.7 % |
| step-finish | 225 | 18.7 % |
| step-start | 226 | 18.8 % |
| text | 299 | 24.9 % |
| tool | 202 | 16.8 % |
| **Total** | **1201** | **100 %** |

| Terminaison | Nombre | Part |
|---|---:|---:|
| non exposée | 1 | 0.4 % |
| stop | 71 | 31.4 % |
| tool-calls | 153 | 67.7 % |
| unknown | 1 | 0.4 % |
| **Total** | **226** | **100 %** |

| Outil natif | Total | Part | Succès | Taux | Refus | Taux | Erreurs | Taux | Inconnus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| bash | 11 | 5.4 % | 10 | 90.9 % | 0 | 0.0 % | 1 | 9.1 % | 0 |
| cgpt-validation_broker_health | 19 | 9.4 % | 19 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| cgpt-validation_broker_readiness | 28 | 13.9 % | 28 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| cgpt-validation_cancel_approval | 4 | 2.0 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| cgpt-validation_get_approval | 13 | 6.4 % | 13 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| cgpt-validation_list_pending | 19 | 9.4 % | 19 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| cgpt-validation_poll_approval | 1 | 0.5 % | 0 | 0.0 % | 0 | 0.0 % | 1 | 100.0 % | 0 |
| cgpt-validation_request_validation | 38 | 18.8 % | 27 | 71.1 % | 0 | 0.0 % | 11 | 28.9 % | 0 |
| edit | 10 | 5.0 % | 10 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| glob | 4 | 2.0 % | 4 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| grep | 7 | 3.5 % | 7 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| invalid | 1 | 0.5 % | 0 | 0.0 % | 0 | 0.0 % | 1 | 100.0 % | 0 |
| read | 36 | 17.8 % | 36 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| write | 11 | 5.4 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| **Total** | **202** | **100 %** | **188** | **93.1 %** | **0** | **0.0 %** | **14** | **6.9 %** | **0** |

Le type invalid est une erreur technique sans écriture ni once consommée. La cancellation MCP réussie n’est pas un refus de permission.

## 3. Fichiers modifiés

Compteurs de tentatives natives edit/write, avec résultats et pourcentages ; les fichiers indirectement déplacés par la commande d’archive sont signalés séparément.

| Chemin absolu complet | Total | Part | Succès | Taux | Refus | Taux | Erreurs | Taux | Inconnus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/BUILD.md | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/TECHNICAL.md | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/openspec/changes/add-p0-artifact-trust-and-preinstallation-verification/design.md | 2 | 9.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/openspec/changes/add-p0-artifact-trust-and-preinstallation-verification/proposal.md | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/openspec/changes/add-p0-artifact-trust-and-preinstallation-verification/requirements.md | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/openspec/changes/add-p0-artifact-trust-and-preinstallation-verification/tasks.md | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-20-add-p0-artifact-trust-and-preinstallation-verification/VALIDATION.md | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/openspec/changes/build-first-pbo-pfo-debian-package/design.md | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/openspec/changes/build-first-pbo-pfo-debian-package/proposal.md | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/openspec/changes/publish-first-qualified-pbo-release/design.md | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/openspec/changes/publish-first-qualified-pbo-release/proposal.md | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/openspec/changes/qualify-first-pbo-composition/design.md | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/openspec/changes/qualify-first-pbo-composition/proposal.md | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/src/pixs/backend/artifact_trust_gate.py | 2 | 9.5 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/src/pixs/backend/artifact_trust_materials.py | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/src/pixs/backend/artifact_trust_proof.py | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/tests/integration/test_artifact_trust_gate_integration.py | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/tests/unit/test_artifact_trust_materials.py | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/tests/unit/test_artifact_trust_proof.py | 1 | 4.8 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| **Total** | **21** | **100 %** | **21** | **100.0 %** | **0** | **0.0 %** | **0** | **0.0 %** | **0** |

Déplacement unique du dossier N03 vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-20-add-p0-artifact-trust-and-preinstallation-verification. Les écritures avant déplacement gardent leurs chemins d’origine. VALIDATION.md est créé dans l’archive ; STATISTIQUES.md est produit après cette borne de mesure.

Les deux phrases RSMP BUILD/TECHNICAL et les six liens C17/C18/C19 sont les ajustements extérieurs au dossier N03. Aucun autre change réalisé ; édition C02 indépendante de TECHNICAL préservée. Temporaires et clés de tests nettoyés ; aucune clé privée statique ajoutée.

## 4. Commandes

| Famille | Total | Part | Succès | Taux | Refus | Taux | Erreurs | Taux | Inconnus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| /usr/bin/true | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| OpenSpec | 5 | 45.5 % | 5 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| Python venv | 5 | 45.5 % | 4 | 80.0 % | 0 | 0.0 % | 1 | 20.0 % | 0 |
| **Total** | **11** | **100 %** | **10** | **90.9 %** | **0** | **0.0 %** | **1** | **9.1 %** | **0** |

| Commande — 100 caractères maximum | Total | Part | Succès | Taux | Refus | Taux | Erreurs | Taux | Inconnus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| /home/devops/.local/npm/bin/openspec archive --help | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/.local/npm/bin/openspec archive add-p0-artifact-trust-and-preinstallation-verification… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 3 | 27.3 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import hashlib, json, pathlib, re state = json.loa… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import pathlib, py_compile, tempfile files = ['"'… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import pathlib, py_compile, tempfile with tempfile… | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| /home/devops/datas/pixs/.venv/bin/python3 -B -c 'import sys, unittest sys.path[:0] = ['"'src'"'… | 2 | 18.2 % | 1 | 50.0 % | 0 | 0.0 % | 1 | 50.0 % | 0 |
| /usr/bin/true | 1 | 9.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| **Total** | **11** | **100 %** | **10** | **90.9 %** | **0** | **0.0 %** | **1** | **9.1 %** | **0** |

Commandes explicitement refusées : aucune permission native de commande refusée observée. Les demandes annulées avant permission et erreurs de schéma n’exécutent pas leur commande. Le passage de tests exit 1 et la revalidation complète exit 0 sont conservés séparément.

## 5. Accès web

| Périmètre | Total | Part | Autorisés/réussis | Taux | Refus | Erreurs |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | 0 | 0.0 % | 0 | N/A | 0 | 0 |
| Recherches Codex documentées | 2 | 100.0 % | 2 | 100.0 % | 0 | 0 |
| **Total documenté** | **2** | **100 %** | **2** | **100 %** | **0** | **0** |

Deux recherches ont fourni les extraits primaires utiles. Aucune navigation /open vers les pages n’est prouvée ; ces références ne sont pas présentées comme des URL ouvertes par OpenCode. Références utilisées, chacune sous 100 caractères :

- https://docs.openssl.org/3.5/man1/openssl-pkeyutl/ — source repérée et consultée via extraits.
- https://www.rfc-editor.org/rfc/rfc8410.html — source repérée et consultée via extraits.

Aucune URL refusée observée. Les appels locaux CAB/OpenCode ne constituent pas du web externe. Aucun compte, message tiers, téléchargement de dépendance ou publication externe.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début — réservation du RUN technique | 2026-10-20T07:24:46.060000+00:00 |
| Fin — après archive et sonde finale | 2026-10-20T08:47:13+00:00 |
| Durée globale, pauses et attentes incluses | 01 h 22 min 26 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — avant première écriture de codage | 2026-10-20T07:25:45+00:00 | 4 % | 2026-10-27T06:33:48+00:00 |
| Après — après archive et sonde finale | 2026-10-20 08:47:13 UTC | 11 % | 2026-10-27T06:33:48+00:00 |
| Différence après − avant | — | 7 points | — |

Même compte et même fenêtre Codex 10080 minutes. Le quota est partagé : la variation peut inclure les autres travaux simultanés et n’est pas exclusivement attribuée à N03. Aucune conversion en tokens ou euros. Le relevé historique du parent reste distinct.

| Domaine observé | Total | Part | Succès | Taux | Refus | Taux | Erreurs | Taux | Inconnus |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Autres outils natifs | 170 | 83.3 % | 157 | 92.4 % | 0 | 0.0 % | 13 | 7.6 % | 0 |
| Commandes natives | 11 | 5.4 % | 10 | 90.9 % | 0 | 0.0 % | 1 | 9.1 % | 0 |
| Fichiers natifs | 21 | 10.3 % | 21 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| Web Codex documenté | 2 | 1.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % | 0 |
| **Total** | **204** | **100 %** | **190** | **93.1 %** | **0** | **0.0 %** | **14** | **6.9 %** | **0** |

Le dénominateur global contient les outils OpenCode exhaustifs et deux recherches Codex documentées. Les autres outils de l’orchestrateur ne sont pas exportés : N/A, sans reconstruction.

Preuves : 35 tests finaux OK ; archive unique ; strict postarchive 192/192 ; 78 canons inchangés ; publication CAB référence 50. Avertissement non bloquant sur titres français conservé dans VALIDATION.md. Git non inspecté, aucune opération Git mandatée. Secrets fournisseur uniquement dans le processus sécurisé, aucune valeur exposée ; clés de tests éphémères confinées et supprimées.

Le rapport précède sa propre écriture et le gate. Leur résultat final est vérifié dans le checkpoint et le registre CAB. Le cycle global demeure incomplet ; installation et qualification finales restent dans C17/C18/C19.
