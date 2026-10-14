## 1. Préparation et implémentation

- [x] 1.1 Fournir quatre artefacts cohérents, delta MODIFIED B03 verbatim sans règle nouvelle ; réussir la validation strict du change avant code.
- [x] 1.2 Ajouter validate_publisher_contract, constantes et export dans src/pixs/backend/bulk_trusted_ports.py, sans modifier les validateurs existants ni compose_bulk_trusted_ports.
- [x] 1.3 Étendre tests/unit/test_bulk_trusted_ports.py par des preuves de non-invocation, refus None/méthode absente/non-Python/propriété/getattr hostile sans hooks ni écho, et acceptation des méthodes Python explorables selon le mécanisme existant.
- [x] 1.4 Compiler séparément les deux fichiers avec le Python .venv du projet ; exécuter les tests unitaires ports et contrats runtime avec le mécanisme unittest existant.
- [x] 1.5 Vérifier strict change sans issue, validation globale OpenSpec sans nouvelle issue (trois WARNING de longueur préexistants qualifiés), UTF-8/LF, delta canonique verbatim, cadrages cohérents et seuls fichiers attendus modifiés.

## Procédure après preuves

Cocher ces tâches seulement après leurs preuves. Sous exclusion intégration, revalider la référence commune puis archiver une seule fois avec --skip-specs. Publier STATISTIQUES.md par un mandat distinct, vérifier six sections, UTF-8/LF et totaux, avant gate, désarmement, libération et retour SÉLECTION du parent CISMP.
