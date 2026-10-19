# Conception BulkAuthorityAction v1

## Références et décisions

Le canon bulk-operations B03 et le contrat AuthorityPort imposent ADMIT, EXECUTE, CANCEL et READ_RESULT. Le module bulk_trusted_ports contrôle déjà les str exactes et refuse les autres types avant le callback.

Un Enum Python simple dans src/pixs/backend/bulk_authority_action.py représente ces quatre actions dans leur ordre de déclaration. Cet ordre ne constitue aucun classement ni séquencement runtime. __all__ expose uniquement BulkAuthorityAction. Aucune façade ni conversion implicite n’est ajoutée.

## Compatibilité et frontière

Les membres ne sont pas des str. Le port existant continue à les refuser avant tout callback. Le choix explicite de .value permet de transmettre la str canonique à un port synthétique, sans modifier le garde existant ni établir une autorisation de production. Aucun fichier de production existant ne change.

## Vérifications

Tests unitaires : membres exacts, noms/valeurs, export public, absence de mixin str, défaut, normalisation et ordre ordinal. Tests d’intégration synthétique : réutilisation des fixtures _compose et _Authority de unit.test_bulk_trusted_ports ; .value transmis une fois à identité conservée, membre Enum refusé avant callback. Les régressions des contrats et ports existants restent applicables.

Trois compilations Python, tests dans le venv projet et validations OpenSpec ciblée stricte puis globale standard et stricte. Contrôle UTF-8/LF, empreintes de production et périmètre. PostgreSQL et navigateur sans objet pour ce contrat passif.

## Limites et retour

Aucun runtime, politique, droit acquis, mapping, défaut, transition, accès réseau, base, audit ou garantie P0. Le retour consiste uniquement à retirer les nouveaux fichiers sous autorisation distincte ; aucune migration. Archivage et STATISTIQUES.md relèvent de mandats distincts après preuves.
