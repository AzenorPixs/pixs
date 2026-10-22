# Conception — N05 : Réconciliation et réadmission après restauration

Préparation dédiée et rédaction du delta proposées validées explicitement par le développeur le 17 octobre 2026. Leur intégration au canon et la réalisation ne sont pas autorisées.

## Écart démontré

C16 restaure données et traitements avec réapplication des effacements/holds ; C10 possède les gouvernances ; C03/C01 possèdent sessions/secrets ; N01 possède les décisions d’incident. Leurs conceptions ne définissent pas ensemble la remise en service d’un état antérieur : un snapshot peut précéder une révocation, un incident ou un effet déjà envoyé. Restaurer des données cohérentes ne démontre pas que les droits, matériaux de confiance ou effets différés sont encore admissibles.

Références : [backup-disaster-recovery #3/#4](../../../openspec/specs/backup-disaster-recovery/spec.md), [authentication #3](../../../openspec/specs/authentication/spec.md), [identity-assurance #4](../../../openspec/specs/identity-assurance/spec.md), [C16](../../../openspec/changes/add-upgrade-backup-and-restore-contracts/design.md), [C09](../../../openspec/changes/add-reference-worker-scheduler-and-event-delivery/design.md), [N01](../../../openspec/changes/add-pbo-security-quarantine-and-revocation/design.md).

## Préparation recommandée

Créer `add-p0-post-restore-reconciliation-and-readmission`. Après restauration, maintenir l’état contrôlé sans trafic métier ni départ automatique des traitements non réconciliés. Construire un plan versionné couvrant mode/marqueur externe, composition, effacements/holds, sessions/identités, références et versions de secrets, incidents/quarantaines, idempotences, jobs, outbox et effets incertains réellement présents.

Chaque propriétaire fournit ses faits vérifiables et décisions. Si la fraîcheur d’un fait nécessaire manque, le plan marque l’écart et ne prétend pas que le snapshot l’établit. Une réponse perdue ou un effet externe antérieur ne se rejoue pas comme un travail neuf. Réadmission explicite après résultats des vérifications ; ni purge ni réactivation implicite.

## Décision de politique proposée

La restauration ne restaure pas automatiquement une confiance ou une assurance supérieure. La recette doit préciser comment obtenir les faits courants ou invalider/revalider les éléments concernés. Aucun journal externe universel, nouvel algorithme ou délai n’est imposé ici. L’exception Super Admin du canon est conservée : aucune extension à un worker ni preuve de fraîcheur fabriquée du fait d’une dérogation.

Prévoir une exigence ciblée de barrière de réadmission dans `backup-disaster-recovery`, avec scénarios de révocation postérieure au snapshot et d’effet déjà engagé ; compléter d’autres capacités seulement si la politique validée l’exige.

## Dépendances et critères futurs

C01/C03/C04/C05/C08/C09/C10/C15/C16/N01 avant intégration ; C17 exige la preuve avant qualification. C16 garde sauvegarde/restauration et choix d’outil ; N05 coordonne la réadmission. Snapshot antérieur à révocation/effacement/incident, perte de réponse d’un effet, référence de secret obsolète, marqueur incohérent, crash de réconciliation : résultats contrôlés et observables sans double effet ni faux droit rétabli.

## Plans et résultats à préciser avant réalisation

Le plan relie acteur, périmètre, version du point restauré, état contrôlé, propriétaires, faits requis, décisions confirmées/inconnues/refusées et autorisation de réadmission. Le format de stockage n’est pas une nouvelle API publique adoptée par ce document. Un checkpoint de réconciliation persiste les résultats et reprend sans relancer un effet confirmé.

Les marqueurs externes d’installation et de désactivation du compte fonctionnel restent distincts du snapshot PostgreSQL. La réactivation de secours garde l’authentification propre du compte et n’impose pas de MFA interdit par le canon. Une dérogation ne fabrique ni audit, ni fraîcheur, ni état appliqué. RPO/RTO restent déclarés par le déploiement, jamais déduits de ce plan.

## Portée de préparation et retour

Aucun code produit, secret, compte, service, dépendance, migration, données réelles, signature ou publication n’est manipulé par cette préparation. Les tâches restent futures et non cochées. Une évolution persistante ultérieure exige schéma/version, contrat de compatibilité et reprise/compensation revue ; aucun downgrade automatique ni purge implicite.

## Dépendances après audit transversal P0

[C01](../archive/2026-10-19-add-pbo-runtime-secret-provider/proposal.md), [C03](../archive/2026-10-21-add-initial-authentication-and-sessions/proposal.md), [C04](../archive/2026-10-21-integrate-runtime-authorization-and-super-admin/proposal.md), [C05](../archive/2026-10-21-add-durable-minimized-audit/proposal.md), [C08](../add-installation-and-first-configuration/proposal.md), [C09](../add-reference-worker-scheduler-and-event-delivery/proposal.md), [C10](../enforce-core-data-governance-and-lifecycle/proposal.md), [C15](../add-runtime-observability-and-operations/proposal.md), [C16](../add-upgrade-backup-and-restore-contracts/proposal.md), [N01](../add-pbo-security-quarantine-and-revocation/proposal.md).

Les conditions d’activation et la construction des résultats sont séparées de cet ordre de préparation ; aucun cycle inverse vers la recette finale.
