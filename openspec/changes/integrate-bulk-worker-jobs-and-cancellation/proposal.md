# B08 — Worker, baux, reprise et annulation Bulk

## Pourquoi

Des structures, dépôts PostgreSQL et façades bornées existent ; le dernier sous-lot couvre IMPORT ATOMIC_PER_CHUNK/REJECT. Le catalogue prévoit un complément du runtime, pas une recréation des profils ou records déjà livrés.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

Worker réel avec jobs, baux/checkpoints et annulation existants ; contexte/acteur/configuration actuels.

## Capacités

### Capacités nouvelles

Aucun comportement normatif nouveau n’est prévu. Ce dossier prépare la réalisation ou la qualification des contrats déjà présents dans le canon.

### Capacités modifiées

Aucune modification de texte canonique. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios ; `skip_specs: true` évite un delta identique artificiel. Si un audit ou une décision exige une évolution normative, présenter son delta avant réalisation, sans considérer cette métadonnée comme une dispense de conformité.

## Sélection et périmètre autorisé

Hors premier P0 proposé ; obligation du profil/capacité sélectionné, applicabilité à confirmer. La préparation demandée ne sélectionne, n’active et ne qualifie pas cette capacité dans le premier profil P0.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [add-reference-worker-scheduler-and-event-delivery](../add-reference-worker-scheduler-and-event-delivery/proposal.md).
- [complete-bulk-owner-admission-and-import-mapping](../complete-bulk-owner-admission-and-import-mapping/proposal.md).
- [integrate-bulk-inbox-outbox-and-publication](../integrate-bulk-inbox-outbox-and-publication/proposal.md).



## Impact de réalisation future

Compléter les façades et dépôts Bulk existants par les ports propriétaires et transactions déclarés. Réutiliser les profils, records, migrations, baux et checkpoints livrés ; distinguer validation, admission, effet et résultat durable. Rattacher chaque effet à autorité/gouvernance/tenant courants, conserver atomicité du mode choisi et reprise idempotente.

## Critère de sortie de réalisation future

Perte de bail/fencing, annulation concurrente et reprise ; droits réévalués ; bail Bulk distinct du bail scheduler.

## Décisions restant à valider

Branchement worker et unités de reprise/annulation, acteur et configuration courants ; les baux Bulk ne deviennent pas le bail scheduler.
