## 1. Préparation et implémentation

- [x] 1.1 Fournir quatre artefacts cohérents et un delta MODIFIED B03 verbatim sans règle nouvelle ; réussir la validation stricte du change avant code.
- [x] 1.2 Ajouter validate_download_contract, ses constantes et son export dans src/pixs/backend/bulk_trusted_ports.py, sans modifier les validateurs existants ni la composition.
- [x] 1.3 Étendre tests/unit/test_bulk_trusted_ports.py par des preuves d'acceptation, de refus fermés, de non-invocation et de diagnostics fixes sans écho.
- [x] 1.4 Après extension autorisée de la ressource de tests, compiler séparément les deux fichiers avec le Python .venv du projet et exécuter les tests unitaires ports et contrats runtime.
- [x] 1.5 Vérifier validation stricte du change, absence de nouvelle issue OpenSpec, UTF-8/LF, delta canonique verbatim, cohérence des cadrages et absence de modification hors périmètre.

## Procédure après preuves

Cocher uniquement après preuves. Sous exclusion d'intégration, revalider la référence commune puis archiver une seule fois avec --skip-specs. Publier STATISTIQUES.md par un mandat distinct ; vérifier ses six sections, UTF-8/LF et totaux avant gate, désarmement, libération et retour à la sélection du parent CISMP.
