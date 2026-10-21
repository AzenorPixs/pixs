# Tâches — C04

Le RUN CISMP3 autorise la réalisation de ce seul change. Les preuves
exécutées, leurs limites et les propriétaires sont détaillés dans
VALIDATION.md. Une archive, un inventaire ou une coche ne remplace pas une
validation actuelle. La qualification commune du composite a été recoupée directement :
21 PG avec Auth, Core et C05 réels ; trust/assurance et plan restent des fixtures déclarées.

## 1. Revue de conception

- [x] 1.1 Revoir requirements.md, le profil C00 et les sources actuelles : matrice, canons et profils purs recoupés ; OpenSpec strict 191/191.
- [x] 1.2 Qualifier les contrats R01 D15/D16 : DTO opérateur disjoint, Ed25519 C03, plan/hash/cibles C08, 600 s, consommation au commit et inspection ; banc commun R0114 réel, C08/classification/assurance fixtures explicites.

## 2. Réalisation

- [x] 2.1 Relier faits Auth, contexte, policies et ressources aux frontières Django : code et12 PG C04 validés ; banc commun21 PG RuntimeTrustedFactsProvider/AuthInvocationSource/CoreFactSource/CoreAuthorizationStore/RuntimeAuthorizationDecider et C05 réels, incluant7 scénarios du composite.
- [x] 2.2 PEP, filtre SQL, obligations/fraîcheur et réévaluations : Core query et C05 filter_audit réels, 18PG ; ports de contrôle final et fraîcheur10+8PG.
- [x] 2.3 Compte fonctionnel actif/Binding unique d'installation, PLATFORM et accords tenant explicites, sans transfert ; store/decider27PG.
- [x] 2.4 DENY ordinaire, tenant non accordé/accordé malgré ACL, dérogations et façades Core : 192 tests purs, 113 PG C04 distincts, 200 scénarios Core C02 et migrations. Les interfaces C06/C09/C13 non activées restent hors de cette preuve.

## 3. Vérifications de réalisation

- [x] 3.1 Syntaxe et suites applicables exécutées : 25 Python compilés,192 tests et recettes PG isolées, preuves natives dans VALIDATION.md.
- [x] 3.2 Isolation, échecs, refus fermés et absence de valeur secrète exposée : schémas propres détruits, connexions fermées, doubles identifiés ; contraintes des consommateurs déclarées.
- [x] 3.3 Effets/fichiers examinés et sources préexistantes préservées : SHA/natifs unitaires/CAB, aucun Git ou P0 global annoncé, impacts et limites documentés.
- [x] 3.4 Périmètre des opérations de clôture vérifié : archivage/synchronisation OpenSpec nécessaires délégués par CISMP/ISMP ; aucun commit, push, déploiement ou autre change autorisé dans ce RUN.

## 4. Obligations de clôture suivies par le gate

Après les critères de réalisation, observer l'archive réussie et la
publication resource-scoped-v1, puis produire et vérifier le rapport propre
STATISTIQUES.md à six sections UTF-8/LF. Le gate individuel, le désarmement
et la libération du seul RUN restent obligatoires. Cette liste décrit des
obligations post-archivage et ne les présente pas comme déjà réalisées.
Aucun état TERMINÉ n'est admis avant leurs preuves.
