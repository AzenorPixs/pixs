## ADDED Requirements

### Requirement: Frontière Core Auth et dépendance unidirectionnelle

pixs.core MUST rester propriétaire de User, DigitalIdentity, liens, groupes, appartenances, tenants, rôles, ACL et permissions. pixs.auth MUST consommer ses contrats publics pour ces données. Core MUST NOT dépendre d'une implémentation Auth ni héberger ses protocoles, sessions ou secrets. Les contrats purs partagés existants MUST rester réutilisables sans déplacement imposé.

#### Scenario: Révocation canonique
- **WHEN** Core confirme la révocation d'une DigitalIdentity
- **THEN** Auth invalide les accès concernés selon son contrat sans écriture Core dans une table privée Auth ni cycle de dépendances

### Requirement: Moyens multiples sans multiplication implicite des identités

Une DigitalIdentity MUST pouvoir être liée explicitement à plusieurs moyens et sources d'authentification sous propriété Auth sans modifier la cardinalité User 0..1 et DigitalIdentity 0..1. Une méthode, un identifiant d'annuaire ou un principal Kerberos MUST NOT devenir un nouvel identifiant canonique Core ni créer de droit implicite.

#### Scenario: Passkey et principal pour une identité
- **WHEN** une passkey et un principal Kerberos sont liés explicitement à la même identité
- **THEN** son UUID Core et sa liaison User sont conservés sans compte ni permission supplémentaire
