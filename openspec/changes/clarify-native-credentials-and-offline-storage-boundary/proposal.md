# N02 — Frontière du coffre natif et des données hors ligne

## Pourquoi

L’audit relève une ambiguïté entre l’obligation de stockage sécurisé des credentials natifs et l’interdiction générale des secrets/jetons stockés localement dans offline-first. Le développeur a validé le 17 octobre 2026 la préparation de la séparation du coffre natif et des données hors ligne.

## Modifications proposées

- Préciser la séparation entre mécanisme sécurisé de credentials de la plateforme et projections, caches et files d’intentions hors ligne.
- Conserver l’interdiction des secrets et jetons hors coffre natif sécurisé et dans les données hors ligne ; maintenir l’interdiction de stockage local des données restreintes.
- Refuser tout repli vers un stockage ordinaire si le mécanisme sécurisé est indisponible.
- Conserver les règles de conflits, révocation, purge et réévaluation backend ; aucune mutation métier confirmée localement.

## Capacités modifiées

- `offline-first` : périmètre explicite de l’interdiction de stockage.
- `native-clients` : stockage protégé séparé et absence de fallback non protégé.

Aucune nouvelle capacité, dépendance ou plateforme choisie. O17/O18/O23 et leurs recettes consomment cette clarification dans les profils combinés. Les identités et sessions restent sous les contrats C03.

## Impact

Deux deltas proposés dans ce dossier, sans synchronisation du canon ni code. Aucun accès à un coffre réel, installation de bibliothèque, migration, application native, clé ou credential créé/manipulé. La validation de préparation ne vaut pas qualification d’un mécanisme de plateforme.
