## ADDED Requirements

### Requirement: Vérifications spécialisées des propriétaires au raccord PA PZT

Le raccord PA/PZT MUST composer explicitement les interfaces spécialisées : Z12 pour la confiance cryptographique applicable ; PZT pour canal/relation/routage ; PA pour admission/gardes/préconditions ; C08 pour intention/confirmation opérateur ; Agent pour origine/confirmation de gestion ; producteur temporel sélectionné pour le temps au point d'usage. Il MUST NOT créer une autorité unique nouvelle ni transférer ces responsabilités au Kernel.

#### Scenario: Composition des vérifications propriétaires

- **WHEN** un raccord PA/PZT est préparé ou sélectionné
- **THEN** chaque contrôle reste attribué à son fournisseur compétent et la présence d'une interface abstraite ne vaut pas livraison du fournisseur concret

### Requirement: Autorité courante recontrôlée avant chaque effet PA PZT

Les conditions d'autorité requises MUST être vérifiées au point d'usage avant chaque effet. Un fournisseur requis absent ou une preuve courante manquante MUST entraîner un refus. Une signature correcte MUST NOT remplacer les autres conditions d'admission. L'adoption de cette répartition MUST NOT être présentée comme un raccord ou une qualification déjà réalisés.

#### Scenario: Signature valide et autre condition d'admission absente

- **WHEN** une signature est correcte mais qu'un fournisseur requis ou une preuve courante d'autorité manque
- **THEN** l'effet est refusé sans admission déduite de la seule signature

#### Scenario: Autorité changée après un premier contrôle

- **WHEN** l'autorité applicable change entre deux effets
- **THEN** les conditions courantes sont recontrôlées avant l'effet suivant et une condition devenue invalide le bloque


### Requirement: Admission PZT des remises du relais Agent

PZT MUST conserver admission, relation, identité et routage vers PA pour les demandes du relais Agent R1. Le relais MUST NOT contourner PZT ni remplacer ses gardes ou celles de PA. Un reçu PZT MUST rester distinct du succès technique et de la confirmation Agent. La sélection F1 de l'adaptateur MUST NOT être présentée comme un transport livré ou qualifié.

##### Contrat détaillé validé R1 F1 — frontière PZT

| Élément | Règle validée |
| --- | --- |
| Entrée | Remise par le relais PBO de l'outbox privée Agent après commit local vérifié ; le contexte initial C08/PA reste séparé et sans génération Agent fictive. |
| Autorités | Relation, identité, admission et routage PZT courants ; gardes PA avant chaque effet inchangées ; une liaison ACTIVE ou un contrôle du relais ne vaut pas autorité permanente. |
| Transport retenu | Adaptateur PZT ; pour E3 local, Cython/OpenSSL 3 mTLS déjà adopté. Aucun canal direct PBO–PA ni nouveau broker externe. |
| Retour | ACK limité à son contrat de réception ; succès technique, résultat durable, origine, postcondition et confirmation restent des preuves distinctes. |
| Livraison et preuve | Client/serveur, admission, routage et fournisseurs courants restent à réaliser et qualifier ; aucun port, endpoint, compte ou budget supplémentaire choisi ici. |

#### Scenario: Liaison valide et garde PZT devenue invalide

- **WHEN** une demande issue d'une liaison Agent valide arrive par le relais mais qu'une condition courante PZT est invalide
- **THEN** PZT refuse l'admission ou le routage protégé sans se fonder sur la seule liaison ou sur un ancien contrôle du relais

#### Scenario: Reçu PZT sans résultat technique

- **WHEN** PZT accuse réception sans résultat technique durable PA vérifié
- **THEN** le reçu ne vaut ni effet réussi ni confirmation Agent et le parcours reste soumis à la lecture et à la réconciliation propriétaires

### Requirement: Interface privée PZT du relais Agent validée D F1

Le fournisseur PZT D-F1 MUST respecter les entrées submit et inspect_submission et retourner les observations privées D-R1 validées. Il MUST conserver ses contrôles courants d'admission, relation, terminal et routage, sans canal direct PBO–PA. Une observation de transport MUST NOT prouver un effet PA, remplacer son résultat durable ou étendre le wire.

##### Contrat détaillé validé D-F1 — transport PZT

| Interface validée et propriétaire | Opérations et entrées détaillées | Sorties et responsabilités |
| --- | --- | --- |
| AgentPztTransport — PZT | submit(attempt_ref, binding_ref, référence de demande native exacte, relation/terminal attendus, contexte propriétaire courant) ; inspect_submission(référence d'invocation, cible, mandat de lecture courant). | TransportObservation pour submit ; observation propriétaire de remise pour inspect. Admission, canal et routage PZT ; aucun accès direct PBO–PA et aucune confirmation d'effet PA. E3 local reprend Cython/OpenSSL 3 mTLS. |

##### Contrat détaillé validé D-R1 — observations privées

TransportObservation 1.0.0, privé, définit les champs exacts :
attempt_ref, outcome, receipt_ref, native_operation_ref, detail_ref.
outcome vaut RECEIPT, REFUSED_NO_SUBMISSION ou UNKNOWN. receipt_ref est requis
pour RECEIPT ; native_operation_ref est présent seulement si le propriétaire
l'a établi ; detail_ref reste une référence minimisée, sans corps secret.

REFUSED_NO_SUBMISSION exige une preuve contractuelle que cet appel n'a pas
été soumis, sans prétendre qu'une tentative antérieure n'a pas eu d'effet.
Timeout, rupture après début d'IO, parsing ambigu ou retour non vérifiable
sont UNKNOWN. Une référence de reçu non vérifiée ne classe pas RECEIPT.

Motifs privés validés : COMMIT_UNRESOLVED, BINDING_STALE, GENERATION_STALE,
CLAIM_STALE, PROVIDER_UNAVAILABLE, AUTHORITY_REFUSED, TIME_IN_DOUBT,
SUBMISSION_UNKNOWN, RECEIPT_UNVERIFIABLE, RESULT_DIVERGENT,
IDEMPOTENCE_CONFLICT et PROFILE_UNAVAILABLE. Ils restent des décisions
de diagnostic, sans ajout aux codes wire, aux phases PA ou aux issues Agent.

#### Scenario: Demande native et terminal attendus

- **WHEN** le relais soumet une demande native exacte avec relation et terminal attendus
- **THEN** PZT vérifie son admission et son routage courants sans attribuer une permission à la seule liaison Agent ni présenter son retour comme un résultat technique PA

#### Scenario: Reçu invérifiable ou inspection non autorisée

- **WHEN** le retour est invérifiable ou que la lecture de remise ne dispose pas de son mandat courant
- **THEN** aucune réception vérifiée ou inspection autorisée n'est fabriquée et le doute ou refus reste explicite sans succès PA ou confirmation Agent

