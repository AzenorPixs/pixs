# Références normatives — Z22

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 10526 | [Contrat A10i97 — Manifeste de purge en JSON UTF-8 fermé, typé et versionné — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10526) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10576 | [Contrat A10i98 — Empreinte SHA-384 entière du manifeste de purge sur octets exacts — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10576) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10625 | [Contrat A10i99 — Manifeste de purge plafonné à 128 Kio par version et phase — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10625) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10675 | [Contrat A10i100 — Empreinte de manifeste SHA-384 encodée Base64url sans remplissage — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10675) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10718 | [Contrat A10i101 — Complexité du manifeste JSON plafonnée à 8 niveaux, 32 membres et 1 000 éléments — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10718) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10762 | [Contrat A10i102 — Lot préparé par préfixe déterministe sous capacité d'audit de toutes phases — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10762) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10816 | [Contrat A10i103 — Manifeste JSON produit selon JCS RFC 8785 sous schéma qualifié — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10816) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10863 | [Contrat A10i104 — Sources de purge ordonnées par première persistance puis identité et génération — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10863) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10910 | [Contrat A10i105 — Manifeste revalidé et empreinte recalculée à chaque usage — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10910) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 10953 | [Contrat A10i106 — Sources du travail délimitées par borne stable versionnée et parcours par lots — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L10953) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11000 | [Contrat A10i107 — Conservation du manifeste liée aux durées et holds de l'audit — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11000) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 11048 | [Contrat A10i108 — Anomalie de manifeste confinée sous preuve, blocage global sinon — option A validée le 9 octobre 2026](../../specs/pzt/spec.md#L11048) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--abc29b404d

Source : `openspec/specs/pzt/spec.md`, ligne 10526. SHA-256 du bloc : `81247fd73c737df8461dbb47fd1a32ca38480225ef63ba08dddc32d603d3691e`.

~~~~text
### Requirement: Contrat A10i97 — Manifeste de purge en JSON UTF-8 fermé, typé et versionné — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i97 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i97

Audit de lot lié à manifeste durable A10i94 A et sélection bornée A10i86 A
conservés. Format indépendant de l'empreinte A10i98 et du plafond A10i99 ;
manifeste de purge distinct du dossier racine A10i38.

| Choix validé | Format du manifeste | Conséquence |
| --- | --- | --- |
| A | Document JSON UTF-8 typé/versionné, schéma fermé | Inspection textuelle et conventions Pixs, coût à qualifier |

Un objet racine, types/champs obligatoires et usages/version déclarés ;
inconnus/doublons après décodage, Unicode invalide, BOM, NaN/Infinity,
commentaires ou données après objet refusés. Champs int64/uint64 selon
conventions décimales exactes A10i64 explicitement réutilisées dans ce profil,
identifiants opaques sans conversion numérique. Profondeur/cardinalités/plages
du manifeste à qualifier, limites IPC A10i56/A10i65 sans transposition automatique.
CBOR B non retenu comme format alternatif, aucune conversion JSON/CBOR
silencieuse ou extension de schéma admise. Complexité 8/32/1 000 A10i101 A
validée le 9 octobre 2026.
Commun : contexte/IDs commande-opération-travail-lot, classe/périmètre,
politique/version, cibles exactes et résultat/phase liés. Sélection avant effet
et résultats confirmés/inconnus après effet distingués ; toute évolution
produit nouvelle version immuable et référence d'audit, aucune réécriture
d'un ancien manifeste ou résultat anticipé. Couplage audit/effet à qualifier.
Octets exacts conservés durablement, référence vers document mutable ou simple
structure parsée insuffisante ; pas de re-sérialisation admise comme mêmes
octets pour vérifier empreinte. Empreinte externe au document qu'elle couvre,
sans autoréférence ; durée/accès/holds et retrait A10i96 toujours contrôlés.
A validée pour format textuel déjà familier. [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) et
[RFC 8949](https://www.rfc-editor.org/rfc/rfc8949) définissent JSON/CBOR ;
préférence de format choisie par Pixs, sans bibliothèque/version adoptées.
Aucun contenu source/secret ajouté, manifeste réel, codec, migration, purge
ou OpenSpec créés/modifiés. Recette : champs inconnus/doublons, phase incohérente,
version remplacée, conversion, octets modifiés et refus sans audit/preuve inventés.
A10i97 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i97

- **WHEN** un profil revendique le traitement A10i97 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--9b000144ed

Source : `openspec/specs/pzt/spec.md`, ligne 10576. SHA-256 du bloc : `27098c45cd9ae70a8b96c88084725653fe5493f4a98eaa2805a31de1fa98f7a8`.

~~~~text
### Requirement: Contrat A10i98 — Empreinte SHA-384 entière du manifeste de purge sur octets exacts — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i98 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i98

Liaison d'audit A10i94 A conservée. Choix explicite pour manifeste de purge,
indépendant du format/plafond ; empreinte du dossier racine A10i36 B inchangée.

| Choix validé | Empreinte sur octets exacts | Taille entière du digest |
| --- | --- | --- |
| A | SHA-384 | 48 octets |

SHA-384 A retenu, SHA-256 B non retenu comme alternative.
Digest complet sans troncature, algorithme/type/version déclarés dans référence
d'audit avec identité/phase/version et longueur exacte du manifeste. Référence
extérieure au document couvert, absence d'autoréférence et octets immuables
contrôlés ; réencodage ou changement de résultat produit nouvelle référence.
A validée pour cohérence d'algorithme avec dossiers déjà SHA-384, sans
transposer droits/clé/signature de racine ; aucun
gain CPU/latence universel présumé. Le [NIST, FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)
définit ces algorithmes ; choix validé par Pixs, pas d'obligation externe
ou conformité de l'implémentation revendiquées.
Encodage du digest, champs exacts, calcul/vérification/bibliothèques et budgets
à qualifier ; encodage Base64url/64 A10i100 A validé le 9 octobre 2026. Aucun
Base64url du dossier A10i37 automatiquement adopté ici.
Hash ne prouve ni autorisation, authenticité de l'émetteur, dernier état,
commit PostgreSQL ni réalisation physique de purge. Contrôles d'audit/source
autorisée/exclusion/corrélation et résultat courant restent requis ; digest
recalculé sur document substitué sans audit admissible toujours refusé.
Aucune signature supplémentaire, clé métier, mode de chiffrement WireGuard/
TLS ou format de reçu A12 modifiés. Audit/manifeste requis absent/incohérent :
aucun nouvel effet de purge, résultat inconnu réconcilié sans preuve inventée.
Coûts/providers/plateformes à qualifier, aucun digest réel/clé/backend,
signature, purge ou OpenSpec créés/modifiés. Recette : digest entier/incorrect/
tronqué, confusion d'algorithme, changement d'octets/phase/version et ancien
manifeste sans permission ou état actuel présumés par intégrité seule.
A10i98 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i98

- **WHEN** un profil revendique le traitement A10i98 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--c2ed4a665a

Source : `openspec/specs/pzt/spec.md`, ligne 10625. SHA-256 du bloc : `f877690db8410439d171ae4e6d9b33b65ad3de24507fa8d85d0c505a581727d4`.

~~~~text
### Requirement: Contrat A10i99 — Manifeste de purge plafonné à 128 Kio par version et phase — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i99 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i99

Manifeste durable requis A10i94 A et lots au plus 1 000 sources A10i86 A
conservés. Plafond par version/phase de document encodé, indépendant du format
et du digest ; premier jet configurable, aucune garantie de capacité observée.

| Choix validé | Taille maximale par document encodé |
| --- | --- |
| A | 128 Kio |

Plafond A 131 072 octets inclusifs retenu, B 1 Mio non adopté. Octets exacts
du manifeste JSON UTF-8, métadonnées et cibles/
résultats inclus, aucune compression/externalisation arbitraire pour contourner
taille. Enveloppe d'audit/références et nombre de versions/copies à borner
séparément ; plafond par document sans limite globale d'espace automatiquement
prouvée. Taille annoncée non fiable, écriture/lecture/validation bornées avant
allocation non maîtrisée, pas de copie des payloads sources pour justification.
Lot doit pouvoir être audité intégralement dans limites qualifiées avant
effet. Document trop grand/incomplet/ambigu => lot refusé, aucun nouvel effet
destructif sans audit admissible. Pas de troncature de cibles/résultats,
checkpoint avancé ou éléments ignorés pour sembler conforme. Plan/lot plus
petit seulement par contrat autorisé/qualifié, dans mêmes budgets/mandats
et sans nouveau compteur de retries ; traitement de préfixe A10i102 A validé
le 9 octobre 2026 sous capacité d’audit prouvée avant effet.
1 000 sources est un maximum, pas promesse que toutes descriptions tiennent
dans 128 Kio. Taille d'IDs/dérivés/versions, profondeur/cardinalités/amplification
et volume d'audit/manifeste à qualifier ; budget global 60 s et ressources
backend prioritaires, pas de RAM 128 Kio ou tampon métrique A10i74 transposés.
A validée comme premier jet borné, besoins/
consommation à mesurer par profil/provider. Pas de hausse automatique, nouveau
stockage local PA, sélecteur d'algorithme ou droit de purge déduits du plafond.
Aucun document, donnée d'audit, variable/runtime, purge ou OpenSpec modifiés.
Recette : taille exacte/plus un, sources nombreuses/gros IDs, document partiel,
copies/versions, annonce fausse et aucun effet sans audit complet admissible.
A10i99 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i99

- **WHEN** un profil revendique le traitement A10i99 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--07099b9279

Source : `openspec/specs/pzt/spec.md`, ligne 10675. SHA-256 du bloc : `d4010275ed289d11c59bfb9a5f78f2cb634efaf6a3c547e8fa7970eff90aa692`.

~~~~text
### Requirement: Contrat A10i100 — Empreinte de manifeste SHA-384 encodée Base64url sans remplissage — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i100 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i100

SHA-384 entier/48 octets A10i98 A conservé. Encodage de la référence externe
d'audit du manifeste, indépendant des limites JSON A10i101 et du choix de lot
A10i102 ; aucun format de reçu ou de signature supplémentaire adopté.

| Choix validé | Encodage du digest SHA-384 | Longueur exacte |
| --- | --- | --- |
| A | Base64url sans remplissage | 64 caractères ASCII |

Alphabet lettres/chiffres/tiret/underscore, aucun « = », espace, retour
ligne ou variante Base64 classique. Décodage strict de 64 caractères vers
48 octets, réencodage identique ; absence de correction/trimming implicites.
Hexadécimal canonique B non retenu comme encodage alternatif ;
pas de conversion silencieuse ou tolérance de variantes.
Commun : type/algorithme/version/rôle déclarés, décodage avant comparaison
exacte des octets ; empreinte valide sans authentification/autorisation,
état courant, commit ou purge réalisée présumés. Référence externe liée à
phase/lot/version et longueur exacte, original immuable toujours requis.
Choix explicite pour ce manifeste ; conventions du dossier A10i37 sans portée
automatique. A validée pour cohérence et représentation plus courte,
coûts à mesurer.
[RFC 4648](https://www.rfc-editor.org/rfc/rfc4648) définit alphabets/encodages ;
profil strict choisi par Pixs, pas de bibliothèque/provider choisis.
Aucun digest réel, champ/API, clé, signature, purge ou OpenSpec modifiés.
Recette : longueur/alphabet/casse, caractères Unicode, espace/remplissage,
digest tronqué, rôle/phase incorrects et aucune normalisation permissive.
A10i100 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i100

- **WHEN** un profil revendique le traitement A10i100 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--ea000178ff

Source : `openspec/specs/pzt/spec.md`, ligne 10718. SHA-256 du bloc : `f0a5af2f42db360c91b1db6fe193cdd9078213cefa246ad1d01961372721e24e`.

~~~~text
### Requirement: Contrat A10i101 — Complexité du manifeste JSON plafonnée à 8 niveaux, 32 membres et 1 000 éléments — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i101 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i101

JSON fermé A10i97 A, contenu 128 Kio A10i99 A et au plus 1 000 sources A10i86 A
conservés. Plafonds distincts du JSON IPC A10i65 et du dossier racine A10i39.

| Choix validé | Profondeur maximale | Membres par objet | Éléments par tableau |
| --- | --- | --- | --- |
| A | 8 | 32 | 1 000 |

Plafonds A 8/32/1 000 validés ; B 16/64/1 000 non retenus.
Objet racine niveau 1, chaque objet/tableau imbriqué ajoute 1, primitives sans
niveau supplémentaire. Plafonds inclusifs appliqués ensemble avec 131 072 octets,
types/champs déclarés, nombre de sources et budgets courants ; 1 000 éléments
dans un tableau n'autorisent pas 1 000 sources dans chaque tableau.
Doublons comptés/rejetés avant écrasement, conteneurs/nombres/Unicode/unités
stricts ; aucune construction d'arbre non borné suivie de troncature. Limites
détectées au plus tôt, message ambigu/trop complexe refusé sans effet de purge,
cible omise ou checkpoint avancé. Sérialisation et référence conservées exactes.
Taille de champs/total des éléments/tokens/amplification RAM et coût de validation
qualifiés au plafond de contenu/budget 60 s, aucun plafond RSS démontré par ces
seules valeurs. Profondeur/cardinalité sans type ou extension inconnue admis.
A validée pour structure restreinte, coût/couverture à mesurer. Plafonds de premier jet configurables sous
profil/version autorisés, sans bascule automatique A/B pour accepter entrée.
Le tableau des cibles de lot peut contenir au plus 1 000 références sous limite
de taille simultanée ; remplissage de cette capacité non garanti.
Aucun parseur/version, manifeste, configuration, purge ou OpenSpec modifiés.
Recette : racine/profondeur exacte/plus un, objet 32/64 membres, tableau 1 000/
plus un, sources répétées, contenu saturé et refus sans données tronquées.
A10i101 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i101

- **WHEN** un profil revendique le traitement A10i101 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--8e038084af

Source : `openspec/specs/pzt/spec.md`, ligne 10762. SHA-256 du bloc : `46f6c28d66e33feec58c3288784e8ffed762086c9dd8e0420229378528f54996`.

~~~~text
### Requirement: Contrat A10i102 — Lot préparé par préfixe déterministe sous capacité d'audit de toutes phases — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i102 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i102

Lot au plus 1 000 A10i86 A, audit complet A10i94 A et manifeste 128 Kio A10i99 A
conservés. Préparation avant engagement/effet, indépendante de réessai A10i89,
empreinte/encodage ; aucun agrandissement de limite ou omission de preuve.

| Choix validé | Préparation avant effet | Conséquence |
| --- | --- | --- |
| A | Préfixe déterministe admissible sous capacité d'audit de toutes phases | Lot éventuellement réduit, contrôles/budgets conservés |

Ordre stable/curseur/contexte/politique qualifiés, sélection d'un préfixe
contigu parmi cibles admissibles reconnues, jamais saut d'une cible gênante.
Nombre au plus 1 000 ; capacité de manifeste de sélection et de toutes phases/
résultats/refs/dérivés requis bornée avant effet, y compris résultats partiels/
inconnus. Limites de schéma/tailles des résultats permettent réserve conservative
qualifiée ; seule taille de la sélection initiale insuffisante.
Choix du plus grand préfixe prouvé admissible selon contrat déterministe borné,
pas de mesure prétendant deviner résultat futur. Si une seule cible ne peut
être couverte intégralement, ou borne de résultat inconnue : refus/diagnostic
avant effet, requalification/replanification autorisées requises.
Cibles restantes restent dans progression reconnue pour lots ultérieurs ;
checkpoint avancé seulement après lot confirmé A10i88, aucune suppression
silencieuse de backlog ou nouvelle identité permettant de repartir à zéro.
Refus/replanification systématique B non retenu comme règle alternative ;
refus avant effet requis si aucun préfixe ne peut être prouvé admissible.
Commun : calcul/sélection/validation/réservation chargés au travail 60 s et aux
ressources qualifiées, pas de boucle infinie de tailles ou de retries wrapper.
Manifestes/versions/résultats exacts, contrôle courant des holds/bail/mandat,
audit et déduplication conservés. Estimation invalide après effet => incident
et réconciliation, pas de résultat tronqué ou réussite inventée ; profil ne
garantissant pas audit complet refusé avant activation.
A validée pour adapter le nombre de cibles à preuve d'audit disponible ;
algorithme/provider/coûts à qualifier, aucun
débit ou nombre de cibles traitées garantis. Ordre première persistance/ID-génération A10i104 A
validé le 9 octobre 2026. Aucun lot calculé/exécuté, Job,
purge, autorisation ou OpenSpec modifiés ici.
Recette : 1 000 cibles admissibles, préfixe réduit, première cible trop grande,
résultat maximal/partiel, borne inconnue, temps épuisé et aucune cible perdue.
A10i102 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i102

- **WHEN** un profil revendique le traitement A10i102 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--f2b88854e9

Source : `openspec/specs/pzt/spec.md`, ligne 10816. SHA-256 du bloc : `eea74deecce9f430d774873ba0cfdf6f120214998e56a42589c1781a6ea12935`.

~~~~text
### Requirement: Contrat A10i103 — Manifeste JSON produit selon JCS RFC 8785 sous schéma qualifié — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i103 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i103

JSON fermé A10i97 A, octets exacts/SHA-384 A10i98 A, limites A10i99/A10i101 A
conservés. Production du document indépendante de l'ordre des sources A10i104
et de la vérification A10i105 ; aucun ancien document réécrit.

| Choix validé | Sérialisation à la production | Conséquence |
| --- | --- | --- |
| A | JCS RFC 8785 sous schéma qualifié | Octets déterministes, codec/nombres/Unicode à qualifier |

Préconditions I-JSON/JCS et schéma Pixs conjointement validés, rejet des
doublons/Unicode invalide/nombres non admissibles. Champs int64/uint64 restent
chaînes décimales A10i97/A10i64, aucune coercition flottante ; autres nombres
limités à représentations exactes compatibles, encodage ECMAScript qualifié.
Tri des noms selon JCS et ordre des tableaux conservé, pas de tri des cibles
déduit du tri de clés. Chaînes sans normalisation Unicode implicite.
Sérialisation sans exigence JCS B non retenue comme profil alternatif ;
aucun reformatage d'original pour faire correspondre une empreinte.
Commun : conserver octets de production immuables, calculer/vérifier digest
sur ces octets. Document reçu incohérent/non conforme au profil refusé, pas de
« réparation » le transformant en ancien document autorisé. Vue lisible ou
pretty-print restent représentations distinctes sans empreinte d'original présumée.
Migration de profil/version explicite, audit et refs restent liés aux phases
et versions, nouvelle référence pour nouveaux octets. Taille 128 Kio et
budget 60 s comprennent production/analyse/vérification, aucune CPU/RAM garantie.
A validée pour production déterministe.
[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) définit JCS ; qualification
du codec/corpus/nombres exigée avant activation, pas de dépendance choisie.
Aucune signature, manifeste réel, conversion historique, purge ou OpenSpec modifiés.
Recette : ordre de clés, UTF-16/JCS, nombres/chaînes 64 bits, Unicode, ordre des
cibles, document non canonique et vérification sans reformatage permissif.
A10i103 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i103

- **WHEN** un profil revendique le traitement A10i103 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--f8e023f0af

Source : `openspec/specs/pzt/spec.md`, ligne 10863. SHA-256 du bloc : `b581722dc68d0baeb993dd9d7b62624f806c7b8c1c0a72259a223ceb14c99fc3`.

~~~~text
### Requirement: Contrat A10i104 — Sources de purge ordonnées par première persistance puis identité et génération — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i104 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i104

Préfixe contigu A10i102 A, checkpoint A10i88 A et rotation de classes A10i92 A
conservés. Ordre à l'intérieur d'une sélection admissible classe/périmètre,
distinct de l'ordre des travaux ou de la sérialisation des clés JSON.

| Choix validé | Ordre des sources admissibles | Conséquence |
| --- | --- | --- |
| A | Première persistance durable croissante puis identité immuable/génération | Ancienneté de stockage prioritaire dans sélection admissible |

Référence de première persistance protégée selon A10i82–A10i84, distincte
d'heure d'événement non fiable ; réingestion/restauration sans vieillissement
remis à zéro. Identité/génération exactes liées au manifeste, comparaison de
temps/type/encodage et départage stable qualifiés, pas d'ordre locale-dépendant.
Ordre fondé seulement sur identité/génération B non retenu ; départage
canonique des identités/générations reste qualifié.
Commun : sélection/coupure/curseur stables ou réconciliation explicite malgré
insertions/modifications concurrentes ; source nouvelle/réutilisée sans
suppression sous référence ancienne. Hold/rétention/mandat/bail réévalués,
ordre seul ne rend aucune source purgeable.
Préfixe est celui de l'ordre admis, cibles surdimensionnées sans saut silencieux ;
reste conservé pour traitement ultérieur, aucun checkpoint au-delà d'effet
confirmé. Fin de travail/budget sans ensemble complet prétendu, backlog et
couverture exposés. Dates incertaines ou sélection ambiguë bloquent effet
concerné, pas d'ancienneté inventée ou tri autorisant droits supplémentaires.
A validée pour prioriser l'ancienneté de stockage ;
plans/index/provider et coûts à qualifier, aucun index ou format ID imposés.
Stabilité par borne versionnée A10i106 A validée le 9 octobre 2026.
Aucun tri réel, requête SQL, source, purge ou OpenSpec modifiés ici.
Recette : égalité de dates, insertion concurrente, ID réutilisé, copie/restauration,
hold, première cible trop grande et aucune cible perdue ou droit élargi.
A10i104 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i104

- **WHEN** un profil revendique le traitement A10i104 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--c56e4f4144

Source : `openspec/specs/pzt/spec.md`, ligne 10910. SHA-256 du bloc : `a2ca3fe62003be2bed1daca362b290ad53ec7349e4748a7d178007b2a99d5645`.

~~~~text
### Requirement: Contrat A10i105 — Manifeste revalidé et empreinte recalculée à chaque usage — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i105 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i105

Octets originaux immuables/SHA-384/encodage A10i97/A10i98/A10i100 A conservés.
Vérification d'intégrité/structure du document, indépendante des contrôles
courants d'autorisation/source/rétention qui restent évalués à chaque usage.

| Choix validé | Vérification à lecture/export/usage probatoire | Conséquence |
| --- | --- | --- |
| A | Revalider structure/profil et recalculer digest sur octets à chaque usage | Sans cache de résultat, coûts répétés à qualifier |

Contenu original complet disponible, profil/version/taille/corrélation
et digest entier comparés à référence d'audit admissible ; document manquant/
altéré sans aperçu présenté comme preuve valide ou nouvel effet de purge.
Cache de vérification sur copie immuable B non retenu comme mode alternatif ;
chaque usage relit/valide les octets effectivement utilisés selon contrat.
Commun : aucune autorisation/révocation/validité de mandat héritées du résultat
cryptographique ; accès et audit individuel d'administration toujours requis.
Intégrité sans authenticité/commit/réalisation physique présumés, document
original et manifeste d'audit durable restent nécessaires sous leur rétention.
Pas de cache de preuve temporelle A10i51 ou droit de récupération racine modifiés.
Coûts inclus dans budget du travail lorsque usage participant, limites JSON/
128 Kio applicables, aucun contrôle ou erreur ignorés pour économiser CPU.
A validée pour simplicité de validation et invalidation ; coûts CPU/RAM/
latence à mesurer. Blocage ciblé sous confinement prouvé sinon global A10i108 A validé le 9 octobre 2026.
Aucune validation réelle, mémoire de cache, fichier/backend, purge ou OpenSpec
créés/modifiés. Recette : contenu altéré, référence changée, ancien profil,
copie immuable relue, reprise et absence de droit déduit d'une vérification passée.
A10i105 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i105

- **WHEN** un profil revendique le traitement A10i105 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--5bd7342997

Source : `openspec/specs/pzt/spec.md`, ligne 10953. SHA-256 du bloc : `6befe899b9207ead655762a46a9c16311e4b91bc88c4066d04614ae0337f7840`.

~~~~text
### Requirement: Contrat A10i106 — Sources du travail délimitées par borne stable versionnée et parcours par lots — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i106 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i106

Ordre première persistance/identité A10i104 A, préfixe A10i102 A et checkpoint
A10i88 A conservés. Délimitation des cibles du travail indépendante de rétention
du manifeste A10i107 et du traitement d'anomalie A10i108.

| Choix validé | Ensemble de sources du travail | Conséquence |
| --- | --- | --- |
| A | Borne stable versionnée, curseur par lots sous contrat provider qualifié | Parcours progressif, stabilité d'appartenance à prouver |

Contexte/classe/périmètre/politique et borne liés à travail/opération,
état de provider/générations admissibles ; borne et progression durables.
Timestamp ou identifiant maximal seuls sans stabilité d'appartenance présumée :
insertions tardives, dates corrigées, ID réutilisés, restore/rollback doivent
être traités par contrat qualifié. Nouvelle source hors ensemble sans entrée
silencieuse dans travail existant ; reste suivi dans plans/travaux futurs autorisés.
Liste complète matérialisée B non retenue comme stratégie alternative ;
borne/curseur sans preuve de stabilité restent inadmissibles.
Commun : candidat dans ensemble sans permission de purge acquise ; hold/
rétention/autorisation/bail et génération revalidés au lot/effet. Source nouvelle
à position réutilisée jamais traitée comme ancienne. Ordre/préfixe/checkpoint
conservés, coupure/curseur invalides => arrêt/réconciliation, pas de saut
d'éléments ou fin de travail inventée. Date d'éligibilité actuelle sans objectif
mobile illimité et sans budgets 60 s/2 tentatives réinitialisés par snapshot.
A validée pour sélection progressive sous preuve provider ; coûts/couverture
et mécanismes à qualifier, aucun snapshot PostgreSQL/
API/index/provider concret adopté. Profil ne prouvant stabilité refusé.
Autorité Django/Jobs persistants, PA sans SQL/secret/source de vérité parallèle.
Aucune liste/borne/snapshot réel, requête, purge ou OpenSpec créés/modifiés.
Recette : insertion concurrente/backdatée, ID réutilisé, borne restaurée, liste
incomplète, hold concurrent, reprise et aucune nouvelle cible sous ancien mandat.
A10i106 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i106

- **WHEN** un profil revendique le traitement A10i106 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--9b11df840f

Source : `openspec/specs/pzt/spec.md`, ligne 11000. SHA-256 du bloc : `b165990179e2e03858342f036daccd2bdc6533f29a1728654cd5a31435e54bdf`.

~~~~text
### Requirement: Contrat A10i107 — Conservation du manifeste liée aux durées et holds de l'audit — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i107 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i107

Manifeste durable A10i94 A et métadonnées terminales 14 jours A10i96 A conservés.
Choix de politique du manifeste, indépendant de sélection/réaction à anomalie ;
durées techniques logs/métriques/traces A10i82–A10i84 sans portée sur preuve d'audit.

| Choix validé | Politique de conservation du manifeste | Conséquence |
| --- | --- | --- |
| A | Durée/holds hérités de l'audit lié, prolongation tant que référence/reprise l'exige | Couple audit/manifeste conservé sous contraintes courantes |

Chaque phase/version immuable et référence d'audit suivies ; politique de
rétention applicable aux événements liés identifiée, contraintes combinées si
plusieurs références, plus protectrice conservée en cas de conflit non résolu.
Nouveau hold/référence/extension de rétention sans manifeste effacé selon
ancienne durée. Aucune durée numérique d'audit métier adoptée implicitement.
Politique propre indépendante B non retenue comme règle alternative ;
contraintes des audits/références liés et évolution courante conservées.
Commun : âge/échéance seuls sans purge ; autorisation/horloge/gouvernance/
dépendances/anti-résurrection et audit requis avant retrait. Métadonnées de Job
retirables sans suppression du manifeste encore nécessaire ; aucune conservation
de payload source/secret ajoutée, classification et accès déclarés séparément,
héritage de rétention sans ouverture automatique d'accès au contenu.
Manifeste manquant alors que preuve nécessaire => incident, référence marquée
incomplète, pas d'événement ou digest prétendant reconstruire octets perdus.
Stockage/provider/copies/sauvegardes et propagation des effacements à qualifier ;
aucune archive, signature ou matériel supplémentaire imposés par ce choix.
A validée pour cohérence de conservation ; volumes/durabilité à mesurer,
pas de conformité externe
ou conservation éternelle déduites. Audit métier et dossiers racine gardent
leurs politiques propres, aucun OpenSpec/historique/manifeste purgé/modifié.
Recette : audits de durées différentes, hold ajouté, Job âgé de 14 jours,
référence encore vivante, restauration et preuve jamais retirée prématurément.
A10i107 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i107

- **WHEN** un profil revendique le traitement A10i107 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--0559c964ff

Source : `openspec/specs/pzt/spec.md`, ligne 11048. SHA-256 du bloc : `17f961a2588baa2da3f54c074ce73e87ece370cc75c0dda6abf5b407753ef5b4`.

~~~~text
### Requirement: Contrat A10i108 — Anomalie de manifeste confinée sous preuve, blocage global sinon — option A validée le 9 octobre 2026

Le rôle chargé du traitement A10i108 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i108

Vérification à chaque usage A10i105 A, audit/échec fermé OpenSpec et exclusion
globale A10i90 A conservés. Portée des purges de télémétrie bloquées après
manifeste absent/altéré/incohérent, sans exception de sécurité ou réparation tacite.

| Choix validé | Portée du blocage de purge télémétrie | Conséquence |
| --- | --- | --- |
| A | Lot/périmètre concerné si confinement prouvé, global sinon | Autres purges seulement sous indépendance/exclusion/contrôles prouvés |

Périmètre exact, origine/cause et absence d'effet partagé qualifiés,
autorité/source d'audit/provider admissibles pour autres travaux. Même backend/
hôte ou simple hash valide sur autre document sans indépendance présumée.
Cause inconnue, compromission suspectée, audit/source de vérité/exclusion
partagés non fiables => blocage global, aucune isolation seulement déclarative.
Blocage global systématique B non retenu comme règle alternative ;
blocage global obligatoire dès confinement ou confiance non démontrés.
Commun : aucun nouvel effet dans portée bloquée, effets déjà engagés suivis/
réconciliés, preuve/checkpoint conservés sans effacement de l'incident.
Concurrence 1 et A10i90 toujours requis : poursuite ailleurs seulement après
libération/exclusion effectivement prouvées de l'acteur précédent, pas de
nouveau worker pendant purge ancienne encore active ou inconnue.
Diagnostic/alerte et audit individuel requis dès constat, sans délai 2 observations
A10i93 pour incident d'intégrité. Alerte sans secret/PII, copie valide éventuelle
sans réparation automatique réécrivant manifeste/audit ; provenance/références/
dernier état contrôlés lors de réconciliation autorisée. Compteurs/budgets/
mandats/holds sans remise à zéro ou élargissement sur reprise.
A validée pour confinement prouvé avec repli fermé global ; contrats/preuves
de confinement et procédures à qualifier avant
activation, aucune disponibilité ou résistance absolue à hôte compromis garanties.
Réarmement opérateur A10i109, original protégé A10i110 et alerte persistante
sans rappel A10i111 A validés le 9 octobre 2026. Aucune purge/notification/réparation/commande d'arrêt, droit
ou OpenSpec modifiés.
Recette : anomalie isolée/partagée, audit indisponible, ancien acteur vivant,
cause inconnue, reprise autorisée et aucun effet pendant état non admissible.
A10i108 A validé le 9 octobre 2026.

#### Scenario: Conformité du traitement A10i108

- **WHEN** un profil revendique le traitement A10i108 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

