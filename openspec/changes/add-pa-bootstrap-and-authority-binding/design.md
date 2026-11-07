# Conception — PA02

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

Périmètre propre à ce lot : Identité, références de secrets, ancrages et relations PBO–PA ; plusieurs autorités sans conflit résolu par dernière écriture ; provisionnement distinct du contrôle continu.

## Choix déjà fixés et alternatives

Les décisions validées dans les contrats sources sont conservées, y compris formats, algorithmes, valeurs, rôles et alternatives rejetées. Elles ne sont pas rouvertes sous prétexte d’un nouveau dossier. Les plafonds d’un auxiliaire, collecteur, validateur ou travail ne deviennent pas un budget général du PA/PBO.

Les modalités concrètes encore ouvertes ne reçoivent pas de valeur de défaut inventée. Une bibliothèque, un provider ou une dépendance présent dans DEVOPS n’est ni sélectionné ni qualifié. Les références normatives complètes sont dans requirements.md ; les mentions historiques qu’elles contiennent ne décrivent pas des effets réalisés pendant cette préparation.

## Barrières de conception avant réalisation

Formats du provisionnement et ancrages, identité par relation, règles de conflit entre autorités ; aucune confiance par premier contact.

Ces barrières n’empêchent pas la rédaction conditionnelle du dossier. Avant tout code, les choix ayant un impact réel sur sécurité, périmètre, compatibilité, exploitation ou ressources devront être soumis avec conséquences et recommandation ; pour PA/PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages. Les paramètres déjà décidés sont à qualifier, pas à remplacer par une nouvelle décision supposée.

## Dépendances et interfaces

- [add-pbo-runtime-secret-provider](../archive/2026-10-19-add-pbo-runtime-secret-provider/proposal.md).
- [add-core-postgres-services](../archive/2026-10-20-add-core-postgres-services/proposal.md).
- [add-initial-authentication-and-sessions](../archive/2026-10-21-add-initial-authentication-and-sessions/proposal.md).



Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent explicitement incomplètes tant que les obligations manquent.

## Vérification future

Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée.

Sortie du lot : Reprise sans double identité ; aucun premier PBO approuvé implicitement ; isolation des autorités ; aucune autorité métier locale.

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


## Addendum RSMP — orientations adoptées et détails proposés

Statut : orientations D1A, D2A, D3A adoptées par validation humaine du 2026-10-26. Schémas, wire et API détaillés restent PROPOSÉS à revoir avant code. Seuls les six documents PA02 listés ici sont autorisés maintenant, sans code ni effet runtime.

Détails proposés dans [contracts.md](./contracts.md), [identity-bindings.md](./identity-bindings.md) et [authority-policy.md](./authority-policy.md). Canon de référence : [pixs-agent](../../specs/pixs-agent/spec.md), [pzt](../../specs/pzt/spec.md), [core](../../specs/core/spec.md). Références propriétaires distinctes : composition et bootstrap PA01 dans [contracts.md](../add-pa-native-build-and-component-composition/contracts.md), PKI Z12 dans [proposal.md](../add-pzt-ca-hierarchy-rotation-and-recovery/proposal.md), installation C08 dans [proposal.md](../add-installation-and-first-configuration/proposal.md) ; ces propriétaires gardent leurs contrats. PA02 n'adopte aucun algorithme, clé, indice NV ou durée inédit, mais les profils PA02 peuvent devoir fixer les bornes manquantes avant code.

Résumé adopté lisible sans historique : D1 document JSON provisionnement, D2 références stables PA et relation, D3 propriétaire unique avec transfert explicite. Confiance préinstallée, propriétaire admissible unique par ressource et périmètre, transfert explicite sous exclusion, fencing, réconciliation et autorité compétente. Aucun digest ne devient ancrage de confiance. Aucune valeur, preuve ou révision candidate ne vaut approbation.


## Fermeture technique du codec pur — addendum 2026-10-26

Cet addendum ferme la technique de la première unité, sans modifier l'historique et sans qualifier le raccord futur.

L'unité est pure et sans confiance, en bibliothèque standard seule, pour Python 3.12 et versions suivantes retenues par le projet. Elle n'emploie ni import du paquet pixs.agent ni classe privée de Core. Elle ne fait ni entrée-sortie, ni appel réseau, ni accès persistant, ni opération cryptographique, ni lecture d'horloge.

Les deux fichiers proposés pour la première unité sont src/pixs/pa_native/provisioning_contracts.py et tests/unit/test_pa_provisioning_contracts.py. Les noms sont reconnus libres comme nouveaux fichiers de forme. Le raccord de construction, y compris Cython, est à fermer séparément avec l'autre périmètre, sans modifier ses fichiers existants et sans qualification anticipée.

Le constat historique de levée de fenêtre de priorité sur tests/unit le 26 octobre à 11:12:15 UTC ne vaut pas accord permanent ; chaque écriture future exige coordination et révisions fraîches de ressources et de réservation avant effet.

Les orientations B, retrait et INIT A sont adoptées. Les sources Context8, NV7 et Init12 sont écrites et non testées. Aucun port ni vérificateur PA ou PZT n'est livré à ce stade.

## Addendum RSMP fournisseur durable PA02 — principes A ADOPTÉS le 2026-10-26
Décision PROVIDER-LOCAL-DURABLE-PA02 : choix A ADOPTÉ par validation humaine du 2026-10-26 ; choix B SQLite non retenu dans cette phase. Principes ADOPTÉS : fichiers protégés, journal dédié, instantané versionné, flock, fsync fichier ET parent, rename atomique, réconciliation. Interface, code et qualification restant à réaliser sous revue Codex normale. D1A D2A D3A conservés. Architecture 3 binaires PA et modes existants conservée, sans 4e binaire ni nouveau mode. Procédure initiale PA02 locale native PA, distincte du contrôle PBO-PA, sans exiger la disponibilité préalable PG ou PZT ; pas de canal de commandes PBO direct hors PZT ; parcours C08 PBO via PZT avec PA exécutant et rôle métier R01 préservés. Interface initiale exacte à fermer par NFDOC conforme aux cadrages avant code, sans UID chemin permissions par défaut. États exactement non-provisionné en-cours prêt échoué. Inconnu diagnostic sous en-cours fermé, pas état. Prêt local borné à ses prérequis propres. Codec 17 clés et comparateur inchangés. Requirements.md inchangé.
