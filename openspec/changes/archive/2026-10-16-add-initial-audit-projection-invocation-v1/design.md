## Context

La référence 27 contient les neuf exigences et onze scénarios du contrat d'invocation. AuditDecisionProjectionV1 et son validateur public restent purs ; AuditSink.record reçoit l'événement PDP, intentionnellement distinct de l'événement générique. Ce change ajoute une opération séparée et conserve ces formats et leurs producteurs.

## Goals / Non-Goals

Implémenter exactement invoke_audit_projection avec un bool exact et une invocation bornée du port. Ne pas produire de preuve de persistance, de conformité P0, d'accès autorisé, de fraîcheur ou de déduplication globale. Ne pas modifier authorize, plan_filter, leurs signatures, les obligations, les exceptions Super Admin ou les façades existantes.

## Decisions

1. Un nouveau module Core/authz expose localement invoke_audit_projection ; aucune dépendance nouvelle ni modification d'un module existant.
2. Le validateur public est appelé sur la même projection avant tout accès au port. Des diagnostics donnent False ; une exception inattendue du validateur se propage hors du bloc de traitement du port.
3. Une projection valide transmet son decision_event original à sink.record exactement une fois, sans copie, conversion ni enregistrement de l'événement générique.
4. Seul un retour is True donne True. Aucun bool, égalité ou autre callback du retour n'est évalué. Toute autre valeur donne False.
5. La frontière explicitement spécifiée du port convertit ses exceptions ordinaires en False sans écho ni retry ; BaseException directe se propage. Le traitement d'Exception est limité à cette frontière et ne masque pas les erreurs du validateur.
6. Deux invocations explicites conduisent à deux appels distincts ; aucun état de déduplication, horloge, environnement, accès ressource, stockage ou intégration automatique n'est ajouté.
7. Les tests couvrent des ports mémoire, les types hostiles, les erreurs de validation et du port, l'identité des objets et les quatre combinaisons ALLOW/DENY et TENANT/PLATFORM. L'intégration fraîche calibre des gardes contre IO, réseau, sous-processus, environnement, horloge et imports Django/PostgreSQL.

## Risks / Trade-offs

- Le retour True constate uniquement la valeur du port fourni ; il ne prouve pas une persistance, même si le nom du port évoque l'audit.
- Le port est fourni explicitement par un appelant backend de confiance ; aucune découverte ou configuration de provider n'est ajoutée.
- Les exceptions ordinaires du port donnent un résultat False contractuel, sans exposer leur contenu ; les erreurs de validation et interruptions ne sont pas étouffées.
- Les quatre avertissements stricts globaux de longueur préexistants restent hors périmètre, avec exit natif 1 explicitement conservé.

## Migration Plan

Aucune migration. Créer les trois nouveaux fichiers, exécuter py_compile sur chacun, les tests dédiés, l'intégration fraîche et les régressions audit/authz pertinentes. Vérifier les deltas verbatim, la cohérence des cadrages, UTF-8/LF et le périmètre exact. Cocher uniquement après preuves. Sous exclusion de cohorte stable, revalider puis archiver avec --skip-specs, car les canons sont déjà identiques aux deltas. Libérer l'exclusion après publication avant le rapport. Publier STATISTIQUES.md par un mandat distinct et vérifier ses six sections et totaux avant gate et arrêt C3.

## Open Questions

Aucune décision normative nouvelle. La validation humaine RSMP et la condition d'arrêt après la prochaine archive et ses statistiques sont conservées dans le checkpoint parent.
