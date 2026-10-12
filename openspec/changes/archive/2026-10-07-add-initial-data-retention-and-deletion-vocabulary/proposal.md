# Vocabulaire de rétention et de stratégie de suppression

## Why

TECHNICAL.md §14.1 nomme trois états de rétention et quatre stratégies de suppression. Aucun de ces vocabulaires ne figure dans src/pixs/kernel. Le requirement data-lifecycle « Dimensions et états distincts » exige de distinguer les dimensions ; les deux Enums de data_governance.py fournissent le patron local.

## What Changes

Ajouter deux Enums internes distinctes dans un unique module pur, avec les noms et valeurs exacts du cadrage, dans son ordre textuel. Les tests vérifient les membres, les conversions et la distinction des types, ainsi que l'import isolé sans effet sous les gardes positives existantes.

## Périmètre et limites

Trois fichiers Python nouveaux seulement : src/pixs/kernel/data_lifecycle_policy_vocabulary.py, tests/unit/test_data_retention_and_deletion_vocabulary.py et tests/integration/test_data_retention_and_deletion_vocabulary_integration.py. Aucun défaut, ordre de sévérité, calcul, transition, politique, cascade, purge, provider, persistance, façade ou consommateur ajouté. Les champs opaques des profils existants restent inchangés. Livraison déclarative partielle : aucune garantie fonctionnelle de suppression ou de rétention n'est déclarée réalisée. Le delta reprend un bloc canonique sans changement normatif ; archive future avec --skip-specs, sur décision distincte.
