## ADDED Requirements

### Requirement: Module essentiel autonome pixs.auth

Toute composition applicative Pixs MUST inclure `pixs.auth`, module essentiel indépendant de `pixs.core`, avec une capacité locale autonome sélectionnée explicitement par le profil. Son absence MUST empêcher l'activation applicative. Les fixtures structurelles non applicatives MUST rester distinguées de ce profil.

#### Scenario: Composition applicative sans Auth
- **WHEN** une composition applicative omet pixs.auth ou sa capacité locale requise
- **THEN** sa validation échoue avant activation sans annoncer d'authentification disponible

#### Scenario: Fixture structurelle isolée
- **WHEN** un test manipule seulement un contrat pur Core sans runtime applicatif
- **THEN** il reste possible sans Auth et ne constitue pas une composition applicative qualifiée

### Requirement: Autonomie locale et PostgreSQL par défaut

Le profil standard MUST fournir l'authentification locale avec PostgreSQL comme stockage persistant par défaut des données Auth. Il MUST fonctionner sans fournisseur d'identité externe, annuaire, KDC, cloud ou accès Internet obligatoire. Le provisionnement initial MUST sélectionner explicitement ce profil sans créer de justificatif universel par défaut.

#### Scenario: Installation autonome
- **WHEN** une installation provisionnée utilise seulement le profil local PostgreSQL sans source externe, annuaire ni KDC
- **THEN** connexion, déconnexion et gestion locale des sessions restent possibles selon sa politique

#### Scenario: PostgreSQL indisponible
- **WHEN** une opération exige un état Auth persistant courant et PostgreSQL est indisponible
- **THEN** elle échoue fermée sans basculer vers un annuaire, un fichier ou une session supposée valide

### Requirement: Propriété des données Auth et protection des justificatifs

pixs.auth MUST posséder ses justificatifs, liaisons d'authentification, politiques et sessions, rattachés aux identités Core par contrat public. Les mots de passe MUST être stockés uniquement sous empreinte sécurisée ; les jetons réutilisables, clés privées et secrets MFA MUST NOT être stockés en clair dans les tables métier, manifests ou journaux. Les secrets réversibles MUST suivre les contrats de protection et de secrets applicables.

#### Scenario: Session persistée
- **WHEN** Auth conserve une session ou un renouvellement
- **THEN** l'enregistrement permet expiration et révocation sans exposer le jeton brut réutilisable

#### Scenario: Liaison avec Core
- **WHEN** Auth rattache un moyen à une DigitalIdentity
- **THEN** la référence est vérifiée par contrat public sans écriture directe dans les tables Core

### Requirement: Sous-modules Auth composés par les mécanismes communs

Les méthodes locales, l'enrôlement, l'émission d'identité, les services gérés et les sources externes MUST être extensibles par composants déclarés et contrats versionnés. Les sous-modules MUST utiliser le manifest et le lifecycle communs sans registre parallèle. L'installation d'un sous-module MUST NOT suffire à activer une confiance ou un service.

#### Scenario: Source installée sans confiance
- **WHEN** un sous-module de source est installé sans configuration de confiance validée
- **THEN** il ne peut authentifier aucune identité

### Requirement: Politiques Auth déclaratives et contextualisées

Les politiques Auth MUST être typées, versionnées et résolues de façon déterministe selon plateforme, tenant et scope applicable. Méthodes, MFA, fraîcheur, sessions, récupération, sources et confiance MUST exposer leur valeur effective et leur origine aux administrateurs autorisés sans secret. Une règle contradictoire ou non résolue MUST empêcher l'opération concernée.

#### Scenario: Politique contradictoire
- **WHEN** deux règles ne permettent pas de déterminer les méthodes et le niveau requis pour un même contexte
- **THEN** Auth refuse l'opération avec un diagnostic sans sélectionner la règle la moins exigeante

### Requirement: Absence de repli implicite entre méthodes et sources

Une indisponibilité externe MUST NOT activer une authentification locale ou diminuer l'assurance requise. La coexistence des sources et méthodes MUST suivre une politique explicite et préserver la liaison canonique. Le compte de secours MUST conserver son authentification propre et son exception selon authorization et initial-administration, sans extension aux comptes ordinaires.

#### Scenario: IdP externe indisponible
- **WHEN** une politique impose un IdP externe indisponible pour un compte ordinaire
- **THEN** un mot de passe local ne devient pas un repli autorisé par cette seule panne

#### Scenario: Secours propre du Super Admin
- **WHEN** le Super Admin utilise son parcours canonique de secours sans MFA
- **THEN** son exception reste applicable sans attribuer un niveau MULTI_FACTOR non obtenu
