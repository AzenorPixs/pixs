# Proposal — add-initial-command-metadata-representation

## Why

La requirement canonique `interactions` « Idempotence et traçabilité des commandes » exige
qu'une commande rejouable porte identifiant, corrélation, causalité, contexte de périmètre et
clé d'idempotence. Le premier segment — porter ces métadonnées — est déclarativement
représentable au-dessus du Kernel en réutilisant le `ScopeContext` public déjà prouvé de
`pixs.core.scope`. Le second segment (rejou identique restituant le résultat, rejou divergent
produisant un conflit explicite) et le Scenario « Rejou divergent » sont des garanties
d'exécution : elles restent NON PROUVÉES et ne sont ni implémentées ni simulées ici.

## What Changes

- Publier exactement trois nouvelles sources/tests aux chemins fixes ci-dessous. Les cinq
  artefacts OpenSpec nécessaires (proposal, design, tasks, .openspec.yaml et
  specs/interactions/spec.md) sont préparés et mandatés séparément ; aucun autre fichier
  source, test ou configuration existant ne sera modifié :
  - `src/pixs/core/command_metadata.py` — module direct de `pixs.core`, sans nouveau
    sous-paquet et sans aucune modification de `src/pixs/core/__init__.py` ni d'aucune façade
    existante ; atteinte par chemin direct du module.
  - `tests/unit/test_command_metadata.py`
  - `tests/integration/test_command_metadata_integration.py`
- Exposer deux exports seulement : `CommandMetadata` et
  `validate_command_metadata(command: object) -> list[Diagnostic]`.
- `CommandMetadata` : dataclass `frozen=True, slots=True`, structurelle, sans défaut, sans
  `__post_init__`, sans méthode applicative, sans conversion implicite ; sept champs
  obligatoires dans l'ordre figé `command_id`, `correlation_ids`, `causation_ids`,
  `scope_context`, `command_type`, `subject_id`, `idempotency_key`.
- Sémantique déclarative des champs :
  - `command_id`, `command_type`, `subject_id`, `idempotency_key` : `str` de type exact non
    vide ; les chaînes d'espaces sont des références opaques valides ; aucune normalisation,
    grammaire, longueur, classification, ni validation UUID n'est imposée ou affirmée.
  - `correlation_ids`, `causation_ids` : `tuple` de type exact de `str` exacts non vides ;
    ordre et doublons conservés ; le `tuple` vide est permis pour cette seule représentation,
    sans affirmer de cardinalité d'exécution.
  - `scope_context` : instance exacte du `ScopeContext` public, contrôlée par `type` avant
    toute inspection puis par le `validate_structure` public réutilisé ; seule
    `ScopeStructureError` attendue est convertie en diagnostic fixe de champ, toute erreur
    inattendue est propagée à l'identique.
- Validateur unique fermé : `type(command) is CommandMetadata` avant toute lecture d'attribut
  et tout callback, sinon un unique diagnostic `command_metadata.command` ; agrégation d'au
  plus un refus par champ parmi les sept, le contexte étant validé indépendamment des autres
  champs invalides ; diagnostics `step=VALIDATE`, éléments `command_metadata.<champ>`,
  contrainte et message statiques égaux sans reproduction de valeur ; tri et déduplication
  stables par `(element, constraint, message)` ; listes fraîches et indépendantes à chaque appel.
- Imports publics uniquement : `dataclasses.dataclass`, `pixs.kernel.diagnostics`
  (`VALIDATE`, `Diagnostic`), `pixs.core.scope` (`ScopeContext`, `ScopeStructureError`,
  `validate_structure`), `__future__.annotations` si utilisé. Aucun parser SemVer, aucun
  import d'`AuditEvent`, aucun accès à une fonction privée d'un autre module ; helpers internes
  privés non exportés. Module au-dessus du Kernel : aucun import de `pixs.core` n'entre dans
  le Kernel.
- Norme directe : le delta `specs/interactions/spec.md` est la copie byte exact de la seule
  requirement canonique `interactions` « Idempotence et traçabilité des commandes », Scenario
  « Rejou divergent » inclus ; aucune norme nouvelle, modifiée ou supprimée ; delta canonique
  effectif attendu +0/~0/-0.

## Capabilities

- `interactions` : représentation déclarative partielle des métadonnées de commande ; aucune
  capacité d'exécution ajoutée.

## Impact

- Trois nouvelles sources/tests fixes ; les 76 fichiers de baseline exacts protégés, dont
  `scope`/`core`/`identity` et les cycles antérieurs (audit, fanions, backend, event-contract
  archivé), restent inchangés byte à byte.
- Aucune nouvelle dépendance, aucun package exporté, aucun README, aucune opération Git,
  aucune migration, aucune API runtime, aucune exposition extérieure.
- Réutilise sans les modifier les façades publiques prouvées `pixs.kernel.diagnostics` et
  `pixs.core.scope`.

## Limites

- Métadonnées structurelles partielles uniquement. Ne prouve : ni légitimité d'un `subject_id`
  ou d'un `tenant`, ni topologie de périmètre, ni authentification, ni autorisation, ni
  permissions ; ne construit pas la clé composée `tenant_id`/`subject_id`/`command_type`/
  `idempotency_key` de TECHNICAL §18, et n'affirme aucune déduplication PLATFORM/TENANT.
- Exclues, non simulées, restant NON PROUVÉES : comparaison de payload, empreinte/hash/
  sérialisation, callback/foncteur injecté, restitution de résultat, conflit de rejou effectif,
  déduplication, rétention, persistance, transaction, autorisation, exécution.
- Le second segment de la requirement et son Scenario restent non prouvés ; aucune tâche
  d'exécution n'est cochée par ce change.
- Les cas d'oubli d'un des sept champs requis relèvent de la constructibilité Python
  (champs obligatoires sans défaut) et de l'absence de validateur alternatif, non d'une
  politique nouvelle.

## Validation

- Compilations natives `py_compile` séparées des trois fichiers sous mandats distincts, exits réels.
- Tests unitaires ciblés dérivés des comportements ci-dessus (types exacts fermés avant callback,
  opacités d'espaces, tuples vides/ordres/doublons, cross-type refus `command_metadata.command`,
  réutilisation de `validate_structure` avec propagation des erreurs inattendues, agrégation
  d'un refus par champ, tri/dédup, fraîcheur et indépendance des listes, gel des dataclasses) —
  sans nombre ni longueur imposés arbitrairement.
- Intégration sûre en processus frais `-B` avec environnement réduit déclaré et gardes finies des
  routes déjà acquises, adaptées aux imports publics de `pixs.core` et `pixs.kernel` ; aucun PG
  réel, réseau, horloge, Git ou secret ; marqueur de sortie fixe unique.
- Suite de régressions antérieures préservée, élargie aux tests existants de dépendances
  `scope`/`diagnostics` concernés par la façade réutilisée, sans rejouer les artefacts archivés.
- Validation OpenSpec stricte du change et des specs canoniques (`--specs`) avant le code,
  puis du change et du référentiel (`--all`) après les tests ; validation stricte du change
  post-cochage en mandat distinct ; archivage et `STATISTIQUES.md` sous mandats distincts.
