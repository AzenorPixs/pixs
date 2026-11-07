# STATISTIQUES — add-initial-tanstack-shell (change archivé seul)

Périmètre : seul change archivé `add-initial-tanstack-shell`, pas RUN parent complet. Prochain cycle : SÉLECTION.
Archive réelle : `openspec/changes/archive/2026-10-01-add-initial-tanstack-shell` à `2026-10-01T10:06:35.150853+00:00` (cinq hashes identiques, actif absent, canonique inchangé).
Dataset : deux historiques complets actuels + snapshot ancien borné `2026-10-01T02:41:58.131Z`–`04:15:10Z` + preuves unitaires persistées. Aucune extrapolation `23:08–02:41`. Anciennes parts/compactions/config fine N/A.
Durée calendaire `2026-09-30T23:08:57.380Z` → `2026-10-01T10:07:48.490862Z` = `39531.110862 s` = `10 h 58 min 51.110862 s` (pauses incluses, distincte activité). Rapport exclut sa propre rédaction après cutoff `2026-10-01T10:07:48.490862+00:00`.
Coûts en unités de télémétrie (devise non exposée). Cellules inconnues `N/A`. Service inférence `N/A` (les `304.272 s` actuels sont spans assistant sans outil, pas inférence pure).
Transport CAB réussi ne prouve pas décisions manuelles : `32 APPROVED` actuels seuls, décisions legacy `N/A`. Quota 7 j avant/après/diff `N/A` (outil `get_usage_limits` absent ; avant : timestamp initial indisponible source `N/A` ; après : `2026-10-01T10:07:48.490862Z` réellement outil absent, initial préservé).

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A | opencode-go | high | 3544.0 ms | 169.6 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| N/A | N/A | N/A | HIGH demandé | N/A | N/A | N/A |

## 1. Statistiques générales et décisions

Sessions : `ses_f098bb28effes2LPJxLG6SrMr1` 98 msgs, `ses_f0931f77cffegEUAT8Y42JkUJB` 140 msgs, 4 sessions `HTTPError` sans messages exploitables. Rôles : user 95, assistant 423, total 518 (18.3 % / 81.7 %).
Outils classés exclusifs sur 367 : APPROVED_exécuté 358 (97.5 %), refusé 2 (0.5 %), technique 7 (1.9 %), ligne globale 100.0 % (arrondi 99.9 %).
Précision : deux tentatives classées refusées sur décisions natives corrélées après interruptions (une legacy minuterie `cismp-pixs-1790825144399-arm-stop-0730` + une reprise `per_0f6cac3850015TvuS6Dv3c37Cr` édit déjà interrompu) ; 4 tests/commandes Bash nonzero classés techniques, distincts des 5 statuts erreur natifs. Statuts bruts : complétés 362, erreur 5 ; legacy 179/3, actuels 183/2. CAB actuel : APPROVED 32, error 1. Legacy décisions N/A.
Tokens/coût somme snapshot+actuels sauf sondes séparées : legacy in 836226 out 48280 reasoning 25480 total 17635669 cache-read 16725683 coût 0.131826 ; actuels msgs 196 in 528598 out 76668 reasoning 27033 total 17672702 cache-read 17040403 coût 0.107681. Parties messages : texte 83, step-start 196, reasoning 242, outil 185, step-finish 195. Finitions : tool-calls 154, stop 41, absent 1.
Corrections résolues : socket court (`frontend/.cache`, préfixe `b-`, `TMPDIR` éphémère, garde octets `SingletonSocket`), masque Shift 8 cohérent avec preuves avant/après, favicon inline `data:,` ; cleanup profil/processus vérifié. Pas audit WCAG ni P0 intégrée ; protections/nettoyage et zéro effet externe conservés.


| Tokens production documentée | Nombre | Part total |
|---|---|---|
| input | 1364824 | 3.9 % |
| output | 124948 | 0.4 % |
| reasoning | 52513 | 0.1 % |
| cache-read | 33766086 | 95.6 % |
| Total | 35308371 | 100.0 % |


| Coût — unités télémétrie | Valeur | Part |
|---|---|---|
| Snapshot ancien | 0.131825966 | 55.0 % |
| Historiques actuels | 0.107680806 | 45.0 % |
| Total | 0.239506772 | 100.0 % |


| Outils — résultats exclusifs | Nombre | Part |
|---|---|---|
| Approuvés et exécutés | 358 | 97.5 % |
| Refusés | 2 | 0.5 % |
| Erreurs techniques | 7 | 1.9 % |
| Total | 367 | 100.0 % |


| Outils — statuts natifs distincts | Nombre | Part |
|---|---|---|
| Terminés | 362 | 98.6 % |
| Erreur/interruption | 5 | 1.4 % |
| Total | 367 | 100.0 % |


| Surcharge sondes | Sortie tokens | Part tokens | Coût | Part coût |
|---|---|---|---|---|
| 5 anciennes invalides | 11697 | 86.7 % | 0.007368252 | 65.7 % |
| 4 reprise valides | 1796 | 13.3 % | 0.003839800 | 34.3 % |
| Total | 13493 | 100.0 % | 0.011208052 | 100.0 % |


Sondes relevées9 :4 valides (44.4%),5 invalides (55.6%). Deux relèves +60/+90 manquées séparées; nombre prévu hors phases documentéesN/A. TTMT min2362.0ms/max5566.4ms, débit min87.7/max225.8tokens/s. Les40 et200 lignes sont deux séries distinctes, lesinvalides exclues des moyennes.

## 2. Types de messages et d’outils

| Rôle — intervalles documentés | Nombre | Part |
|---|---|---|
| user | 95 | 18.3 % |
| assistant | 423 | 81.7 % |
| Total | 518 | 100.0 % |


| Parties — deux historiques actuels seulement | Nombre | Part |
|---|---|---|
| text | 83 | 9.2 % |
| step-start | 196 | 21.8 % |
| reasoning | 242 | 26.9 % |
| tool | 185 | 20.5 % |
| step-finish | 195 | 21.6 % |
| Total | 901 | 100.0 % |


| Terminaisons assistant — deux historiques actuels seulement | Nombre | Part |
|---|---|---|
| tool-calls | 154 | 78.6 % |
| stop | 41 | 20.9 % |
| absent | 1 | 0.5 % |
| Total | 196 | 100.0 % |

Anciennes parties/terminaisons/compactions N/A; actuels0compaction.



| Outil | Nombre | Part tableau | Approuvés et exécutés (taux ligne) | Refusés (taux ligne) | Erreurs techniques (taux ligne) |
|---|---|---|---|---|---|
| cgpt-validation_broker_readiness | 53 | 14.4 % | 53 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 67 | 18.3 % | 65 (97.0 %) | 0 (0.0 %) | 2 (3.0 %) |
| bash | 39 | 10.6 % | 33 (84.6 %) | 1 (2.6 %) | 5 (12.8 %) |
| cgpt-validation_get_approval | 3 | 0.8 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 1 | 0.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 119 | 32.4 % | 119 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 10 | 2.7 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 4 | 1.1 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 23 | 6.3 % | 23 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 4 | 1.1 % | 3 (75.0 %) | 1 (25.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 34 | 9.3 % | 34 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 9 | 2.5 % | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_cancel_approval | 1 | 0.3 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 367 | 100.0 % | 358 (97.5 %) | 2 (0.5 %) | 7 (1.9 %) |


Domaines : fichiers 26/1/0, commandes 33/1/5, web natif agent 0/0/0, autres 299/0/2. Les 2 refus sont les décisions natives ci-dessus ; les 4 nonzero Bash sont techniques, distincts des 5 erreurs natives. Commandes anciennes sans libellé complet : 2 interrompues `N/A` dont 1 refus minuterie connue, non inventées.

## 3. Fichiers modifiés

Chemins avant déplacement `openspec/changes/add-initial-tanstack-shell/…`, archive réelle `openspec/changes/archive/2026-10-01-add-initial-tanstack-shell/…`. Comptage par tentatives APPROVED (lock/`.openspec.yaml` générés via commandes, non comptés édition) :


| Chemin absolu avant déplacement | Nombre | Part tableau | Approuvés et exécutés (taux ligne) | Refusés (taux ligne) | Erreurs techniques (taux ligne) |
|---|---|---|---|---|---|
| /home/devops/datas/pixs/frontend/tests/browser-check.mjs | 8 | 29.6 % | 7 (87.5 %) | 1 (12.5 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/frontend/index.html | 2 | 7.4 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/frontend/README.md | 3 | 11.1 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-tanstack-shell/design.md | 2 | 7.4 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-tanstack-shell/tasks.md | 3 | 11.1 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-tanstack-shell/proposal.md | 1 | 3.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-tanstack-shell/specs/initial-application-bootstrap/spec.md | 1 | 3.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/frontend/package.json | 1 | 3.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/frontend/src/catalogs.js | 1 | 3.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/frontend/vite.config.js | 1 | 3.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/frontend/tests/shell.test.mjs | 2 | 7.4 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/frontend/src/main.js | 1 | 3.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/frontend/src/theme.css | 1 | 3.7 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 27 | 100.0 % | 26 (96.3 %) | 1 (3.7 %) | 0 (0.0 %) |


13 sources attendues + lock généré npm + `.openspec.yaml` CLI + 5 artefacts déplacés.

## 4. Commandes

Libellés tronqués ≤100 caractères, troncation visible `…` :


| Famille | Nombre | Part tableau | Approuvés et exécutés (taux ligne) | Refusés (taux ligne) | Erreurs techniques (taux ligne) |
|---|---|---|---|---|---|
| CAB test true | 11 | 28.2 % | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Start Vite | 3 | 7.7 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec validation | 5 | 12.8 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Pilotage et nettoyage processus | 4 | 10.3 % | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Chromium test | 4 | 10.3 % | 1 (25.0 %) | 0 (0.0 %) | 3 (75.0 %) |
| Node syntax | 2 | 5.1 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| frontend build | 2 | 5.1 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 | 2.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec création | 1 | 2.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Other command | 1 | 2.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| npm installation | 2 | 5.1 % | 1 (50.0 %) | 0 (0.0 %) | 1 (50.0 %) |
| frontend tests Node | 1 | 2.6 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Anciennes commandes sans résultat exploitable | 2 | 5.1 % | 0 (0.0 %) | 1 (50.0 %) | 1 (50.0 %) |
| Total | 39 | 100.0 % | 33 (84.6 %) | 1 (2.6 %) | 5 (12.8 %) |


Preuves anciennes (exit) : new change 0, strict prep 0, 4× true 0, minuterie checkpoint 0, install config 0, test 0, build 0, start/stop Vite 0, strict checkpoint 0, install shell 1. Deux anciennes interrompues sans libellé exact `N/A` (dont minuterie refusée), non reconstituées.


| Commandes refusées regroupées (libellé ≤100 caractères) | Nombre | Part des refus | Résultat |
|---|---|---|---|
| N/A — minuterie ancienne, libellé exact indisponible dans historique HTTP404 | 1 | 100.0 % | Non exécutée |
| Total | 1 | 100.0 % | — |

## 5. Accès web

Web natif agent : 0 appel. Orchestrateur reprise seule doc CDP : 3 outils / 4 opérations, autres phases `N/A`. URLs ≤100 (tronquées si besoin) :

| URL réellement consultée | Statut et usage |
|---|---|
| https://chromedevtools.github.io/devtools-protocol/tot/Input/ | Consultée avec succès — masque Shift |
| https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol/master/json/browser… | Consultée avec succès — protocole |

Sondes reprise valides 40 lignes (4) : `08:03:23` TTMT 2875 ms 189.5 t/s, `08:34:14` 5566 ms 175.1 t/s, `09:36:33` 3373 ms 87.7 t/s, `10:06:35` 2362 ms 225.8 t/s ; coûts 0.000969/0.0009682/0.000952/0.0009506. Cinq anciennes 200→193 lignes invalides exclues (surcoût 11697 tokens, 0.007368252). Missed +60/+90 signalées sans reconstitution ; finale `10:06:35Z` couvre due `10:06:33Z`.


| Accès orchestrateur — reprise documentée seulement | Appels outils | Part | Succès | Refus | Erreur |
|---|---|---|---|---|---|
| Documentation CDP (4 opérations open/find) | 3 | 100.0 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 3 | 100.0 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Agent de codage :0 outil web; taux N/A, dénominateur0. Aucune URL refusée observée pendant cette reprise. Autres phases orchestrateur N/A. Les requêtes du pilote sont des tests locaux; final52 Fetch autorisées,0 externe bloquée,0 HTTP en erreur.

## 6. Synthèse globale

Change seul archivé avec 5 artefacts, strict final valide, Node 3/3, syntaxes/build 104 modules, navigateur `ok=true` puis cleanup/arrêt Vite et design/README/tasks documentés. Totaux croisés 358/2/7 sur 367 (100.0 % avec arrondi). Limites : pas calendaire complet, compteurs `N/A` non extrapolés, service/orchestration `N/A`, quota `N/A`, web hors reprise `N/A`. Prochain cycle SÉLECTION, sans prétendre RUN parent complet.

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-09-30T23:08:57.380Z (UTC) |
| Fin — après archivage | 2026-10-01T10:07:48.490862Z (UTC) |
| Durée globale (pauses et attentes incluses) | 10 h 58 min 51 s (exact :39531.110862 s) |


| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | N/A — outil absent, initial préservé | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-01T10:07:48.490862Z (UTC) | N/A — outil absent | N/A |
| Différence après − avant | — | N/A — comparaison impossible | — |

Quota codex10080minutes indisponible; compte/fenêtre/reset non vérifiables. Les quotas sont partagés par le compte et peuvent inclure d’autres tâches simultanées; aucune valeur manquante n’est remplacée par zéro.


| Domaine — agent documenté | Nombre | Part tableau | Approuvés et exécutés (taux ligne) | Refusés (taux ligne) | Erreurs techniques (taux ligne) |
|---|---|---|---|---|---|
| files | 27 | 7.4 % | 26 (96.3 %) | 1 (3.7 %) | 0 (0.0 %) |
| commands | 39 | 10.6 % | 33 (84.6 %) | 1 (2.6 %) | 5 (12.8 %) |
| web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| other | 301 | 82.0 % | 299 (99.3 %) | 0 (0.0 %) | 2 (0.7 %) |
| Total | 367 | 100.0 % | 358 (97.5 %) | 2 (0.5 %) | 7 (1.9 %) |

Le total367 exclut la rédaction du rapport, les sondes et les outils de l’orchestrateur non mesurables globalement. Les taux peuvent sommer99.9% ou100.1% après arrondi; total100%. Git non inspecté ni modifié par cette reprise; aucun commit/push observé. Aucun secret lu ou transmis dans le périmètre observé. Service inférence des deux catégoriesN/A : ni dénominateur fiable ni chevauchement mesurable; la durée calendaire inclut pauses/outils/permissions. La maintenance du projet template est séparée. Le RUN parent resteSÉLECTION.
