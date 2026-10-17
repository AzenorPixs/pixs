# Conception — C02

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 formalise le profil ; ses précisions normatives restent proposées tant qu’elles ne sont pas approuvées/adoptées.

## État actuel vérifié

Constat : User, DigitalIdentity, liaisons, groupes et appartenances sont des représentations mémoire. Les modèles backend persistants existants ne constituent pas les services Core complets.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/core/identity/models.py](../../../src/pixs/core/identity/models.py).
- [src/pixs/core/identity/groups.py](../../../src/pixs/core/identity/groups.py).
- [src/pixs/core/identity/tenant_membership.py](../../../src/pixs/core/identity/tenant_membership.py).
- [src/pixs/backend/models.py](../../../src/pixs/backend/models.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Conserver la distinction User/DigitalIdentity et les UUIDv7 ; porter les données Core dans PostgreSQL avec propriétaire explicite, contraintes et services publics. Séparer scopes/platform/tenant, rôles, ACL et permissions ; créer les migrations après revue du schéma, sans écrire les tables d’un autre composant.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Schéma/table propriétaire, contrats de services et concurrence ; modèle de persistance des accords tenant du Super Admin à coordonner avec C04. Aucune réutilisation implicite du modèle User de Django comme fusion de l’identité Pixs.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [define-first-installable-pbo-profile](../define-first-installable-pbo-profile/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Contraintes UUIDv7 et cardinalités exercées sur PostgreSQL ; séparation tenants/scopes ; accès inter-module par contrats ; migrations et concurrence testées.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.
