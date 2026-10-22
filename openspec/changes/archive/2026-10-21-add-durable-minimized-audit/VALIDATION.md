# Validation locale — C05

## État et identité

Validation du propriétaire d’audit durable, autorisée par `1CISMP2` et la reprise explicite du même RUN après correction CAB par CISMP1.

- RUN : `cismp2-pixs-968e38f3e27b4bbf`.
- Session native persistante : `ses_ea598af07fferBsu2YA9oOfSGT`.
- Job de reprise : `c2-c05-resume-36f19ec899c54f79`.
- Change : `add-durable-minimized-audit`.
- Checkpoint non versionné : `output/cismp/cismp2-pixs-968e38f3e27b4bbf/state.json`.
- PostgreSQL observé : `160014` (16.14) ; Django observé : `6.1.2` ; interpréteur de test : `.venv/bin/python3`.

Ce document prouve les contrôles locaux ci-dessous. Il est établi avant l’archivage ; le résultat d’archive, les statistiques postarchive, la publication CAB et le gate restent distincts, vérifiables dans le rapport réel `STATISTIQUES.md` et le checkpoint. Aucun état terminal n’est déduit d’une présence de code ou d’une case cochée.

## Résultats exécutés

| Contrôle | Résultat | Preuve native requestId |
|---|---|---|
| Compilation et empreintes des neuf Python courants | 9/9, UTF-8/LF, cache nettoyé | `c2-cmd-223abf61bb23425fae75bc30038b98f6` |
| Canons référencés | 9/9 identiques | `c2-cmd-223abf61bb23425fae75bc30038b98f6` |
| Régressions ciblées Core/Kernel/C01/audit | 224 réussies, 0 erreur/échec/skip | `c2-cmd-223abf61bb23425fae75bc30038b98f6` |
| Recette C05 PostgreSQL réelle | 35/35, schéma nettoyé, connexions fermées | `c2-cmd-223abf61bb23425fae75bc30038b98f6` |
| État historique et modèles Django | Aucune dérive, backend dummy, sans accès PG | `c2-cmd-e2f5401efa464d03bede3495cc27ea44` |
| Validation OpenSpec stricte du seul C05 | 1/1 valide, issues vide | `c2-cmd-db1fb3b539e442b7822ad1683bc2fa2b` |

Les contrôles ne sont pas additionnés comme des tests unitaires homogènes : 224 tests de suite et 35 scénarios PG sont deux périmètres distincts. La compilation et le strict ne remplacent pas la recette.

## Scénarios PostgreSQL finaux

| Scénario | Verdict |
|---|---|
| `anonymisation_autorisee` | Réussi |
| `c01_collision_rollback_lot` | Réussi |
| `c01_ouvert_refuse` | Réussi |
| `c01_rejeu_et_reconciliation_sans_reexecution` | Réussi |
| `c01_reponse_perdue_apres_commit` | Réussi |
| `c01_transfert_atomique_ordre_hash_et_commit_independant` | Réussi |
| `candidats_c4_prives_bornes_et_isoles` | Réussi |
| `candidats_c4_surcharge_refusee_sans_tronquage` | Réussi |
| `capacite_lecture_politique_explicite` | Réussi |
| `capacite_politique_et_contexte` | Réussi |
| `contrainte_sql_triplet_maintenance` | Réussi |
| `core_service_audit_indisponible_refus_ferme` | Réussi |
| `core_service_ordinaire_audit_pg_commun` | Réussi |
| `core_service_rollback_et_refus_durable` | Réussi |
| `d13_auth_et_audit_communs` | Réussi |
| `d13_echec_avant_commit_aucun_acces` | Réussi |
| `d14_observation_autorite_fraiche_et_source_committe` | Réussi |
| `d14_observation_historique_commit_commun` | Réussi |
| `d14_observation_reponse_perdue_sans_rejeu` | Réussi |
| `d14_observation_source_non_verifiable_refusee` | Réussi |
| `d14_retrait_seul_et_reference_sans_audit_fictif` | Réussi |
| `derogation_c4_synthetique_sans_audit_fictif` | Réussi |
| `durabilite_visibilite_commit` | Réussi |
| `filtrage_perime_refuse` | Réussi |
| `filtrage_source_et_audit` | Réussi |
| `idempotence_collision` | Réussi |
| `immutabilite_orm_sql` | Réussi |
| `isolation_tenant_a_la_source` | Réussi |
| `legal_hold_refuse_purge` | Réussi |
| `pdp_inconnus_et_refus_sans_decision` | Réussi |
| `preuve_transaction_distincte_refusee` | Réussi |
| `purge_tombstone_et_reconciliation` | Réussi |
| `retention_et_job_courants` | Réussi |
| `retour_migration_non_vide_refuse` | Réussi |
| `rollback_commun` | Réussi |

Le cas de refus vérifie aussi un acteur connu conservé après contrôle frais, un DENY courant conservant son acteur vérifié et None lorsque le contexte/identité n’est pas vérifiable. La revue a corrigé cette omission avant livraison.

## Empreintes des sources effectivement compilées

| Chemin projet | SHA-256 |
|---|---|
| `src/pixs/core/audit_access.py` | `c38a79104ead9b7bbf657ad7e54174ab39f51e8a2ea87713d8a2e7981527ee8e` |
| `src/pixs/core/audit_bootstrap_import.py` | `4d811bf7dbf91274c61f78421712568c4635b5e4d59262ea8c968892e495fd1a` |
| `src/pixs/core/audit_contracts.py` | `08bff8da6140e22747b6bf37477781c58ed72c95078584cee6de2f5918c9aa77` |
| `src/pixs/core/audit_sink.py` | `8114fd5768b1633ae8c0e0d065b8d820b51cdd1b6db46d8f27f8696a46320926` |
| `src/pixs/core/migrations/0002_core_audit.py` | `95602cdf0724519a88640221e44db4f42e7203ba937ae72f66335652e152fac7` |
| `src/pixs/core/models.py` | `4e78fc85dfb7b7f65ac52d9b7f87f4e409dfc7e2123dd9dddee1c857a93baaee` |
| `src/pixs/core/persistence/models_audit.py` | `8a2db2c5fe8cdad44b5b089cfce78f0d38c2053140006fb49172eeefb62d5539` |
| `tests/integration/test_core_audit_durable.py` | `870c13e1776f2caeab0994eb9e87cc19a4675f8296befa11872c93165918a868` |
| `tests/unit/test_core_audit_sink.py` | `bdcb6dd96fe6d51a68754504e6e8cf24baf7bc2b6c22ade44bbd5891beacc646` |

## Empreintes canoniques préservées

| Chemin canonique | SHA-256 attendu et observé |
|---|---|
| `openspec/specs/audit/spec.md` | `19c58dc8b16e537967c46e69fca4132867e98ada591980b67872ee8c382a5eb1` |
| `openspec/specs/authorization-engine/spec.md` | `bd9de765f72d4700da314f81dbce9d3d0ee532f3bcc5be319f005ffbfd18b20b` |
| `openspec/specs/authorization/spec.md` | `c09e4dac79ecbe6bdb16550d8a4d1566307127818cdeaf9dfbe9224f50858310` |
| `openspec/specs/data-governance/spec.md` | `85c5176f49270a9eb45a51329fc200f8d1cb293bfa6bc93e62eb7fe88999ddfe` |
| `openspec/specs/data-lifecycle/spec.md` | `a3498cc4d3622d569fc9e3f8251a5c5324a9b3d1c612fe014618146297083426` |
| `openspec/specs/observability/spec.md` | `4793cf6252768ea2673a4eb843caf027fb850b586a8fcfee877b5d37d1e6ff98` |
| `openspec/specs/operations/spec.md` | `13835ff9b1d97cf4196a66f2f991f25f0d5c0357ccc54c7bcd1d56dffe38d5f1` |
| `openspec/specs/secrets-providers/spec.md` | `fa537fca310131c63fae0130d0b30699964c6fa08d709afacc6c5ed153b00b3b` |
| `openspec/specs/security/spec.md` | `c033c6fa6a6fc43d6e7e3295cd7dc7f554bbcbe0c12cb9baf0431acd6f7a685f` |

## Périmètre de la recette

Le stockage, la migration, le trigger, les transactions PostgreSQL, la consultation, la maintenance et le transfert C01 sont réels. Les trois scénarios `core_service_*` exécutent les services Core ordinaires existants avec le participant d’audit réel.

Auth est un propriétaire synthétique privé de test, pas le runtime C03. C4, gouvernance/C10, Jobs/lifecycle, idempotence et outbox sont des ports synthétiques explicitement identifiés. Les deux points propriétaires de candidats et ownership C05 sont réels ; leur composition C4 produit finale reste à qualifier chez C04. Aucune session réelle, aucun nouveau jeton, provider, endpoint, worker ou activation P0 n’est livré par ces fixtures.

La recette D14 conserve un instant de retrait ancien et une identité source stable. Le vérificateur Auth synthétique contrôle une provenance committée et une autorité fraîche, indépendamment d’un ancien ALLOW ; rollback et commit commun de la résolution sont exercés. Une observation déjà committée est confirmée depuis le peer sans réinsertion et sans réutilisation d’un ancien stage. Le propriétaire Auth reste responsable de ses contrôles courants avant de solder pending.

Les cinq valeurs PG ne quittent pas le processus de test : parsing borné, sorties masquées, erreurs rédigées, schéma aléatoire strictement possédé, suppression conditionnée à cette propriété et connexions fermées. Les journaux C01 de régression sont redirigés vers le cache privé possédé du RUN ; aucun journal opérationnel n’est ouvert par l’agent. Les nettoyages du schéma, des connexions et des répertoires temporaires sont prouvés.

## Échecs et reprises bornés

La première recette a validé cinq cas puis rencontré une fixture PDP invalide : le constructeur refusait déjà ALLOW/DENIED avant le test du sink. La fixture a été corrigée pour tester une requête ALLOW structurellement valide sans décision ; le refus attendu par C05 est ensuite exercé.

Une première régression de 224 tests a eu 223 succès et un échec de harnais : le sous-processus d’import Core ne recevait pas `src` via PYTHONPATH. Seule la commande de test a été corrigée ; la suite finale de 224 tests passe sans skip. Les réussites finales ne masquent pas ces tentatives.

Les commandes/identifiants/révisions natifs divergents ont été refusés avant once ou annulés lorsqu’ils restaient PENDING sans admission au contrôleur. Les décisions déjà consommées sont conservées et jamais rejouées. Une séquence Unicode de fixture a été corrigée avant exécution ; une ligne blanche supplémentaire sans différence fonctionnelle a été revue et conservée avec les deux empreintes dans le checkpoint. Les métriques détaillées de ces tentatives appartiennent au rapport statistique.

## Revue, migration et limites

Le périmètre C05 comprend les neuf fichiers Python listés plus les documents du change et les compléments minimaux PROJECT/TECHNICAL/README. Le code des autres RUN, leurs dépendances et les profils structurels existants sont préservés. Aucun Git, nouvelle dépendance C05, configuration OpenCode, service partagé ou déploiement n’est mandaté.

La migration ajoute le seul modèle CoreAuditEvent et une garde transactionnelle PostgreSQL. Son retour refuse explicitement une table d’audit non vide. Le schéma C02 historique reste inchangé. La garde append-only couvre les voies ordinaires ; elle ne protège pas contre un DBA ou un rôle hostile capable de modifier les paramètres de session. L’intégrité cryptographique avancée reste C16.

La classification et les références minimales proviennent des propriétaires de confiance. Les règles de minimisation s’appliquent avant écriture ; il n’existe ni payload avant/après libre ni prétention de détection sémantique universelle d’un secret. Aucun audit absent n’est annoncé sous une dérogation C4 vérifiée.

Aucune qualification complète de C03/C04/C06/C08/C09/C10/C13/C16, de la composition P0 ou du paquet n’est déduite. C17/C18/C19 restent requis. Le frontend, les navigateurs, les chemins d’exploitation non sélectionnés et les autres versions Python ne sont pas testés par cette recette : aucun de leurs fichiers ou runtimes n’est modifié ici. Les outils de lint/types ne sont pas configurés dans pyproject.toml pour ce périmètre.

## Clôture attendue

L’archivage du seul C05 reste explicitement autorisé, sans `--skip-specs` ni `--no-validate`. Le delta déjà adopté reste conservé ; aucun nouveau scénario canonique n’est autorisé. Après succès, publier les révisions CAB et passer à la phase REPORT, produire par mandat distinct le seul `STATISTIQUES.md` de l’archive réelle, vérifier six sections, UTF-8/LF et totaux, puis obtenir le gate et l’arrêt ciblé du RUN. Un rapport échoué est repris sans réarchiver. Aucun change suivant ni arrêt d’OpenCode, du broker ou des services communs.
