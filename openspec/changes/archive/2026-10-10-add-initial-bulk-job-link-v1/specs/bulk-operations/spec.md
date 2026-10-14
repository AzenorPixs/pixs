## MODIFIED Requirements

### Requirement: Profil structurel préparatoire BulkJobLink v1

BulkJobLink v1 MUST être une représentation interne, immuable et purement mémoire
comportant exactement operation_id et job_id, tous deux fournis explicitement sans
valeur par défaut. Chaque champ MUST être une str exacte non vide, opaque et sans
normalisation ; operation_id et job_id MUST être distincts dans cette représentation.

#### Scenario: Lien structurel valide

- **WHEN** un appelant de confiance ou une fixture synthétique fournit deux références de type str exact, non vides et distinctes
- **THEN** la représentation conserve exactement ces références sans produire de diagnostic ni effet

### Requirement: Validation pure et limites de BulkJobLink v1

La validation de BulkJobLink v1 MUST porter uniquement sur son type exact et les
deux références déclarées, en contrôlant les types avant toute comparaison. Elle
MUST produire des diagnostics statiques VALIDATE, triés et dédupliqués, sans
reproduire les valeurs ni invoquer les comportements d'un objet étranger.
Elle MUST NOT résoudre une référence, effectuer une entrée/sortie, ni établir
l'existence, la légitimité, l'autorisation, la cardinalité globale, l'unicité globale,
la corrélation, la causalité, le périmètre, la déduplication ou la persistance.
Les exigences générales BulkOperation et Jobs restent intégralement applicables ;
ce profil ne constitue pas leur implémentation complète.

#### Scenario: Lien structurel invalide refusé

- **WHEN** la représentation est d'un type étranger, un champ n'est pas une str exacte non vide, ou les deux références sont égales
- **THEN** la validation produit des diagnostics statiques sans écho des valeurs, effet ni garantie runtime
