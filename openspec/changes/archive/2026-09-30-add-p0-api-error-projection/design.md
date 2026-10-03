# Design: add-p0-api-error-projection

## API figée

```python
API_ERROR_CONTRACT_VERSION = "1.0.0"

class ApiErrorProjectionError(ValueError): ...

def build_infrastructure_error(correlation_id: object, *,
                               internal_error: object) -> dict: ...
```

`internal_error` est un argument opaque requis : il figure dans la
signature pour exprimer l'intention de normalisation (projection D'une
erreur d'infrastructure) mais le corps ne le référence jamais — ni
inspection, ni conversion, ni `repr`, ni `bool`, ni getter. Aucun test
d'introspection AST du paramètre : le comportement hostile et les
constantes suffisent comme preuves.

## Constantes (choix d'implémentation documentés)

- `error_code` : `"INTERNAL_ERROR"`, code métier stable (constante
  privée, valeur publique par l'enveloppe).
- `message` : `"Erreur interne du service."` (choix CGPT exact,
  constante privée, valeur publique par l'enveloppe, non configurable).
- `details` : `{}` frais par appel ; `field_errors` : `[]` frais par
  appel (littéraux par appel, jamais défaut partagé ni constante
  mutée).
- `API_ERROR_CONTRACT_VERSION = "1.0.0"` : constante PUBLIQUE séparée,
  version contractuelle de cette projection ; jamais champ extra de
  l'enveloppe (l'enveloppe contient exactement les 5 champs TECHNICAL).

## Gardes `correlation_id` (les plus simples répondant à l'objectif)

1. `type(correlation_id) is uuid.UUID`, sinon diagnostic constant.
2. Lecture `object.__getattribute__(correlation_id, "int")` APRÈS le
   contrôle de type ; `AttributeError` → diagnostic constant
   `from None` (rejette forgés `object.__new__` sans charge utile,
   sans getters/repr/brut).
3. `type(entier) is int` exact (`bool` et sous-classes rejetés),
   `0 <= entier < 2**128`, sinon diagnostic constant.
4. Reconstitution `uuid.UUID(int=entier)` puis `str()` canonique :
   NE JAMAIS appeler `str()` du UUID forgé brut avant revalidation.
5. Toute version, tout variant, nil (`0`) et max (`2**128 - 1`)
   acceptés : UUID choisi comme format local sans nouvelle exigence
   fonctionnelle ; aucune norme UUIDv7 imposée et AUCUNE importation
   du helper privé `_check_uuid` de `pixs.core.identity` (norme
   privée hors périmètre). Seule la stdlib `uuid` générale est
   réutilisée.

## Retour

Dict frais à 5 clés exactes `error_code`, `message`, `details`,
`field_errors`, `correlation_id`. Le dict mutable est un snapshot
public frais, pas un modèle figé : aucune immutabilité profonde
revendiquée. Erreur d'entrée : `ApiErrorProjectionError(ValueError)`,
diagnostics constants, `from None`, sans écho de valeurs.

## Non-objectifs

Aucune vérification HTTP, runtime, trace backend ou mapping de statut ;
aucune garantie d'absence de secret par contrôle de noms (garantie
constructive seule : ensemble fermé d'entrées — constantes +
corrélation revalidée) ; aucun refactoring ; autres fichiers
préexistants inchangés.
