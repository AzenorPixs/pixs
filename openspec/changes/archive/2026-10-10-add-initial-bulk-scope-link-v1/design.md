## Context

BulkScopeLink v1 est un profil interne préparatoire validé, distinct du contexte concret ScopeContext et des garanties d'exécution bulk. Les profils voisins BulkJobLink et BulkOperationStatus fournissent les conventions de représentation et de diagnostics; leur règle de distinction éventuelle ne s'applique pas à BulkScopeLink.

## Goals / Non-Goals

Goals : conserver exactement operation_id et scope_context_reference, rendre leur fourniture obligatoire, utiliser une dataclass gelée, refuser les structures interdites sans effet ni écho.

Non-Goals : résolution, existence, rattachement réel, cohérence tenant/scope, autorisation, propagation, persistance, contexte PLATFORM implicite, tenant global, import concret pixs.core ou runtime bulk.

## Decisions

1. Module interne bulk_scope_link.py avec BulkScopeLink et validate_bulk_scope_link, sans export ni modification d'un registre existant.
2. Contrôler type(candidate) is BulkScopeLink avant tout attribut. Lire les deux champs avec un sentinelle d'absence interne, puis contrôler type(value) is str avant toute opération sur la valeur. Une chaîne exacte non vide est acceptée telle quelle, espaces compris; les références égales sont acceptées sans comparaison métier.
3. Construire uniquement des Diagnostic VALIDATE à partir de noms de champs et messages statiques; trier et dédupliquer leurs clés statiques, renvoyer une liste indépendante à chaque appel.
4. Tests unitaires couvrant fourniture obligatoire, immutabilité, valeurs opaques conservées, égalité admise, types exacts, champs absents, objets hostiles et sous-types refusés avant attributs, diagnostics sans écho et déterministes.
5. Test d'intégration dans un processus Python frais avec environnement minimal, timeout et gardes à contrôles positifs sur fichiers, réseau, processus, environnement, base de données et import concret pixs.core. Les limites de ces surfaces surveillées restent explicites.

## Risks / Trade-offs

Le profil n'établit aucune identité, cohérence ni association réelle de contexte. Une validation structurelle ne donne aucun droit. Les diagnostics n'incluent pas les valeurs reçues. Les outils et dépendances existants suffisent; la compatibilité Python >=3.12 est conservée.

## Migration Plan

Aucune migration, configuration ou activation runtime. L'archivage est distinct et autorisé seulement après preuves. Le delta reproduit les exigences canoniques à l'identique; --skip-specs évite de réappliquer une norme déjà présente après contrôle de cette identité. STATISTIQUES.md est produit ensuite sous mandat distinct.
