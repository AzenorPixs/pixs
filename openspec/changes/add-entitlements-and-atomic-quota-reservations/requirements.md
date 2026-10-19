# Références normatives — O15

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| quotas-entitlements / 8 | [Application de l'exception Super Admin](../../specs/quotas-entitlements/spec.md#L8) | NE | AUDIT_AVANT_CREATION |
| quotas-entitlements / 17 | [Droits rattachés sans élargissement](../../specs/quotas-entitlements/spec.md#L17) | NE | AUDIT_AVANT_CREATION |
| quotas-entitlements / 26 | [Quotas cumulatifs et réservations atomiques](../../specs/quotas-entitlements/spec.md#L26) | NE | AUDIT_AVANT_CREATION |
| quotas-entitlements / 37 | [Application applicative et échec fermé](../../specs/quotas-entitlements/spec.md#L37) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence quotas-entitlements--58bee6923e

Source : `openspec/specs/quotas-entitlements/spec.md`, ligne 8. SHA-256 du bloc : `966d8d76b367709721695c1ed764fc8a792d849a4bf408e50d48d85ab2ed5a47`.

~~~~text
### Requirement: Application de l'exception Super Admin

Les exigences et scénarios de contrôle applicatif de cette capacité MUST s'appliquer sous réserve de l'exception définie par `authorization`, dans le périmètre du seul compte décrit par `initial-administration`. Les comptes ordinaires MUST conserver leurs contrôles. Les profils structurels préparatoires MUST rester inchangés.

#### Scenario: Quota ou entitlement dérogé

- **WHEN** le Super Admin demande une opération dans son périmètre autorisé avec dérogation à un quota épuisé ou à un entitlement
- **THEN** le contrôle concerné ne bloque pas son opération et les autres comptes conservent leurs limites
~~~~

### Référence quotas-entitlements--82d09f0497

Source : `openspec/specs/quotas-entitlements/spec.md`, ligne 17. SHA-256 du bloc : `f84279cdcdfbd3e6d8b28481b618a8e387a4746553959218998eab2e9d873872`.

~~~~text
### Requirement: Droits rattachés sans élargissement

Chaque droit MUST déclarer clé, version, propriétaire, portée (installation, plateforme, tenant, scope enfant explicite), expiration et révocation ; un scope enfant MUST NOT élargir le droit du tenant ; aucun droit utilisateur implicite.

#### Scenario: Élargissement par scope refusé

- **WHEN** un scope enfant invoque une capacité absente du tenant
- **THEN** l'accès est refusé même si le scope le déclare
~~~~

### Référence quotas-entitlements--55894230e6

Source : `openspec/specs/quotas-entitlements/spec.md`, ligne 26. SHA-256 du bloc : `cd2047457beff20eb11c65b87c59c54caa1ca95d0566dafc63a660a11a325f51`.

~~~~text
### Requirement: Quotas cumulatifs et réservations atomiques

Le système MUST respecter les garanties suivantes.

Chaque quota déclare dimension, unité, portée, limite, période et agrégation ; les limites multi-portées s'évaluent simultanément ; check, reserve, commit et release sont persistants, atomiques et idempotents, avec réconciliation et libération contrôlée après annulation.

#### Scenario: Rejou sans double consommation

- **WHEN** une réservation est rejouée après reprise ou réessai
- **THEN** aucune double consommation n'est imputée et l'état reste réconcilié
~~~~

### Référence quotas-entitlements--b8fbd4719a

Source : `openspec/specs/quotas-entitlements/spec.md`, ligne 37. SHA-256 du bloc : `8c48b58f1ec670ae19511b6e6d087161f9e8f88e22e8f3f26b07e223ef2d6af6`.

~~~~text
### Requirement: Application applicative et échec fermé

Le système MUST respecter les garanties suivantes.

Droits et quotas sont évalués côté applicatif avant exécution et réévalués pour travaux, commandes asynchrones, imports et exports ; toute indisponibilité ou incohérence échoue fermé pour opérations protégées, avec réponses stables et audit minimisé.

#### Scenario: Contrôle indisponible

- **WHEN** le contrôle des droits ou quotas ne peut statuer sur une opération protégée
- **THEN** l'opération est refusée au lieu d'un accès implicite
~~~~

