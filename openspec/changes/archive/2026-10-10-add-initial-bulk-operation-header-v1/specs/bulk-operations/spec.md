## MODIFIED Requirements

### Requirement: Entête structurel préparatoire BulkOperationHeader v1

BulkOperationHeader v1 MUST être une représentation interne Python, immuable et purement mémoire
comportant exactement operation_id, bulk_type et bulk_version. Les trois champs MUST être
fournis explicitement, sans valeur par défaut.

#### Scenario: Entête explicite sans effet

- **WHEN** un appelant de confiance ou une fixture synthétique fournit les trois champs conformes au profil
- **THEN** la représentation conserve exactement ces valeurs sans effet ni champ supplémentaire

### Requirement: Référence et variante du profil BulkOperationHeader v1

operation_id MUST être une str exacte non vide, opaque et sans normalisation ; ce contrôle
MUST NOT imposer ni prouver un format UUID. bulk_type MUST être un membre de type exact
BulkOperationVariant, limité aux variantes IMPORT et EXPORT ; une chaîne, un autre type,
une conversion implicite, un alias ou un défaut MUST NOT être admis.

#### Scenario: Type de variante étranger refusé

- **WHEN** bulk_type est la chaîne IMPORT ou un objet étranger au lieu du membre IMPORT de BulkOperationVariant
- **THEN** le profil est refusé sans conversion ni comportement d'objet étranger

### Requirement: Version du profil BulkOperationHeader v1

bulk_version MUST être une str exacte au format SemVer 2.0.0 complet, préversion et
métadonnées de build admises conformément à component-model et dependencies, sans
normalisation. Cette validation de forme MUST NOT décider une compatibilité de contrats.

#### Scenario: Version complète conservée

- **WHEN** bulk_version vaut 1.2.3-rc.1+build.7
- **THEN** cette version structurellement valide est conservée telle quelle sans décision de compatibilité

#### Scenario: Version malformée refusée

- **WHEN** bulk_version vaut 1, est vide ou possède un type autre que str exact
- **THEN** le profil est refusé sans version de repli ni écho de la valeur

### Requirement: Validation pure et limites de BulkOperationHeader v1

La validation MUST refuser un objet de type étranger au profil avant tout accès à ses
attributs, puis contrôler les types des champs avant parsing ou comparaison. Elle MUST
produire des diagnostics statiques VALIDATE triés et dédupliqués, sans écho des valeurs
ni invocation de comportement étranger. Elle MUST NOT effectuer d'entrée/sortie, résoudre
des références, prouver existence ou autorisation, persister, rattacher des Jobs, évaluer
une compatibilité, exécuter un import/export ou remplacer les exigences générales BulkOperation.

#### Scenario: Structure invalide diagnostiquée sans effet

- **WHEN** le profil, une référence, une variante ou une version a une structure interdite
- **THEN** des diagnostics statiques sont produits sans effet ni garantie runtime
