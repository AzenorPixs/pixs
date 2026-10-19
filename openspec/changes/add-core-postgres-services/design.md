# Conception — C02

## Statut et périmètre autorisé

ORIENTATIONS_DE_CONCEPTION_VALIDÉES. Les options A de D01, D02, D03 et D04 sont adoptées le 19 octobre 2026. Le complément documentaire couvre la traçabilité, le modèle logique et les interfaces ; le canon, les lots voisins et les tâches de réalisation non cochées restent préservés. C00 a été adopté et archivé le 18 octobre 2026. La portée de ces décisions est exclusivement documentaire : aucune implémentation, production de code ou migration n’est autorisée. Les schémas physiques, signatures et paramètres détaillés restent à décliner dans ces orientations lors d’un mandat de réalisation distinct.

## État actuel vérifié

Constat : User, DigitalIdentity, liaisons, groupes et appartenances sont des représentations mémoire. Les modèles backend persistants existants ne constituent pas les services Core complets.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/core/identity/models.py](../../../src/pixs/core/identity/models.py).
- [src/pixs/core/identity/groups.py](../../../src/pixs/core/identity/groups.py).
- [src/pixs/core/identity/tenant_membership.py](../../../src/pixs/core/identity/tenant_membership.py).
- [src/pixs/backend/models.py](../../../src/pixs/backend/models.py).
- [façade et limites de TenantMembership](../../../src/pixs/core/identity/README.md).
- [topologie pure](../../../src/pixs/core/scope/topology.py), [propagation](../../../src/pixs/core/scope/propagation.py) et [manifest Core](../../../src/pixs/core/component.toml).
- [registre commun de services](../../../src/pixs/kernel/registry/registries.py) et [descripteurs de contrats](../../../src/pixs/kernel/contracts/models.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Conserver la distinction User/DigitalIdentity et les UUIDv7 ; porter les données Core dans PostgreSQL avec propriétaire explicite, contraintes et services publics. Séparer scopes/platform/tenant, rôles, ACL et permissions ; créer les migrations après revue du schéma, sans écrire les tables d’un autre composant.

Le [cadrage Auth du 19 octobre 2026](../define-essential-autonomous-auth-module/design.md) propose `pixs.auth` essentiel indépendant, lui aussi sur PostgreSQL par défaut. C02 conserve exclusivement ses données et contrats Core ; Auth possède justificatifs, mappings d’authentification, politiques et sessions sous migrations distinctes. Les contrats partagés existants sont réutilisés sans déplacement et Core ne dépend d’aucune implémentation Auth. L’enrôlement demande les mutations via Commands Core autorisées ; ni OpenLDAP propre, ni KDC, ni source externe ne devient un référentiel canonique concurrent. Les deltas restent proposés dans les nouveaux changes ; D01–D04 et R01 sont conservés sans code ni tâches cochées.

Les tableaux ci-dessous décrivent le modèle logique et les contrats de travail de cette réalisation. Ils n’introduisent ni schéma HTTP, ni vocabulaire public, ni valeur de configuration. Tout choix qui modifierait une exigence ou une sémantique observable déjà validée requiert un delta présenté avant réalisation ; aucun delta n’est créé par ce complément.

## Modèle logique et propriété des données

Le [complément de stockage réversible du 19 octobre 2026](../add-reversible-core-directory-storage/design.md) prépare une option postinstallation OpenLDAP interne pour utilisateurs, groupes et ACL avec leurs relations nécessaires, puis un retour depuis l'état LDAP courant. C02 conserve son périmètre de provider PostgreSQL initial et ses décisions D01–D04 ; les garanties d'un provider LDAP et des mutations inter-stores requièrent une qualification distincte avant activation. Core reste propriétaire logique, sans transfert de l'évaluation des droits à slapd. Les formulations PostgreSQL ci-dessous décrivent le provider par défaut, sans implémenter cette option ni modifier les contrats purs.

Le propriétaire est `pixs.core`, avec un adapter Django séparé des objets mémoire existants. D01-A retient l’enregistrement existant [PixsCoreConfig](../../../src/pixs/backend/apps.py), `name = "pixs.core"` et `label = "pixs_core"`, pour les modèles et migrations Core dédiés. PostgreSQL externe reste la source de vérité. Les chemins internes des modèles, noms de tables et détails de migrations seront définis sous cette propriété ; aucune table existante de `pixs.backend` n’est réaffectée. Un module consommateur utilise les services publics, sans importer les modèles ORM privés.

| Donnée logique | Identifiants et relations | Invariants et frontière |
|---|---|---|
| Utilisateur | `user_id` UUIDv7 ; aucun champ nominatif ou credential ajouté par ce lot | Existence sans identité ; pas de fusion avec le User de Django ; les enrichissements métier restent propriétaires de leurs modules. |
| Identité numérique | `identity_id` UUIDv7 ; type et état des vocabulaires canoniques | `HUMAN`, `SERVICE`, `DEVICE`, `FEDERATED` et `ACTIVE`, `SUSPENDED`, `REVOKED`, `EXPIRED` restent distincts d’une assurance, d’une permission ou d’un état de persistance. C03 fournit l’authentification et les faits vérifiés. |
| Liaison utilisateur–identité | Références explicites vers les deux entités ; unicité de chaque référence dans la relation | Zéro ou une liaison dans chaque sens ; référence absente refusée ; aucun rapprochement par courriel ou provider. L’absence de ligne représente l’absence de liaison. |
| Tenant | `tenant_id` chaîne opaque non vide | Racine technique ; aucune conversion UUID, normalisation ou suppression des espaces des identifiants des profils existants. Le mode mono-tenant conserve le même contrat. |
| Nœud de scope | `scope_id`, `tenant_id`, `parent_scope_id` optionnel, références opaques | Un parent dans le même tenant, aucun cycle ni référence orpheline ; un parent absent désigne le rattachement au tenant racine. Le graphe générique ne devient pas propriétaire des données métier des scopes enfants. |
| Groupe | `group_id` UUIDv7 et périmètre explicite | TENANT exige un tenant cohérent ; PLATFORM exclut tenant/scope. Un groupe de plateforme ne donne aucun accès implicite dans un tenant. Aucune relation de groupes imbriqués nouvelle n’est ajoutée par le profil utilisateur–groupe existant. |
| Appartenance utilisateur–groupe | Paire `(user_id, group_id)` unique, références existantes | Relation N:N ; le périmètre du groupe ne vaut ni autorisation ni preuve d’appartenance tenant. Les règles runtime viennent de C04. |
| Appartenance identité–tenant | Paire `(identity_id, tenant_id)` unique, références existantes ; activation/révocation explicites | Relation N:N, y compris SERVICE sans utilisateur. Le cycle de vie persistant est distinct de la paire structurelle existante ; aucun état d’identité ne crée une appartenance active par déduction. D01 fixe les champs et transitions sans inventer un nouvel enum public. |
| Permission déclarée | Identifiant canonique, composant propriétaire, références de ressources/actions déclarées | Déclaration et persistance ne valent pas octroi. Les ressources/actions métier restent définies par leur propriétaire, sans clé étrangère vers une table privée externe. |
| Rôle et composition | Identifiant stable, périmètre, relations vers permissions et sujets explicites | Un rôle regroupe des permissions ; aucune autorité implicite d’un rôle administrateur. D01/D02 fixent la représentation des sujets et la validation des références. |
| ACL et politique | Identifiant/version, propriétaire, effet, selectors, conditions, obligations et validité du contrat C04 | Représentation déclarative validée, sans code exécutable ni nouvelle sémantique d’héritage. C02 stocke via contrat propriétaire ; C04 valide et évalue la politique courante. |
| Liaison du compte fonctionnel | Référence d’installation fournie par C08 et identité explicite ; unicité par installation | C08 crée ou réutilise le compte ; C03 l’authentifie ; C04 reconnaît son exception. Une migration ne crée ni compte ni credential. La liaison exclut second Super Admin, compte de service et délégation selon le canon. |
| Accord tenant du Super Admin | Liaison fonctionnelle et tenant explicite ; relation distincte d’une appartenance ordinaire | C02 fournit le stockage ; C04 décide et contrôle l’octroi/retrait, la fraîcheur et le périmètre. Un accord ne change pas la propriété d’une ressource et n’ouvre aucun autre tenant. |

La compatibilité conserve les objets frozen et leurs façades publiques, les erreurs structurelles et les règles d’identifiants actuelles. Les objets ORM et les DTO de services ne remplacent pas ces classes à l’import. Les représentations structurelles continuent à accepter les valeurs que leur contrat admet, sans Django, base ou autorisation réelle. La nouvelle couche persistante vérifie séparément existence, état et contexte ; elle ne renforce pas silencieusement les validateurs purs.

Les clés, références et cardinalités relèvent de contraintes PostgreSQL lorsque leur forme le permet, complétées par la validation propriétaire pour les invariants de graphe, de politique ou inter-entités. D01 distingue précisément ces deux niveaux : un `save()` ou une validation Python seuls ne prouvent pas l’intégrité concurrente. Les limites de taille, la génération des identifiants, les index et les suppressions de relations sont présentés avec le schéma physique avant code ; aucune valeur d’exploitation n’est déduite d’une fixture.

## Catalogue des services et contrats

Les noms d’opérations du tableau décrivent le catalogue de travail, sans signature Python ni route publique arrêtée. D02-A retient des contrats séparés par domaine, avec version SemVer indépendante du composant et déclaration dans les mécanismes communs. Leurs identifiants, signatures et schémas seront détaillés avant réalisation. Les lectures relèvent de QUERY, les mutations de COMMAND ; SERVICE décrit leur point de consommation synchrone. EVENT et HOOK ne remplacent pas une garantie de commande.

| Domaine | Lectures proposées | Mutations propriétaires proposées | Consommateurs et limites |
|---|---|---|---|
| Identités | Lire/lister utilisateurs, identités et liaisons ; résoudre les faits existants | Créer les entités, lier/délier explicitement ; appliquer les changements d’état autorisés par le contrat retenu | C03/C04/C06 ; aucun credential ni niveau d’assurance fabriqué. |
| Groupes et appartenances | Lire/lister groupes et relations utilisateur–groupe ou identité–tenant | Créer/modifier un groupe, ajouter/retirer une relation, activer/révoquer une appartenance tenant selon le modèle retenu | C04/C06 ; aucune appartenance ne devient un droit par elle-même. |
| Tenants et scopes | Lire les racines, le graphe et la propriété canonique sous contexte | Créer les racines et enregistrer/modifier les relations génériques de scopes | C04/C08 et modules propriétaires ; pas de modèle Organization/Workspace/Project métier dans Core. |
| Données d’autorisation | Lire les permissions, rôles, accords et politiques courantes via contrats | Persister les déclarations validées, affectations et accords explicites | C04 propriétaire des règles de décision ; une écriture invalide la version de faits/politique concernée selon le contrat commun. |
| Support d’amorçage | Lire l’état Core persistant nécessaire au parcours autorisé | Persister les éléments explicitement créés ou réutilisés par C08 selon le contrat R01 | C08/C03/C04 ; opérateur vérifié distinct du compte cible, aucune session préexistante du compte futur exigée, aucun privilège déduit d’UID 0 ou de C01. |

Chaque appel reçoit identité de confiance, ScopeContext canonique, corrélation et causalité applicables. Une mutation rejouable reçoit aussi l’identité d’opération et les éléments d’idempotence de C06. Les entrées ne sont pas prises dans un en-tête client comme faits vérifiés. Les sorties sont des valeurs contractuelles minimisées, sans QuerySet ni instance ORM transmise à un autre module.

Pour l’initialisation pré-session, le [contrat R01 propriétaire de C08](../add-installation-and-first-configuration/design.md) précise l’acteur admissible, les preuves, la décision liée au plan et les effets fermés. L’opérateur et l’identité cible sont distincts ; aucune session applicative du compte futur n’est requise comme précondition circulaire. C02 vérifie la provenance et les bindings du contrat par les ports de confiance, avec un sujet conforme au canon, sans accepter un booléen client ni la seule affirmation de C08. Si cette preuve ou ce mapping manque, aucune mutation Core n’est admise. Cette voie ne remplace pas les contrôles des services ordinaires et n’étend pas C01.

Le contrat distingue résultat confirmé, refus, validation invalide, conflit et indisponibilité. C06 conserve les codes publics et la traduction HTTP/localisée ; C02 ne crée pas de nouveau catalogue public d’erreurs. Les diagnostics n’exposent ni requête SQL, valeur sensible, credential, ni existence de ressource hors périmètre. Les exceptions techniques inattendues ne sont pas transformées en succès ou relancées silencieusement.

Les déclarations de capacités/contrats utilisent `provides` et `implements` du manifest et le registre de services existant. L’absence d’un contrat, une version incompatible ou deux fournisseurs admissibles sans sélection explicite restent des refus de composition. Le seul ajout de fonctions dans une façade Python ne prouve pas leur enregistrement contractuel.

## Transactions et concurrence

D03-A retient les transactions Django et les contraintes PostgreSQL existantes, sans nouveau moteur. Les mutations de topologie d’un tenant sont sérialisées sur une ressource propriétaire commune à ce tenant ; la validation du graphe intervient dans la même transaction. Pour les liaisons et appartenances, les références et ressources touchées sont verrouillées dans un ordre déterministe, avec contraintes d’unicité de dernier ressort. Les ressources de plateforme possèdent leur propre périmètre d’exclusion. Le contrôle des versions détecte les écritures obsolètes. Les détails d’exclusion et d’intégration C04/C05 seront définis dans ce choix avant réalisation ; ils ne sont pas remplacés par une stratégie principalement optimiste.

Une version de faits ou de ligne permet de détecter une écriture obsolète ; son format est fixé avec le schéma. Une version du PDP ou un ancien ALLOW ne devient pas une autorisation durable. Le contrat commun définit comment une révocation concurrente, une modification de rôle/ACL ou un changement de scope invalide les faits et s’articule avec la transaction en cours, sans annoncer une absence de course avant preuve.

Séquence de mutation ordinaire à concrétiser avec les lots propriétaires ; la première création/réutilisation suit les contrôles pré-session et de reprise de R01, sans authentifier par avance le compte cible :

1. Résoudre l’acteur, le contexte et les références canoniques ; valider la commande et les conditions courantes par les contrats C03/C04.
2. Ouvrir la transaction propriétaire, acquérir les exclusions nécessaires et revalider les faits dont la modification concurrente influencerait l’autorisation ou l’intégrité. L’exception Super Admin authentifiée suit C04 dans son seul périmètre ; aucune exception n’est transférée aux primitives structurelles.
3. Appliquer la mutation et enregistrer dans la même frontière les résultats d’idempotence et éléments destinés à publication lorsqu’ils sont requis par les contrats C06/C09. Le composant reste propriétaire de ses écritures ; les ports voisins reçoivent le contexte transactionnel convenu, sans accès direct de C02 à leurs tables privées.
4. Obtenir la garantie d’audit C05 applicable avant d’annoncer une mutation conforme. Pour un compte ordinaire, une obligation non satisfaite interdit la confirmation ; pour la dérogation Super Admin reconnue par C04, aucune preuve d’audit absente n’est inventée.
5. Confirmer après commit. C09 publie seulement les éléments engagés. Si la réponse est perdue, C06 restitue le résultat idempotent après contrôles courants, sans refaire la mutation.

Un refus avant mutation ne laisse aucun effet métier. Son audit est géré par C05 dans une frontière qui ne disparaît pas avec le rollback de l’opération refusée. Une panne technique annule les effets de la transaction concernée ; une issue de commit incertaine exige réconciliation avant rejeu. L’indisponibilité du sink, le conflit attendu et l’état inconnu restent des résultats distincts. Aucun callback mémoire ou `on_commit` isolé n’est présenté comme outbox durable, preuve d’audit ou garantie de livraison.

## Interfaces, dépendances et conditions d’activation

La dépendance de préparation et de réalisation de C02 reste C00 adopté. Les interfaces ci-dessous sont des contrats de conception et des conditions d’intégration ; elles n’ajoutent pas une dépendance inverse globale C02 → C04/C05/C06/C09/C10. Les modèles et adapters peuvent être réalisés et testés isolément sur fixtures sans être exposés comme services métier utilisables.

La clôture future de C02 porte sur ses données, contraintes, services propriétaires et points de raccordement conformes aux contrats arrêtés, avec refus fermé si un port obligatoire manque. La conformité locale de ces raccordements peut utiliser des doubles, à condition d’en borner explicitement la preuve. Les recettes runtime complètes sont exécutées par les lots consommateurs après disponibilité de leurs implémentations ; elles ne sont pas exigées en amont comme preuve de leur propre livraison dans C02. Leur état reste une condition d’activation suivie par leur propriétaire et par C17. Si un contrat indispensable reste indéfini, sa définition précède le code dans le mandat de réalisation, sans fabriquer un adapter permissif ni rouvrir D03-A.

| Lot propriétaire | Fourniture attendue et consommation de C02 | Condition avant usage intégré |
|---|---|---|
| [C03 — authentification](../add-initial-authentication-and-sessions/proposal.md) | C02 fournit l’identité persistante et ses références ; C03 fournit le contexte authentifié courant | Aucun état structurel, booléen client ou identité SERVICE ne remplace l’authentification. |
| [C04 — autorisation](../integrate-runtime-authorization-and-super-admin/proposal.md) | C02 fournit faits et données propriétaires ; C04 fournit PEP/PDP, filtrage source, reconnaissance Super Admin et décision d’accord tenant | Identité, périmètre, fraîcheur et obligations applicables vérifiés ; révocations concurrentes traitées selon D03. Les profils PDP préparatoires restent inchangés. |
| [C05 — audit](../add-durable-minimized-audit/proposal.md) | C02 fournit acteur, cible, effet/refus et corrélation minimisés ; C05 fournit stockage, sink et preuve durable | Contrat de commit/rollback et d’audit des refus établi ; indisponibilité et dérogation canonique exercées. La reprise du journal C01 reste dans C05/C08. |
| [C06 — API](../add-protected-core-http-commands-and-queries/proposal.md) | C02 fournit commandes/lectures propriétaires et résultats ; C06 fournit façades HTTP, pagination, idempotence publique et erreurs | Aucun endpoint ni traitement protégé n’utilise un adapter de persistance comme bypass de C04/C05. |
| [C08 — installation](../add-installation-and-first-configuration/proposal.md) | C02 fournit les données et écritures Core ; C08 possède le contrat d’autorité R01, les preuves liées au plan, marqueurs et reprise ; C03/C04 vérifient l’opérateur et l’autorisation | Identité opérateur distincte du compte cible ; effets bornés au plan courant, exclusion/idempotence et audit applicables ; aucune autorité C01 métier ni mutation faute de preuve. Recette B01–B10 de C08, V05/V07 de C02. |
| [C09 — traitements](../add-reference-worker-scheduler-and-event-delivery/proposal.md) | C02 fournit effets et événements contractuels ; C09 possède outbox/livraison et exécution asynchrone | Publication après commit et déduplication ; acteur initial et contexte réautorisés, sans credentials Super Admin. Les contrats Bulk restent distincts. |
| [C10 — gouvernance](../enforce-core-data-governance-and-lifecycle/proposal.md) | C02 fournit propriété, références, dimensions de cycle de vie et protections de schéma ; C10 publie profils/politiques et réalise demandes/purges | Aucune donnée non classifiée exposée ; aucune suppression physique implicite en attendant C10. |

C07 conserve un hôte intermédiaire non prêt tant qu’une garantie obligatoire manque. C17 agrège les preuves sur le paquet C18 ; leur absence ne se remplace pas par le succès des unités de C02. C14 conserve la gestion PZT/DNS ; aucune exécution PA/PZT ou projection LDAP n’est sélectionnée par C02.

## Gouvernance dès la persistance

Le dictionnaire D01 distingue les dimensions métier, de persistance et de rétention. `DigitalIdentity.state` n’est ni `persistence_state`, ni une preuve d’activation de membership ou de droit. Les vocabulaires canoniques sont réutilisés sans transition ni durée inventées. Les références de politique, de rétention et de suppression sont définies avec C10 ; aucune donnée personnelle réelle n’est nécessaire à la conception ou aux fixtures.

D04-A retient des relations explicites avec protection des références et absence de cascade inter-module implicite. Une suppression ordinaire n’est pas traduite par défaut en effacement physique ; suppression logique et retrait/révocation d’une relation sont définis par leur contrat propriétaire. La politique reste restrictive avant classification et la purge explicite relève de C10 avec les garanties applicables. Les durées sont déclarées par ressource, sans valeur déduite d’une fixture. Le schéma conserve les éléments nécessaires aux holds, aux tombstones et à la restauration, sans prétendre que leur seule présence implémente ces mécanismes. Les dérogations Super Admin canoniques restent conservées.

Avant exposition, C10 publie le profil versionné : propriétaire, source, classes, confidentialité, caractère personnel, finalités, consommateurs, rétention, suppression, export et lignée. En attendant, les données restent sous politique restrictive ; aucune API, projection, événement ou diagnostic n’exporte un champ non déclaré. C02 refuse les chemins destructifs sans contrat ; les demandes de purge et la propagation aux dérivés demeurent réalisées par C10/C09/C16 avec les dérogations Super Admin canoniques.

## Recette liée aux tâches

Les vérifications V01 à V12 sont des critères futurs, pas des résultats. `requirements.md` relie chaque exigence/scénario retenu à ces vérifications, aux tâches et au responsable. R01 enrichit V05/V07 avec la recette B01–B10 définie dans C08, sans créer une treizième vérification C02 ni compter ces cas comme des scénarios canoniques ajoutés. Pour une condition non sélectionnée, conserver le motif et la source ; un test absent ou impossible n’est pas assimilé à une réussite.

| Vérification | Cas et résultat attendu | Tâches | Niveau et responsable |
|---|---|---|---|
| V01 | UUIDv7 et vocabulaires valides/inconnus ; entités indépendantes, unicité de liaison dans les deux sens, références absentes ; SERVICE sans User ; façades pures sans IO, session ou privilège nouveaux | 1.1, 2.1, 2.2, 2.4, 3.1, 3.2 | Régression des unités/façades existantes et contraintes PostgreSQL de C02 ; conserver les différences de portée. |
| V02 | Appartenances N:N sans doublon, références absentes refusées ; activation/révocation runtime distinctes de la paire structurelle ; course sur même liaison : pas de double association confirmée | 2.1, 2.2, 2.4, 3.2 | PostgreSQL réel avec transactions concurrentes C02 ; activation sous contrat C04. |
| V03 | Racines et enfants cohérents ; cycle, parent absent, déplacement inter-tenant et propriété ambiguë refusés, y compris lors de deux mutations concurrentes | 2.1, 2.2, 2.4, 3.2 | Régression scope et PostgreSQL réel C02 ; aucune donnée métier de scope enfant introduite. |
| V04 | TENANT sans tenant, PLATFORM avec identifiants et claim d’élargissement refusés ; identité/permission non vérifiable : aucun effet ni divulgation ; liste filtrée à la source | 2.3, 2.4, 3.2 | Contrats C02/C04 puis intégration C06 ; un contexte structurel valide ne suffit pas. |
| V05 | Un seul compte fonctionnel par installation ; opérateur R01 vérifié avant première session, compte cible distinct ; saisies différentes/plan non confirmé refusés, base conservée réutilisée ; usage de service ou délégation du Super Admin refusés ; accords tenant explicites | 1.2, 2.1, 2.3, 2.4, 3.2 | Gardes et stockage C02 ; recette C08 B01–B06/B09/B10 avec C03/C04, y compris tenant non accordé refusé et tenant accordé malgré ACL. Aucun compte réel créé par la rédaction. |
| V06 | Contrat absent/incompatible ou fournisseur ambigu refusé ; catégories et SemVer respectées ; consommation sans modèle privé ; pureté des façades et substitution compatible conservées | 2.1, 2.3, 3.1, 3.2 | Registres/manifests et consommateur de contrat C02 ; pas de nouveau moteur de registre. |
| V07 | Refus et rollback sans effet métier ni publication ; panne d’audit ordinaire refusée ; dérogation Super Admin reconnue sans fausse preuve ; réponse perdue rendue par idempotence ; livraison répétée sans double effet ; R01 rejoué/concurrent/crash avant et après commit ou marqueur réconcilié sans seconde création | 2.3, 2.4, 3.2 | C02 prouve sa transaction et ses gardes ; C08 B01/B02/B06–B10 et C04/C05/C06/C09 prouvent les parcours intégrés. Reçu C01 sans autorité métier et absence de privilège anticipé du compte futur vérifiés ; doubles et preuves runtime séparés. |
| V08 | Migration sans propriétaire/origine/cible/compensation déclarés refusée ; installation vierge distincte d’une mise à niveau ; périmètre de migrations inchangé hors Core | 1.2, 2.2, 2.4, 3.2 | Plan de migration C02, consommé par C08/C16 ; aucune base réelle de production utilisée. |
| V09 | Deux exécuteurs d’un même périmètre : un seul progresse ; arrêt pendant migration puis reprise sur avancement vérifié, sans duplication ni perte | 2.2, 2.4, 3.2 | PostgreSQL réel C02 avec contrats d’exploitation applicables ; limites et propriétaire du planificateur déclarés. |
| V10 | Coexistence N/N+1 si origine supportée ; ancien consommateur encore actif : contraction refusée ; retour applicatif seulement si schéma/données compatibles ; aucune rétrogradation automatique | 2.2, 2.4, 3.2 | Contrat C02/C16. Première installation sans origine ou sans contraction : non-applicabilité limitée et motivée, jamais dispense globale de reprise/exclusion. |
| V11 | Dimensions d’état distinctes ; références protégées et absence de cascade implicite ; donnée non classifiée non exposée ; suppression ordinaire et purge sous leurs contrats, effacements conservés à la restauration | 2.1, 2.2, 2.4, 3.2 | Schéma et refus C02 ; politiques, purge et restauration C10/C09/C16. Les durées/holds non décidés bloquent les opérations concernées. |
| V12 | Refus et indisponibilités à diagnostic stable sans valeur sensible ; secrets absents des modèles, fixtures, déclarations et preuves ; versions/portées des résultats distinctes d’une qualification P0 | 3.1, 3.2, 3.3, 3.4 | Contrôles du périmètre C02 et recette C17 ; succès, échec, non exécuté et non applicable séparés. |

Les tests existants d’identité, liaisons, groupes, TenantMembership et scopes sont des régressions à conserver, notamment `test_identity_models.py`, `test_identity_links.py`, `test_group_membership.py`, `test_tenant_membership.py` et les façades d’intégration correspondantes. Leur présence n’est pas une preuve d’exécution. La réalisation ajoute les preuves PostgreSQL et inter-lots nécessaires sans renommer les tests structurels en preuve de persistance.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions adoptées et détails de réalisation

Les quatre options A sont adoptées le 19 octobre 2026. Les alternatives B sont écartées pour C02. Les détails ci-dessous déclinent ces décisions ; ils ne constituent pas une demande de revalidation des mêmes orientations. Tout écart structurant ou changement normatif resterait à présenter séparément, sans rouvrir C00/C01.

| Arbitrage et statut | Option A retenue | Détails et preuves de réalisation |
|---|---|---|
| D01 — VALIDÉ, option A | Réutiliser `PixsCoreConfig` et le label `pixs_core` ; modèles/migrations Core dédiés et relations normalisées, objets mémoire préservés. | Détailler chemins internes/tables, types/tailles, générateur UUIDv7 compatible, contraintes, cycles de vie et représentation des politiques/accords ; justifier le plan de retour. V01/V02/V03/V05/V08/V11. |
| D02 — VALIDÉ, option A | Contrats versionnés séparément par domaine, catégories COMMAND/QUERY et consommation SERVICE déclarées dans les mécanismes existants. | Détailler identifiants/versions, signatures/schémas, ressources/actions, erreurs et déclarations manifest ; conserver les façades pures. V04/V06/V12. |
| D03 — VALIDÉ, option A | Transactions Django, contraintes PostgreSQL, verrous ciblés dans un ordre déterministe, versions contre écritures obsolètes ; topologie sérialisée par tenant. | Détailler acquisition des faits C04, réconciliation des révocations, port transactionnel C05 et participation C06/C09 ; distinguer preuve locale et activation. V02/V03/V04/V05/V07/V09. |
| D04 — VALIDÉ, option A | Politique restrictive avant classification, dimensions d’état distinctes, références protégées, suppression logique par défaut des ressources métier et purge explicite C10 ; dérogations canoniques conservées. | Détailler par ressource classification, transitions, rétention/suppression, consommateurs et effets de révocation ; aucun secret ni valeur de production. V01/V05/V11/V12. |

La validation porte uniquement sur la conception documentaire : elle n’autorise aucune implémentation ni production de code. Les schémas et contrats détaillés et les preuves restent à établir dans un mandat distinct. Si un détail exige un comportement normatif nouveau, présenter les seules clauses/scénarios affectés avant de modifier le canon. Les arbitrages PA/PZT restent hors périmètre de ce complément.

Le complément documentaire R01 du 19 octobre 2026 précise le raccordement C08/C02 à l’intérieur de ces orientations. C08 conserve la source unique du contrat d’autorité et des cas B01–B10 ; C02 conserve les gardes, contraintes et preuves locales. Les mécanismes concrets C03/C04 restent à déclarer avant réalisation de cette branche, sans prolonger l’exception C01 ni présumer un nouveau comportement normatif validé.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [define-first-installable-pbo-profile](../archive/2026-10-18-define-first-installable-pbo-profile/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

La recette V01 à V12 et la matrice de `requirements.md` constituent les critères de réalisation. Chaque preuve identifie tâche, exigence/scénario, version, environnement, commande, résultat et portée ; une preuve partagée n’est pas comptée plusieurs fois.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

Le contrat de migration fixe propriétaire, origine/cible, préconditions, dépendances, mode d’exécution, avancement persistant et retour/compensation. Il sépare installation vierge, expansion/backfill et contraction éventuelles. Le plan est déterministe et exclut deux exécuteurs du même périmètre ; le démarrage ne migre pas implicitement. La réalisation déclare les origines réellement supportées : aucune ancienne version distribuée n’est inventée pour satisfaire une case. Une inversion de migration exercée sur fixture ne devient pas une politique de downgrade de production. V08/V09/V10 couvrent ces distinctions.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

Cette section conserve l’instantané du 17 octobre. Le complément courant utilise le canon présent et l’adoption C00 ; le nombre historique de clauses PZT ne devient pas un comptage courant ni une autorisation d’exécution.

### T07 — Administration utile avec compte ordinaire

Les grandes rubriques existent ; il faut arrêter le catalogue minimal d’actions et prouver le parcours ordinaire, pas seulement celui du Super Admin. Compléter critères de C06/C13 et recette C17 ; aucun module métier ajouté.

Contrôles à intégrer : Créer identité/utilisateur/groupe/appartenance selon droits ; Lire/modifier ACL sans élargir tenant/scope ; Accès interdit invisible et inexécutable ; API utilisable sans PFO.

### T10 — Mutation, audit, idempotence et outbox

Les composants prévoient chacun leur partie ; la frontière transactionnelle et l’échec avant/après commit doivent être explicitement communs. Compléter contrats C05/C06/C09 avec refus distincts et résultat réconcilié ; pas de nouveau broker.

Contrôles à intégrer : Rollback sans événement publié ; Commit puis réponse perdue restituant résultat idempotent ; Double livraison sans double effet propriétaire ; Refus auditable sans mutation métier.

### T14 — PZT/DNS gérés sans exécution PA

La table 193 clauses reste conditionnelle et exige revue par rôle avant adoption ; classement exécutant ne retire pas les clauses PBO de gestion. Conserver C14 comme propriétaire, contrats/schémas/valeurs administrées explicités avant code ; aucun nouveau change exécutant sélectionné.

Contrôles à intégrer : Modules essentiels présents même réseau désactivé ; État souhaité distinct de mesure/appliqué ; Suffixe/droits/conflits des données gérées conformes ; Aucune publication DNS/réseau ni modification hôte inventée.

Voir [audit transversal durable](../archive/2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.

## Vérifications documentaires du 19 octobre 2026

Les contrôles ci-dessous décrivent le complément documentaire initial, avant adoption des quatre options A. Ils conservent leur périmètre historique ; l’enregistrement ultérieur des décisions et l’alignement des cadrages ne sont pas présentés comme une implémentation ou une recette produit.

Le complément couvre C02-A01 par les références Core rétablies, C02-A02 par le modèle logique et D01, C02-A03 par le catalogue et D02, C02-A04 par les interfaces/transactions et D03, C02-A05 par l’allocation de gouvernance et D04, C02-A06 par V08/V09/V10 et la matrice. Cette couverture documentaire n’est pas une preuve d’implémentation ni une adoption des choix encore ouverts.

| Contrôle exécuté | Résultat et limite |
|---|---|
| OpenSpec 1.14.3 ciblé strict | `/usr/bin/env -i PATH=/home/devops/node/current/bin:/usr/bin:/bin LANG=C.UTF-8 OPENSPEC_TELEMETRY=0 /home/devops/node/current/bin/node /home/devops/.local/npm/bin/openspec validate add-core-postgres-services --strict` : exit 0, change valide. Information native : `skip_specs` accepte zéro delta. Ce résultat ne prouve pas la suffisance fonctionnelle ni les recettes V01–V12. |
| Traçabilité statique | 18 exigences principales / 24 références de scénarios et 46 exigences transversales / 54 références : 64 / 78 au total. Titres, lignes et listes complètes de scénarios vérifiés dans leurs blocs canoniques ; références de tâches et V01–V12 résolues, repères uniques. |
| Encodage et liens | Quatre documents UTF-8 sans BOM, fins de ligne LF ; cibles locales existantes dans le projet et blocs clôturés. Les références du canon correspondent aux titres/lignes indiqués ; aucun rendu graphique ou navigateur revendiqué. |
| Portée et conservation | Empreintes comparées sur 110 fichiers ciblés, sans Git : seuls les quatre documents de C02 sont modifiés ; canon, cadrages, documents voisins et métadonnée du change préservés. Inventaire du dossier inchangé, dix tâches non cochées. Ce relevé ciblé ne prétend pas inspecter tout le système de fichiers. |
| Vérifications produit | Tests applicatifs, PostgreSQL, navigateurs, construction et migrations non exécutés : complément documentaire uniquement. Aucun archivage, rapport statistique, nouveau change, delta ou effet de déploiement. |
