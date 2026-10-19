# Conception — X01

## Statut

PRÉPARATION_DOCUMENTAIRE_CONDITIONNELLE. Le dossier est demandé ; ses choix encore ouverts et son implémentation ne sont pas approuvés implicitement. La présence des fichiers ne signifie pas prêt à coder.

## Contexte actuel

Le README déclare les distributions non livrées ; le canon impose à l’image PBO/PFO avec pixs.agent/pixs.pzt, deux binaires PA et PZT indépendant, avec exclusion des modes utilisateur.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

Sources et périmètres consultés :

- [README.md](../../../README.md).
- [BUILD.md](../../../BUILD.md).
- [openspec/specs/docker-image/spec.md](../../specs/docker-image/spec.md).

## Architecture et frontières

Construire depuis sources et versions déclarées l’image Pixs complète en contenu PBO/PFO avec pixs.agent/pixs.pzt, deux binaires PA et le binaire indépendant PZT. Exclure binaire utilisateur et modes de session, séparer profils applicatifs et supervision distincte PA/PZT, préserver état/configuration/secrets hors image ; transmettre signaux/drain et identité de distribution sans nouvelle autorité métier.

Périmètre propre à ce lot : PBO/PFO avec pixs.agent/pixs.pzt, deux binaires PA et PZT indépendant ; état externe, sondes/arrêt/reproductibilité/publication.

## Choix déjà fixés et alternatives

Les décisions validées dans les contrats sources sont conservées, y compris formats, algorithmes, valeurs, rôles et alternatives rejetées. Elles ne sont pas rouvertes sous prétexte d’un nouveau dossier. Les plafonds d’un auxiliaire, collecteur, validateur ou travail ne deviennent pas un budget général du PA/PBO.

Les modalités concrètes encore ouvertes ne reçoivent pas de valeur de défaut inventée. Une bibliothèque, un provider ou une dépendance présent dans DEVOPS n’est ni sélectionné ni qualifié. Les références normatives complètes sont dans requirements.md ; les mentions historiques qu’elles contiennent ne décrivent pas des effets réalisés pendant cette préparation.

## Barrières de conception avant réalisation

Base/outils/architecture, rôles/comptes/supervision et permissions du profil ; deux binaires PA et PZT indépendant, pas de binaire utilisateur.

Ces barrières n’empêchent pas la rédaction conditionnelle du dossier. Avant tout code, les choix ayant un impact réel sur sécurité, périmètre, compatibilité, exploitation ou ressources devront être soumis avec conséquences et recommandation ; pour PA/PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages. Les paramètres déjà décidés sont à qualifier, pas à remplacer par une nouvelle décision supposée.

## Dépendances et interfaces

- [publish-first-qualified-pbo-release](../publish-first-qualified-pbo-release/proposal.md).
- [build-and-publish-independent-pa-debian-package](../build-and-publish-independent-pa-debian-package/proposal.md).
- [qualify-active-pzt-contracts-and-profiles](../qualify-active-pzt-contracts-and-profiles/proposal.md).



Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent explicitement incomplètes tant que les obligations manquent.

## Vérification future

Contenu inspecté, dépendances fixées, absence du binaire utilisateur et de secret/configuration effective, deux constructions corrélables, configuration invalide, readiness/liveness, arrêt/drain/recréation et identité/signature/révocation.

Sortie du lot : Binaire et modes utilisateur absents ; aucun hôte administré implicitement ; recette isolée ; permissions selon profil autorisé.

Exercer tous les scénarios et clauses applicables des blocs sources, y compris renvois normatifs ; un scénario non applicable doit être motivé par le profil réel. Les contrôles applicatifs suivent l’exception Super Admin du canon dans son seul périmètre, sans fabriquer audit, mesure, signature ou effet absent.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données/états doit préciser propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation/restauration. Aucun retour arrière destructeur, remise à zéro, arrêt de service ou changement de droits implicites.

## Limites du dossier

Pas de PASS actuel ni d’achèvement produit revendiqué. L’autorisation de préparation ne permet ni d’activer la capacité dans P0 ni d’utiliser un compte connecté, publier un artefact ou envoyer une notification réelle.

## Séparation PA/PZT validée le 17 octobre 2026

La [décision adoptée](../separate-pa-pzt-and-pbo-management-modules/design.md) conserve
trois exécutables hors PBO/PFO dans Docker : deux PA et PZT indépendant. Le
binaire utilisateur PA reste exclu. Les snapshots requirements.md doivent
être réconciliés avec le canon actuel avant réalisation ; aucune image n'est
construite ni qualifiée pendant cet alignement documentaire.
