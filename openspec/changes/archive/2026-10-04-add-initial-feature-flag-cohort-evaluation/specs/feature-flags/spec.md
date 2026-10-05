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

### Requirement: Échec fermé pour le sensible

Le système MUST respecter les garanties suivantes.

Une valeur absente, invalide ou périmée MUST appliquer la politique de repli déclarée. À l'exécution, seules les politiques déclaratives DENY et DEFAULT MUST être reconnues. DENY MUST refuser l'opération sans exposer de valeur de fanion. DEFAULT MUST appliquer la valeur par défaut validée de la définition uniquement pour une fonctionnalité non sensible ; DEFAULT MUST NOT être appliqué à une permission, une mutation, une donnée protégée ou un contrat. Une permission, une mutation, une donnée protégée ou un contrat MUST être refusé sur valeur absente, invalide ou périmée, quelle que soit la politique déclarée. Une référence de repli inconnue ou incompatible MUST produire un refus sans valeur et MUST NOT être convertie en alias implicite. La classification sensible ou non sensible MUST provenir du contexte applicatif canonique côté serveur ; le client et le frontal MUST NOT fournir cette classification. Le frontal MUST faire réévaluer le fanion côté applicatif avant toute exposition protégée.

À l'instant de référence UTC fourni par le contexte applicatif canonique côté serveur, une définition dont expires_at est inférieur ou égal à cet instant MUST rendre périmées ses valeurs déjà affectées, même lorsque la fenêtre de l'affectation est encore valide ; la politique de repli déclarée MUST alors s'appliquer. L'expiration MUST bloquer les nouvelles affectations et produire un diagnostic, sans suppression implicite de code, données ou contrats.

#### Scenario: Fanion d'autorisation indisponible

- **WHEN** le fanion requis pour une mutation est indisponible
- **THEN** l'opération est refusée au lieu d'un repli permissif

#### Scenario: Repli par défaut sur fonctionnalité non sensible

- **WHEN** une valeur absente, invalide ou périmée concerne une fonctionnalité non sensible déclarée avec le repli DEFAULT
- **THEN** la valeur par défaut validée de la définition est appliquée et aucune décision d'autorisation n'en découle

#### Scenario: Référence de repli inconnue refusée

- **WHEN** un fanion déclare une référence de repli hors du vocabulaire d'exécution borné
- **THEN** l'évaluation est refusée sans exposition de valeur

#### Scenario: Affectation active sous définition expirée

- **WHEN** une affectation encore dans sa fenêtre est évaluée alors que expires_at de la définition est atteint à l'instant de référence serveur
- **THEN** la valeur affectée n'est pas exposée et la politique de repli déclarée s'applique ; toute nouvelle affectation est refusée avec un diagnostic
