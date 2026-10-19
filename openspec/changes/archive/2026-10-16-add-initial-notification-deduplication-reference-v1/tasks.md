# Tâches — Références préparatoires de déduplication

## 1. Préparation

- [x] 1.1 Valider strictement le change complet et vérifier que son delta reproduit exactement les deux exigences canoniques.

## 2. Implémentation et tests

- [x] 2.1 Ajouter uniquement le profil immuable à deux champs et son validateur défensif selon design.md.
- [x] 2.2 Ajouter et exécuter les tests unitaires des valeurs exactes, refus, objets hostiles, diagnostics et immuabilité.
- [x] 2.3 Ajouter et exécuter l'intégration en processus frais avec contrôles positifs des gardes et absence d'effet.

## 3. Qualification

- [x] 3.1 Compiler séparément les trois fichiers Python.
- [x] 3.2 Exécuter les régressions existantes de notifications avec résultats observés.
- [x] 3.3 Vérifier UTF-8/LF, périmètre des fichiers, absence de secret et conservation du canon.
- [x] 3.4 Valider strictement le change et notifications, relever les validations globales et leurs diagnostics réels, puis vérifier l'éligibilité à l'archivage.

L'archivage --skip-specs et le rapport STATISTIQUES.md nécessitent chacun leur mandat CAB distinct après preuve de toutes les tâches.
