## 1. Persistance runtime
- [x] 1.1 Ajouter les quatre modèles, validateurs explicites et décodage UTC de confiance, sans defaults ni champs logiques supplémentaires.
- [x] 1.2 Enregistrer les modèles par import minimal et ajouter la migration 0004 réversible, sans modifier les contrats existants.
- [x] 1.3 Implémenter CAS/transitions/checkpoints atomiques et baux persistants sous politique explicite.

## 2. Preuves
- [x] 2.1 Ajouter les tests offline sous gardes positives et compiler les six Python.
- [x] 2.2 Prouver en PG isolé contraintes, concurrence CAS/baux, rollback, expiry/perte/reprise, identités des tables et nettoyage.
- [x] 2.3 Vérifier les202 régressions existantes, strict qualifié, UTF8/LF et absence d'écriture hors périmètre.

## Procédure après preuves des tâches
Cocher les tâches uniquement après leurs preuves. Archiver une seule fois avec --skip-specs, publier STATISTIQUES.md sous mandat distinct, vérifier ses six sections et totaux, puis revenir à SÉLECTION sans fin globale.
