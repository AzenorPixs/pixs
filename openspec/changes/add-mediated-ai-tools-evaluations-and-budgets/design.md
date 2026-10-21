# Conception — O25

## Statut

PRÉPARATION_DOCUMENTAIRE_CONDITIONNELLE. Le dossier est demandé ; ses choix encore ouverts et son implémentation ne sont pas approuvés implicitement. La présence des fichiers ne signifie pas prêt à coder.

## Contexte actuel

La capacité est un candidat du canon ; la revue de présence des sources et la matrice ne démontrent pas une réalisation opérationnelle. Les lignes NE historiques ont été auditées le 17 octobre 2026 ; voir les constats individuels ci-dessous, sans qualification runtime.

Ce dossier référence 4 lignes NE dans la matrice historique. Leur audit statique est maintenant documenté ci-dessous ; les barrières de choix et de qualification avant réalisation restent applicables.

Sources et périmètres consultés :

- [README.md](../../../README.md).
- [src/pixs/kernel/composition.py](../../../src/pixs/kernel/composition.py).
- [src/pixs/backend/README.md](../../../src/pixs/backend/README.md).

## Architecture et frontières

Composant/provider optionnel au-dessus du Kernel, déclaré par manifest et sélection explicite. Exposer uniquement ses contrats publics versionnés et écrire ses données via leur propriétaire. Conserver Django/PostgreSQL comme autorités, contexte tenant/scope, audit et gouvernance ; qualifier séparément dépendances, limites et mode dégradé. Ne pas imposer un provider, une bibliothèque ou une ressource métier encore non décidés.

Périmètre propre à ce lot : Outils sous permissions et médiation, prompts/évaluations versionnés, budgets/audit.

## Choix déjà fixés et alternatives

Les décisions validées dans les contrats sources sont conservées, y compris formats, algorithmes, valeurs, rôles et alternatives rejetées. Elles ne sont pas rouvertes sous prétexte d’un nouveau dossier. Les plafonds d’un auxiliaire, collecteur, validateur ou travail ne deviennent pas un budget général du PA/PBO.

Les modalités concrètes encore ouvertes ne reçoivent pas de valeur de défaut inventée. Une bibliothèque, un provider ou une dépendance présent dans DEVOPS n’est ni sélectionné ni qualifié. Les références normatives complètes sont dans requirements.md ; les mentions historiques qu’elles contiennent ne décrivent pas des effets réalisés pendant cette préparation.

## Barrières de conception avant réalisation

Catalogue d’outils, médiation/permissions et protocole d’évaluation/budgets ; résultat modèle sans pouvoir d’autorisation.

Ces barrières n’empêchent pas la rédaction conditionnelle du dossier. Avant tout code, les choix ayant un impact réel sur sécurité, périmètre, compatibilité, exploitation ou ressources devront être soumis avec conséquences et recommandation ; pour PA/PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages. Les paramètres déjà décidés sont à qualifier, pas à remplacer par une nouvelle décision supposée.

## Dépendances et interfaces

- [add-declared-ai-provider-and-governed-retrieval](../add-declared-ai-provider-and-governed-retrieval/proposal.md).
- [add-durable-minimized-audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md).
- [add-reference-worker-scheduler-and-event-delivery](../add-reference-worker-scheduler-and-event-delivery/proposal.md).



Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent explicitement incomplètes tant que les obligations manquent.

## Vérification future

Source de vérité, isolation tenant/scope, refus sans permission, classification/rétention, retries/reprise et révocation ; contrat du provider sélectionné sur dépendance réelle, tests navigateur si interface web et audit manuel lorsque requis.

Sortie du lot : Outil non autorisé bloqué ; sortie modèle sans droit supplémentaire ; budget/échec visibles ; évaluations synthétiques.

Exercer tous les scénarios et clauses applicables des blocs sources, y compris renvois normatifs ; un scénario non applicable doit être motivé par le profil réel. Les contrôles applicatifs suivent l’exception Super Admin du canon dans son seul périmètre, sans fabriquer audit, mesure, signature ou effet absent.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données/états doit préciser propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation/restauration. Aucun retour arrière destructeur, remise à zéro, arrêt de service ou changement de droits implicites.

## Limites du dossier

Pas de PASS actuel ni d’achèvement produit revendiqué. L’autorisation de préparation ne permet ni d’activer la capacité dans P0 ni d’utiliser un compte connecté, publier un artefact ou envoyer une notification réelle.

## Approfondissement issu de l’audit du 17 octobre 2026

Conception proposée sans implémentation. Ces contrats de travail ne modifient pas le canon ; tout changement normatif requiert son delta approuvé.

Le catalogue d’outils relie entrée/sortie versionnées, propriétaire et Command publique. La proposition du modèle passe par validation de schéma et autorisation courante ; aucun appel direct aux tables, au shell ou aux services privés n’est implicite.

Versionner prompts/corpus et réserver le budget via O15 avant appel ; relier opération fournisseur, réponse, coût confirmé/inconnu et consommation réconciliée. Une panne ou réponse perdue ne justifie ni appel doublé ni coût fictif ; budget épuisé interdit la poursuite selon canon.

Ajouter O15 comme dépendance ferme ; O24 fournit adapter/récupération, C05 audit minimisé et C09 exécution durable. Fixer outils autorisés, schémas de médiation et seuils d’évaluation avant code ; aucune exécution d’outil produit pendant la préparation.

### Exigences auditées et preuves de sortie futures

| Référence canonique | Statut statique après audit | Critère à démontrer |
|---|---|---|
| [ai-agents #1](../../../openspec/specs/ai-agents/spec.md#L11) | ND | Provider déclaré et sélection explicite ; présence sans activation et absence testées. |
| [ai-agents #2](../../../openspec/specs/ai-agents/spec.md#L28) | ND | Filtrage avant récupération, minimisation et résidence ; refus hors scope sur corpus synthétique. |
| [ai-agents #3](../../../openspec/specs/ai-agents/spec.md#L41) | ND | Tout effet proposé passe par une Command propriétaire autorisée ; outil non déclaré refusé. |
| [ai-agents #4](../../../openspec/specs/ai-agents/spec.md#L53) | ND | Prompts et corpus versionnés, réservation O15 avant appel, arrêt au budget et coût réconcilié sans double imputation. |

Voir [audit individuel et limites des preuves](../archive/2026-10-18-define-first-installable-pbo-profile/audit-ne-94.json) et [rapport d’audit](../../../reports/audit-ne-94-2026-10-17/RAPPORT.md). Les tâches de réalisation restent non cochées.


## Dépendance issue de l’audit

- [add-entitlements-and-atomic-quota-reservations](../add-entitlements-and-atomic-quota-reservations/proposal.md) — dépendance explicitée après audit du 17 octobre 2026.
