# authentication Specification

## Purpose
L'authentification vérifie les identités via des fournisseurs déclarés et approuvés, sans déplacer la source de vérité des utilisateurs, groupes et appartenances hors de Pixs.

## Requirements

### Requirement: Fournisseurs déclarés et confiance explicite

Chaque fournisseur (local, OIDC, SAML) DOIT déclarer protocole, émetteurs, audiences, algorithmes, clés, claims obligatoires et mappings ; la seule validité cryptographique NE DOIT jamais suffire sans confiance applicative configurée.

#### Scenario: Émetteur non approuvé refusé

- **WHEN** un jeton valide émane d'un émetteur non approuvé
- **THEN** l'authentification est refusée avec une erreur stable et un audit

### Requirement: Identifiant externe canonique et liaison explicite

L'identifiant externe canonique est le triplet fournisseur, émetteur, sujet ; toute liaison à une identité existante est explicite, vérifiée des deux côtés, idempotente et auditée ; aucun rapprochement par courriel seul.

#### Scenario: Courriel seul non rapproché

- **WHEN** deux comptes partagent la même adresse sans preuve bilatérale
- **THEN** aucune fusion n'a lieu et une liaison explicite reste exigée

### Requirement: Sessions bornées et révocation propagée

Sessions, jetons et renouvellements sont bornés, rotatifs avec détection de réutilisation ; toute révocation d'identité, de justificatif, de session ou de confiance invalide les contextes concernés sans supprimer les données métier, avec audit sans secret.

#### Scenario: Révocation propagée

- **WHEN** une identité ou une session est révoquée
- **THEN** les contextes dérivés sont invalidés avant toute nouvelle opération sensible
