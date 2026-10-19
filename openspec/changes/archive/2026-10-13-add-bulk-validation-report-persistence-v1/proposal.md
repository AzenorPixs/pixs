# Proposal: add-bulk-validation-report-persistence-v1

## Why

Le runtime Bulk v1 doit persister un rapport de validation append-only ValidationReportV1 avec huit clefs exactes, captures bornees par policy et catalogues explicites, codec prive TEXT pour progress et diagnostics, et identifiant technique sans unicite operation ni latest. Le validateur pur ne fournit pas de stockage durable des rapports ; les checkpoints déjà livrés et testés restent distincts de ce socle. Cette proposition reste dans la frontiere du contrat et ne cree aucune production de rapport proprietaire, aucune autorisation READ_RESULT, aucune gouvernance reelle, aucun catalogue ou autorite, aucun trust bool nouveau, aucun hash, clock, public wire, endpoint, receiver, provider, Outbox, Manifest, PA, PZT, aucune mutation purs, runtime, archives, CommandIdp, Envelope, Inbox existants, aucun frontend, Git, secret, infra, norme, cardinalite nouvelle, ni B13 global complet.

## What Changes

- Ajouter persistance append-only ValidationReportV1 a huit clefs EXACTES : report_version, operation_id, mode, progress, diagnostics, complete, source_version, mapping_version.
- Six scalaires + deux TEXT prives JSON pour progress et diagnostics, codec stdlib, Progress six noms purs non inventes, diag tuple RowDiagnostic trois champs code, field_reference, line_index sans message brut, capture typee OWNED et FROZEN avant codec, conversion tuple vers liste privee preservant l ordre.
- Policy et declared_codes et declared_fields obligatoires fournis par l appelant trusted, capture de contexte sans defaults, borne max_diagnostics appliquee AVANT inspection poison.
- Codec refusant dup keys, NaN et malformed, revalidation des huit champs dans le contexte policy et catalogs requis explicitement par get et factory, erreurs ValueError et RecursionError statiques avant write, globals int inchanges, processus unit int 640.
- Calcul producer avec vrais compteurs, mode, complete et versions source et mapping ; le stockage n est pas une preuve de completude, d autorisation, de limite d arret, de generation ou de gouvernance ; READ_RESULT exclus.
- Save insert-only sous alias explicite owner, atomique, forced insert, revalidation de __dict__ sans deferred, full_clean huit champs avec exclude, sans requete supplementaire ; get par identifiant technique borne, owned frozen, sans attestation de complétude ni autorisation.
- PK id technique BigAuto hors des huit, aucun Unique sur operation_id, aucune FK vers operation, aucun latest, update, CAS, nouveau format ref ou wire ; insert retourne l’identifiant technique ; get retourne les huit données figées ou None, jamais une attestation métier.
- Migration 0009 seule dependant de 0008, modeles avec import minimal, unit et integration PG sur onze tables preexistantes, forward et reverse, cotransaction isolee, multiple rapports pour meme operation autorise, mode/source_version/total_rows à None explicitement admis selon schéma, codecs, catalog, bornes, gels, cleanup des connexions, schema public stable.
- Exigences : bulk-operations B13 + ValidationReportV1, ProgressV1, RowDiagnosticV1, frontiere du contrat.
- Sources : src/pixs/backend/bulk_validation_report_record.py, src/pixs/backend/bulk_validation_report_repository.py, src/pixs/backend/migrations/0009_bulk_validation_report.py, src/pixs/backend/models.py, tests/unit/test_bulk_validation_report_persistence.py, tests/integration/test_bulk_validation_report_persistence_integration.py.
