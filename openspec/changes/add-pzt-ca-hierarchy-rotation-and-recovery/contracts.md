# Contrats — Z12, documentaire 1.0.0

## 0. Statut

Préparation de la tâche 4. Structures logiques fermées pour
`A10i6–A10i20`, complétées au §12 par D4/D5/D6 adoptés pour la première installation avant PostgreSQL. Aucune activation ou qualification de
runtime supplémentaire ; le profil de test adopté dans design.md reste la référence. Aucune signature, non-exportabilité, exclusion, bascule ou
migration revendiquée. Les ports nommés `P.Z12_*` sont des définitions
documentaires futures, pas des contrats runtime existants.

Sources exactes : `proposal.md` Z12 et graphe `Z12→Z03→Z06`,
`design.md` profil 22/10 et `D1/D2/D3` adoptés 23/10,
`requirements.md` copies `pzt/185` + `A10i6–A10i20`, canon seul
normatif, `TECHNICAL §45.4`. Contrats sources référencés :
`src/pixs/core/command_metadata.py` (`CommandMetadata`), contrats
`A07` portés par `Z06`, contrats `A12` portés par `Z03`. Aucune
enveloppe `core.envelope` ou `a12.engagement_proof` fictive n'est
présentée comme existante.

## 1. Primitives typées

- `public_ref` : chaîne non vide, sans secret ni clé privée. Vide ou
  secret refusé. Deux références peuvent partager la même chaîne
  opaque ; les espaces de noms et types d'identités restent distincts.
  L'indépendance des clés se prouve sur le matériau public et le
  fournisseur, pas sur la seule inégalité des textes.
- `non_negative_int` : entier `>= 0`. Flottant, chaîne ou booléen à la
  place d'un entier refusé. Le rejet du booléen vaut uniquement comme
  substitut d'entier ; `is_ca` booléen `true` extrait des octets du
  certificat `X509` reste admis et cohérent avec `closed_enum[true]`.
- `utc_timestamp` : `RFC3339` avec fuseau, `UTC` seul. Heure naïve
  refusée.
- `closed_enum` : valeur dans la liste fermée. Valeur inconnue refusée.
- `public_set` : tableau de `public_ref` ou d'énum fermé, sans
  doublon. Doublon refusé. Vide admis seulement si indiqué.
- `public_text` : `UTF-8`, `LF`, sans secret ni clé.
- `evidence_ref` : `public_ref` vers enveloppe `A07/A12` ou preuve
  contrôleur existante. Référence pendante refusée.
- Aucun délai, seuil de fraîcheur, quorum ou budget inventé. Les
  durées rappelées au §10 sont le canon, non une ré-autorisation.

Règle commune : les champs de chaque tableau sont exhaustifs ; tout champ inconnu, type divergent, clé JSON dupliquée ou version autre que la chaîne `1.0.0` est refusé. Un champ facultatif est absent ; `null` ne le remplace pas. Un booléen ne remplace jamais un entier, y compris `path_len`. Les références sont typées par leur usage et résolues auprès de leur propriétaire, pas interprétées comme une URL à télécharger. Une référence seule ne prouve aucun état.

Le `context_ref` des opérations désigne le contexte serveur vérifié : sujet, tenant/scope et corrélation de `CommandMetadata`, rattachement domaine/autorité/périmètre, politique, mandat et époque courants. Les égalités entre ce contexte, demande, décision, plan, cible, contenu authentifié et source autoritative sont contrôlées avant effet. Aucun contexte fourni par le demandeur ne devient une autorité par sa seule forme. Une donnée historique n’accorde aucune permission courante. La syntaxe ne peut garantir à elle seule l’absence de secret dans une chaîne : seules références publiques contrôlées et diagnostics prédéfinis sont émis.

## 2. Autorité racine et émetteur intermédiaire séparés

Le schéma racine est par domaine, sans `logical_authority` obligatoire.
Le schéma intermédiaire est par domaine, autorité et périmètre. Ne
jamais confondre `domain` et `root_ref`, ni `logical_authority` et
`issuer_id`, ni `key_ref`, `generation_id` et `cert_ref`.

### 2.1 `z12.root_authority/v1` — racine hors ligne par domaine

| champ | req/opt | type | propriétaire | notes |
|---|---|---|---|---|
| `object_type` | req | `closed_enum[z12.root_authority/v1]` | `Z12` définit | discriminateur |
| `schema_version` | req | `closed_enum[1.0.0]` | `Z12` définit | bornée |
| `domain` | req | `public_ref` | registre `Django` | domaine de confiance |
| `root_ref` | req | `public_ref` | registre `Django` | ancre publique |
| `root_key_ref` | req | `public_ref` | registre `Django` | publique seule |
| `root_cert_ref` | req | `public_ref` | registre `Django` | auto-signé public |
| `root_generation_id` | req | `public_ref` | registre `Django` | génération racine indépendante |
| `key_created_at` | req | `utc_timestamp` | registre `Django` | génération de la paire, pas activation |
| `root_key_material_ref` | req | `public_ref` | fournisseur `TPM2` | clé publique réelle, aucune donnée privée |
| `status` | req | `closed_enum[prepared,active,retired]` | registre `Django` | retrait sans retour implicite ; jamais permission de signer |

Pas de `logical_authority` exigée ici. Clé privée jamais présente.

### 2.2 `z12.intermediate_issuer/v1` — frère dédié par autorité

| champ | req/opt | type | propriétaire | notes |
|---|---|---|---|---|
| `object_type` | req | `closed_enum[z12.intermediate_issuer/v1]` | `Z12` définit | discriminateur |
| `schema_version` | req | `closed_enum[1.0.0]` | `Z12` définit | bornée |
| `domain` | req | `public_ref` | registre `Django` | même domaine que racine |
| `logical_authority` | req | `public_ref` | registre `Django` | autorité métier habilitée |
| `emission_scope` | req | `public_ref` | registre `Django` | périmètre d'émission |
| `issuer_id` | req | `public_ref` | registre `Django` | émetteur dédié |
| `issuer_role` | req | `closed_enum[principal,standby]` | registre `Django` | frères sous même racine |
| `key_ref` | req | `public_ref` | registre `Django` | publique, indépendante |
| `generation_id` | req | `public_ref` | registre `Django` | identité de génération |

Principal et secours frères, clés indépendantes, jamais actifs
conjointement pour les nouvelles émissions dans le même
`domain / logical_authority / emission_scope`. Invariant canon
conservé : une génération admise pour les nouvelles émissions par
émetteur.

## 3. Demande avec discriminateur fermé

### 3.1 `z12.ca_request/v1` — demande courante `A10i`, sans droit accordé

| champ | req/opt | type | propriétaire | notes |
|---|---|---|---|---|
| `object_type` | req | `closed_enum[z12.ca_request/v1]` | `Z12` définit | discriminateur |
| `schema_version` | req | `closed_enum[1.0.0]` | `Z12` définit | bornée |
| `request_id` | req | `public_ref` | `PBO` remplit, `Django` vérifie | unique |
| `request_kind` | req | `closed_enum[terminal_issuance,intermediate_certification,root_succession]` | `PBO` remplit | aiguillage conditionnel |
| `domain` | req | `public_ref` | `Django` vérifie | domaine |
| `policy_version` | req | `public_ref` | `Django` autoritatif | politique courante |
| `epoch` | req | `non_negative_int` | `Django` autoritatif | époque réconciliée |
| `requested_at` | req | `utc_timestamp` | `PBO` remplit | instant courant |
| `command_metadata_ref` | req | `public_ref` | contrat `Core CommandMetadata` | lien `CommandMetadata` |
| `context_ref` | req | `public_ref` | `Django` vérifie | contexte serveur et rattachements courants |
| `target_generation_ref` | opt | `public_ref` | registre `Django` | exigé pour certification intermédiaire |
| `root_plan_ref` | opt | `public_ref` | registre `Django` | exigé pour succession racine |
| `subject_ref` | opt | `public_ref` | `PBO` remplit | exigé si `terminal_issuance` |
| `subject_public_key_ref` | opt | `public_ref` | `PBO` remplit | exigé si `terminal_issuance` |
| `possession_proof_ref` | opt | `public_ref` | `PBO` remplit | exigé si `terminal_issuance` |
| `terminal_contracts_ref` | opt | `public_ref` | `A07/A12` canon | exigé si `terminal_issuance`, `A10i–A10i5` courants |
| `target_issuer_id` | opt | `public_ref` | `PBO` remplit | exigé si `intermediate_certification` |
| `offline_procedure_ref` | opt | `public_ref` | `Django` autoritatif | exigé si `intermediate_certification` ou `root_succession`, mandat hors ligne distinct |
| `supersedes_request_id` | opt | `public_ref` | `PBO` remplit | demande antérieure seule |

Exclusivité des branches : `terminal_issuance` exige les quatre champs terminaux `subject_ref`, `subject_public_key_ref`, `possession_proof_ref`, `terminal_contracts_ref` et interdit `target_issuer_id`, `target_generation_ref`, `offline_procedure_ref`, `root_plan_ref`. `intermediate_certification` exige `target_issuer_id`, `target_generation_ref`, `offline_procedure_ref` et interdit les quatre champs terminaux ainsi que `root_plan_ref`. `root_succession` exige `offline_procedure_ref`, `root_plan_ref` et interdit les quatre champs terminaux et les deux cibles intermédiaires. La procédure hors ligne référence un mandat opérateur explicite, jamais déduit de la demande.

Champ inconnu refusé. `terminal_issuance` consomme identité, sujet,
possession et clé publique plus contrats terminaux courants, et rend
un artéfact terminal, jamais un objet `CA:true`. Certification
intermédiaire et succession racine passent par procédure hors ligne
sous mandat distinct, jamais par appel racine quotidien ni accès
`PBO` à la clé.

## 4. Décision courante séparée de l'engagement `A12`

### 4.1 `z12.ca_decision/v1` — admissibilité `A10i`

| champ | req/opt | type | propriétaire | notes |
|---|---|---|---|---|
| `object_type` | req | `closed_enum[z12.ca_decision/v1]` | `Z12` définit | discriminateur |
| `schema_version` | req | `closed_enum[1.0.0]` | `Z12` définit | bornée |
| `decision_id` | req | `public_ref` | `Django` autoritatif | unique |
| `request_id` | req | `public_ref` | `Django` autoritatif | lie `3.1` |
| `context_ref` | req | `public_ref` | `Django` autoritatif | lié à la demande et à la source courantes |
| `verdict` | req | `closed_enum[admitted,refused]` | `Django` autoritatif | sans troisième valeur |
| `mandate_ref` | opt | `public_ref` | `Django` autoritatif | requis et admissible si `admitted` ; absent admis pour un refus, notamment `mandate_missing` |
| `decision_epoch` | req | `non_negative_int` | `Django` autoritatif | époque courante |
| `a07_envelope_ref` | opt | `public_ref` | canon `A07`, réalisation `Z06` future | transport et version |
| `authorized_issuer` | opt | `public_ref` | `Django` autoritatif | exigé si `admitted`, interdit si `refused` |
| `authorized_key_ref` | opt | `public_ref` | `Django` autoritatif | exigé si `admitted`, interdit si `refused` |
| `authorized_generation` | opt | `public_ref` | `Django` autoritatif | exigé si `admitted`, interdit si `refused` |
| `refusal_code` | opt | `closed_enum[out_of_scope,unknown_issuer,unknown_generation,policy_mismatch,mandate_missing,mandate_expired,epoch_stale,exclusion_pending,precondition_failed]` | `Django` autoritatif | exigé si `refused`, interdit si `admitted` |
| `refusal_detail_public` | opt | `public_text` | `Django` autoritatif | sans secret |

Un refus sur émetteur, clé ou génération inconnus ne peut exiger des
références autorisées valides du registre. La signature `CA` ne vaut
jamais engagement `PostgreSQL`.

## 5. Génération et certificat public vérifié sur octets

### 5.1 `z12.ca_generation/v1` — génération intermédiaire

| champ | req/opt | type | propriétaire | notes |
|---|---|---|---|---|
| `object_type` | req | `closed_enum[z12.ca_generation/v1]` | `Z12` définit | discriminateur |
| `schema_version` | req | `closed_enum[1.0.0]` | `Z12` définit | bornée |
| `generation_id` | req | `public_ref` | registre `Django` | identité de génération |
| `issuer_id` | req | `public_ref` | registre `Django` | émetteur unique |
| `key_ref` | req | `public_ref` | registre `Django` | publique, indépendante |
| `key_created_at` | req | `utc_timestamp` | registre `Django` | âge de la paire, pas activation |
| `key_material_ref` | req | `public_ref` | fournisseur `TPM2` | matériau public, preuve d'indépendance |
| `status` | req | `closed_enum[prepared,reserved,active,retired]` | registre `Django` | transitions §9 |
| `created_epoch` | req | `non_negative_int` | registre `Django` | sans remise à zéro |
| `predecessor_generation_id` | opt | `public_ref` | registre `Django` | absent à la première activation |

### 5.2 `z12.ca_certificate/v1` — métadonnées non preuves

| champ | req/opt | type | propriétaire | notes |
|---|---|---|---|---|
| `object_type` | req | `closed_enum[z12.ca_certificate/v1]` | `Z12` définit | discriminateur |
| `schema_version` | req | `closed_enum[1.0.0]` | `Z12` définit | bornée |
| `cert_ref` | req | `public_ref` | signataire exécute | publique |
| `cert_bytes_ref` | req | `public_ref` | signataire exécute | artéfact cryptographique à vérifier, jamais preuve d’engagement ou permission |
| `ca_kind` | req | `closed_enum[root,intermediate]` | `Z12` définit | rôle typé explicite |
| `root_authority_ref` | req | `public_ref` | registre `Django` | racine du domaine attendu |
| `subject_key_ref` | req | `public_ref` | registre `Django` | clé publique correspondant aux octets |
| `generation_ref` | req | `public_ref` | registre `Django` | génération racine §2.1 ou intermédiaire §5.1 selon rôle |
| `issuer_ref` | opt | `public_ref` | registre `Django` | requis si intermédiaire, interdit si racine |
| `basic_constraints_critical` | req | `boolean true` | extrait du certificat | critique obligatoire |
| `key_usage_critical` | req | `boolean true` | extrait du certificat | critique obligatoire |
| `is_ca` | req | `boolean true` | extrait des octets | `true` seul, `false` refusé |
| `path_len` | req | `closed_enum[0,1]` | `Z12` définit | `1` si `root`, `0` si `intermediate` |
| `key_usage` | req | `public_set` de `closed_enum[keyCertSign]` | `Z12` définit | seule valeur |
| `signature_algorithm` | req | `closed_enum[ecdsa-with-SHA256]` | `Z12` définit | profil fixe |
| `curve` | req | `closed_enum[secp256r1]` | `Z12` définit | `P-256` seul |
| `serial_public` | req | `public_ref` | signataire exécute | numéro X.509 public valide et unique par émetteur, vérifié sur octets |
| `not_before_utc` | req | `utc_timestamp` | signataire exécute | contrôlée |
| `not_after_utc` | req | `utc_timestamp` | signataire exécute | contrôlée |
| `fingerprint_public` | req | `public_ref` | signataire exécute | calculée sur octets |
| `authority_key_id` | opt | `public_ref` | signataire exécute | facultatif si `root` auto-signé, toujours exigé si `intermediate` |
| `subject_key_id` | req | `public_ref` | signataire exécute | `RFC5280` |
| `anchor_ref` | req | `public_ref` | registre `Django` | vérifiée selon `ca_kind` |

Les dates, algorithmes, usages et empreintes déclarés sans
correspondance aux octets vérifiés sont refusés. `AKI` absent pour une
racine auto-signée concrètement admise ; `AKI` exigé pour un
intermédiaire. Aucun usage `TLS`, `WireGuard`, `A12`, `cRLSign` ou
`OCSP` ajouté. `CA:false`, profondeur supplémentaire, extension
critique inconnue, mauvais algorithme, émetteur frère ou ancrage non
provisionné refusés.

## 6. Exclusion par arrêt extérieur seul, preuve vérifiée

Profil `D1` retenu : arrêt du périmètre par contrôleur extérieur.
Les valeurs `inhibit_generation` et `inhibited` et toute alternative
fournisseur non sélectionnée sont supprimées des énum et des ports.

### 6.1 `z12.ca_exclusion/v1` — directive, pas preuve

| champ | req/opt | type | propriétaire | notes |
|---|---|---|---|---|
| `object_type` | req | `closed_enum[z12.ca_exclusion/v1]` | `Z12` définit | discriminateur |
| `schema_version` | req | `closed_enum[1.0.0]` | `Z12` définit | bornée |
| `exclusion_id` | req | `public_ref` | `Django` autoritatif | unique |
| `target_issuer_id` | req | `public_ref` | `Django` autoritatif | cible exacte |
| `target_generation_id` | req | `public_ref` | `Django` autoritatif | génération exacte |
| `target_key_ref` | req | `public_ref` | `Django` autoritatif | clé publique exacte |
| `request_id` | req | `public_ref` | `Django` autoritatif | demande courante liée |
| `context_ref` | req | `public_ref` | `Django` autoritatif | contexte actuel |
| `operation_version` | req | `public_ref` | `Django` autoritatif | version de l’opération contrôlée |
| `epoch_current` | req | `non_negative_int` | `Django` autoritatif | époque actuelle réconciliée |
| `target_set` | req | `public_set` | `Django` autoritatif | processus et sessions avec voie de signature |
| `operation` | req | `closed_enum[stop_perimeter]` | `Django` autoritatif | seule méthode du profil |
| `reason_code` | req | `closed_enum[incident_rotation,planned_rotation,loss_recovery,succession,compromise_suspected,compromise_known]` | `Django` autoritatif | motif explicite |
| `mandate_ref` | req | `public_ref` | `Django` autoritatif | couvre cible et impacts |
| `a12_context_ref` | opt | `public_ref` | canon `A12`, réalisation `Z03` future | contexte d'engagement lié |

### 6.2 `z12.ca_proof/v1` — constat du contrôleur compétent

| champ | req/opt | type | propriétaire | notes |
|---|---|---|---|---|
| `object_type` | req | `closed_enum[z12.ca_proof/v1]` | `Z12` définit | discriminateur |
| `schema_version` | req | `closed_enum[1.0.0]` | `Z12` définit | bornée |
| `proof_id` | req | `public_ref` | contrôleur atteste, `Django` vérifie | unique |
| `exclusion_id` | req | `public_ref` | contrôleur atteste | lie `6.1` |
| `request_id` | req | `public_ref` | contrôleur atteste | demande courante |
| `controller_id` | req | `public_ref` | contrôleur atteste | contrôleur compétent |
| `target_issuer_id` | req | `public_ref` | contrôleur atteste | égalité avec directive |
| `target_key_ref` | req | `public_ref` | contrôleur atteste | égalité avec directive et registre |
| `target_generation_id` | req | `public_ref` | contrôleur atteste | égalité avec directive et registre |
| `target_set` | req | `public_set` | contrôleur atteste | non vide, tous processus et sessions visés |
| `operation` | req | `closed_enum[stop_perimeter]` | contrôleur atteste | égalité avec directive |
| `operation_version` | req | `public_ref` | contrôleur atteste | égalité avec directive |
| `context_ref` | req | `public_ref` | `Django` vérifie | lié à la demande et au contenu authentifié |
| `mandate_ref` | req | `public_ref` | `Django` vérifie | mandat courant couvrant cible et impacts |
| `applied_state` | req | `closed_enum[stopped]` | contrôleur atteste | observé, pas revendiqué |
| `prohibition_maintained` | req | `closed_enum[maintained,not_maintained]` | contrôleur atteste | maintien vérifié |
| `observed_at` | req | `utc_timestamp` | contrôleur atteste | instant courant |
| `epoch_current` | req | `non_negative_int` | contrôleur atteste | réconciliée |
| `proof_content_ref` | req | `public_ref` | contrôleur atteste | contenu authentifié, pas seul identifiant signataire |
| `proof_signature_ref` | req | `public_ref` | contrôleur atteste | signature du contenu vérifiée |

Un reçu, `ACK`, journal ou retrait d'accès seul ne prouve rien. Preuve
périmée, rejouée, partielle ou non liée refuse la bascule. Les
signataires `A12` restent distincts des clés `CA`. Le seul
`proof_signer_ref` ne prouve ni contenu ni signature ; les liens et
vérifications ci-dessus rendent les données déterminantes
authentifiées.

Les champs cibles, opération/version, demande, contexte/mandat et époque de la preuve sont égaux à ceux de la directive et du registre courant. Le contenu authentifié référencé inclut intégralement ces liaisons ; sa signature est vérifiée avec l’identité du contrôleur compétent et les contrôles A12 applicables. `prohibition_maintained=maintained` est requis à l’activation ; `not_maintained`, preuve ancienne ou périmètre incomplet bloquent la bascule. Une signature ou référence d’engagement A12 seule ne prouve pas l’arrêt effectif : Django recoupe le constat système actuel et son maintien. Le caractère facultatif de `a12_context_ref` dans une directive stockée n’autorise jamais d’effet exigeant A12 sans engagement courant admissible.

## 7. Registre, résultat et cycle de vie

Les listes publiques sont versionnées et rattachées au domaine et à l’époque. Un instantané seul ne vaut pas confiance : disponibilité, admissibilité de la source et qualification restent exigées. Les tableaux §7.2–§7.8 en fixent exhaustivement la structure.

### 7.1 `z12.ca_result/v1` — validation, engagement et effet séparés

| champ | req/opt | type | propriétaire | notes |
|---|---|---|---|---|
| `object_type` | req | `closed_enum[z12.ca_result/v1]` | `Z12` définit | discriminateur |
| `schema_version` | req | `closed_enum[1.0.0]` | `Z12` définit | bornée |
| `result_id` | req | `public_ref` | invocateur, `Django/A12` qualifient | unique |
| `operation_id` | req | `public_ref` | invocateur | clé d'idempotence 1/2 |
| `operation_version` | req | `public_ref` | invocateur | clé d'idempotence 2/2 |
| `request_id` | req | `public_ref` | invocateur | demande liée |
| `context_ref` | req | `public_ref` | `Django` vérifie | contexte et versions liés à l’opération observée |
| `result_kind` | req | `closed_enum[current_operation,historical_operation]` | rapporteur | historique distinct d’une autorisation actuelle |
| `recorded_at` | req | `utc_timestamp` | rapporteur | instant de l’observation |
| `engagement_ref` | opt | `evidence_ref` | propriétaire `A12` | requis si `engagement_outcome=engaged` |
| `effect_evidence_ref` | opt | `evidence_ref` | exécutant, `Django` vérifie | requis si `effect_outcome=applied`, constat d’effet distinct du reçu d’engagement |
| `input_fingerprint` | req | `public_ref` | validateur | empreinte exacte de l'entrée validée |
| `validation_outcome` | req | `closed_enum[valid,invalid,uncertain]` | validateur `Z12` | chaîne et politique |
| `engagement_outcome` | req | `closed_enum[engaged,not_engaged,unknown]` | `A12` seul | engagement autoritatif |
| `effect_outcome` | req | `closed_enum[not_started,applied,failed,uncertain]` | exécutant | effet observé |
| `error_code` | opt | `closed_enum[ok,refused,precondition_failed,exclusion_missing,proof_invalid,epoch_stale,mandate_invalid,dependency_unavailable,conflict,unknown]` | rapporteur | codée, sans secret |

Un effet non commencé se représente `not_started`, jamais `failed`.
Un `ACK` confirme seulement une admission. Un effet envoyé dont la fin est inconnue vaut `uncertain` ; `failed` exige un échec réellement observé ; `applied` exige une application réellement observée. `error_code=ok` ne prouve pas l’effet. Signature et engagement restent distincts. Pour une opération courante, validation `invalid` impose engagement `not_engaged` et effet `not_started` ; engagement `unknown` interdit tout nouvel effet. Un ancien résultat peut être consulté après autorisation courante de lecture et réconciliation, avec `result_kind=historical_operation` ; il conserve ses faits historiques et ne rétablit jamais une permission d’émettre. Même identifiant avec empreinte/version/contexte/époque différents : conflit sans effet, jamais réinterprétation.

Les schémas fermés de registre et de cycle de vie sont détaillés ci-dessous. Les références croisées sont résolues et leurs domaines, versions, époques, clés, générations et périmètres doivent correspondre au contexte courant. Les champs conditionnels de dates/preuves sont absents au stade préparé et requis aux stades engagés et retirés ; un statut engagé sans ces faits est refusé. Une preuve conservée d’une étape passée ne vaut jamais permission courante.

### 7.2 Inventaire — `z12.ca_inventory/v1`

Les seuls champs sont ceux ci-dessous et les deux champs communs requis `object_type="z12.ca_inventory/v1"`, `schema_version="1.0.0"`. Propriétaire : registre Django/PostgreSQL.

| champ | requis/condition | type | sens |
|---|---|---|---|
| `inventory_id` | requis | `public_ref` | identité d’inventaire |
| `domain` | requis | `public_ref` | domaine de confiance |
| `epoch` | requis | `non_negative_int` | époque actuelle |
| `inventory_version` | requis | `public_ref` | version du contenu autoritatif |
| `issuer_refs` | requis | `public_set` | émetteurs dédiés, vide admis si aucun |
| `generation_refs` | requis | `public_set` | générations connues et typées, vide admis |
| `cert_refs` | requis | `public_set` | artéfacts publics vérifiables, vide admis |
| `anchor_refs` | requis | `public_set` | ancres explicitement provisionnées, vide admis sans admission |
| `engagement_ref` | requis | `evidence_ref` | engagement A12 du contenu/version, distinct de son application |

### 7.3 État CA — `z12.ca_state/v1`

Les seuls champs sont ceux ci-dessous et les deux champs communs requis `object_type="z12.ca_state/v1"`, `schema_version="1.0.0"`. Propriétaire : registre Django/PostgreSQL.

| champ | requis/condition | type | sens |
|---|---|---|---|
| `state_id` | requis | `public_ref` | identité de l’état |
| `domain` | requis | `public_ref` | domaine |
| `epoch` | requis | `non_negative_int` | époque réconciliée |
| `state_version` | requis | `public_ref` | version autoritative |
| `admitted_issuer_refs` | requis | `public_set` | émetteurs permis par la politique, vide admis |
| `active_generation_refs` | requis | `public_set` | sélection effective via les rattachements autorité/périmètre, vide admis |
| `withdrawn_generation_refs` | requis | `public_set` | générations retirées, vide admis ; aucune intersection avec actives |
| `anchor_refs` | requis | `public_set` | ancres actuelles et suivantes du plan admis, vide admis sans admission |
| `anchor_status` | requis | `closed_enum[not_admitted,current_only,coexistence_admitted,successor_only]` | aucune confiance si not_admitted |
| `succession_plan_ref` | conditionnel | `public_ref` | requis en coexistence et lors du retrait lié à succession |
| `current_decision_ref` | requis | `public_ref` | décision courante A10i, pas certificat |
| `engagement_ref` | requis | `evidence_ref` | engagement A12 du contenu/version |

### 7.4 Rotation intermédiaire — `z12.ca_rotation/v1`

Les seuls champs sont ceux ci-dessous et les deux champs communs requis `object_type="z12.ca_rotation/v1"`, `schema_version="1.0.0"`. Propriétaire : Django pour décision et registre ; signataire pour effet cryptographique.

| champ | requis/condition | type | sens |
|---|---|---|---|
| `plan_ref` | requis | `public_ref` | identité du plan de rotation normale |
| `plan_version` | requis | `public_ref` | version courante |
| `context_ref` | requis | `public_ref` | contexte et mandat de rotation planifiée, pas mandat d’incident A10i11 |
| `domain` | requis | `public_ref` | domaine |
| `logical_authority` | requis | `public_ref` | autorité habilitée |
| `emission_scope` | requis | `public_ref` | périmètre |
| `issuer_ref` | requis | `public_ref` | émetteur concerné |
| `from_generation_ref` | requis | `public_ref` | génération précédente intacte |
| `to_generation_ref` | requis | `public_ref` | nouvelle paire indépendante et certificat propre |
| `offline_procedure_ref` | requis | `public_ref` | recertification par racine hors ligne sous mandat explicite |
| `deadline_utc` | requis | `utc_timestamp` | borne finie du plan courant, sans défaut inventé ni prolongation |
| `status` | requis | `closed_enum[prepared,engaged,withdrawn]` | progression sans retour de droit |
| `engaged_at_utc` | si engaged/withdrawn | `utc_timestamp` | engagement autoritatif de la succession d’émetteur |
| `engagement_ref` | si engaged/withdrawn | `evidence_ref` | engagement A12 courant du plan |
| `exclusion_proof_ref` | si engaged/withdrawn | `evidence_ref` | exclusion du précédent vérifiée avant engagement |
| `withdrawn_at_utc` | si withdrawn | `utc_timestamp` | retrait observé, distinct de la seule échéance |

### 7.5 Perte de clé intermédiaire — `z12.ca_loss/v1`

Les seuls champs sont ceux ci-dessous et les deux champs communs requis `object_type="z12.ca_loss/v1"`, `schema_version="1.0.0"`. Propriétaire : Django pour décision et registre, fournisseur pour faits matériels.

| champ | requis/condition | type | sens |
|---|---|---|---|
| `loss_id` | requis | `public_ref` | identité de l’incident |
| `incident_version` | requis | `public_ref` | version actuelle |
| `context_ref` | requis | `public_ref` | contexte de récupération autorisée |
| `issuer_ref` | requis | `public_ref` | émetteur intermédiaire affecté et rattachements résolus |
| `lost_generation_ref` | requis | `public_ref` | génération perdue, corrompue ou remplacée |
| `loss_class` | requis | `closed_enum[lost,corrupted,replaced,suspected_compromise,known_compromise]` | retrait A05 prioritaire |
| `detected_at_utc` | requis | `utc_timestamp` | constat de l’incident, pas début d’une grâce |
| `recovery_state` | requis | `closed_enum[detected,recertification_pending,reconciled,blocked]` | état inspectable sans droit implicite |
| `replacement_generation_ref` | facultatif | `public_ref` | nouvelle paire indépendante seulement |
| `offline_procedure_ref` | si recertification_pending/reconciled | `public_ref` | procédure de recertification hors ligne |
| `reconciliation_ref` | si reconciled | `evidence_ref` | réconciliation des références, états et autorisations courants |

### 7.6 Succession racine normale — `z12.ca_succession/v1`

Les seuls champs sont ceux ci-dessous et les deux champs communs requis `object_type="z12.ca_succession/v1"`, `schema_version="1.0.0"`. Propriétaire : Django pour plan et engagement ; opérateur mandaté pour cérémonie hors ligne.

| champ | requis/condition | type | sens |
|---|---|---|---|
| `plan_ref` | requis | `public_ref` | identité du plan commun |
| `plan_version` | requis | `public_ref` | version courante du périmètre et des étapes |
| `context_ref` | requis | `public_ref` | contexte et mandat opérateur explicite |
| `domain` | requis | `public_ref` | même domaine de confiance |
| `scope_ref` | requis | `public_ref` | périmètre de migration autorisé et versionné |
| `from_root_ref` | requis | `public_ref` | racine actuelle non compromise |
| `to_root_ref` | requis | `public_ref` | racine suivante, nouvelle paire indépendante |
| `offline_procedure_ref` | requis | `public_ref` | cérémonie et certification hors ligne |
| `deadline_utc` | requis | `utc_timestamp` | borne finie du plan autorisé, jamais inventée par défaut |
| `anchor_bound_at_utc` | requis | `utc_timestamp` | fin d’admissibilité courante de l’ancienne ancre |
| `status` | requis | `closed_enum[prepared,engaged,withdrawn]` | préparation distincte de coexistence |
| `engaged_at_utc` | si engaged/withdrawn | `utc_timestamp` | début commun unique engagé A07/A12 |
| `withdraw_at_utc` | si engaged/withdrawn | `utc_timestamp` | échéance commune, bornée par engagement +30j, ancre et mandat |
| `engagement_ref` | si engaged/withdrawn | `evidence_ref` | engagement commun A07/A12 vérifiable |
| `withdrawn_at_utc` | si withdrawn | `utc_timestamp` | retrait effectif observé, sans retour implicite |

### 7.7 Migration sous coexistence — `z12.ca_migration/v1`

Les seuls champs sont ceux ci-dessous et les deux champs communs requis `object_type="z12.ca_migration/v1"`, `schema_version="1.0.0"`. Propriétaire : registre Django/PostgreSQL ; PA produit les observations, Django les vérifie.

| champ | requis/condition | type | sens |
|---|---|---|---|
| `migration_id` | requis | `public_ref` | identité de migration |
| `succession_plan_ref` | requis | `public_ref` | plan commun §7.6, jamais plan local remplaçant sa borne |
| `plan_version` | requis | `public_ref` | version actuelle du plan |
| `domain` | requis | `public_ref` | même domaine que plan |
| `scope_ref` | requis | `public_ref` | périmètre autorisé, sans exclusion implicite de PA hors ligne |
| `from_anchor_ref` | requis | `public_ref` | ancienne ancre du plan |
| `to_anchor_ref` | requis | `public_ref` | nouvelle ancre du plan explicitement provisionnée |
| `engagement_ref` | requis | `evidence_ref` | référence au même engagement commun |
| `engaged_at_utc` | requis | `utc_timestamp` | égalité avec le début commun du plan |
| `withdraw_at_utc` | requis | `utc_timestamp` | égalité avec échéance commune, pas remise à zéro |
| `anchor_bound_at_utc` | requis | `utc_timestamp` | borne du plan, pas nouveau délai par PA |
| `applied_observation_refs` | requis | `public_set` | observations §7.8, vide admis sans convergence |
| `status` | requis | `closed_enum[prepared,engaged,withdrawn]` | aucun retrait repoussé pour non-convergence |

### 7.8 Observation d’application — `z12.ca_application_observation/v1`

Les seuls champs sont ceux ci-dessous et les deux champs communs requis `object_type="z12.ca_application_observation/v1"`, `schema_version="1.0.0"`. Propriétaire : PA/exécutant atteste via son contrat PZT ; Django vérifie le fait actuel et son rattachement.

| champ | requis/condition | type | sens |
|---|---|---|---|
| `observation_id` | requis | `public_ref` | identité du constat |
| `association_ref` | requis | `public_ref` | association PA concrète actuellement dans le périmètre |
| `plan_ref` | requis | `public_ref` | plan de succession courant |
| `plan_version` | requis | `public_ref` | version appliquée |
| `domain` | requis | `public_ref` | domaine du plan |
| `scope_ref` | requis | `public_ref` | périmètre autorisé |
| `target_anchor_ref` | requis | `public_ref` | nouvelle ancre effectivement appliquée |
| `target_generation_ref` | requis | `public_ref` | génération attendue, liée aux certificats admis |
| `observed_at_utc` | requis | `utc_timestamp` | instant de l’observation |
| `applied_proof_ref` | requis | `evidence_ref` | preuve d’application PZT vérifiée, pas simple reçu de distribution |
| `epoch` | requis | `non_negative_int` | époque actuelle vérifiée |

## 8. Ports documentaires futurs

Les noms ci-dessous sont des points de contrat Z12 documentaires, pas des API déjà livrées. Les données déterminantes et références sont liées au contexte vérifié et à la même opération ; les consommateurs ne choisissent ni autorité ni politique à partir d’un certificat reçu.

| port | entrée | sortie | refus ou incertitude | propriétaire de l’effet et de sa preuve |
|---|---|---|---|---|
| `P.Z12_SUBMIT_REQUEST` | §3.1 + contexte Core/A07 courant | demande enregistrée et identifiant, sans droit | forme/version/champ/branche/contexte inadmissibles | Django vérifie, transport A07 fourni par Z06 à qualifier |
| `P.Z12_DECIDE` | demande et source de politique/mandat actuelle | §4.1, décision A10i sans preuve automatique de commit | demande hors périmètre, mandat/époque invalides ; refus explicite sans effet | Django décide ; Z12 ne se substitue pas à A12 |
| `P.Z12_REGISTER_GENERATION` | §2.1 ou §2.2 + §5.1 et faits fournisseur | enregistrement public rattaché à sa clé et génération | réemploi de paire, identité/rattachement incohérents, protection requise invérifiable | Django registre ; fournisseur prouve les faits matériels |
| `P.Z12_ISSUE_TERMINAL` | demande terminale §3.1, décision admise, génération active, engagement A12 courant | artéfact terminal suivant A10i–A10i5 + résultat §7.1 | possession/périmètre/admissibilité/protection/engagement manquants, mauvaise génération, retrait connu | service CA réalise la signature ; Django et A12 vérifient décision et engagement distincts |
| `P.Z12_CERTIFY_CA` | demande CA §3.1 et procédure racine hors ligne sous mandat propre | §5.2 vérifié et résultat §7.1 | clé/rôle/dates inadmissibles, racine indisponible ou retirée pour certification, procédure non autorisée | opérateur mandaté et service de cérémonie hors ligne ; Django enregistre les références publiques |
| `P.Z12_EXCLUDE` | directive §6.1 et contrôles courants | directive engagée puis constat §6.2 si effet observé | cible/périmètre imprécis, mandat inadmissible, arrêt global implicite, contrôleur indisponible | Django décide, contrôleur extérieur exécute ; aucun ACK ne prouve le fait |
| `P.Z12_PROVE_EXCLUSION` | constat réel du contrôleur, directive et contexte actuels | §6.2 authentifié et vérifié | preuve partielle, ancienne, mal liée, non compétente ou prohibition non maintenue | contrôleur atteste, Django vérifie le fait actuel et son maintien |
| `P.Z12_FAILOVER` | politique/mandat incident préalable, secours valide, décision courante, exclusion vérifiée, engagement A12 | sélection active unique engagée et résultat observé | cause hors mandat, suspicion/compromission, principal non exclu, état incertain ou secours inadmissible | Django/A12 engagent la sélection ; exécutant prouve son application |
| `P.Z12_ROTATE` | plan §7.4 et nouvelle paire/certificat protégés | étapes et résultat §7.1 | rotation planifiée couverte seulement par mandat incident, ancienne clé réutilisée, absence exclusion/recertification | Django pour plan ; cérémonie et signataire pour effets |
| `P.Z12_RECOVER` | incident §7.5 et mandat de récupération courant | nouvelle paire/recertification/réconciliation, sans reprise ancienne clé | état invérifiable, paire réutilisée, ancien signataire encore actif, recertification absente | Django et propriétaires réels du fournisseur, de la cérémonie et de l’exclusion |
| `P.Z12_SUCCEED` | plan normal §7.6 et nouvelle racine indépendante non compromise | engagement commun ou étape préparée ; aucun ancrage appris automatiquement | compromission traitée comme succession normale, paire réutilisée, nouveau périmètre non autorisé | opérateur hors ligne pour clé/certificat ; Django/A12 pour plan courant |
| `P.Z12_MIGRATE` | §7.7 lié au plan commun engagé et observations §7.8 | migration inspectable et retrait effectif à sa borne | plan/version/époque/périmètre étrangers, reçu de distribution sans application, remise à zéro du délai | Django vérifie les associations et preuves ; PA applique via PZT |
| `P.Z12_RECONCILE` | identité/version/empreinte et contexte courant de l’opération | faits durables et observés, résultat courant ou historique explicitement distingués | même identifiant avec contenu différent, source/périmètre non admissibles, effet inconnu pris pour réussite | Django/A12 et exécutant réel ; aucune réémission aveugle |
| `C.A07_ENVELOPE` | commande/lecture/notification autorisée et versionnée | transport et état/deltas admis par le contrat A07 | type/version/droit/ordre ou contexte inadmissibles | Z06 est propriétaire de réalisation future ; canon A07 seul acquis |
| `C.A12_ENGAGEMENT` | décision/mandat/version/époque et octets liés | état d’engagement autoritatif et assertion signée admissible, jamais preuve publique du commit par signature seule | source inadmissible, engagement manquant/incertain, mauvais contexte ou retrait connu | Z03 est propriétaire de réalisation future ; canon A12 seul acquis |
| `C.TPM2_SIGN` | référence de clé locale protégée, demande autorisée et octets à signer | signature et données publiques contrôlées | fournisseur/protection indisponibles, extraction privée ou repli logiciel demandés | fournisseur matériel réellement qualifié ; les prévols de tâche2 ne suffisent pas |
| `C.CONTROLLER_EXEC` | directive §6.1, cible/version/mandat courants | arrêt observé et prohibition persistante ; preuve §6.2 | voie de relance non médiatisée, périmètre incomplet, mauvaise cible, indisponibilité | contrôleur extérieur compétent ; Django vérifie, sans toucher les autres services |

Données publiques contrôlées seulement en charge utile. Les clés privées et blobs privés protégés restent dans le service et le dispositif de clé prévus ; aucune clé privée dans PostgreSQL, le PBO, un PA ordinaire, les résultats ou les journaux. Une référence publique de clé ne contient aucun matériau privé.

## 9. Transitions et retrait `A05`

Ces transitions concernent les générations intermédiaires du §5.1 : `prepared -> reserved -> active -> retired`, plus `prepared -> retired`
et `reserved -> retired` pour abandon et retrait d'une clé compromise
ou expirée sans passer par `active`. Première activation sans
prédécesseur sans preuve d'exclusion d'une cible inexistante ;
exclusion exigée dès remplacement et bascule. Compromission connue :
retrait `A05` bloque immédiatement l’émission, sans attendre un mandat
nouveau et sans permettre un autre usage ; persistance ensuite sous
contexte autorisé. `retired` ne redevient jamais `active`. Retrait
anticipé si convergence prouvée, sinon à l'échéance engagée même si
des `PA` restent non migrés. Dès engagement de la succession racine normale, l’ancienne racine ne certifie plus de nouveaux intermédiaires ; son ancre peut rester temporairement admissible pour vérifier les certificats antérieurs selon le plan et les contrôles courants. Fin de coexistence au plus tôt de `engaged_at_utc + 30 jours`, `anchor_bound_at_utc` et la borne du mandat/plan ; l’échéance engagée ne peut être prolongée par reconnexion, retard, clone ou restauration. Une convergence anticipée exige l’ensemble des associations actuelles du périmètre et des observations appliquées admissibles ; une liste de reçus ou un PA exclu implicitement du périmètre ne suffit pas.

La racine du §2.1 utilise les transitions d’inventaire `prepared -> active -> retired` et `prepared -> retired`, sans étape de secours en ligne `reserved`. Son statut ne donne aucune permission de signature courante : clé toujours hors ligne, procédure sous mandat opérateur et admissibilité d’ancrage contrôlée séparément. Une racine retirée n’est jamais réactivée par restauration.

## 10. Bornes canoniques rappelées et calculs observables

Intermédiaires `365/240/125 jours`, racine `7300/5840/1460 jours`,
seuils effectifs `240/365` et `4/5` sur validité effective, coexistence
au plus `30 jours` depuis engagement commun, chevauchement terminal
au plus `5 minutes`. Jour de `24 heures`, `UTC`, horloge qualifiée.
Atteindre un seuil n'autorise ni signature racine autonome ni bascule.
Âge de paire depuis `key_created_at`, validités des certificats
racine et intermédiaires, `engaged_at_utc`, `withdraw_at_utc` et borne
d'ancrage observés. `withdrawal_epoch` ambigu banni comme substitut
temporel.

## 11. Traçabilité et revue documentaire

| bloc normatif | objets et sections | invariant | cas de contrôle documentaire issu du canon |
|---|---|---|---|
| `pzt/185` | §1, §2, §6, §7.8 | identité et contexte actuels ; aucune confiance par clone, snapshot ou cohébergement | preuve ancienne réutilisée par clone : réévaluation avant admission |
| `A10i6` | §2, §3, §5, ports CA | PKI dédiée ; racine hors ligne, CA distinctes des signataires opérationnels | chaîne/ancrage autorisés ; demande hors périmètre, panne, émission incertaine et clé inaccessible au PA ordinaire |
| `A10i7` | §2.2, §3, §4, §7.3 | émetteur dédié par autorité/périmètre ; pas de confiance par nom issuer ni racine commune seule | émetteur frère interdit, chemin alternatif, membres multiples, changement de rattachement et restauration |
| `A10i8` | §5.1, §6, C.TPM2_SIGN | profil matériel obligatoire sans repli ; confidentialité et protection réelles | fournisseur absent, protection invérifiable, extraction privée demandée, panne/reprise sans droit restauré |
| `A10i9` | §7.5, P.Z12_RECOVER | perte/corruption/remplacement : nouvelle paire et recertification, pas de restauration privée comme reprise | perte, redémarrage normal distinct, ancien détenteur actif, état incertain, provider ou racine indisponible |
| `A10i10` | §2.2, §5.1, §9 | secours frère pré-certifié indépendant, réserve sans pouvoir d’émettre | activation admise/refusée, principal actif, secours expiré/compromis, panne commune et réapprovisionnement |
| `A10i11` | §4, §6, P.Z12_FAILOVER | bascule seulement sous mandat préalable couvrant cibles/causes/durée/opérations et conditions cumulatives | mandat absent/expiré/hors cause, suspicion, secours invalide, exclusion/engagement incertains et doublon |
| `A10i12` | §6.1–§6.2, §9 | exclusion extérieure active et vérifiée avant successeur | clé déjà utilisable, arrêt partiel, mauvaise cible, preuve ancienne, partition, relance/clone/restauration |
| `A10i13` | §6, C.CONTROLLER_EXEC | méthode arrêt retenue, interdiction persistante, principal et secours contrôlables séparément | sessions préexistantes, contrôleur indisponible, voie de relance alternative, escalade refusée, secours affecté |
| `A10i14` | §5.2, ports CA/TPM2 | ECDSA P-256 et SHA-256 pour racine et intermédiaires ; crypto non réimplémentée | algorithme/clé incohérents, encodage invalide, usages/chaîne incorrects et repli interdit |
| `A10i15` | §7.4, §9 | nouvelle paire à chaque renouvellement ; exclusion et mandat de rotation propres | réemploi de clé, réserve préparée, racine indisponible, exclusion manquée et restauration |
| `A10i16` | §5.1–§5.2, §7.4, §10 | âge depuis génération, durée effective et seuil 240/365 ; terminal borné par validité résiduelle | durée nominale/raccourcie, certificat tardif, réserve âgée, rotation inachevée, horloge et révocation |
| `A10i17` | §2.1, §5.2, §7.6, §10 | durée racine et seuil 4/5 ; admissibilité d’ancrage opposable même si bibliothèque ignore ses dates | certificat tardif/raccourci, ancre expirée, intermédiaire trop long, succession manquée et PA hors ligne |
| `A10i18` | §2.1, §7.6–§7.8 | nouvelle paire racine indépendante, provisionnement authentifié et preuve appliquée avant usage | même clé, fausse ancre/périmètre, preuve d’application absente, retrait connu et restauration |
| `A10i19` | §7.3, §7.6–§7.8, §9 | coexistence planifiée actuelle/suivante ; préparation, engagement, application et retrait distincts | ancre non autorisée, distribution sans application, nouvelle association, double émission, état ancien et incertitude |
| `A10i20` | §7.6–§7.8, §10 | plafond commun 30 jours depuis engagement, retrait anticipé sur convergence prouvée | application tardive sans reset, plan inachevé, horloge invérifiable, retrait anticipé et rejet après échéance |

La revue de tâche4 établit ces liaisons et vérifie la cohérence des structures, sans produire de test fonctionnel ni de PASS. Les recettes réelles requises restent à exécuter dans les tâches qui réalisent les effets. Pour ce premier profil Debian13 matériel, les plateformes Windows, autres Linux, LXC et les garanties du profil logiciel ne sont pas sélectionnées ni qualifiées ; leurs essais sont non applicables à cette recette précise. Cela ne dispense jamais les dépendances A07/A12, le canal PZT, la protection matérielle, le registre ou le contrôleur requis pour un effet concerné.

## 12. Contrat initial Z12 consommé par C08 — documentaire 1.0.0

Les cinq ports ci-dessous sont adoptés comme définitions documentaires de l’extension, pas comme API disponibles ou qualifiées. Ils sont distincts des 17 ports ordinaires du §8. Z12 est seul propriétaire de la cérémonie, des primitives CA et de l’état PKI initial ; C08 orchestre sans second émetteur/registre. La seule exception aux décisions/engagements ordinaires A10i6/A12a est bornée par les deux exigences initiales de pzt/authorization et D4/D5/D6 de design.md. Les schémas ordinaires des §§2–9 conservent leur propriétaire Django ; ils ne sont pas détournés pour fabriquer son autorité avant PG.

### 12.1 Entrées et sources de confiance

Le contrat logique initial est fermé et versionné 1.0.0. Il lie installation, cible matérielle, exécutants/rôles/périmètre, identité d’opération et idempotence, version/digest du plan, politique protégée et version, mandat opérateur, contexte natif, bornes/validités/révocation/fraîcheur, audit durable et ancrage TPM NV courant. Les références publiques sont typées par usage ; aucune clé privée, credential PG, objet étranger, version inconnue ou champ supplémentaire n’est admis. Les identités et preuves sont lues et vérifiées par leurs propriétaires compétents, jamais déclarées fiables par l’appelant.

La branche initiale possède un contexte natif propre, indépendant de PostgreSQL, PLATFORM sans tenant_id ni scope_id. Elle ne forge pas un Subject applicatif ou CommandMetadata ordinaire avant disponibilité de leur source. La preuve native du lanceur/opérateur et la politique de la composition de confiance sont vérifiées positivement. UID 0, premier PBO, proximité, booléen client, clé/certificat, fichier présent ou reçu C01 ne suffisent pas. Le mandat initial n’est pas une preuve R01 réutilisée et ne prolonge pas ses pouvoirs.

Une initial_evidence_ref désigne ici une preuve initiale réellement vérifiée par le propriétaire technique : elle reste distincte de evidence_ref du §1, laquelle désigne les sources ordinaires A07/A12/contrôleur. Aucune référence, structure, signature CA ou copie de journal ne prouve par sa seule forme un effet, une autorité actuelle ou un commit PG. Les formats de preuve, paramètres réels et profils de protection sont précisés et qualifiés avant effet, sans défaut de production tiré d’une fixture.

### 12.2 Ports et résultats séparés

| Port | Entrée déterminante | Effet et résultat | Refus / issue incertaine |
|---|---|---|---|
| prepare_initial_trust | Mandat/politique/opérateur natifs vérifiés, installation/cible, plan/version/digest, rôles, opération/idempotence, ancrage et audit admissibles | Z12 admet puis prépare et réalise les seules créations PKI/identités initiales fermées ; résultat inspectable et références publiques liées aux faits matériels | État initial non prouvé, ressources/protection/mandat/ancrage indisponibles ; aucune seconde PKI ni réémission aveugle |
| inspect_initial_trust | Référence d’opération et contexte actuel admissible, accès au propriétaire réel de l’état | Lecture courante des étapes, effets, références et preuves ; aucune nouvelle clé, signature ou permission | Source absente/ancienne, état restauré, identité ou cible étrangère : résultat non prêt, pas succès par snapshot |
| reconcile_initial_trust | Même opération/plan, preuves actuelles et mandat de réconciliation admissible | Rapproche effets réellement observés, journal et ancrage ; distingue historique, incertain et résultat actuel sans répéter un effet engagé | Contenu divergent, effet inconnu ou ancrage incohérent : blocage inspectable, jamais remise à zéro |
| adopt_initial_trust | Lot public et effets vérifiables, contexte et propriétaires courants disponibles, demande d’adoption liée à l’opération | Adoption et relecture indépendantes des références publiques sous PKI/Core/Auth/C05 ; preuve réelle de la transaction propriétaire PG et de son audit, sans clé privée | Source/autorité/engagement absents ou incertains : aucune adoption confirmée, aucun droit ordinaire |
| retire_initial_authority | Adoption courante prouvée, directive bornée, contrôleur compétent et ancrage qualifié | Retrait durable et irréversible de l’autorité, voies/canal/mandats et sessions initiales ; preuve indépendante vérifiable avant admission ordinaire | Adoption/retrait/ancrage incertains, arrêt partiel ou ancien contexte : aucun passage prêt ni restauration de droit |

Le résultat public relie sa version, l’opération, le plan, l’installation/cible et la politique aux références de l’inventaire public CA/certificats/générations/matériau, au résultat local, à l’audit, à l’état/ancrage courant et, lorsqu’ils existent réellement, à l’adoption PG, au retrait initial et à l’admission ordinaire. L’absence d’une preuve exigée pour une étape interdit d’exposer cette étape comme accomplie. La signature et les octets publics sont vérifiés séparément de l’autorisation et de la transaction. L’inventaire conserve les identités distinctes domaine/racine/autorité/émetteur/clé/génération/certificat des sections ordinaires, sans leur attribuer un enregistrement Django encore absent.

### 12.3 États et passage

Le vocabulaire fermé documentaire est PREPARED, EXECUTING, INITIAL_TRUST_READY, ADOPTION_PENDING, ADOPTED_FENCED, INITIAL_AUTHORITY_RETIRED, ORDINARY_READY, IN_DOUBT et BLOCKED. Un état absent n’est pas une preuve de première installation. Chaque transition lie l’opération et sa version au plan/politique/cible courants et à l’ancrage ; une concurrence incompatible ou un effet perdu ne reçoit jamais deux confirmations.

- PREPARED constate les préconditions admissibles, sans preuve d’effet. EXECUTING rend inspectable le début d’exécution sous fencing.
- INITIAL_TRUST_READY exige les faits et références publiques initiales vérifiés ; il n’accorde aucun droit métier ou contrôle ordinaire. ADOPTION_PENDING suit une demande admissible au propriétaire courant.
- ADOPTED_FENCED exige adoption/commit/audit courants réellement prouvés ; l’admission ordinaire reste fermée tant que le retrait initial n’est pas prouvé.
- INITIAL_AUTHORITY_RETIRED exige retrait attesté et ancrage/tombstone durable, irréversible et protégé ; la vérification indépendante du contexte/admission ordinaire reste requise pour ORDINARY_READY.
- IN_DOUBT et BLOCKED restent inspectables. La reprise réconcilie l’effet et le contexte courant, sans revenir à PREPARED par restauration ni rejouer un mandat consommé. Une autorité retirée ne revient jamais initiale.

Ces étapes ne sont pas une transaction atomique entre TPM/système local et PostgreSQL. Le propriétaire PG adopte les références et son audit par sa frontière transactionnelle réelle ; le contrôleur et le dispositif protégé attestent les effets système/ancrage. Aucune PKI supplémentaire ou recertification systématique n’est imposée par le passage, sans remise à zéro des âges, dates, validités, retraits ou rotations canoniques. Les capacités initiales et sessions privilégiées sont retirées sans fabriquer une permission ordinaire à partir du même certificat.

### 12.4 Ancrage et recette encore à réaliser

D5 retient un ancrage monotone TPM NV dédié, lié à installation/cible/étape et protégé contre l’effacement/réinitialisation ou accès non autorisé par les signataires. Le journal logiciel ne suffit pas contre sa propre restauration. Une absence, un clone, une valeur ancienne ou une protection invérifiable ferme la branche ; aucun index existant ou inventaire de handles n’est adopté comme ancre. Aucun index, attribut, politique/authentification ou droit NV de l’hôte courant n’est autorisé par le présent document. Un plan exact et une autorisation distincte précèdent sa recette.

La recette porte sur provenance native et opérateur, politiques/mandats invalides ou révoqués, cibles étrangères, premier PBO auto-admis, champs/types/versions, état initial invérifiable, concurrence, réponse perdue/crash entre chaque étape, ancien journal/clone/restauration, retrait partiel et reprise après passage, plus adoption publique et interdiction d’une seconde PKI. Aucune simulation, référence ou déclaration client ne qualifie l’ancrage, la protection des clés ou les propriétaires A07/A12 réels. Les 53 unités et le smoke TPM2 historique restent des preuves bornées distinctes.

## 13. Identités et résolution TLS initiales — D7/D8 adoptés le 23 octobre 2026

### 13.1 Statut, propriétaires et sources

Les deux schémas ci-dessous et le port de composition sont documentaires, versionnés et fermés. Ils ne déclarent aucun fournisseur, transport ou contrat A07/A12 disponible ou qualifié. Les règles de types, champs inconnus, doublons et versions du §1 s'appliquent. Le profil normatif est celui de [specs/pzt/spec.md](specs/pzt/spec.md), repris à l'identique dans [requirements.md](requirements.md) et dans le [canon PZT](../../specs/pzt/spec.md). Les objets terminaux restent distincts des objets CA des §§2–7 et de toute clé personnelle de mandat PostgreSQL.

Le terme propriétaire courant désigne la source réellement compétente pour l'étape constatée : Z12 initial D4, sous identité native et mandat opérateur liés au plan protégé/versionné, avant le passage D6 ; puis, après adoption et retrait attesté, exclusivement le propriétaire ordinaire Django/A07/A12 courant. Le demandeur ne choisit pas ce propriétaire par un champ ou un booléen. Le registre public, la politique protégée, le contrôleur compétent et l'ancrage sont relus et recoupés ; leur seule référence, un DTO ou un snapshot ne les remplace pas. L'identité initiale n'a pas de tenant_id ou scope_id fabriqués avant PostgreSQL. Les contrôles du propriétaire ordinaire restent soumis à leurs contrats réels, sans API inventée.

### 13.2 Schéma fermé z12.initial_terminal_identity/v1

Dans ce §13, current_evidence_ref désigne initial_evidence_ref du §12.1 dans la branche initiale, puis evidence_ref du §1 sous le propriétaire ordinaire après D6 ; la source découle de l'étape réelle vérifiée, jamais du choix du demandeur. Les champs obligatoires sont exhaustifs ; le seul champ facultatif est conditionnel à l'usage serveur. Les références restent publiques et typées par leur usage ; aucune valeur n'est un chemin de clé privée.

| champ | req/opt | type | propriétaire et contrôle |
|---|---|---|---|
| object_type | req | closed_enum[z12.initial_terminal_identity/v1] | Z12 définit le discriminateur |
| schema_version | req | closed_enum[1.0.0] | Z12 définit la version |
| identity_ref | req | public_ref | propriétaire courant ; identité de cet objet |
| installation_ref | req | public_ref | propriétaire courant ; installation liée au plan |
| target_ref | req | public_ref | propriétaire courant ; cible native réelle |
| terminal_ref | req | public_ref | propriétaire courant ; terminal PA/PZT/PBO sélectionné |
| native_instance_ref | req | public_ref | source native authentifiée, recoupée par le propriétaire courant |
| instance_uuid | req | texte UUIDv7 canonique minuscule | propriétaire courant ; même instance que native_instance_ref, jamais une preuve de fraîcheur |
| role_ref | req | public_ref | propriétaire courant ; rôle prévu par la politique |
| tls_usage | req | closed_enum[clientAuth,serverAuth] | propriétaire courant ; exactement un usage |
| server_ipv4 | opt | texte IPv4 loopback canonique | exigé pour serverAuth, interdit pour clientAuth ; IP exacte de l'endpoint au plan |
| key_ref | req | public_ref opaque locale | fournisseur matériel, résolution privée ; jamais référence CA ni chemin réseau |
| key_generation_ref | req | public_ref | propriétaire courant ; génération réelle de la clé terminale |
| cert_ref | req | public_ref | propriétaire courant ; certificat terminal relu sur octets publics |
| root_authority_ref | req | public_ref | propriétaire courant ; racine D2 authentifiée |
| issuer_generation_ref | req | public_ref | propriétaire courant ; génération intermédiaire émettrice D2 |
| policy_ref | req | public_ref | politique protégée courante, jamais une politique du client |
| policy_version | req | public_ref | version protégée réellement vérifiée |
| plan_ref | req | public_ref | plan autorisé de première installation et d'adoption |
| plan_version | req | public_ref | version protégée réellement vérifiée |
| epoch | req | non_negative_int | propriétaire courant et ancrage ; ancienne époque refusée |
| key_created_at | req | utc_timestamp | propriétaire de la création et source de temps compétente ; âge réel conservé, jamais déduit de l'UUID |
| not_before | req | utc_timestamp | extrait du certificat public, contrôlé contre politique et chaîne |
| not_after | req | utc_timestamp | extrait du certificat public, strictement postérieur à not_before |
| hardware_evidence_ref | req | current_evidence_ref | preuve fournisseur vérifiée de clé matérielle non exportable |
| possession_evidence_ref | req | current_evidence_ref | preuve de possession liée à cette clé, instance et opération |

Le propriétaire vérifie les égalités installation/cible/instance/rôle/usage/clé/génération/certificat/politique/plan/époque, l'origine et la fraîcheur requises des preuves et les octets de certificat et SPKI. Un nom de fournisseur ou deux chaînes key_ref différentes ne prouvent pas deux clés indépendantes. Les usages client et serveur sélectionnés disposent de paires et certificats distincts, vérifiés sur matériau public et fournisseur. Aucune clé CA ou Ed25519 de mandat opérateur n'est réemployée.

Le profil D7 est fermé : X.509 v3 P-256 ; Subject vide ; BasicConstraints critique CA=false sans pathLenConstraint ; KeyUsage critique digitalSignature seul ; ExtendedKeyUsage critique avec exactement clientAuth ou serverAuth ; SAN critique avec exactement urn:uuid:<instance_uuid>, et exactement server_ipv4 pour le seul usage serveur ; SKI/AKI non critiques liés aux clés réelles. Aucune autre extension n'est admise. La chaîne CA D2 conserve seulement BasicConstraints/KeyUsage/SKI/AKI ; NameConstraints et toute extension étrangère y sont refusées. Les contrôles de chaîne, URI, IP et usage sont indépendants. Aucun CN/DNS, IP, port ou autre profil par défaut n'est ajouté. Les durées A10i4, le renouvellement aux deux tiers de la validité effective et le chevauchement maximal A10i3 de cinq minutes restent opposables, sans rajeunissement à l'adoption.

### 13.3 Schéma fermé z12.initial_tls_material/v1

Cet objet décrit un résultat local privé destiné à la composition native, pas un message réseau ou une autorité sérialisable. Les références publiques sont résolues localement auprès de leurs propriétaires authentifiés. Le fournisseur ne restitue jamais les octets privés d'une clé.

| champ | req/opt | type | propriétaire et contrôle |
|---|---|---|---|
| object_type | req | closed_enum[z12.initial_tls_material/v1] | Z12 définit le discriminateur |
| schema_version | req | closed_enum[1.0.0] | Z12 définit la version |
| material_ref | req | public_ref locale | composition native ; résultat lié à sa durée de vie |
| identity_ref | req | public_ref | propriétaire courant ; objet exact du §13.2, recoupé en entier |
| owner_ref | req | public_ref | propriétaire réellement constaté, jamais sélectionné par le client |
| state_ref | req | public_ref | état courant protégé de la cérémonie ou du propriétaire ordinaire |
| policy_ref | req | public_ref | politique protégée courante |
| policy_version | req | public_ref | même version vérifiée que l'identité et l'autorisation |
| plan_ref | req | public_ref | même plan protégé que l'identité et l'opération |
| plan_version | req | public_ref | même version protégée |
| epoch | req | non_negative_int | même époque courante, recoupée avec état et ancrage |
| chain_cert_refs | req | tableau ordonné de exactement deux public_ref distinctes | propriétaire courant ; certificat terminal en premier puis unique intermédiaire D2, ordre et signatures réellement vérifiés |
| anchor_cert_refs | req | public_set non vide | propriétaire courant ; ancres publiques authentifiées, jamais apprises du premier PBO |
| peer_policy_ref | req | public_ref | politique courante de vérification du pair, URI/IP/usage attendus indépendamment de la chaîne |
| key_ref | req | public_ref opaque locale | exactement la clé terminale du §13.2, résolue matériellement dans le même contexte privé |
| libctx_binding_ref | req | référence opaque locale non transférable | composition native ; identifie la liaison au même OSSL_LIB_CTX privé, pas un pointeur public |
| anti_restore_evidence_ref | req | current_evidence_ref | vérification actuelle de l'ancrage lié à installation/cible/étape/époque |
| revocation_evidence_ref | req | current_evidence_ref | propriétaire courant ; état de révocation/retrait effectivement vérifié |
| observed_at | req | utc_timestamp | source de temps compétente et propriétaire courant ; observation réellement effectuée |
| valid_until | req | utc_timestamp | borne effective d'utilisation, postérieure à observed_at et limitée par toutes les dépendances courantes |
| adoption_evidence_ref | opt | evidence_ref | obligatoire après passage D6, adoption publique relue et prouvée |
| initial_retirement_evidence_ref | opt | evidence_ref | obligatoire après passage D6, retrait initial actuel attesté et ancré |

Les deux preuves D6 sont présentes ensemble après le passage et absentes de la branche initiale ; leur présence ne choisit jamais la branche. L'état réel protégé et les propriétaires compétents la déterminent. L'objet ne contient ni certificat brut provenant du réseau, ni configuration libre de fournisseur/TCTI, ni chemin d'ancre ou de clé, ni EVP_PKEY, capsule Python, blob privé ou booléen verified. Les matériaux publics nécessaires sont lus depuis les références authentifiées et contrôlés sur octets avant chargement ; leur taille et leurs bornes viennent de la politique applicable, sans nouvelle valeur d'exploitation inventée.

valid_until ne constitue pas une autorisation valable jusqu'à échéance indépendamment de l'état courant : retrait, révocation, changement de politique/époque, perte d'autorité ou d'ancrage rendent le résultat inutilisable immédiatement selon le contrôle courant. L'identité, la clé, la chaîne, les ancres, le pair attendu et le libctx_binding_ref ne sont pas substituables après résolution. Une réutilisation dans un autre contexte OpenSSL ou une restauration d'un ancien résultat est refusée.

### 13.4 Port local privé C.Z12_TLS_MATERIAL_RESOLVER/v1

Ce nom désigne un contrat documentaire de composition, sans API publique ni implémentation réputée livrée. L'entrée locale fermée contient identity_ref (public_ref sélectionnée au plan), tls_usage (clientAuth ou serverAuth), libctx_binding_ref (référence native locale non transférable) et initial_context_ref (référence vers le contexte initial §12.1, ou son lien adopté relu par le propriétaire ordinaire). Le résultat réussi est le schéma du §13.3 ; aucun champ supplémentaire ou paramètre de propriétaire n'est admis. La composition native de confiance demande cette identité, son usage et son contexte privé ; aucune partie réseau ne fournit directement un propriétaire, une ancre, une référence CA, un chemin, un contexte OpenSSL ou une assertion de validation. Le propriétaire vérifie à nouveau les entrées contre le plan et la politique réels. La signature native concrète et la gestion des ressources sont réalisées et qualifiées dans la composition, sans export public de EVP_PKEY ou de capsule Python.

L'ordre requis est : constater l'étape réelle et le propriétaire compétent ; vérifier provenance native et mandat applicable ; recouper plan/politique/version/cible/identité/usage/époque ; vérifier état, fraîcheur, retrait/révocation et ancrage ; vérifier profil et chaîne sur octets, possession et protection matérielle de la clé ; résoudre cette seule clé terminale dans le même OSSL_LIB_CTX privé ; charger les seuls matériaux publics autorisés ; maintenir les vérifications de pair et de validité courante avant utilisation. Une résolution ou un chargement partiel n'ouvre aucun transport. Un échec libère les objets natifs acquis et ferme l'opération ; aucun repli logiciel, autre profil, autre propriétaire ou ancre non autorisée ne la rétablit.

Le contrat distingue une entrée structurellement invalide, une liaison étrangère, une source absente/invérifiable/périmée, une autorité retirée, une dépendance cryptographique ou matérielle inadmissible et un effet de chargement partiel. Ces refus sont diagnostiqués sans secret ; ils ne prétendent ni engagement A12 ni effet PostgreSQL. Les codes runtime restent à définir avec les contrats de réalisation, sans attribuer un code existant fictif à A07/A12.

Avant PostgreSQL, la cérémonie D4 contrôle positivement origine native, opérateur, mandat lié au plan et politique protégée ; UID 0 seul, C01/R01 ou CommandMetadata forgé ne suffisent pas. INITIAL_TRUST_READY et les étapes d'adoption intermédiaires n'autorisent que les usages initiaux explicitement mandatés et sous fencing ; elles n'ouvrent pas l'admission ordinaire. À tout retrait ou clôture, les capacités initiales et sessions privilégiées correspondantes sont rendues inutilisables. Un état manquant ou une transition partielle ne rouvre pas une branche initiale.

Après adoption et retrait attesté D6, seul le propriétaire ordinaire Django/A07/A12 courant peut fournir le matériel. Références publiques, clés conservées, âges, dates et retraits connus sont adoptés sans recréer la PKI ni réinitialiser les validités. La panne de PostgreSQL ferme l'usage dont l'autorité courante ne peut être vérifiée ; elle ne réactive jamais l'autorité initiale. Le mandat technique PostgreSQL demeure un contrat distinct. L'ancrage NV PKI Z12 ne vaut ni index ni autorisation d'écriture pour le registre technique PA ; leurs plans, politiques et effets restent distincts et coordonnés lorsqu'ils partagent un TPM.

### 13.5 Critères de réalisation et de recette

Réaliser les deux schémas, leurs contrôles de références et le port auprès des vrais propriétaires avant qualification. La recette couvre les deux usages et leurs clés distinctes ; toutes extensions/Subject/SAN/KU/EKU interdits ; URI canonique, IP exacte et absence de repli ; chaîne et durées D2/A10i4 ; références CA ou ancres/chemins étrangers ; substitution de contexte ou de clé ; preuve matérielle/possession absente ; identité native et mandat opérateur invalides ; source/politique/époque/révocation périmées ; ancrage absent, restauré, cloné ou invérifiable ; durée de vie et libération natives ; adoption/retrait partiels, réponse perdue et reprise ; indisponibilité PostgreSQL après D6 et interdiction de réouverture initiale. Ces contrôles exigent leurs effets réels et environnements autorisés. Aucun test unitaire, mock, nom de port ou profil conforme ne prouve seul la qualification intégrée. Aucun effet TPM/NV, installation ou clé ne résulte de ce lot documentaire.

## 14. Propriétaire natif et ancrage PKI — D9/D10 adoptés le 23 octobre 2026

### 14.1 Statut, types et propriétaires

Ces contrats de réalisation privés, fermés et versionnés précisent les §§12–13 ; ils ne rendent aucune API disponible ou qualifiée. Les primitives du §1 restent applicables. Les objets publics de liaison sont distincts des capacités natives effectivement vérifiées. Une référence, une signature ou un descripteur de build ne prouve pas sa propre autorité. Les champs inconnus, doublons, versions inconnues, types ambigus et valeurs nulles hors variante explicite sont refusés ; aucun booléen verified, hardware, fd_protected ou genesis_written fourni par un appelant n’est accepté. PLATFORM sans tenant_id ni scope_id reste la seule branche initiale D4.

| Contrat / propriétaire compétent | Entrée publique fermée | Résultat privé et contrôle réel |
|---|---|---|
| C.Z12_NV_PROVISION_BINDING/v1 — provisionneur extérieur au runtime Z12 | z12.nv_binding/v1 ci-dessous, issu du plan exact humainement autorisé | Constat authentifié des attributs, politique, Name après écriture et genesis réellement écrite ; aucune autorisation de provisionnement portée par le DTO |
| C.Z12_NV_GUARD/v1 — gardien PKI natif de la composition de confiance | Références du contexte initial courant, du binding admis et de l’intention exacte | Capacité native non sérialisable ; lecture/vérification courante et extension seulement sous fencing, jamais suppression/redéfinition |
| C.Z12_INITIAL_OPERATOR/v1 — propriétaire initial Z12 natif | Payload signé et signature du §14.3 | Admission native de l’opérateur préautorisé et consommation du challenge courant ; une signature valide isolée ne produit aucun droit |
| C.Z12_CA_NATIVE/v1 — fournisseur CA privé Z12 | Références publiques de l’opération, du plan admis, du rôle CA et du matériau attendu | Création/usage des seules clés matérielles admises dans le contexte CA privé ; résultats publics et faits matériels réels, jamais clé privée ou pointeur public |

Le provisionneur conserve les capacités de plateforme et de suppression hors runtime. L’autorité de suppression P-256 matérielle non exportable est indépendante des CA, terminaux, opérateur et PA01. Le gardien PKI est distinct du signataire CA et ne remet pas son secret NV au fournisseur de signature. Le propriétaire initial authentifie les sources natives et la politique ; le consommateur TLS du §13 reste propriétaire de son propre OSSL_LIB_CTX. Aucun contrat ne choisit le propriétaire courant par un champ client.

### 14.2 Binding NV fermé et capacités privées

Le schéma public z12.nv_binding/v1 contient exclusivement les champs requis suivants, sans champ facultatif :

| Champ | Type | Source et vérification |
|---|---|---|
| object_type | closed_enum[z12.nv_binding/v1] | discriminateur Z12 |
| schema_version | closed_enum[1.0.0] | version Z12 |
| binding_ref | public_ref | provisionneur extérieur authentifié |
| installation_ref | public_ref | installation du plan protégé |
| target_ref | public_ref | cible matérielle réelle recoupée nativement |
| plan_ref | public_ref | même plan exact autorisé |
| plan_version | public_ref | version du même plan exact autorisé |
| plan_sha256 | ContentSHA256 | octets du plan versionné réellement admis |
| policy_ref | public_ref | politique protégée courante |
| policy_version | public_ref | version de cette politique protégée courante |
| policy_sha256 | ContentSHA256 | politique réellement vérifiée |
| nv_index | entier non signé 32 bits | index NV exact explicitement prévu ; aucune allocation automatique |
| nv_name_sha256 | ContentSHA256 | digest des octets du Name courant après WRITTEN, recoupé avec l’aire publique réelle |
| nv_public_sha256 | ContentSHA256 | aire publique exacte, type extend et nameAlg SHA-256, attributs et authPolicy réellement vérifiés |
| deletion_authority_ref | public_ref | autorité matérielle indépendante admise par le plan extérieur |
| genesis_event_sha256 | ContentSHA256 | événement initial public lié à installation/cible/politique/plan, effectivement étendu |
| genesis_value_sha256 | ContentSHA256 | valeur SHA-256 de l’index après cette extension initiale, réellement relue |
| provision_evidence_ref | initial_evidence_ref | preuves du provisionneur extérieur, relues indépendamment |

Les noms contenant sha256 indiquent exactement les octets dont le digest est calculé ; genesis_value_sha256 désigne la valeur SHA-256 stockée par l’index, sans lui appliquer implicitement un second hachage. Aucun digest ou evidence_ref ne dispense de relire les faits matériels. Le plan exact fixe les octets d’événement, aire publique et politiques, les paramètres, la cible et les commandes ; il vérifie les Names avant/après WRITTEN sans liaison circulaire. Un index non écrit, absent, étranger ou zéro arbitraire n’est pas une genesis. La lecture des attributs publics seuls ne prouve ni la valeur ni sa fraîcheur.

PLATFORMCREATE/POLICY_DELETE sont obligatoires au profil admis ; ORDERLY et les attributs STCLEAR incompatibles avec la persistance sont refusés. L’authPolicy réelle réserve la suppression à l’autorité matérielle indépendante, sans branche équivalente accessible aux signataires. Les droits de plateforme, de suppression et de redéfinition ne sont pas remis au runtime. Leur maintien et la récupération après événement de plateforme sont des critères de recette, sans garantie déduite du seul document ou d’un test simulé.

Le canal du secret NV n’est pas un objet JSON ni un paramètre Python. La composition native remet un FD protégé au gardien compétent, avec provenance, propriétaire, installation, cible et génération de contexte vérifiés. Le gardien lit exactement le secret de 256 bits selon le canal borné, refuse une taille/provenance divergente et le conserve uniquement dans son état natif privé. Un entier de FD, UID 0, mode de fichier ou chaîne de configuration ne suffit pas à l’authentification du canal. Le secret, les calculs HMAC et les états de session restent hors Python, argv, environnement, journaux et fichiers temporaires.

Les commandes nécessitant l’autorisation de l’index utilisent exclusivement des sessions HMAC SHA-256 liées à cet index et à son Name courant ; pas de session mot de passe, de secret vide ou de repli. La vérification de la cible, de l’aire publique et de la valeur, ainsi que le rapprochement avec le journal courant protégé, précèdent chaque effet. Les métadonnées publiques peuvent être inspectées sans révéler un secret, mais cette inspection ne remplace jamais la vérification authentifiée de la valeur. Les sessions, FD et secrets sont fermés/effacés après usage ou erreur et à la clôture de la capacité initiale ; aucune référence publique ne permet leur reconstruction.

L’entrée de C.Z12_NV_GUARD/v1 possède exclusivement object_type=z12.nv_intent/v1, schema_version=1.0.0, initial_context_ref, binding_ref, operation_id, operation_version, intention_sha256, journal_head_sha256 et expected_epoch. Les références sont publiques typées, les digests ContentSHA256 et expected_epoch non_negative_int. La capacité native obtenue d’une composition authentifiée reste implicite au port privé ; elle ne peut pas être jointe comme objet Python ou booléen d’admission. Le gardien résout lui-même intention, binding, époque et tête de journal depuis leurs sources protégées, puis les compare aux faits matériels. Une entrée admissible structurellement n’accorde pas l’extension.

### 14.3 Mandat personnel PKI fermé, challenge et signature

Le payload public signé z12.initial_operator_payload/v1 contient exclusivement les champs requis suivants, dans cet ordre de sérialisation : object_type, schema_version, domain, operator_key_ref, challenge_ref, challenge_nonce, installation_ref, target_ref, executor_set_ref, executor_set_sha256, operation_id, operation_type, operation_version, operation_sha256, idempotency_ref, plan_ref, plan_version, plan_sha256, policy_ref, policy_version, policy_sha256, epoch, issued_at, not_before, expires_at. object_type vaut z12.initial_operator_payload/v1, schema_version 1.0.0 et domain la constante ASCII pixs.z12.initial.operator/v1. operation_type est fermé aux cinq noms exacts du §12.2 et à C.Z12_TLS_MATERIAL_RESOLVER/v1 pour le seul usage initial du §13.4. operation_version est la version sémantique du contrat d’opération. operation_id et les autres références sont des références publiques typées, executor_set_sha256, operation_sha256, plan_sha256 et policy_sha256 sont ContentSHA256, epoch non_negative_int et les trois dates utc_timestamp. challenge_nonce contient exactement 32 octets issus de l’aléa cryptographique natif du propriétaire courant ; il n’est ni un compteur client ni un substitut au temps.

Pour éviter les encodages ambigus, la représentation binaire signée commence par les octets ASCII pixs.z12.initial.operator.payload/v1 suivis d’un octet nul. Chacun des 25 champs, dans l’ordre précédent, est ensuite encodé par une longueur non signée 32 bits big-endian puis ses octets. Les textes utilisent UTF-8 strict sans normalisation implicite ; les références conservent exactement les octets admis par leur propriétaire, les ContentSHA256 leur texte canonique minuscule et epoch son texte décimal canonique sans signe ni zéro initial sauf zéro seul. Les dates utilisent leur forme UTC canonique du §1. Seul challenge_nonce est un champ binaire brut. Les longueurs, tailles et valeurs doivent satisfaire la politique protégée et la représentation ; aucun troncage, dépassement, champ additionnel ou octet final n’est accepté. Il n’existe aucune seconde représentation JSON équivalente que le vérificateur pourrait substituer aux octets signés.

Le port C.Z12_INITIAL_OPERATOR/v1 reçoit un objet fermé contenant exclusivement object_type=z12.initial_operator_proof/v1, schema_version=1.0.0, payload_bytes et signature_bytes ; ces deux derniers champs sont des octets publics bornés, signature_bytes contenant exactement la signature Ed25519 de 64 octets. La signature Ed25519 pure porte sur les octets complets ci-dessus, sans préhachage ou réemploi de domaine PG/R01/C01. Le vérificateur natif résout operator_key_ref uniquement depuis la politique PKI protégée/versionnée déjà admise ; aucune clé publique proposée avec la preuve n’est acceptée. La clé privée personnelle reste sous contrôle de l’opérateur, hors runtime, agents et dépôt.

Le challenge est produit et conservé par le propriétaire natif dans l’état protégé courant, avec installation/cible/exécutants/opération/version/digest/idempotence/plan/politique/époque et bornes temporelles. executor_set_ref et son digest désignent l’ensemble exact de rôles et d’identités natives réellement vérifiés au plan, pas une liste fournie par le client. Toutes les liaisons du payload sont recoupées avec ces sources. Les dates satisfont issued_at <= not_before < expires_at, les bornes de la politique réellement admise et la source de temps compétente actuelle ; temps invérifiable ou retour en arrière non réconcilié ferme l’admission. Aucun TTL ou délai de grâce d’exploitation n’est fixé ici.

Une signature correcte ne suffit pas : identité/provenance native, admission et révocation actuelles de l’opérateur, politique, challenge non consommé, état, époque, ancrage, opération et fencing doivent être réellement vérifiés. Le challenge est consommé durablement avant l’effet qu’il autorise, avec rapprochement journal/ancrage. Le constat protégé de consommation relie le payload signé, l’époque antérieure et l’époque résultante de cette seule opération ; cette transition attendue ne permet pas de substituer un autre mandat ou contexte. En cas de résultat perdu, la même opération se réconcilie ; elle ne reçoit pas une nouvelle capacité par rejeu du payload signé. Un idempotency_ref divergent, une cible/exécutant étrangers, un ancien plan/époque, une preuve PG/R01/C01, UID 0 ou un DTO seuls ferment l’opération. L’inspection et la résolution restent soumises à leurs préconditions et ne confèrent pas un droit de mutation supplémentaire.

### 14.4 Fournisseur CA, build et durée de vie privés

Le composant de réalisation Cython/OpenSSL 3/TSS2 possède une construction indépendante des trois PA, une ABI privée versionnée et son propre contexte CA. Le fournisseur TPM2 retenu est tpm2-openssl 1.3.0 dans le profil Debian 13 à qualifier. Le manifeste de construction relie chemins sources, versions, dépendances et artefacts réels ; ses valeurs ne sont pas une attestation de build ou de qualification. Le plan de build/tests borne les dépendances et l’environnement avant exécution. Le présent lot ne les installe pas, ne compile pas de source et n’utilise aucune clé actuelle.

L’entrée fermée de C.Z12_CA_NATIVE/v1 contient object_type=z12.ca_native_intent/v1, schema_version=1.0.0, initial_context_ref, operation_id, operation_version, operation_sha256, plan_ref, plan_version, policy_ref, policy_version, epoch, ca_role, authority_ref, key_material_ref et public_input_ref. Les références sont public_ref typées, operation_sha256 ContentSHA256, epoch non_negative_int et ca_role fermé à ROOT_OFFLINE ou INTERMEDIATE. Le port est privé à la composition propriétaire initiale ; il ne remplace pas les décisions/engagements ordinaires du §8. La nature et les octets de l’effet permis sont ceux de l’opération admise, relus depuis le plan et public_input_ref ; une référence de clé ne donne aucun droit de signer. ROOT_OFFLINE exige la cérémonie et le mandat hors des processus courants ; elle ne devient pas une capacité de service permanent.

Le propriétaire contrôle lui-même l’étape réelle, la provenance native, le mandat, le plan/politique courants, l’ancrage, la révocation, les limites temporelles et les faits matériels avant d’appeler le fournisseur. Le fournisseur recoupe rôle, clé, matériau public, protection non exportable et possession réellement vérifiés ; aucune assertion client ne les fournit. Le contexte CA, les références natives, sessions, handles et objets EVP restent privés et non transférables. Les secrets d’autorisation CA/parent ne passent pas par Python ni argv ; leur canal exact et leur protection sont arrêtés et qualifiés avant utilisation, sans format ou valeur implicite. Aucun EVP_PKEY, capsule Python ou pointeur public ne constitue une API de transport.

La libération après succès, refus, échec partiel, retrait D6 ou arrêt de contexte ferme toutes les ressources natives acquises et rend les capacités anciennes inutilisables. Les ressources CA ne sont jamais transférées à C.Z12_TLS_MATERIAL_RESOLVER/v1. Le résolveur charge uniquement une clé terminale matériellement admise et les matériaux publics vérifiés dans le même OSSL_LIB_CTX privé du consommateur TLS, selon §13. Après D6, seul le propriétaire ordinaire courant peut fournir ce matériel ; l’ancien propriétaire, FD, challenge ou contexte natif ne le réactive pas.

### 14.5 Séquences, résultats et refus fermés

L’ordre est : constater propriétaire/étape et provenance native ; vérifier plan/politique/temps/état/ancrage courants ; authentifier l’opérateur et toutes les liaisons ; acquérir le fencing et consommer le challenge durablement ; relever l’intention et l’état attendu ; recontrôler avant effet ; effectuer la seule opération autorisée ; constater et rapprocher effet, journal et extension NV ; produire les seules références publiques prouvées. Les frontières TPM/journal/système/PG ne sont pas présentées comme une transaction atomique. Adoption publique et retrait initial D6 conservent les étapes et propriétaires du §12.3, sans seconde PKI ni remise à zéro d’âge.

Le résultat public fermé z12.native_outcome/v1 contient object_type=z12.native_outcome/v1, schema_version=1.0.0, operation_id, operation_version, outcome, state_ref, audit_ref et, selon la seule variante, effect_evidence_ref ou refusal_reason. outcome est fermé à OBSERVED, IN_DOUBT, REFUSED. OBSERVED exige effect_evidence_ref réellement vérifiée et interdit refusal_reason ; il ne confirme que l’effet exact, jamais l’admission ordinaire ou un commit PG non prouvé. IN_DOUBT interdit les deux champs et exige réconciliation actuelle avant nouvel effet. REFUSED exige refusal_reason et interdit effect_evidence_ref ; un effet partiel non résolu utilise IN_DOUBT. Les références sont public_ref typées ou initial_evidence_ref pour les preuves initiales, et l’audit désigne une trace réellement produite sans secret. state_ref et audit_ref permettent au propriétaire compétent de retrouver et vérifier, pour cette seule opération, le lien au payload signé, l’époque antérieure et l’époque résultante de sa consommation ; une copie publique ne remplace pas cette relecture actuelle.

Le vocabulaire fermé de refusal_reason est INVALID_INPUT, FOREIGN_BINDING, NATIVE_PROVENANCE_UNVERIFIED, POLICY_NOT_CURRENT, OPERATOR_NOT_AUTHORIZED, CHALLENGE_NOT_CURRENT, TIME_UNVERIFIABLE, STATE_NOT_CURRENT, ANCHOR_UNVERIFIABLE, MATERIAL_NOT_ADMISSIBLE, CAPABILITY_RETIRED, DEPENDENCY_UNAVAILABLE. Les diagnostics ne révèlent ni secret ni matériau privé. Les refus sont distingués des effets incertains ; ils ne prétendent aucune validation A12. L’absence d’état, de source compétente ou de preuve matérielle ferme l’admission, sans repli logiciel, mot de passe, ancien contexte ou snapshot. Les attributs NV, authentifications, effacements, coupures, reprises et retrait des ressources ouvertes doivent être prouvés sur l’environnement autorisé en seconde phase. Aucun mock, DTO, profil X.509 ou contrôle strict documentaire ne qualifie ces propriétés.

## 15. Observations natives et remise du secret NV — D14/D15, 24 octobre 2026

Ce complément concrétise les profils adoptés, sans remplacer les §12–14. Les ports ci-dessous sont privés à la composition native Z12 Cython/C ; leurs contextes, ressources et résultats internes ne sont ni des objets Python, ni une API publique de pointeurs ou capsules. Les noms versionnés décrivent des contrats à réaliser et qualifier. Une copie publique pour audit n’est jamais une capacité d’admission. PA01 réalise son propre profil D14 avec ses politiques, mandats, sources et construction ; aucune ABI ou inclusion partagée n’est présumée.

### 15.1 Règles communes et demandes fermées

Les champs des demandes sont exhaustifs et obligatoires ; champs inconnus, doublons, null, mauvais types ou versions étrangères sont refusés. Les types public_ref, ContentSHA256, utc_timestamp et non_negative_int conservent leurs définitions du §1. Les quantités natives uint64_ns sont des entiers non signés sur 64 bits en nanosecondes ; booléen, flottant, chaîne, dépassement et troncature favorable sont refusés. Une conversion de mesure incertaine arrondit la borne dans le sens conservateur ou refuse. Aucun booléen client verified, hardware ou fd_protected n’est accepté.

| Champ de demande | Type et valeur | Source et contrôle réel |
| --- | --- | --- |
| object_type | valeur exacte propre au port ci-dessous | composition native, pas sélection d’un propriétaire par le client |
| schema_version | texte exact 1.0.0 | version du présent contrat privé |
| installation_ref | public_ref | installation protégée réelle |
| target_ref | public_ref | cible réelle, recoupée nativement |
| plan_ref | public_ref | plan protégé et autorisé résolu par le propriétaire |
| plan_version | public_ref | version du même plan résolue et recoupée |
| policy_ref | public_ref | politique protégée du propriétaire compétent |
| policy_version | public_ref | version de cette politique, contrôlée contre l’état courant |
| operation_id | public_ref | intention exacte résolue dans l’état protégé |
| operation_version | texte de version sémantique du contrat visé | égalité avec le contrat résolu, jamais référence de clé ou droit client |
| expected_epoch | non_negative_int borné par la représentation native | époque attendue recoupée avec l’état et l’ancrage compétents |

Avant PostgreSQL, ces références sont résolues auprès du propriétaire local initial D4/D10 et de ses sources protégées ; aucun accès à Django/PostgreSQL n’est rendu nécessaire à l’observation initiale. Après D6, seul le propriétaire ordinaire courant peut les résoudre pour l’usage ordinaire. Les sélecteurs de demande ne prouvent aucun fait : contexte et ressources natifs implicites proviennent de la composition authentifiée. Les observations préliminaires peuvent servir à assembler le contexte, mais aucune admission n’est produite avant toutes les vérifications de politique/état/ancrage/opérateur/mandat requises. Une dépendance circulaire ou absente entraîne un refus. Un client ne choisit jamais UID, unité, manager, socket, chemin, fournisseur, ancre, facteur ou budget.

Chaque résultat interne est une variante fermée : OBSERVED contient exclusivement son observation ou sa capacité native ; REFUSED contient exclusivement refusal_reason du vocabulaire fermé §14.5 ; IN_DOUBT ne fournit ni observation utilisable ni capacité et impose une réconciliation. Le contexte de résultat reste lié à l’opération et au propriétaire natifs. Ces variantes ne modifient pas l’état PKI par leur seule production. Le propriétaire produit, lorsqu’applicable, le résultat public z12.native_outcome/v1 du §14.5 et ses traces réellement observées ; aucune copie ne remplace une relecture actuelle.

### 15.2 C.Z12_LAUNCH_OBS/v1 — observation du lanceur

La demande contient exactement les onze champs du §15.1 ; object_type vaut z12.launch_intent/v1. Le port observe directement les faits noyau/libsystemd, puis les recoupe avec les attentes protégées. Son observation native interne exhaustive contient les liaisons de la demande relues, puis les champs suivants :

| Champ natif observé | Type | Contrôle |
| --- | --- | --- |
| uid, euid | entiers natifs non négatifs | identités réelles, égalités exigées par la politique ; UID 0 seul insuffisant |
| pid, main_pid | entiers natifs strictement positifs | processus réel et MainPID du service, relation explicitement admise et vérifiée |
| manager_ref, unit_ref | références privées résolues | manager et unité réellement observés, même périmètre que la politique |
| invocation_id | exactement 16 octets natifs observés | InvocationID actuel, recoupé avec service et processus |
| artifact_observations | ensemble natif borné par la politique | chaque entrée contient seulement artifact_ref, loaded_identity_ref et sha256 ; artefact réellement chargé, identité native et ContentSHA256 vérifiés |
| observed_monotonic_ns | uint64_ns | instant réel d’observation dans le domaine d’horloge natif compétent |
| clock_domain_ref | référence privée résolue | domaine d’horloge réellement lié à l’observation et à son consommateur |

Les capacités et ressources ne sortent pas de la composition. Un nom d’unité ou rapport public ne remplace pas les appels natifs. Changement de PID/MainPID/InvocationID/manager, d’artefact chargé ou de politique invalide l’observation ; le propriétaire reprend les faits nécessaires avant utilisation. L’observateur seul ne prouve ni mandat, ni opérateur, ni état anti-restauration ; D4/D9/D10 et le contrôle ordinaire après D6 restent opposables.

### 15.3 C.Z12_CHRONY_OBS/v1 — temps utilisable par mandat et TLS

La demande contient exactement les onze champs du §15.1 ; object_type vaut z12.chrony_intent/v1. Elle n’accepte ni timestamp, mesure, socket ou preuve client supplémentaires. Le port vérifie provenance et politique du service chrony, source effectivement sélectionnée, authentification NTS et rapports natifs actuels. L’observation privée contient les liaisons relues de la demande et exactement :

| Champ natif | Type | Contrôle et unité |
| --- | --- | --- |
| service_binding | observation native du lanceur §15.2 | service chrony réellement compétent, pas seul nom de processus |
| source_name | texte source réellement vérifié | source NTS autorisée time.cloudflare.com recoupée avec service/politique et source sélectionnée |
| authentication_mode | valeur native exacte NTS | authentification réellement observée, pas déclaration de configuration seule |
| utc_epoch_ns | uint64_ns | temps UTC vérifié, instant de référence correspondant à observed_monotonic_ns |
| observed_monotonic_ns | uint64_ns | instant monotone réel de l’observation |
| clock_domain_ref | référence privée résolue | domaine réellement observé, cohérent avec le consommateur |
| total_uncertainty_ns | uint64_ns | borne totale démontrée, au plus 1000000000 ns |
| sync_evidence_age_ns | uint64_ns | âge réel de la preuve admissible de synchronisation, au plus 600000000000 ns |

Les composantes de l’incertitude, conversions, évolution jusqu’à l’utilisation et âge de synchronisation sont réellement vérifiés selon les sources et politiques compétentes. Absence d’une borne démontrable, mesure incohérente, débordement, source non sélectionnée/autorisée, authentification perdue ou délai excessif entraîne TIME_UNVERIFIABLE. Une durée entière en secondes obtenue par troncature ne peut satisfaire artificiellement une borne. Le temps et son intervalle d’incertitude sont utilisés au contrôle courant des mandats et de TLS/X509, sans repousser échéance, NotBefore ou NotAfter et sans grâce inventée. Le simple CLOCK_REALTIME partagé, un état synchronized, un booléen de client ou une ancienne observation ne suffit pas.

Le profil LXC chronyd -x observe sans modifier l’horloge partagée de hvp1. Les vérifications TLS, y compris celles du premier échange NTS, restent actives ; sans temps ou chaîne de confiance admissibles le chemin se ferme. Les échéances monotones d’opération restent distinctes, bornées explicitement et jamais réinitialisées par une nouvelle observation. Les garanties du service, de ses rapports et des vérifications TLS réelles sont à qualifier avant usage.

### 15.3.1 C.Z12_TIME_OBS/v2 — observation privée du temps à réaliser et qualifier

C.Z12_TIME_OBS/v2 est un contrat privé documentaire à réaliser puis à qualifier ; ce lot ne réalise ni ne livre de port, d’API ou d’ABI v2 et la réalisation comme la qualification restent requises. Ce numéro décrit la conception privée et ne prouve aucune réalisation. C.Z12_CHRONY_OBS/v1 reste intégralement inchangé au §15.3 et le §18.2 reste strictement inchangé. La demande contient exactement les onze champs de liaison du §15.1, sans champ supplémentaire ; object_type vaut z12.time_intent/v2 avec sélection explicite et versionnée du contrat, sans renommage de v1 ni repli implicite. Pour cette demande privée, schema_version vaut exactement "2.0.0", comme exception locale au littéral 1.0.0 du §15.1 ; toutes les autres liaisons et tous les autres contrôles hérités du §15.1 restent inchangés. Les onze champs sont object_type, schema_version, installation_ref, target_ref, plan_ref, plan_version, policy_ref, policy_version, operation_id, operation_version et expected_epoch, avec types, sources et contrôles réels du §15.1 ; les références sont des références privées opaques résolues et protégées par la composition native, jamais des valeurs d’appelant, et aucun nouvel objet public n’est créé. En SYNCHRONISE, l’âge amont est inférieur ou égal à 600 secondes. En HORS_LIGNE, un âge supérieur à 600 secondes n’est admissible qu’avec modèle qualifié, provenance qualifiée et continuité qualifiée, profil valide, acquisition actuelle et U(t) inférieure ou égale à 1 s au point d’usage ; l’âge amont réel n’est jamais rajeuni par lecture et une nouvelle acquisition ne remet à zéro ni droit, ni budget, ni échéance. Les budgets 250 ms par acquisition, 2 acquisitions au maximum et 1 s au global sont conservés et les autres validités de mandat, de politique, d’état et de révocation restent opposables. L’observation privée contient les liaisons relues de la demande et exactement les champs fermés du tableau exhaustif suivant, sans champ inconnu, nul ou dupliqué et sans type divergent. Les trois champs temporels sont exactement utc_estimate, lower_utc et upper_utc, chacun comme paire native (seconds int64, nanoseconds uint32 dans [0..999999999]), sans nom suffixé supplémentaire, sans chaîne et sans époque uint64. La comparaison des paires est lexicographique sur les secondes puis les nanosecondes normalisées, avec lower_utc inférieur ou égal à utc_estimate inférieur ou égal à upper_utc, et la distance conservative des bornes à l’estimation reste couverte par total_uncertainty_ns inférieur ou égal à 1000000000 ns au point d’usage ; toute valeur non représentable, tout débordement et toute troncature favorable sont refusés. La seule dispersion racine ne vaut pas preuve de borne.

| Champ natif | Type exact | Contrôle |
| --- | --- | --- |
| mode | énumération exacte SYNCHRONISE, HORS_LIGNE ou INVERIFIABLE | mode contractuel explicite |
| utc_estimate | paire native (seconds int64 UTC, nanoseconds uint32 dans [0..999999999]) | estimation interne normalisée |
| lower_utc | paire native (seconds int64 UTC, nanoseconds uint32 dans [0..999999999]) | borne basse normalisée |
| upper_utc | paire native (seconds int64 UTC, nanoseconds uint32 dans [0..999999999]) | borne haute normalisée |
| total_uncertainty_ns | uint64 nanosecondes, borne inférieure ou égale à 1000000000 | borne totale démontrée au point d’usage, couvrant l’intervalle entier |
| sync_evidence_age_ns | uint64 nanosecondes réelles | âge réel de la dernière preuve amont authentifiée, jamais rajeuni ; âge admissible selon le mode, sans obligation de rafraîchir l’amont en HORS_LIGNE |
| observed_monotonic_ns | uint64 nanosecondes | instant monotone réel de l’observation |
| clock_domain_ref | référence privée native résolue | domaine réellement observé, cohérent avec le consommateur |
| service_binding | observation native du lanceur du §15.2 | service réellement compétent, pas seul nom de processus |
| source_ref | référence privée native résolue | source réelle, recoupée avec service et politique |
| source_evidence | preuve privée native de la dernière preuve amont authentifiée | authenticité et fraîcheur réellement vérifiées ; concerne la dernière preuve amont authentifiée dont l’âge réel est admissible selon le mode |
| profile_ref | référence privée native résolue | profil déclaré |
| profile_version | version privée native du profil | version contrôlée contre l’état courant |
| model_ref | référence privée native résolue | modèle qualifié selon le mode |
| model_version | version privée native du modèle | version qualifiée selon le mode |
| continuity_evidence | preuve privée native de continuité | continuité qualifiée selon le mode |

En HORS_LIGNE, model_ref, model_version et continuity_evidence sont tous obligatoires. En SYNCHRONISE, ces trois éléments sont soit tous absents sans valeur nulle, soit tous présents et qualifiés, sans groupe partiel, sans valeur nulle et sans champ inconnu. INVERIFIABLE est un état interne non admissible qui produit REFUSED avec TIME_UNVERIFIABLE ou IN_DOUBT selon le §15.1, sans variante OBSERVED contenant un UTC ou une incertitude nulle et sans nouveau champ public de résultat. L’observation est cohérente et actuelle, propagée conservativement jusqu’à l’usage, invalidée sur perte d’origine, rupture de continuité, suspension, reprise, restauration ou retour Internet incohérent, sans renouveler budget, échéance ou droits.

### 15.4 C.Z12_CUSTODY_HANDOFF/v1 — remise privée du secret PKI

La demande utilise object_type=z12.custody_intent/v1 et tous les champs du §15.1, augmentés exclusivement de :

| Champ | Type | Source et contrôle |
| --- | --- | --- |
| binding_ref | public_ref | binding NV PKI §14.2 résolu et admis pour cette installation/cible |
| recipient_ref | public_ref | garde NV destinataire sélectionnée par la politique, identité réelle vérifiée nativement |
| deadline_ref | référence privée résolue | échéance absolue monotone déjà commencée pour l’opération, budget explicite de politique, sans remise à zéro |

Les facteurs host+tpm2, credential, chemins et unités sont résolus par la politique et la composition natives, jamais fournis comme preuve par la demande. Le gardien dans une unité distincte du signataire CA vérifie les deux facteurs effectifs du credential systemd dédié, le canal de lecture natif et les faits courants du destinataire, y compris UID/PID/unité/manager/InvocationID/artefacts applicables, installation/cible, politique/version, état et époque. La vérification anti-restauration D9 nécessaire a lieu dans la frontière native compétente avant toute remise favorable ; une lecture interne de vérification n’autorise pas un effet NV. L’état absent, restauré ou invérifiable ferme la remise. La genesis et le provisionnement extérieurs de D9 ne sont pas recréés implicitement.

OBSERVED ne fournit que la capacité privée de remise au destinataire vérifié : FD natif contenant exactement 32 octets, en lecture seule et scellé contre écriture, croissance, réduction et retrait des sceaux, lié au contexte/opération/époque/échéance courants. Le propriétaire de chaque descripteur et son transfert sont explicites ; aucun entier de FD ou bit de permission ne vaut authentification. Le récepteur vérifie à nouveau canal, taille, sceaux et liaisons avant de charger son état natif. Le secret n’est jamais restitué dans le résultat public, Python, argv, environnement, journaux ou fichiers temporaires. Le fournisseur CA n’en reçoit aucune copie.

Le gardien ne possède aucun droit de plateforme, suppression ou redéfinition NV et ne devient pas un second port d’extension. C.Z12_NV_GUARD/v1 (§14.2) conserve les effets NV et toutes leurs préconditions. Secret, credential, unité, mandat et journal PKI restent distincts de PA/PG et des autorisations CA. Tout facteur manquant ou non démontré entraîne un refus sans repli logiciel, génération automatique de host key, configuration TPM ou nouvelle clé. Le plan exact D5 et son autorisation distincte couvrent les effets de provisionnement ou TPM/NV ; ce contrat n’en autorise aucun.

Succès, refus, échec partiel, interruption, redémarrage ou retrait D6 ferment les descripteurs, sessions et ressources acquis et effacent les copies secrètes natives selon leur durée de vie. Une remise partielle ou incertaine n’émet pas de nouvelle capacité favorable : le propriétaire réconcilie effet, destinataire et état courants. Les anciens FD, contextes, credentials déchiffrés ou capacités ne rouvrent pas l’autorité initiale après D6 ; récupération et redémarrage ne rajeunissent ni PKI, ni politique, ni mandat. Leur fermeture effective et les limites face à l’administrateur hôte font partie de la recette.

### 15.5 Refus, séquences et qualification

L’ordre est : résoudre dans la composition les attentes protégées ; observer provenance et temps réels ; vérifier toutes les liaisons et les préconditions D4/D9/D10 ; rapprocher état et ancrage ; vérifier destinataire et échéance ; effectuer la seule remise admise ; recontrôler au composant consommateur avant effet ; constater résultat et libérer les ressources. Les observations préliminaires n’accordent aucune admission pendant cet assemblage. Les frontières système/TPM/journal/PG ne sont jamais annoncées atomiques. Adoption/retrait D6 et contrôle ordinaire demeurent ceux des §12–14, sans nouvelle PKI ni réouverture initiale en panne PG.

Les refus utilisent exclusivement le vocabulaire §14.5 : INVALID_INPUT, FOREIGN_BINDING, NATIVE_PROVENANCE_UNVERIFIED, POLICY_NOT_CURRENT, OPERATOR_NOT_AUTHORIZED, CHALLENGE_NOT_CURRENT, TIME_UNVERIFIABLE, STATE_NOT_CURRENT, ANCHOR_UNVERIFIABLE, MATERIAL_NOT_ADMISSIBLE, CAPABILITY_RETIRED, DEPENDENCY_UNAVAILABLE. Un effet partiel non résolu reste IN_DOUBT ; aucune absence de preuve n’est convertie en OBSERVED.

La recette de seconde phase couvre nominal avant PG et après D6 ; changement PID/MainPID/InvocationID/manager ou artefact ; ancienne politique et substitution de cible ; source NTS étrangère/non sélectionnée/désactivée ; validation TLS NTS ou TLS terminale défaillante ; incertitude ou âge juste sous/à/au-delà de la borne, fractions et débordements ; passage du temps entre observation et utilisation ; facteur host ou tpm2 absent, restauration/snapshot, mauvais destinataire ; FD mutable, mauvais mode, sceaux/taille/provenance invalides ; secret remis au CA ; échec partiel, concurrence, redémarrage, récupération, retrait D6 et impossibilité de réouverture. Les essais à effets TPM/NV restent soumis au plan exact D5. Compilation, tests de structure, mock, manifeste ou contrôle OpenSpec ne qualifient pas seuls ces garanties réelles.


## 16. Autorisations des clés matérielles — D16, adopté le 24 octobre 2026

### 16.1 Propriétaire et demande privée C.Z12_KEY_AUTH/v1

Ce port privé de composition concrétise le canal d’autorisation CA/parent du §14.4 et le chargement terminal D8. Il ne désigne pas une réalisation réputée disponible. Ses contextes, secrets, FD et buffers natifs ne sont ni une API publique de pointeurs, ni des objets ou capsules Python.

La demande fermée contient exactement les onze champs du §15.1, avec object_type=z12.key_auth_intent/v1 et schema_version=1.0.0, augmentés exclusivement de :

| Champ | Type | Contrôle |
| --- | --- | --- |
| key_material_ref | public_ref typée | clé réellement sélectionnée par la politique ; pour PARENT, résolution du parent de cette seule clé dans le périmètre admis |
| auth_purpose | CA_KEY, PARENT ou TERMINAL_KEY | finalité recoupée avec le rôle, la clé et l’usage courants ; aucune autorité par ce seul sélecteur |
| recipient_ref | public_ref | destinataire natif effectivement vérifié, admis pour ce matériel et cette opération |
| deadline_ref | référence native privée non transférable | échéance monotone actuelle déjà commencée, sans budget remis à zéro |

Les facteurs, credentials, chemins et formats sont résolus dans les sources protégées, jamais ajoutés comme preuve par la demande. La branche réelle initiale/ordinaire est constatée auprès du propriétaire compétent, pas choisie par le client. Les préconditions D4/D9/D10, le fencing et le contrôle ordinaire après D6 restent opposables.

### 16.2 Sources et séparation

| Matériel visé | Source retenue | Frontière |
| --- | --- | --- |
| CA intermédiaire et parent sélectionné | credentials systemd dédiés, chiffrés avec les deux facteurs effectifs host+tpm2 | lecture et effacement exclusivement natifs dans la composition admise du destinataire CA |
| Clé terminale et parent sélectionné | credentials systemd dédiés, chiffrés avec les deux facteurs effectifs host+tpm2 | composition native du consommateur TLS, seule clé terminale D7 et même OSSL_LIB_CTX D8 |
| Racine hors ligne et contexte de parent | remise de cérémonie mandatée par FD natif privé, scellé et en lecture seule | aucun accès permanent de service, vérification du destinataire et du mandat hors ligne |

Les secrets sont distincts par périmètre et usage. Ils ne réutilisent jamais le secret NV PKI de 256 bits ni un secret/credential/canal PA ou PG. Les ressources CA ne sont pas remises au résolveur TLS. Un parent de clé terminale n’autorise aucun accès à une autorisation CA. Le profil ne confère aucun nouveau droit d’administration de plateforme, d’effacement, de changement de hiérarchie ou d’effet NV.

### 16.3 Séquence et résultat

Le propriétaire relit l’autorité/étape, le matériel et son parent, le plan et la politique/version, le destinataire natif et les artefacts applicables, installation/cible/usage, opération/époque, temps, état, retrait/révocation et ancrage avant la remise. Il vérifie réellement le canal : les deux facteurs effectifs pour les credentials, ou provenance native, mode, taille et sceaux du FD de cérémonie. Un booléen de client, nom de credential, entier de FD, UID 0 ou simple configuration déclarée ne fournit aucune de ces preuves.

Le résultat interne reprend les variantes fermées du §15.1 : OBSERVED ne contient que la capacité privée d’utilisation liée au destinataire et au contexte/opération/époque/échéance actuels ; REFUSED ne contient que refusal_reason du §14.5 ; IN_DOUBT ne fournit aucune capacité utilisable et impose réconciliation. Aucune variante ne contient une valeur secrète sérialisée ou un objet EVP/Python public. OBSERVED ne prouve ni signature CA, ni admission ordinaire, ni commit PostgreSQL ou effet NV.

Taille et encodage sont explicitement déterminés par la politique et le plan ; absence, valeur vide implicite, longueur indéterminée/inadmissible ou interface fournisseur incompatible ferment la remise. Les octets réellement admis doivent parvenir au callback natif sans troncature NUL, arrondi de longueur ou transformation implicite. Les 32 octets du secret NV ne définissent ni le format ni la taille d’une autorisation CA/parent/terminale. Aucun passage secret par Python, argv, environnement, journaux ou fichier temporaire ne remplace le canal.

La propriété de chaque FD, buffer et référence, ses transferts et ses fermetures sont explicites. Les copies sont effacées en natif ; le retrait, l’expiration ou une transition partielle invalident l’usage sans fausse preuve de libération. Les opérations réelles de nettoyage/transfert restent vérifiées avant détachement. Après D6, seul le propriétaire ordinaire courant admet le matériel ; un ancien secret/FD/contexte ne réactive pas l’autorité initiale, et les clés/âges adoptés ne sont pas recréés ou rajeunis implicitement.

### 16.4 Refus, recette et portée

Les refus restent ceux du §14.5, notamment NATIVE_PROVENANCE_UNVERIFIED, POLICY_NOT_CURRENT, TIME_UNVERIFIABLE, STATE_NOT_CURRENT, ANCHOR_UNVERIFIABLE, MATERIAL_NOT_ADMISSIBLE et CAPABILITY_RETIRED ; aucun vocabulaire public supplémentaire n’est déduit. La seconde phase doit vérifier les vrais producteurs/destinataires, facteurs host ou tpm2 absents, credential étranger/ancien, FD mutable ou mauvais mode/sceaux/taille, secret vide implicite, mauvaises clé/parent/finalité/usage et substitutions de contexte, perte/récupération/redémarrage, lecture/callback sur les octets réels avec NUL et limites exactes, absence de fuite, erreurs partielles, transfert/libération et retrait D6. Les tests de structure ou mocks ne qualifient pas ces garanties.

D16 autorise conception/réalisation ; le lot documentaire de cinq fichiers ne génère ni ne lit aucun secret actuel, n’installe rien et n’exécute aucun test produit ou effet de clé/TPM/NV. Les plans et autorisations distincts, dont D5 avant ses effets, restent requis. D1–D15, le secret NV et les mandats techniques PostgreSQL restent inchangés.


## 17. Attente administrative M1 — D17, adopté le 25 octobre 2026

### 17.1 Statut, profil natif privé et copie publique d'audit

Contrats documentaires fermés et versionnés, sans API livrée, sans effet, sans clé, installation, test produit ou opération TPM et NV. Les primitives du §1 de contracts.md s'appliquent. Le pin réel vient EXCLUSIVEMENT de l'attente native de l'artefact authentiquement installé, avec identité, domaine et version constatés nativement et comparés à l'attente. Aucune politique, aucun manifeste, aucun DTO candidat et aucun champ client ne choisissent cette clé. Aucune preuve de provenance par stat, SHA, UID0 ou signature Debian de Pixs. Privée Ed25519 dédiée hors runtime et agents, distincte opérateur, CA, TLS, suppression, PA et PG. CA et terminales restent matériels non exportables. TCB initial explicite ; aucune résistance à OS privilégié compromis. D1 à D16, durées, profils CA, certificats, credentials et seules coches 1 et 2 conservés. Aucun wire antérieur adopté.

Le profil natif privé n'est pas sérialisé. Sa copie publique d'audit éventuelle reproduit identité, domaine, version et empreinte observés pour traçabilité et ne porte aucune capacité ; elle ne construit ni ne remplace l'attente native et ne fonde aucune admission.

La politique et le plan sont des contenus extérieurs distincts. Les octets réels de politique portent les préautorisations, jamais un digest d'eux-mêmes. Les descripteurs ci-dessous référencent ces contenus extérieurs par ref, version et sha ; aucun contenu n'inclut son propre digest.

### 17.2 Constantes de domaine exactes

Les domaines sont des constantes exactes comparées à l'attente native, jamais librement issus du plan. Opérateur du §14.3 de contracts.md : domaine pixs.z12.initial.operator/v1 et préfixe d'octets pixs.z12.initial.operator.payload/v1. Constantes admin : domaine admin pixs.z12.admin/v1 ; préfixe de prépublication pixs.z12.admin.prepublication/v1 ; préfixe de publication pixs.z12.admin.publication/v1 ; préfixe de binding pixs.z12.admin.binding/v1. Ces constantes sont distinctes de l'opérateur, de PA et de PG.

### 17.3 Prépublication : champs et octets signés exacts

| Champ z12.admin_prepublication/v1 | Type §1 | Contrôle |
|---|---|---|
| object_type | closed_enum[z12.admin_prepublication/v1] | discriminateur Z12 |
| schema_version | closed_enum[1.0.0] | chaîne 1.0.0 |
| prepublication_ref | public_ref | identité de prépublication, octets UTF8 admis conservés |
| installation_ref | public_ref | installation du plan, octets admis conservés |
| target_ref | public_ref | cible recoupée, octets admis conservés |
| admin_usage | closed_enum[policy_admission] | usage administratif, sans pouvoir d'opération de signature |
| policy_ref | public_ref | politique extérieure, octets admis conservés |
| policy_version | public_ref | version vérifiée contre source courante |
| policy_sha256 | ContentSHA256 | texte canonique minuscule des octets extérieurs |
| plan_ref | public_ref | plan extérieur, octets admis conservés |
| plan_version | public_ref | version vérifiée |
| plan_sha256 | ContentSHA256 | texte canonique minuscule |
| valid_from | utc_timestamp | borne définie par politique et plan, effectivement vérifiée |
| valid_until | utc_timestamp | borne postérieure à valid_from, effectivement vérifiée |
| epoch | non_negative_int | époque de prépublication, bornée |

Octets signés de prépublication : octets ASCII pixs.z12.admin.prepublication/v1 suivis d'un octet nul, puis chaque champ dans l'ordre du tableau encodé par longueur non signée 32 bits big-endian puis ses octets. Références en octets UTF8 admis conservés, sans minusculisation ; seuls ContentSHA256 en minuscule canonique ; dates en forme UTC canonique du §1 ; entiers en décimal canonique sans signe ni zéro initial sauf zéro seul ; nv absent ici. Aucun LE, padding ou format implicite. Champs exhaustifs ; inconnus, doublons, null et versions étrangères refusés. Les bornes de lecture et décodage et les budgets initiaux viennent du profil natif de bootstrap authentiquement installé, jamais de candidats non encore admis. Longueurs u32BE bornées, époques en uint64, nv_index en u32, limites natives explicites, même échéance sans reset. Aucune valeur réelle ni nouveau paramètre libre client n'est choisi.

### 17.4 Publication finale : champs et octets signés exacts

| Champ z12.admin_publication/v1 | Type §1 | Contrôle |
|---|---|---|
| object_type | closed_enum[z12.admin_publication/v1] | discriminateur |
| schema_version | closed_enum[1.0.0] | chaîne 1.0.0 |
| publication_ref | public_ref | identité de publication, octets admis conservés |
| installation_ref | public_ref | même installation et cible que le constat |
| target_ref | public_ref | cible recoupée |
| admin_usage | closed_enum[policy_admission] | même usage, sans droit d'opération |
| policy_ref | public_ref | politique extérieure |
| policy_version | public_ref | version vérifiée |
| policy_sha256 | ContentSHA256 | texte canonique minuscule |
| plan_ref | public_ref | plan extérieur |
| plan_version | public_ref | version vérifiée |
| plan_sha256 | ContentSHA256 | texte canonique minuscule |
| binding_sha256 | ContentSHA256 | représentation exacte du §17.6 |
| observed_at | utc_timestamp | instant de constat extérieur, ne définit pas seul la validité |
| valid_from | utc_timestamp | borne définie et vérifiée |
| valid_until | utc_timestamp | borne définie et vérifiée |
| publication_epoch | non_negative_int | époque du constat et de la publication |

Octets signés de publication : octets ASCII pixs.z12.admin.publication/v1 suivis d'un octet nul, puis chaque champ dans l'ordre du tableau avec mêmes règles canoniques que §17.3. La publication lie le binding ATTENDU réellement constaté extérieurement après WRITTEN et genesis et les digests de plan et politique. Genesis, événement et état-journal constatés antérieurement engagés par la publication ne contiennent ni son digest ni sa signature. Un événement ultérieur peut référencer une publication antérieure SEULEMENT sans entrer dans ses propres octets engagés et sous préconditions existantes ; aucun audit futur non circulaire n'est prohibé. Aucun calcul auto-référent.

### 17.5 Enveloppe fermée

| Champ z12.admin_signed/v1 | Type | Contrôle |
|---|---|---|
| object_type | closed_enum[z12.admin_signed/v1] | discriminateur |
| schema_version | closed_enum[1.0.0] | chaîne 1.0.0 |
| signed_kind | closed_enum[prepublication, publication] | distingue les deux charges sans clé candidate |
| payload_bytes | octets publics bornés | octets exacts du §17.3 si prepublication, du §17.4 si publication |
| signature_bytes | octets publics bornés | exactement 64 octets Ed25519 pure sur la totalité de payload_bytes, sans préhachage |

signed_kind correspond STRICTEMENT au préfixe signé et aux object_type et schema_version décodés de payload_bytes. Aucun essai de secours vers une autre variante ou représentation, aucun suffixe, champ additionnel, troncature ou normalisation implicite. La signature porte la totalité des octets exacts. Le vérificateur résout la clé publique EXCLUSIVEMENT depuis l'attente native de l'artefact authentiquement installé, avec identité, domaine et version constatés. Aucune clé candidate jointe à l'enveloppe n'est acceptée.

### 17.6 Représentation exacte de binding_sha256

binding_sha256 est calculé sur TOUS les champs requis du tableau §14.2 de contracts.md dans son ordre : object_type, schema_version, binding_ref, installation_ref, target_ref, plan_ref, plan_version, plan_sha256, policy_ref, policy_version, policy_sha256, nv_index, nv_name_sha256, nv_public_sha256, deletion_authority_ref, genesis_event_sha256, genesis_value_sha256, provision_evidence_ref. Le §14.2 ne fournit pas déjà un codec binaire. Représentation : octets ASCII pixs.z12.admin.binding/v1 suivis d'un octet nul, puis chaque champ dans cet ordre par longueur u32 big-endian puis octets. Références en octets UTF8 admis conservés ; ContentSHA256 en texte minuscule canonique ; nv_index entier public u32 en décimal canonique sur le wire ; dates et versions selon §1 et §14.3 de contracts.md. genesis_value_sha256 reste la valeur stockée, sans second hachage.

### 17.7 Admission, époques, propriétaires et cycle du pin

Une signature admin n'est JAMAIS R01, C10, mandat opérateur, PG, droit CA ou TLS. Admission complète seulement après D9, D11, état et identité natifs actuels puis D10 pour opérations, avec fencing. Résultats privés non sérialisables ; aucun booléen transportable, EVP ou capsule Python. Versions, états et retraits sont recoupés avec la vraie source courante, jamais déclarés vrais par des champs. valid_from < valid_until pour chaque charge ; à admission, intervalle UTC courant vérifié D11 entièrement dans la fenêtre admise et absence de révocation et retrait courants, sans grâce ni arrondi favorable. Sans temps vérifiable, seulement observation cryptographique préliminaire SANS capacité ; aucune vérification TLS désactivée pour NTS. observed_at ou epoch déclarés ne deviennent pas preuves actuelles.

publication_epoch est l'époque du constat et de la publication, pas une activation acquise par signature. L'admission et le lien effectif de cette publication et politique jusqu'à l'état courant sont constatés par le propriétaire compétent depuis le journal et le NV courants, pas une chaîne fournie réputée autorisée ; si lien, révocation ou état non vérifiable : refus du §14.5 sans capacité. Après D6 aucune nouvelle autorité ordinaire créée par M1. Aucun nouveau droit NV et aucun port ordinaire par implication.

Avant PG et jusqu'à D6, propriétaire INITIAL ; après adoption et retrait D6, seul l'ordinaire courant selon ses contrats, sans pouvoir M1 de contournement ni recréation de l'initial par vieux manifeste, artefact, snapshot, index absent ou Clear. Adoption publique conserve clés, chaînes et âges. Remplacement et révocation du pin uniquement sous procédure extérieure explicitement mandatée, jamais par publication auto-validante d'une nouvelle clé ; aucune autorité ordinaire nouvelle inventée. Si la procédure de révocation et évolution n'est pas réalisée, elle reste garantie à réaliser et qualifier ; ses refus sont ceux du §14.5 de contracts.md et ses propriétaires sont l'artefact natif, le provisionneur extérieur et l'autorité ordinaire courante, sans DTO de preuve.


### 17.8 Interface privée de BUILD du profil compilé

 producteur `src/pixs/pzt_ca/native/_admin_profile_gen.py`, stdlib seule.
 Aucune clé privée lue, générée ou signée. Ni `.env`, ni stockage privé,
 ni outil, ni build, ni test, ni secret, ni TPM.

 entrée JSON fermé 10 champs : `object_type=="z12.admin_profile_data/v1"`,
 `schema_version=="1.0.0"`, `identity_ref` UTF8 `1..256` sans NUL,
 `domain=="pixs.z12.admin/v1"`, `version` UTF8 `1..256` sans NUL,
 `public_key_hex[64]` minuscule, zéro refusé sans preuve de point Ed25519,
 `max_payload_len u32>=1`, `max_field_len u32>=1 <=payload`,
 `budget_ns u64>=1`, `fixture bool` tel quel. Doublons, `null`,
 supplémentaires refusés. `parse_constant` refuse NaN et Infinity.
 `RecursionError` refusé. `--max-input-bytes 1024..65536, défaut 8192`,
 limite de parseur seule. `--procedure-ref` externe UTF8 `1..256`
 sans NUL, validé sans champ JSON ajouté. Entrée par FD réel
 `O_RDONLY|O_NOFOLLOW|O_CLOEXEC|O_NONBLOCK`, `S_ISREG`, taille
 `>0` et `<=limite`, instantané `size, mtime_ns, ctime_ns, dev, ino`
 avant et après, octets `==size` et fin bornée. `_Refuse` et frontière
 CLI unique, `argparse` sans écho, `ValueError` NUL refusé.

 sorties `z12_admin_profile.inc` et `z12_admin_profile.manifest.json`
 dans `--out-dir` par FD `O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC` et `S_ISDIR`.
 Finals `O_EXCL|O_NOFOLLOW|O_CLOEXEC 0600`, jamais écrasés. Écriture,
 `fsync` fichier, puis `fsync` répertoire. Chaque FD fermé en `finally`
 par fermeture unique. Toute erreur de publication ou de fermeture
 rend un retour non zéro. Échec d'écriture ou de `fsync` émet
 `ERR_PAIR_PARTIAL` puis le code d'origine. Fermeture hors erreur active
 émet seulement `ERR_DIR_CLOSE`. Aucune suppression, partiels conservés,
 paire non atomique. Répertoire supposé contrôlé par la procédure, sans
 résistance à un acteur de mêmes droits. En-tête : octets et longueurs
 identité, domaine, version et clé, bornes, `budget ULL`, `fixture`.
 Manifeste `z12.admin_profile_manifest/v1` : valeurs publiques
 `identity_ref, domain, version, procedure_ref`, `public_key_hex` et
 `public_key_sha256` des 32 OCTETS de clé, bornes, budget, fixture,
 `generator, input_sha256, header_sha256`, sans droit ni provenance.
 Le build futur exige succès du générateur puis paire et empreinte
 avant compilation. Le runtime `_admin_profile.pxi` ne lit pas ce manifeste.


### 17.9 Forme UTC canonique des charges initiales signées

Concrétise la forme `UTC` déjà exigée par `§1/14.3/17.3/17.4`, sans créer de port, clé, ancre ni changement d'autorité. Choix de représentation technique dans les normes déjà adoptées. Charges visées exclusivement : mandats `§14.3` et charges `§17.3/17.4`. Aucun format nouveau pour les `DTO` ordinaires ni les certificats `X509`, aucun nouveau `TTL`, aucune adoption `D6` ni capacité conférée.

Forme exacte sur `27` octets `ASCII` : `YYYY-MM-DDTHH:mm:ss.ffffffZ`, soit six chiffres microsecondes fixes, compatibles `datetime/PostgreSQL`. Calendrier grégorien, année `0001..9999`, mois `01..12`, jour valide du mois incluant années bissextiles, heure `00..23`, minute `00..59`, seconde `00..59`. Seconde `60` refusée. `T` et `Z` majuscules seuls, fraction fixe, aucun décalage, aucune autre forme, aucune norme implicite, aucun arrondi ni troncature. Formats étrangers refusés. Aucune réécriture des octets signés.

Fenêtres et ordres `issued_at`, `valid_from<valid_until` restent ceux des contrats. `observed_at` ne prouve pas le temps courant, époque distincte de la date.

Comparaison directe aux intervalles `D11` à précision native, en convertissant exactement la fraction microseconde vers nanosecondes dans une paire secondes/fraction, sans total `int64` nanosecondes à risque de dépassement pour l'année `9999`. Aucune quantification du temps `UTC` courant exigée. Si un pont vers microsecondes est nécessaire, projection uniquement conservatrice par plancher du bas et plafond du haut, sinon refus, sans relâcher les bornes `D11` déjà définies `1s/600s` ni inventer de `TTL`. Variante neuf chiffres nanosecondes non retenue pour ce fil, sans brider les mathématiques ni l'horloge native `NTS`.

Recette en seconde phase sur sources réelles : limites, années bissextiles, refus des variantes, seconde `60`, aucun arrondi favorable, intervalle entièrement dans la fenêtre `D17`, ordre `D10`. Aucune réussite acquise par le présent texte.


### 17.10 Bornes de construction du propriétaire — profil public distinct
1. Objet fermé `z12.owner_limits_data/v1`, 10 champs seuls admis.
   Supplémentaires, doublons, `null`, manquants = `REFUS`.
   Aucune valeur opérationnelle par défaut. Budget admin compilé
   inchangé. Pas de clé, pin, service, port, droit nouveau.

2. Table fermée :

   | # | champ | type JSON | règle |
   |---|---|---|---|
   | 1 | `object_type` | string | `==z12.owner_limits_data/v1` |
   | 2 | `schema_version` | string | `=="1.0.0"` |
   | 3 | `identity_ref` | string | `1..256 OCTETS UTF8 sans NUL`, référence procédure build |
   | 4 | `domain` | string | `==pixs.z12.owner.limits/v1`, tag build, PAS autorité signature |
   | 5 | `version` | string | `1..256 OCTETS UTF8 sans NUL`, version profil build, indépendante, PAS fixée `1.0.0` |
   | 6 | `image_exe_max_bytes` | number entier | u32 `>=1`, non-bool, exigé |
   | 7 | `procmetadata_max_bytes` | number entier | u32 `>=1`, non-bool, exigé |
   | 8 | `unit_path_max_bytes` | number entier | u32 `>=1`, non-bool, exigé |
   | 9 | `unit_name_max_bytes` | number entier | u32 `>=1`, non-bool, exigé |
   | 10 | `fixture` | bool | `true/false` exigé, jamais preuve provenance |

3. Constantes C produites :
   - `Z12_OWNER_IMAGE_EXE_MAX` u32, `Z12_OWNER_PROCMETA_MAX` u32,
     `Z12_OWNER_UNIT_PATH_MAX` u32, `Z12_OWNER_UNIT_NAME_MAX` u32.
   - `Z12_OWNER_LIMITS_FIXTURE` `0/1`.
   - `Z12_OWNER_LIMITS_IDENTITY_BYTES` tableau unsigned char statique NUMÉRIQUE + `Z12_OWNER_LIMITS_IDENTITY_LEN`, `Z12_OWNER_LIMITS_DOMAIN_BYTES` + `Z12_OWNER_LIMITS_DOMAIN_LEN`, `Z12_OWNER_LIMITS_VERSION_BYTES` + `Z12_OWNER_LIMITS_VERSION_LEN`, aucune injection string C.

4. Sorties `z12_owner_limits.inc` + `z12_owner_limits.manifest.json`. Manifeste objet `z12.owner_limits_manifest/v1`, nature déclarative non-autorité : `identity_ref`, `domain`, `version`, `procedure_ref`, 4 bornes, `fixture`, `generator`, `input_sha256`, `header_sha256`, `outputs`. IO `O_EXCL`, `fsync`, non-zéro, partiels conservés, jamais écrasement/suppression. `fixture:false`, `stat`, SHA jamais preuve provenance/admission.

5. Générateur privé séparé
   `src/pixs/pzt_ca/native/_owner_limits_gen.py`.
   Importe seuls helpers réels de `_admin_profile_gen.py` :
   `_read_input`, `_open_output_directory`, `_write_output`,
   `_close_keep`, `_pairs_no_duplicate`, `_reject_constant`,
   `_Refuse`, `_StrictParser`. Sans modifier source admin ni
   ses 10 champs. Invocation exacte :
   `python3 -m pixs.pzt_ca.native._owner_limits_gen`.
   Mêmes 4 options `--input/--out-dir/--procedure-ref/
   --max-input-bytes`, parse `1024..65536` défaut `8192`
   technique, pas budget produit. Paire `O_EXCL/fsync`,
   partiel conservé non-zéro, jamais écrasement/suppression.
   Build futur : deux générateurs + deux paires + SHA headers
   vérifiés avant compilation. Production : deux flags
   compilés non-fixture.

6. Vérification : bornes uint32 positives représentables `size_t`. Chaque `n <= borne`, avec garde `SIZE_MAX`, AVANT toute allocation dépendante de la taille candidate, avant scans/copies. Tout `n+1` explicitement gardé. Pas de limite 16MiB. Aucun claim NTS. Bornes != garantie temps hard. `deadline` courante vérifiée
   avant/après. Constructeurs bibliothèque non interruptibles :
   limite explicite, pas d’annulation promise.
   Futur `owner_context` : prend endpoint observationnel borné
   seul + `out/diag`, crée lui-même LIBCTX, connexion, facts,
   image-ctx. Il ne reçoit ni ctx, ni facts, ni bornes du
   caller. Aucune API inventée fixée ici.
   Cleanup conserve pointeur vers TOUTE ressource encore
   vivante + diag ; ne suppose pas pointeur vivant si helper
   l’a libéré ; pas de détachement d’objet possédé vivant
   sur `unload/munmap` en échec.

## 18. Cérémonie UTC extérieure signée — D18 du 25 octobre 2026

### 18.1 Propriétaires, attente de clé D10 et domaines

Z12 constate, la voie normale n’exige aucune source extérieure et D18 reste exceptionnel, seulement lorsque l’UTC fiable est indémontrable. Quand une cérémonie est nécessaire, le provisionneur extérieur qualifie réellement la source indépendante et l’opérateur personnel D10 signe, avec nonce volatile de 32 octets à usage unique. La clé publique attendue est compilée sous artefact authentique, distincte de l’admin, avant admission de politique. Domaine cérémonie `pixs.z12.time.ceremony/v1`, préfixe binaire `pixs.z12.time.ceremony.payload/v1`, distincts de `pixs.z12.initial.operator/v1`. Aucune clé candidate jointe n’est acceptée et le §18.2 reste inchangé.

### 18.2 Vingt-deux champs exacts, codec et enveloppe fermée

Payload fermé `z12.time_ceremony_payload/v1`, ordre fixe : `object_type`, `schema_version==1.0.0`, `domain`, `key_ref`, `challenge_ref`, `challenge_nonce` brut 32, `installation_ref`, `target_ref`, `executor_set_ref`, `executor_set_sha256`, `plan_ref`, `plan_version`, `plan_sha256`, `policy_ref`, `policy_version`, `policy_sha256`, `source_ref`, `source_evidence_sha256`, `source_measured_at_utc` 27 octets, `lower_utc` 27 octets, `upper_utc` 27 octets, `boot_context_ref`. L’objet vaut `z12.time_ceremony_payload/v1` et le domaine vaut exactement celui du §18.1. Textes UTF-8 sans NUL de 1 à 256 octets ; l’interdiction NUL concerne seulement les textes, le nonce brut de 32 octets et la signature brute de 64 octets peuvent contenir des octets nuls. SHA en hexadécimal minuscule de 64 octets, dates au format 27 octets du §17.9. Représentation binaire : préfixe ASCII suivi d’un octet nul, puis chaque champ par longueur u32 big-endian et octets. Longueur du nonce exigée à 32. Champs étrangers, doublons, types divergents et longueurs invalides refusés. Enveloppe fermée `z12.time_ceremony_proof/v1` à quatre champs, version exactement `1.0.0` : `object_type`, `schema_version`, `payload_bytes`, `signature_bytes` de 64 octets Ed25519 pure sur tout `payload_bytes`, préfixe et longueurs inclus, sans préhachage. Aucun suffixe, bourrage, champ absent ou additionnel, ni type mauvais. Aucune clé candidate.

### 18.3 Profil natif authentique

Identifiant, version et limites positives explicitement apportés sous procédure extérieure, sans défaut ni choix client : longueur maximale de charge et de champ positives u32 représentables, budget global positif u64 en nanosecondes, borne de dérive et incertitudes issues d’un profil qualifié avec version et provenance véritables. Aucune borne administrative candidate ou de manifeste ne vaut authenticité. Ces documents ne créent aucune donnée réelle de profil. Cette description ne qualifie pas l’installation.

### 18.4 Défi volatile et continuité

Défi volatile natif, nonce de 32 octets issu d’une source CSPRNG native, cycle frais, émis, vérification, consommé ou invalidé. Invalidation avant toute utilisation, atomicité et concurrence traitées. Redémarrage, suspension ou perte de contexte détruisent la capacité. Aucun fichier restaurable ne la recharge. Le non-retour D6 reste une garde réelle indépendante.

### 18.5 Mesure extérieure et propagation conservatrice

Mesures natives à l’émission, au retour et à l’usage, avec vérification de continuité, de suspension et de taux avant toute projection. Mesure extérieure après défi et avant réponse, avec `lower_utc <= source_measured_at_utc <= upper_utc`. La mesure extérieure et son UTC signé sont confrontés à la source indépendante qualifiée, sans autorité par la seule signature. Écart entre UTC et horloge hôte relevé nativement. Propagation par élargissement avec borne de dérive qualifiée et bornes de délai du profil, jamais rétrécissement ni choix client. Sinon `TIME_UNVERIFIABLE`. Aucune autre dépendance, admission ou valeur produit créée.

### 18.6 Raccord TLS effectif

Comparaison prudente de l’intervalle entier aux `notBefore` et `notAfter` de chaque certificat admissible, avec l’horloge réelle utilisée et les contrôles TLS normaux, sans contournement des dates et sans prétendre une API `chrony` disponible. Raccord manquant égal qualification bloquante.

### 18.7 Passage D11 après exception

La cérémonie D18 reste exceptionnelle et ne confère aucun mandat. Après réparation, le contrat D11 explicitement choisi s’applique selon son mode, sans NTS ou Internet neuf obligatoire en HORS_LIGNE qualifié, puis seules les gardes existantes s’appliquent. D6 n’est jamais rouvert.

### 18.8 Refus et recette

Refus du vocabulaire du §14.5, dont `TIME_UNVERIFIABLE`. Recette de seconde phase : nominal, bornes exactes et juste au-delà, doublons, types, nonce et signature invalides, mauvais plan, politique, source, fraîcheur, rejeu, suspension, redémarrage, dérive, TLS sans chaîne admissible, D6 sans réouverture.

### 17.11 Tranche publique pré-admission — profil privé versionné

Privé natif seul, sans admission `CA/PG/NV/TLS` ni temps `D11/D18` prétendu. `D1-D18`, `17.8-17.10` et coches `1` et `2` conservés, aucun nouveau choix de sécurité. Écriture documentaire envisagée seulement ici, les cinq autres sources seulement après documentation validée et examens `NFDOC/Codex`.

Graphe exact requis, sans duplication : `deadline`, `admin_profile`, `operator_verify` amenant `_openssl_ed25519` une fois, `launch_obs`, `systemd_connection`, `process_image` sans seconde déclaration `OSSL_LIB_CTX`, `manager_unit`, `owner_context`, `policy_bytes`, `admin_codec`, `admin_values`, `admin_verify`, `admin_time`, puis `owner_public_slice` selon dépendances réelles. Aucun `include` explicite `_ed` en plus dans ce graphe. Les unités autonomes `esys` et `nvguard` incluent `_ed` une fois indépendamment. Aucun fichier adaptateur inventé dans les recettes actuelles, aucun consommateur image existant. Périmètre potentiel exact de six fichiers : `contracts.md`, nouveau `_owner_build_gen.py`, nouveau `_owner_public_slice.pxi`, `_policy_bytes.pxi`, `_process_image.pxi`, `_owner_context.pxi` pour commentaire de prérequis seulement.

Profil `public-read` fermé à douze champs exacts `z12.owner_build_data/v1` version `1.0.0` : `object_type`, `schema_version`, `identity_ref`, `domain==pixs.z12.owner.build/v1`, `version`, `policy_max_bytes`, `plan_max_bytes`, `journal_max_bytes`, `uid`, `gid`, `mode`, `fixture`. Textes `UTF8` strict `1..256` sans `NUL`, `domain` et `schema` exacts, `fixture` booléen. Entiers exacts ni booléen ni flottant. Trois bornes positives `u32` et `<SIZE_MAX`, `<=SSIZE_MAX` avant tout `n+1`. `uid/gid u32` représentables avec aller-retour vers types natifs. `mode` entier décimal bits `POSIX 0..0777`, lecture propriétaire `0400` requise, sans écriture groupe et autres `0022`, sans exécution `0111`, sans bits spéciaux. Aucune valeur par défaut, format privé initial commun aux trois `FD` seulement, sans qualification. `JSON` source fermé avec refus des doublons, inconnus, `null`, substituts et types divergents. En-tête généré à tableaux numériques statiques et macros exactes : `Z12_OWNER_BUILD_POLICY_MAX`, `Z12_OWNER_BUILD_PLAN_MAX`, `Z12_OWNER_BUILD_JOURNAL_MAX`, `Z12_OWNER_BUILD_UID`, `Z12_OWNER_BUILD_GID`, `Z12_OWNER_BUILD_MODE`, `Z12_OWNER_BUILD_FIXTURE`, `Z12_OWNER_BUILD_IDENTITY_LEN` et `Z12_OWNER_BUILD_IDENTITY_BYTES`, `Z12_OWNER_BUILD_DOMAIN_LEN` et `Z12_OWNER_BUILD_DOMAIN_BYTES`, `Z12_OWNER_BUILD_VERSION_LEN` et `Z12_OWNER_BUILD_VERSION_BYTES`. Manifeste `z12.owner_build_manifest/v1` avec `sha256` source et en-tête, sans secret ni droit. Mêmes assistants et quatre options `input/out-dir/procedure-ref/max-input-bytes` avec référence publique de procédure. Sans fusion avec `admin` dix champs ni `owner_limits` dix champs.

Point d’entrée unique `z12_slice_observe_prepub` prenant `owner` réel, trois `FD`, tailles candidates, `payload` candidat, `signature_len_candidate` avec exigence `64`, `signature` candidate, `out/diag` seuls. `payload` borné au profil `admin` compilé légitime pour charge cryptographique, copié en possédé avant vérification. Tailles des trois `FD` positives et `<=` profil `public-read`. Propriété des `FD` fermée : `z12_policy_bytes_load` consomme les trois `FD` y compris en échec via `finish/close_unique`, avant transfert l’adaptateur sait qui détient les `FD`, après transfert aucun double `close`, doublons et `FD` invalides refusés avec fermeture unique selon contrat. Copie native de signature `64` pouvant contenir `NUL`, `payload` sous cadrage strict, durées couvrant copies en lecture seule vérifiées et `policy_bytes`, jamais tampons du caller.

Même `LIBCTX` par variante empruntée réelle `z12_policy_bytes_load_with_ctx`, ancien chargeur conservé avec propriété explicite de son `CTX` éphémère. Aucune libération du `CTX` par l’adaptateur. Appels réels `_admin_verify_signed`, `_admin_values_observe`, `_admin_time_observe` pour prépublication quinze champs, digests réels des `FD` comparés sans hachage supplémentaire. `ref`, `policy_version` et `plan_version` du `payload` liées aux digests réels sans être revendiquées comme valeurs analysées dans des contenus non encore formatés. Enveloppe logique `D17` avec intégration native fermée toujours requise pour admission complète, sans prétendre une porte externe validée pour octets bruts. `TCB`, protection `NTS`, `NV` et état courant restent gardes manquantes refusant toute capacité.

Séquence : garde `PID/TID`, profil `build` observé, `deadline` unique vérifiée avant et après, chargement avec `CTX` emprunté, copies natives, cadrage et signature `M1` compilée, dates structurelles, égalités de digests, refus sinon. Résultat : observation cryptographique native avec liaisons auditables, non admission. Recettes futures en seconde phase sur sources réelles avec bornes exactes et juste au-delà, `FD` invalides, doublons, durées, rejets et élargissements conservateurs. Aucune qualification acquise par ce texte.

## 19. Contrat temps v2 T0 — adoption documentaire

Le présent §19 est adopté documentairement en T0 et fait foi avec [RACCORDS_TEMPS_V2.md](RACCORDS_TEMPS_V2.md) pour l'interface, les durées de vie, les profils et les refus. L'identifiant `pixs.time.evidence` version `2.0.0`, catégorie `API`, propriétaire `pixs.kernel` désigne une déclaration pure, sans autorité temporelle, métier ou cryptographique. Le protocole comporte quatre méthodes avec projections diagnostiques à quatre champs ou `None` non autoritaire, sans manieur transporté. L'intervalle entier est vérifié au point d'usage par les vrais consommateurs Core, Auth, Agent et PZT, avec conservation de `Clock.now` pour horodatage. Les 11 liaisons de demande et 16 champs d'observation sont conservés. Le contrat v1 du `§15.3` et le D18 du `§18.2` restent intacts. Budgets D11 et cérémonie distincts, sans prolongation de certificat ni mandat par dégradation. Aucun changement aux §1 à §18.
