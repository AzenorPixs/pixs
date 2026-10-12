## Context

La source normative reste openspec/specs/bulk-operations/spec.md (B03/B05/B07/B13, annexes et ports déclarés), openspec/specs/events/spec.md (JSONValueV1), authorization et initial-administration. Les archives de validation mémoire et de persistance Bulk sont livrées ; leurs sources et preuves PostgreSQL sont préservées par empreinte, sans replay de test PG pour ce lot sans ORM.

## Goals / Non-Goals

Implémenter les contrats internes et la composition de confiance nécessaires au runtime. Ce lot ne réalise pas une admission, une unité mutatrice propriétaire, un worker, une publication ou un provider de production. Les références ne prouvent aucune existence ou autorisation et une dérogation applicative ne fabrique pas une capacité technique.

## Decisions

- Les entrées logiques conservent exactement les clés et types des annexes ; aucune valeur omise, défaut, coercition ou nouveau wire format. Des snapshots privés figés peuvent porter les données après validation, sans devenir un type d'entrée implicite.
- Toutes clés puis valeurs/structures imbriquées sont gardées avant SemVer, hashing, comparaison étrangère ou I/O. Réutiliser Diagnostic/VALIDATE, parse_version et validate_bulk_policy_values sans modifier les exports existants. Les diagnostics restent statiques et minimisés.
- Les références opaques runtime sont des str exactes non vides UTF-8 sans NUL. JSONValueV1 conserve ses types propres : chaînes Unicode valides y compris chaîne vide et NUL, nombres finis, conteneurs exacts ; cycles refusés, partage acyclique permis, limites serveur explicites. Les doublons de clés ne sont prouvables qu'au parsing, hors de ce lot.
- MappingDescriptorV1 conserve l'ordre et l'unicité expressément déclarée de source_fields, target_fields et required_source_fields ; field_bindings respecte la bijection déclarée. Aucune cardinalité minimale ou unicité supplémentaire des event_references. Les valeurs variant/format sont des str exactes égales aux Enum.value canoniques.
- RowDiagnosticV1 n'accepte que codes et champs déclarés côté serveur, avec position positive ou None ; CommandValidationV1 contrôle accepted si et seulement si diagnostics vide. CommandExecutionV1 n'ajoute pas de couplage outcome/diagnostics absent du canon. Les bornes viennent d'une PolicyV1 explicite.
- Les composants de ports sont déclarés et composés côté serveur ; aucun import dynamique, expression, provider, credential ou callback issu du payload. Réutiliser les registres Kernel si leur contrat applicable compose déjà ces ports ; sinon garder la composition spécifique backend isolée, sans modifier Kernel.
- AuthorityPort délègue les exceptions canoniques à l'autorité serveur et contrôle ses réponses. AuthorityAssessmentV1 ALLOW Bulk exige contexte valide et tenant non None ; DENY/UNAVAILABLE n'offrent aucun contexte exploitable. ServerContextRefsV1 générique peut porter tenant None sans activer Bulk plateforme.
- MappingPort.resolve conserve les trois arguments canoniques (mapping_reference, mapping_version, owner_reference), vérifie le descriptor restitué et son immuabilité selon son identité déclarée. Aucune nouvelle règle globale de namespace entre propriétaires.
- Les ports owner/projection/audit sont des contrats composés et contrôlés ; aucun appel owner mutateur ni audit prétendument réalisé dans ce lot. Les providers réels et garanties transactionnelles restent indisponibles tant qu'ils ne sont pas composés et prouvés.

## Validation

Compiler les cinq nouveaux Python ; tests unitaires des frontières, hostiles, immuabilité et refus de confiance ; processus frais sous gardes positives pour fichiers/réseau/processus/base/Core concret ; régressions des 31 modules existants, total204, regroupables dans une invocation unittest unique si longueur CAB <=2000. Pas de nouveau test PG réel car sources ORM/migrations inchangées, preuve précédente qualifiée par hash. Strict du change sans issue ; strict global qualifié seulement par les trois WARNING historiques exacts et aucune nouvelle issue. UTF-8/LF, périmètre et empreintes vérifiés. Archive unique --skip-specs puis STATISTIQUES sous mandat distinct, avant retour SÉLECTION.

## Risks and Limits

Les providers synthétiques ne prouvent pas une composition de production. Une réponse mal formée ou indisponible n'est pas transformée en ALLOW ; les erreurs de capacité et les données étrangères sont refusées sans écho. Les limites et signatures internes ne doivent pas étendre le schéma ni ajouter de sémantique normative.
