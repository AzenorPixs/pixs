## MODIFIED Requirements

### Requirement: Lien structurel préparatoire BulkTenantLink v1

BulkTenantLink v1 MUST être une représentation interne Python, immuable
et purement mémoire comportant exactement operation_id et tenant_context_reference.
Les deux champs MUST être fournis explicitement sans valeur par défaut.

#### Scenario: Deux références explicites conservées

- **WHEN** un appelant de confiance fournit les deux références conformes
- **THEN** le profil conserve exactement ces valeurs sans effet ni champ supplémentaire

### Requirement: Références opaques de BulkTenantLink v1

operation_id et tenant_context_reference MUST être des str exactes non vides,
opaques et sans normalisation. Elles MAY être égales dans ce profil.
Tout autre type, conversion, interprétation, alias ou valeur de repli MUST NOT
être admis ; aucune existence de référence n'est établie.

#### Scenario: Références égales admises sans résolution

- **WHEN** les deux références sont des str exactes non vides et égales
- **THEN** la structure est acceptée sans résolution ni garantie de contexte tenant

### Requirement: Validation pure de BulkTenantLink v1

La validation MUST refuser tout candidat étranger ou dérivé avant tout accès
à ses attributs, puis contrôler les types exacts avant toute opération sur
les valeurs. Elle MUST produire des diagnostics statiques VALIDATE, triés
et dédupliqués, sans écho des valeurs ni comportement étranger.

#### Scenario: Champ interdit refusé sans effet

- **WHEN** une référence est absente, vide ou de type interdit, ou le candidat est étranger ou dérivé
- **THEN** des diagnostics statiques sont produits sans effet ni écho des valeurs

### Requirement: Limites du profil BulkTenantLink v1

Le profil MUST NOT résoudre une référence, effectuer une entrée/sortie,
établir un rattachement réel, un contexte PLATFORM, une légitimité, une
cohérence tenant/scope, une autorisation, une propagation ou une persistance.
Les exigences générales bulk et d'isolation tenant MUST rester applicables.

#### Scenario: Aucun rattachement tenant déduit

- **WHEN** les deux références sont structurellement acceptées
- **THEN** aucun TenantContext effectif, contexte global ou droit d'accès n'est établi
