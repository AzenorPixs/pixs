## MODIFIED Requirements

### Requirement: Paquet corrélé à la release

Chaque paquet MUST identifier sa release, son périmètre de composition, ses manifests, contrats, compatibilités et garanties. Il MUST rester corrélable aux autres artefacts de cette release pour les capacités communes. Cette corrélation MUST NOT imposer un contenu binaire identique entre le paquet PA, le paquet PBO/PFO et l’image sans fonctions de session ; les noms et versions exactes restent à spécifier.

#### Scenario: Version de paquet incohérente

- **WHEN** un paquet revendique une release différente de l’artefact qu’il installe
- **THEN** l’installation signale l’incohérence et bloque l’activation

#### Scenario: Deux paquets indépendants

- **WHEN** la composition Debian cible est vérifiée
- **THEN** le paquet PA et le paquet PBO/PFO restent distincts selon leurs exigences de composition

## ADDED Requirements

### Requirement: Distribution Debian indépendante PA et PBO PFO

La distribution Debian MUST comporter un paquet PBO/PFO et un paquet PA indépendant. Le paquet PBO/PFO MUST contenir le module essentiel PZT et MUST NOT embarquer les quatre binaires PA. L’installation PA seule MUST NOT requérir PBO/PFO locaux comme contenu embarqué ; les compatibilités et dépendances d’installation restent déclarées.

#### Scenario: Distribution Debian indépendante PA et PBO PFO

- **WHEN** PA est installé seul
- **THEN** son paquet reste indépendant et peut joindre un PBO distant autorisé

### Requirement: Quatre binaires dans le paquet PA

Le paquet PA MUST livrer exactement les quatre exécutables définis par pixs-agent : démon système, événements de démarrage/arrêt de l’hôte, sessions utilisateur et exécution PZT. Il MUST conserver la séparation des modes et permissions ; noms/chemins et versions restent à spécifier.

#### Scenario: Quatre binaires dans le paquet PA

- **WHEN** le paquet PA est vérifié
- **THEN** les quatre binaires et leurs responsabilités sont identifiables sans PBO/PFO embarqués
