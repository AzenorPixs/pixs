# Références normatives — PA06

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 74 | [Arrêt contrôlé et résultats réellement observés](../../specs/pixs-agent/spec.md#L74) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 110 | [Exécution locale et états indéterminés](../../specs/pixs-agent/spec.md#L110) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 137 | [Persistance technique locale bornée](../../specs/pixs-agent/spec.md#L137) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 146 | [Continuité sans PBO et reprise locale PZT](../../specs/pixs-agent/spec.md#L146) | ND | CANDIDAT_PROFIL_PA |
| runtime / 70 | [États techniques PA distincts du runtime PBO](../../specs/runtime/spec.md#L70) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--ecb0f8d963

Source : `openspec/specs/pixs-agent/spec.md`, ligne 74. SHA-256 du bloc : `aed31e04d823e8fbc0d9c3e5cbd3ba326db9fc422077de59ced3026065096002`.

~~~~text
### Requirement: Arrêt contrôlé et résultats réellement observés

Les traitements system-stop et session-stop MUST avoir un budget maximal, un ordre déclaré avec les démons et dépendances, et une protection contre les doublons. PZT MUST être conservé tant que des échanges nécessaires et autorisés restent possibles dans le budget d'arrêt. Panne électrique, arrêt forcé et perte du processus MUST NOT être présentés comme une fermeture exécutée ou un résultat livré.

#### Scenario: Arrêt contrôlé et résultats réellement observés

- **WHEN** le conteneur disparaît avant confirmation du traitement d'arrêt
- **THEN** le résultat reste incomplet ou inconnu et aucun succès n'est inventé
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

### Référence pixs-agent--de6f014038

Source : `openspec/specs/pixs-agent/spec.md`, ligne 137. SHA-256 du bloc : `a2a8cd5382218bdaa810f9d7a390cb550133f43108228b82823d06832e8aa078`.

~~~~text
### Requirement: Persistance technique locale bornée

Les seuls états techniques locaux nécessaires à l'exécution, déduplication, résultats en attente et reprise MUST avoir un propriétaire, un contrat de durabilité, des limites, une rétention, une protection et une stratégie de corruption/restauration déclarés. Ils MUST NOT devenir une source de vérité métier. Un stockage requis plein ou corrompu MUST bloquer les opérations sans preuve durable ; en conteneur il MUST NOT dépendre du filesystem éphémère.

#### Scenario: Persistance technique locale bornée

- **WHEN** l'état durable de reprise est corrompu
- **THEN** les traitements dépendants restent bloqués sans état remis à zéro implicitement
~~~~

### Référence pixs-agent--aacfb93718

Source : `openspec/specs/pixs-agent/spec.md`, ligne 146. SHA-256 du bloc : `8665641b1007fe45d2b73eb02d5a74fbfbac235ce440d82853ca6540720fbe11`.

~~~~text
### Requirement: Continuité sans PBO et reprise locale PZT

Sans PBO joignable, PA MUST se limiter aux capacités explicitement provisionnées, éligibles et encore valides ; une décision en ligne indisponible MUST bloquer l'action concernée. Diagnostic et reprise depuis PBO MUST passer par PZT, y compris local. Si PZT est entièrement indisponible, une réparation interne/opérateur MUST suivre sa procédure distincte, sans canal de substitution PBO–PA.

#### Scenario: Continuité sans PBO et reprise locale PZT

- **WHEN** PZT est entièrement arrêté
- **THEN** PBO ne reçoit aucun canal de contrôle local de contournement
~~~~

### Référence runtime--cc587c5666

Source : `openspec/specs/runtime/spec.md`, ligne 70. SHA-256 du bloc : `76fa9581b4885e8367327b804aae834ad5ddd7fdacbbf5a6c920c6458095b65f`.

~~~~text
### Requirement: États techniques PA distincts du runtime PBO

Les binaires PA MUST rester une couche distincte. Leurs seuls états techniques locaux déclarés par pixs-agent MUST être bornés, protégés et durables lorsque requis, sans autorité métier ni stockage implicite du runtime PBO. Un état PA nécessaire à la reprise MUST NOT dépendre du filesystem éphémère d’un conteneur.

#### Scenario: États techniques PA distincts du runtime PBO

- **WHEN** le conteneur PA est recréé
- **THEN** les états nécessaires reprennent depuis leur stockage déclaré sans données métier rendues autoritatives localement
~~~~

