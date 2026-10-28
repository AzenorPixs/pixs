## ADDED Requirements

### Requirement: Installation BIND 9 par le PA du rôle serveur DNS Debian

Sur Debian, le PA désigné MUST assurer installation et configuration de BIND 9 depuis les paquets de la distribution prise en charge pour un rôle serveur DNS sélectionné et admis. Version du serveur, dépendances et contrôles MUST être identifiables et qualifiés. La présence de PBO ou d'un PA client MUST NOT autoriser cette opération ou activer le rôle serveur.

#### Scenario: Installation sous rôle et plan admissibles

- **WHEN** le PA désigné reçoit une opération courante autorisée d'installation ou de configuration du serveur DNS Debian
- **THEN** il contrôle cible, rôle, version et plan puis applique et rapporte les effets réellement établis
- **AND** une présence admissible déjà vérifiée MUST éviter une réinstallation inutile, sans valoir preuve de configuration ou de service disponible
- **AND** configuration d'instance, données mutables et secrets MUST rester séparés des artefacts immuables selon le profil

#### Scenario: PA client sans rôle serveur

- **WHEN** un PA sans rôle serveur DNS admissible demande l'installation ou l'administration de BIND 9
- **THEN** l'opération est refusée sans transformer ce PA en serveur ni contourner le contrôle par une opération locale directe

#### Scenario: Interruption ou version non qualifiée

- **WHEN** l'installation ou la mise à niveau est interrompue, incertaine ou porte une version non qualifiée pour la cible
- **THEN** l'état reste inspectable et non prêt jusqu'au rapprochement et aux validations nécessaires
- **AND** mise à niveau et reprise MUST préserver droits, révisions et résultats rapprochés, sans rejeu aveugle ni résurrection d'un état ou d'une autorité retirés
