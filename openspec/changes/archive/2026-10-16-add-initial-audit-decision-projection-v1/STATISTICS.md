# Statistiques — AuditDecisionProjectionV1

RUN cismp-pixs-01a13baffc02 ; change add-initial-audit-decision-projection-v1 ; contexte209 ; session ses_ebd050627ffemnW70mmEKTCiI3 ; job cismp3-audit-projection-85913b383111. UTC. PLLM mode1. OpenCode1.19.2 (version application, pas révision modèle).

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| muse-spark-1.3-contributor | N/A — révision non exposée | OpenCode Go | high | 2.493507 s | 170.070396 | N/A — génération active non isolable |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
| --- | --- | --- | --- | --- | --- | --- |
| Codex (CGPT) | N/A — modèle exact non exposé | OpenAI | N/A — télémétrie absente | N/A — non sondé | N/A — non sondé | N/A — durée active non exposée |

Les moyennes arithmétiques proviennent des quatre sondes valides du codeur. Dénominateur de service cumulé indisponible pour les deux agents ; durée calendaire, busy CAB, outils et attentes ne prouvent pas une durée de génération.

## 1. Statistiques générales et décisions

Sources : export CAB filtré RUN/contexte209 et historique natif de la session maîtresse, bornes fixées après archive/sonde finale avant rédaction. Le rapport et le gate forment un épilogue hors compteurs. Les sondes jetables sont séparées.
| Rôle des messages | Nombre | Part |
| --- | --- | --- |
| user | 82 | 40.8 % |
| assistant | 119 | 59.2 % |
| Total | 201 | 100 % |

| Décision CAB | Nombre | Part |
| --- | --- | --- |
| approved | 30 | 100.0 % |
| rejected | 0 | 0.0 % |
| needs_clarification | 0 | 0.0 % |
| pending | 0 | 0.0 % |
| Total | 30 | 100 % |

30 approbations explicites CGPT=30permissions once=20Bash+10Write (100 %). Aucun refus de permission.20Read autorisés par permissions de lecture, sans approbation manuelle déduite.2erreurs MCP sans effet : champ ressource erroné puis poll approval inconnu ; READY/prévol neuf0 et reprise même session prouvés.
| Jeu final de référence | Tests réussis | Part |
| --- | --- | --- |
| Unitaires dédiés | 11 | 5.7 % |
| Intégration initiale | 1 | 0.5 % |
| Régressions audit/authz | 180 | 93.8 % |
| Total sans skip | 192 | 100 % |

Une requalification fraîche supplémentaire réussit1/1 après changement partagé models.py par C2 :193 exécutions finales réussies,192tests dans le jeu de référence. Premier lancement régressions :166tentés,1import-error (fixture tests/unit absente de PYTHONPATH), conservé comme échec ; source non modifiée, nouveau lancement PYTHONPATH=src:tests/unit donne180/180. Aucun succès du premier lancement ajouté au total final. Trois compilations/3 et neuf tâches/9 prouvées (100 %).
Stricts ciblés change et deux canons0 ; strict après cochage0. Global standard81/81 natif0. Global strict avant archive79/81 natif1, après78/80 natif1, exactement4WARNING historiques0ERROR : bulk-operations requirements[6],[10],[13] ; identity-assurance requirements[4], texte>500caractères. Aucun strict global réussi déclaré. Archive0 avec avertissement non bloquant : Consider splitting changes with more than 10 deltas.
| Jetons natifs step-finish (sans double comptage info) | Nombre | Part du total déclaré |
| --- | --- | --- |
| input | 1958194 | 16.8 % |
| output | 68475 | 0.6 % |
| reasoning | 18963 | 0.2 % |
| cache.read | 9624500 | 82.5 % |
| cache.write | 0 | 0.0 % |
| Total déclaré | 11670132 | 100 % |

Somme des composantes égale au total natif ;119étapes. Coût financier N/A — devise/portée facturée non garanties ; somme brute API cost=0.232556, sans conversion. Un compactage OpenCode natif confirmé, agent Go/Muse/high configuré ; variant non exposé sur résumé. API compactage Codex absente : non exécuté, aucune réussite conjointe prétendue.

## 2. Types de messages et d’outils

| Type de partie | Nombre | Part |
| --- | --- | --- |
| text | 198 | 29.7 % |
| step-start | 119 | 17.9 % |
| reasoning | 135 | 20.3 % |
| tool | 94 | 14.1 % |
| step-finish | 119 | 17.9 % |
| compaction | 1 | 0.2 % |
| Total | 666 | 100 % |

| Terminaison assistant | Nombre | Part |
| --- | --- | --- |
| tool-calls | 73 | 61.3 % |
| stop | 46 | 38.7 % |
| Total | 119 | 100 % |

| Outil | Nombre | Part | Succès/terminé | Erreur/échec | Refus |
| --- | --- | --- | --- | --- | --- |
| cgpt-validation_broker_readiness | 8 | 8.5 % | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 31 | 33.0 % | 30 (96.8 %) | 1 (3.2 %) | 0 (0.0 %) |
| bash | 20 | 21.3 % | 17 (85.0 %) | 3 (15.0 %) | 0 (0.0 %) |
| write | 10 | 10.6 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 20 | 21.3 % | 20 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 1 | 1.1 % | 0 (0.0 %) | 1 (100.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 1 | 1.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 1 | 1.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_auto_remediation_policy | 1 | 1.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_remediation_registry | 1 | 1.1 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 94 | 100 % | 89 (94.7 %) | 5 (5.3 %) | 0 (0.0 %) |

Completed signifie terminé, pas réussite fonctionnelle. Trois Bash exit1 sont classés échecs malgré completed ; deux MCP sont en erreur technique. Les44MCP=42succès+2erreurs. CAB et historique rapprochés :94outils=44MCP+20Bash+10Write+20Read.

## 3. Fichiers modifiés

| Chemin absolu de tentative | Écritures approuvées/exécutées | Part des10 | Refusées | Erreurs |
| --- | --- | --- | --- | --- |
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-decision-projection-v1/.openspec.yaml | 1 | 10.0 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-decision-projection-v1/proposal.md | 1 | 10.0 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-decision-projection-v1/design.md | 1 | 10.0 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-decision-projection-v1/tasks.md | 2 | 20.0 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-decision-projection-v1/specs/authorization-engine/spec.md | 1 | 10.0 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-decision-projection-v1/specs/audit/spec.md | 1 | 10.0 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/authz/audit_decision_projection.py | 1 | 10.0 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_audit_decision_projection.py | 1 | 10.0 % | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_audit_decision_projection_integration.py | 1 | 10.0 % | 0 (0.0 %) | 0 (0.0 %) |
| Total | 10 | 100 % | 0 (0.0 %) | 0 (0.0 %) |

Les six artefacts ont été déplacés par un Bash archive distinct vers /home/devops/datas/pixs/openspec/changes/archive/2026-10-16-add-initial-audit-decision-projection-v1, à empreintes identiques. tasks.md écrit2fois : création puis neuf coches prouvées. Trois sources nouvelles,12anciens fichiers de baseline conservés, deux canons inchangés. Trois caches py_compile explicitement réservés ; aucun cache exclu lu. STATISTIQUES.md est une écriture finale distincte hors fenêtre.
models.py modifié par C2, sans attribution à C3 : requalification fraîche réussie. DEVOPS.md régénéré par DIU05:51:18UTC, exécutables retenus inchangés ; aucune écriture C3. Aucun Git, commit ou push.

## 4. Commandes

| Famille (libellé<100caractères) | Nombre | Part | Exit0 | Exit non nul | Refus |
| --- | --- | --- | --- | --- | --- |
| Prévol /usr/bin/true | 3 | 15.0 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec validate | 8 | 40.0 % | 6 (75.0 %) | 2 (25.0 %) | 0 (0.0 %) |
| Python py_compile | 3 | 15.0 % | 3 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Unittest unitaire dédié | 1 | 5.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Unittest intégration fraîche | 2 | 10.0 % | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Unittest régressions audit/authz | 2 | 10.0 % | 1 (50.0 %) | 1 (50.0 %) | 0 (0.0 %) |
| OpenSpec archive | 1 | 5.0 % | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 20 | 100 % | 17 (85.0 %) | 3 (15.0 %) | 0 (0.0 %) |

Commandes refusées : aucune (0/20,0.0 %). Les trois sorties1 sont le premier lancement des régressions et les deux stricts globaux. Aucun regroupement shell ni installation ; prévols3/3 natifs0 séparés des tests métier.

## 5. Accès web

| Accès web métier | Nombre | Part | Approuvés | Refusés | Erreurs |
| --- | --- | --- | --- | --- | --- |
| Total outils/URL | 0 | N/A — total0 | 0 | 0 | 0 |

Aucun websearch/webfetch ni URL métier demandée/visitée/refusée (liste vide dans historique). Transport fournisseur OpenCode Go et API locales OpenCode/CAB relèvent du pilotage. Transmission nécessaire Pixs autorisée, sans secret au modèle.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
| --- | --- |
| Début | 2026-10-16T04:31:46.649865+00:00 |
| Fin — après archivage | 2026-10-16T06:16:22+00:00 |
| Durée globale (pauses et attentes incluses) | 01 h 44 min 35 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
| --- | --- | --- | --- |
| Avant — début de session | N/A — horodatage exact non conservé ; relevé natif avant session/sonde | 19 % | 2026-10-22T06:12:56+00:00 |
| Après — après archivage de la spécification | 2026-10-16T06:16:22+00:00 | 21 % | 2026-10-22T06:12:56+00:00 |
| Différence après − avant | — | 2 points de pourcentage | — |

Même compte/fenêtre codex10080minutes/resetsAt vérifiés sans exposer l’identité. Quota partagé : variation pouvant inclure d’autres travaux, pas de consommation exclusive ni conversion tokens/euros. Horodatage initial absent non inventé.
| Sonde hors production | UTC | TTMT s | Tokens sortie | Tokens/s | Statut |
| --- | --- | --- | --- | --- | --- |
| début | 2026-10-16T04:37:26.600725+00:00 | 2.048124 | 1133 | 95.256024 | Réussie |
| +60 min | 2026-10-16T05:38:34.537386+00:00 | 2.478965 | 1153 | 104.170022 | Réussie |
| +90 min | 2026-10-16T06:08:28.379859+00:00 | 2.291229 | 1141 | 198.753420 | Réussie |
| fin | 2026-10-16T06:15:58.772857+00:00 | 3.155708 | 1128 | 282.102118 | Réussie |
| +30 min | 2026-10-16T05:07:40.642276+00:00 | N/A | N/A | N/A | Manquée — FIFO C2, non reconstruite |

Relèves5 (100 %), réussies4 (80.0 %), échouées0 (0.0 %), manquées1 (20.0 %). Prompt constant185caractères, sessions jetables, même fournisseur/modèle/high, zéro outil. TTMTmoyen=2.493507s, min=2.048124,max=3.155708. Débitmoyen=170.070396,min=95.256024,max=282.102118. Surcharge sondes :4555tokens sortie,42.941159s mesurées (pas service génération isolé), coûtN/A. BenchmarkPLLM distinct TTFT15.8619s/globalTPS2477.389, non mélangé aux sondes.
| Domaine | Nombre | Part globale | Succès/terminé | Erreur/échec | Refus |
| --- | --- | --- | --- | --- | --- |
| Fichiers | 10 | 10.6 % | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 20 | 21.3 % | 17 (85.0 %) | 3 (15.0 %) | 0 (0.0 %) |
| Web | 0 | 0.0 % | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 64 | 68.1 % | 62 (96.9 %) | 2 (3.1 %) | 0 (0.0 %) |
| Total global | 94 | 100 % | 89 (94.7 %) | 5 (5.3 %) | 0 (0.0 %) |

Totaux croisés94outils,20Bash,10Write vérifiés ;89succès+5erreurs/échecs=94 ;30approbations=30once=20Bash+10Write. Les pourcentages sur total0 sontN/A. Temps CAB réservé/busy/idle ne mesure pas la génération ; export observé après borne peut contenir de l’attente documentaire supplémentaire, non ajoutée à la durée finale.
Archive unique native0, six artefacts exacts, canons conservés, publication ref24. Rapport soumis à mandat distinct, puis vérification UTF8/LF/six sections/totaux avant gate. Tests192réussis+requalification1 ; PostgreSQL/navigateur sans objet pour ce profil pur. Aucun Git ni secret lu/transmis au modèle. C1/C2 sous leurs propriétaires. Arrêt humain CISMP3 après ce change/rapport ; aucun achèvement global Pixs prétendu, aucun nouveau candidat, services partagés préservés.
