## 1. Cartographie de conservation

- [x] 1.1 Produire une matrice complète reliant chaque exigence et scénario
  actif à son emplacement cible, ses dépendances et son statut de conservation.
- [x] 1.2 Identifier les contradictions, lacunes et ambiguïtés sans les
  résoudre implicitement.
- [x] 1.3 Faire valider par le développeur la matrice et le découpage en lots
  indépendants avant toute modification des spécifications actives.

## 2. Conclusion documentaire

- [x] 2.1 Constater que la matrice ne requiert aucun delta OpenSpec pour
  conserver les exigences et scénarios actifs.
- [x] 2.2 Vérifier que les relations de bootstrap, d'opérateur initial et de
  `SecretProvider` restent portées par
  `specify-initial-application-bootstrap` et ne sont pas dupliquées ni
  modifiées fonctionnellement.

## 3. Validation documentaire

- [x] 3.1 Valider le change avec `openspec validate --all --strict` et une
  revue de la matrice.
- [x] 3.2 Vérifier que les capacités actives ne nécessitent aucune
  synchronisation supplémentaire.

## 4. Clôture

- [x] 4.1 Vérifier que tous les identifiants de capacités, exigences et
  scénarios sont préservés ou explicitement arbitrés dans un change distinct.
- [x] 4.2 Présenter la baseline consolidée, les validations et les écarts au
  développeur avant toute demande d'archivage.
