# Conception — C14

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 formalise le profil ; ses précisions normatives restent proposées tant qu’elles ne sont pas approuvées/adoptées.

## État actuel vérifié

Constat : Le canon impose les modules PZT et DNS essentiels ; aucun module produit PZT/DNS n’est identifié aux emplacements consultés. La spécification seule ne les fournit pas.

Sources consultées et empreintes recoupées avec la matrice :

- [openspec/specs/pzt/spec.md](../../specs/pzt/spec.md).
- [openspec/specs/reference-runtime/spec.md](../../specs/reference-runtime/spec.md).
- [README.md](../../../README.md).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Composer deux responsabilités de gestion PBO propriétaires via les mécanismes communs ; manifests et contrats exacts après décision d’identifiants. Conserver configuration souhaitée, versions et états d’absence d’exécutant ; appliquer les choix validés pertinents à la configuration. N’engager aucun PA, service DNS ou réseau non sélectionné, ni canal de substitution.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Identifiants canoniques et contrats de gestion, sous-modules et schémas ; recouper chaque clause applicable de la table C00. Toute obligation active non conditionnelle rejoint le chemin critique ; aucune exemption supposée.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [define-first-installable-pbo-profile](../define-first-installable-pbo-profile/proposal.md).
- [add-core-postgres-services](../add-core-postgres-services/proposal.md).
- [integrate-runtime-authorization-and-super-admin](../integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md).
- [add-protected-core-http-commands-and-queries](../add-protected-core-http-commands-and-queries/proposal.md).
- [compose-modular-frontend-with-core-api](../compose-modular-frontend-with-core-api/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Modules composés même réseau désactivé ; absence essentielle bloquante ; configuration/visualisation/supervision honnêtes ; aucune mesure ni application réseau inventée ; aucun canal PBO–PA de substitution ; chaque clause conservée, motivée ou renvoyée vers évolution normative approuvée.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.
