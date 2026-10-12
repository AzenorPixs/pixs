## Why

Les contrats runtime Bulk, la composition serveur et les primitives SQL/CAS/baux sont livrés séparément. Le runtime IMPORT a maintenant besoin d'un parsing CSV/NDJSON incrémental borné et d'un mapping exact pour poursuivre B05/B13 sans convertir une validation de format en preuve de mutation ou de validation propriétaire.

## What Changes

- Ajouter un parseur mémoire incrémental recevant seulement des segments bytes exacts, avec fin/fermeture explicites et état borné.
- Respecter UTF-8 strict sans BOM, framing CSV fixé et NDJSON objet par ligne, en refusant diagnostics sans écho et ambiguïtés de contenu.
- Appliquer le mapping déclaré et versionné sans conversion métier, alias, normalisation ou callback du payload.
- Fournir des résultats intermédiaires Python privés et une complétude explicite, sans introduire de nouveau schéma logique ou wire format.
- Réutiliser les contrats existants sans les modifier, sans ORM ou provider de stockage concret.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- bulk-operations : implémentation du périmètre parsing/mapping et diagnostics de B05/B13 déjà approuvés ; deux exigences MODIFIED strictement verbatim, sans nouveau scénario normatif.

## Impact

Trois nouveaux Python (backend, tests unitaires, intégration fraîche), quatre artefacts du seul change. Aucun I/O direct, provider de production, callback/itérateur du payload, admission, worker, mutation propriétaire, idempotence/outbox SQL, HTTP, PA/PZT, dépendance, Git ou déploiement. Archive unique et STATISTIQUES sous mandat distinct avant retour SÉLECTION.
