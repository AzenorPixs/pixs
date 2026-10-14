# Tâches — add-initial-bulk-operation-status-v1

- [x] 1. Vérifier le delta MODIFIED exact des trois exigences canoniques, l'unicité du change actif, UTF-8/LF et la validation OpenSpec avant code.
- [x] 2. Créer le module interne immuable à deux champs obligatoires et son validateur pur, avec types exacts et diagnostics statiques.
- [x] 3. Créer les tests unitaires comportementaux : dix états, références opaques, refus des types et hooks étrangers, immuabilité, absence de correction et diagnostics sans écho.
- [x] 4. Créer l'intégration en processus frais sous gardes d'effets avec contrôles positifs.
- [x] 5. Compiler séparément les trois fichiers ; exécuter les tests ciblés et les régressions applicables.
- [x] 6. Valider OpenSpec après code ; vérifier les trois sources, le delta canon exact, UTF-8/LF, les façades et les fichiers existants préservés.
- [x] 7. Contrôler l'acceptation complète et les preuves CAB avant de cocher les tâches.

L'archivage --skip-specs et la publication de STATISTIQUES.md restent des mandats
distincts, autorisés après preuves ; aucune case ne les anticipe.

Preuves contrôlées par CGPT : trois compilations exit0 ; 11 tests ciblés et
54 régressions réussis (65/65). OpenSpec avant/après code : 1/1, exit0,
sans ERROR. Trois sources et delta MODIFIED byte-identiques aux contenus
validés, UTF-8/LF ; 102 fichiers existants préservés, façades et dépendances
inchangées. Chaque effet est relié à son mandat CAB, sa décision CGPT,
une permission native once et un outil natif terminé. Archivage et rapport
statistique restent distincts et ne sont pas anticipés.
