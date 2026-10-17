# Références normatives — O29

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| component-registry / 11 | [Catalogue de composants et sources déclarées](../../specs/component-registry/spec.md#L11) | NE | AUDIT_AVANT_CREATION |
| component-registry / 24 | [Installation vérifiée sans activation implicite](../../specs/component-registry/spec.md#L24) | NE | AUDIT_AVANT_CREATION |
| component-registry / 36 | [Révocation et retrait contrôlés](../../specs/component-registry/spec.md#L36) | NE | AUDIT_AVANT_CREATION |
| component-registry / 48 | [Recherche et résolution déterministes](../../specs/component-registry/spec.md#L48) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence component-registry--c000e6fd2a

Source : `openspec/specs/component-registry/spec.md`, ligne 11. SHA-256 du bloc : `57376cd9782fa8b881fd0f8c8763be88c5173265e2010f0dc1120b6177ed40da`.

~~~~text
### Requirement: Catalogue de composants et sources déclarées

Un registre MUST exposer les métadonnées publiques, versions, contrats,
compatibilités, provenances et états de révocation des MODULE, PROVIDER et
EXTENSION qu'il catalogue. Une installation MUST pouvoir utiliser une source
privée ou hors ligne signée déclarée. Un marketplace public MAY être fourni par
un adapter, mais MUST NOT être requis pour la résolution ou l'installation.

#### Scenario: Source locale sélectionnée

- **WHEN** une installation sélectionne un catalogue local compatible
- **THEN** elle résout ses composants sans requérir un marketplace central
~~~~

### Référence component-registry--6cfd37bafa

Source : `openspec/specs/component-registry/spec.md`, ligne 24. SHA-256 du bloc : `44e827ee0152b2a5e42736b038a1216931d54bc03baefe43d2cfbd2873449a03`.

~~~~text
### Requirement: Installation vérifiée sans activation implicite

Avant une installation, le système MUST vérifier signature, provenance, SBOM,
compatibilité et politique de confiance. La présence ou la récupération d'un
composant MUST NOT l'activer, sélectionner ses providers ou modifier la
composition effective implicitement.

#### Scenario: Composant téléchargé non sélectionné

- **WHEN** un composant valide est récupéré mais absent de la composition
- **THEN** il reste installé ou disponible sans devenir actif
~~~~

### Référence component-registry--b9f8616872

Source : `openspec/specs/component-registry/spec.md`, ligne 36. SHA-256 du bloc : `b3d3222b350603b8404aba10426a6859adc843c8537bc9f99313add6d408ef4c`.

~~~~text
### Requirement: Révocation et retrait contrôlés

Le registre MUST publier les états de retrait ou révocation de manière
versionnée et traçable. Une révocation critique MUST empêcher une nouvelle
activation et produire un diagnostic sans supprimer silencieusement les
données, contrats ou composants déjà installés.

#### Scenario: Version révoquée au contrôle de composition

- **WHEN** une composition demande une version révoquée par sa politique
- **THEN** son activation est refusée avec une erreur diagnostiquable
~~~~

### Référence component-registry--05f7e58c02

Source : `openspec/specs/component-registry/spec.md`, ligne 48. SHA-256 du bloc : `6a45ad22ff354d029651d7b921752c001ac71e48206d274ead5231e40c279c20`.

~~~~text
### Requirement: Recherche et résolution déterministes

La recherche et la résolution MUST appliquer les identifiants canoniques, les
contraintes SemVer, les canaux et le niveau de confiance déclarés. Un résultat
ambigu ou non vérifiable MUST NOT être installé comme choix par défaut.

#### Scenario: Deux versions compatibles candidates

- **WHEN** deux candidats satisfont la même contrainte sans règle explicite
- **THEN** la résolution échoue au lieu de choisir selon l'ordre du registre
~~~~

