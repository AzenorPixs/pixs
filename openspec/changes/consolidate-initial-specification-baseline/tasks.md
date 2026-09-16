## 1. Cartographie de conservation

- [ ] 1.1 Produire une matrice complète reliant chaque exigence et scénario
  actif à son emplacement cible, ses dépendances et son statut de conservation.
- [ ] 1.2 Identifier les contradictions, lacunes et ambiguïtés sans les
  résoudre implicitement.
- [ ] 1.3 Faire valider par le développeur la matrice et le découpage en lots
  indépendants avant toute modification des spécifications actives.

## 2. Changes dépendants

- [ ] 2.1 Mettre à jour, dans un périmètre explicitement validé, le change de
  bootstrap afin de déclarer la composition P0 et son composant d'exemple.
- [ ] 2.2 Ajouter, dans ce même périmètre, les garanties de l'opérateur initial
  vérifié, de sa politique d'autorisation et des références `SecretProvider`.

## 3. Consolidation documentaire par lots

- [ ] 3.1 Créer un change dédié pour chaque lot de capacités dont la matrice
  démontre la conservation complète.
- [ ] 3.2 Valider chaque lot avec `openspec validate --all --strict` et une
  revue de la matrice avant le lot suivant.

## 4. Clôture

- [ ] 4.1 Vérifier que tous les identifiants de capacités, exigences et
  scénarios sont préservés ou explicitement arbitrés dans un change distinct.
- [ ] 4.2 Présenter la baseline consolidée, les validations et les écarts au
  développeur avant toute demande d'archivage.
