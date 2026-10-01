# component-model Specification

## Purpose
Le modèle de composant unifie l'identification, le versionnement et la composition des modules, sous-modules, fournisseurs, extensions et thèmes.

## Requirements

### Requirement: Types de composants unifiés

Le système MUST prendre en charge les types KERNEL, MODULE, SUBMODULE, PROVIDER, EXTENSION et THEME avec les mêmes mécanismes de manifest et de cycle de vie. Les contributions frontend sont une facette déclarée des composants MODULE et SUBMODULE ; elles MUST NOT créer de type, registre ou lifecycle frontend parallèle.

#### Scenario: Sous-module validé comme module

- **WHEN** un sous-module valide est déclaré
- **THEN** il est découvert, validé et chargé par le système commun sans moteur parallèle

#### Scenario: Facette frontend d'un sous-module

- **WHEN** un sous-module déclare des contributions frontend dans son manifest
- **THEN** elles sont rattachées au même composant, à sa version et à son lifecycle sans créer un composant frontend distinct

### Requirement: Manifest déclaratif unique

Chaque composant MUST fournir un `component.toml` avec identifiant, type, version SemVer, dépendances, capacités et contrats, sans secret ni logique exécutable.

#### Scenario: Secret dans le manifest rejeté

- **WHEN** un manifest contient un secret ou une expression à évaluer
- **THEN** la composition est refusée avec un diagnostic explicite

### Requirement: Schéma de manifest versionné et validable

Le `component.toml` MUST déclarer une version de schéma. Le schéma MUST définir
les champs obligatoires, leurs types et les règles de compatibilité ; une
version inconnue ou ambiguë MUST bloquer la validation. Le manifest MAY
référencer des déclarations versionnées sans y embarquer de valeur sensible.

#### Scenario: Version de schéma inconnue

- **WHEN** un composant déclare une version de schéma non prise en charge
- **THEN** il reste non validé avec un diagnostic indiquant la version concernée

### Requirement: Identifiants stables namespacés

Le système MUST respecter les garanties suivantes.

Les identifiants `pixs.*` sont réservés ; les composants externes utilisent un espace de noms fournisseur ; tout renommage vaut évolution incompatible.

#### Scenario: Collision d'identifiants refusée

- **WHEN** deux composants déclarent le même identifiant canonique
- **THEN** l'activation est bloquée avant tout chargement

### Requirement: États de composition, installation et santé distincts

Le système MUST distinguer les états de composition, d'installation et de santé ; un composant installé-désactivé, activé-non configuré ou configuré-non sain MUST NOT être confondu avec un composant prêt.

#### Scenario: États non assimilés

- **WHEN** un composant est installé mais désactivé, ou activé mais mal configuré, ou prêt mais dégradé
- **THEN** chaque état est représenté distinctement et la composition ne devient pas ACTIVE tant que manifest, dépendances, contrats et contraintes de sécurité ne sont pas validés

### Requirement: Manifest schéma 1 — capacités et contrats versionnés

Le `component.toml` de `schema_version = "1"` MUST déclarer les capacités
fournies comme tableau de tables inline `[provides].capabilities` avec les
champs `id` (string non vide), `version` (SemVer 2.0.0 complète),
`contracts` (tableau de strings, sous-ensemble des contrats du `[implements]`
du MÊME composant, MAY vide), `criticality` (`REQUIRED` ou `OPTIONAL`) et
`fallback` (string ; valeur `"none"` explicite si `REQUIRED`, non vide si
`OPTIONAL`). Le propriétaire d'une capacité fournie est dérivé de
l'identifiant du composant ; aucune liste de noms parallèle.

Le `[implements].contracts` MUST être un tableau de tables inline `{id,
version}` où `version` est la version exacte du contrat implémenté.

Les `[dependencies]` et `[optional_dependencies]` (`components`,
`capabilities`, `contracts`) sont des listes de strings
`"id [comparateurs]"` dont la grammaire et la sémantique sont définies par la
spécification `dependencies`. Toute ancienne chaîne fournie sans version dans
`[provides].capabilities` ou `[implements].contracts` MUST être refusée en
validation avec un diagnostic nommant le champ et l'entrée ; les fixtures
historiques DOIVENT être adaptées et la version du composant MUST NOT servir
de proxy. Aucune preuve de conformité ne figure dans le manifest.

#### Scenario: Capacité fournie sans version refusée

- **WHEN** un manifest déclare une capacité fournie sans `version`
- **THEN** il reste non validé avec un diagnostic nommant le champ et l'entrée concernée
