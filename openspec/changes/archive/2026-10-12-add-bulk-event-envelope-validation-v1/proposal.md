## Why

Le runtime Bulk v1 doit valider l'enveloppe logique `EventEnvelopeV1` avant toute outbox/publication B11, sans créer de port, d'ORM, de publication, d'horloge ni de preuve propriétaire. `JSONValueV1` dispose déjà de `validate_json_value` borné ; il manque la garde exacte des 13 clés d'enveloppe avec paramètres serveur obligatoires.

## What Changes

- Ajouter un unique validateur public pur `validate_bulk_event_envelope_values(candidate,*,max_depth,max_members,non_tenant_authorized) -> list[Diagnostic]`.
- Contrôler mapping exact 13 clés, types exacts avant valeurs, opaques `str` exacts non vides UTF-8 sans NUL, `kind` exact `DOMAIN|INTEGRATION`, `event_version` SemVer complète, `occurred_at` `datetime` exact aware UTC, `tenant_context_reference`/`causation_id` `str|None`, payload `JSONValueV1` borné via helper existant sans borne par défaut.
- Exiger `max_depth`/`max_members` `int` exacts `>0` et `non_tenant_authorized` `bool` exact obligatoires ; refuser `tenant None` si `False`, sans inférer d'autorité si `True`.
- Ne pas prouver parse/sérialiseurs, doublons après `dict`, schéma propriétaire, déclarations, minimisation, absence de secret ; ne pas capturer, snapshotter, créer d'enveloppe, promettre d'immutabilité, ni ajouter port/ORM/publish/horloge.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- events : outillage partiel de B11 déjà validé ; exigence `MODIFIED` recopiée verbatim, aucune annexe ou règle ajoutée.

## Impact

Trois nouveaux fichiers Python : `src/pixs/backend/bulk_event_envelope_values.py`, `tests/unit/test_bulk_event_envelope_values.py`, `tests/integration/test_bulk_event_envelope_integration.py`, plus quatre artefacts de change. Aucun ORM/migration, provider, worker, publication, route HTTP, dépendance, Git ou déploiement. Le RUN reprend SÉLECTION après archive `--skip-specs` et rapport vérifiés.
