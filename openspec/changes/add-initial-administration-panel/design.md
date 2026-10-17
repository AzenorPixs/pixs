# Conception — C13

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 formalise le profil ; ses précisions normatives restent proposées tant qu’elles ne sont pas approuvées/adoptées.

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
