## Why

Le référentiel décrit la pile de référence et les garanties de Pixs, mais ne
définit pas encore la composition vérifiable de sa première application de
développement. Il faut la spécifier avant toute implémentation afin de rendre
le démarrage Django, le shell TanStack et le test intégré cohérents avec le
socle modulaire.

## What Changes

- Ajouter une capacité qui définit la composition initiale de développement :
  projet Django, configuration PostgreSQL externe, chargement de `pixs.kernel`
  et `pixs.core`, conformité P0, composant d'exemple non métier, surface HTTP
  minimale, shell TanStack et profil de test local.
- Définir les frontières de sécurité, de configuration et de validation de
  cette composition sans imposer de donnée métier, de fournisseur concret, de
  secret ou d'artefact de production.
- Ajouter les modes installateur, première configuration et administration
  initiale, avec leurs états de référence externes et persistés, un Super Admin
  opérateur initial vérifié et une politique d'autorisation déclarée.
- Exiger que les paramètres PostgreSQL recueillis par l'installateur deviennent
  des références externes vers un `SecretProvider`, sans persistance durable de
  leur valeur.
- Étendre les règles d'exploitation et d'audit pour les maintenances à portée
  générale, granulaire et sous-granulaire, ainsi que pour toute activité du
  panneau d'administration.
- Limiter ce change à la spécification : il ne crée ni code, ni dépendance,
  ni configuration exécutable.

## Capabilities

### New Capabilities

- `initial-application-bootstrap` : composition initiale vérifiable de
  l'application de référence Django et TanStack.
- `initial-administration` : premier démarrage, modes d'installation et de
  configuration, compte Super Admin et panneau d'administration.

### Modified Capabilities

- `operations` : niveaux de maintenance et transitions de mode contrôlées.
- `audit` : couverture exhaustive et persistante du panneau d'administration.

## Impact

Les futurs artefacts Django, frontend, provisionnement et administration
devront satisfaire ces capacités. Aucun code, API publiée, dépendance, secret,
base de données ou serveur n'est créé ou modifié par ce change.
