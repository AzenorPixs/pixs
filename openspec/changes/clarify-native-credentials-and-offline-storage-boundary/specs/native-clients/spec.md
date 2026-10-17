## MODIFIED Requirements

### Requirement: Session et stockage local sécurisés

Les credentials et secrets d’un client natif MUST utiliser le mécanisme de stockage sécurisé déclaré par la plateforme, séparé des projections, caches et files hors ligne. Ils MUST NOT être placés dans un fichier, journal, sauvegarde ou stockage local non protégé. Un mécanisme indisponible MUST NOT provoquer un repli vers un stockage ordinaire.

#### Scenario: Sauvegarde d'application

- **WHEN** le système effectue une sauvegarde locale ordinaire
- **THEN** elle n'inclut pas de credential Pixs non protégé

#### Scenario: Mécanisme sécurisé indisponible

- **WHEN** le mécanisme déclaré ne permet pas de conserver ou d’utiliser le credential de façon vérifiable
- **THEN** l’opération concernée est refusée sans copier le credential dans un fichier, une base hors ligne ou un stockage non protégé
