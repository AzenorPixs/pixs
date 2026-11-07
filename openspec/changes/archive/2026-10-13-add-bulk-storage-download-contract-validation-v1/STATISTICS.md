# Statistiques — add-bulk-storage-download-contract-validation-v1

RUN : cismp-pixs-6d45ca1d322c4c05 ; sessions de codage : ses_ec90fea27ffeTiKiYls5ZanMOE, ses_ec902ec4dffex0xaimV94wBdEo ; orchestrateur : 01a1365a-a87a-7440-b950-98b968baed7b.

Archive vérifiée : /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-storage-download-contract-validation-v1. Périmètre : validation structurelle pure de DownloadPort ; ObjectStoragePort existant conservé, aucune référence temporaire émise ni nouvelle sémantique.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | Modèle N/A ; OpenCode 1.19.0 | opencode-go | high | 3.088 s | 303.070 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — identifiant exact du modèle non exposé | N/A | OpenAI | N/A | N/A | N/A | N/A |

Le modèle exact de Codex et la version du modèle Muse ne sont pas exposés par la télémétrie. Temps de service et dénominateur N/A : les bornes des messages englobent attentes MCP/outils et ne permettent pas d’isoler la génération. Aucune sonde de l’orchestrateur. Les messages de compactage natif sont comptés séparément ; leur niveau de raisonnement non exposé n’est pas attribué aux mandats métier, tous transmis avec high. Les TTMT/débits ci-dessus sont les moyennes arithmétiques des sondes natives valides du seul agent de codage, séparées de la production.

## 1. Statistiques générales et décisions

Durée calendaire : 01 h 04 min 49 s, pauses, attente de cohorte et tests inclus. Début natif 2026-10-13T22:24:26.328000+02:00 ; fin après archive et sonde finale 2026-10-13T23:29:16+02:00.

| Mesure | Valeur |
| --- | --- |
| Messages natifs | 177 |
| Parties natives | 652 |
| Appels d’outils natifs | 98 |
| Réussis / autorisés | 95 (96.9 %) |
| Refus explicites | 0 (0.0 %) |
| Erreurs techniques | 3 (3.1 %) |
| Total | 98 (100 %) |
| Tokens entrée | 832346 |
| Tokens sortie | 44514 |
| Tokens raisonnement | 16202 |
| Cache lu | 6814147 |
| Cache écrit | 0 |
| Coût natif source (USD) | 0.109006 |
| Parties de compactage des sessions de codage | 1 |

Mandats opérationnels clôturés du change : 21 ; 20 complets avec preuves et 1 partiel réconcilié. Décisions explicites corrélées de Codex ; les permissions restent unitaires et consommables une fois. Une permission supplémentaire a été refusée après interruption de la session ; son outil natif est classé en erreur technique lorsque la télémétrie indique un abandon. Un outil réussi peut être autorisé automatiquement en lecture ou MCP : réussite ne signifie pas approbation manuelle.

Incident de ce change : l'ancienne session a tenté plusieurs éditions sous le même mandat. Seul l'export a été ajouté ; la permission supplémentaire a été refusée et l'outil interrompu. Le fichier partiel a été relu et son effet exact vérifié, puis le même job a été transféré par récupération prepare/complete avec prévol neuf. Le contenu final a été écrit une seule fois sous mandat neuf, sans effet hors périmètre. Le refus initial de transmission d'ACSP par la revue automatique a été levé après présentation des autorisations explicites ; aucune transmission refusée n'a été exécutée.

Résultat : validateur de téléchargement ajouté avec deux constantes et export ; quatre nouveaux tests comportementaux. 90 tests Bulk locaux puis 93 tests combinés réussis ; ces 93 cas incluent les 90 déjà vérifiés et les 3 cas du vocabulaire frontend, deux compilations Python exit0 et validations strictes du change sans issue. Référence commune : 79 éléments valides ; les avertissements historiques de longueur de bulk-operations restent qualifiés séparément. Validation globale exécutée sans --strict ; aucune réussite stricte globale revendiquée.

Initialisation avortée antérieure hors intervalle : session ses_ec93fe6d7ffe3x81TTnvguzYOa, sans création de change ni modification de code. Sa demande orpheline a été annulée avant la reprise ; ses métriques ne sont pas reconstituées dans les totaux de production ci-dessous.

Deux erreurs de lecture sont conservées dans les totaux : proposal.md était encore absent avant sa création ; une tentative d'outil a ensuite été bloquée par le verrou qui ne laissait disponible que broker_readiness. Aucune de ces tentatives n'a lu de fichier hors périmètre ni produit d'écriture. Les libellés de commandes tronqués identiques sont regroupés en additionnant leurs occurrences.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| assistant | 129 | 72.9 % |
| user | 48 | 27.1 % |
| Total | 177 | 100 % |

Le rôle user désigne les mandats et relances de l’orchestrateur, pas autant de messages humains.

| Partie | Nombre | Part |
| --- | --- | --- |
| compaction | 1 | 0.2 % |
| reasoning | 137 | 21.0 % |
| step-finish | 128 | 19.6 % |
| step-start | 129 | 19.8 % |
| text | 159 | 24.4 % |
| tool | 98 | 15.0 % |
| Total | 652 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| absent | 1 | 0.8 % |
| stop | 45 | 34.9 % |
| tool-calls | 83 | 64.3 % |
| Total | 129 | 100 % |

| Type | Total | Part | Réussi / autorisé | Taux | Refusé | Taux | Erreur technique | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bash | 12 | 12.2 % | 12 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 25 | 25.5 % | 25 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_get_approval | 2 | 2.0 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_list_pending | 1 | 1.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 21 | 21.4 % | 21 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| edit | 2 | 2.0 % | 1 | 50.0 % | 0 | 0.0 % | 1 | 50.0 % |
| grep | 6 | 6.1 % | 6 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 21 | 21.4 % | 19 | 90.5 % | 0 | 0.0 % | 2 | 9.5 % |
| write | 8 | 8.2 % | 8 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 98 | 100 % | 95 | 96.9 % | 0 | 0.0 % | 3 | 3.1 % |

## 3. Fichiers modifiés

Les effectifs sont des tentatives d’écriture natives, pas un nombre de lignes. Le total de ce tableau couvre seulement write/edit, afin de ne pas compter deux fois les créations ou déplacements réalisés par OpenSpec.

| Chemin absolu de la tentative | Total | Part | Approuvé/exécuté | Taux | Refusé | Taux | Erreur | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-bulk-storage-download-contract-validation-v1/design.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-storage-download-contract-validation-v1/proposal.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-storage-download-contract-validation-v1/specs/bulk-operations/spec.md | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-storage-download-contract-validation-v1/tasks.md | 3 | 30.0 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/bulk_trusted_ports.py | 3 | 30.0 % | 2 | 66.7 % | 0 | 0.0 % | 1 | 33.3 % |
| /home/devops/datas/pixs/tests/unit/test_bulk_trusted_ports.py | 1 | 10.0 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 10 | 100 % | 9 | 90.0 % | 0 | 0.0 % | 1 | 10.0 % |

Les quatre artefacts proposal.md, design.md, tasks.md et specs/bulk-operations/spec.md ont été déplacés dans /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-storage-download-contract-validation-v1. Le seul .openspec.yaml initial a été créé par la commande new change puis archivé ; cette action est classée dans les commandes. Le présent STATISTIQUES.md est rédigé après la borne finale et son écriture est hors des totaux de production.

Empreintes/revue : fonctions et classes préexistantes de la source préservées ; anciens tests conservés sauf la liste d’exports attendus explicitement étendue ; source et tests conformes aux textes approuvés ; anciens octets reconstruits correspondent aux empreintes initiales ; neuf cadrages/canons contrôlés inchangés ; UTF-8/LF ; aucune dépendance ajoutée. L’incertitude de provenance Git demeure, Git étant interdit d’inspection.

## 4. Commandes

| Type | Total | Part | Réussi / autorisé | Taux | Refusé | Taux | Erreur technique | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Autre | 2 | 16.7 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Compilation Python | 2 | 16.7 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec | 6 | 50.0 % | 6 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unittest | 2 | 16.7 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 12 | 100 % | 12 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

| Type | Total | Part | Réussi / autorisé | Taux | Refusé | Taux | Erreur technique | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/.local/npm/bin/openspec archive add-bulk-storage-download-contract-validation-v1 --yes… | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/.local/npm/bin/openspec new change add-bulk-storage-download-contract-validation-v1 | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/.local/npm/bin/openspec validate --all --json | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/.local/npm/bin/openspec validate add-bulk-storage-download-contract-validation-v1 --st… | 3 | 25.0 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_trusted_ports.py | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_trusted_ports.py | 1 | 8.3 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/pytho… | 2 | 16.7 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /usr/bin/true | 2 | 16.7 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 12 | 100 % | 12 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes natives refusées : aucune. Une permission supplémentaire d’édition a été refusée séparément. Les compilations, tests et validations ont réellement été exécutés ; l’archivage unique a utilisé --yes --skip-specs --json avec exit0 et specsUpdated=false. Aucune permission consommée n’a été réutilisée.

## 5. Accès web

| Type | Total | Part | Réussi / autorisé | Taux | Refusé | Taux | Erreur technique | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Total | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucun outil web invoqué et aucune URL visitée ou refusée par ces outils. Les accès HTTP locaux de pilotage et les appels fournisseur des sondes sont des canaux de contrôle séparés, pas des visites web de l’agent dans cette session.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début natif | 2026-10-13T22:24:26.328000+02:00 |
| Fin — après archivage | 2026-10-13T23:29:16+02:00 |
| Durée globale (pauses et attentes incluses) | 01 h 04 min 49 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — avant première écriture | 2026-10-13T22:26:31.279860+02:00 | 9 % | 2026-10-20T06:59:31+02:00 |
| Après — après archive et sonde finale | 2026-10-13T21:29:16+00:00 | 10 % | 2026-10-20T06:59:31+02:00 |
| Différence après − avant | — | 1 point(s) | — |

Fenêtre codex 10080 minutes, même réinitialisation. Le relevé initial précède la première écriture ; les premières lectures préparatoires avaient déjà commencé. Les quotas sont partagés par le compte et incluent notamment le RUN concurrent : variation de compte uniquement, aucune attribution exclusive, aucune conversion en tokens/euros. Une différence nulle peut refléter précision/délai de compteur.

| Type | Total | Part | Réussi / autorisé | Taux | Refusé | Taux | Erreur technique | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Autres outils (lecture, recherche, MCP) | 76 | 77.6 % | 74 | 97.4 % | 0 | 0.0 % | 2 | 2.6 % |
| Commandes | 12 | 12.2 % | 12 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Fichiers | 10 | 10.2 % | 9 | 90.0 % | 0 | 0.0 % | 1 | 10.0 % |
| Total | 98 | 100 % | 95 | 96.9 % | 0 | 0.0 % | 3 | 3.1 % |

Sondes séparées de la production : 3 prévues, 2 réussies dans la cadence, 0 échouées, 1 manquées ; 1 mesure(s) complémentaire(s) tardive(s), horodatée(s) réellement et incluse(s) dans les moyennes si valide(s). Prompt fixe de 80 lignes ; sessions jetables sans outil, fichier ni accès réseau propre à la sonde ; configuration Muse/opencode-go/high observée.

| Position | Horodatage Paris | TTMT (s) | Tokens/s | Tokens sortie | Durée (s) | Statut |
| --- | --- | --- | --- | --- | --- | --- |
| début | 2026-10-13T22:26:34.462146+02:00 | 5.753 | 186.718 | 822 | 10.186 | Réussie |
| intermédiaire tardive, échéance +30 min manquée | 2026-10-13T22:59:42.768778+02:00 | 1.247 | 495.743 | 810 | 2.926 | Réussie |
| fin | 2026-10-13T23:23:25.116899+02:00 | 2.264 | 226.750 | 829 | 5.938 | Réussie |

TTMT min/max : 1.247/5.753 s ; débit min/max : 186.718/495.743 tokens/s. Surcharge sondes : 2461 tokens de sortie, 19.049 s de durée mesurée ; coût N/A, non conservé. Débit = tokens réels natifs / intervalle SSE entre premier et dernier delta ; aucune approximation par fragments. Les mesures tardives ne remplacent pas les échéances manquées.

Bilan : tests applicables réussis ; PostgreSQL et navigateurs sans objet pour ce validateur pur ; les trois tests unitaires du vocabulaire frontend sont inclus dans le contrôle combiné, sans validation visuelle ni routage ; archive prouvée et canons préservés ; publication de ce rapport à vérifier sous mandat distinct ; Git non inspecté, aucun commit/push ; aucune référence de téléchargement émise ni effet externe ; aucun secret exposé ou ajouté aux sources/rapport. La livraison de ce lot ne termine pas le cycle global CISMP. Les pourcentages sont arrondis à une décimale : de légers écarts de somme sont possibles ; les effectifs entiers et totaux croisés sont exacts.
