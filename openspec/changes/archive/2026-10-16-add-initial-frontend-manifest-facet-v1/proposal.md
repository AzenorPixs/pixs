# Proposition — add-initial-frontend-manifest-facet-v1

## Objectif
Implémenter le profil FrontendManifestFacet v1 déjà validé dans le canon frontend (quatre exigences, sept scénarios, référence23), via le modèle commun ComponentManifest.

## Périmètre
- Modifier uniquement src/pixs/kernel/manifest/models.py.
- Créer tests/unit/test_frontend_manifest_facet.py et tests/integration/test_frontend_manifest_facet_integration.py.
- Préserver parser.py, les __init__, semver.py, guards.py et les validateurs FCD existants.

## Critères
La table frontend est optionnelle. Présente, elle contient exactement schema_version chaîne "1" et contributions ordonnées, éventuellement vides, pour MODULE/SUBMODULE seulement. Chaque contribution réutilise les six champs FCDv1 ; snapshots immuables, textes et multiplicités préservés. Les diagnostics frontend restent sans écho. Les manifests sans frontend et les gardes communes conservent leur comportement. Les deux ordres d’import fonctionnent en processus frais.

## Exclusions
Aucune nouvelle norme, composition, activation, résolution, autorisation, preuve de confiance ou registre/lifecycle parallèle. Aucun champ enabled ou shell_api. C1 Bulk et C3 Audit restent hors périmètre. Aucun Git, secret, dépendance ou fichier de namespace créé.

## Validation et clôture
Trois compilations séparées, tests unitaires et frais sous gardes, régressions manifest/FCD, stricts locaux, puis globaux sous exclusion. Coches uniquement après preuves. Archive unique avec delta identique au canon et rapport STATISTIQUES.md distinct, vérifié avant clôture.
