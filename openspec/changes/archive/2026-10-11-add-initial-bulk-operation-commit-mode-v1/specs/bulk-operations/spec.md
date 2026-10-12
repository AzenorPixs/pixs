## MODIFIED Requirements

### Requirement: Profil structurel préparatoire BulkOperationCommitMode v1

BulkOperationCommitMode v1 MUST être une représentation interne Python,
immuable et purement mémoire comportant exactement operation_id et commit_mode.
Les deux champs MUST être fournis explicitement sans valeur par défaut.

#### Scenario: Deux champs explicites conservés

- **WHEN** un appelant de confiance fournit une référence conforme et un membre canonique de BulkCommitMode
- **THEN** la représentation conserve exactement ces valeurs sans effet ni champ supplémentaire

### Requirement: Référence et mode de BulkOperationCommitMode v1

operation_id MUST être une str exacte non vide, opaque et sans normalisation.
commit_mode MUST être un membre canonique de type exact BulkCommitMode :
VALIDATE_ONLY, ATOMIC, ATOMIC_PER_CHUNK ou BEST_EFFORT. Toute chaîne, instance
fabriquée hors membres canoniques, autre type, conversion, alias ou valeur de
repli MUST NOT être admis.

#### Scenario: Mode non canonique refusé

- **WHEN** commit_mode est une chaîne, une instance fabriquée hors membres canoniques ou un objet étranger
- **THEN** le profil est refusé sans conversion ni comportement d'objet étranger

### Requirement: Validation pure de BulkOperationCommitMode v1

La validation MUST refuser tout candidat étranger ou dérivé avant tout accès
à ses attributs, puis contrôler les types exacts des champs avant toute autre
opération sur leurs valeurs. Elle MUST produire des diagnostics statiques VALIDATE,
triés et dédupliqués, sans écho des valeurs ni invocation de comportement étranger.

#### Scenario: Structure interdite diagnostiquée sans effet

- **WHEN** une référence est absente, vide ou de type interdit, ou le candidat ou son mode n'est pas canonique
- **THEN** des diagnostics statiques sont produits sans effet ni écho des valeurs

### Requirement: Limites du profil BulkOperationCommitMode v1

Le profil MUST NOT résoudre une référence, choisir ou appliquer un mode,
effectuer une entrée/sortie, une transaction, une mutation, un découpage,
un staging, une autorisation, une persistance ou un import/export.
Les exigences générales bulk MUST rester intégralement applicables.

#### Scenario: Aucune transaction déduite

- **WHEN** les deux champs sont structurellement acceptés
- **THEN** aucun comportement transactionnel, découpage, mutation, autorisation ou persistance n'est établi
