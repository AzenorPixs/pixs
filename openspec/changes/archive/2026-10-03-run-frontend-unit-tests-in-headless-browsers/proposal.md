# Proposal: Exécution des unités frontend web dans les navigateurs déclarés headless

## Why
AGENTS.md §13.4 impose désormais que les tests unitaires frontend web soient
exécutés dans les navigateurs déclarés par DEVOPS.md (/usr/bin/chromium et
/usr/bin/firefox) en mode headless. `npm test` actuel (node --test) ne
constitue pas cette preuve et ne doit pas y substituer.

## What Changes
- Nouveau harnais portable `frontend/tests/browser/` : serveur node:http
  éphémère loopback à whitelist exacte, page avec importmap pour les deux
  spécificateurs `node:test` et `node:assert/strict`, exécution réelle des 3
  cas catalogues existants dans chaque navigateur headless, retour des
  résultats par POST borné corrélé par `run_id` de corrélation (non
  credential), nettoyage profil/processus prouvé.
- `frontend/package.json` : `test` lance le pilote des deux navigateurs par
  défaut ; `test:node` (node --test) conservé comme diagnostic distinct.
- Aucun changement des 3 cas, fixtures, sources de production, ni de
  browser-check.mjs ; aucune nouvelle dépendance ; pas de Vite, pas de CDP/BiDi.

## Impact
- Capabilities : `testing` (une exigence ADDED).
- Files : 4 nouveaux sous frontend/tests/browser/, frontend/package.json et
  mise à jour ciblée de frontend/README.md pour les nouvelles commandes.
- Non impacté : cas/fixtures existants, src/, DEVOPS.md, AGENTS.md, Git.
