# PA10 — Statistiques cumulées du change

Provenance : change separate-pa-pzt-and-pbo-management-modules, RUN cismp8-pixs-6f9152399b784e97, job job-cismp8-7e99bb5260984b01850934d3242fc691, contexte 1372, checkpoint durable output/cismp/cismp8-pixs-6f9152399b784e97/state.json. SID métier conservé ses_e993fd94bffeOEqlArzTvDGgCV pour reprise après clôture. Données coupées le 2026-10-30T20:34:24.682Z avant cette rédaction, sans compter sa propre production. Lacune 17–21/10 explicitement N/A, sans reconstruction. Historique des 7 SID commençant le 22/10, change commençant le 17/10 heure inconnue. Nettoyage ciblé encore à faire, pas de fin de RUN déjà faite. Statut : change ouvert—dépendances manquantes—archivage en attente, voir [BLOCKERS.md](BLOCKERS.md).

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A | opencode-go | high | 2.4304800859641875 s sur 22 sondes | 371.45243736354416 sur 22 sondes | N/A |
| muse-spark-1.3-contributor | N/A | opencode-go | medium | 2.9773194650588235 s sur 17 valides | 251.03642803062436 sur 17 valides | N/A |
| muse-spark-1.3-contributor | N/A | opencode-go | default | N/A — 1 invalide hors moyenne | N/A — 1 invalide hors moyenne | N/A |

Ancien prompt 200 pour HIGH distinct du prompt 128 pour MEDIUM, sans fusion de configuration. MEDIUM : 17 valides sur 18 observées, 1 seul delta invalide. DEFAULT : 1 invalide, sans confondre reprise périodique et reprise unique. Version exacte N/A jamais déduite du nom. Dénominateur du temps de service absent car created et completed incluent attentes et outils, non assimilés au service, sans sonde de l’orchestrateur.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| GPT-6 selon instruction système | N/A | OpenAI | N/A | N/A | N/A | N/A |

Version et service N/A car manquants dans la télémétrie.

## 1. Statistiques générales et décisions

Portée lue, sept SID dédupliqués et neuf contextes.

| SID | Messages lus |
|---|---|
| ses_e9ae70150ffeBZeYuo8m0NK8yX | 205 |
| ses_e9a9bd360ffe3ehO8By2FlpaWG | 435 |
| ses_e9a16cf00ffe7C66ioOTeIySz3 | 12 |
| ses_e9a1019b9ffe5Lt0U9gZkm7Kn8 | 281 |
| ses_e99b7c1dbffe5KlPtd7RB00Z3U | 364 |
| ses_e9949b92fffeiuEVE7F2VS2Jtq | 16 |
| ses_e993fd94bffeOEqlArzTvDGgCV | 3357 |
| TOTAL | 4670 |

| Contexte | Approuvé | Rejeté |
|---|---|---|
| 620 | 95 | 5 |
| 905 | 50 | 0 |
| 1163 | 8 | 1 |
| 1172 | 5 | 0 |
| 1177 | 14 | 1 |
| 1216 | 1 | 0 |
| 1221 | 1 | 0 |
| 1263 | 4 | 0 |
| 1372 | 173 | 1 |
| TOTAL | 351 | 8 |

| Statut de décision | Nombre | Part |
|---|---|---|
| APPROVED | 351 | 97.8 % |
| REJECTED | 8 | 2.2 % |
| TOTAL | 359 | 100.0 % |

Terminée signifie statut technique, autorisée automatiquement ou manuellement, pas preuve d’APPROVED manuel. Once 347 non additionné aux demandes. Annulations au moins 3 documentées, sans inventer de total historique.

| Durée globale | Valeur |
|---|---|
| Début | 17 octobre 2026 — heure inconnue |
| Fin de phase | 30 octobre 2026 à 21:34:12.092 Europe/Paris |
| Durée globale | N/A — début horaire inconnu |
| Fin de change et archive | En attente — change ouvert |

| Quota | Valeur | Horodatage avec fuseau |
|---|---|---|
| Initial du change | N/A — relevé initial absent | N/A |
| Reprise | 63 % | 2026-10-30T04:38:28.287284+00:00 |
| Fin de phase | 100 % | 2026-10-30T20:34:24.538Z |
| Reset | 2026-11-04T06:45:53.000Z | identique aux deux relevés |
| Fenêtre | 10080 min | identique aux deux relevés |
| DIFF | N/A — identité du compte avant non capturée, quota partagé | N/A |

Les 37 points ne sont pas attribués au change.

| Performance des sondes | TTMT min | TTMT max | TPS min | TPS max | Succès | Échec | Manqués | Prévus |
|---|---|---|---|---|---|---|---|
| HIGH ancien prompt 200 | 1.098759972024709 s | 6.004891230957583 s | 119.99587411114025 | 1400.6648583685294 | 22 | 0 | N/A | N/A — horaire complet absent |
| MEDIUM prompt 128 | 1.372785427 s | 8.579799838000001 s | 183.3519220922079 | 610.8327587090366 | 17 | 1 invalide hors moyenne | N/A | N/A — horaire complet absent |
| DEFAULT prompt 128 | N/A | N/A | N/A | N/A | 0 | 1 invalide hors moyenne | N/A | N/A |

| Surcoût des sondes | Sortie | Raisonnement | Coût |
|---|---|---|---|
| DEFAULT invalide 1 | 392 | 131 | 0.00080204 |
| MEDIUM 18 observées | 7093 | 2903 | 0.0009543 |

| Token natif de l’assistant | Total | Connus sur 2648 réponses |
|---|---|---|
| Entrée | 62929480 | 2645 |
| Sortie | 1609712 | 2645 |
| Raisonnement | 609054 | 2645 |
| Cache lu | 882668295 | 2645 |
| Cache écrit | 0 | 2645 |
| Total natif | N/A — champ absent | N/A |
| Coût brut, devise N/A | 5.172970505999998 | 2645 |

Les 5 compteurs restent distincts sans total inventé. Sur 2648 réponses, 2645 avec télémétrie connue et 3 sans télémétrie. Les 15 compactages completed natifs ne sont pas additionnés à cette couche de tokens sans preuve.

Validation produit : 209 unitaires, 97 PG en 7 suites, 12 unités, strict 93 exit 0, limites locales sans archive ni Git ni live.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---|---|
| user | 1404 | 30.1 % |
| assistant | 2648 | 56.7 % |
| compaction | 15 | 0.3 % |
| system | 84 | 1.8 % |
| synthetic | 2 | 0.0 % |
| model-switched | 1 | 0.0 % |
| idle | 516 | 11.0 % |
| TOTAL | 4670 | 100.0 % |

| Fin | Nombre | Part |
|---|---|---|
| tool-calls | 1471 | 55.6 % |
| stop | 1167 | 44.1 % |
| N/A | 7 | 0.3 % |
| error | 3 | 0.1 % |
| TOTAL | 2648 | 100.0 % |

| Partie | Nombre | Part |
|---|---|---|
| text | 3669 | 41.9 % |
| reasoning | 3011 | 34.4 % |
| tool | 2072 | 23.7 % |
| TOTAL | 8752 | 100.0 % |

| Outil | Total | Terminées | Refus | Erreur | Part | Taux terminées | Taux refus | Taux erreur |
|---|---|---|---|---|---|---|---|
| cgpt-validation_broker_readiness | 349 | 349 | 0 | 0 | 16.8 % | 100.0 % | 0.0 % | 0.0 % |
| cgpt-validation_request_validation | 370 | 339 | 0 | 31 | 17.9 % | 91.6 % | 0.0 % | 8.4 % |
| bash | 200 | 198 | 0 | 2 | 9.7 % | 99.0 % | 0.0 % | 1.0 % |
| cgpt-validation_get_approval | 119 | 119 | 0 | 0 | 5.7 % | 100.0 % | 0.0 % | 0.0 % |
| read | 556 | 549 | 0 | 7 | 26.8 % | 98.7 % | 0.0 % | 1.3 % |
| glob | 43 | 43 | 0 | 0 | 2.1 % | 100.0 % | 0.0 % | 0.0 % |
| grep | 41 | 41 | 0 | 0 | 2.0 % | 100.0 % | 0.0 % | 0.0 % |
| cgpt-validation_broker_health | 99 | 99 | 0 | 0 | 4.8 % | 100.0 % | 0.0 % | 0.0 % |
| cgpt-validation_list_pending | 99 | 99 | 0 | 0 | 4.8 % | 100.0 % | 0.0 % | 0.0 % |
| cgpt-validation_broker_remediation_registry | 3 | 3 | 0 | 0 | 0.1 % | 100.0 % | 0.0 % | 0.0 % |
| edit | 40 | 40 | 0 | 0 | 1.9 % | 100.0 % | 0.0 % | 0.0 % |
| write | 109 | 109 | 0 | 0 | 5.3 % | 100.0 % | 0.0 % | 0.0 % |
| cgpt-validation_poll_approval | 25 | 15 | 0 | 10 | 1.2 % | 60.0 % | 0.0 % | 40.0 % |
| todowrite | 3 | 2 | 0 | 1 | 0.1 % | 66.7 % | 0.0 % | 33.3 % |
| cgpt-validation_broker_auto_remediation_policy | 1 | 1 | 0 | 0 | 0.0 % | 100.0 % | 0.0 % | 0.0 % |
| cgpt-validation_cancel_approval | 6 | 6 | 0 | 0 | 0.3 % | 100.0 % | 0.0 % | 0.0 % |
| cab_codemode_discovery | 2 | 2 | 0 | 0 | 0.1 % | 100.0 % | 0.0 % | 0.0 % |
| execute | 6 | 6 | 0 | 0 | 0.3 % | 100.0 % | 0.0 % | 0.0 % |
| cgpt-validation_reject | 1 | 1 | 0 | 0 | 0.0 % | 100.0 % | 0.0 % | 0.0 % |
| TOTAL | 2072 | 2021 | 0 | 51 | 100.0 % | 97.5 % | 0.0 % | 2.5 % |

## 3. Fichiers modifiés

149 tentatives fichiers sur 64 chemins natifs, toutes terminées techniques, pas 149 accords manuels. Absence d’archive et de déplacement pour ce RUN.

| Chemin | Total | Terminées | Refus | Erreur | Part | Taux terminées | Taux refus | Taux erreur |
|---|---|---|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/separate-pa-pzt-and-pbo-management-modules/design.md | 3 | 3 | 0 | 0 | 2.0 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/separate-pa-pzt-and-pbo-management-modules/tasks.md | 18 | 18 | 0 | 0 | 12.1 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/contracts.py | 2 | 2 | 0 | 0 | 1.3 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/__init__.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_agent_management_contracts.py | 2 | 2 | 0 | 0 | 1.3 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_agent_management_contracts_boundary.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/component.toml | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/apps.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_agent_manifest.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_agent_manifest_integration.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/identifiers.py | 3 | 3 | 0 | 0 | 2.0 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/models.py | 7 | 7 | 0 | 0 | 4.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/repository.py | 2 | 2 | 0 | 0 | 1.3 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/migration_lock.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/migrations/__init__.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/migrations/0001_agent_initial.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_agent_storage_codec.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/agent_pg_test_support.py | 7 | 7 | 0 | 0 | 4.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_agent_storage_postgres.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/ports.py | 2 | 2 | 0 | 0 | 1.3 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_agent_service_ports.py | 3 | 3 | 0 | 0 | 2.0 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/audit_adapter.py | 2 | 2 | 0 | 0 | 1.3 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_agent_audit_adapter_postgres.py | 2 | 2 | 0 | 0 | 1.3 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/authorization.py | 2 | 2 | 0 | 0 | 1.3 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_agent_authorization_postgres.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/service.py | 4 | 4 | 0 | 0 | 2.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_agent_management_service_postgres.py | 7 | 7 | 0 | 0 | 4.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/lifecycle.py | 6 | 6 | 0 | 0 | 4.0 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/adapter.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/supervision.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/agent_service_test_support.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_agent_adapter_postgres.py | 2 | 2 | 0 | 0 | 1.3 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_agent_supervision_postgres.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/README.md | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/CHANGELOG.md | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/separate-pa-pzt-and-pbo-management-modules/RACCORDS.md | 5 | 5 | 0 | 0 | 3.4 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/separate-pa-pzt-and-pbo-management-modules/RECETTE_RACCORDS.md | 5 | 5 | 0 | 0 | 3.4 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_agent_pa_native_contract_boundary.py | 2 | 2 | 0 | 0 | 1.3 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_agent_identifiers_v2.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/DEVELOPMENT_MAP.md | 13 | 13 | 0 | 0 | 8.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/contracts_v2.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_agent_contracts_v2.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/documents.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_agent_documents.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/migrations/0002_agent_payload_document.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_agent_payload_document_postgres.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/fact_inventory.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_agent_fact_inventory.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/migrations/0003_agent_payload_provenance.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/_registry_support.py | 4 | 4 | 0 | 0 | 2.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_agent_payload_provenance_postgres.py | 2 | 2 | 0 | 0 | 1.3 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/migrations/0004_agent_pa_binding.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_agent_pa_binding_postgres.py | 3 | 3 | 0 | 0 | 2.0 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/migrations/0005_agent_pa_relay.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_agent_pa_relay_postgres.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/relay_observation.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_agent_relay_observation.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/relay_composition.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_agent_relay_composition.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/resolution_receipt.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/unit/test_agent_resolution_receipt.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/src/pixs/agent/relay_store.py | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/tests/integration/test_agent_relay_store_postgres.py | 2 | 2 | 0 | 0 | 1.3 % | 100.0 % | 0.0 % | 0.0 % |
| /home/devops/datas/pixs/openspec/changes/separate-pa-pzt-and-pbo-management-modules/BLOCKERS.md | 1 | 1 | 0 | 0 | 0.7 % | 100.0 % | 0.0 % | 0.0 % |
| TOTAL | 149 | 149 | 0 | 0 | 100.0 % | 100.0 % | 0.0 % | 0.0 % |

## 4. Commandes

Refus de commandes explicites 0 dans cette collecte, aucun libellé refusé à restituer. Terminées 198 avec 2 erreurs ne sont pas 198 tests PASS.

| Famille | Total | Terminées | Refus | Erreur | Part | Taux terminées | Taux refus | Taux erreur |
|---|---|---|---|---|---|---|---|
| Prévol | 26 | 26 | 0 | 0 | 13.0 % | 100.0 % | 0.0 % | 0.0 % |
| OpenSpec | 20 | 19 | 0 | 1 | 10.0 % | 95.0 % | 0.0 % | 5.0 % |
| Syntaxe | 41 | 41 | 0 | 0 | 20.5 % | 100.0 % | 0.0 % | 0.0 % |
| Tests | 90 | 90 | 0 | 0 | 45.0 % | 100.0 % | 0.0 % | 0.0 % |
| Autres | 23 | 22 | 0 | 1 | 11.5 % | 95.7 % | 0.0 % | 4.3 % |
| TOTAL | 200 | 198 | 0 | 2 | 100.0 % | 99.0 % | 0.0 % | 1.0 % |

| Sortie | Nombre | Part |
|---|---|---|
| zéro | 185 | 92.5 % |
| non-zéro | 13 | 6.5 % |
| absent | 2 | 1.0 % |
| TOTAL | 200 | 100.0 % |

Terminées 198 avec 2 erreurs ne sont pas 198 tests PASS.

## 5. Accès web

Part sur dénominateur 2072 pour 0 %, taux sur 0 restant N/A. API loopback, SSE et connexion LLM non comptés comme web.

| Domaine | Appels | Part | URLs | Taux succès | Taux refus | Taux erreur |
|---|---|---|---|---|---|---|
| web natif | 0 | 0.0 % | aucune | N/A | N/A | N/A |
| TOTAL | 0 | 0.0 % | aucune | N/A | N/A | N/A |

Dénominateur 0, taux N/A.

## 6. Synthèse globale

| Domaine | Total | Part | Terminées | Refus | Erreur | Taux terminées | Taux refus | Taux erreur |
|---|---|---|---|---|---|---|---|
| files | 149 | 7.2 % | 149 | 0 | 0 | 100.0 % | 0.0 % | 0.0 % |
| commands | 200 | 9.7 % | 198 | 0 | 2 | 99.0 % | 0.0 % | 1.0 % |
| web | 0 | 0.0 % | 0 | 0 | 0 | N/A | N/A | N/A |
| other | 1723 | 83.2 % | 1674 | 0 | 49 | 97.2 % | 0.0 % | 2.8 % |
| TOTAL | 2072 | 100.0 % | 2021 | 0 | 51 | 97.5 % | 0.0 % | 2.5 % |

Bilan fin : 209 unitaires PASS, 97 critères PG PASS en 7 suites, 12 unités dont 7 pures et 5 PG, W045 x1 connu avec 0 erreur, 11 tables et 5 migrations TEST, S1 et Agent2 non activés, v1 préservé. Strict ciblé 93 exit 0, pas de qualification runtime, pas d’archive ni Git pour ce RUN. Native OpenCode 2.2.0 conservée, CAB 28 effectif.

| Durée globale | Valeur |
|---|---|
| Début | 17 octobre 2026 — heure inconnue |
| Fin de phase | 30 octobre 2026 à 21:34:12.092 Europe/Paris |
| Durée globale | N/A — début horaire inconnu |
| Fin de change et archive | En attente — change ouvert |

| Quota | Valeur | Horodatage avec fuseau |
|---|---|---|
| Initial du change | N/A — relevé initial absent | N/A |
| Reprise | 63 % | 2026-10-30T04:38:28.287284+00:00 |
| Fin de phase | 100 % | 2026-10-30T20:34:24.538Z |
| Reset | 2026-11-04T06:45:53.000Z | identique aux deux relevés |
| Fenêtre | 10080 min | identique aux deux relevés |
| DIFF | N/A — identité du compte avant non capturée, quota partagé | N/A |

Les 37 points ne sont pas attribués au change. Distinction observée : 0 refus d’outils explicites dans ce classement, 8 rejets CAB dans un compteur distinct non additionné. Type de décisions auto ou manuelles N/A quand non attribuable.
