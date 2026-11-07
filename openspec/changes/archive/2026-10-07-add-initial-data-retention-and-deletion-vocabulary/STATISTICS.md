# Statistiques de session — add-initial-data-retention-and-deletion-vocabulary

RUN `cismp-pixs-20261007-061019` ; session `ses_eea8a1e72ffeOAiwkcLCyeMI1e` ; archive `openspec/changes/archive/2026-10-07-add-initial-data-retention-and-deletion-vocabulary`. Borne initiale native `msg_115d0d80a001V1nghA09DYRmyy` ; dernier rapport `msg_115eac4bc001cSK22owpHqiwtc`. Seuls les travaux de ce change, sa correction de format après archive et les bornes closes ci-dessous sont comptés. JOB1 commun antérieur, archives précédentes, rédaction/écriture du présent rapport exclus.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Qwen3.8 Flash / qwen3.8-flash | N/A — version exacte non publiée | opencode-go | xhigh | 1,7625 s | 73,41 | N/A — durées natives mêlent génération, outils et attentes ; OpenCode 1.18.34 est la version du logiciel |


### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex /root (famille GPT-6 déclarée par plateforme) | N/A | OpenAI | N/A | N/A | N/A | N/A — télémétrie de génération du thread absente |


Dénominateur du temps de service cumulé : N/A ; aucune durée calendaire convertie en génération. Codage, pilotage et sondes peuvent chevaucher leurs activités.

## 1. Statistiques générales et décisions

Durée calendaire 0 h 31 min 2,639 s : 2026-10-07T10:02:50.762Z à 2026-10-07T10:33:53.401Z (UTC), pauses/attentes/tests/archive/correction inclus.

| Mesure | Effectif | Part |
|---|---|---|
| Messages | 110 | 100 % |
| user | 25 | 22,7 % |
| assistant | 85 | 77,3 % |
| Décisions CAB uniques | 23 | 100 % |
| APPROVED | 23 | 100 % |
| REJECTED | 0 | 0,0 % |
| Clarification | 0 | 0,0 % |
| Outils natifs | 63 | 100 % |
| completed | 62 | 98,4 % |
| error | 1 | 1,6 % |


Tokens de production : input 510, output 24968, reasoning 0, cache_read 11865139, cache_write 62732 ; coût 0,214200084 (devise N/A, non publiée). Compactions dans cet intervalle : 0 ; compaction antérieure non réattribuée. Compaction native orchestrateur : API non exposée.

Développement : 21 exécutions de tests, toutes réussies (100 %) : 3 unitaires (14,3 %), 1 intégration (4,8 %), 17 régressions (81,0 %). Trois compilations exit 0 (100 %) ; quatre stricts pré/post exit 0 (100 %). Deux globaux exit 1 natifs qualifiés : identité des findings 19 WARNING/0 ERROR, 76 specs/77 items, aucune norme changée. Cinq tâches cochées après preuves ; UTF-8/LF exact ; 154 références sans dérive ; delta canonique identique.

Archive native exit 0, avec avertissement de format non bloquant de proposal.md (titres français au lieu des deux titres requis). Correction 101 : seulement ## Pourquoi → ## Why et ## Modification → ## What Changes dans la proposition archivée, contenu inchangé. Présence des titres exigés vérifiée localement ; aucune nouvelle validation CLI post-correction ni réarchive prétendue.

### Sondes de performance

| Position / essai | Valide | Tokens | TTMT (s) | Tokens/s | Coût |
|---|---|---|---|---|---|
| début #1 | oui | 535 | 2,1963 | 76,71 | 0,003018150 |
| intermédiaire après archive, avant correction de format #1 | oui | 539 | 1,9066 | 45,57 | 0,003020030 |
| +30 min #1 | oui | 524 | 1,3769 | 75,69 | 0,000468444 |
| fin #1 | oui | 548 | 1,7143 | 67,82 | 0,000479724 |


| Position | Envoi UTC | Premier / dernier SSE texte UTC | Session / message |
|---|---|---|---|
| début | 2026-10-07T10:00:40.114200+00:00 | 2026-10-07T10:00:42.310449+00:00 / 2026-10-07T10:00:49.285062+00:00 | ses_eea312664ffe24EJ0tXqW2zgx2 / msg_115ceda24001bicN78RHOGoLPn |
| intermédiaire après archive, avant correction de format | 2026-10-07T10:28:38.000657+00:00 | 2026-10-07T10:28:39.907251+00:00 / 2026-10-07T10:28:51.735813+00:00 | ses_eea178c2affe8dTmmAfcMQBQM0 / msg_115e87456001U629EpYZycqOeo |
| +30 min | 2026-10-07T10:30:46.300597+00:00 | 2026-10-07T10:30:47.677542+00:00 / 2026-10-07T10:30:54.600205+00:00 | ses_eea1596f0ffe6SE26F82gbkvcn / msg_115ea69af001QovlpP1UgrPcMs |
| fin | 2026-10-07T10:32:25.029450+00:00 | 2026-10-07T10:32:26.743736+00:00 / 2026-10-07T10:32:34.824209+00:00 | ses_eea141541ffeFluTqhHhCH0q3Y / msg_115ebeaf5001Lycu7lBYrkgQ4n |


Trois positions prévues : début, +30 min, fin ; trois réussies (100 %), zéro échouée/manquée (0 %). Quatre tentatives valides (100 %), dont une mesure intermédiaire supplémentaire après archive, avant correction de format : elle reste visible et hors des moyennes périodiques. Première sonde avant le travail ; dernière après correction. Collecteur repris sans nouvelle sonde début, cadence originale 10:00:40.076547Z conservée ; relève +30 envoyée avec 6,224050 s de retard mesuré, sans reconstitution SSE ni attente du créneau pour travailler. Même prompt textuel fixe de 40 lignes, même Qwen/opencode-go/xhigh, aucun outil/fichier/réseau généré par les sondes.

Moyennes sur trois sondes périodiques valides : TTMT 1,7625 s, min/max 1,3769/2,1963 ; débit 73,41 tokens/s, min/max 67,82/76,71. Surcharge hors production, quatre sondes : 2146 tokens, coût 0,006986348, durées cumulées 41,063 s ; invalides 0 token/0 coût (0 %).

## 2. Types de messages et d'outils

| Type de partie | Nombre | Part |
|---|---|---|
| text | 51 | 13,8 % |
| step-start | 85 | 23,0 % |
| reasoning | 85 | 23,0 % |
| tool | 63 | 17,1 % |
| step-finish | 85 | 23,0 % |
| Total | 369 | 100 % |


| Fin assistant | Nombre | Part |
|---|---|---|
| tool-calls | 61 | 71,8 % |
| stop | 24 | 28,2 % |
| Total | 85 | 100 % |


| Outil | Total (part des 63) | Completed (taux ligne) | Erreur (taux ligne) |
|---|---|---|---|
| cgpt-validation_request_validation | 23 (36,5 %) | 22 (95,7 %) | 1 (4,3 %) |
| bash | 14 (22,2 %) | 14 (100,0 %) | 0 (0,0 %) |
| glob | 3 (4,8 %) | 3 (100,0 %) | 0 (0,0 %) |
| write | 7 (11,1 %) | 7 (100,0 %) | 0 (0,0 %) |
| read | 9 (14,3 %) | 9 (100,0 %) | 0 (0,0 %) |
| cgpt-validation_get_approval | 1 (1,6 %) | 1 (100,0 %) | 0 (0,0 %) |
| cgpt-validation_poll_approval | 1 (1,6 %) | 1 (100,0 %) | 0 (0,0 %) |
| grep | 1 (1,6 %) | 1 (100,0 %) | 0 (0,0 %) |
| edit | 2 (3,2 %) | 2 (100,0 %) | 0 (0,0 %) |
| cgpt-validation_broker_readiness | 1 (1,6 %) | 1 (100,0 %) | 0 (0,0 %) |
| cgpt-validation_list_pending | 1 (1,6 %) | 1 (100,0 %) | 0 (0,0 %) |
| Total | 63 (100 %) | 62 (98,4 %) | 1 (1,6 %) |


Convention : completed ne prouve ni une approbation manuelle ni une réussite fonctionnelle. Chacun des 23 effets (9 éditions, 14 Bash) a son APPROVED unique. Le timeout MCP 84 est une erreur technique récupérée par décision et polling corrélés, sans resoumission de requestId ni double exécution. Les deux globaux completed ont un exit 1 natif, qualifié séparément.

## 3. Fichiers modifiés

Neuf tentatives natives (7 write + 2 edit), toutes approuvées et exécutées conformes : 9 (100 %) ; refus 0 (0 %) ; erreur 0 (0 %). Chemins OpenSpec donnés après leur déplacement vers l'archive.

| Chemin absolu | Tentatives (part des 9) | Approuvées exécutées | Refusées | Erreur |
|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-retention-and-deletion-vocabulary/proposal.md | 2 (22,2 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-retention-and-deletion-vocabulary/design.md | 1 (11,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-retention-and-deletion-vocabulary/tasks.md | 2 (22,2 %) | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-07-add-initial-data-retention-and-deletion-vocabulary/specs/data-lifecycle/spec.md | 1 (11,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/src/pixs/kernel/data_lifecycle_policy_vocabulary.py | 1 (11,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/unit/test_data_retention_and_deletion_vocabulary.py | 1 (11,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| /home/devops/datas/pixs/tests/integration/test_data_retention_and_deletion_vocabulary_integration.py | 1 (11,1 %) | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total | 9 (100 %) | 9 (100 %) | 0 (0 %) | 0 (0 %) |


Hors éditions : création de .openspec.yaml par new change et déplacement des cinq artefacts par archive. Empreintes identiques au déplacement ; seule proposition ensuite corrigée sous 101, deux titres, hash final ffdcd5498897aa18a0031cf58e60d75281461f756a0e3ac842019bea291a642f. État orchestrateur /home/devops/datas/pixs/output/cismp-state.json mis à jour hors de ces outils OpenCode ; compteurs orchestrateur N/A. Sources antérieures, canon et façades inchangés.

## 4. Commandes

Quatorze commandes sous APPROVED distinct : douze exit 0 (85,7 %), deux exit 1 qualifiés (14,3 %), aucun refus/échec d'exécution (0 %).

| Famille | Effectif | Part des 14 | exit 0 | exit 1 qualifié |
|---|---|---|---|---|
| openspec new change | 1 | 7,1 % | 1 (100,0 %) | 0 (0,0 %) |
| stricts ciblés pré/post | 4 | 28,6 % | 4 (100,0 %) | 0 (0,0 %) |
| py_compile | 3 | 21,4 % | 3 (100,0 %) | 0 (0,0 %) |
| tests unitaire/intégration/régression | 3 | 21,4 % | 3 (100,0 %) | 0 (0,0 %) |
| globaux OpenSpec | 2 | 14,3 % | 0 (0,0 %) | 2 (100,0 %) |
| archive unique | 1 | 7,1 % | 1 (100,0 %) | 0 (0,0 %) |
| Total | 14 | 100 % | 12 (85,7 %) | 2 (14,3 %) |


| Commande (libellé ≤100 caractères) | Occurrences (part des 14) | Codes natifs |
|---|---|---|
| /home/devops/.local/npm/bin/openspec new change add-initial-data-retention-and-deletion-vocabulary | 1 (7,1 %) | 0 |
| /home/devops/.local/npm/bin/openspec validate add-initial-data-retention-and-deletion-vocabulary --… | 2 (14,3 %) | 0, 0 |
| /home/devops/.local/npm/bin/openspec validate data-lifecycle --type spec --strict | 2 (14,3 %) | 0, 0 |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/data_lifecycle_policy_vocabul… | 1 (7,1 %) | 0 |
| /home/devops/python/current/bin/python3 -m py_compile tests/unit/test_data_retention_and_deletion_v… | 1 (7,1 %) | 0 |
| PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/unit -p tes… | 1 (7,1 %) | 0 |
| /home/devops/python/current/bin/python3 -m py_compile tests/integration/test_data_retention_and_del… | 1 (7,1 %) | 0 |
| PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/integration… | 1 (7,1 %) | 0 |
| PYTHONPATH=src:tests/unit:tests/integration /home/devops/python/current/bin/python3 -B -m unittest … | 1 (7,1 %) | 0 |
| /home/devops/.local/npm/bin/openspec validate --specs --strict --json --report findings | 1 (7,1 %) | 1 |
| /home/devops/.local/npm/bin/openspec validate --all --strict --json --report findings | 1 (7,1 %) | 1 |
| /home/devops/.local/npm/bin/openspec archive add-initial-data-retention-and-deletion-vocabulary --y… | 1 (7,1 %) | 0 |


Commandes refusées : aucune, 0 (0 %). La correction 101 est une édition, aucune commande d'archivage rejouée.

## 5. Accès web

Agent de codage : zéro outil web/URL visitée, 0 sur 63 (0,0 %) ; zéro approbation, refus, erreur, taux internes N/A (dénominateur nul). Orchestrateur : aucun outil web pendant ces bornes. HTTP locaux OpenCode/CAB/SSE et transport modèle distingués des visites web ; réseau interne du modèle non mesuré comme outil web. Aucune requête sans URL visitée ni URL refusée.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-07T10:02:50.762Z (UTC) |
| Fin — après archive, correction et sonde finale | 2026-10-07T10:33:53.401Z (UTC) |
| Durée globale (pauses et attentes incluses) | 0 h 31 min 2,639 s |


| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-10-07T10:00:39.587Z (tentative, UTC) | N/A — outil absent | N/A |
| Après — après archivage de la spécification | 2026-10-07T10:33:53.401Z (tentative, UTC) | N/A — outil absent | N/A |
| Différence après − avant | — | N/A | — |


Outil natif mcp__codex_app__get_usage_limits absent avant et à la vérification après archive/correction/sonde finale ; compte et fenêtre de 10 080 minutes invérifiables, aucune donnée reconstruite. Quotas partagés par le compte ; attribution exclusive non vérifiable.

| Domaine | Appels (part globale) | Succès conformes | Refusés | Erreurs | Qualifiés |
|---|---|---|---|---|---|
| Éditions natives | 9 (14,3 %) | 9 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Commandes natives | 14 (22,2 %) | 12 (85,7 %) | 0 (0,0 %) | 0 (0,0 %) | 2 (14,3 %) |
| Web | 0 (0,0 %) | N/A | N/A | N/A | N/A |
| Autres outils lecture/CAB | 40 (63,5 %) | 39 (97,5 %) | 0 (0,0 %) | 1 (2,5 %) | 0 (0,0 %) |
| Total | 63 (100 %) | 60 (95,2 %) | 0 (0,0 %) | 1 (1,6 %) | 2 (3,2 %) |


Totaux croisés : 9 + 14 + 40 = 63 ; 60 + 0 + 1 + 2 = 63 ; 23 décisions APPROVED couvrent 23 effets ; 25 user + 85 assistant = 110 messages. Sondes, corpus commun précédent et écriture future du rapport hors production ; aucun coût commun inventé ou réparti.

Résultat vérifiable : 21 tests OK, compilations/stricts exit 0, globaux exit 1 qualifiés exacts, 154 références intactes, delta canonique identique, archive unique exit 0 avec --skip-specs et validation conservée, avertissement de titres corrigé sous mandat 101. Git non inspecté ; aucun commit/push/branche. PostgreSQL/navigateur non nécessaires, non exécutés ; aucun accès secret pendant cet intervalle observé. Livraison déclarative partielle, sans rétention effective, suppression, purge, tombstone ou publication des profils. Rapport vérifié requis avant retour parent SÉLECTION ; aucune déclaration globale TERMINÉ.
