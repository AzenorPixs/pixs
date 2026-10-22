# O25 — Outils IA médiés, évaluations et budgets

## Pourquoi

La capacité est un candidat du canon ; la revue de présence des sources et la matrice ne démontrent pas une réalisation opérationnelle. Toute ligne NE impose un audit ciblé avant de confirmer un manque ou de créer du code.

Ce dossier référence 4 lignes NE : leur présence dans le canon ne prouve pas un manque d’implémentation. La demande actuelle autorise leur préparation conditionnelle ; un audit ciblé doit décider du complément réel avant réalisation.

## Modifications proposées

Outils sous permissions et médiation, prompts/évaluations versionnés, budgets/audit.

## Capacités

### Capacités nouvelles

Aucun comportement normatif nouveau n’est prévu. Ce dossier prépare la réalisation ou la qualification des contrats déjà présents dans le canon.

### Capacités modifiées

Aucune modification de texte canonique. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios ; `skip_specs: true` évite un delta identique artificiel. Si un audit ou une décision exige une évolution normative, présenter son delta avant réalisation, sans considérer cette métadonnée comme une dispense de conformité.

## Sélection et périmètre autorisé

Hors premier P0 proposé ; obligation du profil/capacité sélectionné, applicabilité à confirmer. La préparation demandée ne sélectionne, n’active et ne qualifie pas cette capacité dans le premier profil P0.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [add-entitlements-and-atomic-quota-reservations](../add-entitlements-and-atomic-quota-reservations/proposal.md) — dépendance explicitée après audit du 17 octobre 2026.

- [add-declared-ai-provider-and-governed-retrieval](../add-declared-ai-provider-and-governed-retrieval/proposal.md).
- [add-durable-minimized-audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md).
- [add-reference-worker-scheduler-and-event-delivery](../add-reference-worker-scheduler-and-event-delivery/proposal.md).



## Impact de réalisation future

Composant/provider optionnel au-dessus du Kernel, déclaré par manifest et sélection explicite. Exposer uniquement ses contrats publics versionnés et écrire ses données via leur propriétaire. Conserver Django/PostgreSQL comme autorités, contexte tenant/scope, audit et gouvernance ; qualifier séparément dépendances, limites et mode dégradé. Ne pas imposer un provider, une bibliothèque ou une ressource métier encore non décidés.

## Critère de sortie de réalisation future

Outil non autorisé bloqué ; sortie modèle sans droit supplémentaire ; budget/échec visibles ; évaluations synthétiques.

## Décisions restant à valider

Catalogue d’outils, médiation/permissions et protocole d’évaluation/budgets ; résultat modèle sans pouvoir d’autorisation.
