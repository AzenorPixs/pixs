# Tasks

## Préparation

- [x] 1.1 Prouver périmètre CGPT, absence de change actif, baseline et collecte initiale.
- [x] 1.2 Créer les cinq artefacts autorisés, UTF-8/LF et validation OpenSpec stricte avant code.

## Implémentation minimale

- [x] 2.1 Étendre seulement src/pixs/kernel/feature_flags.py : modèle frozen à huit champs requis sans défaut, validateur structurel exact, helpers réutilisés, refus déterministe sans écho ; conserver R1 et ne pas introduire de runtime.
- [x] 2.2 Créer tests/unit/test_feature_flag_assignments.py : huit champs, valeurs, UTC/fenêtres, métadonnées opaques, conteneurs/éléments hostiles, aucune exécution de callback, ordre et diagnostics.
- [x] 2.3 Créer tests/integration/test_feature_flag_assignments_integration.py : import enfant frais sous gardes I/O causales, construction/validation témoin et refus hostile sans effet.

## Preuves

- [x] 3.1 Vérifier syntaxe minimum 3.11 et compilation des trois fichiers sous l'interpréteur DEVOPS.
- [x] 3.2 Réussir les deux suites nouvelles et les deux suites R1 existantes.
- [x] 3.3 Vérifier relecture exacte, conservation des éléments R1, sources hors périmètre, UTF-8/LF et delta R4 MOTAMOT ; expliciter les garanties non livrées.
- [x] 3.4 Réussir OpenSpec strict après les preuves avant tout cochage ; cocher uniquement les tâches réellement prouvées sous mandat distinct.

Archive et STATISTIQUES constituent deux opérations distinctes ultérieures après contrôle CGPT ; le parent CISMP reste OPEN jusqu'à sa clôture conforme.
