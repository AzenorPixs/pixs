## ADDED Requirements

### Requirement: Coffre explicite et qualifié des compositions distribuées

Une composition distribuée MUST déclarer son coffre, son minimum local d’amorçage et ses politiques d’identité, disponibilité et reprise. Avant admission, elle MUST prouver isolation des accès, expiration, révocation, panne et restauration isolée avec RPO/RTO déclarés. La préparation de ce provider MUST NOT sélectionner un profil distribué ni l’imposer au profil initial Debian local.

#### Scenario: Coffre seulement déclaré dans un manifest

- **WHEN** un profil distribué référence un coffre sans preuve de panne, de révocation et de récupération de ses accès
- **THEN** sa dimension secrets reste non qualifiée et bloque l’admission de la capacité concernée

#### Scenario: Profil initial local inchangé

- **WHEN** le déploiement sélectionne uniquement le profil initial Debian local sans composition distribuée
- **THEN** ce change ne lui ajoute pas une dépendance obligatoire à un coffre distant et ses obligations d’amorçage et de protection restent applicables
