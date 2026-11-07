# X01 — Image Docker conforme

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Profils de services, persistances et dépendances de Domaine ; deux binaires PA système/événements et PZT, sans session utilisateur ni droit hôte implicite.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [docker-image](../../specs/docker-image/spec.md).
- [reference-composition](../../specs/reference-composition/spec.md).
- [pixs-domains](../../specs/pixs-domains/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Pourquoi

Le README déclare les distributions non livrées ; le canon impose à l’image PBO/PFO avec pixs.agent/pixs.pzt, deux binaires PA et PZT indépendant, avec exclusion des modes utilisateur.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

PBO/PFO avec pixs.agent/pixs.pzt, deux binaires PA et PZT indépendant ; état externe, sondes/arrêt/reproductibilité/publication.

## Capacités

### Capacités nouvelles

Aucun comportement normatif nouveau n’est prévu. Ce dossier prépare la réalisation ou la qualification des contrats déjà présents dans le canon.

### Capacités modifiées

Aucune modification de texte canonique. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios ; `skip_specs: true` évite un delta identique artificiel. Si un audit ou une décision exige une évolution normative, présenter son delta avant réalisation, sans considérer cette métadonnée comme une dispense de conformité.

## Sélection et périmètre autorisé

Hors premier P0 proposé ; obligation du profil/capacité sélectionné, applicabilité à confirmer. La préparation demandée ne sélectionne, n’active et ne qualifie pas cette capacité dans le premier profil P0.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [publish-first-qualified-pbo-release](../publish-first-qualified-pbo-release/proposal.md).
- [build-and-publish-independent-pa-debian-package](../build-and-publish-independent-pa-debian-package/proposal.md).
- [qualify-active-pzt-contracts-and-profiles](../qualify-active-pzt-contracts-and-profiles/proposal.md).



## Impact de réalisation future

Construire depuis sources et versions déclarées l’image Pixs complète en contenu PBO/PFO avec pixs.agent/pixs.pzt, deux binaires PA et le binaire indépendant PZT. Exclure binaire utilisateur et modes de session, séparer profils applicatifs et supervision distincte PA/PZT, préserver état/configuration/secrets hors image ; transmettre signaux/drain et identité de distribution sans nouvelle autorité métier.

## Critère de sortie de réalisation future

Binaire et modes utilisateur absents ; aucun hôte administré implicitement ; recette isolée ; permissions selon profil autorisé.

## Décisions restant à valider

Base/outils/architecture, rôles/comptes/supervision et permissions du profil ; deux binaires PA et PZT indépendant, pas de binaire utilisateur.
