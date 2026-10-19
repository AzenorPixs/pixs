## 1. Lecteur privé en lecture actuelle

- [x] 1.1 Implémenter l'API asynchrone privée avec trusted_ports exact, server_context opaque, operation_reference serveur, check EXECUTE puis gouvernance RESOLVED sur ObjectMetadataV1 attendu, sans preuve par snapshots reçus ni callback du payload.
- [x] 1.2 Factoriser à strict nécessaire le contrôle de réponse GovernanceResolutionV1 dans bulk_trusted_ports.py avec helper commun, conserver le comportement MappingDescriptorV1 B01, éviter tout cycle ; modification soumise à un mandat CAB distinct.
- [x] 1.3 Implémenter qualification résolue qualify liée instance/version, invocation bornée stat_private/iter_bytes par deadline UTC et asyncio.Event avec asyncio.wait, alimentation du vérificateur existant, fermeture itérateur/tâches/ressources sur toute sortie, aucun octet remis ni copie complète.

## 2. Preuves

- [x] 2.1 Réussir unitaires avec provider synthétique déclaré, bornes PolicyV1 existantes, versions divergentes, authority/governance refusés, types hostiles, absence de fuite ou d'effet après refus.
- [x] 2.2 Réussir intégration fraîche, compiler les Python concernés, prouver sous gardes l'absence d'import ORM et la non-applicabilité PostgreSQL sans test SQL artificiel, vérifier compatibilité B01.
- [x] 2.3 Vérifier strict change/global, UTF-8/LF, cohérence et absence de modification hors périmètre.

## Procédure après preuves

Cocher seulement après preuve. Archiver une seule fois, publier STATISTIQUES.md sous mandat distinct, vérifier six sections/totaux puis revenir à SÉLECTION sans fin globale.

## Résultats des contrôles combinés

Les 545 tests Bulk réussissent sous exclusion d’intégration. OpenSpec standard valide 79/79 éléments ; le strict global est 77/79 avec les quatre WARNING de longueur préexistants inchangés (bulk-operations exigences 6, 10, 13 et identity-assurance exigence 4), sans ERROR ni nouvelle anomalie. Le change B04 est strictement valide sans issue. Ces avertissements extérieurs ne sont pas présentés comme une réussite stricte globale et ne sont pas corrigés dans ce change.
