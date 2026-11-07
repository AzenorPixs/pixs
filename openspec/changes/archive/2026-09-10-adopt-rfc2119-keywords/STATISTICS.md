# STATISTIQUES — adopt-rfc2119-keywords (revalidation)
RUN rcamp1-pixs-0b46eb1e9eee4dde, session ses_e86b1c3f3ffeZnTyXNUdoooMJ1, job rcamp1-audit-adopt-rfc2119-20261026, change_id adopt-rfc2119-keywords, archive openspec/changes/archive/2026-09-10-adopt-rfc2119-keywords. Phase REPORT, réservation 1326. Création autorisée car aucun rapport historique n’existe ; aucune reconstitution de l’implémentation de septembre. Compteurs natifs figés jusqu’au message msg_1797141710014ugu51R5h280rS, 2026-10-26T18:20:30.225+00:00 ; reprises techniques postérieures et production de ces statistiques exclues. Contrôleur : 7 approved, 7 once, 0 rejected ; demande CANCELLED distincte, erreurs schéma/timeout distinctes. Niveaux distingués : API 61 completed/64=95.3 % et 3 error/64=4.7 % ; opérationnel 59 réussis/64=92.2 % et 5 erreurs techniques/64=7.8 %, 0 refus/64=0.0 % ; les 2 bash exit 1 rejoignent les 3 erreurs MCP pour 5 erreurs opérationnelles. Ces dénominateurs ne sont pas les 7 décisions CAB (7 approved, 7 once).

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---|
| muse-spark-1.3-contributor | N/A | opencode-go | high | 1.365 s (3 sondes) | 724.0 (3 sondes) | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---|
| Codex — modèle exact N/A | N/A | OpenAI | N/A | N/A | N/A | N/A |

## 1. Statistiques générales et décisions
Durée calendaire bornée 2026-10-26T17:42:25.846Z à 2026-10-26T18:21:59Z = 39 min 33 s, pauses et attentes incluses ; archivage sans objet. Messages natifs 107 : user 35/107=32.7 %, assistant 72/107=67.3 %, total 100.0 %. Parties 391 : text 96/391=24.6 %, step-start 72/391=18.4 %, reasoning 87/391=22.3 %, tool 64/391=16.4 %, step-finish 72/391=18.4 %. Outils API 64 : 61 completed=95.3 %, 3 error=4.7 %, total 100.0 %. Opérationnel 64 : 59 réussis=92.2 %, 5 erreurs techniques=7.8 %, 0 refus=0.0 %, total 100.0 %. Décisions contrôleur : 7 approved/7=100.0 %, 0 rejected/7=0.0 %, 7 once. Demande CANCELLED distincte rcamp1-doc-control-01 sans effet. Tokens : total 13064263/13064263=100.0 %.

| Poste tokens | Valeur | Part du total |
|---|---|---:|
| input | 905055 | 6.9 % |
| output | 34639 | 0.3 % |
| reasoning | 27684 | 0.2 % |
| cache read | 12096885 | 92.6 % |
| cache write | 0 | 0.0 % |
| total | 13064263 | 100.0 % |

Cache read/write partition du total, sans double addition au total. Coût API brut 0.12716387, devise N/A. Compactions N/A. Développement : 4 verdicts 1C/4=25.0 %, 1E/4=25.0 %, 2NV/4=50.0 %, 0NA/4=0.0 % ; canon 78/78 ; archive 56 deltas, 205 exigences, 206 scénarios ; DOIVENT à component-model:108 ; archive 60/60 préservée ; DEVOPS diff externe préservée.

## 2. Types de messages et d’outils
Rôles, dénominateur 107 : user 35=32.7 %, assistant 72=67.3 %, total 100.0 %. Parties, dénominateur 391 : voir §1. Outils API, dénominateur 64.

| Outil | Completed | Error | Total | Part du total |
|---|---|---|---|---:|
| cgpt-validation_broker_readiness | 10 (100.0 %) | 0 (0.0 %) | 10 | 15.6 % |
| cgpt-validation_request_validation | 7 (77.8 %) | 2 (22.2 %) | 9 | 14.1 % |
| bash | 6 (100.0 %) | 0 (0.0 %) | 6 | 9.4 % |
| cgpt-validation_broker_health | 1 (100.0 %) | 0 (0.0 %) | 1 | 1.6 % |
| cgpt-validation_list_pending | 1 (100.0 %) | 0 (0.0 %) | 1 | 1.6 % |
| read | 19 (100.0 %) | 0 (0.0 %) | 19 | 29.7 % |
| grep | 6 (100.0 %) | 0 (0.0 %) | 6 | 9.4 % |
| glob | 7 (100.0 %) | 0 (0.0 %) | 7 | 10.9 % |
| cgpt-validation_get_approval | 2 (100.0 %) | 0 (0.0 %) | 2 | 3.1 % |
| cgpt-validation_poll_approval | 0 (0.0 %) | 1 (100.0 %) | 1 | 1.6 % |
| cgpt-validation_cancel_approval | 1 (100.0 %) | 0 (0.0 %) | 1 | 1.6 % |
| write | 1 (100.0 %) | 0 (0.0 %) | 1 | 1.6 % |
| Total | 61 (95.3 %) | 3 (4.7 %) | 64 | 100.0 % |

Opérationnel par outil : 6 bash completed incluent 4 exit 0 et 2 exit 1 techniques de résolution archive. Taux refus outils 0/64=0.0 % ; dénominateur 0 = N/A sans objet.

## 3. Fichiers modifiés
Tentative observée à la borne : 1. Le présent STATISTIQUES et les écritures state de l’orchestrateur sont hors compteurs ; nombre d’éditions root N/A.

| Chemin absolu | Approuvées | Refusées | En erreur |
|---|---|---|---|
| /home/devops/datas/pixs/output/rcamp/rcamp1-pixs-0b46eb1e9eee4dde/REVALIDATION.md | 1/1=100.0 % | 0/1=0.0 % | 0/1=0.0 % |

Aucun déplacement ni archivage. Total 1/1=100.0 %.

## 4. Commandes
6 natives, 4 exit 0 et 2 exit 1 techniques, 0 refus/6=0.0 %. Libellés ≤100 car, références exactes dans [REVALIDATION](../../../../output/rcamp/rcamp1-pixs-0b46eb1e9eee4dde/REVALIDATION.md) et [checkpoint](../../../../output/rcamp/rcamp1-pixs-0b46eb1e9eee4dde/state.json).

| Famille | Effectif/6 | Part |
|---|---|---:|
| true inoffensif | 1 | 16.7 % |
| aide validateur | 1 | 16.7 % |
| contrôle Python heredoc | 1 | 16.7 % |
| validation canon | 1 | 16.7 % |
| validation archive nom/chemin | 2 | 33.3 % |
| Total | 6 | 100.0 % |

Aucune commande refusée : 0.

## 5. Accès web
0 outil web observé, 0 URL. Approbations 0, refus 0, erreurs 0 ; dénominateur 0 = N/A pour tous taux. Aucune URL approuvée ou refusée à conserver. Transport modèles/API local non quantifié.

## 6. Synthèse globale
| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-26T17:42:25.846Z |
| Fin — archivage sans objet, fin des travaux | 2026-10-26T18:21:59Z |
| Durée globale (pauses et attentes incluses) | 00 h 39 min 33 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — début de session | N/A réel non exposé | 87 % | 1793599315 |
| Après — archivage sans objet, fin des travaux | entre 2026-10-26 18:21:58 UTC et 2026-10-26 18:21:59 UTC | 99 % | 1793599315 |
| Différence après − avant | — | 12 points | — |

Quotas partagés du compte, fenêtre 10080, même compte/fenêtre ; variation 12 points PARTAGÉE, non exclusive. Sondes codage 3 prévues, 3 réussies/3=100.0 %, 0 échouée/3=0.0 %, 0 manquée/3=0.0 %.

| Sonde | Date réelle | TTMT | Débit | Tokens | Statut |
|---|---|---|---|---:|---|
| début | 2026-10-26T17:48:11.546279+00:00 | 0.864 s | 1137.5/s | 520 | succès |
| +30 min | 2026-10-26T18:18:43.738054+00:00 | 1.345 s | 779.9/s | 520 | succès |
| fin | 2026-10-26T18:21:38.177900+00:00 | 1.887 s | 254.7/s | 520 | succès |
| Moyenne | — | 1.365 s | 724.0/s | 520 | — |
| Min | — | 0.864 s | 254.7/s | 520 | — |
| Max | — | 1.887 s | 1137.5/s | 520 | — |

1560 tokens surcharge séparée ; request moyen 2.468 s ; temps de service RUN N/A ; retard +30 min 32.192 s. Version modèle N/A ; modèle/effort orchestrateur précis non exposés N/A, fournisseur OpenAI, pas de sonde orchestrateur.

| Domaine | Total | Réussi | Erreur | Refus | Part du total | Taux réussi | Taux erreur | Taux refus |
|---|---|---|---|---|---|---:|---:|---:|
| Fichiers | 1 | 1 | 0 | 0 | 1.6 % | 100.0 % | 0.0 % | 0.0 % |
| Commandes | 6 | 4 | 2 | 0 | 9.4 % | 66.7 % | 33.3 % | 0.0 % |
| Web | 0 | 0 | 0 | 0 | 0.0 % | N/A | N/A | N/A |
| Autres outils | 57 | 54 | 3 | 0 | 89.1 % | 94.7 % | 5.3 % | 0.0 % |
| Total | 64 | 59 | 5 | 0 | 100.0 % | 92.2 % | 7.8 % | 0.0 % |

Dénominateurs ci-dessus : 64 outils et lignes respectives, pas les 7 décisions CAB. Ligne globale 64/64=100.0 %. Tests documentaires seuls, runtime non applicables ; canon 78/78 strict valide ; archive 60/60 préservée hors stats, 56/205/206 prouvés ; résidu DOIVENT component-model:108 ; DEVOPS diff externe préservée, 144/145 empreintes identiques. Rapport lié [REVALIDATION](../../../../output/rcamp/rcamp1-pixs-0b46eb1e9eee4dde/REVALIDATION.md). Aucun correctif, Git, synchronisation ou nouvel archivage. Aucun secret observé dans les sorties/livrables autorisés. Historique N/A conservé. Statut de clôture technique dans le [checkpoint](../../../../output/rcamp/rcamp1-pixs-0b46eb1e9eee4dde/state.json).

### Suivi post-clôture — correction DOIVENT → MUST — 26 octobre 2026

Mise à jour documentaire : `2026-10-26T19:53:26+01:00` (Europe/Paris). Référence : `correction-doivent-must-2026-10-26`. Détails et preuves : [suivi dans REVALIDATION.md](../../../../output/rcamp/rcamp1-pixs-0b46eb1e9eee4dde/REVALIDATION.md).

Cette entrée complète le rapport existant par ajout. Tous les tableaux, totaux, mesures, verdicts et conclusions qui précèdent restent ceux de l'audit initial et conservent leurs bornes. Les mentions historiques d'un résidu `DOIVENT` et d'absence de correctif décrivent l'état antérieur à l'autorisation ultérieure du développeur ; le correctif ci-dessous est postérieur à la clôture du RUN.

#### Périmètre et attribution du suivi

Le développeur a autorisé uniquement `DOIVENT` → `MUST` dans `openspec/specs/component-model/spec.md:108`, avec les vérifications ciblées, sans autre correction. Codex a réalisé cette correction directement dans le précédent échange, hors du RUN OpenCode/CAB clôturé. L'état actuel du fichier et la comparaison avec son état avant correction confirment ce seul remplacement. Le SHA-256 après correction est `1a3eb92f8e1694a7c312df750cf7dba0722b40f0d9b55eedc81e6c8e0862deeb`.

L'actualisation documentaire présente concerne seulement le bilan RCAMP et ce rapport statistique. Aucun compteur du RUN initial n'est recalculé ou augmenté avec les actions de correction ou les amendements documentaires. Aucun nouveau mandat CAB, aucune nouvelle sonde et aucun réarmement du RUN initial ne sont attribués à ce suivi.

| Mesure du suivi correctif, séparée de l'audit initial | Valeur |
|---|---|
| Fichier de spécification corrigé | 1 — `/home/devops/datas/pixs/openspec/specs/component-model/spec.md` |
| Remplacement textuel autorisé et observé | 1 — `DOIVENT` → `MUST`, sans autre différence |
| Rapports concernés par cette actualisation | 2 — `REVALIDATION.md` et `STATISTIQUES.md` |
| Agent ayant réalisé la correction et les amendements | Codex, exécution directe ; modèle exact et effort non exposés : `N/A` |
| Durée, tokens, coût et variation de quota propres au suivi | `N/A` — absence de collecte bornée et attribuable à ce suivi |
| Sondes de ce suivi | `N/A` — non activées ; aucune reconstruction rétroactive |

#### Vérifications ciblées déjà observées

Les deux contrôles de la correction ont été exécutés avec succès dans le précédent échange. Les références de sorties et la commande OpenSpec complète figurent dans le bilan lié : `C1 / 98bbc6` et `C2 / 812248`. Leur heure exacte n'est pas exposée (`N/A`) ; la date de cette entrée est celle de l'actualisation documentaire. Ces contrôles ne sont pas rejoués pour l'amendement.

| Famille et libellé du contrôle | Nombre | Part des 2 contrôles | Réussis | Erreurs | Refus |
|---|---:|---:|---:|---:|---:|
| OpenSpec — validation stricte de component-model | 1 | 50,0 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Python — remplacement exact, UTF-8/LF, mots-clés et clauses | 1 | 50,0 % | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total du suivi correctif | 2 | 100,0 % | 2 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

La validation OpenSpec ciblée a retourné `exit 0`, `1/1` spécification valide et `issues: []`. Le contrôle Python a retourné `exit 0` : seul remplacement autorisé, absence de mots-clés français ou hybrides résiduels dans ce fichier, exigences et scénarios inchangés, UTF-8/LF préservés. Les `6` commandes natives, les `64` outils et le résultat `78/78` du canon décrits plus haut restent historiques et ne sont pas augmentés ni présentés comme rejoués après correction.

#### Évolution du bilan et conservation des inconnues

Un écart normatif prouvé sur un a été corrigé (`1/1`, soit `100,0 %` des écarts normatifs prouvés par l'audit initial). Ce taux ne mesure pas la conformité globale du change.

| Tâche | État conservé ou évolution tracée |
|---|---|
| 2.1 | `NON VÉRIFIABLE` inchangé : préimage historique toujours absente |
| 2.2 | Résidu `DOIVENT` corrigé ; volet frontend toujours non vérifiable ; aucune conformité globale de la tâche composite n'est déduite |
| 3.1 | `NON VÉRIFIABLE` inchangé : preuve de validation directe de l'archive toujours absente |

Les deux verdicts historiques non vérifiables des tâches 2.1 et 3.1 sont conservés : `2/2` (`100,0 %` de ces deux verdicts), soit `2/4` (`50,0 %`) des tâches historiques. Le bilan initial `1 CONFORME / 1 ÉCART / 2 NON VÉRIFIABLE / 0 NON APPLICABLE` demeure inchangé dans l'historique. Aucun nouveau total de conformité globale n'est calculé ; la limite frontend de 2.2 n'est pas levée par cette correction.

Le présent ajout est la seule actualisation de ce fichier statistique ; les autres artefacts de l'archive ne sont pas modifiés. Les empreintes et le gate du [checkpoint initial](../../../../output/rcamp/rcamp1-pixs-0b46eb1e9eee4dde/state.json) conservent leur portée historique. Aucun autre correctif, aucune coche, aucune synchronisation, aucune opération Git ni aucun réarchivage n'est attribué à ce suivi.


### Suivi post-clôture — preuves et reclassement de 3.1

Mise à jour documentaire : `2026-10-26T20:41:07+01:00` (Europe/Paris). Référence : `preuves-reclassement-31-2026-10-26`. Autorisation du développeur : maintenir 2.1 en `NON VÉRIFIABLE`, reclasser 3.1 en `ÉCART de validation` et conserver l'historique, sans correction ni réarchivage. Les preuves détaillées sont ajoutées au [bilan RCAMP](../../../../output/rcamp/rcamp1-pixs-0b46eb1e9eee4dde/REVALIDATION.md).

#### Conservation des mesures et attribution

Tout le contenu précédent, y compris le bilan initial et le suivi de la correction `DOIVENT` → `MUST`, est conservé. Le maintien de deux verdicts non vérifiables décrit l'état à la date de ce précédent suivi. Pour le suivi actuel, seule la tâche 3.1 est reclassée ; les compteurs, tokens, coûts, quotas, sondes, durées et décisions CAB de l'audit initial ne sont ni recalculés ni augmentés.

La recherche a été réalisée directement par Codex dans l'échange précédent, hors du RUN OpenCode/CAB clôturé. Ses résultats sont intégrés ici sans nouvelle exécution OpenSpec. Leur horodatage exact n'est pas exposé dans les sorties citées (`N/A`) ; la date ci-dessus est celle de l'amendement. Durée, tokens, coût et variation de quota attribuables à cette recherche : `N/A`, faute de collecte bornée. Aucun nouveau RUN, mandat CAB, gate ou archivage n'est déclaré pour cet amendement.

#### Preuves historiques partielles de 2.1

La comparaison porte sur les 56 spécifications de l'archive du 8 septembre et les 56 deltas de la migration du 10 septembre. Les empreintes des 112 fichiers comparés sont restées identiques pendant la recherche.

| Mesure comparative | Archive du 8 septembre | Migration du 10 septembre | Portée de la preuve |
|---|---:|---:|---|
| Capacités | 56 | 56 | Même ensemble |
| Exigences | 200 | 205 | Les 200 intitulés antérieurs sont retrouvés, aucun supprimé |
| Scénarios | 200 | 206 | Les 200 intitulés antérieurs sont retrouvés, aucun supprimé |

Les cinq exigences supplémentaires portent sur `dependencies`, `extension-contracts`, `frontend`, `modules` et `testing`. Six scénarios supplémentaires et des différences de prose sont constatés. Cette comparaison n'établit pas la préservation sémantique des 205 exigences : la source du 8 septembre n'est pas la préimage immédiate complète de la migration.

Le rapport historique du 10 septembre mentionne `add-frontend-submodularity` et déclare la migration valide. Cette attestation ne fournit pas la préimage manquante. **2.1 reste `NON VÉRIFIABLE`.** Il manque l'état daté du canon à 205 exigences immédiatement avant migration, avec les éléments frontend correspondants.

#### Résultats de validation de 3.1

L'API du validateur OpenSpec installé a été exécutée dans un processus Node doté uniquement d'autorisations de lecture ; `process.permission.has('fs.write')` a retourné `false`. Aucune copie de l'archive ni aucun réarchivage n'a été nécessaire. Les références des sorties de cet échange sont `0fe13d` et `700342`.

Le tableau suivant compte quatre volets distincts. Le canon est un volet portant sur 78 spécifications, pas une seule spécification. La confirmation du contrôle strict de proposition est rattachée au même volet, sans double comptage.

| Volet restitué | Part des 4 volets | Résultat observé | Conforme au contrôle | Écart de validation |
|---|---:|---|---:|---:|
| Deltas de l'archive — API stricte | 25,0 % | `valid: true`, aucun diagnostic ; 205 deltas lus | 1 (100,0 %) | 0 (0,0 %) |
| Canon — API stricte | 25,0 % | 78 spécifications sur 78 valides, aucun diagnostic | 1 (100,0 %) | 0 (0,0 %) |
| Proposition de l'archive — API standard | 25,0 % | `valid: false`, 1 erreur de volume | 0 (0,0 %) | 1 (100,0 %) |
| Proposition de l'archive — API stricte | 25,0 % | `valid: false`, même erreur de volume, confirmée | 0 (0,0 %) | 1 (100,0 %) |
| Total des volets distincts | 100,0 % | 4 volets, sans assimilation aux compteurs de commandes du RUN | 2 (50,0 %) | 2 (50,0 %) |

Diagnostic de proposition en standard et en strict : `ERROR`, chemin `deltas`, `Consider splitting changes with more than 10 deltas`. L'obstacle d'accès à la validation directe est levé, mais la proposition ne satisfait pas ce contrôle. **3.1 est reclassée en `ÉCART de validation`**, sans déclaration de conformité globale.

Le processus initial `0fe13d` a retourné le code 1. Le wrapper de confirmation `700342` a retourné le code 0 tout en affichant deux résultats `valid: false` ; ce code 0 n'est pas compté comme une réussite des validations de proposition. Les quatre volets ci-dessus ne sont pas quatre commandes ou quatre permissions CAB. Aucune statistique globale d'outils ou de commandes de la recherche n'est reconstituée.

#### Bilan du périmètre réexaminé

| Verdict actuel sur les deux tâches réexaminées | Tâche | Nombre | Part des 2 tâches |
|---|---|---:|---:|
| `NON VÉRIFIABLE` maintenu | 2.1 | 1 | 50,0 % |
| `ÉCART de validation` | 3.1 | 1 | 50,0 % |
| Total du périmètre réexaminé | 2.1 et 3.1 | 2 | 100,0 % |

Ce tableau complète les états précédents sans réécrire leurs totaux. Aucun nouveau total sur les quatre tâches n'est déduit : le constat historique de 1.1 et le suivi de 2.2 restent inchangés, y compris la limite frontend de 2.2. Le reclassement de 3.1 ne vaut pas autorisation de corriger ou découper la proposition.

Cette actualisation ajoute uniquement des entrées aux deux rapports. Les spécifications, les autres artefacts de l'archive et le [checkpoint initial](../../../../output/rcamp/rcamp1-pixs-0b46eb1e9eee4dde/state.json) ne sont pas modifiés. Aucune correction, synchronisation, coche de tâche, opération Git ou opération de réarchivage n'est effectuée.


### Suivi post-clôture — découpage appliqué en 21 lots

Mise à jour : `2026-10-26T20:28:25.273105+00:00`. Référence : `decoupage-rfc2119-21-lots-2026-10-26`. Autorisation explicite du développeur : découpage, sauvegarde, validations strictes, archive --skip-specs, canon et contenu normatif inchangés, rapports actualisés, 2.1 NON VÉRIFIABLE maintenu.

Tous les tableaux, totaux, erreurs, verdicts et mesures qui précèdent restent historiques et ne sont pas recalculés. Les métriques OpenCode de l'audit initial ne sont ni répliquées dans les nouveaux lots ni additionnées aux mesures de cette intervention directe de Codex. Les versions de cadrage et tâches initiales sont conservées dans la [sauvegarde intégrale](../../../../output/rfc2119-split/20261026T200749Z/archive-originale/STATISTIQUES.md). L'archive retirée est également conservée dans le dossier de travail.

#### Résultats effectifs et bornes

| Lot | Fichiers | Exigences | Scénarios | Proposition/deltas stricts publiés | Archivage natif |
|---|---:|---:|---:|---|---|
| [01](STATISTIQUES.md) | 4 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [02](../2026-10-26-adopt-rfc2119-keywords-02/STATISTIQUES.md) | 2 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [03](../2026-10-26-adopt-rfc2119-keywords-03/STATISTIQUES.md) | 2 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [04](../2026-10-26-adopt-rfc2119-keywords-04/STATISTIQUES.md) | 2 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [05](../2026-10-26-adopt-rfc2119-keywords-05/STATISTIQUES.md) | 2 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [06](../2026-10-26-adopt-rfc2119-keywords-06/STATISTIQUES.md) | 2 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [07](../2026-10-26-adopt-rfc2119-keywords-07/STATISTIQUES.md) | 2 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [08](../2026-10-26-adopt-rfc2119-keywords-08/STATISTIQUES.md) | 2 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [09](../2026-10-26-adopt-rfc2119-keywords-09/STATISTIQUES.md) | 3 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [10](../2026-10-26-adopt-rfc2119-keywords-10/STATISTIQUES.md) | 3 | 10 | 11 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [11](../2026-10-26-adopt-rfc2119-keywords-11/STATISTIQUES.md) | 3 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [12](../2026-10-26-adopt-rfc2119-keywords-12/STATISTIQUES.md) | 3 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [13](../2026-10-26-adopt-rfc2119-keywords-13/STATISTIQUES.md) | 3 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [14](../2026-10-26-adopt-rfc2119-keywords-14/STATISTIQUES.md) | 3 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [15](../2026-10-26-adopt-rfc2119-keywords-15/STATISTIQUES.md) | 3 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [16](../2026-10-26-adopt-rfc2119-keywords-16/STATISTIQUES.md) | 3 | 9 | 9 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [17](../2026-10-26-adopt-rfc2119-keywords-17/STATISTIQUES.md) | 3 | 9 | 9 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [18](../2026-10-26-adopt-rfc2119-keywords-18/STATISTIQUES.md) | 3 | 9 | 9 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [19](../2026-10-26-adopt-rfc2119-keywords-19/STATISTIQUES.md) | 3 | 9 | 9 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [20](../2026-10-26-adopt-rfc2119-keywords-20/STATISTIQUES.md) | 3 | 9 | 9 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| [21](../2026-10-26-adopt-rfc2119-keywords-21/STATISTIQUES.md) | 2 | 10 | 10 | 2/2 valides, 100,0 % | exit 0, specsUpdated=false |
| Total | 56 | 205 | 206 | 21/21 lots valides, 100,0 % | 21/21 archives réussies, 100,0 % |

Les 56 fichiers spec.md sont inchangés octet pour octet et affectés une seule fois. Le lot 01 garde quatre fichiers au chemin d'origine ; 52 sont transférés aux vingt autres archives. Les cadrages et tâches de validation des lots sont adaptés sans modifier le contenu normatif. Les trois tâches préalables de chaque lot sont cochées après preuve, soit 63/63 (100,0 %), sans reprendre comme validation actuelle les quatre anciennes coches sauvegardées.

Les [preuves API](../../../../output/rfc2119-split/20261026T200749Z/published-strict-api.json) valident strictement propositions et deltas après publication réelle : 21/21 lots conformes, sans diagnostic. Les séries avant archivage et après archivage isolé portent sur les mêmes lots et ne constituent pas 63 lots différents. Le canon réel est validé séparément : 78/78 spécifications valides et 78/78 empreintes inchangées (100,0 %).

Le profil [CLI historique strict](../../../../output/rfc2119-split/20261026T200749Z/prepared-historical-strict-cli.json) valide 21/21 lots (100,0 %). Le profil [comparé au canon actuel](../../../../output/rfc2119-split/20261026T200749Z/prepared-strict-cli.json) conserve 13/21 lots valides (61,9 %) et 8/21 refusés (38,1 %) sur des scénarios postérieurs à septembre. Ces échecs ne sont pas transformés en réussites ; l'archivage --skip-specs ne réapplique aucun ancien delta au canon.

#### Commandes, erreurs conservées et attribution

Le registre principal instrumente 27 commandes de contrôle et d'archivage : 25 avec code 0 et 2 avec code non nul. Ce registre ne représente pas l'intégralité des lectures et outils Codex ; leur nombre, messages, tokens, cache et coût sont N/A faute de collecte attribuable. Les argv complets et résultats se trouvent dans [state.json](../../../../output/rfc2119-split/20261026T200749Z/state.json) et les fichiers de preuve référencés.

| Sous-ensemble borné | Total | Code 0 | Code non nul |
|---|---:|---:|---:|
| Registre principal des contrôles et archivages | 27 | 25 (92,6 %) | 2 (7,4 %) |
| Tentatives d'archivage, sous-ensemble du registre | 22 | 21 (95,5 %) | 1 (4,5 %) |

Le code non nul de la CLI comparée au canon actuel traduit les écarts décrits ci-dessus. La tentative d'archivage sous le modèle de permissions Node a échoué avant déplacement parce que fsync est indisponible dans ce mode. La sonde Landlock, conservée à part du registre principal, a retourné 127 (fonction non supportée) sans lancer d'archivage. Les 21 archivages natifs sont ensuite réussis dans la préparation isolée avec --skip-specs, sans --no-validate, avec contrôle du canon après chaque commande. Les validateurs API sont exécutés sans droit fs.write. Aucun de ces échecs techniques n'est compté comme un refus du développeur.

Les vingt nouveaux rapports statistiques décrivent leur lot et renvoient ici pour les mesures communes. Les anciens compteurs et quotas restent uniques dans leur intervalle historique. Modèle exact, effort, TTMT et temps de service de Codex direct : N/A, non exposés ou non mesurés ; aucun agent orchestrateur distinct ni nouvelle sonde de modèle n'est introduit.

#### Durée et quota du suivi commun

| Durée suivie du découpage | Valeur |
|---|---|
| Début observé — avant première écriture, relevé initial | 2026-10-26T21:03:39+01:00 |
| Fin observée — après archivages, validations et bilan, avant statistiques | 2026-10-26T21:25:20+01:00 |
| Intervalle suivi, pauses et attentes incluses | 00 h 21 min 41 s |

Ces bornes couvrent le suivi instrumenté et non un horodatage de début de conversation non exposé. La rédaction ultérieure des statistiques est hors de cet intervalle.

| Mesure du quota Codex sur 7 jours | Horodatage | Utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — découpage | 2026-10-26 20:03:39 UTC à 2026-10-26 20:03:40 UTC | 100 % | 2026-11-02T06:01:55+00:00 |
| Après — archivages et contrôles finis | 2026-10-26 20:25:18 UTC à 2026-10-26 20:25:20 UTC | 100 % | 2026-11-02T06:01:55+00:00 |
| Différence après − avant | — | 0 points | — |

Fenêtre 10080 minutes ; comparabilité du compte et de la fenêtre vérifiée : true. Le quota est partagé : sa variation ne mesure pas une consommation exclusive de ce découpage. Une variation nulle ne prouve pas une absence de coût ni de consommation de crédits.

#### État actuel et conservation de l'historique

| Tâche | État dans la portée demandée |
|---|---|
| 2.1 | NON VÉRIFIABLE maintenu — préimage immédiate avant migration toujours absente |
| 3.1 | CONFORME — qualification structurelle historique des 21 lots, sans qualification de resynchronisation |

L'écart de volume de 3.1 est levé dans cette portée, sans conclure à la compatibilité d'une réapplication au canon actuel. Les anciennes valeurs 1 CONFORME / 1 ÉCART / 2 NON VÉRIFIABLE restent des constats historiques, pas un total courant recalculé. La limite frontend de 2.2 n'est pas réexaminée.

Le [bilan RCAMP](../../../../output/rcamp/rcamp1-pixs-0b46eb1e9eee4dde/REVALIDATION.md) et les rapports de lot tracent les contrôles et les limites. PROJECT.md et README.md sont actualisés sur l'inventaire courant conformément à la convention du projet : 186 archives, 107 changes actifs, 293 dossiers ; seuls 20 dossiers d'archive supplémentaires sont attribués à ce découpage. Ces nombres ne mesurent aucun avancement fonctionnel.

Aucune modification du canon ou du contenu normatif, aucune opération Git, aucun code ni état runtime modifié. Aucun outil de navigation web observé pendant ce découpage ; le transport du modèle n'est pas mesuré. Les preuves et sauvegardes sont conservées dans le dossier de travail ; aucun nouveau gate CAB n'est attribué à cette opération directe.
