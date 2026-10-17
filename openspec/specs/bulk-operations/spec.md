# bulk-operations Specification

## Purpose
Les opérations en masse exécutent imports et exports volumineux via un contrat versionné, suivi et gouverné, sans contourner commandes, autorisation ni périmètre.

## Requirements

### Requirement: Contrat BulkOperation suivi par operation_id

Chaque opération MUST suivre un contrat versionné avec variantes IMPORT et EXPORT, états, rattachement à operation_id, travaux persistants, tenant et scope ; les formats de référence sont CSV et NDJSON, tout autre format via adaptateur déclaré.

#### Scenario: Suivi distinct des travaux

- **WHEN** une opération longue dépasse le seuil synchrone
- **THEN** elle retourne un operation_id suivi, distinct des identifiants des travaux qui l'exécutent

### Requirement: Import via staging privé et commandes propriétaires

Tout import MUST passer par un espace privé, vérifier taille, type, somme de contrôle et mapping versionné, puis appeler exclusivement les commandes du module propriétaire avec modes VALIDATE_ONLY, ATOMIC, ATOMIC_PER_CHUNK ou BEST_EFFORT explicites ; les conflits sont rejetés par défaut.

#### Scenario: Ligne en conflit rejetée

- **WHEN** une ligne contredit la stratégie de conflit déclarée
- **THEN** elle est rejetée dans un rapport versionné sans mutation partielle silencieuse

### Requirement: Export filtré, gouverné et révocable

Tout export MUST appliquer l'autorisation et le filtrage autorisé à la source, utiliser projections et champs déclarés avec instantané ou filigrane, produire fichier privé temporaire et manifeste, avec expiration, révocation, audit et échec fermé si la gouvernance est irrésolue.

#### Scenario: Export hors périmètre refusé

- **WHEN** un export dépasse le tenant ou le scope autorisé
- **THEN** il est refusé avant toute lecture, avec un audit

### Requirement: Vocabulaire structurel BulkOperationState v1

Le profil structurel préparatoire BulkOperationState v1 MUST utiliser exactement les
dix noms d'états suivants : REQUESTED, STAGED, VALIDATING, READY, RUNNING, COMPLETED,
COMPLETED_WITH_ERRORS, FAILED, CANCELLED, EXPIRED ; tout autre nom MUST NOT être admis
dans ce vocabulaire.

#### Scenario: Acceptation dans le profil v1

- **WHEN** une représentation structurelle déclare un des dix noms d'états
- **THEN** elle est acceptée comme nom du profil BulkOperationState v1, sans décision
  de transition, d'ordre, de terminalité, de rattachement à un Job ou d'effet d'import,
  d'export ou de persistance

#### Scenario: Refus d'un nom hors v1

- **WHEN** un nom d'état sort des dix valeurs déclarées
- **THEN** il est refusé sans alias, substitution ni défaut implicite

### Requirement: Vocabulaire structurel BulkConflictStrategy v1

Le profil structurel préparatoire BulkConflictStrategy v1 MUST utiliser exactement les
quatre noms de stratégie de conflit suivants : REJECT, CREATE_ONLY, UPDATE_ONLY, UPSERT ;
tout autre nom MUST NOT être admis dans ce vocabulaire.

#### Scenario: Acceptation dans le profil v1

- **WHEN** une représentation structurelle déclare un des quatre noms de stratégie
- **THEN** elle est acceptée comme nom du profil BulkConflictStrategy v1, sans choix
  de stratégie, sans résolution de conflit, sans décision de mutation, d'import,
  d'idempotence, de permission ou de persistance

#### Scenario: Refus d'un nom hors v1

- **WHEN** un nom de stratégie sort des quatre valeurs déclarées
- **THEN** il est refusé sans alias, substitution ni défaut implicite

### Requirement: Profil structurel préparatoire BulkJobLink v1

BulkJobLink v1 MUST être une représentation interne, immuable et purement mémoire
comportant exactement operation_id et job_id, tous deux fournis explicitement sans
valeur par défaut. Chaque champ MUST être une str exacte non vide, opaque et sans
normalisation ; operation_id et job_id MUST être distincts dans cette représentation.

#### Scenario: Lien structurel valide

- **WHEN** un appelant de confiance ou une fixture synthétique fournit deux références de type str exact, non vides et distinctes
- **THEN** la représentation conserve exactement ces références sans produire de diagnostic ni effet

### Requirement: Validation pure et limites de BulkJobLink v1

La validation de BulkJobLink v1 MUST porter uniquement sur son type exact et les
deux références déclarées, en contrôlant les types avant toute comparaison. Elle
MUST produire des diagnostics statiques VALIDATE, triés et dédupliqués, sans
reproduire les valeurs ni invoquer les comportements d'un objet étranger.
Elle MUST NOT résoudre une référence, effectuer une entrée/sortie, ni établir
l'existence, la légitimité, l'autorisation, la cardinalité globale, l'unicité globale,
la corrélation, la causalité, le périmètre, la déduplication ou la persistance.
Les exigences générales BulkOperation et Jobs restent intégralement applicables ;
ce profil ne constitue pas leur implémentation complète.

#### Scenario: Lien structurel invalide refusé

- **WHEN** la représentation est d'un type étranger, un champ n'est pas une str exacte non vide, ou les deux références sont égales
- **THEN** la validation produit des diagnostics statiques sans écho des valeurs, effet ni garantie runtime

### Requirement: Entête structurel préparatoire BulkOperationHeader v1

BulkOperationHeader v1 MUST être une représentation interne Python, immuable et purement mémoire
comportant exactement operation_id, bulk_type et bulk_version. Les trois champs MUST être
fournis explicitement, sans valeur par défaut.

#### Scenario: Entête explicite sans effet

- **WHEN** un appelant de confiance ou une fixture synthétique fournit les trois champs conformes au profil
- **THEN** la représentation conserve exactement ces valeurs sans effet ni champ supplémentaire

### Requirement: Référence et variante du profil BulkOperationHeader v1

operation_id MUST être une str exacte non vide, opaque et sans normalisation ; ce contrôle
MUST NOT imposer ni prouver un format UUID. bulk_type MUST être un membre de type exact
BulkOperationVariant, limité aux variantes IMPORT et EXPORT ; une chaîne, un autre type,
une conversion implicite, un alias ou un défaut MUST NOT être admis.

#### Scenario: Type de variante étranger refusé

- **WHEN** bulk_type est la chaîne IMPORT ou un objet étranger au lieu du membre IMPORT de BulkOperationVariant
- **THEN** le profil est refusé sans conversion ni comportement d'objet étranger

### Requirement: Version du profil BulkOperationHeader v1

bulk_version MUST être une str exacte au format SemVer 2.0.0 complet, préversion et
métadonnées de build admises conformément à component-model et dependencies, sans
normalisation. Cette validation de forme MUST NOT décider une compatibilité de contrats.

#### Scenario: Version complète conservée

- **WHEN** bulk_version vaut 1.2.3-rc.1+build.7
- **THEN** cette version structurellement valide est conservée telle quelle sans décision de compatibilité

#### Scenario: Version malformée refusée

- **WHEN** bulk_version vaut 1, est vide ou possède un type autre que str exact
- **THEN** le profil est refusé sans version de repli ni écho de la valeur

### Requirement: Validation pure et limites de BulkOperationHeader v1

La validation MUST refuser un objet de type étranger au profil avant tout accès à ses
attributs, puis contrôler les types des champs avant parsing ou comparaison. Elle MUST
produire des diagnostics statiques VALIDATE triés et dédupliqués, sans écho des valeurs
ni invocation de comportement étranger. Elle MUST NOT effectuer d'entrée/sortie, résoudre
des références, prouver existence ou autorisation, persister, rattacher des Jobs, évaluer
une compatibilité, exécuter un import/export ou remplacer les exigences générales BulkOperation.

#### Scenario: Structure invalide diagnostiquée sans effet

- **WHEN** le profil, une référence, une variante ou une version a une structure interdite
- **THEN** des diagnostics statiques sont produits sans effet ni garantie runtime

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

### Requirement: Profil structurel préparatoire BulkOperationFormat v1

BulkOperationFormat v1 MUST être une représentation interne Python, immuable
et purement mémoire comportant exactement operation_id et format. Les deux
champs MUST être fournis explicitement sans valeur par défaut.

#### Scenario: Deux champs explicites conservés

- **WHEN** un appelant de confiance fournit une référence conforme et le membre canonique CSV ou NDJSON de BulkReferenceFormat
- **THEN** la représentation conserve exactement ces deux valeurs sans effet ni champ supplémentaire

### Requirement: Référence et format de BulkOperationFormat v1

operation_id MUST être une str exacte non vide, opaque et sans normalisation.
format MUST être l'un des membres canoniques de type exact BulkReferenceFormat :
CSV ou NDJSON. Toute chaîne, instance fabriquée hors membres canoniques, autre type,
conversion implicite, alias ou valeur de repli MUST NOT être admis.

#### Scenario: Format non canonique refusé

- **WHEN** format est une chaîne CSV, une instance fabriquée hors membres canoniques ou un objet de type étranger
- **THEN** le profil est refusé sans conversion ni comportement d'objet étranger

### Requirement: Validation pure de BulkOperationFormat v1

La validation MUST refuser tout candidat étranger ou dérivé avant tout accès
à ses attributs, puis contrôler les types exacts des champs avant toute autre
opération sur leurs valeurs. Elle MUST produire des diagnostics statiques VALIDATE,
triés et dédupliqués, sans écho des valeurs ni invocation de comportement étranger.

#### Scenario: Structure interdite diagnostiquée sans effet

- **WHEN** une référence est absente, vide ou n'est pas une str exacte, ou le candidat ou son format est interdit
- **THEN** des diagnostics statiques sont produits sans effet ni écho des valeurs

### Requirement: Limites du profil BulkOperationFormat v1

Le profil MUST NOT résoudre une référence, effectuer d'entrée/sortie, choisir
ou convertir un format, parser un fichier, activer ou résoudre un adaptateur,
prouver validité du contenu, encodage, mapping, compatibilité, autorisation ou
persistance, ni exécuter un import/export. Les exigences générales bulk et les
formats étendus via adaptateur déclaré MUST rester intégralement applicables.

#### Scenario: Aucune validation réelle de fichier déduite

- **WHEN** les deux champs sont structurellement acceptés
- **THEN** aucune validité de fichier, compatibilité, autorisation ou persistance n'est établie

### Requirement: Profil structurel préparatoire BulkOperationConflict v1

BulkOperationConflict v1 MUST être une représentation interne Python, immuable
et purement mémoire comportant exactement operation_id et conflict_strategy.
Les deux champs MUST être fournis explicitement sans valeur par défaut.

#### Scenario: Deux champs explicites conservés

- **WHEN** un appelant de confiance fournit une référence conforme et un membre canonique de BulkConflictStrategy
- **THEN** la représentation conserve exactement ces deux valeurs sans effet ni champ supplémentaire

### Requirement: Référence et stratégie de BulkOperationConflict v1

operation_id MUST être une str exacte non vide, opaque et sans normalisation.
conflict_strategy MUST être un membre canonique de type exact BulkConflictStrategy :
REJECT, CREATE_ONLY, UPDATE_ONLY ou UPSERT. Toute chaîne, instance fabriquée hors
membres canoniques, autre type, conversion, alias ou valeur de repli MUST NOT être admis.

#### Scenario: Stratégie non canonique refusée

- **WHEN** conflict_strategy est une chaîne REJECT, une instance fabriquée hors membres canoniques ou un objet de type étranger
- **THEN** le profil est refusé sans conversion ni comportement d'objet étranger

### Requirement: Validation pure de BulkOperationConflict v1

La validation MUST refuser tout candidat étranger ou dérivé avant tout accès
à ses attributs, puis contrôler les types exacts des champs avant toute autre
opération sur leurs valeurs. Elle MUST produire des diagnostics statiques VALIDATE,
triés et dédupliqués, sans écho des valeurs ni invocation de comportement étranger.

#### Scenario: Structure interdite diagnostiquée sans effet

- **WHEN** une référence est absente, vide ou n'est pas une str exacte, ou le candidat ou sa stratégie est interdit
- **THEN** des diagnostics statiques sont produits sans effet ni écho des valeurs

### Requirement: Limites du profil BulkOperationConflict v1

Le profil MUST NOT résoudre une référence ou un conflit, choisir ou appliquer
une stratégie, effectuer d'entrée/sortie, décider une mutation, une idempotence
ou une autorisation, persister, appeler une commande ni exécuter un import/export.
Les exigences générales bulk, dont le rejet des conflits par défaut dans le
contrat d'import, MUST rester intégralement applicables.

#### Scenario: Aucune résolution de conflit déduite

- **WHEN** les deux champs sont structurellement acceptés
- **THEN** aucune résolution de conflit, mutation, idempotence, autorisation ou persistance n'est établie

### Requirement: Profil structurel préparatoire BulkOperationCommitMode v1

BulkOperationCommitMode v1 MUST être une représentation interne Python,
immuable et purement mémoire comportant exactement operation_id et commit_mode.
Les deux champs MUST être fournis explicitement sans valeur par défaut.

#### Scenario: Deux champs explicites conservés

- **WHEN** un appelant de confiance fournit une référence conforme et un membre canonique de BulkCommitMode
- **THEN** la représentation conserve exactement ces valeurs sans effet ni champ supplémentaire

### Requirement: Référence et mode de BulkOperationCommitMode v1

operation_id MUST être une str exacte non vide, opaque et sans normalisation.
commit_mode MUST être un membre canonique de type exact BulkCommitMode :
VALIDATE_ONLY, ATOMIC, ATOMIC_PER_CHUNK ou BEST_EFFORT. Toute chaîne, instance
fabriquée hors membres canoniques, autre type, conversion, alias ou valeur de
repli MUST NOT être admis.

#### Scenario: Mode non canonique refusé

- **WHEN** commit_mode est une chaîne, une instance fabriquée hors membres canoniques ou un objet étranger
- **THEN** le profil est refusé sans conversion ni comportement d'objet étranger

### Requirement: Validation pure de BulkOperationCommitMode v1

La validation MUST refuser tout candidat étranger ou dérivé avant tout accès
à ses attributs, puis contrôler les types exacts des champs avant toute autre
opération sur leurs valeurs. Elle MUST produire des diagnostics statiques VALIDATE,
triés et dédupliqués, sans écho des valeurs ni invocation de comportement étranger.

#### Scenario: Structure interdite diagnostiquée sans effet

- **WHEN** une référence est absente, vide ou de type interdit, ou le candidat ou son mode n'est pas canonique
- **THEN** des diagnostics statiques sont produits sans effet ni écho des valeurs

### Requirement: Limites du profil BulkOperationCommitMode v1

Le profil MUST NOT résoudre une référence, choisir ou appliquer un mode,
effectuer une entrée/sortie, une transaction, une mutation, un découpage,
un staging, une autorisation, une persistance ou un import/export.
Les exigences générales bulk MUST rester intégralement applicables.

#### Scenario: Aucune transaction déduite

- **WHEN** les deux champs sont structurellement acceptés
- **THEN** aucun comportement transactionnel, découpage, mutation, autorisation ou persistance n'est établi

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

### Requirement: Valeurs préparatoires de persistance BulkOperationRecord v1

Le profil MUST utiliser un dict exact avec exactement les neuf clés operation_id, bulk_type, bulk_version, status, tenant_context_reference, scope_context_reference, format, conflict_strategy et commit_mode. Toutes les clés MUST être fournies explicitement, y compris celles dont la valeur est None. Le profil MUST NOT ajouter de valeur par défaut.

#### Scenario: Neuf valeurs explicitement fournies

- **WHEN** un producteur de confiance fournit exactement les neuf clés conformes
- **THEN** le profil conserve les valeurs sans ajout, omission ni défaut

### Requirement: Références du profil BulkOperationRecord v1

operation_id et tenant_context_reference MUST être des str exactes non vides et opaques. scope_context_reference MUST être None explicite ou une str exacte non vide et opaque. Les références MAY être égales. La validation MUST NOT normaliser, convertir ou résoudre leurs valeurs ; None MUST NOT désigner PLATFORM ou un tenant global.

#### Scenario: Scope explicitement absent

- **WHEN** scope_context_reference vaut None et les autres références sont conformes
- **THEN** la structure accepte cette absence explicite sans contexte global ni résolution

### Requirement: Version du profil BulkOperationRecord v1

bulk_version MUST être une str exacte représentant une version SemVer 2.0.0 complète, validée par parse_version existant après contrôle du type exact. Le profil MUST NOT choisir une version par défaut, décider une compatibilité ou créer une autre grammaire.

#### Scenario: Version non conforme refusée

- **WHEN** bulk_version ne respecte pas le type ou la syntaxe déclarés
- **THEN** la validation refuse la valeur sans la reproduire ni la convertir

### Requirement: Valeurs stockées des enums de BulkOperationRecord v1

bulk_type, status et format MUST être des str exactes égales aux values des membres canoniques respectifs BulkOperationVariant, BulkOperationState et BulkReferenceFormat. conflict_strategy et commit_mode MUST être None explicite ou des str exactes égales aux values des membres canoniques BulkConflictStrategy et BulkCommitMode. Alias, instances Enum, sous-types et conversions implicites MUST NOT être admis.

#### Scenario: Enum déjà construit distinct de sa valeur stockée

- **WHEN** une valeur de champ est une instance Enum au lieu de la str canonique attendue
- **THEN** le profil de stockage la refuse ; les profils Kernel à membres Enum restent inchangés

### Requirement: Validation pure des valeurs BulkOperationRecord v1

validate_bulk_operation_record_values MUST refuser le candidat non dict exact, contrôler les types exacts des clés puis des valeurs avant leur utilisation et refuser clés manquantes ou inconnues. Cette fonction MUST retourner une liste fraîche de Diagnostic VALIDATE statiques, triés et dédupliqués, sans écho de valeur ni comportement étranger. Elle MUST NOT modifier le dict ni effectuer une entrée/sortie.

#### Scenario: Mapping hostile ou incomplet refusé

- **WHEN** le mapping, une clé ou une valeur est interdit, ou une clé est manquante ou inconnue
- **THEN** les diagnostics sont statiques et la validation ne produit aucun effet

### Requirement: Modèle préparatoire BulkOperationRecord v1

Le modèle Django interne BulkOperationRecord MUST persister exactement ces neuf champs textuels, avec operation_id comme clé primaire locale à sa table et sans clé étrangère. Seuls scope_context_reference, conflict_strategy et commit_mode MUST admettre NULL. Le modèle MUST NOT fournir de défaut métier. Les producteurs MUST valider le mapping explicite avant construction ou écriture.

#### Scenario: Persistance de valeurs explicitement validées

- **WHEN** un producteur de confiance construit puis persiste un enregistrement issu des neuf valeurs conformes
- **THEN** les colonnes conservent ces valeurs et NULL explicites sans résolution de référence

### Requirement: Validation ORM explicite de BulkOperationRecord v1

BulkOperationRecord.from_values MUST valider le dict explicite avant construction et retourner une instance non sauvegardée. full_clean MUST valider les neuf attributs avant conversion ORM, même avec exclude ; les refus MUST utiliser des ValidationError statiques sans valeurs. save MUST NOT appeler full_clean implicitement. Ces chemins MUST NOT être présentés comme des contrôles d’autorisation.

#### Scenario: Valeur Python interdite avant conversion ORM

- **WHEN** from_values ou full_clean reçoit une valeur Python non conforme au profil
- **THEN** une ValidationError statique est levée avant conversion ou écriture

### Requirement: Contraintes persistantes de BulkOperationRecord v1

La base MUST imposer non-vacuité des textes obligatoires, appartenance des enums stockés, non-vacuité de scope_context_reference lorsqu’il est non NULL et unicité de la clé primaire dans cette table. La syntaxe SemVer et les types Python exacts MUST rester des contrôles applicatifs explicites ; les contraintes DB MUST NOT être présentées comme leur preuve.

#### Scenario: Insertion SQL structurellement interdite

- **WHEN** une insertion de test autorisée viole une contrainte persistante déclarée
- **THEN** la base refuse l’insertion sans accepter un enregistrement partiellement conforme

### Requirement: Limites du socle BulkOperationRecord v1

Ce socle MUST NOT être présenté comme le contrat BulkOperation complet, une identité de tenant vérifiée, une autorisation, une transition, un worker, un bail, une politique de réessai, une idempotence, une association Job, un staging ou un import/export. Il MUST NOT imposer d’applicabilité des modes selon la variante. Les exigences générales bulk et les formats étendus déclarés MUST rester applicables.

#### Scenario: Aucune exécution ni autorité déduite de la ligne

- **WHEN** un enregistrement préparatoire est stocké
- **THEN** aucun effet métier, contexte autorisé, reprise ou succès d’opération Bulk n’est établi

### Requirement: Runtime Bulk v1 B01 — Périmètre exécutable

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B01 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Admission avant suivi

- **WHEN** une demande IMPORT CSV conforme est admise
- **THEN** l’opération, la demande, le premier Job et la liaison sont engagés avant le retour de operation_id

#### Scenario: Format non pris en charge

- **WHEN** le runtime v1 reçoit un format autre que CSV ou NDJSON
- **THEN** il refuse cette capacité sans fallback ni retrait de l’extensibilité générale

### Requirement: Runtime Bulk v1 B02 — Enveloppe et progression

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B02 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Données explicites

- **WHEN** le producteur serveur fournit toutes les valeurs conformes et leurs None explicites
- **THEN** les valeurs et la révision sont conservées sans coercition ni défaut de modèle

#### Scenario: Valeur étrangère

- **WHEN** un champ est omis, inconnu ou possède un type étranger
- **THEN** la validation refuse avant comportement, parsing ou I/O et sans écho de valeur

### Requirement: Runtime Bulk v1 B03 — Ports serveur et autorité

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B03 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Autorité effective

- **WHEN** Django résout une décision effective ALLOW dans le tenant et périmètre autorisés
- **THEN** le runtime utilise le contexte serveur sans transférer de credentials ni exception

#### Scenario: Autorité indisponible

- **WHEN** le port retourne DENY ou UNAVAILABLE après application des règles canoniques
- **THEN** aucune action demandée n’est exécutée et aucun contexte exploitable n’est fourni

### Requirement: Résolution de gouvernance GovernanceResolutionV1 fermée

La réponse GovernanceResolutionV1 MUST respecter les six clés, types, décisions et garanties de l'annexe correspondante, avec résolution effective et capture immuable. Une validation structurelle seule MUST NOT établir cette résolution.

#### Scenario: Résolution positive

- **WHEN** le port composé résout effectivement politique, classification et obligations pour l'autorité courante
- **THEN** la résolution est RESOLVED avec contexte serveur lié, politique, profil et obligations explicites capturés immuables

#### Scenario: Refus fermé

- **WHEN** la gouvernance refuse pour l'autorité courante
- **THEN** la résolution est DENY avec resolved_context, policy, profile et obligations à None, sans contexte exploitable ni repli

#### Scenario: Indisponible ou exception

- **WHEN** le port composé est indisponible ou lève une exception
- **THEN** la résolution est UNAVAILABLE avec les quatre données résolues à None, sans détail brut ni transfert d'exception

#### Scenario: Structure ou type étranger refusé

- **WHEN** une clé manque ou est inconnue, ou le candidat, une clé ou une valeur n'a pas le type exact attendu
- **THEN** la résolution est refusée avant comportement, parsing ou I/O, sans écho de valeur ni invocation étrangère

#### Scenario: Obligations non résolues

- **WHEN** les obligations ne sont pas effectivement résolues en tuple exact
- **THEN** aucune lecture, transfert ou mutation n'est autorisée ; un tuple vide exige une absence explicitement résolue, jamais un défaut

#### Scenario: Contexte divergent refusé

- **WHEN** le contexte résolu ne correspond pas au sujet, tenant, périmètre et contexte de l'autorité courante
- **THEN** la résolution est refusée sans repli ni contexte exploitable

### Requirement: Runtime Bulk v1 B05 — Parsing et mapping

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B05 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Mapping déclaré

- **WHEN** un fichier conforme utilise un mapping propriétaire immuable et versionné
- **THEN** seuls les champs déclarés sont transmis au contrat public sans conversion heuristique

#### Scenario: Entrée ambiguë

- **WHEN** un CSV contient un header dupliqué ou un NDJSON une clé dupliquée
- **THEN** le parsing refuse l’entrée et produit un diagnostic statique sans contenu brut

### Requirement: Runtime Bulk v1 B06 — Machine à états

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B06 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Transition permise

- **WHEN** une opération non terminale franchit une étape autorisée par la matrice
- **THEN** la transition et sa révision sont persistées avec la preuve de l’étape

#### Scenario: Terminalité conservée

- **WHEN** une demande tente de passer de COMPLETED à RUNNING
- **THEN** la transition est refusée sans réinitialiser progression, checkpoint ou échéance

#### Scenario: Demande d’annulation autorisée sans terminalisation

- **WHEN** une autorité serveur courante autorise CANCEL sur une opération non terminale avec la révision attendue courante
- **THEN** la demande persiste uniquement cancellation_requested et la révision suivante, sans changer progression, checkpoint, échéance, Job ou schedule et sans prétendre annuler une unité déjà engagée

#### Scenario: Demande refusée sans altération concurrente

- **WHEN** l’autorité CANCEL refuse ou reste indisponible, ou que la primitive refuse une opération terminale ou une révision périmée
- **THEN** la demande est refusée sans altérer l’opération ni ses effets engagés, et aucune requête SQL Bulk ne précède l’autorisation serveur

#### Scenario: Transition d’annulation serveur autorisée et coopérative

- **WHEN** une autorité serveur courante autorise CANCEL pour une opération non terminale dont le flag cancellation_requested est True et la révision attendue courante
- **THEN** la transition persiste uniquement CANCELLED et la révision suivante sous les verrous et la matrice canoniques, conserve les effets déjà engagés et tous les autres champs, et interdit de nouvelles unités protégées

#### Scenario: Transition d’annulation refusée sans altération

- **WHEN** l’autorité CANCEL refuse ou reste indisponible, le flag n’est pas True, la révision est périmée ou l’opération est terminale
- **THEN** la transition est refusée sans altération de l’opération ni de ses effets, aucune requête SQL Bulk ne précède l’autorité serveur et aucun retry ou rebase automatique n’est réalisé

### Requirement: Runtime Bulk v1 B07 — Modes et conflits

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B07 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Unité engagée

- **WHEN** un import autorisé applique un mode supporté par le propriétaire
- **THEN** ses engagements, rejets et checkpoints respectent les garanties propres à ce mode

#### Scenario: Garantie absente

- **WHEN** un module ne garantit pas la transaction requise pour ATOMIC
- **THEN** le mode est refusé avant mutation sans fallback vers BEST_EFFORT

#### Scenario: Validation seule après flux complet prouvé

- **WHEN** un import VALIDATE_ONLY présente un flux qualifié complet avec intégrité vérifiée et fermeture réussie avant tout appel propriétaire
- **THEN** le rapport, la progression et le checkpoint finaux sont établis sous gardes actuelles avec applied_rows à zéro et sans exécution propriétaire

#### Scenario: Interruption sans validation complète prétendue

- **WHEN** une limite, une annulation ou une perte de bail interrompt la validation
- **THEN** aucune validation complète ni mutation ni persistance forcée n'est prétendue et l'état reste explicite à réconcilier

#### Scenario: Chunk ATOMIC_PER_CHUNK REJECT engagé sans rejou

- **WHEN** une opération IMPORT ATOMIC_PER_CHUNK REJECT à validation complète prouvée applique un chunk sous autorité EXECUTE et gouvernance RESOLVED actuelles, avec participation propriétaire PostgreSQL déclarée au même alias et unité protégée même thread et même transaction
- **THEN** le chunk est engagé avec checkpoint et outbox requise dans la même transaction, les chunks déjà engagés sont conservés, aucun rejou n'est compté comme nouvel effet et un rejet propriétaire ou conflit REJECT annule le chunk courant entier sans mutation partielle

### Requirement: Runtime Bulk v1 B12 — Export et résultats

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B12 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Résultat gouverné

- **WHEN** une projection propriétaire autorisée fournit sa consistance déclarée
- **THEN** un objet privé et un manifeste complet sont engagés avant disponibilité du résultat

#### Scenario: Résultat non résolu

- **WHEN** la consistance, la gouvernance ou l’autorisation du résultat ne peut être résolue
- **THEN** l’action concernée est refusée sans présentation d’un export complet

### Requirement: Runtime Bulk v1 B13 — Diagnostics, checkpoints et preuves

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B13 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Checkpoint atomique

- **WHEN** une unité est engagée avec progression, idempotence et événements requis
- **THEN** son checkpoint SQL indique uniquement les effets réellement engagés

#### Scenario: Validation incomplète

- **WHEN** la limite de diagnostics est atteinte
- **THEN** le traitement s’arrête avec complétude fausse et sans diagnostic reproduisant une valeur

### Requirement: Runtime Bulk v1 B14 — Retour au cycle

Pour le runtime Bulk v1, la capacité MUST respecter intégralement les clauses B14 et les annexes de données logiques correspondantes ci-dessous. Ces règles MUST NOT modifier les profils préparatoires livrés.

#### Scenario: Preuve locale qualifiée

- **WHEN** les tests utilisent seulement des providers synthétiques déclarés
- **THEN** les preuves du runtime sont conservées sans déclarer un provider de production opérationnel

#### Scenario: Périmètre conservé

- **WHEN** la préparation RSMP est exécutée
- **THEN** seuls les six fichiers autorisés sont modifiés sans code, dépendance, infrastructure ou extension PA/PZT

## Annexes normatives — RSMP-BULK-EXECUTION-V1

Les clauses et schémas ci-dessous sont normatifs par les exigences Runtime Bulk v1 qui les référencent. Le schéma logique ne constitue ni une implémentation ni un nouveau wire format public.

### B01 — Périmètre exécutable

- Le runtime Bulk v1 MUST exécuter IMPORT et EXPORT asynchrones ; l’admission MUST persister opération, demande, premier Job et liaison dans une transaction avant de rendre operation_id.
- Le runtime v1 MUST prendre en charge CSV et NDJSON ; un autre format MUST être refusé comme capacité non implémentée, sans retirer l’extensibilité du contrat général.
- Les profils Kernel et BulkOperationRecord v1 MUST rester inchangés ; les données d’exécution MUST être portées par une extension de persistance liée un-à-un à l’opération.
- Une opération courte MAY rester asynchrone ; ce lot MUST NOT inventer de seuil synchrone ni de route HTTP publique.
- Le runtime v1 MUST exiger un tenant explicitement résolu et autorisé ; le traitement Bulk plateforme hors tenant MUST rester non implémenté, sans tenant global implicite.

### B02 — Enveloppe et progression

- Le contrat interne BulkExecutionV1 MUST respecter exactement les champs et types de l’annexe normative ; toutes les clés, y compris nullables, MUST être explicites.
- Les textes runtime MUST être des str exactes, non vides, UTF-8 strict et sans NUL ; les entiers MUST être des int exacts, bool exclu. Aucun contrôle runtime MUST modifier le profil préparatoire Record v1.
- Les références MUST rester opaques ; leur présence MUST NOT prouver existence ou autorisation. Un scope None MUST NOT désigner PLATFORM ou un tenant global.
- La progression MUST suivre l’annexe ProgressV1, être persistée et actualisée sans double comptage après reprise. Une validation positive MUST NOT être comptée comme mutation appliquée.
- Une révision MUST être contrôlée par compare-and-swap ; une version obsolète MUST refuser l’évolution, sans écraser un checkpoint concurrent.
- Les validateurs runtime MUST contrôler types exacts des clés puis valeurs avant comportement, parsing ou I/O ; une valeur étrangère MUST être refusée sans écho. L’adaptateur ORM MUST restituer les dates sous datetime exact avec timezone.utc.

### B03 — Ports serveur et autorité

- Tous les contrôles applicatifs de ce lot MUST s’appliquer sous réserve de authorization et initial-administration. Une dérogation MUST NOT être annoncée comme contrôle réalisé ni transférée ; elle MUST NOT fabriquer une capacité technique ou une preuve absente.
- Les ports MUST provenir de composants déclarés et composés côté serveur ; le payload MUST NOT fournir de callback, code, provider, credentials ou contexte d’autorité.
- Le port d’autorisation MUST être consulté à l’admission, avant exécution/reprise, avant chaque unité mutatrice et à l’accès au résultat ; DENY et UNAVAILABLE MUST refuser l’action sans repli.
- Le port d’autorisation MUST résoudre acteur, tenant et scope depuis l’autorité serveur et appliquer les exceptions canoniques existantes sans les transférer au worker.
- La gouvernance MUST être résolue par GovernanceResolutionV1 avant lecture, transfert ou mutation ; les secrets et charges interdites MUST NOT entrer dans un fichier de résultat, diagnostic, événement ou journal.
- Une capacité technique non implémentée, un schéma invalide ou une garantie transactionnelle absente MUST produire un refus explicite ; une dérogation métier MUST NOT fabriquer cette capacité.
- Une décision ALLOW MUST fournir les références serveur résolues du sujet, tenant, périmètre et contexte ; DENY ou UNAVAILABLE MUST NOT fournir de contexte exploitable.

### B05 — Parsing et mapping

- CSV v1 MUST utiliser UTF-8 strict sans BOM, séparateur virgule et guillemets doubles avec doublement ; LF et CRLF MUST être acceptés sans autodétection de dialecte.
- Le header CSV MUST contenir des noms exacts non vides et uniques ; colonnes inconnues, ambiguës ou surnuméraires MUST être refusées sans normalisation.
- NDJSON v1 MUST contenir un objet JSON par ligne, accepter une fin de ligne finale et refuser ligne vide, clé dupliquée, valeur non finie, UTF-8 invalide ou dépassement de limite.
- Le mapping MUST être déclaré, immuable et versionné, limité aux champs du contrat public propriétaire ; il MUST NOT modifier l’acteur, le tenant, le scope ou les permissions.
- Les conversions métier MUST relever du contrat propriétaire déclaré ; Bulk MUST NOT évaluer d’expression ou appliquer une conversion heuristique.
- La validation MUST être bornée en octets, lignes, colonnes, profondeur, membres et diagnostics. Une limite atteinte MUST arrêter le traitement et signaler son incomplétude sans faux succès.

### B06 — Machine à états

- Les transitions runtime MUST respecter exclusivement la matrice normative ; la simple appartenance à BulkOperationState MUST NOT autoriser une transition.
- COMPLETED, COMPLETED_WITH_ERRORS, FAILED, CANCELLED et EXPIRED MUST être terminaux ; expiration d’un fichier résultat MUST NOT réécrire un état terminal d’opération.
- Un retry technique MUST conserver le checkpoint et l’état Bulk non terminal courant, sous nouveau bail valide ; il MUST NOT réinitialiser la progression ou l’échéance.
- L’annulation MUST être autorisée et coopérative entre unités ; elle MUST NOT prétendre annuler des unités déjà engagées.
- Pour IMPORT mutateur, une validation rejetée MUST faire échouer ATOMIC et ATOMIC_PER_CHUNK avant APPLY ; BEST_EFFORT MAY appliquer uniquement les éléments admis si le module l’autorise.

### B07 — Modes et conflits

- VALIDATE_ONLY MUST valider et produire un rapport sans exécuter de mutation propriétaire ; son compteur applied_rows MUST rester zéro.
- ATOMIC MUST engager toutes les mutations dans une transaction propriétaire compatible ; une erreur MUST annuler cette unité entière, sans succès partiel.
- ATOMIC_PER_CHUNK MUST engager et checkpoint chaque chunk atomiquement ; une erreur MUST conserver les chunks déjà engagés et refuser de les rejouer comme nouveaux effets.
- BEST_EFFORT MUST être autorisé par le module et engager chaque élément avec ses invariants ; succès et rejets MUST être distincts et diagnostiqués.
- Les modes et stratégies MUST être choisis explicitement par le producteur serveur ; REJECT reste le rejet de conflit par défaut du contrat général et ATOMIC_PER_CHUNK le mode déclaré des gros imports.
- CREATE_ONLY, UPDATE_ONLY et UPSERT MUST être explicitement supportés et autorisés par le propriétaire ; aucune valeur None MUST être transformée implicitement par le profil Record.
- Une garantie atomique absente MUST refuser le mode avant mutation ; le runtime MUST NOT basculer vers BEST_EFFORT ou une transaction d’une autre source.

### B12 — Export et résultats

- EXPORT MUST utiliser une projection déclarée, les champs autorisés et le filtrage à la source avant pagination ; un index/cache MUST NOT remplacer l’autorité métier.
- Le propriétaire MUST déclarer SNAPSHOT ou WATERMARK et fournir sa référence avant READY ; une cohérence non résolue MUST refuser l’export.
- Le résultat MUST rester privé et ne devenir disponible qu’après finalisation et engagement du manifeste ; échec ou résultat partiel MUST NOT être présenté comme export complet.
- L’accès et toute URL temporaire MUST être réautorisés ; durée URL MUST être bornée par politique, expiration résultat et validité du contexte. Une URL signée MUST NOT être persistée.
- Rétention, révocation, effacement, classification et holds MUST suivre la gouvernance résolue ; un résultat non classifié ou un flux non déclaré MUST être refusé.

### B13 — Diagnostics, checkpoints et preuves

- Les diagnostics MUST porter uniquement code statique, champ déclaré et index de ligne éventuel ; ils MUST NOT reproduire valeurs, secrets, credentials ou assertions.
- Les checkpoints MUST respecter BulkCheckpointV1, être en PostgreSQL et s’engager avec l’unité correspondante ; pickle, code, contenu de fichier et état mémoire seul MUST être interdits.
- Le rapport MUST indiquer mode, compteurs, codes, complétude, références et versions ; un arrêt sur limite MUST être explicite et MUST NOT prétendre validation complète.
- La progression et les événements de contrôle MUST être minimisés, versionnés et auditables ; ils MUST NOT remplacer les événements métier propriétaires.

### B14 — Retour au cycle

- Le RSMP MUST rester limité aux six fichiers autorisés et MUST NOT implémenter du code, déployer, installer une dépendance ou étendre PA/PZT.
- Après validation du canon, les changes couverts MUST s’enchaîner selon CISMP, avec tests unitaires, gardes, PostgreSQL isolé, strict, archive unique et rapport par archive.
- Les tests MUST prouver types hostiles, refus d’autorité, rollback, CAS, baux concurrents, interruption/reprise, rejou identique/divergent, limites et absence de secret.
- La présence de providers de test MUST NOT prouver un provider de production ; une composition réelle non résolue MUST rester indisponible.

### Schéma logique BulkExecutionExtensionV1

```json
[
  [
    "execution_version",
    "str SemVer",
    "1.0.0 uniquement"
  ],
  [
    "requested_by_reference",
    "str opaque",
    "obligatoire"
  ],
  [
    "resolved_context_reference",
    "str opaque serveur",
    "contexte initial résolu, réévalué ; jamais une autorisation positive en cache"
  ],
  [
    "mapping_reference",
    "str opaque",
    "obligatoire"
  ],
  [
    "mapping_version",
    "str SemVer",
    "obligatoire"
  ],
  [
    "input_reference",
    "str opaque | None",
    "IMPORT non NULL ; EXPORT None"
  ],
  [
    "input_version",
    "str opaque | None",
    "IMPORT non NULL ; EXPORT None"
  ],
  [
    "input_sha256",
    "str hex minuscule, 64 caractères | None",
    "IMPORT non NULL ; EXPORT None"
  ],
  [
    "input_size_bytes",
    "int exact >= 0 | None",
    "IMPORT non NULL ; EXPORT None"
  ],
  [
    "output_reference",
    "str opaque | None",
    "server-only ; None avant finalisation export"
  ],
  [
    "output_version",
    "str opaque | None",
    "server-only ; None avant finalisation export"
  ],
  [
    "output_sha256",
    "str hex minuscule, 64 caractères | None",
    "server-only ; None avant finalisation export"
  ],
  [
    "output_size_bytes",
    "int exact >= 0 | None",
    "server-only ; None avant finalisation export"
  ],
  [
    "projection_reference",
    "str opaque | None",
    "EXPORT obligatoire ; IMPORT None"
  ],
  [
    "consistency_kind",
    "SNAPSHOT | WATERMARK | None",
    "EXPORT obligatoire ; IMPORT None"
  ],
  [
    "consistency_reference",
    "str opaque | None",
    "EXPORT résolue avant READY ; IMPORT None"
  ],
  [
    "idempotency_key",
    "str opaque",
    "obligatoire"
  ],
  [
    "correlation_id",
    "str opaque",
    "obligatoire"
  ],
  [
    "causation_id",
    "str opaque | None",
    "absence explicite admise"
  ],
  [
    "progress",
    "dict exact ProgressV1",
    "toutes clés explicites ; aucun défaut de modèle"
  ],
  [
    "checkpoint_reference",
    "str opaque | None",
    "référence runtime PostgreSQL ; pas de pickle ni fichier arbitraire"
  ],
  [
    "result_reference",
    "str opaque | None",
    "rapport/manifeste privé ; aucun URL signé persistant"
  ],
  [
    "expires_at",
    "datetime exact, aware UTC",
    "échéance fixe de l'opération ; aucune reprise ne la prolonge"
  ],
  [
    "policy_reference",
    "str opaque",
    "politique serveur déclarée et immuable par version"
  ],
  [
    "policy_version",
    "str SemVer",
    "obligatoire ; pas de sélection latest implicite"
  ],
  [
    "revision",
    "int exact >= 1",
    "producteur initialise explicitement 1 ; CAS à chaque évolution"
  ],
  [
    "cancellation_requested",
    "bool exact",
    "producteur initialise explicitement False ; action autorisée"
  ]
]
```

### Schéma logique ProgressV1

```json
[
  [
    "total_rows",
    "int exact >=0 | None",
    "inconnu explicitement admis"
  ],
  [
    "validated_rows",
    "int exact >=0",
    "inclut lignes invalides examinées"
  ],
  [
    "invalid_rows",
    "int exact >=0",
    "<= validated_rows"
  ],
  [
    "applied_rows",
    "int exact >=0",
    "mutations confirmées ; zéro VALIDATE_ONLY/EXPORT"
  ],
  [
    "execution_rejected_rows",
    "int exact >=0",
    "applied_rows + execution_rejected_rows <= validated_rows - invalid_rows"
  ],
  [
    "exported_rows",
    "int exact >=0",
    "zéro IMPORT ; <= validated_rows"
  ]
]
```

### Schéma logique BulkCheckpointV1

```json
[
  [
    "checkpoint_id",
    "str opaque",
    "clé locale"
  ],
  [
    "operation_id",
    "FK BulkOperationRecord",
    "obligatoire"
  ],
  [
    "phase",
    "STAGE | VALIDATE | APPLY | EXPORT",
    "obligatoire"
  ],
  [
    "source_fingerprint",
    "SHA-256 minuscule 64 caractères",
    "identité immuable source/consistance"
  ],
  [
    "mapping_version",
    "str SemVer",
    "obligatoire"
  ],
  [
    "committed_unit_index",
    "int exact >=0",
    "borne de reprise ; unité 0 = avant premier engagement"
  ],
  [
    "progress",
    "ProgressV1",
    "snapshot validé"
  ],
  [
    "revision",
    "int exact >=1",
    "CAS ; unique(operation_id,revision)"
  ],
  [
    "owner_result_reference",
    "str opaque | None",
    "référence minimisée de résultat propriétaire"
  ]
]
```

### Schéma logique PolicyV1

```json
{
  "positive_integers": [
    "max_input_bytes",
    "max_rows",
    "max_row_bytes",
    "max_columns",
    "max_json_depth",
    "max_json_members",
    "max_diagnostics",
    "read_chunk_bytes",
    "chunk_rows",
    "max_attempts",
    "lease_seconds",
    "renewal_seconds",
    "publish_max_attempts",
    "publish_lease_seconds",
    "publish_renewal_seconds",
    "max_parallel_operations",
    "max_runtime_seconds",
    "replay_window_seconds",
    "idempotency_retention_seconds",
    "staging_retention_seconds",
    "result_retention_seconds",
    "max_download_url_seconds"
  ],
  "lists": [
    "retry_delays_seconds : liste exacte d'int >0, longueur max_attempts-1",
    "publish_retry_delays_seconds : liste exacte d'int >0, longueur publish_max_attempts-1"
  ],
  "constraints": [
    "2*renewal_seconds < lease_seconds",
    "2*publish_renewal_seconds < publish_lease_seconds",
    "idempotency_retention_seconds >= replay_window_seconds",
    "deadline effective <= expires_at",
    "aucun défaut numérique ; toutes clés présentes ; politique immuable par (reference,version)"
  ]
}
```

### Schéma logique AuthorityAssessmentV1

```json
[
  [
    "decision",
    "ALLOW | DENY | UNAVAILABLE",
    "décision effective après application des exceptions canoniques"
  ],
  [
    "resolved_context",
    "ServerContextRefsV1 | None",
    "ALLOW : obligatoire ; DENY/UNAVAILABLE : None"
  ]
]
```

### Schéma logique ServerContextRefsV1

```json
[
  [
    "subject_id",
    "str opaque",
    "identité résolue côté serveur"
  ],
  [
    "tenant_id",
    "str opaque | None",
    "None uniquement contexte plateforme explicitement résolu"
  ],
  [
    "perimeter_reference",
    "str opaque",
    "périmètre effectif déclaré ; aucune déduction depuis None"
  ],
  [
    "context_reference",
    "str opaque serveur",
    "référence non secrète, réévaluée à chaque contrôle"
  ]
]
```

### Schéma logique GovernanceResolutionV1

```json
[
  ["resolution_version", "str exacte", "1.0.0 uniquement"],
  ["decision", "str exacte RESOLVED | DENY | UNAVAILABLE", "aucun défaut"],
  ["resolved_context", "dict exact ServerContextRefsV1 | None", "lié à l'autorité courante sur RESOLVED ; None sur DENY/UNAVAILABLE"],
  ["policy", "dict exact à trois clés | None", "obligatoire sur RESOLVED ; None sur DENY/UNAVAILABLE"],
  ["profile", "DataGovernanceProfile exact | None", "profil existant à quinze champs sur RESOLVED ; None sur DENY/UNAVAILABLE"],
  ["obligations", "tuple exact de str opaques | None", "explicite sur RESOLVED ; None sur DENY/UNAVAILABLE"]
]
```

- La réponse MUST être un dict exact aux six clés explicites, avec resolution_version exactement 1.0.0 ; les types des clés puis des valeurs MUST être contrôlés avant comportement, parsing, comparaison ou I/O, selon les règles runtime B02.
- RESOLVED MUST provenir d'une résolution effective du port déclaré et composé côté serveur ; les quatre données résolues MUST être explicites et non None, et resolved_context MUST correspondre aux quatre références de l'autorité courante.
- policy MUST porter exactement policy_reference str opaque, policy_version SemVer complète et limits respectant intégralement PolicyV1 existant ; les limites numériques MUST NOT être inventées ou fournies par défaut.
- profile MUST réutiliser le DataGovernanceProfile existant à quinze champs sans modifier ses profils préparatoires : profile_version, data_asset_id, owner_component, source_of_truth, data_classes, confidentiality, personal_data, purpose_refs, retention_policy, deletion_policy, residency_constraints, authorized_consumers, processor_refs, export_policy et lineage. Sa seule validation structurelle MUST NOT prouver une résolution.
- obligations MUST être un tuple exact de str exacts opaques non vides, sans normalisation ; un tuple vide MUST exprimer une absence effectivement résolue par le serveur et MUST NOT résulter d'un défaut.
- DENY et UNAVAILABLE MUST porter resolved_context, policy, profile et obligations à None ; un contexte exploitable ou un repli MUST NOT être produit. Une exception de port MUST être refusée sans détail brut ni transfert d'exception.
- Les valeurs résolues MUST être capturées immuables avant usage, sans alias mutable du fournisseur. Le payload MUST NOT fournir callback, code, provider, credentials ou contexte d'autorité, ni transformer un profil structurel ou une référence opaque en preuve de résolution.

### Schéma logique MappingDescriptorV1

```json
[
  [
    "mapping_reference",
    "str opaque",
    "obligatoire"
  ],
  [
    "mapping_version",
    "str SemVer",
    "immuable"
  ],
  [
    "owner_reference",
    "str opaque",
    "module propriétaire déclaré"
  ],
  [
    "variant",
    "IMPORT | EXPORT",
    "obligatoire"
  ],
  [
    "format",
    "CSV | NDJSON",
    "obligatoire"
  ],
  [
    "source_fields",
    "tuple exact de str uniques",
    "ordre déclaré"
  ],
  [
    "target_fields",
    "tuple exact de str uniques",
    "ordre déclaré"
  ],
  [
    "required_source_fields",
    "tuple exact de str uniques",
    "sous-ensemble source_fields"
  ],
  [
    "field_bindings",
    "tuple exact de couples source/target str",
    "bijection déclarée, aucune expression ni alias implicite"
  ]
]
```

### Schéma logique RowDiagnosticV1

```json
[
  [
    "code",
    "str exacte déclarée statique",
    "aucune valeur utilisateur"
  ],
  [
    "field_reference",
    "str déclarée | None",
    "champ de schéma, pas une valeur"
  ],
  [
    "line_index",
    "int exact >=1 | None",
    "position uniquement"
  ]
]
```

### Schéma logique CommandValidationV1

```json
[
  [
    "accepted",
    "bool exact",
    "True si et seulement si diagnostics vide"
  ],
  [
    "diagnostics",
    "tuple exact de RowDiagnosticV1",
    "borné par PolicyV1"
  ]
]
```

### Schéma logique CommandExecutionV1

```json
[
  [
    "outcome",
    "APPLIED | REPLAYED | REJECTED",
    "pas de faux effet nouveau sur REPLAYED"
  ],
  [
    "result_reference",
    "str opaque | None",
    "résultat propriétaire minimal"
  ],
  [
    "diagnostics",
    "tuple exact de RowDiagnosticV1",
    "borné"
  ],
  [
    "event_references",
    "tuple exact de str opaques",
    "outbox de la même transaction, aucune publication directe"
  ]
]
```

### Schéma logique ExportManifestV1

```json
[
  [
    "manifest_version",
    "str SemVer",
    "1.0.0"
  ],
  [
    "operation_id",
    "str opaque",
    "opération persistante"
  ],
  [
    "format",
    "CSV | NDJSON",
    "déclaré"
  ],
  [
    "mapping_reference",
    "str opaque",
    "déclaré"
  ],
  [
    "mapping_version",
    "str SemVer",
    "déclaré"
  ],
  [
    "tenant_context_reference",
    "str opaque",
    "serveur"
  ],
  [
    "scope_context_reference",
    "str opaque | None",
    "serveur, pas de global implicite"
  ],
  [
    "consistency_kind",
    "SNAPSHOT | WATERMARK",
    "propriétaire"
  ],
  [
    "consistency_reference",
    "str opaque",
    "résolue"
  ],
  [
    "row_count",
    "int exact >=0",
    "sortie finalisée"
  ],
  [
    "size_bytes",
    "int exact >=0",
    "octets réels"
  ],
  [
    "sha256",
    "hex minuscule 64 caractères",
    "octets de sortie"
  ],
  [
    "classification_reference",
    "str opaque",
    "gouvernance"
  ],
  [
    "expires_at",
    "datetime exact timezone.utc",
    "politique"
  ],
  [
    "object_reference",
    "str opaque",
    "privé"
  ],
  [
    "object_version",
    "str opaque",
    "immuable"
  ],
  [
    "complete",
    "bool exact",
    "True seulement après finalisation complète"
  ]
]
```

### Schéma logique ValidationReportV1

```json
[
  [
    "report_version",
    "str SemVer",
    "1.0.0"
  ],
  [
    "operation_id",
    "str opaque",
    "obligatoire"
  ],
  [
    "mode",
    "VALIDATE_ONLY | ATOMIC | ATOMIC_PER_CHUNK | BEST_EFFORT | None",
    "IMPORT ; None explicite pour EXPORT si rapport d’erreur"
  ],
  [
    "progress",
    "ProgressV1",
    "compteurs réels"
  ],
  [
    "diagnostics",
    "tuple exact de RowDiagnosticV1",
    "borné, jamais brut"
  ],
  [
    "complete",
    "bool exact",
    "False si limite/interruption"
  ],
  [
    "source_version",
    "str opaque | None",
    "source déclarée"
  ],
  [
    "mapping_version",
    "str SemVer",
    "obligatoire"
  ]
]
```

### Ports serveur déclarés

```json
[
  [
    "AuthorityPort",
    "check(contexte_serveur, action, operation_reference, resource_reference)",
    "ALLOW | DENY | UNAVAILABLE ; contexte résolu par serveur ; actions ADMIT/EXECUTE/CANCEL/READ_RESULT"
  ],
  [
    "GovernancePort",
    "resolve(contexte_serveur, contrat, références)",
    "GovernanceResolutionV1 : politique immuable versionnée, classification et obligations résolues ; refus fermé sinon"
  ],
  [
    "ObjectStoragePort",
    "stat_private, iter_bytes, begin_private_write, finalize_private_write, revoke, purge_authorized",
    "références/versions opaques, octets bornés, SHA-256, deadline/cancellation ; aucun URL public par défaut"
  ],
  [
    "MappingPort",
    "resolve(mapping_reference,mapping_version,owner_reference)",
    "schéma, ordre de champs, projection et mapping déclarés immuables ; aucun code ou expression du payload"
  ],
  [
    "OwnerCommandPort",
    "validate, execute, canonical_bytes",
    "contrat public versionné, diagnostics statiques ; participation PostgreSQL déclarée pour mutation"
  ],
  [
    "OwnerProjectionPort",
    "filter_authorized, acquire_consistency, iterate_projection",
    "champs/filtres/tris déclarés, SNAPSHOT ou WATERMARK borné et versionné"
  ],
  [
    "AuditPort",
    "append_minimized",
    "acteur/périmètre/opération/résultat ; mêmes frontières requises par les contrats propriétaires"
  ],
  [
    "PublisherPort",
    "publish_declared_event",
    "contrat DOMAIN/INTEGRATION déclaré ; idempotence externe si nécessaire"
  ],
  [
    "DownloadPort",
    "authorize_then_issue_temporary_reference",
    "vérification actuelle ; référence temporaire bornée, non persistée"
  ]
]
```

### Matrice des opérations

```json
{
  "import": {
    "REQUESTED": [
      "STAGED"
    ],
    "STAGED": [
      "VALIDATING"
    ],
    "VALIDATING": [
      "READY",
      "COMPLETED (VALIDATE_ONLY, sans rejet)",
      "COMPLETED_WITH_ERRORS (VALIDATE_ONLY, rejets)"
    ],
    "READY": [
      "RUNNING"
    ],
    "RUNNING": [
      "COMPLETED",
      "COMPLETED_WITH_ERRORS (BEST_EFFORT avec rejets)"
    ]
  },
  "export": {
    "REQUESTED": [
      "VALIDATING"
    ],
    "VALIDATING": [
      "READY"
    ],
    "READY": [
      "RUNNING"
    ],
    "RUNNING": [
      "COMPLETED"
    ]
  },
  "shared": "Depuis tout état non terminal : FAILED sur échec définitif, CANCELLED sur annulation autorisée et EXPIRED sur échéance atteinte. Aucun arc sortant terminal. Retries conservant état non terminal courant."
}
```

### Précisions transversales approuvées

- Toutes les données logiques de ces annexes ont exactement leurs clés déclarées ; aucune clé inconnue, valeur omise, coercition de valeur étrangère ou défaut de modèle.
- Les références texte runtime sont str exactes, non vides, UTF-8 strict et sans NUL ; les versions utilisent parse_version existant ; les dates runtime sont datetime exact timezone.utc après décodage ORM explicite de confiance.
- Les initialisations PENDING/REQUESTED, révision1, compteurs0, False et None sont des valeurs explicites du producteur, proposées ici comme nouveaux choix runtime ; elles ne modifient aucun défaut du modèle préparatoire Record.
- La machine à états est un contrat runtime distinct du vocabulaire structurel ; la seule présence d’une ligne ou d’un Enum ne valide aucun effet ni contrôle.
- Les limites de politique sont des données serveur versionnées obligatoires ; les dérogations applicatives respectent authorization. Une dérogation ne vaut jamais capacité absente, fichier effectivement vérifié, transaction engagée ou audit réalisé.
- Les payloads/sérialiseurs/ports propriétaires sont des contrats publics déclarés du composant ; aucun callback ou expression du payload n’est exécuté. Les schemas propriétaires existants restent des dépendances requises, refusées si non résolues.
- Le contrôle autoritatif de l’acteur initial et de son périmètre appartient à Django ; les références persistantes n’en sont pas la preuve.
- Le CSV généré est UTF-8 sans BOM, séparateur virgule, guillemets doubles et CRLF ; NDJSON généré est UTF-8 sans BOM et LF, une ligne par objet JSON.
- Les transactions multi-sources ou effets externes ne sont pas annoncés atomiques ; seules les capacités compatibles explicitement composées sont utilisables.
- Chaque ligne source possède une identité d’unité stable, dérivée de l’opération, de la phase et de sa position dans la version immuable ; le journal transactionnel évite le double comptage.
- Les corps des événements et des Commands sont validés par leurs schémas propriétaires ; les octets canoniques versionnés servent au SHA-256 de leur idempotence, sans nouveau sérialiseur global implicite.
- L’enveloppe de demande et le fingerprint d’admission sont figés ; les références de suivi et la consistance export acquise ensuite n’en changent pas l’identité.
- Aucun temps de rétention ou limite numérique de production n’est choisi par ce lot ; toutes valeurs sont fournies et validées dans PolicyV1.
- Les phases STAGE et VALIDATE IMPORT ne mutent pas le domaine propriétaire ; APPLY revalide dans la transaction courante avant chaque unité.
- Un checkpoint de chunk référence la dernière unité réellement engagée ; zéro signifie avant premier engagement. Le stockage de checkpoint est SQL dans la même transaction, pas un objet externe prétendument atomique.
- Les contrats HTTP publics, un provider de stockage concret, un transport d’événements concret et le déploiement ne sont pas introduits ; leur absence rend la composition de production indisponible, sans empêcher les preuves du runtime avec providers synthétiques déclarés.
- Pour Bulk v1, AuthorityAssessmentV1 ALLOW exige un tenant_id non None et un périmètre effectif résolu. ServerContextRefsV1 générique peut représenter un contexte plateforme pour d’autres capacités, sans activer Bulk plateforme.
- L’échéance opérationnelle est validée à l’admission contre l’horloge serveur et max_runtime_seconds, puis fixe. L’échéance de rétention d’une identité d’idempotence est distincte et couvre la fenêtre après terminalité.
- Les identifiants operation_id, job_id et command_id sont distincts ; les contraintes de liaison runtime doivent le vérifier sans modifier BulkJobLink préparatoire.
- Les secrets d’authentification restent dans leurs providers sécurisés ; les références stockées ne sont pas des credentials ni des assertions brutes. Les interdictions propres aux agents restent intégralement applicables.

### Frontière du contrat

Contrats internes de runtime, pas de nouveau wire format ou endpoint public. Les signatures Python définitives et le découpage physique des tables sont des choix d’implémentation sous les schémas logiques validés, sans ajouter de champ ni de sémantique.
