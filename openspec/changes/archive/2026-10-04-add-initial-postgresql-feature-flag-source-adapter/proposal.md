# Adaptateur PostgreSQL initial de la source de fanions

## Why

Le contrat de snapshot et son codec sont déjà disponibles, mais restent purement mémoire. La spécification `feature-flags` exige que les affectations runtime proviennent d'une source persistante et versionnée. Ce change introduit le premier tronçon de cette exigence : un modèle Django PostgreSQL et un chargeur en lecture qui restituent un snapshot canonique à partir d'une version exacte.

Cette évolution est partielle. Elle ne prétend pas implémenter l'administration, l'audit, la corrélation des changements, la convergence des rôles `web`, `worker` et `scheduler`, l'invalidation de cache, la vérification des artefacts ni l'activation d'un runtime.

## What Changes

- Ajouter une table Django versionnée, identifiée par sa `configuration_version`, contenant le document canonique encodé par le codec existant.
- Ajouter la première migration de l'app Django implicite `pixs.backend`, dont le label `backend` et la découverte sans connexion ont déjà été prouvés en processus frais.
- Publier une migration `CreateModel` standard et automatiquement réversible, sans `DeleteModel` personnalisé supplémentaire.
- Ajouter un chargeur public capable de lire une version exacte depuis PostgreSQL, de valider le document avec le codec existant, puis de retourner le snapshot canonique correspondant.
- Importer et charger le modèle seulement après validation de la version demandée, afin que le chargeur reste importable sans configuration Django ni connexion.
- Ajouter des tests unitaires et d'intégration sûrs pour la structure, la lecture, les refus et l'absence de connexion.
- Ajouter une preuve PostgreSQL réelle exécutée dans un schéma de test isolé, unique et nettoyé, sans création ni suppression de base ni de rôle.
- Vérifier la découverte de la migration seulement après sa publication ; la découverte de l'app seule est déjà prouvée.
- Documenter ce nouveau composant dans le README backend par append seul, sans présenter une capacité complète ou opérationnelle.

Le nombre de tests est déterminé par les comportements réellement couverts. Aucun objectif numérique arbitraire n'est fixé.

## Modified Capabilities

### feature-flags

#### Requirement: Affectations hors artefacts

Le système MUST respecter les garanties suivantes.

Les affectations runtime proviennent d'une source persistante versionnée ; aucun paquet, image ni bundle n'embarque d'affectation ; les changements sont administrés, corrélés et audités.

#### Scenario: Affectation embarquée rejetée

- **WHEN** un artefact contient une affectation d'installation ou de production
- **THEN** le build refuse la composition

Aucune norme nouvelle ou modifiée n'est introduite : cette exigence est recopiée strictement depuis la spécification canonique. Aucune `New Capability` n'est créée.

## Impact

### Sources et fichiers

Nouveaux fichiers :

```text
src/pixs/backend/models.py
src/pixs/backend/migrations/__init__.py
src/pixs/backend/migrations/0001_feature_flag_source_snapshot.py
src/pixs/backend/feature_flag_postgres_source.py
tests/unit/test_feature_flag_postgres_source.py
tests/integration/test_feature_flag_postgres_source_integration.py
```

Modification documentaire en append seul :

```text
src/pixs/backend/README.md
```

Aucune autre source n'est modifiée. En particulier :

- `src/pixs/backend/apps.py` reste inchangé ;
- les applications Django existantes ne changent pas ;
- aucun réglage applicatif réel n'est distribué ;
- aucune nouvelle dépendance n'est ajoutée ;
- aucune configuration, aucun secret et aucune route HTTP ne sont introduits ;
- les modules Kernel et codec existants restent inchangés.

### Preuves préservées

Les huit tâches et l'archive du change `add-initial-feature-flag-snapshot-codec` restent acquises. La suite de `154` tests actuellement réussie est une baseline : les ajouts doivent préserver ces `154` tests et ajouter les preuves nécessaires sans remplacer la baseline.

Les tests PostgreSQL réels s'ajoutent à la validation statique et sûre. Ils doivent prouver le round-trip réel dans PostgreSQL, avec nettoyage en cas de succès comme d'échec.

### Effets attendus

- publication de la première migration de l'app `pixs.backend` ;
- création et suppression locales de l'objet de test dans un schéma PostgreSQL isolé ;
- insertion et lecture de données exclusivement synthétiques dans ce schéma ;
- refus normalisés sans exposition d'une valeur de version, d'un document, d'une erreur SQL, d'un credential ou d'une trace technique.

Les tests PostgreSQL réels ne sont pas exécutés par une suite par défaut sans mandat. Leur commande dédiée ne doit pas exposer de secret dans un résultat, un journal, une assertion ou un traceback.

### Limites explicites

Ce change ne prouve ni ne fournit :

- création, modification ou suppression autorisée de snapshots ;
- administration et autorisation des changements ;
- journal d'audit ;
- identifiant de corrélation opérationnelle ;
- promotion, active pointer ou résolution d'une version courante ;
- convergence des processus `web`, `worker` et `scheduler` ;
- cache, fraîcheur ou invalidation ;
- vérification qu'un paquet, image ou bundle n'embarque pas d'affectation ;
- intégration à une route, une API, une CLI ou une activation runtime ;
- isolation tenant/scope au niveau des accès PostgreSQL ;
- provenance canonique du contexte serveur.
