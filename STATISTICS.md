# Statistiques globales

**NCA — Nombre de changes analysés : 158**

## Périmètre et durée

| Indicateur | Nombre de changes | Valeur (jours décimaux ; NCMA en changes achevés/jour) |
|---|---|---|
| DGCT — Temps total de développement du projet via l’IA | 155 | 18,126014 |
| DGCTSPA — Temps total de développement du projet via l’IA hors pauses et attentes | 14 | 1,264758 |
| NJT — Ecart entre le premier change archivé à l’archivage du dernier | 158 | 24,516217 |
| NCMA — Changes achevés par jour (NCA / NJT) | 158 | 6,444714 |

| Indicateur | Nombre de changes | Valeur en heures décimales |
|---|---|---|
| DGCTM — Durée globale moyenne pour 155 changes | 155 | 2,806609 |
| DGCTSPAM — Durée moyenne par change hors pauses et attentes pour 14 changes | 14 | 2,168157 |

## Agents intervenants et LLM

Les agents de codage et orchestrateurs ont utilisé les dernières versions disponibles au moment de chaque change, conformément au contexte déclaré par le développeur.

### LLM des agents de codage

| Changes réalisés ou partiellement réalisés | Modèle de LLM | Niveau de raisonnement | Pourcentage de NCA |
|---|---|---|---|
| 4 | N/A | N/A | 2,53 % |
| 6 | glm-5.3-flash | high | 3,80 % |
| 83 | muse-spark-1.3-contributor | high | 52,53 % |
| 5 | muse-spark-1.3-contributor | low | 3,16 % |
| 4 | muse-spark-1.3-contributor | medium | 2,53 % |
| 1 | qwen3.8-flash | low | 0,63 % |
| 65 | qwen3.8-flash | xhigh | 41,14 % |

### LLM des agents orchestrateurs

| Changes réalisés ou partiellement réalisés | Modèle de LLM | Niveau de raisonnement | Pourcentage de NCA |
|---|---|---|---|
| 39 | GPT-6 | N/A | 24,68 % |
| 114 | GPT-6.1 | high | 72,15 % |

## Performances des LLM de codage OpenCode

| Modèle de LLM | Niveau de raisonnement | TMTM moyen (s) | Débit moyen (tokens/s) |
|---|---|---|---|
| glm-5.3-flash | high | 5,234 | 88,790 |
| muse-spark-1.3-contributor | high | 3,455 | 341,787 |
| muse-spark-1.3-contributor | low | 2,560 | 333,571 |
| muse-spark-1.3-contributor | medium | 4,744 | 248,529 |
| qwen3.8-flash | xhigh | 2,480 | 87,626 |

| Indicateur | Valeur |
|---|---|
| TMTM total moyen (s) | 3,695 |
| Débit minimal total moyen (tokens/s) | 87,626 |
| Débit moyen total moyen (tokens/s) | 220,061 |
| Débit maximal total moyen (tokens/s) | 341,787 |

## Consommation de tokens, coûts et compactions des codeurs

| Mesure | Total | Moyenne par change |
|---|---|---|
| Tokens d’entrée | 169348218 | 1388100,148 |
| Tokens de sortie | 10527321 | 88464,882 |
| Tokens de raisonnement | 2479777 | 22140,866 |
| Tokens de cache lus | 4048099908 | 34017646,286 |
| Tokens de cache écrits | 62556145 | 525681,891 |
| Total natif des tokens | 3733884709 | 37338847,090 |
| Compactions achevées | 123 | 1,268 |

| Devise du coût de production déclaré | Total | Moyenne par change |
|---|---|---|
| USD | 19,148999270 | 0,638299976 |

## Messages et outils des codeurs

| Mesure | Total | Moyenne par change |
|---|---|---|
| Messages | 39039 | 284,956 |
| Appels d’outils | 23387 | 158,020 |

| Rôle des messages | Nombre | Pourcentage |
|---|---|---|
| Utilisateur | 11815 | 30,35 % |
| Assistant | 27114 | 69,65 % |

Les messages « utilisateur » peuvent provenir de l’orchestrateur et ne sont pas nécessairement des messages humains.

| Outil | Nombre d’appels | Pourcentage |
|---|---|---|
| bash | 2667 | 11,40 % |
| cab-mcp | 159 | 0,68 % |
| cgpt-validation_broker_auto_remediation_policy | 6 | 0,03 % |
| cgpt-validation_broker_evaluate_remediation | 2 | 0,01 % |
| cgpt-validation_broker_execute_controlled_remediation | 1 | 0,004 % |
| cgpt-validation_broker_health | 700 | 2,99 % |
| cgpt-validation_broker_readiness | 4039 | 17,27 % |
| cgpt-validation_broker_remediation_registry | 22 | 0,09 % |
| cgpt-validation_cancel_approval | 52 | 0,22 % |
| cgpt-validation_get_approval | 749 | 3,20 % |
| cgpt-validation_list_pending | 1105 | 4,72 % |
| cgpt-validation_poll_approval | 423 | 1,81 % |
| cgpt-validation_propose_approval | 1 | 0,004 % |
| cgpt-validation_request_validation | 4696 | 20,08 % |
| default.write | 1 | 0,004 % |
| edit | 283 | 1,21 % |
| glob | 768 | 3,28 % |
| grep | 578 | 2,47 % |
| invalid | 11 | 0,05 % |
| question | 5 | 0,02 % |
| read | 5446 | 23,29 % |
| todowrite | 57 | 0,24 % |
| webfetch | 1 | 0,004 % |
| write | 1615 | 6,91 % |

| Résultat technique des appels | Nombre | Pourcentage |
|---|---|---|
| Terminés sans erreur technique | 18788 | 96,13 % |
| Erreurs techniques | 691 | 3,54 % |
| En cours | 0 | 0,00 % |

## Autorisations des opérations des codeurs

| Mesure | Total | Moyenne par change |
|---|---|---|
| Demandes distinctes | 2933 | 32,231 |

| Statut | Nombre de demandes | Pourcentage |
|---|---|---|
| Approuvées | 2792 | 96,61 % |
| Refusées | 74 | 2,62 % |
| Expirées | 5 | 0,20 % |
| Annulées | 9 | 0,35 % |

## Fichiers et volume du code actuel

| Mesure | Cumul | Moyenne par change |
|---|---|---|
| Écritures exécutées | 2372 | 17,970 |
| Fichiers distincts touchés par change | 1542 | 9,822 |

| Périmètre | Lignes de code | Lignes de commentaires |
|---|---|---|
| Global | 80322 | 3854 |
| PFO | 3559 | 20 |
| PBO | 74636 | 3719 |
| PA | 2127 | 115 |
| PZT | 0 | 0 |

## Commandes des codeurs

| Mesure | Total | Moyenne par change |
|---|---|---|
| Commandes exécutées | 2376 | 17,094 |

| Résultat des commandes exécutées | Nombre | Pourcentage |
|---|---|---|
| Code de sortie nul | 484 | 95,46 % |
| Code de sortie non nul | 23 | 4,54 % |

| Famille de commandes | Nombre | Pourcentage |
|---|---|---|
| Autres commandes | 92 | 8,64 % |
| Contrôles syntaxiques | 162 | 15,21 % |
| OpenSpec | 418 | 39,25 % |
| Prévol | 127 | 11,92 % |
| Tests | 207 | 19,44 % |
| Tests d’intégration | 10 | 0,94 % |
| Tests PostgreSQL | 35 | 3,29 % |
| Tests unitaires | 14 | 1,31 % |

## Accès web des codeurs

| Mesure | Total | Moyenne par change |
|---|---|---|
| Appels aux outils web | 1 | 0,009 |

| Résultat | Nombre | Pourcentage |
|---|---|---|
| Appels web réussis | 1 | 100,00 % |

| Type d’appel web | Nombre | Pourcentage |
|---|---|---|
| Recherche | 0 | N/A |
| Consultation | 1 | 100,00 % |

| Type d’appel web | Outil | URL consultée ou requête de recherche | Résultat |
|---|---|---|---|
| Consultation | webfetch | http://127.0.0.1:4096/global/health | Réussi — diagnostic local OpenCode |

## Validation et livraison des codeurs

| Mesure | Total | Moyenne par change |
|---|---|---|
| Tests exécutés dans les bilans finaux | 44340 | 295,600 |
| Fichiers ayant passé un contrôle syntaxique | 223 | 6,194 |
| Tâches OpenSpec prouvées et terminées | 515 | 7,803 |

| Résultat des tests finaux | Nombre | Pourcentage |
|---|---|---|
| Tests finaux réussis | 44340 | 100,00 % |
| Tests finaux échoués | 0 | 0,00 % |

| Catégorie de tests | Nombre |
|---|---|
| Intégration | 3566 |
| OpenLDAP | 4 |
| PostgreSQL | 857 |
| Tests purs | 346 |
| Unitaires | 13391 |
| Unitaires Auth | 116 |

| Validations OpenSpec | Réussies | Échouées | Réussite | Échec |
|---|---|---|---|---|
| Standard | N/A | N/A | N/A | N/A |
| Strict | 102 | 8 | 92,73 % | 7,27 % |

## Synthèse transversale des codeurs

| Domaine | Nombre d’appels | Pourcentage des appels |
|---|---|---|
| Écritures de fichiers | 1950 | 8,34 % |
| Commandes | 2616 | 11,19 % |
| Web | 1 | 0,004 % |
| Autres outils | 18820 | 80,47 % |
| Total | 23387 | 100,00 % |
