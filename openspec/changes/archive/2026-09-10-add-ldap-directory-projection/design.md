## Context

Les primitives `DigitalIdentity`, `Group` et `Membership` sont détenues par
`pixs.core` dans PostgreSQL. Les contrats de synchronisation externe et de
provider permettent déjà une projection sortante, mais ne définissent pas la
sélection de lecture LDAP ni son repli. Voir `proposal.md` et la capacité
`directory-projections` pour les garanties attendues.

## Goals / Non-Goals

**Goals:**

- Fournir un contrat de consultation unique, indépendant du provider concret.
- Utiliser LDAP comme accélération de lecture optionnelle et diagnostiquable.
- Préserver la cohérence immédiatement après une mutation Core.

**Non-Goals:**

- Ne pas ajouter un provider LDAP, une dépendance LDAP, un schéma de DN ou des credentials.
- Ne pas projeter les ACL, permissions, décisions d'autorisation, sessions ou méthodes d'authentification.
- Ne pas autoriser de synchronisation LDAP vers Pixs ni de double autorité.

## Decisions

1. **Une façade Core choisit la source de lecture.** Les consommateurs ne
   contactent jamais LDAP directement ; ils utilisent le contrat de
   consultation Core. Cela conserve l'autorisation et le ScopeContext. Une
   découverte LDAP côté module est rejetée car elle contournerait ces
   frontières.

2. **PostgreSQL est prioritaire pendant la fenêtre de convergence.** La
   synchronisation enregistre son checkpoint et sa confirmation de projection.
   Après une mutation ou lorsque la fraîcheur est insuffisante, la façade lit
   PostgreSQL. Le choix inverse risquerait d'exposer une ancienne appartenance.

3. **LDAP ne reçoit qu'une projection PIXS sortante.** Les mutations sont
   publiées après confirmation de PostgreSQL, avec mapping versionné et
   tombstones. Le bidirectionnel est rejeté car il rendrait ambiguë l'autorité
   des groupes et appartenances.

4. **La disponibilité LDAP est une optimisation.** Une indisponibilité produit
   DEGRADED, des métriques et un audit, puis le repli PostgreSQL. Elle ne peut
   ni élargir des droits, ni empêcher les lectures Core autorisées lorsque la
   base de référence est disponible.

## Risks / Trade-offs

- [Latence supérieure lors du repli] → mise en cache uniquement dérivée et
  bornée, sans modifier la sélection de source ni l'autorisation.
- [Projection LDAP en retard] → borne de fraîcheur déclarée et lecture
  PostgreSQL après mutation.
- [Attribut LDAP trop larges] → profil de gouvernance, allowlist d'attributs et
  scopes minimaux du credential de service.
- [Divergence manuelle LDAP] → absence d'import, détection diagnostiquée et
  resynchronisation explicite depuis PostgreSQL.

## Migration Plan

Le contrat est préparatoire et n'exige aucune migration de donnée. Un futur
provider LDAP sera installé comme composant optionnel, validé par sa suite de
conformité, puis activé avec une projection initiale exportée depuis
PostgreSQL. Le retrait du provider désactive la projection et laisse la
consultation Core lire PostgreSQL ; il ne supprime aucune primitive Core.
