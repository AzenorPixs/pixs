## MODIFIED Requirements

### Requirement: Import via staging privé et commandes propriétaires

Tout import MUST passer par un espace privé, vérifier taille, type, somme de contrôle et mapping versionné, puis appeler exclusivement les commandes du module propriétaire avec modes VALIDATE_ONLY, ATOMIC, ATOMIC_PER_CHUNK ou BEST_EFFORT explicites ; les conflits sont rejetés par défaut.

#### Scenario: Ligne en conflit rejetée

- **WHEN** une ligne contredit la stratégie de conflit déclarée
- **THEN** elle est rejetée dans un rapport versionné sans mutation partielle silencieuse
