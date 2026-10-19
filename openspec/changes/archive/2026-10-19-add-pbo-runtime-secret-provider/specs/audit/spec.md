## ADDED Requirements

### Requirement: Exception de persistance limitée à l’audit d’amorçage C01

Avant disponibilité de la base Pixs et du sink propriétaire C05, le profil C01 MUST utiliser un journal fonctionnel local temporaire distinct des logs techniques, hors dépôt et artefacts distribués. Cette exception à la persistance applicative PostgreSQL MUST être limitée aux événements techniques d’amorçage INSTALLER autorisés. Le journal MUST NOT contenir de valeur de secret ni devenir une autorité métier parallèle après la reprise. Le Kernel MUST rester déclaratif.

#### Scenario: Audit avant existence des sessions

- **WHEN** une résolution technique autorisée est requise avant disponibilité de la base et des sessions Pixs
- **THEN** son événement est conservé dans le journal d’amorçage sans dépendre d’une session applicative ni exposer le secret

#### Scenario: Usage métier hors amorçage refusé

- **WHEN** une demande veut employer ce journal comme stockage métier ordinaire ou hors du périmètre INSTALLER
- **THEN** la demande est refusée sans extension implicite de cette exception

### Requirement: Enregistrement et reçu exacts du journal d’amorçage v1

BootstrapAuditRecordV1 MUST contenir exactement schema_version égal à 1, journal_id UUIDv7, sequence entier exact supérieur ou égal à 1, event et event_sha256. event MUST conserver les treize champs d’AuditEvent existant, avec event_id UUIDv7. L’événement MUST contenir uniquement des références de confiance et des résultats ou raisons minimisés, jamais de secret.

#### Scenario: Reçu lié à l’événement

- **WHEN** un événement conforme reçoit un acquittement durable
- **THEN** le reçu désigne son journal, son identifiant, sa séquence et son empreinte exacts

#### Scenario: Structure ou identifiant étranger

- **WHEN** un enregistrement ajoute un champ, emploie un identifiant non UUIDv7 ou un événement invalide
- **THEN** il est refusé sans coercition ni écho d’une valeur brute

### Requirement: Contexte PLATFORM et reçu exact d’amorçage

Le contexte MUST être explicitement PLATFORM sans tenant_id ni scope_id et MUST NOT valoir permission. BootstrapAuditReceiptV1 MUST contenir exactement journal_id, event_id, sequence et event_sha256.

#### Scenario: Reçu lié à l’événement

- **WHEN** un événement conforme reçoit un acquittement durable
- **THEN** le reçu désigne son journal, son identifiant, sa séquence et son empreinte exacts

#### Scenario: Structure ou identifiant étranger

- **WHEN** un enregistrement ajoute un champ, emploie un identifiant non UUIDv7 ou un événement invalide
- **THEN** il est refusé sans coercition ni écho d’une valeur brute

### Requirement: Sérialisation déterministe et empreinte bornée v1

L’événement MUST être sérialisé en JSON UTF-8 strict, avec clés triées, séparateurs compacts, tableaux JSON pour les tuples de corrélation et causalité, sans normalisation Unicode, coercition, valeur non finie ou objet supplémentaire. event_sha256 MUST être le SHA-256 hexadécimal minuscule du seul événement ainsi sérialisé.

#### Scenario: Même événement même empreinte

- **WHEN** le même événement conforme est sérialisé deux fois
- **THEN** les octets et l’empreinte sont identiques sans transformation de ses références

#### Scenario: Capacité absente ou dépassée

- **WHEN** une limite obligatoire manque ou que l’enregistrement excède la capacité admise
- **THEN** l’ajout est refusé sans troncature ni suppression d’un événement existant

### Requirement: Portée de l’empreinte et capacité du journal

Cette empreinte MUST NOT être présentée comme une signature, JCS, une protection contre un administrateur privilégié ou une preuve contre la restauration d’un état ancien. Les limites de taille événement et journal MUST être explicites, positives et sans défaut numérique.

#### Scenario: Même événement même empreinte

- **WHEN** le même événement conforme est sérialisé deux fois
- **THEN** les octets et l’empreinte sont identiques sans transformation de ses références

#### Scenario: Capacité absente ou dépassée

- **WHEN** une limite obligatoire manque ou que l’enregistrement excède la capacité admise
- **THEN** l’ajout est refusé sans troncature ni suppression d’un événement existant

### Requirement: Append durable et exclusion des écrivains d’amorçage

Le backend MUST vérifier le propriétaire OS, les permissions minimales, le répertoire configuré et un fichier régulier sans suivi de lien symbolique. La création MUST être exclusive sans troncature. Les écritures normales MUST être append-only sous exclusion OS non bloquante portée par un objet stable distinct ; cette exclusion consultative MUST NOT remplacer les protections d’accès.

#### Scenario: Deux écrivains

- **WHEN** deux processus demandent simultanément l’accès exclusif au même journal
- **THEN** un seul écrit et l’autre reçoit un refus explicite sans ajout partiel

#### Scenario: Synchronisation échouée

- **WHEN** l’écriture ou la synchronisation obligatoire échoue
- **THEN** aucun reçu durable n’est annoncé et aucune remise de secret ordinaire n’est autorisée

### Requirement: Acquittement durable du journal d’amorçage

Un reçu MUST être émis seulement après écriture complète et synchronisation réussie du fichier, ainsi que du répertoire lors de la création. Un booléen de callback MUST NOT constituer cette preuve.

#### Scenario: Deux écrivains

- **WHEN** deux processus demandent simultanément l’accès exclusif au même journal
- **THEN** un seul écrit et l’autre reçoit un refus explicite sans ajout partiel

#### Scenario: Synchronisation échouée

- **WHEN** l’écriture ou la synchronisation obligatoire échoue
- **THEN** aucun reçu durable n’est annoncé et aucune remise de secret ordinaire n’est autorisée

### Requirement: Idempotence et incertitude du journal d’amorçage

Les séquences MUST être strictement croissantes dans le journal. Un event_id déjà présent avec contenu et empreinte identiques MUST être réconcilié avec son reçu durable sans ajout dupliqué ; un contenu divergent MUST être refusé. Une fin partielle, une corruption, une saturation, une perte d’acquittement ou un effet incertain MUST être conservé et réconcilié avant toute suite incompatible.

#### Scenario: Réponse perdue après écriture

- **WHEN** l’écriture a réussi mais que son reçu n’est plus disponible au demandeur
- **THEN** la consultation réconcilie le même événement sans nouvel ajout ni succès inventé

#### Scenario: Fin partielle conservée

- **WHEN** une interruption laisse une fin d’enregistrement non validable
- **THEN** la suite est refusée et les octets existants sont préservés pour réconciliation explicite

### Requirement: Préservation du journal sans réparation implicite

Le backend MUST NOT tronquer, purger, recréer ou rejouer implicitement le journal pour masquer cette situation.

#### Scenario: Réponse perdue après écriture

- **WHEN** l’écriture a réussi mais que son reçu n’est plus disponible au demandeur
- **THEN** la consultation réconcilie le même événement sans nouvel ajout ni succès inventé

#### Scenario: Fin partielle conservée

- **WHEN** une interruption laisse une fin d’enregistrement non validable
- **THEN** la suite est refusée et les octets existants sont préservés pour réconciliation explicite

### Requirement: Audit avant remise et absence de Super Admin présumé

Les résolutions, refus, rotations et révocations C01 MUST être auditables avec identité vérifiée, référence, composant/version et corrélation, sans valeur sensible. Une résolution ordinaire MUST NOT remettre le secret si l’événement requis ne possède pas de reçu durable vérifiable. Un échec d’audit MUST échouer fermé sans divulgation. Root OS MUST NOT être assimilé au Super Admin applicatif.

#### Scenario: Audit indisponible avant base

- **WHEN** une résolution technique ordinaire ne peut pas obtenir son reçu d’audit durable
- **THEN** la remise du secret est refusée sans prétendre disposer d’une dérogation Super Admin

### Requirement: Dérogations d’audit sans privilège présumé

Le backend MUST NOT inventer une dérogation de ce compte avant son existence et son contexte vérifié. Les exceptions canoniques existantes MUST rester limitées à leur périmètre.

#### Scenario: Audit indisponible avant base

- **WHEN** une résolution technique ordinaire ne peut pas obtenir son reçu d’audit durable
- **THEN** la remise du secret est refusée sans prétendre disposer d’une dérogation Super Admin

### Requirement: Scellement et transfert propriétaire vers PostgreSQL

Le journal MUST distinguer OPEN pour les ajouts autorisés et SEALED pour la reprise ordonnée seule. Après disponibilité de PostgreSQL et du sink C05, le transfert MUST conserver l’ordre, les identifiants et les empreintes, être idempotent par event_id et empreinte, et être acquitté par la preuve du commit propriétaire. Une preuve structurelle ou un callback mémoire MUST NOT suffire.

#### Scenario: Reprise incomplète

- **WHEN** le journal est scellé mais que le commit propriétaire de sa reprise complète n’est pas prouvé
- **THEN** aucun ajout ordinaire ni admission finale n’est accordé et les données restent conservées

### Requirement: Admission après reprise d’audit prouvée

Avant reprise complète prouvée, le composant MUST NOT annoncer une conformité d’audit P0 ni une admission finale C07/C08. Ce contrat MUST NOT présenter C05/C08 comme implémentés.

#### Scenario: Reprise incomplète

- **WHEN** le journal est scellé mais que le commit propriétaire de sa reprise complète n’est pas prouvé
- **THEN** aucun ajout ordinaire ni admission finale n’est accordé et les données restent conservées

### Requirement: Conservation contrôlée du journal d’amorçage

La politique de rétention et les holds applicables MUST être explicites. Le journal repris MUST être conservé selon cette politique ; une importation réussie MUST NOT déclencher sa suppression automatique. Toute suppression ou minimisation MUST relever d’une procédure distincte, autorisée et auditable. L’absence d’une politique vérifiable MUST refuser une garantie de conservation conforme.

#### Scenario: Import sans purge implicite

- **WHEN** la reprise est confirmée dans PostgreSQL
- **THEN** le journal reste conservé et aucune purge n’est exécutée implicitement
