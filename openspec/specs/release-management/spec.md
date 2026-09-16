# release-management Specification

## Purpose
La gestion des releases définit ce qu'est une version livrée, ses fenêtres de support, ses chemins de mise à niveau vérifiables et ses règles de coexistence, de retour arrière et de retrait.

## Requirements

### Requirement: Définition et support d'une release

Une release MUST être définie par sa version fonctionnelle, sa source, sa composition de composants, ses manifests, ses contrats et ses dépendances ; elle MUST déclarer ses origines compatibles, ses migrations requises, ses éventuelles versions intermédiaires et ses conditions de sortie de support.

#### Scenario: Release sans déclaration de support

- **WHEN** une release est proposée sans fenêtre de support ni conditions de sortie déclarées
- **THEN** elle ne peut être publiée comme supportée et reste explicitement hors support

### Requirement: Chemin de migration vérifiable

La chaîne de migration MUST être ordonnée et vérifiable ; un saut de version n'est permis que si toutes les migrations et garanties intermédiaires sont compatibles ou explicitement regroupées dans le plan, et une version hors fenêtre de support ou sans chemin vérifiable MUST être refusée avant toute modification des données.

#### Scenario: Saut non prouvé

- **WHEN** une mise à niveau demande de sauter des versions sans garantie intermédiaire établie
- **THEN** l'opération est refusée avant modification des données avec le maillon manquant identifié

### Requirement: Mise à niveau orchestrée par prévalidations

Toute mise à niveau MUST suivre une séquence explicite de prévalidation de l'artefact et de la composition, validation des contrats, dépendances et compatibilités, validation et exécution du plan de migration, démarrage, contrôles de santé puis activation du trafic ; le plan MUST être conservé avec son résultat et les versions actives.

#### Scenario: Étape de prévalidation échouée

- **WHEN** une étape de prévalidation échoue pendant une mise à niveau
- **THEN** l'ancienne composition ou un état explicitement sûr est conservé, sans activation partielle ni purge

### Requirement: Coexistence transitoire N et N+1

Un déploiement progressif MUST préserver la compatibilité transitoire entre les versions en présence pour les API, événements, schémas et données partagés, selon une séquence d'expansion, de double compatibilité puis de contraction ; toute suppression d'un élément encore consommé MUST être différée jusqu'à la fin de la fenêtre de compatibilité.

#### Scenario: Contraction pendant la fenêtre

- **WHEN** une contraction cible un élément encore consommé par la version en place
- **THEN** elle est refusée avec la contrainte de coexistence en cause

### Requirement: Retour arrière soumis à la matrice

Le système MUST respecter les garanties suivantes.

Un retour arrière applicatif ne peut être proposé que si la matrice de compatibilité prouve que la version précédente accepte le schéma et les données actuels ; à défaut, la procédure est une restauration explicite, vérifiée et auditée ; une migration n'est jamais annulée automatiquement pour simuler un retour arrière et aucun abaissement automatique de base n'est autorisé pour masquer un échec de release.

#### Scenario: Retour arrière non garanti

- **WHEN** la matrice ne démontre pas la compatibilité de la version précédente avec l'état courant
- **THEN** le retour arrière est refusé et la voie de restauration documentée est proposée

### Requirement: Activation, retrait et instance non valide

Le contrôle d'exploitation MUST distinguer préparation, exposition, activation, retrait et retour arrière ; une instance qui échoue à ses sondes ou à ses contrôles de compatibilité ne reçoit pas de trafic et ne constitue pas une cible de retour arrière valide sans vérification du schéma et des données.

#### Scenario: Instance échouant aux contrôles

- **WHEN** une instance prête à servir échoue un contrôle de compatibilité
- **THEN** elle est tenue hors trafic dans un état diagnostiquable au lieu d'être activée silencieusement
