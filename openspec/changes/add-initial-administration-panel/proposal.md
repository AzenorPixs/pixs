# C13 — Panneau d’administration utilisable

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Contextes Instance/Domaine/Tenant, trois volets des organigrammes, habilitations et états réellement vérifiés.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [pixs-instance](../../specs/pixs-instance/spec.md).
- [pixs-domains](../../specs/pixs-domains/spec.md).
- [organization-charts](../../specs/organization-charts/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Pourquoi

La route UI actuelle affiche le shell de développement ; elle ne démontre pas un panneau /admin/ de première configuration et d’administration Core.

## Modifications proposées

Livrer /admin/, première configuration, gestion des primitives Core, route administrable et secours ; utiliser les mêmes contrats que la CLI et l’API, avec visibilité tenant et contrôle ordinaire/Super Admin.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions du profil C00 adoptées le 18 octobre 2026 et intégrées au canon.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `add-installation-and-first-configuration`.
- `enforce-core-data-governance-and-lifecycle`.
- `compose-modular-frontend-with-core-api`.
- `complete-shared-ui-i18n-and-accessibility`.

## Impact

Périmètre de réalisation futur : Construire le panneau avec les mêmes API/Commands que les autres façades ; conserver droits ordinaires et exception Super Admin dans son seul périmètre. Route initiale /admin/ administrable sans collision ; santé réservée selon niveau ; première configuration réservée au compte fonctionnel ; états/messages et erreurs localisés.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Installation → connexion Super Admin → première configuration → NORMAL → administration ordinaire ; changement route sans collision et ancienne route refusée/auditée ; état santé sans credential ; aucun second compte ni transfert de privilège.

## Barrière de conception

Catalogue exact d’écrans/actions, transitions et changement de route sous contrats publics ; ne pas activer implicitement l’administration Django ni créer un second modèle de permissions.
