# Conception — C13

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 a été adopté et archivé le 18 octobre 2026 ; ses précisions normatives sont intégrées au canon. Les arbitrages propres au présent change restent à lever avant réalisation.

## État actuel vérifié

Constat : La route UI actuelle affiche le shell de développement ; elle ne démontre pas un panneau /admin/ de première configuration et d’administration Core.

Sources consultées et empreintes recoupées avec la matrice :

- [frontend/src/main.js](../../../frontend/src/main.js).
- [frontend/README.md](../../../frontend/README.md).
- [src/pixs/backend/api/README.md](../../../src/pixs/backend/api/README.md).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Construire le panneau avec les mêmes API/Commands que les autres façades ; conserver droits ordinaires et exception Super Admin dans son seul périmètre. Route initiale /admin/ administrable sans collision ; santé réservée selon niveau ; première configuration réservée au compte fonctionnel ; états/messages et erreurs localisés.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Catalogue exact d’écrans/actions, transitions et changement de route sous contrats publics ; ne pas activer implicitement l’administration Django ni créer un second modèle de permissions.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [add-installation-and-first-configuration](../add-installation-and-first-configuration/proposal.md).
- [enforce-core-data-governance-and-lifecycle](../enforce-core-data-governance-and-lifecycle/proposal.md).
- [compose-modular-frontend-with-core-api](../compose-modular-frontend-with-core-api/proposal.md).
- [complete-shared-ui-i18n-and-accessibility](../complete-shared-ui-i18n-and-accessibility/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Installation → connexion Super Admin → première configuration → NORMAL → administration ordinaire ; changement route sans collision et ancienne route refusée/auditée ; état santé sans credential ; aucun second compte ni transfert de privilège.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T06 — Marqueurs externes et états PostgreSQL

Marqueur d’installation et marqueur de désactivation Super Admin ont des fonctions différentes et ne sont pas une transaction atomique avec PostgreSQL. Compléter C08 et les contrats C03/C04/C09 ; N05 vérifie le rapprochement après restauration.

Contrôles à intégrer : Commit base avant marqueur : reprise sans second compte ; Marqueur absent/invalide interdit NORMAL sans relancer INSTALLER ; Désactivation non dérogée refuse nouvelles actions/reprises, transaction engagée préservée ; Secours propre sans MFA imposé.

### T07 — Administration utile avec compte ordinaire

Les grandes rubriques existent ; il faut arrêter le catalogue minimal d’actions et prouver le parcours ordinaire, pas seulement celui du Super Admin. Compléter critères de C06/C13 et recette C17 ; aucun module métier ajouté.

Contrôles à intégrer : Créer identité/utilisateur/groupe/appartenance selon droits ; Lire/modifier ACL sans élargir tenant/scope ; Accès interdit invisible et inexécutable ; API utilisable sans PFO.

### T08 — Audit exhaustif du panneau et navigation SPA

L’audit de chaque activité du panneau inclut navigation/lecture ; des logs ou un acquittement mémoire n’en prouvent pas la persistance. Compléter protocole C05/C13 et critères de volumétrie/minimisation C15 ; préserver exception Super Admin.

Contrôles à intégrer : Panne sink avant affichage/action ordinaire refusée selon contrat ; Dérogation root sans audit annoncé à tort ; Navigation SPA reliée à une preuve serveur et aucune donnée sensible copiée.

### T09 — Contexte tenant et réponse retardée du navigateur

L’invalidation est prévue ; les réponses en vol, onglets et changements de session doivent être inclus dans le contrat de concurrence UI. Compléter C11 et sa recette ; pas d’offline, cache distribué ou client natif imposé.

Contrôles à intégrer : Réponse du tenant précédent n’alimente pas la vue courante ; Déconnexion et révocation invalident contexte ; Identifiant/header fourni ne remplace pas le tenant canonique.

### T15 — Langues, thèmes et accessibilité de tous les parcours

Les parcours CLI, erreurs API, management et secours font aussi partie des textes utilisateur ; couverture ne se limite pas à la page du shell. Compléter la matrice C12/C17 et les contrats de messages ; codes stables non localisés.

Contrôles à intégrer : Deux navigateurs déclarés, clavier/zoom/lecteur d’écran ; Erreurs et confirmations d’installation/exploitation localisées ; Thème/session/tenant sans fuite d’état.

Voir [audit transversal durable](../archive/2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.
