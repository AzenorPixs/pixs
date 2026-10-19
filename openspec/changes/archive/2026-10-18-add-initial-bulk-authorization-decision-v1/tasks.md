# Tâches — add-initial-bulk-authorization-decision-v1

## 1. Préparation et implémentation

- [x] 1.1 Vérifier le canon AuthorityAssessmentV1, l’absence d’équivalent exporté et le NFDOC.
- [x] 1.2 Créer les quatre artefacts OpenSpec sans delta normatif artificiel.
- [x] 1.3 Ajouter BulkAuthorizationDecision passif sans modifier les consommateurs existants.
- [x] 1.4 Ajouter les tests du contrat, la non-substitution des chaînes et l’import isolé sans effet.

## 2. Validation et clôture

- [x] 2.1 Compiler les trois fichiers Python et exécuter les tests ciblés et régressions applicables.
- [x] 2.2 Exécuter les validations OpenSpec ciblée stricte, globale standard et globale stricte ; distinguer les avertissements préexistants.
- [x] 2.3 Vérifier contenus, UTF-8/LF, cohérence avec les cadrages et absence d’écriture hors périmètre.
- [x] 2.4 Présenter les preuves et obtenir l’autorisation distincte de Codex pour l’archivage unique.

STATISTIQUES.md est obligatoire après archivage, sous mandat distinct, avant gate et livraison. Arrêt ciblé de CISMP6 après ce seul change ; aucun Git autorisé.

## Preuves examinées par Codex

- Prévol CAB exact, once, code 0 puis READY.
- Sept fichiers relus à l’identique, UTF-8/LF, sans modification des cadrages, du canon ni des consommateurs (empreintes inchangées).
- Trois fichiers Python compilés, code 0.
- 75 tests ciblés et régressions Bulk réussis, code 0.
- OpenSpec ciblé strict : code 0. Global standard : 187/187, code 0.
- Global strict : 184/186, code 1 ; quatre warnings historiques de longueur (bulk-operations exigences 6/10/13, identity-assurance exigence 4), zéro ERROR. Aucune correction hors périmètre. Les nombres globaux évoluent avec les archives concurrentes.
- Archivage unique autorisé par Codex après revue de ces preuves ; rapport STATISTIQUES.md obligatoire ensuite.
- Git non inspecté et aucune opération Git exécutée. PostgreSQL et frontend sans objet. Cycle global incomplet ; arrêt de CISMP6 après ce seul change.
