# Statistiques — add-initial-startup-mode-vocabulary-v1

RUN : cismp1-pixs-d9d2076629b54d31 ; contexte CAB 274 ; job job-39ea43e9ba874f8b. Sessions de production : ses_eb5b62aafffewOk8PqbwsgKP30, ses_eb5aa6524ffekoUef1ID2ocz12. Fournisseur et modèle vérifiés par métadonnées natives ; sources : historique complet des deux sessions, mandats/effets corrélés, agrégat CAB 1.3.0 et sondes dédiées. Brouillon CAB examiné et complété ; ses compteurs observés sont distingués du relevé natif complet.

Périmètre : un seul change de vocabulaire, archivé puis publié techniquement en référence 32. Intervalle de production arrêté avant la rédaction de ce rapport ; le rapport, sa vérification et la clôture ultérieure sont exclus des totaux figés. L’achèvement du change ne signifie pas l’achèvement du cycle global Pixs.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | OpenCode 1.19.3 ; version exacte modèle N/A | OpenCode Go / opencode-go | high | 1.839 s | 381.6 | N/A |

Une seule sonde entièrement mesurable entre dans les moyennes : la finale. Sondes prévues 2 (100.0 %) : finale valide 1 (50.0 %), initiale incomplète 1 (50.0 %), relève périodique manquée 0 (0.0 %). Aucune échéance +30 minutes atteinte pendant cet intervalle. L’initiale a répondu et sa sortie est comptée en surcharge, mais son instant monotone d’envoi n’a pas été persisté : TTMT N/A, aucune reconstruction ni nouvelle « initiale » rétroactive. Elle est exclue des moyennes.

La finale utilise le même prompt déterministe (0001 à 0200), sans outil/fichier/réseau propre à la sonde, dans une session dédiée supprimée après collecte. Mesures SSE sur deltas de texte visibles et compteur natif info.tokens.output : 625 tokens, 70 deltas, TTMT 1.839 s, 381.6 tokens/s. Ce débit compte des tokens natifs, pas les fragments SSE. Une seule valeur valide ne justifie pas une dispersion estimée. Surcharge des deux sondes : 1 233 tokens de sortie et 1 045 tokens de raisonnement, environ 10.98 s calendaires ; coût exact N/A, exclu du coût de production ci-dessous.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex ; modèle exact N/A dans la télémétrie | N/A | OpenAI | N/A | N/A — non sondé | N/A — non sondé | N/A |

Les durées actives de génération des agents ne sont pas isolées des outils et attentes : temps de service, dénominateur cumulé et chevauchements N/A. La durée calendaire et le busy CAB ne sont pas assimilés au service du modèle.

## 1. Statistiques générales et décisions

| Mesure de production | Valeur |
| --- | --- |
| Durée calendaire, pauses/attentes/tests/archive inclus | 00 h 19 min 32 s |
| Messages natifs | 112 |
| Appels d’outils natifs | 82 (100.0 %) |
| Outils natifs terminés | 81 (98.8 %) |
| Outil en erreur technique | 1 (1.2 %) — request_validation interrompu après refus CAB |
| Commandes natives effectivement exécutées | 10 ; 8 exit 0 (80.0 %), 2 exit 1 (20.0 %) |
| Tests applicables | 29/29 réussis (100.0 %), 0 échec, 0 skip |
| Compilations | 3/3 fichiers réussis (100.0 %) dans une commande |
| Compactions de production observées | 0 ; échéance 1 h 30 non atteinte |

« Terminé » décrit l’état natif completed ; il ne prouve pas à lui seul une approbation manuelle ni une réussite fonctionnelle. Les deux exits 1 sont les validations OpenSpec strictes avec quatre warnings de longueur, et restent des contrôles non réussis globalement. Un refus CAB avant effet n’est pas une commande exécutée. L’interruption de l’appel MCP et la décision rejected décrivent le même incident et ne sont pas additionnées comme deux effets.

| Décision CAB | Nombre | Part |
| --- | --- | --- |
| approved | 18 | 94.7 % |
| rejected | 1 | 5.3 % |
| needs_clarification | 0 | 0.0 % |
| pending | 0 | 0.0 % |
| Total | 19 | 100.0 % |

18 permissions once observées pour 18 effets unitaires (8 écritures et 10 commandes). Le mandat d’archivage initial a été refusé pour un doublon read/write ajouté au manifeste, avant permission native et avant effet. Après réconciliation du même approval_id, récupération prepare/complete dans le même RUN/job et prévol /usr/bin/true neuf sous once : archivage par mandat corrigé unique. Aucune purge, reprise d’écriture ni réarchive.

Le brouillon CAB préparait 77 outils (76 completed, 1 erreur), contre 82 dans l’historique natif complet, notamment une commande de prévol avant armement et des communications techniques. Le rapport privilégie les historiques natifs complets ; aucune addition des deux sources. Le snapshot CAB indique des tentatives HTTP refusées (run-not-quiescent 1, native-validation-not-correlated 3), distinctes du refus de permission. Des prepare ont aussi reçu broker-not-ready avant réconciliation de la réponse refusée ; pas d’effet métier. Les lacunes de collecte restent N/A.

| Champ de tokens natif | Nombre | Part du total |
| --- | --- | --- |
| input | 381039 | 4.4 % |
| output | 24096 | 0.3 % |
| reasoning | 6604 | 0.1 % |
| cache read | 8305360 | 95.3 % |
| cache write | 0 | 0.0 % |
| Total | 8717099 | 100.0 % |

Contrôle croisé : 381 039 + 24 096 + 6 604 + 8 305 360 + 0 = 8 717 099. Coût de production déclaré par OpenCode : 0.060854620 USD ; il n’est pas un relevé fournisseur de facturation. Tokens/coûts de l’orchestrateur N/A, sans estimation.

PLLM1 vérifiée le 2026-10-17T16:33:26+02:00 : Muse high, TTFT 4.5347 s, premier palier 1 024 non concluant puis 2 048 réussi. Le débit global brut du parseur (3882.5 tokens/s) inclut le raisonnement compté par l’API et non exposé intégralement dans le flux ; la borne inférieure conservatrice (1 523 tokens / durée totale 5.0162 s) est 303.6 tokens/s et satisfait elle aussi >15. Quotas utilisés au contrôle : 5 h 0 %, semaine 64 %, mois 97 %, tous status ok. Mesures partagées et horodatées, pas une consommation exclusive du RUN.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
| --- | --- | --- |
| user | 31 | 27.7 % |
| assistant | 81 | 72.3 % |
| Total | 112 | 100.0 % |

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 101 | 23.7 % |
| step-start | 81 | 19.0 % |
| reasoning | 82 | 19.2 % |
| tool | 82 | 19.2 % |
| step-finish | 80 | 18.8 % |
| Total | 426 | 100.0 % |

| Fin de réponse assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 56 | 69.1 % |
| stop | 24 | 29.6 % |
| absent | 1 | 1.2 % |
| Total | 81 | 100.0 % |

La terminaison absente correspond au message interrompu ; elle ne signifie pas une réussite.

| Type d’outil | Total et part | Completed | Erreur technique | Refus natif de permission |
| --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 9 (11.0 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 19 (23.2 %) | 18 (94.7 %) | 1 (5.3 %) | 0 (0.0 %) |
| bash | 10 (12.2 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 3 (3.7 %) | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 20 (24.4 %) | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| glob | 8 (9.8 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 2 (2.4 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (9.8 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 (1.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 (1.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_remediation_registry | 1 (1.2 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 82 (100.0 %) | 81 (98.8 %) | 1 (1.2 %) | 0 (0.0 %) |

Les lectures/recherches et communications MCP réussies n’impliquent pas une approbation manuelle. Les 18 effets mutables sont corrélés aux décisions CAB et once. Le refus CAB unique demeure dans la table des décisions et n’est pas maquillé en refus natif d’une commande déjà commencée.

## 3. Fichiers modifiés

Les chiffres représentent des tentatives d’écriture natives avant rédaction de ce rapport. Les chemins de préparation complets sont conservés même après déplacement par l’archivage.

| Chemin absolu complet | Écritures et part | Approuvées/exécutées | Refusées | Erreur |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-startup-mode-vocabulary-v1/.openspec.yaml | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-startup-mode-vocabulary-v1/proposal.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-startup-mode-vocabulary-v1/design.md | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-startup-mode-vocabulary-v1/tasks.md | 2 (25.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/backend/startup_mode.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_startup_mode.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_startup_mode_integration.py | 1 (12.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total — 7 chemins uniques | 8 (100.0 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

Le CLI a déplacé les quatre fichiers OpenSpec du change dans /home/devops/datas/pixs/openspec/changes/archive/2026-10-17-add-initial-startup-mode-vocabulary-v1/, sans synchronisation canonique (--skip-specs). Les trois fichiers Python sont nouveaux. Aucun fichier produit préexistant n’est modifié ; les 15 empreintes de cadrages, canon, façade et références contrôlées sont préservées. Les .pyc régénérables issus de py_compile sont des artefacts de validation déclarés au manifeste, pas des sources produit. Le checkpoint non versionné est distinct.

Le présent rapport est un huitième fichier livré à /home/devops/datas/pixs/openspec/changes/archive/2026-10-17-add-initial-startup-mode-vocabulary-v1/STATISTIQUES.md, sous mandat propre après cette borne ; son écriture et les éventuelles corrections ne sont pas incluses dans les 8 tentatives ci-dessus.

## 4. Commandes

| Famille exécutée | Nombre et part | Exit 0 | Exit 1 |
| --- | --- | --- | --- |
| Prévol /usr/bin/true | 2 (20.0 %) | 2 (100.0 %) | 0 (0.0 %) |
| Python py_compile | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) |
| Python unittest | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) |
| OpenSpec validate | 5 (50.0 %) | 3 (60.0 %) | 2 (40.0 %) |
| OpenSpec archive | 1 (10.0 %) | 1 (100.0 %) | 0 (0.0 %) |
| Total | 10 (100.0 %) | 8 (80.0 %) | 2 (20.0 %) |

| Commande exécutée — libellé limité à 100 caractères | Occurrences | Part des exécutions |
| --- | --- | --- |
| /usr/bin/true | 2 | 20.0 % |
| /home/devops/.local/npm/bin/openspec validate add-initial-startup-mode-vocabulary-v1 --strict | 2 | 20.0 % |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/startup_mode.py tests/unit… | 1 | 10.0 % |
| /usr/bin/env PYTHONPATH=src:tests:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unitte… | 1 | 10.0 % |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 | 20.0 % |
| /home/devops/.local/npm/bin/openspec validate --all | 1 | 10.0 % |
| /home/devops/.local/npm/bin/openspec archive add-initial-startup-mode-vocabulary-v1 --yes --skip-sp… | 1 | 10.0 % |
| Total | 10 | 100.0 % |

Commande refusée avant exécution, regroupée séparément :

| Commande refusée — au plus 100 caractères | Occurrences | Part des mandats de commande |
| --- | --- | --- |
| /home/devops/.local/npm/bin/openspec archive add-initial-startup-mode-vocabulary-v1 --yes --skip-sp… | 1 | 9.1 % |

Onze mandats de commande : 10 approuvés/exécutés (90.9 %), 1 refusé sans effet (9.1 %). La commande d’archivage ensuite approuvée avec identité neuve n’a été exécutée qu’une fois. Les libellés tronqués ne constituent pas des commandes de rejeu ; les preuves natives et le checkpoint conservent les cibles exactes.

## 5. Accès web

Cinq appels HTTPS techniques du benchmark PLLM sont directement identifiables. Ils sont hors outils de production OpenCode. Les générations du modèle et sondes passent aussi par le fournisseur ; leurs URL effectives et le nombre exhaustif de requêtes internes ne sont pas exposés, donc N/A. Les appels HTTP loopback de pilotage ne sont pas recensés exhaustivement ; aucun zéro global n’est inventé.

| URL effectivement appelée — au plus 100 caractères | Nombre et part | Autorisé/appelé | Refusé | Erreur HTTP observée |
| --- | --- | --- | --- | --- |
| https://opencode.ai/zen/go/v1/models | 1 (20.0 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| https://opencode.ai/zen/go/v1/usage | 2 (40.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| https://opencode.ai/zen/go/v1/responses | 2 (40.0 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total des appels directement comptés | 5 (100.0 %) | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

La première génération est restée non concluante au palier 1 024 : cela ne transforme pas son accès HTTPS en refus ni en erreur HTTP. URL refusées observées dans ce périmètre : aucune. Aucun en-tête, secret, compte ou identifiant de session fournisseur n’est publié.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début — création native de la session maîtresse | 2026-10-17T16:35:15.152000+02:00 |
| Fin — après archive, sonde finale et collecte avant rédaction | 2026-10-17T16:54:47.531909+02:00 |
| Durée globale, pauses et attentes incluses | 00 h 19 min 32 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | N/A — outil natif get_usage_limits non exposé | N/A | N/A |
| Après — après archivage de la spécification | 2026-10-17T16:54:47.531909+02:00 ; outil natif non exposé | N/A | N/A |
| Différence après − avant | — | N/A — deux relevés natifs indisponibles | — |

L’identité codex/fenêtre 10080 minutes n’a pas pu être lue. Aucun quota Spark ni OpenCode Go n’est substitué. Les quotas de compte sont partagés ; leur variation pourrait inclure d’autres tâches simultanées et ne serait pas exclusivement imputée à ce RUN.

| Domaine observé | Nombre | Part globale | Terminé/exécuté | Refus natif | Erreur technique |
| --- | --- | --- | --- | --- | --- |
| Fichiers — tentatives natives | 8 | 9.2 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes natives | 10 | 11.5 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Web technique PLLM directement compté | 5 | 5.7 % | 5 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Autres outils natifs | 64 | 73.6 % | 63 (98.4 %) | 0 (0.0 %) | 1 (1.6 %) |
| Total du périmètre compté | 87 | 100.0 % | 86 (98.9 %) | 0 (0.0 %) | 1 (1.1 %) |

Contrôle croisé : 8 + 10 + 64 = 82 outils natifs ; + 5 appels HTTPS techniques = 87 actions du périmètre compté. Les 19 décisions CAB ne sont pas ajoutées comme effets. Le refus CAB unique reste hors exécutions, et l’erreur MCP consécutive est visible parmi les autres outils. Les deux exits stricts 1 sont distingués des terminaisons natives completed, pas cachés dans un total de « succès ». Ce total n’est pas l’inventaire exhaustif des outils Codex ou des appels fournisseur non exposés. Les arrondis de parts peuvent ne pas sommer exactement à 100.0 %.

| Résultat | État prouvé |
| --- | --- |
| Périmètre | StartupMode : INSTALLER / FIRST_CONFIGURATION / NORMAL / MAINTENANCE, vocabulaire seul |
| Syntaxe | 3 fichiers py_compile, exit 0 |
| Tests | 29/29 réussis, aucun échec/skip |
| OpenSpec ciblé | Deux validations strictes, exit 0 |
| Global standard avant archive | 186/186, exit 0 |
| Global strict avant / après archive | 184/186 puis 183/185, exit 1 ; 4 warnings longueur, 0 ERROR, canons inchangés |
| Avertissements exacts | bulk-operations requirements[6], [10], [13] ; identity-assurance requirements[4] |
| Archive | Unique, exit 0 ; tâches prouvées ; --skip-specs, canon inchangé |
| Publication technique | Reçu publish-985112a087d042b5, référence 32, phase REPORT |
| Limites | Aucun choix de mode runtime, marqueur, transition, base, authentification ou qualification P0 |
| Git | Aucune inspection, aucun commit/push ; état SCM non contrôlé |
| Secrets et accès externes | Seuls fournisseur/prévol et générations nécessaires autorisés ; secrets confinés au processus, aucun secret inclus dans les sources ou le rapport |
| Clôture | Rapport à vérifier ; gate, désarmement/libération et fermeture OpenCode interviennent ensuite, aucune réussite anticipée |

La session s’arrête après ce seul change selon la demande explicite. Aucun prochain change n’est sélectionné ; cycle_global_complete demeure false.
