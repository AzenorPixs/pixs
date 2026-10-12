# Tâches — Formats de référence

- [x] 1. Vérifier les quatre artefacts UTF-8/LF, le delta identique au canon et la validation stricte avant code.
- [x] 2. Ajouter le seul vocabulaire de références CSV/NDJSON ; conserver les deux Enum existants et la façade ; réussir compilation, import neuf et AST/exports.
- [x] 3. Réussir les suites existantes pureté, façades, JobState et NotificationChannel ; consigner leurs preuves natives.
- [x] 4. Valider OpenSpec et les seules cibles autorisées ; conserver les empreintes des fichiers non concernés.

Aucune tâche cochée avant preuve. Aucun parsing ni fermeture du contrat des adapters. Archivage et STATISTIQUES.md restent des mandats distincts.

Preuves CGPT : quatre artefacts UTF-8/LF et delta identique au canon ; compilation et import neuf (codes 0) ; AST/exports exacts, deux Enum préexistants et façade préservés ; 20 tests natifs réussis (3 pureté, 11 façades, 3 JobState, 3 NotificationChannel) ; validation stricte du change avant et après code (codes 0) ; 350 empreintes hors module conservées. Canon inchangé (76 empreintes) : contrôle global antérieur, code natif 1, 21 avertissements de longueur seuls, zéro ERROR ; qualification limitée selon le critère explicite du développeur, sans prétendre à une réussite native globale.
