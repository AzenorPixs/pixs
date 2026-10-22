## ADDED Requirements

### Requirement: Résolution technique après INSTALLER explicitement autorisée

Après INSTALLER, le provider systemd C01 MUST résoudre les références uniquement pour les modes FIRST_CONFIGURATION, NORMAL ou MAINTENANCE expressément autorisés par une politique versionnée liant workload, UID, unité, rôle, finalité, scope, références, versions et bornes. Il MUST conserver les preuves natives, le transport LoadCredentialEncrypted et les règles de rotation/révocation. Un mode MUST NOT être réétiqueté INSTALLER.

#### Scenario: Mode et workload courants autorisés

- **WHEN** un workload dont les preuves natives sont valides demande une référence dans un mode, rôle et finalité autorisés par sa politique courante
- **THEN** la résolution suit cette politique et conserve ses contrôles de validité, de révocation et d’audit

#### Scenario: Mode ou finalité absent de la politique

- **WHEN** une référence existe mais que le mode, le workload ou la finalité ne correspond pas à la politique vérifiée
- **THEN** la remise de valeur est refusée sans secret ni repli vers INSTALLER

### Requirement: Continuité auditée du démarrage avant PostgreSQL

Avant disponibilité de PostgreSQL, la résolution technique MUST disposer d’un audit durable indépendant de cette base, lié à l’invocation et au workload vérifiés. Après ouverture, le relais vers C05 MUST être idempotent et rapproché avant disponibilité applicative. Une preuve absente ou une issue inconnue MUST garder le composant non prêt. Cet audit MUST NOT conférer de droit métier ou R01.

#### Scenario: Audit requis indisponible avant base

- **WHEN** une résolution de démarrage ne peut pas confirmer son audit durable avant disponibilité de PostgreSQL
- **THEN** aucune valeur ni disponibilité applicative n’est annoncée

#### Scenario: Crash pendant le relais vers C05

- **WHEN** un démarrage reprend après un import partiel des événements de son invocation
- **THEN** il inspecte et réconcilie le relais sans événement dupliqué ni disponibilité avant confirmation

### Requirement: Remise de connexion PBO indépendante de la base à ouvrir

La remise de connexion au workload PBO MUST être vérifiée sans dépendance circulaire à Auth PostgreSQL, sous la branche technique explicite de authorization. Le provider MUST contrôler identité native, politique courante, mode, cible, références, versions, validité, révocation et audit. La publication externe et les garanties de non-divulgation et de cycle de vie ci-dessous MUST rester obligatoires.

#### Scenario: Garanties de la remise technique de connexion

- **WHEN** le profil sélectionne cette capacité pour le parcours de préparation PostgreSQL
- **THEN** Pour le parcours PA/PZT PostgreSQL, la remise des secrets de connexion au workload PBO MUST suivre la branche technique explicite de authorization et être vérifiable sans dépendre de la base Pixs à ouvrir. Le provider MUST vérifier les preuves natives d'identité du consommateur et la politique protégée courante liant mode, rôle, finalité de connexion, cible, références, versions et bornes. Le provisionnement opérateur et PA MUST utiliser une publication externe contrôlée distincte du provider de lecture ; PA MUST NOT devenir writer générique par sa seule capacité de préparation. Aucun credential MUST transiter dans les messages de management PBO–PA ; ils MUST porter seulement références et métadonnées minimisées. Les valeurs MUST être remises par le mécanisme de secrets sélectionné au seul consommateur autorisé, sans persistance dans artefact, journal ou checkpoint. Une indisponibilité, rotation ou révocation MUST conserver l'échec fermé et le cycle de vie des copies. L'audit durable pré-base et son relais C05 idempotent MUST être rapprochés avant disponibilité. LoadCredentialEncrypted reste le choix du profil Debian local ; cette règle MUST NOT déclarer le transport Docker qualifié ni choisir silencieusement un nouveau provider.

#### Scenario: Redémarrage sans Auth disponible

- **WHEN** PBO redémarre avec sa base fermée et des références de connexion publiées pour son workload courant
- **THEN** le provider évalue la politique native sans appel préalable à Auth sur cette base et remet seulement les valeurs autorisées au consommateur vérifié

#### Scenario: Référence présente sans remise admissible

- **WHEN** une référence existe mais sa publication, son consommateur, sa politique courante ou sa version ne peut être vérifiée
- **THEN** le démarrage reste non prêt sans secret dans un message PZT et sans repli INSTALLER
