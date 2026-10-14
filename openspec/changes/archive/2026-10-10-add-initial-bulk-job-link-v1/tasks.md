# Tâches — add-initial-bulk-job-link-v1

- [x] 1. Vérifier le delta MODIFIED exact des deux exigences canoniques, l'unicité du change actif et UTF-8/LF.
- [x] 2. Créer le module interne BulkJobLink immuable à deux références explicites et son validateur pur selon D2–D5 ; imports dataclasses/diagnostics seuls, façade inchangée.
- [x] 3. Créer les tests unitaires comportementaux : conservation opaque, égalité refusée, types/objets hostiles sans hooks, diagnostics statiques triés/dédupliqués sans écho, immuabilité et champs obligatoires.
- [x] 4. Créer le test en processus frais isolé, sous gardes d'effets avec contrôles positifs et compteurs nuls pendant import/validation.
- [x] 5. Compiler séparément les trois nouveaux fichiers ; exécuter les tests ciblés et les régressions applicables de pureté/façades et vocabulaires Job/Notification.
- [x] 6. Valider le change OpenSpec avant et après code : aucune ERROR, seul avertissement de longueur déjà accepté.
- [x] 7. Relire les trois fichiers et les artefacts ; vérifier les empreintes des sources/cadrages/canon existants, l'absence d'écriture hors périmètre et l'acceptation complète sans inspection Git.

L'archivage --skip-specs et la publication de STATISTIQUES.md restent des phases ultérieures distinctes, autorisées après preuves ; aucune case ne les anticipe.

Preuves vérifiées par CGPT : trois compilations exit 0 ; 9 tests ciblés dont processus frais et 20 régressions (29 réussites), exits 0 ; change validé avant/après 1/1 sans issue ; 96 empreintes de référence préservées, trois sources relues, UTF-8/LF et delta canon exact. Aucun archivage ni rapport anticipé.
