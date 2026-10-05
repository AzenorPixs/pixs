## MODIFIED Requirements

### Requirement: Composition Django initiale déclarée

L'application initiale MUST fournir un projet Django exécutable par
`manage.py` et déclarer une composition P0 conforme à
`reference-composition`. Ses réglages MUST sélectionner PostgreSQL comme
persistance de référence et charger `pixs.kernel` ainsi que `pixs.core` dans
une composition explicite. La composition MUST inclure un composant d'exemple
technique qui démontre la composition et ses contrats sans créer de domaine,
de donnée métier ou de fournisseur concret. Les paramètres de connexion
PostgreSQL et toute valeur sensible MUST provenir de la configuration runtime
ou de références de secrets ; ils MUST NOT être codés dans le dépôt, les
réglages distribués ou les artefacts de test.

#### Scenario: Composition initiale valide

- **WHEN** le profil de développement valide la composition Django initiale
- **THEN** il identifie `manage.py`, PostgreSQL, `pixs.kernel`, `pixs.core` et
  le composant d'exemple P0 sans exposer de valeur sensible ni de donnée métier
