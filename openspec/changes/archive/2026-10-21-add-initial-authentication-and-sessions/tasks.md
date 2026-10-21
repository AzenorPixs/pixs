# Tâches — C03

Les tâches de réalisation sont prouvées par VALIDATION.md et les résultats natifs du 21 octobre 2026. La tâche postérieure à l’archivage, 3.4, est prouvée par la création effective et la vérification des six sections/totaux de STATISTIQUES.md. Aucun état global P0 n’est déduit.

## 1. Revue de conception

- [x] 1.1 Revoir les exigences/scénarios de requirements.md et l’adoption du profil C00 ; recouper les sources actuelles avant réalisation.
- [x] 1.2 Appliquer les décisions D01–D17 déjà arrêtées ; détailler contrats/schémas, prendre en compte les deltas adoptés le 20 octobre 2026 et qualifier versions stables, coûts Argon2id, profil Django/OpenLDAP, cookie/transport, trousseau et preuve R01 avant écriture de code.

## 2. Réalisation qualifiée

- [x] 2.1 Décliner le provider local autonome de pixs.auth sur PostgreSQL par défaut après adoption des deltas Auth ; préciser confiance et contrats sans installer de source externe ni activer IdP/OpenLDAP/KDC implicitement.
- [x] 2.2 Implémenter les contrats spécialisés Auth, connexion/déconnexion, façade web cookie/CSRF et API/CLI Bearer opaque ; respecter stockage par empreinte, trousseau CLI ou mémoire et plafonds D03–D06/D09.
- [x] 2.3 Traiter rotation à usage unique, concurrence/réutilisation, révocation dérivée et globale D07–D10 ; raccorder transaction C05, exception limitée au retrait et réconciliation, sans audit ou commit inventé.
- [x] 2.4 Tester assurance réelle et exceptions Super Admin, frontières temporelles, réponse de renouvellement perdue, limite de sessions, changement de mot de passe, échecs d’audit/Auth et signature R01 de 10 minutes ; qualifier la vérification Argon2id croisée Django/OpenLDAP sans activation implicite.

## 3. Preuves et clôture

- [x] 3.1 Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, avec résultats natifs et preuves.
- [x] 3.2 Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.
- [x] 3.3 Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.
- [x] 3.4 N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.
