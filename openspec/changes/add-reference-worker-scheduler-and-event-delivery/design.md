# Conception — C09

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 formalise le profil ; ses précisions normatives restent proposées tant qu’elles ne sont pas approuvées/adoptées.

## État actuel vérifié

Constat : JobRecord et des primitives transactionnelles Bulk existent ; ils ne fournissent pas le worker et scheduler généraux ni une livraison d’événements qualifiée.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/backend/models.py](../../../src/pixs/backend/models.py).
- [src/pixs/kernel/jobs.py](../../../src/pixs/kernel/jobs.py).
- [src/pixs/kernel/event_registration.py](../../../src/pixs/kernel/event_registration.py).
- [src/pixs/backend/bulk_runtime_repository.py](../../../src/pixs/backend/bulk_runtime_repository.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Réutiliser les structures applicables sans généraliser un bail Bulk au scheduler. Exécuter jobs et publication après commit via mêmes contrats, persistance PostgreSQL et contexte réautorisé. Lease persistant et clôture de péremption empêchent l’ancien scheduler d’agir ; reprises, retries et états terminaux sont inspectables.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Contrats d’exécution, baux/échéances/fencing, réveil et publication à qualifier. Aucun broker externe ou dépendance ajoutée implicitement ; tout consommateur choisi doit satisfaire sa conformité.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [integrate-runtime-authorization-and-super-admin](../integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md).
- [add-protected-core-http-commands-and-queries](../add-protected-core-http-commands-and-queries/proposal.md).
- [activate-reference-runtime-composition](../activate-reference-runtime-composition/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Deux schedulers → un détenteur admissible ; ancien détenteur rejeté ; crash/reprise sans double effet ; événement jamais avant commit ; révocation avant exécution respectée ; drain borné.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.

## Approfondissement issu de l’audit du 17 octobre 2026

Conception proposée sans implémentation. Ces contrats de travail ne modifient pas le canon ; tout changement normatif requiert son delta approuvé.

Pour O21, fournir schémas publics d’événements et versions compatibles avec les enveloppes réellement émises. Les représentations Python déclaratives et records Bulk existants ne démontrent pas un catalogue machine-readable des contrats publics.

Lier producteur propriétaire, type/version, contexte autorisé, corrélation, idempotence, politique de compatibilité et schéma du payload. Ne pas exposer modèles privés ou données de sécurité dans le bundle générable.

C09 conserve émission post-commit, livraison/rejeu et checkpoints ; O21 génère les SDK depuis les schémas publiés. Contrats manquants/divergents bloquent cette génération, sans dépendance inverse vers O21.


Voir [audit individuel et limites des preuves](../define-first-installable-pbo-profile/audit-ne-94.json) et [rapport d’audit](../../../reports/audit-ne-94-2026-10-17/RAPPORT.md). Les tâches de réalisation restent non cochées.
