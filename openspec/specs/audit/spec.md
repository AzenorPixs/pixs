# audit Specification

## Purpose
L'audit fonctionnel trace les événements métier significatifs, séparés des logs techniques, persistants, append-only et soumis à des politiques de rétention et de minimisation.

## Requirements

### Requirement: Audit dérogeable du Super Admin

Le Super Admin MUST pouvoir déroger à l'obligation d'audit dans son périmètre autorisé. Lorsqu'il utilise cette dérogation, l'absence ou l'indisponibilité d'un audit persistant MUST NOT bloquer son opération ni être présentée comme une preuve d'audit réalisée. Les obligations d'audit des autres comptes MUST rester inchangées.

#### Scenario: Opération Super Admin sans audit persistant

- **WHEN** le Super Admin utilise sa dérogation d'audit pour une opération dans son périmètre autorisé et l'audit est indisponible
- **THEN** l'absence d'audit ne bloque pas l'opération
- **AND** aucune preuve d'audit réalisée n'est annoncée

#### Scenario: Audit ordinaire toujours obligatoire

- **WHEN** un Administrateur ordinaire demande une opération soumise à audit alors que cet audit ne peut pas être persisté
- **THEN** l'opération est refusée selon les exigences ordinaires

### Requirement: Portée de l'exception dans les exigences d'audit

Les exigences et scénarios de contrôle applicatif de cette capacité MUST s'appliquer sous réserve de l'exception définie par `authorization`, dans le périmètre du seul compte décrit par `initial-administration`. Les comptes ordinaires MUST conserver leurs contrôles. Les profils structurels préparatoires MUST rester inchangés.

#### Scenario: Profil d'occultation inchangé

- **WHEN** un profil structurel d'occultation de champ est validé
- **THEN** ses types, modes et limites restent inchangés et sa validation ne vaut ni audit réalisé ni dérogation

### Requirement: Audit fonctionnel distinct des logs techniques

L'audit MUST être un flux fonctionnel séparé des journaux, métriques et traces techniques ; un événement d.audit MUST NOT être reconstitué implicitement à partir de logs.

#### Scenario: Perte de télémétrie technique

- **WHEN** la collecte de logs techniques est indisponible
- **THEN** les événements d'audit requis restent persistés et aucune mutation métier conforme n'est bloquée par cette indisponibilité

### Requirement: Contenu minimal d'un événement d'audit

Un événement d'audit MUST pouvoir représenter au minimum un identifiant, l'instant, l'acteur ou sa référence, le tenant pertinent, l'action, le type et l'identifiant de ressource, le résultat, la raison ou code d'erreur éventuel, les identifiants de corrélation et de causalité, et le composant avec sa version.

#### Scenario: Refus d'autorisation tracé

- **WHEN** une opération autorisée est refusée par l'évaluation d'autorisation
- **THEN** l'événement d'audit contient acteur, action, cible, résultat et corrélation sans attribut confidentiel superflu

### Requirement: Périmètre obligatoire d'audit

Les authentifications, changements d'identité, autorisations sensibles, accès inter-tenants, mutations métier significatives, modifications de configuration et opérations destructives MUST produire un audit persistant, contrôlé et soumis à une politique de rétention.

#### Scenario: Opération destructive sans audit

- **WHEN** une opération destructive ne peut pas enregistrer son événement d'audit
- **THEN** l'opération est refusée en échec fermé avec un diagnostic explicite

### Requirement: Append-only et réécriture contrôlée

L'audit MUST être append-only dans son usage normal ; toute suppression ou minimisation imposée MUST passer par une procédure explicite et auditable d'anonymisation ou de purge de champs autorisés, sans présenter une réécriture comme un événement nouveau.

#### Scenario: Obligation d'effacement

- **WHEN** une obligation légale impose la suppression d'un champ d'audit
- **THEN** la procédure autorisée anonymise le champ et l'opération reste elle-même traçable

### Requirement: Minimisation et non-duplication des données

Les valeurs avant/après MUST être limitées aux champs nécessaires et redacted lorsqu'elles sont sensibles ; l'audit MUST NOT devenir une copie de la base métier ni contenir de secret.

#### Scenario: Payload sensible détecté

- **WHEN** une valeur sensible est proposée pour un champ avant/après
- **THEN** elle est redacted ou remplacée par une référence pseudonymisée dans l'événement d'audit

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

### Requirement: Profil structurel préparatoire d'occultation de champ d'audit v1

Le profil d'occultation v1 MUST être une représentation interne, immuable et purement mémoire comportant exactement field_reference, mode et replacement_reference. Tous les champs MUST être fournis explicitement, sans valeur par défaut ni champ de payload avant/après.

#### Scenario: Structure valide sans effet

- **WHEN** un appelant de confiance fournit les trois champs avec leurs types et contraintes déclarés, en REDACTED avec replacement_reference None ou en PSEUDONYMIZED_REFERENCE avec une référence opaque non vide
- **THEN** la validation ne produit aucun diagnostic ni effet et la représentation conserve exactement ces valeurs

### Requirement: Types et modes du profil d'occultation v1

field_reference MUST être une str exacte non vide, opaque et sans normalisation. mode MUST être une valeur exacte de l'Enum fermé RedactionMode contenant uniquement REDACTED et PSEUDONYMIZED_REFERENCE ; bool et toute sous-classe MUST être refusés.

#### Scenario: Types d'occultation exacts

- **WHEN** un champ ou un mode du profil d'occultation v1 emploie un booléen, une sous-classe ou une valeur hors de RedactionMode
- **THEN** la structure est refusée sans reproduire la valeur

### Requirement: Référence de remplacement du profil d'occultation v1

En mode REDACTED, replacement_reference MUST être None explicite ; en mode PSEUDONYMIZED_REFERENCE, replacement_reference MUST être une str exacte non vide, opaque et sans normalisation. Ces valeurs MUST provenir d'un appelant de confiance ou de fixtures synthétiques ; None MUST NOT être interprété comme une autorisation, une exemption de rétention ou une décision d'applicabilité.

#### Scenario: Référence de remplacement selon le mode

- **WHEN** l'appelant fournit le mode REDACTED ou PSEUDONYMIZED_REFERENCE
- **THEN** replacement_reference doit respectivement être None explicite ou une str exacte non vide et opaque, sans que None accorde une permission

### Requirement: Validation pure du profil d'occultation v1

La validation MUST porter uniquement sur la structure exacte et produire des diagnostics statiques VALIDATE, triés et dédupliqués, sans reproduire les valeurs. Elle MUST NOT inspecter un payload avant/après, consulter une classification, résoudre une référence, lire une horloge, effectuer une entrée/sortie, ni déduire une occultation, une pseudonymisation ou une minimisation effectives.

#### Scenario: Structure invalide refusée sans écho

- **WHEN** une valeur a un type ou une forme interdite, notamment un mode hors de l'Enum fermé, une valeur booléenne, une référence vide dans un mode pseudonymisé, une référence non None en mode REDACTED ou un mode de sous-classe
- **THEN** la validation produit des diagnostics statiques triés et dédupliqués sans reproduire les valeurs ni fournir de garantie runtime

### Requirement: Limites des garanties du profil d'occultation v1

Ce profil préparatoire MUST NOT valoir occultation effective, preuve d'audit persistant, politique de rétention, intégrité, autorisation ni événement d'audit. Les exigences générales d'audit, de minimisation, d'append-only, de purge et de protection des données personnelles restent intégralement applicables aux futures intégrations. Aucun wire format, provider, façade publique, politique, configuration ou nouvelle dépendance n'est introduit par ce profil.

#### Scenario: Profil distinct d'une occultation effective

- **WHEN** le profil d'occultation v1 est structurellement valide
- **THEN** il ne démontre aucune occultation effective, persistance ou autorisation et ne dispense pas des exigences générales d'audit

### Requirement: Portée préparatoire de la projection décision et audit v1

AuditDecisionProjectionV1, défini par authorization-engine, MUST rester un contrôle structurel préparatoire entre deux objets fournis. Sa validation MUST NOT constituer un acquittement d’audit, une persistance, une preuve d’exhaustivité ou une conformité P0. Les contrats existants d’événements, signatures PDP/PEP, obligations ordinaires et exceptions Super Admin MUST rester inchangés.

#### Scenario: Projection distincte d’un audit réalisé

- **WHEN** la projection est structurellement valide
- **THEN** aucune preuve d’audit réalisé, persistant, exhaustif ou P0 n’est annoncée

#### Scenario: Obligations et exceptions conservées

- **WHEN** une opération ordinaire ou Super Admin est évaluée
- **THEN** ses obligations et exceptions existantes restent applicables sans dérogation induite par le profil


### Requirement: Limites de la projection décision et audit v1

Ce profil MUST NOT introduire stockage, cryptographie, WORM, rétention, export, provider, valeur par défaut ou privilège. Il MUST NOT ouvrir EventRegistry, un schéma de manifeste, Bulk ou Frontend. Il MUST préserver les deux formats d’événements intentionnellement distincts et les exigences générales d’audit.

#### Scenario: Aucune ouverture runtime

- **WHEN** la projection est construite ou sa seule validation est exécutée
- **THEN** aucune persistance, exécution runtime, ouverture P0 ou modification d’un contrat étranger au profil n’est effectuée

### Requirement: Portée limitée de l'acquittement observé du port audit v1

L'opération distincte invoke_audit_projection définie par authorization-engine MUST constater uniquement le retour du port PDP fourni pour cet appel. Un résultat True MUST NOT valoir preuve de persistance, d'exhaustivité, de conformité P0, de fraîcheur, de déduplication ou d'accès autorisé.

#### Scenario: Retour du port distinct d'une preuve persistante

- **WHEN** le port fourni retourne True et l'opération reconnaît ce retour
- **THEN** seule cette valeur observée est attestée, sans preuve de persistance ou de conformité P0 et sans autorisation d'accès implicite


### Requirement: Exclusions de l'invocation préparatoire du port audit v1

Cette opération MUST NOT enregistrer ou convertir implicitement l'événement d'audit générique, ni introduire stockage, provider, WORM, rétention, SQL, export, Bulk, Frontend, EventRegistry ou notification.

#### Scenario: Contrats étrangers conservés

- **WHEN** l'opération distincte est invoquée
- **THEN** les décisions, obligations, exceptions Super Admin et formats d'événements existants restent inchangés, sans intégration implicite dans une capacité étrangère


### Requirement: Contrats d'audit et projection pure conservés v1

Les exigences générales d'audit, de minimisation, d'append-only, les deux formats d'événements et les obligations et exceptions Super Admin MUST rester applicables sans modification. La seule validation de la projection MUST rester pure et distincte de cette invocation explicite du port fourni.

#### Scenario: Projection seule sans invocation

- **WHEN** l'appelant construit ou valide seulement la projection sans invoquer l'opération distincte
- **THEN** aucun port n'est appelé et la projection demeure un contrôle structurel préparatoire pur

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
