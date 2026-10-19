# Z05 — Exécution DNS et adapters PA

## Pourquoi

Les contrats PZT et leurs décisions sont spécifiés ; le README ne revendique pas de réseau livré. Les clauses de gestion PBO essentielles restent distinctes des rôles réseau activés et des auxiliaires spécialisés.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

A06c–A06k : service DNS distinct piloté par PA désignés, DoT, vues, cache/TTL, sélection/secours, nommage/suffixe/alias ; compléter C14.

## Capacités

### Capacités nouvelles

Aucun comportement normatif nouveau n’est prévu. Ce dossier prépare la réalisation ou la qualification des contrats déjà présents dans le canon.

### Capacités modifiées

Aucune modification de texte canonique. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios ; `skip_specs: true` évite un delta identique artificiel. Si un audit ou une décision exige une évolution normative, présenter son delta avant réalisation, sans considérer cette métadonnée comme une dispense de conformité.

## Sélection et périmètre autorisé

Hors premier P0 proposé ; obligation du profil/capacité sélectionné, applicabilité à confirmer. La préparation demandée ne sélectionne, n’active et ne qualifie pas cette capacité dans le premier profil P0.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [add-essential-pbo-pzt-and-dns-modules](../add-essential-pbo-pzt-and-dns-modules/proposal.md).
- [add-pa-authorized-instruction-execution](../add-pa-authorized-instruction-execution/proposal.md).
- [add-pzt-private-address-plan-and-ipv6-lifecycle](../add-pzt-private-address-plan-and-ipv6-lifecycle/proposal.md).
- [add-pzt-public-control-contracts-and-state-streams](../add-pzt-public-control-contracts-and-state-streams/proposal.md).



## Impact de réalisation future

Séparer contrôle métier PBO/Django/PostgreSQL, propriétaire réseau pzt-daemon et adapters système. Implémenter le rôle précisément désigné par les contrats sources, avec schémas fermés, versions et contrôles courants ; conserver toutes bornes, unités, conditions de reprise et alternatives rejetées. La cryptographie WireGuard n’est pas réimplémentée. Les bibliothèques de transport, sources de temps et adapters sont qualifiés, sans confiance supposée.

## Critère de sortie de réalisation future

PA ordinaires clients ; isolement des vues ; aucun repli public privé ; bootstrap sans dépendance circulaire DNS ; application prouvée.

## Décisions restant à valider

Schémas/API du module DNS, placement des PA serveurs, bibliothèques et état appliqué ; DoT, caches, choix des serveurs, suffixes et alias suivent les décisions sources.
