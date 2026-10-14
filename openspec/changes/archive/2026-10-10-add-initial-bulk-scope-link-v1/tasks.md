## 1. Profil préparatoire

- [x] 1.1 Ajouter BulkScopeLink immuable à deux champs explicites sans défaut, en conservant les références opaques et égales.
- [x] 1.2 Ajouter validate_bulk_scope_link pur avec types exacts avant attributs/opérations et diagnostics statiques VALIDATE triés/dédupliqués sans écho.
- [x] 1.3 Couvrir les cas valides, invalides, absents, hostiles, dérivés, l'immutabilité et le déterminisme par tests unitaires.
- [x] 1.4 Prouver l'import et la validation dans un processus frais sous gardes d'effets à contrôles positifs, sans dépendance concrète pixs.core.

## 2. Validations avant archivage

- [x] 2.1 Compiler séparément les trois nouveaux fichiers Python et exécuter les tests ciblés et régressions bulk.
- [x] 2.2 Valider strictement le change OpenSpec, contrôler l'identité du delta avec les trois exigences canoniques et la cohérence des cadrages.
- [x] 2.3 Vérifier UTF-8/LF, absence de secrets, périmètre et empreintes de référence; ne cocher les tâches qu'après preuves.
