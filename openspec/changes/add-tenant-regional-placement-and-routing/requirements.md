# Références normatives — O27

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| regional-residency / 8 | [Application de l'exception Super Admin](../../specs/regional-residency/spec.md#L8) | NE | AUDIT_AVANT_CREATION |
| regional-residency / 18 | [Politique de placement versionnée par tenant](../../specs/regional-residency/spec.md#L18) | NE | AUDIT_AVANT_CREATION |
| regional-residency / 27 | [Routage après identité et périmètre](../../specs/regional-residency/spec.md#L27) | NE | AUDIT_AVANT_CREATION |
| regional-residency / 36 | [Bascule contrôlée sans cerveau partagé](../../specs/regional-residency/spec.md#L36) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence regional-residency--3412b15676

Source : `openspec/specs/regional-residency/spec.md`, ligne 8. SHA-256 du bloc : `faf80e301b2e3eec09406b4bb6744a9f3bf5c771a368d9615e14fb866789164d`.

~~~~text
### Requirement: Application de l'exception Super Admin

Les exigences et scénarios de contrôle applicatif de cette capacité MUST s'appliquer sous réserve de l'exception définie par `authorization`, dans le périmètre du seul compte décrit par `initial-administration`. Les comptes ordinaires MUST conserver leurs contrôles. Les profils structurels préparatoires MUST rester inchangés.

#### Scenario: Politique de résidence dérogée

- **WHEN** le Super Admin utilise une dérogation à une politique de résidence pour une opération dans un tenant explicitement accordé
- **THEN** la restriction applicative de résidence dérogée ne bloque pas l'opération
- **AND** la dérogation n'accorde pas un accès à un autre tenant
~~~~

### Référence regional-residency--49b65e67e2

Source : `openspec/specs/regional-residency/spec.md`, ligne 18. SHA-256 du bloc : `586d2864b75c388fa64be049f397e861b0cab2af33b1746c370f64381d94876f`.

~~~~text
### Requirement: Politique de placement versionnée par tenant

Chaque politique MUST déclarer régions logiques autorisées pour primaire, réplicas, traitement, sauvegardes et clés, mode de bascule et époque ; un enfant MUST uniquement restreindre la politique du tenant, jamais l'élargir.

#### Scenario: Élargissement par enfant refusé

- **WHEN** un scope enfant déclare une région hors politique du tenant
- **THEN** la déclaration est refusée avant activation
~~~~

### Référence regional-residency--93c3a8ce37

Source : `openspec/specs/regional-residency/spec.md`, ligne 27. SHA-256 du bloc : `e5bbc9c2b441a173acbc8bf38c38c601319ff7903763ab62576c7235f9987980`.

~~~~text
### Requirement: Routage après identité et périmètre

Le placement est résolu après identité, tenant et scope ; toute région fournie par le client MUST NOT modifier le contexte canonique ni contourner l'autorisation ; chaque dérivé (réplica, index, cache, sauvegarde, journal, événement, copie hors ligne) respecte la même politique.

#### Scenario: Dérivé hors région interdit

- **WHEN** une réplication viserait une région non autorisée
- **THEN** elle est bloquée avec un diagnostic explicite
~~~~

### Référence regional-residency--0d7bd4ca52

Source : `openspec/specs/regional-residency/spec.md`, ligne 36. SHA-256 du bloc : `78d296a878e4644024801bc676d725ad05144e98c0dfb770b67fe0055fd2dfdf`.

~~~~text
### Requirement: Bascule contrôlée sans cerveau partagé

Toute bascule exige région de secours autorisée, barrière ou époque persistante, compatibilité des contrats et schémas, et audit ; l'ancien primaire MUST NOT écrire après bascule ; toute région indisponible ou contrainte insatisfaite produit un état contrôlé.

#### Scenario: Bascule sans barrière refusée

- **WHEN** une bascule est demandée sans mécanisme persistant de barrière
- **THEN** elle est refusée au lieu de risquer deux primaires
~~~~

