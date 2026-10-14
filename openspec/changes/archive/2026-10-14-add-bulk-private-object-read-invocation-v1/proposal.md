## Why

B04 dispose d'un vérificateur mémoire sans invocation réelle du stockage. Des snapshots reçus en arguments ne prouvent pas des contrôles actuels. Il faut invoquer stat_private/iter_bytes via ports composés, avec check EXECUTE puis gouvernance RESOLVED sur le contrat ObjectMetadataV1 attendu, qualification résolue et async bornée, avant tout traitement propriétaire.

## What Changes

- Appeler effectivement AuthorityPort.check EXECUTE sur l'objet demandé via trusted_ports exact, server_context opaque et operation_reference serveur, puis résoudre la gouvernance sur ObjectMetadataV1 attendu avec classification_reference avant stockage.
- Invoquer stat_private/iter_bytes d'une liaison qualifiée résolue, alimenter new_object_integrity_verifier existant, vérifier appartenance/classification/type/taille/SHA-256, bornes PolicyV1 existantes, deadline UTC et asyncio.Event serveur, sans contenu conservé ni remis.
- Factoriser à strict nécessaire l’invocation et la validation profonde intégrale GovernanceResolutionV1 dans bulk_trusted_ports.py, sans changer le comportement MappingDescriptorV1 B01 et sans cycle d'import.
- Qualifier les preuves avec provider synthétique déclaré uniquement, sans qualifier la production.

## Capabilities

### New Capabilities

Aucune nouvelle capacité normative.

### Modified Capabilities

- object-storage : Requirement Runtime Bulk v1 B04 canonique conservé verbatim pour ses deux phrases et ses deux scénarios originaux, avec ajout de scénarios seulement démontrant ces comportements déjà exigés, sans nouveau champ, sémantique ou valeur de production.

## Impact

Quatre fichiers Python concernés (un nouveau lecteur, une factorisation à approuver séparément, deux tests) et quatre artefacts. Aucun worker complet, upload/finalisation/effacement, owner mutation, route HTTP, provider production, persistance/migration, ORM, champ PolicyV1, dépendance, Git ou infrastructure. Archive unique puis STATISTIQUES sous mandat distinct et retour SÉLECTION.
