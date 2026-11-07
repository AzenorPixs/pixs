# Raccords temps v2 — Adopté documentaire T0 — Non réalisé et non qualifié

En-tête : **ADOPTÉ DOCUMENTAIRE T0 — NON RÉALISÉ / NON QUALIFIÉ**. Aucune autorité déduite par cet en-tête et aucune preuve de qualification. Les valeurs réelles restent de phase ultérieure. Aucune réalisation, aucune qualification dans ce document.

`Z12 = openspec/changes/add-pzt-ca-hierarchy-rotation-and-recovery`

## A. Contrat générique pur et contrat privé Z12

Le contrat générique `pixs.time.evidence`, version `2.0.0`, catégorie `API`, propriétaire `pixs.kernel`, est une déclaration pure. Il ne confère aucune autorité temporelle, métier ou cryptographique. Il est distinct du contrat privé Z12 `z12.time_intent/v2`, schéma `2.0.0`, qui porte les 11 liaisons de demande du `§15.1` et les 16 champs d'observation du `§15.3.1`, conservés intacts.

Le futur module générique `src/pixs/kernel/contracts/time.py` contient descripteur, types et protocoles génériques, sans entrée-sortie, sans fournisseur, sans import de Core et sans import de Z12. Ce module relève de T1, aucun code en T0. Aucun troisième `Clock.now` n'est créé. Les types UTC génériques sont secondes `int64` pleine plage et nanosecondes `uint32` dans `[0..999999999]`, sans appel à `_admin_time`, sans calendrier dans Kernel. Seul le codec 27 octets de D18 et de M1 conserve l'année `1..9999` existante. Non représentabilité, invalidité, débordement entraînent refus, sans ancrage calendaire.

La façade Core `src/pixs/core/time_evidence.py` est un adaptateur consommateur et composeur hors Kernel, jamais un contrat universel importé par Kernel. Le propriétaire `pixs.kernel` décrit la déclaration pure, sans autorité sur le temps, le métier et la cryptographie. Les processus PBO, PA, PZT enregistrent leur producteur concret sous composition authentique versionnée, avec contraintes propres, sans horloge supplémentaire, sans sens de Kernel vers Core.

Vocabulaire normatif : `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, `MAY`.

Le `§15` introductif dispose que contextes, ressources et résultats internes ne sont ni des objets Python, ni une API publique de pointeurs ou capsules. Toutes les locations, contextes de budget, contextes de politique, contextes de continuité, manieurs D18 restent exclusivement privés en C et Cython, structures opaques non exportées, sans classe Python exportée, sans constructeur public appelable, sans pointeur entier, sans capsule, sans descripteur comme autorité. La future façade `pyx` effectue acquisition, vérification et consommation intérieurement dans le même propriétaire natif. Ses seules projections Python sont des références, instantanés et diagnostics non autoritaires, jamais un bail ni une preuve admissible transportée.

## B. Interface fonctionnelle commune exacte

Quatre méthodes du producteur attendu enregistré par composition, sans argument producteur client. Aucun type C opaque en Python. Aucune classe `TimeHandle`, capsule, pointeur, descripteur. Jamais d'API privée Z12 importée par Kernel, Core, PA01.

```python
def time_diagnostic(use_ref: TimePublicRef) -> TimeDiagnostic:
    pass
def time_require_use(use_ref: TimePublicRef) -> None:
    pass
def time_ceremony_diagnostic(ceremony_ref: TimePublicRef) -> TimeDiagnostic:
    pass
def time_ceremony_require_use(ceremony_ref: TimePublicRef) -> None:
    pass
```

Type `TimePublicRef` : `public_ref` du `§1`, texte `UTF-8` de `1` à `256` octets sans `NUL`, non autoritaire, lié à l'opération du propriétaire courant. Type `TimeDiagnostic` exact à quatre champs : `outcome` fermé sur `OBSERVED`, `REFUSED`, `IN_DOUBT`, `producer_ref: TimePublicRef`, `clock_domain_ref: TimePublicRef`, `detail_ref: TimePublicRef`, trois références minimisées sans secret, jamais `UTC`, incertitude, âge, manieur comme autorité. Les références diagnostiques attendues ne prouvent pas la qualification.

Garde `time_require_use` : succès `None`, aucune capacité. Échec par `TimeRefusedError` avec `reason` égal à `refusal_reason` du `§14.5`. Doute par `TimeDoubtError` avec `state_ref`, sans `refusal_reason` comme `§14.5`. Aucun résultat partiel d'admission renvoyé. Le client ne peut jamais réinjecter `TimeDiagnostic` et `None` comme permission : il doit appeler le producteur courant au point d'usage, qui observe, vérifie, consomme en interne, avec sélection courante, autres gardes décisionnelles et métier conservées. La source injectée et l'appel réel, non un DTO, fondent la condition temporelle.

## C. API native interne complète

```c
int z12_time_comp_open(Z12OwnerCtx *owner, Z12PolicyBytes *policy_bytes, Z12TimeCompositionCtx **out, Z12TimeDiag *diag);
int z12_time_comp_guard(Z12TimeCompositionCtx *c, Z12TimeDiag *diag);
int z12_time_comp_destroy(Z12TimeCompositionCtx **c, Z12TimeDiag *diag);
int z12_time_binding_resolve(Z12TimeCompositionCtx *c, Z12TimeBindingCtx **out, Z12TimeDiag *diag);
int z12_time_binding_guard(Z12TimeBindingCtx *b, Z12TimeDiag *diag);
int z12_time_binding_destroy(Z12TimeBindingCtx **b, Z12TimeDiag *diag);
int z12_time_policy_resolve(Z12TimeCompositionCtx *c, Z12TimeBindingCtx *b, Z12TimePolicyCtx **out, Z12TimeDiag *diag);
int z12_time_policy_guard(Z12TimePolicyCtx *c, Z12TimeDiag *diag);
int z12_time_policy_destroy(Z12TimePolicyCtx **c, Z12TimeDiag *diag);
int z12_time_budget_create(Z12TimeCompositionCtx *c, Z12TimeBindingCtx *b, Z12MonotonicDeadline *parent, Z12TimeBudgetCtx **out, Z12TimeDiag *diag);
int z12_time_budget_guard(Z12TimeBudgetCtx *c, Z12TimeDiag *diag);
int z12_time_budget_destroy(Z12TimeBudgetCtx **c, Z12TimeDiag *diag);
int z12_time_continuity_resolve(Z12TimeCompositionCtx *c, Z12TimeBindingCtx *b, Z12TimeContinuityCtx **out, Z12TimeDiag *diag);
int z12_time_continuity_guard(Z12TimeContinuityCtx *c, Z12TimeDiag *diag);
int z12_time_continuity_destroy(Z12TimeContinuityCtx **c, Z12TimeDiag *diag);
int z12_time_producer_resolve(Z12TimeCompositionCtx *c, Z12TimeBindingCtx *b, Z12TimeProducer **out, Z12TimeDiag *diag);
int z12_time_producer_guard(Z12TimeProducer *p, Z12TimeDiag *diag);
int z12_time_producer_destroy(Z12TimeProducer **p, Z12TimeDiag *diag);
int z12_time_use_create(Z12TimeCompositionCtx *c, Z12TimeBindingCtx *b, Z12TimeUseCtx **out, Z12TimeDiag *diag);
int z12_time_use_guard(Z12TimeUseCtx *c, Z12TimeDiag *diag);
int z12_time_use_destroy(Z12TimeUseCtx **c, Z12TimeDiag *diag);
int z12_time_observe(Z12TimeProducer *p, Z12TimePolicyCtx *pol, Z12TimeBudgetCtx *b, Z12TimeHandle **out, Z12TimeDiag *diag);
int z12_time_require_window_consume(Z12TimeHandle *h, Z12TimeUseCtx *u, Z12TimeDiag *diag);
int z12_time_invalidate(Z12TimeHandle **h, Z12TimeDiag *diag);
int z12_time_destroy(Z12TimeHandle **h, Z12TimeDiag *diag);
int z12_time_ceremony_profile_resolve(Z12TimeCompositionCtx *c, Z12TimeBindingCtx *b, Z12TimeCeremonyProfile **out, Z12TimeCeremonyDiag *diag);
int z12_time_ceremony_profile_guard(Z12TimeCeremonyProfile *p, Z12TimeCeremonyDiag *diag);
int z12_time_ceremony_profile_destroy(Z12TimeCeremonyProfile **p, Z12TimeCeremonyDiag *diag);
int z12_time_ceremony_context_create(Z12TimeCompositionCtx *c, Z12TimeBindingCtx *b, Z12TimeCeremonyProfile *prof, Z12MonotonicDeadline *parent, Z12TimeCeremonyCtx **out, Z12TimeCeremonyDiag *diag);
int z12_time_ceremony_context_guard(Z12TimeCeremonyCtx *c, Z12TimeCeremonyDiag *diag);
int z12_time_ceremony_context_destroy(Z12TimeCeremonyCtx **c, Z12TimeCeremonyDiag *diag);
int z12_ceremony_create(Z12TimeCeremonyCtx *ctx, Z12TimeCeremonyHandle **out, Z12TimeCeremonyDiag *diag);
int z12_ceremony_issue(Z12TimeCeremonyHandle *h, unsigned char *nonce_out, unsigned int nonce_capacity, Z12PublicRefView *challenge_ref_out, Z12PublicRefView *boot_ref_out, Z12TimeCeremonyDiag *diag);
int z12_ceremony_verify_consume(Z12TimeCeremonyHandle *h, Z12TimeCeremonyCtx *ctx, const Z12TimeCeremonyProofInput *candidate, Z12TimeCeremonyDiag *diag);
int z12_ceremony_invalidate(Z12TimeCeremonyHandle **h, Z12TimeCeremonyDiag *diag);
int z12_ceremony_destroy(Z12TimeCeremonyHandle **h, Z12TimeCeremonyDiag *diag);
```

`comp_open` emprunte des parents déjà sous composition D17 native, prépublication cryptographique observée à recontrôler avant admission. `binding_resolve` résout l'opération courante protégée et les 11 liaisons, liaisons non venues du client. Chaque fabrique de politique, budget, continuité, producteur, usage reçoit composition et liaison ainsi que ses parents de besoin. API opaques locales, sans ABI commune. Structure privée `Z12TimeCeremonyProofInput` non preuve, 8 membres privés exacts : pointeur constant vers octets et longueur pour `object_type`, `schema_version`, `payload_bytes`, `signature_bytes`. Vues candidates non autoritaires, copie en possédé avant contrôles, longueurs gardées, pont fermé à 4 champs refusant inconnu et dupliqué avant vues, fonction C revérifiant valeurs, types, version, charge, signature, sans nouvelle enveloppe binaire, sans clef en argument. Tampon nonce possédé par l'appelant, capacité exacte 32. Vues C de références empruntées valides jusqu'à invalidation et destruction, sans preuve `UTC`. Nonces 32 et signatures 64 pouvant contenir `NUL`, textes sans `NUL`, clef D10 attendue distincte M1 du profil authentique courant. `observe` et `create` exigent tout non nul et `*out` nul, sans perte d'ancien pointeur. `hp == NULL` invalide, `*hp == NULL` succès idempotent pour `destroy` et `invalidate`. Refus avec sortie nulle et nettoyage privé, sans validité nulle positive. Retour `1` de cycle de vie pour création, émission, garde, destruction technique seulement, sans `UTC`. Retour `1` de `observe` et `verify_consume` pour temps valide uniquement, autres `0` refus, `-1` doute, `-2` invalide.

La composition emprunte `Z12OwnerCtx` et `Z12PolicyBytes` qui `MUST` survivre à la composition. Les enfants liaison, politique, budget, continuité, producteur, usage, cérémonie, profil `MUST` survivre à leurs emprunteurs. La composition `MUST` être détruite en ordre inverse après invalidation, sans perte de pointeur restant en nettoyage privé, sans export de contexte et de manieur vers Python. La copie est interdite. Le `PID`, le `TID`, l'installation, le domaine d'horloge, la version d'opération `MUST` être revérifiés avant tout usage, la destruction de pointeur nul est idempotente. Les vues d'argument de preuve candidate sont empruntées seulement pendant l'appel avec copie bornée avant analyse. Les références émises sont empruntées jusqu'à invalidation et destruction, le tampon de nonce possédé par l'appelant. Les contraintes de sortie déjà énoncées restent inchangées.

## D. Table de profil en trois records internes non publics

Aucun fil public nouveau. Chaque champ unique, type nommé et origine exacte dans chaque record. Nul, inconnu, champ étranger, type booléen pour entier, référence non résolue entraînent refus. Les 16 champs `OBS` v2 et les 11 demandes restent strictement inchangés.

Record 1 : `calibration_kind` égal à `z12.hors_ligne_affine` et `calibration_formula_version` égale à `1.0.0` identifiant la méthode ; `model_ref` et `model_version` désignant la calibration effective opaque, sans renommage des tables.

| Champ record 1 | Type nommé | Origine exacte |
|---|---|---|
| `calibration_kind` | chaîne exacte `z12.hors_ligne_affine` | politique protégée actuelle |
| `calibration_formula_version` | chaîne exacte `1.0.0` | politique protégée actuelle |
| `profile_ref` | référence privée résolue | politique protégée actuelle |
| `profile_version` | version privée | état courant |
| `model_ref` | référence privée résolue | politique protégée actuelle |
| `model_version` | version privée | état courant |
| `rho_num` | `uint64` | profil qualifié authentique |
| `rho_den` | `uint64` strictement positif | profil qualifié authentique |
| `max_collection_error_ns` | `uint64` | profil qualifié authentique |
| `max_conversion_error_ns` | `uint64` | profil qualifié authentique |
| `max_elapsed_ns` | `uint64` obligatoire et strictement positif | profil qualifié authentique, domaine calibré du profil, non durée universelle hors ligne |
| `qualification_ref` | référence privée | preuves réelles de qualification |
| `provenance_ref` | référence privée | provenance vérifiée |
| `validity_domain_ref` | référence privée | domaine de validité qualifié |

Record 2 : ancre de référence amont courante.

| Champ record 2 | Type nommé | Origine exacte |
|---|---|---|
| `uref_ns` | `uint64` | mesure authentifiée qualifiée |
| `utc_ref_seconds` | `int64` pleine plage | mesure authentifiée qualifiée |
| `utc_ref_nanos` | `uint32 0..999999999` | mesure authentifiée qualifiée |
| `reference_monotonic_ns` | `uint64` monotone réel | mesure authentifiée qualifiée |
| `source_ref` | référence privée résolue | politique protégée actuelle |
| `source_evidence_ref` | référence privée | preuve authentifiée courante |
| `service_binding_ref` | référence privée | composition authentique |
| `clock_domain_ref` | référence privée | composition authentique |
| `boot_context_ref` | référence privée | composition authentique |
| `continuity_ref` | référence privée | continuité vérifiée |

Record 3 : liaison d'opération courante du `§15.1`.

| Champ record 3 | Type nommé | Origine exacte |
|---|---|---|
| `installation_ref` | référence privée | composition authentique |
| `target_ref` | référence privée | composition authentique |
| `operation_id` | référence privée | opération souveraine courante |
| `operation_version` | version privée | opération souveraine courante |
| `policy_ref` | référence privée | politique protégée actuelle |
| `policy_version` | version privée | état courant |
| `expected_epoch` | `uint64` | opération souveraine courante |
| `plan_ref` | référence privée | composition authentique |
| `plan_version` | version privée | état courant |
| `object_type` | chaîne exacte `z12.time_intent/v2` | demande courante |
| `schema_version` | chaîne exacte `2.0.0` | demande courante |

## E. Méthode fermée

`Delta_ns` égale instant actuel moins référence, domaine identique et continuité prouvée. Unités `rho_num` et `rho_den` dimensionnellement `ns` sur `ns`. Écarts de collecte et conversion couvrent acquisition et temps jusqu'à usage, sans double comptage réduisant la borne. Conversion des paires `int64` pleine plage, nanos normalisés, racine indépendante du calendrier D18. Pas de modèle hors domaine, pas de saut d'horloge admis, sinon invalidité.

Formule désignée par seul `calibration_kind` et `calibration_formula_version`, sans second identifiant ; `Delta_ns` inférieur ou égal à `max_elapsed_ns` obligatoire, domaine et continuité prouvés, entiers `uint64` vérifiés, plafonds conservés, paires `int64` conservées.

`U = Uref + Ecollecte + Econversion + ceil(rho_num * Delta_ns / rho_den)`

Arithmétique entière `uint64` vérifiée à chaque étape, division conservative vers le haut, paires `UTC` élargies de manière conservative avec borne `int64`, débordement refusé. `U_usage <= 1000000000`. Tout risque jusqu'à usage inclus dans la borne, âge amont indépendant de la lecture, `SYNCHRONISE <= 600s`, hors ligne supérieur à `600s` sous modèle et continuité réels, `INVERIFIABLE` sans `UTC` positif inventé.

L'estimation part de l'ancre native `UTC_ref` plus `Delta_ns` du même domaine monotone qualifié, avec `Delta_ns` inférieur ou égal à `max_elapsed_ns`, sans réancrage par lecture, nouvelle ancre seulement sur référence amont authentifiée et qualifiée. L'estimation est une addition vérifiée par paires `int64` secondes et `uint32` nanosecondes normalisées, sans époque en `int64` nanosecondes, intervalle `[estimation - U, estimation + U]` élargi de manière conservative, débordement, `Delta` négatif, pas d'horloge non couvert entraînant refus. `Uref` inclut l'incertitude de rattachement entre référence `UTC` actuelle et monotone, `Ecollecte`, `Econversion` et dérive couvrent tous risques jusqu'à usage. L'âge amont reste distinct de la date de lecture, modulo et coercition interdits. La cohérence avec l'horloge réelle `TLS` `MUST` être prouvée au point d'usage, aucune horloge hôte modifiée par LXC.

## F. Budget et continuité

Acquisition D11 sous budget global `1s`, `2` acquisitions au plus, `250ms` par acquisition, bornes descendantes inférieures ou égales au parent. Budget cérémonie D18 : global et délais positifs requis du profil `§18.3` sans défaut, valeurs de phase de qualification, sans `1s` imposé. Le contexte propriétaire est créé par composition avec échéance d'opération authentique définie par plan, non limitée implicitement à `1s` de D11. Le contexte D18 choisit le minimum du restant parent et du restant de profil dès création et ne prolonge jamais le parent. Acquisitions D11 autour de la réponse avec limites descendantes par décision authentique et temps réel écoulé ne réarmant ni nonce, ni mandat, ni R01. Attente humaine et latence de source et canal restent incertitudes du profil, si `U_usage` supérieur à `1s` ou latence non démontrée alors refus, sans grâce. Tous budgets écoulés avec suspension et reboot invalidant nonces et baux, profils de continuité réels séparés. Candidat LXC conservé, D9 indépendante.

Les profils réels du `§18.3` bornent canal, source, dérive, attente, avec 22 champs et 4 champs préservés. Exemple conservateur adopté sans aller simple nul supposé : `e` émission native, `r` réception, `u` usage monotones du même domaine qualifié, `u >= r >= e` ; mesure extérieure `m` dans `[e, r]`. Bornes `UTC` d'usage égales à `[borne_basse_mesure + (u - r) - E, borne_haute_mesure + (u - e) + E]` avec `E` borne réelle de dérive, collecte, conversion qualifiée et arrondis vers le large. Aucune époque convertie en plein `int64` nanosecondes ; si indémontrable, débordement, refus, `U_usage` supérieur à `1s` alors `TIME_UNVERIFIABLE`. Intervalle entier pour certificats `TLS`, horloge réelle `TLS` à dates actives, sans grâce et sans `nocerttimecheck`. Le profil de temps possède des paramètres d'erreur de taux positifs à dérivation bornée selon `§18.3`, sans nouvelles valeurs par défaut, sans budget de cérémonie imposé à `1s`. Une attente manuelle extérieure trop incertaine reste refusée sans aucune confiance par la seule signature D10. Calibrage de source physique futur à qualifier, sans code actuel.

## G. D18 fermé et graphes concrets

Fabrique, émission, vérification et consommation D18 :

```c
int z12_ceremony_create(Z12TimeCeremonyCtx *ctx, Z12TimeCeremonyHandle **out, Z12TimeCeremonyDiag *diag);
int z12_ceremony_issue(Z12TimeCeremonyHandle *h, unsigned char *nonce_out, unsigned int nonce_capacity, Z12PublicRefView *challenge_ref_out, Z12PublicRefView *boot_ref_out, Z12TimeCeremonyDiag *diag);
int z12_ceremony_verify_consume(Z12TimeCeremonyHandle *h, Z12TimeCeremonyCtx *ctx, const Z12TimeCeremonyProofInput *candidate, Z12TimeCeremonyDiag *diag);
int z12_ceremony_invalidate(Z12TimeCeremonyHandle **h, Z12TimeCeremonyDiag *diag);
int z12_ceremony_destroy(Z12TimeCeremonyHandle **h, Z12TimeCeremonyDiag *diag);
```

`issue` reçoit tampon nonce 32 possédé par l'appelant et capacité exacte 32, projections de références publiques de défi et contexte d'amorçage bornées déjà existantes, aucune preuve `UTC`. Durée des tampons et références vues définie par l'appel. `verify_consume` reçoit candidate `Z12TimeCeremonyProofInput const*`, structure privée non preuve, 4 vues bornées pour `object_type`, `schema_version`, `payload_bytes`, `signature_bytes` et longueurs, jamais clef D10 en argument. Le pont opérateur natif refuse toute enveloppe malformée, inconnue, dupliquée avant projection, l'entrée C entièrement non fiable est recopiée en possédé avant usage. Pas de nouveau pointeur Python ni nouveau format public : les 4 champs logiques `§18.2` restent strictement identiques. Chaque longueur gardée, nonce public 32 et signature 64 pouvant contenir `NUL`, textes sans `NUL`, clé attendue résolue depuis profil de build authentique courant. Signature Ed25519 pure sur charge binaire existante 22 champs et préfixes strictement conservés. Ancienne preuve et défi rejoués refusés avant usage.

Graphe initial concret : observations natives du propriétaire sans admission, authenticité locale du profil, intervalle candidat D11 avec D18, validité finale par politique, profil, garde d'usage, puis `TLS`, PZT, PG, métier. Graphe d'inclusion concret : `deadline`, `admin_profile`, `operator_verify` amenant `_openssl_ed25519` une fois, `launch_obs`, `systemd_connection`, `process_image`, `manager_unit`, `owner_context`, `policy_bytes`, `admin_codec`, `admin_values`, `admin_verify`, `admin_time`, puis `_chrony_protocol`, `_chrony_request`, `_chrony_receive`, `_chrony_socket`, `_chrony_query`, puis `_time_obs` et `_ceremony`, puis `_tls_time_window`. Clé attendue D10 distincte M1, 22 champs, enveloppe 4 champs, domaines, nonce 32, signature 64 strictement inchangés, clé jointe interdite, volatil à usage unique, dates `TLS` actives, `nocerttimecheck` interdit, horloge hôte LXC non modifiable. D18 exception et après D6 seules autorités ordinaires courantes, sinon refus sans réouverture initiale.

## H. Matrice propriétaires et adaptateurs

| Propriétaire | Site exact existant | Prochain fichier adaptateur | Producteur et garde |
|---|---|---|---|
| Kernel et runtime | `src/pixs/kernel/contracts/models.py`, `src/pixs/kernel/contracts/__init__.py` | futur `src/pixs/kernel/contracts/time.py`, T1, présence à recontrôler avant autorisation de source | abstractions génériques admises, fournisseur concret interdit |
| Core | `src/pixs/core/services_common.py`, `src/pixs/core/authz/ports.py` | futur `src/pixs/core/time_guard.py`, T1 et T3, présence à recontrôler avant autorisation de source | vérification de l'intervalle entier au point d'usage |
| Auth | `src/pixs/auth/bootstrap_metadata.py` et fabriques | futur `src/pixs/auth/time_guard.py`, T1 et T3, présence à recontrôler avant autorisation de source | recoupement source, politique, état courant |
| Agent | `src/pixs/agent/authorization.py:180`, `src/pixs/agent/service.py:87`, `src/pixs/agent/ports.py:140` | futur `src/pixs/agent/time_guard.py`, T1 et T3, présence à recontrôler avant autorisation de source | refus si `INVERIFIABLE`, `.now()` conservé pour horodatage |
| PZT | `src/pixs/pzt/adapters.py:84` | futur `src/pixs/pzt/time_guard.py`, T1 et T3, présence à recontrôler avant autorisation de source | consommation d'évidence fermée, seul `C04` décide |
| PA et pixs.agent | `src/pixs/pa_native/builder.py:1`, `linker.py:1`, `postgresql_observation.py:106` | futur `src/pixs/pa_native/time_service.pyx`, T1 et T3, présence à recontrôler avant autorisation de source | un service par horloge sous `pixs.agent`, échanges par PZT |
| Z12 natif | `src/pixs/pzt_ca/native/_chrony_protocol.pxi`, `_chrony_request.pxi`, `_chrony_receive.pxi`, `_chrony_socket.pxi`, `_chrony_query.pxi`, `_monotonic_deadline.pxi`, `_owner_context.pxi`, `_admin_time.pxi`, `_operator_verify.pxi` et fichiers chrony existants à compléter quand nécessaire | futur `src/pixs/pzt_ca/native/_time_obs.pxi`, `src/pixs/pzt_ca/native/_ceremony.pxi`, `src/pixs/pzt_ca/native/_tls_time_window.pxi` consommé nativement, façades `src/pixs/pzt_ca/time_handle.pyx` et `src/pixs/pzt_ca/ceremony_handle.pyx`, présence à recontrôler avant autorisation de source | producteur local par horloge, report distant simple diagnostic |

Temps documentaire PA01 déjà aligné mais B proposé et profil réel non qualifié. Pas d'adoption de leurs codes et documents ici. Conserver `Clock.now` compatible sans valeur de preuve v2.

Recettes de construction : voir la conception adoptée [design.md](design.md) et le manifeste construit avant qualification ; aucune version, dépendance ou condensat nouveau n'est introduit ici.

## I. Manifeste complet T1, T2, T3, T4

Réalisation, contrôles locaux, correction, retest et validation par unité T1, T2, T3 avant suivante ; T4 qualification intégrée et contrôle global final distinct. Toutes réalisations et tests restent futurs hors T0. Aucune écriture T0 dans `src` et `tests`.

| Chemin projet complet | Statut | Rôle |
|---|---|---|
| `src/pixs/kernel/contracts/time.py` | futur T1, présence à recontrôler avant autorisation de source | Kernel, descripteurs et types génériques |
| `src/pixs/kernel/contracts/__init__.py` | existant à modifier, exports génériques, T1 | Kernel, façade |
| `tests/unit/test_time_contract.py` | futur T1, présence à recontrôler avant autorisation de source | T1, tests locaux du contrat générique pur |
| `tests/integration/test_contract_descriptors_integration.py` | existant à modifier, oracle façade étendu T1, tests locaux | T1, intégration façade : union descripteurs et contrat temps |
| `src/pixs/core/services_common.py` | existant à modifier, T1 et T3 | Core, garde d'usage |
| `src/pixs/core/authz/ports.py` | existant à modifier, T1 | Core, ports |
| `src/pixs/core/time_evidence.py` | futur T1, présence à recontrôler avant autorisation de source | Core, adaptateur hors Kernel |
| `src/pixs/core/time_guard.py` | futur T1 et T3, présence à recontrôler avant autorisation de source | Core, garde d'usage |
| `src/pixs/auth/bootstrap_metadata.py` | existant à modifier, T1 et T3 | Auth, recoupement |
| `src/pixs/auth/time_guard.py` | futur T1 et T3, présence à recontrôler avant autorisation de source | Auth, garde d'usage |
| `src/pixs/agent/authorization.py` | existant à modifier, T1 et T3 | Agent, garde d'usage |
| `src/pixs/agent/service.py` | existant à modifier, T1 et T3 | Agent, garde d'usage |
| `src/pixs/agent/ports.py` | existant à modifier, T1 | Agent, ports |
| `src/pixs/agent/time_guard.py` | futur T1 et T3, présence à recontrôler avant autorisation de source | Agent, garde d'usage |
| `src/pixs/pzt/adapters.py` | existant à modifier, T1 et T3 | PZT, branchement |
| `src/pixs/pzt/time_guard.py` | futur T1 et T3, présence à recontrôler avant autorisation de source | PZT, garde d'usage |
| `src/pixs/pa_native/time_service.pyx` | futur T1 et T3, présence à recontrôler avant autorisation de source | PA système, producteur local |
| `src/pixs/pzt_ca/native/_time_obs.pxi` | futur T1, présence à recontrôler avant autorisation de source | Z12, assemblage D11 tous modes |
| `src/pixs/pzt_ca/time_handle.pyx` | futur T1, présence à recontrôler avant autorisation de source | Z12, façade privée |
| `src/pixs/pzt_ca/native/_ceremony.pxi` | futur T2, présence à recontrôler avant autorisation de source | Z12, cycle D18 |
| `src/pixs/pzt_ca/ceremony_handle.pyx` | futur T2, présence à recontrôler avant autorisation de source | Z12, façade privée |
| `src/pixs/pzt_ca/native/_tls_time_window.pxi` | futur T1 et T2, présence à recontrôler avant autorisation de source | Z12, comparateur `TLS` intervalle entier consommé nativement |
| `src/pixs/pzt_ca/native/_chrony_protocol.pxi` et fichiers chrony existants à compléter quand nécessaire | existants à compléter, T1 | Z12, transport local |
| `tests/unit/test_time_evidence_window.py` | futur T1 et T4, présence à recontrôler avant autorisation de source | Z12, contrôles locaux d'unité puis qualification intégrée, fenêtres et refus |
| `tests/unit/test_time_hors_ligne_model.py` | futur T1 et T4, présence à recontrôler avant autorisation de source | Z12, contrôles locaux d'unité puis qualification intégrée, modèle affine et bornes |
| `tests/unit/test_time_suspend_reboot.py` | futur T1, T2 et T4, présence à recontrôler avant autorisation de source | Z12, suspension et restauration |
| `tests/unit/test_ceremony_nonce_replay.py` | futur T2 et T4, présence à recontrôler avant autorisation de source | Z12, nonce et rejeu |
| `tests/unit/test_tls_window.py` | futur T1, T2 et T4, présence à recontrôler avant autorisation de source | Z12, `TLS` et dérive |
| `tests/integration/z12/native_time_math.c` | realise T1-B1, harnais arithmetique pure | Z12, harnais arithmétique pure : bornes, arrondis et refus |
| `src/pixs/pzt_ca/native/z12_time_budget.inc` | futur T1-B2, presence a recontrôler avant autorisation de source | Z12, budget math pur |
| `tests/integration/z12/native_time_budget_check.c` | futur T1-B2, presence a recontrôler avant autorisation de source | Z12, harnais budget pur |
| `tests/integration/test_time_producer_consumer.py` | futur T3 et T4, présence à recontrôler avant autorisation de source | Z12 et runtime, contrôles locaux de raccord puis qualification intégrée, producteur et consommateurs |
| `tests/integration/test_time_pa_service.py` | futur T3 et T4, présence à recontrôler avant autorisation de source | PA système, service local |

Sources et profils natifs si nécessaires pour trois records et budget, identifiants futurs à choisir maintenant : `src/pixs/pzt_ca/native/z12_time_profile.inc` d'abord restreint T1-B1 aux seuls helpers arithmétiques purs (aucune valeur de profil physique, aucun calibrage, aucune admission), puis `src/pixs/pzt_ca/native/z12_time_budget.inc` B2 restreint aux helpers arithmetiques purs (plafonds 1s/250ms/2 tentatives, sans composition ni admission), sans partage d'ABI. Tous modes D11 incluant hors ligne complet, sans SYNCHRONISE seul. Aucun refus systématique présenté comme livraison autonome.

Le producteur runtime PA est une implémentation Cython sous son propriétaire, avec catalogue et supervision par pixs.agent. La construction et la liaison pures ne qualifient pas le runtime. Aucun import privé Z12 ni horloge nouvelle dans Kernel. Le chemin pyx est proposé au détenteur PA01 pour T3, sans permission de code ici.
