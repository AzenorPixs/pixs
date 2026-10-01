# Conception du shell initial

## Context

Le frontend est absent. Les contrats initiaux et les règles internationales, de thème et d’accessibilité sont validés. La surface HTTP backend reste absente ; aucune identité, autorisation ou disponibilité métier ne peut être simulée.

## Goals / Non-Goals

Livrer un shell TanStack/React compilable séparément et vérifiable localement. Les contributions de modules, les clients API, la session tenant et la composition Django/P0 restent des jalons distincts. Ce shell autonome ne satisfait pas à lui seul l’exigence de composition initiale intégrée.

## Decisions

- JavaScript ES modules avec React.createElement et routage TanStack construit explicitement ; aucun générateur, TypeScript, JSX/plugin ni dépendance directe supplémentaire.
- Unique route shell `/` ; la page introuvable ne rend aucune capacité métier. Aucun fetch, authentification, token, tenant ou accès backend.
- Catalogues du propriétaire shell, canon anglais complet et français ; refus au build des doublons, clés manquantes, valeurs invalides et clés non conformes. Aucun paramètre dynamique dans les textes de ce jalon. Résolution locale : choix utilisateur en mémoire, puis préférence navigateur supportée, puis défaut anglais ; aucun tenant applicable.
- CSS sur tokens sémantiques ; modes light/dark, choix utilisateur en mémoire puis préférence système puis défaut light, sans rechargement ni animation. HTML natif, focus visible, lien d’évitement, champs nommés, reflow et tailles relatives. Aucune primitive partagée déclarée stable ni conformité WCAG globale prétendue.
- Vite désactive envDir et publicDir ; serveur lié seulement à 127.0.0.1:5173 avec strictPort et filesystem limité à frontend/. Le build ne charge aucun fichier env, backend ou secret.
- Versions exactes approuvées et lock npm généré sous mandat séparé, cache npm dans frontend/.cache/npm, scripts d’installation tiers désactivés. Dépendances transitives résolues par npm et figées dans le lock.

## Files

frontend/package.json, frontend/package-lock.json (généré), frontend/index.html, frontend/src/main.js, frontend/src/catalogs.js, frontend/src/theme.css, frontend/vite.config.js, frontend/tests/shell.test.mjs, frontend/README.md.

## Validation

OpenSpec strict avant code et finale ; tests Node natifs des refus de catalogues et du fallback ; build réel ; navigateur local pour route/refus, clavier, langues, thèmes sans rechargement, arbre accessible et reflow ; UTF8/LF, hashes des sources existantes préservées. Les contrôles limités ne constituent pas un audit WCAG complet ni une preuve P0. Démarrage et arrêt du serveur de test exigent chacun leur mandat CAB.

## Risks / Trade-offs

Le shell est un jalon initial autonome et sans backend. Aucun mécanisme alternatif de composants frontend n’est introduit. La composition complète, la session, les API et les contrôles d’accessibilité approfondis restent nécessaires avant publication stable.
