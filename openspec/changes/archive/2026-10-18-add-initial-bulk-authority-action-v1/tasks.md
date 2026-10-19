# Tâches BulkAuthorityAction v1

- [x] 1. Confirmer canon, absence d’équivalent et indépendance du sous-lot.
- [x] 2. Ajouter le seul Enum passif BulkAuthorityAction et son export public.
- [x] 3. Prouver fermeture, absence de défaut/ordre et préservation de la frontière des ports synthétiques.
- [x] 4. Exécuter syntaxe, tests ciblés/régressions et validations OpenSpec applicables.
- [x] 5. Vérifier UTF-8/LF, empreintes de production inchangées et périmètre avant archivage distinct.

## Preuves avant archivage

Trois fichiers Python compilés avec le venv projet : exit 0. Tests unitaires, intégration synthétique et régressions des contrats/ports : 76 tests, OK, exit 0. Validation ciblée OpenSpec stricte : exit 0 ; skip_specs accepté. Validation globale standard : 186/186, exit 0. Strict global : exit 1 uniquement pour quatre WARNING historiques de longueur (bulk-operations requirements[6], [10], [13] ; identity-assurance requirements[4]), zéro ERROR. Aucun canon corrigé hors périmètre.

Sept fichiers nouveaux relus identiques aux contenus approuvés, UTF-8/LF. Empreintes des ports, contrats et cadrages concernés inchangées. Les tests sont synthétiques et n’établissent aucune autorisation de production. Archivage, publication CAB et rapport STATISTIQUES restent à réaliser par mandats distincts.
