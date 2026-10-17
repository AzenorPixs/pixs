# PA01 — Composition et compilation des quatre binaires PA

## Pourquoi

Les exigences PA décrivent quatre binaires et sept modes ; le README indique que l’implémentation, la qualification et les artefacts restent à réaliser. Le contrôle de présence ciblé des sources n’est pas une recette de plateforme.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

Catalogue fermé au build, quatre exécutables, sept modes, Nuitka pour trois binaires et Cython pour PZT ; qualifier versions, ABI et runtime avant installation des outils.

## Capacités

### Capacités nouvelles

Aucun comportement normatif nouveau n’est prévu. Ce dossier prépare la réalisation ou la qualification des contrats déjà présents dans le canon.

### Capacités modifiées

Aucune modification de texte canonique. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios ; `skip_specs: true` évite un delta identique artificiel. Si un audit ou une décision exige une évolution normative, présenter son delta avant réalisation, sans considérer cette métadonnée comme une dispense de conformité.

## Sélection et périmètre autorisé

Hors premier P0 proposé ; obligation du profil/capacité sélectionné, applicabilité à confirmer. La préparation demandée ne sélectionne, n’active et ne qualifie pas cette capacité dans le premier profil P0.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [define-first-installable-pbo-profile](../define-first-installable-pbo-profile/proposal.md).
- [activate-reference-runtime-composition](../activate-reference-runtime-composition/proposal.md).



## Impact de réalisation future

Couche locale séparée de Django/PostgreSQL et sans autorité métier. Composer les opérations au build par contrats, dispatch explicite et identité du mode ; isoler comptes/sessions, handles et générations. Lier mandats, contexte, effets et résultats observés ; communiquer avec PBO uniquement via PZT. Les quatre binaires et les choix Nuitka/Cython validés sont conservés.

## Critère de sortie de réalisation future

Contenu et responsabilités exacts ; construction reproductible par cible ; aucune compilation assimilée à une recette fonctionnelle.

## Décisions restant à valider

Versions de Nuitka/Cython et graphe Python/ABI, format de distribution, noms des exécutables et architectures ; les outils eux-mêmes sont déjà décidés, leur installation n’est pas autorisée ici.
