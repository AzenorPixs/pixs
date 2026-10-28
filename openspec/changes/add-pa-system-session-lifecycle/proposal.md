# PA03 — Lifecycle système, sessions et intégration écosystème

## Pourquoi

Le canon distingue trois binaires PA et six modes, plus le binaire indépendant PZT et son mode pzt-daemon ; l'implémentation, la qualification et les artefacts restent à réaliser. Le contrôle de présence ciblé des sources n'est pas une recette de plateforme. Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle.

Historique : ce dossier a d'abord été ouvert comme préparation sans comportement normatif. Cet état est dépassé. Le périmètre final ci-dessous modifie la capacité existante pixs-agent par ajout d'exigences et porte un delta ADDED Requirements en specs/pixs-agent/spec.md. Le document session-integration.md est une documentation détaillée, pas un delta. Les publications documentaires CAB déjà faites sont des faits ; l'absence de publication visée ci-dessous concerne les artefacts produit, pas les reçus documentaires. Les nouveaux schémas et opérations sont définis et proposés dans ce change, pas validés par le développeur ; les orientations systemd, logind, PAM borné, module natif et budgets restent acquises.

## Modifications proposées

Lifecycle borné système et session, délais et annulations, fermeture bornée, isolation des sessions et privilèges, intégration PFO vers PBO vers PZT vers PA vers adaptateur local et retours, déploiement et configuration versionnée par opérations PA fermées typées pa_observe 1.0.0, pa_plan 1.0.0, pa_apply 1.0.0 et pa_reconcile 1.0.0, profils Linux Debian13 physique et VM et contrat cible Windows. Respect du cycle indépendant de PZT et de pzt-daemon. Source unique des opérations et schémas en [session-integration.md](./session-integration.md) ; exigences et scénarios normatifs en [specs/pixs-agent/spec.md](./specs/pixs-agent/spec.md) ; synthèse en [design.md](./design.md) et [contracts.md](./contracts.md). Tâches en [tasks.md](./tasks.md).

## Capacités

### Capacités existantes modifiées

La capacité existante pixs-agent est modifiée par ajout d'exigences : intégration et gestion des adaptateurs de session, opérations PA fermées d'observation, plan, application et réconciliation, profils Linux et contrat cible Windows, sans autorité métier locale. Delta ADDED Requirements en [specs/pixs-agent/spec.md](./specs/pixs-agent/spec.md).

### Autres capacités

Aucune réécriture des canons deb-package, docker-image, compatibility, authorization et audit. Les exceptions SuperAdmin du canon restent dans leur périmètre exact sans fabriquer de preuve native. Ces capacités sont référencées pour packaging, profils, droits et audit ; leur comportement général ne change pas.

`requirements.md` est inchangé et conserve blocs sources, empreintes et scénarios.

## Sélection et périmètre autorisé

Premier profil Linux : Debian13 x86_64 physique et VM avec profil PAM sélectionné. Docker et LXC non sélectionnés comme produit pour les sessions ; libpam et logind ne sont pas imposés aux images Docker ni à Linux sans ce profil. Windows est un contrat cible à réaliser et qualifier séparément, pas un support acquis par Linux. Hors premier P0 jusqu'à sélection explicite. Aucun code, test produit, installation hôte, migration, publication d'artefact produit, Git ou archivage exécuté par ce dossier. Le code du module n'attend ni sa propre qualification future ni un environnement Windows non sélectionné en réalisation.

## Dépendances

- [add-pa-native-build-and-component-composition](../add-pa-native-build-and-component-composition/proposal.md).
- [add-pa-bootstrap-and-authority-binding](../add-pa-bootstrap-and-authority-binding/proposal.md).

PA01 pour build, composition, identités système et permissions minimales, packaging et qualification du module natif. PA02 pour provisionnement, identités de relation et autorités. Z12, C08 et A07 pour PKI, confirmation, transport et enveloppes. Rôles, profils et dépendances étrangers restent chez leurs propriétaires et ne sont pas livrés par ce change. D13, D14 et NV privés ne sont jamais transposés ; le graphe Cython et PyInit ne fournit ni module PAM C ni port session qualifié.

## Impact de réalisation future

Couche locale séparée de Django et PostgreSQL et sans autorité métier. PFO expose paramétrage et états sans effet OS direct. PBO valide configuration versionnée puis émet mandats corrélés. Le module PBO pixs.agent gère PA hors PZT et reste essentiel même sans exécutant OS disponible. PA natif exécute le lifecycle local selon profil installé et droits OS vérifiés, sans exiger un mandat PBO pour l'initialisation locale. Les opérations distantes de gestion restent soumises à autorité PBO valide. PZT transporte exclusivement les échanges PBO et PA. Les trois binaires PA et PZT indépendant restent colivrés sous gestion respective de pixs.agent et pixs.pzt.

## Critère de sortie de réalisation future

Arrêt pendant délai et traitement ; sessions concurrentes indépendantes ; verrouillage distinct de fermeture ; pas de succès après coupure forcée ; opérations fermées idempotentes avec état durable ; réconciliation avant réessai après effet inconnu ; recettes Linux et Windows exigent leurs environnements réels propres.

## Décisions adoptées

Adoptés : modes système par systemd sur Debian13 physique et VM ; session réelle par logind natif avec instance isolée par session et droits réels vérifiés ; paramètres de délais et budgets obligatoires sans défaut avec valeurs de recette 0 et 0, 30 et 10, 30 et 10 secondes ; raccord PAM borné vers binaire PA existant avec contrôle logind et droits réels et recette isolée avant installation ; module PAM natif en bibliothèque partagée avec C minimal et API libpam et artefact propre, sans Python dans PAM ni quatrième exécutable PA, avec qualification et packaging propres et sans installation hôte ; pilotage, déploiement et configuration via PA piloté PBO avec PZT comme seul transport PBO et PA.

Module PAM Linux conditionné au profil Linux PAM sélectionné. Aucune fonction d'authentification Pixs via PAM. Aucun compte, droit, activation hôte, version Windows ou modification PA01 autorisé ici. LocalSystem, SE_TCB_NAME, versions OS et CPU, Credential Provider, LSA, service ou exécutable nouveau ne font l'objet d'aucune adoption implicite ; WTSQueryUserToken reste une possibilité privilégiée documentée, pas une décision d'usage. Objets et catalogue définis et proposés : pa_session_config 1.0.0, pa_operation_envelope 1.0.0, pa_operation_result 1.0.0, pa_observe 1.0.0, pa_plan 1.0.0, pa_apply 1.0.0 et pa_reconcile 1.0.0.
