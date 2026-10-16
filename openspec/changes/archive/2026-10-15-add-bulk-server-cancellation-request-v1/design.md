# Design — add-bulk-server-cancellation-request-v1

## Context

La primitive `BulkRuntimeRepository.request_cancellation` existe, testée en CAS PostgreSQL, mais n'a aucun appelant serveur autorisé `CANCEL`. Le besoin est une façade serveur minimale qui pose une demande d'annulation coopérative B06 sous autorité B03, sans terminaliser l'opération, sans reprendre le worker et sans toucher aux ports, migrations ou cadrages existants.

## Goals / Non-Goals

Goals : exposer `request_bulk_cancellation` synchrone côté serveur ; vérifier les types exacts avant tout comportement et I/O ; contrôler l'autorité `CANCEL` courante sur l'opération cible avant la première requête SQL Bulk ; persister uniquement `cancellation_requested=True` et `revision N+1` via la primitive existante ; retourner soit la révision soit des diagnostics statiques sans valeur.

Non-Goals : aucune transition `CANCELLED`, aucun retry ou rebase CAS, aucune idempotence implicite nouvelle, aucun mapping, gouvernance, stockage, domaine ou wireformat nouveau, aucune modification du repository, des ports, des migrations, des cadrages ou des tests existants, aucun worker, dispatch, transport, route, APPLY ou EXPORT.

## Decisions

API interne : `request_bulk_cancellation(*, trusted_ports, runtime_repository, server_context, operation_id, expected_revision) -> tuple[int | None, list[Diagnostic]]` avec `resource_reference=None` explicite. Import inerte : sans Django, SQL, environnement, réseau ou processus à l'import, la dépendance ORM n'étant chargée qu'à l'appel si faisable.

Gardes : textes `str` exacts non vides UTF-8 sans NUL, `expected_revision` `int` exact compatible `N+1`, `bool`, sous-classes et objets hostiles refusés avant tout comportement, parsing, comparaison ou I/O. Identité exacte exigée : `type(trusted_ports) is _BulkTrustedPorts`, `type(runtime_repository) is BulkRuntimeRepository`, alias `using` `str` exact déclaré et vendor PostgreSQL réellement compatible. Aucun composant, provider ou callback fabriqué depuis le payload.

Autorité : `check_authority(server_context, action="CANCEL", operation_reference=operation_id, resource_reference=None)` avant toute requête Bulk. `DENY`, `UNAVAILABLE`, exception ou `ALLOW` malformé sont fermés sans contexte exploitable ni repli. Zéro SQL Bulk avant autorisation signifie seulement cela. Cible, tenant et scope viennent de l'autorité serveur ; aucune égalité inventée avec `requested_by` initial.

Gouvernance : cette demande de contrôle ne lit, ne transfère et ne mute aucune donnée métier, donc aucun nouvel appel mapping, gouvernance, stockage ou domaine. Une composition de production absente reste indisponible sans contournement.

Persistance : appeler uniquement `request_cancellation` existante ; transaction, verrous, CAS et terminalité inchangés. Succès : `(N+1, [])`. Échec : `(None, diagnostics statiques)`. Un flag déjà posé suit la primitive existante. `CasConflict`, `TransitionRefused`, `ValidationError`/`ConstraintRefused` et `DatabaseError` connus sont convertis sans détails SQL ; aucune capture n'invente un succès.

Fichiers : exactement `src/pixs/backend/bulk_server_cancellation.py`, `tests/unit/test_bulk_server_cancellation.py` et `tests/integration/test_bulk_server_cancellation_postgres_integration.py`.

## Validation

Unitaires : import et gardes hostiles sans I/O, appel autorité avec cible exacte, `DENY`/`UNAVAILABLE` avant SQL Bulk, capacité absente refusée. `py_compile` du module nouveau. PG réel isolé : seuls flag et révision changent, progression, échéance, checkpoint, Job et schedule inchangés, terminaux et CAS préservés, race à un seul gagnant, rollback externe, flag bloquant la prochaine unité sans annuler l'engagé, cleanup, tables publiques et connexions prouvés. Unitaires puis PG explicite ; régressions ciblées et validations combinées seulement sous exclusion propre. Strict ciblé zéro requis ; un global strict historique éventuel `exit 1` avec avertissements et zéro erreur est rapporté sans prétendre succès. Delta B06 original inchangé plus deux scénarios de preuve, tâches jamais cochées avant preuve, archive unique puis `STATISTIQUES.md` distinct.

## Risks / Trade-offs

Risque de contournement de l'autorité par un faux port : traité par identité exacte et refus avant SQL. Risque de fausse annulation : traité par retour de la seule révision persistée et aucun état terminal. Risque d'élargissement vers gouvernance ou mapping : exclu par conception, au prix d'une façade volontairement étroite sans nouvelle capacité.
