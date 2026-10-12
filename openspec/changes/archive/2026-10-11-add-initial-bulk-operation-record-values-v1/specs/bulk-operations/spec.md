## MODIFIED Requirements

### Requirement: Valeurs préparatoires de persistance BulkOperationRecord v1

Le profil MUST utiliser un dict exact avec exactement les neuf clés operation_id, bulk_type, bulk_version, status, tenant_context_reference, scope_context_reference, format, conflict_strategy et commit_mode. Toutes les clés MUST être fournies explicitement, y compris celles dont la valeur est None. Le profil MUST NOT ajouter de valeur par défaut.

#### Scenario: Neuf valeurs explicitement fournies

- **WHEN** un producteur de confiance fournit exactement les neuf clés conformes
- **THEN** le profil conserve les valeurs sans ajout, omission ni défaut

### Requirement: Références du profil BulkOperationRecord v1

operation_id et tenant_context_reference MUST être des str exactes non vides et opaques. scope_context_reference MUST être None explicite ou une str exacte non vide et opaque. Les références MAY être égales. La validation MUST NOT normaliser, convertir ou résoudre leurs valeurs ; None MUST NOT désigner PLATFORM ou un tenant global.

#### Scenario: Scope explicitement absent

- **WHEN** scope_context_reference vaut None et les autres références sont conformes
- **THEN** la structure accepte cette absence explicite sans contexte global ni résolution

### Requirement: Version du profil BulkOperationRecord v1

bulk_version MUST être une str exacte représentant une version SemVer 2.0.0 complète, validée par parse_version existant après contrôle du type exact. Le profil MUST NOT choisir une version par défaut, décider une compatibilité ou créer une autre grammaire.

#### Scenario: Version non conforme refusée

- **WHEN** bulk_version ne respecte pas le type ou la syntaxe déclarés
- **THEN** la validation refuse la valeur sans la reproduire ni la convertir

### Requirement: Valeurs stockées des enums de BulkOperationRecord v1

bulk_type, status et format MUST être des str exactes égales aux values des membres canoniques respectifs BulkOperationVariant, BulkOperationState et BulkReferenceFormat. conflict_strategy et commit_mode MUST être None explicite ou des str exactes égales aux values des membres canoniques BulkConflictStrategy et BulkCommitMode. Alias, instances Enum, sous-types et conversions implicites MUST NOT être admis.

#### Scenario: Enum déjà construit distinct de sa valeur stockée

- **WHEN** une valeur de champ est une instance Enum au lieu de la str canonique attendue
- **THEN** le profil de stockage la refuse ; les profils Kernel à membres Enum restent inchangés

### Requirement: Validation pure des valeurs BulkOperationRecord v1

validate_bulk_operation_record_values MUST refuser le candidat non dict exact, contrôler les types exacts des clés puis des valeurs avant leur utilisation et refuser clés manquantes ou inconnues. Cette fonction MUST retourner une liste fraîche de Diagnostic VALIDATE statiques, triés et dédupliqués, sans écho de valeur ni comportement étranger. Elle MUST NOT modifier le dict ni effectuer une entrée/sortie.

#### Scenario: Mapping hostile ou incomplet refusé

- **WHEN** le mapping, une clé ou une valeur est interdit, ou une clé est manquante ou inconnue
- **THEN** les diagnostics sont statiques et la validation ne produit aucun effet

### Requirement: Limites du socle BulkOperationRecord v1

Ce socle MUST NOT être présenté comme le contrat BulkOperation complet, une identité de tenant vérifiée, une autorisation, une transition, un worker, un bail, une politique de réessai, une idempotence, une association Job, un staging ou un import/export. Il MUST NOT imposer d’applicabilité des modes selon la variante. Les exigences générales bulk et les formats étendus déclarés MUST rester applicables.

#### Scenario: Aucune exécution ni autorité déduite de la ligne

- **WHEN** un enregistrement préparatoire est stocké
- **THEN** aucun effet métier, contexte autorisé, reprise ou succès d’opération Bulk n’est établi
