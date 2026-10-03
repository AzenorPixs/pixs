# Proposal: add-initial-capability-descriptors

## Why

L'exigence « Descripteur de capacité résolu à la composition » de la capacité `capabilities` présente une lacune ciblée : le descripteur typé n'est pas exposé à la composition : recherche ciblée sur `src/pixs` sans aucun `CapabilityDescriptor` ni champ de disponibilité ; les cibles résolues produites par `_resolve_full` ne sont pas exposées au résultat de composition. Les trois autres exigences (états de disponibilité, fanion, résolution sur version déclarée déjà prise en charge par le moteur existant) restent hors périmètre de ce change : aucune disponibilité opérationnelle, aucune activation runtime, aucun fanion n'est prétendu.

## What Changes

- `src/pixs/kernel/capabilities.py` (création) : `CapabilityDescriptor` typé canonique à sept champs obligatoires — `capability_id`, `capability_version`, `owner_component`, `contract_refs`, `provider_ref`, `criticality`, `fallback` — et fonctions pures de construction et de liaison :
  - `build_capability_descriptors(manifests)` : descripteurs dérivés exclusivement des `provided_capabilities` de manifests validés (`owner_component = manifest.id`, `criticality`/`fallback` copiés tels que déclarés, aucune politique inventée) ; tout objet non `ComponentManifest` ou champ invalide produit un `Diagnostic` sans écho de valeur.
  - `bind_capability_descriptors(descriptors, resolved_targets)` : liaison descriptive uniquement — `provider_ref = owner_component` si et seulement si la liaison exacte `(owner, "CAPABILITY", capability_id, capability_version)` figure dans le lot `resolved_targets` déjà produit par `_resolve_full` ; sinon `provider_ref = None` (fourni sans liaison résolue : non consommé ou résolution non réussie). Aucune indisponibilité, aucun état, aucun fanion.
- `src/pixs/kernel/composition.py` (modification strictement additive) : champ `capability_descriptors` (défaut `()`) ajouté à `CompositionResult`, renseigné dans `compose` par réutilisation directe des `resolved_targets` internes ; les algorithmes fournisseurs et de conformité, la sémantique `activated`, `evaluation_scope`, `unevaluated_dimensions` et `globally_compatible = False` restent inchangés ; jamais de reconstruction des cibles par parsing de diagnostics ; jamais de double résolution ni de re-lecture.

Distinguer fourni / non consommé / résolu : la distinction est descriptive et exacte — fourni = descripteur présent ; sélectionné (résolu) = liaison exacte dans `resolved_targets` ; sans liaison résolue = descripteur avec `provider_ref = None` (une consommation non résolue ne devient pas une absence de consommation). Aucun état de disponibilité n'est émis.

## Impact

- Affected specs: `capabilities`
- Affected code:
  - `src/pixs/kernel/capabilities.py` (création)
  - `src/pixs/kernel/composition.py` (additif : champ `capability_descriptors` + renseignement)
  - `tests/unit/test_capability_descriptors.py` (création)
  - `tests/integration/test_capability_descriptors_integration.py` (création)

Régression ciblée : suites composition/conformité existantes exécutées de nouveau sous runtime actuel (Python 3.14.8 déclaré, mandats distincts) ; si un test existant comparant intégralement `CompositionResult` divergeait du fait du nouveau champ renseigné, l'écart est rapporté à CGPT avant toute correction (aucun ajustement silencieux). Aucune claim de P0, readiness, disponibilité, compatibilité globale, activation réelle, Django, PG, Git, installation ou route.
