# Tasks — VALIDATE IMPORT VALIDATE_ONLY

- [x] 1. Vérifier artefacts, delta exact et périmètre strict ciblé avant tout code. Preuve : quatre artefacts UTF-8 LF, B07 canonique exact, `openspec validate add-bulk-import-validation-orchestration-v1 --strict` exit 0, requestId cismp1-751d094337644962a27d8eaccc484dce.
- [ ] 2. Factorisation privée minimale de `bulk_private_object_reader.py` préservant API et comportement hash-only.
- [ ] 3. Helper de capture `validate` dans `bulk_trusted_ports.py` seulement si strictement nécessaire, sous mandat distinct.
- [ ] 4. Nouveau `bulk_import_validate.py` : phase VALIDATE_ONLY, parcours qualifié unique, parsing interne, tampon borné nettoyé, owner après intégrité et fermeture.
- [ ] 5. Persistance finale rapport, checkpoint et progression avec transition sous gardes actuelles seulement et frontière async ORM ; refus sans forçage après annulation, expiration ou perte de bail.
- [ ] 6. Tests unitaires : séquences, gardes, bornes, non-fuite, nettoyage du tampon, aucun owner avant preuve, zéro `execute`.
- [ ] 7. Tests PostgreSQL isolés : nominal, rejets, rollback, CAS et concurrence, bail, replay terminal, aucun forçage.
- [ ] 8. `py_compile` de tous les fichiers Python modifiés et régressions lecteur, trusted ports, parser, repositories et admission utiles.
- [ ] 9. Conformité OpenSpec, UTF-8 LF, empreintes du périmètre et validation combinée sous intégration.

Procédure après preuves : cocher unitairement chaque tâche après sa preuve
observée ; archive unique seulement sur autorisation CGPT sous intégration,
puis `STATISTIQUES.md` sous mandat distinct (six sections et totaux),
publication, gate et libération, puis retour `SÉLECTION` du RUN.
