# Proposal — VALIDATE IMPORT VALIDATE_ONLY (parcours unique)

## Why

Composer la phase VALIDATE des imports volumineux sans mutation propriétaire.
Le flux source doit être prouvé complet (intégrité SHA-256, métadonnées
finales identiques, fermeture réussie) avant toute validation propriétaire,
puis le rapport, le checkpoint et la progression doivent être persistés
ensemble uniquement sous bail, fencing et CAS actuels.

## What Changes

- Nouveau `src/pixs/backend/bulk_import_validate.py` : orchestration
  VALIDATE IMPORT VALIDATE_ONLY en un seul parcours storage qualifié.
- Vérificateur d'intégrité et parser mécanique exact sur chunks bornés ;
  unités logiques typées dans un tampon éphémère strictement borné par la
  PolicyV1 résolue, effacé à chaque refus, annulation ou sortie.
- `owner.validate` invoqué seulement après intégrité complète et fermeture
  positive ; `execute` jamais ; `canonical_bytes` seulement si le contrat
  actuel l'exige.
- Persistance finale atomique (rapport, checkpoint VALIDATE, progression,
  transition) sous `protected_unit`, CAS et bail actuels : révision N+1 pour
  le checkpoint puis N+2 pour la transition, unité finale unique.
- Les refus annulation, expiration ou perte de bail ne forcent aucune
  persistance ni fausse terminalité ; ils sont restitués explicites à
  réconcilier, sans falsifier preuve d'autorité ni checkpoint.
- Factorisation privée minimale de `bulk_private_object_reader.py`
  préservant son API hash-only (aucun contenu restitué par cette API).
- Helper `trusted_ports` éventuel pour la capture de `validate` seulement.
- Deux tests dédiés : unitaire et intégration PostgreSQL isolée.
- Réutilisation stricte de B03, B04, B05, B06, B07, B13 et schémas actuels,
  sans nouvelle norme, seuil, configuration ou dépendance.

## Capabilities

- Modified: bulk-operations seulement.

## Impact

- IMPORT VALIDATE_ONLY uniquement ; applied_rows nul, aucune mutation.
- Exclut worker, APPLY, EXPORT, routes, provider de production, migration,
  Git et autres RUN.
- Pas de reprise intra-validation inventée ; pas de transaction ordinaire
  contournant bail, fencing ou CAS après refus technique.
