## Why

Les 76 capacités actives constituent déjà la baseline fonctionnelle de Pixs,
mais leur rédaction résulte de plusieurs évolutions documentaires. Le
référentiel doit devenir lisible comme une spécification initiale unique : ses
frontières, ses termes, ses dépendances et ses exigences doivent être
cohérents sans changer les capacités ni les comportements validés.

## What Changes

- Établir une matrice traçable attestant que les 76 spécifications actives
  forment le corpus initial unique de Pixs, sans modifier leurs identifiants,
  chemins, exigences ni scénarios.
- Isoler toute relation dont l'harmonisation révélerait une évolution
  fonctionnelle, notamment la composition P0, le provisionnement, l'identité
  numérique de l'opérateur initial, l'autorisation et les références vers les
  `SecretProvider`.
- Produire une matrice de conservation exigence par exigence avant toute
  modification d'une spécification active.
- Valider chaque itération par OpenSpec en mode strict et arrêter la
  consolidation lorsqu'une conservation exacte ne peut pas être démontrée.

## Capabilities

### New Capabilities

Aucune. Ce change ne crée aucune capacité fonctionnelle.

### Modified Capabilities

Aucune. Ce change documentaire ne modifie aucune capacité active. Toute
évolution fonctionnelle ou documentaire d'une capacité reste hors périmètre et
doit être portée par un change distinct.

## Impact

Ce change ne modifie ni code, ni spécification active, ni API publiée, ni
dépendance, ni configuration exécutable. Il documente la conservation de la
baseline sans créer de règle métier ni changer un comportement normatif validé.
