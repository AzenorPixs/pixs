# Conception — C04

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 formalise le profil ; ses précisions normatives restent proposées tant qu’elles ne sont pas approuvées/adoptées.

## État actuel vérifié

Constat : authorize et source-filter-plan-v1 fournissent un PDP et un plan préparatoires ; l’intégration PEP Django et l’exception Super Admin opérationnelle ne sont pas démontrées.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/core/authz/decision.py](../../../src/pixs/core/authz/decision.py).
- [src/pixs/core/authz/filter_plan.py](../../../src/pixs/core/authz/filter_plan.py).
- [src/pixs/core/authz/snapshot.py](../../../src/pixs/core/authz/snapshot.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Reconnaître le seul compte fonctionnel authentifié à la frontière runtime, avec accords tenant explicites. Conserver les profils structurels sans privilège. Pour comptes ordinaires, appliquer DENY/ALLOW/refus par défaut et obligations PEP ; filtrer à la source avant pagination. Propager acteur initial et périmètre sans credentials délégués.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Reconnaissance du compte unique, persistance des accords tenant, interprétation des obligations et protocole de dérogation/audit avec C05 ; conception transversale à revoir avant modification du runtime.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [add-core-postgres-services](../add-core-postgres-services/proposal.md).
- [add-initial-authentication-and-sessions](../add-initial-authentication-and-sessions/proposal.md).

- [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md) : dépendance renforcée après revue des obligations d’audit.

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

DENY/ALLOW et refus par défaut ordinaires ; tenant non accordé refusé même au Super Admin ; tenant accordé et dérogations testés ; même sémantique API/CLI/panneau/asynchrone ; obligations PEP réellement honorées.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.
