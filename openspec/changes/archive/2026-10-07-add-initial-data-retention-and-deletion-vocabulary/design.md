# Conception du vocabulaire déclaratif

## Sources

- openspec/specs/data-lifecycle/spec.md, requirement « Dimensions et états distincts ».
- TECHNICAL.md §14.1 : rétention RETAINED, LEGAL_HOLD, ELIGIBLE_FOR_PURGE ; deletion_strategy SOFT_DELETE, PHYSICAL_DELETE, ARCHIVE, IMMUTABLE.
- src/pixs/kernel/data_governance.py : deux Enums standard distinctes dans un module pur interne.

## Contrat minimal

RetentionState(Enum) porte exactement les trois couples nom/valeur de rétention. DeletionStrategy(Enum) porte exactement les quatre couples nom/valeur de stratégie. Ordre textuel du cadrage conservé, sans sémantique de priorité. __all__ contient exactement ces deux classes. Import enum seul, aucune façade ni __init__ modifiés, aucune dépendance ajoutée ; compatibilité Python >=3.12. Les types ne convertissent ni ne résolvent les références de politique existantes. Aucun défaut n'est appliqué. RESTRICT (cascade) et PURGED sont hors de ces vocabulaires.

## Validation

Stricts du change et de data-lifecycle avant le code puis après. Compilation des trois fichiers ; tests unitaires des deux vocabulaires et de leur séparation ; intégration en processus frais -I -B sous environnement réduit, gardes positives existantes de fichiers/réseau/processus/environnement/base. Le chargement mécanique est comparé après import de la façade pixs.kernel existante, qui charge déjà lifecycle : aucun chargement supplémentaire par le nouveau module. Régression ciblée : test_data_governance_vocabulary, test_kernel_purity, test_public_api_facades. Globaux finaux seulement : codes natifs conservés, comparaison des 19 avertissements historiques et de leurs résumés, zéro erreur nouvelle. UTF-8/LF, delta canonique identique et 154 empreintes de référence intactes.

## Limites

Aucune suppression, restauration, rétention calculée, legal hold, purge, tombstone, autorisation, audit, publication du profil ou runtime. Ce vocabulaire ne prouve pas les scénarios fonctionnels complets de data-lifecycle.
