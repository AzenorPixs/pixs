## MODIFIED Requirements

### Requirement: Surface HTTP initiale minimale

L'application initiale MUST déclarer des routes et des vues de base séparant
la vérification de santé du shell et de l'API versionnée. Toute route publique
MUST être explicitement déclarée ; toute route non déclarée publique MUST être
protégée ou refusée. Les réponses API initiales MUST respecter les contrats
HTTP publics applicables et MUST NOT simuler une capacité métier, une
autorisation ou une identité inexistante.

#### Scenario: Route initiale non déclarée

- **WHEN** une requête vise une route qui n'est ni une route de santé, ni une
  route du shell, ni une route API explicitement déclarée
- **THEN** l'application la refuse avec une réponse sans information sensible

### Requirement: Profil de test intégré isolé

Le projet MUST déclarer un profil de test local permettant de vérifier le
backend Django et le shell TanStack ensemble. Ce profil MUST expliciter les
dépendances nécessaires, l'adresse d'écoute, les capacités absentes et son
cycle de démarrage et d'arrêt ; il MUST NOT être présenté comme un déploiement
de production, initialiser des données métier permanentes ou élargir les
frontières de sécurité.

#### Scenario: Vérification locale conjointe

- **WHEN** le profil de test local est lancé avec une configuration valide
- **THEN** il permet de vérifier la santé, l'accès au shell et une réponse API
  déclarée sans dépendance de production ni secret
