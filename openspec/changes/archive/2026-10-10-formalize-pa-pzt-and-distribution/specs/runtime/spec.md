## MODIFIED Requirements

### Requirement: Processus stateless et coordination persistante

Les processus du runtime applicatif PBO web, worker et scheduler MUST NOT conserver en mémoire ou sur disque local un état nécessaire à l’autorité métier, à l’idempotence, à la reprise ou aux sessions. Leur coordination MUST reposer sur la persistance de référence ; un verrou mémoire n’est qu’une optimisation sans garantie. Les états techniques PA MUST suivre leur exigence distincte ci-dessous.

#### Scenario: Redémarrage d'un worker

- **WHEN** un worker PBO est redémarré en cours de traitement
- **THEN** ses travaux reprennent depuis la persistance de référence sans double effet non maîtrisé

#### Scenario: État technique PA requis en conteneur

- **WHEN** un profil PA nécessite un état durable de reprise
- **THEN** l’exigence distincte des états techniques PA est satisfaite sans autorité métier locale

## ADDED Requirements

### Requirement: États techniques PA distincts du runtime PBO

Les binaires PA MUST rester une couche distincte. Leurs seuls états techniques locaux déclarés par pixs-agent MUST être bornés, protégés et durables lorsque requis, sans autorité métier ni stockage implicite du runtime PBO. Un état PA nécessaire à la reprise MUST NOT dépendre du filesystem éphémère d’un conteneur.

#### Scenario: États techniques PA distincts du runtime PBO

- **WHEN** le conteneur PA est recréé
- **THEN** les états nécessaires reprennent depuis leur stockage déclaré sans données métier rendues autoritatives localement
