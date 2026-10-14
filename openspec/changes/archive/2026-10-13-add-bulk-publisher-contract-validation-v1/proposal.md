# proposal — add-bulk-publisher-contract-validation-v1

## Pourquoi
Le tableau `Ports serveur déclarés` de `bulk-operations` déclare `PublisherPort/publish_declared_event`, mais `bulk_trusted_ports.py` ne fournit aucune validation structurelle correspondante, contrairement aux quatre ports optionnels existants.

## Quoi
Ajouter seulement `validate_publisher_contract`, la constante méthode `publish_declared_event` et le scope `bulk_publisher_port`, avec export `__all__`, selon les mêmes conventions `_structural_refusals` que `validate_audit_contract`. Tests comportementaux de non-invocation, refus `None`/méthode absente/non-Python/propriété/`getattr` hostile sans hooks ni écho, acceptation des méthodes Python réellement explorables par le helper existant.

## Non-objectifs
Aucun câblage nouveau dans `compose_bulk_trusted_ports`, aucune émission, aucun argument/résultat normatif, aucun défaut/champ/schéma/runtime/permission externe. Deux sources seulement : `src/pixs/backend/bulk_trusted_ports.py` et `tests/unit/test_bulk_trusted_ports.py`. Aucune modification des profils préparatoires livrés.
