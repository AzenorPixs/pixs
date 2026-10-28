# Contrats — PA03

Statut : décisions acquises listées en [proposal.md](./proposal.md) et interfaces définies et proposées par ce change avec source unique en [session-integration.md](./session-integration.md) et exigences en [specs/pixs-agent/spec.md](./specs/pixs-agent/spec.md) ; propriétaires et profils externes pas encore disponibles : PA01 pour packaging et qualification, PA02 pour autorités, environnements réels Linux et Windows, politique et profil protégé pour chemins et ABI. PREUVES DISPONIBLES : aucune intégration et qualification PA03. Référence canon : `openspec/specs/pixs-agent/spec.md`. Aucun code, test produit, installation ou qualification par ce texte. Les contrôles applicatifs suivent les exceptions SuperAdmin du canon dans leur périmètre exact sans fabriquer de preuve native.

## Responsabilités

- PFO expose paramétrage, états et résultats sans action OS directe, avec observation minimale observed_artifact_ref, observed_config_ref et activation_state.
- PBO valide pa_session_config 1.0.0 puis émet pa_operation_envelope 1.0.0 avec droits, périmètre, idempotence et audit.
- Le module PBO pixs.agent gère, configure et supervise PA hors PZT et reste essentiel même sans exécutant OS disponible.
- PA natif exécute le lifecycle local selon profil installé et droits OS vérifiés ; l'initialisation locale et la réception d'un événement PAM n'exigent pas un mandat PBO générique. Les quatre opérations distantes exigent des droits opposables courants adaptés. Les opérations distantes de gestion exigent une autorité PBO valide.
- Le module PBO pixs.pzt gère le réseau ; l'exécutable PZT indépendant exécute pzt-daemon sans délais PA. PZT transporte exclusivement les échanges PBO et PA et ne devient pas gestionnaire PAM.
- PBO et Django conservent l'autorité applicative. PA02 conserve ses autorités métier ; l'événement PAM seul n'en crée pas.
- Propriétaires externes : PA01 pour build, composition, identités système, permissions minimales, packaging et qualification du module natif ; PA02 pour provisionnement, identités de relation et autorités ; Z12, C08 et A07 pour PKI, confirmation, transport et enveloppes.

## États

- Opération : OBSERVED, PLANNED, APPLIED, REFUSED, FAILED, IN_DOUBT, RECONCILED. Couples admis : OBSERVED avec NONE ; PLANNED avec NONE ; APPLIED avec APPLIED ; REFUSED avec NONE ; FAILED avec NONE ; FAILED avec PARTIAL ; IN_DOUBT avec UNKNOWN ; RECONCILED avec APPLIED ; RECONCILED avec PARTIAL pour constat historique sans prétendre application complète ; RECONCILED avec NONE. APPLIED signifie application entièrement vérifiée ; partiel connu vaut FAILED avec PARTIAL ou RECONCILED avec PARTIAL. Tout effet de mutation UNKNOWN reste IN_DOUBT avec UNKNOWN, jamais RECONCILED.
- Effet OS : NONE, APPLIED, PARTIAL, UNKNOWN. L'effet désigne la mutation demandée, ou la mutation antérieure désignée lors de pa_reconcile 1.0.0 avec prior_operation_id ; pa_observe 1.0.0 et pa_plan 1.0.0 n'appliquent rien. Une lecture ne doit pas affirmer un nouvel effet APPLIED ; pa_reconcile 1.0.0 peut constater historiquement un effet prouvé sans créer de nouvelle mutation OS.
- Lancement : attente de délai volontaire, attente de préconditions, en cours, annulé, refusé pour paramètres absents ou invalides.
- Arrêt : en cours borné, terminé confirmé, incomplet ou inconnu après coupure forcée, jamais succès inventé.
- Session : active réelle, fermée, verrouillée ou suspendue distincte de fermée.
- PZT : cycle indépendant conservé tant que des échanges nécessaires et autorisés restent possibles dans le budget d'arrêt.
- Activation observée PFO : ABSENT, STAGED, ACTIVE, DISABLED, UNKNOWN, distincte de disponibilité et autorité métier.

## Démarrage, arrêt, annulation

- system-daemon et session-daemon : délais indépendants, configurables, non négatifs, préconditions et attentes maximales déclarées ; paramètres obligatoires sans défaut.
- Arrêt pendant délai : annule le lancement différé sans modifier validité des mandats ni transférer PZT à PA.
- system-stop et session-stop : budget maximal, ordre déclaré avec démons et dépendances du périmètre, protection contre doublons ; PZT conservé dans le budget prévu.
- Panne électrique, arrêt forcé, perte de processus : non présentés comme fermeture exécutée.

## Session réelle Linux

- Accepté : logind comme source native sur Debian13 physique et VM avec profil PAM sélectionné ; instance isolée par session ; contexte, génération et droits réels vérifiés avant effet produit, ressource métier et secret ; les handles natifs d'observation nécessaires à vérifier le contexte restent autorisés ; UID seul insuffisant ; fermeture arrête son démon sans affecter les autres ; verrouillage ou suspension ne vaut pas fermeture.
- Accepté : module PAM natif en bibliothèque partagée avec C minimal et API libpam et artefact propre, sans Python dans PAM ni quatrième exécutable PA ; vérification logind du contexte réel avant enfant borné même contexte, abandon des privilèges vers titulaire vérifié, nettoyage environnement et descripteurs avant exec du binaire utilisateur existant qui revalide avant effet. UID, GID, groupes et capabilités admissibles avec provenance prouvée par propriétaire réel ; pas d'initgroups arbitraire donnant des groupes supplémentaires. Aucun handle et capacité privée D13 et D14 vers PAM ou enfant ; fermeture des handles de preuve et nettoyage propres avant exec, puis vérifications propres du binaire. La réception d'événement reste distincte des droits métier PBO et PA02.
- Défini et proposé par ce change : chemins résolus par profil protégé, catalogue pa_observe 1.0.0, pa_plan 1.0.0, pa_apply 1.0.0 et pa_reconcile 1.0.0, objets pa_session_config 1.0.0, pa_operation_envelope 1.0.0 et pa_operation_result 1.0.0 en session-integration.
- En attente de propriétaires : packaging et qualification PA01, environnements réels. PAM_USER, XDG, environnement, PID libre, UID seul et JSON ne valent pas autorité. L'authtok ne doit être ni lu, ni transmis, ni exposé. Aucun secret, descripteur, FD ou token privé sérialisé.

## Modes système

- Accepté : systemd pour modes système sur Debian13 physique et VM, événements bornés et démons distincts, sans installation de service par cette préparation.
- Défini et proposé par ce change : bindings logiques et catalogue d'opérations ; unités exactes issues du profil protégé.

## Contrat cible Windows

- Défini comme cible : service PA existant avec SCM SERVICE_CONTROL_SESSIONCHANGE et WTS comme sources natives ; événements logon, logoff, verrouillage, déverrouillage et déconnexion distingués ; verrouillage et déconnexion RDP distincts de logoff ; réconciliation des sessions déjà ouvertes au démarrage ; contrôles natifs utilisateur, session et token ; tokens natifs protégés et non exposés.
- LocalSystem, SE_TCB_NAME, versions OS et CPU, Credential Provider, LSA, service ou exécutable nouveau ne doivent pas être adoptés implicitement. WTSQueryUserToken reste une possibilité privilégiée documentée, pas une décision d'usage. Windows reste à réaliser et qualifier séparément. Aucun compte, privilège ou valeur Windows nouveau.

## Origine des preuves

- Mandats, contexte, effets et résultats réellement observés liés ; simulation, préparation, exécution et confirmation distinctes.
- Autorisation : jamais déduite d'une mesure de démarrage ou d'une présence de fichier. IDs, config_ref, artifact_ref, digests et versions seuls ne prouvent ni confiance ni autorité ; résolution contre registre réel protégé obligatoire. Aucun champ de résultat reçu comme configuration. La preuve d'un NONE de mutation est distincte d'une donnée observée inconnue ; une lecture sans mutation ne devient pas IN_DOUBT uniquement parce qu'une observation manque ; aucun nouvel effet produit par ce seul manque.
- Durabilité, fencing, réconciliation : propriétaires PA01 et PA02 et stockage réel à désigner avant code.
- Audit : obligations ordinaires sous exceptions SuperAdmin du canon dans leur seul périmètre ; l'exercice d'une exception ne fabrique aucune preuve native.
- Sources et pointeurs et baux proviennent des propriétaires natifs réels, pas de DTO.

## Préconditions des dépendances

- Préconditions des seules actions concernées selon leurs contrats et propriétaires. La simple initialisation locale ne vaut pas ready fonctionnel et n'impose aucun cycle de dépendances. PA n'exige pas PZT pour son initialisation locale.
- PA01, PA02, Z12, C08 et A07 à vérifier par leurs propriétaires au moment où une unité en a besoin.
- Sans preuve requise : blocage du lancement concerné, sans repli permissif ni canal hors PZT.
- Erreur PA et disponibilité login OS distinguées.

## Paramètres et valeurs de recette

Six champs obligatoires sans défaut production, définis en session-integration : system_start_delay_s, session_start_delay_s, system_preconditions_wait_s, session_preconditions_wait_s, system_shutdown_budget_s, session_shutdown_budget_s. Recette Debian13 x86_64 en secondes : 0 et 0, 30 et 10, 30 et 10. Nombres finis non négatifs exigés ; booléen, chaîne, null, non fini et négatif refusés ; champs inconnus refusés ; absence refusée. Aucun défaut production. Aucune copie implicite vers Windows. La règle des défauts du composant ne s'applique qu'aux champs non budgétaires. config_profile_revision désigne la révision du profil de configuration attribuée par PBO et liée à config_ref, distincte de expected_revision et observed_revision de l'état OS ; le profil d'exécution protégé résolu garde ses règles d'autorité propres.

## Refus

- Paramètres absents ou invalides, préconditions non satisfaites, mandat expiré ou révoqué, autorité ou dépendance manquante : refus avant effet.
- Opération absente du catalogue, mode exclu du profil, canal hors PZT, fichier hors ensemble géré, shell arbitraire : refus sans téléchargement ni exécution arbitraire.
- Conflit d'autorités, effet inconnu après crash, restauration obsolète : blocage et réconciliation, sans double effet ni droit restauré. Le rejeu ne donne jamais une permission nouvelle ; autorités et périmètre courants sont revalidés pour accéder aux résultats et agir. Un timeout avant effet prouvé donne NONE avec REFUSED ou FAILED selon cause réelle, pas IN_DOUBT forcé.
- PAM sensible sans nouvelle autorité ; événement PAM seul ne crée aucun droit PBO et PA02.
