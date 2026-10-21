## ADDED Requirements

### Requirement: Processus PZT configurables sous propriétaire réseau unique

Le binaire PZT MUST permettre un plan de processus et de concurrence selon runtime et les ressources de son environnement. Les rôles, auxiliaires, identités, canaux et limites MUST être déclarés et qualifiés. Le mode pzt-daemon MUST conserver un propriétaire admissible unique des ressources réseau par périmètre ; augmenter les processus MUST NOT créer des écrivains concurrents sur ce périmètre.

#### Scenario: Auxiliaires réseau supplémentaires

- **WHEN** un plan augmente des processus auxiliaires PZT
- **THEN** leurs fonctions restent déclarées sous contrôle du propriétaire réseau sans écriture concurrente des mêmes routes, interfaces ou règles

#### Scenario: Propriétaires réseau concurrents

- **WHEN** un plan demande deux propriétaires simultanément actifs du même périmètre réseau
- **THEN** son activation est refusée sauf séparation explicite de périmètres indépendants qualifiés

### Requirement: Budgets PZT sans affaiblissement des garanties

Le plan de ressources PZT MUST être configuré et suivi par pixs.pzt selon runtime. Il MUST préserver démarrage, contrôle local mTLS, expiration, révocation, protection indépendante, attestation et reprise exigés par le profil. Une insuffisance MUST empêcher l'admission ou déclencher l'état sûr prévu ; elle MUST NOT prolonger un droit ni ouvrir un canal PBO–PA hors PZT.

#### Scenario: Quota incompatible avec la révocation

- **WHEN** un budget CPU ou mémoire ne permet pas de garantir les délais de révocation du profil
- **THEN** le plan n'est pas admis et aucune qualification de ces délais n'est revendiquée

#### Scenario: Réseau désactivé

- **WHEN** le réseau est désactivé malgré un plan de processus disponible
- **THEN** le binaire réseau se ferme selon son lifecycle et le module pixs.pzt reste composé dans PBO
