# C00 — Profil de la première livraison P0 installable

## Pourquoi

Les 135 archives clôturent des sous-lots, sans démontrer une composition P0 installable. L’inventaire validé par le développeur le 17 octobre 2026 doit devenir un profil vérifiable, avec des obligations PZT/DNS explicites et une frontière claire entre préparation documentaire et réalisation.

## Modifications proposées

- Définir le profil `pbo-p0-debian-local-v1` : PBO/PFO sur Debian 13 local, Django/PostgreSQL/TanStack, paquet Debian PBO/PFO indépendant, rôles web/worker/scheduler et premier tenant explicitement provisionné.
- Conserver tous les invariants P0, le module essentiel PZT et le module DNS essentiel dans PBO, même sans réseau actif.
- Déclarer non sélectionnés les échanges PBO–PA, l’exécution du service DNS par PA et le réseau PZT. Les fonctions de gestion PBO demeurent ; aucune mesure ou application réseau n’est simulée.
- Relier les 193 exigences PZT aux rôles et conditions d’applicabilité. Une clause impérative applicable ne reçoit aucune dérogation ; un écart bloque la qualification ou exige un change normatif distinct.
- Ordonner les changes C01–C19 nécessaires à ce profil ; PA, Docker et les capacités optionnelles restent des sélections ultérieures, sauf dépendance obligatoire effectivement identifiée.

## Capacités

### Capacités nouvelles

Aucune : le profil précise les capacités existantes.

### Capacités modifiées

- `reference-composition` : identité, périmètre, parcours et preuve de la première composition distribuée.
- `pzt` : obligations de gestion PBO et portée des fonctions non sélectionnées dans ce profil.
- `deb-package` : contenu et identité de la première distribution PBO/PFO.

## Impact

Écritures limitées au présent dossier OpenSpec et aux futurs dossiers de préparation C01–C19. Les deltas restent proposés ; aucune synchronisation dans `openspec/specs/`, modification du code produit, installation, migration, activation, archivage, commit ou publication n’est autorisée par cette préparation.

Les versions finales, architectures qualifiées, provider concret de secrets, détails de sessions et paramètres opérationnels nécessitent les décisions/qualifications décrites dans `design.md`. La validation syntaxique de ce dossier ne vaut ni approbation de ces choix ni readiness P0.
