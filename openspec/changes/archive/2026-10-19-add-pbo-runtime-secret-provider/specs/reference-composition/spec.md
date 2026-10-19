## ADDED Requirements

### Requirement: Choix C01 systemd et exception d’amorçage du profil Debian local

Le profil pbo-p0-debian-local-v1 MUST sélectionner le transport C01 LoadCredentialEncrypted systemd avec rotation par arrêt attesté et redémarrage contrôlé. Avant disponibilité de la base Pixs et du sink C05, il MUST déclarer explicitement l’exception limitée du journal fonctionnel local d’amorçage, ses politiques et son autorisation INSTALLER.

#### Scenario: Hôte intermédiaire conservé non prêt

- **WHEN** le provider est configuré mais qu’une preuve d’identité, d’audit, de reprise ou de qualification requise manque
- **THEN** la composition reste non prête sans affaiblir les obligations C17/C18/C19

#### Scenario: Source locale hors phase autorisée

- **WHEN** le journal local est proposé comme autorité applicative après reprise complète ou pour des opérations métier ordinaires
- **THEN** la composition refuse cet usage hors de l’exception d’amorçage

### Requirement: Qualification et source de vérité après amorçage

Cette exception MUST NOT devenir une source de vérité métier parallèle après reprise dans PostgreSQL. Les architectures, versions, capacités de stockage et politiques MUST être qualifiées avant distribution ; DEVOPS.md, un test isolé ou un reçu mémoire MUST NOT valoir qualification du paquet.

#### Scenario: Hôte intermédiaire conservé non prêt

- **WHEN** le provider est configuré mais qu’une preuve d’identité, d’audit, de reprise ou de qualification requise manque
- **THEN** la composition reste non prête sans affaiblir les obligations C17/C18/C19

#### Scenario: Source locale hors phase autorisée

- **WHEN** le journal local est proposé comme autorité applicative après reprise complète ou pour des opérations métier ordinaires
- **THEN** la composition refuse cet usage hors de l’exception d’amorçage
