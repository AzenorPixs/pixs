# Références normatives — O21

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| sdk-ecosystem / 8 | [Génération déterministe depuis les contrats](../../specs/sdk-ecosystem/spec.md#L8) | NE | AUDIT_AVANT_CREATION |
| sdk-ecosystem / 17 | [Propagation du contexte et erreurs typées](../../specs/sdk-ecosystem/spec.md#L17) | NE | AUDIT_AVANT_CREATION |
| sdk-ecosystem / 26 | [Outillage validé sans secret](../../specs/sdk-ecosystem/spec.md#L26) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence sdk-ecosystem--1e337e97e1

Source : `openspec/specs/sdk-ecosystem/spec.md`, ligne 8. SHA-256 du bloc : `bed23e28b74e3eee54a723c1fe25d8d859f673883dd25768f62358422d0b2ab9`.

~~~~text
### Requirement: Génération déterministe depuis les contrats

Les kits TypeScript et Python MUST être générés depuis OpenAPI, contrats événementiels et schémas publics avec dépendances verrouillées et matrice de compatibilité ; toute divergence bloque la génération.

#### Scenario: Divergence contrat-kit bloquée

- **WHEN** un kit généré diffère du contrat publié
- **THEN** la génération échoue au lieu de publier un client partiel
~~~~

### Référence sdk-ecosystem--3df32ac65a

Source : `openspec/specs/sdk-ecosystem/spec.md`, ligne 17. SHA-256 du bloc : `f28c9b3d6e2e9ca1de0a71fce7f1dcd80cd66c887646874f5e6b3a58e1782b4d`.

~~~~text
### Requirement: Propagation du contexte et erreurs typées

Les clients MUST propager identité fournie, contextes de tenant et de périmètre, corrélation et idempotence, et exposer pagination, opérations asynchrones, opérations en masse et erreurs typées sans transformer un traitement en cours en succès acquis.

#### Scenario: Périmètre non élargi par le client

- **WHEN** un appel fournit un périmètre hors autorisation
- **THEN** le serveur refuse et le client expose l'erreur typée sans réessai implicite
~~~~

### Référence sdk-ecosystem--e1d2dd0d9a

Source : `openspec/specs/sdk-ecosystem/spec.md`, ligne 26. SHA-256 du bloc : `82fc6877ee01c460e77d398daf4e5a08b476df034353f27bbb38ac4594b73278`.

~~~~text
### Requirement: Outillage validé sans secret

Le kit, l'interface en ligne, les exemples et les tests de conformité réutilisent les validateurs de manifests et de compatibilité, sans créer implicitement identité, donnée ou secret de production ; le navigateur MUST NOT persister jetons ou justificatifs par défaut.

#### Scenario: Exemple sans secret

- **WHEN** un exemple ou un journal contiendrait un jeton ou une donnée de production
- **THEN** sa publication est refusée
~~~~

