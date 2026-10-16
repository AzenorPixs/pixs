## Why

La norme AuditDecisionProjectionV1 est validée et publiée dans la référence commune 22 par le RSMP approuvé. Les événements PDP et audit générique existent, mais leur contrôle explicite de correspondance n'est pas implémenté. Ce lot apporte uniquement le profil préparatoire purement mémoire et ses preuves, sans prétendre réaliser un audit persistant.

## What Changes

- Créer AuditDecisionProjectionV1 et son validateur dans un nouveau module Core/authz.
- Réutiliser les deux événements existants et leurs validateurs publics, sans copier ni fabriquer de données.
- Couvrir les correspondances, refus, types hostiles, métadonnées et limites par tests unitaires et intégration fraîche sans IO.
- Conserver les normes et les anciens contrats ; les deltas reprennent les exigences canoniques mot pour mot.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- authorization-engine : implémenter le profil AuditDecisionProjectionV1 déjà spécifié.
- audit : prouver sa portée préparatoire et ses limites déjà spécifiées.

## Impact

Trois nouveaux fichiers seulement : src/pixs/core/authz/audit_decision_projection.py, tests/unit/test_audit_decision_projection.py et tests/integration/test_audit_decision_projection_integration.py. Aucun ancien module, façade, contrat PDP/PEP, stockage, provider, privilège, Bulk, Frontend, EventRegistry, schéma de manifeste, dépendance ou configuration n'est modifié. Python >=3.12 est préservé. Aucun IO, horloge, audit durable ou P0 n'est introduit. Pas de PostgreSQL nécessaire à ce profil pur. Après preuves et intégration coordonnée, archivage unique puis STATISTIQUES.md distinct ; aucun Git.
