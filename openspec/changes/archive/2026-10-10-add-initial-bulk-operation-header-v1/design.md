# Design — add-initial-bulk-operation-header-v1

## Représentation interne

`@dataclass(frozen=True)` BulkOperationHeader avec exactement `operation_id: str`,
`bulk_type: BulkOperationVariant`, `bulk_version: str`, dans cet ordre.
Trois arguments obligatoires, aucun défaut, aucun `__post_init__`, aucune méthode ajoutée.
`__all__ = ["BulkOperationHeader", "validate_bulk_operation_header"]`.
Les façades et modules existants restent inchangés.

## Validation pure

`validate_bulk_operation_header(candidate: object) -> list[Diagnostic]` rejette le
type étranger ou sous-classé avant tout accès à un attribut. Pour un candidat exact,
les champs manquants sont refusés sans valeur de repli de données.

`operation_id` exige une str exacte non vide, opaque et conservée sans normalisation.
`bulk_type` exige un membre de type exact BulkOperationVariant, sans conversion.
`bulk_version` exige une str exacte puis une forme SemVer 2.0.0 complète, en réutilisant
`pixs.kernel.manifest.semver.parse_version`. Seul ValueError est capturé et transformé
en diagnostic statique ; la version initiale est conservée sans compatibilité évaluée.
Tous les types sont contrôlés avant comparaison ou parsing, sans invocation de hook étranger.

Les diagnostics VALIDATE sont statiques, triés et dédupliqués par
`(element, constraint, message)`, rendus sans valeur candidate. Chaque appel rend
une liste indépendante. Aucun I/O, environnement, réseau, processus, DB ou autre effet.
Le profil ne remplace pas les exigences générales BulkOperation.

## Vérifications

Tests unitaires comportementaux : conservation opaque, variantes admises,
versions complètes avec préversion/build, refus des formes/types interdits,
objets/sous-classes à hooks, immuabilité et champs obligatoires, diagnostics sans écho.
Intégration fraîche `-I -B`, environnement figé, timeout borné, artefacts temporaires
dans la racine projet uniquement ; gardes d'effets avec contrôles positifs.
Trois compilations séparées ; tests ciblés ; régressions du parseur SemVer,
du profil BulkJobLink, de la pureté et des façades du noyau.
Validation OpenSpec avant/après code, aucune ERROR ; avertissements de longueur
qualifiés sans réécriture du canon. Archivage et STATISTIQUES.md sont des mandats distincts.
