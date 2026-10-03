## Context

L'exigence API 2 et TECHNICAL.md §25 imposent data/meta/links et JSON UTF-8, sans exposition de modèles privés. La projection d'erreur, la réponse Django 500 et le runtime Django sont déjà disponibles. Aucun service ou endpoint n'est activé.

## Goals / Non-Goals

Goals : construire une enveloppe de succès publique isolée de ses entrées, puis une réponse JSON 200 conforme à cette seule forme.

Non-goals : schémas métier, filtrage universel de secrets, routes, serveur, tenant, autorisation, curseur, idempotence, cache, statuts 201/202/204, instrumentation, publication ou configuration de production.

## Decisions

- API : ApiSuccessEnvelopeError(ValueError), build_success_envelope(data, *, meta, links), build_success_response(data, *, meta, links). Les paramètres meta et links sont obligatoires, keyword-only et dictionnaires exacts.
- data accepte les valeurs JSON finies : None, bool, int, float fini, str, list et dict exacts ; les clés des dictionnaires sont str exactes. Refuser tout sous-type, objet personnalisé, modèle, datetime, UUID ou Decimal, sans conversion, repr, str ou inspection de ces objets.
- Copier profondément tous les conteneurs. Les alias acycliques sont acceptés et copiés indépendamment ; rejeter les cycles et les nombres NaN/inf. Le dépassement de la profondeur native Python produit la même erreur constante, sans nouvelle limite configurable.
- Diagnostics constants ApiSuccessEnvelopeError, sans écho de valeur, de clé ou de chemin interne ; suppression du contexte exposé par from None. La validation pure précède Django.
- Réponse JsonResponse non streaming, statut fixe 200, Content-Type application/json; charset=utf-8, ensure_ascii=False. Corps décodé égal à l'enveloppe pure.
- Imports Django locaux après validation, garde settings.configured et ImproperlyConfigured constant « Réglages Django non configurés. » si absent. Aucun configure, setup ou fallback dans la production. L'import de la façade reste sans Django.
- Ne modifier ni responses.py, errors.py ni Kernel. La copie profonde est un choix d'isolation d'implémentation, pas une citation normative nouvelle.
- Le contrat public du module appelant valide les données métier, leurs représentations et l'absence d'informations sensibles ; cette fondation ne remplace pas son schéma ou ses contrôles d'autorisation.

## Risks / Trade-offs

Le constructeur ne convertit pas automatiquement les dates, UUID ou décimaux : l'appelant transmet leur représentation publique préalablement validée. La fabrique ne publie aucun contrat OpenAPI et ne constitue aucune route opérationnelle. L'exigence API complète reste partiellement réalisée.

## Validation

Tests purs des types exacts, JSON fini, diagnostics sans écho, copie profonde, alias, cycles et profondeur ; import sans Django et validation avant import. Tests Django réels en sous-processus frais, réglages synthétiques DEFAULT_CHARSET seuls, texte Unicode et HTTP 200, gardes cinq connexions à zéro, apps.ready faux et parent préservé. Régressions unitaires et intégration séparées avec venv existant exécuté uniquement.

AST Python 3.11, UTF-8/LF, exemples, préfixes intacts et 24 références inchangées. Validation stricte à préparation, après preuves et après cochage. Archivage distinct --skip-specs après approbation CGPT, puis statistiques séparées. Pause à 16h30 Paris, sans clôture forcée si une preuve manque.
