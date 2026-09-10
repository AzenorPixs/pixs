# audit-integrity Specification

## Purpose

L'intégrité cryptographique optionnelle renforce la vérifiabilité des audits
sans transformer leur stockage en source d'autorisation ni neutraliser les
obligations de confidentialité et d'effacement.

## Requirements

### Requirement: Mécanisme d'intégrité explicitement déclaré

Un mécanisme d'intégrité MUST commencer par un chaînage vérifiable déclaré par
composant ou déploiement avec son algorithme, sa version, son fournisseur, sa
portée et ses politiques de conservation. Un scellement externe MAY compléter
ce chaînage ; une conservation WORM MUST rester une politique explicitement
déclarée par le déploiement. Le système MUST NOT activer un mécanisme
implicitement pour un audit qui ne le requiert pas.

#### Scenario: Audit standard sans mécanisme déclaré

- **WHEN** une installation n'active aucune politique d'intégrité renforcée
- **THEN** son audit conserve les garanties de base sans revendiquer une preuve cryptographique

### Requirement: Preuves vérifiables et chaînage résilient

Les preuves MUST lier les événements, versions, ordres ou fenêtres déclarés et
permettre de détecter une altération, omission ou rupture dans leur portée. Une
preuve invalide MUST être diagnostiquée et ne peut pas être silencieusement
remplacée par une nouvelle chaîne.

#### Scenario: Événement modifié

- **WHEN** un événement couvert est altéré après son scellement
- **THEN** la vérification échoue avec une corrélation vers la preuve concernée

### Requirement: Exports et conservation vérifiables

Un export d'audit doté d'une preuve d'intégrité MUST contenir les métadonnées
nécessaires à sa vérification, sans inclure clé privée ni secret. Une politique
WORM MAY être utilisée lorsqu'elle est compatible avec la résidence, la
rétention et les contrôles d'accès déclarés.

#### Scenario: Export soumis à vérification

- **WHEN** un opérateur autorisé vérifie un export scellé
- **THEN** il peut confirmer son intégrité ou obtenir une erreur explicite sans accéder aux clés privées

### Requirement: Confidentialité, rétention et droit d'effacement préservés

L'intégrité MUST NOT empêcher l'application d'une obligation légale d'effacement
ou de minimisation. Une anonymisation, un tombstone ou une preuve de retrait
MUST préserver la traçabilité déclarée sans conserver une donnée personnelle ou
un secret au-delà de la politique applicable.

#### Scenario: Effacement d'une donnée auditée

- **WHEN** une obligation d'effacement autorisée concerne un événement scellé
- **THEN** le système applique le traitement déclaré et conserve uniquement la preuve autorisée de l'opération
