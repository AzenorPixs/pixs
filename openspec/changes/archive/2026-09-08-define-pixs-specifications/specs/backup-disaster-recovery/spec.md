## Purpose

La sauvegarde et la reprise après sinistre sont une stratégie déclarée par déploiement avec objectifs RPO/RTO, restaurations vérifiées et preuves auditées, sans jamais substituer la sauvegarde à l'autorité métier.

## ADDED Requirements

### Requirement: Stratégie déclarée par déploiement

Le déploiement DOIT définir ses objectifs de perte et de délai de reprise acceptables, son périmètre, ses durées de conservation, ses contrôles d'accès, ses procédures de restauration et la preuve attendue après restauration ; le socle n'impose aucun outil particulier.

#### Scenario: Procédure sans objectifs déclarés

- **WHEN** une procédure de restauration est demandée sur un déploiement sans objectifs déclarés
- **THEN** l'écart est signalé et la couverture de reprise ne peut être certifiée

### Requirement: Périmètres de sauvegarde distincts

La stratégie DOIT couvrir séparément les données persistantes avec leurs états de traitement, les objets et fichiers avec versions, rétentions et sommes de contrôle, et la configuration avec les références de secrets et leurs mécanismes de rotation ; une sauvegarde NE DOIT PAS devenir une nouvelle source d'autorité.

#### Scenario: Sauvegarde partielle

- **WHEN** un périmètre n'est pas couvert par la sauvegarde invoquée
- **THEN** la reprise est déclarée incomplète avec le périmètre manquant identifié

### Requirement: Restauration cohérente et réapplication des gouvernances

Une restauration DOIT vérifier la cohérence entre métadonnées, objets, événements non publiés, travaux, points de contrôle, mappings externes et versions de composants, et réappliquer les marqueurs de suppression, le journal d'effacement, les restrictions légales et les états de rétention avant toute exposition aux utilisateurs ou aux synchronisations.

#### Scenario: Objet restauré après suppression validée

- **WHEN** un objet restauré contredit une suppression déjà validée
- **THEN** la divergence est bloquée ou rendue explicite et auditable, sans annulation silencieuse

### Requirement: Tests de restauration isolés et preuves

Les restaurations DOIVENT être exécutables dans un environnement isolé, testées régulièrement, et produire une preuve conservée ; après restauration le système DOIT démarrer en état contrôlé, détecter les écarts de composition ou de version et reprendre les traitements idempotents.

#### Scenario: Démarrage après restauration

- **WHEN** une instance démarre depuis une restauration testée
- **THEN** les traitements non confirmés restent dans un état diagnostiquable sans réémission automatique

### Requirement: Restauration destructive autorisée et auditée

Une restauration destructive ou un retour à un point antérieur DOIT être une opération explicitement autorisée, confirmée et auditée ; aucune purge implicite d'identités, tenants, autorisations, secrets ou données métier NE DOIT être tolérée pour rendre la restauration possible.

#### Scenario: Suppression implicite refusée

- **WHEN** une procédure propose de réinitialiser des données pour faciliter la restauration
- **THEN** elle est refusée hors opération autorisée distincte avec audit propre
