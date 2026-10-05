# Proposition — Représentation déclarative des contrats d'événement

## Why

La norme canonique events exige que chaque
événement porte un type, une version, un producteur, un schéma et un périmètre
d'ordre déclaré, et que les contrats de domaine internes et d'intégration publics
restent distincts. Le Kernel ne représente aucun de ces contrats : aucun module
event*.py n'existe dans src/pixs et aucune représentation équivalente n'est
prouvée. Le patron de représentation pure déjà validé pour audit (AuditEvent :
dataclass frozen structurelle, validation fermée, diagnostics sans écho) est la
fondation minimale retenue, sans inventer de wire format, de vocabulaire ni de registre.

## What Changes

- Nouveau module src/pixs/kernel/event_contract.py.
- Deux dataclasses frozen structurelles distinctes, sans __post_init__, sans
  défaut et sans conversion implicite : DomainEventContract et
  IntegrationEventContract.
- Cinq champs ordonnés identiques dans les deux types : event_type,
  contract_version, producer_reference, schema_reference, order_scope_reference.
- Quatre exports publics exactement : les deux dataclasses et deux validateurs.
- Quatre références opaques (event_type, producer_reference, schema_reference,
  order_scope_reference) : type exact str non vide, chaînes d'espaces admises,
  valeurs fournies par un caller trusted ou des fixtures synthétiques, sans
  grammaire, sans vocabulaire et sans registre inventés.
- contract_version validé par le seul parseur public SemVer parse_version ;
  uniquement ses ValueError attendues deviennent des diagnostics statiques ;
  toute autre exception est propagée, sans capture générale.
- Deux validateurs, chacun par type exact vérifié avant toute lecture d'attribut
  et avant tout callback : DomainEventContract est refusé par le validateur
  d'intégration et réciproquement (cross-refus), comme tout objet d'un autre
  type, par un diagnostic unique et statique.
- Diagnostics : step VALIDATE, element event_contract.<champ>, contraintes
  statiques nommant le champ et la règle, sans reproduction de valeur ; liste
  fraîche retournée, triée et dédupliquée par (element, constraint, message).
- Aucune fonction privée d'un autre module n'est utilisée ; les aides internes
  éventuelles restent privées et ne sont pas exportées ; la citation canonique byte exacte de la requirement events est
  reproduite ci-dessous comme source normative.

### Requirement: Événements immuables versionnés

Chaque événement MUST porter type, version, producteur, schéma et périmètre d'ordre déclaré ; les événements de domaine internes et d'intégration publics restent des contrats distincts.

#### Scenario: Contrat d'intégration séparé

- **WHEN** un événement de domaine est exposé vers l'extérieur
- **THEN** il passe par un contrat d'intégration versionné distinct, jamais par exposition directe

### Portée déclarative

- Rien n'est publié, persisté, sérialisé ni diffusé ; aucun wire format, aucun
  registre de schémas, aucune catégorie ajoutée à l'énumeration existante des
  contrats.

## Capabilities

### Modified Capabilities

- events : la requirement canonique « Événements immuables versionnés » (avec
  son Scenario « Contrat d'intégration séparé ») reçoit une représentation
  déclarative partielle dans le Kernel ; le delta normatif du change est la copie
  byte exacte de cette requirement et de son Scenario, sans texte normatif
  ajouté, modifié ni supprimé.

### Added Capabilities

- Aucune.

## Impact

- Fichiers concernés, exactement trois nouveaux chemins :
  - src/pixs/kernel/event_contract.py
  - tests/unit/test_event_contract.py
  - tests/integration/test_event_contract_integration.py
- Aucun autre fichier source, test, README, configuration de paquet, route ou API runtime
  touché ; aucune nouvelle dépendance ; aucune opération Git ; aucun secret.
- Cinquante-huit fichiers de baseline préservés byte à byte : cinquante-deux du
  cycle audit précédent, trois sources du cycle audit (audit_event.py,
  test_audit_event.py, test_audit_event_integration.py), la norme canonique
  events, contracts/models.py et contracts/__init__.py ; la norme canonique audit
  est déjà comprise dans les cinquante-deux et n'est pas comptée deux fois.
- Deux cent cinquante-sept régressions sûres préservées : deux cent trente-huit
  de la commande de régression, dix-huit tests unitaires audit et un test
  d'intégration audit. Nombre de tests nouveaux guidé par les comportements
  réellement prouvés, sans cible numérique.
- Validations : trois compilations natives sous mandats distincts ; tests unitaire
  et d'intégration ciblés ; régression de deux cent cinquante-sept exit 0 ;
  validation OpenSpec stricte du change et canonique concernée avant le code,
  après les tests, puis après cochage ; archivage et rapport STATISTIQUES sous
  mandats distincts.
- Convention TECH9 : les contrats publics portent une version SemVer 2.0.0
  indépendante ; les versions contract et event restent indépendantes des
  versions de composants, ce que la structure isole par construction.

## Limites

- Représentation déclarative partielle uniquement : le Scenario d'exposition
  vers l'extérieur n'est pas prouvé comme flux réel ; seule la séparabilité
  structurelle des deux contrats est éprouvée.
- Non couvert, expressément hors périmètre : instance, payload et enveloppe
  complète (TECH17), audience effective, schéma effectif, ordre effectif,
  partition ou agrégat réel, publisher, outbox, transaction, idempotence,
  diffusion, runtime.
- Les requirements events 2 et 3 (Publication après validation transactionnelle ;
  Consommateurs idempotents et ordonnés) restent NON PROUVÉES ; ce change
  n'affirme aucune complétude de la capacité events, ni de l'audit persistant ou
  de l'administration.

Ces représentations partielles ne remplacent pas `ContractDescriptor` ni les
registres publics : l'identifiant canonique, la catégorie, le propriétaire et les
garanties documentées d'un contrat public restent régis par les contrats
existants (TECH8). Aucun enregistrement ni contrat public complet n'est prouvé.
