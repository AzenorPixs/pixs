## 1. Préparation et implémentation

- [x] 1.1 Préparer quatre artefacts révisés, delta MODIFIED B10 verbatim ; réussir strict change avant code.
- [x] 1.2 Implémenter `bulk_admission_identity_values.py` pur : 9 clés exactes, snapshot bytes strict recapturé octet pour octet, digest/version/bulk_type/idempotency_key cohérents, résolus distincts des références snapshot, expires_at UTC exact.
- [x] 1.3 Implémenter `bulk_admission_identity_record.py` : from_values/as_values/full_clean explicites, PK id locale + UniqueConstraint 4 colonnes, checks non-vide/version/variant/digest, sans unicité operation_id ni FK ni extension crypto.
- [x] 1.4 Implémenter `bulk_admission_identity_repository.py` : insert force_insert seul + get owned, sans update/purge/touch_expiry ni raw SQL hors contrat ; importer minimalement dans `models.py`.
- [x] 1.5 Implémenter migration réversible `0005` unique ; prouver forward/reverse 0005 isolé.
- [x] 1.6 Implémenter test unitaire pur : types hostiles, JSON non canonique/doublons/suivi/float, digest et cohérences, immutabilité owned.
- [x] 1.7 Implémenter test d'intégration en processus frais pur sous gardes fichiers/réseau/processus/environnement/DB/Core, sans effet.
- [x] 1.8 Implémenter test PG synthétique en schéma privé : roundtrip, contraintes SQL, concurrence d'unicité (un seul gagnant), rollback, reverse only 0005, tables existantes stables, connexions fermées, aucun secret affiché.
- [x] 1.9 Compiler séparément les Python touchés ; réussir tests ciblés et régressions Bulk/Kernel/Jobs applicables.
- [x] 1.10 Vérifier strict change sans issue, UTF-8/LF, canon/exports/sources préservés et acceptation complète.

## Procédure après preuves

Cocher seulement après preuves ; archive unique --skip-specs puis STATISTIQUES.md sous mandat distinct. Vérifier six sections et totaux avant retour. Aucune admission complète ni idempotence SQL annoncée au-delà de la persistance.
