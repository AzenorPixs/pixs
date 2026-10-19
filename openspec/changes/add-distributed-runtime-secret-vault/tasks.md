# Tâches futures — coffre d’exploitation distribué

Toutes les tâches restent non cochées. La présente préparation ne lance ni implémentation, ni installation de coffre, ni manipulation de secrets.

## 1. Conception de réalisation

- [ ] 1.1 Inventorier les secrets locaux minimaux et ceux d’exploitation ; vérifier l’absence de dépendance circulaire de démarrage et de récupération.
- [ ] 1.2 Faire valider produit/version, identité initiale, droits par service, protection des clés, durées, topologie, résidence et objectifs de reprise, puis le mandat de réalisation.

## 2. Réalisation sous mandat distinct

- [ ] 2.1 Intégrer le provider de coffre choisi au contrat SecretProvider et aux références existantes, sans le rendre obligatoire pour le P0 local.
- [ ] 2.2 Intégrer authentification des workloads, droits minimaux, credentials courts compatibles, renouvellement et révocation avec arrêt contrôlé des copies si requis.
- [ ] 2.3 Intégrer transport vérifié, audit, refus sans repli implicite et procédures protégées de démarrage/sauvegarde/récupération.

## 3. Qualification future

- [ ] 3.1 Tester refus inter-services et inter-périmètres, identité non vérifiable, rotation, expiration et révocation sans prolongation par cache.
- [ ] 3.2 Tester panne réseau/coffre, perte d’instance, reprise et restauration isolée avec état de confiance courant ; mesurer disponibilité et RPO/RTO déclarés.
- [ ] 3.3 Exécuter syntaxe, régressions, OpenSpec et contrôles de non-exposition sur le périmètre réellement implémenté, sans présenter des mocks comme qualification réelle.

## 4. Intégration et clôture futures

- [ ] 4.1 Relier les preuves à la composition distribuée effectivement sélectionnée et à sa recette, sans activer implicitement ce profil ou modifier C01 archivé.
- [ ] 4.2 Examiner le périmètre et les limites ; ne synchroniser, archiver ou publier que sous autorisation ultérieure, avec statistiques si archivage réussi.
