# Tâches — Vocabulaire des modes d’import en masse

- [x] 1. Vérifier les quatre artefacts UTF-8/LF, le delta identique au canon, et réussir la validation stricte du change avant code.
- [x] 2. Ajouter le seul module interne BulkCommitMode aux quatre membres canoniques, sans façade ni dépendance, puis réussir sa compilation.
- [x] 3. Vérifier l’import isolé, les membres et l’export ; réussir les suites existantes de pureté du noyau, façades et vocabulaires voisins.
- [x] 4. Réussir la validation finale OpenSpec ; vérifier UTF-8/LF, les seules cibles autorisées et les empreintes des fichiers préexistants.

Une tâche n’est cochée qu’après ses preuves. Le vocabulaire ne constitue pas une implémentation de l’import effectif ou du contrat BulkOperation complet. Archivage et STATISTIQUES.md restent deux mandats distincts après les quatre tâches prouvées.

## Preuves de clôture

- Quatre artefacts UTF-8/LF ; delta MODIFIED identique à l’exigence canonique et son scénario.
- Canon bulk-operations et change avant code : validations strictes, codes natifs 0.
- Module relu (AST : quatre membres nom=valeur, export unique) ; py_compile avec Python déclaré, code natif 0.
- Chargement du module en processus neuf via -B -m, code natif 0 ; l’inspection -c initiale a été refusée avant exécution pour échappement divergent et n’est pas une preuve.
- Tests existants : 14 intégration de pureté/façades et 6 unitaires des vocabulaires voisins, soit 20 réussis, aucun échec ni skip ; codes natifs 0.
- Change final strict : code natif 0 ; cinq fichiers autorisés UTF-8/LF et empreintes des cadrages, canon, dépendances et façade initiale inchangées.
- Écarts de pilotage refusés sans effet ; trois transferts de session via job/recover avec prévol neuf, réponse MCP corrélée, permission unique et READY pending0. Résultats réussis conservés.

Archivage et STATISTIQUES.md restent des mandats distincts après ces preuves.
