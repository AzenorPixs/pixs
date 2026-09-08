# services Specification

## Purpose
Le registre de services expose les opérations synchrones des composants via des contrats versionnés, résolus de façon déterministe et traçable.

## Requirements

### Requirement: Enregistrement contractuel des services

Chaque service DOIT être enregistré avec identifiant canonique, version de contrat, composant propriétaire et garanties ; aucune implémentation privée NE DOIT être exposée comme contrat.

#### Scenario: Service privé non exposé

- **WHEN** une implémentation interne n'a pas de contrat déclaré
- **THEN** elle reste inaccessible aux autres composants avec une erreur explicite

### Requirement: Résolution déterministe du fournisseur

La sélection du fournisseur SUIT le fournisseur configuré, sinon le candidat compatible unique, sinon la composition invalide, sans dépendance à l'ordre de découverte.

#### Scenario: Ambiguïté refusée

- **WHEN** deux fournisseurs compatibles existent sans configuration
- **THEN** la résolution échoue avec un diagnostic explicite

### Requirement: Traçabilité et sécurité des appels

Chaque appel DOIT propager identité, contexte de périmètre et corrélation, et échouer fermé en cas d'autorisation ou de contexte non vérifiable, sans exposer de secret.

#### Scenario: Contexte non vérifiable

- **WHEN** l'identité ou le périmètre ne peut être vérifié
- **THEN** l'appel est refusé avec un code d'erreur stable et un audit
