# Conception — O22

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

Périmètre propre à ce lot : Génération/validation et suites versionnées depuis kit local ; CLI par contrats sans activation/identité/donnée implicites.

## Choix déjà fixés et alternatives

Les décisions validées dans les contrats sources sont conservées, y compris formats, algorithmes, valeurs, rôles et alternatives rejetées. Elles ne sont pas rouvertes sous prétexte d’un nouveau dossier. Les plafonds d’un auxiliaire, collecteur, validateur ou travail ne deviennent pas un budget général du PA/PBO.

Les modalités concrètes encore ouvertes ne reçoivent pas de valeur de défaut inventée. Une bibliothèque, un provider ou une dépendance présent dans DEVOPS n’est ni sélectionné ni qualifié. Les références normatives complètes sont dans requirements.md ; les mentions historiques qu’elles contiennent ne décrivent pas des effets réalisés pendant cette préparation.

## Barrières de conception avant réalisation

Parcours et surface CLI/kit sélectionnés, suites versionnées et exemples ; génération distincte d’activation.

Ces barrières n’empêchent pas la rédaction conditionnelle du dossier. Avant tout code, les choix ayant un impact réel sur sécurité, périmètre, compatibilité, exploitation ou ressources devront être soumis avec conséquences et recommandation ; pour PA/PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages. Les paramètres déjà décidés sont à qualifier, pas à remplacer par une nouvelle décision supposée.

## Dépendances et interfaces

- [activate-reference-runtime-composition](../activate-reference-runtime-composition/proposal.md).
- [qualify-first-pbo-composition](../qualify-first-pbo-composition/proposal.md).
- [generate-typescript-python-public-sdks](../generate-typescript-python-public-sdks/proposal.md).



Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent explicitement incomplètes tant que les obligations manquent.

## Vérification future

Source de vérité, isolation tenant/scope, refus sans permission, classification/rétention, retries/reprise et révocation ; contrat du provider sélectionné sur dépendance réelle, tests navigateur si interface web et audit manuel lorsque requis.

Sortie du lot : Parcours propre reproductible ; diagnostics sans fuite ; génération sans effet métier ; suites ciblées/versionnées.

Exercer tous les scénarios et clauses applicables des blocs sources, y compris renvois normatifs ; un scénario non applicable doit être motivé par le profil réel. Les contrôles applicatifs suivent l’exception Super Admin du canon dans son seul périmètre, sans fabriquer audit, mesure, signature ou effet absent.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données/états doit préciser propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation/restauration. Aucun retour arrière destructeur, remise à zéro, arrêt de service ou changement de droits implicites.

## Limites du dossier

Pas de PASS actuel ni d’achèvement produit revendiqué. L’autorisation de préparation ne permet ni d’activer la capacité dans P0 ni d’utiliser un compte connecté, publier un artefact ou envoyer une notification réelle.

## Approfondissement issu de l’audit du 17 octobre 2026

Conception proposée sans implémentation. Ces contrats de travail ne modifient pas le canon ; tout changement normatif requiert son delta approuvé.

Le kit/CLI consomme SDK O21 et validateurs publics ; il ne stabilise pas les modules privés du Kernel. Déclarer commandes, compatibilité et sorties attendues, y compris résultat en cours ou refus.

Exemples et conformité utilisent corpus synthétiques sans création implicite d’identité ni données de production. Les identités et références de secret sont fournies explicitement au runtime autorisé ; jamais stockées dans exemple, journal ou artefact distribué.

Contrôler packaging, installation et compatibilité du kit sur cibles déclarées, sans confondre test du validateur et contrat complet CLI. Fixer commandes initiales, publication et générateur avec O21 avant code.

### Exigences auditées et preuves de sortie futures

| Référence canonique | Statut statique après audit | Critère à démontrer |
|---|---|---|
| [sdk-ecosystem #1](../../../openspec/specs/sdk-ecosystem/spec.md#L8) | ND | C06/C09 publient contrats machine-readable ; O21 verrouille outils, compare sorties et bloque toute divergence. |
| [sdk-ecosystem #2](../../../openspec/specs/sdk-ecosystem/spec.md#L17) | ND | Identité/tenant/scope/corrélation/idempotence propagés ; pagination/async/Bulk/erreurs sans faux succès. |
| [sdk-ecosystem #3](../../../openspec/specs/sdk-ecosystem/spec.md#L26) | ND | Validateurs publics et fixtures synthétiques ; publication bloquée si secret/donnée de production, navigateur sans persistance par défaut. |

Voir [audit individuel et limites des preuves](../define-first-installable-pbo-profile/audit-ne-94.json) et [rapport d’audit](../../../reports/audit-ne-94-2026-10-17/RAPPORT.md). Les tâches de réalisation restent non cochées.
