## MODIFIED Requirements

### Requirement: Compilation différenciée validée

Les trois binaires PA MUST être compilés avec Cython ; le binaire indépendant
PZT MUST suivre Cython selon pzt. Les chaînes MUST partir de Python via C avec
runtime, dépendances et ABI déclarés et qualifiés avant construction. Cette
décision MUST NOT installer un outil ni prouver un gain de performance.

#### Scenario: Compilation des composants distincts

- **WHEN** la matrice de compilation PA/PZT est déclarée
- **THEN** les trois binaires PA et PZT indépendant utilisent Cython avec leurs chaînes et qualifications propres

### Requirement: Paramètres ouverts et absence d'implémentation implicite

Les identifiants pixs.agent, pixs.pzt et le nom du composant/binaire PZT MUST
être considérés validés. Noms/versions de paquets, noms de fichiers exécutables,
chemins, CLI, bibliothèques, comptes, formats et valeurs non arrêtés MUST rester
ouverts jusqu'à décision ou qualification. Les versions de Cython MUST
être qualifiées avant installation. Cette rédaction MUST NOT valoir code,
recette runtime, support de plateforme ou artefact livré.

#### Scenario: Paramètres ouverts et absence d'implémentation implicite

- **WHEN** seules les spécifications sont déclarées
- **THEN** les états d'implémentation, qualification et publication restent explicitement non réalisés

## ADDED Requirements

### Requirement: Processus PA configurables par rôle et session

Les trois binaires et six modes PA MUST conserver leur répartition et permettre un plan de processus et de concurrence selon runtime et les ressources de leur environnement. Le plan MUST distinguer démons permanents, événements bornés et sessions réelles. Il MUST NOT transformer un événement en démon, activer un mode exclu du profil ou partager les privilèges entre système et utilisateur.

#### Scenario: Deux sessions utilisateur

- **WHEN** deux sessions réelles utilisent le binaire utilisateur PA
- **THEN** leurs processus, droits, ressources et arrêts restent isolés dans le budget global déclaré

#### Scenario: Profil Docker dimensionné

- **WHEN** un plan de ressources PA est appliqué dans Docker
- **THEN** seuls les modes système et événements du conteneur admissibles sont sélectionnés, sans mode de session

### Requirement: Unicité des opérations PA multiprocessus

Les processus PA MUST coordonner propriété des ressources, admission, idempotence et résultats durables selon leurs contrats. Leur multiplication MUST NOT dupliquer un effet, créer une identité ou une autorité implicite, ni permettre des mutations concurrentes incompatibles. Les configurations de ressources MUST être gérées par pixs.agent via PZT avec état appliqué vérifié.

#### Scenario: Deux processus pour une opération

- **WHEN** deux processus PA reçoivent une même opération ou des opérations incompatibles sur une ressource
- **THEN** la coordination conserve l'idempotence et la propriété déclarée sans double application ni choix implicite d'autorité
