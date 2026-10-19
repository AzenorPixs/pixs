# Conception — C11

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 a été adopté et archivé le 18 octobre 2026 ; ses précisions normatives sont intégrées au canon. Les arbitrages propres au présent change restent à lever avant réalisation.

## État actuel vérifié

Constat : Le shell est autonome ; les facettes frontend sont des déclarations immuables sans composition récursive de modules opérationnelle.

Sources consultées et empreintes recoupées avec la matrice :

- [frontend/src/main.js](../../../frontend/src/main.js).
- [frontend/README.md](../../../frontend/README.md).
- [src/pixs/kernel/frontend_contribution_declarations.py](../../../src/pixs/kernel/frontend_contribution_declarations.py).
- [src/pixs/kernel/manifest/models.py](../../../src/pixs/kernel/manifest/models.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Composer au build depuis manifests et contrats publics, sans registre/lifecycle frontend parallèle. Résoudre récursion et dépendances, collisions et façades ; le shell fournit session/contexte et consomme les API. Une intention UI ne devient un effet confirmé qu’après réponse serveur ; invalidation sous tenant courant.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

API publique du shell et points de contribution, frontières de build et catalogue de routes à formaliser ; conserver JavaScript existant sans conversion TypeScript implicite ni téléchargement runtime.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [add-protected-core-http-commands-and-queries](../add-protected-core-http-commands-and-queries/proposal.md).
- [activate-reference-runtime-composition](../activate-reference-runtime-composition/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Module et sous-module ajoutés sans éditer le shell ; collision et import privé refusés ; navigation/session/tenant corrects ; annulation ou refus de mutation visibles ; ordre identique entre développement et artefact.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.


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

### T14 — PZT/DNS gérés sans exécution PA

La table 193 clauses reste conditionnelle et exige revue par rôle avant adoption ; classement exécutant ne retire pas les clauses PBO de gestion. Conserver C14 comme propriétaire, contrats/schémas/valeurs administrées explicités avant code ; aucun nouveau change exécutant sélectionné.

Contrôles à intégrer : Modules essentiels présents même réseau désactivé ; État souhaité distinct de mesure/appliqué ; Suffixe/droits/conflits des données gérées conformes ; Aucune publication DNS/réseau ni modification hôte inventée.

Voir [audit transversal durable](../archive/2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.
