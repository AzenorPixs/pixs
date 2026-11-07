# Références normatives — N08

Plan ACL-PIXS-2026-10-31-E3-R1, validé ; relevé du 31 octobre 2026. Les blocs ci-dessous sont des copies de référence, jamais des deltas ADDED/MODIFIED ni une autorité indépendante du canon. Leur présence ne prouve aucune réalisation.

## Traçabilité des exigences et scénarios

| Capacité | Exigence cible | Scénarios | Référence |
|---|---|---:|---|
| brick-redundancy | Remplacement sans déplacement direct | 1 | brick-redundancy-ce67ff7e1fde |
| brick-redundancy | Mode par famille et exceptions | 1 | brick-redundancy-78e23fa4ab8f |
| brick-redundancy | Conditions de reprise propres à la brique | 1 | brick-redundancy-29e8a1e997e2 |
| brick-redundancy | Unicité de l’autorité et automatisation | 1 | brick-redundancy-b7eb34bb70c2 |
| brick-redundancy | Observation et démantèlement | 1 | brick-redundancy-8df77aef5446 |
| brick-redundancy | Compatibilité de versions par famille | 1 | brick-redundancy-73cbc72a8e34 |
| brick-redundancy | Références PostgreSQL répliquées et garanties conservées | 1 | brick-redundancy-9c403ec6ed51 |

## Blocs sources complets

### Référence brick-redundancy-ce67ff7e1fde

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 11. SHA-256 du bloc : `ce67ff7e1fde4ca9f4b7ad0badf7054c4e1fe46c1db73b174b19e30bd470ee1a`.

Scénarios sources : Second PZT.

~~~~text
### Requirement: Remplacement sans déplacement direct

Une brique MUST être remplacée par initialisation d'une seconde brique identifiée, synchronisation, vérification puis activation/reprise avant démantèlement selon ses critères. La procédure MUST NOT déplacer implicitement le processus ou copier l'identité d'un nouveau membre.

#### Scenario: Second PZT

- **WHEN** un PZT supplémentaire est initialisé pour remplacer un rôle
- **THEN** il reçoit son identité et son admission propres avant de reprendre le rôle autorisé.
~~~~

### Référence brick-redundancy-78e23fa4ab8f

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 20. SHA-256 du bloc : `78e23fa4ab8fa0bb63d03ef7d2eed6192c067b88caebb136646f31b66c88d7e2`.

Scénarios sources : Exception au mode.

~~~~text
### Requirement: Mode par famille et exceptions

Chaque famille MUST définir son mode d'autorité et de synchronisation par défaut. Une brique MAY y déroger par configuration explicite ; une exception incompatible avec le mode de famille MUST être justifiée et tracée. La dérogation MUST NOT supprimer une garantie spécifique obligatoire du rôle.

#### Scenario: Exception au mode

- **WHEN** un administrateur propose une exception de mode
- **THEN** sa justification, sa portée et ses contrôles sont enregistrés avant admission.
~~~~

### Référence brick-redundancy-29e8a1e997e2

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 29. SHA-256 du bloc : `29e8a1e997e28be127916e1f936f38f70b6562b68b46d5dab57cff4629b3a465`.

Scénarios sources : Copies requises absentes.

~~~~text
### Requirement: Conditions de reprise propres à la brique

Chaque brique MUST déclarer ses exigences de synchronisation et l'éventuel état partiel admissible avec limites explicites. La procédure MUST vérifier les critères courants avant activation. La règle générale MUST NOT abaisser le minimum PG synchrone ni permettre la perte d'une écriture confirmée dans un profil qui la protège.

#### Scenario: Copies requises absentes

- **WHEN** une reprise CZT ne satisfait pas son minimum synchrone configuré
- **THEN** la règle générale d’état partiel ne permet pas de la confirmer.
~~~~

### Référence brick-redundancy-b7eb34bb70c2

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 38. SHA-256 du bloc : `b7eb34bb70c29f74664bbd69e8874a6819b8e6ecf8a60cc8c2626164191d7f65`.

Scénarios sources : Ancien maître isolé.

~~~~text
### Requirement: Unicité de l’autorité et automatisation

Un rôle à maître unique MUST empêcher l'ancien et le nouveau maître d'exercer simultanément. La reprise MAY être automatique sous politique et mandat préalablement autorisés ; sinon un administrateur MUST confirmer. Une injoignabilité seule MUST NOT prouver l'exclusion.

#### Scenario: Ancien maître isolé

- **WHEN** l’ancien maître est injoignable mais son exclusion n’est pas démontrée
- **THEN** la prise d’autorité reste bloquée selon le contrat du rôle.
~~~~

### Référence brick-redundancy-8df77aef5446

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 47. SHA-256 du bloc : `8df77aef54469a86d9737a29a58a9b52c8f4fc211a4ac422a8bb6a1a5f8b9175`.

Scénarios sources : Nouvel actif non vérifié.

~~~~text
### Requirement: Observation et démantèlement

Chaque brique MUST définir la vérification du nouvel actif, l'éventuelle période d'observation, le statut de l'ancienne et ses critères de démantèlement. L'ancienne MAY rester secours passif, copie de retrait ou autre état déclaré ; elle MUST NOT reprendre des droits expirés ou révoqués.

#### Scenario: Nouvel actif non vérifié

- **WHEN** le service de remplacement n’a pas satisfait les contrôles
- **THEN** le démantèlement n’est pas autorisé sur sa seule activation administrative.
~~~~

### Référence brick-redundancy-73cbc72a8e34

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 56. SHA-256 du bloc : `73cbc72a8e34d14d7ef69dc78d17ffb7d5f3c0e0fcfd1898d8a241e4867f752c`.

Scénarios sources : Versions hors plage.

~~~~text
### Requirement: Compatibilité de versions par famille

Chaque famille MUST déclarer si des versions identiques sont requises ou si une plage de compatibilité est admise. Une paire non qualifiée MUST être refusée pour synchronisation/reprise ; la présence des binaires MUST NOT prouver la compatibilité.

#### Scenario: Versions hors plage

- **WHEN** une réplique est installée dans une version non admise
- **THEN** la synchronisation protégée ou la reprise concernée reste bloquée avec diagnostic.
~~~~

### Référence brick-redundancy-9c403ec6ed51

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 65. SHA-256 du bloc : `9c403ec6ed51a5c3ebdc3db0b60ff70c1382311adacdd6a3fc42fdc997c6fd23`.

Scénarios sources : Copies distinctes.

~~~~text
### Requirement: Références PostgreSQL répliquées et garanties conservées

Les bases PG Instance, Domaine, CZT, DZT et PKIZT MUST pouvoir disposer de répliques synchrones avec un primaire d'écriture unique. Leur minimum de confirmations MUST être configurable sans réduction automatique en panne ; promotion MUST exclure l'ancien primaire et préserver les écritures confirmées. Une réplication MUST rester celle d'une même base logique sans fusion de Domaines.

#### Scenario: Copies distinctes

- **WHEN** deux PG de Domaines différents sont déclarées
- **THEN** elles ne deviennent pas répliques d’une même base par partage de serveur ou de ZT.
~~~~
