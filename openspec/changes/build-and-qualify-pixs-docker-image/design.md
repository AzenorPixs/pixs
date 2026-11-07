# Conception — X01

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Profils de services, persistances et dépendances de Domaine ; deux binaires PA système/événements et PZT, sans session utilisateur ni droit hôte implicite.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [docker-image](../../specs/docker-image/spec.md).
- [reference-composition](../../specs/reference-composition/spec.md).
- [pixs-domains](../../specs/pixs-domains/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

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


## Choix BIND 9 adopté le 24 octobre 2026

Le [choix BIND 9 adopté](../adopt-bind9-managed-dns-and-packaging/proposal.md) est synchronisé le 24 octobre 2026 dans
[docker-image](../../specs/docker-image/spec.md#L131) et [pzt](../../specs/pzt/spec.md#requirement-fournisseur-bind-9-du-dns-géré-sur-debian-et-docker-pixs).
Le lot image devra fournir BIND 9 issu de Debian et ses dépendances
identifiées, sans lancement DNS implicite. Configuration d'instance, données
persistantes, journaux mutables, clés privées et secrets restent hors des
couches de l'image. La recette inspectera toutes les couches et les effets
des scripts de paquet ; effacer une donnée dans une couche ultérieure ne
prouve pas son absence de l'image.

L'activation ultérieure requiert un rôle serveur admis et l'application
puis la supervision du processus BIND 9 distinct par le PA désigné, avec
[Z05](../add-pzt-managed-dns-service-and-pa-adapters/design.md). Ce choix
n'ajoute aucun port, montage, utilisateur ni privilège implicite et conserve
l'exclusion des fonctions PA utilisateur. Le profil Docker C08 et les
budgets réellement autorisés restent à respecter. Aucune image n'est
construite, lancée ou qualifiée par cette adoption normative.

Ce renvoi ne coche aucune tâche de réalisation du lot.
