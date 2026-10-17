# Références normatives — PA04

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 47 | [Composition au build et catalogue fermé](../../specs/pixs-agent/spec.md#L47) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 92 | [Contrat public des instructions et revalidation](../../specs/pixs-agent/spec.md#L92) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 110 | [Exécution locale et états indéterminés](../../specs/pixs-agent/spec.md#L110) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 119 | [Plans sensibles et compensation préautorisée](../../specs/pixs-agent/spec.md#L119) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 182 | [Audit, confidentialité et exception Super Admin](../../specs/pixs-agent/spec.md#L182) | ND | CANDIDAT_PROFIL_PA |
| pzt / 30 | [Passage obligatoire PBO–PA par PZT](../../specs/pzt/spec.md#L30) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--bd3940f601

Source : `openspec/specs/pixs-agent/spec.md`, ligne 47. SHA-256 du bloc : `2cde976931df9e6c3f72460dd263b37705129586eb38a9efc3be6b7269446983`.

~~~~text
### Requirement: Composition au build et catalogue fermé

Chaque capacité PA MUST déclarer identité, version, propriétaire, contrats, dépendances, configuration, sécurité et permissions selon le modèle de composants. La composition initiale MUST se faire au build ; instructions et mandats MUST sélectionner seulement des opérations déjà livrées. PA MUST NOT télécharger ou charger implicitement du code, évaluer du Python ou ouvrir un shell privilégié à partir d'une instruction réseau.

#### Scenario: Composition au build et catalogue fermé

- **WHEN** une instruction demande une opération absente du catalogue livré
- **THEN** elle est refusée sans téléchargement ou exécution de code arbitraire
~~~~

### Référence pixs-agent--ab52dc7fd0

Source : `openspec/specs/pixs-agent/spec.md`, ligne 92. SHA-256 du bloc : `bac905dfacb676eca03b3a498b0c86145e43d6273305d3a1cbf6af100037b74e`.

~~~~text
### Requirement: Contrat public des instructions et revalidation

Une instruction MUST identifier émetteur, acteur initial, exécuteur, opération/version, cible, plateforme, tenant/scope, paramètres typés/bornés, mandat, validité, fraîcheur, corrélation et idempotence lorsqu'applicables. PA MUST vérifier ces éléments à l'exécution, y compris après attente ou reprise. Une permission de lecture/surveillance MUST NOT accorder une reconfiguration ; un canal authentifié MUST NOT accorder un droit métier.

#### Scenario: Contrat public des instructions et revalidation

- **WHEN** une instruction admise expire avant son exécution
- **THEN** elle n'est pas exécutée sur la seule base de son admission passée
~~~~

### Référence pixs-agent--13250f4b84

Source : `openspec/specs/pixs-agent/spec.md`, ligne 110. SHA-256 du bloc : `ba23e50b4d683e00934ba0b17353a922954d7198013e34a9c52a41d803a5d47b`.

~~~~text
### Requirement: Exécution locale et états indéterminés

Chaque opération MUST déclarer préconditions, postconditions, effets, codes stables, caractère rejouable et stratégie d'erreur. Après crash entre effet et persistance du résultat, PA MUST vérifier la postcondition ou demander une intervention autorisée avant réexécution. Simulation, préparation, exécution et confirmation MUST rester distinctes ; une simulation MUST NOT produire de mutation.

#### Scenario: Exécution locale et états indéterminés

- **WHEN** un crash survient après un effet système avant son enregistrement
- **THEN** la reprise distingue l'effet inconnu et évite une réexécution aveugle
~~~~

### Référence pixs-agent--df000cdcc2

Source : `openspec/specs/pixs-agent/spec.md`, ligne 119. SHA-256 du bloc : `e143fe2bc291943350997951ca533d1ccbe2ac1c370072914daaf5f915b3c4fc`.

~~~~text
### Requirement: Plans sensibles et compensation préautorisée

Une reconfiguration sensible MUST utiliser un plan versionné, borné, autorisé et encore courant, avec confirmation ou assurance renforcée lorsque requise. Une compensation après perte de contrôle MUST rester dans le plan préautorisé, sans restaurer une permission révoquée ni ouvrir un canal hors PZT. Un plan obsolète ou hors mandat MUST NOT être appliqué.

#### Scenario: Plans sensibles et compensation préautorisée

- **WHEN** une modification coupe le canal de contrôle
- **THEN** l'état est diagnostiqué et seule une compensation encore autorisée peut être tentée
~~~~

### Référence pixs-agent--8680fa3b61

Source : `openspec/specs/pixs-agent/spec.md`, ligne 182. SHA-256 du bloc : `b9d9011f0a6a37e20b1d9e49627c3c8289fd325c3b015054f91e78ccf530f22a`.

~~~~text
### Requirement: Audit, confidentialité et exception Super Admin

PA et PBO MUST appliquer les obligations ordinaires de security, authorization et audit sous réserve de l'exception unique définie par initial-administration. Une requête Super Admin MUST conserver acteur initial et tenant explicitement accordé, sans credentials ou exception transférés à un worker/autre compte. Audit ou contrôle dérogé/non réalisé MUST NOT être présenté comme effectué ; profils structurels et contrats d'exécution MUST rester distincts.

#### Scenario: Audit, confidentialité et exception Super Admin

- **WHEN** le Super Admin utilise une dérogation d'audit dans son tenant accordé
- **THEN** l'audit absent n'est pas revendiqué comme réalisé et aucun autre compte n'hérite de la dérogation
~~~~

### Référence pzt--b09abd6f60

Source : `openspec/specs/pzt/spec.md`, ligne 30. SHA-256 du bloc : `efd3979f85e17ba446c232d0fd897c0c83be33aca423a3668342e3a8a822481d`.

~~~~text
### Requirement: Passage obligatoire PBO–PA par PZT

Tous les échanges PBO–PA, instructions, configuration, administration, états, diagnostics, événements et résultats MUST passer par PZT dans les deux sens, même sur le même hôte ou conteneur. Le transport local mTLS MUST conserver identification, autorisation, chiffrement, validité, anti-rejeu et traçabilité ; WireGuard local n'est pas obligatoire. Un profil local indisponible MUST NOT déclencher un canal Unix, loopback ou fichier de substitution hors PZT.

#### Scenario: Passage obligatoire PBO–PA par PZT

- **WHEN** le transport local PZT n'est pas vérifiable
- **THEN** le contrôle PBO–PA concerné est bloqué sans repli de proximité
~~~~

