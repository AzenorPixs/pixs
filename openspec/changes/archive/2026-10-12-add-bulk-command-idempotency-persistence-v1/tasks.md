## 1. Préparation et implémentation

- [x] 1.1 Préparer quatre artefacts révisés, delta MODIFIED B10 verbatim ; réussir strict change avant code.
- [x] 1.2 Implémenter `bulk_command_idempotency_record.py` + `bulk_command_idempotency_repository.py` + import minimal `models.py` + migration réversible `0006` : 12 champs explicites, PK locale hors 12 clés, uniques 4 colonnes, insertion privée dans unit seul, finalize exige jeton actif même thread/alias, atomic savepoint=False + latched + set_rollback.
- [x] 1.3 Implémenter test unitaire pur unittest : types hostiles/noecho avant I/O, import inerte, capture/copies owned et métadonnées/migration sans DB ; rejeu/divergence/CAS comportementaux prouvés en PG réel, sans mocks miroirs.
- [x] 1.4 Implémenter test d'intégration PG isolé unittest : autodetection + forward/reverse 0006 seule, unique clé/race, replay stable/divergent même clé digest ET serializer, rollback technique et sortie non finalisée non committable même après capture, co-transaction synthétique/progression/checkpoint, nettoyage/conns/public stables.
- [x] 1.5 Exécuter `.venv/bin/python3` pour compilation et tests cibles, gardes, puis régressions pertinentes nommées après inspection du code touché avec le mécanisme unittest du projet ; validations OpenSpec avec exécutable DEVOPS.
- [x] 1.6 Vérifier strict change sans issue, UTF-8/LF, périmètre 6 sources, delta verbatim, canon/exports préservés et acceptation complète.

## Procédure après preuves

Sur preuves des six tâches, les cocher. Puis archive unique `--skip-specs`, rapport distinct six sections vérifié, retour SÉLECTION. Ne pas cocher archive/STATISTIQUES avant leur preuve.
