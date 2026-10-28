# Statistiques — lot administration, maintenance et audit

> **Validation globale stricte du 26 octobre 2026 : 186/186 valides, 0 erreur, 0 avertissement, 88 INFO.** Ce relevé commun est ajouté aux historiques sans modification du canon.

Archive : `2026-10-26-specify-initial-administration-and-maintenance`.
Rapport créé après archivage, pour le découpage documentaire explicitement demandé.
Les mesures historiques du change initial ne sont ni copiées comme mesures
actuelles ni réparties arbitrairement. Les données absentes valent N/A.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Codex — famille GPT-6 déclarée | N/A | OpenAI | N/A | N/A — sondes non activées | N/A — sondes non activées | N/A — non instrumenté |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---:|
| Aucun agent orchestrateur dans cette intervention directe | N/A | N/A | N/A | N/A | N/A | N/A |

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

Lot propre : **9 exigences / 13** (69.2 %) et
**15 scénarios / 21** (71.4 %) ; le complément se trouve
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
L’incident d’E/S de préparation du bootstrap est documenté dans les preuves communes ; il n’est pas réattribué comme une deuxième erreur de ce lot.

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


### Fichiers de cette phase — lot administration, maintenance et audit

| Chemin absolu | Nature | Part de la liste propre au lot |
|---|---|---:|
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-specify-initial-administration-and-maintenance/.openspec.yaml | Document ou métadonnée propre au lot | 10,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-specify-initial-administration-and-maintenance/proposal.md | Document ou métadonnée propre au lot | 10,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-specify-initial-administration-and-maintenance/design.md | Document ou métadonnée propre au lot | 10,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-specify-initial-administration-and-maintenance/tasks.md | Document ou métadonnée propre au lot | 10,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-specify-initial-administration-and-maintenance/README.md | Document ou métadonnée propre au lot | 10,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-specify-initial-administration-and-maintenance/REVALIDATION.md | Document ou métadonnée propre au lot | 10,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-specify-initial-administration-and-maintenance/STATISTIQUES.md | Document ou métadonnée propre au lot | 10,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-specify-initial-administration-and-maintenance/specs/initial-administration/spec.md | Delta transféré sans modification | 10,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-specify-initial-administration-and-maintenance/specs/operations/spec.md | Delta transféré sans modification | 10,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-specify-initial-administration-and-maintenance/specs/audit/spec.md | Delta transféré sans modification | 10,0 % |
| Total | Liste de 10 fichiers propres | 100 % |

Sept documents ou métadonnées sont créés pour ce lot et trois deltas sont transférés sans changement. Ces fichiers ne constituent pas neuf exigences nouvelles dans le canon. Le rapport commun et le suivi global sont partagés avec le bootstrap.
Nombre d'écritures bas niveau et répartition par permission : N/A — non instrumentés.
L'autorisation provient directement de la demande du développeur. Les copies
isolées et sauvegardes sous `/home/devops/datas/pixs/output/revalidation-split/20261026T192534Z` sont des artefacts non versionnés distincts.

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


### Commandes instrumentées du lot administration, maintenance et audit

| Preuve | Commande (100 caractères maximum) | Retour | Début UTC |
|---|---|---:|---|
| V-PREP-ADMINISTRATION | `/home/devops/node/current/bin/node --input-type=module - /home/devops/datas/pixs/output/revalidatio…` | 0 | 2026-10-26T19:27:53.727136+00:00 |
| A-TEST-ADMINISTRATION | `/home/devops/.local/npm/bin/openspec archive specify-initial-administration-and-maintenance --skip-…` | 0 | 2026-10-26T19:28:45.102404+00:00 |
| V-CLI-ADMINISTRATION | `/home/devops/.local/npm/bin/openspec validate specify-initial-administration-and-maintenance --type…` | 0 | 2026-10-26T19:29:12.592469+00:00 |
| A-PROJECT-ADMINISTRATION | `/home/devops/.local/npm/bin/openspec archive specify-initial-administration-and-maintenance --skip-…` | 0 | 2026-10-26T19:30:28.596090+00:00 |
| V-FINAL-ADMINISTRATION | `/home/devops/node/current/bin/node --input-type=module - /home/devops/datas/pixs/openspec/changes/a…` | 0 | 2026-10-26T19:31:57.751834+00:00 |

**5 commandes : 5 retours 0 (100,0 %), 0 retour non nul (0,0 %), 0 refus de
permission observé (0,0 %).** Le total commun est de 10 commandes, ces cinq
représentent 50,0 %. Un essai d'archivage isolé et un archivage réel du projet
sont distingués pour chaque lot : il y a deux archivages réels du projet,
non quatre. Le contrôle des propositions et celui des deltas ont chacun leur
rapport JSON ; aucun n'est omis du calcul de succès des commandes V-*.
L'incident de copie Python est traité séparément, hors ce dénominateur.
Arguments et entrées JavaScript complets, sorties et dates : [preuves](../../../../output/revalidation-split/20261026T192534Z/state.json).

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

Résultat propre au lot : 9 exigences et 15 scénarios,
proposition complète et deltas stricts valides, archivage réel retour 0,
`specsUpdated=false`. L'erreur documentaire de granularité est levée ; le bilan
commun des douze tâches est 10/0/1/1. La présentation préalable à l'archivage
initial de septembre reste non vérifiable et la restriction Super Admin au seul
panneau reste remplacée par l'évolution canonique ultérieure. Aucune preuve de
fonctionnement produit n'est créée. Le canon, le nombre de garanties normatives
et leur texte sont conservés. Les statistiques antérieures conservent leur
périmètre et ne sont ni recalculées ni additionnées à cette phase.
Rapport courant : [rapport commun](../../../../output/rcamp/rcamp2-pixs-d2dfdf5ddd024b9b/REVALIDATION.md).

