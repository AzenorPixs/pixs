# Tasks — add-initial-identity-assurance-vocabulary-v1

- [x] Créer le seul fichier tests/unit/test_identity_assurance.py avec unittest et stdlib existante, sans dépendance nouvelle.
- [x] Tester en unitaire la fermeture exacte CLAIMED, VERIFIED, PROOFED avec type et littéral, le refus FOREIGN, None et absence sans défaut, et l'absence d'ordre intrinsèque.
- [x] Créer le seul fichier tests/integration/test_identity_assurance_integration.py avec unittest et stdlib existante.
- [x] Tester en intégration l'import frais et l'identité nominale avec consommateurs authz ; bloquer imports de modules DB non déjà chargés, sockets et écritures observables, sans invocation des ports horloge, audit ou auth ; noter que l'import lit nécessairement des modules Python.
- [x] Vérifier les régressions identité et authz et la préservation des garanties existantes.
- [x] Compiler chacun avec py_compile, contrôler UTF-8 et fins de ligne LF, vérifier production et façades existantes inchangées par contrôle des contenus et empreintes, sans inspection Git.
- [x] Exécuter les validations OpenSpec applicables sans affirmer de strict sans observation ; seule alerte de longueur canonique exacte acceptée.
- [x] Préparer l'archivage du change et le rapport STATISTIQUES, sans Git.

## Preuves de qualification avant archivage

- Tests dédiés : 6 unitaires et 1 intégration fraîche, codes natifs 0.
- Régressions identité/authz : 91 tests, code natif 0 ; total réussi 98.
- Syntaxe : py_compile de chacun des deux fichiers, deux codes natifs 0.
- UTF-8/LF et contenus natifs vérifiés ; production et façades existantes inchangées par empreintes, sans inspection Git.
- Validation ciblée stricte du change préparé : 1/1, code natif 0 ; contrôle final et global à réexécuter avant publication.
- Incident de lancement : import pixs absent du venv, résolu par PYTHONPATH=src limité au processus après prévol neuf ; aucun changement source.
- Archivage prévu sous exclusion avec --skip-specs : canon déjà identique préservé. Rapport STATISTIQUES.md séparé après archive et collecte finale ; aucune preuve d’archive ou de rapport n’est anticipée ici.
