# Références normatives — O20

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| reporting-analytics / 10 | [Projections analytiques dérivées et propriétaires](../../specs/reporting-analytics/spec.md#L10) | NE | AUDIT_AVANT_CREATION |
| reporting-analytics / 21 | [Couche sémantique versionnée](../../specs/reporting-analytics/spec.md#L21) | NE | AUDIT_AVANT_CREATION |
| reporting-analytics / 32 | [Filtrage, gouvernance et résidence à la source](../../specs/reporting-analytics/spec.md#L32) | NE | AUDIT_AVANT_CREATION |
| reporting-analytics / 44 | [Exports et rapports asynchrones contrôlés](../../specs/reporting-analytics/spec.md#L44) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence reporting-analytics--8294460d08

Source : `openspec/specs/reporting-analytics/spec.md`, ligne 10. SHA-256 du bloc : `8c81f3cccc2bf1210daf1bd7d9de45f7876a5a184c4554b14757eb5dc50099b7`.

~~~~text
### Requirement: Projections analytiques dérivées et propriétaires

Chaque projection analytique MUST déclarer son composant propriétaire, ses
sources, son schéma, sa fraîcheur, sa reconstruction et sa lignée. Une
projection MUST NOT devenir la source de vérité d'une ressource métier.

#### Scenario: Projection reconstruite

- **WHEN** une projection est invalidée ou perdue
- **THEN** elle est reconstruite depuis les sources et événements autorisés avec un état de fraîcheur explicite
~~~~

### Référence reporting-analytics--08753652ec

Source : `openspec/specs/reporting-analytics/spec.md`, ligne 21. SHA-256 du bloc : `32eb0107b7cd88a3d9f725b96588ba32253fd8b9ba111ddee50d18119bb53264`.

~~~~text
### Requirement: Couche sémantique versionnée

Les métriques, dimensions, définitions de rapport et filtres autorisés MUST
être versionnés et testables. Une métrique ambiguë ou incompatible MUST être
refusée avant publication d'un rapport ou d'un tableau de bord.

#### Scenario: Définition de métrique modifiée

- **WHEN** une métrique change de sens ou de calcul de manière incompatible
- **THEN** une nouvelle version est publiée sans réécrire silencieusement les résultats précédents
~~~~

### Référence reporting-analytics--0f2354e0de

Source : `openspec/specs/reporting-analytics/spec.md`, ligne 32. SHA-256 du bloc : `cea31b0b33266e5c762cdf43806de4405fc63cd05c43e47e32dbdc79bacfeb61`.

~~~~text
### Requirement: Filtrage, gouvernance et résidence à la source

Toute requête analytique et tout rapport MUST appliquer le ScopeContext,
l'autorisation, la classification, la résidence et la minimisation avant toute
agrégation ou exposition. Un tableau de bord MUST NOT déduire ou révéler une
donnée non accessible par ses résultats agrégés.

#### Scenario: Agrégat inter-tenant non autorisé

- **WHEN** un rapport demande des données de plusieurs tenants sans droit plateforme explicite
- **THEN** la requête est refusée ou limitée au périmètre autorisé
~~~~

### Référence reporting-analytics--04b2c9438c

Source : `openspec/specs/reporting-analytics/spec.md`, ligne 44. SHA-256 du bloc : `c7e055e372294caaafdd68603742d3a6b257a6c0b0ea3b1d0ffde74e81c17db7`.

~~~~text
### Requirement: Exports et rapports asynchrones contrôlés

Un rapport coûteux ou un export MUST utiliser une opération persistante avec
durée de conservation, audit et révocation. Son résultat MUST être filtré,
gouverné et stocké via les providers déclarés.

#### Scenario: Autorisation révoquée pendant un export

- **WHEN** le droit du demandeur est retiré avant la remise du résultat
- **THEN** le résultat est refusé ou révoqué selon la politique déclarée
~~~~

