# Intégration et plateformes — PA03

Documentation détaillée des flux, des trois objets versionnés, du catalogue d'opérations et des profils Linux et Windows. Les documents proposal, design, contracts et tasks y renvoient. Le delta normatif reste [specs/pixs-agent/spec.md](./specs/pixs-agent/spec.md). Nouveaux schémas définis et proposés dans ce change, pas validés par le développeur ; orientations systemd, logind, PAM borné, module natif et budgets restent acquises. Aucun code, installation ou qualification par ce texte. Références officielles : HandlerEx https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nc-winsvc-lphandler_function_ex pour événements session avec logon reçu seulement si service chargé auparavant ; WM_WTSSESSION_CHANGE https://learn.microsoft.com/en-us/windows/win32/termserv/wm-wtssession-change pour logon, logoff, verrouillage et connexions ; WTSQueryUserToken https://learn.microsoft.com/en-us/windows/win32/api/wtsapi32/nf-wtsapi32-wtsqueryusertoken pour exigence LocalSystem et SE_TCB_NAME sans les adopter.

## Flux aller

PFO expose paramétrage, états et résultats sans action OS directe. PBO valide pa_session_config 1.0.0 puis émet pa_operation_envelope 1.0.0 avec droits, périmètre, idempotence et audit. Le module PBO pixs.agent prépare le plan PA hors PZT. PZT transporte exclusivement instruction et mandat vers PA. PA vérifie profil installé, droits OS, préconditions, budgets, contexte et droits puis exécute l'adaptateur local : systemd et logind sur Linux, SCM et WTS sur Windows. L'initialisation locale et la réception PAM n'exigent pas un mandat PBO générique ; les quatre opérations distantes exigent des droits opposables courants adaptés. Aucune donnée PAM, XDG, environnement, PID libre, UID seul ou JSON ne vaut autorité. Aucun canal PBO et PA hors PZT. Aucun port réseau PAM local.

## Répartition des rôles

Le déploiement, l'installation, la mise à jour, l'activation, la désactivation, le retrait, le rollback et la configuration de l'intégration PAM de l'hôte sont exécutés par le rôle système PA déclaré par le profil et catalogue autorisé, avec system-daemon pour la cible Linux existante, sous droits et autorité actuels, jamais par callback PAM ou rôle utilisateur et session. Les données locales de session et événements restent dans le rôle utilisateur sans créer un droit de mutation hôte, même si UID0 ou parent PAM privilégié. Le callback ne reçoit pas les commandes PBO ni ne devient serveur réseau. Les contrôles du profil, rôle, opération et mode réels restent exigés ; aucun nouveau service et exécutable, aucun compte ou privilège Windows implicite. Windows conserve le rôle système logique du profil futur, sans sélection de LocalSystem. Cette répartition précise des frontières existantes et n'accorde aucun droit nouveau.

## Flux retour

PA produit exclusivement pa_operation_result 1.0.0 et lie mandat, contexte, effet et résultat observé avec corrélation et idempotence. PZT transporte exclusivement le résultat vers PBO. PBO vérifie, persiste l'état durable chez le vrai propriétaire, audite sans secret et expose l'état à PFO avec observed_artifact_ref, observed_config_ref et activation_state ; PFO ne transmet jamais un résultat comme vérité. La réception PZT reste distincte de l'effet OS. Effet UNKNOWN impose IN_DOUBT avec UNKNOWN ; timeout avant effet prouvé donne NONE avec REFUSED ou FAILED selon cause réelle. Sessions concurrentes isolées en processus, droits, ressources et arrêts. Le rejeu ne donne jamais une permission nouvelle ; autorités et périmètre courants sont revalidés pour accéder aux résultats et agir.

## Objet pa_session_config 1.0.0

Configuration seule, sans résultat ni mandat. config_profile_revision désigne la révision du profil de configuration attribuée par PBO et liée à config_ref, distincte de expected_revision et observed_revision de l'état OS ; le profil d'exécution protégé résolu garde ses règles d'autorité propres. Champs inconnus refusés. Nombres déguisés depuis booléen refusés. Révisions booléennes refusées comme les autres nombres.

| Champ | Type | Obligatoire | Contraintes | Origine d'autorité |
|---|---|---|---|---|
| schema_version | chaîne | oui | vaut pa_session_config 1.0.0 | politique versionnée PBO |
| profile_id | chaîne | oui | identifiant de profil protégé non vide | politique et profil protégé PBO |
| config_profile_revision | entier | oui | entier positif attribué par PBO et lié à config_ref | registre PBO versionné |
| artifact_ref | chaîne | oui | référence d'artefact versionnée non vide | catalogue PA01 corrélé à la release |
| config_ref | chaîne | oui | référence de configuration versionnée non vide | registre PBO versionné |
| system_start_delay_s | nombre | oui | fini et non négatif ; booléen, chaîne, null, non fini, négatif et champ inconnu refusés ; absence refusée | profil protégé PBO |
| session_start_delay_s | nombre | oui | fini et non négatif ; booléen, chaîne, null, non fini, négatif et champ inconnu refusés ; absence refusée | profil protégé PBO |
| system_preconditions_wait_s | nombre | oui | fini et non négatif ; booléen, chaîne, null, non fini, négatif et champ inconnu refusés ; absence refusée | profil protégé PBO |
| session_preconditions_wait_s | nombre | oui | fini et non négatif ; booléen, chaîne, null, non fini, négatif et champ inconnu refusés ; absence refusée | profil protégé PBO |
| system_shutdown_budget_s | nombre | oui | fini et non négatif ; booléen, chaîne, null, non fini, négatif et champ inconnu refusés ; absence refusée | profil protégé PBO |
| session_shutdown_budget_s | nombre | oui | fini et non négatif ; booléen, chaîne, null, non fini, négatif et champ inconnu refusés ; absence refusée | profil protégé PBO |

Exemple JSON complet valide du seul profil de recette Debian13 x86_64, avec références fictives non résolubles ni probantes, sans valeur probante :

```json
{
  "schema_version": "pa_session_config 1.0.0",
  "profile_id": "EXEMPLE-FICTIF-recette-debian13-pam",
  "config_profile_revision": 1,
  "artifact_ref": "EXEMPLE-FICTIF-pa-pzt-release-recette",
  "config_ref": "EXEMPLE-FICTIF-pa-session-recette-r1",
  "system_start_delay_s": 0,
  "session_start_delay_s": 0,
  "system_preconditions_wait_s": 30,
  "session_preconditions_wait_s": 10,
  "system_shutdown_budget_s": 30,
  "session_shutdown_budget_s": 10
}
```

IDs, config_ref et artifact_ref ne valent pas autorité ; résolution contre registre réel protégé obligatoire. Aucun champ de résultat reçu comme configuration. Délais de recette seulement pour ce profil, sans défaut production ni copie Windows. Couches : schéma, puis configuration statique, puis configuration runtime, puis références de secrets ; les défauts du composant ne s'appliquent qu'aux champs non budgétaires. Secrets par référence hors artefacts. Chemins PAM, ABI, permissions et cibles de service résolus par profil protégé, pas par champs libres UI.

## Objet pa_operation_envelope 1.0.0

Enveloppe d'entrée avec sélecteur operation distinct de operation_id de corrélation, et operation_version 1.0.0 partout. Champs inconnus refusés. Aucun secret, descripteur ou token sérialisé. intent seulement pour pa_plan et pa_apply ; absent pour pa_observe et pa_reconcile ; une observation ne choisit aucune intention de mutation. plan_ref absent en entrée de pa_plan, requis en entrée de pa_apply, absent pour pa_observe et pa_reconcile ; pas de plan arbitraire transformé en autorisation. prior_operation_id obligatoire pour pa_reconcile, absent sinon. expected_revision et expected_preimage_ref obligatoires pour pa_plan et pa_apply, absents pour pa_observe, absents pour pa_reconcile qui cible prior_operation_id et constate l'état courant. config_ref selon besoin réel : absent pour pa_observe, requis pour pa_plan et pa_apply, absent pour pa_reconcile. expected_revision 0 admis pour état initial ABSENT réellement observé côté OS ; la révision de configuration config_profile_revision reste positive. authority_ref exigé pour les quatre opérations avec droits adaptés à observer, planifier, appliquer ou réconcilier.

| Champ | Type | Présence | Contraintes | Origine d'autorité |
|---|---|---|---|---|
| schema_version | chaîne | toujours | vaut pa_operation_envelope 1.0.0 | politique versionnée PBO |
| operation | chaîne | toujours | vaut pa_observe, pa_plan, pa_apply ou pa_reconcile | catalogue du change |
| operation_version | chaîne | toujours | vaut 1.0.0 | catalogue du change |
| operation_id | chaîne | toujours | corrélation non vide, distinct du sélecteur | PBO avec idempotence |
| target | chaîne | toujours | cible et périmètre non vides | PBO et profil protégé |
| intent | chaîne | pa_plan et pa_apply seulement ; absent pour pa_observe et pa_reconcile | vaut INSTALL, UPGRADE, CONFIGURE, ENABLE, DISABLE, REMOVE ou ROLLBACK | PBO avec autorité valide |
| config_ref | chaîne | absent pa_observe ; requis pa_plan et pa_apply ; absent pa_reconcile | référence pa_session_config non vide ; pa_plan reçoit config_ref qui référence artifact_ref, sans artifact_ref supplémentaire | registre PBO versionné |
| plan_ref | chaîne | absent pa_plan en entrée ; requis pa_apply ; absent pa_observe et pa_reconcile | plan persisté non vide | PA avec état durable |
| prior_operation_id | chaîne | obligatoire pa_reconcile ; absent sinon | référence d'opération antérieure non vide | PA avec corrélation |
| idempotency_key | chaîne | toujours | clé non vide | PBO avec idempotence |
| expected_revision | entier | pa_plan et pa_apply seulement ; absent pa_observe et pa_reconcile | 0 admis pour ABSENT observé ; sinon positif ou nul observé ; booléen refusé | état durable du vrai propriétaire |
| expected_preimage_ref | chaîne | pa_plan et pa_apply seulement ; absent pa_observe et pa_reconcile | préimage attendue ou sa référence résolue non vide | état durable du vrai propriétaire |
| authority_ref | chaîne | toujours | contexte et droits adaptés à observer, planifier, appliquer ou réconcilier | PBO avec droits opposables |

Exemple JSON complet valide d'enveloppe pa_apply, avec toutes références explicitement fictives :

```json
{
  "schema_version": "pa_operation_envelope 1.0.0",
  "operation": "pa_apply",
  "operation_version": "1.0.0",
  "operation_id": "EXEMPLE-FICTIF-op-0001",
  "target": "EXEMPLE-FICTIF-debian13-vm-01",
  "intent": "CONFIGURE",
  "config_ref": "EXEMPLE-FICTIF-pa-session-recette-r1",
  "plan_ref": "EXEMPLE-FICTIF-plan-0001",
  "idempotency_key": "EXEMPLE-FICTIF-idem-0001",
  "expected_revision": 1,
  "expected_preimage_ref": "EXEMPLE-FICTIF-preimage-0001",
  "authority_ref": "EXEMPLE-FICTIF-autorite-pbo-appliquer-0001"
}
```

## Objet pa_operation_result 1.0.0

Résultat produit exclusivement par PA, jamais transmis par PFO comme vérité. observed_revision autorise null quand inconnue avec cause explicite ; aucun entier ni preuve fabriqué pour satisfaire le schéma. evidence_refs liste peut être vide si preuve réellement indisponible, avec diagnostic motivé ; une revendication d'effet APPLIED ou NONE prouvé exige ses preuves. plan_ref réel pour PLANNED et lien au plan validé pour apply ; absent ou null selon cas explicitement précisés ; jamais inventé sur refus préalable. Champs inconnus refusés. Diagnostics sans secret. Activation OS distincte de disponibilité et autorité métier. Aucune valeur inconnue fabriquée. La preuve d'un NONE de mutation est distincte d'une donnée observée inconnue ; une lecture sans mutation ne devient pas IN_DOUBT uniquement parce qu'une observation manque ; aucun nouvel effet produit par ce seul manque.

| Champ | Type | Obligatoire | Contraintes | Origine d'autorité |
|---|---|---|---|---|
| schema_version | chaîne | oui | vaut pa_operation_result 1.0.0 | PA avec catalogue |
| operation_id | chaîne | oui | corrélation exacte avec enveloppe, distincte de prior_operation_id | PA avec corrélation |
| prior_operation_id | chaîne | pa_reconcile seulement ; absent ou null sinon | référence antérieure non vide quand présente | PA avec corrélation |
| operation_status | chaîne | oui | vaut OBSERVED, PLANNED, APPLIED, REFUSED, FAILED, IN_DOUBT ou RECONCILED | PA avec état durable |
| effect_state | chaîne | oui | vaut NONE, APPLIED, PARTIAL ou UNKNOWN ; désigne la mutation demandée, ou la mutation antérieure désignée lors de pa_reconcile | PA avec effet OS observé |
| observed_revision | entier ou null | oui | entier positif ou 0 observé, ou null quand inconnue avec cause explicite ; booléen refusé ; aucune valeur inventée | état durable et réel PA |
| observed_artifact_ref | chaîne ou null | oui | artefact observé ou null quand indisponible avec cause | état réel PA |
| observed_config_ref | chaîne ou null | oui | configuration observée ou null quand indisponible avec cause | état réel PA |
| activation_state | chaîne | oui | vaut ABSENT, STAGED, ACTIVE, DISABLED ou UNKNOWN | état réel PA |
| plan_ref | chaîne ou null | selon cas | réel pour PLANNED et lien au plan validé pour apply ; null pour OBSERVED, REFUSED, FAILED sans plan, IN_DOUBT sans plan ; jamais inventé sur refus préalable | PA avec état durable |
| evidence_refs | liste de chaînes | oui | peut être vide si preuve réellement indisponible avec diagnostic motivé ; APPLIED ou NONE prouvé exige preuves | PA avec preuves |
| diagnostic | chaîne | oui | diagnostic sans secret, avec cause explicite si null ou vide | PA sans secret |

Couples admis : OBSERVED avec NONE ; PLANNED avec NONE ; APPLIED avec APPLIED ; REFUSED avec NONE ; FAILED avec NONE ; FAILED avec PARTIAL ; IN_DOUBT avec UNKNOWN ; RECONCILED avec APPLIED ; RECONCILED avec PARTIAL pour constat historique sans prétendre application complète ; RECONCILED avec NONE. pa_observe 1.0.0 et pa_plan 1.0.0 n'appliquent rien. pa_reconcile 1.0.0 constate un effet antérieur sans créer de nouvelle mutation OS. Si preuves insuffisantes, l'ancienne opération reste IN_DOUBT sans faux RECONCILED.

Exemple JSON complet valide de résultat, avec références fictives non résolubles ni probantes :

```json
{
  "schema_version": "pa_operation_result 1.0.0",
  "operation_id": "EXEMPLE-FICTIF-op-0001",
  "operation_status": "APPLIED",
  "effect_state": "APPLIED",
  "observed_revision": 1,
  "observed_artifact_ref": "EXEMPLE-FICTIF-pa-pzt-release-recette",
  "observed_config_ref": "EXEMPLE-FICTIF-pa-session-recette-r1",
  "activation_state": "ACTIVE",
  "plan_ref": "EXEMPLE-FICTIF-plan-0001",
  "evidence_refs": ["EXEMPLE-FICTIF-preuve-pa-0001"],
  "diagnostic": "EXEMPLE-FICTIF-application-verifiee-sans-secret"
}
```

## Catalogue pa_observe 1.0.0, pa_plan 1.0.0, pa_apply 1.0.0 et pa_reconcile 1.0.0

pa_observe 1.0.0 en lecture : entrées target, authority_ref pour observer, operation_id et idempotency_key ; sans intent, config_ref, plan_ref, prior_operation_id, expected_revision et expected_preimage_ref ; sorties état et révision courante avec OBSERVED et NONE et observation minimale ; refus périmètre inconnu, droit observer manquant et révision illisible ; aucune intention de mutation ; jamais d'affirmation d'un nouvel effet APPLIED. pa_plan 1.0.0 en lecture persistante sans mutation OS : entrées target, intent, config_ref qui référence artifact_ref, expected_revision, expected_preimage_ref, authority_ref pour planifier, operation_id et idempotency_key ; sans plan_ref en entrée et sans prior_operation_id ; sorties plan_ref et préimage avec PLANNED et NONE et plan_ref réel en résultat ; refus incompatibilité, révision dépassée et preuve manquante ; n'accorde aucun droit d'appliquer. pa_apply 1.0.0 en mutation : entrées target, intent, config_ref, plan_ref obligatoire d'un plan validé, expected_revision, expected_preimage_ref, authority_ref pour appliquer, operation_id et idempotency_key ; sorties APPLIED avec APPLIED, REFUSED avec NONE, FAILED avec NONE ou PARTIAL, IN_DOUBT avec UNKNOWN ; refus mandat invalide, préconditions non satisfaites, effet inconnu et retour arrière impossible sans nouveau plan. pa_reconcile 1.0.0 en lecture et rapprochement : entrées target, prior_operation_id obligatoire, authority_ref pour réconcilier, operation_id et idempotency_key ; sans intent, config_ref, plan_ref, expected_revision et expected_preimage_ref imposés ; sorties RECONCILED avec APPLIED, PARTIAL ou NONE constaté sur opération antérieure désignée, ou maintien IN_DOUBT avec UNKNOWN ; refus preuve insuffisante ; toute correction ou rollback exige un nouveau plan et une application autorisée.

## Profil Linux

Debian13 x86_64 physique et VM avec profil PAM sélectionné. systemd pour modes système, événements bornés et démons distincts. logind comme source native ; instance isolée par session ; contexte, génération et droits réels vérifiés. Premier module PAM conditionnel au profil Linux, pas imposé à Docker. Module PAM natif en bibliothèque partagée avec C minimal et API libpam, sans Python dans PAM ni quatrième exécutable PA ; vérification logind avant enfant borné même contexte, abandon vers UID, GID et groupes du titulaire vérifié avec provenance prouvée, sans initgroups arbitraire, nettoyage environnement et descripteurs avant exec du binaire existant qui revalide avant effet ; aucun handle et capacité privée D13 et D14 vers PAM ou enfant ; fermeture des handles de preuve et nettoyage propres avant exec, puis vérifications propres du binaire. Packaging PA et PZT existant selon deb-package et docker-image ; compatibilité, authorization et audit comme références sans réécriture. Verrouillage et suspension distincts de fermeture. Ordre ouverture et fermeture, contexte PAM root, perte de contexte pendant close, double événement, annulation, crash et isolation multi-session à qualifier en environnement réel. Journal durable chez le vrai propriétaire avec comparaison expected_preimage_ref et expected_revision.

## Profil Windows

Contrat cible à réaliser et qualifier séparément avec environnement réel propre. Service PA existant avec notifications SCM SERVICE_CONTROL_SESSIONCHANGE et WTS ; événements logon, logoff, verrouillage, déverrouillage et déconnexion distingués ; verrouillage et déconnexion RDP distincts de logoff ; réconciliation des sessions déjà ouvertes au démarrage car logon reçu seulement si service chargé auparavant ; contrôles natifs utilisateur, session et token ; tokens natifs protégés et non exposés. Pas de PAM porté. LocalSystem, SE_TCB_NAME, versions OS et CPU, Credential Provider, LSA, service ou exécutable nouveau non adoptés. WTSQueryUserToken comme possibilité privilégiée documentée, pas comme décision d'usage. Aucune qualification héritée du Linux. Rôle PFO, PBO, PZT et PA et retour d'état obligatoires.
