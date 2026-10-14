## Why

Les validateurs mémoire Bulk et la persistance SQL/CAS/baux sont livrés séparément. Le runtime a maintenant besoin de contrats de données contrôlés et de ports composés côté serveur pour poursuivre les exigences Bulk déjà approuvées sans confondre références opaques, autorité et capacité technique.

## What Changes

- Ajouter des gardes internes des sept schémas AuthorityAssessmentV1, ServerContextRefsV1, MappingDescriptorV1, RowDiagnosticV1, CommandValidationV1, CommandExecutionV1 et JSONValueV1.
- Composer les interfaces et déclarations de ports serveur pertinentes, avec refus fermé de DENY, UNAVAILABLE, contexte invalide, mapping non résolu ou capacité absente.
- Vérifier types et structures avant parsing ou comportement, immuabilité des déclarations, absence de callback du payload et isolation des modules.
- Conserver les profils Kernel, les trois validateurs mémoire existants et la persistance déjà livrée sans modification.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- bulk-operations : implémentation partielle des contrats et frontières de B03, B05, B07 et B13 déjà validés ; exigences MODIFIED recopiées verbatim, aucune annexe ou règle ajoutée.

## Impact

Cinq nouveaux fichiers Python dans le backend et les tests, quatre artefacts de change. Aucun ORM/migration, provider de production, admission, worker, parseur effectif, idempotence/outbox SQL, route HTTP, PA/PZT, dépendance, Git ou déploiement. Les providers synthétiques prouvent seulement le périmètre interne. Le RUN reprend SÉLECTION après archive et rapport vérifiés.
