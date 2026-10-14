## MODIFIED Requirements

### Requirement: Modèle préparatoire BulkOperationRecord v1

Le modèle Django interne BulkOperationRecord MUST persister exactement ces neuf champs textuels, avec operation_id comme clé primaire locale à sa table et sans clé étrangère. Seuls scope_context_reference, conflict_strategy et commit_mode MUST admettre NULL. Le modèle MUST NOT fournir de défaut métier. Les producteurs MUST valider le mapping explicite avant construction ou écriture.

#### Scenario: Persistance de valeurs explicitement validées

- **WHEN** un producteur de confiance construit puis persiste un enregistrement issu des neuf valeurs conformes
- **THEN** les colonnes conservent ces valeurs et NULL explicites sans résolution de référence


### Requirement: Validation ORM explicite de BulkOperationRecord v1

BulkOperationRecord.from_values MUST valider le dict explicite avant construction et retourner une instance non sauvegardée. full_clean MUST valider les neuf attributs avant conversion ORM, même avec exclude ; les refus MUST utiliser des ValidationError statiques sans valeurs. save MUST NOT appeler full_clean implicitement. Ces chemins MUST NOT être présentés comme des contrôles d’autorisation.

#### Scenario: Valeur Python interdite avant conversion ORM

- **WHEN** from_values ou full_clean reçoit une valeur Python non conforme au profil
- **THEN** une ValidationError statique est levée avant conversion ou écriture


### Requirement: Contraintes persistantes de BulkOperationRecord v1

La base MUST imposer non-vacuité des textes obligatoires, appartenance des enums stockés, non-vacuité de scope_context_reference lorsqu’il est non NULL et unicité de la clé primaire dans cette table. La syntaxe SemVer et les types Python exacts MUST rester des contrôles applicatifs explicites ; les contraintes DB MUST NOT être présentées comme leur preuve.

#### Scenario: Insertion SQL structurellement interdite

- **WHEN** une insertion de test autorisée viole une contrainte persistante déclarée
- **THEN** la base refuse l’insertion sans accepter un enregistrement partiellement conforme


### Requirement: Limites du socle BulkOperationRecord v1

Ce socle MUST NOT être présenté comme le contrat BulkOperation complet, une identité de tenant vérifiée, une autorisation, une transition, un worker, un bail, une politique de réessai, une idempotence, une association Job, un staging ou un import/export. Il MUST NOT imposer d’applicabilité des modes selon la variante. Les exigences générales bulk et les formats étendus déclarés MUST rester applicables.

#### Scenario: Aucune exécution ni autorité déduite de la ligne

- **WHEN** un enregistrement préparatoire est stocké
- **THEN** aucun effet métier, contexte autorisé, reprise ou succès d’opération Bulk n’est établi
