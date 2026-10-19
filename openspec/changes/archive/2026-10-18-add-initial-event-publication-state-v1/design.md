# Conception du vocabulaire initial de publication

## Référentiel

`openspec/specs/events/spec.md`, B11 et `OutboxPublicationV1`, fixent les cinq états. Les garanties après commit, au moins une fois, de bail, de réessai et d’ordre restent inchangées. `RETRYING` exige `next_attempt_at` et `PUBLISHED` exige `published_at` dans leurs contrats existants ; le présent vocabulaire ne les vérifie pas.

## Implémentation minimale

`src/pixs/backend/event_publication_state.py` définit uniquement `EventPublicationState(Enum)` et `__all__ = ["EventPublicationState"]`. Noms et valeurs : `PENDING`, `PUBLISHED`, `RETRYING`, `FAILED`, `DEAD_LETTER`, dans cet ordre, sans alias ni normalisation. Le patron est celui de `StartupMode`. Le module appartient au backend car B11 exclut la responsabilité de l’outbox du Kernel. Aucune façade, représentation Bulk ou validation existante n’est modifiée.

## Validation

Tests unitaires : noms, valeurs, ordre, Enum sans mixin `str`, export explicite et refus des valeurs non déclarées sans normalisation. Intégration : import frais `-I -B` dans un environnement synthétique minimal, gardes d’écriture, réseau, processus, environnement et base, contrôles positifs des gardes et façade backend inchangée. Compiler séparément les trois fichiers, exécuter les tests du vocabulaire et les régressions backend pertinentes, contrôler UTF-8/LF et les empreintes des canons/cadrages. Rapporter séparément la validation OpenSpec ciblée stricte, globale standard et globale stricte, avec leurs codes natifs et avertissements exacts.

## Limites et retour

Aucune transition, persistance, transaction, publication, séquence, bail, politique de réessai, lettre morte opérationnelle, webhook, ordre effectif, interface, installation ou sélection de provider. Aucun delta normatif. Les fichiers nouveaux peuvent faire l’objet d’un retrait séparément autorisé ; aucun fichier existant n’est à rétablir.
