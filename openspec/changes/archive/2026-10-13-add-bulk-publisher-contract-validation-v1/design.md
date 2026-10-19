# design — add-bulk-publisher-contract-validation-v1

## Contexte
Source normative : `openspec/specs/bulk-operations/spec.md` (B03, `Ports serveur déclarés` avec `PublisherPort/publish_declared_event`, `Frontière du contrat`) et `openspec/specs/events/spec.md` (B11, sans modification). Source : `src/pixs/backend/bulk_trusted_ports.py` (`_structural_refusals`, `_AUDIT_METHODS`, `_AUDIT_SCOPE`, `validate_audit_contract`).

## Décisions
- `_PUBLISHER_METHODS = ("publish_declared_event",)` et `_PUBLISHER_SCOPE = "bulk_publisher_port"`, miroir de `_AUDIT_METHODS`/`_AUDIT_SCOPE`.
- `def validate_publisher_contract(component: object) -> list[Diagnostic]: return _structural_refusals(component, _PUBLISHER_METHODS, _PUBLISHER_SCOPE)`, sans invocation de méthode.
- Ajout de `"validate_publisher_contract"` à `__all__`, sans toucher à `compose_bulk_trusted_ports` ni aux quatre validateurs existants.
- Capture via `_capture_python_method` existant : `None`, propriété, `__getattr__` hostile et méthode non-Python refusés sans hooks ni écho ; méthode Python réellement explorable par le helper existant (instance ou fonction attachée) acceptée ; politiques du helper inchangées.

## Non-décisions
Aucune émission, aucun transport, aucun bail, aucune séquence, aucune outbox, aucune persistance, aucune autorisation effective, aucun format public nouveau.
