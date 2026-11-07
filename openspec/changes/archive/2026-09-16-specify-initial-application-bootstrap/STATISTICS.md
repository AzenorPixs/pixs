# STATISTIQUES.md — `2026-09-16-specify-initial-application-bootstrap` — Revalidation RCAMP2

> **Validation globale stricte du 26 octobre 2026 : 186/186 valides, 0 erreur, 0 avertissement, 88 INFO.** Ce relevé commun est ajouté aux historiques sans modification du canon.

> **Découpage du 26 octobre 2026 validé :** proposition et deltas stricts conformes pour chacun des deux lots (4 et 9 exigences). Les compléments de cette phase remplacent les anciennes conclusions « 13 deltas > 10 » pour l’état courant ; toutes les mesures historiques restent conservées.

> **Actualisation du 26 octobre 2026 :** les compléments datés de chaque section décrivent la correction et le réarchivage autorisés. Les anciennes mesures RCAMP2 sont conservées comme historique ; leur périmètre sans correction ne décrit pas cette nouvelle intervention.

- RUN : `rcamp2-pixs-d2dfdf5ddd024b9b` — reservation 1322 — phase REPORT — contextId 1317
- Change : `specify-initial-application-bootstrap` — session `ses_e86b0336dffe6bnYfvR5k7iiGf`
- Coupure : avant génération statistiques — `started_at 2026-10-26T17:43:55.282000+00:00` → `ended_at 2026-10-26T18:08:44.982832+00:00`
- Publication du bilan prouvée, aucune nouvelle archive : `REVALIDATION.md` créé sous mandat distinct ; archivage « sans objet — change déjà archivé ».
- Bilan : [REVALIDATION.md](../../../../output/rcamp/rcamp2-pixs-d2dfdf5ddd024b9b/REVALIDATION.md) — preuves 8 commandes intégrales : [preuves-tests.json](../../../../output/rcamp/rcamp2-pixs-d2dfdf5ddd024b9b/preuves-tests.json)
- Historique : N/A — aucune télémétrie historique d'implémentation disponible ; ne pas la reconstituer.
- Références complètes : `/home/devops/datas/pixs/openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/` (9 fichiers), `/home/devops/datas/pixs/openspec/specs/initial-application-bootstrap/spec.md`, `/home/devops/datas/pixs/openspec/specs/initial-administration/spec.md`, `/home/devops/datas/pixs/openspec/specs/operations/spec.md`, `/home/devops/datas/pixs/openspec/specs/audit/spec.md`, `/home/devops/datas/pixs/openspec/specs/authorization/spec.md`, `/home/devops/datas/pixs/openspec/specs/api/spec.md`, `/home/devops/datas/pixs/openspec/specs/frontend/spec.md`, `/home/devops/datas/pixs/openspec/specs/secrets-providers/spec.md`, `/home/devops/datas/pixs/openspec/specs/contracts/spec.md`, `/home/devops/datas/pixs/openspec/specs/reference-composition/spec.md`.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| muse-spark-1.3-contributor | N/A — version exacte absente de la télémétrie | OpenCodeGo | high | 2.589932 s | 223.429209 t/s | N/A — busy inclut outils/attentes, aucune assimilation à la génération |
| Codex — famille GPT-6 déclarée, actualisation du 26 octobre 2026 | N/A — version exacte non télémétrée | OpenAI | N/A — effort non télémétré | N/A — sondes non activées | N/A — sondes non activées | N/A — temps de service non instrumenté |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| GPT-6 famille déclarée | N/A — version exacte absente | OpenAI | N/A — effort non télémétré | N/A | N/A — performance non télémétrée | N/A — service non instrumenté |

## 1. Statistiques générales et décisions

### Validation globale stricte du 26 octobre 2026

Relevé commun aux deux archives : une seule exécution globale, sans nouveau
réarchivage ni correction du canon. **186 éléments examinés, 186 valides
(100 %), 0 échec (0 %)** : 108 changes actifs (58,1 %) et 78 spécifications
canoniques (41,9 %). Retour de commande 0 ; **0 erreur, 0 avertissement,
88 informations**. Les 78 empreintes canoniques sont identiques avant/après.
Ces résultats sont ajoutés aux historiques sans addition des anciens relevés.
Le bilan documentaire des douze tâches historiques reste 10/0/1/1.
[Rapport JSON complet](../../../../output/openspec-global-strict/20261026T194321Z/validation.json) ; [journal et empreintes](../../../../output/openspec-global-strict/20261026T194321Z/state.json).


### Découpage validé — 26 octobre 2026

Lot propre : **4 exigences / 13** (30.8 %) et
**6 scénarios / 21** (28.6 %) ; le complément se trouve
dans l'autre archive. L'union contient 13 exigences et 21 scénarios une seule fois.
La proposition complète et les deltas passent le strict avant et après archivage :
0 erreur, 0 avertissement. Le défaut initial des 13 deltas > 10 est résolu par
une séparation en lots de 4 et 9 exigences. Les informations CLI « already exists »
(1 pour le bootstrap, 3 pour l'administration) expliquent l'usage de `--skip-specs`.
Chaque archivage réel sort en 0 avec `specsUpdated=false`. Les 78 empreintes
canoniques sont identiques au début de cette phase. Le bilan historique commun
est **10 CONFORME / 0 ÉCART / 1 NON VÉRIFIABLE / 1 NON APPLICABLE partielle**, soit
12 tâches uniques ; les tâches communes ne sont comptées qu'une fois.
Aucune ancienne mesure n'est présentée comme une mesure actuelle. [Preuves](../../../../output/revalidation-split/20261026T192534Z/state.json).


### Actualisation — correction et réarchivage du 26 octobre 2026

Intervention directe de Codex, explicitement autorisée par le développeur.
Les mesures RCAMP2 conservées dans cette section restent historiques et ne
sont ni remplacées ni additionnées à cette intervention. Les preuves courantes
sont [enregistrées séparément](../../../../output/revalidation-correction/20261026T184155Z/state.json). Le réarchivage réel réussit avec
`specsUpdated=false` ; les 78 empreintes canoniques sont identiques sur la
fenêtre immédiate de la commande native de réarchivage (18:45:59–18:46:00 UTC).

| Mesure documentaire | Avant correction | Après réarchivage |
|---|---:|---:|
| Fichiers de deltas | 4 | 4 |
| Exigences | 13 | 13 |
| Scénarios | 15 | 21 |
| Avertissements des deltas stricts | 5 | 0 |
| Erreurs des deltas stricts | 0 | 0 |
| Erreur de granularité de la proposition complète | 1 | 1 |

Le contrôle des deltas stricts passe ; la proposition complète reste refusée,
en mode standard comme en strict, pour plus de 10 deltas. Le retour 0 des
commandes de contrôle ciblant les deltas ne transforme pas ce refus en succès.
Verdicts actuels : **9 CONFORME (75,0 %), 1 ÉCART (8,3 %), 1 NON VÉRIFIABLE
(8,3 %), 1 NON APPLICABLE partielle (8,3 %), total 12 (100 %)** ; écarts de
somme à une décimale dus aux arrondis. L'écart est documentaire (proposition),
aucun comportement produit n'est qualifié. La permission actuelle couvre les
corrections et ce réarchivage ; aucune décision CAB nouvelle n'est revendiquée.


- Durée calendaire source : 1489.700832 s = 00 h 24 min 49.701 s (pauses et attentes incluses).
- Messages : 85 (table rôles en section 2, sans attribution succès/échec).
- Outils natifs : 68 = 64 succès (94.1 %) + 4 erreurs (5.9 %) — total 100 %.
  - Détail erreurs sans double-compte : 2 CLI exit 1 + 1 MCP -32602 + 1 read absent.
- Décisions CAB (périmètre RUN) : 9 = 9 approved (100.0 %) + 0 rejected (0.0 %) + 0 needs_clarification (0.0 %) ; once 9/9 (100.0 %) ; pending 0 ; technicalErrors 0.
- Tokens natifs seule session : total 10159195 = input 589311 + output 29617 + reasoning 7509 + cache_read 9532758 + cache_write 0.
- Coût natif seule session : 0.085421816 USD — coût natif mesuré de cette session, pas « partagé », ni facture vérifiée ; seuls les QUOTAS compte sont partagés (voir section 6).
- Compaction : N/A motivé (non instrumentée en session native).
- Convention : approuvé et exécuté = appel terminé avec succès ; refusé = refus permission explicite (0 ici) ; erreur technique = échec sans refus (4 ici). Un appel réussi ne prouve pas une approbation manuelle.
- Résultats : 4 stricts valides (canons V1–V4) / 2 limites adressage archive (E1–E2) ; verdicts 9 CONFORME (75.0 % des 12), 0 ÉCART (0.0 %), 2 NON VÉRIFIABLE (16.7 %), 1 NON APPLICABLE (8.3 %).
- Intégrité temporelle : constat préliminaire 32 identiques à `2026-10-26T18:00:32.903544+00:00` ; CHANGEMENT CONCURRENT après publication : différence `DEVOPS.md` constatée à `2026-10-26T18:10:54.100106+00:00` — final 31 empreintes identiques + DEVOPS différent, archive 9 inchangée hors stats. Non annulé, non attribué à cet audit. Nouveau DEVOPS relu par Codex : inventaire `2026-10-26T18:00:35Z` au lieu de `16:53:15Z`, rubrique SSH/SSHPASS absente, chemins/versions OpenSpec 1.15.0 OpenCode 1.19.4 Python 3.14.10 Node 24.22.1 NPM 11.19.1 conservés, autorisations et index prompts conservés. Aucun SSH utilisé. 4 contrôles mêmes entrées, pas de retest justifié. Complément en section 6 ; sans réécrire le rapport publié ni revendiquer 32 au final. Résultat 9/0/2/1 inchangé.

## 2. Types de messages et d'outils

### Collecte de la validation globale

Intervention directe de Codex, famille GPT-6 déclarée, fournisseur OpenAI ;
aucun agent orchestrateur ni nouvelle session OpenCode. Version exacte,
effort, messages, tokens, coût, TTMT, débit et temps de service : N/A —
télémétrie exclusive indisponible. Sondes périodiques non activées.
Une commande externe instrumentée produit ce relevé ; le nombre total des
lectures et appels techniques n'est pas reconstitué. Aucune décision CAB
n'est comptabilisée comme une nouvelle autorisation dans cette phase.


### Agent et collecte de cette phase de découpage

Codex intervient directement comme agent de codage ; aucun agent orchestrateur
ni nouvelle session OpenCode n'est lancé. Modèle : famille GPT-6 déclarée,
fournisseur OpenAI. Version exacte, effort, tokens, coût, TTMT, débit, durée de
génération, messages et outils globaux : **N/A — données exclusives non instrumentées**.
Sondes : N/A — non activées, sans reprise des sondes historiques comme mesures
actuelles. Cinq commandes externes sont instrumentées pour ce lot, dix pour
l'ensemble des deux lots ; ces commandes sont détaillées, sans estimation du
nombre total d'appels de l'agent. Aucune nouvelle décision CAB n'est revendiquée.
Un incident d’E/S sur la copie des métadonnées de `proposal.md` est réconcilié sans changement de permissions ; il est distinct des cinq commandes externes réussies et ne doit pas être compté comme échec du validateur.


### Actualisation — agent direct et limites de collecte

Agent de codage de cette actualisation : Codex, famille GPT-6 déclarée,
fournisseur OpenAI ; version exacte, effort, tokens, coût, TTMT, débit et temps
de service : **N/A — télémétrie exclusive indisponible**. Aucun agent
orchestrateur ou OpenCode n'opère dans cette intervention directe.
Les tableaux d'agents et les messages du RUN RCAMP2 restent historiques.
Messages et outils globaux de cette demande : N/A — absence de collecte
exhaustive attribuable ; les cinq commandes instrumentées sont détaillées
séparément. Sondes périodiques : N/A — non activées, sans reconstruction
rétroactive ni reprise des anciennes sondes comme mesures actuelles.


| Rôles messages (85, sans succès/échec) | Effectif | % / 85 |
|---|---:|---:|
| utilisateur | 31 | 36.5 % |
| assistant | 54 | 63.5 % |
| Total | 85 | 100 % |

| Outils natifs (68) | Total | Succès | Erreurs | % domaine / 68 | Taux succès ligne | Taux erreur ligne |
|---|---:|---:|---:|---:|---:|---:|
| cgpt-validation_broker_readiness | 5 | 5 | 0 | 7.4 % | 100.0 % | 0.0 % |
| cgpt-validation_request_validation | 10 | 9 | 1 | 14.7 % | 90.0 % | 10.0 % |
| bash (transport completed 8 expliqué ; succès/échec au niveau commande) | 8 | 6 | 2 | 11.8 % | 75.0 % | 25.0 % |
| cgpt-validation_broker_health | 1 | 1 | 0 | 1.5 % | 100.0 % | 0.0 % |
| read | 43 | 42 | 1 | 63.2 % | 97.7 % | 2.3 % |
| write | 1 | 1 | 0 | 1.5 % | 100.0 % | 0.0 % |
| Total | 68 | 64 | 4 | 100 % | 94.1 % | 5.9 % |

| Parties (313) | Effectif | % / 313 |
|---|---:|---:|
| text | 80 | 25.6 % |
| step-start | 54 | 17.3 % |
| reasoning | 57 | 18.2 % |
| tool | 68 | 21.7 % |
| step-finish | 54 | 17.3 % |
| Total | 313 | 100 % |

| Terminaisons réponses (54) | Effectif | % / 54 |
|---|---:|---:|
| stop | 19 | 35.2 % |
| tool-calls | 35 | 64.8 % |
| Total | 54 | 100 % |

- Sondes codage (surcharge séparée, hors production) : 2 prévues, 2 réussies (100.0 %), 0 échouée (0.0 %), 0 manquée (0.0 %) ; intervalle < 30 min ; initiale `2026-10-26T17:49:14.068309+00:00` TTMT 2.346235085 s débit 253.962035737 t/s tokens 909 ; finale `2026-10-26T18:07:53.724192+00:00` TTMT 2.833629152 s débit 192.896383177 t/s tokens 929 ; min TTMT 2.346235085 s / max 2.833629152 s ; min débit 192.896383177 t/s / max 253.962035737 t/s ; moyenne TTMT 2.589932 s ; moyenne débit 223.429209 t/s ; sortie cumulée 1838 tokens ; requêtes cumulées 13.782166 s ; versions/service N/A. Pas de métrique benchmark PLLM en guise de production.
- Temps de service et % : N/A — busy CAB inclut outils/attentes, aucune assimilation à la génération.

## 3. Fichiers modifiés

### Périmètre des écritures de cette actualisation

La liste commune des quatre documents actualisés est la suivante ; ses
éléments ne sont comptés qu'une fois pour cette intervention.

| Chemin absolu | Part des quatre documents |
|---|---:|
| /home/devops/datas/pixs/output/rcamp/rcamp2-pixs-d2dfdf5ddd024b9b/REVALIDATION.md | 25,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-specify-initial-administration-and-maintenance/REVALIDATION.md | 25,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/STATISTIQUES.md | 25,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-specify-initial-administration-and-maintenance/STATISTIQUES.md | 25,0 % |
| Total | 100 % |

Les sauvegardes et sorties de preuve sont des artefacts non versionnés sous
`output/openspec-global-strict/` ; les taux d'écritures bas niveau sont
N/A — non instrumentés. Aucune spécification canonique ni delta archivé,
proposition, tâche, configuration, README ou PROJECT.md n'est modifié.
Aucun nouvel archivage n'est effectué.


### Fichiers de cette phase — lot bootstrap

| Chemin absolu | Nature | Part de la liste propre au lot |
|---|---|---:|
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/proposal.md | Métadonnée ou rapport actualisé | 20,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/design.md | Métadonnée ou rapport actualisé | 20,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/tasks.md | Métadonnée ou rapport actualisé | 20,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/README.md | Métadonnée ou rapport actualisé | 20,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/STATISTIQUES.md | Métadonnée ou rapport actualisé | 20,0 % |
| Total | Liste de 5 fichiers propres | 100 % |

Le delta bootstrap et `.openspec.yaml` sont conservés. Les trois autres deltas sont transférés au lot compagnon à octets identiques. Le rapport commun, README.md et PROJECT.md sont des fichiers partagés, non comptés deux fois.
Nombre d'écritures bas niveau et répartition par permission : N/A — non instrumentés.
L'autorisation provient directement de la demande du développeur. Les copies
isolées et sauvegardes sous `/home/devops/datas/pixs/output/revalidation-split/20261026T192534Z` sont des artefacts non versionnés distincts.


### Actualisation — périmètre des quatre fichiers documentaires

| Fichier cible (chemin absolu) | Modification | Part des 4 cibles |
|---|---|---:|
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/specs/initial-administration/spec.md | Répartition de quatre descriptions dans les scénarios | 25,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/specs/initial-application-bootstrap/spec.md | Répartition d'une description dans les scénarios | 25,0 % |
| /home/devops/datas/pixs/output/rcamp/rcamp2-pixs-d2dfdf5ddd024b9b/REVALIDATION.md | Résultat courant, verdicts et réarchivage ; relevé historique conservé | 25,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/STATISTIQUES.md | Ajouts datés dans les six sections ; anciens chiffres conservés | 25,0 % |
| Total | 4 cibles | 100 % |

Les trois déplacements techniques du réarchivage sont tracés dans les preuves,
sans être comptés comme de nouvelles modifications fonctionnelles. L'identité
historique du dossier est restituée. Sauvegardes, copie isolée et journal sous
`/home/devops/datas/pixs/output/revalidation-correction/20261026T184155Z` : artefacts non versionnés distincts ; nombre d'écritures bas niveau
N/A — non instrumenté. Les cases de `tasks.md` restent identiques.


| Chemin absolu complet | Tentatives | Approuvées | Refusées | Erreur | % / total écritures natives |
|---|---:|---:|---:|---:|---:|
| /home/devops/datas/pixs/output/rcamp/rcamp2-pixs-d2dfdf5ddd024b9b/REVALIDATION.md | 1 (100 %) | 1 (100 %) | 0 (0 %) | 0 (0 %) | 100 % |

- Il s'agit de tentatives ; 1 écriture bilan approuvée observée, 0 refusée, 0 en erreur.
- Fichiers orchestrateur hors session native, effectifs N/A non instrumentés (chemins absolus complets) : `/home/devops/datas/pixs/output/rcamp/rcamp2-pixs-d2dfdf5ddd024b9b/state.json` (N/A), `/home/devops/datas/pixs/output/rcamp/rcamp2-pixs-d2dfdf5ddd024b9b/preuves-tests.json` (N/A), `/home/devops/datas/pixs/output/rcamp/rcamp2-pixs-d2dfdf5ddd024b9b/preuves-statistiques.json` (N/A), `/home/devops/datas/pixs/output/rcamp/rcamp2-pixs-d2dfdf5ddd024b9b/preuves-sse.jsonl` (N/A).
- Futur `/home/devops/datas/pixs/openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/STATISTIQUES.md` hors coupure : ne pas l'inclure rétroactivement.
- Aucun déplacement ni archivage nouveau ; archive 9 fichiers préservés.

## 4. Commandes

### Commande globale instrumentée

| Commande exacte (moins de 100 caractères) | Exécutions | Retour 0 | Retours non nuls |
|---|---:|---:|---:|
| `/home/devops/.local/npm/bin/openspec validate --all --strict --json --no-interactive` | 1 | 1 (100 %) | 0 (0 %) |

Début : 2026-10-26T19:43:21.110328+00:00 ; fin : 2026-10-26T19:43:21.865184+00:00.
Durée instrumentée du contrôle et de ses relevés : 0.757762 s.
Aucun refus de permission n'est observé pour cette commande. Les 88 INFO
se répartissent en 87 déclarations préexistantes `skip_specs` et une
information de simulation d'ajout déjà présent pour
`define-common-pbo-binary-and-resource-profiles`. Ils ne sont comptés ni
comme avertissements ni comme échecs. Les anciens contrôles ciblés des
archives ne sont pas présentés comme rejoués par `--all`.
[Sortie intégrale](../../../../output/openspec-global-strict/20261026T194321Z/validation.json).


### Commandes instrumentées du lot bootstrap

| Preuve | Commande (100 caractères maximum) | Retour | Début UTC |
|---|---|---:|---|
| V-PREP-BOOTSTRAP | `/home/devops/node/current/bin/node --input-type=module - /home/devops/datas/pixs/output/revalidatio…` | 0 | 2026-10-26T19:27:53.572462+00:00 |
| A-TEST-BOOTSTRAP | `/home/devops/.local/npm/bin/openspec archive specify-initial-application-bootstrap --skip-specs --y…` | 0 | 2026-10-26T19:28:44.372220+00:00 |
| V-CLI-BOOTSTRAP | `/home/devops/.local/npm/bin/openspec validate specify-initial-application-bootstrap --type change -…` | 0 | 2026-10-26T19:29:49.382899+00:00 |
| A-PROJECT-BOOTSTRAP | `/home/devops/.local/npm/bin/openspec archive specify-initial-application-bootstrap --skip-specs --y…` | 0 | 2026-10-26T19:30:21.015919+00:00 |
| V-FINAL-BOOTSTRAP | `/home/devops/node/current/bin/node --input-type=module - /home/devops/datas/pixs/openspec/changes/a…` | 0 | 2026-10-26T19:31:57.604803+00:00 |

**5 commandes : 5 retours 0 (100,0 %), 0 retour non nul (0,0 %), 0 refus de
permission observé (0,0 %).** Le total commun est de 10 commandes, ces cinq
représentent 50,0 %. Un essai d'archivage isolé et un archivage réel du projet
sont distingués pour chaque lot : il y a deux archivages réels du projet,
non quatre. Le contrôle des propositions et celui des deltas ont chacun leur
rapport JSON ; aucun n'est omis du calcul de succès des commandes V-*.
L'incident de copie Python est traité séparément, hors ce dénominateur.
Arguments et entrées JavaScript complets, sorties et dates : [preuves](../../../../output/revalidation-split/20261026T192534Z/state.json).


### Actualisation — commandes instrumentées de correction et de réarchivage

| Identifiant de preuve | Commande (100 caractères au plus) | Retour | Début UTC |
|---|---|---:|---|
| V-CORRECTED-PREPARED | `/home/devops/node/current/bin/node --input-type=module - /home/devops/datas/pixs/output/revalidatio…` | 0 | 2026-10-26T18:44:46.044790+00:00 |
| A-SANDBOX | `/home/devops/.local/npm/bin/openspec archive specify-initial-application-bootstrap --skip-specs --y…` | 0 | 2026-10-26T18:44:52.380319+00:00 |
| V-ARCHIVE-CORRECTED | `/home/devops/node/current/bin/node --input-type=module - /home/devops/datas/pixs/openspec/changes/a…` | 0 | 2026-10-26T18:45:48.372285+00:00 |
| A-PROJECT | `/home/devops/.local/npm/bin/openspec archive specify-initial-application-bootstrap --skip-specs --y…` | 0 | 2026-10-26T18:45:59.751814+00:00 |
| V-REARCHIVE | `/home/devops/node/current/bin/node --input-type=module - /home/devops/datas/pixs/openspec/changes/a…` | 0 | 2026-10-26T18:47:00.974867+00:00 |

Total instrumenté : **5 commandes, 5 retours 0 (100,0 %),
0 refus de permission observé (0,0 %), 0 retour non nul (0,0 %)**.
Ce dénominateur couvre les commandes de validation et d'archivage enregistrées,
pas les lectures et préparations antérieures. Trois commandes de contrôle
ciblent le succès des deltas ; elles conservent séparément les rapports de
proposition non conformes. Le rejet sur 13 deltas est un diagnostic observé,
non un succès du validateur complet. Une exécution d'archivage concerne la
copie isolée et une seule le projet réel : ne pas les confondre ni compter
deux réarchivages du projet. Commandes et sorties intégrales : [preuves](../../../../output/revalidation-correction/20261026T184155Z/state.json).


| Famille | Effectif | % / 8 commandes | exit 0 | exit 1 |
|---|---:|---:|---:|---:|
| /usr/bin/true (prévol) | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) |
| openspec validate --help | 1 | 12.5 % | 1 (100.0 %) | 0 (0.0 %) |
| openspec validate <spec> strict (V1–V4) | 4 | 50.0 % | 4 (100.0 %) | 0 (0.0 %) |
| openspec validate <archive> strict (E1–E2) | 2 | 25.0 % | 0 (0.0 %) | 2 (100.0 %) |
| Total | 8 | 100 % | 6 (75.0 %) | 2 (25.0 %) |

- Libellés tronqués à 100 caractères : `/usr/bin/true` ; `/home/devops/.local/npm/bin/openspec validate --help` ; `/home/devops/.local/npm/bin/openspec validate initial-application-bootstrap --type spec --stric…` ; `/home/devops/.local/npm/bin/openspec validate initial-administration --type spec --strict --json -…` ; `/home/devops/.local/npm/bin/openspec validate operations --type spec --strict --json --no-intera…` ; `/home/devops/.local/npm/bin/openspec validate audit --type spec --strict --json --no-interactive` ; `/home/devops/.local/npm/bin/openspec validate openspec/changes/archive/2026-09-16-specify-in…` ; `/home/devops/.local/npm/bin/openspec validate 2026-09-16-specify-initial-application-bootstrap -…`.
- Commandes refusées regroupées : aucune (0 refus permission ; E1/E2 et -32602 = erreurs techniques, non refus).
- 8 commandes intégrales non tronquées : voir [preuves-tests.json](../../../../output/rcamp/rcamp2-pixs-d2dfdf5ddd024b9b/preuves-tests.json).
- 4 stricts valides sans diagnostic (V1–V4) ; 2 limites adressage archive (E1 chemin refusé, E2 nom actif sans delta).

## 5. Accès web

### Accès de cette validation globale

Aucun outil de recherche ou de navigation web n'est utilisé : 0 accès web
d'agent observé ; pourcentages N/A — dénominateur nul. Les relevés de quota
natifs sont des opérations techniques distinctes. Le réseau interne du CLI
n'est pas instrumenté, sans affirmation d'absence globale de trafic hôte.
Aucun secret n'est lu ou copié dans les preuves ; Git n'est ni inspecté
ni modifié.


### Accès de cette phase

Aucun outil de recherche ou de navigation web n'est utilisé : 0 accès web d'agent
observé. Pourcentages web N/A — dénominateur nul. Les lectures natives de quota
et du registre local sont des opérations techniques distinctes. Le réseau
interne des exécutables n'est pas instrumenté ; aucune absence globale de
trafic hôte n'est affirmée. Aucun secret n'est lu, affiché ou copié dans les
preuves. Aucune opération Git n'est exécutée ou inspectée.


### Actualisation — accès observés

Aucun outil de recherche ou de navigation web n'est utilisé pour cette
correction : 0 accès web d'agent observé. Pourcentages de succès, refus et
erreur web : N/A — dénominateur nul. Les lectures de quota natives et du
registre local sont des opérations techniques distinctes. Le réseau interne
des exécutables n'est pas instrumenté ; aucune absence globale de trafic hôte
n'est déduite de ce relevé. Aucune valeur secrète n'est lue ou copiée dans les
preuves. Aucune opération Git n'est exécutée ou inspectée.


| Statut | Nombre | % / total web natif |
|---|---:|---:|
| Approuvés | 0 | N/A — dénominateur zéro, aucune URL approuvée à conserver |
| Refusés | 0 | N/A — dénominateur zéro, aucune URL refusée à conserver |
| Erreurs | 0 | N/A — dénominateur zéro |
| Total observé session native | 0 | N/A — dénominateur zéro (aucun % calculable) |

- Aucune URL effectivement visitée par l'agent ; ne pas présenter une URL refusée comme visitée.
- HTTP loopback technique (contrôleur/broker) distinct hors session : N/A pour l'agrégat orchestration.
- Aucune requête web agent : indiqué explicitement.

## 6. Synthèse globale

### Synthèse du contrôle global strict

| Mesure | Valeur |
|---|---|
| Début du contrôle instrumenté | 2026-10-26T19:43:21.110328+00:00 |
| Fin du contrôle | 2026-10-26T19:43:21.865184+00:00 |
| Durée du contrôle et de ses relevés | 0.757762 s |
| Relevé final après contrôle, avant synthèse | 2026-10-26T19:43:51+00:00 |
| Durée totale de la demande | N/A — analyse préparatoire non chronométrée |
| Archivage | Sans objet — actualisation de rapports uniquement |

| Quota Codex sur sept jours | Horodatage UTC | Utilisé | Réinitialisation |
|---|---|---:|---|
| Avant contrôle | 2026-10-26T19:43:21+00:00 | 100 % | 2026-11-02T06:01:55+00:00 |
| Après contrôle, avant synthèse | 2026-10-26T19:43:51+00:00 | 100 % | 2026-11-02T06:01:55+00:00 |
| Variation | — | 0 point de pourcentage | — |

Source native : `mcp__codex_app__get_usage_limits`, même compte et même fenêtre
10080 minutes vérifiés. Le compteur partagé, plafonné à 100 %, ne permet pas
de déduire une consommation nulle de sa variation nulle. Les relevés sont
communs aux deux archives et ne sont pas additionnés ni attribués à un lot.

Bilan global : **186/186 valides, retour 0, 0 erreur, 0 avertissement,
88 INFO**. Les anciens résultats ciblés des deux archives et les relevés des
interventions antérieures restent datés et séparés. La portée de `--all` est
108 changes actifs et 78 spécifications canoniques ; elle ne revalide ni
les archives ni un comportement produit. Le canon est préservé et aucune
correction ou opération Git n'est effectuée. [Preuve](../../../../output/openspec-global-strict/20261026T194321Z/validation.json).


### Synthèse de la phase de découpage et archivage

| Durée de collecte commune aux deux lots | Valeur |
|---|---|
| Début enregistré de la préparation | 2026-10-26T19:25:34.517521+00:00 |
| Fin après archivages et contrôles, avant synthèse | 2026-10-26T19:32:58+00:00 |
| Durée de l'intervalle enregistré, attentes incluses | 00 h 07 min 23.482 s |
| Durée totale de la demande, analyse préliminaire incluse | N/A — début de l'analyse non chronométré |

| Quota Codex sur 7 jours — source native | Horodatage UTC | Utilisé | Réinitialisation |
|---|---|---:|---|
| Avant préparation | 2026-10-26T19:25:34+00:00 | 100 % | 2026-11-02T06:01:55+00:00 |
| Après archivages, avant synthèse | 2026-10-26T19:32:58+00:00 | 100 % | 2026-11-02T06:01:55+00:00 |
| Variation | — | 0 point de pourcentage | — |

Source : `mcp__codex_app__get_usage_limits`, même compte et même fenêtre
10080 minutes vérifiés. Le compteur partagé est plafonné à 100 % : une variation
nulle ne prouve pas une consommation nulle. Les deux archives partagent ces
bornes et ces relevés ; ils ne doivent pas être additionnés ni attribués
exclusivement à un lot. Les tokens et le coût de cette phase sont N/A.

Résultat propre au lot : 4 exigences et 6 scénarios,
proposition complète et deltas stricts valides, archivage réel retour 0,
`specsUpdated=false`. L'erreur documentaire de granularité est levée ; le bilan
commun des douze tâches est 10/0/1/1. La présentation préalable à l'archivage
initial de septembre reste non vérifiable et la restriction Super Admin au seul
panneau reste remplacée par l'évolution canonique ultérieure. Aucune preuve de
fonctionnement produit n'est créée. Le canon, le nombre de garanties normatives
et leur texte sont conservés. Les statistiques antérieures conservent leur
périmètre et ne sont ni recalculées ni additionnées à cette phase.
Rapport courant : [rapport commun](../../../../output/rcamp/rcamp2-pixs-d2dfdf5ddd024b9b/REVALIDATION.md).


### Actualisation — synthèse après réarchivage

| Mesure de durée de cette intervention | Valeur |
|---|---|
| Début de l'intervalle local enregistré | 2026-10-26T18:41:55.333053+00:00 |
| Fin après réarchivage et contrôles, avant rédaction de la synthèse | 2026-10-26T18:49:32+00:00 |
| Durée de l'intervalle instrumenté, attentes comprises | 00 h 07 min 36.667 s |
| Durée totale de la demande, analyse préliminaire comprise | N/A — début de l'analyse non horodaté, sans reconstruction rétroactive |

| Quota Codex sur 7 jours — cette actualisation | Horodatage | Utilisé | Réinitialisation |
|---|---|---:|---|
| Avant les modifications | N/A — heure exacte non enregistrée ; relevé natif antérieur aux écritures | 100 % | 2026-11-02T06:01:55+00:00 |
| Après réarchivage et contrôles | 2026-10-26T18:49:32+00:00 | 100 % | 2026-11-02T06:01:55+00:00 |
| Variation après moins avant | — | 0 point de pourcentage | — |

Source : outil natif `mcp__codex_app__get_usage_limits`, fenêtre 10080 minutes.
Identité du compte et fenêtre identiques vérifiées. Quota partagé et compteur
plafonné à 100 % : cette variation nulle ne prouve pas une consommation nulle
et ne permet aucune attribution exclusive, en tokens ou en coût, à cette
intervention. Les anciens relevés 88 % et 95 % du RUN RCAMP2 restent historiques.

Les quatre fichiers de deltas passent le strict sans diagnostic. La proposition
complète conserve une erreur sur ses 13 deltas, en standard et en strict ;
le bilan actuel est donc **9 CONFORME / 1 ÉCART / 1 NON VÉRIFIABLE /
1 NON APPLICABLE partielle**. Le défaut de preuve historique de présentation
initiale demeure ; l'autorisation du réarchivage actuel ne le résout pas.

Réarchivage du projet : retour 0 le 2026-10-26T18:46:00.406520+00:00,
`specsUpdated=false`, identité historique restituée, aucune seconde archive
ni change actif résiduel. Cinq exigences sont réorganisées sans suppression
de garantie ; 13 exigences et 21 scénarios après correction. Canon :
78 empreintes conservées sur la fenêtre immédiate du réarchivage. Rapport actuel : [REVALIDATION.md](../../../../output/rcamp/rcamp2-pixs-d2dfdf5ddd024b9b/REVALIDATION.md).
### Limite du contrôle concurrent — constat du 2026-10-26T18:57:04.802915+00:00

Par rapport à l'empreinte initiale de cette intervention, une différence est
observée dans `openspec/specs/component-model/spec.md`, hors de la liste des
fichiers écrits par cette correction. Son instant de modification n'est pas
établi par ce contrôle. Elle n'est ni annulée ni incorporée à cette correction.
La comparaison des 78 empreintes immédiatement avant et après la commande
native de réarchivage reste positive ; les quatre capacités canoniques portées
par cette archive sont inchangées. L'intégrité globale du canon depuis le début
n'est donc pas revendiquée. La validation stricte des deltas archivés ne
réapplique aucune spécification et conserve son résultat sans diagnostic.

Le présent ajout autorisé remplace les anciennes conclusions pour le strict
de cette cible ; les anciennes mesures, leurs bornes et leurs totaux ne sont
pas recalculés. Aucun nouveau gate CAB ni résultat produit n'est annoncé.


| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-26T17:43:55.282000+00:00 |
| Fin — avant synthèse (archivage sans objet) | 2026-10-26T18:08:44.982832+00:00 |
| Durée globale (pauses et attentes incluses) | 00 h 24 min 49.701 s (1489.700832 s) |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | 2026-10-26T17:45:33.089306+00:00 | 88 % | 2026-11-02T06:01:55+00:00 |
| Après — avant synthèse (archivage sans objet) | 2026-10-26T18:08:44.982817+00:00 | 95 % | 2026-11-02T06:01:55+00:00 |
| Différence après − avant | — | +7 points de pourcentage | — |

- Quotas partagés du compte : variation +7 points pendant la session, peut inclure d'autres tâches simultanées ; même resetsAt `1793599315` → `2026-11-02T06:01:55+00:00`, comparaison vérifiable ; ne pas attribuer exclusivement au RUN.
| Domaine | Total | Part globale / 68 | Succès | Refus | Erreurs | Taux succès ligne | Taux refus ligne | Taux erreur ligne |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fichiers | 1 | 1.5 % | 1 | 0 | 0 | 100.0 % | 0.0 % | 0.0 % |
| commandes | 8 | 11.8 % | 6 | 0 | 2 | 75.0 % | 0.0 % | 25.0 % |
| web | 0 | 0.0 % | 0 | 0 | 0 | N/A | N/A | N/A |
| autres | 59 | 86.8 % | 57 | 0 | 2 | 96.6 % | 0.0 % | 3.4 % |
| Global | 68 | 100 % (100.1 % possible par arrondis à une décimale) | 64 | 0 | 4 | 94.1 % | 0.0 % | 5.9 % |
- Complément final au REVALIDATION.md : ancien constat 32 identiques PRÉLIMINAIRE à `2026-10-26T18:00:32.903544+00:00` ; final 31 empreintes identiques + DEVOPS différent (`initial 76f49bd4859af677c59a6154eb7e45a917426b45bf43c60b48b204af7fe19bdf` → observé `16c3edca135d7491a309574fbfc211013159b57750fae67bb51976c2de47fc2a` à `2026-10-26T18:10:54.100106+00:00`), archive 9 inchangée hors stats. Ceci corrige la portée temporelle, sans réécrire le rapport publié ni prétendre 32 au final. Résultat 9/0/2/1 inchangé.
- État : tests documentaires 4/4 valides, 2 limites archive documentées, secrets non lus, accès externes agent 0. Gate et livraison : aucune conclusion validée ou livrée avant preuve.
- Demande : création après révision Codex, pas de rédaction source hors stats.
