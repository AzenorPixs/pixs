# Shell local initial

Ce jalon fournit une interface autonome TanStack/React à la route publique `/`, une page indisponible pour toute autre route, les catalogues anglais et français et les modes clair/sombre. Il ne charge aucune donnée applicative et ne fournit ni session, ni tenant, ni API, ni contribution de module, ni composition Django/P0. Il ne prouve pas la disponibilité intégrée du profil de référence.

## Dépendances

Les versions de Node.js et npm de l'environnement de référence sont relevées dans [DEVOPS.md](../DEVOPS.md). Les quatre dépendances directes autorisées sont figées: @tanstack/react-router1.170.41, react19.3.0, react-dom19.3.0 et vite8.3.1. Le lock npm fixe également leurs dépendances transitives. Aucun plugin JSX, TypeScript ou générateur supplémentaire n’est utilisé.

## Installation et vérifications

Depuis la racine du projet, utiliser l’environnement propre et la configuration utilisateur vide et un chemin global absent. Le cache reste dans frontend/.cache/npm. Le chemin no-global-config.npmrc doit rester absent; aucun secret ni fichier env n’est chargé.

```sh
/usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node/current/bin/npm --userconfig=/dev/null --globalconfig=/home/devops/datas/pixs/frontend/.cache/npm/no-global-config.npmrc --cache /home/devops/datas/pixs/frontend/.cache/npm --prefix /home/devops/datas/pixs/frontend install --ignore-scripts --no-audit --no-fund
/usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node/current/bin/npm --userconfig=/dev/null --globalconfig=/home/devops/datas/pixs/frontend/.cache/npm/no-global-config.npmrc --cache /home/devops/datas/pixs/frontend/.cache/npm --prefix /home/devops/datas/pixs/frontend test
/usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 /home/devops/node/current/bin/npm --userconfig=/dev/null --globalconfig=/home/devops/datas/pixs/frontend/.cache/npm/no-global-config.npmrc --cache /home/devops/datas/pixs/frontend/.cache/npm --prefix /home/devops/datas/pixs/frontend run build
```

`npm test` exécute les trois cas unitaires existants dans Chromium et Firefox
headless, aux chemins déclarés par `DEVOPS.md` (`/usr/bin/chromium` et
`/usr/bin/firefox`). Les deux exécutables doivent être présents ; un navigateur
absent, un cas non exécuté ou une erreur de nettoyage fait échouer le verdict.
Le harnais sert uniquement les modules de test et `catalogs.js` sur un serveur
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

Le profil est utilisable pour développer et vérifier le shell seul. Les services applicatifs, la composition complète, la session, les API et les contrôles d’accessibilité approfondis restent des jalons nécessaires avant de présenter une application intégrée disponible.
