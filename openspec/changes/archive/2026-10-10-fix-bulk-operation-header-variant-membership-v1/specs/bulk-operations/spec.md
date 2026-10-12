## MODIFIED Requirements

### Requirement: Référence et variante du profil BulkOperationHeader v1

operation_id MUST être une str exacte non vide, opaque et sans normalisation ; ce contrôle
MUST NOT imposer ni prouver un format UUID. bulk_type MUST être un membre de type exact
BulkOperationVariant, limité aux variantes IMPORT et EXPORT ; une chaîne, un autre type,
une conversion implicite, un alias ou un défaut MUST NOT être admis.

#### Scenario: Type de variante étranger refusé

- **WHEN** bulk_type est la chaîne IMPORT ou un objet étranger au lieu du membre IMPORT de BulkOperationVariant
- **THEN** le profil est refusé sans conversion ni comportement d'objet étranger
