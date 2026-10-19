# Proposition — validation structurelle du téléchargement Bulk v1

## Pourquoi
Le port DownloadPort et sa méthode authorize_then_issue_temporary_reference sont déclarés par le canon bulk-operations, mais leur validation structurelle manque dans bulk_trusted_ports.py. ObjectStoragePort dispose déjà de sa validation dans bulk_object_staging.py : aucun doublon n'est nécessaire.

## Quoi
Ajouter uniquement validate_download_contract, son export et ses constantes, en réutilisant _structural_refusals sans invocation. Prouver l'acceptation des méthodes Python explorables, les refus fermés, la non-invocation des hooks et les diagnostics fixes sans écho.

## Non-objectifs
Aucun accès temporaire émis, aucune autorisation effective, aucun contrat de réponse ou argument nouveau, aucune composition, aucun fournisseur de production, aucune mutation du stockage ni du canon. Deux fichiers de code seulement : src/pixs/backend/bulk_trusted_ports.py et tests/unit/test_bulk_trusted_ports.py. Les tests communs attendent l'extension de réservation.
