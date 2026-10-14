# feature-flags — Delta

## MODIFIED Requirements

### Requirement: Ciblage et cohorte déterministes

Le système MUST respecter les garanties suivantes.

L'évaluation utilise uniquement les dimensions déclarées (installation, environnement, tenant, scope enfant) avec priorité du général au spécifique et cohorte stable sans tirage par requête.

Une cohorte progressive MUST être résolue par une règle déclarative côté serveur, distincte de la définition du fanion, contenant cohort_key, subject_dimension, threshold_basis_points et configuration_version. subject_dimension MUST être l'une des dimensions déclarées du fanion parmi INSTALLATION, ENVIRONMENT, TENANT ou SCOPE ; son identité MUST provenir du contexte applicatif canonique côté serveur, sans ciblage individuel ni élargissement implicite de tenant ou de scope. threshold_basis_points MUST être un entier compris entre 0 et 10000 inclus. Pour une même clé, une même dimension et une même identité canonique, le calcul MUST fournir le même bucket compris entre 0 et 9999 ; il MUST NOT dépendre de l'instant de requête, du seuil ou d'un tirage aléatoire. Le sujet MUST appartenir à la cohorte exactement lorsque bucket est strictement inférieur à threshold_basis_points. Avant toute évaluation d'affectation soumise à une cohorte, la configuration et l'identité du sujet MUST être validées. Une clé non résolue, une règle invalide, une identité absente ou une version incompatible avec la configuration canonique attendue MUST refuser cette évaluation avant la sélection de valeur et MUST NOT introduire un défaut implicite de configuration. Pour une règle valide, un sujet hors cohorte MUST exclure la valeur affectée et appliquer le repli R3 pour la cause ABSENT ; cette décision MUST NOT constituer une permission. Un fanion sans cohort_key MUST conserver son évaluation sans cohorte.

#### Scenario: Même contexte même décision

- **WHEN** le même contexte est évalué deux fois
- **THEN** le résultat est identique

#### Scenario: Bornes du déploiement progressif

- **WHEN** une règle de cohorte valide est évaluée sur une identité canonique avec un seuil de 0 ou de 10000 points de base
- **THEN** respectivement aucun sujet ou tout sujet valide appartient à la cohorte, sans décision d'autorisation implicite

#### Scenario: Sujet hors cohorte

- **WHEN** le bucket stable d'un sujet valide est supérieur ou égal au seuil déclaré
- **THEN** la valeur affectée n'est pas exposée et le repli R3 pour ABSENT s'applique, avec refus pour le sensible

#### Scenario: Configuration de cohorte indisponible

- **WHEN** la clé ne se résout pas, la règle est invalide, l'identité manque ou la version est incompatible avec la configuration canonique attendue
- **THEN** l'évaluation est refusée sans valeur et sans défaut implicite
