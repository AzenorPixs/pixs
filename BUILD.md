# BUILD.md — Pixs

## 1. Objet

Ce document définit le cadre de construction et de packaging de Pixs.

Il complète `PROJECT.md` en précisant les principes techniques applicables à la production des artefacts distribuables de Pixs sans redéfinir son architecture fonctionnelle.

Les deux formes initiales de distribution sont :

```text
Sources Pixs
     │
     ├── build
     │     ├── paquet Debian (.deb)
     │     └── image Docker
     │
     └── exécution directe
           └── environnement de développement
```

Le présent document concerne principalement :

* la construction du paquet Debian ;
* la construction de l'image Docker ;
* le contenu des artefacts ;
* la séparation entre build et runtime ;
* la reproductibilité ;
* la configuration externe ;
* les données persistantes ;
* les secrets ;
* les dépendances ;
* le versionnement des artefacts ;
* leur validation.

Il ne remplace ni `PROJECT.md` ni les spécifications OpenSpec.

En cas de divergence :

```text
Spécification OpenSpec validée
        ↓
PROJECT.md
        ↓
BUILD.md
        ↓
Implémentation du build
```

Une spécification OpenSpec validée portant explicitement sur un comportement de construction ou de packaging constitue la référence normative de ce comportement.

---

## 2. Principe fondamental

Le packaging ne constitue pas une variante fonctionnelle de Pixs.

Une même version fonctionnelle doit pouvoir être exécutée :

```text
                    Pixs
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
    développement    Debian      Docker
       local          .deb        image
```

sans modifier :

* le modèle de composants ;
* le Kernel ;
* les responsabilités de `pixs.core` ;
* les contrats publics ;
* les règles métier ;
* les règles d'autorisation ;
* la propriété des données ;
* les frontières transactionnelles ;
* les mécanismes de modules ;
* les invariants de compatibilité.

Les différences entre les modes de distribution doivent rester limitées aux responsabilités nécessaires à l'installation, à la configuration, à l'exécution et à l'exploitation.

---

## 3. Source de construction

Les artefacts distribuables doivent être construits à partir des sources versionnées du projet.

Le processus de build ne doit pas dépendre implicitement :

* d'un état local non versionné ;
* d'un cache indispensable à la validité fonctionnelle ;
* d'un fichier secret présent sur la machine de développement ;
* d'une configuration personnelle du développeur ;
* d'un artefact produit manuellement hors du processus de build.

Les éléments nécessaires à la construction doivent être soit :

* présents dans les sources ;
* déclarés comme dépendances ;
* générés explicitement pendant le build ;
* fournis explicitement comme paramètres de construction lorsque cela est nécessaire.

Un cache peut accélérer une construction mais ne doit pas en définir le résultat fonctionnel.

Les composants distribués doivent embarquer leur manifest `component.toml` et les métadonnées nécessaires à leur résolution. Le build doit valider les identifiants, types, versions SemVer, dépendances et capacités déclarées avant de produire un artefact.

Les contrats OpenAPI des API distribuées doivent être présents ou générés de manière reproductible à partir des sources versionnées. Chaque version majeure publiée doit disposer de son contrat OpenAPI identifiable. Le build doit vérifier la cohérence entre les versions déclarées, les préfixes de routes, les schémas publics et les contrats générés, sans intégrer de secret ou de configuration de production.

Les contributions frontend des composants doivent être déclarées dans les manifests ou sources contractuelles versionnées et résolues de manière reproductible. Le build frontend doit vérifier les identifiants, types, versions, dépendances, collisions de routes ou de slots, ressources de traduction, exigences de permissions d'affichage et compatibilité avec le shell. Une contribution non résolue, ambiguë ou incompatible doit bloquer le build ou l'activation selon le moment de détection.

Le build doit intégrer les sources ou artefacts frontend des modules dans une composition déterministe et produire les bundles ou chunks distribuables. Il ne doit pas dépendre d'un téléchargement de code ou d'une installation de paquet au runtime. Les artefacts Debian, Docker et développement doivent embarquer ou référencer une composition équivalente, avec les métadonnées nécessaires au diagnostic des composants frontend chargés. Une extension distante éventuelle doit être explicitement sélectionnée comme adapter et ne peut pas être introduite implicitement par le build.

Le build frontend doit vérifier que les extensions utilisent les clients et contrats API publics, que les clients générés correspondent aux versions OpenAPI publiées et qu'aucun accès direct à une base, un modèle privé ou une route non documentée n'est embarqué. Les tests doivent couvrir les clés de cache tenant-aware, l'invalidation après Command, les états provisoires et confirmés des mutations, ainsi que le comportement déclaré des capacités Electric.

Le build frontend doit publier ou générer de manière reproductible les tokens, primitives et adapters du Design System. Il doit vérifier les versions de contrat, l'absence de valeurs visuelles interdites dans les modules, la compatibilité des thèmes, l'accessibilité déclarée des primitives et l'absence d'import vers des implémentations privées. Les artefacts Debian, Docker et développement doivent utiliser le même contrat de Design System.

Le build doit valider le schéma et les types des tokens, la présence des modes `light` et `dark`, la cohérence des valeurs `high-contrast` lorsqu'il est fourni, les valeurs par défaut, les contraintes de contraste déclarées et la résolution déterministe du thème. Il doit détecter les valeurs visuelles codées en dur dans les extensions lorsque la règle est applicable et vérifier que le changement de thème ne dépend pas d'un rechargement ou d'une donnée runtime secrète.

Les tests frontend doivent couvrir les tailles d'affichage et contraintes d'espace représentatives, le reflow et le zoom, les densités déclarées, les tableaux, formulaires et navigations sur petits écrans, ainsi que l'absence de débordement ou de contenu inaccessible. Le build doit vérifier les tokens de layout et les contraintes minimales déclarées par les extensions.

Le build doit valider les identifiants de locale, les namespaces de clés, l'absence de doublons, les catalogues obligatoires, les messages ICU, les placeholders cohérents entre locales et les ressources RTL déclarées. Il doit détecter les textes utilisateur non externalisés lorsque la règle est applicable, vérifier les formats localisés et produire un diagnostic pour chaque fallback autorisé. Les catalogues chargés de manière différée doivent être inclus dans les artefacts et associés à leur composant.

Le build doit exiger le catalogue canonique `en` pour les composants qui fournissent des textes, contrôler sa complétude et vérifier que les locales d'installation déclarées sont compatibles avec les clés et paramètres canoniques. Il ne doit pas transformer la locale active de l'environnement de build en dépendance du code ou du contrat frontend.

Les tests frontend doivent couvrir les combinaisons de locales, fuseaux horaires, calendriers, systèmes de numération et devises d'affichage déclarées, sans utiliser le fuseau de la machine de build comme valeur implicite. Ils doivent vérifier la conservation de la précision, la distinction entre affichage et valeur métier et la sérialisation UTC des instants transmis aux APIs.

Les validations frontend doivent inclure les contrôles applicables à WCAG 2.2 AA : analyse automatisée, tests de clavier et de focus, vérification du contraste et du reflow, tests avec les modes de réduction des mouvements et parcours représentatifs avec technologies d'assistance. Une primitive ou extension stable qui échoue aux critères obligatoires doit bloquer le build ou être exclue de la composition stable. Les composants expérimentaux doivent être identifiés sans être utilisés implicitement par les modules.

Les validations frontend doivent vérifier que le contexte de session est fourni par le shell, que les extensions n'embarquent aucun accès aux tokens ou stockage navigateur interdit, que les guards ne remplacent pas les appels d'autorisation backend et qu'un changement de tenant invalide les états associés. Les artefacts et journaux de build ne doivent contenir ni token, ni secret, ni donnée de session.

Le build et les tests frontend doivent vérifier le lifecycle des extensions, la détection des composants obligatoires, l'isolation des erreurs optionnelles, le retrait des contributions invalides, la cohérence des états `DISCOVERED`, `RESOLVED`, `LOADED`, `ACTIVE`, `DEGRADED`, `FAILED` et `DISABLED`, ainsi que la présence d'informations de diagnostic corrélées. Une extension marquée obligatoire ne doit pas pouvoir être silencieusement ignorée.

La chaîne de build frontend doit vérifier la provenance et les empreintes des manifests, dépendances, bundles et chunks, l'absence de code distant non autorisé, la conformité CSP, l'absence d'usage interdit d'évaluation dynamique et la conservation de l'intégrité après packaging Debian ou Docker. Les tests doivent confirmer qu'une extension intégrée ne peut pas lire les secrets runtime du shell et qu'une extension sandboxée ne reçoit que les APIs explicitement autorisées.

Les tests frontend doivent vérifier les contrats du bus UI, les namespaces et versions d'événements, la validation des payloads, l'absence d'accès direct aux stores d'autres extensions, le refus des actions non déclarées et la séparation entre événements d'interface et décisions métier backend. Les changements incompatibles d'un événement UI public doivent être détectés comme les autres contrats versionnés.

Le build et les tests frontend doivent vérifier les modes CSR, SSR, streaming et SSG déclarés par les routes, la compatibilité d'hydratation des extensions concernées, l'absence de donnée sensible dans le HTML pré-rendu ou les bundles, la reproductibilité des contenus statiques et l'absence de dépendance à un contexte tenant ou une session au moment d'un SSG.

Le build frontend doit vérifier l'unicité des `route_id`, des chemins et des priorités, la détection des collisions avec le shell, la déclaration des périmètres d'accès, la génération de la navigation, les redirections versionnées et le fonctionnement des deep links après packaging. Toute route ambiguë, non résolue ou susceptible de masquer une route protégée doit bloquer la composition.

Le build doit analyser le graphe de dépendances frontend, vérifier les imports autorisés, les façades publiques, les contraintes SemVer et l'absence de cycles ou d'accès à des chemins privés. Une dépendance obligatoire non résolue ou incompatible doit échouer le build ; une dépendance optionnelle doit produire un état diagnostiquable sans rendre la composition ambiguë.

Le build doit lire la section frontend du `component.toml`, valider son schéma et contrôler chaque contribution déclarée : type, identifiant namespacé, version, point d'entrée, dépendances et compatibilité avec l'API du shell. Une contribution non déclarée ne doit pas être incluse par découverte implicite. Un point d'entrée absent, extérieur au composant, ambigu ou incompatible doit faire échouer la composition.

Lorsque l'artefact fournit ou consomme des contrats publics, le build doit également préserver leurs identifiants, catégories, versions et contraintes de compatibilité. Une implémentation privée ne doit pas être publiée comme contrat simplement parce qu'elle est présente dans l'artefact.

Le build ne doit pas préinitialiser de tenant, d'appartenance, de rôle, d'ACL ou de donnée métier dans un artefact destiné à un environnement de production. Ces éléments relèvent du runtime, des migrations ou d'une opération d'administration explicitement définie.

---

## 4. Reproductibilité

Le processus de construction doit tendre vers un résultat reproductible à partir :

```text
Sources
+
Version
+
Dépendances déclarées
+
Paramètres de build explicitement autorisés
```

Les dépendances utilisées pendant la construction doivent être suffisamment contraintes pour éviter qu'une reconstruction d'une même version fonctionnelle ne produise silencieusement une composition incompatible.

Les mécanismes exacts de verrouillage des dépendances Python, JavaScript, Debian et des images de base seront définis par les capacités OpenSpec concernées.

Une dépendance non maîtrisée ne doit pas devenir implicitement une partie du contrat de build.

La découverte des composants pendant le build doit être déterministe. Le résultat ne doit pas dépendre de l'ordre du filesystem, des imports ou de l'ordre d'installation. Une composition ambiguë ou incompatible doit faire échouer le build ou la validation de l'artefact.

---

## 5. Séparation BUILD / RUNTIME

Le build prépare les éléments nécessaires à l'exécution.

Le runtime configure et exécute l'application.

Principe :

```text
BUILD
  │
  ├── assembler
  ├── installer les dépendances
  ├── compiler / générer les ressources
  ├── préparer les fichiers applicatifs
  └── produire un artefact
              │
              ▼
RUNTIME
  │
  ├── charger la configuration
  ├── accéder aux secrets
  ├── vérifier les dépendances externes
  ├── appliquer les opérations runtime autorisées
  └── démarrer Pixs
```

Une information dépendante de l'environnement de déploiement ne doit pas être figée dans l'artefact lorsqu'elle peut être fournie au runtime.

En particulier, les secrets de production ne doivent jamais être intégrés au paquet Debian ou à l'image Docker.

La sélection runtime d'un provider doit utiliser les manifests et la configuration déclarative validés. Le build ne doit pas figer un provider concret lorsque celui-ci relève d'une configuration de déploiement, mais il doit vérifier que les composants distribués exposent des contrats et capacités compatibles.

Le runtime doit pouvoir recevoir explicitement le contexte tenant nécessaire à l'exécution. Une configuration de déploiement ne doit pas désactiver silencieusement l'isolation tenant ou transformer un accès inter-tenant en accès implicite.

Le runtime doit préserver les métadonnées de Command nécessaires à l'exécution et au diagnostic, notamment l'identité appelante, le contexte tenant, les identifiants de corrélation et de causalité. Une Command asynchrone doit pouvoir être suivie après redémarrage ou recréation du processus lorsque sa capacité le prévoit.

Les caches et projections utilisés par les Queries peuvent être reconstruits ou invalidés sans devenir la source de vérité applicative. Leur déploiement ne doit pas permettre de servir une donnée hors du contexte tenant ou des permissions applicables.

Lorsque l'outbox est activée, ses données persistantes doivent être stockées dans la source de vérité ou le provider explicitement prévu. Le build, l'installation et le redémarrage d'un service ne doivent pas supprimer les événements non publiés ni contourner leur relation transactionnelle avec la mutation métier.

Les mécanismes de supervision et de redémarrage doivent préserver la reprise des événements `PENDING`, `RETRYING` ou `FAILED` selon la politique de livraison. Un déploiement ne doit pas transformer une livraison `at-least-once` en suppression silencieuse des événements non publiés.

Les informations nécessaires à l'idempotence des Commands — clé, empreinte de payload, état et résultat lorsque nécessaire — doivent être persistantes et préservées lors des redémarrages, mises à niveau et recréations de conteneurs.

Les Jobs asynchrones et leurs états `PENDING`, `SCHEDULED`, `RUNNING`, `RETRYING`, `FAILED`, `CANCELLED` ou `DEAD_LETTER` doivent être persistants lorsque leur reprise est nécessaire. Leur exécution ne doit pas dépendre uniquement de la durée de vie d'un processus ou d'un conteneur.

Les états de Notification et les informations de déduplication doivent être persistants lorsqu'une reprise ou un diagnostic est nécessaire. Le packaging ne doit pas embarquer de provider de messagerie ou de secret de canal sans configuration runtime explicite.

---

# Partie I — Paquet Debian

## 6. Objectif du paquet Debian

Le paquet Debian fournit une installation native de Pixs sur un système Debian compatible.

Il doit permettre au gestionnaire de paquets de connaître et gérer l'installation de Pixs sans transformer le packaging Debian en nouvelle couche fonctionnelle de l'application.

Le paquet doit pouvoir prendre en charge, selon les spécifications OpenSpec correspondantes :

* les fichiers applicatifs ;
* les dépendances système ;
* les fichiers de configuration système ;
* les identités système nécessaires ;
* les permissions ;
* les répertoires runtime ;
* l'intégration avec le gestionnaire de services ;
* l'installation ;
* la mise à niveau ;
* la suppression ;
* la purge lorsque celle-ci est explicitement demandée.

---

## 7. Construction du paquet Debian

La construction doit être effectuée depuis une arborescence de travail contrôlée.

Le processus conceptuel est :

```text
Sources Pixs
     │
     ├── sélection du contenu distribuable
     ├── préparation des dépendances applicatives
     ├── préparation du frontend
     ├── génération des métadonnées Debian
     ├── création de l'arborescence du paquet
     ├── validation
     │
     ▼
  paquet .deb
```

Les répertoires de développement, caches, configurations d'agents, métadonnées Git, spécifications de travail et artefacts temporaires ne doivent pas être embarqués simplement parce qu'ils sont présents dans l'arborescence du projet.

Le contenu du paquet devra être défini explicitement par la spécification OpenSpec dédiée au packaging Debian.

---

## 8. Architecture Debian cible

L'installation Debian doit respecter autant que possible les conventions du système Debian et séparer les différentes catégories de données.

La spécification Debian devra déterminer explicitement l'emplacement de :

```text
code applicatif
configuration
données variables
journaux éventuels
fichiers runtime
ressources statiques
services système
```

Les chemins définitifs ne sont pas imposés par ce document.

Ils devront être choisis avant implémentation du packaging et spécifiés dans OpenSpec.

Les données applicatives persistantes ne doivent pas être mélangées au code immuable de l'application.

---

## 9. Dépendances Debian

Les dépendances système nécessaires à Pixs doivent être déclarées explicitement.

Une dépendance Debian ne doit être ajoutée que lorsqu'elle correspond à une nécessité réelle du runtime ou de l'installation.

Les dépendances Python ou frontend ne doivent pas être transformées arbitrairement en dépendances système Debian lorsque leur mode de distribution relève du packaging applicatif.

La stratégie exacte concernant :

* Python ;
* environnement Python ;
* dépendances Python ;
* Node.js ;
* dépendances frontend ;
* serveur applicatif de production ;

doit être déterminée par les spécifications techniques correspondantes avant finalisation du paquet.

---

## 10. Configuration Debian

Les fichiers de configuration administrables doivent rester distincts des fichiers applicatifs immuables.

Une mise à niveau du paquet ne doit pas écraser silencieusement une configuration locale valide administrée par l'exploitant.

Les valeurs dépendantes du déploiement doivent rester configurables après installation.

La configuration doit respecter les mécanismes communs définis par Pixs et ne doit pas introduire une seconde configuration fonctionnelle spécifique au paquet Debian.

Les paramètres d'authentification, les références de providers et les secrets associés aux identités numériques doivent rester des données de configuration runtime. Ils ne doivent jamais être intégrés au paquet ni préinitialiser des identités de production.

La configuration Debian doit alimenter la hiérarchie commune de Pixs : schéma, défauts du composant, configuration statique, configuration runtime puis références de secrets. Les fichiers administrés par l'exploitant ne doivent pas être écrasés silencieusement lors d'une mise à niveau.

Les secrets Debian doivent être fournis par un mécanisme runtime approprié et uniquement sous forme de références ou d'accès contrôlé. Ils ne doivent pas être inclus dans le paquet, ses métadonnées, ses journaux de construction ou ses scripts de maintenance.

---

## 11. Données et PostgreSQL

Le paquet Debian ne doit contenir aucune base PostgreSQL préinitialisée représentant des données métier de production.

PostgreSQL reste la source de vérité applicative indépendamment du mode de distribution.

Le paquet peut fournir les mécanismes nécessaires à l'utilisation des migrations Pixs, mais les migrations restent gouvernées par l'architecture applicative et les spécifications correspondantes.

Les migrations et scripts de maintenance ne doivent pas créer automatiquement des données tenant-scoped, des appartenances ou des permissions de production sans opération explicitement définie et auditable.

Les opérations de build, d'installation et de migration ne doivent pas remplacer les identifiants internes UUIDv7 par des entiers locaux ou des identifiants externes de provider. Les identifiants externes nécessaires au runtime doivent rester fournis par la configuration ou les systèmes d'intégration concernés.

Le packaging et les migrations doivent préserver les champs communs déclarés par les modules, notamment les identifiants UUIDv7, les horodatages UTC, les versions de concurrence et les références tenant. Une mise à niveau ne doit pas réinitialiser ces valeurs ni convertir silencieusement une ressource tenant-scoped en ressource globale.

Une suppression ou une mise à niveau du paquet ne doit pas entraîner implicitement la destruction des données applicatives.

---

## 12. Lifecycle Debian

Les opérations suivantes doivent être considérées séparément :

```text
installation
     │
mise à niveau
     │
suppression
     │
purge explicite
```

Une mise à niveau doit préserver les données persistantes et les secrets.

Une suppression non destructive ne doit pas supprimer implicitement les données métier.

La stratégie de suppression propre à un module — suppression physique, marqueur de suppression, archivage ou conservation — doit être explicitement définie et ne doit pas être modifiée silencieusement par le paquet ou l'image.

Une éventuelle purge destructive doit être explicitement définie et ne doit jamais résulter d'un comportement ambigu.

Les scripts de paquet doivent respecter les étapes de lifecycle applicables et ne doivent pas assimiler installation, activation, configuration, mise à niveau, désinstallation et purge. Une configuration ou compatibilité invalide doit produire un échec explicite avant le démarrage d'une nouvelle composition.

La mise à niveau d'un paquet doit préserver les manifests, versions de composants et contraintes de compatibilité nécessaires à la validation de la nouvelle composition. Une incompatibilité détectée ne doit pas être masquée par le script de maintenance.

Les scripts de maintenance Debian doivent être idempotents lorsque raisonnablement possible.

---

## 13. Service de production Debian

Le serveur de développement Django ne doit pas être utilisé comme serveur applicatif de production.

Le mécanisme exact utilisé pour exécuter Django en production sera défini par une spécification dédiée avant finalisation du paquet.

Lorsque Pixs est intégré à un gestionnaire de services système, celui-ci doit assurer uniquement les responsabilités d'exploitation nécessaires :

* démarrage ;
* arrêt ;
* redémarrage ;
* supervision du processus ;
* environnement runtime ;
* gestion correcte des codes de sortie.

Il ne doit pas absorber les responsabilités fonctionnelles du runtime Pixs.

---

# Partie II — Image Docker

## 14. Objectif de l'image Docker

L'image Docker fournit une exécution conteneurisée reproductible de Pixs.

Elle doit encapsuler les composants nécessaires à l'exécution de l'application tout en maintenant la configuration, les secrets et les données persistantes hors de l'image lorsque leur nature l'exige.

Principe :

```text
Image Pixs
   │
   ├── runtime système
   ├── runtime Python
   ├── application Pixs
   ├── dépendances applicatives
   ├── frontend construit
   └── entrypoint
           │
           ▼
      Conteneur
           │
           ├── configuration externe
           ├── secrets externes
           ├── PostgreSQL externe
           └── stockage persistant si nécessaire
```

---

## 15. Image de base

L'image de base doit être explicitement définie par la spécification OpenSpec Docker.

Elle doit être :

* compatible avec les runtimes nécessaires à Pixs ;
* maintenue ;
* suffisamment minimale ;
* adaptée à un usage de production ;
* cohérente avec les versions de Debian supportées par le projet lorsqu'une base Debian est retenue.

La version de l'image de base doit être maîtrisée afin d'éviter les changements implicites de runtime.

Le choix définitif de l'image et sa stratégie de verrouillage relèvent de la spécification Docker.

---

## 16. Construction multi-étapes

La construction Docker devrait séparer, lorsque cela apporte un bénéfice réel, les environnements nécessaires à la construction de ceux nécessaires à l'exécution.

Architecture cible possible :

```text
Builder backend
      │
      ├── dépendances de build Python
      └── préparation application
              │
              │
Builder frontend
      │
      ├── Node / outils frontend
      └── build TanStack
              │
              ▼
       Image runtime
              │
              ├── runtime Python
              ├── Pixs
              ├── dépendances runtime
              └── assets frontend construits
```

Les compilateurs, caches et outils exclusivement nécessaires au build ne devraient pas être conservés dans l'image runtime.

La structure définitive du Dockerfile sera spécifiée avant implémentation.

---

## 17. Contenu de l'image

L'image runtime doit contenir uniquement ce qui est nécessaire à l'exécution de Pixs.

Elle ne doit notamment pas embarquer inutilement :

* `.git/` ;
* configuration OpenCode ;
* données locales de développement ;
* caches de développement ;
* rapports temporaires ;
* secrets ;
* credentials ;
* clés privées ;
* configuration spécifique à une installation de production ;
* base PostgreSQL contenant des données métier.

Les spécifications OpenSpec et la documentation nécessaires au développement ne font pas partie du runtime par défaut, sauf décision explicitement justifiée.

---

## 18. Identité d'exécution

Pixs ne doit pas être exécuté avec des privilèges supérieurs à ceux nécessaires.

L'image devra définir explicitement :

* l'utilisateur runtime ;
* le groupe runtime ;
* les permissions nécessaires ;
* les répertoires accessibles en écriture.

Le processus applicatif ne devrait pas s'exécuter sous `root` lorsque cela n'est pas techniquement nécessaire.

Les éventuelles opérations nécessitant des privilèges élevés doivent être limitées, justifiées et séparées autant que possible de l'exécution normale.

---

## 19. Entrypoint

L'image Docker doit disposer d'un mécanisme de démarrage explicitement défini.

L'entrypoint doit rester un orchestrateur technique du runtime et ne doit pas devenir une seconde implémentation de la logique applicative Pixs.

Il peut notamment :

```text
charger l'environnement
        ↓
valider les préconditions runtime
        ↓
préparer les ressources locales nécessaires
        ↓
effectuer les opérations de démarrage autorisées
        ↓
lancer le processus applicatif
```

Les règles métier restent sous l'autorité de Django.

L'entrypoint doit propager correctement les signaux et permettre au processus applicatif d'être supervisé correctement par Docker.

---

## 20. Configuration Docker

La configuration dépendante du déploiement doit être fournie au runtime.

Elle peut provenir, selon les spécifications futures, de mécanismes tels que :

* variables d'environnement ;
* fichiers montés ;
* configuration externe ;
* mécanismes de secrets du moteur d'orchestration.

La configuration Docker doit alimenter le modèle de configuration commun de Pixs.

Elle ne doit pas créer une configuration fonctionnelle parallèle propre à Docker.

Le contexte tenant, le mode mono-tenant ou multi-tenant et les accès d'administration plateforme doivent être fournis par une configuration runtime validée. L'image ne doit pas embarquer un tenant ou une autorisation inter-tenant implicite.

Les variables d'environnement, fichiers montés et mécanismes de secrets Docker doivent être convertis vers le modèle de configuration commun de Pixs. Ils ne doivent pas introduire une priorité ou une clé fonctionnelle inconnue du schéma déclaré.

Les secrets Docker doivent être injectés au runtime et ne doivent apparaître dans aucune couche d'image, aucun Dockerfile, aucun log de build ou artefact publié. Une rotation doit pouvoir être effectuée sans reconstruire l'image lorsque le provider le permet.

Les identités numériques, comptes de service, sessions et secrets d'authentification ne doivent pas être créés implicitement par la construction de l'image. Leur provisionnement relève du runtime Pixs ou d'une opération d'administration explicitement définie.

---

## 21. Secrets Docker

Aucun secret de production ne doit être inscrit dans :

* le Dockerfile ;
* une couche de l'image ;
* le dépôt Git ;
* les ressources frontend ;
* les journaux de build ;
* les métadonnées publiques de l'image.

Un secret nécessaire au runtime doit être injecté depuis l'environnement de déploiement au moyen d'un mécanisme approprié.

Le build d'une image distribuable ne doit pas nécessiter l'intégration permanente d'un secret de production.

Les manifests `component.toml` et les métadonnées de version peuvent être présents dans l'image runtime lorsqu'ils sont nécessaires au diagnostic ou à la validation de composition. Ils ne doivent contenir aucune donnée secrète.

---

## 22. Persistance Docker

Le système de fichiers writable du conteneur doit être considéré comme éphémère sauf lorsqu'un stockage persistant est explicitement monté.

Les données métier ne doivent pas dépendre de la durée de vie du conteneur.

PostgreSQL reste la source de vérité applicative.

Les données persistantes relatives aux utilisateurs, identités numériques, comptes de service, méthodes d'authentification et révocations doivent rester dans les mécanismes de persistance prévus par Pixs. Elles ne doivent pas être stockées uniquement dans le système de fichiers éphémère du conteneur.

Les données tenant-scoped, memberships, rôles, ACL et journaux d'accès doivent également rester dans les mécanismes persistants prévus par Pixs. La recréation d'un conteneur ne doit pas modifier la frontière d'isolation ni accorder un accès supplémentaire.

Les états et résultats persistants nécessaires au suivi des Commands asynchrones ne doivent pas dépendre uniquement du système de fichiers éphémère du conteneur.

Les entrées d'outbox et leur état de publication ne doivent pas dépendre uniquement du système de fichiers éphémère du conteneur. Une recréation du conteneur doit permettre leur reprise selon les garanties du provider.

Les compteurs de tentatives, échéances de backoff et états `DEAD_LETTER` doivent rester observables et persistants lorsque la capacité de publication les utilise.

Une mise à niveau ou un redémarrage ne doit pas supprimer les Jobs planifiés ou en attente. Les changements incompatibles de contrat d'un Job doivent être détectés avant reprise ou traités par une migration explicite.

Une mise à niveau ou une recréation de conteneur ne doit pas supprimer silencieusement les notifications `QUEUED`, `SENDING` ou `FAILED`. Les providers de canal doivent être configurables au runtime et leurs secrets injectés selon les règles de gestion des secrets.

Une mise à niveau ne doit pas réinitialiser la fenêtre de déduplication d'une Command ni permettre la réexécution silencieuse d'une mutation déjà traitée.

La destruction puis la recréation d'un conteneur Pixs ne doit pas, à elle seule, provoquer la perte des données métier persistantes.

Les éventuels répertoires nécessitant un stockage persistant local devront être identifiés explicitement dans les spécifications correspondantes.

---

## 23. Ports et réseau

L'image doit exposer uniquement les interfaces réseau nécessaires au service applicatif.

Le port applicatif interne définitif sera fixé dans la spécification Docker/runtime.

La publication d'un port sur l'hôte relève du déploiement du conteneur et ne doit pas être confondue avec l'exposition interne de l'image.

Les dépendances externes, notamment PostgreSQL, doivent être accessibles au travers d'une configuration réseau explicite et non au moyen d'adresses codées en dur dans l'image.

---

## 24. Health checks

L'image Docker doit permettre de déterminer si Pixs est opérationnel.

Le health check ne doit pas se limiter à tester arbitrairement l'existence d'un processus lorsque l'état applicatif peut être vérifié plus précisément.

Le packaging et les tests runtime doivent distinguer les probes `liveness`, `startup`, `readiness` et le diagnostic détaillé. Ils doivent vérifier les délais, codes et états `HEALTHY`, `DEGRADED`, `FAILED` et `DISABLED`, l'évaluation des dépendances obligatoires et optionnelles, l'absence de mutation ou de secret dans les probes et la protection des détails opérateur. Une dépendance optionnelle indisponible ne doit pas rendre automatiquement l'artefact `unhealthy` si le mode dégradé est déclaré et cohérent.

Les niveaux exacts de santé seront coordonnés avec les capacités `runtime`, `observability` et `resilience`.

Le mécanisme devra éviter qu'une dépendance optionnelle indisponible rende automatiquement Pixs `unhealthy` lorsqu'un fonctionnement dégradé conforme est explicitement supporté.

---

## 25. Arrêt du conteneur

Pixs doit supporter un arrêt contrôlé.

Le processus principal doit recevoir les signaux d'arrêt du moteur de conteneurs et disposer du temps nécessaire pour terminer proprement les opérations en cours compatibles avec cette phase.

L'entrypoint ne doit pas empêcher la propagation correcte des signaux.

Le conteneur ne doit pas dépendre d'un mécanisme externe de destruction forcée pour son fonctionnement normal.

L'entrypoint ne doit pas effectuer implicitement une purge ou une opération destructive de lifecycle. Les opérations de migration, activation et health check doivent rester cohérentes avec le lifecycle Pixs et leurs échecs doivent être propagés explicitement.

---

# Partie III — Cohérence des distributions

## 26. Parité fonctionnelle

À version applicative identique :

```text
Pixs installé par .deb
          ≡
Pixs exécuté depuis image Docker
```

du point de vue des comportements fonctionnels définis par les spécifications.

Cela ne signifie pas que les deux environnements utilisent les mêmes mécanismes d'exploitation.

Les différences autorisées concernent notamment :

```text
                 Debian                 Docker
                 ──────                 ──────
installation     dpkg/apt               image
service          système hôte           runtime conteneur
configuration    système                injection runtime
filesystem       système hôte           image + mounts
lifecycle        paquet/service         conteneur
```

Ces différences ne doivent pas modifier les contrats fonctionnels de Pixs.

---

## 27. Versionnement

Le paquet Debian et l'image Docker doivent permettre d'identifier sans ambiguïté la version de Pixs qu'ils contiennent.

Une même version fonctionnelle doit être corrélable entre :

```text
version source
      │
      ├── paquet Debian
      └── image Docker
```

Le schéma exact de versionnement, de tags Docker et de versions Debian sera défini par la capacité OpenSpec de packaging correspondante.

Le build ne doit pas produire silencieusement deux artefacts portant la même version alors qu'ils correspondent à des sources fonctionnellement différentes.

---

## 28. Métadonnées de build

Lorsque nécessaire au diagnostic, un artefact doit pouvoir être relié aux sources ayant servi à sa construction.

Les métadonnées peuvent notamment représenter :

* version Pixs ;
* révision source ;
* date de construction ;
* architecture cible ;
* version du format de packaging.

Ces informations ne doivent contenir aucun secret ni information sensible propre à l'environnement de construction.

Les artefacts doivent conserver les métadonnées nécessaires à la corrélation du composant, de sa version, de ses contrats et de sa construction avec les diagnostics runtime. Le build ne doit pas inclure de secret, token, payload utilisateur, configuration de production ou donnée personnelle dans les métadonnées, journaux, bundles ou rapports générés.

Le build doit valider la présence des politiques de rétention, de portée et d'accès déclarées pour les signaux et diagnostics distribués. Il doit vérifier que les mécanismes d'expiration, de pseudonymisation, de legal hold et d'anonymisation contrôlée sont identifiables, que les accès inter-tenant sont auditables et qu'aucune donnée technique sensible n'est conservée implicitement dans un artefact ou un rapport.

---

## 29. Validation des artefacts

Un build terminé techniquement ne suffit pas à considérer un artefact comme valide.

Le processus de validation devra couvrir progressivement :

```text
sources
   ↓
build
   ↓
validation structurelle
   ↓
tests
   ↓
installation / démarrage
   ↓
health
   ↓
tests fonctionnels essentiels
```

La validation des artefacts doit également vérifier que la composition de composants est déterministe, que les dépendances obligatoires sont satisfaites, que les dépendances optionnelles sont correctement signalées et qu'aucun provider ambigu n'est sélectionné.

Elle doit aussi vérifier la cohérence des contrats publics déclarés, la compatibilité de leurs versions et, lorsque disponible, les tests de conformité associés aux providers et services.

Pour les API, la validation doit également couvrir la présence ou la génération du contrat OpenAPI, les tests de contrat, les exemples versionnés, le contrôle automatique de compatibilité et l'échec du build en cas de rupture non déclarée, la cohérence des schémas et des préfixes `/api/vN`, l'absence de rupture non déclarée dans une version majeure, les versions publiées, la déclaration des exigences d'authentification et des routes publiques, la résolution vers une `DigitalIdentity`, la déclaration des routes tenant-scoped et platform-scoped, la vérification du contexte tenant, l'enveloppe de succès (`data`, `meta`, `links`), la pagination par curseur, les filtres et tris autorisés, les plafonds de taille de page, les règles `ETag`, `If-None-Match`, `If-Match` et `Cache-Control`, la déclaration et la persistance des `Idempotency-Key`, la déclaration des limites de débit et de leurs dimensions, la représentation correcte des réponses `429`, des Commands asynchrones en `202`, les enveloppes et signatures des webhooks sortants et entrants, les mécanismes de protection contre le rejeu, les règles CORS et CSRF par environnement, les limites de taille JSON/multipart/upload, les budgets de durée et les réponses `413`, `408` et `504`, les formats `Content-Type`/`Accept`, les erreurs `415` et `406`, la sérialisation RFC 3339 UTC et la stabilité des codes et structures non localisés, les références de secrets, les politiques de retries et de dead-letter, l'enveloppe d'erreur standard (`error_code`, `message`, `details`, `field_errors` optionnel et `correlation_id`) et l'absence d'exposition involontaire de détails privés, de secrets ou de traces d'exécution.

Les tests frontend doivent également vérifier la résolution déterministe des contributions, le chargement des extensions, les collisions, les contrats de routes et de slots, les traductions, les permissions d'affichage et le respect des APIs publiques du shell. Ils doivent confirmer qu'une extension frontend ne peut pas remplacer une décision d'autorisation backend.

Pour le paquet Debian, les validations devront notamment permettre de vérifier :

* la validité du paquet ;
* ses métadonnées ;
* son contenu ;
* ses dépendances ;
* son installation ;
* sa mise à niveau ;
* sa suppression ;
* la préservation des données et configurations concernées.

Pour Docker, elles devront notamment permettre de vérifier :

* la construction de l'image ;
* son contenu ;
* l'identité runtime ;
* le démarrage ;
* la configuration externe ;
* la connectivité PostgreSQL ;
* le health check ;
* l'arrêt contrôlé ;
* la recréation du conteneur ;
* l'absence de secrets intégrés à l'image.

---

## 30. Tests de packaging

Les tests de packaging doivent compléter les tests applicatifs et ne pas les remplacer.

Les tests applicatifs valident Pixs.

Les tests de packaging valident que Pixs est correctement transporté et exécuté dans un environnement donné.

```text
Tests Pixs
    │
    ├── tests applicatifs
    │
    ├── tests de contrats
    │
    ├── tests d'intégration
    │
    └── tests de packaging
             │
             ├── Debian
             └── Docker
```

Un échec propre au packaging ne doit pas être masqué comme un échec fonctionnel générique de Pixs.

---

## 31. Sécurité de la chaîne de build

La construction doit respecter le principe du moindre privilège.

Le processus de build ne doit pas exiger un accès aux secrets de production simplement pour produire les artefacts distribuables.

Les entrées externes utilisées pendant la construction doivent être maîtrisées autant que raisonnablement possible.

Les journaux de construction ne doivent pas exposer :

* mots de passe ;
* tokens ;
* clés privées ;
* credentials ;
* valeurs de configuration marquées comme secrètes.

Les fichiers temporaires contenant des informations sensibles doivent être évités ou protégés et supprimés après utilisation.

Le build doit produire un SBOM couvrant les dépendances applicatives, frontend, système et de packaging lorsque leur inventaire est disponible. Il doit vérifier les profils de sécurité des composants, scanner les secrets, analyser le code et les dépendances, contrôler les vulnérabilités des paquets et images, calculer les empreintes, vérifier les signatures et produire une attestation de provenance reliée aux sources, à la configuration de build et aux entrées principales. Une vulnérabilité critique connue doit bloquer la publication. Une exception de vulnérabilité élevée doit être documentée, approuvée, limitée dans le temps et incluse dans le diagnostic de l'artefact.

Les vérifications doivent être exécutables pour les chemins Debian, Docker et développement avec des garanties équivalentes, même si les outils d'analyse sont fournis par des adapters différents. Les rapports doivent être exportables et ne doivent pas inclure de secret, token, contenu utilisateur ou détail sensible non nécessaire.

Les validations doivent vérifier les scénarios fail-closed : secret absent ou expiré, signature invalide, provenance non vérifiable, permission manquante, contexte tenant ambigu, provider révoqué et artefact altéré. Elles doivent confirmer qu'aucun de ces cas n'accorde un accès ou ne déclenche une mutation, qu'une capacité optionnelle peut être isolée sans contourner la sécurité et que chaque blocage ou réactivation produit le diagnostic et l'audit attendus.

Le build et les tests d'exploitation doivent vérifier le traitement des avis de sécurité, la vérification de révocation aux étapes d'installation, démarrage et mise à niveau, le blocage d'un artefact compromis, la procédure de désactivation d'urgence, la production de la timeline d'incident, la notification prévue et la restauration sans purge implicite des données. Les tests de reprise utilisent des fixtures ou données synthétiques et ne doivent pas nécessiter de secret de production.

---

## 32. Artefacts de construction

Les artefacts produits doivent être séparés des sources.

Une organisation de principe pourra être :

```text
projet Pixs
├── sources
├── packaging
│   ├── debian
│   └── docker
└── dist
    ├── debian
    └── docker
```

Cette arborescence est illustrative et non normative.

Les chemins définitifs seront fixés lors de la spécification et de l'implémentation des capacités de packaging.

Les artefacts générés et reproductibles ne doivent pas devenir des sources fonctionnelles de Pixs.

---

## 33. Publication

La construction et la publication constituent deux responsabilités distinctes.

```text
build
  ↓
artefact local
  ↓
validation
  ↓
publication
```

La construction d'un paquet ou d'une image ne doit pas entraîner implicitement sa publication dans un dépôt distant sauf workflow explicitement défini.

Les mécanismes futurs de publication pourront notamment concerner :

* dépôt Debian ;
* registre d'images Docker ;
* Release de forge ;
* chaîne CI/CD.

Ils devront être spécifiés séparément du mécanisme de construction lorsque leurs responsabilités diffèrent.

---

## 34. Compatibilité et mises à niveau

Les deux formats de distribution doivent respecter les règles de compatibilité définies par Pixs.

Une mise à niveau doit notamment prendre en compte :

* version applicative ;
* migrations ;
* contrats publics ;
* configuration ;
* compatibilité des composants ;
* dépendances système ;
* dépendances externes.

Le packaging ne doit pas contourner les mécanismes de compatibilité du framework.

Une incompatibilité connue doit produire un diagnostic explicite plutôt qu'une composition implicitement dégradée ou non déterministe.

Une mise à niveau ne doit pas supprimer ou modifier silencieusement un contrat public consommé par un autre composant. Toute rupture doit être détectée avant activation et respecter la politique Pixs : dépréciation annoncée dans une version mineure, maintien pendant la version majeure courante et suppression au plus tôt dans la version majeure suivante, sauf exception explicitement justifiée.

Une mise à niveau ne doit pas élargir implicitement le périmètre d'accès d'une identité, d'un groupe, d'un rôle ou d'un tenant. Toute modification de memberships, rôles ou ACL doit être portée par une migration ou une opération d'administration explicite, traçable et réversible lorsque cela est possible.

---

## 35. Déterminisme

À sources, versions de dépendances et paramètres de build équivalents, le processus de construction doit tendre vers un comportement déterministe.

Le build ne doit notamment pas sélectionner implicitement :

* un provider ;
* un module ;
* une configuration ;
* une dépendance alternative ;

en fonction de l'ordre du filesystem ou d'un état accidentel de la machine de construction.

Les principes de résolution déterministe de Pixs restent applicables aux artefacts distribués.

---

## 36. Éléments volontairement non figés

Le présent document ne fixe volontairement pas encore :

* la version Debian minimale supportée ;
* l'architecture CPU ou les architectures supportées ;
* le nom exact du paquet Debian ;
* le schéma exact de version Debian ;
* l'arborescence Debian définitive ;
* le format précis des scripts de maintenance Debian ;
* le serveur applicatif Django de production ;
* le mécanisme de gestion du frontend dans le paquet ;
* l'image Docker de base exacte ;
* son éventuel digest ;
* le nom exact du Dockerfile ;
* la structure définitive du build multi-stage ;
* l'utilisateur et le groupe runtime ;
* les UID/GID ;
* le port interne de Pixs ;
* les volumes Docker ;
* le format exact de l'entrypoint ;
* les commandes exactes de migration au démarrage ;
* la stratégie de collecte des fichiers statiques ;
* la stratégie précise de health check ;
* le nom du registre Docker ;
* le nom de l'image ;
* la convention de tags ;
* le dépôt Debian cible ;
* la stratégie de signature des artefacts ;
* la stratégie CI/CD de publication.

Ces décisions doivent être prises dans les spécifications OpenSpec appropriées avant que leur implémentation ne soit considérée comme normative.

---

## 37. Capacités OpenSpec recommandées

Le packaging devrait être spécifié par capacités indépendantes plutôt que comme une extension implicite du runtime.

Une décomposition initiale possible est :

```text
openspec/specs/
├── ...
├── deb-package/
│   └── spec.md
├── docker-image/
│   └── spec.md
└── runtime/
    └── spec.md
```

Des capacités supplémentaires pourront être créées si leur responsabilité devient suffisamment distincte, par exemple pour :

```text
artifact-publication
release-management
production-runtime
```

Cette décomposition n'est pas normative tant qu'elle n'a pas été introduite et validée dans OpenSpec.

---

## 38. Frontières de responsabilité

Les responsabilités doivent rester clairement séparées :

```text
PROJECT.md
    │
    └── définit le cadre global et les invariants du projet

OpenSpec
    │
    └── définit les comportements normatifs et vérifiables

BUILD.md
    │
    └── définit le cadre technique de construction des artefacts

Packaging Debian / Docker
    │
    └── implémente les spécifications de distribution

Runtime Pixs
    │
    └── compose et démarre l'application

Django
    │
    └── reste l'autorité des règles et mutations métier

PostgreSQL
    │
    └── reste la source de vérité applicative
```

Aucun mécanisme de packaging ne doit déplacer silencieusement une responsabilité d'une couche vers une autre.

---

## 39. Principe final

Le build doit rester une transformation contrôlée :

```text
                 Sources Pixs
                      │
                      ▼
              Build reproductible
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
      paquet Debian        image Docker
            │                   │
            └─────────┬─────────┘
                      ▼
                 Runtime Pixs
                      │
                      ▼
                    Django
                      │
                      ▼
                 PostgreSQL
               SOURCE DE VÉRITÉ
```

Le paquet Debian et l'image Docker transportent Pixs.

Ils ne redéfinissent pas Pixs.

## 40. Stockage, recherche, workflows et synchronisations

Les artefacts de build ne doivent contenir aucun fichier utilisateur, credential, token, endpoint privé ou configuration de production provenant d'un provider. Les credentials nécessaires aux tests sont injectés à l'exécution et proviennent de fixtures ou de secrets de test contrôlés.

Les providers de stockage objet doivent être soumis à une suite de conformité commune. Les tests peuvent utiliser un filesystem temporaire, un service S3-compatible de test ou une instance dédiée, mais ne doivent jamais accéder au répertoire interne d'une instance Nextcloud ni au bucket primaire qu'elle gère exclusivement.

Pour un `ObjectStorageProvider`, le build et les tests runtime doivent vérifier :

* la configuration externe de l'endpoint, du bucket et des credentials ;
* l'absence de secret dans les paquets, images, logs et rapports ;
* la création réservée et la finalisation d'un objet ;
* les uploads multipart et la reprise lorsqu'ils sont déclarés ;
* la taille, le type et le checksum ;
* les états `PENDING`, `UPLOADING`, `QUARANTINED`, `AVAILABLE`, `FAILED`, `DELETED` et `EXPIRED` ;
* l'accès privé et les URLs temporaires ;
* la suppression logique, la purge différée et les legal holds ;
* la détection d'objets orphelins et la réparation explicite ;
* la séparation des tenants, des permissions et des références externes ;
* l'immuabilité des objets finalisés et la création des versions.

L'adapter Nextcloud doit être testé contre une instance locale ou distante dédiée, selon les mêmes contrats fonctionnels. Les tests vérifient l'usage d'une interface publique, la validation TLS lorsque nécessaire, l'identité de service, les versions, les `ETag`, les verrous, les erreurs de connexion, les limites de débit et l'absence d'accès direct au volume ou au bucket primaire de Nextcloud.

Les deux modes documentaires doivent être testés séparément :

* dans le mode piloté par Pixs, les écritures passent par une Command autorisée, les modifications externes inattendues sont détectées comme divergences et l'état Pixs n'est pas remplacé silencieusement ;
* dans le mode externe, les modifications Nextcloud sont importées selon les mappings, les checkpoints et la stratégie de conflit déclarés, avec prise en compte des replays, suppressions et versions concurrentes.

Les tests de recherche doivent vérifier que le provider est sélectionné explicitement, que les index sont dérivés et reconstruisibles, que les projections respectent le tenant et les ACL, que les suppressions et expirations sont répercutées, que les filtres et tris non déclarés sont rejetés, que les curseurs restent valides, que les limites de requête sont appliquées et que le retard ou l'indisponibilité de l'index est observable. La reconstruction doit être idempotente et ne doit pas modifier la source de vérité. Un provider de recherche indisponible ne doit pas autoriser un contournement des ACL ni provoquer une mutation implicite.

Les tests de workflow doivent vérifier la persistance des définitions et instances, la sélection de la version interprétée, les transitions autorisées, le déterminisme des gardes, les permissions, les délais, les retries, l'idempotence, l'annulation, la reprise, la dead-letter, l'intervention manuelle et l'absence d'exécution arbitraire de code. Les instances en cours doivent rester interprétables lorsqu'une nouvelle version de définition est publiée ; toute migration nécessaire doit être explicite, testée et réversible lorsque cela est possible.

Les tests de synchronisation doivent couvrir les modes `IMPORT`, `EXPORT`, `BIDIRECTIONAL` et `PROJECTION`, les modes d'autorité `PIXS`, `EXTERNAL` et `EXPLICIT_BIDIRECTIONAL`, les mappings d'identifiants, les cursors, checkpoints, webhooks, polling, replays, backoff, quotas, dead-letters, pertes de connexion, divergences, suppressions et conflits. Ils doivent confirmer que la source d'autorité, la stratégie de conflit et la politique de suppression sont déclarées, qu'une valeur absente ou ambiguë bloque l'activation, et qu'aucune modification externe ne contourne une Command, l'autorisation ou l'audit Pixs.

Ils doivent également vérifier la sélection déterministe du provider, les états `PENDING`, `RUNNING`, `PAUSED`, `DEGRADED`, `FAILED`, `CONVERGED` et `QUARANTINED`, la suspension et la reprise autorisées, la réinitialisation contrôlée des checkpoints, la validation des signatures et fenêtres de rejeu, la rotation des secrets, les scopes minimaux, la propagation des corrélations et l'absence de secret ou de payload sensible dans les diagnostics. Les tests de rejeu et de reprise doivent confirmer l'idempotence et l'absence de suppression ou duplication non déclarée.

Les environnements Debian, Docker et développement doivent exposer la même configuration conceptuelle de ces providers. Une dépendance optionnelle indisponible peut produire un état `DEGRADED` lorsqu'un fonctionnement cohérent est déclaré ; elle ne doit pas provoquer une sélection implicite d'un provider différent ni une perte silencieuse de données.

Les validations doivent confirmer le caractère stateless du runtime : aucune donnée métier, session durable, clé d'idempotence, file, lease, checkpoint ou état de synchronisation ne doit dépendre du filesystem local ou de la mémoire d'un processus. Les tests doivent couvrir une installation mono-instance puis plusieurs instances web, workers et schedulers partageant les mêmes services persistants.

Les artefacts et images doivent pouvoir démarrer les rôles `web`, `worker` et `scheduler` à partir du même contenu, avec une configuration de rôle externe et validée. Les tests de développement peuvent couvrir un mode regroupé ; les tests de production doivent vérifier la séparation explicite des rôles, le lease persistant du scheduler, son expiration, la reprise après perte de lease et la montée en charge de plusieurs workers.

Les scénarios de redémarrage, recréation de conteneur, remplacement de paquet et montée en charge doivent vérifier la reprise des Jobs, de l'outbox, des synchronisations et des workflows sans perte ni double traitement non déclaré. Les verrous et leases locaux ne peuvent être acceptés que s'ils sont explicitement non autoritatifs. Les adapters systemd, runtime conteneur et orchestrateur doivent conserver les mêmes comportements applicatifs.

Les validations d'exploitation doivent vérifier la stratégie de sauvegarde et de restauration déclarée par déploiement : objectifs `RPO` et `RTO`, sauvegarde PostgreSQL, conservation ou versionnement des objets, protection de la configuration et des secrets, contrôle d'accès, rétention et journaux d'opération. Les tests de restauration doivent utiliser un environnement isolé et confirmer la cohérence des modèles, migrations, outbox, Jobs, idempotences, workflows, audits, fichiers, checksums, mappings, checkpoints, identités, tenants et ACL.

Une restauration doit également vérifier le démarrage contrôlé, les health checks, la reprise idempotente, la détection des versions incompatibles, le traitement des événements non publiés et l'état des synchronisations externes. Le build ou le runtime ne doit jamais lancer automatiquement une purge, un downgrade de schéma, une réinitialisation des identités ou une suppression de fichiers pour masquer un écart de restauration.

Les validations doivent couvrir un déploiement avec interruption courte ainsi que, lorsque les adapters correspondants existent, les stratégies rolling, blue/green et canary. Les scénarios progressifs doivent vérifier la coexistence temporaire des versions `N` et `N+1`, la compatibilité des API, événements, schémas et données partagés, l'arrêt du trafic vers une instance non prête et le retrait de l'ancienne version seulement après validation de la nouvelle.

Les migrations destructives doivent être testées comme une étape séparée et bloquées tant qu'une ancienne version ou un consommateur compatible peut encore utiliser la structure concernée. Le build doit vérifier la séquence expansion, compatibilité, migration des usages, retrait puis contraction, ainsi que la possibilité de revenir à une version compatible sans downgrade automatique de la base.

Les validations doivent confirmer qu'une mise à jour applicative ne s'exécute que sur déclenchement explicite ou via un mécanisme d'exploitation autorisé et traçable. Elles doivent vérifier l'existence d'un plan d'upgrade, la validation de la provenance et de la signature, les préconditions, les migrations, les contrats affectés, les health checks, le résultat, les diagnostics et le rollback autorisé. Une tentative automatique non autorisée, une migration destructive non approuvée ou une activation partielle doit être refusée.

Les mises à jour de sécurité automatisées par l'environnement doivent être testées comme un chemin distinct. Elles peuvent accélérer le déclenchement, mais ne doivent pas contourner les contrôles de compatibilité, d'intégrité, de configuration ou de récupération. Un échec doit préserver l'ancienne version ou produire un état sûr et diagnostiquable.

Le build doit tester les chemins d'upgrade depuis les versions supportées, l'ordre des migrations intermédiaires, les changements de version majeure, les versions hors support et les origines sans chemin vérifiable. Il doit bloquer un saut de version non déclaré, signaler la version intermédiaire requise et vérifier que les périodes de support, de dépréciation et de fin de vie sont cohérentes avec les manifests, contrats, migrations et artefacts publiés.

Le build doit produire et vérifier les métadonnées de canal : `stable`, `security` ou `experimental`. Il doit confirmer que les artefacts `security` restent compatibles avec la release supportée, que les artefacts expérimentaux ne sont pas sélectionnés par défaut, que la version et le digest identifient sans ambiguïté l'artefact et qu'un tag mutable comme `latest` n'est pas utilisé comme preuve de provenance ou de compatibilité.

Le build doit signer les artefacts `stable`, `security` et `experimental`, produire leur SBOM et leur attestation de provenance, puis vérifier la signature et la chaîne de confiance dans les scénarios d'installation, de démarrage et de mise à niveau. Les tests doivent couvrir signature absente, invalide, expirée, révoquée ou liée à un mauvais canal, et confirmer le blocage avant toute mutation persistante. Les clés privées et credentials de signature restent hors des artefacts, journaux et fixtures versionnées.

Le build et la publication doivent vérifier l'autorité attendue pour chaque canal, le trust store de l'environnement, la rotation avec chevauchement, la révocation et le refus d'une clé expérimentale pour un artefact `stable` ou `security`. Les tests doivent pouvoir fonctionner avec des clés synthétiques dédiées, sans accès à une clé privée de production, et couvrir la vérification hors ligne lorsque le dépôt de publication est indisponible.

Les tests de packaging et d'exploitation doivent valider la CLI et les façades non interactives de management : inspection, validation, génération de plan, migration, upgrade, rollback autorisé, health et diagnostic. Ils doivent vérifier la stabilité des codes de sortie, l'idempotence des commandes, la persistance du suivi des opérations longues, la séparation avec l'API métier, l'autorisation de l'acteur et l'audit. Les sorties doivent être contrôlées pour confirmer l'absence de secret, token, clé privée, credential ou payload sensible.

Les tests d'exploitation doivent couvrir l'entrée et la sortie de `MAINTENANCE`, le drainage borné des requêtes et traitements en cours, le refus des nouvelles mutations, la politique de lecture, la suspension ou reprise des Jobs et synchronisations, les health checks, les permissions opérateur, la reprise après redémarrage et l'audit de la cause et de l'acteur. Ils doivent confirmer qu'une requête métier bloquée n'est pas exécutée partiellement et qu'une sortie de maintenance ne réactive pas le trafic avant validation de la composition et des dépendances.

Ils doivent également vérifier le comportement par défaut en lecture seule : Queries compatibles acceptées, Commands métier et asynchrones refusées, Jobs et synchronisations suspendus, réponse API stable, absence de mutation partielle et traitement séparé des opérations d'administration ou de sécurité explicitement autorisées.

## 41. Validation des releases, upgrades et exploitation

Le build doit produire des artefacts Debian et OCI/Docker corrélables à la même version fonctionnelle, à la même source et à la même composition de composants. Les artefacts publiés doivent être immuables ; une modification de source ou de composition doit produire un nouvel identifiant ou une nouvelle version. Les tags pratiques ne remplacent pas l'identification par version et digest lorsque le registre le permet.

La validation d'une mise à niveau doit exécuter au minimum :

```text
artefact et provenance
    ↓
composition et compatibilité
    ↓
plan de migration
    ↓
migration sur données de test représentatives
    ↓
startup
    ↓
readiness / health
    ↓
tests fonctionnels et arrêt contrôlé
```

Les tests doivent confirmer qu'une migration échouée, une incompatibilité ou un health check bloquant empêche l'activation de la nouvelle version. Ils doivent vérifier qu'un downgrade de base de données n'est jamais lancé automatiquement et qu'un rollback applicatif est refusé lorsque la compatibilité avec le schéma courant n'est pas démontrée.

Le paquet Debian doit être testé avec son adapter systemd ou équivalent de service ; l'image OCI/Docker doit être testée avec un runtime de conteneurs. Les deux chemins doivent vérifier les mêmes migrations, configurations, secrets externes, health checks, signaux d'arrêt, préservation des données et diagnostics. Les tests Kubernetes, Nomad ou autres orchestrateurs sont optionnels et ne doivent pas être requis pour valider le Kernel ou la release de base.

Les suites de conformité des providers sont versionnées avec leurs contrats et exécutées dans une matrice de validation :

```text
ObjectStorageProvider
    local / S3-compatible

DocumentRepositoryProvider
    Nextcloud local / Nextcloud distant

SearchProvider
    projection / reconstruction / filtrage sécurisé

Workflow runtime
    définition / transition / reprise / migration

SynchronizationProvider
    import / export / bidirectionnel / projection
```

Pour chaque entrée, le build doit distinguer les tests de contrat, d'intégration, de sécurité, de reprise et de packaging. Les tests utilisent des données synthétiques, des fixtures et des instances dédiées. Ils ne doivent pas exiger de secret de production, intégrer de credential dans un artefact ou accéder au volume interne de Nextcloud.

Une incompatibilité obligatoire, une violation d'isolation tenant, un contournement d'autorisation, une perte d'idempotence, une sélection ambiguë ou une exposition de secret bloque la validation. Une capacité optionnelle peut être marquée `DEGRADED` ou `DISABLED` uniquement si son absence est déclarée, diagnostiquée et sans perte silencieuse de données.
## 42. Providers concrets et modules métier

Le build doit traiter séparément les composants `CORE`, `OFFICIAL`, `EXTERNAL` et `PRIVATE`. Il doit vérifier leurs manifests, versions, capacités, dépendances, contrats, configuration, niveau de confiance, provenance, signatures et tests de conformité. Un provider présent dans un artefact ne doit pas être activé automatiquement.

Les providers officiels doivent être testés comme des implémentations de référence sans devenir des dépendances implicites du Kernel. Les providers externes et privés doivent être vérifiés par les mêmes suites de contrat lorsqu'ils déclarent une compatibilité. Une incompatibilité, une ambiguïté de résolution, une capacité obligatoire absente ou une signature non conforme bloque la composition.

Le build des modules métier doit vérifier la propriété des modèles et migrations, l'identification des permissions et ressources, la présence des contrats publics, l'absence d'écriture directe dans les modules voisins et la séparation entre code métier et providers d'intégration. Les modules ou providers non sélectionnés ne doivent pas modifier les artefacts, les migrations ou la configuration effective d'une installation.

La sélection du provider doit être reproductible entre Debian, Docker et développement. Le build doit refuser qu'un ordre d'import, un chemin de filesystem, une dépendance transitive ou la simple présence d'un paquet choisisse implicitement l'implémentation active.
