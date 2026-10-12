# Tâches — Vocabulaire des variantes d’opération en masse

- [x] 1. Vérifier les quatre artefacts UTF-8/LF, le delta identique au canon et réussir la validation stricte du change avant code.
- [x] 2. Ajouter uniquement BulkOperationVariant IMPORT/EXPORT au module existant, conserver BulkCommitMode et la façade, puis réussir compilation, inspection AST et import en processus neuf.
- [x] 3. Réussir les suites existantes de pureté du noyau, façades et vocabulaires voisins ; consigner résultats et codes natifs.
- [x] 4. Réussir la validation finale OpenSpec et contrôler UTF-8/LF, les seules cibles autorisées et les empreintes initiales.

Aucune tâche n’est cochée avant preuve. Ce vocabulaire ne livre pas le contrat BulkOperation complet. Archivage et STATISTIQUES.md restent deux mandats distincts après ces preuves.

## Preuves de clôture

- Quatre artefacts exacts UTF-8/LF et delta canon identique ; strict précode code 0 conservé sans rejeu.
- Module exact, AST et exports inspectés par CGPT ; BulkCommitMode conservé, façade inchangée, 350 empreintes préservées.
- Compilation et import en processus neuf réussis, codes natifs 0.
- 20 tests réussis : pureté 3, façades 11, JobState 3, NotificationChannel 3 ; aucun échec ni skip.
- Change final strict : code natif 0. Canon global : 63 passed / 13 failed warning-only, exit natif 1 ; 21 avertissements de longueur, zéro ERROR, 76 fichiers canoniques inchangés. Résultat qualifié selon le critère développeur excluant la longueur, pas présenté comme une réussite native globale.
- Demandes divergentes refusées sans effet ; délais MCP résolus par polling corrélé ; aucune permission réutilisée.

Archivage et STATISTIQUES.md restent des mandats distincts.
