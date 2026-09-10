## Why

Les exigences OpenSpec actives emploient des mots-clés normatifs français qui
ne sont pas reconnus par le validateur RFC 2119. Pixs doit utiliser une forme
normative interopérable, vérifiable automatiquement et cohérente dans ses
cadrages et spécifications.

## What Changes

- Définir la convention RFC 2119 applicable aux exigences Pixs : prose en
  français, mots-clés normatifs `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT` et
  `MAY` en majuscules.
- Employer les formes négatives canoniques `MUST NOT` et `SHOULD NOT`, sans
  construction hybride telle que `NE MUST` ou `NE SHOULD`.
- Appliquer cette convention aux exigences actives d'OpenSpec.
- Documenter la même convention dans les cadrages global, technique et de
  construction.
- Préserver la signification, les scénarios et les garanties existants.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

Toutes les capacités existantes sous `openspec/specs/` : les exigences sont
modifiées uniquement pour employer les mots-clés normatifs RFC 2119, sans
changement de comportement ni de scénario.

## Impact

Ce changement ne modifie ni code, ni API, ni dépendance. Il supprime les
avertissements de conformité RFC 2119 du validateur OpenSpec et fournit une
convention normative unique pour les évolutions futures.
