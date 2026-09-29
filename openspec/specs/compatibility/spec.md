# compatibility Specification

## Purpose
La compatibilité vérifie les contraintes de version entre composants, contrats, schémas, événements, providers et clients via une matrice calculée avant activation ou mise à niveau.

## Requirements

### Requirement: Contraintes de version déclarées et vérifiées

Chaque consommateur MUST déclarer les contraintes de version des contrats dont il dépend ; le noyau MUST vérifier ces contraintes avant activation et lors de toute mise à niveau.

#### Scenario: Contrainte insatisfaite à l'activation

- **WHEN** un module déclare une contrainte de contrat non satisfaite par la composition
- **THEN** l'activation est refusée avec la référence de la contrainte violée

### Requirement: Aucune compatibilité présumée

Une incompatibilité connue MUST produire un échec explicite ; le système MUST NOT présumer une implémentation compatible au seul motif d'un nom proche ou d'une version plus récente.

#### Scenario: Version supérieure non testée

- **WHEN** un fournisseur publie une version supérieure jamais validée contre le contrat déclaré
- **THEN** la composition reste bloquée jusqu'à validation de conformité

### Requirement: Matrice de compatibilité globale

La compatibilité MUST être représentée par une matrice calculée avant activation ou mise à niveau, couvrant exécution, composants et capacités, contrats et API, schémas et migrations, événements, providers, configuration et clients, avec des états distincts dont au minimum compatible, migration requise, déprécié et bloqué.

#### Scenario: État bloqué déterministe

- **WHEN** la matrice produit un état bloqué pour une mise à niveau demandée
- **THEN** la mise à niveau est refusée et l'état est diagnostiquable avec sa cause

### Requirement: Compatibilité déclarative distincte de la conformité comportementale

La compatibilité déclarative par contraintes de version et la conformité comportementale par suites de tests MUST être évaluées séparément et toutes deux satisfaites avant de déclarer une composition valide.

#### Scenario: Déclaration sans conformité

- **WHEN** un composant déclare une plage compatible sans preuve de conformité comportementale à cette version
- **THEN** la composition est incomplète et l'activation reste refusée

### Requirement: Coexistence pendant les montées de version

Les évolutions MUST préserver la coexistence des versions supportées ; les ruptures ne sont autorisées qu'au changement de version majeure accompagné, et les suppressions d'éléments consommés restent différées jusqu'à la fin de la fenêtre de compatibilité.

#### Scenario: Suppression prématurée

- **WHEN** une suppression de champ ou de contrat cible un élément encore consommé par une version supportée
- **THEN** l'opération est refusée avec la contrainte de coexistence en cause

### Requirement: Contraintes de contrats sur versions exactes déclarées

Les contraintes de version des contrats MUST être évaluées contre la
`contract_version` exacte déclarée au format défini par la spécification
`component-model`, selon la grammaire définie par la spécification
`dependencies` ; la version du composant implémenteur MUST NOT servir de
proxy.

#### Scenario: Contrat implémenté en version incompatible

- **WHEN** un consommateur exige `pixs.authentication.contract >=1.0.0 <2.0.0` et l'implémenteur déclare ce contrat en version `2.1.0`
- **THEN** l'activation est refusée avec la référence de la contrainte violée et la version trouvée

### Requirement: Preuve de conformité externe

La conformité comportementale MUST être établie par des
`ConformityAttestation` fournies en mémoire par l'appelant de confiance,
extérieures au manifest, de la forme `{ component_id: string non vide,
component_version: SemVer complète, scope: COMPONENT|CAPABILITY|CONTRACT,
target_id: string non vide, target_version: SemVer complète exacte,
suite_id: string non vide, suite_version: SemVer complète, verdict: PASS,
proof_ref: string non vide }`, sans secret ni contenu de rapport. La liaison
exacte porte sur `component_version` et `target_version` des attestations et
inclut l'identité textuelle déclarée, métadonnées de build comprises ; les
comparateurs restent évalués selon la spécification `dependencies`. Pour le
scope `COMPONENT`, `target_id` et `target_version` sont l'identifiant et la
version du composant. Une chaîne auto-déclarée du manifest n'est JAMAIS une
preuve.

La couverture suivante est exigée avant activation : chaque composant activé
MUST être couvert par une preuve de portée `COMPONENT` de son fournisseur
(id et version exacts) ; chaque capacité ou contrat résolu MUST être couvert
par une preuve ciblée de son fournisseur (cible et version exactes). Toute
preuve absente, contradictoire, en échec, en mismatch de version, ambiguë ou
malformée MUST refuser l'activation avec un diagnostic non sensible nommant
la preuve manquante ou en cause. L'appelant authentifie les preuves et atteste
la réalisation des tests ; le noyau valide seulement leur structure et leur
couverture sans prétendre exécuter de suites. La bibliothèque P0 reste
utilisable par tout appelant réel externe fournissant des preuves vérifiées ;
les doubles de tests sont clairement nommés et limités aux fixtures.

#### Scenario: Activation sans preuve refusée

- **WHEN** une composition résout ses dépendances mais aucune attestation ne couvre un composant activé
- **THEN** l'activation est refusée avec un diagnostic nommant la preuve manquante

#### Scenario: Preuve d'un autre fournisseur ou d'une autre version refusée

- **WHEN** la seule attestation couvre le même identifiant de capacité fourni par un autre composant ou en une autre version exacte
- **THEN** l'activation est refusée avec un diagnostic nommant le mismatch de fournisseur ou de version

#### Scenario: Preuves concordantes autorisant l'activation

- **WHEN** chaque composant activé et chaque capacité ou contrat résolu est couvert par une attestation PASS de version exacte de son fournisseur
- **THEN** la couverture est satisfaite et ne bloque pas l'activation pour ce motif

### Requirement: Matrice P0 limitée aux dimensions connues

Les exigences de matrice de compatibilité globale et d'états minimum sont
préservées ; P0 MUST évaluer seulement les dimensions qu'il connaît
(composants, capacités et contrats déclarés, preuves fournies) et MUST NOT
déclarer de matrice globale complète ni de compatible global si des
dimensions restent hors périmètre ou inconnues.

#### Scenario: Dimension inconnue non évaluée

- **WHEN** une dimension de compatibilité (schéma, migration, événement, provider, client) n'est pas évaluable en P0
- **THEN** P0 expose la dimension comme non évaluée et ne délivre pas de validation globale
