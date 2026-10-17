# PA02 — Provisionnement PA et rattachement aux autorités

## Pourquoi

Les exigences PA décrivent quatre binaires et sept modes ; le README indique que l’implémentation, la qualification et les artefacts restent à réaliser. Le contrôle de présence ciblé des sources n’est pas une recette de plateforme.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

Identité, références de secrets, ancrages et relations PBO–PA ; plusieurs autorités sans conflit résolu par dernière écriture ; provisionnement distinct du contrôle continu.

## Capacités

### Capacités nouvelles

Aucun comportement normatif nouveau n’est prévu. Ce dossier prépare la réalisation ou la qualification des contrats déjà présents dans le canon.

### Capacités modifiées

Aucune modification de texte canonique. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios ; `skip_specs: true` évite un delta identique artificiel. Si un audit ou une décision exige une évolution normative, présenter son delta avant réalisation, sans considérer cette métadonnée comme une dispense de conformité.

## Sélection et périmètre autorisé

Hors premier P0 proposé ; obligation du profil/capacité sélectionné, applicabilité à confirmer. La préparation demandée ne sélectionne, n’active et ne qualifie pas cette capacité dans le premier profil P0.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [add-pbo-runtime-secret-provider](../add-pbo-runtime-secret-provider/proposal.md).
- [add-core-postgres-services](../add-core-postgres-services/proposal.md).
- [add-initial-authentication-and-sessions](../add-initial-authentication-and-sessions/proposal.md).



## Impact de réalisation future

Couche locale séparée de Django/PostgreSQL et sans autorité métier. Composer les opérations au build par contrats, dispatch explicite et identité du mode ; isoler comptes/sessions, handles et générations. Lier mandats, contexte, effets et résultats observés ; communiquer avec PBO uniquement via PZT. Les quatre binaires et les choix Nuitka/Cython validés sont conservés.

## Critère de sortie de réalisation future

Reprise sans double identité ; aucun premier PBO approuvé implicitement ; isolation des autorités ; aucune autorité métier locale.

## Décisions restant à valider

Formats du provisionnement et ancrages, identité par relation, règles de conflit entre autorités ; aucune confiance par premier contact.
