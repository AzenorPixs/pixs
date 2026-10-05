# feature-flags — Delta

## MODIFIED Requirements

### Requirement: Échec fermé pour le sensible

Le système MUST respecter les garanties suivantes.

Une valeur absente, invalide ou périmée MUST appliquer la politique de repli déclarée. À l'exécution, seules les politiques déclaratives DENY et DEFAULT MUST être reconnues. DENY MUST refuser l'opération sans exposer de valeur de fanion. DEFAULT MUST appliquer la valeur par défaut validée de la définition uniquement pour une fonctionnalité non sensible ; DEFAULT MUST NOT être appliqué à une permission, une mutation, une donnée protégée ou un contrat. Une permission, une mutation, une donnée protégée ou un contrat MUST être refusé sur valeur absente, invalide ou périmée, quelle que soit la politique déclarée. Une référence de repli inconnue ou incompatible MUST produire un refus sans valeur et MUST NOT être convertie en alias implicite. La classification sensible ou non sensible MUST provenir du contexte applicatif canonique côté serveur ; le client et le frontal MUST NOT fournir cette classification. Le frontal MUST faire réévaluer le fanion côté applicatif avant toute exposition protégée.

#### Scenario: Fanion d'autorisation indisponible

- **WHEN** le fanion requis pour une mutation est indisponible
- **THEN** l'opération est refusée au lieu d'un repli permissif

#### Scenario: Repli par défaut sur fonctionnalité non sensible

- **WHEN** une valeur absente, invalide ou périmée concerne une fonctionnalité non sensible déclarée avec le repli DEFAULT
- **THEN** la valeur par défaut validée de la définition est appliquée et aucune décision d'autorisation n'en découle

#### Scenario: Référence de repli inconnue refusée

- **WHEN** un fanion déclare une référence de repli hors du vocabulaire d'exécution borné
- **THEN** l'évaluation est refusée sans exposition de valeur
