# STATISTIQUES.md — revalidation `2026-09-16-consolidate-initial-specification-baseline` — création lors de la revalidation

Création lors de la revalidation RUN `rcamp2-pixs-01a1794bbc21`, distincte des données historiques. Historique d’implémentation : `N/A` sans session historique autorisée. Photographie figée avant rédaction/écriture statistiques, pas compteurs de clôture futurs. Session OpenCode principale seule ; outils/messages Codex orchestrateur non disponibles complètement : `N/A`, aucune extrapolation. Sondes dédiées séparées production. Mesures réservation occupé/inactif ne sont pas temps modèle ; temps de service `N/A`. Version exacte LLM non exposée : `N/A`. Agent OpenCode `1.19.4` noté hors colonne version LLM.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A | opencode-go | high | 2,343 s | 191,9 tok/s | N/A (absence télémétrie temps génération) |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex (modèle exact non exposé) | N/A | OpenAI | N/A | N/A | N/A | N/A |

## 1. Statistiques générales et décisions

- Cible : `openspec/changes/archive/2026-09-16-consolidate-initial-specification-baseline`
- RUN `rcamp2-pixs-01a1794bbc21`, contextId `1318`, reservation_version `1323`, phase `REPORT`
- Rapport : `/home/devops/datas/pixs/output/rcamp/rcamp2-pixs-01a1794bbc21/REVALIDATION.md`
- Statistiques : `/home/devops/datas/pixs/openspec/changes/archive/2026-09-16-consolidate-initial-specification-baseline/STATISTIQUES.md`
- Publication : transaction `rcamp2-report-publication-20261026`, referenceVersion `86`, version `1323`, inputDigest `79d95d292b4bed4d24c2ca3b1964bdd4529776ece82ff22190b748054a04f60d`, evidenceDigest `80894a977546a3acc75dc4836e67f8889e35683aa5b1cd32dd563fe47d4df5e6`, revisions `file:output/rcamp/rcamp2-pixs-01a1794bbc21: 10550`
- Verdicts audit (9, 100 %) : `CONFORME 0 (0,0 %)`, `ÉCART 2 (22,2 %)`, `NON VÉRIFIABLE 7 (77,8 %)`, `NON APPLICABLE 0 (0,0 %)`
- Matrice historique : `277+1+1+4+7=290` vs `300` annoncé (manque `10`), `280+1+1+4+9=295` vs `305` annoncé (manque `10`), capacités `72+4=76` cohérent ; pas régression actuelle
- Actuels DOC-01 : `78 spec.md`, `859 exigences`, `1064 scénarios` ; 5 références présentes ; 6 artefacts UTF-8/LF
- OS-01 : sortie `1`, `184 passés, 1 refusé / 185`, seul refus `add-pa-system-session-lifecycle` 7 avertissements hors archive ; ne valide pas archive
- Archivage : sans objet, change déjà archivé ; Git : aucune opération ; compressions : `0` observée, `N/A` historique justifié (sans invention)
- CAB : `5` décisions (100 %) dont `approuvée 4 (80,0 %)`, `rejetée 1 (20,0 %)` pour `commands[]` omis, `needs_clarification 0`, `en attente 0`, `once 4` ; sans double compte des refus natifs `2`
- HTTP techniques `3`, distincts permissions : `resource-revision-stale 1`, `run-not-quiescent 1`, `access-operation-not-prepared 1`
- Gate terminal : non déclaré validé ; libération : non déclarée réussie ; preuves finales dans état
- Messages session principale : `utilisateur 30`, `assistant 66`, total `96 (100 %)` dont `utilisateur 31,2 %`, `assistant 68,8 %`
- Tokens session principale : entrée `909076`, sortie `27439`, raisonnement `15010`, cache lecture `10255665`, cache écriture `0`, coût natif `0,11990873 USD`
- Liens : [Rapport](../../../../output/rcamp/rcamp2-pixs-01a1794bbc21/REVALIDATION.md) et [Checkpoint](../../../../output/rcamp/rcamp2-pixs-01a1794bbc21/state.json)

## 2. Types de messages et d’outils

Outils natifs total `55 (100 %)` dont `aboutis 52 (94,5 %)`, `refus 2 (3,6 %)`, `erreur technique 1 (1,8 %)` ; `2` lectures refusées avant effet pendant remise en état ; `1` écriture sans arguments/contenu rejetée par schéma AVANT permission, sans chemin ni effet, puis 1 écriture valide. Aboutissement outil ne prouve ni approbation manuelle ni test passé. Décisions CAB non double comptées dans appels outils.

| Outil | Aboutis | Refus | Erreur | Total (dénominateur 55) | Taux ligne sur son dénominateur |
|---|---|---|---|---|---|
| cgpt-validation_broker_readiness | 11 | 0 | 0 | 11 (20,0 %) | 100,0 % aboutis |
| cgpt-validation_request_validation | 5 | 0 | 0 | 5 (9,1 %) | 100,0 % transport |
| bash | 3 | 0 | 0 | 3 (5,5 %) | 100,0 % transport ; dont 1 contrôle sortie 1 (succès transport ≠ succès test) |
| read | 29 | 2 | 0 | 31 (56,4 %) | 93,5 % aboutis, 6,5 % refus |
| glob | 3 | 0 | 0 | 3 (5,5 %) | 100,0 % aboutis |
| write | 1 | 0 | 1 | 2 (3,6 %) | 50,0 % aboutis, 50,0 % erreur schéma sans cible |
| Total | 52 | 2 | 1 | 55 (100 %) | 94,5 % / 3,6 % / 1,8 % |

## 3. Fichiers modifiés

Aucune modification code/tests/specs/cadrages par le RUN. Création présent `STATISTIQUES.md` exclue photographie mais fichier livré distinct. Checkpoint orchestrateur réellement mis à jour, nombre écritures `N/A` (non collecté), non doublonné dans statistiques natives. Relevé DEVOPS 16:53:15Z → 18:00:35Z et rubrique OpenSSH/SSHPASS retirée : changement concurrent extérieur au RUN, chemins/versions Python et OpenSpec relus identiques, aucune restauration.

| Chemin absolu | Écritures abouties | Part ligne |
|---|---|---|
| /home/devops/datas/pixs/output/rcamp/rcamp2-pixs-01a1794bbc21/REVALIDATION.md | 1 | 100,0 % (dénominateur 1) |

Appel écriture invalide `1` sans chemin, erreur technique, non attribué à un fichier.

## 4. Commandes

`3` commandes (100 %), `2` contrôles audit (`1` succès / `1` refus strict global), aucun test fonctionnel applicable, aucune commande refusée. Voir état pour heredoc exact. Transports `3` aboutis.

| Libellé (≤100 car.) | Effectif (dénominateur 3) | Résultat commande |
|---|---|---|
| /usr/bin/true (test CAB) | 1 (33,3 %) | sortie 0 |
| heredoc python3 constat conservation | 1 (33,3 %) | sortie 0 DOC-01 |
| openspec validate --all --strict | 1 (33,3 %) | sortie 1 OS-01 (184/185, 7 avertissements hors archive) |
| Total | 3 (100 %) | 0, 0, 1 |

## 5. Accès web

Outil web `0`, aucune URL visitée. API locales pilotage non comptées comme visites web, nombre complet `N/A`. Générations fournisseur hors visites web.

| Domaine | Nombre | Taux (dénominateur 0) |
|---|---|---|
| URLs visitées | 0 | N/A (dénominateur 0, ni 0 % ni 100 % inventés) |
| Total web | 0 | N/A |

## 6. Synthèse globale

Revalidation documentaire complète périmètre autorisé : `9` tâches dont `2 ÉCART (22,2 %)`, `7 NON VÉRIFIABLE (77,8 %)` ; `ÉCART`/`NON VÉRIFIABLE` ne bloquent pas clôture audit. Sommes matrice `290/295` vs `300/305` écart `10/10` constaté, pas régression `78/859/1064`. Contrôles `DOC-01` succès, `OS-01` refus global hors archive distingué. Intégrité `90/91` après contrôles avant statistique, `DEVOPS.md` concurrent explicité, aucun fichier restauré.

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-10-26T18:44:22.422000+01:00 |
| Fin — archivage sans objet | 2026-10-26T19:17:44+01:00 |
| Durée globale (pauses et attentes incluses) | 00h33min21,578s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | N/A (conservation séparée 17:50:30Z, non lecture) | 89 % | 2026-11-02T07:01:55+01:00 (fenêtre 10080 min) |
| Après — fin des travaux (archivage sans objet) | 2026-10-26T19:17:44+01:00 (18:17:44Z) | 97 % | même fenêtre vérifiée |
| Différence après − avant | — | +8 points partagés, hors attribution exclusive | — |

| Domaine (dénominateur 55) | Effectif / part du 55 | Aboutis / taux domaine | Refus / taux domaine | Erreur / taux domaine |
|---|---|---|---|---|
| Écritures | 2 (3,6 %) | 1 / 50,0 % | 0 / 0,0 % | 1 / 50,0 % |
| Lectures/recherches | 34 (61,8 %) | 32 / 94,1 % | 2 / 5,9 % | 0 / 0,0 % |
| Commandes | 3 (5,5 %) | 3 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| MCP | 16 (29,1 %) | 16 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| Web | 0 (0,0 %) | N/A | N/A | N/A |
| Total | 55 (100 %) | 52 (94,5 %) | 2 (3,6 %) | 1 (1,8 %) |

Sondes dédiées séparées production : prévues `2`, réussies `2 (100,0 %)`, échouées `0`, manquées `0` ; aucune `+30 min` venue à échéance avant fin `17:50:30→18:17:44`, finale `18:14:48` ; moyennes TTMT `2,343 s`, débit `191,9 tok/s`, surcoût `2864` tokens, `19,949 s` ; débits calculés entre premier/dernier événement SSE, pas débit PLLM request_average ; 2 protocoles différents. Détail sondes : début `2026-10-26T17:50:30.531802+00:00`, modèle `muse-spark-1.3-contributor`, fournisseur `opencode-go`, raisonnement `high`, TTMT `2,471 s`, `167,5 tok/s`, sortie `1441`, réussie ; fin `2026-10-26T18:14:48.782663+00:00`, mêmes modèle/fournisseur/raisonnement, TTMT `2,214 s`, `216,2 tok/s`, sortie `1423`, réussie. Gate et libération non déclarés ; preuves finales dans état. Liens : [Rapport](../../../../output/rcamp/rcamp2-pixs-01a1794bbc21/REVALIDATION.md) et [Checkpoint](../../../../output/rcamp/rcamp2-pixs-01a1794bbc21/state.json).
