## Why

Les 74 capacités actives constituent déjà la baseline fonctionnelle de Pixs,
mais leur rédaction résulte de plusieurs évolutions documentaires. Le
référentiel doit devenir lisible comme une spécification initiale unique : ses
frontières, ses termes, ses dépendances et ses exigences doivent être
cohérents sans changer les capacités ni les comportements validés.

## What Changes

- Consolider les 74 spécifications actives comme le corpus initial unique de
  Pixs, tout en conservant leurs identifiants et chemins de capacité.
- Préparer les règles, la matrice et les lots nécessaires à une future
  uniformisation de structure, de vocabulaire normatif, de références croisées
  et de frontières, sans modifier les exigences et scénarios actifs dans ce
  change.
- Identifier les relations à traiter par des changes fonctionnels distincts,
  notamment la composition P0, le provisionnement, l'identité numérique de
  l'opérateur initial, l'autorisation et les références vers les
  `SecretProvider`.
- Produire une matrice de conservation exigence par exigence avant toute
  modification d'une spécification active.
- Valider chaque itération par OpenSpec en mode strict et arrêter la
  consolidation lorsqu'une conservation exacte ne peut pas être démontrée.

## Capabilities

### New Capabilities

Aucune. Ce change ne crée aucune capacité fonctionnelle.

### Modified Capabilities

Aucune dans ce change. Toute modification d'une exigence ou d'un scénario sera
portée par un change distinct, précédé d'une matrice démontrant sa conservation
ou, si cela est impossible, d'une décision explicite du développeur.

## Impact

Ce change ne modifie ni code, ni API publiée, ni dépendance, ni configuration
exécutable, ni spécification active. Il ne crée aucune règle métier. Les
modifications ultérieures des spécifications actives resteront documentaires et
devront préserver tous les comportements normatifs validés.
