# internationalization Specification

## Purpose
Le multilinguisme natif externalise les textes par composant avec catalogues versionnés, sans dépendre de la langue de l'environnement de construction.

## Requirements

### Requirement: Catalogues par composant et langue canonique

Chaque texte utilisateur MUST être externalisé dans le catalogue du composant propriétaire avec langue canonique anglaise complète ; doublons, clés manquantes et paramètres incohérents sont refusés au build.

#### Scenario: Clé manquante bloquée

- **WHEN** une langue déclare une clé absente du canon ou un paramètre divergent
- **THEN** le build refuse la composition ou produit un diagnostic de repli autorisé

### Requirement: Résolution déterministe et formats localisés

Le système MUST respecter les garanties suivantes.

La résolution SUIT préférence utilisateur, périmètre applicable, préférence navigateur, puis défaut d'installation ; dates en UTC sérialisé, précision conservée, affichage localisé sans altérer la valeur métier.

#### Scenario: Valeur métier préservée

- **WHEN** un montant ou un instant est affiché dans une langue donnée
- **THEN** la valeur transmise à l'interface reste exacte et sérialisée en UTC

#### Scenario: Préférence navigateur avant défaut d'installation

- **WHEN** aucune préférence utilisateur ni de périmètre n'est définie, le navigateur demande le français supporté et le défaut d'installation est l'anglais
- **THEN** la locale française est retenue avant le défaut anglais de l'installation
