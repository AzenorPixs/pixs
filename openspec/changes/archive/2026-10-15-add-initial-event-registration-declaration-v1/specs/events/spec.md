## MODIFIED Requirements

### Requirement: Profil préparatoire de déclaration d'enregistrement d'événement v1

Le profil `EventRegistrationDeclarationV1` MUST être figé et contenir uniquement `owner_id`, `entry_id` et `event_contract`. Les deux identifiants MUST être des chaînes exactes non vides, sans coercition ni normalisation ; `event_contract` MUST être un objet exact `DomainEventContract` ou `IntegrationEventContract` existant, sans copie de leurs cinq champs.

#### Scenario: Déclaration passive de contrat de domaine

- **WHEN** une déclaration fournit les trois champs et un contrat de domaine structurellement valide
- **THEN** sa validation structurelle réussit sans enregistrer ni publier un événement

#### Scenario: Contrat d'intégration distinct

- **WHEN** le champ `event_contract` porte un objet exact `IntegrationEventContract`
- **THEN** sa nature distincte est conservée sans substitution par un contrat de domaine

### Requirement: Validation fermée de la déclaration d'enregistrement v1

La validation MUST refuser les types étrangers, sous-classes et valeurs invalides sans coercition ; elle MUST réutiliser les validateurs structurels existants du contrat porté. Les refus MUST produire des diagnostics `VALIDATE` existants, stables et triés, sans écho des valeurs brutes, sans IO ni exécution de callback fourni par l'appelant.

#### Scenario: Référence ou type étranger refusé

- **WHEN** un identifiant est vide, non exactement une chaîne, ou un objet de déclaration ou de contrat est étranger au profil
- **THEN** la validation refuse l'entrée avec des diagnostics sans valeur brute et sans effet

#### Scenario: Contrat porté invalide

- **WHEN** un contrat de domaine ou d'intégration exact ne satisfait pas son validateur structurel existant
- **THEN** la déclaration est refusée sans réinterpréter les champs ni affaiblir la validation du contrat

### Requirement: Frontière préparatoire de la déclaration d'enregistrement v1

Cette validation MUST rester seulement structurelle : elle ne prouve ni propriétaire admis, existence, résolution, légitimité ou sensibilité d'une référence. Elle MUST NOT réaliser d'enregistrement, d'abonnement, de publication ou de livraison, ni ouvrir le registre d'événements P0 ; sa réussite MUST NOT être présentée comme un bus d'exécution livré.

#### Scenario: Validité structurelle sans admission runtime

- **WHEN** une déclaration satisfait le profil préparatoire
- **THEN** les refus d'admission du registre P0 et les garanties existantes après commit, au-moins-une-fois, d'idempotence et d'ordre déclaré restent inchangés
