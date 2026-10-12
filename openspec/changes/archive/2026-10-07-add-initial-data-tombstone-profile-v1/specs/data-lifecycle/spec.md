## MODIFIED Requirements

### Requirement: Profil structurel préparatoire de tombstone v1

Le profil tombstone-v1 MUST être une représentation interne, immuable et purement mémoire comportant exactement resource_reference, deletion_version, deleted_at, tenant_id, scope_id, retention_reference, synchronization_reference et deduplication_reference. Tous les champs MUST être fournis explicitement, sans valeur par défaut ni champ de payload.

resource_reference MUST être une str exacte non vide, opaque et sans normalisation. deletion_version MUST être un int exact supérieur ou égal à zéro ; bool MUST être refusé. deleted_at MUST être une str exacte représentant un instant calendaire UTC valide au format YYYY-MM-DDTHH:MM:SS, avec fraction optionnelle de 1 à 6 chiffres, suivi de Z ou +00:00 ; heures 00–23, minutes et secondes 00–59.

tenant_id, scope_id, retention_reference, synchronization_reference et deduplication_reference MUST être chacun None explicite ou une str exacte non vide, opaque et sans normalisation. Un scope_id non None MUST avoir un tenant_id non None. Ces valeurs MUST provenir d'un appelant de confiance ou de fixtures synthétiques ; None MUST NOT être interprété comme une autorisation, une exemption de rétention ou une décision d'applicabilité.

La validation MUST porter uniquement sur la structure exacte et produire des diagnostics statiques VALIDATE, triés et dédupliqués, sans reproduire les valeurs. Elle MUST NOT résoudre une référence, lire une horloge, effectuer une entrée/sortie, ni déduire une légitimité, une minimisation ou une classification de données.

Ce profil préparatoire MUST NOT valoir preuve de suppression, de purge, de persistance durable, de propagation, de reconstruction ou de restauration sans résurrection. Les exigences générales de tombstone, rétention, autorisation, audit et propagation restent intégralement applicables aux futures intégrations. Aucun wire format, provider, façade publique, politique, configuration ou nouvelle dépendance n'est introduit par ce profil.

#### Scenario: Structure valide sans effet

- **WHEN** un appelant de confiance fournit les huit champs avec leurs types et contraintes déclarés
- **THEN** la validation ne produit aucun diagnostic ni effet et la représentation conserve exactement ces valeurs

#### Scenario: Structure invalide refusée sans écho

- **WHEN** une valeur a un type ou une forme interdite, notamment une version booléenne ou négative, un instant non UTC, une référence vide ou un scope sans tenant
- **THEN** la validation produit des diagnostics statiques triés et dédupliqués sans reproduire les valeurs ni fournir de garantie runtime
