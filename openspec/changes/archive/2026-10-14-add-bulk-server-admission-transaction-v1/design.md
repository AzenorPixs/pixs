# Design — Admission serveur Bulk B01

## Périmètre

Admission interne IMPORT/EXPORT asynchrone, formats CSV et NDJSON seuls, tenant résolu par
l'autorité serveur. Aucune route HTTP, aucun seuil synchrone, aucun worker, aucune migration
de production, aucune modification des modèles existants ni des profils Kernel et Record.

## Interface interne

`admit_bulk_operation(*, trusted_ports, server_context, using, execution_values,
policy, owner_reference, job_id, job_causation_id, schedule_values,
identity_expires_at, failure_codes, now_utc)` retourne `operation_id`.

Le service construit lui-même les treize valeurs Job canoniques et les repositories internes
sur le même alias `using` explicite. Aucune fabrique arbitraire ni callback du payload ne
participe à cette construction. `trusted_ports` est une instance exacte composée côté serveur ;
`server_context` reste opaque et non sérialisé. `owner_reference`, `job_id` et
`job_causation_id` sont des str opaques explicites serveur ; les déclarations de propriétaire
sont celles déjà capturées par la composition. `schedule_values` fournit les sept clés
JobScheduleV1 exactes. `identity_expires_at` est un datetime UTC exact fourni par le serveur,
distinct de la deadline opérationnelle. `failure_codes` est le frozenset exact du catalogue
serveur ; `now_utc` est un datetime UTC exact. Le type et la version du premier Job sont
les constantes canoniques liées à la variante et à la phase, sans choix arbitraire. La
politique explicite est validée puis liée à la politique effectivement résolue. Les imports
ORM et tout accès SQL sont différés après les gardes et contrôles effectifs des ports.

Les arguments sont fournis par le code serveur appelant. Les valeurs d'exécution portent
les trente-six clés exactes déjà validées, la politique porte les vingt-quatre clés
PolicyV1 explicites sans défaut, l'instant est un datetime aware UTC exact.

## Ordre des contrôles

Contrôle des types exacts des clés puis des valeurs avant tout comportement, parsing ou
entrée/sortie, sans écho de valeur. Validation de l'enveloppe d'exécution par le
validateur existant, puis résolution du mapping par identité stricte avec la déclaration
serveur immuable. Consultation du port d'autorité pour l'action ADMIT, puis résolution
de la gouvernance avant tout accès SQL. Un refus d'autorité ou de gouvernance arrête
l'admission sans contexte exploitable ni repli. Les secrets et charges interdites
restent hors fichiers, diagnostics, événements et journaux.

La gouvernance utilise exclusivement la résolution effective du GovernancePort composé selon GovernanceResolutionV1. Les six clés explicites sont contrôlées par types exacts avant comportement puis capturées immuables. RESOLVED exige le contexte lié à l'autorité courante, la politique, le profil existant et les obligations effectivement résolues ; DENY/UNAVAILABLE imposent quatre None sans contexte exploitable ni repli. La validation structurelle seule et les références opaques ne constituent jamais cette preuve.

## Identité et empreinte B10

L'identité d'admission suit BulkAdmissionIdentityV1 par tenant résolu, acteur résolu,
type et clé d'idempotence, avec unicité atomique de la clé complète. L'empreinte suit
FingerprintV1 sur le snapshot initial immuable, hors identifiants de suivi, état,
progression et sorties. Le contenu initial et son empreinte restent immuables après
admission. Le rejeu identique rend l'opération initiale après le contrôle actuel, le
rejeu divergent produit un conflit sans mutation propriétaire.

## Transaction unique

Une transaction Django extérieure durable, sur le même alias et engagée avant le retour,
assemble l'identité d'admission, la demande d'exécution,
l'extension d'exécution, le premier Job et la liaison, puis l'ordonnancement initial
lorsque la phase l'exige. La création de l'opération et de son extension réutilise la
primitive existante de création conjointe. La liaison réutilise la primitive de liaison
d'un Job construit par le service, avec phase STAGE pour IMPORT puis VALIDATE,
ou EXPORT seul. Le payload du Job porte exactement la référence et la version de la
demande d'exécution. Les métadonnées du Job conservent les références originales, les
corrélations et le périmètre serveur sans transférer de credentials ni d'exception.
L'échéance opérationnelle borne la reprise, la rétention d'identité couvre la fenêtre
de rejeu après état terminal avec les holds. La concurrence repose sur l'unicité SQL
de la clé d'admission, de la clé primaire d'opération et des couples opération/phase
et opération/révision. Tout échec annule la transaction sans effet partiel. Une transaction ambiante ou un
autocommit désactivé est refusé explicitement ; aucun retour n'annonce un COMMIT encore
dépendant du caller. L'insertion de l'identité est isolée par savepoint et précède toute
ligne nouvelle d'opération ou de Job ; après conflit d'unicité, le rejeu compare uniquement
l'identité initiale validée, sans laisser de ligne orpheline.

## Concurrence et rollback

Aucune modification des modèles existants. Les conflits d'unicité deviennent des refus
de contrainte sans second effet. L'admission neuve et le rejeu restent distingués par
la clé d'admission et l'empreinte, après réévaluation de l'autorité et de la
gouvernance au moment du contrôle.

## Preuves

Tests unitaires inertes en sous-processus frais sous gardes, sans base ni réseau ni
secret. Callable PostgreSQL dédié avec schéma privé, migrations cohérentes aux modèles
actuels, vérification du rollback, de l'isolation, du rejeu identique et divergent,
puis nettoyage et fermeture des connexions prouvés. Aucun test de baux ou de CAS sans
rapport avec l'admission.

## Liens et valeurs serveur explicites

La référence de demande d'exécution utilise l'operation_id de l'extension persistante existante, sans identité supplémentaire. Le payload JobPayloadV1 porte exactement execution_reference et execution_version. JobMetadataBindingV1 conserve les références originales et le périmètre serveur ; la causalité non vide du Job est fournie explicitement par le serveur, sans fallback dérivé d'un None.

Les sept valeurs JobScheduleV1 et l'échéance de rétention d'identité sont fournies explicitement ; cette rétention reste distincte de l'échéance opérationnelle et de l'horloge courante. Le rejeu ne modifie jamais le snapshot initial.

Le contrat de résolution de gouvernance est fixé par le canon. Aucun audit supplémentaire, worker, traitement de bail ou mode d'import/export n'est ajouté à cette admission.
