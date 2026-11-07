# auth-managed-active-directory Specification

## Purpose

La compatibilité de jonction native Windows et GPO est un objectif du même Domaine Pixs, à qualifier avec ses autorités PG/OpenLDAP/MIT Kerberos.

Cible documentaire du cadrage validé du 31 octobre 2026 ; les contrats proposés existants de cette capacité sont à réconcilier avec ce référentiel avant réalisation. Aucun fournisseur ni plateforme n’est réputé qualifié par cette rédaction.

## Requirements

### Requirement: Domaine Pixs commun et objectif Windows V1

La V1 MUST prévoir la jonction native des postes Windows et les politiques de type GPO dans le même Domaine Pixs. La compatibilité MUST être démontrée avec PG source Core, LZT/OpenLDAP et KZT/MIT Kerberos ; une seconde autorité incompatible pour le même realm MUST NOT être introduite par déduction.

#### Scenario: Fournisseur compatible AD proposé

- **WHEN** un fournisseur utilise un autre annuaire ou mécanisme Kerberos
- **THEN** son articulation doit être qualifiée avant toute sélection sans déclarer automatiquement l’assemblage conforme.

### Requirement: Produit et capacité démontrés avant activation

Le fournisseur compatible AD, ses dépendances et ses garanties MUST être explicitement sélectionnés et qualifiés avant activation. La présence d'un paquet ou une documentation de protocole MUST NOT prouver sa compatibilité avec les autorités Pixs. Une capacité non démontrée MUST rester indisponible sans changement silencieux du modèle.

#### Scenario: Paquet disponible seul

- **WHEN** un paquet de contrôleur est disponible mais aucune recette de l’assemblage n’existe
- **THEN** la jonction native n’est pas déclarée disponible.

### Requirement: Jonction et politiques depuis PBO

La jonction Windows MUST être orchestrée depuis PBO avec préparation et exécution autorisées PA et intégration ZT préalable. L'administration des GPO MUST passer par PBO en V1. Les politiques MUST suivre managed-device-policies sans déléguer les décisions métier au contrôleur natif.

#### Scenario: Jonction sans ZT

- **WHEN** un poste tente une jonction avant intégration ZT
- **THEN** le parcours est bloqué jusqu’à satisfaction du prérequis.

### Requirement: Éditions et périmètre Windows

Le profil V1 MUST qualifier Windows 10/11 dans les éditions autorisant la jonction native ; Home MUST NOT être déclarée admissible à cette jonction. Windows Server MUST rester hors périmètre des membres natifs V1 ; son éventuel déploiement PA/PZT MUST être évalué séparément.

#### Scenario: PA sur serveur Windows

- **WHEN** un profil PA/PZT pour Windows Server est examiné
- **THEN** il ne confère pas la jonction native V1 et n’est pas exclu par cette seule décision.
