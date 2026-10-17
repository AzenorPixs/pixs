# Conception — C12

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 formalise le profil ; ses précisions normatives restent proposées tant qu’elles ne sont pas approuvées/adoptées.

## État actuel vérifié

Constat : Catalogues anglais/français et thèmes du shell existent ; les erreurs API comportent encore des textes fixes et les primitives partagées ne sont pas complètement qualifiées.

Sources consultées et empreintes recoupées avec la matrice :

- [frontend/src/catalogs.js](../../../frontend/src/catalogs.js).
- [frontend/src/theme.css](../../../frontend/src/theme.css).
- [frontend/README.md](../../../frontend/README.md).
- [src/pixs/backend/api/README.md](../../../src/pixs/backend/api/README.md).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Étendre les catalogues par propriétaire, canon anglais complet, préférences et formats sans altérer les valeurs métier. Stabiliser tokens/primitives publiques nécessaires aux parcours P0, clair/sombre, noms/états natifs et focus. Exécuter unités dans les deux navigateurs et compléter par vérifications manuelles WCAG.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Surface publique des primitives, résolution préférences/périmètre/installation et protocole manuel d’accessibilité ; pas de bibliothèque UI nouvelle implicite.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [add-protected-core-http-commands-and-queries](../add-protected-core-http-commands-and-queries/proposal.md).
- [compose-modular-frontend-with-core-api](../compose-modular-frontend-with-core-api/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Aucun texte utilisateur hors catalogue propriétaire ; build refuse incohérences ; unités dans Chromium et Firefox headless ; parcours manuels et outillés WCAG 2.2 AA ; pas de substitution par build ou Node.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.
