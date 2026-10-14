# Design — VALIDATE IMPORT VALIDATE_ONLY (parcours unique)

## Context

Les briques B01, B04, B05, B06, B07 VALIDATE_ONLY et B13 existent. `B04`
qualifie le storage, vérifie le flux complet et retourne un bilan hash-only
sans octets. Les parseurs B05 sont mécaniques. Le repository impose CAS,
baux, checkpoints et transitions. L'objectif est de composer la seule phase
VALIDATE sans worker, sans APPLY ni EXPORT.

## Goals

- Un seul parcours storage qualifié, même liaison provider capturée du
  début à la fin ; aucun transfert de preuve entre deux qualifications.
- Factorisation privée minimale de `bulk_private_object_reader.py`,
  API `read_private_object_once` inchangée (hash-only, aucun contenu
  restitué par cette API).
- Parser mécanique exact interne sans callback du payload ; tampon logique
  d'unités typées éphémère, borné par les limites existantes de la PolicyV1
  résolue uniquement, effacé sur toute sortie.
- Aucun `owner.validate` ni `canonical_bytes` avant SHA-256 complet,
  métadonnées finales identiques et fermeture réussie.
- `owner.validate` réel sous contrat serveur composé, `CommandValidationV1`
  profondément gardé ; `execute` jamais.
- Mode `VALIDATE_ONLY` et références lus et recroisés au persistant ;
  phase `VALIDATE` fixée en interne.
- Fournisseur async et owner bornés sans transaction ouverte ; ORM via
  `sync_to_async` thread-sensitive, unité protégée créée et utilisée dans
  la même transaction et le même thread.
- Préconditions : opération `STAGED` ou `VALIDATING`, Job `VALIDATE`
  serveur déjà déclaré ; pas de création de phase ou Job suivante.
- Sous gardes actuelles seulement : rapport, progression et checkpoint
  final unique atomiques, checkpoint en révision N+1 puis transition en
  N+2, compteurs `applied`, `execution_rejected` et `exported` à zéro, sans
  checkpoint de mutation ni reprise intra-phase inventée.

## Non-Goals

- Worker, APPLY (`ATOMIC`, `ATOMIC_PER_CHUNK`, `BEST_EFFORT`), EXPORT,
  routes, provider de production, migration, seuil, dépendance,
  documentation, Git.
- Reprise intra-validation, renouvellement de bail, retry nouveau,
  reconstitution d'autorité depuis un checkpoint.

## Decisions

1. Parcours qualifié unique avec liaison conservée : `qualify`,
   `stat_private` avant et après, `iter_bytes`, vérificateur incrémental,
   contrôles d'autorité `EXECUTE` et de gouvernance `RESOLVED` actuels,
   deadline effective, annulation et fermetures bornées identiques à B04.
2. Parsing mécanique interne : chaque chunk borné alimente d'abord le
   vérificateur puis le parser ; les unités logiques restent en mémoire
   éphémère bornée (`max_input_bytes`, `max_rows`, `max_row_bytes`,
   `max_columns`, `max_json_depth`, `max_json_members`, `max_diagnostics`),
   sans copie complète des octets, fichier, spool ni backup local.
3. Owner après intégrité complète seulement : soumission des unités
   tamponnées à `validate` après `finish` positif et fermeture réussie ;
   capacités async incompatibles refusées ; diagnostics statiques sans
   valeurs ni secrets ; accès au rapport réautorisé.
4. Persistance nominale atomique unique : `protected_unit` VALIDATE,
   `commit_checkpoint` N+1, `insert_report`, `apply_transition` N+2 vers
   `COMPLETED`, `COMPLETED_WITH_ERRORS` ou `FAILED` ; rejets d'examen
   complet distingués des arrêts incomplets ou techniques.
5. Correction impérative : après annulation, expiration ou perte de bail,
   aucune transaction ordinaire contournant `protected_unit`, bail,
   fencing ou CAS ; refus explicite sans persistance forcée, sans fausse
   terminalité, sans checkpoint d'autorité et sans faux succès.
6. Primitives manquantes éventuelles implémentées au strict nécessaire
   dans la norme existante, sans extension normative.

## Validation

- Tests PostgreSQL isolés : gardes nominales, refus, non-fuite,
  rollback, CAS, concurrence, bail, replay terminal, régressions B04,
  trusted ports, parser et repositories.
- Syntaxe des fichiers modifiés, périmètre strict du change et
  combinaison globale sous intégration.
- Cibles exactes : cinq fichiers Python maximum déjà réservés, sans
  migration, seuil, dépendance, documentation ni Git.

## Risks / Limits

- Bail perdu ou opération expirée ou annulée : aucun rapport forcé ;
  état explicite à réconcilier par l'orchestrateur.
- Limite PolicyV1 atteinte ou flux divergent : bilan incomplet explicite,
  jamais présenté comme validation complète.
- Fournisseur incompatible ou owner indisponible : refus technique fermé,
  sans repli vers un autre mode.
