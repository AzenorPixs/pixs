# SP27 — Spécification de l’administration initiale, de la maintenance et de l’audit

<!-- ACL-R2 : code de lot attribué rétrospectivement le 2026-10-28. -->

## Why

Cette proposition extrait de l'archive historique du 16 septembre 2026 le lot
d'administration initiale, de maintenance et d'audit. Ses neuf exigences sont
séparées des quatre exigences de composition de développement pour supprimer
le dépassement du seuil de dix deltas par proposition. Leur texte est conservé
intégralement ; aucune ancienne restriction n'est réadoptée dans le canon actuel.

## What Changes

- Transférer sans changement les sept exigences et treize scénarios du delta
  historique `initial-administration`.
- Transférer sans changement l'exigence et le scénario de maintenance
  hiérarchisée du delta `operations`.
- Transférer sans changement l'exigence et le scénario d'audit du panneau du
  delta `audit`.
- Valider ce lot de neuf exigences et quinze scénarios indépendamment du lot
  bootstrap ; ne créer ni comportement supplémentaire ni doublon de delta.

## Capabilities

### New Capabilities

- `initial-administration` : capacité historique de modes de démarrage et
  d'administration initiale ; elle existe déjà dans le canon courant.

### Modified Capabilities

- `operations` : maintenance hiérarchisée du périmètre historique.
- `audit` : audit des interactions administratives du périmètre historique.

## Impact

Ce lot est une extraction documentaire de l'archive d'origine. Il n'implémente
ni application, installateur, service, fournisseur concret ou politique de
sécurité. Les évolutions ultérieures du canon, notamment l'exception transverse
Super Admin, restent prioritaires. Le réarchivage est réalisé avec `--skip-specs`.
Le lot bootstrap conserve [l'identité historique](../2026-09-16-specify-initial-application-bootstrap/proposal.md).
