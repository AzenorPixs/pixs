# Proposal

## Why

Le profil `source-filter-plan-v1` (`authorization-engine`, `TECHNICAL §12.6`) est validé mais sans implémentation. `authorize` mappe refus légitime et défaillance (fait/type inconnu, malformé, budget, port, horloge, audit) au même `DENIED` public, et une condition absente (`decision.py` `_evaluate`) produit `DENIED` sans exception du provider. Distinguer après-coup ou recopier validations/matching dupliquerait le moteur de façon fragile et risquerait un plan partiel après erreur.

## What Changes

- Extrait dans `decision.py` un helper privé commun d'évaluation détaillée, même moteur et mêmes ports, exécuté une seule fois par ressource pour `authorize`. `authorize` conserve exactement signature, `Decision` publique et comportements précédents (mappage détaillé→public inchangé).
- Le helper distingue trois statuts privés fermés : `ALLOW`, `DENY_POLICY` (refus explicite ou absence de politique applicable, conditions non satisfaites, seuils/fenêtres/périmètres, révocation connue `REVOKED`, expiration connue, via exception privée dédiée) et `ERROR` (entrée/faits malformés, type/attribut/fait inconnu ou absent requis, `bool` comme `int`, budget dépassé, snapshot/horloge non fiables, exception port, audit non honoré — audit non honoré toujours `ERROR`).
- Nouveau `filter_plan.py` utilisant ce helper une seule fois par ressource : `DENY_POLICY` exclut sans invalider ; `ERROR` invalide tout le lot fermé sans ID. Aucun callback global, aucun double appel provider/audit, aucune validation copiée.
- Lot/plan immuables selon spec : homogénéité, unicité IDs, `max_filter_requests` positif sans défaut, vide admis, même snapshot canonique validé (validations pures répétées autorisées via wrapper interne partagé sans bypass), horloge capturée une fois, `resource_ids` triés/dédupliqués ALLOW seuls, union AUDIT ALLOW seuls, `expires_at` minimum, vide/None si aucun ALLOW.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `authorization-engine` : traçabilité d'implémentation du profil préparatoire `source-filter-plan-v1`, sans évolution normative ni nouvelle exigence.

## Impact

- Code : `decision.py` (extraction seule), `filter_plan.py`, `__init__.py` (exports bornés). Tests : unitaires + intégration mémoire. Exclus : PEP Django, PostgreSQL, filtrage source exécuté, caches, audit durable, providers concrets, frontend, dépendances nouvelles, runtime complet, P0 global.
- Le plan ne prouve ni fraîcheur runtime, ni jeton d'accès, ni AUDIT honoré ; réévaluation/invalidation futures restent obligatoires.
