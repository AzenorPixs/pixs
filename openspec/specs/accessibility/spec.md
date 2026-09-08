# accessibility Specification

## Purpose
L'accessibilité garantit que le shell, les primitives et les interfaces des modules sont utilisables au clavier, avec les technologies d'assistance et au niveau cible WCAG 2.2 AA.

## Requirements

### Requirement: Niveau cible WCAG 2.2 AA

Le shell et les primitives du design system DOIVENT satisfaire WCAG 2.2 AA ; les interfaces des modules DOIVENT rester conformes au niveau cible sans régression introduite par une contribution.

#### Scenario: Contribution non conforme

- **WHEN** une contribution frontend échoue à un critère du niveau cible
- **THEN** elle ne peut pas être publiée comme stable et l'écart est documenté

### Requirement: Fonctionnement clavier et technologies d'assistance

Tous les éléments interactifs DOIVENT fonctionner au clavier avec ordre de tabulation et gestion du focus cohérents, et rester utilisables avec les technologies d'assistance.

#### Scenario: Parcours clavier complet

- **WHEN** un utilisateur réalise un parcours métier sans souris
- **THEN** chaque action reste atteignable, le focus est visible et aucun piège de clavier n'apparaît

### Requirement: Sémantique native préservée

Les éléments HTML natifs DOIVENT être préférés ; ARIA NE DOIT PAS recréer ni contredire une sémantique native, et chaque composant DOIT exposer un nom accessible, des rôles et des états documentés.

#### Scenario: Rôle ARIA redondant

- **WHEN** un composant applique un rôle ARIA équivalent à la sémantique native déjà présente
- **THEN** le contrôle de conformité signale la violation avant publication

### Requirement: Validation outillée et manuelle combinées

L'automatisation DOIT détecter une partie des défauts, mais la validation DOIT inclure des parcours manuels au clavier et avec des technologies d'assistance ; les messages d'erreur, contrastes, comportement au zoom et réduction des mouvements DOIVENT être vérifiés.

#### Scenario: Défaut non détectable automatiquement

- **WHEN** un défaut de libellé accessible échappe à la détection automatisée
- **THEN** le parcours manuel de validation l'identifie et bloque la publication stable de la primitive concernée
