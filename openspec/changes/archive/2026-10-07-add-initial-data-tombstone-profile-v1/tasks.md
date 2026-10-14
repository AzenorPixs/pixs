# Tâches — profil tombstone-v1

## 1. Préparation

- [x] 1.1 Vérifier les artefacts UTF-8/LF, le delta mot pour mot identique au requirement canonique et les validations OpenSpec du change et du canon.

## 2. Implémentation minimale

- [x] 2.1 Ajouter uniquement src/pixs/kernel/data_tombstone_profile.py : TombstoneProfile immuable à huit champs sans défaut et validateur structurel pur à diagnostics VALIDATE statiques triés/dédupliqués.
- [x] 2.2 Ajouter les tests unitaires de surface, valeurs opaques, types exacts/hostiles, calendrier UTC, scope/tenant et diagnostics sans écho.
- [x] 2.3 Ajouter et réussir l'intégration en processus frais -I -B avec gardes positives d'effets, d'environnement, de base et d'horloge.

## 3. Validation

- [x] 3.1 Compiler les trois fichiers Python avec l'interpréteur déclaré et réussir les tests ciblés.
- [x] 3.2 Réussir les régressions des profils/vocabulaires de données, des diagnostics, de pureté Kernel et des façades.
- [x] 3.3 Vérifier la conformité canon/cadrages/code/tests, les validations OpenSpec finales, UTF-8/LF et l'absence de modification hors périmètre par empreintes sans Git.

L'archivage --skip-specs reste un mandat distinct après toutes les preuves. Le rapport STATISTIQUES.md de l'archive exige ensuite son propre mandat et la vérification de ses six sections et totaux. Ce profil n'achève pas les exigences runtime générales de cycle de vie.

## Preuves de fin du périmètre

- Trois compilations natives réussies, code 0 pour chaque fichier Python.
- Tests ciblés : 21 unitaires et 1 intégration en processus frais, tous réussis.
- Régressions : 108 tests dans 23 modules historiques, sans échec, erreur ou skip.
- Change validé strictement : 1/1, issues vides, code 0 ; global : 77/77, code 0.
- Canon validé sur les critères applicables ; les 20 WARNING globaux portent uniquement sur la longueur, explicitement exclue comme critère de qualité par le développeur. Le contrôle strict du canon à code 1 n'est pas déclaré réussi.
- Delta canonique identique ; UTF-8/LF ; 198 empreintes de référence intactes et trois nouveaux fichiers conformes aux contenus revus.
- Cadrages cohérents dans ce périmètre ; aucun Git, dépendance, façade, configuration, accès PostgreSQL ou comportement runtime ajouté.
