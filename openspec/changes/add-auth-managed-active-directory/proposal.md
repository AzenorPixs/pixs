# Active Directory propre géré par pixs.auth.directory.ad

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
