# C16 — Migrations, mise à niveau et restauration

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Bases et dépendances séparées ; restauration ciblée ; fonctionnement normal LDAP/Kerberos et reconstruction d’urgence critique distincts, sans retour Standalone.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [backup-disaster-recovery](../../specs/backup-disaster-recovery/spec.md).
- [brick-redundancy](../../specs/brick-redundancy/spec.md).
- [pixs-instance](../../specs/pixs-instance/spec.md).
- [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Pourquoi

Des migrations bornées existent, mais aucune recette de restauration produit cohérente avec gouvernance, travaux et composition n’est démontrée.

## Modifications proposées

Déclarer contrats et ordre exclusif des migrations, reprises, expansion/contraction ; stratégie sauvegarde du profil avec RPO/RTO déclarés ; restauration isolée et réapplication des gouvernances avant exposition.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions du profil C00 adoptées le 18 octobre 2026 et intégrées au canon.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `add-installation-and-first-configuration`.
- `add-reference-worker-scheduler-and-event-delivery`.
- `enforce-core-data-governance-and-lifecycle`.
- `add-runtime-observability-and-operations`.

## Impact

Périmètre de réalisation futur : Versionner contrats/plans de migration, ordre exclusif, reprise et contraction séparée. Sauvegarder les périmètres réellement livrés puis restaurer isolément, réappliquer effacements/holds avant exposition. Retour arrière applicatif seulement si matrice compatible ; sinon restauration explicite confirmée/auditée.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Installation et mise à niveau interrompues puis reprises ; contraction prématurée refusée ; origine compatible explicitée ; restauration mesurée sans résurrection ; rollback seulement si matrice le prouve, sinon restauration confirmée ; aucune downgrade automatique.

## Barrière de conception

RPO/RTO et rétention du profil, stratégie de sauvegarde et origines/version compatibles ; ne pas sélectionner un outil ni rétrograder une base implicitement.
