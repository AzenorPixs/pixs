# Z15 — Dossier de preuve et validation bornée

## Pourquoi

Les contrats PZT et leurs décisions sont spécifiés ; le README ne revendique pas de réseau livré. Les clauses de gestion PBO essentielles restent distinctes des rôles réseau activés et des auxiliaires spécialisés.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

A10i35–A10i40 : reçu de clôture, SHA-384 entier/Base64url, JSON/pièces, plafonds et budgets séquentiels.

## Capacités

### Capacités nouvelles

Aucun comportement normatif nouveau n’est prévu. Ce dossier prépare la réalisation ou la qualification des contrats déjà présents dans le canon.

### Capacités modifiées

Aucune modification de texte canonique. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios ; `skip_specs: true` évite un delta identique artificiel. Si un audit ou une décision exige une évolution normative, présenter son delta avant réalisation, sans considérer cette métadonnée comme une dispense de conformité.

## Sélection et périmètre autorisé

Hors premier P0 proposé ; obligation du profil/capacité sélectionné, applicabilité à confirmer. La préparation demandée ne sélectionne, n’active et ne qualifie pas cette capacité dans le premier profil P0.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [add-pzt-authoritative-control-and-signed-receipts](../add-pzt-authoritative-control-and-signed-receipts/proposal.md).
- [add-pzt-offline-root-backup-and-recovery](../add-pzt-offline-root-backup-and-recovery/proposal.md).
- [add-pzt-monotonic-witness-and-key-sanitation](../add-pzt-monotonic-witness-and-key-sanitation/proposal.md).



## Impact de réalisation future

Séparer contrôle métier PBO/Django/PostgreSQL, propriétaire réseau pzt-daemon et adapters système. Implémenter le rôle précisément désigné par les contrats sources, avec schémas fermés, versions et contrôles courants ; conserver toutes bornes, unités, conditions de reprise et alternatives rejetées. La cryptographie WireGuard n’est pas réimplémentée. Les bibliothèques de transport, sources de temps et adapters sont qualifiés, sans confiance supposée.

## Critère de sortie de réalisation future

Octets et références vérifiables ; dossier malformé/surdimensionné refusé ; bornes locales non extrapolées à tout PA/PBO.

## Décisions restant à valider

Codec/schémas et stockage des pièces, qualification des plafonds et ressources ; SHA-384/Base64url et format décidés sont conservés.
