# Tâches — C07

Ces tâches suivent la réalisation du socle hôte intermédiaire autorisée par CISMP. Une coche exige la preuve du critère local complet ; elle ne certifie ni le P0 installé ni les lots C14/C17/C18/C19. La présence du dossier et sa validation syntaxique ne prouvent aucune réalisation.

## 1. Revue de conception

- [x] 1.1 Revoir les exigences/scénarios de requirements.md et l’adoption du profil C00 ; recouper les sources actuelles avant réalisation.
- [x] 1.2 Lever les barrières de conception énoncées dans design.md, présenter les fichiers/contrats et tout delta nécessaire avant écriture de code.

## 2. Réalisation future

- [x] 2.1 Définir l’hôte Django et les points de branchement explicites au pipeline commun.
- [x] 2.2 Relier sources runtime, composants/providers, configuration et lifecycle.
- [x] 2.3 Refuser readiness sur dépendance, attestation ou module essentiel manquant.
- [x] 2.4 Tester démarrage/arrêt isolés, ordre déterministe, ambiguïtés et conservation des dimensions non évaluées ; qualifier le socle hôte intermédiaire C07 en conservant le P0 non prêt et documenter son raccordement à l’intégration finale portée par C14.

## 3. Preuves et clôture futures

- [x] 3.1 Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, avec résultats natifs et preuves.
- [x] 3.2 Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.
- [x] 3.3 Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.
- [x] 3.4 N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.
