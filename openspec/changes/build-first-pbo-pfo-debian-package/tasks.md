# Tâches — C18

Ces tâches décrivent une réalisation future non autorisée par la demande de préparation. Toutes restent non cochées ; la création du dossier et son strict syntaxique ne prouvent aucune de ces réalisations.

## 1. Revue de conception

- [ ] 1.1 Revoir les exigences/scénarios de requirements.md et l’adoption du profil C00 ; recouper les sources actuelles avant réalisation.
- [ ] 1.2 Lever les barrières de conception énoncées dans design.md, présenter les fichiers/contrats et tout delta nécessaire avant écriture de code.

## 2. Réalisation future

- [ ] 2.1 Fixer composition/versions/architecture et plan reproductible du paquet, sans PA embarqué.
- [ ] 2.2 Implémenter packaging et unités/adapters de services alignés sur lifecycle/santé/drain.
- [ ] 2.3 Préserver configuration et données aux mises à niveau/désinstallations, sans purge implicite.
- [ ] 2.4 Construire et éprouver installation vierge/mise à niveau/interruption/désinstallation sur environnement isolé ; transmettre le paquet à C17.

## 3. Preuves et clôture futures

- [ ] 3.1 Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, avec résultats natifs et preuves.
- [ ] 3.2 Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.
- [ ] 3.3 Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.
- [ ] 3.4 N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.
