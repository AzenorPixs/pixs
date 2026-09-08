# authorization-engine Specification

## Purpose
Le moteur d'autorisation décide de façon déclarative, déterministe et bornée, avec filtrage autorisé, cohérence de cache et échec fermé.

## Requirements

### Requirement: Politiques déclaratives versionnées

Chaque politique DOIT déclarer identifiant, version, propriétaire, effet DENY ou ALLOW, sélecteurs de sujets, ressources, actions et périmètres, conditions typées, obligations et validité, sans code arbitraire ni expression distante.

#### Scenario: Politique à code rejetée

- **WHEN** une politique embarque du code exécutable ou une expression distante
- **THEN** elle est refusée avant activation

### Requirement: Décisions et filtrage tracés

Le contrat de décision retourne effet, motif fonctionnel, version de politique et échéance ; le filtrage autorisé traduit la décision en contrainte source avant pagination ou export ; les décisions positives expirent et sont invalidées après tout changement de politique, ACL, rôle, appartenance, périmètre, révocation ou assurance.

#### Scenario: Décision périmée non réutilisée

- **WHEN** une mutation invoque une décision antérieure à un changement de politique
- **THEN** la politique courante est réévaluée avant toute exécution

### Requirement: Groupes bornés et délégation auditée

Les groupes imbriqués restent acycliques et bornés ; toute délégation, usurpation ou élévation est explicitement accordée, limitée en temps et périmètre, soumise à l'assurance requise et auditée ; l'indisponibilité du moteur échoue fermé pour mutations et données protégées.

#### Scenario: Moteur indisponible

- **WHEN** le moteur ne peut être joint pour une mutation sensible
- **THEN** l'opération est refusée au lieu d'une autorisation implicite
