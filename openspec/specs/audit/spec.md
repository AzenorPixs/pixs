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

- **WHEN** le profil est utilisé ou validé
- **THEN** aucune persistance, exécution runtime, ouverture P0 ou modification d’un contrat étranger au profil n’est effectuée
