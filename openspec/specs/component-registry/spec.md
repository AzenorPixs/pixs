# component-registry Specification

## Purpose

Le registre de composants permet de cataloguer et distribuer des composants
signés sans imposer une source centrale, un fournisseur concret ou une
installation connectée.

## Requirements

### Requirement: Catalogue de composants et sources déclarées

Un registre MUST exposer les métadonnées publiques, versions, contrats,
compatibilités, provenances et états de révocation des MODULE, PROVIDER et
EXTENSION qu'il catalogue. Une installation MUST pouvoir utiliser une source
privée ou hors ligne signée déclarée. Un marketplace public MAY être fourni par
un adapter, mais MUST NOT être requis pour la résolution ou l'installation.

#### Scenario: Source locale sélectionnée

- **WHEN** une installation sélectionne un catalogue local compatible
- **THEN** elle résout ses composants sans requérir un marketplace central

### Requirement: Installation vérifiée sans activation implicite

Avant une installation, le système MUST vérifier signature, provenance, SBOM,
compatibilité et politique de confiance. La présence ou la récupération d'un
composant MUST NOT l'activer, sélectionner ses providers ou modifier la
composition effective implicitement.

#### Scenario: Composant téléchargé non sélectionné

- **WHEN** un composant valide est récupéré mais absent de la composition
- **THEN** il reste installé ou disponible sans devenir actif

### Requirement: Révocation et retrait contrôlés

Le registre MUST publier les états de retrait ou révocation de manière
versionnée et traçable. Une révocation critique MUST empêcher une nouvelle
activation et produire un diagnostic sans supprimer silencieusement les
données, contrats ou composants déjà installés.

#### Scenario: Version révoquée au contrôle de composition

- **WHEN** une composition demande une version révoquée par sa politique
- **THEN** son activation est refusée avec une erreur diagnostiquable

### Requirement: Recherche et résolution déterministes

La recherche et la résolution MUST appliquer les identifiants canoniques, les
contraintes SemVer, les canaux et le niveau de confiance déclarés. Un résultat
ambigu ou non vérifiable MUST NOT être installé comme choix par défaut.

#### Scenario: Deux versions compatibles candidates

- **WHEN** deux candidats satisfont la même contrainte sans règle explicite
- **THEN** la résolution échoue au lieu de choisir selon l'ordre du registre
