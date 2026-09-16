## Purpose

Le testing organise les niveaux de vérification — unitaire, intégration et conformité des contrats — et produit des preuves reproductibles sans secret ni donnée de production.

## ADDED Requirements

### Requirement: Trois niveaux de vérification distincts

Le projet DOIT distinguer les tests unitaires des comportements internes, les tests d'intégration des compositions et des dépendances réelles de référence, et les tests de conformité des contrats publiés ; le succès d'un niveau NE DOIT PAS tenir lieu de preuve pour un autre.

#### Scenario: Unitaires verts, intégration rouge

- **WHEN** des tests unitaires réussissent alors qu'un test d'intégration de composition échoue
- **THEN** la release est considérée non valide et l'échec d'intégration est rapporté explicitement

### Requirement: Suites de conformité versionnées par contrat

Chaque contrat de fournisseur DOIT disposer d'une suite de conformité versionnée, indépendante de la technologie implémentée ; le runtime NE DOIT PAS déclarer compatible un provider dont la conformité obligatoire est absente, expirée ou échouée.

#### Scenario: Certification expirée

- **WHEN** un provider présente une preuve de conformité expirée pour sa version déclarée
- **THEN** il est exclu de la sélection tant qu'une nouvelle exécution de la suite ne réussit pas

### Requirement: Garanties obligatoires séparées des capacités optionnelles

Les tests DOIVENT distinguer les garanties obligatoires des capacités optionnelles : une capacité optionnelle absente ou indisponible peut produire un état dégradé ou désactivé si elle reste isolée ; une incompatibilité de contrat, une ambiguïté de fournisseur, un défaut d'isolation de tenant ou une violation de sécurité DOIT bloquer l'activation.

#### Scenario: Isolement acceptable

- **WHEN** une capacité optionnelle tombe sans fuite d'accès ni perte de donnée
- **THEN** l'état dégradé est accepté et diagnostiqué alors que le socle reste actif

### Requirement: Reproductibilité sur la topologie de référence

Les tests DOIVENT être exécutables sur la topologie de référence du projet et sur toute topologie isolée déclarée compatible ; une différence de topologie NE DOIT PAS modifier silencieusement les règles d'autorisation, de partage, de projection ou de suppression.

#### Scenario: Divergence de topologie

- **WHEN** un test d'invariant de périmètre produit un résultat différent selon la topologie
- **THEN** l'écart est bloquant et la topologie concernée perd sa mention de compatibilité

### Requirement: Preuves sans secret ni donnée de production

Les fixtures, exemples et rapports produits par les tests DOIVENT être synthétiques et reproductibles, sans secret, sans token et sans donnée de production ; les rapports ne DOIVENT PAS exposer de détail exploitable.

#### Scenario: Secret détecté dans un rapport

- **WHEN** un artefact de test contient une valeur sensible réelle ou apparentée
- **THEN** le rapport est invalidé, la fuite est signalée et l'exécution est bloquante pour la publication
