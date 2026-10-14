## Why
Le profil BulkTenantLink v1 est validé dans le canon mais ne dispose pas encore de représentation Python ni de validation pure.

## What Changes
- Ajouter uniquement le profil interne immuable à deux références explicites.
- Ajouter les tests comportementaux et la vérification dans un processus frais.
- Conserver les exigences générales bulk et tenant sans comportement runtime.

## Capabilities
### New Capabilities
Aucune.

### Modified Capabilities
- bulk-operations : implémenter exclusivement les quatre exigences BulkTenantLink v1 déjà canoniques.

## Impact
Trois nouveaux fichiers Python ; aucun changement de dépendance, configuration, persistance, API publique ou fichier existant.
