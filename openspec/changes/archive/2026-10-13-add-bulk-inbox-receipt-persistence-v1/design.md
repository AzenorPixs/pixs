# Design — add-bulk-inbox-receipt-persistence-v1

## Fondation partielle et données

Huit clés logiques canoniques, toutes explicitement requises, sans défaut :
- consumer_reference : str déclarée, clé composée avec event_id.
- event_id : str opaque, pas de FK vers une enveloppe locale ni existence inventée.
- event_version : str SemVer, version traitée prévalidée par le producteur serveur.
- content_sha256 : hex minuscule de 64 caractères, empreinte prévalidée ; divergence même clé refusée.
- state : CONSUMED seul, construit explicitement ; jamais preuve avant commit.
- consumed_at : datetime exact aware timezone.utc, écrit dans la même transaction que les effets.
- correlation_id : str opaque obligatoire.
- causation_id : str opaque ou None explicitement fourni.

PK locale id BigAutoField technique hors huit clés, UniqueConstraint(consumer_reference,event_id).
Les captures/exportations n’exposent que les huit valeurs ; aucune clé owner_ref, event_type, consumer, event_sha, status ou received_at_utc.
Références de consommateur, version et empreinte sont des préconditions d’un appelant serveur de confiance, sans nouvelle autorité, attestation booléenne, catalogue, calcul de hash ou sérialisation publique.

## Modèle et copies

Réutiliser validate/capture_bulk_inbox_receipt_values existants, jamais les modifier.
from_values valide et capture owned avant construction, sans sauvegarde ; cls/sous-classes/valeurs hostiles refusés avant callbacks.
as_values lit les huit attributs courants sans chargement différé et retourne une copie owned ; snapshot figé issu de la capture existante.
full_clean contrôle tout même avec exclude, sans requête de validation SQL ; erreurs statiques sans écho.
save surchargé insert-only, force_insert True, force_update False, update_fields None, alias str exact explicite et transaction active sur cet alias après validation avant ORM.
Une instance hydratée ou déjà sauvegardée ne peut pas être mise à jour ; QuerySet/rawSQL hors primitive, aucune immutabilité globale DB inventée.
SQL : non-vacuité, SHA64 et état CONSUMED, nullabilité déclarée, unicité de la clé composée. UTC/SemVer contrôlés applicativement.

## Dépôt et frontière transactionnelle

insert/get seuls, même alias validé avant I/O, get retourne capture figée owned ou None ; aucune réponse n’atteste un commit.
insert exige une transaction propriétaire active. atomic(savepoint=False) rejoint cette transaction.
Un savepoint privé ENTOURE l’INSERT : en cas de 23505, ce savepoint est d’abord annulé pour permettre de lire l’existant dans la frontière propriétaire.
Seule la contrainte consumer_reference/event_id au nom EXACT connu sous SQLSTATE23505 est reconnue.
Comparer event_version ET content_sha256 de l’entrée validée et de l’existant :
identiques -> refus Duplicate statique ; différence de version ou empreinte -> refus Divergence statique.
Dans les deux cas, aucun écrasement ni second effet confirmé, originaux correlation_id/causation_id/consumed_at conservés et transaction propriétaire marquée rollback même si le refus est capturé.
Les autres erreurs de base sont propagées sans masque et la frontière transactionnelle garde leur rollback.
Pas de replay avec effet, pas d’AlreadyConsumed ni ack ; une ligne CONSUMED peut encore être inflight dans la transaction de son propre appelant.

## Sources et validation

Six sources : bulk_inbox_receipt_record.py, bulk_inbox_receipt_repository.py, migration0008_bulk_inbox_receipt.py dépendant de0007_bulk_event_envelope, import minimal models.py, unittest offline et harness PostgreSQL isolé.
Migration réversible, une seule création de table, aucun changement des dix tables préexistantes.
Unit : véritables gardes d’import/I/O, types hostiles/no-écho, captures/exports/gels, métadonnées/migration sans DB ; ne pas simuler la preuve SQL du duplicata.
PG réel : version ET empreinte, consumer indépendant, refus capturé rollback owner, race deux workers réellement bloqués puis un seul gagnant, copies et visibilité inflight non assimilée à un ack.
Prouver co-commit/co-rollback avec effet propriétaire synthétique ET création d’un JobRecord existant dans la même source persistante, sans modifier son modèle ni exécuter un worker.
Nettoyage owned, connexions fermées, public et dix tables stables, forward/reverse0008 seule, régressions pertinentes, strict ciblé et global qualifié.
Aucun receiver/provider/autorité/catalogue/callback nouveau, Outbox/publisher/séquence/bail, effet externe, frontend, Git, secret, infrastructure ou norme ; B11 global reste incomplet.
