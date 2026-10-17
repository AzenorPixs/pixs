# C15 — Exploitation, santé et maintenance

## Pourquoi

correlated_log et health_classifier sont bornés/purs ; ils ne démontrent ni métriques/traces globales ni opérations de maintenance persistantes.

## Modifications proposées

Brancher sondes bornées réelles, journaux/métriques/traces corrélés, rétention séparée, management non public, opérations persistées avec plan/application, maintenance hiérarchisée et drainage.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions de profil proposées dans C00.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `integrate-runtime-authorization-and-super-admin`.
- `add-durable-minimized-audit`.
- `activate-reference-runtime-composition`.
- `add-reference-worker-scheduler-and-event-delivery`.

## Impact

Périmètre de réalisation futur : Brancher signaux/santé sur faits runtime réellement sondés, avec bornes et corrélation. Management distinct non public, plans et résultats persistés, confirmation des effets sensibles, maintenance générale/composant/route et drainage. Le diagnostic reste sans effet de réparation.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

PG indisponible → readiness fausse avec liveness distincte ; panne optionnelle isolée ; opération non autorisée refusée ; maintenance générale/composant/route ; arrêt/reprise observés sans perte silencieuse.

## Barrière de conception

Surfaces et identités de management, objectifs/limites, méthodes de mesure et rétentions ; aucun seuil arbitraire ou privilège système nouveau.
