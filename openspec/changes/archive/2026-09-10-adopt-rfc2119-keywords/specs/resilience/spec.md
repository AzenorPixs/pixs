## MODIFIED Requirements

### Requirement: Isolation des défaillances optionnelles

La défaillance d'un fournisseur ou d'une intégration optionnelle MUST NOT rendre Pixs indisponible lorsqu'un fonctionnement dégradé cohérent reste possible ; chaque composant expose HEALTHY, DEGRADED, FAILED ou DISABLED.

#### Scenario: Fournisseur optionnel en panne isolé

- **WHEN** un fournisseur optionnel échoue sans compromettre les invariants
- **THEN** le périmètre passe en DEGRADED diagnostiqué et le reste reste disponible

### Requirement: Dégradation sans affaiblissement sécurité

Un mode dégradé MUST NOT affaiblir une frontière de sécurité ; toute autorisation, signature ou contexte non vérifiable échoue fermé même en mode dégradé.

#### Scenario: Dégradé sans permissivité

- **WHEN** un contrôle de sécurité est invérifiable en mode dégradé
- **THEN** l'opération protégée est refusée au lieu d'un accès permissif

### Requirement: Révocation et diagnostic des compromissions

Composants, fournisseurs, jetons et points d'accès compromis MUST pouvoir être révoqués explicitement ; blocages, révocations et réactivations sont diagnostiquables et auditables sans exposer de secret.

#### Scenario: Composant compromis bloqué

- **WHEN** un composant est signalé compromis
- **THEN** il est bloqué ou désactivé via une procédure d'urgence distincte du cycle normal
