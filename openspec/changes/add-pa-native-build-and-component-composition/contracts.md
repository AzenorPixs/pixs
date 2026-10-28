# Contrats techniques PostgreSQL PA01 — profils 1.0.0 et 1.1.0

Statut : spécification de frontière dans le périmètre adopté, réalisation en cours ; aucune API transportée, identité, autorisation, persistance, préparation PostgreSQL ou recette n'est livrée par la seule présence de ces définitions. Réalisation puis tests/validation selon l'instruction du développeur.

## Propriété et périmètre

Le catalogue adopté comporte exactement inspect_postgresql, prepare_postgresql et get_postgresql_result, version 1.0.0, sous gestion pixs.agent, seul mode system-daemon. Préparation Critique, lectures Protégé. Les références publiques des contrats sont pixs.agent.postgresql.<nom_opération>, version 1.0.0.

La répartition du plan a été explicitement adoptée : PA01/pixs.agent possède le contrat du plan technique et ses résultats durables, limités au service, au rôle et à la base PostgreSQL ; C08 conserve intention et confirmation opérateur et fournit une projection technique autorisée. Le plan privé applicatif R01 Core/Auth/tenant et les credentials MUST NOT être transmis à PA.

Tous échanges MUST emprunter PZT/A07, même localement. Cette représentation logique MUST conserver les corrélations et causalités complètes de l'enveloppe A07 existante : correlation_id lie ce contexte, sans supprimer ses références ni créer un format de transport concurrent. Le parcours initial MUST NOT forger un Subject ou CommandMetadata ordinaire avant PG.

## Requête fermée

Champs exacts : schema_version, catalog_operation, catalog_version, operation_id, idempotency_key, correlation_id, installation_ref, target_ref, mandate_ref, params.

schema_version et catalog_version valent 1.0.0. Les identifiants/références sont des chaînes UTF-8 non vides et sans contrôles ASCII, bornées par le profil explicite ; ils MUST NOT être interprétés comme URI, chemins, commandes, secrets ou autorisations par leur seule forme.

| catalog_operation | Champs params exacts | Sens |
| --- | --- | --- |
| inspect_postgresql | Aucun, objet vide | Inspection technique sous accès courant, sans mutation de la cible. |
| prepare_postgresql | plan_ref, plan_version, plan_digest | Résolution serveur du plan technique confirmé et vérification courante avant tout effet. |
| get_postgresql_result | operation_ref | Lecture actuellement autorisée du résultat technique durable de l'opération ciblée. |

plan_version est une version opaque du plan, distincte de la SemVer du catalogue. plan_digest est l'empreinte SHA256 en 64 hexadécimaux minuscules des octets du plan technique défini ci-dessous. Référence, version, empreinte et confirmation MUST être résolues et vérifiées par leurs propriétaires, pas crues depuis le corps client.

Acteur, exécutant effectivement vérifié, mode, politique/fraîcheur/validité/révocation, fencing et matériel MUST provenir des sources propriétaires courantes. Un champ client verified, actor, tenant_id, scope_id, SQL, shell, credential ou chemin exécutable supplémentaire MUST être refusé. L'ancien mandat consommé MUST NOT autoriser get_postgresql_result : une autorisation courante de lecture de l'opération et de la cible est requise.

## Plan technique fermé

Contrat logique pixs.agent.postgresql.technical_plan, schéma 1.0.0. Champs exacts : schema_version, catalog_operation, catalog_version, operation_id, idempotency_key, correlation_id, plan_ref, plan_version, installation_ref, target_ref, projection_ref, confirmation_ref, policy_ref, preconditions_ref, service_ref, role_ref, database_ref.

catalog_operation vaut prepare_postgresql et catalog_version 1.0.0. Les autres valeurs sont des références/identifiants UTF-8 non vides bornés ; elles MUST être résolues dans leur usage et périmètre propres. service_ref/role_ref/database_ref ne sont pas des noms SQL arbitraires fournis à l'exécutant : le profil serveur et ses sources vérifiées déterminent les seules ressources techniques autorisées.

La sérialisation versionnée est JSON UTF-8, clés fermées triées, séparateurs compacts, chaînes seulement et sans valeur flottante. L'empreinte est SHA256 de ces octets. Ceci définit le format de ce contrat fermé ; aucune qualification générale JCS n'est revendiquée. La signature et la confiance A07 restent distinctes. L'empreinte MUST NOT devenir une preuve d'autorisation, de confirmation, d'exécution ou de commit.

La projection C08 et la confirmation opérateur MUST rester distinctes du plan propriétaire PA et de son résultat. Un producteur/résolveur absent, plan non confirmé, cible/politique/préconditions modifiées ou contenu divergent MUST bloquer la préparation. Aucun producteur déployé n'est supposé par ces DTO.

## Résultat fermé et états distincts

Champs exacts : schema_version, catalog_operation, catalog_version, operation_id, correlation_id, installation_ref, target_ref, subject_operation_ref, phase, result_ref, observation_refs, plan_ref, plan_version, plan_digest, diagnostic_code.

| phase | Sens et contraintes |
| --- | --- |
| RECEIVED | Accusé de réception seul : ne prouve ni exécution, ni résultat, ni commit applicatif. |
| RUNNING | Exécution en cours, référence durable de suivi obligatoire. |
| SUCCEEDED | Résultat technique durable et références de postconditions réellement observées exigés ; pour préparation/lecture de préparation, liaison au plan obligatoire. |
| FAILED | Échec technique connu, référence durable et diagnostic obligatoire ; ne permet pas de traiter une issue inconnue comme rejouable. |
| IN_DOUBT | Effet ou résultat incertain, référence inspectable et diagnostic obligatoires ; réconciliation avant effet, jamais rejeu aveugle. |
| BLOCKED | Précondition, autorité, ressource ou source manquante/refusée ; diagnostic obligatoire, aucun effet déduit. |

Les phases sont techniques et MUST rester disjointes du mode PBO, du marqueur d'installation C08 et d'un commit Core/Auth. Les références observation_refs sont uniques et bornées ; leur forme n'est pas une preuve. RUNNING/SUCCEEDED/FAILED/IN_DOUBT exigent result_ref non vide. SUCCEEDED exige des références d'observation et, pour prepare_postgresql/get_postgresql_result, le triplet complet de plan. Un triplet partiel ou une empreinte invalide MUST être refusé.

get_postgresql_result exige subject_operation_ref. Le triplet de plan est soit absent, soit complet. diagnostic_code est un code stable en lettres ASCII majuscules, chiffres et underscore, commençant par une lettre ; aucun contenu brut reçu n'est renvoyé comme diagnostic.

L'état durable, les observations, la portée cible et les droits MUST être relus auprès des propriétaires courants. Un snapshot, un DTO, une référence ou une réponse perdue MUST NOT être présentés comme preuve de réussite. Avant effet/reprise, l'exécutant vérifie idempotence, mandat, plan/cible/politique courants et postconditions ; une concurrence incompatible ou effet inconnu bloque/réconcilie sans double effet.

## Bornes, parsing et implémentation

PayloadLimits fournit explicitement max_json_bytes, max_ref_bytes et max_observation_refs, entiers positifs stricts ; aucun défaut de production ou plafond numérique nouveau n'est introduit. Les fixtures de tests ne sélectionnent pas ces budgets. UTF-8, types exacts, champs/versions/opérations, doublons JSON, constantes non JSON, références et couplages d'état/plan MUST être contrôlés. Les DTO sont immuables, à repr masqué ; leurs invariants intrinsèques sont vérifiés même en construction directe, et les bornes à chaque encodage/décodage avec profil explicite.

Source de frontière : src/pixs/pa_native/postgresql_contracts.py. Tests : tests/unit/test_pa_native_postgresql_contracts.py, données synthétiques, préparés puis exécutés en seconde phase. Ces contrôles structurels MUST NOT être assimilés à vérification PKI/mandat, transport PZT, durabilité, driver SQL, effet PostgreSQL ou qualification d'environnement.

## Raccords encore requis

Producteur/projection/confirmation C08, plan/résultat durable PA, identités/mandats natifs et sources courantes, stockage/fencing/réconciliation, transport E3 et ses providers, backend SQL technique et profils réels restent à réaliser et qualifier. Les ports initiaux Z12 publiés sont documentaires ; leurs références publiques ne livrent ni TrustStore, poignée privée, identité terminale mTLS ni autorité courante. Aucun adapter permissif, premier PBO auto-approuvé, clé/CA ou privilège implicite n'est ajouté.


## Primitive Ed25519 du contexte privé — E4

L'adoption E4 de C08 retient la vérification de la signature opérateur Ed25519 par libcrypto OpenSSL 3. Le noyau natif TLS13Context fournit à cette fin verify_ed25519(public_key, signature, message, max_message_bytes), dans son propre OSSL_LIB_CTX, avec fournisseur default explicite et sans contexte OpenSSL global ou bibliothèque Python cryptographique supplémentaire.

Cette méthode est une primitive locale du code de confiance, jamais une opération du catalogue ou un endpoint. public_key et signature sont des octets bruts de longueur exacte 32 et 64 ; message est bytes et sa taille respecte max_message_bytes, entier positif strict fourni explicitement. Elle vérifie Ed25519 en une seule opération, sans préhachage applicatif, retourne seulement None en cas de validité cryptographique et lève un diagnostic stable masqué sinon. Les objets EVP sont privés, libérés même après échec, et aucun pointeur ou objet clé n'est retourné.

La primitive ne prouve ni la provenance/préautorisation de la clé publique, ni l'identité appelante, ni politique, révocation, fraîcheur, cible, confirmation, consommation durable ou permission. Le vrai propriétaire d'admission devra résoudre la clé courante protégée, valider tous ces éléments et construire les octets exacts E4 : préfixe ASCII PIXS:PA:POSTGRESQL:INITIAL:1.0.0, LF, document canonique. Une signature valable sous une clé fournie librement ne devient aucune autorisation.

Ce complément ne charge pas de clé privée ou de certificat TLS, n'utilise pas de clé TPM, ne signe pas et n'ouvre aucune connexion ; ready_for_transport reste False. Il ne remplace pas les ports Z12 courants ou le registre E4 encore à réaliser. Les nouvelles recettes sources utilisent seulement les clés publiques, messages et signatures publiés dans RFC 8032 §7.1 (vecteurs 1 et 2), jamais leurs graines ou clés privées ; aucune génération de clé ni test n'est exécuté pendant cette réalisation.


## Schéma propriétaire du mandat initial E4 — 1.0.0

Ce schéma précise l'adoption E4, revue en coordination avec C08, sans produire de permission ni livrer son transport. Les opérations wire restent exactement inspect_postgresql, prepare_postgresql et get_postgresql_result. Les DTO NativeRequest, TechnicalPlan et NativeResult antérieurs sont conservés.

### Enveloppe et document exacts

L'enveloppe JSON a exactement document et signature_b64. document est l'objet fermé ci-dessous. signature_b64 est une base64 standard canonique d'exactement 64 octets Ed25519 ; ni clé embarquée, autre algorithme, base64url, champ supplémentaire ou preuve R01 n'est admis.

Champs document obligatoires exacts :

schema_version, domain, mandate_ref, invocation_ref, operator_ref, operator_key_ref, policy_ref, policy_version, installation_ref, target_ref, caller_terminal_ref, executor_terminal_ref, pzt_relation_ref, catalog_operation, catalog_version, criticality, operation_id, idempotency_key, correlation_id, correlation_ids, causation_ids, issued_at, not_before, expires_at, request_digest, anchor_binding, claims.

schema_version et catalog_version valent 1.0.0 ; domain vaut PA_POSTGRESQL_INITIAL. La classe est exactement Protégé pour inspect_postgresql/get_postgresql_result et Critique pour prepare_postgresql. Elle est comparée au catalogue, jamais crue comme droit reçu.

Les références/identifiants et policy_version sont des chaînes opaques UTF-8 non vides sans contrôles ASCII, bornées par le profil protégé. Elles ne deviennent ni chemins, ni identité ou mandat vérifié. invocation_ref doit être rapprochée de l'invocation A07 réelle ; aucun Subject ou CommandMetadata métier n'est fabriqué avant PostgreSQL.

correlation_ids et causation_ids sont des tableaux de références ordonnés dont l'ordre et les doublons sont conservés. correlation_id doit figurer dans correlation_ids ; causation_ids peut être vide. Le vrai contexte PZT doit comparer ces tableaux complets à ses propres données vérifiées : le rapprochement de structure ne prouve pas l'origine de l'enveloppe.

issued_at, not_before et expires_at suivent exactement YYYY-MM-DDTHH:MM:SS.ffffffZ, UTC avec six décimales. Dates valides et issued_at <= not_before < expires_at sont exigés. Le codec ne lit pas l'horloge et ne prétend donc pas prouver la fraîcheur. Les contrôles temporels emploieront le propriétaire et les bornes qualifiées du profil effectif ; ni fenêtre R01 de 600 secondes ni plafond d'un autre usage n'est importé.

### Bindings et branches

Un ContentBinding possède exactement ref, version, sha256. ref/version sont opaques et bornées ; sha256 est une empreinte SHA-256 minuscule de 64 hexadécimaux. L'identité des contenus doit être vérifiée par leurs vrais propriétaires courants.

anchor_binding engage l'instantané public d'ancrage PA courant. Il ne contient ni secret ni valeur NV choisie implicitement. Son format matériel et son résolveur restent à arrêter : ce binding ne sélectionne pas NVextend, un index, un attribut, une autorisation de hiérarchie ou une politique de suppression. Un fichier ou une référence ne constitue jamais une lecture fraîche de TPM.

| Opération | Champs claims exacts |
| --- | --- |
| inspect_postgresql | Objet vide exact ; aucun effet de préparation. |
| prepare_postgresql | projection_binding, plan_binding, preconditions_binding, confirmation_binding, effects_digest. Les quatre bindings ont la forme ci-dessus. |
| get_postgresql_result | operation_ref ; vise le résultat durable d'une préparation et exige une autorité actuelle de lecture. |

projection_binding.version vaut schema_version 1.0.0 de la publication C08 immuable. plan_binding.version est plan_version opaque PA. preconditions_binding lie le manifeste PA observé et ses préconditions. confirmation_binding.ref correspond à TechnicalPlan.confirmation_ref préalloué et sa version au bundle propriétaire C08 effectivement supporté.

Le bundle de confirmation est produit après le plan et avant l'acte signé ; il ne contient ni acte, signature ni digest du mandat. Le plan ne porte que confirmation_ref, jamais le digest de ce futur bundle. La projection exclut toujours plan futur et confirmation. Le graphe d'empreintes reste ainsi acyclique.

request_digest est SHA-256 des seuls octets canoniques encode_request(NativeRequest), dont mandate_ref ne contient pas l'acte signé. Les références communes requête/mandat, versions/opération, cible/installation, idempotence et corrélation sont rapprochées exactement. En préparation, plan_ref/version/digest de la requête correspondent au plan_binding ; en lecture de résultat, operation_ref correspond au paramètre demandé.

effects_digest est SHA-256 du tableau allowed_effects canonique ordonné de la projection. La signature engage EN PLUS projection_binding et le manifeste/profils liés, donc le sens complet, pas seulement des noms d'effets ou trois références. Les profils et observations protégés sont revalidés avant effet. Pour PA01 sélectionné, un plan contenant RECREATE/DATABASE_DROP ou une branche Docker non sélectionnée MUST être refusé en entier avant tout effet, sans conversion silencieuse en CREATE.

### Octets, bornes et limites de preuve

Le document est sérialisé en JSON UTF-8 à champs fermés, clés triées, séparateurs compacts, sans coercition, nombre, doublon de clé ou constante non JSON. L'ordre des tableaux est conservé. Les octets signés sont exactement le préfixe ASCII PIXS:PA:POSTGRESQL:INITIAL:1.0.0 suivi de LF puis ces octets du document, sans préhachage applicatif. La signature ne porte pas sur l'enveloppe qui la contient. Ce format fermé ne revendique pas une qualification générale JCS.

MandateLimits compose PayloadLimits existant et max_correlation_refs/max_causation_refs, entiers positifs stricts. Les plafonds proviennent du profil protégé, jamais du message reçu ; aucun défaut de production n'est introduit. Enveloppe et octets signés sont bornés, les références aussi. Encodage/décodage, classes immuables à repr masqué et constructions directes appliquent leurs invariants.

Sources : extension de postgresql_contracts.py et de ses tests unitaires. mandate_signed_bytes, encode_signed_mandate/decode_signed_mandate et les rapprochements de requête/plan restent des opérations structurelles sans résolution, vérification de signature, IO ou droit. La primitive Ed25519 est distincte ; même sa réussite ne remplace pas provenance de clé, contexte natif/PZT, politique/révocation, UTC fiable, confirmation réelle, préconditions, journal/ancre, consommation, contrôle avant chaque effet ou retrait d'autorité. Aucun handler, registre NV, signer C08, test ou recette n'est livré par ce texte.


## Ancrage du journal technique PA — adoption D10–D12

Le profil adopté dans design.md est NV_Extend SHA-256 avec Cython/ESAPI, séparation de provisionnement/maintenance et autorisation d'usage par FD natif protégé/HMAC-SHA-256. Ce profil est propre au journal PA, distinct de PKI Z12. Les points matériels laissés ouverts dans la section E4 sont désormais décidés par D10–D12 ; leur réalisation et qualification restent à faire. Cette inscription définit les formes publiques et obligations de raccord ; aucun résolveur, index, descripteur, session TPM ou propriétaire de temps/autorité n'est réputé livré.

### Instantané public pixs.agent.postgresql.anchor_snapshot/v1

Schéma fermé 1.0.0. Champs exacts : object_type, schema_version, snapshot_ref, installation_ref, target_ref, registry_ref, registry_generation_ref, epoch, sequence, head_sha256, index_ref, index_name, nv_value_sha256, owner_ref, policy_ref, policy_version, observed_at.

object_type vaut pixs.agent.postgresql.anchor_snapshot/v1 ; schema_version vaut 1.0.0. Les références/versions sont des textes opaques UTF-8 non vides sans contrôles ASCII, bornés par la politique. epoch et sequence sont des entiers non négatifs stricts, jamais booléens, avec plafonds protégés explicites. head_sha256 et nv_value_sha256 sont 64 hexadécimaux minuscules ; ce dernier champ désigne la valeur d'extension SHA-256 courante relue, pas le digest d'une chaîne texte ni une valeur fournie par le demandeur. index_name est le Name TPM canonique SHA-256, encodé en hexadécimal minuscule avec préfixe d'algorithme 000b suivi de 64 hexadécimaux ; il est rapproché de la zone publique et de la configuration protégée réelles. index_ref reste opaque, sans numéro d'index implicite. observed_at suit la forme UTC à six décimales déjà définie pour E4, depuis une source compétente réellement vérifiée.

L'instantané engage le journal protégé et son ancre après lecture actuelle authentifiée ; ni observation mémoire ni copie d'un ancien fichier n'est suffisante. L'installation, la cible native/TPM, la génération, l'époque, le contenu du journal, la politique courante, le Name et la valeur NV doivent être recoupés. Le Name n'identifie pas à lui seul le TPM. L'observation n'accorde pas un droit durable jusqu'à une échéance : révocation, retrait, changement de politique/cible/époque, perte d'accès ou divergence invalident son utilisation courante.

anchor_binding.ref correspond à snapshot_ref, anchor_binding.version à 1.0.0, anchor_binding.sha256 à SHA-256 des octets JSON UTF-8 canoniques de cet objet : clés triées, séparateurs compacts, types stricts, tableaux absents, entiers décimaux non négatifs, ni flottant/coercition/doublon/champ étranger/constante non JSON. L'objet public ne contient aucun authValue, HMAC de session, secret de hiérarchie, FD, chemin de credential, clé de maintenance, preuve R01 ou booléen verified. Cet engagement structurel doit être vérifié par le propriétaire PA courant et ne remplace jamais sa lecture TPM.

### Composition et refus

Le lanceur/composition native réellement authentifiés fournissent le FD par capacité locale, hors entrées HTTP/JSON/PZT et hors chaîne/argument de configuration libre ; le secret est lu et confiné en mémoire native, avec refus des formes, origines et durées de vie non conformes. Le propriétaire de garde/remise reste à livrer. Le natif rapproche la configuration publique protégée de l'index et vérifie les échanges HMAC réels ; la résolution structurelle de index_ref ne crée aucune autorité. Les commandes de provisionnement, suppression, Clear et gestion de hiérarchie sont absentes du contrat d'exécution PA.

L'autorité de maintenance matérielle P-256 est indépendante des clés CA/TLS/opérateur et des droits d'usage. Ses usages et sa récupération après reset, la politique de suppression et la protection de la plateforme doivent être prouvés par le plan de qualification ; aucun mécanisme de suppression par simple détention de l'autorisation d'usage. Une configuration incompatible, un état non initialisé, une autorité/heure/politique invérifiable, une mauvaise cible/installation/génération/Name/zone publique, un journal absent/divergent/restauré ou une extension non réconciliée ferment l'usage. La disponibilité de PostgreSQL ne réactive aucune autorité initiale retirée.

Chaque transition du registre porte installation/cible/époque/génération, séquence, précédent, contenu/digest, mandats/corrélations/causalités et état précis. L'algorithme de persistance et les états incertains doivent distinguer journal local et valeur TPM, sans atomicité fictive avec SQL/service. L'absence de preuve requise interdit un effet privilégié, la consommation d'un mandat ou un résultat SUCCEEDED. Une perte de réponse d'extension doit être traitée par observation actuelle et quiescence réelle, jamais par nouvelle extension supposée idempotente.

La recette matérielle exigera cible et index exacts, autorisations distinctes, bornes, preuves avant/après, pannes/reprises, concurrence, restauration/clonage, interdictions de reset/suppression par signataires/runtime et nettoyage autorisé. Aucun essai matériel ni écriture NV actuelle n'est autorisé par les formes documentaires ci-dessus. Les tests de codec ou les mocks ne qualifieront ni D10–D12 ni la résistance matérielle à la restauration.


## Lecteur natif du FD d'autorisation NV — D12, ABI privée v1

Réalisation prévue : src/pixs/pa_native/nv_secret.pyx, sans API Python de lecture, handle, capsule ou valeur de secret. Cython produit les symboles C et leur header ; aucun C généré n'est modifié. Le raccord est privé au natif de pixs-pa-system/system-daemon et ne constitue ni admission, ni propriétaire ou preuve d'origine du descripteur.

pa01_nv_secret_read32(int *fd_inout, uint8_t *output, size_t output_size, int timeout_ms) retourne un uint32_t. output_size vaut exactement 32. timeout_ms est un entier C positif fourni explicitement par le profil, sans défaut. Le caller natif vérifie positivement autorité/mandat/politique et la garde/remise réelle du FD, puis garantit propriété unique et durée de vie des pointeurs/descripteur. Aucun paramètre HTTP/JSON/PZT ne choisit ce FD ou ce tampon.

Argument ou horloge invalide avant transfert : le FD reste au caller. Dès transfert, *fd_inout vaut -1 et le lecteur ferme le FD dans chaque issue. Le FD est au moins 3, en lecture seule, régulier ou pipe ; pas de chemin ouvert, terminal, socket ou périphérique. Un fichier régulier doit commencer à l'offset zéro, mesurer exactement 32 octets et rester stable sur le FD, sans lien physique non maîtrisé. Ces formes ne prouvent pas le propriétaire ou l'absence d'autres copies du secret.

La lecture non bloquante et poll emploient CLOCK_MONOTONIC et la borne explicite jusqu'à exactement 32 octets ET fin vérifiée. Trente-deux octets sans EOF ne valent pas succès. Le FD est marqué CLOEXEC ; aucune valeur ou erreur brute n'est journalisée. OPENSSL_cleanse nettoie nos tampons en cas d'échec ; seul statut zéro laisse les 32 octets dans le tampon C du vrai consommateur natif, qui doit ensuite les confiner et les libérer. Aucune isolation OS ou gestion mémoire interne ESAPI n'est prouvée par ce lecteur.

Statut bas 16 bits : 0 OK, 1 ARGUMENT, 2 CLOCK, 3 FD, 4 SHORT, 5 EXTRA, 6 TIMEOUT, 7 IO, 8 CHANGED. Le bit16 CLOSE_FAILED préserve une erreur de fermeture sans perdre la cause principale ; aucun retry de close susceptible de fermer un FD réutilisé sous Linux. pa01_nv_secret_diagnostic(uint32_t) ne rend qu'un diagnostic C constant sans entrée reçue. Des arguments invalides de pointeur/taille ne permettent pas d'affirmer un nettoyage de mémoire inconnue.

Les sources de tests natives utilisent exclusivement des fixtures publiques de pipe/fichier local, avec un conducteur ctypes de test, jamais un secret hôte ou une recette TPM. Elles exigent l'extension compilée sélectionnée, ne sautent pas une dépendance absente et ne prouvent ni garde réelle, rôle/admission, HMAC, journal, NV ou intégration. Header généré, ABI, graphe de compilation, dépendances et confinement du vrai appelant restent à inventorier et qualifier en seconde phase. Aucun test ni lecture de credential actuel n'est déclenché par cette conception.


## En-têtes C générés et ordre de construction — D9/D12

ModuleSource, métadonnée privée de construction et non message réseau ou manifest PBO/TOML, ajoute generated_headers: tuple[str, ...] = (). Les cinq arguments existants sont conservés. Le tuple est strict, ordonné et sans doublons ; les seuls noms possibles sont module_name.h et module_name_api.h. Les collisions entre modules sont refusées avant tout outil. Pour nv_secret.pyx/nv_anchor.pyx, le mécanisme _api.h et ses capsules Python sont refusés ; leur interface reste C privée. Le tuple vide exige l'absence de header généré, pas une découverte autorisée implicitement.

Toutes les sources sont d'abord cythonisées, puis toutes sont compilées par le compilateur C épinglé. Après chaque génération, seul l'ensemble des headers déjà produits plus ceux déclarés pour le module courant est admis ; disparition, altération, création prématurée/étrangère ou collision ferment le build. Aucun C/header généré n'est édité manuellement. La racine de la sortie neuve de build est le seul include généré ajouté aux includes explicites ; aucune ancienne construction, plugin ou source .pxd/.pxi nouvelle n'est introduite par ce raccord.

Chaque module du build-report conserve generated_headers, liste de dictionnaires fermés path/sha256/size. path est ici le basename canonique relatif à ce seul répertoire de build, pas un chemin libre. SHA-256, taille positive et octets réels sont recoupés ; fichiers spéciaux, symlinks et liens physiques non maîtrisés sont refusés. Les inventaires sont limités aux .h à la racine de ce répertoire protégé, jamais au dépôt/hôte entier. Les pins sont contrôlés avant/après compilation et avant succès.

Le linker rapproche à nouveau ces fichiers et leur inventaire dans le même répertoire que les objets/rapport de construction, avant liaison puis avant succès. Un ancien rapport sans generated_headers équivaut à une liste vide et n'autorise aucun .h supplémentaire. Les autres contrôles source/C/.d/.o, outils, rôles, catalogue, runtime et lanceur sont conservés ; ces traces locales ne deviennent ni signature ni autorité.

Les unités préparées couvrent formes/collisions/API privée, anciens rapports et fichiers réellement altérés/manquants/étrangers/alias. La recette native prépare un consommateur nommé avant son fournisseur C, et le refus d'un vrai header non déclaré avant toute compilation C. Il s'agit de sources de tests non exécutées ; compilation, ABI, symboles, comportement, fermeture et reproductibilité restent à qualifier. Aucun résultat fonctionnel, propriétaire de confiance ou accès matériel n'est livré par cet enregistrement.

Références de conception : [Cython 3.3.0, déclarations publiques](https://cython.readthedocs.io/en/latest/src/userguide/external_C_code.html#public-declarations) et [implémentation 3.3.0 de génération des headers](https://raw.githubusercontent.com/cython/cython/3.3.0/Cython/Compiler/ModuleNode.py).


## Lecteur de zone publique NV — tranche ESAPI privée D10–D12

Réalisation : src/pixs/pa_native/nv_anchor.pyx, dans le seul graphe natif pixs-pa-system. L'interface C opaque utilise les symboles pa01_nv_public_new/start/step/status/close et le seul header généré nv_anchor.h ; aucune fonction Python, capsule ou _api.h. Les contextes ESYS_CONTEXT et OSSL_LIB_CTX sont prêtés exclusivement par leur propriétaire natif réel, déjà initialisés et qualifiés ; ce code n'initialise aucun TCTI/provider et n'ouvre aucun chemin/périphérique. Les void* de l'ABI sont des capacités C privées, jamais des valeurs reçues via Python, HTTP/JSON/PZT. Le propriétaire garantit leurs types, durée de vie, exclusivité, absence d'alias et un contexte sans commande pendante.

new(void **state_out, void *esys_context, void *crypto_context, uint32_t index, uint32_t attributes, const uint8_t *policy, size_t policy_size, const uint8_t *name, size_t name_size, uint64_t deadline_ns) alloue un état opaque seulement si *state_out est NULL et les arguments valides. L'index explicite est dans l'espace NV TPM 0x01000000–0x01ffffff, sans choix d'index par défaut. Les attentes protégées sont copiées : attributs exacts, authPolicy SHA-256 de 32 octets, Name canonique de 34 octets commençant par 000b. Le type est NV_Extend (TPM2_NT_EXTEND décalé de quatre bits), avec PLATFORMCREATE, POLICY_DELETE, AUTHREAD, AUTHWRITE et WRITTEN. CLEAR_STCLEAR, ORDERLY et les états READLOCKED/WRITELOCKED sont refusés pour cette tranche persistante et utilisable. Les attributs ne prouvent pas la séparation effective de maintenance D11.

start(void *state) appelle Esys_SetTimeout(0) puis une seule fois Esys_TR_FromTPMPublic_Async ; aucun index TPM brut n'est converti en ESYS_TR. step(void *state) termine cet import par Finish, puis lance NV_ReadPublic_Async lors d'un appel distinct seulement si l'échéance reste valide. Les Finish utilisent le timeout nul. Le demandeur natif ordonne les appels et leur cadence, sans boucle d'attente interne ni appel concurrent. La zone publique réelle doit correspondre à l'index, SHA-256, aux attributs exacts, à la policy, à dataSize 32 et à sa taille canonique. Le Name reçu correspond à l'attente et à 000b || SHA256(TPMS_NV_PUBLIC canonique), calculé par libcrypto dans le contexte privé avec provider=default. Ce fournisseur de digest public est celui déjà requis par le contexte OpenSSL ; aucun fournisseur de clé ou repli n'est sélectionné.

deadline_ns est une échéance CLOCK_MONOTONIC explicite future, sans défaut et sans valeur UTC. Les TRY_AGAIN des couches logicielles TSS prises en charge préservent la commande et autorisent seulement sa continuation Finish. Une expiration ou perte d'horloge pendant une commande est conservée : les Finish peuvent constater sa fin, mais aucune nouvelle commande ou réussite tardive n'est admise. Une autre erreur ESAPI/transport dont la quiescence n'est pas prouvée met l'état en quarantaine IN_DOUBT ; aucun rejeu, nouvelle commande, fermeture de contexte ou effacement de cet état par ce lecteur. La récupération/quiescence du vrai propriétaire reste à livrer, elle n'est pas remplacée par un booléen.

status(void *state, uint32_t *last_tss_rc) donne uniquement le statut local et, si demandé, le code TSS numérique au propriétaire C. Ce résultat peut être historique ; il ne publie aucune observation d'ancrage courante. close(void **state_inout) refuse une commande pendante ou une quarantaine. Aux frontières connues, il ferme la seule métadonnée importée par Esys_TR_Close, vérifie le retour, puis libère et met le pointeur à NULL. Un échec de fermeture conserve l'état et le handle pour diagnostic/reprise contrôlée. Les buffers de réponse sont libérés par Esys_Free ; ESYS/OSSL restent possédés par l'appelant. Aucun FlushContext, Finalize, secret, session HMAC, lecture authentifiée de valeur NV, Extend, provisionnement, suppression, Clear ou effet PostgreSQL n'est présent dans cette tranche.

Statuts uint32_t : 0 OK, 1 ARGUMENT, 2 MEMORY, 3 CLOCK, 4 STATE, 5 PENDING, 6 EXPIRED (fin connue), 7 VERIFY, 8 TSS_ERROR avant émission, 9 IN_DOUBT, 10 CLEANUP_ERROR. Le succès porte seulement sur une comparaison de métadonnées publiques : il ne prouve ni TPM/cible, garde/remise FD, maintenance, identité initiale, mandat, UTC, HMAC, journal ou ancre durable et ne produit aucun AnchorSnapshot. Les tests sources utiliseront des réponses publiques et un conducteur ESAPI simulé explicitement séparé ; les qualifications réelles restent à exécuter en seconde phase sur environnements autorisés.


## Lecture NV authentifiée et nettoyage privé — D10–D12

Cette seconde tranche étend le même nv_anchor.pyx et conserve les interfaces de lecture publique. Elle reste C privée à pixs-pa-system : aucun authValue, FD, pointeur de contexte, capsule ou fonction de lecture de secret n'est exposé par Python/HTTP/PZT. Le module fermé nv_secret est initialisé avant ses appels C ; nv_secret.h et nv_anchor.h, leurs modules et leurs objets sont déclarés dans le graphe de build. Ces imports n'ouvrent aucun credential, TCTI ou TPM. Aucun autre binaire, index, provider de clé ou chemin par défaut n'est ajouté.

pa01_nv_auth_start(void *state, int *fd_inout, int fd_timeout_ms, uint64_t auth_deadline_ns) exige une lecture publique COMPLETE dans le même état, sans session ou valeur préalable. L'échéance d'authentification est explicite, future et au plus égale à l'échéance de l'opération publique ; elle ne renouvelle pas une observation historique. Le propriétaire natif réel doit auparavant vérifier contexte, cible, politique et provenance/garde/remise du FD. L'ABI du lecteur ne fournit aucune de ces preuves.

Le budget du FD est le minimum du budget positif fourni et du reste monotone arrondi vers le bas en millisecondes ; moins d'une milliseconde restante refuse avant transfert. pa01_nv_secret_read32 lit les seuls 32 octets natifs et vérifie EOF selon son contrat. Les retours FD restent séparés des codes TSS. Les buffers locaux sont nettoyés après lecture et après Esys_TR_SetAuth sur l'OBJET NV. L'état conserve l'obligation d'effacer cet authValue à une frontière sûre, y compris après échec local ; aucun secret n'est retourné.

Le nonce de session de 32 octets utilise RAND_bytes_ex dans l'OSSL_LIB_CTX privé emprunté, puis l'échéance est recontrôlée avant émission. Le vrai StartAuthSession Async/Finish emploie bind = handle ESYS de notre index, tpmKey = NONE, HMAC/SHA-256 et un TPMT_SYM_DEF réel d'algorithme NULL. Après création réussie, la session est enregistrée comme possédée avant tout autre contrôle. Esys_TRSess_SetAttributes efface CONTINUESESSION ; NV_Read_Async utilise cette session dans shandle1, les deux autres étant NONE, pour taille 32/offset 0. Il n'existe aucune session mot de passe ou autorisation de hiérarchie.

pa01_nv_auth_step(void *state) poursuit uniquement le Finish correspondant ou l'étape suivante autorisée dans le budget courant. La réussite de NV_Read_Finish doit provenir de la vraie vérification de réponse ESAPI, pas d'un indicateur client. Les buffers de réponse sont libérés ; une taille différente de 32 ne produit pas de valeur. Une réponse validée pour CONTINUESESSION=0 consomme la session TPM. ESAPI 4.1.3 conserve sa métadonnée après NV_Read : elle est fermée LOCALement par TR_Close, sans Flush d'une session consommée, avec conservation du handle si cette fermeture échoue. Cette distinction est requise avant toute réussite locale.

Une expiration/perte d'horloge est conservée ; les Finish après échéance servent à réconcilier, jamais à obtenir un succès tardif ou à émettre la commande suivante. Une autre erreur d'émission ou de réponse inconcluante conserve le contexte, la session et les obligations de mémoire en QUARANTINED/IN_DOUBT, sans rejeu, Finalize ou Flush aveugle. La récupération du vrai propriétaire reste requise. Les contrôles avant/après ne prouvent pas une borne de latence interne des syscalls, RNG, TCTI ou bibliothèques ; cette qualification de runtime reste distincte.

pa01_nv_auth_status(void *state, uint32_t *last_tss_rc, uint32_t *fd_status_out) distingue ces diagnostics. pa01_nv_auth_value(void *state, uint8_t *output, size_t output_size) n'accepte qu'un tampon C de 32 octets ; il le nettoie avant retour en échec lorsque sa forme est valide. Seule la valeur NV publique de la lecture authentifiée fraîche peut être copiée, jamais l'authValue. step/status/value invalident et nettoient la valeur à expiration ou perte d'horloge. Aucune cible, époque, génération, heure UTC, observation courante complète ou AnchorSnapshot n'est fabriqué par ce résultat.

Si une session créée n'a pas été consommée et que la fin de commande est prouvée, pa01_nv_cleanup_start(void *state, uint64_t cleanup_deadline_ns) autorise seulement le FlushContext_Async de cette session possédée. Sa borne distincte explicite ne réautorise aucune lecture ou action privilégiée. pa01_nv_cleanup_step(void *state) utilise Finish timeout zéro, y compris après échéance pour constater sa fin ; une issue inconnue conserve la quarantaine. Dans ESAPI 4.1.3, FlushContext_Finish réussi ferme aussi sa métadonnée ESYS : aucun second TR_Close de ce handle. Une fin tardive permet la clôture locale tout en rapportant l'expiration/perte d'horloge ; l'échec primaire reste conservé. pa01_nv_cleanup_status(void *state, uint32_t *last_cleanup_rc) rend ce statut séparément.

pa01_nv_public_close conserve sa clôture locale à frontières connues. Il refuse session vivante, commande pendante ou quarantaine ; il peut réessayer la seule fermeture locale d'une métadonnée de session déjà consommée. Il efface l'autorisation de l'objet NV via TR_SetAuth vide avant TR_Close et conserve les ressources/diagnostics si un retour échoue. Les allocations internes de TSS/OpenSSL et leur zéroisation ne sont pas réputées confinées par le seul nettoyage de nos buffers. Les statuts précédents 0–10 sont conservés ; les fonctions d'authentification ajoutent 11 FD_ERROR et 12 CRYPTO_ERROR.

Le libctx emprunté ne configure pas automatiquement le backend crypto interne ESAPI. Le producteur de contexte, la bibliothèque réellement livrée, ses callbacks/configurations éventuels, ses journaux, ressources et durées de vie doivent être qualifiés avant de recevoir un authValue. La source TSS 4.1.3 contient une trace de clé dans son chemin HMAC ; l'absence d'exposition de secrets doit donc être prouvée pour la pile exacte retenue, sans présumer le niveau de journalisation du binaire installé. Aucune installation, configuration ou utilisation de secret sur l'hôte actuel n'est déclenchée ici.

La recette source utilise un artefact de TEST contenant les deux modules Cython initialisés et le conducteur ESAPI simulé, les vrais headers TSS, des fixtures publiques et des wrappers de test explicites pour horloge/RNG/observation du budget FD. Elle ne lie ni ESAPI réel ni TCTI et ne qualifie pas le HMAC/TPM, le propriétaire initial, la garde FD ou la résistance matérielle. Sources et ABI restent NON COMPILÉES/NON TESTÉES jusqu'à la seconde phase ; aucune tâche n'est cochée et aucun AnchorSnapshot, journal durable ou effet PostgreSQL n'est livré par cette tranche.

Références de conception : [NV_Read ESAPI 4.1.3](https://raw.githubusercontent.com/tpm2-software/tpm2-tss/4.1.3/src/tss2-esys/api/Esys_NV_Read.c), [vérification de réponse](https://raw.githubusercontent.com/tpm2-software/tpm2-tss/4.1.3/src/tss2-esys/esys_iutil.c), [FlushContext](https://raw.githubusercontent.com/tpm2-software/tpm2-tss/4.1.3/src/tss2-esys/api/Esys_FlushContext.c) et [backend OpenSSL interne](https://raw.githubusercontent.com/tpm2-software/tpm2-tss/4.1.3/src/tss2-esys/esys_crypto_ossl.c).


## Transition de journal — codec structurel D10, version 1.0.0

Cette extension de postgresql_contracts.py définit seulement la représentation des données. Aucun objet décodé, état déclaré ou digest calculé ne constitue une intention durable, un verrou/fence, une transition ancrée, un retrait d'autorité ou une permission. Ces faits restent à produire et recouper par les propriétaires natifs réels, avec IO et observations authentifiées. Aucun nouveau module runtime ou import frère n'est ajouté.

JournalTransition possède exactement les champs suivants : object_type, schema_version, transition_ref, installation_ref, target_ref, registry_ref, registry_generation_ref, epoch, sequence, previous_head_sha256, previous_nv_value_sha256, state, operation_ref, mandate_binding, content_binding, correlation_refs, causation_refs. object_type vaut pixs.agent.postgresql.journal_transition/v1, schema_version vaut 1.0.0. mandate_binding et content_binding réutilisent ContentBinding(ref, version, sha256) ; aucun payload arbitraire, authValue ou credential n'est ajouté. INTENT, OBSERVED, RESULT et RETIRED sont les seuls états de représentation ; leur signification et leur emploi sont vérifiés par le véritable propriétaire sémantique. RETIRED dans un DTO ne retire aucune autorité et n'autorise aucune voie initiale à se retirer comme propriétaire ordinaire.

Les références et versions sont des textes UTF-8 non vides, sans contrôles ASCII, soumis aux plafonds protégés. Les digests sont 64 hexadécimaux minuscules. epoch et sequence sont des uint64 non négatifs stricts, jamais booléens. JournalLimits compose PayloadLimits avec max_epoch/max_sequence explicites dans ce domaine et max_correlation_refs/max_causation_refs strictement positifs, sans valeur de production par défaut. Les traces sont des tuples immuables ; ordre et doublons A07 sont préservés. Les constructions directes, encodages et décodages appliquent leurs invariants et bornes lorsqu'un profil est fourni.

Le head candidat est SHA-256 des octets ASCII PIXS:PA:POSTGRESQL:JOURNAL:1.0.0 suivis d'un LF puis du JSON UTF-8 canonique de ces seuls champs : clés triées, séparateurs compacts, champs/types fermés, sans doublon de clé, flottant, constante non JSON ou coercition. previous_head_sha256 figure une seule fois dans cette transition ; aucun head futur ou confirmation n'est un champ de son propre engagement. previous_nv_value_sha256 désigne les 32 octets de valeur NV antérieure, pas le hash du texte hexadécimal. La valeur NV attendue est SHA256(ancienne_valeur32 || head_candidat32). Cette dérivation ne lit aucun TPM et ne prouve pas que l'ancienne valeur est actuelle ni que l'extension a eu lieu.

Les confirmations locales d'écriture/ancrage sont des reçus de cette transition, distincts des nouvelles transitions sémantiques ; elles ne déclenchent pas une récursion infinie d'engagements. Un fsync local ne prouve pas une tête NV. Le mandat E4 reste lié à son instantané initial : sa progression propre doit être réconciliée par le registre réel selon le contrat existant, sans tolérance à une divergence, extension d'autorité/durée ou réutilisation aveugle d'une signature. Le codec ne réalise pas cette réconciliation.

Les sources de tests sont préparées séparément pour schémas, types, bornes, traces, canonicité et dérivations de digest. Elles n'exercent ni FD, stockage, session, NV_Extend, autorité, horloge ou effet PostgreSQL et ne qualifient aucun de ces mécanismes. Aucune syntaxe, unité, construction ou validation produit n'est exécutée en phase 1.


## Stockage POSIX du journal PA — tranche native privée, sans NV_Extend

Source : src/pixs/pa_native/nv_journal.pyx. Le module et son header généré nv_journal.h sont limités à pixs-pa-system par le générateur, le builder et le linker ; _api.h, capsule et fonctions Python de production sont refusés. Cette tranche produit uniquement des observations et reçus LOCAUX d'IO. Aucun reçu local n'est le head sémantique JournalTransition, une valeur NV, une ancre courante, une admission ou une capacité d'extension.

Le vrai propriétaire natif doit fournir un répertoire persistant préexistant, distinct du runtime de distribution, un basename ASCII fermé, UID attendu égal à geteuid, les couples device/inode attendus du répertoire ET du fichier, les plafonds explicites max_bytes/max_record/max_records, une échéance monotone future et un OSSL_LIB_CTX privé vivant/exclusif déjà qualifié. Aucun chemin de production par défaut, profil implicitement découvert ou FD reçu par Python/HTTP/PZT n'est ajouté. Provenance et protection du profil restent à livrer. Le propriétaire garantit absence d'alias, de concurrence et de fork ; le contrôle PID refuse les appels hérités, mais ne prouve pas à lui seul l'absence de descripteurs hérités.

pa01_journal_open alloue un état opaque après duplication CLOEXEC du seul FD répertoire prêté. Le répertoire est contrôlé avant openat ; le basename est copié et terminé, 1–255 octets, premier caractère lettre/chiffre/_/-, caractères suivants identiques ou point, sans slash ni NUL, avec refus de « . » et « .. ». Le fichier nommé est contrôlé avant ouverture, puis le fichier ouvert et son nom sont rapprochés avant/après les IO : types répertoire/fichier régulier, UID, modes exacts 0700/0600 sans bits spéciaux, inode/device attendus et nlink fichier égal à 1. Le profil et le répertoire doivent exclure les écrivains adverses ; ces contrôles et flock restent des mécanismes POSIX coopératifs, pas une frontière contre tout code du même compte ou une autorité de restauration.

L'ouverture utilise O_RDWR|O_APPEND|O_NOFOLLOW|O_CLOEXEC|O_NONBLOCK, sans O_CREAT ni troncature. flock exclusif non bloquant est conservé jusqu'à clôture. L'absence, le vide, une erreur, un fichier spécial, un cadrage incomplet ou des données supplémentaires incohérentes ferment l'ouverture sans création, réparation, reset ou adoption automatique d'une nouvelle base. max_bytes est borné au domaine off_t positif 64 bits retenu ; les tailles, additions, allocations et compteurs sont contrôlés avant IO. Une échéance CLOCK_MONOTONIC n'est ni une date UTC ni un renouvellement d'autorité.

Format local 1.0.0 : préfixe ASCII PIXS:PA:JOURNAL:1.0.0 suivi de LF (22 octets), puis au moins un enregistrement. Chaque frame contient longueur uint32 big-endian strictement positive, payload public borné puis reçu de 32 octets. Le reçu est SHA256(ASCII PIXS:PA:JOURNAL:RECORD:1.0.0 + LF || reçu précédent32 || longueur4 || payload). Le premier reçu précédent est zéro32 uniquement pour vérifier une première frame PRÉEXISTANTE, jamais pour créer une genèse. Le digest est calculé par EVP_Q_digest dans le libctx prêté, provider=default explicite. Le payload est opaque ici ; sa canonicité, son schéma JournalTransition et sa liaison au registre/mandat doivent être réellement vérifiés par le futur propriétaire sémantique. Aucun octet réseau libre ou secret ne devient admis par ce cadrage.

open vérifie l'intégralité bornée du fichier, sans prétendre prouver un fsync antérieur ou un ancrage. pa01_journal_snapshot relit et vérifie toute la chaîne, les identités/protections et la taille, puis exige le même reçu/taille/compte que l'état local. Il retourne seulement leurs copies. pa01_journal_record_copy relit également toute la chaîne et copie le payload et le reçu de l'enregistrement sélectionné, pas un pointeur ni une empreinte du dernier enregistrement présentée comme celle du premier. Une modification externe, même une nouvelle chaîne valide, n'est jamais adoptée silencieusement par un état déjà ouvert. Ces relectures n'assurent ni anti-rollback ni réconciliation TPM.

pa01_journal_append compare le reçu et la taille attendus à l'état réellement relu sous verrou. Il copie et cadre un seul payload public, écrit les octets avec continuation bornée des seuls appels partiels/EINTR puis effectue fsync du fichier ET du répertoire. La chaîne entière et les identités sont relues, avec vérification de taille, compte, reçu et échéance avant toute copie positive. Un succès signifie seulement que ces IO locales ont retourné le succès dans le budget observé. Les syscalls/FS/RNG/bibliothèques ne sont pas réputés avoir une latence dure bornée par les seuls contrôles avant/après.

Dès la première tentative d'écriture, toute panne, écriture nulle, délai, erreur fsync ou divergence laisse l'état IN_DOUBT et interdit nouvel append, snapshot ou reçu positif. Le fichier, y compris une frame partielle ou complète non confirmée localement, est conservé sans troncature ni rejeu automatique. Les boucles vérifient l'échéance à chaque continuation ; l'état courant et le diagnostic primaire sont distincts. Les erreurs antérieures à écriture ne deviennent pas un succès de durabilité.

pa01_journal_status retourne seulement le diagnostic local, invalide l'état à expiration et n'est aucune observation d'ancre. pa01_journal_close, à frontière synchrone connue, libère seulement les FD/verrou/mémoire propres ; le FD répertoire prêté et le libctx restent possédés par l'appelant. Il peut libérer un état IN_DOUBT sans réparer le disque et conserve ce statut au retour. cleanup_out rapporte séparément les erreurs de déverrouillage/fermeture. Sous Linux un close ayant retourné une erreur n'est pas rejoué sur le même numéro de FD. Un échec de nettoyage d'une ouverture refusée est rendu comme CLEANUP, sans succès implicite.

Statuts uint32_t propres à ce module : 0 OK, 1 ARGUMENT, 2 MEMORY, 3 CLOCK, 4 FD, 5 STATE, 6 EXPIRED, 7 VERIFY, 8 IO, 9 IN_DOUBT, 10 LOCK, 11 CRYPTO, 12 CLEANUP. Les tampons de sortie valides sont nettoyés avant les échecs ; les sorties ne contiennent que des données publiques. Le propriétaire de reprise devra distinguer frame locale et transition réellement ancrée, vérifier chaque transition et relire l'index authentifié courant. Une réouverture locale ne renouvelle ni mandat, autorité, UTC ou droit d'effet.

Sources de recette : tests/native/test_nv_journal.py (17 méthodes) et fixtures/nv_journal_driver.c. Elles préparent un artefact de TEST explicite, des fichiers/verrous/fsync nominaux réels sous output/tests/pa01-nv-journal et des wrappers de pannes/horloge limités à cet artefact. Aucun ESAPI/TCTI/TPM n'y est lié. Les tests ne qualifient pas les propriétés de stockage physique, de restauration, le véritable profil protégé, NV_Extend ou les propriétaires manquants. Ces sources et l'ABI demeurent NON COMPILÉES/NON TESTÉES en phase 1 ; aucune tâche n'est cochée.


## Garde de transmission TCTI — étape native D10–D12, non qualifiée

Réalisation dans nv_anchor.pyx, avec le header nv_anchor.h généré et le confinement System existants. Aucun header généré n'est édité manuellement ; aucun module supplémentaire, _api.h, capsule Python, backend découvert ou nouvelle dépendance n'est ajouté. Le propriétaire C réel prête un TCTI déjà initialisé/quiescent, exclusif, vivant et qualifié. La garde n'initialise ni ESYS, TCTI, provider, périphérique ou clé et ne reçoit aucun authValue.

La source ESAPI 4.1.3 réémet depuis NV_Extend_Finish sur certaines réponses RETRY/TESTING/YIELDED. Un contrôle applicatif entourant Finish ne suffit donc pas à empêcher cette délégation après échéance. La garde fournit le point d'admission transport à raccorder réellement au contexte ESYS ; sa seule présence ne rend pas les lecteurs antérieurs ou un futur Extend qualifiés.

pa01_tcti_guard_new(void **state_out, void **tcti_out, void *backend, uint32_t nv_index, uint64_t deadline_ns, size_t max_command, size_t max_response) exige sorties distinctes initialement NULL, index NV explicite 0x01000000–0x01ffffff, bornes 10..UINT32_MAX du cadrage filaire et échéance CLOCK_MONOTONIC future. Ces bornes de représentation ne fixent aucun budget d'exploitation. Le profil protégé doit fournir les plafonds réels. Le contexte gardé est remis au seul propriétaire natif pendant new. Le backend emprunté doit exposer ABI 1 ou 2 et transmit/receive ; ses marqueur/version/callbacks sont conservés et rapprochés pendant l'usage. Cela ne prouve ni provenance, identité TPM ni exclusivité contre un acteur hostile.

La structure interne commence par le vrai TSS2_TCTI_CONTEXT_COMMON_V2 avec membre v1 et signatures des headers. Son marqueur est propre à cette implémentation, sans constante universelle de confiance. Le PID limite les appels hérités d'un fork ; le propriétaire reste responsable de tous alias et consommateurs. Il doit créer son ESYS sur CE TCTI et installer les contrôles crypto/logging qualifiés avant authValue et première commande. Aucun getter de contexte ESYS ni preuve cliente « gardé » ne remplace ce raccord réel.

Transmit contrôle l'horloge avant délégation ; expiration ou perte d'horloge demeure acquise même si une lecture ultérieure revient sous la borne. Pending/quarantaine interdisent toute nouvelle délégation. Le cadrage taille/tag/longueur/code est vérifié. Seuls NV_ReadPublic vers cet index, NV_Read/NV_Extend avec authHandle=nvIndex=attente et tag avec sessions, StartAuthSession sans session avec tpmKey=NULL et bind=attente, puis FlushContext sans session de classe HMAC sont admis. La possession de LA session Flush et l'autorisation courante restent vérifiées par leur propriétaire ESAPI ; la garde ne fournit aucune de ces preuves. Elle ne valide pas tous les paramètres TPM, le HMAC, un mandat ou un droit d'effet.

Une tentative TX est enregistrée avant l'unique appel backend. Son échec est conservateur IN_DOUBT, sans retransmission automatique. Une acceptation transport reste pending et doit être réconciliée, même si l'appel finit après l'échéance. La garde refuse la délégation quand son contrôle constate l'expiration ; elle ne prétend pas borner la préemption, le temps interne du backend ou l'instant physique de transfert. Le budget initialisé avant la garde, les syscalls et la quiescence demandent leurs preuves propres.

Receive délègue toujours avec timeout zéro, y compris si le consommateur demande un timeout infini. Après délai ou perte d'horloge, la réception sert seulement au drainage/réconciliation d'une tentative existante. Une requête de taille sans tampon ne consomme pas pending. Les tailles sont bornées avant toute allocation par le consommateur ; la capacité remise au backend est plafonnée à max_response. TRY_AGAIN et buffer insuffisant conservent pending. Une réponse complète de forme cohérente le retire, mais ne blanchit jamais une issue inconnue précédente, expiration ou perte d'horloge. La première erreur ambiguë significative reste disponible. Aucun octet de commande/réponse n'est journalisé ou rendu à Python par cette ABI.

pa01_tcti_guard_status(void *state, uint32_t *flags_out, uint32_t *last_rc_out, uint64_t *tx_calls_out, uint64_t *rx_calls_out) rapporte seulement l'état local et les délégations réellement effectuées, avec compteurs saturants. Bits : 1 pending, 2 unknown, 4 expired, 8 clock_lost. Les retours locaux sont 0 OK, 1 ARGUMENT, 2 MEMORY, 3 CLOCK, 4 STATE, 5 PENDING, 6 EXPIRED, 7 VERIFY, 9 IN_DOUBT selon l'API et l'état ; les callbacks TCTI emploient les vrais codes TSS2. Une réponse de transport n'est ni vérification HMAC ni instantané NV actuel.

Le callback finalize ne libère rien et ne touche pas le backend. Cancel, getPollHandles, setLocality et makeSticky ne délèguent rien et rendent NOT_IMPLEMENTED pour un contexte valide. pa01_tcti_guard_close(void **state_inout) ne libère que le wrapper à frontière connue, sans pending/unknown, dans son processus propriétaire ; il ne finalise ni ESYS ni backend et ne Flush aucune ressource. Le propriétaire doit avoir terminé tous les consommateurs et invalider ses alias tcti_out. En quarantaine, l'état est conservé jusqu'à récupération ou arrêt réellement supervisé ; aucun forcefree ou booléen de quiescence.

L'échéance de cette garde ne peut pas être réarmée. Le futur propriétaire doit la rapprocher des bornes des lecteurs et de l'authentification ; une borne de garde plus large ne suffit pas à protéger un délai applicatif plus court. Un nettoyage autorisé sous une borne distincte nécessite son propre raccord, limité aux seules ressources possédées, sans rouvrir les opérations expirées. Les obligations de garde/remise FD, politique/autorité/UTC courantes, constructeur ESYS, confinement crypto et reprise du journal restent à réaliser. Aucune interface positive réseau n'est ouverte par cette tranche.

Les sources de recette sont préparées dans tests/native/fixtures/nv_public_driver.c et tests/native/test_tcti_guard.py : backend TCTI et horloge simulés, artefact PA01_NV_PUBLIC_DRIVER sélectionné sous output/tests/pa01-nv-public, capacités/compteurs et refus vérifiables, quarantaine en sous-processus sans effacement de l'état réel. Elles ne simulent pas une réussite HMAC ni une qualification ESAPI/TPM. Leur compilation et leur exécution, puis la recette avec ESAPI réel et transport autorisé, restent en seconde phase sur LXC. Aucun test produit, commande TPM, effet NV, installation ou nouvelle coche n'est exécuté par cette inscription.

Références : [NV_Extend ESAPI 4.1.3](https://raw.githubusercontent.com/tpm2-software/tpm2-tss/4.1.3/src/tss2-esys/api/Esys_NV_Extend.c), [ABI TCTI](https://raw.githubusercontent.com/tpm2-software/tpm2-tss/4.1.3/include/tss2/tss2_tcti.h) et [codes TSS2](https://raw.githubusercontent.com/tpm2-software/tpm2-tss/4.1.3/include/tss2/tss2_common.h).


## Liaison concrète du lecteur NV à sa garde TCTI — source privée

pa01_nv_public_new_guarded conserve les paramètres de pa01_nv_public_new et ajoute le seul pointeur de garde avant le contexte ESYS. Il utilise le vrai Esys_GetTcti pour rapprocher le contexte remis à ESAPI et le wrapper attendu, son index et son échéance exacte. Le marqueur natif, le PID, les callbacks backend conservés et l'absence de pending/unknown/expiration sont contrôlés. Un lecteur unique est inscrit comme possesseur ; un second est refusé et sa seule allocation locale est nettoyée sans IO. La construction ne prouve toujours ni origine du contexte, autorité courante, politique, UTC, garde du secret, identité TPM ou confinement crypto.

Le lecteur conserve cette référence privée et contrôle la liaison et les flags sticky aux entrées et sorties pertinentes de start/step/status/value et des Finish. Une perte de liaison, une issue inconnue ou une activité transport étrangère à sa phase pendante conserve QUARANTINED/IN_DOUBT. CLOCK/EXPIRED invalident et nettoient toute valeur, même si une lecture courante de l'horloge redevient acceptable. Les phases pendantes sont conservées pour réconciliation ; les handles/session reçus avec succès restent suivis et les buffers de réponse sont libérés avant le retour tardif. Aucun passage à COMPLETE ne rétablit une valeur invalidée par la garde.

Les échéances du lecteur et de sa garde sont communes. Pour ce constructeur, auth_start exige exactement cette échéance ; cleanup_start ne peut pas la dépasser. Une garde déjà expirée ou privée d'horloge refuse un nouveau nettoyage avant Async ; elle n'est jamais réarmée. Les flags du nettoyage en cours et son statut restent séparés de l'échec primaire. Une procédure de récupération sous un autre budget reste à réaliser par le véritable propriétaire et ne découle pas de ces paramètres.

La garde refuse close tant qu'un lecteur demeure lié. Le lecteur ne libère cette possession qu'après les clôtures locales effectivement réussies et en l'absence de pending/unknown transport. Un refus conserve les pointeurs et diagnostics ; aucun Finalize/Flush du backend n'est ajouté. Le propriétaire natif doit encore gérer la durée de vie de son ESYS et de tous ses consommateurs avant de libérer le wrapper et le backend prêté.

Le constructeur legacy reste disponible comme primitive historique non liée ; les futurs chemins opérationnels gardés doivent employer le nouveau constructeur, sans repli vers legacy en cas de refus. Aucun handler d'admission, ancre, effet PostgreSQL ou droit nouveau n'est ouvert par cette compatibilité. Les quatre sources de cas supplémentaires vérifient les rapprochements, possession, horloge sticky, refus de borne avant consommation d'un vrai pipe de fixture et conservation d'un lecteur pending. Le conducteur Esys_GetTcti et les opérations ESAPI y restent simulés ; les 22 méthodes de test_tcti_guard.py sont préparées, non exécutées, et ne constituent aucune qualification ESAPI/TPM.


## Baux natifs de durée de vie — journal et lecteur NV

Cette tranche D10–D12 ajoute des liens C privés entre ressources réellement ouvertes et leur consommateur natif. Elle ne produit ni intention sémantique durable, ni admission, ni droit d'extension. Les pointeurs owner ne sont jamais reçus de Python/HTTP/JSON/PZT : leur unicité, leur durée de vie et l'absence de concurrence sont garanties par la composition native exclusive. Aucun jeton client, booléen verified ou objet de données ne crée ces ressources.

nv_anchor.h expose pa01_nv_lease_acquire/snapshot/release. acquire requiert un lecteur effectivement couplé à la garde TCTI, une lecture authentifiée terminée, sa fraîcheur courante, un handle connu et aucune session vivante/métadonnée de session résiduelle. Il restitue la valeur de 32 octets, le Name de 34 octets, l'index et l'échéance réellement conservés par ce lecteur ; les sorties sont effacées en cas de refus. Un seul owner est accepté. snapshot exige ce même owner et répète les contrôles réels ; une observation passée ne prolonge pas l'autorité. close refuse le bail avant toute suppression de métadonnée ou d'authValue. release réobserve la garde et refuse les commandes/sessions pendantes ou inconnues ; la libération connue après expiration ne réarme ni le lecteur ni sa fraîcheur.

nv_journal.h expose pa01_journal_lease_acquire/snapshot/release et pa01_journal_append_leased. acquire conserve le journal déjà ouvert/verrouillé, vérifie de nouveau les identités, toute la chaîne de frames, le reçu/la taille/le nombre et l'échéance ; il restitue aussi la borne de record déjà imposée par le propriétaire. Un second owner est refusé. Les sorties sont effacées lors d'un échec. Le snapshot sous bail relit réellement le journal ; il ne restitue pas seulement une copie déclarée par l'appelant. L'ajout public ordinaire est refusé tant que le bail est détenu. L'ajout réservé exige le même owner et utilise le même corps réel d'écriture, contrôles, fsync du fichier et du répertoire, relecture et traitement IN_DOUBT ; aucun chemin nominal simplifié ne le remplace. close refuse de libérer les FD/verrou avant release. Les IO étant synchrones et revenues, release peut détacher le lien après une erreur/expiration connue, sans effacer la panne du journal, réparer le disque ou autoriser un rejeu.

Les ABI précédentes restent conservées hors bail. Aucun bail ne qualifie le contexte ESAPI/OpenSSL/TCTI, son origine ou son logging. Les sources de recette ajoutent quatre cas NV gardé dans test_tcti_guard.py (26 méthodes au total) et quatre cas IO dans test_nv_journal.py (21 méthodes au total). Le conducteur ESAPI/TCTI est simulé ; les futures IO de journal utilisent des fichiers/verrous/fsync réels. Ces sources restent non compilées/non testées. Le producteur de l'intention canonique liée à toute l'histoire, la consommation unique, NV_Extend et la confirmation authentifiée restent à raccorder.

## Décisions communes PA01 / C08 / Z12 et cible de seconde phase

Le profil commun D14 adopté humainement dans CISMP6 (question call_20139b370fa549b183e97acbb1e5b7bf/0, message 01a16d40-7505-79f2-bc3c-5bcdfc5569ff) autorise, pour PA01 System et Z12, des observations natives Cython/C via libsystemd : UID/PID, unité et manager, MainPID/InvocationID, avec installation, cible, artefacts et politique protégée versionnée. Un UID 0 ou DTO Python ne suffit jamais. Les domaines, politiques, mandats et builds restent distincts. libsystemd-dev/libsystemd0 257.13-1~deb13u1 et dépendances Debian signées sont adoptés pour les images isolées de construction/essai des deux RUNs en seconde phase, sans installation ou modification des services de l'hôte courant. Ce texte n'affirme aucun producteur de faits déjà réalisé ou qualifié.

Le profil Linux conserve le choix chrony/NTS sur time.cloudflare.com. Sur LXC, l’emploi proposé de chronyd -x doit préserver l’horloge partagée ; aucune installation ou heure vérifiée n’est présentée comme déjà disponible. Le raccord applique les canons runtime et PZT A10i52. L’amorçage du temps peut précéder PostgreSQL et PZT et ne dépend pas de l’admission B, sous politique protégée courante, opérateur mandaté, capacité du catalogue fermé, cible et exécutant réellement vérifiés, sans droit métier, R01 ou SuperAdmin, sans autorité de renouvellement PKI et sans réouverture D6. NTS seul n’établit pas l’heure initiale et aucun téléchargement circulaire n’est admis.

En mode SYNCHRONISE, la preuve amont est âgée d’au plus 600 secondes, avec une incertitude U(t) d’au plus une seconde. En mode HORS_LIGNE, une preuve âgée de plus de 600 secondes n’est admise qu’avec un modèle, une provenance et une continuité qualifiés, un profil courant et une acquisition actuelle, avec la même exigence U(t) d’au plus une seconde. Hors de ces conditions, le résultat est INVERIFIABLE et aucun effet dépendant du temps n’est admis. L’intervalle UTC conservateur entier reste contenu dans les fenêtres de validité exigées par chaque contrôle de mandat et de certificat, sans troncature favorable ; l’incertitude ne couvre pas la durée totale d’une fenêtre de validité.

Les budgets d’acquisition sont cumulés : 250 millisecondes par acquisition, deux acquisitions au maximum, une seconde au total. L’échéance la plus courte est prioritaire, sans réarmement ni rajeunissement. Une lecture récente ne rajeunit pas la preuve amont et aucun ancien échantillon n’est réemployé entre décisions. La perte de provenance ou de continuité, une suspension, une restauration ou un retour réseau incohérent invalident la continuité. Une nouvelle acquisition ne renouvelle aucun mandat, certificat ou droit. L’absence d’Internet n’abolit pas les règles d’autorisation PZT des opérations critiques.

L’interface commune reste à réaliser et à qualifier. Le contrat C.Z12_TIME_OBS/v2 reste privé et n’ouvre aucun droit d’import de son ABI. Les fonctions indépendantes du temps conservent leurs propres contrats.

D15 Z12 porte uniquement sur son gardien PKI et sa remise de credential host+tpm2 ; cette adoption ne livre ni gardien, service, secret ou autorisation NV PA01. Les ressources et secrets PA/PKI restent séparés.

La réalisation précède toujours la phase de compilation/tests/validation sur LXC, selon l'instruction courante. La cible désignée est CT100 cismp ; l'autorisation humaine vérifiée du message 01a16d40-0729-7742-9816-f8601f823249 dispense de nouvelle approbation pour les opérations strictement intérieures au conteneur. L'identité SSH réelle et l'accès TPM restent à observer. L'exemption ne s'étend pas au dépôt hôte, Git/OpenSpec, Proxmox ou aux effets sur le TPM physique partagé ; ces derniers conservent leur plan exact distinct. CISMP6 centralise le premier contrôle SSH/identité/TPM, avant toute campagne concurrente. Aucune connexion, installation, commande SQL/TPM ou recette n'est exécutée par cette inscription.


## Reçu sémantique d'IO — producteur privé de l'intention PA

Réalisation prévue dans nv_intent.pyx, réservé au seul graphe System, headers générés nv_journal.h/nv_anchor.h/nv_intent.h. Le codec postgresql_contracts est un module compilé/initialisé explicitement de ce même graphe ; ni découverte d'import ni repli vers un module externe. Aucune fonction Python, capsule ou _api.h n'expose les capacités C. Le GIL est détenu pendant le codec public ; les pointeurs, buffers et ressources proviennent de la composition C exclusive déjà initialisée. Le producteur ne vérifie pas à lui seul la provenance du profil, l'autorité native, le mandat, le fencing ou la politique : aucun de ces faits n'est déduit d'un pointeur ou UID.

pa01_intent_prepare reçoit deux sorties vides distinctes (intention et quarantaine), un journal réellement ouvert/verrouillé, un lecteur réellement gardé/authentifié, le SHA-256 public de la PREMIÈRE transition préexistante épinglé par le profil protégé et les octets de la prochaine transition. Les bornes max_json, max_ref, max_epoch, max_sequence, max_correlation et max_causation proviennent du même propriétaire natif/profil, sans valeurs de production implicites ; elles alimentent JournalLimits/PayloadLimits. Le pin lie le point de départ complet et son contexte, sans créer de genèse, initialiser un index ou prouver sa propre provenance. L'exposition de ces entrées sur PZT/Python n'est pas autorisée.

L'état natif alloué avant acquisitions sert d'owner aux deux baux. Les échéances doivent être exactement communes. Chaque record préexistant est réellement copié depuis le journal ; décodage fermé, réencodage canonique exact, empreintes avec le domaine du codec, pin initial, contexte installation/cible/registre/génération/époque, séquence contiguë, liens head/NV et unicité de transition_ref sont vérifiés sur toute l'histoire. La valeur du lecteur HMAC doit égaler la valeur attendue après la dernière transition ; un écart est IN_DOUBT, sans écriture, réparation ou extension automatique. La prochaine transition doit prolonger exactement cette histoire.

Le payload est copié en mémoire détenue avant effet ; la valeur validée est celle réellement ajoutée. Après calculs/allocations, le producteur recontrôle les baux/snapshots, utilise l'unique corps réel append_leased avec ses deux fsync et recontrôle reçu, taille, nombre, bornes, échéance, Name/index et ancienne valeur NV. Seul un succès réel émet l'intention préparée. Il ne prétend pas avoir déjà étendu NV : le nouveau record durable reste non ancré à ce stade. Un crash ou abandon ne le supprime pas ; une nouvelle préparation normale constate l'écart et exige une réconciliation sous autorité courante.

pa01_intent_claim recontrôle les snapshots réels et le même lecteur borné par la garde, puis marque le reçu consommé AVANT restitution du head/ancienne valeur/valeur attendue et des pointeurs C réels. Un second appel retourne CONSUMED et des sorties effacées. Ce reçu ne constitue pas une permission d'effet ni une nouvelle lecture physique du TPM : la prochaine tranche NV_Extend doit encore imposer son consommateur C, la session HMAC, les contrôles d'autorité/actualité et la confirmation physique. Aucun raw_extend(head), reset ou confirmation par booléen n'est fourni.

Codes du producteur : 0 OK, 1 ARGUMENT, 2 MEMORY, 4 STATE, 7 VERIFY, 9 IN_DOUBT, 14 CONSUMED. Le tableau C detail_out de quatre uint32 conserve séparément étape (1 journal, 2 lecteur NV, 3 codec, 4 divergence sémantique), statut source primaire, libération du journal et libération NV. Les appels avec GIL ont aussi une convention d'erreur Python UINT32_MAX avec PyErr_Occurred ; le consommateur C doit la traiter comme échec, jamais succès. Les erreurs de contrat/UTF-8/mémoire attendues sont traitées explicitement ; une exception inattendue conserve sa cause après nettoyage et n'est pas transformée silencieusement en réussite.

Aucune mémoire owner n'est libérée tant qu'un bail subsiste. Après échec de préparation, aucune intention consommable n'est émise ; si le détachement réel est refusé, la sortie de quarantaine conserve seulement l'état de nettoyage, non admis par claim. close laisse l'état et les liens en place tant que la libération est incertaine. Avant claim, un détachement connu peut libérer les liens/mémoire, avec retour IN_DOUBT si un ajout a été tenté ; il ne répare pas l'histoire non ancrée. Après claim, close reste fermé et conserve l'état tant que le futur consommateur n'a pas établi une confirmation physique réelle. La présente tranche n'invente pas ce consommateur ou son API de confirmation.

Les sources et leurs dépendances de compilation/import restent à raccorder et qualifier avec des cas de chaînes réelles de fichiers, refus canoniques/contextes/séquences/doublons, divergence NV, fsync/expiration, consommation unique et quarantaine. Les simulations ESAPI/TCTI ne qualifient pas HMAC/TPM, l'autorité réelle, les restaurations ou la persistance physique. Aucune construction, import, syntaxe ou exécution de test n'est effectuée en phase 1.


## Nouvelle observation HMAC et confirmation physique de l'intention

Le compteur read_serial du lecteur est interne, monotone sur uint64 et incrémenté uniquement après une réponse NV_Read HMAC de bonne taille, nettoyage connu de session et contrôles de fraîcheur réussis. Il n'est ni une autorité, ni un compteur TPM, ni une preuve cryptographique isolée. pa01_nv_lease_read_serial exige le même owner du bail, la garde courante et un lecteur effectivement terminé/authentifié ; sa sortie est effacée sur refus.

pa01_nv_lease_refresh_start, réservé au même owner C, démarre une NOUVELLE session HMAC-SHA256 liée au même index avec nonce natif neuf et session à usage unique. L'authValue déjà confinée à ESAPI reste dans le même contexte natif ; aucun nouveau secret n'est remis à Python ou par argument. Le lecteur doit être quiescent en AUTH_COMPLETE, sans session/métadonnée pendante, avec garde/profil/index et échéance communs inchangés. La valeur en cache est invalidée avant envoi ; le chemin existant pa01_nv_auth_step termine réellement StartAuthSession puis NV_Read. Une phase échouée/quarantainée n'est jamais réarmée ; expiration, issue inconnue ou saturation du compteur ferment l'usage. Une nouvelle lecture peut remplacer un cache absent après une opération connue quiescente ; elle ne prouve pas par elle-même un droit d'effet.

Le producteur d'intention mémorise le serial réellement observé avec ses snapshots et impose sa stabilité jusqu'à claim. pa01_intent_confirm reçoit l'intention déjà consommée et le lecteur C réel identique. Il recontrôle le journal complet/snapshot, la cible/Name/index/échéance et la lecture authentifiée courante. La confirmation exige un serial STRICTEMENT postérieur à celui préparé ET la valeur NV attendue pour le nouveau head. Un compteur seul, le vieux cache ou un booléen de succès ne confirme rien. Une divergence conserve l'intention consommée en IN_DOUBT ; aucune remise à zéro ou nouvelle extension n'est déclenchée.

Seule cette observation physique positive fait passer l'intention à CONFIRMED. Une nouvelle remise par claim reste refusée (CONSUMED). close peut alors détacher les liens connus et restituer un succès de nettoyage, sans rendre une ancienne autorité à nouveau courante. Une expiration postérieure ne détruit pas le fait historique de confirmation et n'autorise aucune opération nouvelle. Le journal et l'index ne sont jamais créés/réparés dans ce raccord.

Ces fonctions sont des primitives C privées encore non compilées/non testées ; leur qualification exige l'ESAPI/TCTI/TPM autorisé et les propriétaires réellement compétents. NV_Extend lui-même, son consommateur C et ses contrôles d'autorité avant effet restent à réaliser ; les scénarios de test simulent explicitement la valeur NV au conducteur ESAPI, puis passent par le véritable chemin natif de relecture pour tester la confirmation. Aucun effet TPM, import, syntaxe, build ou test n'est exécuté en phase 1.


## Cohérence des bibliothèques adoptées dans le build

Le linker et l'assembleur partagent désormais la même liste fermée de SONAME candidats : OpenSSL 3/libpq déjà retenus, la pile TSS déjà déclarée pour D10–D12 et le provider TPM2, et libsystemd.so.0 adopté par le profil commun D14. L'ajout de libsystemd à cette représentation ne prouve ni présence, version Debian, ABI qualifiée ou observation native compétente. TCTI/device ou tabrmd ne sont pas sélectionnés implicitement par la liste.

Aucun fichier n'est chargé, copié ou lié sur la seule base du SONAME : les entrées restent explicites par rôle, épinglées par SHA-256 dans l'inventaire du profil, vérifiées ELF et SONAME réel avant liaison. Les règles d'assets de l'assembleur et leur inventaire restent conservées. Les bibliothèques étrangères et autres majeurs d'ABI restent refusés. Les dépendances transitives et leur fermeture réelle doivent encore être inventoriées/qualifiées ; cette liste n'en constitue pas une preuve ni une autorisation d'installation sur l'hôte. Le test unitaire préparé vérifie que des bibliothèques TSS/systemd candidates sans inventaire sont toujours refusées avant outil de liaison. Aucun test ou build n'est exécuté.


## Durée de vie du consommateur C de l'intention

Le raccord prévu pour NV_Extend distingue la possession de l'intention de celle de son consommateur C. pa01_intent_claim_owned ajoute une identité de durée de vie C non nulle, issue du consommateur natif exclusif. Elle ne constitue ni une autorité ni un paramètre client. La consommation reste unique et précède la restitution des données publiques/pointeurs natifs réels. Les API antérieures claim/confirm conservent leur signature et leur comportement privé, avec l'intention comme propriétaire local par défaut.

pa01_intent_confirm_owned exige le consommateur exact en plus des vrais contrôles journal/lecteur/serial/valeur attendue déjà définis. Même après confirmation, close conserve les liens et l'état tant que ce consommateur n'a pas été détaché. pa01_intent_consumer_release ne détache que le consommateur identique d'une intention réellement CONFIRMED, après contrôle natif de quiescence du lecteur. Il ne libère pas lui-même les baux NV/journal : close de l'intention effectue ensuite leur libération réelle. Un mauvais consommateur, une commande/session pendante, un contexte inconnu ou une confirmation absente ne libère rien.

pa01_nv_lease_quiescent vérifie le même owner du bail, la garde courante et un état connu du lecteur, sans session/métadonnée en attente et avec handle conservé. Une expiration/perte d'horloge déjà connue peut autoriser ce seul détachement de ressources quiescentes, sans nouvelle IO, confirmation ou permission. La fonction de libération du bail réutilise ce contrôle ; aucun état inconnu n'est réarmé ou masqué.

pa01_intent_journal_current_owned est un contrôle C du SEUL journal avant un futur effet : même intention consommée et consommateur, mêmes liens réellement détenus, PID/UID et nouvelle lecture de toute la chaîne locale avec rapprochement du reçu, taille, nombre, borne et échéance. Il n'affirme rien sur l'autorité, le mandat ou la politique courante et ne remplace pas les contrôles du lecteur/consommateur. Une altération réelle du fichier est refusée ; les liens consommés restent conservés et aucune extension/reprise automatique n'est déclenchée.

Le consommateur NV_Extend lui-même reste à réaliser. Il devra être construit réellement avant claim, conserver sa propre durée de vie et ses états d'effets/sessions, établir la relecture/confirmation réelles et se détacher avant destruction de l'intention. Aucun drapeau de succès ou objet Python ne peut remplacer cette séquence. Deux recettes sources isolées supplémentaires préparent le contrôle de ce lien de durée de vie et la détection d'une altération réelle du journal. Ces sources restent non compilées/non testées ; aucune opération TPM/SQL ou nouvelle admission n'est produite par ce raccord.


## Primitives internes NV_Extend et modèle ESAPI de recette

La prochaine tranche prépare seulement les fonctions internes C pa01_h_extend_async/finish dans nv_anchor.pyx. Elles utilisent les API ESAPI 4.1.3 NV_Extend_Async/Finish, le même index en authHandle/nvIndex, la session HMAC en premier slot et aucun autre slot ; le buffer est exactement le head SHA-256 de 32 octets. Le buffer local est nettoyé après Async. Finish est appelé une fois, sans boucle synchrone, sans délai indéfini ni rejeu d'effet. Ces fonctions restent statiques/privées au module, absentes de l'API Python et du header public ; elles ne constituent pas un handler, une admission ou un point public raw_extend(head).

Le consommateur opaque, l'unicité de la tentative, la mise à jour des phases du lecteur, le contrôle courant du journal/garde/mandat et la relecture de confirmation doivent encore être raccordés avant qu'une extension puisse être exposée par le propriétaire réel. La seule présence de ces helpers n'autorise aucun effet. Le contrôle Transmit déjà adopté reste nécessaire contre les resoumissions internes de Finish après expiration observée. Le contexte et le logging/mémoire de la pile exacte restent à qualifier avant authValue ou commande autorisée.

Le conducteur ESAPI de TEST conserve désormais une valeur NV PAR CONTEXTE simulé, initialement A3 répété, afin que Read et Extend simulent le même état. Son Extend vérifie la cible, les trois slots, l'authValue déclarée dans le modèle, la session liée/à usage unique et la taille ; la session HMAC elle-même reste simulée et ne prouve aucune authentification cryptographique. Le modèle calcule SHA-256(ancienne_valeur || head) et compte une application par commande simulée ; les TRY_AGAIN de Finish ne répètent pas cette application. Les modes21/22 injectent des erreurs Async/Finish, 23 une attente bornée et 24 une réponse perdue après effet, conservant contexte/pending inconnus et interdisant la destruction de la fixture.

Le conducteur intégré d'intention utilise ce même état par contexte. Son setter public de TEST reçoit explicitement la fixture concernée ; modifier la fixture seule ne modifie pas le cache du lecteur ni le serial de lecture. Les sources de recette sont adaptées à cette ABI de TEST. Aucun de ces conducteurs, wrappers ou modes n'entre dans un artefact produit. Ils ne qualifient ni HMAC/TPM réel, ni persistance physique, ni clonage/restauration ou réconciliation de l'index partagé. Aucune compilation, syntaxe, exécution de recette ou commande TPM n'est effectuée ici.


## Consommateur privé NV_Extend — première tranche de réalisation

Cette tranche complète les helpers internes avec un état C opaque construit avant consommation du reçu IO. pa01_nv_extend_start reçoit seulement une intention native réelle et une sortie C vide, jamais un head ou un index client. Après claim_owned réussi, l'adresse du consommateur demeure vivante sur TOUT échec ; elle n'est libérée qu'après confirmation positive et détachement réel. Les modules/contextes/ressources doivent être initialisés, exclusifs et qualifiés par leur propriétaire ; aucune adresse fournie par Python/PZT n'est admise.

Le flux nominal comporte une nouvelle lecture HMAC vérifiant ancienne valeur et serial neuf ; une nouvelle session liée à l'index, nonce natif et usage unique ; un état EXTEND_READY sans extension automatique ; un commit C EXPLICITE qui relit le journal réel et recontrôle garde, cible/Name/index, budget, ancienne valeur et serial. La tentative est marquée avant l'unique Async ; l'ancien cache est invalidé. Finish n'est appelé qu'une fois par progression, avec traitement des TRY_AGAIN de la seule commande existante. Après réponse HMAC positive et fermeture connue de la métadonnée de session consommée, une NOUVELLE lecture HMAC doit retrouver la valeur attendue et confirm_owned doit réussir sur le journal/lecteur réels avant DONE/OK.

Les phases internes du lecteur 0–10 sont conservées ; EXTEND_SESSION_PENDING=11 et EXTEND_PENDING=13 sont réellement pendantes, EXTEND_READY=12 ne l'est pas. Les observateurs et le refus de clôture prennent en compte ces phases. Aucune transmission n'est autorisée après expiration connue par la garde TCTI, même lors d'une resoumission interne ESAPI. Les Finish encore nécessaires peuvent constater une fin connue après délai sans rendre un succès applicatif tardif ou initier un nouvel Async.

Les API C sont start, step, commit, status et close. status reçoit cinq sorties uint32 obligatoires après state : phase, erreur primaire, premier code TSS fatal, erreur de cleanup et code TSS du cleanup. Il décrit un état historique inspectable, sans preuve d'autorité actuelle. Les erreurs primaires et de nettoyage restent distinctes ; une erreur Finish/transport ou toute issue non confirmée après tentative reste IN_DOUBT, sans seconde Async. close ne déclenche ni commande ni confirmation ; il ne libère que le consommateur réellement DONE après consumer_release réussi, puis vide la sortie.

Ce premier lot CONSERVATEUR conserve les états/liens avant confirmation, y compris après certaines erreurs connues avant effet. Le détachement contrôlé de ces échecs, le drainage/cleanup complet, la reprise avec nouveau contexte/autorité et la réconciliation après crash restent à réaliser et à qualifier dans la suite de la tâche6. Le consommateur ne se substitue pas au propriétaire réel d'admission : mandat, politique/révocation, confirmation, préconditions, fencing et UTC courants doivent être vérifiés avant chaque effet par les raccords encore manquants. Aucun handler public n'est ouvert par ce code.

Le nouveau lien C nv_anchor vers nv_intent impose la composition explicite des cinq modules déjà décrits et leurs vrais headers générés, notamment dans les artefacts de recette NV. Les chargeurs/graphe et recettes doivent être adaptés avant leur exécution. Aucun acteur, callback de succès, libération forcée, clé, CA ou index n'est créé ; aucun test/build/import/syntaxe produit, commande SQL/TPM ou qualification n'est effectué en phase1.


## Nettoyage connu avant tentative NV — complément du consommateur

pa01_nv_extend_cancel_step traite uniquement un consommateur n'ayant pas tenté NV_Extend. La demande d'annulation ferme son commit ; le marqueur local cancelled exprime une demande de contrôle, jamais une autorité ou preuve de réussite. La progression d'une création de session déjà envoyée est drainée sans démarrer le NV_Read prévu. Un NV_Read déjà envoyé est seulement terminé ; aucune session d'extension n'est créée ensuite. Seule la session réellement possédée peut être flushée, dans l'échéance déjà déclarée ; le budget n'est pas réarmé. Une session TPM déjà consommée ne nécessite que la fermeture locale de sa métadonnée.

Les phases X_CANCEL_PENDING=9 et X_CANCELLED=10 appartiennent au consommateur, sans modifier les phases du lecteur ou celles du résultat technique. Le retour 0 de cancel_step signifie seulement quiescence des ressources avant effet, pas résultat métier ou ancrage. Les erreurs primaires et de nettoyage restent inspectables. Un Finish encore pending après délai peut être drainé ; toute nouvelle commande tardive est refusée. Session inconnue, commande incertaine, issue inconnue ou budget insuffisant pour un nouveau Flush conservent l'état et les liens. L'annulation après tentative NV n'est pas admise par cette API.

pa01_nv_extend_abort_fact vérifie le véritable état opaque du consommateur, sa liaison à l'intention/lecteur, l'absence de tentative NV et la quiescence réellement constatée par la garde du lecteur. Ce n'est ni un booléen client ni un callback de succès. pa01_intent_abandon_owned exige ce fait C réel, le même consommateur, les ressources effectivement détenues et le contexte courant du processus ; il détache le seul consommateur et marque l'intention BROKEN. Il ne crée/répare/ancre aucun record, ne rend aucun mandat et ne réouvre aucune opération consommée.

close du consommateur peut alors rendre IN_DOUBT avec sortie NULL lorsqu'un détachement connu AVANT effet a réellement libéré sa mémoire ; le record durable reste non ancré. IN_DOUBT avec sortie non NULL conserve au contraire un état encore possédé/inconnu. Le succès 0 du close opérationnel reste réservé au consommateur réellement confirmé DONE. La clôture ultérieure de l'intention libère ses baux connus, sans effacer l'échec ou la divergence d'ancrage. Toute tentative NV déjà commencée conserve le chemin de confirmation/réconciliation distinct et interdit ce détachement anticipé.

Les recettes sources supplémentaires préparent annulation avant commit, drainage d'une création de session sans envoi de Read, drainage du Read sans session d'extension, et échec RNG après claim sans adresse consumer pendante. Les scénarios inconnus/expirés et après effet conservent leurs refus. Elles restent non compilées/non testées ; aucune commande TPM, source d'autorité ou qualification n'est fournie par cette inscription. La reprise après crash/effet incertain avec nouveau contexte et autorité courante reste à réaliser.


## Garde et source du secret PA — D13 adopté

D13 PA adopte LoadCredentialEncrypted avec source dédiée host+tpm2 et garde/remise dans le lanceur System existant, sans autre exécutable/mode, secret partagé ou repli. L'authValue reste exactement 32 octets binaires, distincte de toute maintenance/CA/TLS/opérateur/PBO/PKI. Les profils/publics et capacités FD ne sont jamais des champs de la requête PZT.

La provenance réelle du fournisseur, le chiffrement source combiné et la liaison versionnée au consommateur/installation/cible/index doivent être rapprochés par les propriétaires natifs courants avant remise. Les bornes et choix de déploiement sont explicites ; aucun PCR ou chemin n'est choisi implicitement. L'absence du propriétaire D14/politique, du credential ou de sa protection ferme l'usage. Aucun DTO, état de fichier ou descripteur seul ne prouve l'admission.

Les adaptateurs natifs peuvent vérifier/ouvir les seuls objets de credential désignés par le lanceur/profil protégé, puis transférer une capacité FD privée au lecteur existant pa01_nv_secret_read32. Ils ne remettent pas les octets à Python ou à un appelant réseau. La preuve de forme/identité/protection d'un fichier constitue un contrôle de ressource, pas la preuve que le fournisseur est le service systemd autorisé ; les deux sont requis. Les secrets et tampons natifs sont nettoyés et les erreurs primaires/cleanup séparées.

Cette conception ne charge aucun credential actuel et ne provisionne rien. Les versions/ABI/systemd, protections mémoire, facteurs/chiffrement réels, rotation/révocation, arrêt et récupération devront être inventoriés et qualifiés en seconde phase, sans assimiler présence du TPM ou source écrite à livraison.


## Adaptateur de ressource credential FD — sous-ensemble D13, pas propriétaire

pa01_nv_credential_open32 est une ABI C privée de nv_secret, réservée au graphe System sans export Python/capsule/_api.h. Elle reçoit une sortie FD initialement -1, un dirfd emprunté natif, basename ASCII canonique borné, UID/dev/ino/mode du répertoire attendus et échéance monotone ns explicites. Le lanceur/profil réellement vérifiés fournissent ces valeurs ; le client PZT/Python ne les fournit pas. Aucun paramètre verified ou source de configuration implicite n'est accepté.

L'adaptateur duplique le parent en CLOEXEC, vérifie le vrai répertoire owner/identité/mode owner-only déclaré (0500 ou0700), préobserve l'entrée sans suivre de lien, ouvre seulement O_RDONLY|O_NOFOLLOW|O_CLOEXEC|O_NONBLOCK, puis rapproche FD/entrée courante/parent. Le fichier doit être régulier, owner attendu, mode0400, lien unique et taille32 ; identités, modes, liens, taille, mtime/ctime sont rapprochés contre substitution. L'offset initial doit rester0 et le FD est non héritable. Le basename est copié dans un tampon natif borné, sans lire au-delà de sa longueur. Aucun octet du credential n'est lu par l'adaptateur.

Le budget courant est vérifié avant/après les opérations ; une égalité à l'échéance refuse la remise. Cela n'est pas une garantie de préemption d'un syscall/filesystem non qualifié. Les seuls FD propres sont fermés une fois sur refus, sans rejeu close/EINTR ; le parent emprunté reste intact. Le transfert readonly n'a lieu qu'après contrôles et fermeture connue du parent dupliqué. errno primaire et cleanup sont distincts et la sortie reste-1 sur échec. Les statuts réutilisent le lecteur :0OK,1ARGUMENT,2CLOCK,3FD,6TIMEOUT,8CHANGED ; bit16 signale closefailed, errno conservés séparément. Tout statut non nul est un refus, même si seuls les bits cleanup sont présents.

Un FD/fichier conforme ne démontre ni LoadCredentialEncrypted, ni modehost+tpm2, ni source chiffrée ou autorité courante. Ces preuves et la liaison unité/manager/MainPID/InvocationID/artefacts/politique/installation/cible/index restent exigées auprès du propriétaire natif D13 encore à réaliser. L'adaptateur ne lit aucun chemin par découverte/env, ne crée rien, ne charge aucun secret actuel et ne modifie pas le lecteur générique pa01_nv_secret_read32. Le FD remis peut ensuite être consommé uniquement par ce lecteur natif et ses contrôles existants.

Les cinq recettes sources nouvelles utilisent seulement des fichiers/FD publics temporaires : remise readonly puis consommation native du fixture, parent étranger, taille/mode/liens/symlink, basename/délai et sortie occupée préservée. Les pannes/intrusions du fournisseur et la qualification réelle de protection mémoire/stockage restent distinctes. Aucun import/compilation/test ou lecture de credential réel n'est exécuté.


## Port privé INITIAL_MATERIAL du contexte TLS PA

Le fichier tls_context.pyx contient un port Cython interne de durée de vie, utilisable uniquement par le client Z12 inclus dans le même module et graphe natif qualifié. Il n'ajoute aucun symbole cdef public/api, capsule, getter Python, client Z12 fictif, clé, certificat ou transport. L'initialisation TLS1.3/E3 et ready_for_transport=False restent celles du noyau existant.

_tls_lease_new conserve une référence forte à l'exact TLS13Context et lie le couple réel OSSL_LIB_CTX/SSL_CTX créé ensemble, l'owner C, le PID/thread natif, le côté client=1/serveur=2, l'usage INITIAL_MATERIAL=1, les 32 octets d'engagement d'opération et une échéance CLOCK_MONOTONIC en nanosecondes. Aucun délai ou contexte n'est déduit d'un DTO externe. Ce sont des liens de ressource ; PID/thread ne prouvent pas l'identité PKI, l'admission, le mandat ou la politique courante.

_tls_lease_context ne restitue les pointeurs typés OSSL_LIB_CTX** et SSL_CTX** qu'au même owner/scope/thread/processus, pendant le budget et avant retrait. Les sorties sont mises à NULL sur refus. _tls_lease_withdraw retire irréversiblement ce prêt. Les opérations Python configuration/verify/close/enter/exit refusent tout prêt actif ; la référence forte prévient une destruction automatique prématurée. Les statuts locaux sont 0 OK, 1 ARGUMENT, 2 MEMORY, 3 CLOCK, 4 STATE et 6 EXPIRED. Ils ne sont pas des résultats techniques PostgreSQL ou une autorisation.

La précondition de _tls_lease_close appartient au graphe fermé : l'unique client Z12 inclus possède un état C réel, y enregistre ses acquisitions et réalise les transferts/libérations OpenSSL avant de consommer son état et détacher le prêt. Aucun booléen resources_quiescent fourni par un appelant ne le remplace. Une opération encore active ou un cleanup inconnu conserve état, références et prêt pour réconciliation. Le port ne devine pas les objets d'un emprunteur arbitraire. La fermeture peut libérer la ressource après échéance, au seul owner/processus/thread d'origine. Un futur transport doit conserver le vrai propriétaire OSSL_LIB_CTX tant qu'un SSL en dépend ; SSL_CTX_up_ref seul ne garantit pas cette durée de vie.

Le client concret Z12, ses signatures et appels effectifs de destruction/transfert restent absents. Le port seul ne constitue donc pas un raccord INITIAL_MATERIAL intégré ou qualifié. Les deux sources tests/native/fixtures/tls_lease_driver.pyx et tests/native/test_tls_lease.py préparent dix recettes : couple réel, exclusivité, double acquisition, formes fermées, substitution de portée, échéance, erreur d'horloge, retrait, autre thread, référence forte et absence d'export produit. Le conducteur expose seulement ses wrappers de TEST et une horloge simulée ; il ne doit jamais entrer dans un artefact PA. Aucune compilation, syntaxe ou recette n'est exécutée en phase de réalisation.


## Observation locale de reprise du journal NV — phase source

nv_intent.pyx porte une capacité C d'observation distincte d'une intention consommable. Elle permet de rapprocher une histoire locale réouverte avec une nouvelle lecture HMAC, sans append, NV_Extend, rejeu, réparation, droit d'effet ou résultat PostgreSQL déduit. L'admission courante, le nouveau contexte et la quiescence réelle de l'ancien propriétaire restent des obligations séparées ; ce lot ne réalise pas une reprise positive complète.

pa01_observe_start reçoit le journal réel déjà ouvert/verrouillé, le lecteur réel gardé et authentifié, le pin initial de tête et les bornes natives explicites. Les sorties doivent être distinctes et vides. Il acquiert réellement les deux baux et leurs snapshots, rapproche échéances/Name/index et serial, mémorise les seules bornes C et conserve l'état avant l'unique pa01_nv_lease_refresh_start. Celui-ci réutilise l'autorisation déjà confinée dans ESYS et une nouvelle session HMAC à usage unique ; aucun secret n'est remis à Python ou au journal. Le retour 5 PENDING est normal. Après la tentative, une erreur conserve la capacité et ses obligations de ressources. Avant tentative seulement, un détachement effectivement impossible restitue une capacité de quarantaine, jamais une intention.

pa01_observe_step fait une seule continuation réelle pa01_nv_auth_step. Après son succès, il exige un serial strictement postérieur à l'initial, le même scope Name/index/délais et le même journal réel (reçu/taille/compte/borne). Le scanner partagé avec prepare relit tous les records : forme canonique exacte, pin, contexte constant, séquences +1 depuis le premier record, liens des têtes/valeurs et unicité des références. Il ne suppose ni séquence initiale égale à1, ni valeurs NV historiques disponibles. Après calcul, une seconde relecture réelle exige l'instantané frais identique avant toute publication.

Les classes locales sont HEAD_MATCH=0 si la valeur fraîche égale expected(last), TAIL_UNANCHORED=1 si elle égale seulement previous_nv(last), et DIVERGED=2 sinon. Elles décrivent seulement le rapprochement borné de la dernière transition. HEAD_MATCH n'est ni CONFIRMED ni SUCCEEDED, ni preuve de quiescence ancienne, de mandat courant, d'effet SQL ou d'autorité restaurée. Un échec est sticky et conserve son premier diagnostic ; le propriétaire réel garde le lecteur et ses API de drainage/cleanup, sans commande cachée de l'observateur.

pa01_observe_snapshot restitue classe, nombre, tête, valeur attendue, valeur observée et serial, après nouveau rapprochement réel des baux. Les sorties sont nettoyées et la classe vaut UINT32_MAX lors d'un refus. Les phases 5 OBSERVING, 6 OBSERVED et 7 OBSERVE_FAILED sont propres à cette capacité ; claim/confirm et les consommateurs d'intention ne les admettent jamais. Les statuts d'interface sont 0 OK, 1 ARGUMENT, 2 MEMORY, 4 STATE, 5 PENDING, 7 VERIFY, 9 IN_DOUBT et la convention d'exception Cython existante. detail[0..1] conserve étape/statut source primaire ; detail[2..3] sert au détachement journal/NV.

pa01_observe_close ne libère son état qu'après détachement réel des baux quiescents. Une commande encore pendante ou une issue inconnue conserve le pointeur et les ressources. Aucun Flush/Finalize, renouvellement de budget ou snapshot positif fictif n'est utilisé pour le cleanup. Un retour0 du close libère une capacité de ressource ; il ne change pas une divergence ou un résultat métier.

Le scanner refactorisé conserve les exigences du prepare existant, dont NV==expected(last) avant son unique append et la validation inchangée de la proposition suivante. Les mêmes cinq modules natifs demeurent requis ; aucun sixième module ou canal de partage n'est ajouté. Les recettes simulées seront préparées et resteront distinctes de la qualification matérielle sur LXC.


## Observation native D14 propre à PA — SELF et pair à la connexion

systemd_observation.pyx est un module privé du graphe System. Il utilise uniquement les API et structures des headers publics libsystemd/POSIX Linux, avec -D_GNU_SOURCE=1 explicite à la construction. Aucun fichier pxi Z12 ou ABI commune n’est importé. libsystemd est déjà adopté en D14 ; cette représentation ne qualifie ni son binaire/ABI réel ni la pile système. Les sources privées sont refusées dans Events, Session et PZT ; aucun header _api.h ou capsule Python n’est admis.

Le propriétaire natif prête un vrai sd_bus direct déjà connecté et en conserve sa référence et l’usage exclusif du graphe fermé. pa01_sysd_open acquiert sa propre référence par sd_bus_ref et la libère par sd_bus_unref ; il n’appelle jamais sd_bus_close, flush ou close_unref. Les bus implicites SD_BUS_DEFAULT* sont refusés. Aucun endpoint, manager, chemin, connexion, RPC, clé ou secret n’est déduit.

open conserve réellement les pidfds self/peer et la référence SDK, puis rapproche UID/EUID/PID du processus, propriétaire thread/processus, socket connecté AF_UNIX/SOCK_STREAM et identité fstat dev/ino, SO_PEERCRED et credentials PID/EUID/PIDFD réellement présents et non augmentés. Les deux pidfds doivent être CLOEXEC et vivants selon poll0. snapshot refait les lectures SDK/socket/pidfds, compare la liaison initiale et relit le bus et le processus avant copie. peer_euid est explicitement la valeur à la connexion ; elle n’est pas présentée comme l’EUID actuel observé dans le processus pair.

Les fonctions C publiques au seul graphe natif utilisent des types scalaires/void* dans leurs headers générés, sans type interne du .c : pa01_sysd_open(out,bus,deadline_ns,stage,native_code,cleanup_errno), pa01_sysd_snapshot(state,facts,facts_len,stage,native_code,cleanup_errno) et pa01_sysd_close(inout,stage,native_code,cleanup_errno). facts_len doit valoir7 : self_pid,self_uid,self_euid,peer_pid,peer_euid_at_connect,observed_monotonic_ns,end_ns. Aucun numéro de pidfd/socket, pointeur SDK ou objet Python n’est retourné. Un tampon de longueur incorrecte n’est pas écrit ; un tampon valide est effacé avant refus.

CLOCK_MONOTONIC, échéance explicite, égalité, débordement et régression sont vérifiés à chaque étape ; le premier statut d’échec reste distinct du code natif signé et du premier errno de nettoyage. Statuts locaux :0OK,1ARGUMENT,2MEMORY,3CLOCK,4STATE,6EXPIRED,7VERIFY,8IO,10CLEANUP. Les étapes sont1horloge,2socket,3pidfd self,4credentials SDK,5pidfd peer,6liaison/arguments et7nettoyage. Un échec de snapshot reste sticky ; un appel mal formé ou d’un autre thread ne rend pas favorable l’état de l’owner. Après fork, snapshot/close refusent avant tout SDK et conservent la sortie héritée ; le propriétaire doit faire terminer son enfant sans réutilisation de cet état.

Les opérations sont locales synchrones, sans phase PENDING ou quiescence fictive. Les sorties éventuellement allouées malgré une erreur SDK restent suivies et nettoyées. Les FD propres sont consommés une fois selon Linux, sans retry close/EINTR ; une erreur de nettoyage ne produit aucun snapshot positif. close permet le nettoyage connu après expiration, préserve et retourne la première erreur sticky, puis met la sortie àNULL après consommation des ressources ; une sortie NULL n’est pas une identité ou admission validée. Les latences et préemptions internes des syscalls/libsystemd restent à qualifier ; aucun délai physique strict n’est affirmé.

Ces faits SELF/PEER_AT_CONNECT ne prouvent ni le rôle manager, l’unité/MainPID/InvocationID, les artefacts chargés, la politique/époque/installation/cible, UTC, la provenance host+tpm2 du credential ou la garde/remise D13. Leurs raccords positifs restent à réaliser. Les recettes préparées utilisent un SDK simulé et des sockets/pidfds locaux, sans daemon ni credential réel ; elles ne qualifient pas l’identité forte ou l’autorité.

Références publiques de conception : https://www.freedesktop.org/software/systemd/man/257/sd_bus_get_owner_creds.html et https://www.freedesktop.org/software/systemd/man/257/sd_bus_ref.html. Les lectures de documentation ne constituent pas une vérification de l’ABI runtime installée.


## D14 PA — constructeur de connexion locale propre, sources seules

Le complément de systemd_observation.pyx ajoute pa01_sysd_conn_start/step/snapshot/close : capacités C opaques distinctes de l’observation. Les deux familles OBS/CONN sont reconnues avant accès aux layouts/SDK ; ces tags préviennent une confusion de type et ne prouvent aucune autorité. Le guard embarqué de connexion sert seulement budget/owner/diagnostic, jamais d’observation substituée. Le graphe reste System seul, sans capsule/API Python ni getter SDK.

Le chemin C fourni explicitement doit être absolu/canonique, sans NUL interne, contrôle ou segment vide/dot/dotdot, et borné par le vrai sockaddr_un. Sa longueur exclut le NUL ajouté localement. Aucun endpoint, environnement, bus implicite, mode/binaire ou dépendance nouveau n’est choisi. start crée son socket AF_UNIX/SOCK_STREAM NONBLOCK+CLOEXEC et appelle connect une fois ; EINPROGRESS conserve une progression, EAGAIN et les autres erreurs ne sont pas rejoués. step CONNECT utilise poll0 puis SO_ERROR/getpeername/identité avant configuration SDK.

Le succès réel de sd_bus_set_fd transfère immédiatement la propriété du FD avant tout contrôle ultérieur ; son échec laisse notre FD suivi. Le SDK neuf est explicitement direct client-bus0/server0, anonymous0, interactive0, exit-on-disconnect0, close-on-exit1, avec négociation FD et credentials PID/EUID/PIDFD. Aucun callback applicatif ni RPC métier n’est installé. La connexion propre peut fermer son SDK ; l’observation sur un bus emprunté ne libère toujours que sa propre référence.

L’authentification avance avec au plus un sd_bus_process par step. Après un retour0, elle attend seulement poll0 ou le timeout SDK absolu CLOCK_MONOTONIC en microsecondes, converti sans débordement ni ajout à now et borné par le budget PA original. Un timer SDK échu peut faire avancer le SDK tant que PA reste valide. 5PENDING est normal ; aucun sd_bus_wait bloquant, boucle interne d’attente ou réarmement. La cadence et les latences du futur propriétaire restent à qualifier.

READY exige vraie observation fille et relectures du socket initial/final, des faits et du budget/owner. snapshot utilise un tampon local et copie facts7 seulement après le dernier contrôle. Le premier statut/code/cleanup reste conservé. close détache réellement la fille avant de fermer notre seul bus et FD restant ; un lien non libéré conserve la capacité. Les FD sont consommés une fois, sans double close ; les limites du cleanup SDK selon son API restent à qualifier. Après fork ou mauvais thread, step/snapshot/close refusent avant SDK et conservent la sortie.

Les faits restent SELF/PEER_AT_CONNECT : aucun manager/unité/MainPID/InvocationID, artefact, politique/UTC ou guardian D13 ne devient prouvé. Le profil d’endpoint et son propriétaire protégé restent à raccorder. Les recettes utilisent SDK simulé et sockets locaux de test, sans qualification du protocole réel. Aucun test, syntaxe/compilation/import produit, connexion actuelle, secret, SQL, clé ou TPM/NV n’est exécuté par cette inscription.

Les primitives de temps/événements sont documentées dans https://www.freedesktop.org/software/systemd/man/257/sd_bus_get_timeout.html ; propriété et progression dans sd_bus_set_fd/sd_bus_process v257. Leur lecture ne vérifie pas l’ABI runtime installé.


## E5 — Échanges techniques 1.1 et retour du plan avant confirmation

Le lot documentaire commun C08/PA01 a été validé humainement par la réponse
« Valider le lot documentaire commun » à
call_0ef16343f01847f698d3411cb89b5cd3/0. La transcription coordonnée couvre
treize documents C08 et les quatre documents PA01. Son écriture ne livre
aucun codec, handler, transport, autorité, effet PostgreSQL ou recette.

Les profils 1.0.0 existants MUST rester inchangés et explicitement distincts
du profil 1.1.0 ci-dessous. Une enveloppe 1.1 non liée ou invalide MUST NOT
être convertie ou acceptée en 1.0. Le catalogue logique conserve exactement
les trois noms, version 1.0.0 et classes déjà adoptées. TechnicalPlan 1.0.0,
ses octets canoniques et son digest propre MUST rester inchangés.

### Enveloppe de requête 1.1 fermée

Champs communs exacts : schema, schema_version, purpose, request.
schema vaut pixs.agent.postgresql.exchange.request ; schema_version vaut
1.1.0 ; request est le NativeRequest 1.0.0 existant, sans modification.

| purpose | catalog_operation interne | Champs supplémentaires exacts |
| --- | --- | --- |
| OBSERVE | inspect_postgresql | Aucun. |
| PREPARE_PLAN | inspect_postgresql | projection_document, projection_binding, confirmation_ref. |
| PREPARE | prepare_postgresql | Aucun. |
| READ_RESULT | get_postgresql_result | Aucun. |

Les params internes 1.0.0 restent fermés : inspect {}, prepare triplet du
plan, get_result operation_ref. Le purpose MUST correspondre à l'opération
et au mandat courant ; aucune classe reçue ne devient une permission.
projection_document est la publication C08 canonique 1.0.0 exacte,
projection_binding son ContentBinding vérifié ; confirmation_ref est
préallouée et MUST NOT être traitée comme consentement.

Le mandat initial 1.1 conserve domain PA_POSTGRESQL_INITIAL et les champs
communs E4, avec schema_version 1.1.0, catalog_version 1.0.0 et préfixe signé
PIXS:PA:POSTGRESQL:INITIAL:1.1.0 suivi de LF. Son UNIQUE request_digest MUST
engager tous les octets canoniques de l'enveloppe 1.1 entière, jamais la
seule requête interne. inspect a les claims exacts purpose ; get_result
conserve operation_ref. prepare a les claims exacts projection_binding,
observation_binding, plan_binding, preconditions_binding,
confirmation_binding, effects_binding, effects_digest. Toute liaison,
signature, politique, révocation, validité, cible et identité MUST être
vérifiée par son propriétaire courant ; aucune autorité n'est livrée ici.

### Enveloppe de réponse 1.1 fermée

Champs exacts : schema, schema_version, purpose, result, payload.
schema vaut pixs.agent.postgresql.exchange.response ; schema_version vaut
1.1.0 ; result est le NativeResult 1.0.0 existant. purpose MUST correspondre
à l'appel réellement traité. payload MUST être {} hors phase SUCCEEDED.

En SUCCEEDED, OBSERVE a exactement observation_document et
observation_binding ; PREPARE_PLAN a exactement planning_bundle et
planning_binding ; PREPARE et READ_RESULT ont {}. Une réponse positive MUST
porter les références durables exigées par NativeResult ; le résultat de
planning conserve l'opération de lecture et le triplet du plan retourné.
Ses observation_refs MUST inclure la référence du manifeste lié.
SUCCEEDED de planning ne prouve aucun effet de préparation ou commit métier.

Les documents suivants sont JSON UTF-8 à champs fermés, clés triées et
séparateurs compacts, avec types exacts. Les références, listes, documents et
octets MUST respecter des bornes positives strictes du profil protégé
explicitement fourni ; aucun plafond de production implicite n'est choisi.
Les versions de binding sont projection=1.0.0, observation=1.0.0,
préconditions=1.0.0, effets=1.0.0, planning=1.0.0,
confirmation=1.0.0 ; plan=plan_version opaque existant. Une nouvelle
publication immuable MUST avoir une nouvelle référence, sans réécriture des
mêmes ref/version sous un autre hash. Les preuves, temps et profils gardent
leurs versions propriétaires explicitement supportées, jamais devinées.

### Observation publique 1.0.0

schema vaut pixs.agent.postgresql.observation_manifest ; schema_version
vaut 1.0.0. Champs exacts : schema, schema_version, observation_ref, inspection_operation_id, installation_ref, target_ref, policy_ref, policy_version, profile_bindings, resources, observed_at, time_evidence_binding.

inspection_operation_id MUST identifier l'appel OBSERVE producteur, pas le
planning ou la préparation future. profile_bindings a exactement runtime,
service, role et database, chacun ContentBinding. ref/version MUST
correspondre aux profils de la projection ; sha256 désigne les octets du
profil protégé réellement utilisé, dont le contenu privé n'est pas transmis.
Aucune valeur secrète ou empreinte de valeur de credential n'entre dans ces
profils/bindings. Un éventuel document public expurgé MUST avoir son identité
et binding distincts avec liaison propriétaire explicite, jamais le même
ref/version et un hash substitué.

resources est une liste de cinq entrées uniques dans l'ordre SOFTWARE,
CLUSTER, SERVICE, ROLE, DATABASE. Chaque entrée a exactement kind,
resource_ref, state, match, evidence_binding. Les références SOFTWARE et
CLUSTER sont résolues par le profil service ; les références SERVICE/ROLE/
DATABASE correspondent aux ressources de la projection. L'état SERVICE est
ABSENT, STOPPED, RUNNING ou UNOBSERVABLE ; les autres ont ABSENT, PRESENT ou
UNOBSERVABLE. match est MATCH, MISMATCH ou UNDETERMINED. UNOBSERVABLE MUST
impliquer UNDETERMINED et MUST NOT devenir ABSENT. L'absence d'unité ne prouve
ni absence de logiciel ni absence de cluster. Les preuves de chaque entrée,
y compris indisponibilité, sont des ContentBinding non nuls de sources
propriétaires ; aucune donnée privée brute n'est rendue.

observed_at est UTC à six décimales exactes, sans conversion. Le
time_evidence_binding non nul lie la preuve temporelle propriétaire ;
observed_at seul MUST NOT prouver fraîcheur. Projection et planning
réutilisent ce document immuable après vérification propriétaire actuelle ;
une simple progression d'horloge ne réécrit pas observed_at. Âge, validité,
autorité, politique, temps et réalité technique MUST être recontrôlés
séparément. Une divergence impose nouvelle observation/projection/plan
plutôt qu'adoption silencieuse ; aucun producteur de preuve n'est supposé.

### Préconditions publiques 1.0.0

schema vaut pixs.agent.postgresql.preconditions_manifest ; schema_version
vaut 1.0.0. Champs exacts : schema, schema_version, preconditions_ref, installation_ref, target_ref, operation_id, projection_binding, observation_binding, resource_guards, conditions.

resource_guards contient exactement cinq entrées kind, resource_ref,
profile_binding pour les cinq ressources, jamais une liste vide. Elles
imposent les vérifications natives actuelles de cible/profil/conformité selon
la phase et les actions, avant chaque effet et avant SUCCEEDED, même pour
REUSE et allowed_effects=[] ; aucune boucle vide ne vaut conformité.
Avant SERVICE_START, ROLE/DATABASE UNOBSERVABLE ne sont tolérés que couverts
par une condition différée valide ; identité/cible/profil/politique restent
courants. Après démarrage, les lectures requises sont obligatoires avant
chaque CREATE ; conformité réelle complète est exigée avant SUCCEEDED.

conditions est une liste ordonnée bornée sans doublon condition_ref.
Champs exacts d'une condition : condition_ref, resource_kind, resource_ref, profile_binding, effect, check_stage, expected_state, expected_match, evidence_binding.
La couverture complète des conditions requises est dérivée par PA des
actions/effets/profils ; un client MUST NOT la supprimer par liste vide.
conditions peut être vide seulement sans effet, les cinq resource_guards et
la garde finale restant obligatoires. effect appartient à allowed_effects ;
resource_kind désigne l'une des cinq ressources. check_stage vaut exactement
BEFORE_EFFECT ou AFTER_SERVICE_START_BEFORE_EFFECT. expected_state suit le
domaine de la ressource ; expected_match suit MATCH/MISMATCH/UNDETERMINED
et ne dispense aucune vérification actuelle.

evidence_binding est la seule valeur nullable de ces nouveaux manifestes.
null est admis seulement pour une condition ROLE/DATABASE actuellement
UNOBSERVABLE, check_stage AFTER_SERVICE_START_BEFORE_EFFECT, effet
ROLE_CREATE/DATABASE_CREATE et SERVICE_START explicitement planifié avant.
La preuve réelle d'ABSENT est alors obligatoire juste avant le CREATE.
CLUSTER_INITIALIZE exige également absence réelle du cluster, jamais
inférée de l'unité ou du logiciel. Écart ou incertitude MUST arrêter le
reste, conserver les effets connus inspectables et MUST NOT convertir
CREATE en REUSE ou déclencher une compensation destructive. La progression
prévue ne réécrit pas le plan confirmé ou ses bindings signés.

### Effets et bundle de planning publics 1.0.0

Le manifeste d'effets a schema pixs.agent.postgresql.effects_manifest,
schema_version 1.0.0 et les champs exacts : schema, schema_version, effects_ref, installation_ref, target_ref, operation_id, projection_binding, allowed_effects.
allowed_effects est la copie ordonnée exacte de la projection. Seuls les
effets PA01 sélectionnés sont admis ; Docker/INITIALIZE_START/RECREATE/
DATABASE_DROP restent exclus de ce lot. effects_binding.sha256 engage le
document entier ; effects_digest reste le SHA-256 du seul tableau canonique
allowed_effects 1.0.0. Ces deux empreintes MUST NOT être confondues.

Le bundle de planning a schema pixs.agent.postgresql.planning_bundle,
schema_version 1.0.0 et les champs exacts : schema, schema_version, bundle_ref, installation_ref, target_ref, planning_operation_id, preparation_operation_id, correlation_id, projection_document, projection_binding, observation_document, observation_binding, plan_document, plan_binding, preconditions_document, preconditions_binding, effects_document, effects_binding, effects_digest.
Chaque document MUST correspondre à son binding, aux références communes et
à son propriétaire. plan_document est TechnicalPlan 1.0.0 inchangé ;
plan_binding.version vaut plan_version. planning_binding engage le bundle
entier avec ref=bundle_ref et version 1.0.0, sans auto-binding à l'intérieur.
Seules les métadonnées immuables du plan sont persistées sous inspect :
aucun effet PostgreSQL, NV_Extend ou consommation d'un mandat Critique.

### Opérations, provenance A07 et confirmation acyclique

| Contenu | Opération et invocation de provenance |
| --- | --- |
| NativeRequest/NativeResult | Appel courant et son invocation A07 réelle. |
| Observation.inspection_operation_id | Appel OBSERVE producteur. |
| planning_bundle.planning_operation_id | Appel PREPARE_PLAN courant. |
| Projection.operation_id, TechnicalPlan.operation_id, confirmation.operation_id | Même préparation future, distincte des deux lectures. |
| Lecture de résultat | Nouvelle opération READ_RESULT ; subject_operation_ref vise la préparation. |

Chaque mandat 1.1 MUST comparer invocation_ref/correlation_ids/causation_ids
aux tableaux complets de sa propre invocation réelle, ordre et doublons
conservés. Les tableaux de la projection 1.0 déjà publiée gardent strictement
leurs octets et provenance ; ils MUST NOT être réécrits pour les égaler à
OBSERVE, planning ou future exécution. Bindings et opérations distinctes
relient les contenus. Le correlation_id scalaire du plan/parcours reste
rapproché selon les contrats existants ; il ne remplace aucun tableau A07.

C08 possède le seul bundle technique de confirmation :
schema pixs.c08.postgresql-confirmation.v1, schema_version 1.0.0 ;
champs exacts schema, schema_version, confirmation_ref, installation_ref,
target_ref, operation_id, operator_ref, projection_binding,
observation_binding, plan_binding, preconditions_binding, effects_binding,
policy_ref, policy_version, confirmed_at, correlation_id. Ce NOUVEAU format
ne porte pas les deux tableaux redondants A07 ; aucun format 1.0 existant
n'est altéré. confirmed_at est UTC6 exact. Pas de confirmed=true, signature,
hash de futur mandat, secret ou contexte critique futur inventé.

C08 MUST présenter projection/plan/préconditions/effets exacts avant le
consentement. Puis un NOUVEAU mandat Critique signé 1.1 engage tous les
bindings et les tableaux A07 de son invocation critique réelle. Une
confirmation_ref préallouée, signature de lecture, référence, digest ou
métadonnée MUST NOT devenir autorité de préparation. Projection sans plan
futur/confirmation, plan sans digest du futur bundle, confirmation sans
acte/signature/digest du futur mandat maintiennent un graphe acyclique.
Une réponse perdue ou métadonnée manquante/divergente ferme la résolution
ou impose nouvelle planification ; aucun droit Critique n'est restauré.

Ce lot ne produit aucun Subject/CommandMetadata métier pré-PG, aucun mapping
de génération Agent, conversion de dates ou nouveau canal/endpoint/opération.
Les propriétaires natifs, résolveurs, transport, handlers, persistance et
preuves restent à réaliser/qualifier avant activation. L'adoption
documentaire et les empreintes ne sont pas une validation produit.


## D14 lookup readonly — 4 API C-only, sources seules

`pa01_sysd_lookup_start(void**,void*,size_t max_path,size_t max_unit,uint32_t*,int*,int*)`, `pa01_sysd_lookup_step(void*,uint32_t*,int*,int*)`, `pa01_sysd_lookup_snapshot(void*,char*,size_t,char*,size_t,uint8_t*,uint64_t*,uint32_t*,int*,int*)` 10 args, `pa01_sysd_lookup_close(void**,uint32_t*,int*,int*)`. C-only opaque, sans pointeur Python, sans capsule/getter SDK.

Production décrite par API publiques et ressources réellement détenues dans `PA01SOLookup` : slot annulable, référence propre au reply emprunté, pidfd/namespaces/bail/deadline, message relâché selon contrat SDK. Héritage deadline/bail exclusif du parent : un seul pending par bus, `start` 5 sans envoi, `SETUP` 5 avec un seul envoi, `DONE` 0 ou erreur terminale stable, `snapshot` avant `DONE` 4, caps petites après `DONE` 1 puis lecture normale encore 0. Appels readonly `GetUnitByPIDFD` SELF seuls, destination NULL, `auto_start` 0, `allow_interactive` 0, `floating` 0, `h` seul. Namespace SELF/PEER vérifié par API ioctl publiques et `fstat` dev/ino. Aucun layout SDK inventé, aucune rétention interne précise du message query revendiquée.

Paragraphe TEST distinct, non exécuté/non qualifiant : détails simulés `m->fd`, `query/refcount/delivered`, modes namespace 1/2/3, compteurs vivants et fixtures `test.service/path/iid16`. Contrat de source écrite seul, aucune observation du vrai manager revendiquée. Pas manager/MainPID/artefacts/politique/UTC/gardien D13/autorité. SDK simulé ne qualifie pas systemd réel. M1 reste proposition Z12 sans adoption PA, non barrière au lookup indépendant.


## Bootstrap B — obligations avant code
Vérification publique de la source installée, des formes et signatures et de l’histoire d’abord, avec scanner dispatch bootstrap+PG et cohérence calculée des liens tête/NV attendu/contexte/époque/génération ; puis capacité strictement privée de vérification par lecture sous D13/D14, contextes et budgets actuels, non utilisable dans les constructeurs d’intention ni dans les consommateurs Extend, sans secret rendu au code Python ou au réseau ; lecture HMAC courante et rapprochement ; puis seulement admission selon l’opération réellement autorisée : la configuration B exige origine installée, signature admin avec pin et domaine, contexte, politique, temps et provenance selon son contrat, sans mandat E4, sans confirmation C08, sans droit NV, SQL ou retrait ; les opérations PG et administratives conservent séparément leurs contrôles propres, leur confirmation et leurs droits actuels lorsqu’ils sont requis ; la capacité privée de vérification ne délivre aucun de ces droits. Les invariants d’admission décrivent le runtime recevant un R0 préexistant ; la création initiale de R0 et les opérations matérielles INIT demeurent exclusivement extérieures sous leur plan exact, sans exiger une publication FIN future avant sa propre production. Aucun enforcement prétendu déjà réalisé par le garde TCTI. L’append puis le fsync précèdent toute Extend autorisée, recontrôle courant juste avant, HMAC de confirmation avant retrait prouvé. Tous formats détaillés des brouillons restent NON adoptés ; aucun codec B livré. Le contrôle de type actuel garantit seulement le rejet par ce décodeur PG lorsqu’il est atteint (`PA01_JOURNAL_SCHEMA_INVALID`), sans universel ni B sûr. Fermeture obligatoire avant code B : wire, profils, séquences, retrait, admission ordinaire, migration, refus legacy. Aucun chiffre, champ ou autorité nouveaux implicites. Perte d’origine, substitution, deadline, alias ou issue inconnue ferme l’usage ; nettoyage et ressources incertaines conservés sans libération forcée ni rejeu.


## Retrait — règles normatives et refus
Signatures et domaines adoptés : `withdraw_initial_authority`, domaine `PA_POSTGRESQL_WITHDRAWAL`, classe `Critique`, validité UTC finie bornée par profil protégé, consommation unique anti-rejeu. Formats détaillés de données, scanner, résolveur et preuves proposés dans le lot complet à valider humainement ; sources, résolveurs et preuves natives à réaliser puis qualifier, sans code B autorisé ; aucun format bootstrap PG1.0 modifié, aucune opération PG ni `get_result` pour l'admin. Époque et génération configurées par profil conservées ; leur CHANGEMENT et MIGRATION non adoptés sont refusés.
Dans la branche initiale après retrait : nouvelles préparations interdites ; inspection et réconciliation courantes permises selon droits, remise minimale PBO canonique conservée ; management ordinaire seulement après vraies preuves. Garde : vérification publique de la source installée, des formes et signatures et de l’histoire d’abord, avec cohérence calculée des liens tête/NV attendu/contexte/époque/génération ; puis capacité strictement privée de vérification par lecture sous D13/D14, contextes et budgets actuels, non utilisable dans les constructeurs d’intention ni dans les consommateurs Extend, sans secret rendu au code Python ou au réseau, sans exiger une ancre HMAC avant la lecture qui la produit ; lecture HMAC courante et rapprochement ; puis seulement append local, remise ou effet selon la branche et ses droits actuels, avec signature et clé, politique, révocation, UTC, confirmation, identité, cible et contexte courants. Aucun enforcement prétendu déjà réalisé par le garde TCTI. Sous quiescence et fencing, append du canonical intent puis fsync ; recontrôle courant juste avant une Extend autorisée ; confirmation HMAC actuelle avant retrait démontré et résultat. Jamais d’ancrage futur requis pour son propre append. Histoire initiale distincte de l’autorisation actuelle : l’initial n’est jamais rouvert et l’ordinaire exige ses preuves actuelles indépendantes après les deux retraits PA et Z12. Inconnu bloque : inspection et rapprochement du même intent, jamais rejeu `NV_Extend` automatique. `RETIRED` déclaratif n’est aucune preuve et n’autorise rien. Nettoyage et ressources incertaines conservés sans libération forcée ni rejeu.


## Contrat administratif retrait/inspection v3.1

Famille PA_POSTGRESQL_WITHDRAWAL. Deux opérations admin uniquement :
withdraw_initial_authority classe Critique, inspect_initial_authority
classe Protégé. Les 3 opérations PG restent inchangées. schema_version et
catalog_version valent 1.0.0. Octets à signer : préfixe ASCII exact
PIXS:PA:WITHDRAWAL:MANDATE:1.0.0 suivi d'un unique LF pour le retrait,
PIXS:PA:INSPECTION:MANDATE:1.0.0 suivi d'un unique LF pour l'inspection,
puis JSON canonique UTF-8 sans LF final. Canon exact :
json.dumps(ensure_ascii=False,allow_nan=False,sort_keys=True,separators=(",",":")).
Domaine, opération, classe, préfixe et types couplés ; toute
interchangeabilité avec PG, adminB ou R01 est refusée. Forme seulement :
aucune preuve d'identité, autorisation, fraîcheur, révocation ou effet.
Politique, temps, révocation et effets relèvent du vérificateur et des
propriétaires serveurs.

Source publique : 4 types AdminRequest, AdminMandate (27 champs fermés),
SignedAdminMandate, WithdrawalClaims ; ContentBinding importé de
postgresql_contracts avec PayloadLimits et MandateLimits, jamais
réinventé. Source à compiler Cython dans le graphe System avant
distribution ; compilation non branchée ici. Aucune promesse de
qualification.

AdminRequest 10 champs fermés : schema_version, catalog_operation,
catalog_version, operation_id, idempotency_key, correlation_id,
installation_ref, target_ref, mandate_ref, params tuple trié, fil objet
fermé. Retrait params vide seul. Inspection params vide (état
installation et cible) ou subject_operation_ref seul (résultat
d'opération retrait). correlation_id reste trace. WithdrawalClaims 3
champs fermés : plan_binding, confirmation_binding, proofs_binding, tous
ContentBinding opaques pour le livrable suivant. AdminMandate 27 champs
fermés : schema_version, domain, mandate_ref, invocation_ref,
operator_ref, operator_key_ref, policy_ref, policy_version,
installation_ref, target_ref, caller_terminal_ref, executor_terminal_ref,
pzt_relation_ref, catalog_operation, catalog_version, criticality,
operation_id, idempotency_key, correlation_id, correlation_ids tuple,
causation_ids tuple, issued_at, not_before, expires_at, request_digest,
anchor_binding, claims. Références UTF-8 non vides, sans ASCII inférieur
à 32 ni 127, bornées par le profil. Digest hexadécimal minuscule 64.
Traces ordre et doublons conservés, correlation_id membre. Temps UTC6
avec calendrier réel et ordre issued <= not_before < expires.
request_digest = SHA256 de la requête entière encodée par
encode_admin_request. Retrait : anchor_binding ContentBinding
obligatoire, claims WithdrawalClaims. Inspection : anchor_binding None
null obligatoire, claims None null obligatoire. Enveloppe exacte
document et signature_b64 de 88 caractères canoniques pour 64 octets
Ed25519 pure sans préhash. claims None vaut null jamais objet vide.
Nombres, booléens, flottants et constantes refusés. Profils serveur
explicites obligatoires, plafonds charge utile incluant les octets
signés. Fonctions : encode_admin_request(AdminRequest,PayloadLimits)->str,
decode_admin_request(str,PayloadLimits)->AdminRequest,
encode_admin_mandate(AdminMandate,MandateLimits)->str,
decode_admin_mandate(str,MandateLimits)->AdminMandate,
admin_signed_bytes(AdminMandate,MandateLimits)->bytes,
encode_signed_admin_mandate(SignedAdminMandate,MandateLimits)->str,
decode_signed_admin_mandate(str,MandateLimits)->SignedAdminMandate,
match_admin_request_mandate(AdminRequest,AdminMandate,MandateLimits)->None
ou AdminContractError de forme.


## Résultat administratif v3 (représentation seule)

Famille PA_POSTGRESQL_WITHDRAWAL. Deux opérations admin uniquement :
withdraw_initial_authority classe Critique, inspect_initial_authority
classe Protégé. Les 3 opérations PG restent inchangées. schema_version et
catalog_version valent 1.0.0. Canon exact :
json.dumps(ensure_ascii=False,allow_nan=False,sort_keys=True,separators=(",",":")),
sans LF. Domaine, opération, classe et types couplés ; interchangeabilité
PG/adminB/R01 refusée. Forme seulement, sans preuve ni effet.

AdminResult, 18 champs fermés comptés réels : schema_version,
catalog_operation, catalog_version, operation_id, subject_operation_ref,
invocation_ref, correlation_id, correlation_ids tuple, causation_ids
tuple, installation_ref, target_ref, mandate_ref, phase
(RECEIVED/RUNNING/SUCCEEDED/FAILED/IN_DOUBT/BLOCKED de l'opération
courante), observed_state
(UNKNOWN/UNAVAILABLE/NON_OBSERVABLE/INITIAL_ACTIVE/PENDING/WITHDRAWN_DECLARED),
subject_outcome (null ou
UNKNOWN/NOT_WITHDRAWN/WITHDRAWN_DECLARED/FAILED/IN_DOUBT/BLOCKED),
observed_at UTC6 ou null, proof_bindings tuple immuable de
ContentBinding opaque (fil tableau JSON, maximum
limits.payload.max_observation_refs), diagnostic_code ou null.
Références UTF-8 non vides sans ASCII<32/127 bornées profil ; digest 64
hex minuscule ; traces ordre/doublons réels conservés, correlation_id
membre, invocation_ref du contexte courant obligatoire.

Retrait : subject_operation_ref égale operation_id, subject_outcome null
dans toutes ses phases ; SUCCEEDED retrait impose WITHDRAWN_DECLARED +
temps valide + preuves non vides. Inspection état (params vide) : sujet
null/null. Inspection op (params subject_operation_ref) : sujet exact du
param, issue non-nulle dans tout l'enum y compris FAILED. Global non
observable : observed_at null, preuves vides, phase jamais SUCCEEDED ;
RECEIVED/RUNNING admis sans diagnostic, FAILED/IN_DOUBT/BLOCKED
diagnostic obligatoire. Global observable : temps valide et preuves non
vides, données à prouver hors codec ; IN_DOUBT peut garder un état
retiré observé sans admission ordinaire. Inspection SUCCEEDED admet
sujet UNKNOWN/FAILED/autre sans mutation implicite ; le codec ne change
jamais l'issue par la phase. APIs : encode_admin_result,
decode_admin_result, match_admin_result_request(result,request,limits)
sous MandateLimits avec limits.payload, retour None ou
AdminContractError. match compare schéma, catalogue, op, operation_id,
install, target, corr, mandate_ref et sujet exact ; contexte A07 réel
complet à rapprocher par le propriétaire futur. Plan/confirmation/preuves
internes opaques au prochain livrable.


### D14 MainPID C-only — pa01_sysd_mpid_start/step/snapshot/close

APIs exactes :
`uint32_t pa01_sysd_mpid_start(void **out, void *lookup_done, uint32_t *stage, int *code, int *cleanup);`
`uint32_t pa01_sysd_mpid_step(void *state, uint32_t *stage, int *code, int *cleanup);`
`uint32_t pa01_sysd_mpid_snapshot(void *state, uint32_t *main_pid, uint8_t *invoc16, uint64_t *observed_ns, uint32_t *stage, int *code, int *cleanup);`
`uint32_t pa01_sysd_mpid_close(void **state, uint32_t *stage, int *code, int *cleanup);`

- C-only opaque, 5 appels readonly réellement adoptés sur connexion directe existante, destination NULL, aucun nom de bus découvert : Properties.Get(Service.MainPID) variant u ; Manager.GetUnitByPIDFD(main_pidfd) ; Manager.GetUnitByPIDFD(self_pidfd) ; relecture Properties.Get(Service.MainPID) ; Properties.Get(Unit.InvocationID) variant ay16.
- Snapshots après DONE seul, sans autorité D13/manager/policy/UTC ; bail réel parent sur lookup DONE/connexion, refus parent busy sans poison.
- MainPID 0 refusé ; cohérence exigée MainPID/self/unité/path/IID, pidfd/ns/horloge/owner, diagnostics cleanup sticky.
- Budgets du parent, progression unitaire ; profil D14 déjà adopté, aucun nouveau seuil/provider/preuve positive.
- Recettes SDK simulées à écrire puis exécuter phase2 LXC, aucune qualification réelle.


### Clarification composition admin — D8 PA01 / D9 déjà adoptés

Le codec `admin_withdrawal_contracts` est structurel/public, sans autorité. D8 PA01 déjà adopté = initialisation/chargement du runtime dans le lanceur ; le D8 résolveur TLS concerne Z12, hors périmètre, non repris ici. D9 composition déjà adoptée conservée. Quand la source admin figure dans l'inventaire fermé, chaque rôle effectivement déclaré doit être couvert par le `postgresql_contracts` canonique plat du même inventaire, modules canoniques uniques, `operations=()` pour l'admin, sans dépendance cachée, sans 5e binaire ni opération nouvelle. Cette fermeture et l'import builtin explicite ne qualifient ni origine des artefacts, ni identité/politique/autorité courante. Garde `_api.h` limitée aux privés adoptés, étendue au seul `systemd_observation.pyx` omis dans linker.


### Codec Observation publique 1.0.0

Module canonique `src/pixs/pa_native/postgresql_observation.py`, dépendance
publique PG `ContentBinding/PayloadLimits` (import package/builtin style
admin, aucun validateur privé). DTO gelés `slots repr=False`
`ObservationProfileBindings/ObservationResource/ObservationManifest`.
Erreur publique `ObservationContractError(ValueError)` ; `ContractError` PG
importé seulement comme cause précise si `ContentBinding` public refuse
après validation locale. API `encode_observation(value,PayloadLimits)->str`,
`decode_observation(text,PayloadLimits)->ObservationManifest`,
`observation_binding(value,PayloadLimits)->ContentBinding(ref=observation_ref,
version="1.0.0",sha256=SHA256(canon))`. Version manifeste `1.0.0` fixée ;
versions preuves/profils opaques préservées. Limites = `max_json_bytes` /
`max_ref_bytes` explicites ; listes normatives 4 profils / 5 ressources ;
`max_observation_refs` non recyclé. Canon trié compact
`ensure_ascii=False allow_nan=False`. Decode fermé : clés/duplicats/
nombres/coercions/nulls/UTF-8/UTC6/état-match/ordre/bindings obligatoires,
diagnostics sans contenu. Forme et octets seulement.


### E5-COMP — composition PG/observation
- Garde `_check_observation_composition(records)` analogue admin sur
  métadonnées : source unique `src/pixs/pa_native/postgresql_observation.py`,
  `module_name postgresql_observation` unique, `operations()` vide ; PG
  unique `src/pixs/pa_native/postgresql_contracts.py` /
  `module_name postgresql_contracts` ; `executables` PG couvrent chaque
  `executable` déclaré du codec. Défaut => `ProfileError`
  `PA01_OBSERVATION_COMPOSITION_INCOMPLETE`.
- Rôles = `records.executables`, pas profils DTO `runtime/service/role/database`.
- Appels effectifs dans `_checked_records` et validation `builder` avant
  outil via imports partagés comme admin ; même PG unique => union auto-couverte.


### E5-EFF — effets 1.0.0 (codec seul)
- `EffectsManifest` 8 champs exacts : schema, schema_version, effects_ref,
  installation_ref, target_ref, operation_id, projection_binding,
  allowed_effects. `projection_binding.version==1.0.0` connue.
- Six fermés ordre canonique sans doublon :
  SERVICE_INSTALL/SERVICE_CONFIGURE/CLUSTER_INITIALIZE/SERVICE_START/ROLE_CREATE/DATABASE_CREATE ;
  DATABASE_DROP/Docker/RECREATE exclus. Vide admis comme FORME sans admission.
- `effects_binding.sha256` = SHA document entier ; `effects_digest` = SHA seul
  tableau canonique `allowed_effects` après validation document+budget JSON.
- Binding propre version `1.0.0` recontrôlé sous `max_ref_bytes`, autres versions
  opaques au bon schéma. `PayloadLimits` direct, `max_observation_refs` non consommé.
- Aucun cross/owner ici. Cross `service_start_planned`/map NON adopté.


### E5-PRE — préconditions 1.0.0 (codec seul)
- Module canonique `src/pixs/pa_native/postgresql_preconditions.py`, dépendance publique PG `ContentBinding/PayloadLimits` direct (import package/builtin style observation/effets, aucun validateur privé). DTO gelés `slots repr=False` `PreconditionsLimits/ResourceGuard/PreconditionCondition/PreconditionsManifest`.
- Erreur publique `PreconditionsContractError(ValueError)` ; `ContractError` PG importé seulement comme cause précise si `ContentBinding` public refuse après validation locale. API `encode_preconditions(value,PreconditionsLimits)->str`, `decode_preconditions(text,PreconditionsLimits)->PreconditionsManifest`, `preconditions_binding(value,PreconditionsLimits)->ContentBinding(ref=preconditions_ref,version="1.0.0",sha256=SHA256(canon))`. Version manifeste `1.0.0` fixée ; versions preuves/profils opaques préservées sauf `projection_binding.version==1.0.0` et `observation_binding.version==1.0.0` recontrôlées.
- `PreconditionsLimits` exact : `payload:PayloadLimits`, `max_conditions:int` strict >0 `type is int` non-bool sans défaut. `max_observation_refs` non consommé. `ResourceGuard` exact `kind/resource_ref/profile_binding`. `PreconditionCondition` exact `condition_ref/resource_kind/resource_ref/profile_binding/effect/check_stage/expected_state/expected_match/evidence_binding` seule nullable.
- `PreconditionsManifest` 10 champs exacts : `schema/schema_version/preconditions_ref/installation_ref/target_ref/operation_id/projection_binding/observation_binding/resource_guards/conditions`. `schema=pixs.agent.postgresql.preconditions_manifest`.
- `resource_guards` exactement 5 entrées uniques ordonnées `SOFTWARE/CLUSTER/SERVICE/ROLE/DATABASE`, jamais vide, avant chaque effet et avant SUCCEEDED même REUSE et `allowed_effects=[]`. `conditions` ordre d’entrée conservé avec unicité `condition_ref`, bornée `max_conditions`, vide admise comme FORME sans admission ; le propriétaire exige aucun effet sur vide. `effect` dans 6 fermés `SERVICE_INSTALL/SERVICE_CONFIGURE/CLUSTER_INITIALIZE/SERVICE_START/ROLE_CREATE/DATABASE_CREATE`. `check_stage` exact `BEFORE_EFFECT` ou `AFTER_SERVICE_START_BEFORE_EFFECT`. `expected_state` suit domaine ressource, `expected_match` `MATCH/MISMATCH/UNDETERMINED` sans dispense de vérification actuelle.
- `evidence_binding` null admis seulement pour `resource_kind ROLE/DATABASE`, `check_stage AFTER_SERVICE_START_BEFORE_EFFECT`, effet couplé `ROLE_CREATE/DATABASE_CREATE`. Null local couplé n’établit ni courant ni `SERVICE_START` planifié ; preuve réelle `ABSENT` obligatoire juste avant CREATE. Pas de déduction depuis `expected_state`. Cross `service_start_planned`/map NON adopté ici, à dériver par propriétaire depuis manifestes typés ensuite. La sémantique native — vérifications actuelles cible/profil/conformité avant chaque effet et avant SUCCEEDED — reste obligatoire.
- Limites `max_json_bytes/max_ref_bytes` explicites à chaque encodage/décodage ; listes normatives 5 ressources. Canon trié compact `ensure_ascii=False allow_nan=False`. Decode fermé : clés/duplicats/nombres/coercions/nulls/UTF-8/ordre/bindings obligatoires, diagnostics sans contenu. Forme et octets seulement, aucune autorité/fraîcheur/admission.


### E5-PRE-COMP — composition PG/préconditions
- Garde `_check_preconditions_composition(records)` analogue observation sur métadonnées : source unique `src/pixs/pa_native/postgresql_preconditions.py`, `module_name postgresql_preconditions` unique, `operations()` vide ; PG unique `src/pixs/pa_native/postgresql_contracts.py` / `module_name postgresql_contracts` ; `executables` PG couvrent chaque `executable` déclaré du codec. Défaut => `ProfileError` `PA01_PRECONDITIONS_COMPOSITION_INCOMPLETE`.
- Rôles = `records.executables`, pas profils DTO. Nouveau codec dépend seulement PG, pas observation/effets comme modules.
- Appels effectifs dans `_checked_records` et validation `builder` avant outil via imports partagés comme observation ; même PG unique => union auto-couverte avec admin/observation.


### RSMP-U1 — BOOTSTRAP B UNITÉ1 ADOPTÉE PAR LE DÉVELOPPEUR LE 26 OCTOBRE 2026 — PHASE1 SOURCES AUTORISÉE SOUS MANDATS CAB, SANS ADMISSION RUNTIME NI EFFET MATÉRIEL
- Statut : `ADOPTÉ`. Lot complet B et retrait et option INIT A adoptés par le développeur le 26 octobre 2026 comme spécification, sans port livré ni succès de test. Les mentions proposées et non adoptées ci-dessous décrivent l’état avant l’accord et sont levées uniquement pour les formes corrigées présentées, hors alternatives B/C et hors fonctions nouvelles. Autorisation phase1 sources uniquement, avant compilation et tests LXC ultérieurs ; aucun effet matériel, SQL, secret, clé, installation ou Git. Aucune coche. Préfixes exacts : `PIXS:PA:BOOTSTRAP:PREPUBLICATION:1.0.0` pré pub, `PIXS:PA:BOOTSTRAP:PUBLICATION:1.0.0` fin ; aucun préfixe PG pour B.

#### B-TA — TRUST ANCHOR ADMIN INSTALLÉ HORS CANDIDAT
- `admin_key_ref:str` UTF8 non-vide sans C0/DEL/surrogates, `admin_public_key_hex:str` regex `^[0-9a-f]{64}$` =32o Ed25519, `admin_identity_ref:str`, `admin_key_pin:str` regex `^[0-9a-f]{64}$` `=hexlower(SHA256(admin_public_key_32o))` révisable, `domain:str="PA_ADMIN_INITIAL"`, `version:str` exacte. `MUST` égalité stricte aux attendus installés D14/constats positifs hors codec ; `MUST NOT` choisir clé depuis candidat, aucun `first_head` en TA, aucun hash auto-document, aucune `authValue`/clé privée/PCR/secret.

#### B-NV — PROFIL NV D10 EXISTANT
- Structure `TPMS_NV_PUBLIC` déclarée `nv_anchor.pyx:43` via `TPM2B_NV_PUBLIC.nvPublic`. `nv_index:int` uint `[0x01000000,0x01FFFFFF]`, `nv_attributes:int` uint `[0,0xFFFFFFFF]`, prédicats littéraux : `(attrs & required)==required`, `(attrs & forbidden)==0`, `(attrs & 0xF0)==(TPM2_NT_EXTEND<<4)` ; jamais `attrs==required`. `required` : `TPMA_NV_PLATFORMCREATE/TPMA_NV_POLICY_DELETE/TPMA_NV_AUTHREAD/TPMA_NV_AUTHWRITE/TPMA_NV_WRITTEN`. `forbidden` : `TPMA_NV_CLEAR_STCLEAR/TPMA_NV_ORDERLY/TPMA_NV_READLOCKED/TPMA_NV_WRITELOCKED`. Correspondance `TPMS_NV_PUBLIC` : `nv_name_alg:str="SHA256"=nameAlg`, `nv_data_size:int==32=dataSize uint sans bool`, `nv_authpolicy_hex:str ^[0-9a-f]{64}$=authPolicy 32o`, `nv_name_hex:str ^000b[0-9a-f]{64}$=Name 34o`. `maintenance_p256_ref:str` référence publique protégée à vérifier positivement ; sinon DÉPENDANCE D11 non livrée. Aucun renommage de code historique, aucun nouveau seuil.

#### B-PUB — PRÉPUBLICATION SIGNÉE INDÉPENDANTE, POLITIQUE INSTALLÉE PROTÉGÉE NON SIGNÉE
- Enveloppe `{document:object,signature_b64:str}` fermée. `document` fermé : `object_type:str="pixs.agent.bootstrap_prepublication/v1"`, `schema_version:str="1.0.0"`, `prepublication_ref:str`, `installation_ref:str` exacte, `target_ref:str` exacte sans wildcard, `policy_ref:str`, `policy_version:str`, `admin_key_ref:str`, `admin_public_key_hex:str ^[0-9a-f]{64}$`, `admin_key_pin:str ^[0-9a-f]{64}$`, `domain:str="PA_ADMIN_INITIAL"`, `version:str`, `nv_index:int`, `nv_attributes:int`, `nv_name_alg:str="SHA256"`, `nv_data_size:int==32`, `nv_authpolicy_hex:str ^[0-9a-f]{64}$`, `nv_name_hex:str ^000b[0-9a-f]{64}$`, `maintenance_p256_ref:str`, `valid_not_before_utc6:str`, `valid_not_after_utc6:str` fenêtre finie bornée profil avec `not_before<not_after`. Octets signés `PIXS:PA:BOOTSTRAP:PREPUBLICATION:1.0.0`+LF+canon. `MUST NOT` tête/plan futur/auto-inclusion/état/mandat NV-E4-SQL-retrait.

#### B-FIN — PUBLICATION FINALE SIGNÉE APRÈS CONSTATS
- Enveloppe fermée idem. `document` fermé : `object_type:str="pixs.agent.bootstrap_publication/v1"`, `schema_version:str="1.0.0"`, `publication_ref:str`, `installation_ref:str`, `target_ref:str` obligatoire comparé `first_context`, `prepublication_binding:ContentBinding{ref:str,version:str,sha256:str ^[0-9a-f]{64}$}`, `policy_binding:ContentBinding` idem vers document public propriétaire typé indépendant `pixs.agent.bootstrap_policy/v1` distinct de B-PUB — Policy14 proposée fermée `pixs.agent.bootstrap_policy/v1`, sans adoption avant validation humaine, DÉPENDANCE EXPLICITE sans résolveur nommé, `plan_type:str` littéral exact `pixs.agent.bootstrap_plan/v1`, `plan_binding:ContentBinding` idem vers Plan15 existant, `first_head_sha256:str ^[0-9a-f]{64}$`, `first_sequence:int uint64 [0,2^64-1] TOUJOURS PRÉSENT issu du premier record préexistant ; 0 autorisé seulement si fixé explicitement, genèse automatique et défaut implicite INTERDITS`, `first_context:{installation_ref:str,target_ref:str,registry_ref:str,registry_generation_ref:str,epoch:int uint64 [0,2^64-1] TOUJOURS PRÉSENT}`, `valid_not_before_utc6:str` PROPRE FIN, `valid_not_after_utc6:str` PROPRE FIN `MUST` INCLUSE dans intersection validités courantes pré pub+politique jamais extension, `observed_from_utc6:str`, `observed_to_utc6:str` distincts validité, `provenance_observed_binding:ContentBinding` vers Provenance28 proposée, `admission_scope:str="CONFIGURATION_ONLY"`. Dates UTC6 strictes calendrier+ordre vérifiés, aucun modèle UTC depuis candidat. Octets signés `PIXS:PA:BOOTSTRAP:PUBLICATION:1.0.0`+LF+canon. Ni admission actuelle ni mandat NV.
- DÉPENDANCES FORMAT proposées ci-dessous ; vrais propriétaires D11, D13, scanner, contexte et provenance à réaliser et qualifier, sans disponibilité supposée ; aucune adoption avant validation humaine.

#### B-SIG — CLAUSE COMMUNE ENVELOPPES/SIGNATURES
- Enveloppe `{document:object,signature_b64:str}` fermée, `document` objet non chaîne ; `signature_b64` base64 canonique 88 caractères vers 64 octets Ed25519. Canon explicite `json.dumps(ensure_ascii=False,allow_nan=False,sort_keys=True,separators=(",",":"))` UTF8 sans LF final ; octets signés `ASCII(préfixe)+LF+canon`. Références UTF8 non vides sans C0/DEL/surrogates, bornes `payload/max_ref` protégées. Entiers JSON seulement champs déclarés uint, refus `bool/float/null/duplicats/inconnus`. Validités finies `valid_not_before_utc6<valid_not_after_utc6` et `observed_from_utc6<=observed_to_utc6` distinctes, validité FIN incluse dans intersection prépublication/politique. `version/domaine` fixés aux attendus installés sans valeur par absence. Canons actuels applicables et raccord normatif écrit ; aucun port PA v2, profil réel de continuité ou ABI commune livré ou adopté par cela ; privé Z12 non importable.


### RSMP-U2 — Plafonds et échéance privés proposés

Statut : PROPOSÉ NON ADOPTÉ. N'autorise aucun code ni effet.
Ne constitue ni plan complet ni clôture globale de l'option B.
Ne redéfinit ni `PayloadLimits` ni `JournalLimits` de PG 1.0.
Les seuils d'interface et de format ci-dessous restent distincts
des valeurs de production. Sans valeur par défaut.

#### Règles de provenance exigée

Chaque valeur effective MUST provenir d'une politique ou d'un profil installé, protégé, vérifié et courant, qualifié au point d'usage.
Une valeur manquante MUST provoquer un refus.
Le contenu d'appel, le plan ou un autre démarrage MUST NOT servir d'autorité.
L'échéance MUST NOT provenir du document JSON du plan ni d'un autre démarrage.
Le consommateur MUST NOT déduire une valeur par défaut, proroger ou réinitialiser implicitement un budget.
D11 extérieur établit la configuration et le provisionnement. Le moteur reçoit l'échéance d'un propriétaire natif courant, sous politique et profil protégés et vérifiés, avec garde D13 et contexte conservés.
L'interface actuelle ne prouve pas ce propriétaire fourni. L'exigence de provenance reste à réaliser et à qualifier. Elle reste distincte des prédicats en C décrits ci-dessous.
Le chemin de code prouve la forme de la contrainte et ne prouve jamais la provenance des valeurs.
Aucun objet de plafonds à clés libres. Les noms, types et champs ci-dessous sont exhaustifs. Aucun chemin, PCR, fournisseur ou opération supplémentaire n'est introduit.

#### Prédicats natifs écrits de temps

`_now()` utilise `clock_gettime(CLOCK_MONOTONIC)`. Échec d'appel : retour `0`.
`_now()` retourne `0` si `tv_sec < 0`, ou `tv_sec >= UINT64_MAX // 1000000000`, ou `tv_nsec < 0`, ou `tv_nsec >= 1000000000`. Sinon retour `tv_sec * 1000000000 + tv_nsec`.
`_time()` retourne `J_CLOCK` si `_now == 0`, `J_EXPIRED` si `now >= deadline`, `J_OK` sinon.
L'échéance est une valeur privée native en nanosecondes monotones, de même horloge et de même contexte de durée de vie vérifiée. Elle n'est ni un temps UTC ni une preuve de fraîcheur universelle.
Condition actuelle écrite et non qualifiée, conservée hors tableau : `journal_deadline == nv_deadline`, aux points `nv_intent.pyx:131`, `nv_intent.pyx:284` et `nv_intent.pyx:615`, avec refus `I_VERIFY` en cas d'inégalité. Cette égalité ne prouve ni propriétaire ni fraîcheur.
Le troisième paramètre positionnel de `PayloadLimits` reçoit aujourd'hui `max_correlation`. Il existe pour `max_observation_refs` et reste inutilisé par le codeur de journal pour ce sens. Aucune correction PG n'est proposée hors mandat. Ce sens MUST NOT être recyclé pour les plafonds ou les étapes.
Les documents de publication utilisent une instance de plafonds propre à leur usage. Le silence MUST NOT imposer la même instance que le journal.

#### Tableau complet des onze paramètres

| Champ | Type exact | Borne numérique | Unité | Relation | Origine exigée |
|---|---|---|---|---|---|
| `payload.max_json_bytes` | Python `type() is int`, pont `uint32_t max_json` | Python `> 0`, pont `1..4294967295` | Octets UTF-8 du document JSON | `payload_len > 0` et `payload_len <= max_json` ; `len(texte UTF-8) <= max_json_bytes`, sinon `PA01_PAYLOAD_LIMIT_EXCEEDED` ou `I_ARGUMENT` ; `capacity = min(max_record observé, max_json)` | Politique ou profil installé, protégé, vérifié et courant, qualifié au point d'usage |
| `payload.max_ref_bytes` | Python `type() is int`, pont `uint32_t max_ref` | Python `> 0`, pont `1..4294967295` | Octets UTF-8 par référence | Référence non vide, sans caractère de contrôle, UTF-8 valide ; `taille <= max_ref_bytes`, sinon `PA01_REFERENCE_LIMIT_EXCEEDED` ; appliqué aux identifiants d'opération, de corrélation, d'installation, de cible, aux six références de journal et à chaque référence de traçage et d'attache | Politique ou profil installé, protégé, vérifié et courant, qualifié au point d'usage |
| `payload.max_observation_refs` | Python `type() is int` | Python `> 0` | Compte de références d'observation | Existant PG 1.0, inchangé et inutilisé pour les étapes et plafonds U2 | Conservé PG 1.0, sans autorité U2 |
| `max_epoch` | Python `type() is int`, pont `uint64_t max_epoch` | `0..18446744073709551615`, zéro inclus | Entier logique d'époque | `0 <= borne <= UINT64_MAX`, sinon `PA01_JOURNAL_LIMITS_INVALID` ; `epoch <= UINT64_MAX` et `epoch <= plafond`, sinon `PA01_JOURNAL_NUMBER_INVALID` ou `LIMIT_EXCEEDED` ; décodage : refus si nombre `> max(max_epoch, max_sequence)` | Politique ou profil installé, protégé, vérifié et courant, qualifié au point d'usage |
| `max_sequence` | Python `type() is int`, pont `uint64_t max_sequence` | `0..18446744073709551615`, zéro inclus | Entier logique de séquence | Mêmes contrôles que `max_epoch` ; proposition suivante : `sequence == séquence précédente + 1`, sinon `PA01_INTENT_NEXT_MISMATCH` | Politique ou profil installé, protégé, vérifié et courant, qualifié au point d'usage |
| `max_correlation_refs` | Python `type() is int`, pont `uint32_t max_correlation` | Python `> 0`, pont `1..4294967295` | Compte de références de corrélation | `correlation_refs` de type tuple ; `longueur <= plafond`, sinon `PA01_JOURNAL_TRACE_LIMIT_EXCEEDED` ; chaque élément contrôlé comme référence | Politique ou profil installé, protégé, vérifié et courant, qualifié au point d'usage ; distinct de `max_observation_refs` |
| `max_causation_refs` | Python `type() is int`, pont `uint32_t max_causation` | Python `> 0`, pont `1..4294967295` | Compte de références de causalité | Mêmes contrôles que la corrélation | Politique ou profil installé, protégé, vérifié et courant, qualifié au point d'usage |
| `max_bytes` | C `uint64_t max_bytes` | `59..9223372036854775807` (`59..0x7fffffffffffffff`) | Octets du fichier de journal local | `max_bytes < 59` ou `> 0x7fffffffffffffff` : `J_ARGUMENT` ; `max_record + 58 <= max_bytes` exigé | Politique ou profil installé, protégé, vérifié et courant, qualifié à l'ouverture du journal |
| `max_record` | C `uint32_t max_record` | `1..4294967295`, avec `max_record + 58 <= max_bytes` et `max_record <= SIZE_MAX - 65` selon `sizeof(size_t)` | Octets de charge utile d'une trame | `max_record == 0` : `J_ARGUMENT` ; `max_record + 58 > max_bytes` : `J_ARGUMENT` ; dépassement de `SIZE_MAX - 65` : `J_ARGUMENT` ; `payload_len > max_record observé` : `I_VERIFY` ; une trame ajoute 4 octets de longueur, la charge utile et 32 octets de reçu, l'en-tête de fichier de 22 octets expliquant le supplément de 58 exigé à l'ouverture | Politique ou profil installé, protégé, vérifié et courant, qualifié au point d'usage ; charge utile distincte de `max_json_bytes` |
| `max_records` | C `uint32_t max_records` | `1..4294967295` | Compte de trames du journal | `max_records == 0` : `J_ARGUMENT` | Politique ou profil installé, protégé, vérifié et courant, qualifié au point d'usage |
| `deadline_ns` | C `uint64_t` privé natif, conservé comme échéance | `deadline_ns > now`, avec `now = _now() != 0` ; ensuite `now < échéance conservée` pendant la durée de vie | Nanosecondes monotones `CLOCK_MONOTONIC` | `now == 0` : `J_CLOCK` ; `deadline_ns <= now` : `J_EXPIRED` ; `now >= échéance conservée` : `J_EXPIRED` | Reçue d'un propriétaire natif courant, sous politique et profil protégés et vérifiés, avec garde et contexte conservés ; propriétaire concret non fourni par l'interface actuelle |


### Plan B canonique non signé proposé

Statut : PROPOSÉ NON ADOPTÉ. Document de données seulement. Sans plan
complet utilisable. Sans code ni effet. Sans enveloppe signée. Sans
chronologie, état, opération ou permission nouveaux.

#### Tableau complet des quinze champs

| Champ | Type exact | Domaine | Liaison | Vérification |
|---|---|---|---|---|
| `object_type` | `str` | Égal à `pixs.agent.bootstrap_plan/v1` | Aucune liaison externe | Égalité stricte, sinon refus de schéma |
| `schema_version` | `str` | Égal à `1.0.0` | Aucune liaison externe | Égalité stricte, sinon refus de schéma |
| `plan_ref` | `str` UTF-8 bornée | Référence externe du gel, borne octets `max_ref_bytes` du profil qualifié | Identifiant externe repris dans la liaison du plan | Valeur non vide, sans caractères `C0`, `DEL` ou substituts, validité UTF-8, borne octets respectée, sinon refus |
| `plan_version` | `str` UTF-8 bornée | Version externe du gel | Identifiant externe repris dans la liaison du plan | Valeur non vide, sans caractères `C0`, `DEL` ou substituts, validité UTF-8, borne octets respectée, sinon refus |
| `installation_ref` | `str` UTF-8 bornée | Cible d'installation, borne octets `max_ref_bytes` | Égalité exigée entre plan, prépublication et profil natif courant D14 | Valeur non vide, sans caractères `C0`, `DEL` ou substituts, validité UTF-8, borne octets respectée ; inégalité entre sources provoque refus ; contenu d'appel sans valeur d'autorité |
| `target_ref` | `str` UTF-8 bornée | Cible d'exécution, borne octets `max_ref_bytes` | Égalité exigée entre plan, prépublication et profil natif courant D14 | Même contrôle complet que `installation_ref` |
| `prepublication_binding` | `ContentBinding` fermé `{ref:str non vide,version:str non vide,sha256:hex64 minuscule}` | Désigne la prépublication B | Liaison de données vers prépublication, avec égalité `ref` et `version` à l'objet producteur toujours obligatoire, et `sha256` de l'enveloppe entière signée selon table des liaisons, sans placeholder | Attache complète et bornée, manquant provoque refus ; condensat prouve intégrité des octets, sans valeur d'autorité |
| `policy_binding` | `ContentBinding` fermé `{ref:str non vide,version:str non vide,sha256:hex64 minuscule}` | Désigne Policy14 réellement proposée `pixs.agent.bootstrap_policy/v1` | Liaison de données vers définition publique protégée | Attache complète et bornée, sans affirmation de propriétaire livré ; forme déjà proposée fermée, producteur à réaliser et qualifier |
| `resource_profile_binding` | `ContentBinding` fermé `{ref:str non vide,version:str non vide,sha256:hex64 minuscule}` | Désigne Resource24 réellement proposée, profil protégé courant qualifié U2-CAPS | Liaison de données vers profil protégé courant | Attache complète et bornée, profil manquant provoque refus ; plafond depuis le contenu d'appel interdit ; échéance `deadline_ns` depuis un autre démarrage interdite |
| `nv_profile` | Objet fermé, sept champs | Copie des représentations et types U1, avec prédicats existants conservés exactement : `nv_index` en `uint32` dans `0x01000000..0x01ffffff`, `nv_attributes` en `uint32` valeur exacte attendue, `nv_name_alg` égal à `SHA256`, `nv_data_size` en `int` égal à 32 strict non booléen, `nv_authpolicy_hex` en `str` avec `^[0-9a-f]{64}$`, `nv_name_hex` en `str` avec `^000b[0-9a-f]{64}$`, `maintenance_p256_ref` en `str` référence publique à vérification positive | Contexte TPM distinct du nom, sans hiérarchie `OWNER` choisie, sans valeur secrète | Chaque champ vérifié en type, forme et valeur ; masque reçu à la place de la valeur exacte provoque refus ; valeur secrète, fournisseur, PCR et fanion libre interdits ; référence utilisée à la place d'une valeur publique NV attendue interdite, référence publique opaque `maintenance_p256_ref` à résoudre admise ; liste des sept noms fait foi |
| `tpm_context_binding` | `ContentBinding` fermé `{ref:str non vide,version:str non vide,sha256:hex64 minuscule}` | Désigne Context8 réellement proposé, contexte public protégé installé, distinct du nom NV | Liaison de données vers contexte installé, à résolution positive | Attache complète et bornée ; clé choisie interdite ; hiérarchie choisie interdite ; sans interface imaginaire ; forme déjà proposée fermée, producteur à réaliser et qualifier |
| `recipe` | Objet de type déclaré `BootstrapRecipe/v1` | Recipe13 déjà proposée fermée, recette typée déterministe, sans `first_head_sha256`, sans condensat contenant le plan, sans publication finale future, sans auto-liaison | Liaison de données vers Recipe13 déjà proposée fermée, producteur à réaliser et qualifier | Type déclaré présent ; objet générique interdit ; non instanciable opérationnellement avant autorisations et preuves ; forme de test ne vaut pas admission, code B non autorisé avant validation humaine du lot ; global complet non prétendu |
| `authority_binding` | `ContentBinding` fermé `{ref:str non vide,version:str non vide,sha256:hex64 minuscule}` | Désigne l'autorité externe | Simple liaison, prouve zéro autorité | Attache complète et bornée ; acteur à vérifier positivement, sinon refus |
| `procedure_binding` | `ContentBinding` fermé `{ref:str non vide,version:str non vide,sha256:hex64 minuscule}` | Désigne la procédure D11 qualifiée | Simple liaison, prouve zéro exécution | Attache complète et bornée ; procédure qualifiée actuellement non fournie ; permission à vérifier positivement, sinon refus |
| `executor_binding` | `ContentBinding` fermé `{ref:str non vide,version:str non vide,sha256:hex64 minuscule}` | Désigne l'exécutant | Simple liaison, prouve zéro exécution | Attache complète et bornée ; procédure d'exécution à vérifier positivement, sinon refus |

#### Canon et liaison

`BINDING(plan,limits)` vaut `ContentBinding` avec `ref` égal à
`DOCUMENT.plan_ref`, `version` égal à `DOCUMENT.plan_version`, `sha256`
égal à `SHA256(CANON(document entier))`. Cette liaison et cette empreinte
restent hors document.
`CANON` vaut `json.dumps(ensure_ascii=False, allow_nan=False, sort_keys=True,
separators=(",", ":"))` en UTF-8 sans saut final, sur le document entier.
Refus en cas de champ inconnu, de duplication, de booléen, de nombre hors
position entière non signée, de nul, de `C0`, de `DEL` ou de substitut, et en
cas de limite exigée non respectée au point d'usage. Champs de liaison
fermés : `{ref,version,sha256}`.
Chaque consommateur MUST vérifier positivement acteur, permission et
procédure avant acte. Chaque valeur effective MUST provenir du profil
protégé courant qualifié. Le contenu d'appel MUST NOT servir d'autorité.


### Recette `BootstrapRecipe/v1` fermée proposée

Statut : PROPOSÉ NON ADOPTÉ. Sans écriture, code, test ou NV.
Sans instanciation opérationnelle avant autorisations et preuves ; `BootstrapRecipe/v1`, `BootstrapBase/v1`, premier enregistrement, scanner normatif et provenance proposés fermés, exécutant extérieur à qualifier ; préparation de fixtures publiques non autorisantes admise. Sans admission, acte ou code global.

| Champ | Type exact | Contrainte | Origine | Rôle |
|---|---|---|---|---|
| `object_type` | `str` | Égal à `pixs.agent.bootstrap_recipe/v1` | Constante documentée | Typage de la recette |
| `schema_version` | `str` | Égal à `1.0.0` | Constante documentée | Version de la recette |
| `recipe_ref` | `str` UTF-8 bornée | Référence externe non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Identifiant produit et figé par procédure extérieure autorisée, sans producteur concret présumé | Identifiant repris dans `recipe_binding` de l'enregistrement, avec `ref` égal à `recipe.recipe_ref` |
| `recipe_version` | `str` UTF-8 bornée | Version externe non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Identifiant produit et figé par procédure extérieure autorisée, sans producteur concret présumé | Identifiant repris dans `recipe_binding` de l'enregistrement, avec `version` égale à `recipe.recipe_version` |
| `renderer_id` | `str` | Égal littéral à `pixs.bootstrap.fixed_renderer/v1`, valeur unique versionnée non libre | Constante du contrat | Désigne le rendu fixe ; règle de copie normative dans l'algorithme, sans donnée fournie par le contenu d'appel ; constantes d'en-tête et de préfixe dans le contrat |
| `transition_ref` | `str` UTF-8 bornée | Valeur explicite unique non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Paramètre produit et figé par procédure extérieure autorisée | Référence de transition du premier enregistrement |
| `registry_ref` | `str` UTF-8 bornée | Valeur non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes`, validée contre profil protégé | Paramètre explicite de contexte | Référence de registre du premier enregistrement |
| `registry_generation_ref` | `str` UTF-8 bornée | Valeur non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes`, validée contre profil protégé | Paramètre explicite de contexte en `str` selon `_context` | Génération de registre du premier enregistrement, sans entier de génération |
| `epoch` | `int` strict non booléen | `0..18446744073709551615`, zéro possible explicite pour premier enregistrement extérieur, sans valeur par défaut | Paramètre d'époque vérifié contre profil protégé courant | Époque du premier enregistrement |
| `sequence` | `int` strict non booléen | `0..18446744073709551615`, zéro possible explicite pour premier enregistrement extérieur, sans valeur par défaut | Paramètre de séquence vérifié contre profil protégé courant | Séquence du premier enregistrement |
| `correlation_refs` | Tableau ordonné de `str` | Références non vides UTF-8, sans `C0`, `DEL` ou substitut, borne octets `max_ref_bytes`, ordre conservé, doublons conservés sous plafond exact `max_correlation_refs` | Traces produites et figées par procédure extérieure autorisée, vérifiées contre profil protégé | Traçage de corrélation du premier enregistrement |
| `causation_refs` | Tableau ordonné de `str` | Références non vides UTF-8, sans `C0`, `DEL` ou substitut, borne octets `max_ref_bytes`, ordre conservé, doublons conservés sous plafond exact `max_causation_refs` | Traces produites et figées par procédure extérieure autorisée, vérifiées contre profil protégé | Traçage de causalité du premier enregistrement |
| `initial_base_binding` | `ContentBinding` fermé `{ref,version,sha256}` | Désigne `BootstrapBase/v1` proposée fermée | Proposition BootstrapBase/v1 déjà fermée dans le lot, sans producteur matériel livré | Base initiale déclarative |

Zéro objet ouvert. Zéro `plan_binding` dans la recette. Zéro `plan_sha256`
dans la recette. Zéro première tête dans la recette. Zéro condensat
d'enregistrement final dans la recette. Zéro publication finale future dans
la recette. Zéro gabarit JSON, shell ou rendu dynamique.
Paramètres de contexte, époque, génération et séquence, avec plafonds,
vérifiés contre profil protégé courant. Identifiants et traces produits et
figés par procédure extérieure autorisée. Contenu d'appel sans valeur
d'autorité. Base NV zéro ou aléatoire jamais présumée. Initialisation par
le moteur interdite. Forme de données distincte de l'admission : la recette
structurelle prouve zéro base, zéro qualité et zéro procédure.

#### Canon et liaisons de recette

`CANON` vaut `json.dumps(ensure_ascii=False, allow_nan=False,
sort_keys=True, separators=(",", ":"))` en UTF-8 sans saut final, même
forme que le plan. Refus en cas de champ inconnu, de duplication, de
booléen, de nombre hors position entière non signée, de nul, de `C0`, de
`DEL` ou de substitut, et en cas de limite exigée non respectée au point
d'usage.
`recipe_binding` vaut `ContentBinding` obligatoire, avec `ref` égal à
`recipe.recipe_ref`, `version` égale à `recipe.recipe_version`, `sha256`
égal à `SHA256(CANON(recette entière))`. Cette liaison reste extérieure à
la recette, sans hash parent, sans hash de plan et sans première tête.
`plan_binding` reste calculé seulement après gel du document entier du plan.
Chaque valeur effective MUST provenir du profil protégé courant qualifié
pour paramètres et plafonds. Le contenu d'appel MUST NOT servir d'autorité.

#### Dérivation vers premier enregistrement B

Type initial avec constantes exactes : `object_type` égal à
`pixs.agent.bootstrap_initial_record/v1`, `schema_version` égal à `1.0.0`.
Type initial seulement, sans état d'admission, sans état retiré, sans
opération nouvelle. `payload_bytes` et `head` valent sorties, jamais champs
du JSON. Liste fermée ci-dessous les exclut.

| Champ du premier enregistrement | Source |
|---|---|
| `object_type` | Constante `pixs.agent.bootstrap_initial_record/v1` |
| `schema_version` | Constante `1.0.0` |
| `transition_ref` | Recette, champ `transition_ref` |
| `registry_ref` | Recette, champ `registry_ref` |
| `registry_generation_ref` | Recette, champ `registry_generation_ref` |
| `epoch` | Recette, champ `epoch` validé par profil protégé |
| `sequence` | Recette, champ `sequence` validé par profil protégé |
| `correlation_refs` | Recette, champ `correlation_refs` |
| `causation_refs` | Recette, champ `causation_refs` |
| `installation_ref` | Plan, champ `installation_ref` |
| `target_ref` | Plan, champ `target_ref` |
| `prepublication_binding` | Plan, champ `prepublication_binding` |
| `policy_binding` | Plan, champ `policy_binding` |
| `resource_profile_binding` | Plan, champ `resource_profile_binding` |
| `nv_profile` | Plan, champ `nv_profile` |
| `tpm_context_binding` | Plan, champ `tpm_context_binding` |
| `initial_base_binding` | Recette, champ `initial_base_binding` |
| `plan_binding` | Calculé seulement après gel du document entier du plan |
| `recipe_binding` | Obligatoire, avec `ref`, `version` et `SHA256(CANON(recette entière))` ci-dessus |

Contrats proposés fermés : `BootstrapBase/v1`, premier enregistrement, `BootstrapInitProfile/v1`, provenance et scanner normatif. Source native et vérifications à réaliser et qualifier. Instanciation opérationnelle interdite avant autorisations et preuves ; préparation de fixtures publiques non autorisantes admise. Liaison seule sans preuve de
matériel.


### Contrat `BootstrapBase/v1` minimal proposé

Statut : PROPOSÉ NON ADOPTÉ. Sans écriture, code, test, NV ou secret.
Sans admission, acte ou qualification. Matière extérieure. Zéro
fournisseur ou propriétaire livré supposé.

| Champ | Type exact | Contrainte | Provenance typée | Rôle |
|---|---|---|---|---|
| `object_type` | `str` | Égal à `pixs.agent.bootstrap_base/v1` | Constante documentée | Typage de la base |
| `schema_version` | `str` | Égal à `1.0.0` | Constante documentée | Version de la base |
| `base_ref` | `str` UTF-8 bornée | Référence externe non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Identifiant produit et figé par procédure extérieure autorisée | Identifiant repris dans `initial_base_binding` |
| `base_version` | `str` UTF-8 bornée | Version externe non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Identifiant produit et figé par procédure extérieure autorisée | Version reprise dans `initial_base_binding` |
| `tpm_context_binding` | `ContentBinding` fermé `{ref,version,sha256}` | Désigne le contexte public protégé installé, distinct du nom NV | Context8 actuel lié à INIT_A12 par mappings actuels, à résolution positive, avant moteur | Contexte matched exigé avant `SHA256(base32 \|\| tête32)` |
| `nv_coordinates` | Objet fermé `{nv_index,nv_name_hex}` | `nv_index` en `uint32` dans `0x01000000..0x01ffffff`, `nv_name_hex` en `str` avec `^000b[0-9a-f]{64}$` | Coordonnées publiques copiées du profil NV, vérifiées contre profil protégé | Localisation publique, sans preuve de contenu |
| `expected_base_hex64` | `str` | Avec `^[0-9a-f]{64}$`, valeur initiale attendue et configurée de 32 octets, sans zéro ni aléatoire présumé | Dérivation INIT_A12 déjà proposée `SHA256(32 zéros \|\| entrée initiale de 32)`, non valeur libre indépendante | Attente préparée pour observation future, jamais preuve déjà produite |
| `init_profile_binding` | `ContentBinding` fermé `{ref,version,sha256}` | Désigne `BootstrapInitProfile/v1` déjà proposé, lié à Context8 par mappings actuels, sans auto-hash ni cycle, sans preuve réelle déjà produite ni propriétaire réputé livré | INIT_A12 déjà proposé fermé, producteur réel à réaliser et qualifier, sans autorité depuis le binding | Origine antérieure à qualifier, sans invocation magique |

`ContentBinding` vaut toujours `{ref,version,sha256}` avec `ref` en `str`
non vide et `version` en `str` non vide, UTF-8 bornées `max_ref_bytes`,
sans caractère de contrôle ni substitut, et `sha256` en hexadécimal
minuscule de 64 caractères.
Chaque valeur effective MUST provenir du profil protégé courant qualifié.
Le contenu d'appel MUST NOT servir d'autorité. Liaison seule sans preuve
de matériel.

#### Canon et liaison

`CANON` vaut `json.dumps(ensure_ascii=False, allow_nan=False,
sort_keys=True, separators=(",", ":"))` en UTF-8 sans saut final. Refus en
cas de champ inconnu, de duplication, de booléen, de nombre hors position
entière non signée, de nul, de `C0`, de `DEL` ou de substitut, et en cas de
limite exigée non respectée au point d'usage.
`initial_base_binding` vaut `ContentBinding` avec `ref` égal à
`base.base_ref`, `version` égale à `base.base_version`, `sha256` égal à
`SHA256(CANON(base entière))`, hors document de base.

#### Prédicats, ordre et dépendances

| Prédicat | Vérificateur | Moment | Fait actuel | Dépendance |
|---|---|---|---|---|
| Coordonnées dans bornes et nom cohérent | Procédure extérieure | Avant gel de la base | Coordonnées vérifiées | Profil NV et contexte installés |
| Valeur attendue configurée sans défaut présumé | Procédure extérieure | Avant gel du plan et de la recette | Attente préparée | Profil protégé, sans défaut zéro ou aléatoire |
| Contexte matched avec coordonnées | Consommateur | Avant `SHA256(base32 \|\| tête32)` | Contexte résolu positivement | Contexte installé, distinct du nom |
| Initialisation extérieure vérifiée écrite, avec `HMAC` avant `Extend` | Observateur extérieur | Après génération déterministe, avant `Extend` | Initialisation constatée | Plan exact avant effet selon D11, zéro index nouveau et zéro `Extend` sous seule signature d'administration |
| Valeur réelle égale à `expected_base_hex64` | Observateur extérieur | Avant `Extend` | Comparaison exigée | Valeur indisponible ou dérivation non fermée bloque instanciation |
| `HMAC` après égal à `SHA256(base32 \|\| tête32)` | Observateur extérieur | Après `Extend` | Observation produite | Base qualifiée et tête dérivée des octets du premier enregistrement avant `Extend`, zéro tête sortant d'`Extend` |

Ordre exact : profils, politique et prépublication protégés, puis BASE dérivée, recette et plan figés, puis octets de R0 et tête calculés sans effet, puis définition NV extérieure autorisée et zone publique observée, puis initialisation INIT extérieure, puis lecture HMAC de BASE, puis R0 durable et synchronisé, puis Extend B autorisée, puis HMAC de NV_B, puis provenance, puis publication finale. Aucune lecture HMAC avant WRITTEN ; aucune tête issue d'Extend ; lecture courante de la queue après avancement, jamais l'ancienne base. Formats existants comme propositions ; vrais acteurs et vérifications à réaliser et qualifier.


### Premier enregistrement `BootstrapInitialRecord/v1` proposé

Statut : PROPOSÉ NON ADOPTÉ. Sans écriture, code, test, matériel ou
secret. Sans admission, acte ou qualification. Type futur distinct, sans
modification de PG 1.0, sans balayeur livré prétendu. Constat actuel :
le décodeur canonique actuel accepte seulement `JournalTransition` PG 1.0,
l'histoire comparant la première tête à l'épingle, puis contexte à cinq
éléments, séquence plus un, tête précédente et NV précédent, avec
identifiants uniques, et comparant le dernier NV au NV observé courant.
Donc l'actuel refuse l'objet B et ne prouve pas d'histoire mixte.

| Champ | Type exact | Contrainte | Source par R |
|---|---|---|---|
| `object_type` | `str` | Égal à `pixs.agent.bootstrap_initial_record/v1` | Constante |
| `schema_version` | `str` | Égal à `1.0.0` | Constante |
| `transition_ref` | `str` UTF-8 bornée | Référence explicite unique non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Recette, champ `transition_ref` |
| `registry_ref` | `str` UTF-8 bornée | Valeur non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes`, validée contre profil protégé | Recette, champ `registry_ref` |
| `registry_generation_ref` | `str` UTF-8 bornée | Valeur non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes`, validée contre profil protégé | Recette, champ `registry_generation_ref` |
| `epoch` | `int` strict non booléen | `0..18446744073709551615`, zéro possible explicite, sans valeur par défaut | Recette, champ `epoch` validé par profil protégé |
| `sequence` | `int` strict non booléen | `0..18446744073709551615`, valeur explicite de B, zéro seulement si fixé, sans zéro imposé | Recette, champ `sequence` validé par profil protégé |
| `correlation_refs` | Tableau ordonné de `str` | Références non vides UTF-8, sans `C0`, `DEL` ou substitut, borne octets `max_ref_bytes`, ordre conservé, doublons conservés sous plafond exact `max_correlation_refs` | Recette, champ `correlation_refs` |
| `causation_refs` | Tableau ordonné de `str` | Références non vides UTF-8, sans `C0`, `DEL` ou substitut, borne octets `max_ref_bytes`, ordre conservé, doublons conservés sous plafond exact `max_causation_refs` | Recette, champ `causation_refs` |
| `installation_ref` | `str` UTF-8 bornée | Valeur non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Plan, champ `installation_ref` |
| `target_ref` | `str` UTF-8 bornée | Valeur non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Plan, champ `target_ref` |
| `prepublication_binding` | `ContentBinding` fermé | Attache complète et bornée selon base | Plan, champ `prepublication_binding` |
| `policy_binding` | `ContentBinding` fermé | Attache complète et bornée selon base | Plan, champ `policy_binding` |
| `resource_profile_binding` | `ContentBinding` fermé | Attache complète et bornée selon base | Plan, champ `resource_profile_binding` |
| `nv_profile` | Objet fermé sept champs | Copie exacte du plan, selon plan B et contrats U1 | Plan, champ `nv_profile` |
| `tpm_context_binding` | `ContentBinding` fermé | Attache complète et bornée selon base | Plan, champ `tpm_context_binding` |
| `initial_base_binding` | `ContentBinding` fermé | Attache complète et bornée selon base | Recette, champ `initial_base_binding` |
| `plan_binding` | `ContentBinding` fermé | Attache calculée seulement après gel du document entier du plan | Plan gelé |
| `recipe_binding` | `ContentBinding` fermé | Attache obligatoire avec `ref`, `version` et `SHA256(CANON(recette entière))` | Recette gelée |

Zéro champ de propre tête ou de propre condensat dans l'enregistrement.
`ContentBinding.sha256` autorisé dans les dix-neuf champs. Chaque valeur
effective MUST provenir du profil protégé courant qualifié. Le contenu
d'appel MUST NOT servir d'autorité. Condensat compté comme intégrité des
octets, jamais comme autorité. Zéro état, opération ou propriétaire
nouveau.

#### Canon, octets, tête et ancre attendue

`CANON` vaut `json.dumps(ensure_ascii=False, allow_nan=False,
sort_keys=True, separators=(",", ":"))` en UTF-8 sans saut final, avec
plafonds U2 protégés. Refus en cas de champ inconnu, de duplication, de
booléen, de nombre hors position entière non signée, de nul, de `C0`, de
`DEL` ou de substitut.
`ContentBinding` vaut toujours `{ref,version,sha256}` avec `ref` en `str`
non vide et `version` en `str` non vide, UTF-8 bornées `max_ref_bytes`,
sans caractère de contrôle ni substitut, et `sha256` en hexadécimal
minuscule de 64 caractères, selon base. Profil NV sept champs selon plan B
et contrats U1. Plafonds tous U2.
Tête sémantique B égale à `SHA256` sur ASCII
`PIXS:PA:BOOTSTRAP:INITIAL_RECORD:1.0.0` suivi d'un unique `LF`, puis
`CANON` de l'enregistrement B. Domaine sémantique B proposé, sans
changement PG.
Condensat de trame physique égal à `SHA256` sur ASCII
`PIXS:PA:JOURNAL:RECORD:1.0.0` plus `LF`, plus reçu précédent de 32 octets,
plus longueur sur 4 octets en grand-boutiste, plus octets de charge utile.
Préfixe de 29 octets. En-tête de fichier égal à ASCII
`PIXS:PA:JOURNAL:1.0.0` plus `LF`, soit 22 octets. Constat documentaire
vérifié : `nv_journal.pyx:245-320` initialise le reçu précédent à 32 zéros
pour la première trame physique, puis chaînage par reçu calculé. Cette source ne fixe ni base NV ni épingle de tête.
Tête B attendue égale à `publication_finale.document.first_head_sha256`,
pas à l'objet de publication.
Valeur NV B égale à `SHA256(base attendue de 32 || tête B de 32)`, après
provenance `HMAC` réelle. Première suivante PG 1.0 chaînée à tête B, NV B,
contexte identique et séquence plus un depuis la séquence explicite de B,
sans dépassement. Codec PG suivant actuel strict intact. Un seul B en
position zéro préexistante. Journal vide
refusé. Réinitialisation, journal absent et index recréé ne rouvrent jamais B ; réouverture d'un journal persistant réel non interdite, inspection et réconciliation courantes restant possibles. Autogenèse rejetée. Zéro E4 pour fabriquer B.
Zéro mandat NV depuis administration.

#### Balayeur d'histoire mixte futur et préparation

Balayeur futur distinct, hors PG 1.0 : reconstitution déterministe de R0
depuis vrai plan, recette et base, avec comparaison des octets, pas
uniquement de l'épingle. Aiguillage unique sur type B exact en position zéro, puis PG 1.0 seulement, avec canon strict, tous plafonds, compte de queue et de trames, contextes d'époque, de génération et d'installation fixes, séquence plus un avec absence de dépassement, tête précédente, NV précédent et doublon de transition_ref entre B et tout PG vérifiés. Zéro trou, zéro B ailleurs, nouveau registre, époque ou génération automatiques interdits. Si B seul, NV courant égal à NV B ; si suite PG, NV courant égal au dernier NV PG. Preuve historique R0 distinguée de la validité actuelle pour les droits de la branche ; PUB et FIN finies ne donnent ni autorité initiale éternelle ni permission ordinaire nouvelle après retrait ; inspection et histoire n'offrent aucun droit ; régime ordinaire exige ses propres preuves actuelles et les deux retraits ; sans migration, rotation ou renouvellement nouveaux, sans repli vers decoder legacy après refus B. Si politique protégée attend un PG hérité, zéro adoption de B depuis contenu candidat. Publication signée vérifiée pour contexte,
provenance et politique courante avant admission. NV courant vérifié pour
la queue, jamais l'ancienne base quand avancée. Histoire PG 1.0 actuelle et
balayeur historique inchangés. Zéro migration automatique. Zéro adoption B
depuis candidat. Zéro mode, binaire, catalogue ou droit nouveau.
R0 préparé hors moteur sous plan exact, avec ajout et synchronisation avant
`Extend` et constat `HMAC` après, sans atomicité feinte. Inconnu bloque la
suite. Même intention réconciliée, jamais rejouée.
Contrat fermé proposé par cette unité : premier enregistrement avec les
dix-neuf champs ci-dessus. Implémentation non livrée. Contrats proposés couverts : `BootstrapBase/v1` et premier
enregistrement par cette unité. Formes proposées fermées ci-dessous ; source native à réaliser et qualifier après validation ; contrôles d'histoire conservés.


### Politique `BootstrapPolicy/v1` minimale proposée

Statut : PROPOSÉ NON ADOPTÉ. Sans écriture, code, test, secret ou
matériel. Sans admission, acte ou qualification. Document public,
indépendant de la prépublication, du plan, de la base, de la recette et
de la publication finale, sans cycle. Type déjà référencé par B-FIN.
Zéro octroi, opération, domaine ou signataire nouveau. Zéro objet ouvert.
Zéro booléen de vérification. Zéro acteur installé réputé livré. Zéro
réplique de mandat E4, de revendications d'administration, de bibliothèque
système ou de secret.

| Champ | Type exact | Bornes et sémantique | Règles de lien |
|---|---|---|---|
| `object_type` | `str` | Égal à `pixs.agent.bootstrap_policy/v1` | Égalité stricte, sinon refus de schéma |
| `schema_version` | `str` | Égal à `1.0.0` | Égalité stricte, sinon refus de schéma |
| `policy_ref` | `str` UTF-8 bornée | Référence externe non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Égalité obligatoire avec `policy_ref` de B-PUB au point d'usage ; source installée protégée obligatoirement résolue avant acceptation de prépublication et de publication finale ; reprise dans `policy_binding` de B-FIN avec `ref` égal à `policy.policy_ref` |
| `policy_version` | `str` UTF-8 bornée | Version externe non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Égalité obligatoire avec `policy_version` de B-PUB au point d'usage ; source installée protégée obligatoirement résolue avant acceptation de prépublication et de publication finale ; reprise dans `policy_binding` de B-FIN avec `version` égale à `policy.policy_version` |
| `domain` | `str` | Égal à `PA_ADMIN_INITIAL` | Égalité stricte, sans valeur par absence |
| `admission_scope` | `str` | Égal à `CONFIGURATION_ONLY` | Portée d'admission courante, sans mandat E4, sans confirmation et sans mandat NV |
| `withdrawal_right` | `str` | Égal à `WITHDRAW_PA_INITIAL`, nom de droit existant, sans octroi déduit de la politique installée protégée, la clé d'administration ne suffisant pas comme octroi | Droit existant ; mandat ADMIN personnel distinct du PG E4 et R01 selon AdminMandate déjà écrit, révocation, mise en correspondance de contexte C08 et confirmation courante restent obligatoires avant retrait ; zéro dérivation d'administration vers droit NV, SQL ou retrait |
| `nv_profile` | Objet fermé sept champs | `nv_index` en `uint32` dans `0x01000000..0x01ffffff`, `nv_attributes` en `uint32` valeur exacte attendue, `nv_name_alg` égal à `SHA256`, `nv_data_size` en `int` égal à 32 strict non booléen, `nv_authpolicy_hex` en `str` avec `^[0-9a-f]{64}$`, `nv_name_hex` en `str` avec `^000b[0-9a-f]{64}$`, `maintenance_p256_ref` en `str` référence publique à vérification positive, avec prédicats stricts B-NV | Copie conforme au plan B et aux contrats U1 ; égalité exigée entre politique, prépublication, plan et premier enregistrement, avec source NV protégée actuelle ; zéro autre artefact NV futur |
| `installation_ref` | `str` UTF-8 bornée | Cible d'installation non vide, sans caractère générique, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Égalité exigée entre politique, prépublication, plan, publication finale et base dans le contexte protégé |
| `target_ref` | `str` UTF-8 bornée | Cible d'exécution non vide, sans caractère générique, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Égalité exigée entre politique, prépublication, plan, publication finale et base dans le contexte protégé |
| `tpm_context_binding` | `ContentBinding` fermé `{ref,version,sha256}` | Désigne le contexte public protégé installé, distinct du nom NV | Liaison de données vers Context8 réellement proposé |
| `resource_profile_binding` | `ContentBinding` fermé `{ref,version,sha256}` | Désigne le profil de ressources protégé courant | Liaison de données vers Resource24 réellement proposée |
| `valid_not_before_utc6` | `str` | Fenêtre propre finie bornée par profil, forme `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z$`, calendrier réel et ordre vérifiés, avec `not_before < not_after` | Validité propre indépendante de la politique, sans inclusion avec une publication future ; seule la publication finale reste incluse dans l'intersection des validités politique et prépublication |
| `valid_not_after_utc6` | `str` | Fenêtre propre finie bornée par profil, forme `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z$`, calendrier réel vérifié | Même validité propre indépendante, avec fin incluse ; seule la publication finale reste incluse dans l'intersection des validités politique et prépublication |

`ContentBinding` vaut toujours `{ref,version,sha256}` avec `ref` en `str`
non vide et `version` en `str` non vide, UTF-8 bornées `max_ref_bytes`,
sans caractère de contrôle ni substitut, et `sha256` en hexadécimal
minuscule de 64 caractères.
`CANON` vaut `json.dumps(ensure_ascii=False, allow_nan=False,
sort_keys=True, separators=(",", ":"))` en UTF-8 sans saut final. Refus en
cas de champ inconnu, de duplication, de booléen, de nombre hors position
entière non signée, de nul, de `C0`, de `DEL` ou de substitut, et en cas de
limite exigée non respectée au point d'usage.
Politique installée protégée liée par B-PUB en `ref` et `version`, et par
B-FIN en liaison recalculée avec `sha256` égal à `SHA256(CANON(politique
entière))`, hors document de politique. Condensat prouvant l'intégrité des
octets, sans valeur d'autorité. Zéro troisième signature et zéro clé
ajoutées, B-PUB et B-FIN restant les seules enveloppes signées proposées.
Exigence de temps reçue comme contexte privé, jamais depuis le candidat.
Raccord normatif écrit et canons actuels applicables ; aucun port PA v2, profil réel de continuité ou ABI commune livré ou adopté ; privé Z12 non importable.
Chaque valeur effective MUST provenir de la source installée authentique
hors candidat, qualifiée au point d'usage. Le contenu d'appel MUST NOT
servir d'autorité.


### Profil `BootstrapResourceProfile/v1` proposé

Statut : PROPOSÉ NON ADOPTÉ. Sans écriture, code, test, secret ou
matériel. Sans admission, acte ou qualification. Document protégé
installé hors candidat, servant à vérifier politique, plan, recette et
premier enregistrement. Migration d'époque ou de génération refusée,
selon principe adopté. Contraintes UTC6 et canons courants applicables ; modèle réel, source et port PA à réaliser et qualifier, sans import ABI privée Z12.

U2 vaut onze paramètres historiques du code, avec échéance privée native
courante. Les dix paramètres publics ci-dessous reprennent U2 sans
l'échéance. Zéro confusion entre ces dix reprises, vingt-quatre champs de ce profil ou onze constantes nouvelles. Correspondance explicite `payload_max_json_bytes` vers `PayloadLimits.max_json_bytes`, `payload_max_ref_bytes` vers `PayloadLimits.max_ref_bytes`, `payload_max_observation_refs` vers `PayloadLimits.max_observation_refs` sans renommage du code ; tous champs de références non vides UTF-8 sans `C0`, `DEL` ou substitut, validité UTF-8 et bornes octets respectées, avec `epoch <= max_epoch`, première séquence `<= max_sequence`, charges canoniques de charge utile de journal B et PG `<= min(max_json,max_record)` avant allocation native, sans imposer `max_record` à tout profil ou publication hors journal, ces autres documents restant bornés par le `max_json` approprié. `payload.max_observation_refs`
conservé PG, sans réemploi pour les étapes. `deadline_ns` restant une
capacité privée native courante, jamais un champ JSON absolu.

| Champ | Type exact | Bornes et unités | Source et rôle |
|---|---|---|---|
| `object_type` | `str` | Égal à `pixs.agent.bootstrap_resource_profile/v1` | Constante documentée, typage du profil |
| `schema_version` | `str` | Égal à `1.0.0` | Constante documentée, version du profil |
| `profile_ref` | `str` UTF-8 bornée | Référence externe non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Identifiant repris dans `resource_profile_binding` |
| `profile_version` | `str` UTF-8 bornée | Version externe non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Version reprise dans `resource_profile_binding` |
| `installation_ref` | `str` UTF-8 bornée | Cible d'installation non vide, sans caractère générique, borne octets `max_ref_bytes` | Contexte résolu, égalité exigée entre politique, prépublication, plan et base |
| `target_ref` | `str` UTF-8 bornée | Cible d'exécution non vide, sans caractère générique, borne octets `max_ref_bytes` | Contexte résolu, même égalité exigée |
| `registry_ref` | `str` UTF-8 bornée | Référence non vide, borne octets `max_ref_bytes`, validée contre profil protégé | Contexte résolu |
| `registry_generation_ref` | `str` UTF-8 bornée | Référence non vide, borne octets `max_ref_bytes`, validée contre profil protégé | Contexte résolu en `str`, sans entier de génération |
| `epoch` | `int` strict non booléen | `0..18446744073709551615`, valeur explicite épinglée | Contexte épinglé, sans genèse par le moteur |
| `first_sequence` | `int` strict non booléen | `0..18446744073709551615`, valeur explicite épinglée, zéro seulement si fixé | Première séquence explicite, sans genèse par le moteur |
| `payload_max_json_bytes` | `int` strict non booléen | `1..4294967295`, octets UTF-8 de document JSON | Reprise U2, plafond JSON avant allocation réelle protégée |
| `payload_max_ref_bytes` | `int` strict non booléen | `1..4294967295`, octets UTF-8 par référence | Reprise U2, même règle d'allocation |
| `payload_max_observation_refs` | `int` strict non booléen | `> 0`, compte de références d'observation | Reprise U2 conservée PG, sans réemploi pour les étapes |
| `max_epoch` | `int` strict non booléen | `0..18446744073709551615` | Reprise U2, plafond logique d'époque |
| `max_sequence` | `int` strict non booléen | `0..18446744073709551615` | Reprise U2, plafond logique de séquence |
| `max_correlation_refs` | `int` strict non booléen | `1..4294967295`, compte de corrélation | Reprise U2, ordre et doublons conservés |
| `max_causation_refs` | `int` strict non booléen | `1..4294967295`, compte de causalité | Reprise U2, même règle de traçage |
| `max_bytes` | `int` strict non booléen | `59..9223372036854775807`, octets de fichier de journal | Reprise U2 ; minimum 59 égal à en-tête fichier 22 plus trame 4 plus charge utile minimale 1 plus reçu 32 ; `max_record + 58 <= max_bytes` exigé ; `SIZE_MAX - 65` concerne `max_record`, sans borne `max_bytes <= SIZE_MAX` inventée |
| `max_record` | `int` strict non booléen | `1..4294967295`, octets de charge utile de trame, avec `max_record + 58 <= max_bytes` et `max_record <= SIZE_MAX - 65` selon `sizeof(size_t)` | Reprise U2, plafond de charge, distinct du plafond JSON |
| `max_records` | `int` strict non booléen | `1..4294967295`, compte de trames | Reprise U2 |
| `max_validity_span_ns` | `int` strict non booléen | `1..18446744073709551615`, nanosecondes entières | Champ documentaire nouveau proposé, distinct des onze U2, source politique figée hors candidat ; toute fenêtre des trois objets politique, prépublication et publication finale avec durée strictement positive et inférieure ou égale à la borne, sans choix de production implicite et sans extension de budget de mandat personnel par cette borne |
| `max_command_bytes` | `int` strict non booléen | `10..4294967295`, octets | Champ documentaire de profil à mapper au paramètre API existant `max_command` en `uint32`, sans durée et hors onze U2, sans backend nouveau sélectionné |
| `max_response_bytes` | `int` strict non booléen | `10..4294967295`, octets | Champ documentaire de profil à mapper au paramètre API existant `max_response` en `uint32`, sans durée et hors onze U2, sans backend nouveau sélectionné |
| `operation_budget_ns` | `int` strict non booléen | `1..18446744073709551615`, nanosecondes entières sans troncature favorable, avec contrôle anti-dépassement | Champ documentaire nouveau proposé, distinct des onze U2 ; durée ns privée source profil, jamais échéance JSON ; dérivation native observant maintenant `CLOCK_MONOTONIC` non nul, refusant dépassement maintenant plus budget, fixant une échéance commune unique pour gardes, lecteur et journal du même démarrage, sans réarmement ni reprise de budget après délai ou nettoyage ; sans paramètre C actuel nouveau, contexte propriétaire à réaliser |

Zéro champ `deadline_ns` dans ce document. Le propriétaire natif courant
créera une échéance `CLOCK_MONOTONIC` finie à partir du budget protégé
explicite et conservera une garde identique. Durée distincte de
l'échéance, du contenu d'appel, de l'UTC et d'un réarmement. Origine et
format des bornes d'exploitation fermés ci-dessus, sans fournisseur livré
prétendu. Dépassements refusés. Plafond de chargement des références du profil garanti d'abord dans la composition installée protégée D14 hors candidat, sans prendre le profil demandé comme sa propre autorité pour allouer sans taille ; chargeur effectif à réaliser. Contrats proposés non qualifiés comme profils installés actuels.
Chaque valeur effective MUST provenir du profil protégé courant qualifié.
Le contenu d'appel MUST NOT servir d'autorité. Liaison seule sans preuve
de matériel.

#### Canon et liaison

`CANON` vaut `json.dumps(ensure_ascii=False, allow_nan=False,
sort_keys=True, separators=(",", ":"))` en UTF-8 sans saut final. Refus en
cas de champ inconnu, de duplication, de booléen, de nombre hors position
entière non signée, de nul, de `C0`, de `DEL` ou de substitut, et en cas de
limite exigée non respectée au point d'usage.
`resource_profile_binding` vaut `ContentBinding` avec `ref` égal à
`profile.profile_ref`, `version` égale à `profile.profile_version`,
`sha256` égal à `SHA256(CANON(profil entier))`, hors document de profil.
Zéro auto-condensat. Zéro cycle. Zéro clé. Zéro secret. Zéro descripteur.


### Contexte `BootstrapTpmContext/v1` proposé

Statut : PROPOSÉ NON ADOPTÉ. Sans écriture, code, test, secret,
matériel ou hôte. Sans admission, acte ou qualification. Source
protégée installée hors candidat. Capacités réelles courantes
uniquement privées, avec D13, D14, `HMAC` et TCB de système et
distribution selon exposé. Zéro attestation TPM nouvelle. Zéro champ ou
booléen de vérification. Références opaques sans valeur d'autorité.
Absence de preuve TPM et de gardes actuels empêchant l'admission.

| Champ | Type exact | Contrainte | Provenance typée | Rôle |
|---|---|---|---|---|
| `object_type` | `str` | Égal à `pixs.agent.bootstrap_tpm_context/v1` | Constante documentée | Typage du contexte |
| `schema_version` | `str` | Égal à `1.0.0` | Constante documentée | Version du contexte |
| `context_ref` | `str` UTF-8 bornée | Référence externe non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Identifiant produit et figé par procédure extérieure autorisée | Identifiant repris dans `tpm_context_binding` |
| `context_version` | `str` UTF-8 bornée | Version externe non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Identifiant produit et figé par procédure extérieure autorisée | Version reprise dans `tpm_context_binding` |
| `installation_ref` | `str` UTF-8 bornée | Cible d'installation non vide, borne octets `max_ref_bytes` | Contexte résolu | Liaison installation et cible |
| `target_ref` | `str` UTF-8 bornée | Cible d'exécution non vide, sans caractère générique, borne octets `max_ref_bytes` | Contexte résolu | Liaison installation et cible |
| `tcti_backend_ref` | `str` UTF-8 bornée | Référence exacte de backend TCTI et de configuration publique opaque non vide, borne octets `max_ref_bytes` | Configuration publique protégée, sans condensat de credential et sans canal | Désignation du backend TCTI réel, sans preuve de canal |
| `usage_custody_ref` | `str` UTF-8 bornée | Référence de configuration publique opaque non vide, borne octets `max_ref_bytes` | Configuration publique protégée, sans condensat de credential | Désignation de la garde d'usage, sans preuve de possession |

`CANON` vaut `json.dumps(ensure_ascii=False, allow_nan=False,
sort_keys=True, separators=(",", ":"))` en UTF-8 sans saut final. Refus en
cas de champ inconnu, de duplication, de booléen, de nombre hors position
entière non signée, de nul, de `C0`, de `DEL` ou de substitut, et en cas de
limite exigée non respectée au point d'usage.
`tpm_context_binding` vaut `ContentBinding` avec `ref` égal à
`context.context_ref`, `version` égale à `context.context_version`,
`sha256` égal à `SHA256(CANON(contexte entier))`, hors document de
contexte.
Toutes les références relèvent des mêmes contrôles : UTF-8 non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, bornes octets respectées, cibles sans caractère générique, avec comparaisons courantes installation et cible avant usage. Résolution native explicite du backend réel, du descripteur de garde, de la session `HMAC`, du credential D13 `host+tpm2` et du manager D14 avec `MainPID`, `InvocationID` et artefacts, pour les deux contextes uniquement privés, sans valeur secrète, sans condensat de credential et sans capacité dans le JSON. Zéro mécanisme d'attestation créé.
Chaque valeur effective MUST provenir du profil protégé courant qualifié.
Le contenu d'appel MUST NOT servir d'autorité.

### Fiche de décision pour entrée initiale et initialisation — PROPOSÉE NON ADOPTÉE

Statut : PROPOSÉE NON ADOPTÉE. Sans écriture, code, test, secret, matériel ou hôte. Sans admission, acte ou qualification. Choix humain concret préparé, sans adoption automatique.

#### Source primaire

Source primaire : [NV_Extend.c](https://raw.githubusercontent.com/microsoft/ms-tpm-20-ref/main/TPMCmd/tpm/src/command/NVStorage/NV_Extend.c). Code source générique avec ancien condensat, algorithme de nom et projection D10 vers `SHA256`, sans norme modifiée prétendue. Source 1.38 non vérifiée, avec retour 429 par lecture publique, en mémoire aussi. Zéro exécution et zéro version de projet relevées.

#### Option A recommandée proposée, non adoptée

Entrée initiale publique exacte de 32 octets, fixée explicitement sans valeur par défaut. Base attendue égale à `SHA256(32 zéros || entrée initiale de 32)` selon D10 avec `SHA256`, seulement pour un index neuf défini hors runtime PA, avec `WRITTEN`, `READLOCKED` et `WRITELOCKED` à zéro à la définition sous vrai contexte de plateforme, puis zone publique `WRITTEN-clear` observée et nom calculé et rapproché avant initialisation. Tête R0 distincte. Valeur NV B égale à `SHA256(base || tête B)`. Même plan figé avant tout effet, avec tentative durable et autorisation propres par opération, et zéro réussite avant constat. Ordre : plan figé avant tout effet ; index réellement absent, droits de plateforme vérifiés, définition exacte hors runtime PA ; zone publique `WRITTEN-clear` observée et nom calculé et rapproché ; première `Extend` d’initialisation ; nouveau `ReadPublic` et nom `WRITTEN-set` ; lecture `HMAC` de `BASE` réelle ; `R0` durable et synchronisé ; `Extend` B autorisée ; `HMAC` de `NV_B` réelle ; provenance puis publication finale. Trois opérations matérielles mutantes distinctes : `NV_DefineSpace` extérieur, `NV_Extend(INIT32)` extérieur, puis `NV_Extend(head_B)`, chacune avec tentative durable et autorisation propres, sous autorisations et constats propres. Aucun `Clear`, suppression, redéfinition, choix d’index automatique ou création par le runtime. Une issue inconnue exige réconciliation du même plan et de la même opération, jamais répétition aveugle. Ne prouve pas l’absence d’un index depuis un simple handle inaccessible. Ni administration B ni rapport CAB créant des droits TPM. D11 adopté pour la séparation des droits ne choisissant aucun algorithme. Zéro binaire, mode ou opération PG nouveaux. Identité administrative distincte du NV, d'E4 et du retrait. Nom et bit écrit avant et après gérés par provisionneur extérieur, jamais par garde du moteur. Base initiale avant plan contenue dans le profil attendu, jamais vrai compte rendu post-effet. Zéro publication future dans base, profil ou plan. Zéro auto-condensat et zéro cycle. Impacts : sans variante réalisée et qualifiée, instanciation, `Extend`, observation et qualification restent bloquées. Autorisation présente des quatre documents ne valant ni choix A, ni adoption de format, ni code B, ni effets TPM. Documentés pour revue C08 puis validation humaine, sans adoption INIT A ni code B ou effet matériel ; réalisation et qualification ensuite sous leurs autorisations ; forme de test ne vaut pas admission, code B non autorisé avant validation humaine du lot, sans autorisation de source créée par la correction documentaire.

#### Variante B non adoptée

Seul index préprovisionné avec base attendue de provenance historique positive antérieure indépendante et déjà qualifiée. Zéro initialisation dans le plan B. Autre précondition et autre preuve, sans repli.

#### Variante C non adoptée

Attente de fourniture d'une autre procédure.

### Profil `BootstrapInitProfile/v1` proposé

Statut : PROPOSÉ NON ADOPTÉ. Sans méthode, format ou code B adopté. Sans code ni effet produit, sans accès aux secrets, sans test ni matériel ; les écritures documentaires observées restent hors adoption. Sans admission, acte ou qualification. Ensemble entièrement révisable avant décision humaine ; option A seule décrite, sans sélecteur libre ni méthode de repli.

| Champ | Type exact | Contrainte | Provenance typée | Rôle |
|---|---|---|---|---|
| `object_type` | `str` | Égal à `pixs.agent.bootstrap_init_profile/v1` | Constante documentée | Typage du profil |
| `schema_version` | `str` | Égal à `1.0.0` | Constante documentée | Version du type, algorithme A seul |
| `init_profile_ref` | `str` UTF-8 bornée | Référence externe non vide, sans `C0`, `DEL` ou substitut, validité UTF-8, borne octets `max_ref_bytes` | Identifiant produit et figé par procédure extérieure autorisée | Identifiant repris dans `init_profile_binding` |
| `init_profile_version` | `str` UTF-8 bornée | Version externe non vide, mêmes contrôles | Identifiant produit et figé par procédure extérieure autorisée | Version reprise dans `init_profile_binding` |
| `installation_ref` | `str` UTF-8 bornée | Cible d’installation non vide, sans caractère générique, borne octets `max_ref_bytes` | Contexte résolu | Liaison installation et cible |
| `target_ref` | `str` UTF-8 bornée | Cible d’exécution non vide, sans caractère générique, borne octets `max_ref_bytes` | Contexte résolu | Liaison installation et cible |
| `tpm_context_binding` | `ContentBinding` fermé | `ref` égal à `context.context_ref`, `version` égale à `context.context_version`, `sha256` égal à `SHA256(CANON(contexte entier))` | Liaison vers contexte protégé courant | Désignation du contexte réel, sans preuve |
| `nv_profile` | Objet fermé, sept champs existants | Mêmes représentations et types que le profil B-NV, attributs exacts avec `WRITTEN-set` conservés pour le lecteur runtime | Contexte TPM distinct du nom | Cadre NV de référence, sans hiérarchie choisie |
| `initialization_input_hex64` | `str` | `^[0-9a-f]{64}$`, 32 octets publics exacts, pas un secret | Valeur publique explicite fixée avant plan, sans défaut | Entrée INIT32 de la dérivation |
| `authority_binding` | `ContentBinding` fermé | Même valeur que le vrai plan, configuration publique protégée antérieure seule | Liaison de données, sans autorité | Autorité désignée, résolution par propriétaire extérieur |
| `procedure_binding` | `ContentBinding` fermé | Même valeur que le vrai plan, configuration publique protégée antérieure seule | Liaison de données, sans autorité | Procédure désignée, sans droit nouveau |
| `executor_binding` | `ContentBinding` fermé | Même valeur que le vrai plan, configuration publique protégée antérieure seule | Liaison de données, sans autorité | Exécutant désigné, sans signataire nouveau |

Aucune attache de compte rendu post-effet, de plan futur, de Base, de recette, de tête ou de publication dans ce profil. Références et condensats ne créent aucune autorité ; leur résolution positive relève du véritable propriétaire extérieur. Aucun nouveau signataire ou droit matériel choisi.

`BASE` attendue est DÉRIVÉE, pas une seconde donnée libre : `SHA256(32 octets zéro || initialization_input32)`. `Base.expected_base_hex64` doit égaler cette dérivation et `Base.init_profile_binding` doit engager ce profil entier. Calcul préparatoire, sans effet et sans valeur NV zéro présumée observable. Ne concerne qu’une première `Extend` sur index neuf `WRITTEN-clear` effectivement prouvé. Formats, bornes U2 et Resource24, canon et binding extérieur complets.

`CANON` vaut `json.dumps(ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))` en UTF-8 sans saut final. Refus en cas de champ inconnu, duplication, booléen, nombre hors position entière non signée, nul, `C0`, `DEL` ou substitut, et en cas de limite exigée non respectée au point d’usage. `init_profile_binding` vaut `ContentBinding` avec `ref` égal à `profile.init_profile_ref`, `version` égale à `profile.init_profile_version`, `sha256` égal à `SHA256(CANON(profil entier))`, hors document de profil. Chaque valeur effective MUST provenir du profil protégé courant qualifié. Le contenu d’appel MUST NOT servir d’autorité.

Sources : [NV_Extend.c](https://raw.githubusercontent.com/microsoft/ms-tpm-20-ref/main/TPMCmd/tpm/src/command/NVStorage/NV_Extend.c), ancien condensat nul seulement si `WRITTEN-clear`, puis condensat et `WRITTEN-set`. [NV_spt.c](https://raw.githubusercontent.com/microsoft/ms-tpm-20-ref/main/TPMCmd/tpm/src/command/NVStorage/NV_spt.c), lignes 372 à 403, `WRITTEN`, `READLOCKED` et `WRITELOCKED` doivent être à zéro à la définition, `PLATFORMCREATE` et `POLICY_DELETE` exigent le vrai contexte de plateforme ; lignes 15 à 48, lecture de valeur refusée avant `WRITTEN`. Source courante seulement ; compatibilité 1.38 et cible matérielle restent à qualifier. Les types récents `TPMT_NV_PUBLIC_2` de la source consultée ne sont pas adoptés : PA conserve `TPMS_NV_PUBLIC` et les ABI `TSS2` adoptées. Le profil runtime B-NV conserve ses attributs exacts avec `WRITTEN-set` ; le provisionneur extérieur doit dériver et vérifier la zone publique pré-écriture explicitement, sans affaiblir le lecteur runtime ni employer ses masques depuis un candidat.

### Provenance initiale observée proposée

Statut : PROPOSÉE NON ADOPTÉE. Sans code, test, matériel ou secret. Sans admission, acte ou qualification. Document fermé antérieur à `B-FIN` ; `B-FIN` sera créé après et engagera cette provenance entière. Aucun lien vers `B-FIN` futur, signature, publication finale, propre condensat ou autre objet futur.

| Champ | Type exact | Contrainte | Provenance typée | Rôle |
|---|---|---|---|---|
| `object_type` | `str` | Égal à `pixs.agent.bootstrap_provenance_observed/v1` | Constante documentée | Typage |
| `schema_version` | `str` | Égal à `1.0.0` | Constante documentée | Version |
| `provenance_ref` | `str` UTF-8 bornée | Référence externe non vide, sans `C0`, `DEL` ou substitut, borne octets `max_ref_bytes` | Identifiant produit et figé par procédure extérieure autorisée | Identifiant repris dans le binding |
| `provenance_version` | `str` UTF-8 bornée | Mêmes contrôles | Identifiant produit et figé par procédure extérieure autorisée | Version reprise dans le binding |
| `installation_ref` | `str` | UTF-8 non vide et valide, sans `C0`, `DEL` ou substitut, sans caractère générique, borne octets `max_ref_bytes` | Contexte résolu | Liaison |
| `target_ref` | `str` | UTF-8 non vide et valide, sans `C0`, `DEL` ou substitut, sans caractère générique, borne octets `max_ref_bytes` | Contexte résolu | Liaison |
| `prepublication_binding` | `ContentBinding` fermé | Attache complète vers prépublication proposée | Liaison de données | Lien exact |
| `policy_binding` | `ContentBinding` fermé | Attache complète vers politique proposée | Liaison de données | Lien exact |
| `plan_binding` | `ContentBinding` fermé | Attache complète vers vrai plan | Liaison de données | Lien exact |
| `recipe_binding` | `ContentBinding` fermé | Attache complète vers recette proposée | Liaison de données | Lien exact |
| `initial_base_binding` | `ContentBinding` fermé | Reprend exactement le binding `BASE` existant | Liaison de données | Base dérivée |
| `init_profile_binding` | `ContentBinding` fermé | Attache complète vers profil `INIT` proposé | Liaison de données | Lien exact |
| `tpm_context_binding` | `ContentBinding` fermé | Attache complète vers contexte | Liaison de données | Lien exact |
| `r0_payload_binding` | `ContentBinding` fermé | `ref` égal à `R0.transition_ref`, `version` égale à `R0.schema_version` `1.0.0`, `sha256` égal à `SHA256(CANON(R0))` sur les seuls octets `CANON(R0)` | Objets figés | Charge `R0` |
| `r0_semantic_head_hex64` | `str` | `^[0-9a-f]{64}$`, tête sémantique de domaine `B` ; trois dérivations distinctes : charge canonique `R0`, tête sémantique `B`, reçu physique de trame | Objets figés, un seul `B` en position 0 puis `PG1.0` strict | Tête sémantique |
| `r0_physical_receipt_hex64` | `str` | `^[0-9a-f]{64}$`, égal à `hexlower(SHA256(ASCII("PIXS:PA:JOURNAL:RECORD:1.0.0") + LF + 32 zéros + uint32BE(len(payload_R0)) + payload_R0))`, depuis la première trame réellement relue et son cadrage vérifié ; ce zéro est le prédécesseur de la première trame, pas la `BASE` NV ; définitions séparées de `payload_hash`, tête `B` et reçu physique, sans inégalité numérique arbitraire imposée | File réelle rapprochée | Reçu physique |
| `nv_base_observed_hex64` | `str` | `^[0-9a-f]{64}$`, lecture `HMAC` après initialisation `INIT` et avant `ExtendB`, égale `BASE` dérivée, jamais `HMAC` avant `WRITTEN` | Observation extérieure rapprochée | Base observée |
| `nv_after_B_observed_hex64` | `str` | `^[0-9a-f]{64}$`, lecture `HMAC` après `ExtendB`, égale `SHA256(BASE32 \|\| headB32)` | Observation extérieure rapprochée | Après `B` |
| `observed_from_utc6` | `str` | Instant UTC `YYYY-MM-DDTHH:MM:SS.ffffffZ`, calendrier et ordre réels, avec `observed_from_utc6 <= observed_to_utc6`, égalité possible, exactement repris dans `B-FIN`, sans durée de validité implicite du constat historique | Période réelle | Début |
| `observed_to_utc6` | `str` | Même format UTC `YYYY-MM-DDTHH:MM:SS.ffffffZ`, avec `observed_from_utc6 <= observed_to_utc6`, égalité possible, exactement repris dans `B-FIN` | Période réelle | Fin |
| `authority_binding` | `ContentBinding` fermé | Mêmes liaisons publiques protégées antérieures que `INIT` et `PLAN` | Vérifiées par vrais propriétaires privés | Autorité désignée |
| `procedure_binding` | `ContentBinding` fermé | Mêmes liaisons antérieures que `INIT` et `PLAN` | Vérifiées par vrais propriétaires privés | Procédure |
| `executor_binding` | `ContentBinding` fermé | Mêmes liaisons antérieures que `INIT` et `PLAN`, désigne l’exécutant extérieur | Vérifié par vrai propriétaire privé | Exécutant |
| `definition_attempt_ref` | `str` UTF-8 non vide, sans `C0`, `DEL` ou substitut, borne octets `max_ref_bytes` | Référence non secrète distincte des deux autres tentatives, liée au même plan et à `NV_DefineSpace` par le propriétaire réel | Trace extérieure | Tentative définition |
| `initialization_attempt_ref` | `str` UTF-8 non vide, sans `C0`, `DEL` ou substitut, borne octets `max_ref_bytes` | Référence non secrète distincte des deux autres tentatives, liée au même plan et à `NV_Extend(INIT32)` par le propriétaire réel | Trace extérieure | Tentative initialisation |
| `bootstrap_extend_attempt_ref` | `str` UTF-8 non vide, sans `C0`, `DEL` ou substitut, borne octets `max_ref_bytes` | Référence non secrète distincte des deux autres tentatives, liée au même plan et à `NV_Extend(head_B)` par le propriétaire réel | Trace extérieure | Tentative `B` |
| `nv_public_before_initialization` | Objet fermé de six champs | `nv_index` `uint32` strict non bool dans `0x01000000..0x01ffffff`, `nv_attributes` `uint32` exacts, `nv_name_alg` littéral `SHA256`, `nv_data_size` `int` strict `32`, `nv_authpolicy_hex` `^[0-9a-f]{64}$`, `nv_name_hex` `^000b[0-9a-f]{64}$`, sans booléen ni valeur implicite et sans masque client, comparés exactement aux attendus protégés avant `WRITTEN`, nom recalculé | Zone publique observée | Public avant |
| `nv_public_after_initialization` | Objet fermé de six champs | Mêmes six types et bornes exacts que l’objet avant, dont `nv_index` `uint32` strict non bool dans `0x01000000..0x01ffffff`, sans booléen ni valeur implicite et sans masque client, comparés exactement aux attendus protégés après `WRITTEN`, nom recalculé | Zone publique observée | Public après |

Les trois tentatives sont des traces, pas des permissions ni des preuves portables. Aucun `maintenance_p256_ref` présenté comme champ `TPMS_NV_PUBLIC` observé. Les six valeurs ne remplacent ni les droits de plateforme ni l’authentification réelle du `TPM` par des valeurs déclarées. Aucune liste libre, booléen `verified`, secret, `HMAC` de session, `FD` ou condensat de credential. Le producteur extérieur et ses preuves restent à réaliser et qualifier ; un `DTO` ne les livre pas. Pas d’audit `PG` avant `PG`.

Les deux dates sont les dates exactes de `B-FIN`, sans expiration inventée du fait historique. Les validités de `PUB`, `POLICY` et `FIN` sont séparées et bornées. Les observations initiales restent historiques après avancement ; les autorisations initiales actuelles exigent leurs preuves courantes.

`CANON` vaut `json.dumps(ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))` en UTF-8 sans saut final. Refus en cas de champ inconnu, duplication, booléen, nombre hors position entière non signée, nul, `C0`, `DEL` ou substitut, et en cas de limite exigée non respectée au point d’usage. `ContentBinding` vaut exactement `{ref, version, sha256}` ; `ref` et `version` non vides UTF-8 valides, sans `C0`, `DEL` ou substitut, bornés par `max_ref_bytes` ; `sha256` vaut `^[0-9a-f]{64}$` ; toutes les comparaisons de contexte et tous les bindings sont explicites. Aucune attache vers `FIN` dans la provenance. La version de schéma n’est pas la version de clé admin. Les seules signatures sont `PUB` et `FIN` ; politique installée protégée reste non signée. Signatures et droits vérifiés séparément de ces condensats.

| Binding | `ref` exact | `version` exacte | `sha256` exact |
|---|---|---|---|
| prépublication | `document.prepublication_ref` | `document.schema_version` `1.0.0` | `SHA256(CANON(enveloppe entière document+signature))` |
| politique | `policy_ref` | `policy_version` | `SHA256(CANON(politique entière))` |
| plan | `plan_ref` | `plan_version` | `SHA256(CANON(plan entier))` |
| recette | `recipe_ref` | `recipe_version` | `SHA256(CANON(recette entière))` |
| base | `base_ref` | `base_version` | `SHA256(CANON(objet base entier))` |
| init | `init_profile_ref` | `init_profile_version` | `SHA256(CANON(profil init entier))` |
| contexte | `context_ref` | `context_version` | `SHA256(CANON(contexte entier))` |
| ressource | `profile_ref` | `profile_version` | `SHA256(CANON(profil entier))` |
| charge `R0` | `transition_ref` | `schema_version` `1.0.0` | `SHA256(CANON(R0))` |
| provenance | `provenance_ref` | `provenance_version` | `SHA256(CANON(provenance))` |
| publication finale utilisée plus tard | `document.publication_ref` | `schema_version` `1.0.0` | `SHA256(CANON(enveloppe entière))` |

Les deux enveloppes signées sont hachées entières, incluant `signature_b64` ; `R0`, provenance, politique et autres objets sont hachés selon leur canon entier, aucun propre condensat dans l’objet. Le binding de provenance vaut `ContentBinding` avec `ref` égal à `provenance_ref`, `version` égale à `provenance_version`, `sha256` égal à `SHA256(CANON(document entier))`, hors document. Chaque valeur effective MUST provenir du profil protégé courant qualifié. Le contenu d’appel MUST NOT servir d’autorité.

### Plan administratif de retrait PA proposé

Statut : PROPOSÉ NON ADOPTÉ. Sans code, test, matériel ou secret. Sans admission, acte ou qualification. Périmètre exact irréversible.

Provenance documentaire : le serveur C08 produit une proposition administrative NON AUTORISANTE depuis une nouvelle inspect_initial_authority Protégée PA et depuis ses propres sources applicatives et sa politique administrative actuelles. Ce plan n’est pas le TechnicalPlan PostgreSQL E5. L’inspection active peut renvoyer, dans un AdminResult18 inchangé, les deux liaisons ordonnées que sont l’AnchorSnapshot courant réel puis la publication B initiale réellement installée. C08 fige les identifiants logiques futurs operation_id et idempotency_key, sans inventer le futur A07. Aucun nouvel appel, endpoint, wrapper, catalogue ou mandat n’est créé. PA revalide ses faits techniques, la politique administrative et tous les engagements avant retrait ; aucun droit n’est accordé depuis le plan.

| Champ | Type exact | Contrainte | Provenance typée | Rôle |
|---|---|---|---|---|
| `object_type` | `str` | Égal à `pixs.agent.withdrawal_plan/v1` | Constante documentée | Typage |
| `schema_version` | `str` | Égal à `1.0.0` | Constante documentée | Version |
| `plan_ref` | `str` | UTF-8 non vide et valide, sans `C0`, `DEL` ou substitut, borne octets `max_ref_bytes` | Identifiant produit et figé par le serveur `C08` | Identifiant |
| `plan_version` | `str` | Mêmes contrôles de référence | Identifiant produit et figé par le serveur `C08` | Version |
| `installation_ref` | `str` | Mêmes contrôles de référence, sans caractère générique | Contexte résolu | Installation |
| `target_ref` | `str` | Mêmes contrôles de référence, sans caractère générique | Contexte résolu | Cible |
| `catalog_operation` | `str` | Égal à `withdraw_initial_authority` | Contrat admin déjà écrit | Opération |
| `catalog_version` | `str` | Égal à `1.0.0` | Contrat admin déjà écrit | Version catalogue |
| `operation_id` | `str` | Mêmes contrôles de référence | Contexte courant figé par C08 | Opération courante |
| `idempotency_key` | `str` | Mêmes contrôles de référence | Contexte courant figé par C08 | Idempotence |
| `policy_ref` | `str` | Mêmes contrôles de référence | Politique administrative courante vérifiée avec `C03` et `C04` | Politique |
| `policy_version` | `str` | Mêmes contrôles de référence | Politique administrative courante vérifiée avec `C03` et `C04` | Version politique |
| `initial_publication_binding` | `ContentBinding` fermé | Attache fermée vers publication `B`, document de configuration initiale distinct de la politique administrative et du droit personnel | Liaison de données | Publication |
| `anchor_binding` | `ContentBinding` fermé | Vrai `AnchorSnapshot` déjà défini, même contexte registre, époque et génération, jamais futur | Lecture actuelle authentifiée | Ancre antérieure |
| `installation_result_ref` | `str` | Mêmes contrôles de référence ; désigne un enregistrement privé courant du propriétaire `C08`, à résoudre par ses vrais contrôles, pas une attestation portable | Propriétaire `C08` | Résultat installation |
| `quiescence_scope` | `str` | Littéral égal à `stop_new_initial_preparations_and_quiesce_concerned_preparations` ; périmètre d’arrêt des nouvelles préparations initiales et de quiescence des préparations concernées de cette installation et cible ; ni preuve ni permission | Constante documentée | Périmètre |

`ContentBinding` vaut exactement `{ref, version, sha256}` ; `ref` et `version` bornés, `sha256` vaut `^[0-9a-f]{64}$`. `CANON` vaut `json.dumps(ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))` en UTF-8 sans saut final. Refus en cas de champ inconnu, duplication, booléen, nombre hors position entière non signée, nul, `C0`, `DEL` ou substitut. Le binding du plan vaut `ref` égal à `plan_ref`, `version` égale à `plan_version`, `sha256` égal à `SHA256(CANON(plan entier))`, hors document.

### Confirmation C08 spécifique au retrait proposée

Statut : PROPOSÉE NON ADOPTÉE. Produite et conservée par le serveur `C08` sous autorité réelle.

| Champ | Type exact | Contrainte | Provenance typée | Rôle |
|---|---|---|---|---|
| `object_type` | `str` | Égal à `pixs.c08.pa_initial_withdrawal_confirmation/v1` | Constante documentée | Typage |
| `schema_version` | `str` | Égal à `1.0.0` | Constante documentée | Version |
| `confirmation_ref` | `str` | Mêmes contrôles de référence | Propriétaire serveur `C08` | Identifiant |
| `confirmation_version` | `str` | Mêmes contrôles de référence | Propriétaire serveur `C08` | Version |
| `installation_ref` | `str` | Mêmes contrôles de référence | Contexte résolu | Installation |
| `target_ref` | `str` | Mêmes contrôles de référence | Contexte résolu | Cible |
| `operation_id` | `str` | Mêmes contrôles de référence | Contexte courant | Opération |
| `idempotency_key` | `str` | Mêmes contrôles de référence | Contexte courant | Idempotence |
| `plan_binding` | `ContentBinding` fermé | Plan de retrait ci-dessus | Liaison de données | Plan |
| `policy_ref` | `str` | Mêmes contrôles de référence | Politique administrative courante | Politique |
| `policy_version` | `str` | Mêmes contrôles de référence | Politique administrative courante | Version politique |
| `operator_ref` | `str` | Mêmes contrôles de référence ; désigne le signataire attendu | Propriétaire serveur | Opérateur |
| `operator_key_ref` | `str` | Mêmes contrôles de référence ; désigne la clé attendue | Propriétaire serveur | Clé |
| `confirmer_subject_ref` | `str` | Mêmes contrôles de référence ; sujet `C03` et `C04` | Propriétaires `C03` et `C04` | Confirmeur |
| `authorization_decision_ref` | `str` | Mêmes contrôles de référence ; décision d’autorisation réelle, relue et droit réévalué actuellement | Propriétaire serveur | Décision |
| `confirmed_at` | `str` | UTC `YYYY-MM-DDTHH:MM:SS.ffffffZ` réel ; vivacité, expiration, révocation et consommation relues auprès du propriétaire au point d’usage selon sa politique protégée, sans durée par défaut | Propriétaire serveur | Instant |
| `correlation_id` | `str` | Mêmes contrôles de référence ; trace conservée de cette confirmation, pas la provenance du futur A07 | Contexte courant | Corrélation |

Le vrai lien depuis le confirmeur `C03` et `C04` est vérifié par leur propriétaire dans l’état courant, jamais contenu dans une chaîne. Aucun acte, signature ou condensat du futur mandat, ni tableau de futurs `A07`. Même `CANON` et même binding fermé, avec `ref` égal à `confirmation_ref`, `version` égale à `confirmation_version`, `sha256` égal à `SHA256(CANON(confirmation entière))`.

### Bundle de preuves du retrait proposé

Statut : PROPOSÉ NON ADOPTÉ. Engagements documentaires stables et références typées à résoudre, pas les preuves d’une future invocation.

Provenance documentaire : C08 compose ce bundle depuis le plan et la confirmation ci-dessus, depuis ses prérequis vérifiés et depuis ses propres sources applicatives et sa politique administrative actuelles. PA revalide ses faits avant tout retrait. Aucun droit nouveau, aucun rôle nouveau, aucun signataire nouveau, aucun service nouveau.

| Champ | Type exact | Contrainte | Provenance typée | Rôle |
|---|---|---|---|---|
| `object_type` | `str` | Égal à `pixs.agent.withdrawal_proofs/v1` | Constante documentée | Typage |
| `schema_version` | `str` | Égal à `1.0.0` | Constante documentée | Version |
| `proofs_ref` | `str` | Mêmes contrôles de référence | Produit et figé par le serveur `C08` | Identifiant |
| `proofs_version` | `str` | Mêmes contrôles de référence | Produit et figé par le serveur `C08` | Version |
| `installation_ref` | `str` | Mêmes contrôles de référence | Contexte résolu | Installation |
| `target_ref` | `str` | Mêmes contrôles de référence | Contexte résolu | Cible |
| `operation_id` | `str` | Mêmes contrôles de référence | Contexte courant | Opération |
| `idempotency_key` | `str` | Mêmes contrôles de référence | Contexte courant | Idempotence |
| `plan_binding` | `ContentBinding` fermé | Plan ci-dessus | Liaison de données | Plan |
| `confirmation_binding` | `ContentBinding` fermé | Confirmation ci-dessus | Liaison de données | Confirmation |
| `installation_result_ref` | `str` | Mêmes contrôles de référence ; relu via vrais `C08ResultReader` et `GenericAuditReceipt` et contextes transactionnels propriétaires, avec prérequis et audits exacts | Propriétaire `C08` | Résultat |
| `authorization_decision_ref` | `str` | Mêmes contrôles de référence | Propriétaire serveur | Décision |
| `operator_ref` | `str` | Mêmes contrôles de référence | Propriétaire serveur | Opérateur |
| `operator_key_ref` | `str` | Mêmes contrôles de référence | Propriétaire serveur | Clé |
| `policy_ref` | `str` | Mêmes contrôles de référence | Politique administrative courante | Politique |
| `policy_version` | `str` | Mêmes contrôles de référence | Politique administrative courante | Version politique |
| `anchor_binding` | `ContentBinding` fermé | Ancre applicable | Lecture actuelle authentifiée | Ancre |
| `prepared_at` | `str` | UTC `YYYY-MM-DDTHH:MM:SS.ffffffZ` réel | Contexte courant | Instant |

Les contrôles natifs courants de la vraie requête `Critique` sont pris séparément de son vrai contexte, après réception et avant chaque effet. Aucune identité future ni booléen vérifié sérialisé avant le mandat. Résolution `C08` avec résultat confirmé, prérequis et audits exacts ; aucune recherche par condensat libre et aucun `SQL` direct `PA`. Source qualifiée indisponible égale refus. Même `CANON` et binding fermé avec `ref` égal à `proofs_ref`, `version` égale à `proofs_version`, `sha256` égal à `SHA256(CANON(bundle entier))`.

### Intention additionnelle fermée

Statut : PROPOSÉE NON ADOPTÉE. Objet fermé de sept champs pour `content_binding`.

| Champ | Type exact | Contrainte | Provenance typée | Rôle |
|---|---|---|---|---|
| `object_type` | `str` | Égal à `pixs.agent.withdrawal_intent/v1` | Constante documentée | Typage |
| `schema_version` | `str` | Égal à `1.0.0` | Constante documentée | Version |
| `installation_ref` | `str` | Mêmes contrôles de référence | Contexte résolu | Installation |
| `target_ref` | `str` | Mêmes contrôles de référence | Contexte résolu | Cible |
| `operation_id` | `str` | Mêmes contrôles de référence | Contexte courant | Opération |
| `request_binding` | `ContentBinding` fermé | `ref` égal à `AdminRequest.operation_id`, `version` égale à `schema_version` `1.0.0`, `sha256` égal à `SHA256(CANON(requête entière))` | Liaison de données | Requête |
| `signed_mandate_binding` | `ContentBinding` fermé | `ref` égal à `document.mandate_ref`, `version` égale à `document.schema_version` `1.0.0`, `sha256` égal à `SHA256(CANON(enveloppe signée entière))` | Liaison de données | Mandat signé |

Son binding vaut `ref` égal à `operation_id`, `version` égale à `schema_version`, `sha256` égal à `SHA256(CANON(intention entière))`. Aucun lien vers la future `JournalTransition`. Le mandat engage déjà les trois `Claims` fermés sans duplication inutile.

### Mapping journal fermé

`JournalTransition` `1.0.0` inchangé avec état `RETIRED` déjà présent : `operation_ref` égal à `AdminRequest.operation_id`, `mandate_binding` égal au binding du mandat signé, `content_binding` égal au binding de l’intention à sept champs. `mandate_binding` reste un `ContentBinding` complet avec `ref` égal à `document.mandate_ref`, `version` égale à `document.schema_version` `1.0.0`, `sha256` égal à `SHA256(CANON(enveloppe signée entière))`. `content_binding` est un `ContentBinding` avec `ref` égal à `Intent.operation_id`, `version` égale à `Intent.schema_version` `1.0.0`, `sha256` égal à `SHA256(CANON(Intent7 entier))`. Il n’est jamais un SHA scalaire. `transition_ref` unique, contexte actuel verrouillé, `sequence` égale à `queue.sequence + 1` sans dépassement, `previous_head_sha256` et `previous_nv_value_sha256` égaux à la file réelle observée ; avant effet, vérification native de toutes les autorités et réclamations réelles. La représentation `PG` accepte ces champs de forme sans valider l’opération administrative. Aucun quatrième catalogue `PG`, aucun préfixe `PG` de mandat réemployé ; `AdminMandate` conserve son domaine, sa classe et ses octets signés distincts. Tous artefacts liés préexistants et persistés avant intention, fsync et `Extend`, aucun cycle vers cette transition future.

Deux politiques distinctes : `bootstrap B` est configuration seule ; `policy_ref` et `policy_version` de ce lot sont la politique administrative courante vérifiée avec les propriétaires `C03` et `C04`, jamais un droit déduit de la clé admin `B`. Chaque valeur effective provient du propriétaire courant qualifié. Le contenu d’appel ne sert jamais d’autorité. Les bindings de forme et les enums `AdminResult` ne sont pas autorisants. Aucune disponibilité de port supposée.

### Séquences PA et Z12 en clauses

La séquence PA est acyclique : les prérequis et le plan sont établis d’abord, puis la confirmation est obtenue, puis les preuves sont composées, puis le mandat ADMIN personnel distinct R01 et PG-E4 est émis, puis les contrôles courants sont exécutés, puis la quiescence et le fencing sont appliqués, puis l’intention et la transition RETIRED sont rendues durables avec fsync, puis un recontrôle est effectué, puis l’Extend unique est réalisé, puis la valeur NV actuelle réellement authentifiée par session HMAC est lue et rapprochée de la valeur attendue après Extend ; aucun calcul local ne constitue cette observation, puis la preuve et le résultat sont établis. Aucun ancrage futur n’est utilisé pour son propre ajout. L’état inconnu garde les mêmes opérations et les mêmes ressources pour l’inspection et la réconciliation, sans répétition automatique. Toute nouvelle préparation initiale est bloquée après le retrait ; la remise minimale PBO canonique est préservée ; l’inspection est une nouvelle inspect_initial_authority Protégée avec son propre mandat, jamais get_postgresql_result. Le même intent réconcilié ne rejoue jamais l’Extend.

La séquence Z12 applique d’abord adopt_initial_trust avec état ADOPTED_FENCED, puis retire_initial_authority avec état INITIAL_AUTHORITY_RETIRED, puis un contrôle ordinaire indépendant. D8 est un résolveur de matériau TLS qui ne vaut ni adoption ni autorisation ordinaire. Il n’existe pas d’ordre total entre les retraits PA et Z12 ; la continuation légitime avant fermeture reste possible, sans grâce, sans recréation PKI, sans reset, sans migration. Le régime ordinaire global n’intervient qu’après les deux retraits et les contrôles ordinaires actuels, sans aucune réouverture en cas de panne PG, de reset ou d’expiration.

Le retrait est irréversible. La clé personnelle est vérifiée auprès d’Auth, C03 et C04 et elle est réellement distincte de adminB, CA, TLS et maintenance. La branche réelle et le matériau courants sont exigés.

### Comparaisons obligatoires

| Référence | `PLAN16` | `CONF17` | `PROOFS18` | `AdminRequest`, `AdminMandate` et `Claims` | `Intent7` | Contexte réel |
|---|---|---|---|---|---|---|
| installation et cible | `installation_ref` et `target_ref` | mêmes valeurs | mêmes valeurs | mêmes valeurs rapprochées exactement | mêmes valeurs | recoupés par le propriétaire courant |
| `operation_id` et idempotence | `operation_id` et `idempotency_key` figés par C08 | mêmes valeurs | mêmes valeurs | `AdminRequest.operation_id` rapproché ; l’idempotency_key est exactement identique dans PLAN16, CONF17, PROOFS18, AdminRequest et AdminMandate ; ce sont les corrélations et causalités A07 qui sont propres à la nouvelle invocation, pas la clé d’idempotence | `operation_id` seul puis `request_binding` et `signed_mandate_binding` ; sans `idempotency_key` propre | contexte courant ; l’idempotence, la politique et l’opérateur d’Intent7 se vérifient via leurs documents liés |
| politique | `policy_ref` et `policy_version` de politique administrative | mêmes valeurs | mêmes valeurs | `AdminRequest` ne porte pas de politique ; `AdminMandate` porte politique et opérateur | sans politique propre | politique administrative courante avec `C03` et `C04`, pas le bootstrap B CONFIGURATION_ONLY |
| opérateur et clé | sans opérateur propre | `operator_ref` et `operator_key_ref` | mêmes valeurs | mêmes valeurs dans le mandat | sans opérateur propre | clé publique personnelle résolue par la source `Auth` courante et réellement distincte de `adminB` et des clés `CA`, `TLS` et maintenance, pas seulement par un autre `ref` |
| plan et confirmation | plan propre | `plan_binding` vers `PLAN16` | `plan_binding` et `confirmation_binding` | `Claims` avec `plan_binding`, `confirmation_binding` et `proofs_binding` | `request_binding` et `signed_mandate_binding` | vérifiés par leurs propriétaires |
| `installation_result_ref` et `authorization_decision_ref` | `installation_result_ref` du plan chez C08 | pas d’`installation_result_ref` propre, seulement `plan_binding` ; décision et sujet du confirmeur avec `authorization_decision_ref` relue et droit réévalué | `installation_result_ref` et `authorization_decision_ref` relus chez leurs propriétaires | `AdminRequest` ne porte ni `installation_result_ref` ni `authorization_decision_ref` ; les deux références de prérequis et de décision passent par `Claims.proofs_binding` et `confirmation_binding` | sans résultat propre | relus dans leurs vrais contextes propriétaires |
| ancre | `anchor_binding` antérieure | sans ancre propre | `anchor_binding` applicable | `anchor_binding` du mandat | sans ancre propre | lecture actuelle authentifiée |
| corrélation | — | `correlation_id` comme trace conservée | — | nouvelle requête Critique avec ses propres corrélations, causalités et vraies identités et relation PZT vérifiées séparément | — | `correlation_id` de CONF17 n’est pas la provenance du futur A07 |

Confirmation et preuves ni signées ni autorisantes par leur seule forme.

### Futur raccord privé de vérification

Le futur raccord privé s’adresse au propriétaire `C08`, via le transport `PZT` et `A07` autorisé, à partir de ces références et du vrai contexte `Critique` après réception. Aucun nouveau canal, service ou catalogue créé ; aucune disponibilité affirmée. Il relit la confirmation conservée, le lien `C03` et `C04` au signataire, la décision courante `WITHDRAW_PA_INITIAL` et le résultat confirmé avec prérequis et audits exacts sous leurs vrais contrôles propriétaires, ainsi que le résultat d’installation confirmé, les migrations, R01, Core et Auth, les audits exacts et les contextes propriétaires. Il ne transforme pas `GenericAuditReceipt` en recherche publique par condensat ni `C08ResultReader.guard_confirmed` en attestation portable. Le bundle ne contient pas le futur `A07` : sa nouvelle provenance native et sa relation sont vérifiées séparément. Aucun SQL direct PA. Source ou garde absente égale refus. Cette réalisation et cette qualification sont une dépendance d’implémentation, pas un choix humain nouveau. Aucun droit, rôle, signataire ou service nouveau.

### Sémantique de `proof_bindings` d’`AdminResult`

Structure à dix-huit champs inchangée. Le succès de retrait immédiat exige deux bindings ordonnés : vers la `JournalTransition` `RETIRED` réellement persistée puis vers le nouvel `AnchorSnapshot` à dix-sept champs réellement acquis par `HMAC`, avec même contexte, séquence, tête et `NV`, signature et réclamations `Admin` vérifiées par leurs propriétaires. Le premier binding porte `ref` égal à `transition_ref`, `version` égale à `schema_version` `1.0.0`, `sha256` égal à `SHA256(CANON(transition entière))`. Le second porte `ref` égal à `snapshot_ref`, `version` égale à `schema_version` `1.0.0`, `sha256` égal à `SHA256(CANON(snapshot entier))`. À l’instant de confirmation exclusive, la séquence, la tête et le NV correspondent à cette transition. Pour une inspection ultérieure avec une queue avancée, l’inclusion du retrait est vérifiée dans la chaîne courante entière et le NV actuel, sans figer la tête. En l’absence de preuve, les états existants appropriés sont conservés et aucune paire n’est fabriquée ; la règle des deux preuves ne s’applique pas aux simples résultats UNKNOWN et assimilés. Si le profil ne peut pas représenter ces deux preuves, refus avant effet. Un échec fsync, `Extend`, confirmation, nettoyage ou une réponse perdue ne reçoit pas un succès. L’inspection est une nouvelle `inspect_initial_authority` `Protégée` avec son propre mandat, pas `get_postgresql_result`. Enums existants inchangés, `WITHDRAWN_DECLARED` reste déclaratif et ne prouve rien. Aucune disponibilité de port livrée supposée.

`ContentBinding` complet, canon sans antislash devant les guillemets, dates UTC6 à calendrier réel et ordre vérifié, refus de type, coercition, champ inconnu, duplicat et nul exigés pour les quatre objets. Chaque binding a ses `ref`, `version` et `SHA` exacts. Aucune valeur de production, aucun booléen `verified`, aucun droit ni signataire nouveau. La réalisation et la qualification du raccord `C08` sont une dépendance d’implémentation. Ce lot est proposé non adopté et devra être relu par C08 puis soumis au développeur avant tout code B.

### Clarifications de la revue propriétaire C08

La référence de résultat d’installation est une référence opaque détenue par le propriétaire C08, dont le producteur et le résolveur restent à réaliser. Elle ne s’assimile ni à la clé primaire installation_ref ni à une result_ref logique Core. Le modèle actuel distingue la clé primaire installation_ref de result_ref, result_version et authorization_ref, avec un writer imposant result_ref à partir d’installation_ref ; inspect_confirmed(act)->str|None et guard_confirmed(installation_ref=...) exigent un writer, un acte, une configuration protégée déjà liés et un vrai contexte, sans accepter installation_result_ref comme lookup libre. Les valeurs sont recoupées et aucune attestation portable n’est admise.

La référence de décision d’autorisation désigne la décision administrative de retrait d’autorité initiale, à produire et à résoudre, sans supposer une interface déjà existante. Le sens historique de la référence d’autorisation R01 et l’identifiant optionnel de décision d’audit restent distingués, sans imposer d’inégalités brutes entre chaînes de namespaces différents. La confirmation et le bundle de preuves portent la même décision de confirmation, avec égalité explicite et revalidation actuelle indépendante de l’ancien R01. Une correspondance typée future reste possible, sans assimilation à un octroi.

Les identifiants d’opération et d’idempotence sont préalloués et identiques dans le plan, la confirmation, les preuves, la requête et le mandat, sans constituer une future invocation déjà observée. Les références d’invocation, de corrélation et de causalité sont comparées sur la vraie requête Critique reçue, avec tableaux complets dont l’ordre et les doublons sont préservés, sans réemploi de l’inspection, de la confirmation ou de R01. L’identifiant de corrélation de la confirmation reste sa trace propre et non la provenance d’un futur A07. Le retrait withdraw_initial_authority exige strictement params==() ; l’inspection inspect_initial_authority accepte params==() ou subject_operation_ref seul ; trois Claims et AdminMandate27 restent inchangés.

## Annexe du 26 octobre 2026 — fondations B écrites, non testées

Le lot documentaire B/retrait + INIT A reste adopté sans modification ni revalidation ; les canons adoptés sont inchangés. Codecs écrits sous mandats CAB unitaires, forme publique seulement : Context8, huit champs exacts (object_type, schema_version, context_ref, context_version, installation_ref, target_ref, tcti_backend_ref, usage_custody_ref), APIs publiques encode_bootstrap_context, decode_bootstrap_context, bootstrap_context_binding ; NV7, sept champs exacts (nv_index, nv_attributes, nv_name_alg, nv_data_size, nv_authpolicy_hex, nv_name_hex, maintenance_p256_ref), APIs publiques encode_bootstrap_nv_profile, decode_bootstrap_nv_profile, sans binding autonome ; INIT12, douze champs exacts (object_type, schema_version, init_profile_ref, init_profile_version, installation_ref, target_ref, tpm_context_binding, nv_profile, initialization_input_hex64, authority_binding, procedure_binding, executor_binding), APIs publiques encode_bootstrap_init_profile, decode_bootstrap_init_profile, bootstrap_init_profile_binding (SHA256 du canon du profil entier), bootstrap_expected_base_hex64. INIT A calcule une attente SHA256(32 zéros || entrée32) sans observation. Corps des bindings et Name sont des données et ne prouvent ni identité TPM, ni autorité, ni permission.

Recoupement des bits avec [l'en-tête officiel tpm2-tss des types TPM 2.0](https://raw.githubusercontent.com/tpm2-software/tpm2-tss/master/include/tss2/tss2_tpm2_types.h), sans relever de version ni prétendre la compatibilité 1.38.

Preuves exactes des dix fichiers : voir l'annexe VALIDATION.md du même jour. État : 58 fichiers suivis (25 de réalisation, 33 de tests), 131 méthodes préparées non exécutées, aucune qualification produit.

Reste dû : Base8, Resource24, Policy14, PUB/FIN, recette et R0, provenance, scanner mixte, admission et retrait effectifs ; vrais producteurs et résolveurs D11/D13/D14/temps/PZT/handlers/résultats/lifecycles, puis campagne LXC et effets matériels sous plan exact distinct. Aucun port livré, admission, NV/SQL, installation, secret, Git ou archive.

## Réalisation partielle Base8 — 26/10/2026, FORME PYTHON seulement

Contrats Base8 réalisant la forme (8 champs, coords, bindings, derive et rapprochements ci-dessus) sans changer les formats adoptés ; graphe optionnel sans rôle/catalogue nouveau. Preuves : 37 + 69 tests et 4 contrôles en VALIDATION.md ; Cython/link/builtin positif/PZT/TPM et qualification globale restent non faits.


## Annexe Resource24 — 26/10/2026, contrats 24 inchangés

Contrats Resource24 inchangés, 24 champs exacts : object_type, schema_version, profile_ref, profile_version, installation_ref, target_ref, registry_ref, registry_generation_ref, epoch, first_sequence, payload_max_json_bytes, payload_max_ref_bytes, payload_max_observation_refs (>0 sans plafond), max_epoch, max_sequence, max_correlation_refs, max_causation_refs, max_bytes (59..INT63_MAX, sans borne SIZE_MAX), max_record (<=SIZE_MAX-65, record+58<=max_bytes), max_records, max_validity_span_ns, max_command_bytes (10..), max_response_bytes (10..), operation_budget_ns. APIs (value, limits)->str, (text, limits)->DTO, (value, limits)->ContentBinding PG réel ; type exact ; forme complète en __post_init__ ; plafonds externes aux APIs ; caractère * interdit dans installation_ref et target_ref, autres références opaques ; canon trié compact ; SHA du canon entier. Aucune deadline_ns, horloge, auto-autorité ou qualification produit.


## Annexe Policy14 — 26/10/2026, contrats 14 inchangés

Contrats Policy14 inchangés, 14 champs exacts : encode et binding (value,limits,resource_profile), decode (text,limits,resource_profile) ; types publics PG/NV7/Resource24 réels sans providers qualifiés, 2 bindings PG fermés, UTC6 calendaire réel, 0<span_ns<=max_validity_span_ns inclusive, recoupe DATA sans authentifier l'origine, binding POLICY entier pour FIN ultérieur seul, sans data_equal/bool/clé/signature/port. Graphe optionnel sans rôle nouveau. Preuves 13+81 et syntaxes en [VALIDATION.md](VALIDATION.md) ; B/INIT_A/C08/Z12 inchangés ; aucune coche 2-10.
