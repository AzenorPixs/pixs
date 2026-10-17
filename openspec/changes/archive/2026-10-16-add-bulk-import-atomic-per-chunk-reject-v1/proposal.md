# Proposal — add-bulk-import-atomic-per-chunk-reject-v1

## Why
Le canon Bulk v1 prévoit des imports mutateurs, tandis que l’orchestration livrée couvre VALIDATE_ONLY et les demandes/transitions d’annulation. Ce premier sous-lot couvre uniquement IMPORT ATOMIC_PER_CHUNK avec REJECT, avec validation complète préalable et participation propriétaire PostgreSQL explicitement déclarée.

## What Changes
Ajouter une façade interne et sa composition serveur pour engager une unité par chunk, avec autorité/gouvernance courantes, idempotence, progression, checkpoint et outbox requise dans la même transaction PostgreSQL. Ajouter des tests de gardes et une preuve PostgreSQL réelle isolée. Le delta B07 conserve ses quatre scénarios existants et ajoute une preuve du sous-lot.

Ce change ne couvre pas ATOMIC, BEST_EFFORT, CREATE_ONLY/UPDATE_ONLY/UPSERT, EXPORT, HTTP, worker, provider de production, migration, dépendance, configuration persistante ou Git. Les contrats et profils préparatoires existants restent inchangés.
