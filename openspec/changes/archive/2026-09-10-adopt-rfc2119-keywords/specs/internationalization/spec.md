## MODIFIED Requirements

### Requirement: Catalogues par composant et langue canonique

Chaque texte utilisateur MUST être externalisé dans le catalogue du composant propriétaire avec langue canonique anglaise complète ; doublons, clés manquantes et paramètres incohérents sont refusés au build.

#### Scenario: Clé manquante bloquée

- **WHEN** une langue déclare une clé absente du canon ou un paramètre divergent
- **THEN** le build refuse la composition ou produit un diagnostic de repli autorisé

### Requirement: Résolution déterministe et formats localisés

Le système MUST respecter les garanties suivantes.

La résolution SUIT préférence utilisateur, périmètre applicable, puis défaut d'installation ; dates en UTC sérialisé, précision conservée, affichage localisé sans altérer la valeur métier.

#### Scenario: Valeur métier préservée

- **WHEN** un montant ou un instant est affiché dans une langue donnée
- **THEN** la valeur transmise à l'interface reste exacte et sérialisée en UTC
