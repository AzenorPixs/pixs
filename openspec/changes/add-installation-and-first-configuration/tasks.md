# Tâches — C08

Ces tâches décrivent la réalisation future C08. Les validations distinctes du 22 octobre 2026 couvrent la rédaction documentaire, l’alignement de la métadonnée puis l’adoption exacte des deux deltas ; elles ne prouvent aucune réalisation. Toutes les tâches de réalisation restent non cochées ; un contrôle documentaire ne prouve aucune recette produit.

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


## Compléments proposés par la reprise documentaire du 22 octobre 2026

Ces tâches supplémentaires restent non cochées. L’adoption normative et la correction de métadonnée ont leurs preuves distinctes ; aucune réalisation n’en est déduite.

- [ ] 1.3 Après adoption des deux deltas et alignement de .openspec.yaml, vérifier les politiques de résolution par mode/workload, l’audit avant base, son relais C05 et la procédure externe de publication des références.
- [ ] 1.4 Déclarer la dépendance minimale de gouvernance initiale, vérifier la source de confiance et le profil complet/versionné ; aucun défaut de rétention ni producteur de fixture en exploitation.
- [ ] 2.5 Réaliser et qualifier après adoption le raccord post-INSTALLER du provider existant, sans writer implicite, réétiquetage de NORMAL, contournement de révocation ni modification des gabarits purs ; exécuter S01–S04.
- [ ] 2.6 Raccorder une attestation de gouvernance réelle au port propriétaire dans la transaction C08 et sa revalidation ; exécuter G01–G03 et B01/B02/B06/B07/B08 sans dispense du compte futur.

## Jalon documentaire d’adoption

Le développeur a validé l’intégration exacte de quatre exigences et huit scénarios dans les deux canons et l’alignement de ces quatre documents C08. Les contrôles OpenSpec de ce lot restent distincts de la réalisation. Les quatorze tâches futures ci-dessus demeurent non cochées ; la source de gouvernance réelle et les recettes produit restent à prouver.

Cette limite de l’adoption antérieure est conservée : avant adoption du nouveau complément PA/PZT, les preuves techniques UID/unité ne créent pas seules d’exception supplémentaire. La proposition 1.3 de design.md distingue remise technique de connexion pré-base et décisions applicatives après ouverture.


## Complément PA/PZT — préparation documentaire et réalisation future

Le développeur a validé la formalisation du parcours PA/PZT → PostgreSQL → PBO. Les huit deltas et la conception 1.3 sont proposés à l’intégration canonique ; les quatre exigences antérieurement adoptées restent acquises. La validation documentaire, l’adoption normative et la qualification exécutée sont trois preuves distinctes. Les quatorze tâches précédentes et les trois suivantes restent non cochées.

- [ ] 1.5 Après revue et adoption explicites des deltas PA/PZT, aligner la sélection du profil initial et les cadrages BUILD/PROJECT/TECHNICAL ; déclarer les profils physique/VM et Docker, leurs processus, versions, stockage, budgets, supervision et mécanisme de secrets Docker à qualifier. Une qualification historique sans exécutants n’est pas réutilisée.
- [ ] 1.6 Détailler et vérifier le provisionnement opérateur indépendant de PG, le catalogue fermé de préparation PA, le profil local PZT mTLS, la politique technique native de connexion PBO et les paramètres de validité/fraîcheur/révocation/audit ; conserver R01 et interdire tout bypass local ou droit métier implicite.
- [ ] 2.7 Réaliser seulement après cadrage des mandats les raccords propriétaires PA/PZT/PG/PBO, puis exécuter P01–P10 sur cibles autorisées : première connexion PA, stockage Docker existant, reprise et concurrence, droits techniques refusés hors périmètre, secrets, audit et relais ; compléter les preuves B/S/G sans déclarer P0 disponible avant qualification.

Ce lot documentaire n’installe aucun service, ne lance aucune migration ni recette sur une base réelle et ne modifie aucun canon. La seule validation OpenSpec, même réussie, ne coche pas ces dix-sept tâches et ne livre pas C08.
