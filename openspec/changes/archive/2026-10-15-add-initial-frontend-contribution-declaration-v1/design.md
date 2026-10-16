# Design — add-initial-frontend-contribution-declaration-v1
## Contrat et API
Source normative : `openspec/specs/frontend/spec.md`, FrontendContributionDeclaration v1, quatre exigences et sept scénarios déjà validés. Python >=3.12, bibliothèque standard seule.
L'API publique unique est `validate_frontend_contribution_declaration_v1(value: object)`. Le choix d'entrée Python est un dictionnaire builtin exact à six clés str builtin ; les champs textuels sont des str builtin et requires une liste builtin de str builtin. Ces choix internes évitent les hooks des objets hostiles ; ils n'ajoutent pas de grammaire au canon.
Une dataclass privée frozen/slots conserve exactement les six champs. type est reconnu par l'Enum existant ; id/entry par leurs validateurs ; version par parse_version ; chaque dépendance par parse_requirement. Les textes, l'ordre et les doublons sont conservés sans trim, normalisation, décodage ni changement de casse. requires est copié en tuple, indépendant des mutations ultérieures de l'entrée.
Les erreurs attendues TypeError/ValueError ont un diagnostic générique sans écho brut. Aucun autre export public ni modification de kernel/__init__.py.
## Fichiers et preuves
- `src/pixs/kernel/frontend_contribution_declarations.py` : composition passive des validateurs existants, aucune regex ou résolution parallèle, scope limité aux quatre catégories normées.
- `tests/unit/test_frontend_contribution_declaration.py` : sept scénarios, champs manquants/supplémentaires, types hostiles sans hooks/coercition, erreurs sans écho, textes/ordre/multiplicité, immuabilité et copie de requires.
- `tests/integration/test_frontend_contribution_declaration_integration.py` : processus frais -I/-B, environnement fixe non secret, délai borné, gardes fichiers/réseau/processus/environnement/BDD et contrôles positifs ; compteurs nuls pendant import et validation. Les temporaires du driver restent sous REPO_ROOT et sont nettoyés. Aucun PostgreSQL réel.
Trois compilations distinctes, deux modules dédiés et les six modules de régression frontend existants, sans test ignoré. Les nombres de tests sont relevés après exécution.
## Limites et clôture
Contrôle structurel en mémoire seulement, sans IO, manifest, résolution, compatibilité, droits, composition ou activation. Les helpers existants et leurs tests restent inchangés.
Delta MODIFIED strictement identique au canon. Après preuves locales : contrôles globaux sous exclusion, archive unique --skip-specs si égalité canonique prouvée, puis STATISTIQUES.md distinct à six sections sous mandat séparé. Aucun archivage avant preuves ; la barrière CAB commune C3 ne doit pas être contournée.
