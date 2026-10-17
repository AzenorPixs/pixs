# Conception — O09

## Statut

PRÉPARATION_DOCUMENTAIRE_CONDITIONNELLE. Le dossier est demandé ; ses choix encore ouverts et son implémentation ne sont pas approuvés implicitement. La présence des fichiers ne signifie pas prêt à coder.

## Contexte actuel

La capacité est un candidat du canon ; la revue de présence des sources et la matrice ne démontrent pas une réalisation opérationnelle. Les lignes NE historiques ont été auditées le 17 octobre 2026 ; voir les constats individuels ci-dessous, sans qualification runtime.

Ce dossier référence 3 lignes NE dans la matrice historique. Leur audit statique est maintenant documenté ci-dessous ; les barrières de choix et de qualification avant réalisation restent applicables.

Sources et périmètres consultés :

- [README.md](../../../README.md).
- [src/pixs/kernel/composition.py](../../../src/pixs/kernel/composition.py).
- [src/pixs/backend/README.md](../../../src/pixs/backend/README.md).
- [src/pixs/developer_kit/README.md](../../../src/pixs/developer_kit/README.md).
- [src/pixs/developer_kit/validators.py](../../../src/pixs/developer_kit/validators.py).
- [src/pixs/kernel/contracts/README.md](../../../src/pixs/kernel/contracts/README.md).
- [src/pixs/kernel/contracts/models.py](../../../src/pixs/kernel/contracts/models.py).
- [src/pixs/example/__init__.py](../../../src/pixs/example/__init__.py).
- [src/pixs/backend/composition_initial.py](../../../src/pixs/backend/composition_initial.py).
- [src/pixs/backend/composition_proof.py](../../../src/pixs/backend/composition_proof.py).
- [src/pixs/backend/local_test_composition.py](../../../src/pixs/backend/local_test_composition.py).
- [src/pixs/backend/liveness_view.py](../../../src/pixs/backend/liveness_view.py).
- [frontend/README.md](../../../frontend/README.md).
- [frontend/package.json](../../../frontend/package.json).

## Architecture et frontières

Composant/provider optionnel au-dessus du Kernel, déclaré par manifest et sélection explicite. Exposer uniquement ses contrats publics versionnés et écrire ses données via leur propriétaire. Conserver Django/PostgreSQL comme autorités, contexte tenant/scope, audit et gouvernance ; qualifier séparément dépendances, limites et mode dégradé. Ne pas imposer un provider, une bibliothèque ou une ressource métier encore non décidés.

Périmètre propre à ce lot : Lecture sous contrat, préférence LDAP, fraîcheur après mutation, repli PG et DEGRADED.

## Choix déjà fixés et alternatives

Les décisions validées dans les contrats sources sont conservées, y compris formats, algorithmes, valeurs, rôles et alternatives rejetées. Elles ne sont pas rouvertes sous prétexte d’un nouveau dossier. Les plafonds d’un auxiliaire, collecteur, validateur ou travail ne deviennent pas un budget général du PA/PBO.

Les modalités concrètes encore ouvertes ne reçoivent pas de valeur de défaut inventée. Une bibliothèque, un provider ou une dépendance présent dans DEVOPS n’est ni sélectionné ni qualifié. Les références normatives complètes sont dans requirements.md ; les mentions historiques qu’elles contiennent ne décrivent pas des effets réalisés pendant cette préparation.

## Barrières de conception avant réalisation

Limites déclarées de fraîcheur et contrat de consultation ; réévaluation/filtrage Pixs même lors du repli PostgreSQL.

Ces barrières n’empêchent pas la rédaction conditionnelle du dossier. Avant tout code, les choix ayant un impact réel sur sécurité, périmètre, compatibilité, exploitation ou ressources devront être soumis avec conséquences et recommandation ; pour PA/PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages. Les paramètres déjà décidés sont à qualifier, pas à remplacer par une nouvelle décision supposée.

## Dépendances et interfaces

- [add-ldap-outbound-directory-projections](../add-ldap-outbound-directory-projections/proposal.md).



Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent explicitement incomplètes tant que les obligations manquent.

## Vérification future

Source de vérité, isolation tenant/scope, refus sans permission, classification/rétention, retries/reprise et révocation ; contrat du provider sélectionné sur dépendance réelle, tests navigateur si interface web et audit manuel lorsque requis.

Sortie du lot : Retard/panne avec repli autorisé ; fraîcheur conforme ; refus inter-tenant ; aucune donnée interdite exposée.

Exercer tous les scénarios et clauses applicables des blocs sources, y compris renvois normatifs ; un scénario non applicable doit être motivé par le profil réel. Les contrôles applicatifs suivent l’exception Super Admin du canon dans son seul périmètre, sans fabriquer audit, mesure, signature ou effet absent.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données/états doit préciser propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation/restauration. Aucun retour arrière destructeur, remise à zéro, arrêt de service ou changement de droits implicites.

## Limites du dossier

Pas de PASS actuel ni d’achèvement produit revendiqué. L’autorisation de préparation ne permet ni d’activer la capacité dans P0 ni d’utiliser un compte connecté, publier un artefact ou envoyer une notification réelle.

## Approfondissement issu de l’audit du 17 octobre 2026

Conception proposée sans implémentation. Ces contrats de travail ne modifient pas le canon ; tout changement normatif requiert son delta approuvé.

La lecture reçoit identité, tenant/scope canonique, attributs autorisés et exigence de fraîcheur. Préférer LDAP seulement si sa projection est admissible ; PostgreSQL conserve son autorité et fournit le repli déclaré.

Une mutation récente transporte une référence/version permettant d’écarter une ancienne projection. Absence, retard, retrait ou panne déclenche le repli ou le refus conforme ; ne pas joindre les résultats de deux sources de fraîcheurs incompatibles comme s’ils étaient atomiques.

Appliquer les mêmes autorisations et minimisation aux deux chemins ; diagnostic sans divulgation d’attributs cachés. Définir preuve de fraîcheur, politique de préférence et budget de lecture avant code ; aucun seuil de retard inventé.

### Exigences auditées et preuves de sortie futures

| Référence canonique | Statut statique après audit | Critère à démontrer |
|---|---|---|
| [directory-projections #9](../../../openspec/specs/directory-projections/spec.md#L98) | ND | LDAP uniquement si admissible ; absence ou obsolescence déclenchant le repli source déclaré. |
| [directory-projections #10](../../../openspec/specs/directory-projections/spec.md#L113) | ND | Version/fraîcheur contrôlée ; ancienne projection jamais annoncée courante après mutation. |
| [directory-projections #11](../../../openspec/specs/directory-projections/spec.md#L126) | ND | Même tenant/scope/attributs autorisés sur LDAP et source ; aucun diagnostic divulguant des données. |

Voir [audit individuel et limites des preuves](../define-first-installable-pbo-profile/audit-ne-94.json) et [rapport d’audit](../../../reports/audit-ne-94-2026-10-17/RAPPORT.md). Les tâches de réalisation restent non cochées.
