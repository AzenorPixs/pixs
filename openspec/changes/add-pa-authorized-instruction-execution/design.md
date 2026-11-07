# Conception — PA04

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Instructions et mandats contextualisés, opérations multi-rôles, revalidation, résultats observés et reprise sans double effet.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [pixs-agent](../../specs/pixs-agent/spec.md).
- [scope-context](../../specs/scope-context/spec.md).
- [zt-controller](../../specs/zt-controller/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Statut

PRÉPARATION_DOCUMENTAIRE_CONDITIONNELLE. Le dossier est demandé ; ses choix encore ouverts et son implémentation ne sont pas approuvés implicitement. La présence des fichiers ne signifie pas prêt à coder.

## Contexte actuel

Le canon distingue trois binaires PA et six modes, plus le binaire indépendant PZT et son mode pzt-daemon ; le README indique que l’implémentation, la qualification et les artefacts restent à réaliser. Le contrôle de présence ciblé des sources n’est pas une recette de plateforme.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

Sources et périmètres consultés :

- [README.md](../../../README.md).
- [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md).
- [BUILD.md](../../../BUILD.md).

## Architecture et frontières

Couche locale séparée de Django/PostgreSQL et sans autorité métier. Composer les opérations au build par contrats, dispatch explicite et identité du mode ; isoler comptes/sessions, handles et générations. Lier mandats, contexte, effets et résultats observés ; communiquer avec PBO uniquement via PZT. Les trois binaires PA (Cython) et PZT indépendant (Cython) restent colivrés, sous gestion respective de pixs.agent et pixs.pzt.

Périmètre propre à ce lot : Contrats publics des instructions, fraîcheur, scopes, idempotence, revalidation, compensation préautorisée et réconciliation après résultat incertain ; aucun code distant implicite.

## Choix déjà fixés et alternatives

Les décisions validées dans les contrats sources sont conservées, y compris formats, algorithmes, valeurs, rôles et alternatives rejetées. Elles ne sont pas rouvertes sous prétexte d’un nouveau dossier. Les plafonds d’un auxiliaire, collecteur, validateur ou travail ne deviennent pas un budget général du PA/PBO.

Les modalités concrètes encore ouvertes ne reçoivent pas de valeur de défaut inventée. Une bibliothèque, un provider ou une dépendance présent dans DEVOPS n’est ni sélectionné ni qualifié. Les références normatives complètes sont dans requirements.md ; les mentions historiques qu’elles contiennent ne décrivent pas des effets réalisés pendant cette préparation.

## Barrières de conception avant réalisation

Catalogue exact des opérations, schémas d’instructions/mandats et preuves de postconditions ; aucun shell arbitraire ou compensation hors plan.

Ces barrières n’empêchent pas la rédaction conditionnelle du dossier. Avant tout code, les choix ayant un impact réel sur sécurité, périmètre, compatibilité, exploitation ou ressources devront être soumis avec conséquences et recommandation ; pour PA/PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages. Les paramètres déjà décidés sont à qualifier, pas à remplacer par une nouvelle décision supposée.

## Dépendances et interfaces

- [add-pa-system-session-lifecycle](../add-pa-system-session-lifecycle/proposal.md).
- [add-pzt-wireguard-local-transport-and-filtering](../add-pzt-wireguard-local-transport-and-filtering/proposal.md).
- [add-pzt-network-mandates-and-fail-closed-revocation](../add-pzt-network-mandates-and-fail-closed-revocation/proposal.md).
- [add-pzt-public-control-contracts-and-state-streams](../add-pzt-public-control-contracts-and-state-streams/proposal.md).
- [add-pzt-pa-admission-and-ephemeral-peer-generation](../add-pzt-pa-admission-and-ephemeral-peer-generation/proposal.md).
- [integrate-runtime-authorization-and-super-admin](../archive/2026-10-21-integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md).



Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent explicitement incomplètes tant que les obligations manquent.

## Vérification future

Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée.

Sortie du lot : Mandat périmé/révoqué bloqué ; crash entre effet et résultat réconcilié ; acteur initial conservé sans credentials Super Admin transférés.

Exercer tous les scénarios et clauses applicables des blocs sources, y compris renvois normatifs ; un scénario non applicable doit être motivé par le profil réel. Les contrôles applicatifs suivent l’exception Super Admin du canon dans son seul périmètre, sans fabriquer audit, mesure, signature ou effet absent.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données/états doit préciser propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation/restauration. Aucun retour arrière destructeur, remise à zéro, arrêt de service ou changement de droits implicites.

## Limites du dossier

Pas de PASS actuel ni d’achèvement produit revendiqué. L’autorisation de préparation ne permet ni d’activer la capacité dans P0 ni d’utiliser un compte connecté, publier un artefact ou envoyer une notification réelle.

## Alignement PA/PZT validé le 17 octobre 2026

La [décision adoptée](../separate-pa-pzt-and-pbo-management-modules/design.md) fixe pixs.agent pour
la configuration, l'administration et la supervision de PA hors PZT, et
pixs.pzt pour le binaire indépendant PZT. PA/PZT restent colivrés : trois
binaires PA plus PZT dans Debian, deux binaires PA plus PZT dans Docker.
Le présent lot conserve son périmètre de réalisation, sans code engagé ici.
Les copies requirements.md et empreintes de préparation sont historiques et
doivent être réconciliées avec le canon avant réalisation ; le réseau ne
redevient pas une responsabilité PA du fait d'une formulation héritée.

## Proposition de texte documentaire pour consigner des choix validés — premier lot 1A-2B-3A du 26 octobre 2026

Source : décision humaine du 26 octobre 2026 validant 1A-2B-3A. Texte RSMP proposé, distinct des choix acquis, sans code ni qualification.

Portée fonctionnelle produit : gestion bornée d'un service explicitement autorisé et inscrit au catalogue livré, par OBSERVE, PREPARE_PLAN, START, STOP, READ_RESULT. Catalogue au build : allowlist fermée des opérations et services autorisés. Mandat courant : cible et effets autorisés pour l'exécution concernée, distincts de la whitelist. Essais : exclusivement service factice dédié en environnement de test autorisé, sans toucher services existants de l'hôte de développement.

Le choix fonctionnel initial OBSERVE/PREPARE_PLAN/START/STOP/READ_RESULT est acquis. Restent à fermer avant réalisation applicable : identifiants API, schémas, paramètres, effets, postconditions, durabilité et budgets. Confirmation, idempotence et postcondition ne sont pas implicites.

Choix 1A Debian 13 physique/VM, PA système seul. Choix 3A connecté via PZT avec autorité courante, sans effet hors ligne. Exclusions premier lot : aucun service PA/PZT/CAB/SSH/PostgreSQL piloté, aucun nom libre ni commande arbitraire, pas de sessions utilisateur, conteneurs produit ou hors ligne, pas de SQL direct. PBO-PA via PZT. PA03 et dépendances PZT restent exigibles, aucune livraison déduite.

Critères observables : mandat périmé ou révoqué bloqué, crash incertain réconcilié sans double effet, acteur initial conservé. Sessions utilisateur, autres plateformes et hors ligne différés, aucune obligation de la suite PA04 supprimée. Premier lot non équivalent à livraison PA04, sans exigence canonique nouvelle.

## Lien delta et contrats proposés — 1A-2B-3A inchangés

Choix 1A-2B-3A acquis conservés. Delta proposé en specs/pixs-agent/spec.md et descriptions en contracts.md, non appliqués. START/STOP portent sur service produit explicitement autorisé, essai seul sur factice dédié sans toucher existants. Preuve d’effet par propriétaire courant liée à cible/génération/artefact. Barrières restantes explicites : schémas, identifiants, versions, confiance, durabilité, bornes, budgets et dépendances non adoptés ; aucun prêt à coder.
