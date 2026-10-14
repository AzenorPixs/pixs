## MODIFIED Requirements

### Requirement: Profil structurel préparatoire BulkOperationConflict v1

BulkOperationConflict v1 MUST être une représentation interne Python, immuable
et purement mémoire comportant exactement operation_id et conflict_strategy.
Les deux champs MUST être fournis explicitement sans valeur par défaut.

#### Scenario: Deux champs explicites conservés

- **WHEN** un appelant de confiance fournit une référence conforme et un membre canonique de BulkConflictStrategy
- **THEN** la représentation conserve exactement ces deux valeurs sans effet ni champ supplémentaire

### Requirement: Référence et stratégie de BulkOperationConflict v1

operation_id MUST être une str exacte non vide, opaque et sans normalisation.
conflict_strategy MUST être un membre canonique de type exact BulkConflictStrategy :
REJECT, CREATE_ONLY, UPDATE_ONLY ou UPSERT. Toute chaîne, instance fabriquée hors
membres canoniques, autre type, conversion, alias ou valeur de repli MUST NOT être admis.

#### Scenario: Stratégie non canonique refusée

- **WHEN** conflict_strategy est une chaîne REJECT, une instance fabriquée hors membres canoniques ou un objet de type étranger
- **THEN** le profil est refusé sans conversion ni comportement d'objet étranger

### Requirement: Validation pure de BulkOperationConflict v1

La validation MUST refuser tout candidat étranger ou dérivé avant tout accès
à ses attributs, puis contrôler les types exacts des champs avant toute autre
opération sur leurs valeurs. Elle MUST produire des diagnostics statiques VALIDATE,
triés et dédupliqués, sans écho des valeurs ni invocation de comportement étranger.

#### Scenario: Structure interdite diagnostiquée sans effet

- **WHEN** une référence est absente, vide ou n'est pas une str exacte, ou le candidat ou sa stratégie est interdit
- **THEN** des diagnostics statiques sont produits sans effet ni écho des valeurs

### Requirement: Limites du profil BulkOperationConflict v1

Le profil MUST NOT résoudre une référence ou un conflit, choisir ou appliquer
une stratégie, effectuer d'entrée/sortie, décider une mutation, une idempotence
ou une autorisation, persister, appeler une commande ni exécuter un import/export.
Les exigences générales bulk, dont le rejet des conflits par défaut dans le
contrat d'import, MUST rester intégralement applicables.

#### Scenario: Aucune résolution de conflit déduite

- **WHEN** les deux champs sont structurellement acceptés
- **THEN** aucune résolution de conflit, mutation, idempotence, autorisation ou persistance n'est établie
