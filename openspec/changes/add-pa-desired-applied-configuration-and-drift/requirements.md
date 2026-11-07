# Références normatives — PA05

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| pixs-agent | Plans sensibles et compensation préautorisée | 1 | pixs-agent-4ad8f35c03d3 |
| pixs-agent | Configuration souhaitée et appliquée distinctes | 1 | pixs-agent-a6f952049268 |
| pixs-agent | Observation des dérives et corrections distinctes | 1 | pixs-agent-92ae8b557da9 |
| managed-device-policies | Cibles V1 et exécutants locaux | 1 | managed-device-policies-8a43d725b9c8 |
| managed-device-policies | Gestion ZT et jonction d’authentification distinctes | 1 | managed-device-policies-f3d868c20f8b |
| managed-device-policies | Politiques communes et spécifiques | 1 | managed-device-policies-0fc04bee903f |
| managed-device-policies | Priorités et contradictions | 1 | managed-device-policies-a7f801c0bbd9 |
| managed-device-policies | Application par PA et état vérifié | 1 | managed-device-policies-fc87e0db8071 |
| managed-device-policies | Session hors ligne bornée | 1 | managed-device-policies-53ac3cf3063d |
| managed-device-policies | Rotation des secrets machine et services | 1 | managed-device-policies-0e3d3ee17150 |
| managed-device-policies | Redémarrage par profil et conclusion après reprise | 1 | managed-device-policies-0a228d3c9bf5 |

### Référence courante pixs-agent-4ad8f35c03d3

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 184. SHA-256 : `4ad8f35c03d379f498c31ee1258ee9d1b218e3913266d4cb8670d6b807881e5f`.

Scénarios : Plans sensibles et compensation préautorisée.

~~~~text
### Requirement: Plans sensibles et compensation préautorisée

Une reconfiguration sensible MUST utiliser un plan versionné, borné, autorisé et encore courant, avec confirmation ou assurance renforcée lorsque requise. Une compensation après perte de contrôle MUST rester dans le plan préautorisé, sans restaurer une permission révoquée ni ouvrir un canal hors PZT. Un plan obsolète ou hors mandat MUST NOT être appliqué.

#### Scenario: Plans sensibles et compensation préautorisée

- **WHEN** une modification coupe le canal de contrôle
- **THEN** l'état est diagnostiqué et seule une compensation encore autorisée peut être tentée
~~~~

### Référence courante pixs-agent-a6f952049268

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 193. SHA-256 : `a6f952049268fabbdab923584a6898efcd3844c0f95c3e36fe59eac06de435fb`.

Scénarios : Configuration souhaitée et appliquée distinctes.

~~~~text
### Requirement: Configuration souhaitée et appliquée distinctes

PBO MUST conserver la configuration souhaitée et PA MUST rapporter version, résultat et état réellement appliqués. Validation de schéma, compatibilité, préconditions et concurrence MUST précéder l'application ; application partielle et conflit MUST être déclarés. Envoyé ou reçu MUST NOT être présenté comme appliqué ; un feature flag MUST NOT supprimer une capacité requise ni élargir un droit.

#### Scenario: Configuration souhaitée et appliquée distinctes

- **WHEN** PA a reçu une configuration mais son application échoue
- **THEN** PBO conserve la distinction souhaité/appliqué et affiche l'échec
~~~~

### Référence courante pixs-agent-92ae8b557da9

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 220. SHA-256 : `92ae8b557da9cee29a4d5bd42c67fb7559ad7e67ec3620f81f3f4e64b8eb682e`.

Scénarios : Observation des dérives et corrections distinctes.

~~~~text
### Requirement: Observation des dérives et corrections distinctes

PA MUST distinguer constat de dérive et correction. La surveillance MUST produire des états et diagnostics autorisés ; une correction MUST disposer de sa politique et de son mandat propres. Référentiels, fréquences, budgets et catalogue de corrections MUST être spécifiés et qualifiés avant activation, sans valeurs implicites.

#### Scenario: Observation des dérives et corrections distinctes

- **WHEN** une dérive est détectée sans mandat de correction
- **THEN** le constat est rapporté sans engager de modification non autorisée
~~~~

### Référence courante managed-device-policies-8a43d725b9c8

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 11. SHA-256 : `8a43d725b9c8f9f725eb22c048e5e91d1ee208d3af98a44e61ea75cfae643633`.

Scénarios : Poste administré.

~~~~text
### Requirement: Cibles V1 et exécutants locaux

Les profils V1 MUST couvrir postes Linux/Windows et serveurs Linux membres, avec Debian stable et Windows 10/11 admissibles à qualifier. Les postes administrés et serveurs Linux soumis aux politiques MUST disposer de PA/PZT locaux. Les rôles serveur de domaine MUST NOT être imposés sur chaque poste.

#### Scenario: Poste administré

- **WHEN** un poste reçoit une politique Pixs
- **THEN** les exécutants locaux sont vérifiés sans le transformer en LZT ou KZT.
~~~~

### Référence courante managed-device-policies-f3d868c20f8b

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 20. SHA-256 : `f3d868c20f8b51c27e721a1df72180c8508e9cfdf1ff06948b8294b817119a29`.

Scénarios : Hôte tiers géré.

~~~~text
### Requirement: Gestion ZT et jonction d’authentification distinctes

Un hôte MAY être intégré à ZT et administré sans jonction de domaine pour l'authentification de ses utilisateurs. Cette jonction MUST rester facultative mais exiger l'intégration ZT préalable lorsqu'elle est demandée. Le passage du PA en mode Domaine MUST NOT joindre automatiquement l'hôte au domaine d'authentification.

#### Scenario: Hôte tiers géré

- **WHEN** un hôte rejoint ZT sans jonction d’authentification
- **THEN** PA peut gérer ses capacités autorisées tandis que les utilisateurs conservent l’authentification configurée sur l’hôte.
~~~~

### Référence courante managed-device-policies-0fc04bee903f

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 29. SHA-256 : `0fc04bee903fa7c526db55656c40db141fc78bd93e1a2f658507d54be92da507`.

Scénarios : Règle propre à Windows.

~~~~text
### Requirement: Politiques communes et spécifiques

Les politiques MUST permettre des intentions communes Windows/Linux et des règles propres aux plateformes, avec politiques de poste et d'utilisateur et ciblage explicite. Les capacités non qualifiées MUST être déclarées non applicables ou indisponibles, sans simulation de succès.

#### Scenario: Règle propre à Windows

- **WHEN** une politique commune comporte une règle GPO Windows
- **THEN** l’application Linux ne prétend pas avoir appliqué cette règle native.
~~~~

### Référence courante managed-device-policies-a7f801c0bbd9

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 38. SHA-256 : `a7f801c0bbd9d9343d1e85e137ebc5eb30e56d499daabeba1006d7fe6d26ebbe`.

Scénarios : Deux valeurs au même niveau.

~~~~text
### Requirement: Priorités et contradictions

Les politiques de configuration MUST avoir des priorités explicites ; les contradictions à priorité égale MUST être signalées sans règle implicite du dernier reçu. La résolution MUST respecter les contrats de propriété et autorisations de chaque périmètre.

#### Scenario: Deux valeurs au même niveau

- **WHEN** deux politiques de même priorité imposent des valeurs incompatibles
- **THEN** l’écart est signalé et aucune valeur n’est choisie par ordre d’arrivée.
~~~~

### Référence courante managed-device-policies-fc87e0db8071

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 47. SHA-256 : `fc87e0db80717cda5b2c979b05d5045ee0bf334a5dd2cf6559bb9d13857e9c0e`.

Scénarios : Configuration reçue sans effet.

~~~~text
### Requirement: Application par PA et état vérifié

PA MUST appliquer les opérations livrées et autorisées dans le contexte système ou utilisateur approprié via pixs.agent. Réception, application, dérive et résultat confirmé MUST rester distincts. Les corrections automatiques MUST posséder leur propre politique et mandat.

#### Scenario: Configuration reçue sans effet

- **WHEN** PA reçoit une politique mais échoue à la mettre en place
- **THEN** PBO affiche l’échec sans état appliqué fictif.
~~~~

### Référence courante managed-device-policies-53ac3cf3063d

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 56. SHA-256 : `53ac3cf3063d580b57f56441ca276f52645441d643d76c41f8e4077b7e5882e7`.

Scénarios : Pas de profil hors ligne.

~~~~text
### Requirement: Session hors ligne bornée

L'ouverture de session hors ligne MAY être permise par profil explicite et borné. Elle MUST conserver les exigences de validité, protection locale et retraits connus ; une panne MUST NOT activer ce profil ni repousser ses échéances.

#### Scenario: Pas de profil hors ligne

- **WHEN** le contrôleur est indisponible sans profil hors ligne autorisé
- **THEN** aucune nouvelle permission de connexion locale n’est déduite de la panne.
~~~~

### Référence courante managed-device-policies-0e3d3ee17150

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 65. SHA-256 : `0e3d3ee171504e6660c5650982a199dc41378de37affda7cbe83cb40f3506336`.

Scénarios : Rotation native autorisée.

~~~~text
### Requirement: Rotation des secrets machine et services

La rotation des secrets machine MUST être sélectionnable par profil entre pilotage Pixs/PBO/PA et rotation native qualifiée. Les services techniques MUST pouvoir utiliser un moyen propre ou une représentation habilitée selon profil. Ces secrets MUST rester distincts du mot de passe des individus changé depuis PBO.

#### Scenario: Rotation native autorisée

- **WHEN** un poste utilise la rotation machine native qualifiée
- **THEN** elle suit son profil et sa cohérence contrôleurs sans autoriser un changement natif du mot de passe individuel.
~~~~

### Référence courante managed-device-policies-0a228d3c9bf5

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 74. SHA-256 : `0a228d3c9bf5969235d9a1b17bf8161742513eb0cd8bfd88e93f3901641b2177`.

Scénarios : Jonction exigeant redémarrage.

~~~~text
### Requirement: Redémarrage par profil et conclusion après reprise

Le profil MUST choisir redémarrage manuel ou automatique sous fenêtre autorisée, avec manuel par défaut. PBO MUST distinguer redémarrage requis et opération terminée ; les vérifications après redémarrage MUST précéder la conclusion de jonction ou de politique.

#### Scenario: Jonction exigeant redémarrage

- **WHEN** la configuration est appliquée mais le poste n’a pas redémarré
- **THEN** l’opération reste à terminer jusqu’aux contrôles après reprise.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

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

