# brick-redundancy Specification

## Purpose

Le remplacement d'une brique Pixs procède par une nouvelle installation synchronisée et une reprise d'activité ou d'autorité.

Cible documentaire du cadrage validé du 31 octobre 2026 (PROJECT.md §45, TECHNICAL.md §46 et BUILD.md §49). Cette spécification ne constitue pas une implémentation ni une qualification de plateforme.

## Requirements

### Requirement: Remplacement sans déplacement direct

Une brique MUST être remplacée par initialisation d'une seconde brique identifiée, synchronisation, vérification puis activation/reprise avant démantèlement selon ses critères. La procédure MUST NOT déplacer implicitement le processus ou copier l'identité d'un nouveau membre.

#### Scenario: Second PZT

- **WHEN** un PZT supplémentaire est initialisé pour remplacer un rôle
- **THEN** il reçoit son identité et son admission propres avant de reprendre le rôle autorisé.

### Requirement: Mode par famille et exceptions

Chaque famille MUST définir son mode d'autorité et de synchronisation par défaut. Une brique MAY y déroger par configuration explicite ; une exception incompatible avec le mode de famille MUST être justifiée et tracée. La dérogation MUST NOT supprimer une garantie spécifique obligatoire du rôle.

#### Scenario: Exception au mode

- **WHEN** un administrateur propose une exception de mode
- **THEN** sa justification, sa portée et ses contrôles sont enregistrés avant admission.

### Requirement: Conditions de reprise propres à la brique

Chaque brique MUST déclarer ses exigences de synchronisation et l'éventuel état partiel admissible avec limites explicites. La procédure MUST vérifier les critères courants avant activation. La règle générale MUST NOT abaisser le minimum PG synchrone ni permettre la perte d'une écriture confirmée dans un profil qui la protège.

#### Scenario: Copies requises absentes

- **WHEN** une reprise CZT ne satisfait pas son minimum synchrone configuré
- **THEN** la règle générale d’état partiel ne permet pas de la confirmer.

### Requirement: Unicité de l’autorité et automatisation

Un rôle à maître unique MUST empêcher l'ancien et le nouveau maître d'exercer simultanément. La reprise MAY être automatique sous politique et mandat préalablement autorisés ; sinon un administrateur MUST confirmer. Une injoignabilité seule MUST NOT prouver l'exclusion.

#### Scenario: Ancien maître isolé

- **WHEN** l’ancien maître est injoignable mais son exclusion n’est pas démontrée
- **THEN** la prise d’autorité reste bloquée selon le contrat du rôle.

### Requirement: Observation et démantèlement

Chaque brique MUST définir la vérification du nouvel actif, l'éventuelle période d'observation, le statut de l'ancienne et ses critères de démantèlement. L'ancienne MAY rester secours passif, copie de retrait ou autre état déclaré ; elle MUST NOT reprendre des droits expirés ou révoqués.

#### Scenario: Nouvel actif non vérifié

- **WHEN** le service de remplacement n’a pas satisfait les contrôles
- **THEN** le démantèlement n’est pas autorisé sur sa seule activation administrative.

### Requirement: Compatibilité de versions par famille

Chaque famille MUST déclarer si des versions identiques sont requises ou si une plage de compatibilité est admise. Une paire non qualifiée MUST être refusée pour synchronisation/reprise ; la présence des binaires MUST NOT prouver la compatibilité.

#### Scenario: Versions hors plage

- **WHEN** une réplique est installée dans une version non admise
- **THEN** la synchronisation protégée ou la reprise concernée reste bloquée avec diagnostic.

### Requirement: Références PostgreSQL répliquées et garanties conservées

Les bases PG Instance, Domaine, CZT, DZT et PKIZT MUST pouvoir disposer de répliques synchrones avec un primaire d'écriture unique. Leur minimum de confirmations MUST être configurable sans réduction automatique en panne ; promotion MUST exclure l'ancien primaire et préserver les écritures confirmées. Une réplication MUST rester celle d'une même base logique sans fusion de Domaines.

#### Scenario: Copies distinctes

- **WHEN** deux PG de Domaines différents sont déclarées
- **THEN** elles ne deviennent pas répliques d’une même base par partage de serveur ou de ZT.
