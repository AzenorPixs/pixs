# Références normatives — O05

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| workflows / 8 | [Définitions et instances versionnées](../../specs/workflows/spec.md#L8) | NE | AUDIT_AVANT_CREATION |
| workflows / 17 | [Transitions gardées et autorisées](../../specs/workflows/spec.md#L17) | NE | AUDIT_AVANT_CREATION |
| workflows / 26 | [Reprise persistante sans perte](../../specs/workflows/spec.md#L26) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence workflows--2955744eef

Source : `openspec/specs/workflows/spec.md`, ligne 8. SHA-256 du bloc : `716b840c4dfb7713fb9486cd38302413a5ee925cbcd2ef307155225cdda29949`.

~~~~text
### Requirement: Définitions et instances versionnées

Chaque définition et instance MUST porter version, propriétaire et état persistant ; toute migration d'instance active suit une compatibilité déclarée.

#### Scenario: Instance incompatible non migrée

- **WHEN** une définition évolue de façon incompatible
- **THEN** les instances actives restent sur l'ancienne version ou suivent une migration explicite, jamais une bascule silencieuse
~~~~

### Référence workflows--47ee284385

Source : `openspec/specs/workflows/spec.md`, ligne 17. SHA-256 du bloc : `3d912e8eb7b34faf72aaa3344d2984834215807882817140497b3ed5e5d5e8f9`.

~~~~text
### Requirement: Transitions gardées et autorisées

Chaque transition MUST vérifier gardes, autorisation, périmètre et assurance requise ; toute intervention manuelle, délai ou reprise est explicite, bornée et auditée.

#### Scenario: Transition non autorisée refusée

- **WHEN** un acteur sans permission déclenche une transition sensible
- **THEN** la transition est refusée avec une erreur explicite et un audit
~~~~

### Référence workflows--4ae70ad99e

Source : `openspec/specs/workflows/spec.md`, ligne 26. SHA-256 du bloc : `e12b8745d5fcff24ad40b75381fece0976200e42c48e5125ff248053b61da78b`.

~~~~text
### Requirement: Reprise persistante sans perte

Délais, points de reprise et états survivent au redémarrage via persistance déclarée ; aucune donnée nécessaire à la reprise MUST NOT dépendre de la mémoire locale.

#### Scenario: Redémarrage avec reprise

- **WHEN** un processus s'interrompt pendant une instance
- **THEN** l'instance reprend à son point persistant sans rejouer un effet confirmé
~~~~

