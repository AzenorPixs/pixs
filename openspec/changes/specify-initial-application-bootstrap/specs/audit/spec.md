## ADDED Requirements

### Requirement: Audit exhaustif du panneau d'administration

Toute activité du panneau d'administration MUST produire un audit persistant :
connexion, déconnexion, lecture, navigation entre affichages, création,
modification, suppression, refus, changement de configuration, de route ou de
marqueur externe. Une action administrative qui ne peut pas produire cet audit
MUST être refusée. La politique d'audit MUST déclarer l'événement minimal, la
rétention, l'intégrité, les droits de consultation et la capacité de traitement
requise pour cette volumétrie.

#### Scenario: Navigation non auditable

- **WHEN** le panneau ne peut pas persister l'événement de navigation demandé
- **THEN** il refuse l'accès à l'affichage concerné sans exposer de donnée
  sensible
