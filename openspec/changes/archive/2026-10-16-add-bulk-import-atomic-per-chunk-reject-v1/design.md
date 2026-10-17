# Design — add-bulk-import-atomic-per-chunk-reject-v1

## Périmètre
B01/B02/B03/B05/B06/B07/B13/B14 de bulk-operations, B04 object-storage, B08/B09 jobs, B10 interactions et B11 events définissent le comportement. Le premier chemin couvre seulement IMPORT ATOMIC_PER_CHUNK et REJECT. Les autres modes et stratégies restent hors capacité de cette façade, sans repli. Les signatures Python et la composition serveur ci-dessous sont des choix d’implémentation, sans champ de payload ou schéma logique ajouté.

## Participation propriétaire
Les déclarations propriétaire tuple4 et la présence de validate/execute/canonical_bytes ne prouvent aucune participation transactionnelle. Introduire dans le module serveur une déclaration interne distincte, figée, construite uniquement à partir de véritables ports composés côté serveur, de leurs références/versions propriétaire et mapping déjà déclarées, et de l’alias PostgreSQL du dépôt runtime.
La fonction de composition reçoit les ports de confiance exacts ; elle capture les méthodes de leur adaptateur propriétaire, sans accepter de callbacks indépendants d’un payload. Elle lie leur identité au snapshot et refuse références/versions divergentes ou garanties absentes. Une déclaration ne crée pas de provider implicite.
À l’exécution, vérifier l’alias commun, le vendor PostgreSQL, l’identité de l’unité active du dépôt réel et le même thread. La mutation reste synchrone dans cette frontière ; aucun await ne traverse la transaction propriétaire. Une méthode non compatible est une capacité indisponible, sans adaptation implicite vers une autre source.
La déclaration serveur explicite et ces gardes restent distinctes des preuves : les tests PG doivent montrer des écritures propriétaires réelles, idempotence, progression, checkpoint et outbox requise visibles ensemble au commit et absentes ensemble après rollback. in_atomic_block seul ne prouve pas la déclaration du provider.

## Validation et état
Qualifier le flux privé immuable, son intégrité SHA-256 et sa fermeture avant validation propriétaire. Réutiliser le lecteur qualifié et le parseur existants, sans copie massive du pipeline VALIDATE_ONLY. Une validation complète bornée sous ATOMIC_PER_CHUNK doit précéder READY puis tout APPLY ; elle revalide autorité EXECUTE, gouvernance et références déclarées aux frontières requises.
Ne pas appeler la terminaison VALIDATE_ONLY COMPLETED comme préparation d’une opération mutatrice. La matrice existante autorise VALIDATING→READY pour ATOMIC_PER_CHUNK avec invalid_rows nul ; RUNNING→COMPLETED exige l’absence de rejets. Aucun correctif du dépôt n’est nécessaire pour ces arcs existants. Un rejet de validation fait échouer le mode avant mutation conformément à B06/B07, sans inventer de priorité entre échecs.
Les commandes validées et leur reprise restent liées à la version d’entrée, au mapping et à l’identité initiale ; la complétude n’est pas déduite d’un compteur isolé.

## Engagement par chunk
Utiliser la primitive protected_unit du dépôt exact avec bail, révisions, échéances et annulation actuels, puis les commandes propriétaires et les dépôts existants dans la même transaction et le même thread. Les octets canoniques proviennent du sérialiseur public versionné du propriétaire ; la clé d’idempotence et son fingerprint suivent B10.
Mutation, résultat d’idempotence final, progression, checkpoint et événements/outbox requis s’engagent ensemble. Une exception technique annule cette transaction et ses effets ; aucun IN_PROGRESS ne reste engagé. Le rejet propriétaire ou conflit REJECT annule tout le chunk courant, sans checkpoint ni outbox partiels ; les chunks déjà engagés restent conservés. Aucun retry métier ou rebase CAS automatique.
REPLAYED ne crée pas de seconde mutation ou événement et ne double pas la progression. Reprise, index d’unité et checkpoint restent cohérents. Le bail, l’annulation et l’échéance interdisent de nouvelles unités sans prétendre annuler les effets déjà engagés. Aucune publication externe n’est effectuée dans ce sous-lot.

## Fichiers et limites
Les trois cibles envisagées sont bulk_server_apply.py, son test unitaire et son intégration PostgreSQL isolée. Une adaptation strictement nécessaire d’un helper existant nécessite une proposition de fichier/fonctions, sa réservation et une validation CGPT distincte avant écriture ; préserver intégralement le comportement VALIDATE_ONLY et ses tests.
Ne modifier ni Events/Kernel, ni les profils préparatoires, ni les sources des migrations, ni les services, ni les dépendances. La composition de test ne prouve pas un provider de production. Aucun secret, charge brute ou valeur hostile ne doit entrer dans les diagnostics ou rapports.

## Preuves attendues
Import inerte et types hostiles sans I/O avant gardes ; refus d’autorité/gouvernance et garanties insuffisantes ; limites de parsing et validation incomplète sans mutation ; positive PG déclarée même transaction ; rollback à différents points ; CAS et baux concurrents ; chunk antérieur conservé ; rejeu identique/divergent sans double effet ; annulation/expiration ; fermeture des connexions et suppression du seul schéma privé. Syntaxe, tests ordinaires, régressions, validation combinée et résultats OpenSpec exacts précèdent toute coche et archive.
