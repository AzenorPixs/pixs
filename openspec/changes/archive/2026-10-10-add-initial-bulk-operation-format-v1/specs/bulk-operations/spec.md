## MODIFIED Requirements

### Requirement: Profil structurel préparatoire BulkOperationFormat v1

BulkOperationFormat v1 MUST être une représentation interne Python, immuable
et purement mémoire comportant exactement operation_id et format. Les deux
champs MUST être fournis explicitement sans valeur par défaut.

#### Scenario: Deux champs explicites conservés

- **WHEN** un appelant de confiance fournit une référence conforme et le membre canonique CSV ou NDJSON de BulkReferenceFormat
- **THEN** la représentation conserve exactement ces deux valeurs sans effet ni champ supplémentaire

### Requirement: Référence et format de BulkOperationFormat v1

operation_id MUST être une str exacte non vide, opaque et sans normalisation.
format MUST être l'un des membres canoniques de type exact BulkReferenceFormat :
CSV ou NDJSON. Toute chaîne, instance fabriquée hors membres canoniques, autre type,
conversion implicite, alias ou valeur de repli MUST NOT être admis.

#### Scenario: Format non canonique refusé

- **WHEN** format est une chaîne CSV, une instance fabriquée hors membres canoniques ou un objet de type étranger
- **THEN** le profil est refusé sans conversion ni comportement d'objet étranger

### Requirement: Validation pure de BulkOperationFormat v1

La validation MUST refuser tout candidat étranger ou dérivé avant tout accès
à ses attributs, puis contrôler les types exacts des champs avant toute autre
opération sur leurs valeurs. Elle MUST produire des diagnostics statiques VALIDATE,
triés et dédupliqués, sans écho des valeurs ni invocation de comportement étranger.

#### Scenario: Structure interdite diagnostiquée sans effet

- **WHEN** une référence est absente, vide ou n'est pas une str exacte, ou le candidat ou son format est interdit
- **THEN** des diagnostics statiques sont produits sans effet ni écho des valeurs

### Requirement: Limites du profil BulkOperationFormat v1

Le profil MUST NOT résoudre une référence, effectuer d'entrée/sortie, choisir
ou convertir un format, parser un fichier, activer ou résoudre un adaptateur,
prouver validité du contenu, encodage, mapping, compatibilité, autorisation ou
persistance, ni exécuter un import/export. Les exigences générales bulk et les
formats étendus via adaptateur déclaré MUST rester intégralement applicables.

#### Scenario: Aucune validation réelle de fichier déduite

- **WHEN** les deux champs sont structurellement acceptés
- **THEN** aucune validité de fichier, compatibilité, autorisation ou persistance n'est établie
