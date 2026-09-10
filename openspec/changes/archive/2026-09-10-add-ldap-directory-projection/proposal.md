## Why

Pixs définit PostgreSQL comme source de vérité des identités numériques,
groupes et appartenances, mais ne formalise pas le contrat permettant de les
consulter depuis un annuaire LDAP optionnel. Cette projection doit améliorer
la disponibilité des lectures sans créer une seconde autorité ni affaiblir
l'autorisation.

## What Changes

- Introduire une capacité de projection d'annuaire pour les seules identités
  numériques, groupes et appartenances de `pixs.core`.
- Définir LDAP comme provider optionnel de projection sortante depuis Pixs,
  avec mapping explicite, synchronisation idempotente, suppression propagée et
  reprise persistante.
- Définir la consultation préférentielle via LDAP et le repli contrôlé sur
  PostgreSQL lorsque LDAP est indisponible ou non convergé.
- Interdire l'utilisation de LDAP comme source d'autorisation, de gestion des
  ACL, de révocation ou d'authentification par cette capacité.
- Ajouter les validations de build et de conformité nécessaires à cette
  projection et à son comportement dégradé.

## Capabilities

### New Capabilities

- `directory-projections`: projection optionnelle et en lecture des identités
  numériques, groupes et appartenances Pixs vers un annuaire externe, dont
  LDAP, avec repli PostgreSQL.

### Modified Capabilities

- `core`: les primitives d'identité et de groupe exposent une consultation via
  un contrat de projection d'annuaire sans changer leur autorité PostgreSQL.
- `external-synchronization`: la synchronisation de projection d'annuaire
  précise son sens sortant, sa convergence et l'absence d'import autoritatif.
- `testing`: les suites de conformité couvrent la projection d'annuaire, sa
  fraîcheur, son repli PostgreSQL et ses frontières de sécurité.

## Impact

Le changement prépare un contrat, des manifests et des validateurs futurs ;
il n'introduit ni fournisseur LDAP concret, ni dépendance, ni endpoint, ni
credential. `PROJECT.md`, `TECHNICAL.md` et `BUILD.md` décrivent les garanties
architecturales, techniques et de construction associées.
