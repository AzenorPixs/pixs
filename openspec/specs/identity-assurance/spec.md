# identity-assurance Specification

## Purpose
L'assurance normalise la force de l'identification, de l'authentification et de la confiance fédérée, et conditionne les opérations sensibles avec élévation explicite.

## Requirements

### Requirement: Assurance et exception Super Admin

Les contrôles d'assurance MUST s'appliquer sous réserve de l'exception Super Admin de `authorization`. Au premier démarrage et à la réactivation de secours de ce compte, le MFA MUST NOT être exigé, conformément à `initial-administration`. Les niveaux d'assurance MUST décrire les preuves réellement obtenues ; une dérogation MUST NOT augmenter artificiellement un niveau.

#### Scenario: Secours avec assurance réellement obtenue

- **WHEN** le Super Admin se réactive en secours avec son authentification propre sans MFA
- **THEN** l'absence de MFA ne bloque pas l'accès de secours et le contexte ne déclare pas MULTI_FACTOR sans preuve

### Requirement: Contexte vérifié et dimensions distinctes

Le système MUST respecter les garanties suivantes.

Toute authentification réussie produit un contexte vérifié, limité dans le temps, rattaché à une identité numérique et au périmètre applicable, avec assurance d'identité, assurance d'authentification et confiance fédérée évaluées séparément selon le mapping déclaré du fournisseur.

#### Scenario: Claim absent sans surclassement

- **WHEN** une preuve ou un claim est absent, ambigu ou expiré
- **THEN** le niveau d'assurance n'est jamais augmenté implicitement

### Requirement: Seuil sensible et élévation explicite

Le profil MUST définir l'assurance requise pour ses opérations, y compris administratives, avec MFA configurable sans obligation générale Pixs. L'opération MUST vérifier le seuil effectivement sélectionné et refuser ou demander un step-up si nécessaire. Le frontal MUST NOT simuler cette élévation et un profil MUST NOT annoncer une assurance que son chemin ne peut qualifier.

#### Scenario: Élévation exigée

- **WHEN** le profil exige une assurance supérieure à celle effectivement obtenue
- **THEN** le système refuse ou engage une élévation explicite selon le contrat.

### Requirement: Fraîcheur, révocation et récupération sans élévation implicite

Le système MUST respecter les garanties suivantes.

Expiration, fraîcheur maximale, rotation et révocation sont vérifiées avant toute décision sensible ; une récupération invalide les sessions concernées sans restaurer implicitement un niveau élevé.

#### Scenario: Récupération sans restauration d'assurance

- **WHEN** un compte est récupéré après compromission
- **THEN** les niveaux élevés restent perdus jusqu'à nouvelle preuve ou intervention autorisée

### Requirement: Vocabulaire structurel préparatoire IdentityAssurance v1

Le vocabulaire structurel préparatoire IdentityAssurance v1 MUST admettre exactement CLAIMED, VERIFIED et PROOFED. Toute autre valeur MUST être refusée. Sa représentation MUST NOT fournir de valeur par défaut, de classement ordinal, de mapping fournisseur ou de transition.

#### Scenario: Valeurs fermées sans effet

- **WHEN** Une des valeurs CLAIMED, VERIFIED ou PROOFED est représentée
- **THEN** Seul ce vocabulaire structurel est produit, sans preuve, droit, session, audit ni persistance

#### Scenario: Valeur étrangère refusée

- **WHEN** Une valeur étrangère au vocabulaire est présentée
- **THEN** La représentation est refusée sans augmentation implicite du niveau

#### Scenario: Absence sans défaut implicite

- **WHEN** Aucune valeur n’est fournie
- **THEN** Le profil ne choisit aucun niveau par défaut

### Requirement: Absence d'effets du vocabulaire IdentityAssurance v1

La représentation IdentityAssurance v1 MUST NOT établir une preuve, calculer ou augmenter une assurance, authentifier, créer une session, accorder un accès, produire un audit ou persister une donnée. Les garanties existantes de séparation des dimensions et de non-surclassement MUST rester applicables.

#### Scenario: Valeur représentée sans assurance calculée

- **WHEN** une valeur du vocabulaire IdentityAssurance v1 est représentée
- **THEN** aucune preuve, assurance calculée, authentification, session, permission, écriture d'audit ou persistance n'en découle
