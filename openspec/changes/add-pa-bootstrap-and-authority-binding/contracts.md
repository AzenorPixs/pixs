# Contrat sémantique proposé — provisionnement PA02

Statut proposé, non opérationnel. Noms proposés, pas classes livrées. Référence : [pixs-agent](../../specs/pixs-agent/spec.md). Détails relation dans [identity-bindings.md](./identity-bindings.md), autorités dans [authority-policy.md](./authority-policy.md).

Les références d'ancrage et racines apportées par le candidat ne créent aucune autorité. Le contexte protégé installé choisit les racines attendues, valide origine et autorisation opérateur, puis compare toutes les liaisons. Preuves produites séparées du contenu candidat, aucune autocertification.

## Table des objets sémantiques

| Objet | Champs sémantiques | Type et source | Propriétaire et usage | Refus |
|---|---|---|---|---|
| Document provisionnement | version de schéma, référence PA stable, référence relation stable, révision et configuration candidates comme attributs proposés sans faire identité, autorité logique, périmètre, liaisons de contexte protégé, références opaques de secrets sans valeurs secrètes, références d'ancrages | types, champs obligatoires ou conditionnels et limites à fermer par profil, preuve opérateur séparée du contenu | PA02 désigne le lot, producteur et propriétaire de l'état technique égale procédure locale PA autorisée, consommateur égale composition PA concernée, contrats, adapter et stockage réels à désigner avant code | candidat forgé ou incomplet refusé, référence de confiance du seul candidat jamais autorité |
| Approbation opérateur | référence opérateur, liens vers octets exacts, cible, contexte, périmètre, version et validité applicable | proposition liée au contenu exact | usage admission initiale | cible ou octets modifiés refusés |
| État inspectable | non-provisionné, en-cours, prêt, échoué | source procédure locale PA autorisée à désigner et qualifier, absence bloquante pour la tranche concernée, sans autorité locale Django ou PostgreSQL | usage diagnostic et blocage | état ambigu refusé |

Obligatoire ou conditionnel selon profil à fermer. Pas d'import du format PG. Forme, intégrité, origine, autorisation et effet restent distincts. Validité courante des preuves selon leur contrat ; temps inconnu ferme seulement actes dépendants.

## Table des transitions

| Départ | Condition | Arrivée |
|---|---|---|
| non-provisionné | origine et autorisation validées, verrou et contexte vérifiés | en-cours |
| en-cours | persistance atomique durable et sources requises valables | prêt |
| en-cours | échec reconnu et état durable | échoué |
| panne en en-cours | réconciliation de l'état persisté avant rejeu ; prêt seulement si engagement durable exact et conditions propres prouvées ; échoué seulement si faillite reconnue ; sinon en-cours avec diagnostic inconnu sous réconciliation et verrous préservés, sans rejeu aveugle ni fausse preuve | prêt ou échoué, sinon en-cours avec diagnostic inconnu |
| réessai après échec reconnu | nouvelle autorisation courante encadrée, même identité technique stable, sans dupliquer autorisation ou opération déjà engagée ; aucune réutilisation d'autorisation expirée ou consommée | en-cours sans duplication |
| base PG ou PZT indisponible | provisionnement initial local indépendant de la base et du transport non encore préparés, peut s'achever pour ses prérequis propres prouvés ; échanges PBO et PA fermés jusqu'à PZT valide ; actes PG dépendants indisponibles sans PG ; prêt de provisionnement ne prouve ni transport ni base ni admission ni mandat ; aucun canal PBO et PA direct local | prêt local borné aux prérequis propres, sinon en-cours bloqué |

Stockage technique local proposé, propriétaire procédure locale PA autorisée à désigner et qualifier, absence bloquante pour la tranche concernée, sans autorité locale Django ou PostgreSQL : entrée protégée, instantané cohérent, version, exclusion, fencing, validation durable. Mécanisme et bornes réels à fermer et qualifier, pas d'outil installé nommé. Corruption, restauration obsolète ou racines périmées bloquants, pas de remise à zéro automatique, pas d'équivalence avec journal NV ni anti-retour matériel.


## Contrat de forme v1 — fermeture pour revue Codex — addendum 2026-10-26

Cet addendum fait autorité pour la première unité pure, sans modifier l'historique. La validation réelle reste à faire sur preuves. Il ne vaut ni qualification ni exécution.

### Clés du document wire v1

Le document wire est un objet JSON fermé à 17 clés, toutes requises et jamais omises. Les clés nullables restent présentes avec la valeur null.

1. anchor_ref : chaîne opaque non vide, sans contrôles ASCII 0x00-0x1F ni 0x7F, UTF-8 valide, taille en octets inférieure ou égale à max_ref_bytes. Jamais interprétée comme UUID, URI, chemin, commande, secret ou autorisation.

2. anchor_version : chaîne opaque de version du propriétaire, mêmes règles opaque, non fixée à 1.0.0.

3. authority_ref : chaîne opaque, mêmes règles opaque.

4. config_revision_ref : chaîne opaque, mêmes règles opaque, distincte de l'époque et de la génération d'autorité.

5. document_ref : chaîne opaque, mêmes règles opaque.

6. object_type : constante exacte pa.provisioning.document/v1.

7. pa_id : chaîne UUIDv7 canonique minuscule de 36 caractères, version 7 et variante RFC 4122.

8. policy_ref : chaîne opaque, mêmes règles opaque.

9. policy_version : chaîne opaque de version du propriétaire, non fixée à 1.0.0.

10. relation_ref : chaîne opaque, mêmes règles opaque.

11. resource_perimeter_ref : chaîne opaque, mêmes règles opaque, distincte du scope.

12. resource_perimeter_version : chaîne opaque de version du propriétaire, non fixée à 1.0.0.

13. schema_version : constante exacte 1.0.0.

14. scope_id : chaîne opaque non vide ou null selon scope_type.

15. scope_type : valeur exacte PLATFORM ou TENANT.

16. secret_refs : tableau JSON fermé d'objets SecretRef, ordre conservé, longueur de 0 à max_secret_refs. Les couples ref et version exactement dupliqués sont refusés.

17. tenant_id : chaîne opaque non vide ou null selon scope_type.

Règle de scope : PLATFORM exige tenant_id null et scope_id null. TENANT exige tenant_id opaque non vide et scope_id opaque non vide ou null.

Objet SecretRef : objet JSON fermé à deux clés exactes ref et version, sans champ supplémentaire. ref est une chaîne opaque non vide. version est une chaîne opaque de version du propriétaire. Mêmes règles sans contrôles ASCII, UTF-8 valide, taille en octets inférieure ou égale à max_ref_bytes.

### Structures Python

ProvisioningLimits : max_json_bytes de type int exact strictement positif, unité octets UTF-8 du document. max_ref_bytes de type int exact strictement positif, unité octets UTF-8 par référence opaque. max_secret_refs de type int exact strictement positif, unité nombre de références secret_refs. Paramètres locaux non sérialisés dans le document.

SecretRef : ref de type str exact. version de type str exact. Les trois structures proposées sont des dataclasses avec frozen=True, slots=True et repr=False, sans valeur par défaut mutable ni coercition ; tous les champs de document et de limites sont explicitement fournis, y compris les nullables ; les invariants de construction sont indépendants du profil et les contrôles de profil sont refaits en encodage et en décodage. Le repr ne contient aucune valeur de référence. Aucun état ni aucune autorité n'est porté par la simple construction.

ProvisioningDocument : anchor_ref de type str exact. anchor_version de type str exact. authority_ref de type str exact. config_revision_ref de type str exact. document_ref de type str exact. object_type de type str exact. pa_id de type uuid.UUID exact. policy_ref de type str exact. policy_version de type str exact. relation_ref de type str exact. resource_perimeter_ref de type str exact. resource_perimeter_version de type str exact. schema_version de type str exact. scope_id de type str exact ou None exact. scope_type de type str exact. secret_refs de type tuple exact de SecretRef. tenant_id de type str exact ou None exact.

### Signatures

decode_provisioning_document(data:bytes, limits:ProvisioningLimits) retourne ProvisioningDocument. encode_provisioning_document(value:ProvisioningDocument, limits:ProvisioningLimits) retourne bytes.

Aucune fonction de condensat, d'ancrage, de signature ni d'horloge n'est imposée dans cette tranche.

### Diagnostic unique

Type unique ProvisioningContractError héritant de ValueError. Code unique PROVISIONING_INVALID pour tous les refus de forme. Élément provisioning_document. Étape validate_provisioning_document. Message fixe : Contrat provisionnement invalide. Toute exception attendue du parseur, d'Unicode ou d'UUID est transformée sans fuite, sans valeur ni objet reçu et sans cause brute vers l'appelant. Les erreurs inattendues ne sont pas masquées.

### Règles de lecture et de canonicité

Le profil est vérifié avant toute lecture : type exact ProvisioningLimits et trois entiers exacts strictement positifs, booléens et sous-classes refusés. L'entrée de décodage est de type bytes exact. Le décodage est UTF-8 strict, avec rejet du BOM initial EF BB BF et des surrogats malformés. La taille en octets du document est inférieure ou égale à max_json_bytes.

La profondeur maximale est 3, dérivée du schéma : objet document au niveau 1, tableau secret_refs au niveau 2, objets SecretRef au niveau 3. Elle est contrôlée avant json.loads en tenant compte des chaînes et des échappements de guillemet et de barre oblique inverse. Tout conteneur supplémentaire est refusé.

La lecture JSON refuse les clés inconnues, les clés manquantes parmi les 17, les clés dupliquées, tout nombre entier ou flottant, tout booléen, toute constante NaN Infinity et tout null inattendu. Les fonctions parse_int et parse_float refusent avant conversion. Seuls tenant_id et scope_id admettent null.

Les contrôles ASCII 0x00-0x1F et 0x7F sont refusés dans les opaques. Chaque opaque non vide respecte sa borne en octets. La racine est un objet exact, secret_refs est une liste exacte et chaque SecretRef est un objet exact.

La construction directe du DTO vérifie ses invariants sans profil. L'encodage et le décodage recontrôlent le profil et tous les champs à chaque usage, y compris pour un objet altéré après construction. Aucun appel str, repr, conversion utilisateur ni accès attributaire n'est fait sur des types non vérifiés.

Les octets reçus doivent être exactement égaux à la réémission canonique : tri des clés, séparateurs virgule et deux-points sans espace, sortie UTF-8 directe sans échappement ASCII forcé, refus des nombres non finis, sans saut de ligne final. Sinon refus sans normalisation. Rendre les octets canoniques suffit.

La borne max_ref_bytes porte sur les références opaques seulement, pas sur les constantes object_type et schema_version ni sur la forme UUID de 36 caractères. Les bornes max_json_bytes et max_secret_refs strictement positives peuvent être trop petites pour un document particulier, sans défaut inventé.

### Exemple canonique intégral et profil TEST

Profil TEST synthétique non opérationnel : max_json_bytes 8192, max_ref_bytes 256, max_secret_refs 4. Il ne devient ni défaut ni limite de production.

Exemple canonique synthétique : {"anchor_ref":"anchor-synth-001","anchor_version":"v-opaque-001","authority_ref":"authority-synth-001","config_revision_ref":"cfgrev-synth-001","document_ref":"doc-synth-001","object_type":"pa.provisioning.document/v1","pa_id":"0193a1b2-c3d4-7e5f-8a90-1234567890ab","policy_ref":"policy-synth-001","policy_version":"v-opaque-pol-001","relation_ref":"rel-synth-001","resource_perimeter_ref":"perim-synth-001","resource_perimeter_version":"v-opaque-perim-001","schema_version":"1.0.0","scope_id":null,"scope_type":"PLATFORM","secret_refs":[{"ref":"sec-synth-001","version":"v-opaque-sec-001"}],"tenant_id":null}

### Matrice de cas concrets

Cas nominaux : document PLATFORM décodé puis réencodé à octets identiques. Document TENANT avec scope_id null accepté. Document TENANT avec scope_id texte accepté. secret_refs vide accepté.

Cas de refus : clé inconnue. Clé manquante parmi les 17. Clé JSON dupliquée. Nombre entier ou flottant. Booléen ou constante. BOM initial. Texte non canonique par espaces, ordre, échappement ASCII ou saut final. UUID non v7 ou non canonique. Scope PLATFORM avec tenant ou scope non null. Scope TENANT avec tenant vide ou manquant. Opaque vide, avec contrôle ASCII ou de taille supérieure à max_ref_bytes. secret_refs de longueur supérieure à max_secret_refs ou couple exactement dupliqué. Profondeur 4 ou conteneur supplémentaire. Document de taille supérieure à max_json_bytes.

Cas aux limites : document à max_json_bytes octets accepté, à max_json_bytes plus un refusé. secret_refs à max_secret_refs accepté, à max_secret_refs plus un refusé. Opaque à max_ref_bytes octets acceptée, à max_ref_bytes plus un refusée. Opaque multi-octets mesurée en octets UTF-8, par exemple accents ou idéogrammes, refusée si ses octets dépassent max_ref_bytes même si son nombre de caractères est inférieur.

### Confiance et périmètre

Un codec ne certifie pas qu'une chaîne opaque est une référence autorisée. Il ne résout rien, ne vérifie aucun secret et n'accorde aucune confiance. Il ne promet ni preuve valide ni secret valide ni détection sémantique de secret. Aucune entité DigitalIdentity n'est créée. Les règles de scope existantes de Core sont reproduites sans import du paquet agent, sans import PBO et sans classe privée.

## Addendum RSMP données et engagement — principes A ADOPTÉS, code et qualification restants
Choix A ADOPTÉ le 2026-10-26 ; B non retenu. Principes ADOPTÉS : données et règles ci-dessous ; code et qualification restant à réaliser sous revue Codex normale. Données non secrètes persistables : pa_id stable UUIDv7 canonique, relation_ref opaque, autorité logique citée, périmètre et version, config_revision_ref, scope PLATFORM TENANT, secret_refs comme références opaques jamais valeurs, versions et validités apportées comme références, operation_id et idempotence, instantané versionné. Secrets via refs provider existant, jamais valeurs. Engagement durable : écriture tmp, fsync fichier, rename atomique, fsync répertoire parent, puis réponse. Réponse avant fsync refusée. Concurrence : exclusion flock, fencing au point d'effet par consommateurs réels, ancien opérateur réellement empêché avant réouverture. Crash : avant effet, réconciliation avant tout nouvel effet, aucune autorisation consommée ou périmée ne revit, identité stable conservée, reprise sous preuves et autorisation courantes sans rejeu automatique ; entre effet et commit réconciliation avant réengagement ; après commit sans double effet ; réponse dupliquée sans réexécution. Corruption fichier plein permission refusée instantané ancien fermés sans reset auto. Restauration obsolète fermée, migration seulement explicitement autorisée. Aucun checksum ne crée confiance. Bornes profils déclarées sans défaut, TEST synthétique non prod.

## Addendum backend liaison unique — contrat final A
### 1. Profil donnees, pas preuve
StoreProfile{expected_uid:int>=0, expected_gid:int>=0, expected_dir_mode:int==0o700, expected_file_mode:int==0o600, max_revisions:int>0, max_journal_bytes:int>0, max_op_len:int>0, max_idem_len:int>0, limits:ProvisioningLimits{max_json_bytes:int>0,max_ref_bytes:int>0,max_secret_refs:int>0}}: tous exacts requis sans defaut. 0 UID/GID valide. Aucun root_fd serialise. Aucune creation repertoire, aucun umask global modifie. Creation fichiers sous masque ambiant puis fstat/fchmod du seul nouveau FD vers 0600 si besoin, sans toucher preexistants. Refuse S_ISUID/S_ISGID/S_ISVTX, type exact S_IFDIR dir / S_IFREG fichiers, pas comparaison mode&0777 seule. Domaines format: UID/GID et longueurs op/idem/doc en uint32, compteurs en uint64, max_journal_bytes en off_t positif64 retenu, champs ProvisioningLimits aux domaines numeriques serialisables correspondants sans changer codec seul; domaines non quotas prod; budgets contenus derives tailles reelles, meta calculee avant IO et chaque fichier borne, sans 512; trop petit refuse avant effet. Total=sum doc_len engages; seq==revisions en append-only; enveloppes physiques bornees par max_journal_bytes reel, aucun budget/nombre defaut invente.
### 2. Liaison et revisions
Fixe 7 champs initiaux: pa_id, authority_ref, relation_ref, resource_perimeter_ref, scope_type, tenant_id, scope_id. resource_perimeter_version et autres versions stockees seulement, jamais fraiches/autorisees. Premier append fixe liaison.
### 3. Fichiers et FD
Repertoire existant fourni via root_fd emprunte. Fichiers prives constants: meta.v1.json, journal.v1.log, snapshot.v1.bin, lock.v1.lock, tmp.v1.tmp. Init exclusive unique create_store_and_open(root_fd:int, profile:StoreProfile)->handle interne: cree seulement les 4 fichiers O_EXCL|O_NOFOLLOW, jamais repertoire. open_store(root_fd:int,profile)->handle: duplique O_CLOEXEC, verifie dir/UID/GID/mode/nlink dir, ouvre lock EX|NB tenu vie handle, lit sans creer/reparer. Chaque handle son FD lock. Inspection ne convertit pas SH. Tmp preexistant jamais adopte; open sur queue/tmp residuel/discordance refuse, ferme FD propres, ne laisse aucun verrou. Apres echec handle failed interdit ajouts, fichiers conserves, close ferme FD propres une fois.
### 4. Meta JSON ferme
Cles exactes: {format:str==store-meta/v1, version:int==1, max_revisions:int, max_journal_bytes:int, max_op_len:int, max_idem_len:int, limits:{max_json_bytes:int,max_ref_bytes:int,max_secret_refs:int}}. Serialisation canonique exacte de la table StoreProfile (seules cles listees) calculee avant IO; taille reelle bornee avant creation puis a l ouverture octets compares EXACTEMENT a cette serialisation attendue, sans lecture JSON generique meta donc aucun doublon/cle supplementaire accepte. Zero 512. Bornes profile controlees avant calcul. Tailles reelles journal/snapshot/tmp/meta bornees explicitement sans pretendre borner allocation disque physique.
### 5. Formats binaires reels
Journal header 8: MAGIC 50 41 4A 31 + u16BE 1 + u16BE 0. Record stocke commence par seq, pas MAGIC: u64BE seq>=1, u32BE op_len 1..max_op_len + op:str exact non vide UTF-8 strict sans 0x00-0x1F/0x7F ni surrogats borne octets, u32BE idem_len 1..max_idem_len + idem:str exact meme regle, u32BE doc_len 1..limits.max_json_bytes + doc bytes canoniques valides codec public, 32 doc_sha256=SHA256(doc), 32 prev_head (zeros seq1), 32 record_sha256=SHA256(header8 + corps exact jusqu a prev_head). Snapshot: MAGIC 50 41 53 31 + u16BE1+u16BE0, u64BE seq, u64BE revisions (=seq), u64BE total, u32BE op_len+op, u32BE idem_len+idem, u32BE doc_len+doc, 32 head == record_sha256 dernier. Vide: seq=0,revisions=0,total=0,op_len=0,idem_len=0,doc_len=0 sans payloads, head 32 zeros, meme ordre/largeurs. Refuse troncature/surplus/cles supplementaires. Corps verifie liaison/compteurs/somme/chaine/octets/tete.
### 6. Signatures typées
create_store_and_open(root_fd:int, profile:StoreProfile)->StoreHandle interne. open_store(root_fd:int, profile:StoreProfile)->StoreHandle. append(handle:StoreHandle,data:bytes,op:str,idem:str,expected_head:str)->AppendNew|AppendExisting. read_last(handle:StoreHandle)->bytes. read_seq(handle:StoreHandle,seq:int)->bytes. inspect(handle:StoreHandle)->StoreStatus{seq:int,revisions:int,total:int,head:str(hex64),state:str}: seuls EMPTY et COHERENT en retour reussi avec donnees; queues/tmp/discordances levent INCOMPLETE_TAIL/TMP_RESIDUEL/DISCORDANT. AppendNew{kind:str==STORED_NEW,seq:int,written:int,head:str(hex64)}: recu local. AppendExisting{kind:str==OBSERVED_EXISTING,seq:int,head:str(hex64)}: observation existant sans nouveau fsync. Tous donnees/recus locaux, aucune preuve autorite. Vide: read_last refuse EMPTY, read_seq hors 1..seq refuse OUT_OF_BOUNDS. StoreError(ValueError) code=STORE_INVALID element=store step=validate_store message=Magasin invalide. repr fixe StoreError(STORE_INVALID) sans valeur recue. Ordre retry exact: idempotence d abord (meme couple+octets/liaison -> Existing; op OU idem existant divergent -> refuse; puis tete expected_head:str exact hex64 minuscule 64 requis egal head courant verifie avant coercition). Erreurs fermees: INVALID_ARGS,NOT_A_DIRECTORY,OWNER_MISMATCH,MODE_MISMATCH,SPECIAL_BITS,TYPE_MISMATCH,SYMLINK_DETECTED,HARDLINK_DETECTED,LOCK_BUSY,FORK_DETECTED,FD_INVALID,HANDLE_FAILED,HANDLE_CLOSED,DOC_INVALID,LIAISON_MISMATCH,HEAD_MISMATCH,DUPLICATE_DIVERGENT,LIMIT_EXCEEDED,CORRUPT_JOURNAL,CORRUPT_SNAPSHOT,TRUNCATED,EXTRA_BYTES,INCOMPLETE_TAIL,TMP_RESIDUEL,DISCORDANT,OUT_OF_BOUNDS,EMPTY,WRITE_FAILED,FSYNC_FAILED,IO_ERROR. Classe StoreError(ValueError) code fixe STORE_INVALID, reason enum vocabulaire ferme, element=store, step=validate_store, message fixe Magasin invalide., repr fixe StoreError(STORE_INVALID), jamais donnees recues. OS cooperatif seulement, meme compte adverse hors garantie; ni fsync passe, ni restauration ancienne paire coherente, ni perte alimentation prouves; profil TEST et handle ne donnent ni origine/autorisation/pret PA; backend jamais fournisseur autorite. Inattendues propagees apres nettoyage des seuls FD propres acquis dans l operation.
### 7. Sequence et controles
EX|NB acquis open/init tenu; append: reverifier PID/FD/inode/device/UID/GID/modes/nlink fichiers==1 dir type dir avant+apres, valider doc, liaison, idempotence, tete; journal+fsync, tmp+fsync, rename, fsync parent, acquit. Partiel/EINTR verifie, aucun recu avant retours. Reread ne prouve jamais fsync passe. Fork: toute operation refusee FORK_DETECTED; close enfant ferme seules copies sans LOCK_UN, aucune promesse meme processus adverse. Fichiers reguliers nlink1, repertoire type dir. Pas de reparation/troncature/reset. Autorite ulterieure non realisee.
### 8. Recettes TEST
tests/.pa02-store-tests racine, synthetique, processus propres, FD/nettoyage bornes. Nominal, limites reelles, doublon/divergence, corruption/cadrage, substitution/liens, permissions, verrou 2 processus, panne chaque etape, crash/relecture. Pas hote/TPM/PG/PZT/secret/service. TEST non defaut/prod. /home/devops/python/current/bin/python3 exact une commande par mandat. Primitive sans proprietaire externe; autorisation ulterieure separee.


## Preuve locale backend et API réelle

API réelle actuelle : StoreProfile, create_store_and_open, open_store, append_document, read_last, read_seq, inspect_store, close_store. L ancien append de la signature se réalise par append_document ; inspect et close se réalisent par inspect_store et close_store, sans alias non réalisé. read_seq hors bornes répond OUT_OF_BOUNDS, y compris magasin vide ; close_store est idempotent. Validé Python IO seul par 30 tests en 0.496 s et compilations syntaxiques, pas Cython natif, admission, anti-rollback, power-loss ou PZT. A, 17 clés et 7 liaisons fixes préservés.
