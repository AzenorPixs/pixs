# Design

## Décisions
1. Transport minimal sans protocole navigateur : serveur node:http sur
   127.0.0.1:0, whitelist exacte `/tests/shell.test.mjs`, `/src/catalogs.js`,
   `/t/test-adapter.mjs`, `/t/assert-adapter.mjs`, `/` (runner.html),
   `POST /result`. Le fichier de test existant est servi tel quel ; son import
   relatif `../src/catalogs.js` se résout naturellement. Aucune réécriture,
   fetch ou Blob de source.
2. Importmap de la page servant à mapper exactement `node:test` et
   `node:assert/strict` vers des adaptateurs limités au sous-set réellement
   utilisé (deepEqual strict, ok, equal strict, match, throws {message}) ;
   toute divergence de sémantique = échec du cas.
3. Pilote `catalog-browser.mjs` : paramètres figés —
   Chromium : `/usr/bin/chromium --headless --user-data-dir=<profiléphémère>` ;
   Firefox : `/usr/bin/firefox --headless --no-remote --profile <profiléphémère>` ;
   sandbox conservé, aucun accès au profil personnel, env PATH=/usr/bin:/bin,
   TMPDIR/XDG dans un dossier éphémère sous frontend/.cache.
4. Corrélation : chaque exécution navigateur porte un `run_id` aléatoire de
   corrélation (non credential, non secret d'authentification) ; corps POST
   borné en taille ; verdict ok = 3/3 cas pass pour les deux navigateurs,
   deux réponses corrélées reçues dans une deadline bornée, arrêt
   SIGTERM→SIGKILL du groupe, profil supprimé, cleanup sans erreur.
5. Node n'exécute jamais les cas à la place du navigateur ; `test:node` reste
   un diagnostic explicite séparé.

## Alternatives écartées
- CDP/BiDi/geckodriver/Playwright/Selenium : nouvelles dépendances ou
  protocoles non requis pour des unités ESM pures ; écartés par mandat.
- Vite dev server : non nécessaire pour des modules ESM servis statiquement.
- Réécriture/Blob de la source de test : dupliquerait implicitement le
  chargement ; l'importmap suffit et la source reste intacte.

## Bornes et invariants du harnais

- Les chemins sont résolus depuis `import.meta.url`, indépendamment du cwd de npm.
- Corps POST limité à 64 KiB ; erreurs et sorties bornées ; run_id de corrélation
  non credential, sans lecture de DEVOPS.md ni des profils personnels.
- Délai global maximal de 90 secondes pour les deux navigateurs, arrêt borné de
  chaque processus créé et fermeture du serveur ; préfixes éphémères courts.
- Les réponses doivent porter les trois noms de cas exacts, uniques, chacun
  exécuté une fois ; aucun zéro cas, doublon, réponse tardive ou répétée ne peut
  devenir une réussite. Les ressources servent uniquement la whitelist exacte.
- HOME, TMPDIR et XDG du processus navigateur restent dans son espace éphémère ;
  aucun drapeau no-sandbox ou disable-web-security n'est accepté.
- Le rapport ne devient vert qu'après fermeture des processus et du serveur,
  suppression des profils et observation des trois résultats de chaque moteur.

## Limites
- Sans interception réseau : la page est strictement same-origin loopback et
  le serveur ne sert que la whitelist ; le blocage du réseau externe du
  navigateur n'est pas imposé par le pilote.
