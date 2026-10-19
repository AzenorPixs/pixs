# Tasks — add-initial-capability-criticality-vocabulary-v1

## 1. Préparation et implémentation

- [x] 1.1 Vérifier component-model, capabilities, absence de vocabulaire existant et valider le périmètre NFDOC.
- [x] 1.2 Créer les quatre artefacts OpenSpec cohérents, sans delta normatif artificiel.
- [x] 1.3 Ajouter CapabilityCriticality sans effet ni modification des consommateurs, façades ou manifests.
- [x] 1.4 Ajouter les tests unitaires et l'import isolé avec gardes d'effets.

## 2. Validation et clôture

- [x] 2.1 Compiler les deux nouveaux fichiers Python et exécuter les tests ciblés et régressions applicables.
- [x] 2.2 Exécuter la validation OpenSpec ciblée stricte, globale standard et stricte ; distinguer échecs et avertissements historiques.
- [x] 2.3 Vérifier contenu, UTF-8/LF, absence d'écriture hors périmètre et conformité aux cadrages.
- [x] 2.4 Présenter toutes les preuves à CGPT et obtenir son autorisation distincte pour l'archivage unique.

Le rapport STATISTIQUES.md est exigé après archivage, sous mandat distinct, avant gate et livraison. Aucun Git autorisé.

## Modules de test

test_modules: ["tests.unit.test_capability_criticality", "tests.unit.test_manifest_models", "tests.unit.test_manifest_schema1", "tests.unit.test_capability_resolution"]

## Preuves examinées par Codex

- Deux fichiers Python compilés séparément : code 0.
- Six modules ciblés : 97 tests réussis, code 0, dont import frais sous gardes positives.
- OpenSpec ciblé strict : code 0, aucun delta normatif requis (skip_specs:true).
- OpenSpec global standard : 187/187, code 0.
- OpenSpec global strict : 185/187, code 1 ; quatre avertissements de longueur préexistants (bulk-operations exigences 6/10/13 ; identity-assurance exigence 4), aucune ERROR ; aucun canon corrigé hors périmètre. Ce résultat ne constitue pas une réussite stricte globale.
- Six fichiers relus et vérifiés UTF-8/LF ; module et tests conformes aux contenus approuvés. Un littéral de test divergent a été corrigé sous mandat neuf avant exécution.
- Empreintes des cadrages, canons component-model/capabilities, façade Kernel, manifest/models.py, capabilities.py et lifecycle/availability.py inchangées.
- Archivage unique explicitement autorisé par Codex après examen des preuves ; STATISTIQUES.md obligatoire sous mandat distinct après archivage.
- PostgreSQL et frontend sans objet pour ce vocabulaire pur ; Git non inspecté et non autorisé. Le cycle global reste incomplet.
