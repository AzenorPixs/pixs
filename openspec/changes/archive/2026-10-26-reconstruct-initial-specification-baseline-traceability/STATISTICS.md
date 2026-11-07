# Statistiques — reconstruct-initial-specification-baseline-traceability

Archive : `2026-10-26-reconstruct-initial-specification-baseline-traceability`. Lot documentaire réalisé directement par Codex dans le chat `01a1794b-bc21-76c1-965d-a251b9ee5157`. Le RCAMP préparatoire est un audit distinct : ses agents, sondes, quotas et compteurs ne sont pas réaffectés à ce lot.

Ce rapport distingue les observations conservées de la réalisation initiale et les opérations enregistrées de la phase d’archivage. Il ne reconstitue pas des compteurs complets de messages, outils, tokens, cache ou coût Codex : ces mesures sont `N/A`, faute d’export exhaustif autorisé disponible. Les sondes périodiques sont non activées ; aucune mesure rétrospective n’est simulée.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — modèle exact non exposé | N/A | OpenAI | N/A | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Aucun agent distinct identifiable pour ce lot direct | N/A | N/A | N/A | N/A | N/A | N/A |

Un seul agent de réalisation est identifié pour ce lot. Les versions de l’agent et du modèle ainsi que le temps de génération ne sont pas exposés par la télémétrie utilisée. Les durées de commandes et la durée calendaire ne sont pas assimilées au temps de service d’un LLM.

## 1. Statistiques générales et décisions

Le développeur a autorisé la réalisation documentaire et la consultation Git, puis validé le lot et demandé son archivage avec statistiques, en conservant explicitement les réserves historiques et les points partiels. Ces décisions actuelles ne prouvent ni un accord de septembre ni l’arbitrage historique du remplacement d’un scénario. Aucun compteur complet de décisions ou de compactions n’est inventé : `N/A`.

| Indicateur | Effectif | Part et dénominateur |
| --- | --- | --- |
| Tâches de réalisation et vérification cochées | 14 | 100,0 % de 14 |
| Exigences historiques cartographiées | 300 | 49,6 % de 605 |
| Scénarios historiques cartographiés | 305 | 50,4 % de 605 |
| Total d’éléments historiques | 605 | 100 % |
| Blocs identiques à leur source définie | 603 | 99,7 % de 605 |
| Repliements de prose explicitement documentés | 2 | 0,3 % de 605 |

Les bordures blanches de séparation des blocs sont retirées avant leur comparaison. Les empreintes de fichiers complets sont conservées séparément. Les deux écarts documentaires ont été corrigés dans ce lot : matrice détaillée et réintégration dans l’agrégation des cinq exigences/cinq scénarios anciens d’audit et des cinq exigences/cinq scénarios anciens d’operations. Les totaux prouvés restent 300/305 ; l’archive de septembre n’est pas corrigée rétrospectivement.

| Résultat des sept points | Effectif | Part |
| --- | --- | --- |
| Levés sur le contenu historique | 3 | 42,9 % |
| Partiellement établis | 2 | 28,6 % |
| Historiquement non vérifiables | 2 | 28,6 % |
| Total examiné | 7 | 100 % |

| Point | Statut conservé | Limite ou preuve |
| --- | --- | --- |
| 1.3 | NON VÉRIFIABLE historique | Accord daté sur la matrice et les lots non retrouvé |
| 2.1 | LEVÉ sur le contenu historique | Aucun delta normatif résiduel de consolidation dans H1 |
| 2.2 | LEVÉ pour le portage H1 | Les évolutions du canon actuel ne sont pas prétendues identiques au comportement de septembre |
| 3.1 | PARTIEL | Sortie d’exécution historique non retrouvée ; outil déclaré v1.13 non réexécuté ; résultats actuels distingués |
| 3.2 | LEVÉ pour cette archive | Aucun élément attendu du bootstrap manquant dans H1 |
| 4.1 | PARTIEL | Conservation H1 prouvée ; remplacement ultérieur du scénario du Super Admin constaté sans référence d’arbitrage humain retrouvée |
| 4.2 | NON VÉRIFIABLE historique | Présentation et autorisation d’archivage de septembre non retrouvées |

Les quatorze coches attestent des vérifications réalisées, pas sept conformités intégrales. La section des sept conclusions a gardé la même empreinte pendant la préparation et après le déplacement. La validation et l’archivage actuels ne lèvent aucun des deux points partiels ni aucune des deux réserves historiques. Les pourcentages sont arrondis à une décimale ; leur somme affichée peut différer de 100 %.

## 2. Types de messages et d’outils

Les messages, parties, appels d’outils Codex et leurs terminaisons ne sont pas disponibles sous forme d’un export complet pour ce lot : `N/A`. Un appel abouti ne prouve pas une approbation manuelle spécifique. Les interventions ci-dessous sont couvertes par les demandes explicites du développeur ; aucun nouveau RUN CAB ou agent OpenCode n’a été lancé pour l’archivage.

| Registre observable | Succès/code 0 | Résultats non nuls | Total |
| --- | --- | --- | --- |
| Observations de réalisation initiale | 10 (76,9 %) | 3 (23,1 %) | 13 (100 %) |
| Commandes de la phase d’archivage | 7 (100 %) | 0 (0,0 %) | 7 (100 %) |

Les treize observations initiales comprennent onze commandes enregistrées et deux contrôles documentaires, sans représenter l’ensemble des appels d’outils. Elles conservent deux refus stricts et un arrêt conservatoire sur une dérive de l’annexe. Les sept commandes d’archivage comprennent six vérifications et une opération native d’archivage ; elles ont toutes terminé avec le code 0. Refus de permission et erreurs techniques : zéro dans ce seul registre de sept commandes, décompte exhaustif du lot `N/A`.

## 3. Fichiers modifiés

Neuf fichiers ont été déplacés par une seule opération native OpenSpec. Cinq gardent leur contenu de fin de réalisation ; quatre ont reçu des adaptations nécessaires à l’archivage. Le fichier statistique est ensuite créé comme dixième fichier de l’archive. Les interventions de contenu identifiées avant rédaction statistique sont six, réparties sur quatre fichiers ; il ne s’agit pas d’un décompte des appels système ou de toutes les écritures de la réalisation initiale.

| Chemin absolu | Interventions identifiées | Part des six | Objet |
| --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-reconstruct-initial-specification-baseline-traceability/verify_traceability.py | 1 | 16,7 % | Autorisée et constatée ; Résolution de la racine dans les deux emplacements |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-reconstruct-initial-specification-baseline-traceability/proposal.md | 1 | 16,7 % | Autorisée et constatée ; Autorisation actuelle d’archivage explicitée |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-reconstruct-initial-specification-baseline-traceability/design.md | 1 | 16,7 % | Autorisée et constatée ; Transition documentaire et maintien des réserves |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-reconstruct-initial-specification-baseline-traceability/VERIFICATIONS.md | 3 | 50,0 % | Autorisée et constatée ; Autorisation, liens déplacés, nouveaux résultats datés ; sept conclusions inchangées |
| Total avant statistiques | 6 | 100 % | Sur quatre fichiers distincts |

Création séparée après le relevé final : `/home/devops/datas/pixs/openspec/changes/archive/2026-10-26-reconstruct-initial-specification-baseline-traceability/STATISTIQUES.md`, une création autorisée, hors dénominateur des six interventions. Les neuf déplacements ne sont pas comptés comme neuf éditions de contenu. Les preuves techniques sous `/home/devops/datas/pixs/output/baseline-traceability/20261026-consolidate-initial-specification-baseline/archivage` sont produites ou complétées ; leur nombre total d’écritures est `N/A` (non instrumenté).

Les sept fichiers de l’archive historique cible et les 78 spécifications canoniques sont protégés par empreintes. La modification concurrente de l’archive auxiliaire du bootstrap reste signalée, sans restauration ni attribution à ce lot ; ses sources normatives sont lues dans Git H1. Aucune préservation globale de la copie de travail de cette annexe n’est affirmée.

## 4. Commandes

Les commandes exactes, horodatages, sorties et codes sont dans les JSON de la phase d’archivage. Les libellés suivants sont abrégés à moins de 100 caractères.

| Libellé de commande | Occurrences, dénominateur 7 | Code |
| --- | --- | --- |
| python3 -m py_compile verify_traceability.py | 1 (14,3 %) | 0 |
| python3 -B verify_traceability.py — dossier actif | 1 (14,3 %) | 0 |
| openspec validate — lot ciblé --type change --strict --json | 1 (14,3 %) | 0 |
| openspec archive — lot validé --yes --skip-specs --json | 1 (14,3 %) | 0 |
| python3 -B verify_traceability.py — dossier archivé | 1 (14,3 %) | 0 |
| openspec validate --all --json --no-interactive | 1 (14,3 %) | 0 |
| openspec validate --all --strict --json --no-interactive | 1 (14,3 %) | 0 |
| Total enregistré | 7 (100 %) | 7 codes 0 |

| Famille, phase d’archivage | Effectif | Part | Succès / refus de permission / erreur technique |
| --- | --- | --- | --- |
| Python | 3 | 42,9 % | 3 / 0 / 0 |
| OpenSpec validation | 3 | 42,9 % | 3 / 0 / 0 |
| OpenSpec archivage | 1 | 14,3 % | 1 / 0 / 0 |
| Total | 7 | 100 % | 7 / 0 / 0 |

Les consultations Git restent en lecture seule. Aucun commit, push ou changement de branche n’a été effectué. Aucune commande refusée par une permission n’est observée dans les registres de contrôle ; les refus stricts initiaux sont des résultats de validation, pas des refus de permission. Le nombre complet des commandes préparatoires, Git et scripts de collecte de toute la réalisation reste `N/A` ; les onze enregistrements initiaux ne sont pas substitués à ce total.

## 5. Accès web

Aucun outil de navigation ou recherche web n’a été utilisé pour ce lot ou cette phase : aucune URL visitée ou refusée n’est enregistrée. Les deux relevés de quota proviennent de l’outil natif ; ils ne sont pas comptés comme visites web.

| Accès web observés | Nombre | Taux sur ce domaine |
| --- | --- | --- |
| Approuvés et exécutés | 0 | N/A — dénominateur nul |
| Refusés | 0 | N/A — dénominateur nul |
| Erreurs | 0 | N/A — dénominateur nul |
| Total | 0 | N/A — dénominateur nul |

## 6. Synthèse globale

Archivage natif confirmé vers `2026-10-26-reconstruct-initial-specification-baseline-traceability`, code 0, `specsUpdated: false`. Le dossier actif a disparu et les neuf sources sont présentes dans l’archive. Le vérificateur reproduit les 605 éléments depuis son nouvel emplacement. La section des sept conclusions reste identique ; les réserves et points partiels ne sont pas convertis en conformités.

| Validation | Réalisation initiale, résultats conservés | Phase d’archivage, résultats nouveaux |
| --- | --- | --- |
| Lot ciblé strict | 1/1 | 1/1 avant déplacement |
| Copie isolée H1 standard | 77/77 | Non rejouée |
| Copie isolée H1 stricte | 75/77 : cinq avertissements de longueur dans deux capacités | Non rejouée ; résultat antérieur maintenu |
| Globale standard | 186/186 | 185/185 après déplacement |
| Globale stricte | 185/186 : refus extérieur au lot | 185/185 après déplacement |

Le succès strict courant ne prouve pas une exécution de septembre et n’annule aucun des refus datés de la réalisation initiale. Les versions historiques et actuelles de l’outil, le manque d’accords humains et le remplacement ultérieur du scénario du Super Admin restent des limites explicites.

| Durée de la session de codage | Valeur |
| --- | --- |
| Début global de la réalisation | N/A — préparation historique antérieure non horodatée exhaustivement |
| Première borne d’artefact conservée | 2026-10-26T19:04:13.754308+00:00 ; ne vaut pas début global |
| Fin — après archivage, avant rédaction statistique | 2026-10-26T20:56:49+01:00 |
| Durée globale de tout le lot, pauses incluses | N/A — borne initiale exhaustive absente |
| Début de l’intervalle mesuré d’archivage | 2026-10-26T20:46:22+01:00 |
| Durée mesurée de la phase d’archivage, pauses incluses | 00 h 10 min 27 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de réalisation du lot | N/A — relevé initial absent | N/A | N/A |
| Après — après archivage | 2026-10-26T20:56:49+01:00 | 100 % | 2026-11-02T07:01:55+01:00 |
| Différence globale après − avant | — | N/A — relevé initial absent | — |

| Sous-intervalle d’archivage mesuré | Horodatage | Quota utilisé |
| --- | --- | --- |
| Avant phase d’archivage | 2026-10-26T20:46:22+01:00 | 100 % |
| Après archivage | 2026-10-26T20:56:49+01:00 | 100 % |
| Différence dans ce seul intervalle | Même compte et même fenêtre vérifiés | 0 point |

Les quotas sont partagés par le compte : la variation ne lui est pas attribuée exclusivement. Une différence nulle peut refléter la précision ou le délai du compteur ; elle ne signifie pas zéro token ou zéro coût. Aucune conversion du quota en tokens ou en euros n’est effectuée.

| Opérations identifiées avant rédaction statistique | Effectif | Part de ce sous-total | Abouties / refusées / en erreur |
| --- | --- | --- | --- |
| Interventions de contenu, par fichier | 6 | 46,2 % | 6 / 0 / 0 |
| Commandes enregistrées | 7 | 53,8 % | 7 / 0 / 0 |
| Web externe | 0 | 0,0 % | N/A / N/A / N/A |
| Sous-total observable | 13 | 100 % | 13 / 0 / 0 |

Ce sous-total normalise des interventions de contenu et des commandes ; il n’est pas le nombre d’appels d’outils Codex. Les autres outils et les écritures de collecte ne sont pas intégralement instrumentés : total global exhaustif `N/A`. La création du présent rapport est distincte et exclue de l’intervalle de quota et de ce sous-total.

Les tokens, cache, coûts, temps de service, TTMT et débits du codeur restent `N/A` faute de télémétrie complète. Sondes périodiques non activées ; aucune sonde rétroactive ni mesure d’un autre agent n’est utilisée. Les compactions sont `N/A` (non collectées pour ce lot). Aucun test applicatif, accès PostgreSQL, navigateur ou déploiement n’est revendiqué. Aucun secret ni source exclue n’a été utilisé comme donnée statistique.

[Bilan et réserves](VERIFICATIONS.md) · [Matrice](conservation-matrix.md) · [Données](evidence.json) · [Preuves de réalisation](../../../../output/baseline-traceability/20261026-consolidate-initial-specification-baseline/controls-index.json) · [Preuves d’archivage](../../../../output/baseline-traceability/20261026-consolidate-initial-specification-baseline/archivage/state.json)
