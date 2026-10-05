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

### Convention normative RFC 2119

Les contraintes de build, de packaging et de distribution qui sont vérifiables sont spécifiées dans OpenSpec avec les mots-clés RFC 2119 `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT` et `MAY`, en majuscules, au sein d'une prose française. `MUST` et `MUST NOT` bloquent la validation lorsqu'ils ne sont pas satisfaits ; tout écart à `SHOULD` ou `SHOULD NOT` doit être justifié et traçable ; `MAY` exprime une option sans activation implicite. Les interdictions utilisent exclusivement `MUST NOT` ou `SHOULD NOT` ; une forme hybride telle que `NE MUST` n'est pas valide. Les formulations françaises ou en minuscules des explications de ce document ne constituent pas des mots-clés RFC 2119.

Le build doit vérifier les exigences applicables et ne peut ni réinterpréter, ni assouplir, ni contourner une clause RFC 2119 définie par une spécification OpenSpec validée.

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

Le modèle commun `Component` constitue une entrée obligatoire de la composition de build. Le build doit vérifier l'unicité des identifiants, le schéma du manifest, les versions de composants, contrats et capacités, les dépendances obligatoires et optionnelles, l'absence de cycles, les propriétaires de données et migrations déclarés, ainsi que les permissions, points d'entrée et profils de sécurité nécessaires. Une composition invalide ne doit pas produire un artefact activable.

Les contrats d'extension doivent être validés au même titre que les autres contrats publics. Le build vérifie pour chaque contribution son identifiant namespacé, son composant cible, son point d'extension, sa version, son point d'entrée, ses dépendances, ses collisions, ses conditions d'activation et sa compatibilité avec l'API consommée. Une contribution non déclarée, ambiguë, incompatible ou extérieure au périmètre du composant doit bloquer la composition concernée.

Le build doit résoudre les capacités fournies et requises dans le graphe de composition, avec leur version, leur contrat, leur provider, leur caractère obligatoire ou optionnel et leur politique de repli. Il doit refuser une capacité obligatoire absente, incompatible ou bloquée ; une capacité optionnelle indisponible doit rester isolée et être diagnostiquée. Un feature flag ne peut pas modifier ce graphe ni remplacer la résolution d'une capacité.

Le build doit valider les définitions de feature flags déclarées par les composants : identifiant namespacé, version, propriétaire, finalité, type de valeur, défaut, dimensions de ciblage, prérequis, repli, expiration et audit. Les règles doivent être déclaratives, bornées et déterministes. Les affectations d'installation, d'environnement, de tenant et de scope sont fournies au runtime ; elles ne doivent pas être embarquées dans un paquet, une image ou un bundle, et ne doivent contenir ni secret ni donnée de production non déclarée.

Le build doit également valider le modèle de scopes déclaré par les composants : unicité des types et identifiants de scopes, `Tenant` comme racine, parent unique pour chaque scope enfant, absence de cycle, règles d'appartenance explicites et compatibilité des ressources avec leur périmètre. Il doit rejeter toute ressource déclarée avec un `scope_id` sans `tenant_id` cohérent, toute ressource possédant plusieurs propriétaires canoniques et toute extension qui élargit implicitement son contexte d'accès.

Les providers d'authentification doivent déclarer leurs capacités, protocoles, issuers, audiences, méthodes, algorithmes, clés, claims obligatoires, mappings d'identifiants et niveaux d'assurance maximaux. Le build doit vérifier la cohérence de ces déclarations, l'unicité du triplet `(provider_id, issuer, subject)`, l'absence de confiance implicite et l'absence de credentials, tokens ou assertions brutes dans les manifests et artefacts.

Le build doit valider les déclarations du moteur d'autorisation : identifiants et versions de politiques, composants propriétaires, selectors de sujets, ressources, actions et scopes, effets `DENY` ou `ALLOW`, conditions typées, obligations et périodes de validité. Il doit refuser toute politique ambiguë, non namespacée, cyclique, non bornée ou contenant du code exécutable. Les dépendances vers des implémentations privées et les PDP externes non déclarés doivent bloquer la composition.

Le build doit valider les politiques de cycle de vie déclarées par les modules : séparation de l'état métier et des états de persistance, de rétention et de projection ; stratégie de suppression ; durée de rétention ; restauration ; conditions de purge ; legal holds ; cascade ; historique et synchronisation. Il doit vérifier que `RESTRICT` est la règle inter-modules par défaut, qu'une purge dispose d'un contrat de Job idempotent et qu'un tombstone ou journal d'effacement est prévu lorsque des projections, caches, synchronisations ou restaurations pourraient résurrectionner une donnée. Une politique ambiguë, incompatible avec les migrations ou permettant une cascade SQL implicite doit bloquer la composition.

Le build doit également valider le `DataGovernanceProfile` de chaque composant qui introduit, dérive ou transfère des données : version, propriétaire, source de vérité, classes de données, confidentialité, données personnelles, finalités, rétention, suppression, consommateurs, processeurs, contraintes de résidence ou de transfert, politique d'export et lignée. Il doit refuser une classification inconnue, une source de vérité ambiguë, un flux sortant sans consommateur déclaré ou une contrainte de transfert sans garantie compatible. Les valeurs de secret, credentials et données personnelles réelles sont interdites dans les profils, exemples, manifests et artefacts.

Les contrôles de gouvernance doivent vérifier que les données non classifiées restent soumises à une politique restrictive et ne sont pas exposées, exportées, publiées dans un événement d'intégration ou transférées à un provider. Le build doit aussi vérifier la compatibilité entre gouvernance, cycle de vie, migrations, projections, caches, fichiers, sauvegardes et synchronisations, ainsi que la présence d'un contrat générique pour les demandes d'accès, d'export, de rectification, d'effacement ou de restriction lorsque le composant déclare cette capacité.

Le build doit valider les contrats `BulkOperation` déclarés par les composants : version, variantes `IMPORT`/`EXPORT`, états, rattachement à `operation_id`, Jobs, tenant et scope. Il doit vérifier les formats `CSV` et `NDJSON`, les adapters optionnels, les mappings versionnés, les limites de taille et de lignes, les contrôles de type et de checksum, le staging privé, les champs autorisés, les modes `VALIDATE_ONLY`, `ATOMIC`, `ATOMIC_PER_CHUNK` et `BEST_EFFORT`, ainsi que les stratégies de conflit et d'idempotence.

Pour les exports, il doit contrôler la déclaration des projections, champs, filtres et tris autorisés, l'usage de `filter_authorized`, le snapshot ou watermark, le manifeste, la classification, la rétention et la référence de fichier temporaire. Les profils de build ne doivent contenir ni données utilisateur réelles, ni secret, ni fichier de production ; le build ne doit ni créer de tenant ou scope, ni produire un mapping qui élargit l'autorisation.

Le build doit valider les contrats de Commands, Events et Jobs : identifiants et versions, schémas de payload, contexte d'identité et de scope, corrélation, causalité, idempotence, garanties transactionnelles, modes synchrones ou asynchrones, ordre déclaré, politique de retry, lease, délai, dead-letter et limites de reprise. Il doit distinguer les événements de domaine internes des événements d'intégration publics et refuser tout handler, consommateur ou Job qui introduit une mutation ou une dépendance privée non déclarée.

La composition de référence des extensions frontend est réalisée au build à partir des sources ou artefacts versionnés du composant. Le runtime ne télécharge ni n'installe de code pour activer une extension et ne doit pas évaluer de code distant. Un adapter distant ultérieur doit être explicitement sélectionné et vérifier provenance, intégrité, signature, permissions, isolation et compatibilité avant tout chargement. Le marketplace et le registre de publication ne font pas partie du P0, mais leurs futurs composants devront respecter ces contrats.

Les contrats OpenAPI des API distribuées doivent être présents ou générés de manière reproductible à partir des sources versionnées. Chaque version majeure publiée doit disposer de son contrat OpenAPI identifiable. Le build doit vérifier la cohérence entre les versions déclarées, les préfixes de routes, les schémas publics et les contrats générés, sans intégrer de secret ou de configuration de production.

Le build doit également traiter les contrats d'événements comme des artefacts versionnés séparés des contrats HTTP. Une représentation compatible avec AsyncAPI peut décrire les types, schémas, producteurs, consommateurs, canaux, garanties, ordre et replays sans imposer de broker. Le build doit vérifier la compatibilité des producteurs et consommateurs, l'enveloppe versionnée, l'absence de modèles privés ou de secrets et la cohérence des événements d'intégration exposés par les webhooks.

Les contributions frontend des composants doivent être déclarées dans les manifests ou sources contractuelles versionnées et résolues de manière reproductible. Le build frontend doit vérifier les identifiants, types, versions, dépendances, collisions de routes ou de slots, ressources de traduction, exigences de permissions d'affichage et compatibilité avec le shell. Une contribution non résolue, ambiguë ou incompatible doit bloquer le build ou l'activation selon le moment de détection.

Le build doit intégrer les sources ou artefacts frontend des modules dans une composition déterministe et produire les bundles ou chunks distribuables. Il ne doit pas dépendre d'un téléchargement de code ou d'une installation de paquet au runtime. Les artefacts Debian, Docker et développement doivent embarquer ou référencer une composition équivalente, avec les métadonnées nécessaires au diagnostic des composants frontend chargés. Une extension distante éventuelle doit être explicitement sélectionnée comme adapter et ne peut pas être introduite implicitement par le build.

Le build frontend doit vérifier que les extensions utilisent les clients et contrats API publics, que les clients générés correspondent aux versions OpenAPI publiées et qu'aucun accès direct à une base, un modèle privé ou une route non documentée n'est embarqué. Les tests doivent couvrir les clés de cache tenant-aware, l'invalidation après Command, les états provisoires et confirmés des mutations, ainsi que le comportement déclaré des capacités Electric.

Le build doit produire les SDK TypeScript et Python à partir des contrats OpenAPI, des contrats événementiels compatibles avec AsyncAPI et des JSON Schemas publics, avec une génération déterministe, des dépendances verrouillées et des métadonnées `sdk_version` et de compatibilité. Il doit vérifier que le code généré, les façades éventuelles, les types, les exemples et la documentation correspondent aux contrats publiés ; une divergence ou une génération non reproductible doit faire échouer le build.

Le Developer Kit et la CLI doivent être construits à partir des mêmes validateurs que le build de Pixs. Le build doit vérifier les commandes de scaffolding, de validation des manifests, de contrôle des imports publics, de génération, de compatibilité et de conformité, sans inclure de credential, token, donnée de production ou dépendance d'installation runtime.

Le build doit valider les déclarations d'entitlements et de quotas des composants : clés, versions, propriétaires, portées, dimensions, unités, limites, périodes, agrégations, dépendances, comportements de repli et exigences de conformité. Il ne doit embarquer ni entitlement actif, ni compteur, ni réservation, ni plan commercial ou donnée de consommation de production dans un paquet, une image, un bundle ou un exemple.

Le build doit valider les déclarations `OfflineSyncCapability` : ressources et projections éligibles, Commands différées, tenants et scopes autorisés, classifications de données, rétention locale, politique de chiffrement ou de stockage sécurisé, fraîcheur maximale, révocation, invalidation, stratégie de conflit, `local_schema_version` et `sync_protocol_version`. Une capacité offline-first non déclarée, ambiguë ou incompatible doit bloquer le composant concerné ; elle ne doit pas être activée par la seule présence d'Electric, d'un cache ou d'un service worker.

Les schémas de réplique locale et de file de Commands doivent être construits et migrés de manière déterministe. Le build doit vérifier la compatibilité entre versions de projection, protocoles, contrats API, événements, Commands, gouvernance, cycle de vie et releases `N`/`N+1`. Aucun état local de production, snapshot utilisateur, entitlement offline, réservation, credential, token ou preuve d'authentification ne doit figurer dans un artefact, une fixture ou un exemple.

Le build doit valider les politiques `TenantPlacementPolicy` et les contraintes de résidence déclarées : identifiants de régions logiques, région principale, régions de réplication, de traitement, de sauvegarde et de clés, classes de données, mode de bascule, epoch, transfert, rétention, suppression et révocation. Il doit vérifier la compatibilité entre ces politiques, le `DataGovernanceProfile`, les tenants, les scopes, les providers, les schémas, les migrations et les artefacts ; aucune région concrète ne doit être déduite de l'ordre des packages ou de la configuration accidentelle de la machine de build.

Les providers régionaux doivent déclarer leurs garanties de placement, réplication, chiffrement, gestion des clés, sauvegarde, restauration, suppression, révocation et transfert. Le build doit refuser un provider ou une topologie qui ne démontre pas la résidence demandée, la primaire unique, le fencing, la compatibilité inter-release ou la conservation des obligations sur les copies. Les configurations et fixtures ne doivent contenir ni donnée de production, ni secret, ni affectation régionale réelle non nécessaire au test.

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

Le build ne doit pas préinitialiser de tenant, d'appartenance, de rôle, d'ACL, de politique d'autorisation, d'identité, de session, de credential, de trust policy ou de donnée métier dans un artefact destiné à un environnement de production. Ces éléments relèvent du runtime, des migrations ou d'une opération d'administration explicitement définie.

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

La qualification d'une nouvelle release devra vérifier la dernière version
stable officielle supportée de Django selon
[TECHNICAL.md § 41.1](TECHNICAL.md#411-politique-de-version-django), actualiser son
relevé horodaté et fixer exactement la version qualifiée et les dépendances
résolues. Les dépendances Python devront employer leurs versions disponibles
les plus récentes compatibles avec Django et le graphe complet. Les versions
exactes ou plages imposées par Django auront priorité ; la version la plus
récente admissible dans une plage devra être retenue. Python, le code, les
migrations, les tests et l'ensemble des dépendances
devront être adaptés et validés avant de déclarer la release conforme. Une
migration restante devra être déclarée explicitement. Les artefacts historiques
conserveront leurs versions exactes pour leur reconstruction ; cette conservation
ne constitue pas une dérogation pour une nouvelle release. Aucun téléchargement
flottant ni mise à niveau silencieuse au runtime ne remplace la qualification.

Toute évolution de version de dépendance Python devra être supportée par le
Python actuel du projet déclaré dans `DEVOPS.md`. Avant installation, la
qualification devra vérifier `Requires-Python`, les wheels et les tests sur cet
interpréteur. Une incompatibilité avec ce Python devra suspendre l'évolution :
seul le développeur pourra la valider ou la refuser, ainsi que tout changement
de version de Python éventuellement nécessaire. Les agents ne devront ni
forcer l'installation ni changer la cible pour masquer le conflit. La solution
retenue devra être qualifiée avant installation, même après validation humaine.

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

Le build doit produire un même artefact fonctionnel pour les profils d'exécution `web`, `worker` et `scheduler`. Le rôle actif, ses capacités et ses limites sont fournis par la configuration runtime validée ; ils ne doivent pas générer de variante fonctionnelle cachée. Le build ne doit pas imposer de broker, d'orchestrateur ou de provider de coordination particulier, mais doit vérifier la présence d'un contrat persistant compatible lorsque la reprise ou la coordination est requise.

Le runtime doit pouvoir recevoir explicitement le `ScopeContext` nécessaire à l'exécution, comprenant le tenant racine et le scope enfant éventuel. Une configuration de déploiement ne doit pas désactiver silencieusement l'isolation tenant, changer de topologie sans conserver les garanties déclarées ou transformer un accès parent, descendant ou inter-tenant en accès implicite.

Le runtime doit également recevoir un `AuthenticationContext` vérifié avant toute autorisation. Il doit contrôler sa validité temporelle, sa révocation, sa fraîcheur, son provider de confiance, ses niveaux d'assurance et sa correspondance avec la `DigitalIdentity` et le `ScopeContext`. Une action sensible dont le niveau requis n'est pas satisfait doit être refusée ou soumise à un step-up explicite ; le build et le packaging ne doivent jamais préinitialiser une identité, une session, un credential ou une assurance de production.

Le runtime doit exécuter les transitions de cycle de vie uniquement via les Commands et Jobs autorisés du module propriétaire. Il doit vérifier la rétention, les legal holds, les références bloquantes, la version de concurrence et l'état des projections avant une purge ou une restauration. Les tombstones et journaux d'effacement doivent rester persistants et être pris en compte par les caches, index, synchronisations et restaurations ; un redémarrage ou une reprise ne doit pas réintroduire une ressource supprimée.

Le runtime doit appliquer le profil de gouvernance aux flux et dérivés concernés. Toute API, événement, webhook, recherche, projection, cache, fichier, sauvegarde ou export doit conserver la classification et les obligations de confidentialité applicables. Une demande relative aux données doit réévaluer l'autorisation, respecter les legal holds et la rétention, puis propager sa décision à la source de vérité et aux providers déclarés sans accès direct aux implémentations privées.

Le runtime doit charger les affectations de feature flags depuis une source persistante et versionnée. Les rôles `web`, `worker` et `scheduler` doivent converger vers une configuration cohérente ou signaler un état de version incompatible. Un cache local est autorisé pour les lectures, avec durée et invalidation contrôlées ; il ne doit pas maintenir une activation après expiration, révocation ou mise en pause déclarée. Les décisions de flag doivent rester secondaires aux permissions, au `ScopeContext`, aux contrats et aux garanties de données.

Le runtime doit exécuter les imports et exports au travers de `BulkOperation` et des providers de stockage objet déclarés. Un traitement dépassant le seuil synchrone doit utiliser des Jobs persistants ; les états, progrès, checkpoints, retries, annulation, expiration et résultats doivent survivre au redémarrage et rester corrélés à l'opération. Le staging, les rejets et les exports sont privés, ne dépendent pas du filesystem local et sont soumis aux quotas, au tenant, au scope, à la gouvernance et à la révocation.

Un import doit revalider le checksum, le mapping et le contexte d'autorisation avant les mutations, puis appeler les Commands du module propriétaire. Un export doit revalider les permissions, filtrer à la source, utiliser les projections et champs déclarés et produire un manifeste traçable. Une reprise ou un rejeu ne doit pas promettre `exactly-once` et doit appliquer la stratégie d'idempotence et de conflit déclarée.

La génération des SDK, du Developer Kit, de la CLI, des types et des exemples est une responsabilité du build. Le runtime utilise les packages produits et les contrats versionnés ; il ne télécharge ni ne génère de code pour découvrir ou activer un composant. Une application peut fournir ses propres credentials et sa configuration au runtime, mais ceux-ci ne doivent pas être incorporés dans les SDK, bundles, images ou paquets.

La configuration effective des entitlements, politiques de quota, compteurs et réservations est fournie au runtime. Le build ne choisit pas de plan commercial, n'active pas d'entitlement de production et ne préinitialise aucune consommation. Les rôles `web`, `worker` et `scheduler` doivent utiliser les mêmes contrats et la même source persistante ou des providers explicitement compatibles ; un provider indisponible ne peut pas produire une décision positive implicite pour une opération protégée.

La configuration effective offline-first est fournie au runtime et au client par une source validée. Le build ne précharge pas de réplique, de file de Commands, de bail d'accès offline ou de décision d'autorisation. La persistance locale du client peut survivre à un redémarrage lorsqu'elle est déclarée, mais elle reste distincte de la persistance autoritative de PostgreSQL ; aucun état nécessaire à l'autorité métier, à l'idempotence serveur ou à la reprise des Jobs ne doit dépendre du filesystem local d'un processus Pixs.

À la reconnexion, le runtime doit soumettre les Commands locales au backend et réévaluer l'identité, le `ScopeContext`, l'autorisation, l'entitlement, les quotas, la concurrence et la gouvernance. Le client peut signaler `OFFLINE` ou `STALE`, mais ne peut pas transformer une intention locale en succès métier. Les rôles `web`, `worker` et `scheduler` utilisent les mêmes contrats de synchronisation ; une perte de provider, une révocation ou un conflit doit produire un état contrôlé plutôt qu'une activation permissive.

Le runtime doit résoudre le placement après l'identité, le tenant et le scope, puis diriger les lectures et écritures selon le `ResidencyContext`. Un routage régional fourni par le client ne peut pas remplacer le contexte canonique. Les rôles `web`, `worker` et `scheduler`, les providers de stockage, les recherches, les caches, les événements, les sauvegardes et les copies offline doivent appliquer la même politique ; une région interdite ou indisponible ne doit pas être utilisée comme repli implicite.

Une bascule active-passive ne peut être activée qu'avec une région de secours autorisée, un epoch ou fencing persistant, un checkpoint vérifiable, une compatibilité de version et un audit. Le runtime doit empêcher l'ancien primaire d'écrire après la bascule et doit produire un état contrôlé en cas de split-brain, d'epoch divergent ou de transfert non autorisé. Une migration de tenant ou une restauration inter-région doit être exécutée par une opération d'exploitation explicite et reprendre les obligations de résidence, de rétention, de suppression et de gouvernance.

Le runtime doit configurer explicitement le PEP Django, le PDP de référence ou un adapter PDP compatible, la version ou l'epoch de politique et les règles de cache. Une indisponibilité du PDP ne doit pas produire d'autorisation positive pour une mutation, une action sensible ou une donnée protégée. Toute politique, relation de groupe, ACL, membership ou scope modifié doit invalider les décisions positives concernées.

Le runtime doit préserver les métadonnées de Command nécessaires à l'exécution et au diagnostic, notamment l'identité appelante, le `ScopeContext`, les identifiants de corrélation et de causalité. Une Command asynchrone doit pouvoir être suivie après redémarrage ou recréation du processus lorsque sa capacité le prévoit.

Les caches et projections utilisés par les Queries peuvent être reconstruits ou invalidés sans devenir la source de vérité applicative. Leur déploiement ne doit pas permettre de servir une donnée hors du `ScopeContext` ou des permissions applicables ; leurs clés et partitions doivent intégrer le scope lorsqu'il est applicable.

Lorsque l'outbox est activée, ses données persistantes doivent être stockées dans la source de vérité ou le provider explicitement prévu. Le build, l'installation et le redémarrage d'un service ne doivent pas supprimer les événements non publiés ni contourner leur relation transactionnelle avec la mutation métier.

Les mécanismes de supervision et de redémarrage doivent préserver la reprise des événements `PENDING`, `RETRYING` ou `FAILED` selon la politique de livraison. Un déploiement ne doit pas transformer une livraison `at-least-once` en suppression silencieuse des événements non publiés.

Les informations nécessaires à l'idempotence des Commands — clé, empreinte de payload, état et résultat lorsque nécessaire — doivent être persistantes et préservées lors des redémarrages, mises à niveau et recréations de conteneurs.

Les Jobs asynchrones et leurs états `PENDING`, `SCHEDULED`, `RUNNING`, `SUCCEEDED`, `RETRYING`, `FAILED`, `PAUSED`, `CANCELLED` ou `DEAD_LETTER` doivent être persistants lorsque leur reprise est nécessaire. Leur exécution ne doit pas dépendre uniquement de la durée de vie d'un processus ou d'un conteneur.

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

Le packaging et les migrations doivent préserver les champs communs déclarés par les modules, notamment les identifiants UUIDv7, les horodatages UTC, les versions de concurrence, les références tenant et les références de scope. Une mise à niveau ne doit pas réinitialiser ces valeurs, changer le propriétaire canonique ni convertir silencieusement une ressource tenant-scoped ou scope-scoped en ressource globale.

Les migrations et mises à niveau doivent également préserver les identités, mappings `(provider_id, issuer, subject)`, états de révocation, sessions et références de credentials selon les contrats applicables. Elles ne doivent jamais exporter, réinitialiser ou intégrer un token, un secret, une preuve d'authentification ou un niveau d'assurance de production.

Une suppression ou une mise à niveau du paquet ne doit pas entraîner implicitement la destruction des données applicatives.

Les migrations et mises à niveau doivent préserver les états métier et de persistance, les échéances de rétention, les legal holds, les tombstones, les journaux d'effacement, les historiques et les références `tenant_id`/`scope_id`. Les scripts de maintenance ne doivent pas purger automatiquement une donnée ni contourner la politique déclarée du module ; toute purge doit être une opération explicitement déclenchée et traçable.

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

Le packaging Debian doit pouvoir déclarer séparément les unités de service correspondant aux profils `web`, `worker` et `scheduler`, sans imposer leurs noms définitifs. Chaque unité doit utiliser le même contenu applicatif, recevoir une configuration de rôle explicite, propager les signaux et exposer des codes de sortie exploitables. Les workers et schedulers ne doivent pas être publiés comme services réseau publics par défaut.

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

L'entrypoint doit sélectionner un seul profil d'exécution explicitement configuré ou refuser une configuration ambiguë. Il ne doit pas lancer implicitement plusieurs rôles de production dans un même conteneur ni exécuter une migration destructive au démarrage. Un regroupement de rôles peut être utilisé par l'environnement de développement lorsqu'il est déclaré comme tel.

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

Le `ScopeContext`, le mode mono-tenant ou multi-tenant, la topologie de persistance et les accès d'administration plateforme doivent être fournis par une configuration runtime validée. L'image ne doit pas embarquer un tenant, un scope, une appartenance ou une autorisation inter-tenant implicite.

Les politiques de confiance des providers, les niveaux d'assurance requis, les paramètres de step-up, les sessions et les credentials doivent également rester configurables au runtime. L'image ne doit pas contenir d'issuer de production approuvé par défaut, de clé privée, de token, de session ou de credential.

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

Les données tenant-scoped, les scopes, memberships, rôles, ACL et journaux d'accès doivent également rester dans les mécanismes persistants prévus par Pixs. La recréation d'un conteneur ne doit pas modifier la hiérarchie, la frontière d'isolation ou le propriétaire canonique, ni accorder un accès supplémentaire.

Les politiques d'autorisation, leurs versions ou epochs, les relations de groupes et les états nécessaires à la révocation doivent bénéficier des mêmes garanties de persistance. Une recréation ou une mise à niveau de conteneur ne doit pas restaurer une ancienne décision positive ni perdre une révocation.

Les états de cycle de vie des ressources, les tombstones, les journaux d'effacement, les échéances de rétention, les legal holds et les résultats de Jobs de purge doivent bénéficier des mêmes garanties de persistance. Une recréation, une mise à niveau ou une restauration de conteneur ne doit pas rendre visible une ressource `SOFT_DELETED` ou `PURGE_PENDING`, ni effacer la preuve nécessaire à l'empêchement d'une résurrection.

Les états et résultats persistants nécessaires au suivi des Commands asynchrones ne doivent pas dépendre uniquement du système de fichiers éphémère du conteneur.

Les entrées d'outbox et leur état de publication ne doivent pas dépendre uniquement du système de fichiers éphémère du conteneur. Une recréation du conteneur doit permettre leur reprise selon les garanties du provider.

Les états d'inbox et de déduplication des consommateurs doivent bénéficier des mêmes garanties de persistance. Une recréation ou une mise à niveau ne doit pas faire perdre la preuve qu'un `event_id` a déjà été consommé ni provoquer un nouvel effet secondaire confirmé.

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

Les tests de packaging doivent confirmer que seul le profil `web` est exposable publiquement par défaut, que les ports ou endpoints des workers, schedulers et stores de coordination restent privés et que l'interface de management dispose d'une frontière d'accès distincte. Une modification de l'exposition réseau ne doit pas accorder de permission métier ni contourner l'authentification ou l'autorisation.

---

## 24. Health checks

L'image Docker doit permettre de déterminer si Pixs est opérationnel.

Le health check ne doit pas se limiter à tester arbitrairement l'existence d'un processus lorsque l'état applicatif peut être vérifié plus précisément.

Le packaging et les tests runtime doivent distinguer les probes `liveness`, `startup`, `readiness` et le diagnostic détaillé. Ils doivent vérifier les délais, codes et états `HEALTHY`, `DEGRADED`, `FAILED` et `DISABLED`, l'évaluation des dépendances obligatoires et optionnelles, l'absence de mutation ou de secret dans les probes et la protection des détails opérateur. Une dépendance optionnelle indisponible ne doit pas rendre automatiquement l'artefact `unhealthy` si le mode dégradé est déclaré et cohérent.

Les niveaux exacts de santé seront coordonnés avec les capacités `runtime`, `observability` et `resilience`.

Le mécanisme devra éviter qu'une dépendance optionnelle indisponible rende automatiquement Pixs `unhealthy` lorsqu'un fonctionnement dégradé conforme est explicitement supporté.

Les probes doivent être vérifiées pour chaque profil : `web` doit indiquer sa capacité à recevoir du trafic, `worker` sa capacité à consommer ou reprendre les unités persistantes et `scheduler` sa capacité à acquérir ou renouveler son lease. Une perte de lease ne doit pas être masquée par un état de santé positif du scheduler, et un détenteur périmé doit être empêché de déclencher un traitement autoritatif.

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

La release doit également référencer les versions de composants, contrats, capacités, manifest, schéma, migrations, événements, APIs, configuration, gouvernance des données, feature flags, opérations de masse, SDK, entitlements, politiques de quota, capacités offline-first et politiques régionales qui composent l'artefact. Ces dimensions restent distinctes, notamment `feature_flag_version`, `bulk_operation_version`, `sdk_version`, `entitlement_version`, `quota_policy_version`, `offline_capability_version`, `local_schema_version`, `sync_protocol_version`, `residency_policy_version`, `placement_policy_version` et `region_topology_version`, et doivent être vérifiables dans les métadonnées sans embarquer de secret. Les affectations runtime des flags et entitlements, les compteurs et réservations, les répliques et Commands locales, les placements et régions effectifs, les opérations de masse en cours et les credentials des SDK restent hors de l'artefact.

Le build doit produire ou vérifier une matrice de compatibilité entre l'artefact, les composants, les providers, les contrats, les schémas, les migrations et les clients déclarés. Chaque relation est marquée `COMPATIBLE`, `REQUIRES_MIGRATION`, `DEPRECATED` ou `BLOCKED`. Une version plus récente, un tag mutable ou la simple présence d'un paquet ne constituent pas une preuve de compatibilité.

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

Pour le modèle `Component` et les extensions, elle doit en outre vérifier la séparation des états `DISCOVERED`, `VALIDATED`, `RESOLVED`, `LOADED` et `ACTIVE`, l'indépendance des états `INSTALLED`, `ENABLED`, `CONFIGURED`, `READY` et des états de santé `HEALTHY`, `DEGRADED`, `FAILED`, `DISABLED`. Elle doit confirmer qu'une extension obligatoire non résolue bloque l'activation, qu'une extension optionnelle défaillante reste isolée et que les transitions, raisons, versions et corrélations sont diagnostiquables sans exposer de secret.

Les tests doivent démontrer qu'un composant consommateur utilise les contrats et façades publiques sans importer l'implémentation privée d'un autre composant, qu'une contribution ne peut pas contourner le backend ou les permissions, et que deux compositions identiques produisent le même graphe et le même ordre de chargement. Les artefacts Debian, Docker et développement doivent conserver cette composition et ces métadonnées de manière équivalente.

Pour la gestion des capacités et des feature flags, les tests doivent vérifier la résolution déterministe des capacités obligatoires et optionnelles, la cohérence des providers, les états `AVAILABLE`, `DEGRADED`, `DISABLED` et `BLOCKED`, ainsi que l'isolement d'une capacité optionnelle indisponible. Ils doivent vérifier les définitions, versions, propriétaires, valeurs par défaut, prérequis, expirations et affectations de flags, la priorité entre installation, environnement, tenant et scope, la cohorte stable, l'absence d'expressions exécutables et le refus d'une configuration ambiguë.

Ils doivent également confirmer qu'un flag ne contourne ni permissions, ni scopes, ni gouvernance des données, ni migrations, ni contrats, qu'un frontend ne peut pas autoriser une action en modifiant son affichage, et qu'une valeur absente, invalide, périmée ou une source indisponible applique le repli déclaré. Les tests doivent couvrir la persistance, l'audit, l'invalidation et l'expiration, la convergence des rôles `web`, `worker` et `scheduler`, la promotion du même artefact entre environnements et la réévaluation des Commands, Events et Jobs selon leur contrat.

Pour les opérations en masse, les tests doivent vérifier le contrat `BulkOperation`, les états persistants, la distinction entre `operation_id` et `job_id`, les seuils de bascule asynchrone, les quotas, les limites de taille, de lignes et de concurrence et les formats `CSV`/`NDJSON`. Ils doivent couvrir le staging privé, le checksum, les mappings versionnés, les champs autorisés, `VALIDATE_ONLY`, les modes `ATOMIC`, `ATOMIC_PER_CHUNK` et `BEST_EFFORT`, les conflits, l'idempotence, les checkpoints, les retries, l'annulation, l'expiration et la dead-letter.

Ils doivent aussi démontrer qu'un import passe par les Commands du module propriétaire, qu'un export applique `filter_authorized` à la source et utilise une projection déclarée, qu'un snapshot ou watermark est traçable, que les manifestes et fichiers restent privés et temporaires et que la classification, le tenant, le scope, la rétention, la révocation et les obligations de gouvernance sont conservés. Aucun secret, fichier de production ou payload personnel réel ne doit être utilisé par les fixtures ou les artefacts de build.

Pour les SDK et l'écosystème développeur, les tests doivent vérifier la reproductibilité de la génération TypeScript et Python, la correspondance avec les contrats OpenAPI/AsyncAPI/JSON Schema, les versions `sdk_version`, les contraintes de compatibilité, les dépendances verrouillées, la compilation des exemples et les façades au-dessus du code généré. Ils doivent couvrir les clients d'authentification injectable, la propagation du tenant et du scope, les erreurs typées, la pagination, l'idempotence, les retries bornés, le suivi asynchrone, les opérations bulk et la vérification des webhooks.

Ils doivent également vérifier le Developer Kit et la CLI : scaffolding déterministe, validation du manifest, contrôle des imports publics, génération, diagnostic, codes de sortie et tests de conformité. Le build doit échouer en cas de divergence contractuelle, de code distant implicite ou de secret dans les packages, exemples, fixtures, bundles, logs ou rapports. Les artefacts Debian, Docker et de développement doivent conserver les mêmes contrats et versions de SDK.

Pour les quotas et entitlements, les tests doivent distinguer une capacité indisponible, un entitlement absent, expiré ou révoqué, une permission refusée et un quota dépassé. Ils doivent vérifier les portées installation, plateforme, tenant et scope, l'absence d'entitlement utilisateur implicite, la résolution cumulative des limites et l'absence d'élargissement par un scope enfant.

Ils doivent couvrir les dimensions de débit, concurrence, requêtes, octets, objets, lignes, Jobs et coût d'opération, les unités et périodes déclarées, les réponses d'erreur stables, `429` et `Retry-After` lorsque possible, ainsi que les états de provider `DEGRADED`, `FAILED` et `REVOKED`. Ils doivent démontrer l'atomicité et l'idempotence de `check`, `reserve`, `commit` et `release`, l'absence de double consommation après retry ou reprise, la réconciliation de la consommation réelle et la libération après annulation.

Les tests doivent vérifier que les API, SDK, Commands asynchrones, Jobs et opérations bulk réévaluent les entitlements et quotas au moment approprié, que les compteurs et décisions survivent aux redémarrages et que les rôles `web`, `worker` et `scheduler` convergent. Aucun entitlement, compteur, réservation, plan commercial, secret ou donnée de consommation de production ne doit apparaître dans les fixtures, bundles, images, paquets, logs ou rapports.

Pour l'offline-first conditionnel, les tests doivent vérifier que l'activation est opt-in par composant et par ressource, que l'absence d'Electric, de service worker ou de provider local ne produit aucune activation implicite et que les versions `offline_capability_version`, `local_schema_version` et `sync_protocol_version` sont compatibles avec la release et les contrats publics.

Ils doivent simuler les pertes de connexion, la reconnexion, les redémarrages du client, les projections `STALE`, les checkpoints, les messages dupliqués ou désordonnés, les migrations de schéma local et la reconstruction complète d'une réplique. Ils doivent confirmer qu'une projection locale ne devient jamais une source de vérité et qu'une Command locale reste provisoire jusqu'à sa validation serveur.

Les scénarios de reconnexion doivent démontrer la réévaluation de l'identité, du `ScopeContext`, de l'autorisation, de l'entitlement, du quota, de la concurrence et de la gouvernance. Ils doivent couvrir l'idempotence, les retries, les expirations, les révocations, les changements de tenant ou de scope, les tombstones, les suppressions et les conflits `REJECT`, `MANUAL_REVIEW`, `DOMAIN_MERGE` et `LAST_WRITE_WINS` lorsqu'il est déclaré. Aucun Event de domaine ne doit être publié localement avant confirmation serveur.

La conformité doit vérifier l'isolation des répliques et files entre utilisateurs, appareils, tenants et scopes, la rétention, l'effacement, le chiffrement ou stockage sécurisé déclaré et l'absence de secrets, tokens, credentials ou preuves d'authentification brutes. `RESTRICTED` et `SENSITIVE_PERSONAL` doivent être refusés par défaut, `CONFIDENTIAL` doit exiger une politique explicite, et les imports, exports, opérations bulk, purges et actions sensibles doivent être refusés hors ligne par défaut.

Pour la multi-région et la résidence par tenant, les tests doivent vérifier le mode par défaut mono-région, la résolution d'une `TenantPlacementPolicy`, la version du placement, l'epoch régional et l'absence de réplication, transfert, sauvegarde ou bascule inter-région implicite. Ils doivent couvrir la région principale, les régions de traitement, de réplication, de sauvegarde et de clés, ainsi que l'héritage vers les scopes enfants et la possibilité de renforcer une contrainte sans l'élargir.

Les tests doivent valider les régions logiques indépendamment des providers et vérifier la conformité de PostgreSQL, des objets, réplicas, index, caches, fichiers temporaires, sauvegardes, logs, traces, audits, événements, webhooks et copies offline. Aucun dérivé ne doit sortir du périmètre autorisé ; une politique absente, ambiguë ou impossible à satisfaire doit produire un blocage ou un état contrôlé.

Les scénarios de routage doivent démontrer que l'identité, le tenant et le scope sont résolus avant le `ResidencyContext`, qu'une région fournie par le client ne peut pas modifier le placement canonique et qu'un cache, index ou provider ne peut pas contourner la résidence. Les tests doivent aussi confirmer que les quotas, entitlements, idempotences, événements et audits conservent leur portée lors d'un changement de région.

Les scénarios active-passive doivent couvrir la compatibilité de schéma et de contrat, les checkpoints, les tombstones, les rétentions, les clés, le fencing ou epoch persistant, l'arrêt d'écriture de l'ancien primaire, la détection du split-brain et l'audit de la bascule. Une région de secours non autorisée, un transfert sans garanties ou une restauration hors périmètre doit bloquer l'opération. L'actif-actif et le multi-primary restent hors de la suite de conformité de base.

Pour les scopes, la validation des artefacts doit vérifier la résolution explicite du `ScopeContext`, la cohérence de la hiérarchie, l'unicité du propriétaire canonique, le refus des références croisées entre tenants, l'absence de fuite dans les caches et projections et l'équivalence des garanties entre la topologie PostgreSQL partagée de référence et toute topologie isolée déclarée compatible. Le build ne doit pas choisir implicitement une topologie ni créer de tenant, scope, appartenance ou permission de production.

Pour l'identité et l'assurance d'authentification, les tests doivent vérifier la résolution vers une `DigitalIdentity`, la confiance explicite du provider, la validation de l'issuer et de l'audience, les mappings d'assurance, l'expiration, la fraîcheur, la rotation, la révocation, la détection du rejeu et le refus d'une action lorsque l'assurance est insuffisante. Ils doivent couvrir le step-up, l'invalidation des sessions après récupération, la liaison explicite sans rapprochement automatique par e-mail et l'absence de tokens, credentials ou preuves brutes dans les artefacts, journaux et diagnostics.

Pour le moteur d'autorisation, les tests doivent vérifier la priorité des `DENY`, le `deny by default`, l'absence de permission implicite par propriété, rôle administrateur ou scope parent, la résolution bornée des groupes imbriqués, le filtrage à la source des collections, les décisions groupées, l'invalidation après modification de politique et le refus fermé lorsque le PDP est indisponible. Ils doivent confirmer que les obligations de step-up, d'audit ou de confirmation non satisfaites empêchent l'autorisation.

Pour le cycle de vie des données, les tests doivent vérifier la séparation des états métier, de persistance, de rétention et de projection, la stratégie `SOFT_DELETE` par défaut, les transitions autorisées, la restauration contrôlée, l'idempotence et l'autorisation des Jobs de purge, les legal holds, les références bloquantes et la règle `RESTRICT` inter-modules. Ils doivent vérifier la création et la propagation des tombstones vers les caches, index, projections et synchronisations, l'absence de résurrection après reprise ou reconstruction, la conservation de `tenant_id`/`scope_id` et la réapplication des effacements lors d'une restauration de sauvegarde.

Pour la gouvernance des données et la confidentialité, les tests doivent vérifier la validation du `DataGovernanceProfile`, l'unicité du propriétaire et de la source de vérité, les classifications `PUBLIC`, `INTERNAL`, `CONFIDENTIAL` et `RESTRICTED`, les niveaux `NONE`, `PERSONAL` et `SENSITIVE_PERSONAL`, ainsi que la séparation stricte des secrets. Ils doivent confirmer que les données non classifiées sont traitées restrictivement et ne peuvent pas sortir par une API, un événement, un webhook, un export ou un provider avant déclaration.

Ils doivent également couvrir la propagation de la classification et des obligations vers les recherches, projections, caches, fichiers, sauvegardes et synchronisations, la lignée des données, les consommateurs et processeurs autorisés, les contraintes de résidence ou de transfert, le chiffrement déclaré, la suppression et la révocation côté provider. Les scénarios de `DataSubjectRequest` doivent couvrir l'accès, l'export, la rectification, l'effacement et la restriction, avec autorisation, idempotence, traitement asynchrone, audit, respect des legal holds et absence de fuite de payload sensible.

Pour les API, la validation doit également couvrir la présence ou la génération du contrat OpenAPI, les tests de contrat, les exemples versionnés, le contrôle automatique de compatibilité et l'échec du build en cas de rupture non déclarée, la cohérence des schémas et des préfixes `/api/vN`, l'absence de rupture non déclarée dans une version majeure, les versions publiées, la déclaration des exigences d'authentification et des routes publiques, la résolution vers une `DigitalIdentity`, la déclaration des routes tenant-scoped et platform-scoped, la vérification du contexte tenant, l'enveloppe de succès (`data`, `meta`, `links`), la pagination par curseur, les filtres et tris autorisés, les plafonds de taille de page, les règles `ETag`, `If-None-Match`, `If-Match` et `Cache-Control`, la déclaration et la persistance des `Idempotency-Key`, la déclaration des limites de débit et de leurs dimensions, la représentation correcte des réponses `429`, des Commands asynchrones en `202`, les enveloppes et signatures des webhooks sortants et entrants, les mécanismes de protection contre le rejeu, les règles CORS et CSRF par environnement, les limites de taille JSON/multipart/upload, les budgets de durée et les réponses `413`, `408` et `504`, les formats `Content-Type`/`Accept`, les erreurs `415` et `406`, la sérialisation RFC 3339 UTC et la stabilité des codes et structures non localisés, les références de secrets, les politiques de retries et de dead-letter, l'enveloppe d'erreur standard (`error_code`, `message`, `details`, `field_errors` optionnel et `correlation_id`) et l'absence d'exposition involontaire de détails privés, de secrets ou de traces d'exécution.

Les tests frontend doivent également vérifier la résolution déterministe des contributions, le chargement des extensions, les collisions, les contrats de routes et de slots, les traductions, les permissions d'affichage et le respect des APIs publiques du shell. Ils doivent confirmer qu'une extension frontend ne peut pas remplacer une décision d'autorisation backend, qu'elle reçoit le `ScopeContext` en lecture seule et que les changements de tenant ou de scope invalident les états et caches associés.

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

Ces scénarios doivent également couvrir un `AuthenticationContext` absent, expiré, révoqué, non mappé ou d'un niveau inférieur à l'exigence de l'action. Le build doit confirmer qu'un échec de step-up ou de récupération ne provoque aucune élévation implicite et que les sessions et credentials invalidés ne sont plus acceptés.

Ils doivent aussi couvrir une politique d'autorisation absente, ambiguë, périmée ou non compatible, un conflit `DENY`/`ALLOW`, un cache positif obsolète, une relation de groupe cyclique ou hors limite et une indisponibilité du PDP. Aucun de ces cas ne doit accorder un accès, exposer une collection ou déclencher une mutation.

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

Le build doit refuser un saut de version non déclaré et signaler les migrations intermédiaires nécessaires. Il doit valider la coexistence de la release courante et de la release immédiatement précédente pendant la fenêtre supportée, ainsi que la compatibilité transitoire des APIs, événements, schémas, configurations, providers et clients. Une migration destructive doit être séparée du chemin d'activation initial et bloquée tant qu'un consommateur compatible peut encore utiliser la structure concernée.

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
* les unités de service et la stratégie d'exécution définitives des profils `web`, `worker` et `scheduler` ;
* le contrat concret des files, de la coordination persistante et des leases ;
* les nombres minimaux et maximaux d'instances par rôle ;
* la frontière réseau et les règles d'exposition de l'interface de management ;
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

Les spécifications OpenSpec actives couvrent les garanties normatives associées aux domaines suivants. Les précisions ci-dessous restent à choisir au moment de l'implémentation ; toute décision qui modifie ces garanties nécessite une évolution OpenSpec approuvée :

* le schéma concret du `DataGovernanceProfile`, sa version et son rattachement aux manifests ;
* la taxonomie définitive de confidentialité et de données personnelles, ainsi que les contrôles sur les données non classifiées ;
* le contrat des demandes génériques relatives aux données et les validations d'accès, d'export, de rectification, d'effacement et de restriction ;
* les contrôles concrets de lignée, de résidence, de transfert, de suppression, de révocation et de conformité des providers.
* le contrat du registre de capacités et les règles de disponibilité des capacités obligatoires ou optionnelles ;
* le schéma des feature flags, des affectations runtime, des priorités de ciblage et des cohortes déterministes ;
* les politiques de repli, d'échec fermé, d'expiration, d'invalidation et de convergence entre les profils d'exécution ;
* les contrôles de compatibilité des flags avec les permissions, scopes, données, migrations, API, événements et Jobs.
* le contrat `BulkOperation`, ses versions, états, variantes, limites et son rattachement aux Jobs persistants ;
* les formats, mappings, staging, contrôles d'import, modes de commit, stratégies de conflit et rapports de rejets ;
* les projections d'export, le filtrage à la source, les snapshots ou watermarks, les manifestes, la rétention, la révocation et la purge ;
* les quotas, seuils d'asynchronisme, checkpoints, annulation, retries, dead-letter et tests de conformité des adapters de stockage ;
* le périmètre exact des SDK TypeScript et Python, le client bas niveau, les façades éventuelles, l'authentification injectable et la propagation du tenant et du scope ;
* la stratégie de génération depuis OpenAPI, les contrats événementiels compatibles avec AsyncAPI et JSON Schema, la reproductibilité, les dépendances verrouillées et la séparation entre code généré et code maintenu ;
* les commandes de la CLI, le scaffolding du Developer Kit, les validateurs partagés, les exemples et les suites de conformité ;
* le versionnement `sdk_version`, la matrice de compatibilité avec les APIs, contrats, composants et schémas, ainsi que les packages et canaux de distribution ;
* les politiques de credentials, de stockage navigateur, de retries, d'idempotence, d'erreurs, de suivi asynchrone et de vérification des webhooks dans les SDK ;
* le modèle des entitlements, de leurs portées, priorités, héritages, états, expirations, révocations et sources ;
* le modèle des politiques de quota, dimensions, unités, périodes, agrégations, compteurs, consommations et réservations ;
* les contrats `EntitlementProvider` et `QuotaProvider`, la référence PostgreSQL, les providers spécialisés, les caches et le comportement en indisponibilité ;
* l'ordre de décision entre capacité, entitlement, autorisation, feature flag et quota, ainsi que les codes d'erreur, réponses `429`, `Retry-After` et diagnostics ;
* les règles de réservation, réconciliation et libération pour les API, Jobs, Commands asynchrones, imports, exports et opérations bulk, sans facturation dans le Kernel ;
* le contrat `OfflineSyncCapability`, les ressources, projections et Commands éligibles, les états locaux et la politique de fraîcheur ;
* les modèles `LocalReplica`, `OfflineCommand` et `OfflineAccessLease` éventuel, leur stockage, isolation, chiffrement, rétention et effacement ;
* le protocole de reconnexion, de réévaluation serveur, de soumission idempotente, de checkpoint et de réconciliation avec PostgreSQL, l'outbox et les Jobs ;
* les stratégies de conflit, de révocation, de tombstone et de purge, ainsi que la compatibilité des schémas locaux et protocoles entre releases ;
* le contrat `TenantPlacementPolicy`, le `ResidencyContext`, les régions logiques, les versions, les epochs et les états de placement ;
* les règles d'héritage de résidence du tenant vers les scopes enfants, les ressources platform-scoped et les classes de données ;
* les capacités des providers régionaux pour le placement, la réplication, le chiffrement, les clés, les sauvegardes, la suppression, la restauration et la révocation ;
* le routage régional après résolution de l'identité, du tenant et du scope, ainsi que les refus de transfert ou de région non autorisée ;
* les garanties de primaire unique, de fencing, de bascule active-passive, de split-brain, de quotas, d'idempotence et d'agrégation inter-régions ;
* les migrations de tenant, restaurations inter-régions, changements de politique et le périmètre des copies offline, logs, traces, caches, index, événements et webhooks ;
* les conditions exactes d'une éventuelle topologie active-active ou multi-primary, qui restent hors du socle de référence ;

Ces choix ne complètent une spécification que lorsqu'ils introduisent ou modifient un comportement normatif.

---

## 37. Capacités OpenSpec applicables

La construction, le packaging et la publication s'appuient notamment sur les capacités actives `runtime`, `installation-provisioning`, `deb-package`, `docker-image`, `artifact-publication`, `release-management`, `component-registry` et `progressive-deployment`. Les capacités transverses `configuration`, `secrets-providers`, `security`, `compatibility`, `testing`, `observability`, `operations`, `backup-disaster-recovery`, `data-governance`, `regional-residency`, `offline-first` et `sdk-ecosystem` apportent les garanties complémentaires.

Toute capacité supplémentaire reste soumise à un changement OpenSpec approuvé ; elle ne doit pas être déduite d'un mécanisme de packaging existant.

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

Les tests de conformité des providers doivent également vérifier la propagation du `ScopeContext`, la propriété canonique des ressources, la cohérence entre tenant et scope enfant, l'absence de fuite entre scopes ou tenants et l'équivalence des garanties dans les topologies partagée et isolée déclarées compatibles.

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

Pour une projection LDAP optionnelle des identités numériques, groupes et
appartenances de `pixs.core`, le build et les suites de conformité doivent
vérifier le mapping versionné, l'allowlist des attributs, les tenants et scopes
admissibles, la projection sortante sous autorité `PIXS`, les checkpoints, les
retries, l'idempotence, les suppressions et tombstones. Ils doivent confirmer
qu'une indisponibilité LDAP active le repli PostgreSQL et l'état `DEGRADED`,
qu'une projection insuffisamment fraîche n'est pas lue après une mutation, et
que LDAP ne peut ni importer une écriture Core, ni fournir une ACL, une
décision d'autorisation, une révocation ou une authentification. Les fixtures,
rapports et artefacts ne doivent contenir ni credential LDAP, ni DN de
production, ni donnée personnelle réelle.

Les tests du `RegionalPlacementProvider` doivent couvrir la résolution des régions logiques, le placement primaire, les réplicas, les régions de traitement, les sauvegardes, les clés, les transferts, les tombstones, la suppression, la restauration, la révocation et les limites de provider. Ils doivent vérifier la compatibilité de la `TenantPlacementPolicy`, l'absence de fuite entre tenants ou régions, la primaire unique, le fencing, l'epoch régional, la détection du split-brain et le refus d'une région non autorisée.

Les tests de Commands, Events et Jobs doivent vérifier la validation avant mutation, l'autorisation et la transaction Django, la création atomique d'une outbox, la séparation entre `operation_id`, `command_id`, `event_id` et `job_id`, la déduplication Inbox, les replays, l'ordre par agrégat ou partition, les retries bornés, les erreurs non rejouables, les leases, la reprise après perte d'un worker ou du scheduler et l'absence de promesse `exactly-once`. Ils doivent également confirmer la propagation du `ScopeContext`, la réévaluation de l'autorisation à l'exécution, la conservation de l'acteur initial et l'absence de secrets ou de payloads privés dans les événements et diagnostics.

Les tests de contrats API doivent vérifier les artefacts OpenAPI, les évolutions additives, le refus des ruptures dans une version majeure, les erreurs et réponses asynchrones, les exigences d'authentification, de tenant, de scope et d'idempotence. Les tests de contrats événementiels doivent vérifier les versions, l'enveloppe (`event_id`, type, version, producteur, sujet, contexte, corrélation, causalité et payload), la compatibilité des consommateurs, la distinction entre domaine et intégration, les replays et la transformation contrôlée des webhooks entrants et sortants.

Ils doivent également vérifier la sélection déterministe du provider, les états `PENDING`, `RUNNING`, `PAUSED`, `DEGRADED`, `FAILED`, `CONVERGED` et `QUARANTINED`, la suspension et la reprise autorisées, la réinitialisation contrôlée des checkpoints, la validation des signatures et fenêtres de rejeu, la rotation des secrets, les scopes minimaux, la propagation des corrélations et l'absence de secret ou de payload sensible dans les diagnostics. Les tests de rejeu et de reprise doivent confirmer l'idempotence et l'absence de suppression ou duplication non déclarée.

Les environnements Debian, Docker et développement doivent exposer la même configuration conceptuelle de ces providers. Une dépendance optionnelle indisponible peut produire un état `DEGRADED` lorsqu'un fonctionnement cohérent est déclaré ; elle ne doit pas provoquer une sélection implicite d'un provider différent ni une perte silencieuse de données.

Les validations doivent confirmer le caractère stateless du runtime : aucune donnée métier, session durable, clé d'idempotence, file, lease, checkpoint ou état de synchronisation ne doit dépendre du filesystem local ou de la mémoire d'un processus. Les tests doivent couvrir une installation mono-instance puis plusieurs instances web, workers et schedulers partageant les mêmes services persistants.

Les artefacts et images doivent pouvoir démarrer les rôles `web`, `worker` et `scheduler` à partir du même contenu, avec une configuration de rôle externe et validée. Les tests de développement peuvent couvrir un mode regroupé ; les tests de production doivent vérifier la séparation explicite des rôles, le lease persistant du scheduler, son expiration, la reprise après perte de lease et la montée en charge de plusieurs workers.

Les scénarios de redémarrage, recréation de conteneur, remplacement de paquet et montée en charge doivent vérifier la reprise des Jobs, de l'outbox, des synchronisations et des workflows sans perte ni double traitement non déclaré. Les verrous et leases locaux ne peuvent être acceptés que s'ils sont explicitement non autoritatifs. Les adapters systemd, runtime conteneur et orchestrateur doivent conserver les mêmes comportements applicatifs.

Les validations d'exploitation doivent vérifier la stratégie de sauvegarde et de restauration déclarée par déploiement : objectifs `RPO` et `RTO`, sauvegarde PostgreSQL, conservation ou versionnement des objets, protection de la configuration et des secrets, contrôle d'accès, rétention, résidence et journaux d'opération. Les tests de restauration doivent utiliser un environnement isolé et confirmer la cohérence des modèles, migrations, outbox, Jobs, idempotences, workflows, audits, fichiers, checksums, mappings, checkpoints, identités, tenants, ACL et politiques de placement.

Une restauration doit également vérifier le démarrage contrôlé, les health checks, la reprise idempotente, la détection des versions incompatibles, le traitement des événements non publiés, l'état des synchronisations externes et la région cible autorisée. Le build ou le runtime ne doit jamais lancer automatiquement une purge, un downgrade de schéma, une réinitialisation des identités, un transfert inter-région ou une suppression de fichiers pour masquer un écart de restauration.

Les validations doivent couvrir un déploiement avec interruption courte ainsi que, lorsque les adapters correspondants existent, les stratégies rolling, blue/green et canary. Les scénarios progressifs doivent vérifier la coexistence temporaire des versions `N` et `N+1`, la compatibilité des API, événements, schémas et données partagés, l'arrêt du trafic vers une instance non prête et le retrait de l'ancienne version seulement après validation de la nouvelle.

Les migrations destructives doivent être testées comme une étape séparée et bloquées tant qu'une ancienne version ou un consommateur compatible peut encore utiliser la structure concernée. Le build doit vérifier la séquence expansion, compatibilité, migration des usages, retrait puis contraction, ainsi que la possibilité de revenir à une version compatible sans downgrade automatique de la base.

Les migrations doivent former une chaîne versionnée et déterministe par module. Le build doit vérifier les identifiants, versions source et cible, dépendances, préconditions, postconditions, idempotence, mode d'exécution et stratégie de compensation. Les backfills doivent être testés comme des opérations reprenables, bornées et observables ; un saut de version ou une dépendance circulaire non déclaré doit bloquer la release.

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

Le build doit vérifier que toute migration dispose d'un plan inspectable avec ses versions source et cible, dépendances, préconditions, postconditions, mode `ONLINE`, `MAINTENANCE` ou `OFFLINE`, caractère destructif, stratégie de reprise et résultats attendus. Le démarrage ne doit effectuer qu'un contrôle préalable ; une migration en attente doit être exécutée par une commande d'exploitation autorisée avant que l'instance puisse devenir `ready`.

La validation de la topologie doit vérifier qu'un même artefact peut démarrer en mono-instance puis en plusieurs instances `web` et `worker`, que le scheduler est limité par un lease persistant et que les traitements reprennent après redémarrage, recréation ou perte de lease. Elle doit confirmer qu'aucun état d'autorité ne dépend du filesystem local, de la mémoire d'un processus ou d'un conteneur particulier.

Le paquet Debian doit être testé avec son adapter systemd ou équivalent de service ; l'image OCI/Docker doit être testée avec un runtime de conteneurs. Les deux chemins doivent vérifier les mêmes migrations, configurations, secrets externes, health checks, signaux d'arrêt, préservation des données et diagnostics. Les tests Kubernetes, Nomad ou autres orchestrateurs sont optionnels et ne doivent pas être requis pour valider le Kernel ou la release de base.

Les tests doivent couvrir le drainage et l'arrêt contrôlé des trois profils, le refus de trafic public vers les workers et schedulers, le redémarrage d'un worker sans perte ni double effet non déclaré, l'expiration et le renouvellement du lease du scheduler, le refus d'action d'un détenteur de lease périmé, ainsi que la conservation des Jobs, outbox, inbox, files, checkpoints, sessions et idempotences. Ils doivent également vérifier qu'un orchestrateur externe ne devient pas une source d'autorité métier et que la haute disponibilité des dépendances persistantes reste déclarée par le déploiement.

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

RegionalPlacementProvider
    placement / réplication / transfert / bascule / restauration
```

Pour chaque entrée, le build doit distinguer les tests de contrat, d'intégration, de sécurité, de reprise et de packaging. Les tests utilisent des données synthétiques, des fixtures et des instances dédiées. Ils ne doivent pas exiger de secret de production, intégrer de credential dans un artefact ou accéder au volume interne de Nextcloud.

Une incompatibilité obligatoire, une violation d'isolation tenant, un contournement d'autorisation, une perte d'idempotence, une sélection ambiguë ou une exposition de secret bloque la validation. Une capacité optionnelle peut être marquée `DEGRADED` ou `DISABLED` uniquement si son absence est déclarée, diagnostiquée et sans perte silencieuse de données.
## 42. Providers concrets et modules métier

Le build doit traiter séparément les niveaux de confiance `PLATFORM`,
`TRUSTED`, `SANDBOXED` et `DEVELOPMENT`. Il doit vérifier leurs manifests,
versions, capacités, dépendances, contrats, configuration, provenance,
signatures et tests de conformité. Un composant `DEVELOPMENT` ne peut pas être
embarqué dans un artefact de production ; un composant `SANDBOXED` ne reçoit que
les permissions et interfaces explicitement accordées.

Les providers officiels doivent être testés comme des implémentations de référence sans devenir des dépendances implicites du Kernel. Les providers externes et privés doivent être vérifiés par les mêmes suites de contrat lorsqu'ils déclarent une compatibilité. Une incompatibilité, une ambiguïté de résolution, une capacité obligatoire absente ou une signature non conforme bloque la composition.

Le build des modules métier doit vérifier la propriété des modèles et migrations, l'identification des permissions et ressources, la présence des contrats publics, l'absence d'écriture directe dans les modules voisins et la séparation entre code métier et providers d'intégration. Les modules ou providers non sélectionnés ne doivent pas modifier les artefacts, les migrations ou la configuration effective d'une installation.

Chaque module doit embarquer ou référencer les métadonnées de ses migrations sans les confondre avec les migrations d'un autre propriétaire. Le build doit vérifier que les migrations préservent les données tenant-scoped, les scopes, les ACL, les tombstones, les états de rétention, les événements et les configurations versionnées. Une migration partiellement appliquée doit rester identifiable et ne doit pas rendre l'artefact activable comme si elle avait réussi.

La sélection du provider doit être reproductible entre Debian, Docker et développement. Le build doit refuser qu'un ordre d'import, un chemin de filesystem, une dépendance transitive ou la simple présence d'un paquet choisisse implicitement l'implémentation active.

## 43. Composition frontend récursive

Le build doit composer les facettes frontend déclarées par les composants `MODULE` et `SUBMODULE` dans le même graphe que leurs dépendances fonctionnelles. Il doit résoudre récursivement les contributions, les façades publiques, les contraintes SemVer, les traductions, les points d'entrée et les compatibilités avec le shell avant de produire les bundles ou chunks livrés. Aucun type de composant, registre ou lifecycle frontend parallèle ne doit être introduit pour cette composition.

La validation de build doit refuser une dépendance frontend obligatoire absente, cyclique ou incompatible, un import d'implémentation privée, une collision de route, d'identifiant ou de contribution, ainsi qu'une politique de fusion ou de priorité implicite. Un sous-module optionnel invalide ne peut retirer que ses contributions et les dépendances qui les requièrent explicitement ; il doit laisser un diagnostic corrélé sans modifier l'ordre ni l'état des composants indépendants.

Les artefacts Debian, Docker et de développement doivent produire la même composition frontend pour les mêmes manifests, versions et paramètres de build autorisés. Le lazy loading ne peut différer que le chargement d'un chunk déjà construit et livré ; le runtime ne doit ni découvrir par scan, ni télécharger, ni installer, ni évaluer du code distant pour rendre active une contribution de module ou de sous-module.

## 44. Validation des capacités d'extension de plateforme

Le build doit vérifier les manifests, contrats, versions, signatures,
provenances, SBOM et contraintes de compatibilité des composants obtenus par un
registre. Un composant récupéré depuis une source distante doit être vérifié
avant son inclusion ; un registre ne peut pas rendre active une dépendance ou
un provider non sélectionné. Les artefacts doivent d'abord rester utilisables
avec une source privée ou hors ligne signée ; un marketplace public est validé
comme adapter optionnel.

Le build des règles métier doit valider le DSL restreint, ses schémas, versions,
déterminisme, tests et frontières avec l'autorisation et les workflows ; il doit
refuser toute évaluation de code arbitraire au runtime. Le build IA doit vérifier
la désactivation par défaut, les contrats des providers, l'autorisation explicite
des outils médiés par Commands, les versions de prompts et d'évaluations, les
limites de budget, la politique de sortie des données et l'absence de données,
credentials ou sorties sensibles dans les artefacts.

Pour les caches, l'analytique et la collaboration, les validations contrôlent
les partitions tenant/scope, la propagation des invalidations, la reconstruction
des dérivés, le filtrage autorisé, les politiques de rétention et les modes
dégradés. Les tests de collaboration couvrent les conflits, le rejeu, la
révocation, la reconnexion et la convergence sans mutation métier implicite.
Ils valident les adapters CRDT ou OT déclarés sans imposer de référence avant
l'identification des premières ressources collaboratives.

Les builds de clients mobiles et desktop génèrent ou valident des SDK fondés
sur les contrats publics. Ils vérifient le stockage local chiffré lorsque la
plateforme le déclare, l'absence de jeton dans les artefacts et la propagation
du tenant, du scope, de l'identité et de la révocation aux notifications et
liens profonds.

Le build vérifie que les références de secrets restent externes, sont liées à
des identités de workload et privilégient des credentials courts, que les
providers SCIM, de secrets et de déploiement déclarent leurs contrats et que
leurs tests n'utilisent que des données synthétiques. Il valide d'abord le
chaînage vérifiable d'audit et le scellement externe optionnel ; les politiques
WORM ne sont validées que lorsqu'un déploiement les déclare. Il valide enfin les
stratégies canary ou blue/green sans promouvoir une révision incompatible ni
masquer un échec de health gate, de migration, de compatibilité ou de sécurité.

## 45. Runtime de référence, P0 et objectifs de service

Les builds de référence doivent valider une unique pile Django, PostgreSQL et
TanStack. Ils ne doivent pas introduire une variante de runtime cachée ni
présenter une implémentation expérimentale comme compatible avec le P0. Les
adapters futurs sont des composants distincts, validés par leurs contrats et
leurs matrices de compatibilité.

Un artefact P0 doit vérifier la composition minimale approuvée : mécanismes de
composition, `pixs.core`, contexte tenant/scope, autorisation, API, migrations,
runtime, provisionnement, sécurité, secrets, audit, observabilité, gouvernance,
cycle de vie des données, conformité et composant d'exemple. Une capacité hors
P0 ne peut devenir active que par sélection explicite.

Chaque release ou profil de déploiement doit déclarer des objectifs de service
versionnés et mesurables couvrant disponibilité, latence, invalidation, reprise
et compatibilité. Le build et les suites applicables doivent produire une preuve
reproductible de leur vérification, ou un diagnostic explicite lorsque le profil
ne les satisfait pas. Aucun seuil chiffré universel ne doit être inventé par la
chaîne de build.
