# Conception — validation structurelle de DownloadPort

## Sources
Le canon bulk-operations B03, Ports serveur déclarés et Frontière du contrat autorise ce choix interne de Python. La méthode canonique unique est authorize_then_issue_temporary_reference. Le validateur ObjectStoragePort existant dans bulk_object_staging.py reste inchangé.

## Décisions
- Ajouter _DOWNLOAD_SCOPE = "bulk_download_port" et _DOWNLOAD_METHODS = ("authorize_then_issue_temporary_reference",).
- Ajouter validate_download_contract(component: object) -> list[Diagnostic] en appelant uniquement _structural_refusals avec ces constantes, puis l'exporter dans __all__.
- Préserver _capture_python_method, les validateurs existants et compose_bulk_trusted_ports sans modification.
- Vérifier par des fournisseurs synthétiques l'absence d'invocation, l'acceptation des méthodes Python explorables et les refus des composants absents, méthodes non Python, propriétés, descripteurs et accès dynamiques, sans écho de valeurs.
- Conserver les politiques existantes du helper concernant staticmethod et classmethod.

## Limites
Ce contrôle de structure n'atteste ni la fraîcheur d'une autorisation, ni la validité d'une référence temporaire, ni un service de téléchargement opérationnel. Aucun effet externe, accès PostgreSQL ou changement frontend.
