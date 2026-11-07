# Statistiques — add-initial-audit-field-redaction-v1

RUN parent : cismp-pixs-20261007-061019. Archive : openspec/changes/archive/2026-10-08-add-initial-audit-field-redaction-v1. Production du change après la reprise normative audit, de la sélection à la fin après archive et sonde finale. Le rapport et sa validation sont hors intervalle.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Raisonnement | TTMT moyen | Tokens/s moyens | Service et part globale |
|---|---|---|---|---:|---:|---|
| Qwen3.8 Flash (qwen3.8-flash) | Modèle N/A ; OpenCode 1.18.34 | opencode-go | xhigh | 1.697 s | 69.523 | 325.798 s ; part globale N/A |

Les moyennes arithmétiques portent uniquement sur les sondes valides. Le service mesurable est l'union des intervalles natifs de texte/raisonnement. Les attentes et outils ne sont pas ajoutés. Le service orchestrateur n'est pas exposé : le dénominateur global reste N/A.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Raisonnement | TTMT | Tokens/s | Service |
|---|---|---|---|---:|---:|---:|
| Codex, identifiant exact N/A | N/A — télémétrie non exposée | OpenAI | N/A | N/A | N/A | N/A |

## 1. Statistiques générales et décisions

Durée globale : 00 h 37 min 48 s, pauses, outils et attentes inclus. Messages : 116 ; parties : 384 ; appels : 65.

Un outil natif terminé est classé exécuté, y compris lectures sans permission et transport MCP. Les mandats CAB sont comptés séparément ; READY ne vaut jamais approbation. Les codes de commandes viennent des metadata natives.

| Résultat des appels | Nombre | Part |
|---|---:|---:|
| Exécutés | 62 | 95.4 % |
| Refus de permission natifs | 2 | 3.1 % |
| Erreurs techniques | 1 | 1.5 % |
| Total | 65 | 100.0 % |

| Statut natif distinct des mandats | Nombre | Part |
|---|---:|---:|
| APPROVED | 22 | 100.0 % |
| Total des requestId observés | 22 | 100.0 % |

Tokens de production : entrée 528, sortie 45405, raisonnement déclaré 0, cache lu 16098616, cache écrit 93255. Valeurs natives, sans reconstruction du raisonnement. Coût total natif : 0.297648406, unité OpenCode, devise non exposée.

Tests : 22 unitaires, 1 intégration fraîche et 56 régressions, soit 79/79, zéro échec/erreur/skip. Trois compilations : 3/3. Change strict : 1/1, code 0. Global avant archive : 77/77, code 0. WARNING de longueur seuls, exclus par instruction développeur ; aucune ERROR. Canon audit non strict 1/1, code 0 ; strict code 1 uniquement pour longueur, qualifié séparément. Sept tâches sur sept cochées. Archive native code 0, specsUpdated=false.

| Sonde | UTC | Lignes | Tokens sortie | TTMT | Tokens/s | État |
|---|---|---:|---:|---:|---:|---|
| début | 2026-10-08T03:33:11.130942+00:00 | 40 | 572 | 1.937 s | 67.308 | Valide |
| +30 min | 2026-10-08T04:03:12.865992+00:00 | 1 | 43 | 1.405 s | 52.846 | Invalide, exclue des moyennes |
| +30 min — unique reprise | 2026-10-08T04:05:39.369573+00:00 | 40 | 822 | 1.646 s | 62.259 | Valide |
| fin après archive | 2026-10-08T04:10:25.716011+00:00 | 40 | 696 | 1.508 s | 79.002 | Valide |

Sondes toutes les 30 minutes sans attendre le créneau. 4 tentatives, 3 valides (75.0 %) ; surcharge séparée : 2133 tokens sortie, 38.697 s calendaires cumulées, coût natif 0.005617598. Positions manquées : [].

## 2. Types de messages et d'outils

| Rôle | Nombre | Part |
|---|---:|---:|
| user | 28 | 24.1 % |
| assistant | 88 | 75.9 % |

| Type de partie | Nombre | Part |
|---|---:|---:|
| reasoning | 88 | 22.9 % |
| step-finish | 88 | 22.9 % |
| step-start | 88 | 22.9 % |
| text | 55 | 14.3 % |
| tool | 65 | 16.9 % |

| Outil | Appels et part | Exécutés et taux | Refusés et taux | Erreurs et taux |
|---|---:|---:|---:|---:|
| bash | 15 (23.1 %) | 13 (86.7 %) | 2 (13.3 %) | 0 (0.0 %) |
| cgpt-validation_broker_readiness | 2 (3.1 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_get_approval | 1 (1.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 22 (33.8 %) | 22 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| edit | 1 (1.5 %) | 0 (0.0 %) | 0 (0.0 %) | 1 (100.0 %) |
| glob | 1 (1.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| read | 15 (23.1 %) | 15 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| write | 8 (12.3 %) | 8 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |

## 3. Fichiers

| Chemin d'outil natif | Tentatives et part | Exécutées et taux | Refusées et taux | Erreurs et taux |
|---|---:|---:|---:|---:|
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-field-redaction-v1/design.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-field-redaction-v1/proposal.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-field-redaction-v1/specs/audit/spec.md | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-initial-audit-field-redaction-v1/tasks.md | 3 (33.3 %) | 2 (66.7 %) | 0 (0.0 %) | 1 (33.3 %) |
| /home/devops/datas/pixs/src/pixs/kernel/audit_field_redaction.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_audit_field_redaction_integration.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_audit_field_redaction.py | 1 (11.1 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 9 (100.0 %) | 8 (88.9 %) | 0 (0.0 %) | 1 (11.1 %) |

Le fichier .openspec.yaml est généré par la CLI de création, compté avec cette commande et non comme outil write. Le rapport STATISTIQUES.md lui-même est hors intervalle. Les lectures natives n'ont pas été assimilées à des modifications. Fichiers préexistants préservés selon empreintes ciblées ; sources attendues exactes UTF-8/LF.

## 4. Commandes

| Commande exacte, retour à la ligne aplati | Occurrences | Part | Codes natifs |
|---|---:|---:|---|
| /home/devops/.local/npm/bin/openspec new change add-initial-audit-field-redaction-v1 | 1 | 6.7 % | [0] |
| /home/devops/.local/npm/bin/openspec validate add-initial-audit-field-redaction-v1 --strict --json | 2 | 13.3 % | [0, 0] |
| /home/devops/python/current/bin/python3 -m py_compile src/pixs/kernel/audit_field_redaction.py | 1 | 6.7 % | [0] |
| /home/devops/python/current/bin/python3 -m py_compile tests/unit/test_audit_field_redaction.py | 1 | 6.7 % | [0] |
| /home/devops/python/current/bin/python3 -B -c 'import sys import unittest sys.path[:0] = ["src", "tests/unit"] suite = unittest.defaultTestLoader.loadTestsFromName("test_audit_field_redaction") result = unittest.TextTestRunner(verbosity=2).run(suite) sys.exit(not result.wasSuccessful())' | 1 | 6.7 % | [0] |
| /home/devops/python/current/bin/python3 -m py_compile tests/integration/test_audit_field_redaction_integration.py | 1 | 6.7 % | [0] |
| /home/devops/python/current/bin/python3 -B -c 'import sys import unittest sys.path[:0] = ["src", "tests/integration"] suite = unittest.defaultTestLoader.loadTestsFromName("test_audit_field_redaction_integration") result = unittest.TextTestRunner(verbosity=2).run(suite) sys.exit(not result.wasSuccessful())' | 1 | 6.7 % | [0] |
| /home/devops/python/current/bin/python3 -B -c 'import sys import unittest sys.path[:0] = ["src", "tests/unit", "tests/integration"] suite = unittest.defaultTestLoader.loadTestsFromNames(['"'"'test_audit_event'"'"', '"'"'test_diagnostics_typed'"'"', '"'"'test_audit_event_integration'"'"', '"'"'test_kernel_purity'"'"', '"'"'test_public_api_facades'"'"']) result = unittest.TextTestRunner(verbosity=2).run(suite) sys.exit(not result.wasSuccessful())' | 1 | 6.7 % | [0] |
| true | 1 | 6.7 % | ['N/A'] |
| /usr/bin/true | 2 | 13.3 % | [0, 0] |
| /home/devops/.local/npm/bin/openspec validate --all --json | 1 | 6.7 % | [0] |
| grep -n "effet prouv" /home/devops/datas/pixs/openspec/changes/add-initial-audit-field-redaction-v1/tasks.md / xxd / head -60 | 1 | 6.7 % | ['N/A'] |
| /home/devops/.local/npm/bin/openspec archive add-initial-audit-field-redaction-v1 --skip-specs --yes --json | 1 | 6.7 % | [0] |
| Total | 15 | 100.0 % | — |

Chaque commande et écriture autorisée correspond à un requestId inédit, une décision CGPT explicite et une seule opération. Aucun chaînage ni opération implicite. Incidents : une commande true supplémentaire puis une inspection Bash non mandatée ont été refusées avant exécution. Un edit typographique avec chaînes identiques a échoué sans modifier le fichier. Les deux sessions ont été isolées, les sources et spécifications contrôlées inchangées, puis une session neuve READY et un CAB test neuf ont permis la reprise. L'apostrophe ASCII, factuellement correcte, a été acceptée sans réécriture. La course root de lecture/écriture du checkpoint a été corrigée par verrouillage du fichier existant, sans rejeu d'effet. Rapports OpenCode sur le code de retour qualifiés par les metadata effectivement disponibles côté CGPT.

## 5. Accès web

| Outils web natifs | Appels | Part | Exécutés | Refusés | Erreurs |
|---|---:|---:|---:|---:|---:|
| webfetch/websearch | 0 | 0.0 % | 0 | 0 | 0 |

Aucune URL visitée par un outil web de production. Appels fournisseur et sondes de service séparés. Aucun test navigateur ou PostgreSQL nécessaire pour ce profil mémoire ; aucun secret affiché ou transmis au modèle.

## 6. Synthèse globale

| Durée de session de codage | Valeur |
|---|---|
| Début | 2026-10-08T03:32:47.857000+00:00 UTC |
| Fin après archive et sonde finale | 2026-10-08T04:10:36.156901+00:00 UTC |
| Durée globale | 00 h 37 min 48 s |

| Quota Codex 7 jours | Relevé | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant | 2026-10-08T03:32:47.857000+00:00 | N/A | N/A |
| Après | 2026-10-08T04:10:36.156901+00:00 | N/A | N/A |
| Différence après - avant | — | N/A | — |

Outil natif usage_limits absent : aucune mesure de la fenêtre codex/10080 minutes disponible, aucune reconstruction ou conversion en coût/tokens. Quotas partagés par le compte.

| Domaine | Appels et part globale | Exécutés et taux | Refusés et taux | Erreurs et taux |
|---|---:|---:|---:|---:|
| Fichiers | 9 (13.8 %) | 8 (88.9 %) | 0 (0.0 %) | 1 (11.1 %) |
| Commandes | 15 (23.1 %) | 13 (86.7 %) | 2 (13.3 %) | 0 (0.0 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres outils | 41 (63.1 %) | 41 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total général | 65 (100.0 %) | 62 (95.4 %) | 2 (3.1 %) | 1 (1.5 %) |

Bilan : 79 tests réussis, 3 compilations, change strict et validation globale réussis selon critères applicables. Archive sans modification des canons, sept tâches prouvées. Trois sources nouvelles, aucune façade/configuration/dépendance/Git modifiée. Ce profil ne réalise ni occultation/pseudonymisation/minimisation effective ni audit persistant. SSE en direct, contrôle 3 s, vérifications de rédaction 7 s, sondes 30 min. L'ancienne échéance 08h00 a été révoquée ; clôture demandée après cette archive et ce rapport vérifié, sans change suivant.

Preuves non secrètes : output/cismp-state.json, historique natif ses_ee64ec32cffezU3f10dR4hG02g, mandats/propositions/metadata. La reprise normative audit précédente et le change tombstone sont hors intervalle de ce rapport.

Contexte des sources statistiques natives :

- ses_ee7d5a17bffeFr0I2iT6pQFZAg
- ses_ee656fa0cffef5KJGv7503Imfk
- ses_ee64ec32cffezU3f10dR4hG02g

Compactions OpenCode pendant cet intervalle : 0 parties natives observées. Compactage natif CGPT avant cet intervalle, télémétrie de service N/A ; API compact OpenCode HTTP 503 avant intervalle, qualifiée sans blocage ni arrêt du processus.

Validité des sondes : 40 lignes, aucun outil, modèle/provider/raisonnement imposés et deltas texte SSE mesurables. TTMT au premier delta texte ; débit = tokens sortie natifs / (dernier delta - premier delta). La tentative +30 min à une seule ligne est exclue des moyennes ; son unique reprise est conservée avec sa surcharge. La précision lexicale des lignes ne constitue pas une mesure.

Contrôle PLLM mode1 en cours de cycle, 2026-10-08T05:53:15+02:00 : rolling 5 %, weekly 81 %, monthly 60 %, tous statut ok et seuil non épuisé. Mesure fournisseur distincte du quota Codex indisponible ; aucune clé ni valeur d'authentification publiée.
