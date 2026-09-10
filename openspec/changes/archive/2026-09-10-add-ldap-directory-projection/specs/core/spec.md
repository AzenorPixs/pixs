## MODIFIED Requirements

### Requirement: Primitives minimales communes

pixs.core MUST exposer utilisateurs, identités numériques, groupes,
appartenances, tenants, rôles, ACL et permissions comme capacités communes de
bas niveau, consommées via contrats et services. La consultation des identités
numériques, groupes et appartenances MAY utiliser une projection d'annuaire
optionnelle sous contrat ; PostgreSQL MUST rester leur source de vérité et le
service MUST fournir un repli PostgreSQL contrôlé.

#### Scenario: Primitive consommée par contrat

- **WHEN** un module a besoin d'une identité ou d'une appartenance
- **THEN** il passe par le contrat ou le service exposé, sans accès direct aux tables internes
