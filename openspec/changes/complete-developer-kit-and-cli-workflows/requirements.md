# Références normatives — O22

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| developer-experience / 10 | [Parcours local reproductible](../../specs/developer-experience/spec.md#L10) | P | COMPLETER_OU_INTEGRER |
| developer-experience / 21 | [Génération sans activation implicite](../../specs/developer-experience/spec.md#L21) | P | COMPLETER_OU_INTEGRER |
| developer-experience / 32 | [Diagnostics sans fuite](../../specs/developer-experience/spec.md#L32) | P | COMPLETER_OU_INTEGRER |
| sdk-ecosystem / 8 | [Génération déterministe depuis les contrats](../../specs/sdk-ecosystem/spec.md#L8) | NE | AUDIT_AVANT_CREATION |
| sdk-ecosystem / 17 | [Propagation du contexte et erreurs typées](../../specs/sdk-ecosystem/spec.md#L17) | NE | AUDIT_AVANT_CREATION |
| sdk-ecosystem / 26 | [Outillage validé sans secret](../../specs/sdk-ecosystem/spec.md#L26) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence developer-experience--9bcbe069d2

Source : `openspec/specs/developer-experience/spec.md`, ligne 10. SHA-256 du bloc : `b45270b1c563fd91ab6dac69a17fa2f9900135da725ba6a514b57831ead40ec3`.

~~~~text
### Requirement: Parcours local reproductible

Le Developer Kit MUST fournir un parcours local reproductible pour créer et
valider un composant d'exemple compatible P0. Ce parcours MUST utiliser les
contrats et validateurs publiés et MUST NOT exiger de secret ou donnée de production.

#### Scenario: Premier composant local

- **WHEN** un développeur initialise le composant d'exemple P0
- **THEN** il obtient un manifest valide et des diagnostics reproductibles
~~~~

### Référence developer-experience--88eeec99d2

Source : `openspec/specs/developer-experience/spec.md`, ligne 21. SHA-256 du bloc : `fb6bbb0c534e9654b9398a8deaa1d50f88a9660b643add706e86b1f9d6781443`.

~~~~text
### Requirement: Génération sans activation implicite

Le scaffolding MAY générer des fichiers déclaratifs et exemples. Il MUST NOT
enregistrer, activer, provisionner ou publier un composant, provider, tenant ou
secret sans opération explicite autorisée.

#### Scenario: Scaffolding d'un provider

- **WHEN** le Developer Kit génère un squelette de provider
- **THEN** le provider reste non installé et non sélectionné
~~~~

### Référence developer-experience--29852b7822

Source : `openspec/specs/developer-experience/spec.md`, ligne 32. SHA-256 du bloc : `a19297abcb17cfb95ef8f1184c29593ba5021dbf67aad9cda6db576fc2f95f5b`.

~~~~text
### Requirement: Diagnostics sans fuite

Les validateurs et exemples MUST associer les erreurs à la règle ou au champ.
Leurs diagnostics MUST NOT révéler de secret, credential, donnée de production
ou détail privé non nécessaire.

#### Scenario: Manifest incomplet

- **WHEN** un manifest omet un champ obligatoire
- **THEN** le validateur indique le champ et la règle attendue sans donnée sensible
~~~~

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

