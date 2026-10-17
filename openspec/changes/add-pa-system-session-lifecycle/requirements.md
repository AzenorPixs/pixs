# Références normatives — PA03

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 11 | [Quatre binaires et sept modes explicitement répartis](../../specs/pixs-agent/spec.md#L11) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 56 | [Démarrage système et session borné](../../specs/pixs-agent/spec.md#L56) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 74 | [Arrêt contrôlé et résultats réellement observés](../../specs/pixs-agent/spec.md#L74) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 83 | [Isolation des sessions et des privilèges](../../specs/pixs-agent/spec.md#L83) | ND | CANDIDAT_PROFIL_PA |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--24f2ceb983

Source : `openspec/specs/pixs-agent/spec.md`, ligne 11. SHA-256 du bloc : `7d77582c9257ea14c361d203416f60c56bc861c3552acc98a217d029ad22e615`.

~~~~text
### Requirement: Quatre binaires et sept modes explicitement répartis

PA MUST comporter exactement quatre binaires dédiés : démon système pour system-daemon ; événements système pour system-start et system-stop ; sessions utilisateur pour session-start, session-stop et session-daemon ; exécution PZT pour pzt-daemon. Les noms d'exécutables, chemins et options CLI restent à spécifier. Le découpage MUST NOT créer un cinquième binaire pour le démon de session.

#### Scenario: Quatre binaires et sept modes explicitement répartis

- **WHEN** une distribution PA complète décrit ses exécutables
- **THEN** elle identifie les quatre responsabilités et les sept modes sans les confondre
~~~~

### Référence pixs-agent--53648bdcca

Source : `openspec/specs/pixs-agent/spec.md`, ligne 56. SHA-256 du bloc : `8a5948a7ba60a40096f5a016fe042497befd117bbc772fb210d3f394ae2396e1`.

~~~~text
### Requirement: Démarrage système et session borné

system-daemon et session-daemon MUST avoir des délais indépendants, configurables et non négatifs, des préconditions et attentes maximales déclarées. pzt-daemon MUST être lancé sans ces délais au démarrage du système ou du conteneur ; il MUST exécuter PZT seulement s'il est activé/configuré, sinon se fermer. L'arrêt pendant un délai MUST annuler le lancement différé. Une mesure temporelle de démarrage MUST NOT tenir lieu de validité d'autorisation.

#### Scenario: Démarrage système et session borné

- **WHEN** le système s'arrête pendant le délai du démon système
- **THEN** ce lancement est annulé sans modifier la validité des mandats
~~~~

### Référence pixs-agent--ecb0f8d963

Source : `openspec/specs/pixs-agent/spec.md`, ligne 74. SHA-256 du bloc : `aed31e04d823e8fbc0d9c3e5cbd3ba326db9fc422077de59ced3026065096002`.

~~~~text
### Requirement: Arrêt contrôlé et résultats réellement observés

Les traitements system-stop et session-stop MUST avoir un budget maximal, un ordre déclaré avec les démons et dépendances, et une protection contre les doublons. PZT MUST être conservé tant que des échanges nécessaires et autorisés restent possibles dans le budget d'arrêt. Panne électrique, arrêt forcé et perte du processus MUST NOT être présentés comme une fermeture exécutée ou un résultat livré.

#### Scenario: Arrêt contrôlé et résultats réellement observés

- **WHEN** le conteneur disparaît avant confirmation du traitement d'arrêt
- **THEN** le résultat reste incomplet ou inconnu et aucun succès n'est inventé
~~~~

### Référence pixs-agent--66003e3bf6

Source : `openspec/specs/pixs-agent/spec.md`, ligne 83. SHA-256 du bloc : `99cbc1551e804651d03af579505a95e1fd0106b16882a87d0fc791622deaf1d5`.

~~~~text
### Requirement: Isolation des sessions et des privilèges

Le binaire utilisateur MUST fonctionner avec l'identité et les droits de la session réelle, distincte du compte utilisateur ; sessions concurrentes MUST être isolées. Fermer une session MUST arrêter son démon sans affecter les autres ; verrouillage ou suspension MUST NOT valoir fermeture. Le démon système et le binaire PZT MUST conserver leurs comptes, clés et frontières déclarés, sans élévation implicite depuis une session.

#### Scenario: Isolation des sessions et des privilèges

- **WHEN** une session demande une clé ou un droit réservé au système
- **THEN** l'accès est refusé selon les contrôles applicables sans transfert de privilège
~~~~

