# Conception — C16

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 formalise le profil ; ses précisions normatives restent proposées tant qu’elles ne sont pas approuvées/adoptées.

## État actuel vérifié

Constat : Des migrations bornées existent, mais aucune recette de restauration produit cohérente avec gouvernance, travaux et composition n’est démontrée.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/backend/README.md](../../../src/pixs/backend/README.md).
- [src/pixs/backend/models.py](../../../src/pixs/backend/models.py).
- [openspec/specs/backup-disaster-recovery/spec.md](../../specs/backup-disaster-recovery/spec.md).
- [openspec/specs/migrations/spec.md](../../specs/migrations/spec.md).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Versionner contrats/plans de migration, ordre exclusif, reprise et contraction séparée. Sauvegarder les périmètres réellement livrés puis restaurer isolément, réappliquer effacements/holds avant exposition. Retour arrière applicatif seulement si matrice compatible ; sinon restauration explicite confirmée/auditée.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

RPO/RTO et rétention du profil, stratégie de sauvegarde et origines/version compatibles ; ne pas sélectionner un outil ni rétrograder une base implicitement.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [add-installation-and-first-configuration](../add-installation-and-first-configuration/proposal.md).
- [add-reference-worker-scheduler-and-event-delivery](../add-reference-worker-scheduler-and-event-delivery/proposal.md).
- [enforce-core-data-governance-and-lifecycle](../enforce-core-data-governance-and-lifecycle/proposal.md).
- [add-runtime-observability-and-operations](../add-runtime-observability-and-operations/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Installation et mise à niveau interrompues puis reprises ; contraction prématurée refusée ; origine compatible explicitée ; restauration mesurée sans résurrection ; rollback seulement si matrice le prouve, sinon restauration confirmée ; aucune downgrade automatique.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.
