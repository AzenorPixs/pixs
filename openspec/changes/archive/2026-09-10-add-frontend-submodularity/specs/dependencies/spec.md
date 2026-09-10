## ADDED Requirements

### Requirement: Graphe frontend récursif et façades publiques

Le résolveur MUST intégrer les contributions frontend des modules et sous-modules dans le graphe de composants commun, vérifier leurs contraintes SemVer, leurs dépendances obligatoires et optionnelles, et n'autoriser que les façades frontend publiques déclarées par le shell, le Design System ou un composant. Les chemins physiques, l'ordre des imports et l'arborescence parent-enfant MUST NOT créer de dépendance ou de priorité implicite.

#### Scenario: Import privé d'un parent refusé

- **WHEN** un sous-module frontend dépend d'un store ou d'une implémentation privée de son parent sans façade publique déclarée
- **THEN** la composition est refusée avant exposition avec un diagnostic du contrat manquant
