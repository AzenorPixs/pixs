# Tâches — C08

Ces tâches décrivent une réalisation future non autorisée par la demande de préparation. Toutes restent non cochées ; la création du dossier et son strict syntaxique ne prouvent aucune de ces réalisations.

Le complément R01 du 19 octobre 2026 précise les responsabilités C08/C02 et les cas B01–B10 de `design.md`, sans ajouter de tâche ni lancer une implémentation ou une production de code. D01–D04 de C02 restent validés ; les mécanismes de preuve et paramètres C08 ne sont pas réputés exécutés ou qualifiés par leur description.

## 1. Revue de conception

- [ ] 1.1 Revoir les exigences/scénarios de requirements.md et l’adoption du profil C00 ; recouper les sources actuelles avant réalisation.
- [ ] 1.2 Détailler les mécanismes conformes au contrat R01 : preuve d’opérateur sans session préalable, mapping de sujet C03/C04, politique et plan fermés, marqueur/checkpoint et audit C05 ; présenter fichiers/contrats et tout delta nécessaire dans un mandat distinct, sans rouvrir D01–D04 de C02.

## 2. Réalisation future

- [ ] 2.1 Concevoir marqueur externe, machine de modes, preuve d’éligibilité et état d’opération persistant ; lier version du plan, installation/base cible, acteur et confirmations selon R01, sans secret dans les checkpoints.
- [ ] 2.2 Implémenter CLI et inspection base absente/conforme/migrable/incompatible avec plans et confirmations.
- [ ] 2.3 Créer ou réutiliser le Super Admin unique et provisionner le premier tenant via les écritures propriétaires C02 et les gardes R01 ; vérifier l’opérateur, la décision et le plan sans authentifier par avance le compte cible ; exclure autorité C01 métier, deuxième compte, reset et accord tenant implicites. Conserver credential privé C03, audit et transaction déclarés.
- [ ] 2.4 Exécuter B01–B10 : première création pré-session, preuve/plan/confirmation invalides, saisies différentes, base conservée, concurrence, rejeu identique/divergent, interruption avant/après commit ou marqueur, audit indisponible, autorité réutilisée hors périmètre et transitions contrôlées. Distinguer gardes locales C02 V05/V07 et preuves intégrées C03/C04/C05/C08.

## 3. Preuves et clôture futures

- [ ] 3.1 Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, avec résultats natifs et preuves.
- [ ] 3.2 Vérifier isolation, échecs attendus, absence de secret et conformité de tous les scénarios applicables ; déclarer non exécuté ou non applicable avec motif.
- [ ] 3.3 Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.
- [ ] 3.4 N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.
