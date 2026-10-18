# Tâches — Représentation Enum des phases BulkJob B08

## 1. Vocabulaire structurel pur

- [x] 1.1 Publier `src/pixs/kernel/bulk_job_phase.py` : `BulkJobPhase(Enum)` aux quatre membres canoniques `STAGE`, `VALIDATE`, `APPLY`, `EXPORT`, docstring de frontière, `__all__`, sans mixin `str`, alias, défaut, validation ni runtime, sans façade ni `__init__` modifiés.
- [x] 1.2 Publier et exécuter le test unitaire `tests/unit/test_bulk_job_phase.py` : adhésion exacte aux noms/valeurs et à l'ordre canonique B08, absence de membre supplémentaire, refus sans normalisation, frontière explicite entre Enum et chaînes canoniques ; les vrais validateurs existants sont couverts par les régressions distinctes, sans les modifier.
- [x] 1.3 Publier et exécuter le test d'intégration `tests/integration/test_bulk_job_phase_integration.py` : import et adhésion dans un processus frais sous gardes éprouvées, sans effet observable.
- [x] 1.4 Exécuter les compilations ciblées des trois nouveaux fichiers et les régressions structurelles utiles (`test_bulk_operation_commit_mode`, `test_bulk_operation_status`, `test_bulk_operation_conflict et test_bulk_runtime_records`), sans tests PostgreSQL ; contrôler les résultats natifs, UTF-8/LF et les empreintes des sources non concernées.

- [x] 1.5 Exécuter les validations OpenSpec ciblée stricte, globale standard et globale stricte ; conserver leurs codes et avertissements réels.
- [x] 1.6 Vérifier le périmètre et les preuves avant décision distincte d'archivage.

Aucune tâche d'archivage ni de rapport de statistiques ; l'archivage et le rapport STATISTIQUES.md relèvent de décisions et mandats CGPT distincts après preuve des tâches.

<!-- DB/frontend: N/A — vocabulaire pur sans PostgreSQL ni frontend. -->

## Preuves exécutées

- Prévol PLLM mode 1 Muse high courant valide ; test CAB exact /usr/bin/true avec once, code 0, READY final.
- Sept fichiers nouveaux aux contenus exacts relus, UTF-8/LF ; empreintes des onze fichiers existants suivis inchangées. Aucun canon, runtime, façade ni __init__ modifié.
- Compilation py_compile des trois fichiers Python : code 0.
- Tests ciblés et régressions : 32/32 OK, dont trois nouveaux tests ; import frais sous gardes éprouvées, modèles/validateurs Bulk existants testés sans connexion PostgreSQL.
- Validation OpenSpec ciblée stricte : code 0 ; skip_specs reconnu, aucun delta fonctionnel.
- Global standard : 186/186, code 0. Global strict : 184/186, code 1 ; quatre WARNING historiques de longueur (bulk-operations exigences 6/10/13 ; identity-assurance exigence 4), zéro ERROR. Résultat conservé sans correction hors périmètre.
- Une demande de proposition à révision inconnue a été annulée avant effet ; demande neuve corrélée ensuite exécutée, sans réutilisation de permission.
- PostgreSQL et frontend : N/A pour ce vocabulaire passif ; aucune dépendance, migration, activation runtime ni opération Git.
- L’archivage et les statistiques restent des mandats distincts, non revendiqués par les coches ci-dessus.
