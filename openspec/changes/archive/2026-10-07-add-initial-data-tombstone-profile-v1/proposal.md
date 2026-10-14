# Profil structurel préparatoire de tombstone v1

## Why

Le canon data-lifecycle et TECHNICAL.md §14.3 définissent le profil tombstone-v1. Sa représentation mémoire et sa validation structurelle ne sont pas encore implémentées.

## What Changes

Ajouter TombstoneProfile, une dataclass interne immuable à huit champs explicites, et validate_data_tombstone_profile, un validateur pur retournant des diagnostics VALIDATE statiques, triés et dédupliqués. Les tests couvrent les types exacts, l'instant UTC calendaire, la cohérence scope/tenant et l'absence d'effet.

## Périmètre et limites

Trois fichiers Python nouveaux : src/pixs/kernel/data_tombstone_profile.py, tests/unit/test_data_tombstone_profile.py et tests/integration/test_data_tombstone_profile_integration.py. Aucune façade publique, dépendance, configuration, résolution de référence, lecture d'horloge, entrée/sortie, suppression, purge, persistance, propagation ou restauration. Les références restent opaques et les None explicites ne fournissent aucune autorisation ou exemption.

Le delta reprend mot pour mot le requirement canonique et ses deux scénarios, sans évolution normative. L'archivage futur utilise --skip-specs sous mandat distinct, après toutes les preuves et avant un rapport STATISTIQUES.md par archive.
