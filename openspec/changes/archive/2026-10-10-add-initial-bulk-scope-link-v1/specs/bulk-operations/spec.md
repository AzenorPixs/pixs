## MODIFIED Requirements

### Requirement: Profil structurel préparatoire BulkScopeLink v1

BulkScopeLink v1 MUST être une représentation interne Python, immuable et purement mémoire
comportant exactement operation_id et scope_context_reference, fournis explicitement sans
valeur par défaut. Chaque champ MUST être une str exacte non vide, opaque et sans
normalisation. Le profil MUST NOT imposer que ces deux références soient différentes.

#### Scenario: Références explicites conservées

- **WHEN** un appelant de confiance fournit les deux références conformes, y compris deux chaînes identiques
- **THEN** la représentation conserve exactement ces valeurs sans diagnostic ni effet

### Requirement: Validation pure de BulkScopeLink v1

La validation MUST refuser tout candidat de type étranger ou dérivé avant accès à ses
attributs et contrôler les types exacts des champs avant toute autre opération sur leurs
valeurs. Elle MUST produire des diagnostics statiques VALIDATE triés et dédupliqués,
sans écho des valeurs ni invocation de comportement d'objet étranger.

#### Scenario: Structure interdite refusée sans effet

- **WHEN** le candidat est étranger ou dérivé, ou une référence est absente, vide ou n'est pas une str exacte
- **THEN** des diagnostics statiques sont produits sans effet ni écho des valeurs

### Requirement: Limites du lien de périmètre BulkScopeLink v1

Le profil MUST NOT résoudre une référence, prouver existence, rattachement réel,
cohérence tenant/scope, autorisation, propagation ou persistance, ni importer un contexte
concret de pixs.core. Une référence absente MUST NOT désigner PLATFORM ou un tenant global.
Les contrats généraux bulk et ScopeContext MUST rester intégralement applicables.

#### Scenario: Aucune garantie de périmètre déduite

- **WHEN** les deux références sont structurellement acceptées
- **THEN** aucune identité, autorisation, cohérence ou association effective de contexte n'est établie
