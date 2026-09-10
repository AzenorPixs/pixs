## MODIFIED Requirements

### Requirement: Types de composants unifiés

Le système MUST prendre en charge les types KERNEL, MODULE, SUBMODULE, PROVIDER, EXTENSION et THEME avec les mêmes mécanismes de manifest et de cycle de vie. Les contributions frontend sont une facette déclarée des composants MODULE et SUBMODULE ; elles MUST NOT créer de type, registre ou lifecycle frontend parallèle.

#### Scenario: Sous-module validé comme module

- **WHEN** un sous-module valide est déclaré
- **THEN** il est découvert, validé et chargé par le système commun sans moteur parallèle

#### Scenario: Facette frontend d'un sous-module

- **WHEN** un sous-module déclare des contributions frontend dans son manifest
- **THEN** elles sont rattachées au même composant, à sa version et à son lifecycle sans créer un composant frontend distinct

### Requirement: Manifest déclaratif unique

Chaque composant MUST fournir un `component.toml` avec identifiant, type, version SemVer, dépendances, capacités et contrats, sans secret ni logique exécutable.

#### Scenario: Secret dans le manifest rejeté

- **WHEN** un manifest contient un secret ou une expression à évaluer
- **THEN** la composition est refusée avec un diagnostic explicite

### Requirement: Identifiants stables namespacés

Le système MUST respecter les garanties suivantes.

Les identifiants `pixs.*` sont réservés ; les composants externes utilisent un espace de noms fournisseur ; tout renommage vaut évolution incompatible.

#### Scenario: Collision d'identifiants refusée

- **WHEN** deux composants déclarent le même identifiant canonique
- **THEN** l'activation est bloquée avant tout chargement

### Requirement: États de composition, installation et santé distincts

Le système MUST distinguer les états de composition, d'installation et de santé ; un composant installé-désactivé, activé-non configuré ou configuré-non sain MUST NOT être confondu avec un composant prêt.

#### Scenario: États non assimilés

- **WHEN** un composant est installé mais désactivé, ou activé mais mal configuré, ou prêt mais dégradé
- **THEN** chaque état est représenté distinctement et la composition ne devient pas ACTIVE tant que manifest, dépendances, contrats et contraintes de sécurité ne sont pas validés
