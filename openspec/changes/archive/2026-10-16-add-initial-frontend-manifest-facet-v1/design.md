# Conception — add-initial-frontend-manifest-facet-v1

## Fondation validée
Le canon frontend référence23 définit quatre exigences et sept scénarios. Le parser TOML contrôle le schéma puis délègue à parse_manifest. Son interface et ses fichiers restent inchangés.

## Modification minimale
Ajouter à models.py une seule valeur privée de facette, immuable, portant schema_version et le tuple des objets directement renvoyés par validate_frontend_contribution_declaration_v1. Aucun nouveau type FrontendContribution ni recopie des six champs dans une classe parallèle.
Ajouter ComponentManifest.frontend avec défaut None en fin de modèle ; le parent porte l’identité, la version et le lifecycle communs. Étendre _TOP_ALLOWED avec frontend seul.

## Validation
Distinguer absence de frontend et frontend présent de valeur nulle. La facette présente exige un composant de schéma1, de type MODULE/SUBMODULE ; sa version de facette est la chaîne "1", indépendante des versions du composant et des contributions.
Contrôler les deux clés exactes de la table, les types, puis figer la séquence et déléguer les contributions au validateur FCD public existant. Préserver textes, ordre et multiplicité ; aucun nettoyage, déduplication, grammaire nouvelle ou effet runtime.
Importer le validateur FCD localement au moment de la validation pour préserver les ordres d’import du paquet. Ne modifier aucun export ni semver.
Conserver les gardes de contenu communes sur les champs legacy et sur une projection sûre des valeurs frontend validées. Ne pas parcourir les valeurs frontend invalides ou leurs hooks via le garde générique ; ne pas rescanner des entrées frontend mutables après leur snapshot. Les erreurs frontend sont génériques ou à chemin/index fixes, sans valeur brute. Capturer seulement les exceptions attendues ; propager les anomalies inattendues.

## Tests
Unitaires publics parse_manifest et parse_manifest_text : sept scénarios normés, types/versions/clés invalides, nullité, ordre/doublons, mutation après validation, immutabilité, diagnostics sans écho et maintien des gardes communes sur les valeurs frontend lexicalement valides mais interdites comme expressions.
Intégration dans deux processus frais pour les deux ordres d’import, gardes avant import, canary anti-contournement du loader et contrôles positifs. Aucun remplacement du type datetime. Réutiliser le dispositif FCD éprouvé ; durée bornée, environnement fixe, temporaires dans le dépôt, nettoyage vérifié.
Régressions : quatre modules manifest, unitaires FCD et intégration FCD. Tests via unittest du Python projet, sans nouvelle dépendance. Les temporaires legacy utilisent TMPDIR local au processus dans la racine du dépôt.

## Limites
Aucune modification du parser, des gardes, des __init__, de semver, de FCD, des canons ou cadrages pendant ISMP. Les trois sources pressenties font l’objet de NFDOC et mandats distincts après préparation stricte.
