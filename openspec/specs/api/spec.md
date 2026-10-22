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

### Requirement: Façade web à cookie et API Bearer explicitement distinctes

Le profil local MUST déclarer une façade web à session serveur et cookie protégé inaccessible au JavaScript, avec CSRF. L’API standard et la CLI MUST conserver Authorization: Bearer avec jeton opaque du profil local. Une route Bearer MUST NOT accepter implicitement un cookie comme substitut.

#### Scenario: Cookie seul sur route Bearer
- **WHEN** un client présente uniquement un cookie sur une route Bearer
- **THEN** la route ne l’utilise pas implicitement et retourne le refus prévu

### Requirement: Contrats de transport et stockage navigateur

Routes, contrats et protections MUST indiquer leur mode d’authentification et une règle explicite pour les justificatifs ambigus sans élargir l’admission. Le navigateur MUST NOT persister de jeton accessible au JavaScript par défaut. Attributs du cookie et transport MUST être qualifiés avant code. Les exceptions Super Admin MUST rester préservées sans transformer un justificatif non vérifié en fait de confiance.

#### Scenario: Façade web authentifiée
- **WHEN** un navigateur utilise une route à session serveur
- **THEN** la session courante et les protections du cookie/CSRF sont vérifiées sans jeton persistant accessible au JavaScript
