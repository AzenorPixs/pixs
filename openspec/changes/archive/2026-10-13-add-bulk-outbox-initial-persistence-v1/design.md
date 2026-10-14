# Design add-bulk-outbox-initial-persistence-v1

Choix fermes, preconditions serveur, sans norme nouvelle. Pur Outbox 12 et Envelope 13 inchanges.

## Donnees canoniques

Les 12 noms logiques OutboxPublicationV1 MUST rester exactement : event_id (FK enveloppe immuable, unique), state, attempt_count, lease_owner, lease_expires_at, next_attempt_at, published_at, failure_code, sequence_index, policy_reference, policy_version, revision. Aucun champ logique nouveau, aucun defaut normatif, aucun profil 11 public ni wire format nouveau.

La table publication MUST porter 13 colonnes physiques : les 12 mappees + scope_prive derive de order_scope_reference verrouille de l'enveloppe. La table compteur MUST porter 2 colonnes privees (scope_prive PK, next_index). Les 2 tables MUST etre creees par 0011 apres 0010 ; les 13 tables preexistantes MUST rester intactes. FK event_id MUST referencer reellement BulkEventEnvelopeRecord avec protect/immuable ; aucune modification Envelope.

## Allocation et concurrence

Le scope exact MUST deriver de l'enveloppe verrouillee lue dans la meme transaction proprietaire. Le compteur MUST etre verrouille par rowlock SQL exact sur scope, sans hash, sans advisory, sans collision. UNIQUE(scope_prive, sequence_index) MUST etre contrainte SQL. La sequence MUST etre allouee exclusivement par le runtime owner dans la meme transaction SQL que l'insert publication ; aucun caller index stocke comme allocation ; aucun index caller normalise ou ignore ; aucune sentinelle persistee.

Racine compteur absent : savepoint unique pour le cas 23505 PK scope correle seulement, puis rowlock ; tout autre IntegrityError MUST se propager avec rollback owner. Toute erreur DB MUST se propager avec rollback owner, sans faux succes.

## Types, capacites, contextes

Tous compteurs normatifs MUST rester TEXT decimaux prives, types int stricts (type(x) is int, bool exclu), capacite stdlib reelle verifiee avant write ; aucun cap int64 arbitraire ni re global. Revision positive fournie MUST etre conservee ; initial PENDING/attempt0 canoniques MUST etre explicites et valides. Autres nullables admis sans norme None imposee. Datetimes MUST etre timezone.utc exact avant IO ; _TrustedUtcDateTimeField reste decodage ORM de confiance uniquement.

Contextes, catalogues, UTC et types MUST etre valides avant IO/callback, puis owner atomique explicite alias/join savepoint False, readonly sans lazy queries. Model save initial MUST passer uniquement par contexte allocation prive du Repo lie (owner/event/scope/seq/alias/atomic) ; aucun trust bool caller ; aucun nouveau champ normatif ; acces ORM direct, pas d'API publique.

Seed : validation source 11 champs hors sequence avant IO d'apres contraintes pures existantes, puis capture reelle 12 apres allocation. Scope/counter restent techniques hors contrat public.

## API initiale et getter

API initiale Source MUST exiger ELEVEN valeurs source obligatoires (tous champs sauf sequence, incluant nullable/state/attempt/revision/policy) + catalogue failure explicite tuple/frozenset valide et copie ; aucun defaut Python. Record factory from_values MUST mapper 12 exact avec capture pure existante (validate/capture bulk_outbox_publication_values) et scope prive contexte hors 12. Policy refs opaques MUST rester metadonnees serveur trusted validees structurellement (texte runtime, SemVer complete), sans composition prod attestee ni catalogue par defaut. PENDING metadata initiale MUST NOT etre preuve auth/gouvernance/emit.

Getter MUST etre capture pure figee 12 : catalogue avant ORM meme absent, coherence scope fail-closed, pas de lazy loads, pas d'ack ni available-publish. Revision persistee sans operation CAS dans ce scope.

## Exclusions fermes

Aucun publisher/daemon/emit/ack, transition CAS/bail-claim/retry-reset, clock, authority/gouvernance concrete, provider/API/transport, Git/frontend/dependance, fallback semantique, Enum/type/logical-default/nouveau format ou const policy normative. Kernel/purs/runtime existants et Envelope immuables.

## Frontieres de preuve

Une enveloppe inseree dans l owner courant doit etre utilisable sans exiger un commit prealable. La publication et son index restent invisibles a une connexion independante avant commit ; un retour de donnees dans l owner ne vaut pas ack ni disponibilite publisher. Les sources de policy/catalogue serveur sont des preconditions explicites, pas une composition de production resolue. Le catalogue est requis aussi au get d un event inexistant.

Les parametres nullables obligatoires acceptent les valeurs deja admises par le pur ; aucune nouvelle regle les forcant a None n est ajoutee. La revision positive fournie, y compris une valeur differente de 1, reste intacte. Les initialiseurs techniques du compteur ne deviennent pas des valeurs par defaut de modele ni de politique. Les limites physiques DB inattendues se propagent et annulent l owner ; aucune garantie de stockage arbitraire n est inventee.

Le full_clean revalide toutes donnees et le scope prive meme si exclude est demande, sans requete de validation de FK implicite. Le FK est confirme par l enveloppe verrouillee du repository et la contrainte SQL. Les getters utilisent les attributs stockes sans lazy load ni lecture de payload inutile ; mismatch de scope prive et scope Envelope refuse. Les codes statiques demeurent uniquement ceux du catalogue fourni, sans grammaire ni valeur globale ajoutee.
