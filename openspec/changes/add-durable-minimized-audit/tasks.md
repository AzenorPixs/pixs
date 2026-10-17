# Tâches — C05

Ces tâches décrivent une réalisation future non autorisée par la demande de préparation. Toutes restent non cochées ; la création du dossier et son strict syntaxique ne prouvent aucune de ces réalisations.

## 1. Revue de conception

- [ ] 1.1 Revoir les exigences/scénarios de requirements.md et l’adoption du profil C00 ; recouper les sources actuelles avant réalisation.
- [ ] 1.2 Lever les barrières de conception énoncées dans design.md, présenter les fichiers/contrats et tout delta nécessaire avant écriture de code.

## 2. Réalisation future

- [ ] 2.1 Définir stockage propriétaire, contrat de sink et frontière transactionnelle des effets et refus.
- [ ] 2.2 Implémenter écritures durables append-only, accès autorisés et minimisation.
- [ ] 2.3 Intégrer l’audit aux opérations ordinaires et les dérogations Super Admin explicites.
- [ ] 2.4 Tester pannes avant/après écriture, accès inter-tenant, réécriture refusée et portée honnête des acquittements.

## 3. Preuves et clôture futures

- [ ] 3.1 Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, avec résultats natifs et preuves.
- [ ] 3.2 Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.
- [ ] 3.3 Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.
- [ ] 3.4 N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.
