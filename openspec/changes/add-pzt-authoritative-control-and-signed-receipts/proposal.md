# Z03 — Autorité de contrôle, durabilité et reçus

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Rôle CZT, PG indépendante chiffrée, confirmations synchrones, exclusion et continuité bornée ; pas de fusion avec la PG applicative PBO.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [pzt](../../specs/pzt/spec.md).
- [zt-controller](../../specs/zt-controller/spec.md).
- [brick-redundancy](../../specs/brick-redundancy/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Pourquoi

Les contrats PZT et leurs décisions sont spécifiés ; le README ne revendique pas de réseau livré. Les clauses de gestion PBO essentielles restent distinctes des rôles réseau activés et des auxiliaires spécialisés.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

A12a–A12g : primaire admissible, coordination, réplication/promotion, signataires, preuves d'engagement, reçus versionnés et récupération des clés.

## Capacités

### Capacités nouvelles

Aucun comportement normatif nouveau n’est prévu. Ce dossier prépare la réalisation ou la qualification des contrats déjà présents dans le canon.

### Capacités modifiées

Aucune modification de texte canonique. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios ; `skip_specs: true` évite un delta identique artificiel. Si un audit ou une décision exige une évolution normative, présenter son delta avant réalisation, sans considérer cette métadonnée comme une dispense de conformité.

## Sélection et périmètre autorisé

Hors premier P0 proposé ; obligation du profil/capacité sélectionné, applicabilité à confirmer. La préparation demandée ne sélectionne, n’active et ne qualifie pas cette capacité dans le premier profil P0.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [add-core-postgres-services](../archive/2026-10-20-add-core-postgres-services/proposal.md).
- [add-durable-minimized-audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md).
- [add-pzt-ca-hierarchy-rotation-and-recovery](../add-pzt-ca-hierarchy-rotation-and-recovery/proposal.md).



## Impact de réalisation future

Séparer contrôle métier PBO/Django/PostgreSQL, propriétaire réseau pzt-daemon et adapters système. Implémenter le rôle précisément désigné par les contrats sources, avec schémas fermés, versions et contrôles courants ; conserver toutes bornes, unités, conditions de reprise et alternatives rejetées. La cryptographie WireGuard n’est pas réimplémentée. Les bibliothèques de transport, sources de temps et adapters sont qualifiés, sans confiance supposée.

## Critère de sortie de réalisation future

Un seul écrivain ; exclusion avant promotion ; signature distincte de commit PostgreSQL ; réponse perdue réconciliée ; clés hors preuves.

## Décisions restant à valider

Topologie et seuils de durabilité, mécanisme d’exclusion/promotion et interfaces des signataires ; préserver PostgreSQL autoritatif et les choix JWS/Ed25519 existants.
