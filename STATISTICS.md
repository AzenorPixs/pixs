# Statistiques globales

**NCA — Nombre de changes analysés : 187**

## 1. Périmètre et durée

| Indicateur | Nombre de changes | Valeur (jours décimaux ; NCMA en changes achevés/jour) |
| --- | --- | --- |
| DGCT — Temps total de développement du projet via l’IA | 165 | 24,573863 |
| DGCTSPA — Temps total de développement du projet via l’IA hors pauses et attentes | 0 | N/A |
| NJT — Ecart entre le premier change archivé à l’archivage du dernier | 187 | 37,473013 |
| NCMA — Changes achevés par jour (NCA / NJT) | 187 | 4,990258 |

| Indicateur | Nombre de changes | Valeur en heures décimales |
| --- | --- | --- |
| DGCTM — Durée globale moyenne pour 165 changes | 165 | 3,574380 |
| DGCTSPAM — Durée moyenne par change hors pauses et attentes pour 0 changes | 0 | N/A |

N/A : aucune durée globale hors pauses et attentes établie sur un périmètre complet et comparable.

## 2. Agents intervenants et LLM

Les agents de codage et les agents orchestrateurs ont toujours utilisé les dernières versions disponibles au moment de chaque change, selon le contexte déclaré. Cette indication concerne les logiciels agents ; elle ne renseigne pas une version exacte de LLM absente des rapports.

### LLM des agents de codage

| Nombre de changes réalisés ou partiellement réalisés | Modèle de LLM | Niveau de raisonnement | Pourcentage de NCA |
| --- | --- | --- | --- |
| 6 | glm-5.3-flash | high | 3,21 % |
| 2 | GPT-6 | N/A | 1,07 % |
| 105 | muse-spark-1.3-contributor | high | 56,15 % |
| 5 | muse-spark-1.3-contributor | low | 2,67 % |
| 5 | muse-spark-1.3-contributor | medium | 2,67 % |
| 22 | N/A | N/A | 11,76 % |
| 1 | qwen3.8-flash | low | 0,53 % |
| 71 | qwen3.8-flash | xhigh | 37,97 % |

### LLM des agents orchestrateurs

| Nombre de changes réalisés ou partiellement réalisés | Modèle de LLM | Niveau de raisonnement | Pourcentage de NCA |
| --- | --- | --- | --- |
| 67 | GPT-6 | N/A | 35,83 % |
| 89 | GPT-6.1 | high | 47,59 % |
| 1 | N/A | high | 0,53 % |
| 3 | N/A | medium | 1,60 % |

## 3. Performances des LLM de codage OpenCode

| Modèle de LLM | Niveau de raisonnement | TMTM moyen (s) | Débit moyen (tokens/s) |
| --- | --- | --- | --- |
| glm-5.3-flash | high | 5,234 | 88,790 |
| muse-spark-1.3-contributor | high | 3,370 | 345,273 |
| muse-spark-1.3-contributor | low | 2,560 | 333,570 |
| muse-spark-1.3-contributor | medium | 4,744 | 248,529 |
| qwen3.8-flash | xhigh | 2,480 | 87,974 |

| Indicateur | Valeur |
| --- | --- |
| TMTM total moyen (s) | 3,678 |
| Débit minimal total moyen (tokens/s) | 87,974 |
| Débit moyen total moyen (tokens/s) | 220,827 |
| Débit maximal total moyen (tokens/s) | 345,273 |

## 4. Consommation de tokens, coûts et compactions des codeurs

| Mesure | Total | Moyenne par change |
| --- | --- | --- |
| Tokens d’entrée | 239954324 | 1643522,767 |
| Tokens de sortie | 13103233 | 93594,521 |
| Tokens de raisonnement | 2835626 | 30166,234 |
| Tokens de cache lus | 5637662274 | 38614125,164 |
| Tokens de cache écrits | 66450172 | 461459,528 |
| Total natif des tokens | 4236992505 | 39598060,794 |
| Compactions achevées | 134 | 1,457 |

| Devise du coût de production déclaré | Total | Moyenne par change |
| --- | --- | --- |
| USD | 16,292576464 | 0,479193425 |

## 6. Messages et outils des codeurs

Les messages utilisateur peuvent provenir de l’orchestrateur et ne représentent pas nécessairement des messages humains.

| Mesure | Total | Moyenne par change |
| --- | --- | --- |
| Messages des codeurs | 52310 | 328,994 |
| Appels d’outils des codeurs | 29578 | 183,714 |

| Rôle des messages | Nombre | Pourcentage |
| --- | --- | --- |
| assistant | 35362 | 67,60 % |
| compaction | 3 | 0,01 % |
| idle | 702 | 1,34 % |
| synthetic | 2 | 0,004 % |
| system | 19 | 0,04 % |
| utilisateur | 16222 | 31,01 % |

| Outil | Nombre d’appels | Pourcentage |
| --- | --- | --- |
| bash | 3325 | 11,24 % |
| cab-mcp | 159 | 0,54 % |
| cab_codemode_discovery | 19 | 0,06 % |
| cgpt-validation_broker_auto_remediation_policy | 6 | 0,02 % |
| cgpt-validation_broker_evaluate_remediation | 3 | 0,01 % |
| cgpt-validation_broker_execute_controlled_remediation | 2 | 0,01 % |
| cgpt-validation_broker_health | 1196 | 4,04 % |
| cgpt-validation_broker_readiness | 4903 | 16,58 % |
| cgpt-validation_broker_remediation_registry | 108 | 0,37 % |
| cgpt-validation_cancel_approval | 56 | 0,19 % |
| cgpt-validation_get_approval | 995 | 3,36 % |
| cgpt-validation_list_pending | 1657 | 5,60 % |
| cgpt-validation_lookup_validation | 4 | 0,01 % |
| cgpt-validation_poll_approval | 523 | 1,77 % |
| cgpt-validation_propose_approval | 1 | 0,003 % |
| cgpt-validation_request_validation | 5811 | 19,65 % |
| default.write | 1 | 0,003 % |
| edit | 472 | 1,60 % |
| execute | 87 | 0,29 % |
| glob | 880 | 2,98 % |
| grep | 730 | 2,47 % |
| invalid | 10 | 0,03 % |
| question | 7 | 0,02 % |
| read | 6729 | 22,75 % |
| todowrite | 68 | 0,23 % |
| webfetch | 1 | 0,003 % |
| write | 1825 | 6,17 % |

| Résultat technique des appels | Nombre | Pourcentage |
| --- | --- | --- |
| Terminés | 6678 | 94,66 % |
| Erreurs techniques | 252 | 3,65 % |
| En cours | 0 | 0,00 % |

## 7. Autorisations des opérations des codeurs

| Mesure | Total | Moyenne par change |
| --- | --- | --- |
| Demandes d’autorisation distinctes | 3800 | 36,538 |

| Statut | Nombre | Pourcentage |
| --- | --- | --- |
| Approuvées | 3641 | 96,45 % |
| Refusées | 91 | 3,48 % |
| Expirées | 5 | 3,42 % |
| Annulées | 8 | 4,44 % |

## 8. Fichiers et volume du code actuel

| Mesure | Total | Moyenne par change |
| --- | --- | --- |
| Écritures effectivement exécutées | 2285 | 14,647 |
| Fichiers distincts touchés par change | 1758 | 9,503 |

Le volume mesure le stock actuel de sources propres au produit ; chaque fichier physique est compté une seule fois. Les lignes mixtes contribuent aux deux compteurs. Les docstrings de documentation sont classées en commentaires.

| Périmètre | Lignes de code | Lignes de commentaires |
| --- | --- | --- |
| Global | 121289 | 5274 |
| Backend Django | 38960 | 1400 |
| CA PZT | 13453 | 518 |
| DNS | 2545 | 53 |
| Frontend | 4170 | 48 |
| Kit développeur | 198 | 50 |
| Module exemple | 79 | 5 |
| PA natif | 21660 | 961 |
| pixs.agent | 7169 | 196 |
| pixs.auth | 6560 | 240 |
| pixs.backend.systemd-secret-provider | 1421 | 14 |
| pixs.core | 14792 | 484 |
| pixs.kernel | 7000 | 1209 |
| pixs.pzt | 2224 | 48 |
| Règles métier | 1042 | 45 |

## 9. Commandes des codeurs

| Mesure | Total | Moyenne par change |
| --- | --- | --- |
| Commandes exécutées | 1567 | 14,645 |

| Résultat | Nombre | Pourcentage |
| --- | --- | --- |
| Code de sortie nul | 192 | 87,27 % |
| Code de sortie non nul | 28 | 12,73 % |

| Famille de commandes | Nombre | Pourcentage |
| --- | --- | --- |
| Autres | 185 | 12,20 % |
| Compilation et syntaxe | 222 | 14,63 % |
| Compilation frontend | 1 | 0,07 % |
| Navigateurs | 2 | 0,13 % |
| OpenSpec | 546 | 35,99 % |
| PostgreSQL | 39 | 2,57 % |
| Prévol | 187 | 12,33 % |
| Tests | 300 | 19,78 % |
| Tests d’intégration | 13 | 0,86 % |
| Tests unitaires | 22 | 1,45 % |

## 10. Accès web des codeurs

| Mesure | Total | Moyenne par change |
| --- | --- | --- |
| Appels aux outils web | 1 | 0,005 |

| Mesure | Nombre | Pourcentage |
| --- | --- | --- |
| Appels web réussis | 1 | 100,00 % |
| Recherches | 0 | 0,00 % |
| Consultations | 1 | 100,00 % |

| Type d’appel web | Outil | URL consultée ou requête de recherche | Résultat |
| --- | --- | --- | --- |
| Consultation | webfetch | http://127.0.0.1:4096/global/health | réussi |

## 11. Validation et livraison des codeurs

| Mesure | Total | Moyenne par change |
| --- | --- | --- |
| Tests exécutés dans le bilan final | 20359 | 264,403 |
| Fichiers ayant passé un contrôle syntaxique | 129 | 5,609 |
| Tâches OpenSpec prouvées et terminées | 511 | 7,862 |

| Résultat des tests finaux | Nombre | Pourcentage |
| --- | --- | --- |
| Réussis | 19553 | 100,00 % |
| Échoués | 0 | 0,00 % |

| Catégorie de tests | Nombre |
| --- | --- |
| Intégration | 2203 |
| Intégration Python | 7 |
| Navigateurs | 290 |
| Node | 162 |
| Unitaires | 8211 |
| Unitaires Python | 25 |

| Validations OpenSpec | Nombre | Pourcentage |
| --- | --- | --- |
| standard — réussies | 14 | N/A |
| standard — échouées | N/A | N/A |
| strict — réussies | 3 | 50,00 % |
| strict — échouées | 3 | 50,00 % |

N/A : mesure absente, partielle, contradictoire ou sans périmètre comparable établi. Les cumuls historiques ne constituent pas une validation actuelle du projet.

## 12. Synthèse transversale des codeurs

| Domaine | Nombre d’appels | Pourcentage des appels |
| --- | --- | --- |
| Écritures de fichiers | 2298 | 7,77 % |
| Commandes | 3325 | 11,24 % |
| Web | 1 | 0,003 % |
| Autres outils | 23954 | 80,99 % |
| Total | 29578 | 100,00 % |

