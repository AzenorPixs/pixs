# Conception — O26

## Statut

PRÉPARATION_DOCUMENTAIRE_CONDITIONNELLE. Le dossier est demandé ; ses choix encore ouverts et son implémentation ne sont pas approuvés implicitement. La présence des fichiers ne signifie pas prêt à coder.

## Contexte actuel

La capacité est un candidat du canon ; la revue de présence des sources et la matrice ne démontrent pas une réalisation opérationnelle. Les lignes NE historiques ont été auditées le 17 octobre 2026 ; voir les constats individuels ci-dessous, sans qualification runtime.

Ce dossier référence 4 lignes NE dans la matrice historique. Leur audit statique est maintenant documenté ci-dessous ; les barrières de choix et de qualification avant réalisation restent applicables.

Sources et périmètres consultés :

- [README.md](../../../README.md).
- [src/pixs/kernel/composition.py](../../../src/pixs/kernel/composition.py).
- [src/pixs/backend/README.md](../../../src/pixs/backend/README.md).

## Architecture et frontières

Composant/provider optionnel au-dessus du Kernel, déclaré par manifest et sélection explicite. Exposer uniquement ses contrats publics versionnés et écrire ses données via leur propriétaire. Conserver Django/PostgreSQL comme autorités, contexte tenant/scope, audit et gouvernance ; qualifier séparément dépendances, limites et mode dégradé. Ne pas imposer un provider, une bibliothèque ou une ressource métier encore non décidés.

Périmètre propre à ce lot : Mécanisme d'intégrité, chaînage/provenance/export/conservation ; confidentialité/rétention/effacement conservés.

## Choix déjà fixés et alternatives

Les décisions validées dans les contrats sources sont conservées, y compris formats, algorithmes, valeurs, rôles et alternatives rejetées. Elles ne sont pas rouvertes sous prétexte d’un nouveau dossier. Les plafonds d’un auxiliaire, collecteur, validateur ou travail ne deviennent pas un budget général du PA/PBO.

Les modalités concrètes encore ouvertes ne reçoivent pas de valeur de défaut inventée. Une bibliothèque, un provider ou une dépendance présent dans DEVOPS n’est ni sélectionné ni qualifié. Les références normatives complètes sont dans requirements.md ; les mentions historiques qu’elles contiennent ne décrivent pas des effets réalisés pendant cette préparation.

## Barrières de conception avant réalisation

Mécanisme d’intégrité, stockage et preuves d’export/rétention ; choix non fixé par le canon à soumettre avant réalisation.

Ces barrières n’empêchent pas la rédaction conditionnelle du dossier. Avant tout code, les choix ayant un impact réel sur sécurité, périmètre, compatibilité, exploitation ou ressources devront être soumis avec conséquences et recommandation ; pour PA/PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages. Les paramètres déjà décidés sont à qualifier, pas à remplacer par une nouvelle décision supposée.

## Dépendances et interfaces

- [add-durable-minimized-audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md).
- [enforce-core-data-governance-and-lifecycle](../enforce-core-data-governance-and-lifecycle/proposal.md).
- [add-upgrade-backup-and-restore-contracts](../add-upgrade-backup-and-restore-contracts/proposal.md).



Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent explicitement incomplètes tant que les obligations manquent.

## Vérification future

Source de vérité, isolation tenant/scope, refus sans permission, classification/rétention, retries/reprise et révocation ; contrat du provider sélectionné sur dépendance réelle, tests navigateur si interface web et audit manuel lorsque requis.

Sortie du lot : Altération détectée ; exports vérifiables ; données sensibles et contraintes de conservation non contournées.

Exercer tous les scénarios et clauses applicables des blocs sources, y compris renvois normatifs ; un scénario non applicable doit être motivé par le profil réel. Les contrôles applicatifs suivent l’exception Super Admin du canon dans son seul périmètre, sans fabriquer audit, mesure, signature ou effet absent.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données/états doit préciser propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation/restauration. Aucun retour arrière destructeur, remise à zéro, arrêt de service ou changement de droits implicites.

## Limites du dossier

Pas de PASS actuel ni d’achèvement produit revendiqué. L’autorisation de préparation ne permet ni d’activer la capacité dans P0 ni d’utiliser un compte connecté, publier un artefact ou envoyer une notification réelle.

## Approfondissement issu de l’audit du 17 octobre 2026

Conception proposée sans implémentation. Ces contrats de travail ne modifient pas le canon ; tout changement normatif requiert son delta approuvé.

Le journal durable vient de C05 ; O26 ajoute preuve d’intégrité et vérificateur, sans confondre SHA256 d’un manifest Bulk et chaîne d’audit. Déclarer mécanisme/version, unités chaînées et règles d’ordre/reprise.

Séparer transaction d’événement durable et calcul/publication de preuve. Marquer trou, délai, rupture ou vérification impossible au lieu de conclure intact. Exports relient versions, manifeste et preuve vérifiable hors du service émetteur ; rotation conserve la vérifiabilité requise.

La cryptographie ne confère aucun droit d’accès ni permission de conservation illimitée. Politique de rétention/effacement et confidentialité doit être validée avec C10 avant choix de mécanisme/clés/provider. Aucun algorithme nouveau ni conformité juridique générale annoncé.

### Exigences auditées et preuves de sortie futures

| Référence canonique | Statut statique après audit | Critère à démontrer |
|---|---|---|
| [audit-integrity #1](../../../openspec/specs/audit-integrity/spec.md#L11) | ND | Mécanisme, périmètre, version et vérificateur déclarés avant activation. |
| [audit-integrity #2](../../../openspec/specs/audit-integrity/spec.md#L25) | ND | Altération, rupture, ordre, rotation et reprise testés ; distinguer événement durable et preuve calculée. |
| [audit-integrity #3](../../../openspec/specs/audit-integrity/spec.md#L37) | ND | Export autorisé et manifeste vérifiable indépendamment ; pièce manquante ou modifiée détectée. |
| [audit-integrity #4](../../../openspec/specs/audit-integrity/spec.md#L49) | ND | Concilier minimisation, rétention/effacement et vérifiabilité sans conserver de données personnelles par commodité cryptographique. |

Voir [audit individuel et limites des preuves](../archive/2026-10-18-define-first-installable-pbo-profile/audit-ne-94.json) et [rapport d’audit](../../../reports/audit-ne-94-2026-10-17/RAPPORT.md). Les tâches de réalisation restent non cochées.
