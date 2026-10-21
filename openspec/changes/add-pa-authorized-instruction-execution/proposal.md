# PA04 — Instructions, mandats et exécution locale

## Pourquoi

Le canon distingue trois binaires PA et six modes, plus le binaire indépendant PZT et son mode pzt-daemon ; le README indique que l’implémentation, la qualification et les artefacts restent à réaliser. Le contrôle de présence ciblé des sources n’est pas une recette de plateforme.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

Contrats publics des instructions, fraîcheur, scopes, idempotence, revalidation, compensation préautorisée et réconciliation après résultat incertain ; aucun code distant implicite.

## Capacités

### Capacités nouvelles

Aucun comportement normatif nouveau n’est prévu. Ce dossier prépare la réalisation ou la qualification des contrats déjà présents dans le canon.

### Capacités modifiées

Aucune modification de texte canonique. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios ; `skip_specs: true` évite un delta identique artificiel. Si un audit ou une décision exige une évolution normative, présenter son delta avant réalisation, sans considérer cette métadonnée comme une dispense de conformité.

## Sélection et périmètre autorisé

Hors premier P0 proposé ; obligation du profil/capacité sélectionné, applicabilité à confirmer. La préparation demandée ne sélectionne, n’active et ne qualifie pas cette capacité dans le premier profil P0.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [add-pa-system-session-lifecycle](../add-pa-system-session-lifecycle/proposal.md).
- [add-pzt-wireguard-local-transport-and-filtering](../add-pzt-wireguard-local-transport-and-filtering/proposal.md).
- [add-pzt-network-mandates-and-fail-closed-revocation](../add-pzt-network-mandates-and-fail-closed-revocation/proposal.md).
- [add-pzt-public-control-contracts-and-state-streams](../add-pzt-public-control-contracts-and-state-streams/proposal.md).
- [add-pzt-pa-admission-and-ephemeral-peer-generation](../add-pzt-pa-admission-and-ephemeral-peer-generation/proposal.md).
- [integrate-runtime-authorization-and-super-admin](../integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md).



## Impact de réalisation future

Couche locale séparée de Django/PostgreSQL et sans autorité métier. Composer les opérations au build par contrats, dispatch explicite et identité du mode ; isoler comptes/sessions, handles et générations. Lier mandats, contexte, effets et résultats observés ; communiquer avec PBO uniquement via PZT. Les trois binaires PA (Cython) et PZT indépendant (Cython) restent colivrés, sous gestion respective de pixs.agent et pixs.pzt.

## Critère de sortie de réalisation future

Mandat périmé/révoqué bloqué ; crash entre effet et résultat réconcilié ; acteur initial conservé sans credentials Super Admin transférés.

## Décisions restant à valider

Catalogue exact des opérations, schémas d’instructions/mandats et preuves de postconditions ; aucun shell arbitraire ou compensation hors plan.
