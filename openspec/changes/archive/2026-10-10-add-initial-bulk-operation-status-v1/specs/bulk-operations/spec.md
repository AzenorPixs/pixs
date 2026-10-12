## MODIFIED Requirements

### Requirement: Profil structurel préparatoire BulkOperationStatus v1

BulkOperationStatus v1 MUST être une représentation interne Python, immuable et
purement mémoire comportant exactement operation_id et status. Les deux champs
MUST être fournis explicitement sans valeur par défaut.

#### Scenario: Statut explicitement fourni

- **WHEN** un appelant de confiance ou une fixture synthétique fournit les deux champs conformes
- **THEN** la représentation conserve exactement ces valeurs sans effet ni champ supplémentaire

### Requirement: Référence et état du profil BulkOperationStatus v1

operation_id MUST être une str exacte non vide, opaque et sans normalisation.
status MUST être un membre de type exact BulkOperationState, limité aux dix valeurs
du vocabulaire structurel BulkOperationState v1 ; toute chaîne, conversion,
substitution ou valeur par défaut MUST NOT être admise.

#### Scenario: Chaque état du vocabulaire est représentable

- **WHEN** status est l'un des dix membres de type exact BulkOperationState et operation_id est une str exacte non vide
- **THEN** le profil est structurellement accepté sans interpréter l'état ni établir son rattachement réel

#### Scenario: Chaîne d'état refusée

- **WHEN** status est la chaîne RUNNING au lieu du membre RUNNING de BulkOperationState
- **THEN** la validation refuse le profil sans convertir la chaîne ni invoquer un comportement étranger

### Requirement: Validation pure et limites de BulkOperationStatus v1

La validation MUST refuser tout objet de type étranger au profil avant d'accéder à
ses attributs, puis vérifier les types des champs avant toute comparaison. Elle
MUST produire des diagnostics statiques VALIDATE triés et dédupliqués, sans écho
des valeurs ni invocation de comportement étranger. Elle MUST NOT effectuer
d'entrée/sortie, résoudre une référence, prouver une existence ou une autorisation,
rattacher des Jobs, persister, décider une transition, un ordre ou une terminalité,
mesurer une progression ni exécuter un import/export. Les exigences générales
BulkOperation restent intégralement applicables ; ce profil ne constitue pas leur
implémentation complète.

#### Scenario: Objet étranger refusé avant ses hooks

- **WHEN** le candidat est d'un type étranger, y compris un sous-type du profil
- **THEN** la validation produit un diagnostic statique sans accéder à ses attributs ni produire d'effet
