## MODIFIED Requirements

### Requirement: Génération déterministe depuis les contrats

Les kits TypeScript et Python MUST être générés depuis OpenAPI, contrats événementiels et schémas publics avec dépendances verrouillées et matrice de compatibilité ; toute divergence bloque la génération.

#### Scenario: Divergence contrat-kit bloquée

- **WHEN** un kit généré diffère du contrat publié
- **THEN** la génération échoue au lieu de publier un client partiel

### Requirement: Propagation du contexte et erreurs typées

Les clients MUST propager identité fournie, contextes de tenant et de périmètre, corrélation et idempotence, et exposer pagination, opérations asynchrones, opérations en masse et erreurs typées sans transformer un traitement en cours en succès acquis.

#### Scenario: Périmètre non élargi par le client

- **WHEN** un appel fournit un périmètre hors autorisation
- **THEN** le serveur refuse et le client expose l'erreur typée sans réessai implicite

### Requirement: Outillage validé sans secret

Le kit, l'interface en ligne, les exemples et les tests de conformité réutilisent les validateurs de manifests et de compatibilité, sans créer implicitement identité, donnée ou secret de production ; le navigateur MUST NOT persister jetons ou justificatifs par défaut.

#### Scenario: Exemple sans secret

- **WHEN** un exemple ou un journal contiendrait un jeton ou une donnée de production
- **THEN** sa publication est refusée
