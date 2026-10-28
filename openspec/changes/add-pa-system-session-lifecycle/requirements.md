# Références normatives — PA03

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 64 | [Trois binaires PA et six modes distincts de PZT](../../specs/pixs-agent/spec.md#L64) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 117 | [Démarrage système et session borné](../../specs/pixs-agent/spec.md#L117) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 139 | [Arrêt contrôlé et résultats réellement observés](../../specs/pixs-agent/spec.md#L139) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 148 | [Isolation des sessions et des privilèges](../../specs/pixs-agent/spec.md#L148) | ND | CANDIDAT_PROFIL_PA |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--24f2ceb983

Source : `openspec/specs/pixs-agent/spec.md`, ligne 64. SHA-256 du bloc : `75afef0ebd4a6d966f0a81ead33b8b4d1a4e65e0de5176d506eb82484e9b9040`.

~~~~text
### Requirement: Trois binaires PA et six modes distincts de PZT

PA MUST comporter exactement trois binaires : démon système pour system-daemon ;
événements système pour system-start et system-stop ; sessions utilisateur pour
session-start, session-stop et session-daemon. PZT et son mode pzt-daemon MUST
rester un composant exécutable indépendant, colivré selon deb-package et
docker-image. Le démon de session MUST NOT créer un binaire supplémentaire.
Les chemins et options CLI restent à spécifier.

#### Scenario: Répartition PA et PZT

- **WHEN** la composition complète PA/PZT est décrite
- **THEN** elle distingue trois binaires et six modes PA du binaire indépendant PZT et de son mode pzt-daemon
~~~~

### Référence pixs-agent--53648bdcca

Source : `openspec/specs/pixs-agent/spec.md`, ligne 117. SHA-256 du bloc : `9ed0bb531792f1443955b293fd3a5bc5e4737e73cbe698ac8a3eb93618e18063`.

~~~~text
### Requirement: Démarrage système et session borné

system-daemon et session-daemon MUST avoir des délais indépendants,
configurables et non négatifs, des préconditions et attentes maximales déclarées.
L'arrêt pendant un délai MUST annuler le lancement différé. Le démarrage du
composant indépendant PZT MUST suivre pzt et MUST NOT être attribué à un mode PA.
Une mesure de démarrage MUST NOT tenir lieu de validité d'autorisation.

#### Scenario: Arrêt pendant délai PA

- **WHEN** le système s’arrête pendant le délai du démon système
- **THEN** ce lancement est annulé sans modifier la validité des mandats ni transférer la gestion de PZT à PA
~~~~

### Référence pixs-agent--ecb0f8d963

Source : `openspec/specs/pixs-agent/spec.md`, ligne 139. SHA-256 du bloc : `aed31e04d823e8fbc0d9c3e5cbd3ba326db9fc422077de59ced3026065096002`.

~~~~text
### Requirement: Arrêt contrôlé et résultats réellement observés

Les traitements system-stop et session-stop MUST avoir un budget maximal, un ordre déclaré avec les démons et dépendances, et une protection contre les doublons. PZT MUST être conservé tant que des échanges nécessaires et autorisés restent possibles dans le budget d'arrêt. Panne électrique, arrêt forcé et perte du processus MUST NOT être présentés comme une fermeture exécutée ou un résultat livré.

#### Scenario: Arrêt contrôlé et résultats réellement observés

- **WHEN** le conteneur disparaît avant confirmation du traitement d'arrêt
- **THEN** le résultat reste incomplet ou inconnu et aucun succès n'est inventé
~~~~

### Référence pixs-agent--66003e3bf6

Source : `openspec/specs/pixs-agent/spec.md`, ligne 148. SHA-256 du bloc : `99cbc1551e804651d03af579505a95e1fd0106b16882a87d0fc791622deaf1d5`.

~~~~text
### Requirement: Isolation des sessions et des privilèges

Le binaire utilisateur MUST fonctionner avec l'identité et les droits de la session réelle, distincte du compte utilisateur ; sessions concurrentes MUST être isolées. Fermer une session MUST arrêter son démon sans affecter les autres ; verrouillage ou suspension MUST NOT valoir fermeture. Le démon système et le binaire PZT MUST conserver leurs comptes, clés et frontières déclarés, sans élévation implicite depuis une session.

#### Scenario: Isolation des sessions et des privilèges

- **WHEN** une session demande une clé ou un droit réservé au système
- **THEN** l'accès est refusé selon les contrôles applicables sans transfert de privilège
~~~~
