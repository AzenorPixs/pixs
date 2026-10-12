## Context
B01-B14 et leurs annexes sont approuvés. Le change de validation mémoire est archivé avec rapport. Ce lot implémente la persistance du runtime et ses primitives transactionnelles internes ; il ne constitue pas encore le runtime Bulk complet.

## Goals / Non-Goals
Quatre modèles : extension 27 champs liée un-à-un au Record existant, checkpoint 9 clés, binding Job 3 clés et schedule 7 clés. Les clés physiques/FK sont des choix internes, sans nouvelle donnée logique. Aucune valeur numérique, date automatique ou valeur métier par défaut.
Un repository interne contrôle révisions, transitions fermées, checkpoints atomiques et baux selon politique serveur explicite. Aucun port d'autorité, commande propriétaire ou production complète n'est annoncé par ces primitives. Aucune création/dérivation supplémentaire du payload ou de la causalité Job ; les Jobs existants sont fournis explicitement.

## Decisions
Conserver intégralement les modèles préparatoires, leurs neuf/treize champs et exports. models.py reçoit uniquement l'import de registration des nouveaux modèles. related_name="+" préserve les métadonnées existantes ; PROTECT empêche les orphelins comme garde technique, sans introduire une API de suppression.
Valider dict, clés et valeurs exactes avant parsing ou I/O ; refuser sans écho de valeur. Réutiliser les validateurs mémoire et parse_version. Un décodage ORM de confiance restitue des datetime exacts timezone.utc ; une entrée étrangère ne bénéficie pas de ce décodage.
Révision opération CAS, transition B06 exacte et aucun arc sortant terminal. L'évolution de progression et le checkpoint s'engagent dans la même transaction ; conflit ou rollback ne laissent aucune trace partielle.
Le bail reste dans les champs JobRecord existants. La révision du schedule et les verrous transactionnels du Job/opération protègent acquisition, renouvellement, libération et exclusion des phases. Perte/expiration interdit une nouvelle unité ; reprise conserve checkpoint/progression et expires_at. Délais et limites viennent exclusivement de PolicyV1 explicitement fournie.
Les limites techniques PostgreSQL ne redéfinissent pas les types logiques int des validateurs mémoire ; une capacité non supportée est refusée explicitement avant écriture, sans fallback.

## Validation
Syntaxe des six Python, tests offline sous gardes positives et PG isolés. Prouver PK/FK/unicités, types hostiles, UTC, CAS concurrents, un seul titulaire de bail, expiry/perte/reprise, rollback de checkpoint, transitions terminales et invariants de schedule.
Exécuter les 202 régressions existantes selon groupes exacts, sans mélange avec les nouveaux tests. Les scénarios PG chargent les secrets uniquement dans leur processus sensible, jamais dans prompts/sorties. Forward/reverse 0004 seul, tables0001-0003 stables, schéma supprimé et connexions fermées.
Strict change avant/après, global qualifié par exactement trois WARNING historiques et aucune nouvelle issue ; UTF8/LF, fichiers attendus seuls. Archivage unique --skip-specs car deltas MODIFIED verbatim, puis STATISTIQUES distinct à six sections.

## Risks / Trade-offs
Une primitive persistante n'est ni admission ni autorisation ni preuve d'effet métier. Les providers synthétiques et tests PG ne prouvent pas une composition de production. Les refus de capacité, de révision, de bail et de transition restent explicites.

## Rollback
Migration 0004 réversible dans le schéma de test autorisé. Aucune suppression de code, donnée de production ou migration antérieure.
