# Tasks

## 1. Modèles et contrats

- [x] 1.1 Implémenter les trois modèles immuables, les deux enums et les validations UUIDv7/types/états avec erreurs constantes.
- [x] 1.2 Implémenter la validation des liaisons : références, unicité bidirectionnelle, doublons et absence d'effets.
- [x] 1.3 Publier la façade identity et l'intégrer à core en préservant scope.

## 2. Tests

- [x] 2.1 Prouver les cas modèles, états, types, UUID, immutabilité et entrées invalides avec la suite unitaire modèles.
- [x] 2.2 Prouver les cardinalités, références, doublons et absence de mutation avec la suite unitaire liaisons.
- [x] 2.3 Prouver le contrat via la façade publique et les refus sans valeur brute.

## 3. Validation finale

- [x] 3.1 Réussir les suites complètes, AST, UTF-8/LF et OpenSpec strict ; vérifier conformité normative et absence de modification hors périmètre avant archivage.

## Preuves finales contrôlées par CGPT

- Sources, contrat public et tests relus ; unicité UUID globale conforme à TECHNICAL §13, liaison 0..1 dans chaque sens, références et refus sans valeur brute.
- Unités : `identity-unit02`, outil `msg_0ee92a4380012vGUugsVHriiwR` — 304 tests OK, exit 0, dont 10 modèles et 13 liaisons.
- Intégration : `identity-integration02`, outil `msg_0ee9380840019OYIr0dmscleJx` — 100 tests OK, exit 0, dont 4 tests de façade identité.
- Syntaxe et encodage : `identity-ast03`, outil `msg_0ee9468c0001oEIiVT34cQG6BU` — 6 AST et 10 fichiers UTF-8/LF valides, exit 0.
- OpenSpec : `identity-strict03`, outil `msg_0ee952457001OYXA2wPjEasmjF`, rapport `msg_0ee95302b001DDBpjgCbjpBHh8` — 77 éléments valides, 0 échec, exit 0.
- Contrôle de périmètre : dix fichiers attendus, écritures observées et contenus réconciliés ; cadrages PROJECT/TECHNICAL/BUILD/DEVOPS/README cohérents pour ce socle structurel. Aucune dépendance nouvelle, aucun Git ni effet d'authentification/persistance.
- Incidents tracés : `identity-ast01` refusé pour commande divergente, non exécuté ; découverte globale `identity-alltests01` échouée sur import existant du PDP. Reprise CAB `identity-recovery01` réussie et suites habituelles finales ci-dessus réussies. L'échec antérieur n'est pas présenté comme un succès.
- L'archivage reste une opération distincte à autoriser par CGPT. Les exigences de backend réel, d'authentification et d'audit durable restent hors de ce change.
