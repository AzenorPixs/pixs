## Why

La RSMP validée et publiée en référence 27 définit invoke_audit_projection. Le contrôle structurel AuditDecisionProjectionV1 existe, mais aucune opération distincte ne valide la projection avant d'invoquer le port PDP fourni. Ce change implémente uniquement ce contrat borné, sans assimiler un retour True à une preuve d'audit persistant ou d'accès autorisé.

## What Changes

- Créer un module Core/authz avec invoke_audit_projection(projection, sink).
- Réutiliser le validateur public de projection avant tout accès au port ; conserver l'événement PDP original par identité.
- Reconnaître seulement True exact et couvrir les erreurs du port, la propagation des interruptions et l'absence de relance.
- Ajouter des tests unitaires et une intégration en processus frais sous gardes.
- Reprendre mot pour mot les neuf exigences et leurs onze scénarios canoniques dans les deux deltas.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- authorization-engine : implémenter l'invocation bornée du port déjà spécifiée.
- audit : prouver la portée limitée et les exclusions déjà spécifiées.

## Impact

Trois nouveaux fichiers Python : src/pixs/core/authz/audit_projection_invocation.py, tests/unit/test_audit_projection_invocation.py et tests/integration/test_audit_projection_invocation_integration.py. Aucun module ou façade existant, contrat PDP, validateur, Kernel, stockage, provider, politique, privilège, Bulk, notification, Frontend ou schéma de manifeste n'est modifié. Python >=3.12 et les dépendances actuelles sont conservés. Le seul effet explicite est l'appel unique du port fourni après validation ; aucun backend réel, accès ressource, horloge, SQL ou IO autonome n'est introduit. Aucune base PostgreSQL ni aucun navigateur n'est nécessaire. Après validations, archivage unique puis STATISTIQUES.md distinct et arrêt ciblé CISMP3 demandé ; aucune sélection suivante, aucun Git.
