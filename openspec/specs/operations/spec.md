# operations Specification

## Purpose
L'exploitation repose sur une interface de management distincte de l'API métier, des opérations persistantes planifiées et confirmées, et un état de maintenance contrôlé.

## Requirements

### Requirement: Interface de management distincte et non publique

L'interface d'exploitation DOIT être distincte de l'API métier et consommer les mêmes contrats et la même autorité quelle que soit la façade ; elle NE DOIT PAS être exposée au trafic public par défaut, toute exposition passant par une frontière avec identité, autorisation, périmètre et audit explicites.

#### Scenario: Façades convergeant sur le même contrat

- **WHEN** une opération est déclenchée via la ligne de commande officielle ou l'interface d'administration
- **THEN** elle produit le même plan, les mêmes contrôles et le même résultat audités

### Requirement: Opérations persistantes avec plan et idempotence

Toute opération d'exploitation DOIT porter identifiant, version, acteur, contexte, périmètre, clé d'idempotence, plan, état et résultat persistés ; les mutations sensibles DOIVENT exiger une confirmation ou une étape d'application distincte de la génération du plan.

#### Scenario: Rejeu d'une opération annulée

- **WHEN** une opération est rejouée avec la même clé d'idempotence
- **THEN** elle ne produit pas d'effet en double et renvoie son état persisté

### Requirement: Sorties sans secret et codes stables

Les façades d'exploitation NE DOIVENT PAS exposer de secret, token, clé ou charge sensible dans leurs sorties, réponses, journaux ou diagnostics ; les modes non interactifs DOIVENT produire des codes de sortie et des erreurs stables exploitables par un pipeline.

#### Scenario: Commande non autorisée

- **WHEN** une opération non autorisée, ambiguë ou non idempotente est demandée
- **THEN** elle échoue explicitement avec un code stable au lieu de simuler un succès

### Requirement: État de maintenance avec drainage borné

La mise en maintenance DOIT drainer les traitements en cours dans une durée bornée avant de bloquer les nouvelles mutations, n'autoriser par défaut que les lectures explicitement compatibles, et réévaluer configuration, composition, migrations, dépendances et permissions avant la sortie ; le refus de maintenance NE DOIT PAS être présenté comme un échec métier définitif.

#### Scenario: Requête reçue pendant le drainage

- **WHEN** une requête métier arrive pendant la phase de drainage
- **THEN** elle reçoit un état contractuel stable et n'est jamais exécutée partiellement

### Requirement: Health, diagnostic et audit opérateur

L'exploitation DOIT exposer la santé et le diagnostic sans effet métier ni secret, et chaque action d'opérateur DOIT être corrélée et audité avec acteur, périmètre et résultat.

#### Scenario: Réparation via le diagnostic

- **WHEN** un opérateur demande une action de réparation ou de reconfiguration
- **THEN** elle passe par une opération explicitement autorisée et auditée, distincte de la lecture de diagnostic
