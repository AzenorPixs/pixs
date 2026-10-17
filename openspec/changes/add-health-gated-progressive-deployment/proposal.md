# O30 — Déploiement progressif

## Pourquoi

La capacité est un candidat du canon ; la revue de présence des sources et la matrice ne démontrent pas une réalisation opérationnelle. Toute ligne NE impose un audit ciblé avant de confirmer un manque ou de créer du code.

Ce dossier référence 4 lignes NE : leur présence dans le canon ne prouve pas un manque d’implémentation. La demande actuelle autorise leur préparation conditionnelle ; un audit ciblé doit décider du complément réel avant réalisation.

## Modifications proposées

Révisions/stratégies/prévalidations/health gates, routage borné et rollback audité compatible.

## Capacités

### Capacités nouvelles

Aucun comportement normatif nouveau n’est prévu. Ce dossier prépare la réalisation ou la qualification des contrats déjà présents dans le canon.

### Capacités modifiées

Aucune modification de texte canonique. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios ; `skip_specs: true` évite un delta identique artificiel. Si un audit ou une décision exige une évolution normative, présenter son delta avant réalisation, sans considérer cette métadonnée comme une dispense de conformité.

## Sélection et périmètre autorisé

Hors premier P0 proposé ; obligation du profil/capacité sélectionné, applicabilité à confirmer. La préparation demandée ne sélectionne, n’active et ne qualifie pas cette capacité dans le premier profil P0.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [add-runtime-observability-and-operations](../add-runtime-observability-and-operations/proposal.md).
- [add-upgrade-backup-and-restore-contracts](../add-upgrade-backup-and-restore-contracts/proposal.md).
- [publish-first-qualified-pbo-release](../publish-first-qualified-pbo-release/proposal.md).



## Impact de réalisation future

Composant/provider optionnel au-dessus du Kernel, déclaré par manifest et sélection explicite. Exposer uniquement ses contrats publics versionnés et écrire ses données via leur propriétaire. Conserver Django/PostgreSQL comme autorités, contexte tenant/scope, audit et gouvernance ; qualifier séparément dépendances, limites et mode dégradé. Ne pas imposer un provider, une bibliothèque ou une ressource métier encore non décidés.

## Critère de sortie de réalisation future

Instance hors santé/incompatible hors trafic ; pas d'accès élargi ; rollback seulement prouvé par matrice.

## Décisions restant à valider

Stratégies et fenêtres de coexistence, seuils health et routage ; rollback soumis à compatibilité prouvée.
