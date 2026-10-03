## 1. Preparation OpenSpec

- [x] 1.1 Relire proposal et design, vérifier le seul delta canonique API versionné par majeure sans nouvelle norme.
- [x] 1.2 Créer les artefacts nécessaires, valider le change en mode strict et vérifier UTF-8/LF et cohérence des cadrages.

## 2. Fondation plans API

- [x] 2.1 Préparer le paquet pur avec ApiContractPlan figé à deux champs obligatoires et façade publique, ContractDescriptor exact de catégorie API et référence logique nue, sans modification d'API existante.
- [x] 2.2 Préparer api_major_prefix et check_api_evolution réutilisant les APIs publiques de contrat et SemVer, préfixe indépendant des versions runtime, breaking bool exact, refus des ruptures sans majeure et des baisses.
- [x] 2.3 Revalider les objets forgés et champs manquants, imposer document distinct et coexistence non blanche seulement à majeure strictement supérieure, sans attestation réelle ni diagnostic reproduisant une entrée.
- [x] 2.4 Documenter le parcours synthétique et les exclusions, sans I/O, secret, base, réseau ou dépendance nouvelle.
- [x] 2.5 Préparer les tests purs unitaires et d'intégration significatifs avec entrées invalides, immutabilité, sous-classes et objets hostiles, SemVer 0/préversions/builds, majeure/mineure/corrective, références et coexistence.

## 3. Preuves et clôture

- [x] 3.1 Exécuter les tests dédiés unitaires et d'intégration avec données synthétiques ; rapporter leurs comptes réellement observés.
- [x] 3.2 Exécuter les régressions unitaires et d'intégration séparées, contrôler syntaxe AST Python3.11, UTF-8/LF, delta canonique, strict OpenSpec et périmètre.
- [x] 3.3 Vérifier les preuves, les critères, la cohérence et la validation explicite CGPT du dossier de clôture avant archivage.

L'archivage est exigé après toutes les tâches ci-dessus prouvées et cochées, sous mandat CAB distinct après contrôle CGPT ; il ne fait pas partie de la case 3.3.
La production de STATISTIQUES.md est un mandat distinct après archivage effectif, avec sonde finale et quotas réels ou N/A motivés. Aucune case ci-dessus n'est une preuve acquise. Si la session s'arrête à 16h30 Paris, conserver l'état du premier jalon non prouvé sans archivage ni déclaration de réussite.
