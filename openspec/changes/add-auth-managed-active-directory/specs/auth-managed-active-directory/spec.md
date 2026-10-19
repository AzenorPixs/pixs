## ADDED Requirements

### Requirement: Sous-module Active Directory propre optionnel

Le sous-module `pixs.auth.directory.ad` MUST permettre de provisionner, configurer, démarrer, arrêter et superviser un service Active Directory propre selon une implémentation et un profil qualifiés. Son activation MUST être explicite. Il MUST rester non requis et non activé dans le profil autonome PostgreSQL standard, sans dépendance à un connecteur externe.

#### Scenario: Domaine propre sélectionné

- **WHEN** un plan autorisé sélectionne le sous-module et satisfait ses prérequis
- **THEN** Auth peut gérer le service propre sans installer de connecteur vers un domaine tiers

#### Scenario: Installation locale sans AD

- **WHEN** le profil autonome standard est installé sans service AD
- **THEN** son authentification PostgreSQL reste utilisable et aucune activation AD n'est déduite

### Requirement: Référentiel PostgreSQL et domaine technique distincts

PostgreSQL MUST être le stockage Auth par défaut et la référence Core sauf migration engagée vers OpenLDAP interne selon core-storage. AD MUST déclarer son stockage natif et son autorité de domaine sans remplacer le référentiel Core sélectionné. Les flux et objets gérés MUST être explicites ; une mutation AD MUST NOT modifier implicitement une primitive Core.

#### Scenario: Modification directe dans le domaine

- **WHEN** un objet AD est modifié sans Command Core ni flux entrant autorisé
- **THEN** aucune identité ou permission Core n'est modifiée par simple observation de cet objet

### Requirement: Identifiants de domaine liés explicitement à Core

Les comptes, SID, objectGUID et principals AD gérés MUST être associés par mappings persistants explicites aux identités et périmètres Pixs applicables. Ces identifiants MUST NOT remplacer l'UUID Core ni conférer un rôle Pixs par correspondance de nom ou appartenance de domaine.

#### Scenario: Compte administrateur du domaine

- **WHEN** un compte AD porte un rôle de domaine privilégié sans autorisation Pixs correspondante
- **THEN** ce rôle ne lui attribue ni Super Admin Pixs ni accès à un tenant non accordé

### Requirement: Composition coordonnée des services de domaine

Le plan AD MUST déclarer responsabilités annuaire, Kerberos et DNS, placement, noms et ports. Il MUST vérifier la coexistence avec les services OpenLDAP/KDC/DNS sélectionnés. L'activation AD MUST NOT démarrer implicitement un service autonome supplémentaire ni créer un trust ou adopter un domaine existant.

#### Scenario: Collision de service

- **WHEN** un service AD et un service déjà sélectionné revendiquent le même endpoint ou une propriété DNS incompatible
- **THEN** l'activation concernée est refusée avant modification du service existant

#### Scenario: Domaine existant découvert

- **WHEN** la découverte révèle un domaine AD existant hors du plan autorisé
- **THEN** aucun rattachement, trust, adoption ou changement de configuration n'est engagé

### Requirement: Moyens et secrets AD sous contrôle déclaré

Les credentials de domaine, clés et moyens de récupération MUST être protégés selon les contrats de secrets, sous identités techniques minimales. Les moyens AD MUST être enrôlés par un mécanisme qualifié sans conversion supposée d'une empreinte Pixs. Les valeurs secrètes MUST NOT être exposées dans tables métier en clair, manifests, journaux ou diagnostics.

#### Scenario: Enrôlement depuis une empreinte locale

- **WHEN** un plan suppose qu'un hash local suffit à créer un justificatif AD compatible
- **THEN** le plan est refusé jusqu'à définition d'un mécanisme d'enrôlement qualifié

### Requirement: Révocation et restauration du domaine vérifiables

Le service AD MUST déclarer les bornes de révocation et leurs effets sur émissions, sessions Pixs et clients tiers. Un ticket valide MUST NOT contourner l'état Core courant avant opération sensible. Avant réadmission après restauration, retraits, mappings, générations et confiance MUST être réconciliés sans réactiver implicitement un accès.

#### Scenario: Ticket valide après révocation Core

- **WHEN** une identité révoquée présente un ticket de domaine non expiré pour une opération sensible Pixs
- **THEN** le contrôle de l'état courant refuse l'opération selon les garanties et exceptions applicables sans déduire un droit du ticket

#### Scenario: Restauration antérieure au retrait

- **WHEN** une sauvegarde de domaine contient un compte ou une confiance retiré depuis
- **THEN** la réadmission reste bloquée pour les accès concernés avant réconciliation de l'état courant
