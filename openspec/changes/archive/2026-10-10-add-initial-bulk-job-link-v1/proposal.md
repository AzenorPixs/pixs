# add-initial-bulk-job-link-v1

## Pourquoi

Le canon `bulk-operations` déclare désormais le profil structurel préparatoire
BulkJobLink v1 (couple explicite `operation_id`/`job_id`) et sa validation pure.
Ce change pose le premier artefact interne de ce profil dans le Kernel, sans
implémenter le contrat `BulkOperation`, le contrat `Job` ni leur gouvernance.

## Ce qui change

- Nouveau module interne `src/pixs/kernel/bulk_job_link.py` : représentation
  immuable purement mémoire à deux références explicites, et validation pure
  produisant des diagnostics statiques `VALIDATE` triés et dédupliqués.
- Nouveaux tests unitaires et d'intégration ciblés sur ce seul profil.
- Aucune modification des façades du noyau, du canon, de `JobCorrelation`, des
  contrats `BulkOperation`/`Job`, de la persistance, de l'autorisation, de la
  configuration, des dépendances ni du frontend.

## Impact

- Capacité : `bulk-operations` (profil déjà canonique) ; `jobs` inchangée.
- Spécification : le delta du change reproduit exactement le canon ; l'archivage
  sera exécuté avec `--skip-specs` parce que le canon est déjà identique (la RSMP
  BulkJobLink v1 a été appliquée sur `openspec/specs/` avant ce change).
- Code : un module et deux fichiers de tests ; module en stdlib uniquement (`dataclasses`,
  `unittest`), aucune nouvelle dépendance ; le module seul reste sans I/O, les tests utilisent un processus jetable.
- Avertissement known : la longueur du texte d'exigence fait l'objet d'un
  `WARNING` de `openspec validate`, explicitement accepté par le développeur
  (« la longueur n'est pas un critère de qualité ») ; aucun texte canon n'est
  reformulé pour le supprimer.
