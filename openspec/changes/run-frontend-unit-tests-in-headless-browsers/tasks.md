# Tasks

- [ ] 1. Créer frontend/tests/browser/test-adapter.mjs (collecteur de cas)
- [ ] 2. Créer frontend/tests/browser/assert-adapter.mjs (subset strict des 5 méthodes assert/strict utilisées)
- [ ] 3. Créer frontend/tests/browser/runner.html (importmap + import du fichier de test servi tel quel + POST /result corrélé par run_id)
- [ ] 4. Créer frontend/tests/browser/catalog-browser.mjs (serveur whitelist + lancement Chromium/Firefox headless + deadlines + cleanup prouvé + verdict JSON borné)
- [ ] 5. Modifier frontend/package.json : test= pilote deux navigateurs ; test:node = node --test diagnostics
- [ ] 6. Exécuter /home/devops/node/current/bin/npm --prefix frontend test : preuve 3/3 pass par navigateur, 2 réponses corrélées, cleanup
- [ ] 7. Exécuter /home/devops/node/current/bin/npm --prefix frontend run build : exit 0
- [ ] 8. Exécuter /home/devops/node/current/bin/npm --prefix frontend test:node : diagnostic inchangé
- [ ] 9. Mettre à jour frontend/README.md uniquement si un texte existant entre en incompatibilité avec test=2 moteurs / test:node=diagnostic
