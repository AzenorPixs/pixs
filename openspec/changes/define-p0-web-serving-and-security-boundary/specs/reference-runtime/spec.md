## ADDED Requirements

### Requirement: Entrée web déclarée du profil P0 installable

Le profil P0 installable MUST déclarer son service HTTP, ses hôtes et frontières de transport, les routes du shell construit, de l’API, de l’administration et de santé. Il MUST servir le bundle distribué sans téléchargement de code implicite ni serveur de développement. Les autres rôles et le management MUST conserver leur frontière privée. Une route API inconnue MUST NOT être remplacée par une page du shell.

#### Scenario: Navigation directe vers le shell

- **WHEN** le navigateur ouvre directement une route déclarée du shell sur le paquet installé
- **THEN** le bundle distribué est servi par le service déclaré, avec les contrôles d’accès applicables
- **AND** aucun serveur de développement ni code distant téléchargé implicitement n’est nécessaire

#### Scenario: Route API inconnue

- **WHEN** une requête vise une route API non déclarée
- **THEN** le service produit le refus API déclaré sans exposer de détail privé ni retourner la page HTML du shell

#### Scenario: Profil privé exposé

- **WHEN** la configuration rend un worker, scheduler ou endpoint de management publiquement accessible sans sa frontière explicite
- **THEN** la composition refuse cette exposition selon runtime et operations
