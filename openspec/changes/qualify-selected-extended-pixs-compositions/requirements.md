# Références normatives — Q01

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| testing / 8 | [Trois niveaux de vérification distincts](../../specs/testing/spec.md#L8) | P | COMPLETER_OU_INTEGRER |
| testing / 17 | [Kit de conformité et composant d'exemple](../../specs/testing/spec.md#L17) | P | COMPLETER_OU_INTEGRER |
| testing / 30 | [Suites de conformité versionnées par contrat](../../specs/testing/spec.md#L30) | P | COMPLETER_OU_INTEGRER |
| testing / 39 | [Garanties obligatoires séparées des capacités optionnelles](../../specs/testing/spec.md#L39) | P | COMPLETER_OU_INTEGRER |
| testing / 48 | [Reproductibilité sur la topologie de référence](../../specs/testing/spec.md#L48) | P | COMPLETER_OU_INTEGRER |
| testing / 57 | [Preuves sans secret ni donnée de production](../../specs/testing/spec.md#L57) | P | COMPLETER_OU_INTEGRER |
| testing / 66 | [Conformité de la composition frontend récursive](../../specs/testing/spec.md#L66) | P | COMPLETER_OU_INTEGRER |
| testing / 75 | [Conformité des projections d'annuaire optionnelles](../../specs/testing/spec.md#L75) | P | COMPLETER_OU_INTEGRER |
| testing / 89 | [Exécution navigateur headless des unités frontend web](../../specs/testing/spec.md#L89) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence testing--3bc15eb3da

Source : `openspec/specs/testing/spec.md`, ligne 8. SHA-256 du bloc : `8bd293063511d9ff7c4e776d91f7b343192d9b7ad3654f1060f2ba0866743e16`.

~~~~text
### Requirement: Trois niveaux de vérification distincts

Le projet MUST distinguer les tests unitaires des comportements internes, les tests d'intégration des compositions et des dépendances réelles de référence, et les tests de conformité des contrats publiés ; le succès d'un niveau MUST NOT tenir lieu de preuve pour un autre.

#### Scenario: Unitaires verts, intégration rouge

- **WHEN** des tests unitaires réussissent alors qu'un test d'intégration de composition échoue
- **THEN** la release est considérée non valide et l'échec d'intégration est rapporté explicitement
~~~~

### Référence testing--b553810d1f

Source : `openspec/specs/testing/spec.md`, ligne 17. SHA-256 du bloc : `ff6ff6ed413bc587bd7f4420c4d84bc5d78f3ed21ebc0419cb4a65928eb5e7af`.

~~~~text
### Requirement: Kit de conformité et composant d'exemple

Le Developer Kit MUST fournir des validateurs et suites de conformité
versionnés pour les manifests, contrats et composants déclarés compatibles. Un
composant d'exemple P0 MUST démontrer la composition par contrats, le contexte
tenant/scope et l'autorisation ; il MUST NOT devenir une dépendance de
production.

#### Scenario: Exemple P0 validé

- **WHEN** le composant d'exemple est validé par le Developer Kit
- **THEN** les preuves indiquent les versions de contrats et les contrôles P0 exécutés
~~~~

### Référence testing--8240234124

Source : `openspec/specs/testing/spec.md`, ligne 30. SHA-256 du bloc : `1a25f001ea6e86cc778df2ec2938ccb06868648d5b1702000d191653c4c631c9`.

~~~~text
### Requirement: Suites de conformité versionnées par contrat

Chaque contrat de fournisseur MUST disposer d'une suite de conformité versionnée, indépendante de la technologie implémentée ; le runtime MUST NOT déclarer compatible un provider dont la conformité obligatoire est absente, expirée ou échouée.

#### Scenario: Certification expirée

- **WHEN** un provider présente une preuve de conformité expirée pour sa version déclarée
- **THEN** il est exclu de la sélection tant qu'une nouvelle exécution de la suite ne réussit pas
~~~~

### Référence testing--ec900517c4

Source : `openspec/specs/testing/spec.md`, ligne 39. SHA-256 du bloc : `0310541d7ae00ce5d4425cb1235794b54133d8de93060c47e76a5acc04cdfa38`.

~~~~text
### Requirement: Garanties obligatoires séparées des capacités optionnelles

Les tests MUST distinguer les garanties obligatoires des capacités optionnelles : une capacité optionnelle absente ou indisponible peut produire un état dégradé ou désactivé si elle reste isolée ; une incompatibilité de contrat, une ambiguïté de fournisseur, un défaut d'isolation de tenant ou une violation de sécurité MUST bloquer l'activation.

#### Scenario: Isolement acceptable

- **WHEN** une capacité optionnelle tombe sans fuite d'accès ni perte de donnée
- **THEN** l'état dégradé est accepté et diagnostiqué alors que le socle reste actif
~~~~

### Référence testing--ea8ece8809

Source : `openspec/specs/testing/spec.md`, ligne 48. SHA-256 du bloc : `3b2d50452802a83d20b35dec44cd60cd7109aa0c54aaca3bcb541088cadba393`.

~~~~text
### Requirement: Reproductibilité sur la topologie de référence

Les tests MUST être exécutables sur la topologie de référence du projet et sur toute topologie isolée déclarée compatible ; une différence de topologie MUST NOT modifier silencieusement les règles d'autorisation, de partage, de projection ou de suppression.

#### Scenario: Divergence de topologie

- **WHEN** un test d'invariant de périmètre produit un résultat différent selon la topologie
- **THEN** l'écart est bloquant et la topologie concernée perd sa mention de compatibilité
~~~~

### Référence testing--f0b3bab690

Source : `openspec/specs/testing/spec.md`, ligne 57. SHA-256 du bloc : `d9ae4d21e57d739e7b642389b1085eccff510000f3a51fdb8f674d17f68d439c`.

~~~~text
### Requirement: Preuves sans secret ni donnée de production

Les fixtures, exemples et rapports produits par les tests MUST être synthétiques et reproductibles, sans secret, sans token et sans donnée de production ; les rapports MUST NOT exposer de détail exploitable.

#### Scenario: Secret détecté dans un rapport

- **WHEN** un artefact de test contient une valeur sensible réelle ou apparentée
- **THEN** le rapport est invalidé, la fuite est signalée et l'exécution est bloquante pour la publication
~~~~

### Référence testing--2632c92c48

Source : `openspec/specs/testing/spec.md`, ligne 66. SHA-256 du bloc : `99bd959f22eec7645e810ce689df821fbd8fd6c00a706a82d3ec898d4fa2f54e`.

~~~~text
### Requirement: Conformité de la composition frontend récursive

Les suites de conformité MUST vérifier la résolution récursive des modules et sous-modules frontend, la propriété des contributions, les dépendances publiques, les contraintes SemVer, les collisions, les modes obligatoire et optionnel, ainsi que l'équivalence de composition entre développement et artefacts distribués. Une résolution frontend MUST NOT dépendre de l'ordre des imports, du filesystem ou d'un code distant runtime.

#### Scenario: Composition reproductible avec sous-module

- **WHEN** la même composition incluant un module et un sous-module frontend est construite deux fois
- **THEN** les contributions actives, l'ordre de chargement et les diagnostics produits sont identiques
~~~~

### Référence testing--19ab684105

Source : `openspec/specs/testing/spec.md`, ligne 75. SHA-256 du bloc : `4d1c7c58c3080d486f81efcd997cab6ade6c991c51d056d9ea8daa81ef6f6fa5`.

~~~~text
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
~~~~

### Référence testing--22ba62c0b8

Source : `openspec/specs/testing/spec.md`, ligne 89. SHA-256 du bloc : `121a020f91da796da68634e9f74a654ebc2160b8922ae90a777a642f3d3fe310`.

~~~~text
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
~~~~

