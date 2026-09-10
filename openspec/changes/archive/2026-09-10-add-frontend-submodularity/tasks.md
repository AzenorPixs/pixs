## 1. Modèle de manifest et de composition

- [ ] 1.1 Définir le schéma versionné de la facette `[frontend]` dans `component.toml`, y compris contributions, façades et contraintes du shell, puis vérifier le rejet des déclarations incomplètes.
- [ ] 1.2 Étendre le résolveur de composants pour parcourir les contributions frontend des modules et sous-modules, puis vérifier un ordre identique sur deux compositions équivalentes.
- [ ] 1.3 Mettre en place les contrôles de façades publiques, cycles, collisions et priorités déclarées, puis vérifier qu'un import privé ou une route ambiguë bloque la composition.

## 2. Shell et build de référence

- [ ] 2.1 Implémenter le registre frontend du shell et le lifecycle des contributions imbriquées, puis vérifier l'isolation d'un sous-module optionnel indisponible.
- [ ] 2.2 Produire la composition de routes, navigation, traductions et chunks au build depuis les manifests validés, puis vérifier l'absence de découverte par filesystem ou de code distant runtime.
- [ ] 2.3 Ajouter un module et un sous-module frontend de référence, puis vérifier leurs limites publiques, leur ScopeContext en lecture seule et l'usage exclusif des APIs publiques.

## 3. Conformité et distribution

- [ ] 3.1 Ajouter les suites de conformité de composition frontend récursive, puis vérifier dépendances SemVer, collisions, modes obligatoire et optionnel, accessibilité et internationalisation par composant propriétaire.
- [ ] 3.2 Vérifier la parité de composition entre développement, paquet Debian et image Docker, puis confirmer que les mêmes manifests produisent les mêmes contributions actives et diagnostics.
