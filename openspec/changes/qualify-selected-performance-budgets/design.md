# Conception — O31

## Statut

PRÉPARATION_DOCUMENTAIRE_CONDITIONNELLE. Le dossier est demandé ; ses choix encore ouverts et son implémentation ne sont pas approuvés implicitement. La présence des fichiers ne signifie pas prêt à coder.

## Contexte actuel

La capacité est un candidat du canon ; la revue de présence des sources et la matrice ne démontrent pas une réalisation opérationnelle. Les lignes NE historiques ont été auditées le 17 octobre 2026 ; voir les constats individuels ci-dessous, sans qualification runtime.

Ce dossier référence 8 lignes NE dans la matrice historique. Leur audit statique est maintenant documenté ci-dessous ; les barrières de choix et de qualification avant réalisation restent applicables.

Sources et périmètres consultés :

- [README.md](../../../README.md).
- [src/pixs/kernel/composition.py](../../../src/pixs/kernel/composition.py).
- [src/pixs/backend/README.md](../../../src/pixs/backend/README.md).
- [src/pixs/backend/correlated_log.py](../../../src/pixs/backend/correlated_log.py).
- [src/pixs/backend/health_classifier.py](../../../src/pixs/backend/health_classifier.py).
- [src/pixs/backend/pg_connectivity.py](../../../src/pixs/backend/pg_connectivity.py).
- [src/pixs/backend/runtime_profiles.py](../../../src/pixs/backend/runtime_profiles.py).

## Architecture et frontières

Composant/provider optionnel au-dessus du Kernel, déclaré par manifest et sélection explicite. Exposer uniquement ses contrats publics versionnés et écrire ses données via leur propriétaire. Conserver Django/PostgreSQL comme autorités, contexte tenant/scope, audit et gouvernance ; qualifier séparément dépendances, limites et mode dégradé. Ne pas imposer un provider, une bibliothèque ou une ressource métier encore non décidés.

Périmètre propre à ce lot : Périmètres/méthodes/seuils retenus puis mesure des budgets de composition ; aucune optimisation avant mesure.

## Choix déjà fixés et alternatives

Les décisions validées dans les contrats sources sont conservées, y compris formats, algorithmes, valeurs, rôles et alternatives rejetées. Elles ne sont pas rouvertes sous prétexte d’un nouveau dossier. Les plafonds d’un auxiliaire, collecteur, validateur ou travail ne deviennent pas un budget général du PA/PBO.

Les modalités concrètes encore ouvertes ne reçoivent pas de valeur de défaut inventée. Une bibliothèque, un provider ou une dépendance présent dans DEVOPS n’est ni sélectionné ni qualifié. Les références normatives complètes sont dans requirements.md ; les mentions historiques qu’elles contiennent ne décrivent pas des effets réalisés pendant cette préparation.

## Barrières de conception avant réalisation

Objectifs par profil, méthode/seuil/période/charge ; aucune valeur universelle inventée ni optimisation avant mesure.

Ces barrières n’empêchent pas la rédaction conditionnelle du dossier. Avant tout code, les choix ayant un impact réel sur sécurité, périmètre, compatibilité, exploitation ou ressources devront être soumis avec conséquences et recommandation ; pour PA/PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages. Les paramètres déjà décidés sont à qualifier, pas à remplacer par une nouvelle décision supposée.

## Dépendances et interfaces

- [define-first-installable-pbo-profile](../archive/2026-10-18-define-first-installable-pbo-profile/proposal.md).
- [add-runtime-observability-and-operations](../add-runtime-observability-and-operations/proposal.md).
- [qualify-first-pbo-composition](../qualify-first-pbo-composition/proposal.md).



Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent explicitement incomplètes tant que les obligations manquent.

## Vérification future

Source de vérité, isolation tenant/scope, refus sans permission, classification/rétention, retries/reprise et révocation ; contrat du provider sélectionné sur dépendance réelle, tests navigateur si interface web et audit manuel lorsque requis.

Sortie du lot : Pas de seuil universel ; preuves par profil ; invariants jamais sacrifiés pour performance.

Exercer tous les scénarios et clauses applicables des blocs sources, y compris renvois normatifs ; un scénario non applicable doit être motivé par le profil réel. Les contrôles applicatifs suivent l’exception Super Admin du canon dans son seul périmètre, sans fabriquer audit, mesure, signature ou effet absent.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données/états doit préciser propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation/restauration. Aucun retour arrière destructeur, remise à zéro, arrêt de service ou changement de droits implicites.

## Limites du dossier

Pas de PASS actuel ni d’achèvement produit revendiqué. L’autorisation de préparation ne permet ni d’activer la capacité dans P0 ni d’utiliser un compte connecté, publier un artefact ou envoyer une notification réelle.

## Approfondissement issu de l’audit du 17 octobre 2026

Conception proposée sans implémentation. Ces contrats de travail ne modifient pas le canon ; tout changement normatif requiert son delta approuvé.

Le protocole fixe release/profil, surface, plateforme, charge, données synthétiques, échauffement, répétitions, instrumentation, seuil et période. Mesures brutes et critères définis avant campagne ; le coût logique PDP n’est pas une latence ni un quota fournisseur.

Comparer référence et candidat dans les mêmes conditions ; publier mesure, budget, écart et insatisfaction explicite. Tester maintien des invariants, perte de cache et repli source pour les accélérations sélectionnées. Une mesure locale hors profil demeure informative.

C17 mesure les garanties nécessaires au P0 avant release ; O31 approfondit ensuite les charges/options retenues et dépend de cette base qualifiée. Pas de dépendance inverse créant un cycle. Valeurs de budgets/charges restent à faire valider, sans promesse universelle.

### Exigences auditées et preuves de sortie futures

| Référence canonique | Statut statique après audit | Critère à démontrer |
|---|---|---|
| [performance #1](../../../openspec/specs/performance/spec.md#L8) | P | Référence initiale, protocole et signal observé conservés avant justification d’une optimisation. |
| [performance #2](../../../openspec/specs/performance/spec.md#L17) | ND | Budgets par surface/profil, seuils déclarés avant mesure, dépassement reproductible signalé. |
| [performance #3](../../../openspec/specs/performance/spec.md#L26) | P | Release/profil, matériel, surface, charge, méthode et validité associés ; hors profil informatif. |
| [performance #4](../../../openspec/specs/performance/spec.md#L38) | P | Aucune suppression d’isolation, d’échec fermé ou d’audit dans le chemin optimisé. |
| [performance #5](../../../openspec/specs/performance/spec.md#L47) | ND | Perte/péremption et repli source observés sans résultat erroné ou obsolète déclaré courant. |
| [service-objectives #1](../../../openspec/specs/service-objectives/spec.md#L10) | P | Objectif lié à version/périmètre/seuil/méthode/période, valeur non inventée par test local. |
| [service-objectives #2](../../../openspec/specs/service-objectives/spec.md#L21) | P | Rapport hors profil informatif ; aucune extrapolation d’un résultat ou d’une borne PZT à tout Pixs. |
| [service-objectives #3](../../../openspec/specs/service-objectives/spec.md#L32) | ND | Campagne synthétique avec versions/charge/méthode, mesure/seuil/écart ; insatisfaction explicitement remontée. |

Voir [audit individuel et limites des preuves](../archive/2026-10-18-define-first-installable-pbo-profile/audit-ne-94.json) et [rapport d’audit](../../../reports/audit-ne-94-2026-10-17/RAPPORT.md). Les tâches de réalisation restent non cochées.
