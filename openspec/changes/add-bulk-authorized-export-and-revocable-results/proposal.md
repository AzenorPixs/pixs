# B06 — Export et résultats révocables

## Pourquoi

Des structures, dépôts PostgreSQL et façades bornées existent ; le dernier sous-lot couvre IMPORT ATOMIC_PER_CHUNK/REJECT. Le catalogue prévoit un complément du runtime, pas une recréation des profils ou records déjà livrés.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

Export filtré, manifeste existant, flux et résultat gouverné ; téléchargement réautorisé et révocation.

## Capacités

### Capacités nouvelles

Aucun comportement normatif nouveau n’est prévu. Ce dossier prépare la réalisation ou la qualification des contrats déjà présents dans le canon.

### Capacités modifiées

Aucune modification de texte canonique. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios ; `skip_specs: true` évite un delta identique artificiel. Si un audit ou une décision exige une évolution normative, présenter son delta avant réalisation, sans considérer cette métadonnée comme une dispense de conformité.

## Sélection et périmètre autorisé

Hors premier P0 proposé ; obligation du profil/capacité sélectionné, applicabilité à confirmer. La préparation demandée ne sélectionne, n’active et ne qualifie pas cette capacité dans le premier profil P0.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [complete-bulk-owner-admission-and-import-mapping](../complete-bulk-owner-admission-and-import-mapping/proposal.md).
- [add-selected-object-storage-provider](../add-selected-object-storage-provider/proposal.md).
- [enforce-core-data-governance-and-lifecycle](../enforce-core-data-governance-and-lifecycle/proposal.md).



## Impact de réalisation future

Compléter les façades et dépôts Bulk existants par les ports propriétaires et transactions déclarés. Réutiliser les profils, records, migrations, baux et checkpoints livrés ; distinguer validation, admission, effet et résultat durable. Rattacher chaque effet à autorité/gouvernance/tenant courants, conserver atomicité du mode choisi et reprise idempotente.

## Critère de sortie de réalisation future

Contrôles avant sélection/pagination/téléchargement ; versions/empreintes cohérentes ; révocation ferme ; export non classifié refusé.

## Décisions restant à valider

Projection/export par propriétaire et formats/résultats applicables ; réautorisation et révocation effectives, sans URL permissive par défaut.
