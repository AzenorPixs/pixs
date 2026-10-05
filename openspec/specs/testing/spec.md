# testing Specification

## Purpose
Le testing organise les niveaux de vérification — unitaire, intégration et conformité des contrats — et produit des preuves reproductibles sans secret ni donnée de production.

## Requirements

### Requirement: Trois niveaux de vérification distincts

Le projet MUST distinguer les tests unitaires des comportements internes, les tests d'intégration des compositions et des dépendances réelles de référence, et les tests de conformité des contrats publiés ; le succès d'un niveau MUST NOT tenir lieu de preuve pour un autre.

#### Scenario: Unitaires verts, intégration rouge

- **WHEN** des tests unitaires réussissent alors qu'un test d'intégration de composition échoue
- **THEN** la release est considérée non valide et l'échec d'intégration est rapporté explicitement

### Requirement: Kit de conformité et composant d'exemple

Le Developer Kit MUST fournir des validateurs et suites de conformité
versionnés pour les manifests, contrats et composants déclarés compatibles. Un
composant d'exemple P0 MUST démontrer la composition par contrats, le contexte
tenant/scope et l'autorisation ; il MUST NOT devenir une dépendance de
production.

#### Scenario: Exemple P0 validé

- **WHEN** le composant d'exemple est validé par le Developer Kit
- **THEN** les preuves indiquent les versions de contrats et les contrôles P0 exécutés

### Requirement: Suites de conformité versionnées par contrat

Chaque contrat de fournisseur MUST disposer d'une suite de conformité versionnée, indépendante de la technologie implémentée ; le runtime MUST NOT déclarer compatible un provider dont la conformité obligatoire est absente, expirée ou échouée.

#### Scenario: Certification expirée

- **WHEN** un provider présente une preuve de conformité expirée pour sa version déclarée
- **THEN** il est exclu de la sélection tant qu'une nouvelle exécution de la suite ne réussit pas

### Requirement: Garanties obligatoires séparées des capacités optionnelles

Les tests MUST distinguer les garanties obligatoires des capacités optionnelles : une capacité optionnelle absente ou indisponible peut produire un état dégradé ou désactivé si elle reste isolée ; une incompatibilité de contrat, une ambiguïté de fournisseur, un défaut d'isolation de tenant ou une violation de sécurité MUST bloquer l'activation.

#### Scenario: Isolement acceptable

- **WHEN** une capacité optionnelle tombe sans fuite d'accès ni perte de donnée
- **THEN** l'état dégradé est accepté et diagnostiqué alors que le socle reste actif

### Requirement: Reproductibilité sur la topologie de référence

Les tests MUST être exécutables sur la topologie de référence du projet et sur toute topologie isolée déclarée compatible ; une différence de topologie MUST NOT modifier silencieusement les règles d'autorisation, de partage, de projection ou de suppression.

#### Scenario: Divergence de topologie

- **WHEN** un test d'invariant de périmètre produit un résultat différent selon la topologie
- **THEN** l'écart est bloquant et la topologie concernée perd sa mention de compatibilité

### Requirement: Preuves sans secret ni donnée de production

Les fixtures, exemples et rapports produits par les tests MUST être synthétiques et reproductibles, sans secret, sans token et sans donnée de production ; les rapports MUST NOT exposer de détail exploitable.

#### Scenario: Secret détecté dans un rapport

- **WHEN** un artefact de test contient une valeur sensible réelle ou apparentée
- **THEN** le rapport est invalidé, la fuite est signalée et l'exécution est bloquante pour la publication

### Requirement: Conformité de la composition frontend récursive

Les suites de conformité MUST vérifier la résolution récursive des modules et sous-modules frontend, la propriété des contributions, les dépendances publiques, les contraintes SemVer, les collisions, les modes obligatoire et optionnel, ainsi que l'équivalence de composition entre développement et artefacts distribués. Une résolution frontend MUST NOT dépendre de l'ordre des imports, du filesystem ou d'un code distant runtime.

#### Scenario: Composition reproductible avec sous-module

- **WHEN** la même composition incluant un module et un sous-module frontend est construite deux fois
- **THEN** les contributions actives, l'ordre de chargement et les diagnostics produits sont identiques

### Requirement: Conformité des projections d'annuaire optionnelles

Les suites de conformité MUST vérifier le mapping versionné, la projection
sortante idempotente, la reprise, les suppressions propagées, l'isolation de
tenant et de scope, la fraîcheur après mutation, le repli PostgreSQL et l'état
DEGRADED d'un provider LDAP indisponible. Elles MUST vérifier que LDAP ne peut
ni écrire dans Pixs, ni fournir une ACL, une décision d'autorisation, une
révocation ou une authentification par cette capacité.

#### Scenario: Repli conforme sans élargissement de droits

- **WHEN** LDAP devient indisponible pendant une consultation autorisée
- **THEN** la suite confirme la réponse PostgreSQL, l'état DEGRADED et l'absence de divulgation ou de droit supplémentaire

### Requirement: Exécution navigateur headless des unités frontend web

Les tests unitaires de la partie frontend web MUST être exécutés dans tous les
navigateurs déclarés par DEVOPS.md, en mode headless ; le succès de ces tests
uniquement sous Node MUST NOT tenir lieu de preuve de cette exigence.

#### Scenario: Les deux moteurs déclarent les cas

- **WHEN** `npm --prefix frontend test` s'exécute sur un environnement
  déclarant Chromium et Firefox headless
- **THEN** chaque cas unitaire frontend reçoit une preuve d'exécution issue de
  chaque navigateur déclaré et le résultat global n'est vert qu'avec les deux
  moteurs

#### Scenario: Moteur manquant ou cas non exécuté

- **WHEN** un navigateur déclaré est indisponible, ne répond pas dans les
  bornes, ou n'exécute pas l'intégralité des cas
- **THEN** l'exécution est en échec diagnostiqué, sans substitution par le
  seul résultat Node ou par la réussite du build
