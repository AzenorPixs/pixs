## MODIFIED Requirements

### Requirement: Contrat BulkOperation suivi par operation_id

Chaque opération MUST suivre un contrat versionné avec variantes IMPORT et EXPORT, états, rattachement à operation_id, travaux persistants, tenant et scope ; les formats de référence sont CSV et NDJSON, tout autre format via adaptateur déclaré.

#### Scenario: Suivi distinct des travaux

- **WHEN** une opération longue dépasse le seuil synchrone
- **THEN** elle retourne un operation_id suivi, distinct des identifiants des travaux qui l'exécutent

### Requirement: Import via staging privé et commandes propriétaires

Tout import MUST passer par un espace privé, vérifier taille, type, somme de contrôle et mapping versionné, puis appeler exclusivement les commandes du module propriétaire avec modes VALIDATE_ONLY, ATOMIC, ATOMIC_PER_CHUNK ou BEST_EFFORT explicites ; les conflits sont rejetés par défaut.

#### Scenario: Ligne en conflit rejetée

- **WHEN** une ligne contredit la stratégie de conflit déclarée
- **THEN** elle est rejetée dans un rapport versionné sans mutation partielle silencieuse

### Requirement: Export filtré, gouverné et révocable

Tout export MUST appliquer l'autorisation et le filtrage autorisé à la source, utiliser projections et champs déclarés avec instantané ou filigrane, produire fichier privé temporaire et manifeste, avec expiration, révocation, audit et échec fermé si la gouvernance est irrésolue.

#### Scenario: Export hors périmètre refusé

- **WHEN** un export dépasse le tenant ou le scope autorisé
- **THEN** il est refusé avant toute lecture, avec un audit
