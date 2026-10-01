# Proposition — déclarations de profils runtime

## Why

La norme runtime exige des profils déclarant capacités garanties, dépendances obligatoires, limites et capacités désactivées. Le backend préparatoire expose seulement des rôles indisponibles ; il manque un descripteur déclaratif vérifiable sans service.

## What Changes

Ajouter RuntimeProfile frozen et validate_runtime_profile, purs et sans effets, avec tests de structure, contradictions et imports. Une déclaration ne prouve aucune capacité effective et ne modifie aucun invariant de sécurité.

## Capabilities

### New Capabilities

Aucune nouvelle exigence normative.

### Modified Capabilities

- runtime : implémentation partielle de Profils de déploiement déclarés, sans modification du texte validé.

## Impact

Trois créations source/tests uniquement. Aucune façade existante modifiée, aucun service, déploiement, Django effectif, base, secret ou dépendance nouvelle.
