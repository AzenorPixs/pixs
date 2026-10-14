# api Specification

## Purpose
L'interface applicative expose les capacités via des contrats HTTP versionnés, stables et documentés, consommables indépendamment du frontal de référence.

## Requirements

### Requirement: Application de l'exception Super Admin

Les exigences et scénarios de contrôle applicatif de cette capacité MUST s'appliquer sous réserve de l'exception définie par `authorization`, dans le périmètre du seul compte décrit par `initial-administration`. Les comptes ordinaires MUST conserver leurs contrôles. Les profils structurels préparatoires MUST rester inchangés.

#### Scenario: API tenant-scoped du Super Admin

- **WHEN** le compte Super Admin authentifié vise le chemin canonique d'un tenant explicitement accordé avec une dérogation ACL
- **THEN** l'ACL dérogée ne bloque pas l'appel et le tenant du chemin reste canonique
- **AND** un autre tenant fourni par en-tête ne remplace pas ce contexte

### Requirement: Contrats OpenAPI versionnés par majeure

Chaque capacité exposée MUST disposer d'un contrat OpenAPI publié et versionné ; la majeure figure dans le chemin, les évolutions compatibles conservent l'URL, toute rupture impose une nouvelle majeure avec coexistence déclarée.

#### Scenario: Rupture sans nouvelle majeure bloquée

- **WHEN** une évolution incompatible conserve la même majeure
- **THEN** le build refuse la publication du contrat

### Requirement: Enveloppes stables et erreurs typées

Le système MUST respecter les garanties suivantes.

Les succès utilisent données, métadonnées et liens avec pagination par curseur ; les erreurs suivent un code métier versionné, un message, des détails et un identifiant de corrélation, sans secret ni trace interne ; les commandes rejouables portent une clé d'idempotence.

#### Scenario: Rejou identique restitué

- **WHEN** la même clé d'idempotence est rejouée avec un contenu identique
- **THEN** le résultat enregistré est restitué au lieu d'un double effet

### Requirement: Périmètre canonique et autorisation à la frontière

Le système MUST respecter les garanties suivantes.

Les ressources de périmètre exposent le tenant dans le chemin et vérifient l'appartenance avant lecture ou mutation ; l'authentification Bearer reste le mode privilégié et tout accès anonyme est explicitement déclaré public.

#### Scenario: Tenant d'en-tête non canonique rejeté

- **WHEN** un client fournit le tenant hors chemin canonique en contradiction avec le contexte
- **THEN** la requête est refusée avec une erreur stable
