## Purpose

Les interactions distinguent les commandes de mutation et les requêtes de lecture, exécutées dans des frontières transactionnelles explicites et autorisées.

## ADDED Requirements

### Requirement: Commandes validées et autorisées

Toute commande DOIT être validée métier, autorisée puis exécutée en transaction ; une commande synchrone retourne le résultat, une asynchrone retourne un identifiant d'opération sans présenter la mutation comme acquise.

#### Scenario: Mutation sans autorisation refusée

- **WHEN** une commande ne dispose pas d'une autorisation valide
- **THEN** aucune mutation n'est appliquée et une erreur métier explicite est retournée

### Requirement: Requêtes sans mutation implicite

Une requête de lecture NE DOIT produire aucune mutation métier implicite et DOIT appliquer le filtrage autorisé à la source avant pagination ou projection.

#### Scenario: Lecture filtrée à la source

- **WHEN** une collection contient des ressources non autorisées
- **THEN** seules les ressources autorisées sont retournées, sans filtrage frontal

### Requirement: Idempotence et traçabilité des commandes

Toute commande rejouable DOIT porter identifiant, corrélation, causalité, contexte de périmètre et clé d'idempotence ; un rejou à contenu identique restitue le résultat, à contenu divergent produit un conflit explicite.

#### Scenario: Rejou divergent

- **WHEN** la même clé d'idempotence est réutilisée avec un contenu différent
- **THEN** le système retourne un conflit explicite au lieu d'un double effet
