# Statistiques — add-p0-group-membership

Session OpenCode `ses_f130e4e87ffeaY8YzgPakaCCOl`, Pixs `/home/devops/datas/pixs`, RUN `cismp-pixs-20260929-1134`.
Intervalle : 2026-09-29 19:22:20.774089 UTC à 2026-09-29 19:53:21.473933 UTC. Archive réelle : `openspec/changes/archive/2026-09-29-add-p0-group-membership`.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor | N/A — version exacte non exposée | opencode-go | low | 3,417 s | 334,952 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex | N/A — version exacte absente de la télémétrie collectée | OpenAI | N/A | N/A — non sondé | N/A — non sondé | N/A |

Les 55 messages assistant de production (100 %) utilisent le modèle, fournisseur et variant ci-dessus. Le temps de génération isolé et le temps de service cumulé des agents sont N/A. Les attentes CAB et la durée calendaire ne sont pas du temps de génération. La sonde périodique chevauche l'archivage ; les sondes sont exclues des totaux de production.

## 1. Statistiques générales et décisions

Intervalle de ce seul change, avant première écriture et après archivage/sonde finale. Sélection préalable, changes précédents et rédaction du rapport exclus. Les compteurs d'outils concernent OpenCode ; ceux de l'orchestrateur sont N/A faute d'un relevé exhaustif.

| Mesure | Valeur |
| --- | --- |
| Durée calendaire, attentes incluses | 00 h 31 min 00 s (1860,700 s) |
| Messages | 72 (100,0 %) |
| Appels d'outils | 38 (100,0 %) |
| Réussites techniques | 37 (97,4 %) |
| Erreurs techniques | 1 (2,6 %) |
| Refus natifs | 0 (0,0 %) |
| Mandats CAB distincts | 17 (100,0 %) |
| APPROVED | 17 (100,0 %) |
| REJECTED | 0 (0,0 %) |
| Tâches OpenSpec prouvées | 6 (100,0 %) |
| Tests finaux réussis | 419 (100,0 %) |
| Nouveaux tests | 15 (3,6 %) |
| Coût natif API | 0.122279882 USD |
| Compactions observées | 0 (0,0 %) |

Un appel terminé avec succès est compté « approuvé et exécuté », sans présumer une approbation manuelle pour une lecture ou un appel MCP. Les décisions CAB sont distinctes des résultats techniques : 17 mandats approuvés couvrent 11 écritures et 6 commandes. Le timeout MCP reste une erreur technique malgré l'approbation corrélée obtenue ensuite ; aucun refus n'en est déduit.

| Compteurs natifs de tokens, sans contenu | Nombre et part |
| --- | --- |
| input | 821262 (4,3 %) |
| cache_read | 18160741 (95,6 %) |
| cache_write | 0 (0,0 %) |
| output | 17984 (0,1 %) |
| reasoning | 1177 (0,0 %) |
| Total natif | 19001164 (100,0 %) |

Somme des cinq compteurs égale au total natif. Le contenu du raisonnement n'est pas reproduit. Coût API observé, sans estimation tarifaire ni conversion en quota Codex.

Prompt déterministe constant des sondes :
`Sans outil, fichier ni réseau. Réponds uniquement avec exactement 64 lignes identiques, chacune contenant : alpha beta gamma delta epsilon zeta eta theta. Aucun commentaire, aucune numérotation.`

| Position | Envoi UTC | Message preuve | Tokens sortie | TTMT s | Débit tokens/s | Résultat |
| --- | --- | --- | --- | --- | --- | --- |
| début | 2026-09-29 19:22:20.797367 UTC | msg_0ee9e352d001CpzIPPqIliFSV1 | 586 | 1,406 | 358,395 | Réussie |
| +30 min (retard de quelques secondes horodaté) | 2026-09-29 19:52:40.994986 UTC | msg_0eeb9fb66001anpK0f5SWc3Pq4 | 586 | 1,561 | 320,352 | Réussie |
| fin | 2026-09-29 19:53:03.042861 UTC | msg_0eeba5181001voaZ9BrbcUWLeE | 585 | 7,284 | 326,109 | Réussie |

| Prévues | Réussies | Échouées | Manquées |
| --- | --- | --- | --- |
| 3 (100,0 %) | 3 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

Moyennes arithmétiques sur trois sondes valides. TTMT min–max : 1,406–7,284 s ; débit min–max : 320,352–358,395 tokens/s. La sonde périodique est envoyée 20,198 s après +30 min depuis l'envoi initial (17,081 s après l'échéance calculée depuis sa fin) ; aucune mesure rétroactive.

Surcharge distincte : 1757 tokens de sortie (100 % des sorties des sondes), 15,738 s entre envoi et fin native cumulées. Entrée et coût des sondes N/A, non conservés par le collecteur. Trois sessions jetables supprimées ; zéro outil exécuté (0 %, dénominateur des résultats outil N/A).

Incident observé : `groups-integrationfile01`, message `msg_0eead9d43001yVrhjDpoI6Flb2`, timeout MCP -32001. Puis get_approval PENDING et poll_approval APPROVED corrélé à 19:40:32Z, avant l'unique écriture. Aucun nouveau test CAB de reprise observé entre le timeout et cette écriture : écart au protocole de récupération conservé explicitement. Correction de tests avant exécution : tuple vide remplacé par véritable sous-classe de tuple, contrôles de contexte incomplet/altéré ajoutés. Aucun test exécuté en échec dans cet intervalle. Une lecture prématurée de design.md par l'orchestrateur a rencontré FileNotFoundError puis a été relancée après écriture ; hors compteur OpenCode, sans effet sur les fichiers.

## 2. Types de messages et d'outils

| Rôle | Nombre et part |
| --- | --- |
| user | 17 (23,6 %) |
| assistant | 55 (76,4 %) |
| Total | 72 (100,0 %) |

| Type de partie (métadonnées) | Nombre et part |
| --- | --- |
| text | 34 (13,7 %) |
| step-start | 55 (22,2 %) |
| reasoning | 66 (26,6 %) |
| tool | 38 (15,3 %) |
| step-finish | 55 (22,2 %) |
| Total | 248 (100,0 %) |

| Terminaison assistant | Nombre et part |
| --- | --- |
| tool-calls | 38 (69,1 %) |
| stop | 17 (30,9 %) |
| Total | 55 (100,0 %) |

| Outil | Total et part | Approuvés/exécutés | Refus natifs | Erreurs |
| --- | --- | --- | --- | --- |
| cgpt-validation_request_validation | 17 (44,7 %) | 16 (94,1 %) | 0 (0,0 %) | 1 (5,9 %) |
| write | 11 (28,9 %) | 11 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| bash | 6 (15,8 %) | 6 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| read | 2 (5,3 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_get_approval | 1 (2,6 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| cgpt-validation_poll_approval | 1 (2,6 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 38 (100,0 %) | 37 (97,4 %) | 0 (0,0 %) | 1 (2,6 %) |

Aucune erreur de message ni compaction observée. L'unique erreur technique est le timeout MCP précisé ci-dessus.

## 3. Fichiers modifiés

Tentatives d'édition, pas nombre de lignes. Les artefacts sont présentés à leur chemin final ; leurs écritures ont eu lieu dans le change actif.

| Chemin absolu complet | Total et part | Approuvés/exécutés | Refus natifs | Erreurs |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-29-add-p0-group-membership/proposal.md | 1 (9,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-29-add-p0-group-membership/design.md | 1 (9,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-29-add-p0-group-membership/tasks.md | 2 (18,2 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-29-add-p0-group-membership/.openspec.yaml | 1 (9,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/core/identity/groups.py | 1 (9,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/core/identity/__init__.py | 1 (9,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_identity_facade.py | 1 (9,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_group_membership.py | 2 (18,2 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_group_facade.py | 1 (9,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 11 (100,0 %) | 11 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

Neuf fichiers distincts ; onze écritures approuvées. Le déplacement de quatre artefacts est compté comme une commande d'archivage. Le rapport STATISTIQUES.md est une écriture autorisée distincte après l'intervalle, exclue de son propre décompte. Réconciliation des contenus avec les dernières écritures autorisées, sans Git. Identity models.py inchangé : SHA-256 `253bac3be28375e78f8ca406a790e7e504a0b53d480785e5cb319baef2fe1a57`.

## 4. Commandes

Libellés inférieurs à 100 caractères ; commandes complètes dans les mandats et la session.

| Famille / libellé | Total et part | Approuvés/exécutés | Refus natifs | Erreurs |
| --- | --- | --- | --- | --- |
| OpenSpec validate --all --strict | 2 (33,3 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Python -B unittest discover -s tests/unit -v | 1 (16,7 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Python -B unittest discover -s tests/integration -v | 1 (16,7 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Python -B : AST 5 fichiers, UTF-8/LF 9 fichiers | 1 (16,7 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| OpenSpec archive add-p0-group-membership --yes --skip-specs --json | 1 (16,7 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 6 (100,0 %) | 6 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

Commandes refusées CAB : 0 (0 % des 17 mandats ; part interne des refus N/A). Les six Bash ont réussi. Validation OpenSpec initiale et finale : 77 éléments ; tests finaux : 316 unités + 103 intégrations = 419, dont 15 nouveaux.

## 5. Accès web

| Domaine | Appels (% outils) | Approuvés | Refusés | Erreurs |
| --- | --- | --- | --- | --- |
| Web | 0 (0,0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |

Aucun outil web ni URL approuvée/refusée observée. HTTP/SSE local d'OpenCode et CAB est un transport de pilotage, sans consultation web externe.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-09-29 19:22:20.774089 UTC |
| Fin — après archivage et sonde finale | 2026-09-29 19:53:21.473933 UTC |
| Durée globale, attentes incluses | 00 h 31 min 00 s (1860,700 s) |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | 2026-09-29 19:22:20.774089 UTC | N/A | N/A |
| Après — après archivage de la spécification | 2026-09-29 19:53:21.473933 UTC | N/A | N/A |
| Différence après − avant | — | N/A | — |

Outil natif get_usage_limits non exposé aux deux bornes : aucune mesure du quota codex fenêtre 10080 minutes. Horodatages de constat d'indisponibilité, pas de mesure réussie. Réinitialisation et différence N/A. Le quota est partagé par le compte et peut inclure d'autres tâches ; aucune conversion en tokens ou euros.

| Domaine | Total et part | Approuvés/exécutés | Refus natifs | Erreurs |
| --- | --- | --- | --- | --- |
| autres | 21 (55,3 %) | 20 (95,2 %) | 0 (0,0 %) | 1 (4,8 %) |
| fichiers | 11 (28,9 %) | 11 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| commandes | 6 (15,8 %) | 6 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| web | 0 (0,0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Total | 38 (100,0 %) | 37 (97,4 %) | 0 (0,0 %) | 1 (2,6 %) |

Totaux croisés : 11 éditions + 6 commandes + 21 autres = 38 appels ; 37 réussites et 1 erreur. Autres : 2 lectures + 19 appels MCP. Décisions CAB : 17 APPROVED, 0 REJECTED, 0 non résolu.

Preuves finales : unités `msg_0eeb054ce001ido650hzodg3Wv` (316/316), intégrations `msg_0eeb1d205001C1KoqA05AtP7mp` (103/103), AST/UTF-8/LF `msg_0eeb34555001SScPRfZpw7SuvD` (5 AST et 9 fichiers), OpenSpec `msg_0eeb49602001y74Wbnm1qd0W5j` (77/77), tâches `msg_0eeb683eb001Sm13OjrrE0jGLf` (6 cochées), archive `msg_0eeba164e001JyIygoLuCJqEBu` exit 0, specsUpdated=false, rapport `msg_0eeba2289001mV1uNdPaLwrINJ`. Archive réelle et absence du répertoire actif vérifiées.

Le change fournit Group, Membership et leurs validations structurelles n:m, sans authentification, autorisation, persistance ni état applicatif. Aucune dépendance nouvelle, opération Git, accès web externe ou consultation de secret observée dans les outils audités. À la demande explicite du développeur, arrêt du RUN après vérification de ce rapport et clôture CAB ; aucun nouveau change ne doit être lancé. Le projet global n'est pas déclaré terminé.
