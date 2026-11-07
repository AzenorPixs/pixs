# Shell frontend — modes autonome et composé

Le mode STANDALONE fournit le shell TanStack/React autonome à la route publique `/`, une page indisponible pour toute autre route, les catalogues anglais/français et les thèmes clair/sombre. Il ne charge aucune donnée applicative. Le mode COMPOSED C11 raccorde une sélection opérateur explicite, les contributions déclarées et le contexte WEB Auth ; sa réalisation ne prouve pas sa validation fonctionnelle ni la disponibilité P0.

## Dépendances

Les versions de Node.js et npm de l'environnement de référence sont relevées dans [DEVOPS.md](../DEVOPS.md). Les quatre dépendances directes autorisées sont figées: @tanstack/react-router1.170.41, react19.3.0, react-dom19.3.0 et vite8.3.1. Le lock npm fixe également leurs dépendances transitives. Aucun plugin JSX, TypeScript ou générateur supplémentaire n’est utilisé.

## Installation et vérifications

Depuis la racine du projet, utiliser l’environnement propre et la configuration utilisateur vide et un chemin global absent. Le cache reste dans frontend/.cache/npm. Le chemin no-global-config.npmrc doit rester absent; aucun secret ni fichier env n’est chargé.

```sh
/usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node/current/bin/npm --userconfig=/dev/null --globalconfig=/home/devops/datas/pixs/frontend/.cache/npm/no-global-config.npmrc --cache /home/devops/datas/pixs/frontend/.cache/npm --prefix /home/devops/datas/pixs/frontend install --ignore-scripts --no-audit --no-fund
/usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node/current/bin/npm --userconfig=/dev/null --globalconfig=/home/devops/datas/pixs/frontend/.cache/npm/no-global-config.npmrc --cache /home/devops/datas/pixs/frontend/.cache/npm --prefix /home/devops/datas/pixs/frontend test
/usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node/current/bin/npm --userconfig=/dev/null --globalconfig=/home/devops/datas/pixs/frontend/.cache/npm/no-global-config.npmrc --cache /home/devops/datas/pixs/frontend/.cache/npm --prefix /home/devops/datas/pixs/frontend run build
```

`npm test` exécute les cas déclarés dans son harnais de catalogue et de contrats
du shell dans Chromium et Firefox
headless, aux chemins déclarés par `DEVOPS.md` (`/usr/bin/chromium` et
`/usr/bin/firefox`). Les deux exécutables doivent être présents ; un navigateur
absent, un cas non exécuté ou une erreur de nettoyage fait échouer le verdict.
Le harnais sert les modules de test et une liste fermée des catalogues et
contrats purs de `src/shell/` sur un serveur
HTTP loopback éphémère. Chaque navigateur possède son profil jetable, sans
compte connecté, et conserve ses protections ; résultats, fermeture des
processus et du serveur, suppression des profils sont vérifiés avant réussite.
Le délai global est borné à 90 secondes. Aucune dépendance supplémentaire ni
réécriture des trois cas n'est introduite.

Le diagnostic distinct `npm run test:node` conserve l'exécution des trois cas
sous Node ; son succès ne remplace pas la preuve issue des deux navigateurs.
Les cas vérifient les catalogues complets, le refus des doublons/valeurs invalides
et la résolution de langue déterministe. Le build valide les catalogues avant compilation et produit frontend/dist/. Les scripts tiers d’installation sont désactivés. Cache, node_modules et dist sont des artefacts régénérables et ne sont pas des sources.

## Démarrage et arrêt

```sh
/usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node/current/bin/npm --userconfig=/dev/null --globalconfig=/home/devops/datas/pixs/frontend/.cache/npm/no-global-config.npmrc --cache /home/devops/datas/pixs/frontend/.cache/npm --prefix /home/devops/datas/pixs/frontend run dev
```

Le serveur reste uniquement sur http://127.0.0.1:5173, refuse un port déjà occupé et limite l’accès au filesystem frontend/. Attendre le message de disponibilité avant le contrôle au navigateur. Arrêter cette commande avec Ctrl+C puis vérifier que le port ne répond plus. En session orchestrée, démarrage et arrêt constituent deux mandats CAB distincts et n’autorisent pas d’autre processus. Aucun déploiement ni accès public n’est fourni.

## Test navigateur reproductible

Une fois le serveur Vite prêt sur http://127.0.0.1:5173, exécuter depuis la racine du projet :

```sh
/usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node/current/bin/node frontend/tests/browser-check.mjs
```

Le script utilise Chromium installé direct via /usr/lib/chromium/chromium, sans dépendance nouvelle. La sandbox est conservée, le profil est jetable et isolé sous frontend/.cache avec préfixe court et TMPDIR éphémère, garde socket en octets et nettoyé après exécution. Les échanges CDP sont bornés avec délai global et nettoyage du processus. Le zoom CSS 200 est un proxy explicite sans zoom natif. Ces contrôles limités ne constituent ni un audit WCAG complet ni une preuve de disponibilité intégrée.

## Présentation et limites

La langue choisie en mémoire prévaut sur la préférence navigateur supportée, puis l’anglais. La racine HTML suit la langue active. Les textes appartiennent au catalogue shell, sans donnée dynamique.

Le thème choisi en mémoire prévaut sur la préférence système, puis le clair. Les changements s’appliquent sans rechargement; couleurs, espacements, typographie, bordures et focus utilisent les tokens sémantiques du shell. Les contrôles HTML natifs, noms accessibles, lien d’évitement, focus visible et reflow font l’objet de vérifications locales. Ces vérifications limitées ne constituent ni un audit WCAG complet ni une déclaration de stabilité de primitives partagées.

Le mode STANDALONE reste utilisable pour développer le shell seul. Le mode COMPOSED et ses limites sont décrits plus bas ; sa disponibilité intégrée exige les preuves de recette, de transport et d’accessibilité applicables.


## Contrats publics C11 — tâche 2.1

Les suites isolées de ces contrats purs n’activent pas de contribution ni de raccord Auth réel. Les doubles de transport ne qualifient ni C03/C04 ni une autorisation serveur. Leur utilisation par le renderer composé exige sa propre recette ; le rendu autonome reste distinct.

- src/shell/api-v1.js expose la façade version 1.0.0 : ports explicites, snapshots immuables de périmètre/époque, QueryClient et CommandClient, navigation, invalidation, traduction et présentation. Les requêtes ciblent les routes WEB publiques C06 ; aucune clé ni jeton n’est conservé côté client. Une réponse d’une époque périmée est refusée. Une commande n’est confirmée qu’après une enveloppe serveur valide ; refus connu, panne et issue inconnue restent distincts.
- src/shell/composition-descriptor-v1.js vérifie un descripteur 1.0.0 par rapport à une facette déjà validée par le Kernel, avec validateCompositionDescriptor(value, { facet, extensionPoints, limits }). Les huit types sont ROUTE, PAGE, NAVIGATION, COMPONENT, FORM, TRANSLATION, UI_PERMISSION et UI_SLOT. Le snapshot retourné est profondément gelé. Les limites maxTextLength (unités UTF-16), maxRequires, maxPermissions, maxPoints, maxLocales et maxCatalogKeys sont toutes explicites et strictement positives, sans valeur par défaut. La grammaire de dépendances et SemVer appartient au Kernel ; les textes, l’ordre et la multiplicité de requires sont seulement comparés et préservés ici.
- createShellExtensionPoints() fournit onze points publics sous pixs.shell.* : routes, pages, navigation-items, components, forms, translations, ui-permissions et les slots header/navigation/main/footer. Chaque point déclare propriétaire, catégorie, version, schéma et garanties structurelles. Les points modulaires supplémentaires doivent être explicitement fournis avec les mêmes métadonnées. Les permissions d’affichage et le niveau de confiance sont des déclarations ; leur validation structurelle ne constitue ni une décision d’autorisation ni une preuve de sandbox.
- Les payloads de rendu désignent des exports JS nommés de la seule entrée entry déclarée par le manifest. Ils n’ajoutent aucun chemin de module privé. Une ROUTE porte {path, mode: "CSR", page} ; PAGE/COMPONENT/FORM portent {export} ; NAVIGATION porte {route, labelKey} ; TRANSLATION porte {catalog} ; UI_PERMISSION porte {key, fallback} ; UI_SLOT porte {slot, export}. Les chemins de route utilisent des segments littéraux ou {param_name}, sans décodage ni normalisation. La résolution des exports, la provenance, les collisions et l’activation sont contrôlées par la composition du build, pas par ce validateur pur.
- scripts/build_frontend_composition.py réutilise les vrais validate et compose du Kernel, puis projette les facettes suivant l’ordre commun. BuildLimits et les sélections sont explicites. L’API pure reçoit les attestations externes authentifiées par son appelant de confiance ; elle n’en fabrique aucune. Les empreintes SHA-256 tracent les textes et ne prouvent pas leur authenticité. La CLI ne reçoit aucune attestation : une composition non vide qui exige ces preuves est refusée, sans produire ni remplacer de plan. Elle ne constitue donc pas, seule, un chemin de build nominal authentifié. Les accès source sont sélectionnés exactement et sans suivre les liens symboliques ; les sorties JSON sont confinées à frontend/.generated/ et remplacées atomiquement. Ce plan ne déclare jamais de compatibilité globale.

Contrôles complémentaires depuis la racine, sans réseau ni secret :

~~~sh
/usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node/current/bin/node --test /home/devops/datas/pixs/frontend/tests/shell-contracts.test.mjs
/usr/bin/env -i PATH=/home/devops/python/current/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONPATH=/home/devops/datas/pixs/src PYTHONDONTWRITEBYTECODE=1 /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest discover -s /home/devops/datas/pixs/frontend/tests -p test_build_composition.py -v
~~~

La suite Python comporte 35 cas sur le vrai Kernel, l’API pure, la CLI et les opérations filesystem. Les attestations fournies par ses fixtures sont des entrées de test explicites, sans qualification d’un fournisseur réel. Les temporaires sont créés sous frontend/tests/ et frontend/.generated/, dans des répertoires uniques nettoyés. Ces preuves de contrat ne remplacent ni les contrôles du bundle intégré, ni les tests Auth réels, ni les vérifications visuelles et d’accessibilité applicables lorsque le rendu sera raccordé.

## Mode composé C11

Les scripts npm conservent un choix explicite : `dev`/`build` lancent STANDALONE, `dev:composed`/`build:composed` lancent COMPOSED. Le second exige une sélection opérateur épinglée et une politique complète ; il ne découvre aucun composant, provider, secret ou fichier de configuration par défaut. Les contributions proviennent des vrais manifests et des seules entrées frontend déclarées.

La forme suivante décrit les arguments à renseigner, depuis la racine du projet. Les valeurs en majuscules sont des paramètres à remplacer, pas un profil de production fourni :

~~~sh
/home/devops/node/current/bin/node frontend/scripts/run_frontend_build.mjs \
  --mode COMPOSED --command build \
  --selection CHEMIN_SELECTION_JSON --selection-sha256 SHA256_SELECTION \
  --policy CHEMIN_POLITIQUE_JSON --policy-sha256 SHA256_POLITIQUE \
  --max-policy-bytes MAX_POLICY_BYTES --max-wire-bytes MAX_WIRE_BYTES \
  --python /home/devops/datas/pixs/.venv/bin/python3
~~~

La commande `serve` utilise la même sélection, politique, empreintes et chaîne de composition. Les chemins JSON sont relatifs à la racine du projet ; les traversées, liens symboliques et sources exclues sont refusés. Les SHA-256 portent sur les octets originaux fournis par l'opérateur. Les deux bornes de transport sont des entiers strictement positifs, concordants avec la politique. Aucun fichier env n'est chargé par cette CLI.

Les formats exécutables font autorité dans `scripts/build_frontend_selection.py` et `scripts/frontend_composition_bridge.py` : sélection `pixs.frontend.selection/1.0.0`, frontière `LOCAL_OPERATOR_SELECTION` ; document de politique `pixs.frontend.build-policy/1.0.0` à trois clés `schema`, `policy`, `limits`. Les sept groupes de limites sont `selection`, `imports`, `graph`, `requirements`, `sourceProfile`, `presentation`, `wire`. Les admissions, points modulaires, façades étrangères, locales et limites sont explicites. Un exemple synthétique et ses attestations de test ne qualifient jamais les composants réels ou le profil P0.

L'appelant de confiance fournit et authentifie les attestations externes exigées par le Kernel : composant/cible et versions exactes, suite/version, verdict et référence de preuve. La chaîne frontend n'en fabrique aucune. Une attestation absente ou invalide bloque la composition. Une empreinte de source ne remplace pas cette preuve et une suite bornée ne démontre pas les obligations qu'elle n'a pas exécutées.

Le pipeline capture les octets avant analyse, réutilise la composition Kernel, contrôle les imports publics et le profil syntaxique, résout les exigences et collisions, puis fournit le module virtuel privé `virtual:pixs-composition/v1`. Vite compile ces octets capturés ; les sources et entrées opérateur sont revérifiées avant publication et lors des accès de développement. Une dérive produit un refus explicite ; elle ne recharge pas silencieusement une contribution différente. Le niveau TRUSTED et les gardes syntaxiques ne constituent pas une sandbox universelle. SANDBOXED sans adapter effectif reste refusé.

Les routes du graphe sont enregistrées indépendamment de leur visibilité à la connexion. Les emplacements publics header/navigation/main/footer et les composants référencés passent par l'adapter privé de présentation ; ils ne reçoivent ni moteur React, ni store de session, ni accès aux implémentations privées des autres propriétaires.

### Session et contexte WEB

Le mode composé propose un choix explicite plateforme, tenant ou tenant/scope. Un contexte ne devient actif qu'après le GET serveur Auth correspondant. Les références opaques sont encodées segment par segment ; elles ne sont pas contraintes à UUIDv7. L'identifiant de session reste celui d'Auth.

Login, logout, cookie protégé et CSRF utilisent les frontières WEB existantes. Aucun Bearer, cookie d'authentification ou justificatif n'est lu ou persisté par le JavaScript ; le champ mot de passe est vidé après tentative. L'origine doit être HTTPS et approuvée côté serveur. Le serveur Vite local décrit plus haut écoute en HTTP : ce démarrage seul ne permet donc pas de qualifier l'authentification applicative. Une recette HTTPS réellement composée est nécessaire.

La métadonnée du contexte contient le résolveur public contrôlé : 37 opérations Core, complétées uniquement par les liaisons propriétaires explicitement injectées. Une liaison absente ou ambiguë est refusée avant envoi. Cette métadonnée ne constitue ni un droit, ni une disponibilité serveur.

Les requêtes authentifiées du shell portent l'indication optionnelle `X-Shell-Session-ID` de la session affichée. Le serveur la compare à la session réellement résolue depuis le cookie ; une différence est refusée avant dispatch. Le bootstrap contexte, le login et CSRF n'utilisent pas l'ancien identifiant. Les clients legacy sans cet en-tête conservent leur contrat. Cette indication ne crée jamais d'autorisation.

Un changement de contexte, de session, une déconnexion, une expiration ou une invalidation purge les données dépendantes ; les réponses d'une ancienne époque ne sont pas affichées. L'indisponibilité réseau, HTTPS ou inter-onglets reste visible. Une erreur 401/403 ne démontre pas à elle seule une révocation. Les échanges inter-onglets ne transportent que des invalidations.

### Intentions et champs

Query et Command gardent des états distincts : LOADED signifie données lues ; CONFIRMED exige un résultat serveur confirmé. PENDING interdit le double envoi. UNKNOWN conserve la même clé d'idempotence et l'empreinte du contenu ; aucune relance automatique ni nouvelle commande de remplacement n'est produite. Un autre contenu ou contexte de session est refusé pour cette reprise. L'indisponibilité, le refus et les saisies invalides restent explicites.

Les cinq champs sont texte, booléen, entier sûr, liste de chaînes et liste d'enregistrements. Le booléen false reste valide ; un entier facultatif vide reste null. Les listes utilisent une zone multiligne par valeur/cellule, avec ajout et suppression de lignes : ordre, doublons et LF sont conservés sans trim, split ou conversion de JSON. Plages, cardinalités et colonnes viennent des contrats déclarés. Le changement explicite de modèle ou d'époque réinitialise les brouillons ; une simple progression de l'action ne les remonte pas arbitrairement.

Les hints UI serveur indisponibles ne créent aucun droit. En l'absence de correspondance positive action/ressource spécifiée, une contribution demandant des display_permissions reste indisponible de façon conservatrice. L'autorisation réelle de chaque Query/Command appartient toujours au serveur ; cette limite ne qualifie pas une politique UI positive.

### Validation de C11

Le séquencement demandé distingue réalisations et preuves : les sources C11 ci-dessus sont réalisées, mais la phase de tests/validation reste à exécuter. Les résultats historiques sont datés et ne qualifient pas les sources nouvelles. Syntaxe, suites Node/Python, Chromium/Firefox headless, bundle et développement composés, HTTPS intégré, clavier/focus, contraste, reflow et technologies d'assistance applicables restent à recouper avant validation. Les doubles et contrôles manuels doivent être identifiés. Le paquet Debian et la qualification installée restent dans C18/C17/C19 ; aucun P0 complet n'est annoncé.
