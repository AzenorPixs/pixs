# Tâches — États d'opération en masse v1

- [x] 1. Vérifier les quatre artefacts UTF-8/LF, le delta identique au requirement canonique et la validation stricte avant code.
- [x] 2. Ajouter le seul vocabulaire BulkOperationState de dix noms ; préserver octet pour octet les trois Enum et la façade ; réussir compilation, import neuf et AST/exports.
- [x] 3. Réussir les suites existantes pureté, façades, JobState et NotificationChannel ; consigner leurs preuves natives.
- [x] 4. Valider OpenSpec et les seules cibles autorisées ; conserver les empreintes des fichiers non concernés.

Aucune tâche n'est cochée avant preuve. Aucun runtime, transition, alias, défaut,
terminalité ni rattachement à Job. Pas de test miroir d'Enum ni de fichier de test
modifié. Archivage et STATISTIQUES.md restent des mandats distincts.

Preuves CGPT : quatre artefacts UTF-8/LF, delta identique au canon, validation stricte avant et après code 1/1 (codes 0) ; compilation et import en processus neuf codes 0 ; revue AST de déclarations seules, dix noms=valeurs sans alias, trois Enum et façade préservés ; 20 tests natifs réussis (3 pureté, 11 façades, 3 JobState, 3 NotificationChannel) ; empreintes hors module conservées, dont les 76 spécifications canoniques. Canon global validé après RSMP 76/76, zéro issue, code 0. Aucun runtime, transition ou persistance.
