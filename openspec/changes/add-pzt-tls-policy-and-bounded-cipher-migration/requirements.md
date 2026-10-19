# Références normatives — Z10

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 129 | [TLS et choix de chiffrement borné](../../specs/pzt/spec.md#L129) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 3165 | [Contrat A10g — Versions TLS pour les canaux PZT — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L3165) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 3259 | [Contrat A10h — Choix du chiffrement TLS depuis PBO — choix du développeur validé le 6 octobre 2026](../../specs/pzt/spec.md#L3259) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 3379 | [Contrat A10h2 — Portée du choix de chiffrement PBO — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L3379) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 3451 | [Contrat A10h3 — Chiffrement global initial — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L3451) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 3514 | [Contrat A10h4 — Changement de chiffrement coordonné — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L3514) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 3606 | [Contrat A10h5 — Unités de migration calculées par PBO — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L3606) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 3670 | [Contrat A10h6 — Migration séquentielle par unité — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L3670) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 3730 | [Contrat A10h7 — Budgets par phase et échéance globale de migration — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L3730) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 3798 | [Contrat A10h8 — Tentatives de reconnexion transitoires bornées — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L3798) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 3863 | [Contrat A10h9 — Temporisation exponentielle plafonnée et déterministe — option A validée le 6 octobre 2026](../../specs/pzt/spec.md#L3863) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--a263a81ed1

Source : `openspec/specs/pzt/spec.md`, ligne 129. SHA-256 du bloc : `f15866c2f27f1568be70e7f6b039c3f4708947870a80eecd4d174e69ce5985a0`.

~~~~text
### Requirement: TLS et choix de chiffrement borné

Les canaux TLS PZT concernés MUST utiliser TLS 1.3 sans 0-RTT. PBO MUST pouvoir choisir explicitement AES-256-GCM ou ChaCha20-Poly1305 selon A10h–A10h9 ; migration, unités, phases, budgets et reconnexions MUST être bornés et prouvés. Ce réglage MUST NOT modifier le chiffrement natif WireGuard ni appliquer aux relais QUIC un choix TLS/TCP non prévu.

#### Scenario: TLS et choix de chiffrement borné

- **WHEN** la migration de chiffrement dépasse son budget
- **THEN** son état reste explicite sans prolongation de droit ou succès inventé
~~~~

### Référence pzt--13b5623d9e

Source : `openspec/specs/pzt/spec.md`, ligne 3165. SHA-256 du bloc : `65becb8b0e168e130ac5e1b731e372dc7fe9564f9316dfd625c0332556cd5e34`.

~~~~text
### Requirement: Contrat A10g — Versions TLS pour les canaux PZT — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10g MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10g

Profil des canaux TLS contrôlés par PZT : amorçage A02, local A03, requêtes
DNS DoT A06f, contrôle HTTP/WS/SSE A07 et WSS A09b lorsqu'utilisés. WireGuard
A01 conserve son protocole ; QUIC A09c conserve TLS 1.3 requis par QUIC,
sans profil TLS 1.2 ajouté. Aucun changement des TLS d'autres applications
ou services externes. A02 conserve ses étapes d'identité avant admission :
TLS réussi ne vaut ni admission ni dispense de preuve.

L'option A validée retient TLS 1.3 exclusivement, sans TLS 1.2 ou
version antérieure ni fallback après échec. Provider incompatible : profil
non activable/connexion refusée, diagnostic et qualification d'un provider
compatible requis. Un provider applicatif peut être étudié quand l'OS natif
ne convient pas, sans bibliothèque supplémentaire ni privilège approuvés
par ce choix. Support Linux/Windows physique/VM, Docker/LXC Proxmox à démontrer.

Identité, chaîne/ancrage/usages, contexte, permissions et révocation
A05/A10b vérifiés selon le rôle du canal. TLS mutuel requis après admission
dans les profils déjà validés ; WireGuard, attestation A10c et mandats restent
applicables. Version TLS distincte de l'algorithme Ed25519 des reçus/permissions
A12e ; suites, groupes, signatures de certificat et bibliothèques ne sont
pas choisis implicitement. Données précoces TLS 0-RTT désactivées pour ces
canaux PZT ; aucune requête protégée avant fin des contrôles requis.

Reprise de session éventuelle bornée par identité/contexte et validités,
sans fraîcheur d'attestation, droits ou révocation contournés ; ticket/session
ne vaut pas nouvelle habilitation. Contrôles impossibles : reprise refusée
ou handshake complet dans le même profil autorisé, jamais sécurité réduite.
Tailles/parsing, handshakes concurrents, connexions, temps et retries bornés,
diagnostics sans secrets ni contenu privé. Réutilisation de connexions valide
possible, sans permission prolongée ; migration des profils existants explicite.

Un seul profil de version TLS pour ce socle PZT, interopérabilité à qualifier ;
aucun profil de compatibilité TLS 1.2 adopté. Aucun gain CPU/RAM,
latence ou débit garanti ; mesurer établissement complet/reprise, connexions
réutilisées et coûts des providers/attestations. Recette par rôle et cible :
versions négociées/interdites, provider absent, certificat/contexte invalides,
0-RTT refusé, reprise après retrait/expiration/restauration, TPM courant,
WireGuard/QUIC préservés et absence de fallback.

[La RFC 8446 définit TLS 1.3 et les limites des données 0-RTT](https://www.rfc-editor.org/rfc/rfc8446.html#section-2.3) ;
[la RFC 9325 recommande TLS 1.3 et encadre le maintien de TLS 1.2 pour compatibilité](https://www.rfc-editor.org/rfc/rfc9325.html#section-3.1.1).
Ce profil Pixs restreint ne constitue pas une interdiction générale de TLS 1.2
imposée par ces RFC. A10g, option A, est validé le 6 octobre 2026 ; providers
et qualification ouverts. Choix explicite AES-256-GCM/ChaCha20-Poly1305
depuis PBO validé en A10h ; portée globale avec dérogations validée en A10h2.

##### Application au PA — A10g

Canaux TLS PZT A02/A03, DoT A06f, HTTP/WS/SSE A07 et WSS A09b ; WireGuard
A01 inchangé, QUIC A09c toujours TLS 1.3, autres applications TLS hors choix.
A02 conserve ses étapes d'identité/admission/preuves, handshake sans admission
implicite.

L'option A validée retient TLS 1.3 exclusivement, sans TLS 1.2 ni fallback.
Provider incompatible : activation/connexion refusée et diagnostic ; provider
applicatif envisageable après qualification, sans dépendance ou privilège
approuvés implicitement. Support de toutes les cibles à démontrer.

Identité/chaîne/ancrage/usages/contexte, permissions/révocation A05/A10b,
mTLS après admission dans profils validés, attestation A10c et mandats conservés.
Ed25519 A12e distinct des choix TLS ; suites/groupes/signatures de certificat/
bibliothèques ouverts. 0-RTT désactivé sur ces canaux PZT, aucune requête
protégée avant contrôles requis. Reprise éventuelle bornée avec contrôles
courants, sans ticket accordant droit/fraîcheur ; si contrôles impossibles,
refus ou handshake complet dans même profil, jamais sécurité réduite.

Parsing/tailles, handshakes/concurrence/connexions/temps/retries bornés, diagnostics
sans secrets/contenu privé ; connexions réutilisées sous validités courantes.
Migration explicite, profil de version unique et interopérabilité à qualifier ;
aucun profil TLS 1.2 adopté.
CPU/RAM/latence/débit à mesurer, établissement/reprise/connexions et providers/
attestation inclus. Recette par rôle/cible : versions permises/interdites,
provider absent, certificat/contexte invalides, 0-RTT, reprise après retrait/
expiration/restauration, TPM courant et absence de fallback ; WireGuard/QUIC
préservés. Sources RFC dans cadrage PZT, sans interdiction générale TLS 1.2 attribuée
aux normes. A10g, option A, est validé le 6 octobre 2026 ; providers/qualification
ouverts. Choix explicite AES-256-GCM/ChaCha20-Poly1305 depuis PBO validé
en A10h ; portée globale avec dérogations validée en A10h2.

#### Scenario: Conformité du traitement A10g

- **WHEN** un profil revendique le traitement A10g et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--2b5633f473

Source : `openspec/specs/pzt/spec.md`, ligne 3259. SHA-256 du bloc : `30e30c92c3b144086fa6bb6bc0b29b17d073967603a58c5bfbd87a0141400cfd`.

~~~~text
### Requirement: Contrat A10h — Choix du chiffrement TLS depuis PBO — choix du développeur validé le 6 octobre 2026

Le rôle chargé du traitement A10h MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10h

Le développeur demande de pouvoir choisir depuis PBO entre AES-256-GCM et
ChaCha20-Poly1305. Cette décision remplace les alternatives A10h soumises ;
elle retient un choix explicite administré, pas une sélection automatique
selon la performance. Canaux TLS sur TCP A10g : amorçage, local, DoT,
HTTP/WS/SSE et WSS PZT. WireGuard conserve son chiffrement natif, QUIC A09c
son profil distinct ; aucune suite de ces transports modifiée par ce réglage.

PBO expose deux valeurs lisibles et leurs correspondances protocolaires :

| Choix PBO | Suite TLS 1.3 attendue |
|---|---|
| AES-256-GCM | `TLS_AES_256_GCM_SHA384` |
| ChaCha20-Poly1305 | `TLS_CHACHA20_POLY1305_SHA256` |

Une seule valeur effective par profil de canal concerné. Aucun choix
AES-128-GCM ou mode automatique ajouté ; aucune valeur initiale sélectionnée
par cette décision. L'absence/incohérence du choix requis bloque activation/
readiness selon contrat, sans configuration devinée ; amorçage A02 conserve
ses paramètres et ancrages provisionnés avant accès au PBO. Restriction de
configuration, sans supprimer les capacités normativement requises du provider.
Portée globale/héritage/dérogations validée en A10h2.

Choix et modifications depuis l'interface PBO ou ses contrats publics,
avec permission d'administration du périmètre, contrôles Django, configuration
typée/versionnée, audit et engagement coordonné A07/A12. Diffusion aux PA
par PZT, y compris même hôte A03 ; pas d'édition locale contournant PBO.
Avant activation, compatibilité vérifiée des deux extrémités et du provider
qualifié, inventaire de capacités vérifié sans déclaration de pair suffisante.
PBO expose choix souhaité, choix appliqué/suite négociée et incompatibilités ;
commande reçue ou configuration enregistrée ne vaut pas application réussie.

Nouvelles connexions/reprises n'utilisent que la suite effective autorisée,
vérifiée avant trafic protégé. Incompatibilité : refus diagnostiqué, sans
bascule vers l'autre choix, AES-128, TLS 1.2, mTLS désactivé ou contrôles allégés.
Une connexion établie ne change pas de suite en place ; appliquer un changement
nécessite fermeture/reconnexion contrôlées et preuves de l'état appliqué.
Plan de migration validé avant activation, pour éviter la perte du contrôle
PBO–PA ; temporisations, convergence et reprise à qualifier. Ancienne suite
ne vaut pas application du nouveau choix, aucun maintien illimité ni droit
prolongé. Restauration sans choix retiré réactivé, retour arrière seulement
par nouvelle décision autorisée compatible avec les politiques courantes.

TLS 1.3 maintenu et 0-RTT désactivé selon A10g, mTLS selon rôle, contexte/permissions A05/A10b,
attestation fraîche A10c et mandats conservés. Reprise/ticket sans politique
modifiée ou révocation contournée. Clés TLS distinctes de WireGuard et des
signatures opérationnelles Ed25519 A12e ; groupes d'échange/signatures de
certificat non choisis ici. Aucun algorithme annoncé plus sûr ou moins coûteux
globalement ; CPU/RAM/latence/débit à mesurer par OS/provider/cible avec ou
sans accélération, handshake/reprise/connexions réutilisées inclus.

Recette Linux/Windows physiques/VM, Docker/LXC Proxmox : les deux valeurs
PBO, permission refusée, configuration absente/invalide, provider incompatible,
suite réelle, souhaité/appliqué, changement/reconnexion et perte de contrôle,
reprise après retrait/restauration, TPM/identité/0-RTT et absence de fallback.
A10h est validé dans ce périmètre le 6 octobre 2026 ; portée précisée en A10h2.
Schéma, providers et migration restent à préciser, sans implémentation.

[La RFC 8446 définit les deux suites TLS](https://www.rfc-editor.org/rfc/rfc8446.html#appendix-B.4) ;
[WireGuard utilise ChaCha20 avec Poly1305 dans son protocole](https://www.wireguard.com/protocol/).
Le sélecteur PBO est une spécification Pixs, pas un réglage AES de WireGuard.

##### Application au PA — A10h

Choix explicite demandé depuis PBO entre AES-256-GCM et ChaCha20-Poly1305,
remplaçant les alternatives A10h soumises. TLS sur TCP A10g : amorçage/local/
DoT/HTTP/WS/SSE/WSS ; WireGuard natif et QUIC A09c inchangés.

| Choix PBO | Suite TLS 1.3 attendue |
|---|---|
| AES-256-GCM | `TLS_AES_256_GCM_SHA384` |
| ChaCha20-Poly1305 | `TLS_CHACHA20_POLY1305_SHA256` |

Une valeur effective par profil de canal, sans AES-128-GCM ou mode automatique.
Aucune valeur initiale choisie ici ; absence/incohérence bloque activation/
readiness selon contrat, sans réparation devinée. A02 conserve paramètres/
ancrages provisionnés pour joindre PBO. Capacités normativement requises du
provider conservées ; portée/héritage/dérogations validés en A10h2.

Interface PBO/contrats publics, permission d'administration de périmètre,
Django, configuration typée/versionnée, audit/engagement A07/A12. Diffusion
PA via PZT même hôte inclus, sans édition locale contournant PBO. Deux
extrémités/provider qualifiés vérifiés avant activation, capacités sans simple
affirmation du pair. PBO expose souhaité/appliqué, suite négociée et incompatibilités ;
réception/enregistrement sans succès appliqué implicite.

Connexions/reprises nouvelles seulement dans suite effective autorisée,
vérifiée avant trafic protégé ; incompatibilité sans autre choix, AES-128,
TLS 1.2, mTLS désactivé ou contrôle allégé. Connexion ouverte sans suite changée
en place ; fermeture/reconnexion contrôlées et preuve appliquée requises.
Plan de migration validé avant activation pour préserver le contrôle PBO–PA,
convergence/délais/reprise à qualifier ; ancienne suite sans nouveau choix
appliqué ni maintien illimité/droits prolongés. Restauration sans choix retiré
réactivé, retour arrière par nouvelle décision autorisée/politique courante.

TLS 1.3 maintenu et 0-RTT désactivé selon A10g, mTLS selon rôle, A05/A10b et attestation fraîche
A10c conservés ; ticket/reprise sans politique/retrait contournés. Clés TLS
séparées de WireGuard/Ed25519 A12e, groupes/signatures TLS ouverts. CPU/RAM/
latence/débit à mesurer selon provider/OS/cible et accélération, sans supériorité
globale promise. Recette par rôle/cible : deux choix PBO, droits, configuration,
provider, suite réelle, souhaité/appliqué, changement/reconnexion/perte contrôle,
reprise/retrait/restauration, TPM/0-RTT et refus de fallback. A10h validé le
6 octobre 2026 ; portée précisée en A10h2, schéma/providers/migration ouverts, sans implémentation.
Sources RFC/WireGuard dans cadrage PZT ; sélecteur PBO sans réglage AES de WireGuard.

#### Scenario: Conformité du traitement A10h

- **WHEN** un profil revendique le traitement A10h et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--867b266f75

Source : `openspec/specs/pzt/spec.md`, ligne 3379. SHA-256 du bloc : `09df6648c28dd2bfb7ed7008a114d5338ab74bd7dda964991858aa6151b1ee41`.

~~~~text
### Requirement: Contrat A10h2 — Portée du choix de chiffrement PBO — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10h2 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10h2

Valeur globale explicitement configurée dans PBO, héritée par les profils,
avec dérogation AES-256-GCM ou ChaCha20-Poly1305 par profil/périmètre autorisé.
PBO affiche la valeur effective et son origine globale/dérogation. Création,
modification et retrait d'une dérogation nécessitent la permission applicable,
les contrôles Django et un engagement versionné/audité selon A07/A12.
Une dérogation applicable remplace la valeur héritée ; revenir à l'héritage
est une opération autorisée. Aucun mélange de suites ni choix automatique
par PA. La résolution des périmètres et priorités doit être déterministe ;
une ambiguïté ou une valeur effective non vérifiable bloque l'activation,
sans valeur de secours inventée ni prolongation des droits.

Le choix effectif d'un canal doit être compatible et autorisé aux deux
extrémités ; affectations, endpoints et versions sont vérifiés avant activation.
Un serveur partagé ne rend pas compatibles deux politiques contradictoires
sur un même canal. Partage et frontières à qualifier, sans nouvelle écoute
implicite ; nom d'endpoint/SNI sans contexte authentifié ni droit implicites.
Divergence ou provider incompatible diagnostiqués et bloquants, sans
négociation d'une suite hors choix effectif. Changement global ou dérogation :
périmètre d'impact explicite, audit, preuve souhaité/appliqué et reconnexion
contrôlée A10h, garanties A05 et restauration sans politique retirée réactivée.
Un changement global affecte les profils héritiers ; les dérogations explicites
restent applicables tant qu'elles sont autorisées et compatibles.

A10h2 A est validé le 6 octobre 2026. Chiffrement global initial
ChaCha20-Poly1305 précisé en A10h3. Schéma, résolution des périmètres,
partage TLS et migration à qualifier, sans gain CPU/RAM promis. Recette par
cible : héritage, dérogation autorisée/refusée/modifiée/retirée, changement
global avec et sans dérogation, ambiguïté, profil absent, endpoints incompatibles,
serveur partagé, reconnexion/restauration et absence de droits supplémentaires.

##### Application au PA — A10h2

Valeur globale explicite dans PBO, héritée par les profils ; dérogation
AES-256-GCM ou ChaCha20-Poly1305 par profil/périmètre autorisé. PBO expose
valeur effective/origine. Création/modification/retrait sous permission,
contrôles Django, configuration versionnée et engagement/audit A07/A12.
Dérogation applicable prioritaire sur héritage ; retour à l'héritage autorisé,
aucune fusion de suites ni sélection automatique PA. Résolution déterministe
des périmètres/priorités ; ambiguïté ou valeur non vérifiable bloquante,
sans défaut inventé ni validité des droits prolongée.

Choix compatible/autorisé aux deux extrémités, affectations/endpoints/versions
vérifiés. Serveur partagé sans compatibilité présumée de politiques
contradictoires, partage/frontières à qualifier sans écoute implicite ;
endpoint/SNI sans droit ni contexte authentifié implicites. Divergence/provider
incompatible bloquants, sans suite hors choix effectif. Impacts, audit,
souhaité/appliqué, reconnexion A10h/A05 et restauration sans politique retirée
réactivée. Changement global appliqué aux profils héritiers ; dérogations
explicites conservées tant qu'autorisées et compatibles.

A10h2 A validé le 6 octobre 2026 ; chiffrement initial précisé en A10h3.
Schéma/résolution, partage TLS, migration et coûts à qualifier. Recette par
cible : héritage, dérogation autorisée/refusée/modifiée/retirée, changement global
avec/sans dérogation, ambiguïté, profil absent, endpoints incompatibles,
serveur partagé, reconnexion/restauration et absence de droits supplémentaires.

#### Scenario: Conformité du traitement A10h2

- **WHEN** un profil revendique le traitement A10h2 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--83f50070da

Source : `openspec/specs/pzt/spec.md`, ligne 3451. SHA-256 du bloc : `21715e24ce4269a6caa3c5e8e6cee0044692efac323665f7cb46402703d85d7c`.

~~~~text
### Requirement: Contrat A10h3 — Chiffrement global initial — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10h3 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10h3

ChaCha20-Poly1305, suite `TLS_CHACHA20_POLY1305_SHA256`, est la valeur globale
proposée au provisionnement d'un nouveau périmètre PZT pour les canaux TLS/TCP
A10h. PBO permet de la confirmer ou de la modifier avant activation ; la valeur
retenue est matérialisée dans la configuration versionnée. AES-256-GCM
(`TLS_AES_256_GCM_SHA384`) reste sélectionnable depuis PBO selon A10h/A10h2,
comme valeur globale ou dérogation autorisée. Cette initialisation ne remplace
aucune configuration existante, aucune dérogation ni les paramètres d'amorçage
préprovisionnés A02. Absence/incohérence bloquante, sans défaut déduit au runtime.

A10h3 A est validé le 6 octobre 2026. Aucun choix automatique selon CPU ou
basculement vers l'autre suite si le provider ne supporte pas la valeur effective ;
correction par décision autorisée. WireGuard natif, QUIC, certificats et
signatures opérationnelles inchangés. Le choix initial ne signifie ni clé
commune avec WireGuard ni réutilisation de ses paramètres cryptographiques.

Le choix vise les cibles hétérogènes, notamment sans accélération AES. Les
propriétés d'implémentation sont documentées dans la
[RFC 8439, introduction](https://www.rfc-editor.org/rfc/rfc8439.html#section-1),
sans benchmark Pixs. L'accélération matérielle peut favoriser AES ; coûts réels
des suites TLS selon provider, endpoints, CPU exposé aux VM/conteneurs, trafic
et connexions. Aucun classement universel de sécurité, CPU/RAM ou débit retenu.
Support/coût à qualifier sur Linux/Windows physiques/VM et Docker/LXC Proxmox.
Recette : nouveau périmètre, confirmation/modification PBO, AES-256-GCM encore
sélectionnable, existant/dérogations préservés, configuration absente, provider
incompatible, suite réelle et absence de fallback. Migration coordonnée validée en A10h4,
sans implémentation.

##### Application au PA — A10h3

ChaCha20-Poly1305 (`TLS_CHACHA20_POLY1305_SHA256`) : valeur globale proposée
au provisionnement d'un nouveau périmètre TLS/TCP A10h, confirmable/modifiable
depuis PBO avant activation et matérialisée en configuration versionnée.
AES-256-GCM (`TLS_AES_256_GCM_SHA384`) reste sélectionnable comme valeur
globale ou dérogation autorisée A10h2. Existant, dérogations et paramètres
d'amorçage A02 préservés ; absence/incohérence bloquante sans défaut runtime.

A10h3 A validé le 6 octobre 2026, sans sélection automatique CPU ni fallback
si incompatible ; correction par décision autorisée. WireGuard/QUIC/certificats/
signatures inchangés, aucune clé ni paramètres WireGuard réutilisés pour TLS.
Choix pour cibles hétérogènes, notamment sans accélération AES ; source RFC
8439 dans cadrage PZT. Coût réel selon provider/endpoints/CPU exposé/trafic, sans
benchmark Pixs ni classement universel sécurité/CPU/RAM/débit. Qualification
Linux/Windows physiques/VM, Docker/LXC Proxmox. Recette : nouveau périmètre,
confirmation/modification PBO, AES encore sélectionnable, existant/dérogations,
configuration absente, provider incompatible, suite réelle et absence de
fallback. Migration coordonnée A10h4 validée, sans implémentation.

#### Scenario: Conformité du traitement A10h3

- **WHEN** un profil revendique le traitement A10h3 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--58e1823abd

Source : `openspec/specs/pzt/spec.md`, ligne 3514. SHA-256 du bloc : `5114a85eb88248c388670630d3fa93b0f7e73d8e9967a38e5fc860c425784363`.

~~~~text
### Requirement: Contrat A10h4 — Changement de chiffrement coordonné — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10h4 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10h4

Option A validée : migration coordonnée en phases préparation, engagement versionné,
reconnexion contrôlée et vérification. PBO calcule les profils héritiers et
les dérogations affectés, vérifie les permissions et la compatibilité des deux
extrémités, puis diffuse la configuration candidate par les canaux PZT encore
autorisés. Accusé de réception et validation de préparation ne valent ni
activation ni suite appliquée. La bascule ne commence que pour une unité
cohérente de canaux/endpoints dont les prérequis sont vérifiés ; progression
par unités compatibles, sans supposer tous les PA commutés simultanément.
Configuration candidate sans trafic métier autorisé par anticipation. Une
seule suite effective autorisée par canal ; pas de liste transitoire des deux
suites acceptées, de double flux métier ni de nouvelle écoute implicite.

La suite ancienne reste utilisable uniquement avant sa coupure prévue et tant
que sa politique et les permissions courantes l'autorisent. Son maintien ne
renouvelle aucun droit et cesse immédiatement si elle est retirée pour raison
de sécurité. Après engagement de la nouvelle valeur, fermeture/reconnexion
contrôlées selon A10h ; identité, attestation fraîche A10c, suite négociée et
permissions vérifiées avant reprise des opérations. PBO expose préparation,
engagement, reconnexion, application prouvée ou échec ; un PA hors ligne reste
non convergé et rejoint la politique courante à son retour, sans ancienne
configuration restaurée. Les mandats et délais de coupure doivent permettre
une exécution autorisée après perte de l'ancien canal, sans autorité locale
ni besoin d'une nouvelle commande sur le canal déjà coupé. Faisabilité à
qualifier avant lancement ; aucun maintien illimité de l'ancien canal.

Garanties de la migration : audit, version/époque, idempotence et engagement A07/A12 ; résultat
incertain réconcilié, refus ou incompatibilité sans fallback. Avant engagement,
candidate annulable sous autorisation ; après engagement, retour arrière par
nouvelle décision explicite compatible avec les politiques courantes, jamais
restauration automatique d'une suite retirée. Refus d'un plan irréalisable,
sans passage automatique en maintenance. Cette procédure ne garantit pas l'absence
d'interruption. Délais, taille des unités, ressources et procédure de reprise
à qualifier sur toutes les cibles ; partage de serveur TLS à prendre en compte.

A10h4 A est validé le 6 octobre 2026. Constitution des unités validée en A10h5 ;
aucun gain chiffré CPU/RAM ou délai promis. Recette : changement global/dérogation,
prérequis refusés, réception sans application, PA hors ligne, serveur partagé,
perte du contrôle à la coupure, application partielle, commit incertain,
révocation pendant préparation, reconnexion/attestation, restauration et
retour arrière autorisé sans droits ou suites supplémentaires.

##### Application au PA — A10h4

Option A validée : préparation, engagement versionné, reconnexion contrôlée puis
preuve d'application. PBO vérifie profils/dérogations affectés, permissions et
compatibilité aux deux extrémités ; configuration candidate diffusée par PZT
encore autorisé. Réception/préparation sans activation ni suite appliquée ;
bascule seulement par unité de canaux/endpoints cohérente dont les prérequis
sont vérifiés, sans simultanéité de tous les PA présumée. Candidate sans
trafic métier anticipé ; une suite effective par canal, sans acceptation
transitoire des deux suites, double flux métier ou nouvelle écoute implicite.

Ancienne suite utilisable avant coupure seulement sous politique/permissions
courantes ; retrait de sécurité immédiat sans droits renouvelés. Après engagement,
fermeture/reconnexion A10h, identité/attestation fraîche A10c/suite/permissions
avant reprise. PBO expose préparation, engagement, reconnexion, application
prouvée/échec ; PA hors ligne non convergé, politique courante au retour.
Mandats/délais permettent la coupure et reconnexion autorisées sans nouvelle
commande sur canal déjà coupé ni autorité locale ; faisabilité qualifiée
avant lancement, sans maintien illimité de l'ancien canal.

Garanties de la migration : audit, versions/époques, idempotence/engagement A07/A12, résultat incertain
réconcilié ; aucun fallback. Candidate annulable avant engagement sous
autorisation ; après engagement, retour arrière par nouvelle décision
compatible avec politiques courantes, aucune suite retirée restaurée
automatiquement. Plan irréalisable refusé sans passage automatique en maintenance.
Aucune absence d'interruption garantie ; délais/unités/ressources/reprise et
serveur TLS partagé à qualifier sur toutes les cibles.

A10h4 A validé le 6 octobre 2026 ; constitution des unités validée en A10h5,
sans gains chiffrés promis.
Recette : changement global/dérogation, prérequis, réception sans application,
PA hors ligne/serveur partagé, perte de contrôle, application partielle,
commit incertain, révocation en préparation, reconnexion/attestation,
restauration/retour arrière sans droits ou suites supplémentaires.

#### Scenario: Conformité du traitement A10h4

- **WHEN** un profil revendique le traitement A10h4 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--5e45c1c889

Source : `openspec/specs/pzt/spec.md`, ligne 3606. SHA-256 du bloc : `94f89c9c17728dfa0e6fd5ad3d379abb37a82f4367e9a3c622530d1fdd185ea4`.

~~~~text
### Requirement: Contrat A10h5 — Unités de migration calculées par PBO — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10h5 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10h5

Option A validée : PBO construit un plan déterministe à partir des dépendances
explicitement décrites et vérifiées : profils effectifs A10h2, endpoints,
configurations TLS partagées et canaux nécessaires au contrôle/reprise A10h4.
Les ressources qui imposent une bascule commune sont regroupées dans une unité
indivisible ; les unités indépendantes peuvent être ordonnées. PBO expose
membres, dépendances, versions, impacts et motifs du regroupement. Calcul du
plan sans autorisation de l'exécuter : mandat et contrôles courants requis.
Une modification de dépendance, de politique ou de version impose une nouvelle
validation du plan avant la prochaine étape affectée, sans reprendre aveuglément.

Garanties du plan : données typées issues de contrats publics et providers qualifiés, jamais
simple inférence depuis OS, nom DNS, IP ou proximité physique. Inconnue,
incohérence, cycle empêchant la reprise ou dépendance hors mandat bloquent
le plan concerné. Les PA hors ligne restent visibles et non convergés, sans
omission permettant de déclarer une unité partagée entièrement appliquée.
Si une unité exige un arrêt commun, PBO indique son impact ; aucune séparation
artificielle, double suite, nouvelle écoute ou extension de périmètre implicite.
Délai, concurrence et budget restent à fixer ; un plafond ne permet pas de
couper une unité indivisible. Aucune atomicité globale ni continuité garantie.

A10h5 A est validé le 6 octobre 2026. Progression séquentielle entre unités validée en A10h6.
Coûts de calcul/mémoire à qualifier côté PBO et PA,
sans nouveau collecteur ou composant retenu ici. Recette : mêmes entrées/même
plan, héritage/dérogations, serveur partagé, dépendance manquante, PA hors ligne,
cycle/reprise, changement concurrent, unité trop grande et mandat insuffisant.

##### Application au PA — A10h5

Option A validée : plan déterministe calculé dans PBO depuis dépendances explicites
et vérifiées des profils effectifs A10h2, endpoints/configurations TLS partagés
et canaux de contrôle/reprise A10h4. Ressources à bascule commune regroupées
en unité indivisible ; unités indépendantes ordonnables. Membres/dépendances/
versions/impacts/motifs visibles. Calcul sans autorisation d'exécution : mandat
et contrôles courants requis. Dépendance/politique/version modifiée : plan
revalidé avant prochaine étape affectée, aucune reprise aveugle.
Garanties du plan : données typées de contrats publics/providers qualifiés, sans inférence
OS/DNS/IP/proximité hôte. Inconnue/incohérence/cycle empêchant la reprise ou
dépendance hors mandat bloquants. PA hors ligne visibles/non convergés, aucune
unité partagée annoncée entièrement appliquée sans preuve. Arrêt commun/impact
explicites si requis ; pas de séparation artificielle, double suite, écoute
ou périmètre implicites. Délais/concurrence/budgets ouverts, plafond sans
fractionnement d'unité indivisible ; aucune atomicité/continuité globale promise.
A10h5 A validé le 6 octobre 2026 ; progression séquentielle entre unités validée en A10h6.
Coûts PBO/PA à qualifier,
aucun collecteur/composant retenu ici. Recette : déterminisme, profils,
serveur partagé, dépendance manquante, PA hors ligne, cycle/reprise, modification
concurrente, unité trop grande et mandat insuffisant.

#### Scenario: Conformité du traitement A10h5

- **WHEN** un profil revendique le traitement A10h5 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--e8c67e515b

Source : `openspec/specs/pzt/spec.md`, ligne 3670. SHA-256 du bloc : `06849e2d43026652208cc9c08d3c4f1b3c07e88c2b6c45b223fc5f7ed6258573`.

~~~~text
### Requirement: Contrat A10h6 — Migration séquentielle par unité — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10h6 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10h6

Option A validée : progression séquentielle, une unité A10h5 à la fois. PBO ne
commence la bascule de la suivante qu'après preuve d'application de l'unité
courante et revalidation des prérequis, politiques et mandat encore valides.
Une unité peut contenir plusieurs endpoints devant changer ensemble ;
« une unité à la fois » ne signifie pas « un PA à la fois ». La préparation
sans activation peut être anticipée dans les limites du plan et du budget.

Garanties de progression : progression automatisable seulement sous mandat préalable explicite
couvrant plan/version, périmètre, délais et limites. Aucun nouveau mandat
déduit d'un succès ou d'un ACK. Échec, état incertain, dépassement de délai,
retrait de permission ou prérequis non vérifiable suspendent le lancement
des unités suivantes. Les unités déjà engagées sont réconciliées et achevées
seulement dans les limites encore autorisées ; aucun droit prolongé, abandon
silencieux ou retour automatique à l'ancienne suite. Reprise après échec sous
décision autorisée et état courant vérifié ; après redémarrage PBO, pas de
réexécution aveugle. Versions et idempotence A07/A12, reconnexion A10h4 maintenues.

A10h6 A est validé le 6 octobre 2026. Budgets par phase et échéance globale validés en A10h7.
Aucun gain CPU/RAM/délai garanti :
charge d'une unité, préparation et handshakes à mesurer sur toutes les cibles.
Recette : dépendances/ordre, unité multi-endpoints, mandat expiré ou retiré,
échec/état incertain, délai dépassé, interruption/redémarrage PBO, engagement
partiel, reprise autorisée et refus de concurrence hors plan/budget.

##### Application au PA — A10h6

Option A validée : une unité A10h5 à la fois ; bascule suivante après preuve
d'application et revalidation des prérequis/politiques/mandat courants.
Unité multi-endpoints possible, pas nécessairement un seul PA. Préparation
sans activation anticipable dans les limites du plan/budget.
Garanties de progression : automatisation sous mandat préalable explicite pour plan/version,
périmètre/délais/limites, aucun mandat déduit d'un succès/ACK. Échec/état
incertain/délai dépassé/retrait de permission/prérequis non vérifiable suspendent
les lancements suivants. Unités engagées réconciliées et achevées seulement
sous autorisations encore valides, sans droits prolongés/abandon silencieux/
retour automatique à l'ancienne suite. Reprise après échec par décision
autorisée/état courant ; redémarrage PBO sans réexécution aveugle. A07/A12
versions/idempotence et reconnexion A10h4 maintenues.
A10h6 A validé le 6 octobre 2026 ; budgets par phase et échéance globale validés en A10h7.
Charge par unité/préparation/handshakes à mesurer, aucun gain CPU/RAM/délai
garanti. Recette : ordre/dépendances, unité multi-endpoints, mandat expiré/
retiré, échec/état incertain/délai, redémarrage, engagement partiel, reprise
et refus de concurrence hors plan/budget.

#### Scenario: Conformité du traitement A10h6

- **WHEN** un profil revendique le traitement A10h6 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--57b5bfa9d3

Source : `openspec/specs/pzt/spec.md`, ligne 3730. SHA-256 du bloc : `659b801064ea3ce708928614f296cbc9b60d8c6d09fa976dbc89d98cc4dffa7f`.

~~~~text
### Requirement: Contrat A10h7 — Budgets par phase et échéance globale de migration — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10h7 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10h7

Option A validée : budgets finis distincts par phase et par unité (préparation,
engagement, reconnexion, preuve d'application), complétés par une échéance
globale du plan séquentiel A10h6. PBO expose les valeurs, le début de chaque
phase, le temps restant vérifiable et la cause d'arrêt. Valeurs configurées
et validées avant lancement selon les cibles et la taille des unités ; aucune
durée numérique retenue ici, aucune valeur illimitée ou déduite d'un ACK.

Garanties temporelles : aucune échéance ne prolonge un mandat, une permission, l'attestation ou
la validité de l'ancienne suite. Limite effective au plus égale aux validités
courantes applicables. Retry, événement de progression, reconnexion ou
redémarrage ne réinitialisent pas l'échéance globale ni le budget déjà consommé
d'une même phase ; passage à une nouvelle phase soumis aux prérequis A10h4.
Horloges, persistance et vérification du temps restant à qualifier ; état
temporel non vérifiable bloquant, sans nouveau délai inventé après restauration.

Dépassement : diagnostic explicite, suspension des nouveaux lancements A10h6,
réconciliation de l'unité engagée et actions seulement encore autorisées.
Une absence de réponse ne prouve ni succès, ni annulation, ni absence de commit.
Reprise après échec sous décision autorisée et état courant vérifié, sans
fallback, rollback automatique ou renouvellement implicite. Une nouvelle
échéance ne réactive pas l'ancienne opération expirée ou des droits retirés.

A10h7 A est validé le 6 octobre 2026. Délais techniques des providers et
validités de sécurité restent applicables ; valeurs numériques à qualifier.
Tentatives de reconnexion transitoires bornées validées en A10h8. Aucun gain de performance ou
objectif de convergence garanti. Recette : budget de phase/global dépassé, sécurité expirée
avant budget, commit incertain, progression sans réponse, retry, reconnexion,
redémarrage/restauration et impossibilité de vérifier le temps restant.

##### Application au PA — A10h7

Option A validée : budgets finis distincts par phase/unité (préparation, engagement,
reconnexion, preuve d'application), plus échéance globale du plan A10h6.
Valeurs/début/temps restant vérifiable/cause d'arrêt visibles dans PBO,
configuration validée avant lancement par cible/taille d'unité, sans durée
numérique choisie ni valeur illimitée ou déduite d'un ACK.
Garanties temporelles : limites sans mandat/permission/attestation/ancienne suite prolongés ;
limite effective bornée par validités courantes. Retry/progression/reconnexion/
redémarrage sans remise à zéro d'échéance globale ou du budget consommé de
la même phase ; phase suivante sous prérequis A10h4. Horloge/persistance/temps
restant à qualifier, non vérifiable bloquant sans délai restauré inventé.
Dépassement : diagnostic, nouveaux lancements suspendus A10h6, unité engagée
réconciliée et actions encore autorisées seulement ; absence de réponse sans
succès/annulation/absence de commit présumés. Reprise après échec autorisée
avec état courant, sans fallback/rollback ou renouvellement implicites ;
nouvelle échéance sans ancienne opération ou droits expirés réactivés.
A10h7 A validé le 6 octobre 2026. Délais techniques providers et validités
de sécurité maintenus, valeurs numériques à qualifier ; tentatives A10h8
validées. Aucun gain/performance/convergence promis. Recette : phase/global,
validité de sécurité plus courte, commit incertain, progression sans réponse,
retry/reconnexion/redémarrage/restauration et temps restant non vérifiable.

#### Scenario: Conformité du traitement A10h7

- **WHEN** un profil revendique le traitement A10h7 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--6ef8816da6

Source : `openspec/specs/pzt/spec.md`, ligne 3798. SHA-256 du bloc : `2ba18b3ebdab237402baecd4a7289c5389aef3e1f1da0738d08b678993673517`.

~~~~text
### Requirement: Contrat A10h8 — Tentatives de reconnexion transitoires bornées — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10h8 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10h8

Option A validée : nouvelles tentatives automatiques bornées pour les seules erreurs
techniques transitoires de reconnexion explicitement classifiées et qualifiées.
Le mandat de migration doit les autoriser avant lancement, avec nombre maximal,
intervalle et budget total finis configurés. Une tentative à la fois par canal,
sans boucle active ; aucun nombre ou intervalle concret retenu ici. Elles
concernent la même unité A10h6 et le même choix effectif, sans relancer le
commit ni les effets métier. Chaque nouvelle association conserve les contrôles
d'identité, attestation fraîche A10c, suite et permissions courantes A10h4.

Garanties des tentatives : unités suivantes suspendues pendant l'incident. A ne permet aucune
reprise automatique d'une unité déclarée en échec définitif, après échéance,
retrait de mandat ou décision de suspension. Erreur de sécurité, provider
incompatible, configuration divergente, état d'engagement ou temps restant
non vérifiable : arrêt et réconciliation, jamais erreur transitoire présumée.
Panne de réseau ne prouve pas absence de commit ; A07/A12 restent applicables.
Aucun fallback d'algorithme, renouvellement de droits ou remise à zéro des
budgets A10h7. Sans autorisation/prérequis vérifiables, action protégée refusée.
Tentatives, causes et compteurs exposés dans PBO sans données sensibles.

A10h8 A est validé le 6 octobre 2026. Tentatives d’une phase en cours sous
mandat préalable, distinctes d’une reprise après échec définitif A10h6/A10h7.
Temporisation validée en A10h9 ; valeurs et classification d’erreurs à qualifier.
Coûts CPU/RAM/attestation et trafic à qualifier ; aucune disponibilité promise.
Recette : incident transitoire qualifié, limite atteinte, budget expiré,
mandat retiré, refus TLS/attestation, commit incertain, redémarrage sans compteur
réinitialisé et absence de nouvelle unité ou effet métier dupliqué.

##### Application au PA — A10h8

Option A validée : tentatives automatiques bornées, uniquement pour erreurs techniques
transitoires de reconnexion explicitement classifiées/qualifiées. Autorisation
préalable dans mandat, nombre/intervalle/budget finis configurés ; une tentative
par canal à la fois sans boucle active. Valeurs numériques ouvertes. Même unité
A10h6/choix effectif, sans commit ou effet métier relancés ; chaque association
avec identité/attestation fraîche A10c/suite/permissions courantes A10h4.
Garanties des tentatives : nouvelles unités suspendues pendant incident. A sans reprise automatique
après échec définitif, échéance, mandat retiré ou décision de suspension.
Sécurité/provider incompatible/divergence/engagement ou temps non vérifiables
arrêtent la procédure, jamais transitoires présumés. Réseau indisponible sans
absence de commit présumée, A07/A12 conservés. Pas de fallback, droits renouvelés
ou budgets A10h7 remis à zéro ; action protégée refusée si prérequis non vérifiés.
PBO expose tentatives/causes/compteurs sans données sensibles.
A10h8 A validé le 6 octobre 2026 : phase en cours sous mandat préalable,
distincte d’une reprise après échec définitif A10h6/A10h7. Temporisation A10h9
validée, valeurs/classification à qualifier. Coûts CPU/RAM/attestation/trafic
à qualifier, aucune disponibilité garantie. Recette : transitoire qualifié,
limite/budget, retrait mandat, refus TLS/attestation, commit incertain,
redémarrage sans compteur neuf, absence d'unité ou effet métier dupliqué.

#### Scenario: Conformité du traitement A10h8

- **WHEN** un profil revendique le traitement A10h8 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--c753a71342

Source : `openspec/specs/pzt/spec.md`, ligne 3863. SHA-256 du bloc : `b4b8e4e5b3f972c4fcf55a21d1c2715025367c72839a37a53e24a9e1bdad4b05`.

~~~~text
### Requirement: Contrat A10h9 — Temporisation exponentielle plafonnée et déterministe — option A validée le 6 octobre 2026

Le rôle chargé du traitement A10h9 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10h9

Option A validée : temporisation exponentielle plafonnée, avec dispersion déterministe
bornée entre canaux. Paramètres explicites et versionnés dans PBO : intervalle
initial strictement positif, plafond fini, règles de dispersion et nombre
maximal A10h8. Même plan/canal/numéro de tentative et paramètres donnent le
même délai ; entrées stables non sensibles, sans nouveau secret ou dépendance
retenus ici. Calcul borné sans dépassement numérique, résultat dans les limites
configurées. Formule précise et valeurs restent à qualifier ; aucune promesse
que toutes les tentatives de canaux distincts seront désynchronisées.

Les limites de nombre, budgets et échéances A10h7/A10h8 restent applicables.

Garanties de temporisation : attente sans boucle active ni nouveau flux permanent. Compteur et temps
consommé conservés après redémarrage ; état non vérifiable bloquant, sans
compteur neuf ou ancienne autorisation réactivée. Avant chaque tentative,
contrôles courants et temps restant vérifiés. Si le délai prévu ou le budget
ne permet pas la tentative autorisée, aucune attente prolongée ni tentative
immédiate inventée pour atteindre le nombre maximal. Révocation, suspension
et échéance priment pendant l'attente ; garde indépendante A05 conservée.
Politique de temporisation ne modifie ni classification des erreurs A10h8,
ni suite choisie, ni identité, ni attestation A10c, ni progression A10h6.

A10h9 A est validé le 6 octobre 2026. Paramètres et formule restent à qualifier.
CPU/RAM, trafic,
coût d'attestation et délai de reprise à qualifier, aucun gain chiffré garanti.
Recette : déterminisme, intervalle/plafond invalides, très grand compteur,
canaux multiples, budget insuffisant, révocation pendant attente et redémarrage.

##### Application au PA — A10h9

Option A validée : temporisation exponentielle plafonnée et dispersion déterministe
bornée. Paramètres PBO explicites/versionnés : intervalle initial positif,
plafond fini, dispersion et nombre maximal A10h8. Même plan/canal/tentative/
paramètres donnent même délai ; entrées stables non sensibles, aucun secret
ou dépendance retenus ici. Calcul borné sans overflow, limites configurées
respectées ; formule/valeurs à qualifier, désynchronisation de tous les canaux
non garantie. Les limites de nombre, budgets et échéances A10h7/A10h8 restent applicables.

Garanties de temporisation : attente sans boucle active/flux permanent, compteur/temps consommé
conservés au redémarrage, état non vérifiable bloquant sans compteur neuf.
Contrôles courants/temps restant avant chaque tentative ; délai ou budget
insuffisant sans prolongation ni tentative immédiate inventée. Révocation/
suspension/échéance prioritaires pendant attente, garde A05 maintenue.
Classification A10h8/suite/identité/attestation A10c/progression A10h6 inchangées.
A10h9 A validé le 6 octobre 2026, paramètres/formule à qualifier.
Coûts CPU/RAM/trafic/attestation/reprise à qualifier sans
gain chiffré. Recette : déterminisme, intervalle/plafond invalides, grand
compteur, canaux multiples, budget insuffisant, révocation et redémarrage.

#### Scenario: Conformité du traitement A10h9

- **WHEN** un profil revendique le traitement A10h9 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

