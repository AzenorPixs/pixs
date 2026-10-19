# Conception préparatoire — secrets d’amorçage liés à l’hôte et au TPM2

## Statut et autorisation

PRÉPARATION_DOCUMENTAIRE, 19 octobre 2026. Le choix d’architecture et la rédaction des cadrages, spécifications et changes sont autorisés par le développeur. Les tâches d’implémentation, de qualification matérielle et de récupération restent non exécutées et demandent un mandat de réalisation distinct. Ce dossier ne reprend pas le RUN CISMP3 livré.

## Couverture existante et manque constaté

| Source vérifiée | Déjà présent | Complément du présent change |
| --- | --- | --- |
| [PROJECT.md §26](../../../PROJECT.md#26-configuration) et [TECHNICAL.md §21](../../../TECHNICAL.md#21-secrets) | Références externes, provider indépendant du stockage, valeurs runtime | Choix de protection pour l’amorçage local, reprise après perte d’hôte |
| [secrets-providers](../../specs/secrets-providers/spec.md) | Identité de workload, durée de vie, révocation, échec fermé, C01 systemd | Mode combiné explicite, préconditions matérielles et preuves cryptographiques |
| [reference-composition](../../specs/reference-composition/spec.md) | Profil Debian local et adoption C01 | Critères d’admission en production pour la protection et le secours |
| [backup-disaster-recovery](../../specs/backup-disaster-recovery/spec.md) | Objectifs de reprise, périmètres séparés, tests isolés, restauration autorisée | Perte du TPM d’origine, secours indépendant et remplacement des liaisons |
| [Archive C01](../archive/2026-10-19-add-pbo-runtime-secret-provider/STATISTIQUES.md) et [harnais existant](../../../tests/integration/test_c01_systemd_harness.py) | Transport et cycle de vie fonctionnels avec fixtures publiques | Aucune preuve `host+tpm2` ni récupération de production déduite |

Les recherches dans les cadrages, le canon et les changes actifs n’ont pas trouvé de contrat explicite équivalent. Les profils TPM/attestation PA/PZT et le coffre des clients natifs ont d’autres finalités ; leurs clés et identités ne sont pas réutilisées pour les secrets PBO.

## Décision d’architecture

Le profil d’amorçage local protège ses sources persistantes par le mode combiné `host+tpm2`, puis utilise le transport C01 `LoadCredentialEncrypted`. Le choix est explicite : un mode automatique ne prouve pas que les deux facteurs ont été utilisés. Les sources chiffrées restent hors dépôt, paquet et image ; les valeurs déchiffrées ne sont remises qu’aux consommateurs de confiance. Les vérifications UID/unité, politique, références, validités, audit durable, rotation par arrêt attesté et révocation C01 restent applicables.

Le mode combiné requiert la clé hôte de l’installation et le TPM d’origine. Une copie des seuls fichiers chiffrés, même accompagnée de la clé hôte, ne constitue donc pas un plan de reprise sur une autre machine. Les fichiers de fixtures sous `output/` de C01 ne sont ni un emplacement d’exploitation ni du matériel de secours.

L’absence ou l’incompatibilité du TPM laisse la dimension de protection non qualifiée et bloque l’admission sous ce profil. Une autre protection doit faire l’objet d’un choix explicite et d’une qualification distincte ; ce dossier ne sélectionne ni repli `host` seul, ni mode `null`, ni nouveau composant matériel. Un TPM physique, un TPM transmis et un vTPM ont des frontières de confiance distinctes à déclarer.

## Politique de démarrage et limites de protection

La réalisation précisera les versions supportées, le type de TPM, la persistance/protection de la clé hôte, les mesures de démarrage et la politique PCR ou signée réellement sélectionnée. Aucun numéro PCR ni effet de Secure Boot n’est réputé validé ici. Les mises à jour légitimes et les changements de politique doivent rester compatibles avec une reprise contrôlée, sans désactiver les vérifications pour redémarrer.

La protection vise notamment la lecture de copies de stockage et la modification des credentials. Elle ne démontre pas la résistance à un administrateur de l’hôte compromis, à la lecture mémoire du consommateur ou à un hyperviseur contrôlant un vTPM. La protection du swap, des dumps et des diagnostics fait partie de la revue du déploiement ; aucune garantie matérielle globale n’est déduite du seul nom TPM2.

## Récupération sans la machine d’origine

Le plan de secours déclare les secrets récupérables par réémission auprès de leur autorité et ceux nécessitant un matériel de récupération protégé conservé séparément. L’autorité, les accès, le mécanisme de protection et les objectifs RPO/RTO restent à préciser avant réalisation. Une clé de secours stockée en clair avec la sauvegarde chiffrée est incompatible avec ce plan. Aucun coffre distant n’est imposé au profil initial local par cette préparation.

Le scénario décisif part de l’indisponibilité complète de l’ancien hôte et du TPM. Un opérateur système habilité reprovisionne les références nécessaires, chiffre pour les facteurs du nouvel hôte et met à jour les politiques/liaisons sous contrôle et audit. La procédure ne prétend pas exporter une clé TPM non exportable ni rendre l’ancien ciphertext portable. Elle conserve les preuves et applique les révocations courantes ; une ancienne sauvegarde ne réactive pas une version interdite ou une identité clonée.

Le secret Django de signature et les credentials PostgreSQL n’ont pas nécessairement les mêmes effets de réémission : sessions/signatures existantes et accès à la base doivent être traités par leurs contrats propriétaires, sans promesse de reprise transparente. Aucun accès à PostgreSQL n’est requis pour obtenir son propre credential initial ou pour démarrer le mécanisme de secours nécessaire à cette obtention.

## Intégration et responsabilités futures

- C01 reste le socle livré du transport et de l’audit local ; pas de réarchivage.
- [C08](../add-installation-and-first-configuration/proposal.md) intègre les préconditions et l’admission du runtime.
- [C16](../add-upgrade-backup-and-restore-contracts/proposal.md) consomme le contrat de récupération ; [N05](../add-p0-post-restore-reconciliation-and-readmission/proposal.md) conserve la réconciliation de confiance avant réadmission.
- [C18](../build-first-pbo-pfo-debian-package/proposal.md) intègre sans secret réel les préconditions de distribution ; [C17](../qualify-first-pbo-composition/proposal.md) qualifie l’artefact réel ; [C19](../publish-first-qualified-pbo-release/proposal.md) contrôle la preuve finale. Ce sont des consommateurs de preuves, pas des dépendances inverses bloquant la préparation du présent contrat.
- Le [coffre distribué](../add-distributed-runtime-secret-vault/proposal.md) est une extension conditionnelle, sans activation implicite du P0 local.

La réadmission ne change pas les règles canoniques du Super Admin. L’autorité système de gestion des clés n’est pas une permission métier, et une dérogation applicative ne fabrique ni déchiffrement ni preuve matérielle absente.

## Barrières avant réalisation

Restent à décider : plateformes et versions effectives, matériel disponible, politique de démarrage/mise à jour, chemins et permissions de production, autorité de reprovisionnement et protection du secours, rétention, RPO/RTO et effets de rotation propres à chaque secret. Ces paramètres ne sont pas remplis par des valeurs de fixtures. Les fichiers d’implémentation et les essais hôte seront présentés dans un mandat distinct.

## Validation future et retour

La matrice couvre déchiffrement sur hôte autorisé, refus avec TPM ou clé hôte incorrects/manquants, ciphertext altéré, politique de démarrage incompatible, mise à jour autorisée, rotation/révocation et récupération sur nouvel hôte avec ancien TPM inaccessible. Elle mesure les objectifs de reprise et vérifie l’absence de secret dans les preuves. Un échec garde l’état non prêt et conserve les éléments de diagnostic ; aucun repli automatique ou réactivation d’ancienne version n’est un retour acceptable.

## Sources primaires

Consultation du 19 octobre 2026 : [systemd-creds 257](https://www.freedesktop.org/software/systemd/man/257/systemd-creds.html), modes `host+tpm2`, `null`, politiques PCR et politiques signées. La version de documentation est un support de conception, pas une qualification de la plateforme cible.
