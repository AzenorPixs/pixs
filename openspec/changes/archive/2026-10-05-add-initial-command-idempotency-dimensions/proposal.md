# Proposal — add-initial-command-idempotency-dimensions

## Why

La requirement canonique `interactions` « Idempotence et traçabilité des commandes »
exige qu'une commande rejouable porte identifiant, corrélation, causalité, contexte de
périmètre et clé d'idempotence ; TECHNICAL §18 et PROJECT §28 précisent que la
déduplication effective utilise au minimum les quatre dimensions `tenant_id`,
`subject_id`, `command_type` et `idempotency_key`. Le cycle `CommandMetadata` publié et
archivé porte ces identifiants et refuse explicitement de construire cette clé. Le
présent change est un jalon structurel utile : collecter exactement ces quatre
dimensions telles qu'elles existent déjà dans une `CommandMetadata` validée par son
validateur public, sans en faire une clé de lookup, un format durable ou une politique
de déduplication. Le second segment de la requirement (rejou identique restituant le
résultat, rejou divergent produisant un conflit explicite) et son Scenario « Rejou
divergent » sont des comportements d'exécution : ils restent NON PROUVÉS, ni
implémentés ni simulés.

## What Changes

- Publier exactement trois nouvelles sources/tests aux chemins fixes ci-dessous, sous
  mandats distincts. Les cinq artefacts OpenSpec du change (proposal, design, tasks,
  .openspec.yaml et specs/interactions/spec.md) sont un périmètre séparé, préparé et
  mandaté pour lui seul ; aucun autre fichier source, test ou configuration existant ne
  sera créé ou modifié :
  - `src/pixs/core/idempotency_dimensions.py` — module direct de `pixs.core`, sans
    nouveau sous-paquet et sans aucune modification de `src/pixs/core/__init__.py` ni
    d'aucune façade existante ; atteinte par chemin direct du module.
  - `tests/unit/test_command_idempotency_dimensions.py`
  - `tests/integration/test_command_idempotency_dimensions_integration.py`
- Exposer deux exports seulement : `CommandIdempotencyDimensions` et
  `collect_command_idempotency_dimensions(command: object) ->
  tuple[CommandIdempotencyDimensions | None, list[Diagnostic]]`.
- `CommandIdempotencyDimensions` : dataclass `frozen=True, slots=True`, structurelle,
  sans défaut, sans `__post_init__`, sans méthode applicative, sans conversion
  implicite ; quatre champs obligatoires dans l'ordre de §18 : `tenant_id`,
  `subject_id`, `command_type`, `idempotency_key`, avec `tenant_id: str | None` et les
  trois autres en `str`. Le constructeur accepte structurellement toute valeur : la
  collecte reste le seul point fermé.
- Sémantique de collecte :
  - le collecteur appelle le `validate_command_metadata` public existant exactement
    une fois avant toute lecture locale d'attribut, sans recontrôler le type ni
    dupliquer aucune règle de `command_metadata` ou de `pixs.core.scope` ;
  - refus : `(None, la liste publique exacte retournée par cet appel, inchangée)` ;
  - succès : nouvelle instance portant les quatre valeurs lues telles quelles dans la
    commande validée, avec la même liste publique vide exacte ;
  - `tenant_id` `None` est uniquement la valeur déjà portée par un `ScopeContext`
    PLATFORM valide, conservée sans sentinelle, substitution, namespace ni politique de
    lookup ; ce n'est pas l'admission d'une clé d'exécution sans tenant ;
  - toute erreur inattendue levée par le validateur public est propagée à l'identique,
    sans capture ni transformation.
- Imports minimums publics : `dataclasses.dataclass`, `validate_command_metadata` de
  `pixs.core.command_metadata`, `Diagnostic` de `pixs.kernel.diagnostics`, et
  `__future__.annotations` si utilisé. Les classes `CommandMetadata` et `ScopeContext`
  ne sont pas importées si elles ne sont pas utilisées. Aucun hash, empreinte,
  sérialisation, concaténation en chaîne unique, normalisation, grammaire nouvelle,
  stockage, cache, fenêtre de rétention ou transaction.
- Norme directe : le delta `specs/interactions/spec.md` est la copie byte exact de la
  seule requirement canonique `interactions` « Idempotence et traçabilité des
  commandes », Scenario « Rejou divergent » inclus ; aucune norme nouvelle, modifiée ou
  supprimée ; delta canonique effectif attendu +0/~0/-0.

## Capabilities

- `interactions` : collecte structurelle des quatre dimensions d'idempotence déjà
  portées ; aucune capacité d'exécution, de déduplication ou de lookup ajoutée.

## Impact

- Trois nouvelles sources/tests fixes ; les soixante-dix-neuf fichiers de baseline
  exacts protégés — les soixante-seize antérieurs (Kernel, `pixs.core` et ses paquets
  `scope`/`identity`, cycles audit, fanions, backend, event-contract archivé)
  plus les trois sources du cycle `CommandMetadata` — restent inchangés byte à byte.
- Aucune nouvelle dépendance, aucun package exporté, aucun README, aucune opération
  Git, aucune migration, aucune API d’exécution métier, aucune exposition extérieure.
- Réutilise sans les modifier les APIs publiques prouvées `validate_command_metadata`,
  `ScopeContext` et `pixs.kernel.diagnostics`.

## Limites

- Représentation de données trusted ou synthétiques uniquement. Ne prouve : aucune
  déduplication effective PLATFORM/TENANT, aucun rejou identique restitué, aucun
  conflit divergent, aucune autorisation, légitimité d'un sujet ou tenant, persistance,
  transaction, rétention, fenêtre de rejeu ou exécution ; ne construit ni clé durable,
  ni format wire, ni index de lookup.
- Le second segment de la requirement et son Scenario restent NON PROUVÉS ; aucune
  tâche d'exécution n'est cochée par ce change.
- La constructibilité structurelle avec valeurs invalides relève de la convention
  publiée des dataclass non validantes, non d'une politique nouvelle.

## Validation

- Compilations natives `py_compile` séparées des trois fichiers sous mandats distincts,
  exits réels.
- Tests unitaires ciblés par comportements : appel public du validateur exactement une
  fois avant lecture locale (espion de l'alias du module) ; identité de la liste
  publique sur refus et sur succès ; `None` PLATFORM conservé à l'identique ; types
  étrangers et sous-classes refusés sans aucune lecture locale ni callback des valeurs
  hostiles ; propagation à l'identique des erreurs inattendues ; constructeur acceptant
  les valeurs invalides ; frozen, slots, absence de défauts, de `__post_init__` et de
  méthodes ; fraîcheur et absence d'état partagé entre appels.
- Intégration sûre en processus frais `-B` avec environnement réduit déclaré et gardes
  finies du cadre déjà acquis : les sondes existantes peuvent être mockées, le
  validateur applicatif public n'est jamais mocké dans l'enfant ; scènes TENANT,
  PLATFORM avec `None` conservé, refus étranger à liste reprise ; aucun PG réel,
  réseau, horloge, Git ou secret ; marqueur de sortie fixe unique.
- Suite de régressions : les trois cent vingt-cinq tests antérieurs déjà identifiés
  (lot de trois cent un du design CommandMetadata et tests `CommandMetadata` vingt
  quatre), sans rejouer les artefacts archivés ; le nombre réel de tests est relevé
  après exécution du nouveau lot, sans cible imposée.
- Validation OpenSpec stricte du change et des specs canoniques (`--specs`) avant le
  code, puis du change et du référentiel (`--all`) après les tests ; validation
  stricte du change post-cochage en mandat distinct ; cochages uniquement après preuves
  observables ; archivage puis `STATISTIQUES.md` (six sections, sondes de modèle
  périodiques de trente minutes indépendantes, cycle conjoint de 1 h 30, totaux croisés, UTF-8/LF, mesures `N/A` motivées) sous mandats
  distincts.
