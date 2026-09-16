## 1. Socle planning

- [x] 1.1 Valider proposal+design CGPT (fait, reprise de session approuvée)
- [x] 1.2 Figer l'ordre lots A-G (§35) et vérifier openspec validate define-pixs-specifications (fait, change valide)

## 2. Lots specs A-G

- [x] 2.1 Lot A rédigé (kernel, component-model, contracts, extension-contracts, capabilities, feature-flags, dependencies, lifecycle) et validé
- [x] 2.2 Lot B rédigé, complété par providers, modules, migrations
- [x] 2.3 Lots C-D-E rédigés et validés
- [x] 2.4 Lot F rédigé, complété par audit, accessibility, design-system, compatibility, testing
- [x] 2.5 Lot G rédigé (performance, runtime, operations, backup-disaster-recovery, deb-package, docker-image, artifact-publication, release-management)
- [x] 2.6 openspec validate global : 56/56 deltas, change valide, seuls WARNING RFC 2119 systématiques (convention française)

## 3. Restant (bloqué tant que CGPT n'a pas tranché)

- [x] 3.1 Décision convention française DOIT vs avertissements RFC 2119 (option 1 approuvée, arbitrage mcp-8, tracée dans design.md décision 5)
- [x] 3.2 Relecture croisée des 56 deltas par lots (56/56, 200 exigences, 200 scénarios, 1 scénario par exigence, aucun SHALL/MUST anglais, structure Purpose/ADDED homogène)
- [x] 3.3 Sync/archive vers openspec/specs/ (exécution immédiate par `openspec archive define-pixs-specifications --yes` dans le présent périmètre approuvé)
