## MODIFIED Requirements

### Requirement: Périmètre canonique et autorisation à la frontière

Le système MUST respecter les garanties suivantes.

Les ressources de périmètre exposent le tenant dans le chemin et vérifient l'appartenance avant lecture ou mutation ; l'authentification Bearer reste le mode privilégié et tout accès anonyme est explicitement déclaré public.

#### Scenario: Tenant d'en-tête non canonique rejeté

- **WHEN** un client fournit le tenant hors chemin canonique en contradiction avec le contexte
- **THEN** la requête est refusée avec une erreur stable
