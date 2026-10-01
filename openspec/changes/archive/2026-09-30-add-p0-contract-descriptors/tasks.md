## 1. Preparation OpenSpec

- [x] 1.1 Relire proposal et design, vérifier le delta canonique contracts sans nouvelle norme.
- [x] 1.2 Créer le seul delta requis et valider le change en mode strict ; vérifier UTF-8/LF et cohérence des cadrages.

## 2. Fondation descripteurs

- [x] 2.1 Préparer le paquet pur contracts avec `ContractCategory` à sept valeurs et `ContractDescriptor` figé à cinq champs obligatoires, sans parseur divergent ni modification d’API existante.
- [x] 2.2 Préparer `require_category` à catégorie exacte avec retour du membre validé et `check_evolution` avec `breaking` bool exact, ruptures id/catégorie en majeure indépendamment du build/préversion, idempotence à précédence égale limitée aux mêmes champs hors version, refus des baisses et des changements propriétaire/doc à même précédence.
- [x] 2.3 Préparer `DeprecationNotice` séparé lié au descripteur annonçant en identité exacte build inclus, annonce normale stable seulement en mineure avec remplacement documenté obligatoire, préversions refusées, puis `check_retirement` stable en majeure strictement supérieure, sans suppression réelle ni exception critique.
- [x] 2.4 Documenter le parcours synthétique et les exclusions ; aucun effet externe, secret, base ou dépendance nouvelle.
- [x] 2.5 Préparer les tests purs unitaires/integration avec entrées invalides réelles, immutabilité, SemVer avec préversions/build, category mismatch, baisse/rupture, `breaking` non bool refusé, idempotence build seul, dépréciation/retrait normaux stables, refus des annonces en préversion, des retraits anticipés et des chemins non supportés.

## 3. Preuves et clôture

- [x] 3.1 Exécuter les tests dédiés unitaires/integration avec données synthétiques et refus des entrées invalides.
- [x] 3.2 Exécuter les régressions applicables, contrôles de syntaxe, UTF-8/LF et validation OpenSpec stricte, puis vérifier le périmètre.
- [x] 3.3 Vérifier les preuves, les critères, la cohérence et la validation CGPT du dossier de clôture avant archivage.

L’archivage est exigé après toutes les tâches ci-dessus prouvées et cochées, sous mandat CAB distinct après contrôle CGPT ; il ne fait pas partie de la case 3.3.
La production de STATISTIQUES.md est un mandat distinct après archivage effectif, avec sonde finale et quotas réels ou N/A motivés. Aucune case ci-dessus n’est une preuve acquise. Si la session s’arrête à 16h30 Paris, conserver l’état du premier jalon non prouvé sans archivage ni déclaration de réussite.
