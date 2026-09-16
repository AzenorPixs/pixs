## Why

Le référentiel actif compte 74 capacités validées, mais 18 d'entre elles ne
disposent d'aucun change OpenSpec retraçable. Une consolidation documentaire
est nécessaire pour établir une référence complète, vérifiable et non
destructive avant toute évolution fonctionnelle.

## What Changes

- Déclarer les 74 capacités actives comme le référentiel fonctionnel de
  référence de Pixs.
- Conserver sans renommage, suppression, déplacement ni modification de leurs
  exigences et scénarios les frontières des capacités actives.
- Documenter la provenance historique connue, les limites de cette provenance
  et la méthode de contrôle de cohérence à appliquer aux évolutions futures.
- **BREAKING** : aucune rupture fonctionnelle, d'API ou de compatibilité n'est
  introduite.

## Capabilities

### New Capabilities

Aucune. Cette évolution ne définit pas de comportement produit.

### Modified Capabilities

Aucune. Les exigences actives sont conservées à l'identique ; l'évolution est
documentaire et déclare donc `skip_specs: true`.

## Impact

Aucun code, API, dépendance, artefact de distribution ou comportement runtime
n'est affecté. Seuls les artefacts du change OpenSpec documentent la décision
de consolidation et les vérifications associées.
