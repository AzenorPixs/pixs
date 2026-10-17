# Références normatives — PA05

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 119 | [Plans sensibles et compensation préautorisée](../../specs/pixs-agent/spec.md#L119) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 128 | [Configuration souhaitée et appliquée distinctes](../../specs/pixs-agent/spec.md#L128) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 155 | [Observation des dérives et corrections distinctes](../../specs/pixs-agent/spec.md#L155) | ND | CANDIDAT_PROFIL_PA |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--df000cdcc2

Source : `openspec/specs/pixs-agent/spec.md`, ligne 119. SHA-256 du bloc : `e143fe2bc291943350997951ca533d1ccbe2ac1c370072914daaf5f915b3c4fc`.

~~~~text
### Requirement: Plans sensibles et compensation préautorisée

Une reconfiguration sensible MUST utiliser un plan versionné, borné, autorisé et encore courant, avec confirmation ou assurance renforcée lorsque requise. Une compensation après perte de contrôle MUST rester dans le plan préautorisé, sans restaurer une permission révoquée ni ouvrir un canal hors PZT. Un plan obsolète ou hors mandat MUST NOT être appliqué.

#### Scenario: Plans sensibles et compensation préautorisée

- **WHEN** une modification coupe le canal de contrôle
- **THEN** l'état est diagnostiqué et seule une compensation encore autorisée peut être tentée
~~~~

### Référence pixs-agent--77bc3db6bd

Source : `openspec/specs/pixs-agent/spec.md`, ligne 128. SHA-256 du bloc : `e331aa1c24d59e68ef7a120688266ac4382e1160626feb8e6d6385c11b9aea9e`.

~~~~text
### Requirement: Configuration souhaitée et appliquée distinctes

PBO MUST conserver la configuration souhaitée et PA MUST rapporter version, résultat et état réellement appliqués. Validation de schéma, compatibilité, préconditions et concurrence MUST précéder l'application ; application partielle et conflit MUST être déclarés. Envoyé ou reçu MUST NOT être présenté comme appliqué ; un feature flag MUST NOT supprimer une capacité requise ni élargir un droit.

#### Scenario: Configuration souhaitée et appliquée distinctes

- **WHEN** PA a reçu une configuration mais son application échoue
- **THEN** PBO conserve la distinction souhaité/appliqué et affiche l'échec
~~~~

### Référence pixs-agent--8a01f515dd

Source : `openspec/specs/pixs-agent/spec.md`, ligne 155. SHA-256 du bloc : `3b36f611c76fb438dc32bc6831516c8541d383aa5adf1be499101caa28a172c1`.

~~~~text
### Requirement: Observation des dérives et corrections distinctes

PA MUST distinguer constat de dérive et correction. La surveillance MUST produire des états et diagnostics autorisés ; une correction MUST disposer de sa politique et de son mandat propres. Référentiels, fréquences, budgets et catalogue de corrections MUST être spécifiés et qualifiés avant activation, sans valeurs implicites.

#### Scenario: Observation des dérives et corrections distinctes

- **WHEN** une dérive est détectée sans mandat de correction
- **THEN** le constat est rapporté sans engager de modification non autorisée
~~~~

