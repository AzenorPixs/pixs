## Context

La source normative reste `openspec/specs/events/spec.md` (B11, annexes `EventEnvelopeV1`/`JSONValueV1`) et `src/pixs/backend/bulk_runtime_contracts.py` (`validate_json_value`, `Diagnostic`/`VALIDATE`, `parse_version`). Les archives Bulk précédentes sont livrées ; leurs sources et preuves sont préservées par empreinte, sans replay PG pour ce lot sans ORM.

## Goals / Non-Goals

Garder en mémoire la forme exacte d'une enveloppe candidate sans effet externe. Ce lot ne réalise ni admission, ni persistance, ni outbox SQL, ni publisher, ni inbox, ni séquence, ni bail, ni retry, ni dead-letter, ni validation de schéma propriétaire, ni minimisation, ni preuve d'absence de secret.

## Decisions

- Clés logiques exactes dans l'ordre canonique : `event_id`, `kind`, `event_type`, `event_version`, `producer_reference`, `schema_reference`, `order_scope_reference`, `occurred_at`, `subject_reference`, `tenant_context_reference`, `correlation_id`, `causation_id`, `payload`. `type(candidate) is dict`, clés `str` exactes, refus si clé manquante ou inconnue ; aucune omission, défaut, coercition, ni nouveau wire format.
- Garde en deux temps : types exacts de toutes les clés puis valeurs/structures avant `parse_version`, comparaison étrangère ou appel `validate_json_value`. Diagnostics `VALIDATE` statiques, triés, dédupliqués, sans écho de valeur. Liste fraîche à chaque appel.
- Opaques : `event_id`, `event_type`, `producer_reference`, `schema_reference`, `order_scope_reference`, `subject_reference`, `correlation_id` sont `str` exacts non vides UTF-8 sans NUL ; `tenant_context_reference` et `causation_id` admettent `None` explicite avec même règle si `str`. `kind` est `str` exact `DOMAIN` ou `INTEGRATION`. `event_version` est `str` exacte acceptée par `parse_version` sans normalisation.
- `occurred_at` : `type(value) is datetime` puis `value.tzinfo is timezone.utc` ; refus des dates naïves, décalées, ZoneInfo ou tzinfo étrangers avant tout callback, sans utcoffset/astimezone/conversion ni horloge.
- Paramètres serveur keyword-only obligatoires : `max_depth` et `max_members` `type is int` et `>0`, `non_tenant_authorized` `type is bool`. Tout paramètre invalide produit un refus `bulk_event_envelope_values.<param>` et arrête la validation sans utiliser le payload. Aucune borne par défaut.
- Règle tenant : si `tenant_context_reference is None` et `non_tenant_authorized is False`, refus fermé ; si `True`, `None` admis sans prouver un contexte non-tenant, une autorisation, ni une existence.
- Payload : tout `JSONValueV1` admis (`None`, `bool` exact, `int` exact, `float` exact fini, `str` Unicode valide y compris vide/NUL, `list`/`dict` exacts) délégué à `validate_json_value(payload,max_depth=max_depth,max_members=max_members)` ; diagnostics préfixés au scope enveloppe sans ajout de sémantique. Les doublons de clés après construction `dict` ne sont ni détectés ni annoncés.
- Pureté : stdlib + `Diagnostic`/`VALIDATE` + `parse_version` + `validate_json_value` uniquement ; sans I/O, ORM, import dynamique, état global mutable, capture, snapshot, classe publique, ni modification du `dict` candidat et des exports existants. `__all__` contient uniquement `validate_bulk_event_envelope_values`.

## Validation

`py_compile` des 3 Python ; unitaires frontières 13 clés, 9 `str` obligatoires, opaques, `kind`, SemVer, UTC aware, garde `None`, bornes JSON, hostiles sans hooks, fraîcheur des listes ; intégration en processus frais sous gardes positives sans fichiers/réseau/processus/base/Core concret ; régressions existantes ; strict du change sans issue ; UTF-8/LF et périmètre vérifiés. Archive unique `--skip-specs` puis `STATISTIQUES.md` sous mandat distinct, avant retour SÉLECTION.

## Risks and Limits

Un candidat valide ne prouve ni schéma propriétaire, ni déclaration, ni minimisation, ni absence de secret, ni immutabilité, ni publication, ni ordre global. Les types hostiles ne doivent ni être comparés ni encoder hors garde exacte. Les limites serveur ne doivent pas étendre le schéma.
