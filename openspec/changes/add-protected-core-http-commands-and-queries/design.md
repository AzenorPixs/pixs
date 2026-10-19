# Conception — C06

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 a été adopté et archivé le 18 octobre 2026 ; ses précisions normatives sont intégrées au canon. Les arbitrages propres au présent change restent à lever avant réalisation.

## État actuel vérifié

Constat : Plans OpenAPI et fabriques de réponses sont isolés ; les documents backend indiquent l’absence de routes Core complètes, pagination et idempotence générale.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/backend/api/README.md](../../../src/pixs/backend/api/README.md).
- [src/pixs/backend/api/contracts.py](../../../src/pixs/backend/api/contracts.py).
- [src/pixs/backend/api/success.py](../../../src/pixs/backend/api/success.py).
- [src/pixs/backend/local_test_composition.py](../../../src/pixs/backend/local_test_composition.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Exposer les services Core propriétaires par API versionnée et contrats publiés. Résoudre tenant du chemin, identité et autorisation avant exposition ; requêtes sans mutation, listes filtrées à la source. Lier clé d’idempotence, empreinte de requête, périmètre et résultat durable ; localiser les messages par catalogue.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Catalogue exact de routes et commandes, schémas/versions, contrat de curseur et conservation idempotence ; ne pas annoncer Bulk ou SDK optionnels.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [add-core-postgres-services](../add-core-postgres-services/proposal.md).
- [add-initial-authentication-and-sessions](../add-initial-authentication-and-sessions/proposal.md).
- [integrate-runtime-authorization-and-super-admin](../integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Parcours API sans frontend ; contrat et réponse concordants ; rejeu même clé/même contenu sans double effet, conflit explicite ; tenant du chemin canonique ; accès privé et inter-tenant refusés.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.

## Approfondissement issu de l’audit du 17 octobre 2026

Conception proposée sans implémentation. Ces contrats de travail ne modifient pas le canon ; tout changement normatif requiert son delta approuvé.

Pour O21, publier un document OpenAPI machine-readable versionné par majeure, associé aux routes et erreurs effectivement exposées. ApiContractPlan référence ce document logiquement mais ne contient pas sa publication ni sa conformité.

Relier chaque opération publique au contexte canonique, authentification, autorisation, pagination, idempotence et statut asynchrone applicable. Validation du document et tests contrat-serveur doivent détecter dérive ou surface privée exposée.

La construction du bundle d’entrée SDK appartient à O21 ; C06 possède contrat et serveur HTTP. Format de publication/version et compatibilité doivent être revus avant code, sans créer ici un nouveau change déjà couvert par ce lot.


Voir [audit individuel et limites des preuves](../archive/2026-10-18-define-first-installable-pbo-profile/audit-ne-94.json) et [rapport d’audit](../../../reports/audit-ne-94-2026-10-17/RAPPORT.md). Les tâches de réalisation restent non cochées.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T02 — PBO/PFO réellement servi par le paquet

Le serveur/bundle/routage et la frontière HTTP distribuée ne sont pas détaillés par un propriétaire commun. N04 dédié et deltas ciblés validés ; décisions de serveur/session/transport encore ouvertes.

Contrôles à intégrer : Navigation directe du shell via service livré ; Erreur API sans fallback HTML ; Hôtes/origines/en-têtes non fiables, CSRF si cookie ; Management et rôles non publics.

### T07 — Administration utile avec compte ordinaire

Les grandes rubriques existent ; il faut arrêter le catalogue minimal d’actions et prouver le parcours ordinaire, pas seulement celui du Super Admin. Compléter critères de C06/C13 et recette C17 ; aucun module métier ajouté.

Contrôles à intégrer : Créer identité/utilisateur/groupe/appartenance selon droits ; Lire/modifier ACL sans élargir tenant/scope ; Accès interdit invisible et inexécutable ; API utilisable sans PFO.

### T08 — Audit exhaustif du panneau et navigation SPA

L’audit de chaque activité du panneau inclut navigation/lecture ; des logs ou un acquittement mémoire n’en prouvent pas la persistance. Compléter protocole C05/C13 et critères de volumétrie/minimisation C15 ; préserver exception Super Admin.

Contrôles à intégrer : Panne sink avant affichage/action ordinaire refusée selon contrat ; Dérogation root sans audit annoncé à tort ; Navigation SPA reliée à une preuve serveur et aucune donnée sensible copiée.

### T09 — Contexte tenant et réponse retardée du navigateur

L’invalidation est prévue ; les réponses en vol, onglets et changements de session doivent être inclus dans le contrat de concurrence UI. Compléter C11 et sa recette ; pas d’offline, cache distribué ou client natif imposé.

Contrôles à intégrer : Réponse du tenant précédent n’alimente pas la vue courante ; Déconnexion et révocation invalident contexte ; Identifiant/header fourni ne remplace pas le tenant canonique.

### T10 — Mutation, audit, idempotence et outbox

Les composants prévoient chacun leur partie ; la frontière transactionnelle et l’échec avant/après commit doivent être explicitement communs. Compléter contrats C05/C06/C09 avec refus distincts et résultat réconcilié ; pas de nouveau broker.

Contrôles à intégrer : Rollback sans événement publié ; Commit puis réponse perdue restituant résultat idempotent ; Double livraison sans double effet propriétaire ; Refus auditable sans mutation métier.

### T14 — PZT/DNS gérés sans exécution PA

La table 193 clauses reste conditionnelle et exige revue par rôle avant adoption ; classement exécutant ne retire pas les clauses PBO de gestion. Conserver C14 comme propriétaire, contrats/schémas/valeurs administrées explicités avant code ; aucun nouveau change exécutant sélectionné.

Contrôles à intégrer : Modules essentiels présents même réseau désactivé ; État souhaité distinct de mesure/appliqué ; Suffixe/droits/conflits des données gérées conformes ; Aucune publication DNS/réseau ni modification hôte inventée.

### T15 — Langues, thèmes et accessibilité de tous les parcours

Les parcours CLI, erreurs API, management et secours font aussi partie des textes utilisateur ; couverture ne se limite pas à la page du shell. Compléter la matrice C12/C17 et les contrats de messages ; codes stables non localisés.

Contrôles à intégrer : Deux navigateurs déclarés, clavier/zoom/lecteur d’écran ; Erreurs et confirmations d’installation/exploitation localisées ; Thème/session/tenant sans fuite d’état.

Voir [audit transversal durable](../archive/2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.
