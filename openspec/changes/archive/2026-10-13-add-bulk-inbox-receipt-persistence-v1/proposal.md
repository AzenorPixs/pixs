# Proposal add-bulk-inbox-receipt-persistence-v1

## Why

Le runtime Bulk v1 a besoin d'une persistance interne append-only des accusés de réception pour empêcher un second effet confirmé lors d'une livraison répétée, sans présenter un état comme preuve avant commit propriétaire. Aucune primitive de persistance InboxReceiptV1 n’a été observée dans le périmètre ciblé ; les valeurs pures existantes ne constituent pas une consommation effective. Cette proposition couvre uniquement l'enregistrement, le refus déterministe des doublons et divergences, et la co-transaction avec le propriétaire, sans receiver, sans publication et sans effet externe.

## What Changes

Créer un enregistrement InboxReceiptV1 à huit clés logiques explicites avec clé primaire locale technique hors décompte, contrainte d'unicité sur le couple consumer/event, état unique CONSUMED, fabrique pure sans entrée-sortie, méthodes modèle insert-only avec alias explicite sous transaction active, dépôt limité à insert et get avec gestion exacte de la contrainte d'unicité 23505 par savepoint privé de lecture, comparaison conjointe version ET empreinte avec refus statiques Duplicate et Divergence, préservation des originaux sans écrasement, annulation propriétaire même après capture, propagation des autres erreurs de base, migration 0008 réversible dépendante de 0007, tests unitaires et d'intégration PostgreSQL isolés, sans foreign key locale vers envelope et sans ack avant commit.

## Périmètre

Inclus : events B11 et InboxReceiptV1, frontière du contrat bulk-operations, six sources validées (record, repository, migration 0008, models, test unitaire, test intégration), fabrique pure existante à préserver, modèles Envelope et CommandIdempotency en lecture seule comme référence.

## Validation

Validation par tests unitaires insert/get, refus Duplicate à l'identique et Divergence sur version ou empreinte différente, co-transaction propriétaire avec rollback sans publication, course avec deux bloqués et un seul gagnant, consommateur indépendant isolé, vol en cours non accusé, migration seule avec dix tables stables, nettoyage connexions et schéma public, régressions pertinentes.

## Exclusions

Exclus : receiver, provider, authority, catalogue, callback, trust bool, hash et serializer nouveaux ; Outbox, publisher, séquence, bail et effets externes ; toute mutation des modules purs, du runtime, de CommandIdempotency et EventEnvelope existants ; frontend, Git, secrets, infra, norme nouvelle, B11 global complet.
