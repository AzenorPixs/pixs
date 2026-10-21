# PA08 — Qualification des plateformes et recette PA

## Pourquoi

Le canon distingue trois binaires PA et six modes, plus le binaire indépendant PZT et son mode pzt-daemon ; le README indique que l’implémentation, la qualification et les artefacts restent à réaliser. Le contrôle de présence ciblé des sources n’est pas une recette de plateforme.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

Matrice R01–R68 par binaire/mode/OS/CPU/topologie ; Debian/Linux et Docker d'abord, puis Windows/VM/LXC selon sélection.

## Capacités

### Capacités nouvelles

Aucun comportement normatif nouveau n’est prévu. Ce dossier prépare la réalisation ou la qualification des contrats déjà présents dans le canon.

### Capacités modifiées

Aucune modification de texte canonique. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios ; `skip_specs: true` évite un delta identique artificiel. Si un audit ou une décision exige une évolution normative, présenter son delta avant réalisation, sans considérer cette métadonnée comme une dispense de conformité.

## Sélection et périmètre autorisé

Hors premier P0 proposé ; obligation du profil/capacité sélectionné, applicabilité à confirmer. La préparation demandée ne sélectionne, n’active et ne qualifie pas cette capacité dans le premier profil P0.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [add-pa-supervision-maintenance-and-quarantine](../add-pa-supervision-maintenance-and-quarantine/proposal.md).
- [add-pzt-wireguard-local-transport-and-filtering](../add-pzt-wireguard-local-transport-and-filtering/proposal.md).
- [add-pzt-managed-dns-service-and-pa-adapters](../add-pzt-managed-dns-service-and-pa-adapters/proposal.md).
- [add-pzt-public-control-contracts-and-state-streams](../add-pzt-public-control-contracts-and-state-streams/proposal.md).
- [add-pzt-service-identities-and-tpm-attestation](../add-pzt-service-identities-and-tpm-attestation/proposal.md).
- [add-pzt-pa-admission-and-ephemeral-peer-generation](../add-pzt-pa-admission-and-ephemeral-peer-generation/proposal.md).



## Impact de réalisation future

Couche locale séparée de Django/PostgreSQL et sans autorité métier. Composer les opérations au build par contrats, dispatch explicite et identité du mode ; isoler comptes/sessions, handles et générations. Lier mandats, contexte, effets et résultats observés ; communiquer avec PBO uniquement via PZT. Les trois binaires PA (Cython) et PZT indépendant (Cython) restent colivrés, sous gestion respective de pixs.agent et pixs.pzt.

## Critère de sortie de réalisation future

Preuves par cible ; sessions non applicables à Docker et absence contrôlée ; aucun support ni gain CPU/RAM inféré de DEVOPS ou d'une compilation.

## Décisions restant à valider

Matrice OS/CPU/topologie/bureaux/vTPM et scénarios applicables ; les plateformes demandées ne deviennent pas supportées sans preuve.
