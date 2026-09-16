# architecture-decisions Specification

## Purpose

Les décisions d'architecture tracent les précisions apportées aux choix ouverts
sans remplacer les spécifications OpenSpec.

## Requirements

### Requirement: Décision contextualisée

Toute décision précisant un choix architectural ouvert MUST posséder un
identifiant stable, un état, un contexte, les alternatives examinées, ses
conséquences, les spécifications affectées et une date de réévaluation lorsque
pertinente.

#### Scenario: Décision de provider documentée

- **WHEN** une décision fixe une stratégie de provider pour un profil
- **THEN** elle identifie ses contrats et limites sans modifier implicitement le Kernel

### Requirement: OpenSpec reste normatif

Une décision MUST NOT modifier ou affaiblir une exigence normative sans évolution
OpenSpec approuvée. Lorsqu'elle entre en conflit avec une spécification validée,
cette dernière MUST prévaloir.

#### Scenario: Décision contradictoire

- **WHEN** une décision propose un comportement contraire à une exigence active
- **THEN** elle est bloquée ou renvoie vers l'évolution OpenSpec nécessaire

### Requirement: États traçables

Une décision MUST exposer `PROPOSED`, `ACCEPTED`, `SUPERSEDED` ou `REJECTED`.
Une décision remplacée MUST référencer celle qui la remplace sans réécrire son historique.

#### Scenario: Décision remplacée

- **WHEN** une nouvelle décision remplace une décision acceptée
- **THEN** les deux décisions et leur relation restent traçables
