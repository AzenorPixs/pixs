# Statistiques — add-bulk-publisher-contract-validation-v1

RUN : cismp-pixs-6d45ca1d322c4c05 ; session de codage : ses_ec987546bffeW1zaGiIbavHmuG ; orchestrateur : 01a1365a-a87a-7440-b950-98b968baed7b.

Archive vérifiée : /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-publisher-contract-validation-v1. Périmètre : validation pure de PublisherPort, sans émission ni nouvelle sémantique runtime.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | Modèle N/A ; OpenCode 1.19.0 | opencode-go | high | 2.609 s | 149.160 | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex — identifiant exact du modèle non exposé | N/A | OpenAI | N/A | N/A | N/A | N/A |

Le modèle exact de Codex et la version du modèle Muse ne sont pas exposés par la télémétrie. Temps de service et dénominateur N/A : les bornes des messages englobent attentes MCP/outils et ne permettent pas d’isoler la génération. Aucune sonde de l’orchestrateur. Les TTMT/débits ci-dessus sont les moyennes arithmétiques des sondes natives valides du seul agent de codage, séparées de la production.

## 1. Statistiques générales et décisions

Durée calendaire : 00 h 51 min 34 s, pauses, attente de cohorte et tests inclus. Début natif 2026-10-13T20:14:00.340000+02:00 ; fin après archive et sonde finale 2026-10-13T21:05:34.767006+02:00.

| Mesure | Valeur |
| --- | --- |
| Messages natifs | 201 |
| Parties natives | 792 |
| Appels d’outils natifs | 153 |
| Réussis / autorisés | 152 (99.3 %) |
| Refus explicites | 0 (0.0 %) |
| Erreurs techniques | 1 (0.7 %) |
| Total | 153 (100 %) |
| Tokens entrée (champ natif input, cache séparé) | 1118573 |
| Tokens sortie | 50087 |
| Tokens raisonnement | 8690 |
| Cache lu | 28430021 |
| Cache écrit | 0 |
| Coût natif source (USD) | 0.180473 |
| Parties compaction du master | 0 |

Décisions opérationnelles Codex de ce change : 18 mandats unitaires approuvés et exécutés, 100.0 % ; aucun mandat de ce change refusé. Chaque permission native est once ; le gate CAB vérifiera leur consommation. Un outil réussi peut être autorisé automatiquement (lecture/MCP) : réussite ne signifie pas approbation manuelle. Un délai MCP est une erreur technique même si le polling de la même approbation réussit ensuite.

Incidents de démarrage séparés : un prévol initial invalide faute de once a été réconcilié par recover/prepare/complete avant ce change, sans effet métier ; une demande non exécutée a été annulée. Un refus de revue automatique de la création OpenSpec a été levé après vérification de la délégation AGENTS/CISMP/SPCMP ; aucun contournement ni effet de cette tentative refusée. Ces incidents ne sont pas ajoutés artificiellement aux totaux natifs de ce change.

Résultat : validateur ajouté avec deux constantes et export ; quatre nouveaux tests comportementaux. 57 tests passés, deux py_compile exit0, validations strictes du change sans issue. Référence commune : 79 éléments valides et les trois seuls WARNING historiques de longueur dans bulk-operations (requirements[6], requirements[10], requirements[13]). Validation globale exécutée sans --strict ; aucune réussite strict globale revendiquée.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| assistant | 155 | 77.1 % |
| user | 46 | 22.9 % |
| Total | 201 | 100 % |

Le rôle user désigne les mandats et relances de l’orchestrateur, pas autant de messages humains.

| Partie | Nombre | Part |
| --- | --- | --- |
| reasoning | 158 | 19.9 % |
| step-finish | 155 | 19.6 % |
| step-start | 155 | 19.6 % |
| text | 171 | 21.6 % |
| tool | 153 | 19.3 % |
| Total | 792 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| stop | 46 | 29.7 % |
| tool-calls | 109 | 70.3 % |
| Total | 155 | 100 % |

| Type | Total | Part | Réussi / autorisé | Taux | Refusé | Taux | Erreur technique | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bash | 9 | 5.9 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_health | 1 | 0.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_broker_readiness | 26 | 17.0 % | 26 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_list_pending | 25 | 16.3 % | 25 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_poll_approval | 1 | 0.7 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| cgpt-validation_request_validation | 18 | 11.8 % | 17 | 94.4 % | 0 | 0.0 % | 1 | 5.6 % |
| glob | 11 | 7.2 % | 11 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| grep | 5 | 3.3 % | 5 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| read | 48 | 31.4 % | 48 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| write | 9 | 5.9 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 153 | 100 % | 152 | 99.3 % | 0 | 0.0 % | 1 | 0.7 % |

## 3. Fichiers modifiés

Les effectifs sont des tentatives d’écriture natives, pas un nombre de lignes. Le total de ce tableau couvre seulement write/edit, afin de ne pas compter deux fois les créations ou déplacements réalisés par OpenSpec.

| Chemin absolu de la tentative | Total | Part | Approuvé/exécuté | Taux | Refusé | Taux | Erreur | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-bulk-publisher-contract-validation-v1/design.md | 2 | 22.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-publisher-contract-validation-v1/proposal.md | 2 | 22.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-publisher-contract-validation-v1/specs/bulk-operations/spec.md | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/add-bulk-publisher-contract-validation-v1/tasks.md | 2 | 22.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/src/pixs/backend/bulk_trusted_ports.py | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_bulk_trusted_ports.py | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 9 | 100 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Les quatre artefacts proposal.md, design.md, tasks.md et specs/bulk-operations/spec.md ont été déplacés dans /home/devops/datas/pixs/openspec/changes/archive/2026-10-13-add-bulk-publisher-contract-validation-v1. Le seul .openspec.yaml initial a été créé par la commande new change puis archivé ; cette action est classée dans les commandes. Le présent STATISTIQUES.md est rédigé après la borne finale et son écriture est hors des totaux de production.

Empreintes/revue : fonctions et classes préexistantes identiques dans l’AST ; source et tests conformes aux textes approuvés ; anciens octets reconstruits correspondent aux empreintes initiales ; neuf cadrages/canons contrôlés inchangés ; UTF-8/LF ; aucune dépendance ajoutée. L’incertitude de provenance Git demeure, Git étant interdit d’inspection.

## 4. Commandes

| Type | Total | Part | Réussi / autorisé | Taux | Refusé | Taux | Erreur technique | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Compilation Python | 2 | 22.2 % | 2 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| OpenSpec | 6 | 66.7 % | 6 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Tests unittest | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 9 | 100 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

| Type | Total | Part | Réussi / autorisé | Taux | Refusé | Taux | Erreur technique | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/devops/.local/npm/bin/openspec archive add-bulk-publisher-contract-validation-v1 --yes --skip… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/.local/npm/bin/openspec new change add-bulk-publisher-contract-validation-v1 | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/.local/npm/bin/openspec validate --all --json | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/.local/npm/bin/openspec validate add-bulk-publisher-contract-validation-v1 --strict --… | 3 | 33.3 % | 3 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/bulk_trusted_ports.py | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile tests/unit/test_bulk_trusted_ports.py | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| /usr/bin/env PYTHONPATH=src:tests /home/devops/datas/pixs/.venv/bin/python3 -m unittest unit.test_b… | 1 | 11.1 % | 1 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 9 | 100 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |

Commandes refusées : aucune dans l’historique natif du change. Les compilations, tests et validations ont réellement été exécutés avec leur code natif ; l’archivage unique a utilisé --yes --skip-specs --json, exit0, specsUpdated=false. Aucun rejeu d’une permission consommée.

## 5. Accès web

| Type | Total | Part | Réussi / autorisé | Taux | Refusé | Taux | Erreur technique | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Total | 0 | N/A | 0 | N/A | 0 | N/A | 0 | N/A |

Aucun outil web invoqué et aucune URL visitée ou refusée par ces outils. Les accès HTTP locaux de pilotage et les appels fournisseur des sondes sont des canaux de contrôle séparés, pas des visites web de l’agent dans cette session.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début natif | 2026-10-13T20:14:00.340000+02:00 |
| Fin — après archivage | 2026-10-13T21:05:34.767006+02:00 |
| Durée globale (pauses et attentes incluses) | 00 h 51 min 34 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — avant première écriture | 2026-10-13T20:14:39.904764+02:00 | 7 % | 2026-10-20T06:59:31+02:00 |
| Après — après archive et sonde finale | 2026-10-13T21:05:34.767006+02:00 | 8 % | 2026-10-20T06:59:31+02:00 |
| Différence après − avant | — | 1 point(s) | — |

Fenêtre codex 10080 minutes, même réinitialisation. Le relevé initial précède la première écriture ; les premières lectures préparatoires avaient déjà commencé. Les quotas sont partagés par le compte et incluent notamment le RUN concurrent : variation de compte uniquement, aucune attribution exclusive, aucune conversion en tokens/euros. Une différence nulle peut refléter précision/délai de compteur.

| Type | Total | Part | Réussi / autorisé | Taux | Refusé | Taux | Erreur technique | Taux |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Autres outils (lecture, recherche, MCP) | 135 | 88.2 % | 134 | 99.3 % | 0 | 0.0 % | 1 | 0.7 % |
| Commandes | 9 | 5.9 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Fichiers | 9 | 5.9 % | 9 | 100.0 % | 0 | 0.0 % | 0 | 0.0 % |
| Total | 153 | 100 % | 152 | 99.3 % | 0 | 0.0 % | 1 | 0.7 % |

Sondes séparées de la production : trois prévues (début, +30 min, fin), 3 réussies, 0 échouées, 0 manquée. Prompt identique, 80 lignes fixes ; sessions jetables sans outil/fichier/réseau propre à la sonde, configuration Muse/opencode-go/high observée.

| Position | Horodatage Paris | TTMT (s) | Tokens/s | Tokens sortie | Durée (s) | Statut |
| --- | --- | --- | --- | --- | --- | --- |
| début | 2026-10-13T20:15:04.172614+02:00 | 3.691 | 206.407 | 822 | 7.798 | success |
| +30 min | 2026-10-13T20:45:06.790759+02:00 | 2.031 | 216.698 | 810 | 5.789 | success |
| fin | 2026-10-13T21:03:47.669098+02:00 | 2.104 | 24.374 | 810 | 35.356 | success |

TTMT min/max : 2.031/3.691 s ; débit min/max : 24.374/216.698 tokens/s. Surcharge sondes : 2442 tokens de sortie, 48.943 s de durée mesurée ; coût N/A, non conservé. Débit = tokens réels natifs / intervalle SSE entre premier et dernier delta ; aucune approximation par fragments.

Bilan : tests applicables réussis ; PG et navigateurs sans objet pour ce validateur pur, aucun résultat PG/front nouveau revendiqué ; archive prouvée et canons préservés ; publication de ce rapport à vérifier sous mandat distinct ; Git non inspecté, aucun commit/push ; aucun effet externe de publisher ; aucun secret exposé ou ajouté aux sources/rapport. La livraison de ce lot ne termine pas le cycle global CISMP. Les pourcentages sont arrondis à une décimale : de légers écarts de somme sont possibles ; les effectifs entiers et totaux croisés sont exacts.
