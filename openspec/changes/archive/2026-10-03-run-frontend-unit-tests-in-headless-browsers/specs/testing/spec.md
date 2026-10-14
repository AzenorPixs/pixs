# testing — Delta

## ADDED Requirements

### Requirement: Exécution navigateur headless des unités frontend web

Les tests unitaires de la partie frontend web MUST être exécutés dans tous les
navigateurs déclarés par DEVOPS.md, en mode headless ; le succès de ces tests
uniquement sous Node MUST NOT tenir lieu de preuve de cette exigence.

#### Scenario: Les deux moteurs déclarent les cas

- **WHEN** `npm --prefix frontend test` s'exécute sur un environnement
  déclarant Chromium et Firefox headless
- **THEN** chaque cas unitaire frontend reçoit une preuve d'exécution issue de
  chaque navigateur déclaré et le résultat global n'est vert qu'avec les deux
  moteurs

#### Scenario: Moteur manquant ou cas non exécuté

- **WHEN** un navigateur déclaré est indisponible, ne répond pas dans les
  bornes, ou n'exécute pas l'intégralité des cas
- **THEN** l'exécution est en échec diagnostiqué, sans substitution par le
  seul résultat Node ou par la réussite du build
