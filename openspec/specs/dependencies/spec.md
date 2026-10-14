# dependencies Specification

## Purpose
Les dépendances explicites garantissent une composition cohérente, ordonnée et sans cycle avant toute activation.

## Requirements

### Requirement: Dépendances déclarées typées

Chaque composant MUST déclarer dépendances composants et capacités, obligatoires et optionnelles distinguées, avec contraintes SemVer.

#### Scenario: Optionnelle absente tolérée

- **WHEN** une dépendance optionnelle est absente
- **THEN** la composition reste valide avec un comportement dégradé déclaré

### Requirement: Cycles et incompatibilités refusés

Le système MUST respecter les garanties suivantes.

Toute dépendance obligatoire absente, incompatible ou cyclique invalide la composition avant activation.

#### Scenario: Cycle détecté

- **WHEN** A dépend de B qui dépend de A
- **THEN** la composition est refusée avec le cycle diagnostiqué

### Requirement: Ordre de chargement déterministe

L'ordre résolu MUST être identique à composants, versions et configuration identiques, sans dépendre du système de fichiers ni des imports.

#### Scenario: Double composition identique

- **WHEN** la même composition est résolue deux fois
- **THEN** l'ordre de chargement est identique

### Requirement: Graphe frontend récursif et façades publiques

Le résolveur MUST intégrer les contributions frontend des modules et sous-modules dans le graphe de composants commun, vérifier leurs contraintes SemVer, leurs dépendances obligatoires et optionnelles, et n'autoriser que les façades frontend publiques déclarées par le shell, le Design System ou un composant. Les chemins physiques, l'ordre des imports et l'arborescence parent-enfant MUST NOT créer de dépendance ou de priorité implicite.

#### Scenario: Import privé d'un parent refusé

- **WHEN** un sous-module frontend dépend d'un store ou d'une implémentation privée de son parent sans façade publique déclarée
- **THEN** la composition est refusée avant exposition avec un diagnostic du contrat manquant

### Requirement: Grammaire des contraintes de version

Chaque entrée de dépendance (`components`, `capabilities`, `contracts`, y
compris les composants requis portés en données de composition) MUST utiliser
la forme `"id [comparateurs]"` où `comparateurs` est une conjonction séparée
par espaces de comparaisons `comparateur version`, le comparateur appartenant
à `==`, `!=`, `>=`, `<=`, `>`, `<` accolé à une version SemVer 2.0.0 complète
(exemple : `"audit >=1.0.0 <2.0.0"`).

#### Scenario: Conjonction de comparateurs explicites

- **WHEN** un consommateur déclare audit >=1.0.0 <2.0.0
- **THEN** la contrainte suit la grammaire de conjonction de comparateurs sur versions SemVer complètes

### Requirement: Sémantique et refus des contraintes de version

Un identifiant seul signifie l'absence de
restriction de version, jamais l'absence de vérification de conformité. Les préversions suivent l'ordre SemVer 2.0.0 standard ; les métadonnées de
build sont ignorées pour la précédence et les comparateurs. Toute syntaxe
inconnue ou malformée (opérateur logique OR, joker, caret, tilde, plage
ouverte implicite) MUST être refusée avec un diagnostic, jamais ignorée.

#### Scenario: Contrainte malformée refusée

- **WHEN** un consommateur déclare `audit ^1.0.0`
- **THEN** la validation refuse avec un diagnostic référençant l'expression et le consommateur, sans ignorer la contrainte

### Requirement: Évaluation sur versions propres

Les contraintes de composants MUST être évaluées contre la version du
composant cible, celles de capacités contre la `capability_version` fournie,
celles de contrats contre la `contract_version` implémentée ; la version du
composant MUST NOT servir de proxy pour une capacité ou un contrat. Tout
refus MUST nommer le consommateur, la cible, la contrainte violée et la
version trouvée.

#### Scenario: Contrainte de capacité insatisfaite

- **WHEN** un consommateur exige `audit >=1.0.0 <2.0.0` et le seul fournisseur déclare la capacité en version `2.1.0`
- **THEN** la composition est refusée avec un diagnostic nommant le consommateur, la capacité, la contrainte et la version trouvée

### Requirement: Incompatibilités obligatoires et optionnelles

Le système MUST respecter les garanties suivantes.

Une dépendance optionnelle incompatible reste isolée avec un
comportement dégradé déclaré et diagnostiqué ; une dépendance obligatoire
incompatible invalide la composition avant activation.

#### Scenario: Optionnelle incompatible isolée

- **WHEN** une dépendance optionnelle est incompatible
- **THEN** elle reste isolée avec un comportement dégradé déclaré et diagnostiqué, alors qu'une incompatibilité obligatoire invalide la composition
