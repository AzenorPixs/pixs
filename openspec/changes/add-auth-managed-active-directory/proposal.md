# O37 — Active Directory propre géré par pixs.auth.directory.ad

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Jonction native Windows/GPO V1 dans le même Domaine, qualification du fournisseur, orchestration PBO/PA et prérequis ZT.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [auth-managed-active-directory](../../specs/auth-managed-active-directory/spec.md).
- [managed-device-policies](../../specs/managed-device-policies/spec.md).
- [pixs-domains](../../specs/pixs-domains/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Why

Le catalogue Auth doit aussi permettre de gérer un domaine Active Directory propre. Cette capacité est distincte d'un simple connecteur vers un AD externe et des services OpenLDAP/KDC autonomes.

## What Changes

- Ajouter le sous-module optionnel `pixs.auth.directory.ad` pour provisionner et gérer un service de domaine Active Directory compatible avec le profil retenu.
- Prévoir configuration, démarrage, arrêt, santé, comptes gérés, mappings et reprise sous contrôle Auth.
- Préserver PostgreSQL comme stockage Auth par défaut et le provider Core effectivement sélectionné ; déclarer séparément les données natives du domaine sans faire d'AD un backend Core implicite.
- Coordonner annuaire, Kerberos et DNS du domaine avec les autres services sans collision ni confiance implicite.
- Maintenir AD non requis et non activé dans le profil local standard.

## Capabilities

### New Capabilities

- `auth-managed-active-directory` : domaine Active Directory propre géré par le sous-module `pixs.auth.directory.ad`.

### Modified Capabilities

Aucune. Le change d'architecture Auth complète son catalogue et son delta de composition pour inclure cette option sans l'imposer au P0.

## Impact

Préparation documentaire du 19 octobre 2026, sans implémentation, code, manifest produit, migration, dépendance installée, serveur, domaine, secret, Git ou déploiement. Les deltas restent proposés sans synchronisation du canon. Le choix d'implémentation AD, de plateforme et de versions reste à qualifier ; aucun produit n'est sélectionné par la seule désignation Active Directory.

## Statut des deltas antérieurs après contrôle E3

Les anciens fichiers sous specs/ ont été déplacés, avec empreintes conservées, vers [l’historique interne](historique-deltas-avant-e3/README.md). Le [contrôle de couverture](COUVERTURE_DELTAS_E3.md) relie chaque ancienne exigence au contrat courant et aux tâches ouvertes. Le dossier reste actif ; skip_specs évite seulement la réapplication des anciennes prescriptions. Il ne termine ni la réalisation, ni les tests, ni les 49 tâches encore ouvertes dans les sept dossiers concernés.
