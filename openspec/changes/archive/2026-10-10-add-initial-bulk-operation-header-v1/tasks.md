# Tâches — add-initial-bulk-operation-header-v1

- [x] 1. Vérifier le delta MODIFIED exact des quatre exigences canoniques, l'unicité du change actif, UTF-8/LF et la validation OpenSpec avant code.
- [x] 2. Créer le module interne immuable à trois champs obligatoires et son validateur pur, avec types exacts, parseur SemVer existant et diagnostics statiques.
- [x] 3. Créer les tests unitaires comportementaux : conservation, variantes/versions, refus des types et hooks étrangers, immuabilité, diagnostics déterministes sans écho.
- [x] 4. Créer l'intégration en processus frais sous gardes d'effets avec contrôles positifs.
- [x] 5. Compiler séparément les trois fichiers ; exécuter les tests ciblés et les régressions applicables.
- [x] 6. Valider OpenSpec après code ; vérifier les trois sources, le delta canon exact, UTF-8/LF, les façades et les fichiers existants préservés.
- [x] 7. Contrôler l'acceptation complète et les preuves CAB avant de cocher les tâches.

L'archivage --skip-specs et la publication de STATISTIQUES.md restent des mandats
distincts, autorisés après preuves ; aucune case ne les anticipe.

Preuves vérifiées par CGPT : trois compilations exit0 ; 11 tests ciblés dont processus frais gardé et 43 régressions, soit 54 réussites ; validations OpenSpec avant/après code 1/1 exit0 issues[] ; sept fichiers relus exacts UTF-8/LF, delta canon identique, 21 empreintes de référence préservées après réconciliation des évolutions externes AGENTS.md v0.4 / ORCHESTRATED_CODING.md v0.1. Aucune nouvelle dépendance ni façade modifiée. Archivage et rapport restent à exécuter sous mandats distincts.
