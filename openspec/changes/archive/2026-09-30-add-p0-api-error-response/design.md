## Context

TECHNICAL.md §25 et openspec/specs/api/spec.md requirement 2 exigent des erreurs normalisées sans détail privé. La projection publique build_infrastructure_error et Django 5.2.17 existent ; la disponibilité effective d'un service reste non prouvée.

## Goals / Non-Goals

Goals : construire une réponse JSON Django d'infrastructure à partir de la seule interface publique existante ; préserver l'import pur et les réglages de l'appelant.

Non-goals : routes, serveur, middleware, activation, identité, tenant, HTTP de succès, pagination, idempotence, classification d'exception, instrumentation, header de corrélation, stockage, schéma ou publication.

## Decisions

- API : build_infrastructure_response(correlation_id, *, internal_error). Aucun paramètre de statut, de header ou de réglage.
- Appeler build_infrastructure_error avant tout import Django. UUID et objet interne opaque sont exclusivement traités par la projection existante ; aucune conversion, inspection ou capture supplémentaire.
- Import local de django.http.JsonResponse dans la fabrique. L'import du module et de la façade n'importe ni Django ni ses réglages, et ne lit aucun environnement.
- Réponse non streaming ; statut fixe 500 pour erreur serveur inattendue ; Content-Type exact application/json; charset=utf-8. Le corps décodé est égal à la projection publique.
- Ne pas appeler settings.configure, django.setup ni créer de fallback dans le code de production. Des réglages Django déjà configurés sont une précondition de l'appel ; les erreurs natives éventuelles sont propagées sans être sérialisées.
- Aucune règle de cache ou de route inventée. La version de l'enveloppe existante n'est ni changée ni ajoutée au corps.
- Façade et README ajoutés à la fin, en conservant intégralement leurs préfixes existants.

## Risks / Trade-offs

Cette fabrique n'intercepte aucune exception et ne relie pas encore une requête à une trace. Elle ne constitue ni une route publique ni une preuve de conformité API complète. Le choix HTTP 500 ne classe pas les erreurs métier.

## Validation

Tests unitaires de délégation, imports paresseux, UUID invalides et erreurs internes hostiles. Tests d'intégration avec Django réel installé dans le venv existant exécuté uniquement, en sous-processus frais ; configuration synthétique DEFAULT_CHARSET seule, sans secret ou base réels, sans altération des réglages du parent. Gardes explicites contre sockets et accès PostgreSQL. Régressions unitaires et d'intégration lancées séparément.

Contrôle AST Python 3.11, UTF-8/LF, exemples, dix fichiers, préfixes intacts, exigences canoniques et cadrages inchangés. Validation stricte à la préparation, après preuves et après cochage. Archivage distinct --skip-specs après approbation explicite CGPT, puis statistiques hors intervalle.
