# X01 — Image Docker conforme

## Pourquoi

Le README déclare les distributions non livrées ; le canon impose à l’image PBO/PFO/PZT et trois binaires PA, avec exclusion des modes utilisateur.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

PBO/PFO/PZT et trois binaires PA ; état externe, sondes/arrêt/reproductibilité/publication.

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

Construire depuis sources et versions déclarées l’image Pixs complète en contenu PBO/PFO/PZT et exactement trois binaires PA. Exclure binaire utilisateur et modes de session, séparer profils applicatifs et supervision PA, préserver état/configuration/secrets hors image ; transmettre signaux/drain et identité de distribution sans nouvelle autorité métier.

## Critère de sortie de réalisation future

Binaire et modes utilisateur absents ; aucun hôte administré implicitement ; recette isolée ; permissions selon profil autorisé.

## Décisions restant à valider

Base/outils/architecture, rôles/comptes/supervision et permissions du profil ; trois binaires PA seulement, pas de binaire utilisateur.
