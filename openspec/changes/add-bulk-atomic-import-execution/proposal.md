# B02 — Import ATOMIC complet

## Pourquoi

Des structures, dépôts PostgreSQL et façades bornées existent ; le dernier sous-lot couvre IMPORT ATOMIC_PER_CHUNK/REJECT. Le catalogue prévoit un complément du runtime, pas une recréation des profils ou records déjà livrés.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

Mode ATOMIC global, distinct du sous-lot ATOMIC_PER_CHUNK/REJECT livré ; transaction propriétaire, progression et échecs.

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
- [integrate-bulk-private-object-storage](../integrate-bulk-private-object-storage/proposal.md).



## Impact de réalisation future

Compléter les façades et dépôts Bulk existants par les ports propriétaires et transactions déclarés. Réutiliser les profils, records, migrations, baux et checkpoints livrés ; distinguer validation, admission, effet et résultat durable. Rattacher chaque effet à autorité/gouvernance/tenant courants, conserver atomicité du mode choisi et reprise idempotente.

## Critère de sortie de réalisation future

Erreur/interruption avec garanties ATOMIC effectives ; concurrence/rejeu réels ; aucun résultat partiel présenté comme engagement global.

## Décisions restant à valider

Définir le contrat transactionnel propriétaire de l’import global ; ne pas requalifier ATOMIC_PER_CHUNK/REJECT déjà livré en ATOMIC.
