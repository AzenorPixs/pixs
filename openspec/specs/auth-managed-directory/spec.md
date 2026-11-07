# auth-managed-directory Specification

## Purpose

LZT est le service OpenLDAP obligatoire de chaque Domaine, exploité par PA et administré par les contrats PBO/Core/Auth.

Cible documentaire du cadrage validé du 31 octobre 2026 ; les contrats proposés existants de cette capacité sont à réconcilier avec ce référentiel avant réalisation. Aucun fournisseur ni plateforme n’est réputé qualifié par cette rédaction.

## Requirements

### Requirement: LZT obligatoire par Domaine et exploitation PA

Chaque Domaine MUST disposer d'au moins un LZT/OpenLDAP et MAY en redonder plusieurs. PA MUST installer, configurer et exploiter les services ; PBO/Core/Auth MUST administrer données, politiques et habilitations par leurs contrats publics. PZT MUST assurer le réseau sans appliquer la configuration OpenLDAP.

#### Scenario: ZT partagé

- **WHEN** deux Domaines partagent ZT
- **THEN** chacun conserve son annuaire et les exécutants PA requis sans fusion des données.

### Requirement: PG source Core et LDAP opérationnel

Les individus et identités numériques déclarées, groupes et ACL applicatifs MUST garder PG comme source de vérité. LZT MUST publier les identités/groupes autorisés pour consultation des applications. Les écritures directes LDAP MUST NOT remplacer les Commands Core ni être réimportées comme vérité métier ; les ACL techniques LDAP MUST rester distinctes des droits Pixs.

#### Scenario: Écriture divergente

- **WHEN** une entrée projetée est modifiée directement dans LDAP
- **THEN** la divergence est diagnostiquée sans mutation Core implicite.

### Requirement: Référence PG et état opérationnel Kerberos normal

PG MUST rester souveraine pour les individus, identités déclarées, groupes, ACL et configurations Pixs. En fonctionnement normal, l'état Kerberos durable MUST résider dans LDAP et la publication PG MUST préserver principals, clés et états natifs. La reconstruction complète depuis PG MUST être une procédure d'urgence en mode critique selon auth-managed-kerberos, sans exiger le déplacement des écritures natives normales vers PG.

#### Scenario: Publication normale

- **WHEN** Core/Auth republient les références PG
- **THEN** les données natives Kerberos présentes dans LDAP restent préservées.

#### Scenario: Perte totale des annuaires

- **WHEN** le Domaine déclenche une reconstruction complète
- **THEN** il suit la procédure critique déclarée sans présenter PG seule comme copie courante de toutes les clés Kerberos.

### Requirement: Multi-maître et convergence observable

Les LZT d'un Domaine MUST pouvoir fonctionner en multi-maître avec réplication propre à LDAP, protections de transport, règles explicites de concurrence, conflits et partition. La confirmation PG MUST NOT valoir convergence LDAP et le multi-maître LDAP MUST NOT modifier l'unicité du primaire PG.

#### Scenario: Publication en retard

- **WHEN** une modification PG est confirmée sans convergence d’un LZT
- **THEN** son retard reste visible et les fonctions exigeant cet état n’annoncent pas une mise à jour effective.

### Requirement: Authentification LDAP déléguée à Auth

Les applications et identités explicitement autorisées MAY s'authentifier via LDAP sous profil Auth. La vérification MUST être déléguée à pixs.auth par un mécanisme qualifié, sur canaux protégés et avec verrouillage commun par identité. La seule projection MUST NOT fournir ce droit ou constituer un repli d'authentification implicite.

#### Scenario: Projection seule

- **WHEN** un profil ne sélectionne que la consultation LDAP
- **THEN** aucun bind d’authentification des individus n’est admis par cette seule sélection.

#### Scenario: Délégation indisponible

- **WHEN** la vérification Auth exigée n’est pas disponible
- **THEN** l’authentification concernée est refusée sans vérification locale moins exigeante.

### Requirement: Réintégration contrôlée des annuaires

Un LZT restauré ou en retard MUST réconcilier retraits, identités, état Kerberos et politiques courantes avant son admission aux services concernés. L'exclusion puis la réadmission MUST suivre le profil et ses preuves ; une ancienne copie MUST NOT réintroduire un accès retiré.

#### Scenario: Ancienne copie LDAP

- **WHEN** la copie restaurée contient un compte révoqué
- **THEN** elle ne traite pas les authentifications concernées avant réconciliation vérifiée.
