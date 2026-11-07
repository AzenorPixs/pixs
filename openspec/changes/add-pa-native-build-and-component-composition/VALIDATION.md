# Validation — PA01

## Portée et autorisation

Le développeur a autorisé la poursuite du change le 23 octobre 2026. Les décisions D1–D9 restent acquises. Chaque tâche est traitée et validée séparément ; les statuts de réalisation sont ceux de tasks.md, sans qualification globale déduite de ce document. Aucun droit système, installation, accès métier, dépendance nouvelle, Git ou activation réseau supplémentaire ne découle de la poursuite.

## Tâche 1 — Audit courant du 23 octobre 2026

L’ancien inventaire qui déclarait les modules de gestion Agent/PZT absents est périmé. L’audit courant distingue les contrats présents, les preuves historiques, la chaîne minimale exercée et les exécutants restant à réaliser. Le périmètre est limité aux sources explicitement listées ci-dessous ; aucune absence générale du dépôt ni validité fonctionnelle actuelle d’un service n’est inférée d’une lecture.

### Six correspondances canoniques

Les copies et empreintes historiques de [requirements.md](requirements.md) restent inchangées. Le canon courant prévaut sur les anciennes mentions Nuitka ou du quatrième binaire PA rattaché à PZT. Empreinte du bloc : titre Requirement inclus jusqu’au suivant exclu, blancs terminaux retirés puis un LF ajouté ; scénarios inclus.

| Source | Exigence | Ligne | Scénarios inventoriés | SHA-256 du bloc courant |
| --- | --- | ---: | ---: | --- |
| [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md) | Trois binaires PA et six modes distincts de PZT | 64 | 1 | `5cd5cae10cd478a8ffb30c4e15180dfdc341506019583f78882f62ec99106408` |
| [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md) | Compilation différenciée validée | 78 | 1 | `49d91499d8f83f1c794a0c59612a178648ad502a5b43f2965eba5f1f79a072e6` |
| [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md) | Composition au build et catalogue fermé | 108 | 1 | `0ed896227fd4520562a556c15ca86d634e059dc29313794ff743d8324201c20b` |
| [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md) | Paramètres ouverts et absence d'implémentation implicite | 296 | 1 | `2fe8f8e831ff5c8809f75a824394b629f715e43baab2b850615835c04c39ba78` |
| [openspec/specs/pzt/spec.md](../../specs/pzt/spec.md) | Module essentiel pixs.pzt et exécutable PZT indépendant | 77 | 1 | `1063497b290fd7bb8e8abad2dad81ac19bb67f139b4c911c98be000279df7b7c` |
| [openspec/specs/reference-runtime/spec.md](../../specs/reference-runtime/spec.md) | Couche exécutable PA séparée | 221 | 1 | `409ab89f825b092bd0b952bce1b1e35b9f4b326cd4c20d55d333a5a993bb892f` |

Les six scénarios sont :

- Répartition PA et PZT.
- Compilation des composants distincts.
- Composition au build et catalogue fermé.
- Paramètres ouverts et absence d'implémentation implicite.
- Réseau désactivé et gestion conservée.
- Exécutants distincts du backend.

### Dépendances canoniques de préparation PostgreSQL et de prébase

| Source | Exigence | Ligne | Scénarios inventoriés | SHA-256 du bloc |
| --- | --- | ---: | ---: | --- |
| [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md) | Préparation PostgreSQL par le PA système | 422 | 3 | `1bb84b21ded8a901d211dc09b79448de9fd592ef859b33e281bc1139eebe9bbf` |
| [openspec/specs/pzt/spec.md](../../specs/pzt/spec.md) | Amorçage local PA PZT indépendant de PostgreSQL | 13327 | 4 | `e9018bc483e91c46211cb10f1d6c1bc24340a8a979a254734e2d507a09320bc9` |
| [openspec/specs/authorization/spec.md](../../specs/authorization/spec.md) | Autorité technique PA PZT et lancement PBO sans base applicative | 156 | 4 | `5754adc44be72ee6925550ff504f32552ed7760dcfa01d85b0ea3961b9406b2f` |

La préparation technique PostgreSQL et le prébase sont adoptés fonctionnellement, mais leur exécutant concret n’est pas livré par cette lecture. Le prébase PLATFORM repose sur une politique et des identités techniques protégées indépendantes de la base à préparer ; il ne dépend pas de C03/C04 pour obtenir leur propre connexion. Il ne confère ni tenant, ni mutation métier, ni migration applicative ou exception Super Admin. Tous échanges PBO–PA restent sous PZT ; absence de PZT ou fraîcheur non vérifiable ferment l’admission. Les services de gestion PBO dépendants PostgreSQL ne satisfont pas à eux seuls ce contrat prébase.

### Existant à réutiliser et limites

- Les manifests `pixs.agent` et `pixs.pzt` sont présents, version 0.1.0, type MODULE. Ils décrivent la gestion PBO, pas les exécutants PA/PZT.
- `pixs.agent.management` expose ses contrats de frontière 1.0.0, avec AllowedCatalogEntry et paramètres explicites ; la validation de structure ne prouve ni transport ni autorisation cryptographique. Le service PostgresAgentManagementService et ses adapters utilisent les autorités PBO/PG.
- Les contrats/configurations et le lifecycle de gestion `pixs.pzt` existent ; PztManagementAdapter ne constitue pas le démon réseau indépendant.
- Les mécanismes génériques de manifests/composition existent et doivent être réutilisés sans embarquer Django/PostgreSQL comme autorité métier des exécutants. Une composition partielle ou une fixture ne prouve pas la disponibilité produit.
- C00 est recoupé depuis son archive : profil `pbo-p0-debian-local-v1`, exécution PA et réseau PZT non sélectionnés dans le premier P0. La sélection PA01 demeure distincte ; aucun P0 actif n’est déduit.
- C07 est recoupé depuis sa proposition et VALIDATION.md archivées : socle hôte, lifecycle et contrôles historiques bornés, avec limites explicites des adapters/attestations et de la qualification P0. Les fixtures initiales ou frontend ne remplacent pas ces preuves. Ces contrôles historiques ne sont pas réexécutés par cet inventaire.
- Les tests unitaires Agent présents constituent des sources de cas de contrôle ; leurs fixtures synthétiques ne sélectionnent pas un catalogue produit. Aucun de ces tests métier n’est exécuté par la tâche d’inventaire.

### Qualification minimale déjà acquise

Le rapport local `output/cismp/cismp7-pixs-023c11510a274b19/qualification-pa01/rapport-preuves.json` a pour empreinte SHA-256 `89d2f70a43c3e4d566b91dcd2e8c6d592b3ad0636ce9a221bf0e62e6ccbe8b46`. Son rapport et six artefacts ont été relus et leurs empreintes/tailles recoupées. Il prouve le démonstrateur CPython 3.14.9 avec GIL, Cython 3.3.0 et GCC 14.2.0, génération C/compilation/liaison/lancement sur VM, pas les quatre exécutables produit. Le préfixe runtime DevOps subsiste ; aucune distribution autonome, cible physique ou recette PA/PZT n’est qualifiée.

### Complément réellement manquant

1. Les quatre exécutables D4 et leurs modes D6, construits sous leurs propriétaires PA/PZT distincts. Aucune déclaration de build ou de mode n’a été repérée par la recherche ciblée sous src/, scripts/ et pyproject.toml ; ce constat ne couvre pas les sources exclues ni une existence hors périmètre.
2. La fermeture du runtime/dépendances D7, le lancement après déplacement du répertoire et l’absence de Python hôte requis.
3. Le lanceur natif isolé D8, ses erreurs propagées et ses refus des chemins Python externes.
4. Le profil de build TOML fermé D9 et le registre des seules opérations réellement livrées, avec schémas, contrats, propriétaires, versions et compatibilité.
5. Le catalogue concret et les mandats d’exécution du profil retenu. C08 a confirmé que ses noms inspect_postgresql / prepare_postgresql / get_postgresql_result 1.0.0 et leur classification restent proposés : ils ne sont pas traités comme adoptés. Aucun mécanisme de confiance ou droit privilégié n’est inventé.
6. Les recettes R01–R68 applicables, les dépendances réelles, les mesures et preuves par cible, avant toute déclaration de livraison. Les scénarios canoniques sont inventoriés ici, pas exécutés.

### Contrôle natif de l’inventaire

Une commande Python en lecture seule a chargé le contrôle depuis le checkpoint et vérifié son empreinte SHA-256 `415dec1ab09b9e13c9a9076a7c1f70fe92d4ba9eab177731d3793b653a34b86c` avant exécution. Elle n’importe ni n’exécute les sources produit : AST/TOML, textes et empreintes seulement.

- Mandat : `req-2f7957a6c9e347e6a2bbd22ae1ce9b2a`.
- Partie native : `prt_167b0c7040014mFKmlEHkSG1Sc`.
- Rapport OpenCode traité : `msg_167b0d6b2001GlEX5lWceeDXXC`.
- Code de sortie observé : **0**.
- Résultat : 6 correspondances / 6 scénarios, 3 blocs liés, 31 sources fingerprintées, 15 sources Python analysées syntaxiquement sans exécution, manifests de gestion présents, rapport VM et 6 artefacts préservés, UTF-8/LF et 10 cases encore non cochées au contrôle.

La validation OpenSpec ciblée et le cochage élémentaire sont tracés séparément dans le checkpoint et tasks.md. Ce contrôle d’inventaire ne vaut pas recette fonctionnelle ni autorisation des opérations proposées par C08.

### Empreintes des sources de l’audit

| Source au 23 octobre 2026 | SHA-256 |
| --- | --- |
| [openspec/config.yaml](../../config.yaml) | `6b0670871b7624d6ddd4921aa2742eeafeb7444e757c73108dc406dead14872f` |
| [openspec/changes/add-pa-native-build-and-component-composition/.openspec.yaml](.openspec.yaml) | `76742375750274d44605344096cb52afa57ba797f80f5899efa8b738462025f8` |
| [openspec/changes/add-pa-native-build-and-component-composition/requirements.md](requirements.md) | `cb6ccf6c0f15cfbd87f78b1f53fc6850896f7c622e40506e863b8738f9139919` |
| [openspec/changes/add-pa-native-build-and-component-composition/design.md](design.md) | `10e73fc4a3695b4caa1be664a207b5721ea5bfa5c51060754d7cfd9d463fce16` |
| [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md) | `c6ed3e0ac08d37f5d9101ed05dd877f27fee160985a5ee568ec3bc35f6dde7ef` |
| [openspec/specs/pzt/spec.md](../../specs/pzt/spec.md) | `5a5aea7ef86c061905f17cb3acc36cc841acb4d9e4ffa122735793a12a022e0c` |
| [openspec/specs/reference-runtime/spec.md](../../specs/reference-runtime/spec.md) | `6bbb170eb652b0b07a7b7dd61775b1cd52284fa7b53b05374c8f3267b089fed7` |
| [openspec/specs/authorization/spec.md](../../specs/authorization/spec.md) | `7dcd542b1e89020ba0363b6b74d3d0bc8fbd592af5b55226d7e2c00845a413de` |
| [src/pixs/agent/contracts.py](../../../src/pixs/agent/contracts.py) | `bbe5144bd81cbe55a372ee8d0426b1202719ce03aaae345bc1e8650d3661e805` |
| [src/pixs/agent/service.py](../../../src/pixs/agent/service.py) | `ba5d76c2f2c068840a60c686b6a81e76f3fb7a686d8f7d4a1aa1d2f0d26dc1a5` |
| [src/pixs/agent/authorization.py](../../../src/pixs/agent/authorization.py) | `864373830e9f929e02f70a60bc3254e8da2d3bf711ed35af29ee0598d3d5e496` |
| [src/pixs/agent/component.toml](../../../src/pixs/agent/component.toml) | `29347b801dad43255aecc4f630bd3019680f7440cc34ab8a08f4f85a502545a1` |
| [src/pixs/pzt/contracts.py](../../../src/pixs/pzt/contracts.py) | `f71da5bc06c980235634ff64836c5ccfadc0f5d3de59c6050c756ca6435a5451` |
| [src/pixs/pzt/configuration.py](../../../src/pixs/pzt/configuration.py) | `18910097ee2e6c7e8e20c28186bda1205f9ce870c738f71beca2eac058871123` |
| [src/pixs/pzt/lifecycle.py](../../../src/pixs/pzt/lifecycle.py) | `80681efab766d2c18531253d3c8f2cb0c42ce01781f0e67be5c05214918cd2f0` |
| [src/pixs/pzt/component.toml](../../../src/pixs/pzt/component.toml) | `01a01626ee8d4b65472ad5037b17293110197828c57c1e941a908e634abbf090` |
| [src/pixs/backend/host_composition.py](../../../src/pixs/backend/host_composition.py) | `1f839c4a3f4971b7ecf24038779319e995379282520d497b5c19ae9f606a63f9` |
| [src/pixs/backend/host_plan.py](../../../src/pixs/backend/host_plan.py) | `d8804de4fc875a3b36ef5c0c59cb46111fe7b13b59896b60f13a5561e3769393` |
| [src/pixs/backend/host_runtime.py](../../../src/pixs/backend/host_runtime.py) | `7d5de36c83cf0969d89b9f1a899eb69732b083c1f797a19b1fbe063bd8dbec55` |
| [src/pixs/kernel/composition.py](../../../src/pixs/kernel/composition.py) | `0b749b5f6821006b271abc2773ac4616df0a49de5a4dbb2f7131c9fbf0c6cd9d` |
| [src/pixs/kernel/manifest/models.py](../../../src/pixs/kernel/manifest/models.py) | `9c0ea7236d5166c15345260a4b0fd0f43731e023a07dd901630c98c7a088b5e0` |
| [tests/unit/test_agent_management_contracts.py](../../../tests/unit/test_agent_management_contracts.py) | `ddee589e304b5315a5db334fae2243cf8ef4ff72c5d227df531e98f308120085` |
| [tests/unit/test_agent_manifest.py](../../../tests/unit/test_agent_manifest.py) | `7577a599c504b183b7aafc3e93abd04887164401fdbc98be02407be3d6929576` |
| [tests/unit/test_agent_service_ports.py](../../../tests/unit/test_agent_service_ports.py) | `29db90ff29086ff4bbcb20f4d16097d79fa4b47801131560f266550f651bf22c` |
| [tests/unit/test_agent_storage_codec.py](../../../tests/unit/test_agent_storage_codec.py) | `ca842ba7e80c38fa005fe7c9fac4a9c80bb24eafae3354fabe9d61a351115e85` |
| [openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile/proposal.md](../archive/2026-10-18-define-first-installable-pbo-profile/proposal.md) | `caf0b1e7d626e740f403b46d3438a465f1dabf8104a79f2134a391932f6ec7ab` |
| [openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile/tasks.md](../archive/2026-10-18-define-first-installable-pbo-profile/tasks.md) | `f800328cae617670a7dd93a25aa320bc1f7870c1392637c278e20cfb7aa1ff03` |
| [openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile/validation.md](../archive/2026-10-18-define-first-installable-pbo-profile/validation.md) | `aa3f86b0eda9f223b3655eb08b76c1fd3e5d5b8a9ca64339a7b85dd5f625b655` |
| [openspec/changes/archive/2026-10-21-activate-reference-runtime-composition/proposal.md](../archive/2026-10-21-activate-reference-runtime-composition/proposal.md) | `36f763183d5c1538b345f73294f2b85ff208fd7a4ac9b882e3439ac6e898f37b` |
| [openspec/changes/archive/2026-10-21-activate-reference-runtime-composition/tasks.md](../archive/2026-10-21-activate-reference-runtime-composition/tasks.md) | `47df0a213f9bb3f3165795af417e6ea50bd7e729fb3a18c094ddbc93ae19e80e` |
| [openspec/changes/archive/2026-10-21-activate-reference-runtime-composition/VALIDATION.md](../archive/2026-10-21-activate-reference-runtime-composition/VALIDATION.md) | `ecc29e7d5654393634d1803c569a4745459bf6310a9316dd7d1510c8c7b3deff` |

## Tâche 2 — Sélection du profil et dépendances

La poursuite du change autorisée par le développeur sélectionne PA01 pour réalisation selon le canon et D1–D9. Cette sélection ne se limite plus à la préparation documentaire ; elle ne valide pas des opérations, privilèges, contrats ou mécanismes encore proposés.

### Périmètre initial sélectionné

- Première qualification PA01 : Debian/Linux et Docker local conformément à pixs-agent. Pour D3, conserver Debian 13 x86_64 physique et VM comme cibles distinctes et ajouter Docker local ; une preuve distincte est requise pour chaque profil. La VM conserve sa preuve de chaîne minimale ; la cible physique et Docker local n’ont pas de preuve de recette. Le LXC de test reste un profil distinct et ne vaut pas Docker ; les autres OS/architectures et profils LXC restent non qualifiés.
- CPython 3.14.9 avec GIL, Cython 3.3.0, liaison statique candidate ; distribution en répertoire, avec bin/, runtime/ et lib/. D7/D8 restent à qualifier dans le runtime distribué.
- La construction PA/PZT et leurs contrats restent séparés de PBO/PFO ; aucun Django/PostgreSQL embarqué comme autorité métier et aucun accès direct aux tables métier.

| Exécutable relatif | Gestion propriétaire | Modes admis par --mode obligatoire |
| --- | --- | --- |
| `bin/pixs-pa-system` | `pixs.agent` | `system-daemon` |
| `bin/pixs-pa-events` | `pixs.agent` | `system-start`, `system-stop` |
| `bin/pixs-pa-session` | `pixs.agent` | `session-start`, `session-stop`, `session-daemon` |
| `bin/pzt` | `pixs.pzt` | `pzt-daemon` |

D9 conserve un profil TOML fermé distinct des manifests PBO et un registre embarqué des seules opérations livrées. Le catalogue initial de PA01 a ensuite été sélectionné par le choix développeur 1 du 23 octobre 2026 : inspect_postgresql, prepare_postgresql et get_postgresql_result en version 1.0.0, sous gestion pixs.agent et mode system-daemon ; inspect_postgresql et get_postgresql_result sont Protégé, prepare_postgresql est Critique. Cette sélection corrige l’indication antérieure selon laquelle les noms C08 E2 restaient à choisir ; cette mention est historique et supersédée pour PA01. Elle n’atteste ni implémentation, ni qualification du runtime/ABI ou des dépendances, ni recette PostgreSQL ou effet réel. La répartition reste PA01/pixs.agent pour le plan technique et ses résultats durables, et C08 pour l’intention et la confirmation opérateur. Les formats détaillés B, le raccord au journal et les formats de retrait restent NON ADOPTÉS.

### Ressources, interfaces et dépendances

| Élément applicable | État et conséquence pour PA01 |
| --- | --- |
| C00 archivé | Profil PBO initial observé ; PA et réseau PZT non sélectionnés dans P0. La sélection PA01 ne les active pas dans P0. |
| C07 archivé | Socle hôte et contrats réutilisables dans leurs limites historiques ; aucune readiness P0 ou recette PA/PZT déduite. |
| Gestion pixs.agent/pixs.pzt | Manifests 0.1.0 et services/contrats présents ; leur présence ne remplace pas les quatre exécutants. |
| Chaîne / ABI / bibliothèques | Candidat exact et démonstrateur VM observés ; fermeture des dépendances distribuées et qualification physique encore requises. |
| Budgets | Les budgets effectifs sont fournis au runtime, conformément à BUILD §46.0 ; aucun budget général PA n’est inventé depuis les plafonds d’un auxiliaire. Leur admission et leur mesure précèdent les effets réels concernés. |
| Droits et identités | Aucun compte, privilège système, autorité métier ou permission supplémentaire sélectionné par cette tâche. Chaque rôle conserve son périmètre et ses contrôles. |
| Prébase / préparation PG | Conditionnelles au profil qui sélectionne ces effets. Le prébase est PLATFORM sans tenant_id/scope_id et indépendant de la base à préparer ; la gestion ordinaire attend PostgreSQL. Aucune variante ou opération C08 encore proposée n’est promue. |
| Communication | PBO–PA via PZT, y compris local ; aucun repli de proximité hors PZT. Transport, identité et politiques doivent être qualifiés avant utilisation. |

### Limites et passage à la conception

La tâche 2 confirme une sélection et l’état des dépendances ; elle ne prouve pas leur qualification fonctionnelle. Le catalogue concret, ses contrats/schémas et propriétaires ainsi que les mécanismes nécessaires non arrêtés doivent être résolus avant la réalisation correspondante, selon les tâches 3/4. Les cibles non qualifiées, les recettes R01–R68, les mesures et les contrôles physiques restent explicitement sans preuve. Aucun manque n’est converti en réussite.

Les exigences et sources de la tâche 1 restent applicables. Cette sélection ne lance ni code, construction, installation, préparation PostgreSQL, service ni activation réseau. Le contrôle de la sélection, la validation OpenSpec et le cochage élémentaire sont tracés séparément dans le checkpoint et tasks.md.


## Réalisation en cours — relevé du 23 octobre 2026

### Instruction de séquencement et portée des preuves

Le développeur a demandé de réaliser toutes les tâches, puis de procéder à la phase de tests et de validation dans un second lieu. Cette instruction explicite prévaut sur le séquencement antérieur pour ce change. La phase courante écrit les sources et leurs tests ; elle ne coche aucune nouvelle tâche. La tâche 1 conserve ses seules preuves historiques décrites plus haut. Les contrôles affectés par les évolutions devront être réexécutés en phase de validation. La réalisation complète reste ouverte.

Les mentions historiques ci-dessus indiquant un catalogue concret encore à arrêter sont dépassées par le choix 1 explicitement adopté : inspect_postgresql, prepare_postgresql et get_postgresql_result, contrats 1.0.0, propriétaire pixs.agent, mode system-daemon ; lectures Protégé, préparation Critique. Les décisions D1–D9 restent acquises.

Les choix complémentaires explicitement adoptés sont : E3 HTTP/JSON IPv4 loopback sous PZT, TLS 1.3 mutuel, terminaux ECDSA P-256 et suite fournie par l'opérateur, sans 0-RTT ; adaptateurs Cython OpenSSL 3 et libpq ; SQL local par socket Unix avec peer, compte système explicite et requirepeer ; plan technique PostgreSQL et résultats durables sous PA, intention et confirmation privées sous C08 ; clés initiales CA et terminaux non exportables matériellement, fournisseur terminal tpm2-openssl 1.3.0 candidat Debian 1.3.0-1 et pile TSS/gestionnaire de ressources à inventorier et qualifier. Aucune installation, connexion PostgreSQL actuelle, création de compte ou de clé, utilisation de clé, écriture TPM NV ni permission matérielle supplémentaire n'est autorisée par ces choix.

### Sources et recettes écrites, non testées

Le profil de build fermé, la CLI, le lanceur C isolé, le générateur de registre embarqué, les contrats PostgreSQL, le profil Unix/peer, le contexte OpenSSL privé, l'inspection libpq et le constructeur d'objets Cython ont été écrits avec leurs sources de tests. Le constructeur produit seulement des objets non qualifiés ; il ne livre pas les quatre exécutables, leur liaison ni leur distribution autonome. Les recettes natives restent des recettes non exécutées et leurs fixtures ne démontrent pas les comportements PA/PZT réels.

Aucun contrôle syntaxique, test unitaire ou natif, build produit, connexion SQL ou handshake TLS de ces nouvelles sources n'est exécuté par ce relevé. Une écriture native réussie prouve la présence du contenu, pas sa validité fonctionnelle. Les empreintes ci-dessous identifient le relevé ; les mandats, permissions natives, effets et libérations sont conservés au checkpoint du RUN.

| Fichier | SHA-256 au relevé | Mandat de dernière écriture enregistré |
| --- | --- | --- |
| src/pixs/pa_native/__init__.py | d1b384facf3ac8f022b080ce0b6df9632aa8fa851dca431e9ea3c197c4646c24 | req-1ddfdced09fd4e968b7770cc0860de34 |
| src/pixs/pa_native/build_profile.py | c2005ce9b770ce6ac5fb8a8c2f314368c678a1087085475bafeea5eeb8f0e8d0 | req-8f15d4a168254d83b1036f88a90a0473 |
| tests/unit/test_pa_native_build_profile.py | bcaf355f530920f0c70b52941cf98ba57c1c4dab614c0b302b1d282dd485f494 | req-ef0e2776ba504fe5bded95893466789e |
| src/pixs/pa_native/cli.py | 1b1ad266ccf1fa3295fcb5a208ebbad53b0fc1ac2a40169b6e1a410c87c1fafe | req-5c835e59f7e24ca99fbbb478b1cd3ee8 |
| tests/unit/test_pa_native_cli.py | 728f94181de5d2121e8174893ff3b915712ad4cd164f47fcac571829476afd2b | req-2a043d6db5d945f88dc6399501f2d74a |
| native/pa01/launcher.h | 90fdc80e4157f322baf2e08324287782019e981785d3790d3236c8df3beaf4a5 | req-bd83ab45cb6c4fada51d98158d71549e |
| native/pa01/launcher.c | 22a335a9c15f13e496b867b55038f73df115081f3c3d09e6f79211897cb77f49 | req-ffdd09268911421ea2da8368308e509e |
| src/pixs/pa_native/generator.py | a8c9e2c551d8d0085315d0e4359c81b643f4fb94813714d8343315bb13cadc9c | req-9323f3426c6344dab0cc666a1f83c609 |
| tests/unit/test_pa_native_generator.py | 8471b24f68adc75f54a11a08acad6f3ff9bdb2fcb2e93d120ed0e7fc203dc4ea | req-6f21bceb3e5d4efd9e61a8664f740246 |
| src/pixs/pa_native/postgresql_contracts.py | f8362a00aa666033b4c5978c492c9e9c7a190dc5336b982920dd6022f60fe79d | req-ac993c108fed44dbbfda5934ec2d2325 |
| tests/unit/test_pa_native_postgresql_contracts.py | 64879a469b14d7d6032bf9ea32796a7a40e5287557aec56b9ba7bdbecb07a7f3 | req-fa6372526ec74a8981d329ba31b386fa |
| src/pixs/pa_native/tls_context.pyx | e551a784616a2b31865d67d2fc2feaf39e49b9a647ced229f20f14487af33a7b | req-42bf5767bf4048dd911ff7d5f28fb89d |
| tests/native/test_tls_context.py | 29fee3412bca2b9f04c7a124c6378bc567e05e207779beb4547b076074cae962 | req-306e6e16f18c471da23bbd018ae43772 |
| tests/native/test_launcher.py | d24a2863ee4033b3e236a26f271aedcb7f850120f1639218a172dcc03eaf3545 | N/A |
| src/pixs/pa_native/postgresql_profile.py | a80280363730c35116d8b52e771b5f9cad205851887cfdc29f32028966bc438d | N/A |
| tests/unit/test_pa_native_postgresql_profile.py | 3ad71746a63da25f5e010c9b0ff036f18d3dacb6d5ff3e0906e99cb16239961e | N/A |
| src/pixs/pa_native/libpq_inspection.pyx | fca075d728373afac9dc58e88eacce5c908e941a5ede6ace27d8f1da2beef747 | N/A |
| tests/native/test_libpq_inspection.py | 5360d801559d49d0981df313e5ad833fcc0ae5b773d80594858b9abe62f07748 | N/A |
| src/pixs/pa_native/builder.py | a7d9966888fe44529fb1f21f74cc5112b5e532421cce843fa52a124b4f9c2be4 | N/A |
| tests/unit/test_pa_native_builder.py | 36706a3790a0a8b8c3e4fe32d0a1e20430cc8074cb71e52ab1cc49b21164a0ea | N/A |
| tests/native/test_object_builder.py | 577783e6fc1d565c470af709f8bc38d670e91598d9d2347024a0303210b025e1 | N/A |

### Inventaires effectivement exécutés, distincts des recettes

Les trois inventaires portent sur des métadonnées locales de paquets, en-têtes et bibliothèques ; ils ne qualifient ni dépendance complète ni comportement produit.

| Rapport sous output/cismp/cismp7-pixs-023c11510a274b19/qualification-pa01/ | Résultat observé | SHA-256 |
| --- | --- | --- |
| openssl-inventory-e3.json | OpenSSL 3.5.7 et bibliothèques ABI 3 présents ; aucune identité ni handshake | cebed7d73cb434f8a7eb38fdda3b4ae4342b2f732dc30ce21798687dd92179d5 |
| libpq-inventory.json | libpq5 17.11 présent ; libpq-dev, en-têtes et pg_config absents ; aucune connexion | e32ea84df3c47cc410b303ff45a1a80c3cffdd08047430e89f03c6be2f52812f |
| tpm2-terminal-inventory.json | Fournisseur tpm2-openssl, gestionnaire abrmd, TCTI tabrmd et en-têtes TSS absents sur cet hôte ; bibliothèques TSS présentes à distinguer des lignes de paquets virtuels non installés | d016d9d2a59395dcd7136f312a1881d47acb66f103fee6ab2e563d44b9bcebef |

Le développeur a fourni à titre informatif une sortie tpm2_getcap properties-fixed via device:/dev/tpmrm0 : famille 2.0, révision 1.38, fabricant INTC, chaîne fournisseur ADL, PCR_COUNT 24 et ACTIVE_SESSIONS_MAX 64. Cette sortie n'a pas été reproduite par PA01. Ces valeurs ne fixent ni budget applicatif, ni TCTI de production, ni preuve P-256/non-exportabilité, ni distinction physique/vTPM ou recette TLS.

### Contrats à fermer et réalisation restante

La coordination C08 confirme qu'aucun producteur/résolveur concret de mandat technique pré-PostgreSQL ni de confirmation autorisée de projection n'est encore adopté ou écrit. Les DTO privés R01, leurs SHA et fichiers ne donnent aucun droit PA ; l'autorisation ordinaire dépendante de PostgreSQL et l'identité mTLS ne remplacent pas l'admission prébase. Les handlers d'effet PostgreSQL restent fermés. La proposition commune doit arrêter propriétaire, liaison opérateur/cérémonie, cible et effets du plan confirmé, politique et révocation courantes, fraîcheur, rejeu et durabilité.

La coordination Z12 confirme que la représentation X509 terminale, notamment SAN/usages et le port de résolution du matériel courant, reste à arrêter. Le fournisseur TPM2 adopté ne résout pas ce manque. Le contexte TLS écrit ne charge pas encore de chaîne, clé, ancres ou socket et conserve ready_for_transport=False. Les exigences minimales de consommation et de refus ont été transmises aux propriétaires ; elles ne constituent ni adoption normative ni interface livrée.

Restent également la liaison et l'assemblage du runtime autonome, les quatre entrées réelles et leur lifecycle, le transport et l'admission courante, les handlers limités au service/rôle/base PostgreSQL, les états et résultats durables avec reprise/réconciliation, puis les recettes fonctionnelles et de sécurité R01–R68 applicables, la fermeture des dépendances, les mesures et les preuves physique/VM. Aucun substitut synthétique ne sera présenté comme ces preuves.

Les sources nouvelles n'ont pas de publication fonctionnelle validée. La publication documentaire antérieure de référence 70 ne couvre pas leurs écritures ultérieures. Le change n'est ni livré ni archivé ; aucun rapport STATISTIQUES.md d'archive n'est encore produit.


## Réalisation PA01 — état courant du 2026-10-23T15:23:52.423563+00:00

Phase 1 uniquement : réalisations et sources de tests, puis campagne distincte de tests/validation demandée par le développeur. Les empreintes ci-dessous rapprochent les effets natifs autorisés ; elles ne prouvent ni syntaxe, ni comportement ni qualification. Aucune nouvelle case n’est cochée.

### Instructions et décisions courantes

PLLM mode 1 maintenu sur fonds propres, même modèle opencode-go/muse-spark-1.3-contributor avec raisonnement high ; le développeur a explicitement demandé d’ignorer les quotas. Aucune bascule de compte/fournisseur, achat, injection de secret, modification du catalogue global, disposition ou redémarrage partagé. Les sondes auxiliaires mesurent seulement la session de codage, pas le produit.

D10–D12 sont validés directement par le développeur (call_12ea68b4889449f5a3e328e8071f3b6b/0–2) et inscrits dans design.md, contracts.md et tasks.md : NV_Extend SHA256/Cython-ESAPI ; séparation provisionnement/maintenance avec PLATFORMCREATE/POLICY_DELETE et autorité matérielle P256 indépendante ; usage par secret NV256bits confiné natif/FD protégé/HMAC-SHA256. Aucune opération matérielle actuelle autorisée. Le vrai gardien, les propriétaires initiaux/ordinaires, l’UTC fiable et la séparation effective restent à livrer/qualifier.

Le contrat E4 fixe document/signature_b64, 27 champs exacts, préfixe ASCII adopté suivi de LF et JSON canonique, PureEd25519 sans préhachage, branches des trois opérations et bindings acycliques. Le codec public AnchorSnapshot fixe 17 champs ; son Name SHA256, valeur NV et head du journal restent distincts. Les helpers ne résolvent aucune autorité et ne lisent ni TPM, journal, politique ou horloge.

La projection C08 courante a été relue sous accès CAB puis libérée : SHA d459f0532bce00397ea76c9ea72c9bcec66011044a16c36129967223cc2a1578. Refus du plan entier RECREATE/DATABASE_DROP et branche Docker non sélectionnée avant tout effet ; corrélations/causalités A07 complètes avec ordre et doublons conservés. Le nouveau chat C08 est recoupé avec son checkpoint et le registre ; ce fait ne qualifie aucun producteur ou transport. Z12 §13 D7/D8 SHA 96e18b2e00bcd901ed861fdb6c420a02e07b0736694def75fa1884d6fe829020 relu ; aucun resolver matériel positif ou chargement CA/terminal réputé disponible.

### Sources réellement écrites, non testées

26 fichiers suivis (13 de réalisation, 13 de tests), dont linker et bundler. Les quatorze unités du bundler, dix unités E4 et dix unités d’ancrage supplémentaires sont écrites ; aucune de ces sources n’a été exécutée. Le bundler assemble seulement une sortie neuve, copie les assets épinglés avec inventaire/modes/mtime/bornes/fsync et rapport local ; STAGED_UNQUALIFIED ne prouve pas runtime, fermeture de dépendances, reproductibilité ou SBOM signée.

| Fichier | SHA-256 courant | Dernier mandat de source |
| --- | --- | --- |
| native/pa01/launcher.c | 22a335a9c15f13e496b867b55038f73df115081f3c3d09e6f79211897cb77f49 | req-ffdd09268911421ea2da8368308e509e |
| native/pa01/launcher.h | 90fdc80e4157f322baf2e08324287782019e981785d3790d3236c8df3beaf4a5 | req-bd83ab45cb6c4fada51d98158d71549e |
| src/pixs/pa_native/__init__.py | d1b384facf3ac8f022b080ce0b6df9632aa8fa851dca431e9ea3c197c4646c24 | req-1ddfdced09fd4e968b7770cc0860de34 |
| src/pixs/pa_native/build_profile.py | c2005ce9b770ce6ac5fb8a8c2f314368c678a1087085475bafeea5eeb8f0e8d0 | req-8f15d4a168254d83b1036f88a90a0473 |
| src/pixs/pa_native/builder.py | a7d9966888fe44529fb1f21f74cc5112b5e532421cce843fa52a124b4f9c2be4 | N/A |
| src/pixs/pa_native/bundler.py | b1a92216365c3dcba3965c1a5fcf930f23efb4dbdc8631ee19f3d9cb768c1fcd | req-52caecf381d24874b89528335f643719 |
| src/pixs/pa_native/cli.py | 1b1ad266ccf1fa3295fcb5a208ebbad53b0fc1ac2a40169b6e1a410c87c1fafe | req-5c835e59f7e24ca99fbbb478b1cd3ee8 |
| src/pixs/pa_native/generator.py | a8c9e2c551d8d0085315d0e4359c81b643f4fb94813714d8343315bb13cadc9c | req-9323f3426c6344dab0cc666a1f83c609 |
| src/pixs/pa_native/libpq_inspection.pyx | fca075d728373afac9dc58e88eacce5c908e941a5ede6ace27d8f1da2beef747 | N/A |
| src/pixs/pa_native/linker.py | 5c1772abc22146c979314b259da99a218809c9c59cf20ccf9119d5109bfb96a5 | req-4cb23cb9549b4fa691f9e19c17790e3a |
| src/pixs/pa_native/postgresql_contracts.py | d8e3ed5d5a201e3761982d573e9516da533ded9256b00334b9ff2a4baa47d8fe | req-095241380def43a2960a3bb6df1b6e8a |
| src/pixs/pa_native/postgresql_profile.py | a80280363730c35116d8b52e771b5f9cad205851887cfdc29f32028966bc438d | N/A |
| src/pixs/pa_native/tls_context.pyx | a224438f2cbe655140219865fcb108ee0072e252688867583cfa47b0db0e71e9 | req-3eb989aa5740451f923f630d5f1bae70 |
| tests/native/test_launcher.py | d24a2863ee4033b3e236a26f271aedcb7f850120f1639218a172dcc03eaf3545 | N/A |
| tests/native/test_libpq_inspection.py | 5360d801559d49d0981df313e5ad833fcc0ae5b773d80594858b9abe62f07748 | N/A |
| tests/native/test_object_builder.py | 577783e6fc1d565c470af709f8bc38d670e91598d9d2347024a0303210b025e1 | N/A |
| tests/native/test_object_linker.py | 9ec7c75a5c8b2e6a45af3aea49cbc96e9dcd43be577986a541e47ed0f32c180c | req-b77a9a46e126421c9d880554e1e872e6 |
| tests/native/test_tls_context.py | 816b7611c5723dac26dfa04137013b9780d3f34b441060b1a4778ff88e8f567c | req-9c28bd7899c2409f84e5ce8b389e64f7 |
| tests/unit/test_pa_native_build_profile.py | bcaf355f530920f0c70b52941cf98ba57c1c4dab614c0b302b1d282dd485f494 | req-ef0e2776ba504fe5bded95893466789e |
| tests/unit/test_pa_native_builder.py | 36706a3790a0a8b8c3e4fe32d0a1e20430cc8074cb71e52ab1cc49b21164a0ea | N/A |
| tests/unit/test_pa_native_bundler.py | fee4df52abcd1b8957fcc852185970f807ab8a07cb049c412cf01014adc7f3fa | req-1699c18891b34c8195c5a0b6c713a364 |
| tests/unit/test_pa_native_cli.py | 728f94181de5d2121e8174893ff3b915712ad4cd164f47fcac571829476afd2b | req-2a043d6db5d945f88dc6399501f2d74a |
| tests/unit/test_pa_native_generator.py | 8471b24f68adc75f54a11a08acad6f3ff9bdb2fcb2e93d120ed0e7fc203dc4ea | req-6f21bceb3e5d4efd9e61a8664f740246 |
| tests/unit/test_pa_native_linker.py | e6141bdd44963e75f9dabaeeada0c06fbfc0ee5669577890cf8685e51b13d72d | req-f61d9bf1d1de4e329904e2e1d0338b4f |
| tests/unit/test_pa_native_postgresql_contracts.py | b9820c1ba69ee5dbc3d175bfbadfe9dc87eebb509b7743a9b0da0b732f923ac5 | req-06e628ea54744c1f8c0ab4fdf775200f |
| tests/unit/test_pa_native_postgresql_profile.py | 3ad71746a63da25f5e010c9b0ff036f18d3dacb6d5ff3e0906e99cb16239961e | N/A |

L’écriture initiale des unités du bundler req-9d342cc5d5994575b5adc9597a0dacfb a perdu une parenthèse : divergence d’empreinte connue, non acceptée. Correction littérale sous mandat neuf req-1699c18891b34c8195c5a0b6c713a364, même accès rattaché puis libéré, empreinte finale exacte. Aucun test/succès fonctionnel déduit de cette correction.

Le mandat des dix unités d’ancrage req-06e628ea54744c1f8c0ab4fdf775200f a été rapproché après attente d’enregistrement puis accès de lecture propre conservé : refus409 access-extension-while-held/run-not-quiescent compris dans les sources du contrôleur1.7.1, marqueur de job et ordre de clôture corrigés. Lecture libérée à vraie frontière native idle/READY, même décision non consommée et révisions inchangées, effet écrit une seule fois puis empreinte/RAPPORT_OC/READY et libération prouvés. Aucun rejeu de permission ou effet, aucun reset de session/service.

### Inventaire courant et limites de qualification

DEVOPS.md relevé 2026-10-23T13:59:37Z a été relu intégralement, SHA f6a519b4b0532cf938ad7e369d8f43d12ba9d55b83f929121d644daf6c6f3d3e. Debian13, Python3.14.9, OpenSSL3.5.7, clientPostgreSQL17.11 et serveur déclaré16.14 ; OpenCode installé déclaré1.19.4 tandis que l’API vivante observée reste healthy1.19.3. Ces observations ne sont ni installation ni qualification, et n’ont déclenché aucun redémarrage. Les précédents relevés datés sont historiques. Aucun accès à project.env, secret, certificat, TPM ou serveur PostgreSQL n’a été effectué pour cette reprise.

Les essais minimaux historiques CPython/Cython sur VM ne qualifient pas les nouveaux binaires, leur runtime distribué ou les dépendances TPM/libpq. Les headers/librairies/provider manquants dans les relevés antérieurs restent à inventorier et qualifier dans un environnement autorisé, sans installation hôte implicite. Les données TPM communiquées désignent l’hôte Pixs courant ; aucun laboratoire matériel distinct n’est identifié par ces données.

### Réalisation et preuves encore nécessaires

Restent notamment : adaptateur ESAPI privé/FD/HMAC et vrai propriétaire de garde/contexte ; registre durable avec ancrage, concurrence et réconciliation ; résolution actuelle de politiques/identités/temps/plans/préconditions/confirmations ; matériau terminal et transport TLS/PZT réels ; handlers et effets techniques PostgreSQL/service non destructifs ; quatre vraies entrées et sept modes/lifecycles ; graphes de headers et bibliothèques réellement fermés ; inventaires/provenance/licences et artefacts distribués reproductibles. Les sources de préparation ne livrent pas ces raccords.

La phase2 doit exécuter syntaxe et contrôles configurés, unités/négatifs, constructions/liens natifs réels, intégrations/reprises/mandats périmés, puis les recettes complètes applicables R01–R68 sur les cibles autorisées Debian 13 x86_64 physique, VM et Docker local ; les preuves restent distinctes par profil et le conteneur LXC ne remplace aucune de ces cibles. Le plan matériel exact et son autorisation restent distincts avant tout effet NV/clé/hiérarchie. Aucun PASS nouveau, livraison, archivage ou STATISTIQUES.md d’archive n’est déclaré. La tâche1 conserve sa preuve historique ; les neuf suivantes restent non cochées.


## Réalisation PA01 — instantané de sources du 2026-10-24T00:22:53.814446+00:00

Ce relevé complète les instantanés datés précédents, désormais historiques pour les fichiers modifiés. Phase 1 : sources seulement. 35 fichiers suivis : 16 de réalisation et 19 de tests. Le rapprochement des empreintes prouve la fidélité aux écritures autorisées, jamais syntaxe, comportement ou qualification. La tâche 1 conserve sa preuve historique ; aucune nouvelle case n’est cochée.

Les lecteurs natifs NV public/authentifié et leur nettoyage sont écrits, avec 34 méthodes de tests préparées et un conducteur ESAPI simulé. Le codec JournalTransition fermé et canonique est écrit, avec 24 méthodes de tests préparées. Aucun test n’est exécuté et aucun codec ou reçu local ne devient une autorité, une preuve d’ancrage ou un droit d’effet.

Le stockage natif nv_journal.pyx ouvre un journal préexistant, vérifie les fichiers et toute leur chaîne, conserve flock exclusif et prépare les ajouts avec fsync du fichier et du répertoire. Il refuse création/réparation automatique et tout nouvel ajout après tentative incertaine. Sa réalisation reste non compilée/non testée ; elle ne réalise ni NV_Extend ni confirmation TPM. Le module est réservé au seul binaire System, sans capsule/_api.h, par six modifications de construction/unités. Dix-sept méthodes de stockage et leur conducteur de pannes sont écrits, non exécutés ; le nominal futur utilise des fichiers/verrous/fsync réels, sans TPM. PA01_NV_JOURNAL_DRIVER désigne explicitement l’artefact de TEST sous output/tests/pa01-nv-journal, sans repli vers un artefact hôte. Ce n’est pas un paramètre réseau ou runtime. Le contrat détaillé figure dans contracts.md.

| Fichier suivi | SHA-256 rapproché | Identifiant de preuve native |
| --- | --- | --- |
| native/pa01/launcher.c | 22a335a9c15f13e496b867b55038f73df115081f3c3d09e6f79211897cb77f49 | prt_16821d2340013bexr8yEyV2Bwv |
| native/pa01/launcher.h | 90fdc80e4157f322baf2e08324287782019e981785d3790d3236c8df3beaf4a5 | prt_1682112a2001kxENshUCg0DTq6 |
| src/pixs/pa_native/__init__.py | d1b384facf3ac8f022b080ce0b6df9632aa8fa851dca431e9ea3c197c4646c24 | prt_168080af7001b0AHuvRYF9sLIN |
| src/pixs/pa_native/build_profile.py | c2005ce9b770ce6ac5fb8a8c2f314368c678a1087085475bafeea5eeb8f0e8d0 | prt_168087d57001coUlxqZUurZrVW |
| src/pixs/pa_native/builder.py | 7876fc67693f00522ffcfedad1b3142eb16af424004667bdc61abef6a217bd6d | prt_16b3c058f001lq5SXPXvwE0kAe |
| src/pixs/pa_native/bundler.py | b1a92216365c3dcba3965c1a5fcf930f23efb4dbdc8631ee19f3d9cb768c1fcd | prt_16939b547001CjFw0qN3Bw6rVn |
| src/pixs/pa_native/cli.py | 1b1ad266ccf1fa3295fcb5a208ebbad53b0fc1ac2a40169b6e1a410c87c1fafe | prt_16812f81f001ySbD35x36b1lpq |
| src/pixs/pa_native/generator.py | 0b545d45b9e45d521d8a7a3e7ce0e532816a73029354d6a372586abb1bb0df20 | prt_16b3c058f001lq5SXPXvwE0kAe |
| src/pixs/pa_native/libpq_inspection.pyx | fca075d728373afac9dc58e88eacce5c908e941a5ede6ace27d8f1da2beef747 | req-f34d1506c51d4681b06f16cdc24d029c |
| src/pixs/pa_native/linker.py | a1692414ad5601d859973c7abb9c44b63818c23a369c24a4485959caf4066844 | prt_16b3c058f001lq5SXPXvwE0kAe |
| src/pixs/pa_native/nv_anchor.pyx | c8823c75cccdecf81a30a024630e78b48ae6b2e18993abde63958cdf8b1f06db | prt_16ae2f0c80019xsJgALtAWpnAF |
| src/pixs/pa_native/nv_journal.pyx | ca8211f6bf5acc174c80830ace00b97c77e423a3d2079e08c2e4e97399ed56a5 | prt_16b3a5d39001qBgbCXnrtGWNtM |
| src/pixs/pa_native/nv_secret.pyx | 34563c02ed2d8c04d949c24199a5b275e5ee3ebad48dffd0084d979c5d9cf39c | prt_1696fd3850019dy2AaA6b6s2te |
| src/pixs/pa_native/postgresql_contracts.py | 137e6c110659a3fc1d85a72f499777bab2a15003fe06218552d0f54acae307fd | prt_16b296c6c001Sgo8TSD7zpcIOj |
| src/pixs/pa_native/postgresql_profile.py | a80280363730c35116d8b52e771b5f9cad205851887cfdc29f32028966bc438d | req-212d14aab837414e9b07b951d6cfa00b |
| src/pixs/pa_native/tls_context.pyx | a224438f2cbe655140219865fcb108ee0072e252688867583cfa47b0db0e71e9 | prt_168f1ece10018GeKDWseF4X3QY |
| tests/native/fixtures/nv_journal_driver.c | 44c48f87dbfbe2348398c2a8f2f8688b9941b001651023f583ea191146fdbcc2 | prt_16b3db78500174rvchlJANbXp3 |
| tests/native/fixtures/nv_public_driver.c | b6248ff2d52a80be6c4d5b0fb9eaed56a347b9004ca9217051e84142712e3b67 | prt_16af3f622001P4I8nKBQY0N07l |
| tests/native/test_launcher.py | d24a2863ee4033b3e236a26f271aedcb7f850120f1639218a172dcc03eaf3545 | req-e306e72d29ef4b9fa3a38cd56a629b4b |
| tests/native/test_libpq_inspection.py | 5360d801559d49d0981df313e5ad833fcc0ae5b773d80594858b9abe62f07748 | req-680c1c337b184476999bc5212deb7482 |
| tests/native/test_nv_anchor.py | 071f00daf0a2b42be3142cf4e28412f54a0dcf37cbb4d8ebe6c4d4085cabebf3 | prt_16af60463001WmZopHQWkhUsEB |
| tests/native/test_nv_journal.py | 7f22522a73692c89a63a450261c7e955781e40e7e4b5e8b8e242ed847742d672 | prt_16b3e7f1c001xE0Bvww94U9nxm |
| tests/native/test_nv_secret.py | 831dd4bd7353d0a6cd6de06e9dd74f34812d31349dc6f8faad763f43d83689ec | prt_169755111001hJEhniEangXTN4 |
| tests/native/test_object_builder.py | 0736825ea3f56c39e0d7c525e513b4bd7752a6133669eb245bcb73ea543afaf2 | prt_169ba86fb001rUqWrjytp43y9p |
| tests/native/test_object_linker.py | 9ec7c75a5c8b2e6a45af3aea49cbc96e9dcd43be577986a541e47ed0f32c180c | prt_168c43b81001rIkXy8sUCBA7ey |
| tests/native/test_tls_context.py | 816b7611c5723dac26dfa04137013b9780d3f34b441060b1a4778ff88e8f567c | prt_168f8559f001tNnPvUXzgwwtH3 |
| tests/unit/test_pa_native_build_profile.py | bcaf355f530920f0c70b52941cf98ba57c1c4dab614c0b302b1d282dd485f494 | prt_168098cfd001DEWSaaEE8xH4Z5 |
| tests/unit/test_pa_native_builder.py | 7551a730d9a3b9cd926989c58e1c31179a8230cc89cd8c2d413b8b110162604d | prt_16b3c058f001lq5SXPXvwE0kAe |
| tests/unit/test_pa_native_bundler.py | fee4df52abcd1b8957fcc852185970f807ab8a07cb049c412cf01014adc7f3fa | prt_1693ed72a001ZVCrKKwsv6jTjp |
| tests/unit/test_pa_native_cli.py | 728f94181de5d2121e8174893ff3b915712ad4cd164f47fcac571829476afd2b | prt_16813be27001iceRiQjs7K5kSs |
| tests/unit/test_pa_native_generator.py | 670959839b97fe66711786820f73021b27d6152ad585fa98c80d6352905133c5 | prt_16b3c058f001lq5SXPXvwE0kAe |
| tests/unit/test_pa_native_journal_contracts.py | f0d506b563ed4bd503685947b6fd015a484804835993da6c8795371dd22c82bf | prt_16b2d5799001OTDZcwBJT00X3a |
| tests/unit/test_pa_native_linker.py | 4375212d1a79853fc172d28933450aacca933a77198d9f6baad4d610d0196ccb | prt_16b3c058f001lq5SXPXvwE0kAe |
| tests/unit/test_pa_native_postgresql_contracts.py | b9820c1ba69ee5dbc3d175bfbadfe9dc87eebb509b7743a9b0da0b732f923ac5 | prt_1694e822f001uLP4XAWQZ5ASxK |
| tests/unit/test_pa_native_postgresql_profile.py | 3ad71746a63da25f5e010c9b0ff036f18d3dacb6d5ff3e0906e99cb16239961e | req-ae87be3f16824a5fb40d6f02096df295 |

### Réalisation et preuves encore nécessaires

Restent NV_Extend, confirmation authentifiée et réconciliation sans rejeu ; les vrais propriétaires d’admission, UTC fiable, garde/remise FD, contextes qualifiés, profils/politiques/confirmations/préconditions ; le matériel TLS et le transport PZT ; les handlers techniques PostgreSQL/service et résultats durables ; les quatre entrées et sept modes/lifecycles, puis fermeture des dépendances, inventaires/licences et artefacts reproductibles. Aucun propriétaire ou producteur absent n’est remplacé par un booléen ou DTO. La qualification des journaux, callbacks et mémoire de la pile TSS exacte reste exigée avant tout authValue.

La phase 2 doit exécuter syntaxe, contrôles configurés, unités/négatifs, constructions/liens natifs et intégrations/reprises, puis les recettes R01–R68 applicables sur physique/VM explicitement autorisés. Aucun accès SQL, écriture NV, usage de clé/secret matériel, installation ou redémarrage n’est réalisé par ces écritures. Les prévols CAB /usr/bin/true sont des contrôles du circuit, pas des tests produit. Aucun PASS, livraison, archivage ou STATISTIQUES.md d’archive nouveau n’est déclaré.


## Réalisation PA01 — sources rapprochées du 2026-10-24T11:10:20.866131+00:00

Ce relevé complète les instantanés antérieurs, historiques pour les fichiers modifiés. Phase 1 exclusivement : 39 fichiers suivis, 17 de réalisation et 22 de tests. Leurs 39 empreintes ont été rapprochées des écritures autorisées ; ce contrôle de fidélité ne vérifie pas la syntaxe ou le comportement. Aucun import produit, compilation, test, qualification, effet SQL/TPM ou installation n’a été exécuté. Aucune nouvelle case n’est cochée.

La garde TCTI et son couplage au lecteur ESAPI réel sont écrits, avec des sources de recette simulée. Les baux natifs NV/journal retiennent les ressources réellement ouvertes et refusent fermeture/append étrangers ; ils restent distincts de l’autorité et de l’intention sémantique. Le producteur nv_intent parcourt les vrais records et vérifie la chaîne canonique complète, le pin initial protégé, les contextes/séquences/liens/doublons et la valeur du lecteur authentifié, puis utilise le véritable append/fsync et recontrôle les snapshots. claim est consommé avant restitution ; l’état incertain conserve ses liens quand leur libération réelle est impossible. Le reçu ne produit ni mandat, ni permission, ni NV_Extend ou confirmation physique. Les contrats détaillés et leurs limites figurent dans contracts.md.

Le générateur/builder/linker réservent nv_intent au seul System, sans capsule/_api.h. La présence du module impose les cinq sources/noms compilés nv_intent, nv_anchor, nv_secret, nv_journal et postgresql_contracts avec appartenance à System ; les manquants, renommages et rôles étrangers sont refusés avant utilisation. Les contrôles déclaratifs ne qualifient pas la chaîne de compilation ou les imports réels. Les recettes nouvelles comprennent 26 méthodes TCTI/couplage/baux, 21 méthodes de stockage et 17 méthodes d’intention ; les cas natifs utilisent des IO réelles de fichiers et des simulations ESAPI/TCTI clairement séparées. Les sources unitaires de fermeture de graphe sont écrites. Aucune de ces méthodes n’est exécutée.

| Fichier concerné | SHA-256 rapproché | Preuve native d’écriture |
| --- | --- | --- |
| native/pa01/launcher.c | 22a335a9c15f13e496b867b55038f73df115081f3c3d09e6f79211897cb77f49 | prt_16821d2340013bexr8yEyV2Bwv |
| src/pixs/pa_native/nv_anchor.pyx | 5bb39ad08527bffcb81a734537067d04e8de03beecc2214df171464b4f01c3b2 | prt_16d4a389300112kGISjwzAQbIe |
| src/pixs/pa_native/nv_journal.pyx | eba9a469548e120a82f4073a9385bae451ce15c81da1770f33d68af8c7a38253 | prt_16d75f20f001SsQVA8P7EtJHnj |
| src/pixs/pa_native/nv_intent.pyx | 0d708d55771e8f91f2e7b430799b3ba1ac5e1bd9a49447bfa13e7641155cbbd0 | prt_16d88aae5001bAywKBpZJTUE8k |
| src/pixs/pa_native/generator.py | d35daee9af54412a4fcbb3f5ad7261fb48a7277707a9fdc6ab62099ab15de431 | prt_16d8e98e1001obbBUBHiDcWXV1 |
| src/pixs/pa_native/builder.py | b5e96d16835e05b3483a218f2755b89613060a8dfceafd8908954c99ca08e87c | prt_16d9232240012Oxy9IpT4lO4bA |
| src/pixs/pa_native/linker.py | 69c4a8a53f7e7cbb8e7425b11b4db3d01769d315841771046eb6ec16d6d6cdd5 | prt_16d93674f001gixzKNR7PEfUKC |
| tests/native/fixtures/nv_public_driver.c | 080d82aa11fd0958ba1f1d204031400b27a5214660e79e0a816852cbfe913cfb | prt_16d27a0fa001f1KXvRx9C280x0 |
| tests/native/fixtures/nv_intent_driver.c | f483509a4e08ba076645865128f851b2a9f22720cd8f253cf35abcac6be37a32 | prt_16d89b011001ziQdjCN0pNC7H5 |
| tests/native/test_tcti_guard.py | fc991f8ff1fbf02c06aefacdadbb86b927fd8475bd09ff6c3f9746cf7e56c489 | prt_16d7d84e4001KLF8tmBO2j9lJ1 |
| tests/native/test_nv_journal.py | f284c942aa4fd6c9f1df84aa7eddf54b3750b80298a3939a9db68bf42be3be9f | prt_16d7c168d001p2eWa6BCz7697V |
| tests/native/test_nv_intent.py | 49ee0fa2262db2a3404f87a3a12683c8488941c4f79539928de4633580652897 | prt_16d8d2a98001QhZfLGiWlRRvEP |
| tests/unit/test_pa_native_generator.py | 2c6d21963ba7a11ee0c615ad7f2f9ee031c85ebcbcb3a22d077f030b9a00d4f2 | prt_16d941f02001IJ4EAypxfXcO27 |
| tests/unit/test_pa_native_builder.py | 7bbdb6dd3cb538981cc2e223c41e33f095ea38b76249e461891a9a7557e9d88a | prt_16d94beff001xY6mXvNS3WpcjZ |
| tests/unit/test_pa_native_linker.py | 98256f35b2c97c5779756aad6f7e6a972a0fce096a207b23aecb0be21da1f9f3 | prt_16d955288001rPqQkJw2AT06g6 |

### Coordination et seconde phase

Les accords communs recoupés avec C08/Z12 sont conservés : E4 et responsabilités distinctes ; chrony/NTS time.cloudflare.com avec incertitude UTC ≤ 1 s, preuve âgée de ≤ 600 s et contrôles courants ; D14 libsystemd pour les observations natives et le raccord du temps vers mandat ET X509. D15 est propre au gardien PKI et ne vaut pas réalisation ou adoption d’un gardien/credential PA. Les identités, mandats, secrets, index et politiques PA/PKI restent séparés. Les checkpoints des deux RUNs ont été consultés en lecture seule ; aucune livraison de propriétaire positif n’en est déduite.

Le développeur maintient réalisation d’abord, puis tests/validation sur LXC. CT100 cismp est désigné ; son autorisation humaine générale couvre ses opérations internes sans nouveau vote, et ne couvre pas le TPM physique partagé ou les ressources hôte. L’identité SSH et l’accès TPM restent non établis dans PA01 ; CISMP6 centralise leur contrôle initial. Aucun effet sur ce conteneur n’est exécuté par le présent relevé.

Restent à réaliser : NV_Extend et confirmation HMAC courante, réconciliation sans rejeu ; propriétaires natifs réels d’admission, UTC/PKI/profils/politiques/confirmations/préconditions et garde/remise FD ; matériel TLS et transport PZT ; handlers PostgreSQL/service et résultats durables ; quatre entrées/sept modes et lifecycles. La qualification de la pile TSS/logging/mémoire avant authValue, la fermeture réelle des dépendances, les inventaires/licences, la reproductibilité et les recettes R01–R68 applicables restent obligatoires en seconde phase. Aucune réussite, livraison, archive ou clôture n’est déclarée.


## Complément de réalisation PA01 — 2026-10-24T11:37:36.489811+00:00

Toujours 39 fichiers suivis, sources non compilées/non testées, sans nouvelle coche. Les empreintes ci-dessous rapprochent les écritures natives réelles ; aucun contrôle syntaxique, import ou test produit n’est exécuté.

Le lecteur possède maintenant un serial interne incrémenté seulement après une nouvelle réponse HMAC NV_Read valide et ses contrôles réels. Le même owner C peut démarrer une nouvelle lecture dans le budget commun, avec nouveau nonce et session liée à usage unique ; aucune phase échouée/pendante/inconnue n’est réarmée. pa01_intent_confirm exige une observation de lecture postérieure ET la valeur NV attendue, avec même cible/Name/index/échéance et journal réellement relu inchangé. Un cache antérieur, le serial seul ou la modification d’une fixture ne suffit pas. Pour une intention dont l’ajout a été tenté, close n’annonce un succès opérationnel qu’après confirmation physique positive ; le détachement connu avant ancrage conserve IN_DOUBT. Ce mécanisme reste privé et ne crée aucune autorité ; NV_Extend et son consommateur C restent à réaliser.

La suite d’intention compte désormais 18 méthodes préparées, avec un scénario isolé qui appelle les vrais chemins C de nouvelle lecture/confirmation sur ESAPI simulé. Elle n’est pas exécutée et ne qualifie ni HMAC matériel ni TPM. La liste fermée des SONAME candidats est commune au linker/assembleur et inclut libsystemd.so.0 adopté en D14, avec les familles TSS déjà déclarées. Toute bibliothèque doit toujours être explicitement épinglée à l’inventaire ; son ELF et son SONAME réel sont contrôlés avant liaison. Le test unitaire ajouté prépare les refus d’inventaire absent et d’autres majeurs/SONAME étrangers. Les dépendances transitives, versions/ABI effectives et leur fermeture demeurent à qualifier.

| Fichier | SHA-256 rapproché | Preuve native |
| --- | --- | --- |
| src/pixs/pa_native/nv_anchor.pyx | cf9d59118fbabe3231359a53090e3efea71346a5ba14fe868aa837f12150e570 | prt_16da07890001xgesTLSEqlFJ2W |
| src/pixs/pa_native/nv_intent.pyx | fa83c21c8ecdeedb56cd20814f8e65eb219f4ff5697eb89a73a96cd360636072 | prt_16da12f07001Cf7np4PJqcjtp9 |
| tests/native/test_nv_intent.py | f4113f135824360cc688c6531a88138199afab3bc509850193bd7fbf2c8af8c0 | prt_16da212250019MVHoPwenkl7TX |
| src/pixs/pa_native/linker.py | 82a3db3865b93393c617f8b331645263af32d8bf6ba3cc55fc124151f27293a3 | prt_16dac348a001zJrxjroznsx5t6 |
| src/pixs/pa_native/bundler.py | 3085d64eb9b99adc3d5d2c28fd5091baccfcbf495c928921a61cd73237d6e219 | prt_16dacde95001djCQ5LGsdJgdSB |
| tests/unit/test_pa_native_linker.py | 378792da60b950c7f66127b2552a1531e81c10bc81c4d006ac86a2afb51fc018 | prt_16dad7bba0010B0dzhta7gAl4Z |

Les points de coordination destinés à CISMP1/CISMP6 ont été soumis au service de messagerie mais n’ont pas reçu de retour : livraison non confirmée, aucun renvoi aveugle. La source privée Z12 _launch_obs_sysd.pxi a été observée à SHA256 44324ac27710c108b7632f4e336d22da7fc3b14d1362e0bfc4de902f66b2596b ; elle concerne des faits SELF/PEER, sans admission complète ni import PA. Les accords communs sont conservés et ne sont pas soumis à un nouveau vote. Aucun effet LXC/SQL/TPM, installation, livraison, archivage ou clôture.


## Réalisation source PA01 — 2026-10-24T14:23:03.624910+00:00

Les 39 sources suivies (17 de réalisation, 22 de tests) ont leurs empreintes rapprochées des écritures natives autorisées. Ce contrôle de fidélité n’est pas une vérification de syntaxe ou de comportement. Aucun import produit, compilation, test, qualification, action SQL, lecture de secret actuel, clé ou écriture NV PA01 n’a été exécuté. Aucune nouvelle case n’est cochée.

Le consommateur NV_Extend opaque est écrit : nouvelle lecture HMAC avant effet, session liée à usage unique, commit séparé avec relecture réelle du journal, marquage avant l’unique Async, Finish unitaire et nouvelle lecture HMAC attendue avant confirmation. Les inconnus restent conservés, sans rejeu. Le nettoyage connu avant tentative est écrit : drainage sans nouveau Read, Flush de notre seule session dans le budget inchangé, fermeture locale des métadonnées consommées et détachement seulement sur fait C réel non-tentative/quiescence. Un détachement connu peut rendre IN_DOUBT avec sortie NULL ; le record durable demeure non ancré. Une issue encore possédée garde sa sortie. Reprise après crash/effet incertain avec nouveau contexte et autorité courante reste à réaliser.

Le graphe C cyclique impose les cinq modules nv_secret/nv_anchor/nv_journal/postgresql_contracts/nv_intent et leurs noms/headers explicites. Les chargeurs de recette initialisent les cinq modules et conservent leurs références. Le modèle ESAPI de TEST suit une valeur NV par contexte et un compteur d’applications, avec erreurs avant/après effet et réponse perdue. Les 26 méthodes d’intention et scénarios isolés sont seulement préparés ; ils ne qualifient ni HMAC/TPM réel, ni persistance/restauration/antirollback.

D13 PA est adopté et inscrit dans design/contracts/tasks : stockage dédié LoadCredentialEncrypted explicitement host+tpm2, garde/remise dans le lanceur System existant, sans cinquième exécutable/mode, secret partagé, repli ou PCR implicite. L’adaptateur natif de ressource pa01_nv_credential_open32 et ses cinq méthodes de recette sont écrits, non compilés/non testés : ouverture readonly/identité/protection/anti-substitution/délai, aucun octet de credential lu par cet adaptateur. Cela ne livre pas encore le propriétaire D14/politique/fournisseur ou l’intégration positive du lanceur. Les fichiers documentaires sont classés séparément de l’inventaire des 39 sources ; aucune empreinte documentaire n’est un test produit.

| Source | SHA-256 rapproché | Preuve native |
| --- | --- | --- |
| src/pixs/pa_native/nv_anchor.pyx | c283e562b8d7e09299b49f01166299f28982fc9354b3d09a20163608ef10e03e | prt_16e2444f1001VDXrKR2Z3HxKUn |
| src/pixs/pa_native/nv_intent.pyx | c53d39e91f0f54ff39cadc289599520cf25397b9cfbda8a49b959bab6fa58a01 | prt_16e24f064001c95vN2oSKM96ZM |
| src/pixs/pa_native/nv_secret.pyx | 05bb3224b3af53cf6dff3f1b5cd055561c8ba68e9f96efa2c2f1f80a5f7120e8 | prt_16e47bc76001hsaS2AsUonw136 |
| src/pixs/pa_native/generator.py | 37d5d261c89293b9e8bae06c1a6bf50851a7113be6b4c33e8d37a3e1a93e1ac2 | prt_16e0d48ed001hXt4A4Vf9D4ktd |
| tests/native/fixtures/nv_public_driver.c | 4d95382697e1b56178f7fa86129824008ab0360acd8c0ac14c1efa2ebb106d55 | prt_16dcc0157001t8e0ISAixKq5br |
| tests/native/fixtures/nv_intent_driver.c | 49beb0b45a7d7d24c473f494d95affc45a5131b187d6328938ddf10fe1a854e3 | prt_16dccc300001ifPh7gjOEZzPJj |
| tests/native/test_nv_anchor.py | 6363bb2fd05eaf56923d71f19f12a9d1cec5d98df43b41d06e6e501b4fd1fe78 | prt_16e0f4c27001OTRFaBL2Se8VhO |
| tests/native/test_nv_intent.py | d1b6c6287f2a619e4071533f0888c0b471f0186452431f31837b1cb7b4ca34d8 | prt_16e25a67a001jg2sg3Rs7Ksc3v |
| tests/native/test_nv_secret.py | 9b1c094c75736c47b87c701e1bae517d4432e9fe3424ffbe0694ecd39f1f1b81 | prt_16e48972100143gp0Aum3vIqZS |

### Preuve d’accès CT100 et coordination

Le contrôle externe du 24 octobre 2026, chat Diagnostiquer le démarrage LXC 01a16cf2-4b5b-7813-94b5-5fc02ee28a8c, chunk f95e57 exit0, confirme SSH root@10.0.0.1:22, hostname cismp, UID0, /dev/tpmrm0 caractère 0600 root et lecture properties-fixed rc0 du TPM2.0 Intel/INTC, firmware 0x2580012/0x0. /dev/tpm0 est absent. La preuve remplace les erreurs SSH/absence TPM historiques et n’est pas rejouée. Elle est enregistrée puis relayée dans le même SID : message msg_16e17e7970017s3uObxneafCdg et ACK msg_16e17e838001Iz4YCEnVPskwNk. Aucune qualification PA/PKI/PZT ou permission d’effet n’est déduite ; le TPM physique est partagé et non restauré par snapshot.

Le défaut partagé /mcp499 puis refus TCP4096 a été recoupé avec C08/Z12. Le retour health1.19.4, MCPconnected et readiness natif READY instance inst-670877a4dd774fe6b1e9c0e0e3d36730 a été observé. Aucun démarrage/redémarrage/dispose/reconnexion partagée n’a été effectué par PA01. Un prévol once /usr/bin/true réel a précédé les écritures ; il contrôle CAB, pas le produit. Le transport synchrone /message en thread local est observé, même modèle/session, sans modification du service ou des autorisations fonctionnelles.

### Réalisation encore nécessaire

Restent propriétaires positifs d’admission/politique/UTC/garde et contexte qualifié, matériel TLS/résolveur/transport PZT, handlers service/rôle/base et résultats durables, quatre entrées/sept modes et lifecycles, inventaires/fermeture réelle/reproductibilité. C08 déclare non livrés projection autorisée, confirmation opérateur et mandat E4 signé avant PG. Le raccord de publication de projection et production/retour du plan avant signature est un manque de contrat conjoint : les trois opérations actuelles ne fournissent aucun port implicite ; aucune opération supplémentaire ou partage de fichiers n’est adopté par une suggestion. Z12 ne livre pas encore de propriétaire D14/UTC/politique/résolveur TLS/guardian complet partagé ; ses primitives privées ne le remplacent pas. Les tests et la validation restent en seconde phase LXC ; aucun PASS, livraison, archivage ou clôture.


## Réalisation source — prêt TLS et observation NV après crash

Le port privé INITIAL_MATERIAL de tls_context.pyx est écrit (preuve prt_16e9c8934001AwifD8s5UXXxgS), ainsi que son conducteur de TEST (prt_16e9dd4d4001S7FkdT7YYxtc3W) et ses 10 méthodes de recette (prt_16e9ebacd0015LjRrRnQ4RpUiZ). Il conserve le vrai couple de contextes OpenSSL et une référence forte, scope propriétaire/opération/côté/usage/PID/thread/délai, retrait et exclusivité. Aucun export public/capsule n’ouvre ce port. Son client concret Z12, le cleanup/transfert effectif et la durée de vie de futurs SSL restent à raccorder ; aucun port intégré/qualifié n’est revendiqué.

Les contrats correspondants et ceux de l’observation NV sont écrits (prt_16eaaae6f001f7mJUykMnRIgJ3). nv_intent.pyx écrit l’observateur distinct start/step/snapshot/close (prt_16eac864a0011RTV0KBURk9Wcx) : nouvelle lecture HMAC réelle et serial postérieur, scanner canonique partagé, scope réel et relectures avant publication, classes HEAD_MATCH/TAIL_UNANCHORED/DIVERGED, sorties fermées, premier échec conservé et détachement quiescent réel. Aucun append, Extend, rejeu, ancien contexte déclaré quiescent, droit d’effet ou résultat PG n’est déduit. La reprise positive sous nouveau contexte et autorité courante reste donc incomplète.

Douze méthodes de recette d’observation sont écrites dans test_nv_intent.py (prt_16eadb6d4001ZGmNK6nf8J7tQ7), qui contient désormais 38 méthodes au total. Elles préparent lecture HMAC supplémentaire, tête/queue/divergence, forme canonique/pin/contexte/séquence, séquence initiale différente de1, cleanup pendant, refus par le consommateur d’extension, échéances distinctes et séparation des capacités. Elles utilisent IO de fixtures publiques et ESAPI/TCTI simulés ; aucun résultat matériel n’en découle.

Le rapprochement des empreintes couvre 41 sources suivies (17 de réalisation et24 de tests), sans divergence observée. Ce contrôle de fidélité ne vérifie pas la syntaxe ni le comportement. Les candidats initiaux refusés et les corrections de revue restent au checkpoint ; aucune revue statique n’est présentée comme compilation ou test.

L’erreur fournisseur HTTP400 avant outil du 24octobre a été réconciliée sans enregistrement de demande native ni effet pour req-c536e6828bab49f38310d35980c61387. La compaction dans le même SID est prouvée (msg_16e999650001WIFDVZHwdSYFGr), puis broker READY/pending0 (prt_16e9aeee1001z9HKg4TZHSlFdA) et nouveau prévol exact /usr/bin/true (req-62c7c7290bf947cebcd2c9301e53ab57, prt_16e9bae7100131iAnBnkylxeNl). Aucun redémarrage, dispose, changement de modèle ou contrôle de quota n’a été effectué. La sonde statistique auxiliaire ses_e915bea24ffeknZoEhZ614HvOG est terminée, contenu valide, TTMT visible3.004s, débit N/A faute de sémantique de comptage qualifiée ; ce n’est ni un test produit ni une qualification PLLM actuelle.

Restent notamment propriétaires positifs D14/politique/UTC/garde, client matière TLS et transport PZT, raccord adopté de publication/retour du plan avant signature (proposition1.1 portée par C08, adoption humaine encore attendue), handlers PostgreSQL/résultats durables, reprise positive et quatre entrées/sept modes complets, fermeture/inventaires/reproductibilité. D13 PA reste adopté : le FD ressource seul ne livre pas le guardian. Les tests, vérifications syntaxiques, compilation et validation restent en seconde phase LXC. Aucune coche, livraison, archivage ou clôture.


## D14 PA — collecteur SELF/PEER et raccord de construction, sources seules

Le module privé systemd_observation.pyx est écrit, avec son conducteur SDK simulé et17 méthodes de recette. Les fonctions C open/snapshot/close conservent une référence propre du vrai sd_bus et les pidfds, relisent les faits processus/socket/credentials non augmentés et leurs liaisons, protègent longueur de sortie et budget monotone, conservent le premier échec et distinguent le nettoyage. Aucun numéro de FD/pointeur SDK ou secret n’est retourné à Python. Le code n’ouvre pas de bus implicite ou endpoint et n’effectue pas de RPC. Les rejets après fork précèdent tout SDK ; l’usage du bus reste exclusif au propriétaire natif du graphe fermé.

Le constructeur et le générateur réservent cette source à System et refusent les headers _api.h ; -D_GNU_SOURCE=1 est choisi explicitement pour cet objet seul. Les recettes unitaires de rôle/capsule et la recette native de sélection du flag sont adaptées. Le conducteur de TEST utilisera des objets SDK simulés et des sockets/pidfds locaux lors de sa future exécution : aucun daemon/credential réel, aucune recette actuelle. Ses17 cas préparent formes/lifetime, longueur trop petite, erreurs SDK avec sorties allouées, masque/augmentation, incohérences, horloge/expiration/régression, socket remplacé, cleanup EINTR, thread/fork et absence de capsule. Le premier candidat refusé et la correction du statut sticky restent au checkpoint ; une revue statique n’est pas une compilation.

Le close conserve le premier statut d’échec et son diagnostic même après consommation connue des ressources ; une sortie NULL décrit seulement cette consommation. EUID pair reste AT_CONNECT, sans prétendre observer son EUID actuel. Aucun manager/unité/MainPID/InvocationID, artefact chargé, politique/époque/cible, UTC ou guardian D13 n’est prouvé par ces seuls faits. Leurs raccords et leur admission positive restent à réaliser.

| Source | SHA-256 rapproché | Preuve native |
| --- | --- | --- |
| src/pixs/pa_native/systemd_observation.pyx | 52266be788f27183aed8f04d42ec63ab8c1a76c74390c52b3fa629c968069589 | prt_16ec87e08001jDWiN8wKyMphxV |
| tests/native/fixtures/systemd_observation_driver.c | 93c42a4fd8d3b4b1360ee2ac42760b0d4c4d12729046092fee7fb890d054dd94 | prt_16ec95673001Fb4FJHJ2rrPNUH |
| tests/native/test_systemd_observation.py | d34646ac5e6d55e8b83f50f81b443defdbe51c1daa53276ee15309137b853522 | prt_16eca539b001hHyFCVU6tXgP4c |
| src/pixs/pa_native/builder.py | cf2cf02a6062ab9c30cb4d71d4cf8cbf25d8e765d013c32c2cc169ef174d2012 | prt_16ecb2c68001Lp5nMeLZ2NAw6y |
| src/pixs/pa_native/generator.py | 56abe76e5317ecc21dfd8799ae68c96e7b3bc487eb5b978a478dd3f24f1c1d82 | prt_16ecbbff7001JrRdaluL4xuJFd |
| tests/unit/test_pa_native_builder.py | f2e215b78ec0d2a203bd5d8c901960c9cb4dedbd1a7863faeff242344e08a6d7 | prt_16ecd539e001y6tg8oYYn8YMDW |
| tests/unit/test_pa_native_generator.py | a283d968d41fdc42342038f252860189895f8d2147edc707fe8fa13dfc6db31e | prt_16ece386b001QHhP3ZTUeo64E7 |
| tests/native/test_object_builder.py | 51c6634a907c2e36d6d72e4d35d3bb4494e3d6cae124fa4e5f1d714e6bb4682b | prt_16ecef50f001aJp9K9e7hjtBgt |

Tous les accès des huit écritures sont RELEASED. Le rapprochement courant porte44 sources,18 de réalisation et26 de tests, sans divergence observée. Les append documentaires sont indexés séparément à partir de leur dernière preuve native ; leurs empreintes ne sont ni compilation ni validation technique. Aucun contrôle de syntaxe produit, import/compilation/test, installation hôte, connexion SQL, lecture de secret actuel, clé ou effet TPM/NV PA n’a été exécuté. Les cases restent inchangées et la seconde phase reste le LXC.

La coordination distingue D13 PA adopté (secret usage NV dédié host+tpm2) et D16 Z12 encore en attente (autorisations des clés CA/terminales et lot documentaire propre). Aucune adoption D16 n’est inférée de D13. La proposition commune PZT1.1 de retour du plan avant signature reste portée par C08 ; aucun port1.1 ou nouvelle autorité n’est réalisé implicitement. Restent aussi transport/client matière TLS, propriétaires courants et garde/remise, handlers/résultats PostgreSQL, reprise positive, quatre entrées/sept modes complets et fermeture/inventaires/reproductibilité avant qualification/livraison.


## Connexion D14 propre — état source et correction de fidélité

Le client C start/step/snapshot/close et les familles OBS/CONN sont écrits dans systemd_observation.pyx. Le socket et le sd_bus propres, le transfert FD immédiat, la progression unitaire et les relectures de la fille restent non compilés/non testés. Les deux fichiers de recette sont écrits ; test_systemd_observation.py comporte31 méthodes, dont14 nouvelles pour la connexion. Elles simulent le SDK et ne qualifient pas un manager réel.

| Source | SHA-256 rapproché | Preuve native |
| --- | --- | --- |
| src/pixs/pa_native/systemd_observation.pyx | 59e4eb1cc21833c74e8f6861f6a75812f6cde2b1c9c6815c0a472e7d43ee2211 | prt_16f1d5c050012ALlrZV15O9Yku |
| tests/native/fixtures/systemd_observation_driver.c | 8eb99249b2f29dae81e625eafaf888fcc2b8038c79417f936704cf0e637b4744 | prt_16f29d615001ax6jAiuAY2nBfN |
| tests/native/test_systemd_observation.py | 59eddec6e54b0af8d8bfb86a317b99782a8924ca5cb847b1a352c5bb4e7e41e4 | prt_16f2a5396001h9pJ2jZOQzTNdP |

Le premier write du conducteur avait inversé un booléen de test exit_on_disconnect0 vers1. La comparaison d’empreinte l’a refusé ; l’effet exact a été conservé et son accès libéré RECONCILED. La correction ultérieure restitue les octets autorisés8eb99249b2f29dae81e625eafaf888fcc2b8038c79417f936704cf0e637b4744, sans qualification de ce code. Les contenus prérevus du checkpoint ont servi uniquement de transport de bytes, vérifiés par digest fixe avant écriture et après relecture, sans devenir une autorité fonctionnelle. Les commandes courtes déclarent cible/lecture du checkpoint/toolchain sous once et HELD ; aucune transcription libre de code n’est acceptée.

Deux récupérations techniques restent tracées dans le même RUN/job : prévol access_id null refusé avant effet, puis commande de recette tronquée refusée avant effet. Les candidatures ont passé leur seul /usr/bin/true exact et les contrôles de contexte/permissions/readiness ; aucun service partagé, quota ou état fonctionnel n’a été réinitialisé. Session native active ses_e90de5a12ffe3s9O9hAy1YO1M1, prévol req-6f9b587a866442ea916ab03c4cce7733, preuve prt_16f223995001eMxiWD2VFsOYzi, gateOPEN et critères/strictCommands conservés. Une erreur de format MCP commands-chaîne au lieu de liste avait été refusée-32602 avant enregistrement ; elle n’est pas un effet ni une preuve produit.

Le rapprochement courant couvre44 sources (18réalisation/26tests), sans divergence. Aucun import produit, syntaxe/compilation/test ou qualification, secret actuel, clé/TPM/NV ou SQL n’a été exécuté. Les deux contrôles /usr/bin/true sont des prévols CAB uniquement. Manager/unité/MainPID/InvocationID, artefacts, politique/UTC/garde D13, client matière/transport PZT, handlers/résultats et lifecycles restent à compléter. Le raccord PZT1.1 proposé dans C08 et D16 Z12 restent sans adoption déduite de D13 PA. Les tests/validations restent en seconde phase LXC, aucune coche ou livraison.


## Point de reprise normative — retour de plan avant signature

Audit natif lecture seule msg_16f3302e4001sR7cZQUKGGyLW3, corrigé par CGPT sur un point : la projection/son codec1.0 déjà adopté dans C08 ne sont pas niés. Le manque concerne leur transport et la production/retour de l’observation et du plan AVANT signature/confirmation. postgresql_contracts.py20–24 conserve inspect params{}, prepare tripletplan et get_result opération ;68–101 retourne références/triplet,109–140 représente TechnicalPlan sans port de retour du document. Les DTO ne sont pas un producteur ou une autorité.

CISMP1 a confirmé directement que le lot documentaire PA/PZT1.1 commun reste en attente de la décision humaine déjà posée dans son chat. Le choix n’est pas déduit de D13NV, des avis de coordination ou d’un silence. Une quatrième opération, un DryRunCritique ou un partage fichier contournerait le catalogue adopté. L’absence de ce raccord empêche l’achèvement conforme du chemin principal et des tâches4–6 ; ce constat ne prétend pas que les autres réalisations seraient terminées.

Le code indépendant D14 collecteur/connexion est écrit et ses31 recettes fidèles ;44 sources18réalisation/26tests restent non compilées/non testées. Le point de tâches est écrit sous prt_16f34bccc001YIS1TLTbMh3COr, sans nouvelle coche. Les propositions RPC/unité suivantes sont restées candidates et n’ont produit aucune écriture de helper mort ou capacité UNIT factice. Restent D14manager/unité/artefacts/politique/UTC/garde, client matériel/transportTLS-PZT, handlers/résultats PostgreSQL, reprise positive, entrées/lifecycles et inventaires/fermeture. D16clésZ12 reste distinct de D13NVPA adopté.

Le prochain jalon dépendant est la décision explicite sur le lot commun1.1, sa transcription coordonnée puis les réalisations restantes. La question demeure chez CISMP1, sans duplication. Le prompt CISMP impose une REPRISE face à une absence de spécification empêchant une implémentation conforme ; une décision développeur indispensable est une condition terminale de blocage. Les récupérations techniques ont réussi ; elles ne sont pas la cause de ce point de reprise. Aucun test produit, contrôle syntaxique, compilation, secret actuel, clé, TPM/NV, SQL, livraison ou archivage n’est revendiqué. Le LXC est accessible selon la preuve déjà relayée ; ce n’est pas une absence d’autorisation du LXC.


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

### Provenance et état de reprise

La réponse humaine directe est reliée au chat CISMP1
01a16914-17c7-7971-8e8b-294cc3bc96e9, question_item_id
["request_user_input_async","call_0ef16343f01847f698d3411cb89b5cd3",0],
réponse « Valider le lot documentaire commun ». CGPT l'a recoupée sur le
message humain natif, distinct d'une délégation ou d'un checkpoint seul.
Elle autorise ce lot documentaire, aucun effet d'infrastructure ou produit.

Les revues C08/PA ont séparé les tableaux de chaque invocation réelle,
confirmé le bundle C08 seul et les versions, ajouté les preuves temporelles
et techniques, les cinq ressources et les gardes par phase. Les empreintes
des quatre bases et les diffs sont conservés dans le checkpoint PA01.
Les 13 fichiers C08 sont suivis par CISMP1 ; ce document ne déclare pas leur
écriture ni la validation globale du lot avant preuves conjointes.

44 sources suivies (18 réalisation, 26 tests) restent non compilées/non
testées, dont connexion D14 et 31 méthodes de recettes D14. Les historiques
de blocage et contrôles techniques antérieurs restent des faits datés,
pas un blocage humain E5 actuel ni une preuve fonctionnelle actuelle.

DEVOPS régénéré 2026-10-24T21:55:22Z relu : autorisations explicites des
agents/orchestrateurs pour les tests root dédiés Docker/LXC ; les tests
produit restent différés au LXC par l'instruction actuelle. La preuve
d'accès TPM ne qualifie pas les clés, l'ancre ou le transport.

Aucun code 1.1, syntaxe/compilation/import/test produit, connexion PostgreSQL,
secret actuel, clé/NV, modification hôte, Git, livraison ou archive n'est
revendiqué. D13 NV PA reste distinct du profil D16 de clés adopté chez Z12,
dont transcription/qualification et propriétaires réels sont séparés.


## D14 lookup — preuves sources seules, recettes préparées

| Source | SHA-256 rapproché | Preuve native |
| --- | --- | --- |
| src/pixs/pa_native/systemd_observation.pyx | 2990f13493271c9e78301732978814fcb09b175b9a24a8663b2e6603f2db62fe | prt_1706d563e001wzfYDDvEhGdWUg |
| tests/native/fixtures/systemd_observation_driver.c | be08c88696a5eac6cc5570491dff5fefd19c18c61bff86d63bd99ca07742908d | prt_1706dc643001zphAqvkzDAjzrl |
| tests/native/test_systemd_observation.py | 0e497cd25b92b3c8e94f0d95439b31b82dc1ebefc2968a00b674f202dfaa5acf | prt_1706e511d001kSO16rpUE4xvCn |

44 fichiers suivis sans dérive, accès RELEASED. 45 méthodes préparées au total, dont 14 nouvelles, aucun import produit, aucune exécution/réussite de ces recettes revendiquée. Contrat unité/InvocationID seuls ; manager/MainPID/artefacts/politique/UTC/gardien D13/autorité absents. M1 Z12 sans adoption.


## Principe B — preuve d'adoption sans produit
Preuve humaine B + lot 4 docs reçue (« Je valide »). Propositions wire V1-V5 refusées avant effets car cycles, champs non fermés et retraits inventés, sans les reproduire ici. Aucun produit B qualifié. 44 sources suivies sans dérive, aucune exécution produit, aucun test maintenant.


## Adoption retrait — preuve documentaire sans effet produit
Décision `call_f6bf98fe745b4104aa31c80d87a860b7/0` : principe et lot 12 retenus. Lot PA4 ce RUN et lot C08 `proposal.md`, `design.md`, `requirements.md`, `tasks.md` plus deltas `specs/authorization/spec.md`, `specs/pixs-agent/spec.md`, `specs/pzt/spec.md`, `specs/installation-provisioning/spec.md` du change `add-installation-and-first-configuration`, canon audité seul. Dans la branche INITIALE après retrait : nouvelles préparations interdites ; inspection et réconciliation courantes permises selon droits, remise minimale PBO conservée ; management ordinaire seulement après vraies preuves. Recettes : préconditions rapprochées, mandat Critique dédié consommé une fois, ancrage vérifié, preuves des retraits PA et Z12 avec D8 courant si utilisé avant management global. Aucun test ni build produit exécuté.


## D14 MainPID — preuves sources seules, recettes préparées

| Source | SHA-256 rapproché | Preuve native |
| --- | --- | --- |
| src/pixs/pa_native/systemd_observation.pyx | 5eab03f5db581f66814911f933458d14bba329d01119c5d5335781a147e1d787 | prt_174c9aa16001ZtiSNi4I5kW0Td |
| tests/native/fixtures/systemd_observation_driver.c | b3c21cc93d0d0a35e43b12203934a5d82b9e2e69ac3330b61a482feb4fb9d562 | prt_174d52c90001Go22aqfrJwftFr |
| tests/native/test_systemd_observation.py | 7511e5082aa32a3d5fb05e8fdaa6e3793efaa92064b86f5b9e96c7c9569edf14 | prt_174e508dd0017FJKcldAis2c0j |

46 fichiers suivis sans dérive (19 réalisation, 27 tests), accès RELEASED. 54 méthodes préparées au total (45 conservées + 9 MainPID), aucun import produit, aucune exécution/réussite revendiquée. 5 RPC readonly, baux parents, correctif variant, assertions d'ordre préparées, PID vivant/mort, SDK/types/temps/propriétaire, assertions de nettoyage préparées. Mocks sans qualification manager/identité/artefacts/politique/UTC/garde D13 ni SQL/NV ; raccords et lifecycle à finir. Admin écrit séparément sans qualification. CAB 1.10.1 même RUN/version 1200, prévol true exit 0. D18 décision humaine vérifiée dans le chat Z12, pas une source UTC extérieure qualifiée ; strict Z12 seulement annoncé par son RUN, sans UTC/matière déduite. Étape IMPLEMENTATION, archive non faite.


## Composition admin/import — preuves sources seules, tests préparés

| Source | SHA-256 | Requête | Preuve | Statut |
| --- | --- | --- | --- | --- |
| src/pixs/pa_native/generator.py | 860f50b11da907971406b02dfc3af9998ef996ca753818929f88b103c91af2a1 | req-4220fe9db63d4c08b4d8fd76f524590e | prt_174ff0e040014sG5TxDl2dJjHV | ÉCRIT_NON_TESTÉ |
| src/pixs/pa_native/builder.py | ec64ed8ec3f7cd86c2a6dacfe3a6dfce6b0a283d58f0acdf21dcb438b0a5bd95 | req-7846f59c7e2346e3a9205993157868cc | prt_174ff807b001TRBq2dLySZEeiW | ÉCRIT_NON_TESTÉ |
| src/pixs/pa_native/admin_withdrawal_contracts.py | c325ae98a0dd8ff81fd2ccb4598e93c9a8706be45aa663af24b526d64fed7418 | req-0e6e153f87ca4bed9b29df0992f84bbe | prt_174fff615001Q34H3Ox8xcpx9e | ÉCRIT_NON_TESTÉ |
| tests/unit/test_pa_native_generator.py | a2e8dcb15c1ee39a29b0ef56f5065e205c7abfdcfee15eca3b99181f55977798 | req-11f49dd1f1994878bbb2ebedfa602e89 | prt_1750063b0001L5auqn7AauE2Ky | ÉCRIT_NON_TESTÉ |
| tests/unit/test_pa_native_builder.py | a08dd9dd2c431597cc58550f31951e62b3e84e6ff95399da9c308f4aefabac12 | req-2b0f7780857140b386ba4adfd5f43989 | prt_17500cbce001e1NA3fCHhlHmN3 | ÉCRIT_NON_TESTÉ |
| tests/unit/test_pa_admin_withdrawal_contracts.py | 94fc37edb81e012fe1f9e21262fc0524acecb25786e7ac722fbf8580bff48637 | req-56cbf46ccb8c4a5c917a4ebeda127ff4 | prt_175014ba9001Ur6secVs7rwCz2 | ÉCRIT_NON_TESTÉ |
| src/pixs/pa_native/linker.py | 7461f9a6dc1a034d74052cd6d287aff6579a48dfbba522379dcf55ce9464953b | req-8bedac896d7d498a8059cdb8f2bd1b24 | prt_174f72adb001AsSwbPxRTt89li | ÉCRIT_NON_TESTÉ |
| tests/unit/test_pa_native_linker.py | d5d9d1968d12051e844119b94755c2447a2042ff77a598f975f7491a453207db | req-a6a6ef06627e403d8181065f9ea55eac | prt_174f8d9a40019ER51EsH6yXEFW | ÉCRIT_NON_TESTÉ |

46 fichiers sans dérive, accès RELEASED, aucune exécution/réussite revendiquée.


### 2026-10-25 — E5 preuves ÉCRIT_NON_TESTÉ (6 fichiers)
| fichier | sha256 | requestId | proof | status |
|---|---|---|---|---|
| src/pixs/pa_native/postgresql_observation.py | 3f635ca3ceeca7aa14b9c731aede1c06b68c1801de3cb1efb0cf70505870cbb3 | req-01842bafef42413da71cfd21f577a14d | prt_175220340001IefmNLhRGFfrcr | ÉCRIT_NON_TESTÉ |
| tests/unit/test_pa_postgresql_observation.py | ff6312b1b613638dd869914655288d13defcddddfc575233b28a384b8a36f7d9 | req-02a9715a30b24d60af8f21dfed4561f3 | prt_175226adc001vmbIOgQrSaaXJY | ÉCRIT_NON_TESTÉ |
| src/pixs/pa_native/generator.py | 78ba4614d0aa9cf7d1d5b9ca2e90b186a5030222c56414b3e8965b632147f97f | req-95bc118e52fd48609d3e05bd8ad663fd | prt_1752b7a110011Q7zj21tGqZ7aT | ÉCRIT_NON_TESTÉ |
| src/pixs/pa_native/builder.py | a3a295855d2fca13c801ae98b151a65d4004711dac5cef14a40305a6444fa448 | req-acd7c1d202cf4e9ab33e321c8e589249 | prt_1752bdeb90010CAzF5U8KbqT95 | ÉCRIT_NON_TESTÉ |
| tests/unit/test_pa_native_generator.py | 16faeb6a2ab644c5ebd2842e5e2c1c3cdcb056a4ee76b0f4f1477ab83746cfc1 | req-2fc5b88b36b549c389221152644eccf6 | prt_1752c4f3b001Q694FB2IhqpD5w | ÉCRIT_NON_TESTÉ |
| tests/unit/test_pa_native_builder.py | dda58f31541896e8c1304161d364fc19fa86ff76e5da434a4c5baa4b6812a13f | req-72b7a62a36b647c19937f0777eed45ee | prt_1752cc3a9001GftuBj1eTln1yk | ÉCRIT_NON_TESTÉ |
- Sources écrites seulement, assertions préparées jamais prouvées.
  Aucun canon/mode/autorité nouveau.


## E5 Préconditions + graphe — sources rapprochées NON TESTÉES
- Codec SHA `27d290b104f3f723a4f8f96fb38665a91d131b9da23b5c1b3040d7d3120a44fb`, recettes `576350010b416d646fca110412b91657bed0e8d1c30f5061c9f55e45e53d01b1` 17 méthodes, contrat final `4904de66f1d8f8e29e7ef6349b8ff247dad5c7c464507d1110aa56c11d2b4bbc` (E5-PRE `80b53ed5a86e2be38ff17e16642fd686487b6264bb6407e2bd01e1986f4af8aa`).
- Graphe : generator `c66d621e15386525fc6e2e2a345f802e55eeba46d02d0a44afa386b0a02bd720`, builder `bce843dec35f91b8c0b5afbccc4c9fcc032dbe9ed76b79d8fd9199f6214257eb`, tests generator `ce474712818fc278f9f688eea999b7832cbd4869a7c8acb8a0ddd88c281484a0`, tests builder `664864eb6224d8817965b8223b3adc86eef5060444e7659f9a865fb74c543a11`.
- Preuves `prt_175b6fc65001MPtiBPyFu1O5sP`, `prt_175b8b3c1001vQ2fooBoGy4ALO`, `prt_175bbf346001TdpjOdmmHKV2ey`, `prt_175c0c6080013cVuajCDmN9AkC`, `prt_175c16d98001fV4oy1inyxF7xa`, `prt_175c22d300017p92byGX4Yviu5`, `prt_175c2c3a4001JDdgmMcC1HrBOb`, `prt_175c3a730001Q1ycD2fZ4evEP9`.
- 52 fichiers fidèles, 23 méthodes (17+3+3). Contrôle fidélité seul, PAS syntaxe/compilation/import/test. Cases 2-10 vides. Reste B/retrait, owners, transport PZT, handlers, lifecycles.


### Preuves documentaires du lot adopté par le développeur le 26 octobre 2026

Fidélité des écritures en UTF8 avec fins de ligne LF et cinquante-deux sources inchangées, à distinguer de l’avis propriétaire et de la validation ciblée à compléter par preuves ci-dessous, sans validation produit ni validation globale. Avis du propriétaire C08 sur la cohérence du wire, sans produit. Validation OpenSpec C7 ciblée, hors ABI et hors runtime, avec preuve C6 seulement documentaire et sept empreintes recoupées.

Bilan des incidents : demandes MCP invalides rejetées avant admission, sans effet ; un mot altéré avec accès réconcilié sans posthoc, puis nouveau mandat de correction exacte ; aucune permission déjà consommée n’a été rejouée.

Sources préparées et tests déclarés non exécutés, sans archive et sans qualification. Lot et option INIT A adoptés par le développeur le 26 octobre 2026, sans adoption des alternatives B/C ; sans déclarer le RUN parent terminé. Adoption de spécification, sans port livré ni succès de test.

| Objet / étape documentaire | SHA-256 historique | requestId | Outil natif | Issue |
|---|---|---|---|---|
| PA01 E5 — préciser le seul contrat du codec préconditions | `80b53ed5a86e2be38ff17e16642fd686487b6264bb6407e2bd01e1986f4af8aa` | `req-54cfc88cf8b14b5e9dcb942a9fca007c` | `prt_175bbf346001TdpjOdmmHKV2ey` | RELEASED, fidélité vérifiée |
| PA01 E5 — préciser la composition du codec préconditions | `4904de66f1d8f8e29e7ef6349b8ff247dad5c7c464507d1110aa56c11d2b4bbc` | `req-5e4c3fd6dcf64283afc847e11bbc2fe0` | `prt_175c3a730001Q1ycD2fZ4evEP9` | RELEASED, fidélité vérifiée |
| PA01 E5 — consigner les sources préparées après pause annulée | `1d2359955fb291757f1c5166a38c2abae7c00b903e246312dc2ae5ab13063eba` | `req-8182e5315715463388fb626cfaa513bb` | `prt_175ce0265001IaGblIPAYArXgR` | RELEASED, fidélité vérifiée |
| PA01 E5 — rapprocher les preuves de source sans qualifier | `3e8d540d93f432ed746a502e9c7e677ef6f9833a9f627903dd686130b32d2f7a` | `req-6c9ad71fb3ad4ad499addd7c0e416eed` | `prt_175cf095d001Ybe0fv84qo2zEL` | RELEASED, fidélité vérifiée |
| PA01 RSMP — proposition unité1 corrigée après refus sans effet | `a51d27ac55b38ebfe752288e19d73712f120046aae86b1c57acf26d6f88857c7` | `req-079feb94f69d4f7fa88d9a64ac6881f9` | `prt_175f1689b001yK7dErAVwAJqHz` | RELEASED, fidélité vérifiée |
| PA01 RSMP — consigner le statut documentaire U1 en conception | `5091cf5420225aa3b1c40124695e832eefcf545435b540e0fe26517c6e1308dd` | `req-9a7a8156b64c4960af7a6d0ed379bd04` | `prt_175f94872001fYP2vNr6R2UuFQ` | RELEASED, fidélité vérifiée |
| PA01 RSMP — tracer unité1 documentaire et tâches restantes | `1b72889a55be3dea4c3a7622f14612efe2dc757a12e6f224fcce8debdebd611e` | `req-6bd4746a01a740e9aa452dc21dfe545c` | `prt_175fb1741001lgHAGb4aGY3Afh` | RELEASED, fidélité vérifiée |
| PA01 RSMP — rapprocher les preuves documentaires U1 | `f7ab85e758bd818be6bbce5ac59724efa0bdcef860fabd7926ff5101d23a3660` | `req-7b1f2eb9a7bc4fb191f6507f150d1e68` | `prt_175fd8ecc00193p7ujl2yUv0AT` | RELEASED, fidélité vérifiée |
| PA01 RSMP — consigner les plafonds privés U2 proposés | `2214ffbff9b85daf13140f7235b17121f8fe72a0a98850865fde8e96858de763` | `req-1d487eaec2cd42c7b0e71786d3a7decf` | `prt_17650e3fa001o0vN4hipTouT5y` | RELEASED, fidélité vérifiée |
| PA01 RSMP — consigner le plan B non signé proposé | `903886bed38436e679542d1c37751f64cf1f85981a92cc853bd3c0df4df7bab8` | `req-2ec81acab097492791baf8f51d171c0f` | `prt_17661a000001HIv9wf5yff0ibE` | RELEASED, fidélité vérifiée |
| PA01 RSMP — consigner la recette B fermée proposée | `47527a9aa6168456bfaf38ebdcb84b33eb7bd596f9ef354d193541fc842a750b` | `req-fdd912d14e9b4ba89ed83d251f925f9c` | `prt_17676face001peMFRG19dysi7j` | RELEASED, fidélité vérifiée |
| PA01 RSMP : proposition BASE attendue fermée, sans adoption B | `f1a138fd8459fb5034c060a26fde03a2c4893261d546ba413b4f4110f6486993` | `req-6704b3911af84385a225d5029b708d38` | `prt_17681d98e001o5NDA3OI4NecXJ` | RELEASED, fidélité vérifiée |
| PA01 RSMP : record B et chaîne mixte proposés sans code | `6c4dc407482de64c4bf17f31eedc968819d7ca91d74e360b43f53b31572814cf` | `req-d1f2779c7d9e4dd09033d5960717d2b1` | `prt_17685985a001xf1S1N3wi88X73` | RELEASED, fidélité vérifiée |
| PA01 RSMP : politique B indépendante proposée sans adoption | `9c64c4c97516c1b4d92330aaafedb54aef586f8b5d0f4d1913b53d50fcc568e7` | `req-d95b49bb88ba4fa88f793e126fabb46e` | `prt_1768a2191001qKdcR9d00BKcir` | RELEASED, fidélité vérifiée |
| PA01 RSMP : profil ressources B proposé, bornes et durée distinctes | `230e88afd80ed1f077e87d831dda67fbf046ed8e783350f3cf9167917b47ebd0` | `req-a444e14f179b4808a7004991189d5671` | `prt_1768df591001xNE8dxZp2qH1pM` | RELEASED, fidélité vérifiée |
| PA01 RSMP : correction de fidélité du mot approuvé constats | `a2ac97d239302b392fce93d5dc6bfa820d6674e72c8022e0d615aa74b8275f78` | `req-737c08ad193e4401b7dd87e9ca864d12` | `prt_176a06ead001kMOiZqNCk8DDcL` | RELEASED, fidélité vérifiée |
| PA01 RSMP : raccord documentaire aux invariants temporels adoptés | `be67f1feb81bf7b6b4e023370baa4032e4eb264105b00cf32187923060caae72` | `req-9758054ae2ff4282a0d4808c2732e9da` | `prt_176ae1dfe001WueaTwlkWialJQ` | RELEASED, fidélité vérifiée |
| PA01 RSMP : profil INIT A et procédure extérieure proposés sans adoption | `8400d5af41e32db664a915411975d8092fa215ded43daff81f7928d1d758ae4f` | `req-42af0d8f5b9e4314b52a776652e9a73a` | `prt_176c2482b001XoZgkgsAseD4bN` | RELEASED, fidélité vérifiée |
| PA01 RSMP : provenance initiale et admission par étapes proposées | `392e4970190890077114e60c52eeef988bf858b00058d49efc45e99a0a58b226` | `req-5151332d9eb64e4bbf7ce796d5a08006` | `prt_176d8affd001EtJnlVj2wY5AHw` | RELEASED, fidélité vérifiée |
| PA01 RSMP : retrait administratif fermé proposé pour revue C08 | `d95d09deecc865952453dd0459b1dddea95ee9563f124b532382f958f04d8ad6` | `req-a8789248cf2e4d06b42e3385ff062e6b` | `prt_1773abbe8001Cr1UHedJza26j2` | RELEASED, fidélité vérifiée |
| PA01 RSMP : consolidation des renvois et clarifications C08 proposées | `e97a2647686a0a84d2ef68072c3ba0a8165b56d047000634165938b395ebd833` | `req-fc2a8a6090c44a058253ce30982638d3` | `prt_177571746001j2gBg8RTT0dKy0` | RELEASED, fidélité vérifiée |
| PA01 RSMP : synthèse finale de conception proposée à validation | `3dda320ed3c5b818274f81b721481b42848327f859fdbd8329f849387e8732e4` | `req-ba948ee4035b43fabb4a43c1ec486adc` | `prt_177626bef001TzKY1nVBtc9AD6` | RELEASED, fidélité vérifiée |
| PA01 RSMP : suivi des tâches sans coche ni qualification implicite | `b428fa74ea6b629c3016e450fe291cb53ab7dca018a0f5b8134f48e13af66a99` | `req-300299ff8dfd44a5af44332eb903c863` | `prt_17765f0b0001JSrFgdzg6G6n6Q` | RELEASED, fidélité vérifiée |
| PA01 RSMP : deux renvois de cohérence finale sans changement de formats | `6700a7d89ae5cf82de3c2851ddcf3913367fe7e509d7d76de382f027a1f4cae0` | `req-c2af921eda274c3bb70fb79b77bad647` | `prt_1776aa621001bHyuOkWUBlVRtr` | RELEASED, fidélité vérifiée |

Empreinte contracts courante : `6700a7d89ae5cf82de3c2851ddcf3913367fe7e509d7d76de382f027a1f4cae0`.

Avis propriétaire C08 : recevable comme proposition documentaire, sans adoption ; rapport auteur `msg_1774aedb2001O1uGQQaB73iuqs`. Les trois clarifications ont été intégrées et relues sur l’étape `e97a2647686a0a84d2ef68072c3ba0a8165b56d047000634165938b395ebd833`, sans écart résiduel ; les deux renvois de cohérence ultérieurs ne changent pas le retrait ni ces clarifications. Aucun port ou produit qualifié déduit.

Validation OpenSpec C7 ciblée réussie, code retour 0. Commande exacte :

```text
/home/devops/.local/npm/bin/openspec validate add-pa-native-build-and-component-composition --strict --no-interactive
```

Outil natif `prt_1776e08970012NYV5SWwzQJhAZ`, rapport `msg_1776e1dde001G7QNhBkhPYdsF6`, accès RELEASED. Sortie : « Change is valid » ; INFO `skip_specs`, zéro delta accepté. Portée documentaire uniquement : aucune qualification ABI, code ou runtime ; les validations globales C6 restent des preuves C6, sans requalification C7.

## Annexe du 26 octobre 2026 — fondations B écrites, non testées

Le lot documentaire B/retrait + INIT A reste adopté sans modification ni revalidation. Code écrit sous mandats CAB unitaires, dix fichiers RELEASED, non testés ni qualifiés. Empreintes observées avant l'ajout des quatre annexes : design.md df656fb1047bcffeab0ba6b1013c1f4938ccc0b0410fe26260db0b0ed7b7d719, contracts.md ff5473e7be06c711dcbf9fd02f29ff1cd9fa3743f4ffded5be30952fa839a144, tasks.md 932dd6eb296c3d32be26f5834865d265daa7f65904e4fa0581836f3c330d90e4, VALIDATION.md 47a3720a26a8a1b0a0d68160c4284792acfe0f0068e86499e01a77c3c502c020.

| fichier | sha256 | requestId | outil | rapport | readiness | release |
|---|---|---|---|---|---|---|
| src/pixs/pa_native/bootstrap_context.py | 5ce2849a9e87ce2c30898377aa12833d5260d39acb209588af10dd1d4c729c3d | req-10d6b706495042e6bae28d9ffe557398 | prt_177bc1af2001CqgoNT5FBAWvh6 | msg_177bc3075001D2wa0ce72m2u0c | prt_177bc29190019D4M9T43h0izp4 | RELEASED |
| src/pixs/pa_native/bootstrap_init_profile.py | 332765b7302a47596add88d8e0cbef2af9a467b824984effc9f838c0c33095a8 | req-73076c8e4f2143b590f30044b8fbf35c | prt_177d61d1d001DnikkKB1kcfccY | msg_177d63e8d001DuxV4hNrVnlMWv | prt_177d63764001AR0RCKVSmd7eSw | RELEASED |
| src/pixs/pa_native/bootstrap_nv_profile.py | 14ae5068066e21f77e01614fa3770a9cef5c79983f0753fe6e336664b9e7eb18 | req-4d9b7484130f479b972c6d2b22c72909 | prt_177c989ea001zqG6EwobypFcmG | msg_177c9a807001f2f0jnOEk6f01C | prt_177c9a0b8001USQiZSlKJWIAJP | RELEASED |
| src/pixs/pa_native/builder.py | d0bbca9652c4009324a0d52b4e7bf2afbd18c880ef2a1957864a26e4841a7221 | req-c3360521d65346bcb50c3d2987693db3 | prt_177dce5de0014URaNU0buT6WQK | msg_177dcf9e7001ATyCMRJn6AC4uD | prt_177dcf2ab001LwrI7KqCsgz7qY | RELEASED |
| src/pixs/pa_native/generator.py | fab4f2f0668733a4564e2c8d7c9d55e82cdd12e3dc33d21ebd1f9f8ca156d966 | req-30ace58182a64de1a782897403f298db | prt_177dc6b7d001x7043dPjzoFk15 | msg_177dc7c18001kkZ2Rt5ajBemig | prt_177dc74cb001JUt3EXZehGKH2H | RELEASED |
| tests/unit/test_pa_bootstrap_context.py | a564a0aeabba3f8a876cd1fb5ca1a5029925642e0bf676b5f120bf2758277615 | req-5b6ba1ab95b148e386c3aa50fcf8366b | prt_177bee8af001732T6RYBFImS1U | msg_177bf0f14001w71xRAZ9tEI1hd | prt_177bf06c9001BbPIvZckSdJ6mm | RELEASED |
| tests/unit/test_pa_bootstrap_init_profile.py | e3712ef48c2e0f9d69e60b56dd5103add52cdc91597c483953dd092e7b4621b0 | req-058d8bc9b6884a469c759b474b0faf6a | prt_177d6b711001t8EEYMT8F1E013 | msg_177d704b4001BvyQVWyTNn0ewK | prt_177d6fc46001JLMEU5gJeyvd4Z | RELEASED |
| tests/unit/test_pa_bootstrap_nv_profile.py | 2770ab46ac245d28038f284b0c1b678a5594275b2ed9345adcdb05f47a6aad93 | req-c558ecc3f3ae4249a2a7c8fbcdc82473 | prt_177ca231d001wB4RK7LJC9Nef0 | msg_177ca54160013z9m7BTYH0AGCs | prt_177ca4cbe001kjuNIDebL6qryv | RELEASED |
| tests/unit/test_pa_native_builder.py | 24087905de5136630cae12e23da4c67696a87f4b699d590206380639d3398c7f | req-1757a14578de4f8a8dc8a0967ad61730 | prt_177ddc2ae001aLZu7DQc3AkoUT | msg_177ddee36001l1GrP67smvqyU8 | prt_177ddcb77001WASg5gv4VDZ6Wf | RELEASED |
| tests/unit/test_pa_native_generator.py | 720f9cf9b1e8b80d22f2fa053e9d974594b11aa0661d9f86c1f138b858a70797 | req-f9cc99ec92624e92ac393f2d8fdcd9d1 | prt_177dd587b001daUu7nj75gMBka | msg_177dd69ec001p1Wfpyy55px26i | prt_177dd625b001MEWFIY76AOxPpb | RELEASED |

Le rapprochement prouve la fidélité UTF-8/LF et l'effet d'édition, pas la validité du code. État : 58 fichiers suivis (25 de réalisation, 33 de tests), 131 méthodes préparées (43 + 37 + 33 + 18 de graphe), NON EXÉCUTÉES ; aucune syntaxe, import, compilation, unité ou qualification produit.

Reste dû : Base8, Resource24, Policy14, PUB/FIN, recette et R0, provenance, scanner mixte, admission et retrait effectifs ; vrais producteurs et résolveurs D11/D13/D14/temps/PZT/handlers/résultats/lifecycles, puis campagne LXC et effets matériels sous plan exact distinct. Aucun port livré, admission, NV/SQL, installation, secret, Git ou archive.

## Annexe cycle par lot — 26/10/2026, FORME PYTHON seulement

Même cadrage et consigne que tasks.md ci-dessus. Unités validées pour FORME PYTHON et composition de métadonnées seulement, sans qualification globale. Test builder courant SHA `1b462a2881df03b63544bbce6139235671d747b4812e33e15138a6d5ac4fbeb7`, édition `prt_178270b19001pz2lpFjDiMUxCy`.

- Context8 version Python : `req-90e50720446048afa3ba57d0690c74ca` / `prt_178063b83001WbgtykrI9zCC7H` / `msg_178064beb001gDcSsyj7hXSSn4`, exit 0.
- Context8 43 unités : `req-ec1ada4638a046688a9ca42fb83eb031` / `prt_1780a4375001JPW8gkNJQaIOvz` / `msg_1780a5544001wENqkg55yOORFL`, exit 0.
- Context8+graphe syntaxe 6 fichiers : `req-9269fdcec10f4cf4b7f66a4404e006f7` / `prt_1780ec50e001yACguXBcc66Mcq` / `msg_1780ed951001NtPaD1YrmFWJZ1`, exit 0.
- Builder syntaxe après correction : `req-4a20506506374265a84eb044b549617a` / `prt_1782f5b79001zuIA908EaTzHbM` / `msg_1782f6add0013GU6iQ7lyE4B8q`, exit 0.
- Graphe 63 OK après correction : `req-62cbf4e1ed6a4e52b7b5737789e1e8de` / `prt_1782fbe43001xebRHNeLMuj3pL` / `msg_1782fdd23001t35PrHGHiYX300`, exit 0.
- NV7 syntaxe 2 fichiers : `req-dab1feba0f364fdda0d39d6875fcfb20` / `prt_178312a44001YlvulWxty37Pt5` / `msg_17831598a0011eIQj31RARqsle`, exit 0.
- NV7 37 tests : `req-8cd4a54f12ed47118f76ba96cc03e2b0` / `prt_17831d8410010wQqHws84a81ee` / `msg_17831f0a10010WDFWtDG04ikUA`, exit 0.
- INIT12 syntaxe 2 fichiers : `req-f94704508a6e480da229836e85355c87` / `prt_17834399c001FD98Kgc1XNdaCs` / `msg_178344f57001ZnmgMyjRvGn4T6`, exit 0.
- INIT12 33 tests : `req-83bf816b45a8425aa62ab7a55d405ebe` / `prt_17834c777001h9TWO9Hw6eY3V4` / `msg_17834d7f2001SpeKYZjKxRooa5`, exit 0.

## Annexe Base8 — 26/10/2026, FORME/COMPOSITION PYTHON seulement

Fichiers courants (tous RELEASED) :
- `src/pixs/pa_native/bootstrap_base.py` SHA `ddb8308b97eb00d8f0a921a6fe925618ad05b3ddaf2d9d4c2f9565865de0613f` req `req-c4f7874282c04d41a8e262de6ffeedfc` tool `prt_1784cdfff001q8BOexWkqOTYOC` report `msg_1784d0242001LRV9yFZD5RTeXu`
- `tests/unit/test_pa_bootstrap_base.py` SHA `f749d517d5695455700511e6df1822504cb89ba9951fb35351efb9b7135bd947` req `req-be501318993c41b4b11f57dea0452366` tool `prt_1784e6d6f001tGaDUe3erL44HN` report `msg_1784eb1de001Zy4f82IKe1AS1w`
- `src/pixs/pa_native/generator.py` SHA `c7d1aaf738190d1f292f0e92ee3e22b1d954853a81e627b16ffe9a728ac661b7` req `req-38ac9944bdb342ab9fa1441e96213d58` tool `prt_1785a7f0b001Gx19gSoh8cRW5P` report `msg_1785aa0bc001cEQGtkrCQi7yjf`
- `src/pixs/pa_native/builder.py` SHA `81dae7cdee80bf63148e3f2b4e53e8aa87319ce6aebd5d752ee35839d604d7c2` req `req-3dd7284c245c438eb878cdef0e8dfee0` tool `prt_1785b0dc7001b3mXckpyECG43Q` report `msg_1785b22a3001FDnj2KykQrFuJk`
- `tests/unit/test_pa_native_generator.py` SHA `9b09d24e4fe4e9ff8aa6cf2a013f842035c5ac333256540fb53bf6c28fb0dde8` req `req-d00abab1d8cc46c79b66939a74008185` tool `prt_1785b770f001pYqhFcU6k7RrjV` report `msg_1785b943a001xCDJuYGGXHjU8J`
- `tests/unit/test_pa_native_builder.py` SHA `5b5e8f794e2fc0ff01fcda4df21c0c5dac71b9a6503a7e4ec114a7323677e767` req `req-05e839088ddb47b8bc6e94c6a8d080fb` tool `prt_1785be83c001RcV3ILueG6G3PV` report `msg_1785c02d5001DESkrnJIvRKAqV`

Contrôles exit 0 : syntaxe codec+37 recettes `req-c041fef51ba14df9bc4129bf83d931ac`/`prt_17850eea4001xhxSf11hZVWKMd`/`msg_1785106c100195eCoDAfLKNwWu` ; 37 tests `req-8cf7e4acdf0b401fba1ce3fa65570944`/`prt_178518118001HRvXbVsssdLrOh`/`msg_178519653001ciZx5DRxpW2ylt` ; syntaxe 4 fichiers `req-71121608581d458795569c5295e66c5f`/`prt_178620f26001CdT2X2w1m2pbS4`/`msg_178622bf9001a0SqXyEtmJLY0o` ; 69 tests `req-7589a78ac4b34d5fa5cbda877260e810`/`prt_1786578b4001VdgyKz4cehYiMo`/`msg_178658ee30014FQevOfqkHg4g7`.


## Annexe Resource24 — 26/10/2026, FORME/COMPOSITION PYTHON seulement

Fichiers courants (tous RELEASED) :
- `src/pixs/pa_native/bootstrap_resource_profile.py` SHA 7b4f2479fa7715e2b17ef1ac6833a218dcd5eefce9373dfaefcee8db33746404 req req-8e7a91ccae784e2a8cb58170f58d3dfe tool prt_178925518001SA0VpkAUc0QjaC report msg_178927cc20016PCi2H7FzqX1Bz
- `tests/unit/test_pa_bootstrap_resource_profile.py` SHA fbe6aa179c7e4e1119bb6c3bbf3f1eda8e1e995bf9ac9c366cf38c3333c77bf0 req req-5704c8f864cb45439ba23953e65a77d2 tool prt_17895b23b0013K2HbVgkzedcNP report msg_17895c115001XLa9qix2ozTREE
- `src/pixs/pa_native/generator.py` SHA 92fdec1bfd9739918e2d92a68f4a9ee5c89f5ea9e2edd3c05aa827378d3dd4bb req req-f2a7ac9052b445f2af7a80eebd33090a tool prt_1789b25e3001xaBz4yeqsJBTKd report msg_1789b3c63001va2w5qTXL3a0rn
- `src/pixs/pa_native/builder.py` SHA 22ca5897f63c4b354817f62254392e21318bed58649a77ed20a56558b7d4c571 req req-db9c41acf62a48d6a7af09ab36f1a821 tool prt_1789b9175001XvVT6TFr7z8Pvs report msg_1789bab68001z6Wrvn9f2cpiS5
- `tests/unit/test_pa_native_generator.py` SHA 7a560af3406e655421d22b8e82664dbacee4cc3089a2713526bf776b611d5912 req req-e58d8a49ba914558ab39c48224d28d4c tool prt_1789c2f70001OHlbXubpAGbOCb report msg_1789c4c1b001hXAENNbU9liDJT
- `tests/unit/test_pa_native_builder.py` SHA 3274fcd75a064673d2d028538bd03e3ac52f22d64f2ad71fc77aea2f4d860d1f req req-ee01b72d5eb94e9fb4bc25582cd2a7d1 tool prt_1789cc1d4001Mr3J9esCWu5b56 report msg_1789cd779001N7Ah7c9TaHFuMq

Contrôles exit 0 : syntaxe 2 fichiers req-ff3f13adb9024ce09187c22de372100c tool prt_178971652001qRAo2RSEGNen0k report msg_178973283001FehbSAZdiYFA69 readiness prt_1789722f8001a2D8iB7AUBgnGM SHA 3f0d20e824d685b9fdb4a1e600a538a35d77adcd5adeaf9823e3728cb4c4d599 ; 55 tests req-e9656f0454f64ff4af13a05e31e2c278 tool prt_17897874f0017dIqIGCFEwi4fX report msg_1789799e8001IQhTG640XziH19 readiness prt_17897923b001qS0j9p1h59Bqv1 SHA 6610f632676d37831e91c7512a8e081cfce50366612656aac967c19fbad3da4f ; syntaxe 4 fichiers req-a504ad25489e48fb90c80e2bea1db9ce tool prt_1789d75d5001Z2SqXPF8jscFdH report msg_1789d8867001jtxwF5X3eo9i7L readiness prt_1789d8091001axoySgwHXUiV6B SHA 8bdb15ed718a8c42f5d8b493038c88503ad1bd53bcfdd95da271740152edf544 ; 75 tests req-9c1a71fcb39e46c98116ae098b626c21 tool prt_1789df1c2001DmA0fhB92329G5 report msg_1789e05f6001zPo0UwoRPcUmV5 readiness prt_1789dfe3b001OiGlg3xzXmH4ux SHA 0d5777e5b94364a700bbf22eee295527285d6441be473876616f3830a4a8bb5f.

Source/recettes/composition Python validées Root. Contrôle OpenSpec strict à exécuter APRÈS ces 4 écritures, résultat distinct au checkpoint, aucun PASS strict anticipé. Ancien strict Base reste preuve antérieure. Scope forme Python/métadonnées ; pas Cython/link/builtin positif, LXC, TPM, NV/PG effet, PZT, admission, installation, Git, archive.


## Annexe Policy14 — 26/10/2026, FORME/COMPOSITION PYTHON seulement

Fichiers courants (tous RELEASED) :
- `src/pixs/pa_native/bootstrap_policy_profile.py` SHA 87bab3ac2141dfa96b96129614124ac1a2a38dd12959f44a2607b50b12159c9d req req-42780dd1d3c248f49c83b912b5a8bbcd tool prt_178dadfea001yZRhfXtmoC5PtQ report msg_178daf1d80019k009hMoxgEVk2 readiness prt_178dae9de001T9ObDDQzbH6iJC
- `tests/unit/test_pa_bootstrap_policy_profile.py` SHA c243ea790c4ee1958b94f506f900ef605a15a4da099e172cad4d019ad9380911 req req-1d108365aa3c4bd2b6dbebac92313409 tool prt_178db45d0001V8BLHO6exxMemN report msg_178db59ad001YVw0cO65ofJbf8 readiness prt_178db51690010fYRpSpQKT8i7r
- `src/pixs/pa_native/generator.py` SHA 2ace22e36e2d3c90fe42c65ac3a472c6829066ac5915c07f6fc1740530ac2a43 req req-4b1f8292534e483184f86dabfd878e44 tool prt_178fe6cb5001zb28YDSBplWKNp report msg_178fe7de1001jPZiXZQQiTIyTv readiness prt_178fe75ce001fm3ZE7BxVJwZK0
- `src/pixs/pa_native/builder.py` SHA 0f7f0a403ff611d21f1750d432fc4b955a79afb992f685a02fc218639cd7406a req req-d0cd207322a941af99b5c25fa75f4883 tool prt_178fece9e0015k3m9V1XQ1GmIv report msg_178fee0fa001FoaXuX77QOFjHZ readiness prt_178fed90e001ckJfHeag3tiFht
- `tests/unit/test_pa_native_generator.py` SHA 66711883df18ffd5369ca4290f07c2a11613a256dec72df2632dc9592e85cef3 req req-885594f4de984d66ada166c5c6c1608c tool prt_178ff56a1001VjD0C10NbO30GE report msg_178ff67d9001X2iAFY7LRJi54V readiness prt_178ff5fd1001UK7weglmDzwi5O
- `tests/unit/test_pa_native_builder.py` SHA 53436305365a8c85e8d43bfcccbf87d4cbfda12f84a9fe62851d3eea658b2561 req req-959251ee23f64ae399433cfc57b6f036 tool prt_178ffc7a2001bH1aVnmyB0wgrO report msg_178ffd7960014jVFBbZUFhqiwv readiness prt_178ffcf730019Laa6pUauN0HnC

Contrôles exit 0 : syntaxe Policy req-8d47a472a0bd44f4a24a6332a8c0b930 tool prt_178dd276300112GDqQNs4NVxSq report msg_178dd39c6001MvEhrCve3se9ms readiness prt_178dd316a001fw6rWAoWk4e4sA SHA e4165e00678080e85460d968b540c9ec72e67845fe3e74ae36a2e69c7a41aba2 ; 13 tests req-cc51ddf1053945b4a4060bec01de16cc tool prt_178dd8e44001710OzGJ7zSiKKQ report msg_178dda2cb001JL0MybDtebv0zY readiness prt_178dd9a9d001IDMRn7HjdlqHr7 SHA 82a3117a9a50bb37e3980e4bbd96e1e831d763a0167c10ef3f8ac78474894275 ; syntaxe 4 graphes req-9c294e8cf1dc4e44aaf7fc8282db3198 tool prt_17901e900001R3FrsfANbrnIYM report msg_17901f968001cu3c1f2NGDnVjd readiness prt_17901f16b001gOrEFpxydWLYv5 SHA 8bdb15ed718a8c42f5d8b493038c88503ad1bd53bcfdd95da271740152edf544 ; 81 tests req-c1ec3dc97cb64da89f3a0e7d86bac040 tool prt_1790259b10019Pg3P8StM5lAg7 report msg_17902709a0019bcTRqbLHu2WqE readiness prt_179026438001kWGe4kUEDqDZuE SHA 0d5777e5b94364a700bbf22eee295527285d6441be473876616f3830a4a8bb5f.

Table des 10 unités précédentes :

| unité | n_tests | syntaxe (req+tool) | unités (req+tool+report) | exit | release |
|---|---|---|---|---|---|
| PG/journal | 56 | req-1e218c99d2924120b781b13e8078ee4a + prt_178aacea50010uaUJOOEH50Akz | req-6a9e8019388b4babbbc3d1783bcffce8 + prt_178ab4d070019Qm7Ja4i1spus3 + msg_178ab6e6b001BwIprzcoXgRPWu | 0 | RELEASED |
| CLI | 5 | req-e9a41dae17644dcfac3ee656b11dcfa9 + prt_178b2084f001rvwmkU4HHZ0wG9 | req-3befb04a2bd74245aefd2ac3250add95 + prt_178b296a4001iu81LS7bOVN7cR + msg_178b2aa52001kR4tx5JRvx5ZPb | 0 | RELEASED |
| build | 10 | req-44b0a76e649b4dce9b692ff10f50b9f9 + prt_178b3c51f001pMDSitVqP9mMe6 | req-f2e342286479449ebed26f9cd4a66c31 + prt_178b429d70017SeCW3xfqh1QDW + msg_178b43acb001yQvhnsXmwZ3qMN | 0 | RELEASED |
| peer | 8 | req-019ef2f6234d4bbf8f7b11dc590e88e2 + prt_178b5a81f001T2Orn7JGCj6a8F | req-cf4f2b975b314df180852cdad8237dae + prt_178b610bb0012dozopW9KnMTN9 + msg_178b623b90013x3qOA8NbUR44S | 0 | RELEASED |
| admin | 31 | req-e3b27f1e45bd4c09b077670e6e03679b + prt_178b72705001U9nIW4LRd5wHCP | req-a484bd9382994a16aa6aef287420ad6d + prt_178b7c16c001yQjwft4u2AiZux + msg_178b7d23a001ICOENUi01QFoRY | 0 | RELEASED |
| observation | 12 | req-335b2ddfd448447190937d2cd7118c02 + prt_178b98e9f001B5vR2k06GYsbF3 | req-c8a8a1ff63864bdfaf06ab21bcb4af21 + prt_178ba1306001URIZtX5UXkZ6dE + msg_178ba247f0017Tb8W7SbYUy1jc | 0 | RELEASED |
| effets | 10 | req-40d01e632b10409e965934c4d9a5a727 + prt_178bc68b000117VUwJZeq52AcP | req-361282de490441de8cd703c7e28ac3de + prt_178bce56c001tjOza6mtm7Bp6H + msg_178bcf5d4001jb77eIyYQmwAJs | 0 | RELEASED |
| préconditions | 17 | req-477254d4712346fc95b694fbba3378c1 + prt_178bdda9f001CJlwqWcWIQsuex | req-085978c6779744f8868da437816036f8 + prt_178be3a3c001fd5BPGKJLIrG7D + msg_178be4c040015jmEEtQVJdzIXJ | 0 | RELEASED |
| linker | 19 | req-7e8d7c7776ac458294f349af3f2e7d17 + prt_178c00038001g7DyHFBflIAL8q | req-cb77a0ca4455463d908f800b1147d8b6 + prt_178c07d7c001EDPkRSBalESvfl + msg_178c08faf001MCk7OatmCXG62k | 0 | RELEASED |
| bundler | 14 | req-be90a496a1ae4e11a1f3b823ed6d94a1 + prt_178c31e48001Ies5bCYfBHU78U | req-6cadf44c91234cdd877ed93b91043042 + prt_178c3b906001P7W5rSMXW7H1PR + msg_178c3ce51001WKkiJGZJWtCJaj | 0 | RELEASED |

Source/recettes/composition Python validées Root. Contrôle OpenSpec strict à exécuter APRÈS ces 4 écritures, résultat distinct au checkpoint, aucun PASS strict anticipé. Scope forme Python/métadonnées ; pas Cython/link/builtin positif, LXC, TPM, NV/PG effet, PZT, admission, installation, Git, archive.

## Manifeste des environnements de test PA01 — 26 octobre 2026

Environnement LXC canonique `lxc:hvp1/100`, alias historique `resource:lxc-ct100` : même instance unique CT100 sur hvp1, pas deux environnements ; ressource canonique WRITE ajoutée à la réservation. Source d'identification : confirmation humaine explicite du 26 octobre 2026. Accès SSH privé par le seul processus de contrôle (aucune valeur reproduite ici) ; uid 0, Debian 13 x86_64 réels, outil `prt_179556252001Df3jVN4rTOp04w`.

Installations des 19 paquets vérifiées par `prt_1796dacfa001iUPYWBBSqh6M6i` : query 0, audit 0, sortie d'audit vide ; versions SDK `3.5.7-1~deb13u3` libssl-dev, `4.1.3-1.2` libtss2-dev, `17.11-0+deb13u1` libpq-dev, `257.13-1~deb13u1` libsystemd-dev. Cela ne qualifie pas ABI/native/TPM. CPython 3.14.9 GIL statique et Cython 3.3.0 pas encore installés.

Nouveau cycle test-resources-v1 constaté ; réservation de test à acquérir avant futurs travaux conteneurisés, conservée jusqu'à nettoyage propre et vérification distincte. Consigne humaine : binaires et bibliothèques installés restent, seuls propres fichiers de tests seront nettoyés ; aucun effet TPM/SQL/hôte, aucune désinstallation d’outils.

Traçabilité : préparation APT déjà faite sous ressource générale CT100 WRITE avant mise en place de la réservation spécifique de test, réconciliée par dpkg ; aucun test produit natif commencé, historique conservé. Réconciliation effets sans rejeu : commande trop grande refusée puis rejetée avant effet, installation une fois et relecture seule dpkg, aucun succès global.

## Jalon chaîne native persistante — 26/10/2026 vers 19h25 UTC, après manifeste historique 18h21

Chaîne installée persistante conservée après tests dans `lxc:hvp1/100` : CPython 3.14.9 GIL activé/statique (`Py_ENABLE_SHARED=0`), `SOABI=cpython-314-x86_64-linux-gnu`, préfixe neuf `/opt/pixs-pa01/cpython-3.14.9`, binaire explicite `/opt/pixs-pa01/cpython-3.14.9/bin/python3.14` lancé `-I -B`. Configure exact déjà relu `--prefix=/opt/pixs-pa01/cpython-3.14.9 --disable-shared --with-static-libpython --with-ensurepip=install --enable-option-checking=fatal`, `CFLAGS=-O2 -fPIC`, `make -j2`, puis `make altinstall` seul ; aucun remplacement Python système/hôte ni lien global.

Sources officielles et archives vérifiées avant effet : `https://www.python.org/ftp/python/3.14.9/Python-3.14.9.tar.xz` SHA `e02d9ac21cebda6e46435369744a92c65cc7cd8669697694122cf97ffacd1e53` 24176992 octets, roue locale `cython-3.3.0-py3-none-any.whl` SHA `9b24b5c8cd536946b62086fcafee6d5509d3f549f72d553d2336af87ffbe0da1` 1349151 octets. Configure `prt_1798ad82c0013fR6Cvh3uhnU2p` rc0, build `prt_179931a96001od5gUz624uYIhT` make0/sonde0 version 3.14.9/GIL vrai/partagé 0/SOABI/9 imports, altinstall `prt_179999bc4001rSnACLKtA0y4ek` préfixe/exécutable exacts et pip réel, trois SHA binaire `094c99b0dd02ce9ca4156f2d1e6559a5c48abeeeeb50f6935197dd3838c5e9f8` / archive `12f7c8751091b0f78455d426db407e02da1b8206b8cc8c907dba46cca9de660e` / en-tête Python.h `e39aad93d70c3ea1a63b77ec5795ff59a5c177745aedace6f83bbf4275a20d9f` identiques avant/après installation. Cython 3.3.0 depuis roue locale seule `python3.14 -I -B -m pip --isolated install --no-index --no-deps --no-cache-dir --disable-pip-version-check`, sans réseau ni mise à jour pip, import `cython`/`Cython.Compiler.Main` et CLI `python3.14 -I -B -m cython --version` réels rc0, preuve `prt_1799ee49f001jut5GiNb3XHLUC`.

Recette lanceur `prt_179ab709c001QD0Xuxs4OM4S7d` : 7 attendus/7 exécutés, 0 échec/erreur/test ignoré, vrai `TestResult` depuis copie LXC `prt_179a5db39001IlVsDXzgCoXvB8` (`native/pa01/launcher.c` 6628 `22a335a9c15f13e496b867b55038f73df115081f3c3d09e6f79211897cb77f49`, `native/pa01/launcher.h` 491 `90fdc80e4157f322baf2e08324287782019e981785d3790d3236c8df3beaf4a5`, `tests/native/test_launcher.py` 10155 `d24a2863ee4033b3e236a26f271aedcb7f850120f1639218a172dcc03eaf3545`). Limites exactes : fixture C et runtime/encodings seulement, pas qualification 4 exécutables/catalogue/PA/PZT/TPM/PG ni cible physique/VM. Historique 501 tests Python/sonde (481+20) distinct de ces 7 natifs, sans addition de réexécutions ni sondes statistiques. Pas de nouvelle coche 2–10 ni archive/Git.

Réservation test LXC détenue jusqu’à nettoyage des seuls fichiers de tests puis vérification distincte ; outils, bibliothèques, Python et Cython conservés après tests. Accord humain SSH 3 variables limité au seul processus local conservé, aucune valeur reproduite.

Sources de provenance : [publication CPython 3.14.9](https://www.python.org/downloads/release/python-3149/), [publication Cython 3.3.0](https://pypi.org/project/Cython/3.3.0/). Les empreintes effectivement relues dans le LXC restent les preuves d’intégrité citées ci-dessus.

## Jalon constructeur natif — 26/10/2026 20h18 UTC

Recette `tests/native/test_object_builder.py` SHA `51c6634a907c2e36d6d72e4d35d3bb4494e3d6cae124fa4e5f1d714e6bb4682b`, vrai Python 3.14.9 / Cython 3.3.0 installés, manifeste copie 28 SHA `c06e12fbd2c4628505bf5ee34593724457b56f2963e97e837b98043bb953c701`, `builder.py` SHA `0f7f0a403ff611d21f1750d432fc4b955a79afb992f685a02fc218639cd7406a`, `generator.py` SHA `2ace22e36e2d3c90fe42c65ac3a472c6829066ac5915c07f6fc1740530ac2a43`.

Preuve `prt_179dc8e310016xo7I5hWbZyhIu` : 9 attendus / 9 exécutés, 0 échec / erreur / ignoré, vrai `TestResult` ; contrôles compilation Cython/cc, initialiseurs, 2 emplacements, en-têtes, délais, nettoyage parent/enfant, dépassement logs, reproductibilité. Sources 28 identiques après test.

Limite : objets synthétiques seulement, pas programme PA/PZT ni PG/TPM ni cible physique/VM qualifiés. Total natifs distincts 16 = 7 lanceur + 9 constructeur, séparés des 501 tests Python/sonde, sans réaddition graphe ni sondes.

Cycle1 temporaire nettoyé et vérifié (`prt_179c4e8ea001AhtkhImUcY3CXE` / `prt_179ca35c6001FCwBnMfpz1d8Wl`), installations conservées, cycle1 libéré puis extension 28 lectures et cycle2 HELD pour la suite. Demande constructeur précédente à access_id divergent rejetée avant effet, puis exécution unique, pas de double test. Aucune coche 2-10 / Git / archive.

## Lot liaison 5 + correctif chargeur système D7 — 26/10/2026

Correctif minimal conforme D7 (`design.md:112`, runtime Debian 13 x86_64, sans copie aveugle libc/chargeur) : `src/pixs/pa_native/linker.py` `bc3b2b42df72295fd122512d482a086be520ac98dfe09485b0d2df5bfb2934c0` (ajout seul SONAME OS `ld-linux-x86-64.so.2` à `_SYSTEM_SONAMES`), `tests/unit/test_pa_native_linker.py` `6ef4fbf25815d7da7d750f4ae8afb76a5f752978dbd37ce4c14a675569fa1497`, `tests/unit/test_pa_native_bundler.py` `267fd3bc8d25da1fe6744e53990777753dea84600c878a20816e2de52a19d5cb`. `bundler.py` produit inchangé ; refus chargeur exact et `libm` sous `lib/` ajoutés à la recette publique.

Ancien échec `prt_179ed95b10013pzgyuOFO4aN5L` : 0 test exécuté, erreur 1 setup `PA01_LINK_DYNAMIC_DEPENDENCY_INVALID`. Diagnostic `prt_179f8c6f7001D5T73Zc2oCr7de` : premier programme fixture `pixs-pa-events`, `needed` exact `[libm.so.6,libc.so.6,ld-linux-x86-64.so.2]`, `RUNPATH` exact `$ORIGIN/../lib`, reçu `COMPLETED`/`exit 0`, rapport `FAILED`. Aucun masque ni refus levé génériquement.

Preuves : syntaxe 3 fichiers `prt_17a03fca3001RmGMrnRHhiC5Yr` ; 35 tests `prt_17a0478fd001HrXiAjnmb9QsZp` (21 linker + 14 bundler, +2 distincts remplaçant 19+14 : acceptation chargeur exact/RUNPATH, refus arch/noms/libpython/RUNPATH erroné, `AssertionError` fourre-tout, export-dynamic lié au compiler) ; natif 5 `prt_17a075fb9001ACjN67EfXmssgH` expected/run 5, failures/errors/skipped 0, success true, Python 3.14.9/Cython 3.3.0. Complément `prt_17a0a8b640017vtXRJGI4bicXE` : 32 sources miroir inchangées, log 989o SHA `c2a0141227ee54ea0820473c5eb750f20d0a33e85509270ea0ea8f7819890561`, `Ran 5 tests in 27.588s OK`.

Cumul natif distinct 21 = 7 lanceur + 9 constructeur + 5 liaison. Python formes 483 + helper offline 20 = 503 sans double comptage. Tests 4 programmes fixtures, deux emplacements mêmes octets, aucun programme lié exécuté, aucune qualification runtime PA/PZT/TPM/NV/SQL/matériel.

Reste : nettoyage cycle2 et vérification distincte, outils/paquets conservés. Info humaine : Cython local installé, déclarations relues `pyproject[build-system].requires Cython==3.3.0`, `DEVOPS` interpréteur `.venv` Pixs 3.3.0, docs non modifiées par nous ; ne pas assimiler inventaire à qualification hôte. Tâches/D7/contrats/design inchangés, aucun statut livré/TERMINÉ.

## Fin cycle2 + Cython hôte vérifié — 26/10/2026

Cycle2 nettoyé `prt_17a113c1d001V6x2hjyyMCEOj3` (miroir privé supprimé, journal constructeur9 1683o SHA `97ada0e2d8ebae0dd78315de7f7ac3baa95209bad1012f236c5871ba3e261162` préservé, `/opt/pixs-pa01/cpython-3.14.9` conservé), vérifié distinct `prt_17a1235d8001mFNbkBH1BBQmyS` (temporaires absents P1/P2, 3 SHA Python inchangés, GIL/statique 3.14.9/Cython 3.3.0, 19 dpkg identiques), test-lease cycle2 RELEASED.

Cython hôte vérifié `prt_17a13549d001PtNbBN5NxLSTTm` : 3.3.0, `compiler_importable true`, venv Pixs, Python 3.14.10 ; aucun paquet installé par nous. Constat local seul, sans qualification hôte globale ni adoption Python 3.14.10 pour cible (cible reste CPython 3.14.9 LXC).

## Jalon S1 structure seule 43 methodes — 26/10/2026

S1 reste structure pure : enveloppe 5 racines et 11 champs INCHANGES, `selection.verified_at` fraction optionnelle preservee exactement, distincte d'Agent 2.0.0 six decimales obligatoires. Sources `src/pixs/pa_native/campaign_envelope.py 7d6417b228a50f14a3933aa2b0985d08daed8a1105f29f8b20a91e37ab443b1b` et `tests/unit/test_pa_campaign_envelope.py bc1c8f2d2436116cda062c79c7006efb1fad1033347bc79011224888f61a61ff` ecrites HELD once, NON TESTEES avant ce jalon. Preuves : syntaxe 2 `prt_17a666a85001qCZ6EIt5Zmxxkm`, unittest 43 prevus/executes 43, 0 echec/erreur/ignore en 0.006s `prt_17a6705b5001d4KE8rhKme2xVI`, dependances importees avant/apres empreintes identiques. Corrections avant execution : masquage contexte urlsplit/port from None, distributions vide a la racine, DEL/C1 via json.dumps plus surrogate UTF8, gardes IO mockees autour du vrai parseur avec vue factice os.environ sans lecture reelle, URL exacte DTO, assertRaisesRegex code et frontiere, temoin Unicode annee arabes-indics. Gardes IO et env factice prouvees sans reseau effectif. Aucune compilation native, preuve officielle, admission registre ou raccord S2/S3. Nouvelles relectures PREUVE_SELECTION, RACCORD_ENVELOPPE, DETAIL D-A1/D-A2/D-A3/D-MIG et DEVOPS 234l : choix logiques adoptes non rouverts, realisations physiques et fournisseurs non livres ; acces TPM SSH et outils conserves Cython 3.3.0 et Nuitka 4.3.1, sans nouveau NV/SQL ni qualification d'apres inventaire. Pas d'addition qualif globale aux 503 historiques dont 6 sources modifiees externes ; rapport host 10 separe de l'ancien 9 LXC. Specifications, autres docs et taches non touches, aucune coche. Ce code S1 ne finalise pas le raccord de construction.

## 2026-10-27 UTC — PA01 S2a STRUCTURE SEULE validee operationnellement

- `src/pixs/pa_native/selection_evidence.py` SHA `f0ec856c445e3bd31d4d317339079b4e75de9a7a01c9a5a2cb885a79e35ed115`, preuve ecriture `prt_17bc6b3a1001eJ4752ZQyMWoQm`.
- `tests/unit/test_pa_selection_evidence.py` SHA `192b2945f381318b8f78e1f3f18df49b7895d9cf64f4b3c94ef5d99a8877314d`, preuve ecriture `prt_17bc75da7001WnigVfUq2dgeuw`.
- Syntaxe 2 exit 0 `prt_17bcb67390011pKyKiOMC4C4Sa` ; unittest 45 methodes reelles PASS, 0 echec/erreur/ignore, 0.015s, sortie non tronquee, `prt_17bcc0e1b001KjcOGA7wtIzzsI`.
- 25 dependances avant/apres identiques ; aucun import/recompilation du constructeur natif. Interpreteur venv hote, pas qualification LXC 3.14.9.
- JSON fermes manifeste 8/acquisition 7/fichier 3/admission 8/retrait 7, doublons, encodages UTF-8 invalides, CRLF et constantes JSON non finies refuses ; UTF-8 strict et LF attendus ; ordre/Unicode JSON permis sans nouveau format canonique ; UTC exact sans float, fractions arbitraires, `verified_at` identique textuellement a `finished_at`.
- Decodeurs purs, DTO immuables ; aucun acces IO/env/reseau/processus dans le parseur, gardes avec environnement factice. Admission `ADMITTED` reste donnee non certifiee.
- Aucune verification de provenance officielle, empreinte calculee des fichiers references, autorite reelle, registre complet protege, retrait effectif, collecte/admission, construction native ou PA/PZT. S2b/S3 non realises, P01-P06 et 19V/R/N non executes. Pas de total global qualifie a partir des anciens 503 ou recettes natives externes.
- Incident technique : ancien mandat approuve `req-bda31d81db824cbd9331cf4fefdc75ff` reconcilie et libere NO_EFFECT apres arret OpenCode, aucun Bash envoye ; regles natives reinitialisees 33, MCP 1.10.4 READY retabli. Premier mandat syntaxe `req-e88c261910f0471a976c588623fe3d8a` rejete sans effet (modes write au lieu de read), preuve REJECTED `prt_17bca2149001qCTQ4w8fLgOUCc` ; puis nouveau mandat exact reussi. Les deux nouveaux fichiers sont les seuls fichiers produit ecrits dans cette reprise avant le present ajout V.

## S2b1 — Cohérence des octets figés — 27 octobre 2026 UTC — COHÉRENCE DES OCTETS SEULE

CGPT valide S2b1 COHÉRENCE DES OCTETS SEULE, pas le change. Fixtures synthétiques, aucune provenance ou autorité réelle déduite.

Sources finales : `src/pixs/pa_native/selection_file_consistency.py` SHA `e9b85d6c7117b0635d0f4787189fdeae85a5e2dee2b8dec88f0556725b7aa9dc` ; `tests/unit/test_pa_selection_file_consistency.py` SHA `551e9fb5c9037bf25bb6d4e46b35dd7edb73bec36bb7ad0b2ced6e85a1da3b61`.

Écritures initiales `prt_17be207f5001eviH8Rp3IJI5zK` / `prt_17be2b33f001sqt9wBvw8NnAhW` ; corrections ciblées source/test `prt_17be73c73001cuslB4WmRrvemi` / `prt_17be7da75001L03LzpuKRWy2Ga`.

Preuves finales réelles : syntaxe 2 PASS `prt_17be8d33d001iKNvbBwvgkGCv3` ; 48 méthodes PASS, 0 échec/erreur/ignoré en 0,022 s, sortie non tronquée `prt_17be9780c001FkWelX9ViwpXLH`. 27 dépendances importées, mêmes SHA avant/après. Les 48 remplacent les 47 du même module, ne pas les additionner. Essai 47 initial PASS 0,023 s `prt_17be4ae7d001d7r7U8zuT1D8In` historique : la revue détectait encore l'alias du dict appelant ; ce n'était pas un test échoué. Correction par copie possédée avant lectures, test 48 par mutation réelle de valeur et ajout de clé de l'original autour du VRAI `parse_manifest`, sans thread ni faux résultat.

Réalisation : `parse_manifest` interne, entrées `bytes`/`dict`/`str` exactes, SHA réels sur les mêmes octets, map exacte sans manque ni surplus, liaisons campagne/composant/date exactes, snapshot et distributions en bijection, égalité exacte du verrou entre le profil, l'enveloppe, le manifeste de sélection JSON et pyproject.toml, sans contrôle de la version observée par la sonde dans S2b1. Déclaration Cython originale conservée, variantes casse/espaces/tabulations acceptées, doubles références/URL/extras/conditionnels/contrôles rejetés ; code MISMATCH distinct, diagnostics et erreurs spécifiques conservés, marqueurs réels sans fuite. DTO `frozen`/`slots` de constats seulement. Gardes IO/env factices sur le vrai vérificateur, aucune variable réelle lue.

Limites : pas de sélection PyPI/PEP440/latest/yanked, collecte ou provenance officielle ; pas de chemin physique, d'autorité/admission/retrait courant ou registre protégé ; pas de raccord S3 constructeur/sonde/rapport, pas de compilation native ni effet PA/PZT/SQL/TPM. S2b2/S2b3/S3 et unités B restantes dues ; pas de total global qualifié ni coche 2–10. Choix S1/R1/F1 documentaires pris en compte, détails D-S1/D-R1/D-F1/D-SMIG non validés, aucune implémentation de ces détails.

Validation OpenSpec stricte à relancer après cet ajout ; non déclarée réussie pour cet ajout.

## S2b2 — Sélection sur le snapshot fourni — 27 octobre 2026 UTC — SÉLECTION SUR LE SNAPSHOT FOURNI SEULE

CGPT valide S2b2 SÉLECTION SUR LE SNAPSHOT FOURNI SEULE, pas le change. Fixtures synthétiques, aucune provenance ou autorité réelle déduite.

Sources finales : `src/pixs/pa_native/selection_snapshot.py` SHA `f3291a82d929fd756290a0d2ae082dda9e5cf8d4f1a3921a6c490d7d63ca2037` écrite `prt_17c097e06001DdczCOZEspoC25` ; `tests/unit/test_pa_selection_snapshot.py` SHA `fd54d49d9223e3be6d030d685afd23e91a85142c77e7c2e090dca985b318d64f` écrite `prt_17c0c4b35001ZE1aat1rXnjuzc`.

Preuves finales réelles : syntaxe 2 PASS `prt_17c1626a4001L3oDncUV2aMl1n` ; 56 méthodes réelles PASS, 0 échec/erreur/ignoré en 0,012 s, sortie non tronquée `prt_17c196ce8001sNAURENsXf0dTy` ; 26 dépendances, mêmes SHA avant/après. Le nom `test_yanked_max_skipped` désigne un cas de sélection retirée, pas un test ignoré : les 56 lignes finissent `ok` et le résumé est `OK` sans `skipped`.

Fonction pure `analyze_snapshot(snapshot_bytes, envelope_bytes)` : JSON strict avec doublons/constantes refusés, champs consommés typés et extras PyPI légitimes permis, identité Cython ; classificateur PEP440 en stdlib seule pour finales/post et exclusions pré/dev/local reconnues, ordre et équivalence séparés du libellé, normalisations de casse/espaces/epoch et chiffres ASCII. Éligibilité établie sur fichiers non `yanked` à booléen exact AVANT le choix du maximum ; listes vides ou entièrement retirées non éligibles. Alias équivalents ambigus refusés, sans filtre de cible qui rétrograderait. Sous-ensemble déclaré non vide rapproché exactement sur nom/URL/SHA des métadonnées du maximum ; autres fichiers officiels permis, noms ambigus refusés. SHA calculés des deux entrées snapshot/enveloppe, DTO `frozen`/`slots` de constats seulement, gardes IO/env factices effectives.

Incident : la demande de syntaxe `req-16dbd614fddb4c66824a96ac6e823af5` utilisait le cache `10797` au lieu du `10809` prescrit ; refus avant admission et sans effet, rejet natif CGPT `prt_17c139800001jThKpIYZFSawqA`, puis nouveau mandat exact réussi. Aucun test échoué dans cette demande non exécutée.

Limites : maximum DANS LE SNAPSHOT FOURNI, jamais dernière version actuelle ; aucune collecte, origine ou fraîcheur officielle, autorité, admission, retrait ou registre ; aucun raccord S3 constructeur/sonde/rapport, compilation native ni effet SQL/TPM/PZT. S2b2 ne calcule PAS les octets des distributions : ce contrôle relève du lot distinct S2b1 ; ici seul le rapprochement des métadonnées est exercé. Pas de dépendance, installation, Git, archive, total global qualifié ni coche 2–10. S2b3/S3 et unités B/PUB/FIN indépendantes encore dues ; aucun épuisement présumé. Choix S1/R1/F1 documentaires pris en compte, détails D-S1/D-R1/D-F1/D-SMIG non validés et non implémentés.

Validation OpenSpec stricte de cet ajout à relancer ; non déclarée réussie pour cet ajout.


## S2b3(a) — Cohérence du faisceau donné seule — 27 octobre 2026 UTC

Portée validée : cohérence de documents DONNÉS seuls, pas le change et aucune admission utilisable.

Sources : src/pixs/pa_native/selection_record_consistency.py SHA 08d9cb6c257f5fef10f795a0848eed19503940e71eb884fca3e521d27958ea37 écrite prt_17c368666001kKtOKsV7ovMdia ; tests/unit/test_pa_selection_record_consistency.py SHA 86bd17eb51e7a065d99cd24f874eb4129784e2538cb40b91bdc0a1394210ec44 écrite prt_17c371d9e001OhEPlArOuv7kod.

Preuves : syntaxe 2 PASS prt_17c37fc06001VIqmvG7belfysJ ; 26 méthodes PASS, 0 échec, 0 erreur, 0 ignoré, 0.007s, sortie non tronquée prt_17c389e7d001hqMM1z50yEjE2D ; 26 dépendances importées mêmes SHA avant et après.

Réalisation pure : trois entrées manifest_bytes, admission_bytes et tuple exact d'octets de retraits ; décodeurs S2a et comparaison UTC exacte réutilisés ; identité de campagne manifeste et admission et rattachement des retraits par admission_id ; empreintes SHA réelles des trois familles sans réécriture ; identifiants de retraits uniques dans le faisceau sans restriction entre domaines ; reviewed_at >= verified_at et withdrawn_at >= reviewed_at sans flottant à précision arbitraire ; dates et ordre fourni conservés. Nominal avec 0 ou plusieurs retraits, identifiants égaux entre domaines autorisés ; doublons JSON et formes invalides, UTF-8 invalide et CRLF refusés avec codes distincts ; formats UTF-8 strict et LF attendus ; marqueurs présents dans les vrais documents fautifs et vraies traces capturées dans des blocs d'exception précis ; gardes d'entrées-sorties et environnement factice ; objets figés à cases fixes testés. Un faisceau cohérent PEUT contenir des retraits et le résultat ne porte aucun verdict utilisable, autorisé, actif ou complet.

Limites : documents et références de responsable et d'autorisation DONNÉS, non authentifiés ; liste vide ne prouve aucune absence de retrait hors liste ; pas de vue complète, courante, d'autorité ou de registre physique protégé. Chemin, propriétaire, droits, conservation de l'accord, contexte authentique et atomicité après restauration restent à arrêter et qualifier séparément ; S2b3(b), S2b3(c), S3, collecte et unités fermées avec recette R0 et contrôles indépendants restent dus, aucun épuisement. Pas d'effet de construction, natif, SQL, TPM ou PZT, ni dépendance, installation, Git, archive ou coche 2 à 10 ; pas de total global qualifié. DEVOPS relu intégralement après régénération 06:54:19 UTC : seule date différente, inventaire non qualifiant. Choix S1, R1 et F1 documentaires, détails non validés non implémentés. Validation OpenSpec stricte pour cet ajout à relancer ensuite, non annoncée déjà réussie.


## B-PUB — Codec de forme et octets Python seuls — 27 octobre 2026 UTC

Portée validée : forme et octets du codec B-PUB seuls, pas le change ni signatures cryptographiques ni admission.

Sources : src/pixs/pa_native/bootstrap_prepublication.py SHA 5224f2b9e0d6bb199d191ddb37b5b9e35f46d26cc974f5d33b5537f313ad8baa écrite prt_17c4db13f001tKND94UVsWkiZ2 ; tests/unit/test_pa_native_bootstrap_prepublication.py SHA 0c536b5fa4a455e6eccc000647b061add88ec68671c836c213ad7f3ba308f9f6 écrite prt_17c4e56d00011WDyjVOcQ1CW8U.

Preuves : syntaxe 2 PASS prt_17c51c2090017PnLyplOrM67Lh ; 53 méthodes PASS, 0 échec, 0 erreur, 0 ignoré, 0.031s, sortie non tronquée prt_17c526f37001TDAkwBMma2aof5 ; 6 dépendances importées mêmes SHA avant et après. Native MCP APPROVED exact, HELD, once, fin native et release observés, aucun autre effet.

Réalisation : B-PUB adopté conservé avec DTO 15, document wire 21 dont NV 7 aplati et enveloppe 2 fermée ; PayloadLimits et Resource24 réels explicites ; UTC6 calendrier et fenêtre 0 < span <= max_validity_span_ns ; recoupement des cibles ; clef publique 32 octets et pin SHA256 32 octets cohérents ; signature base64 canonique 88 caractères pour 64 octets ; octets signés avec préfixe PREPUBLICATION exact suivi de LF puis canon ; liaison par SHA256 du canon de l'enveloppe entière. Correctif minimal source : version 1.0.0 du ContentBinding, qui mesure 5 octets, bornée par le PayloadLimits explicite, avec test cap 4 refus et cap 5 acceptation ; document et enveloppe à références courtes acceptent cap 4, la liaison refuse 4 et accepte 5.

Tests : 53 méthodes avec leurs fixtures corrigées avant première exécution avec références courtes, vrais URLsafe sans plus dans SIG_A remplacé par octets synthétiques adéquats, vrais pad bits non canoniques conservant 64 octets, limites et profils forcés de bonne nature d'exceptions, budgets JSON indépendants document et enveloppe avec préconditions Resource24, oracles de canon, octets signés et liaison, types uint, null, doublons, schémas, UTC6, immutabilité et espaces de noms, marqueurs et vraies traces, gardes d'entrées-sorties et environnement factice. Aucune réussite passée inventée pour vieux proposés ; pas d'essai produit échoué sur ce codec.

Écart opérationnel : première décision syntaxe req-9ac7b7682b47430ab96702cc339ec7bf en collision transitoire run-transition-in-flight AVANT décision, GET sans décision puis même identifiant décidé explicitement, aucun nouveau request ni rejouement ; ensuite contrôle exécuté 0. Ne pas transformer en échec syntaxique.

Limites : forme et octets seulement, pas de crypto réelle, clefs privées, ancre de confiance protégée, autorité, fraîcheur, admission, TPM, NV, SQL, PZT, horloge ou deadline JSON. Raccord du module au graphe vers générateur et constructeur non réalisé dans ce lot ; B-FIN, recette R0, plan, provenance, scanner, admission, retrait, vrais raccords et collecte avec registre S2b3b, S2b3c et S3 encore dus, aucun épuisement. Aucune construction native, Git, archive, qualification globale ou coche 2 à 10. Validation OpenSpec stricte pour cet ajout relancée ensuite, pas encore annoncée.


## B-PUB graphe — Composition de métadonnées seule — 27 octobre 2026 UTC

Portée validée : composition de métadonnées du graphe B-PUB seule, pas de compilation, d'artefact ni de change.

Sources : src/pixs/pa_native/generator.py SHA e579d8b3deef54d715816cef0877abe94bc58c47db344a59d3d5386b069192f1 écrite prt_17c642797001yjsbCNEnO1UAVW ; src/pixs/pa_native/builder.py SHA 2598889cca731b052e8575e4730d9520fdbc8e9b152f9281d3942c58c5b018da écrite prt_17c64d9390010OWHVuUBoZYJPK ; tests/unit/test_pa_native_generator.py SHA 86fe9d925590e6205527614d720526f2416a515d50fc6f7af1f8e0e034237b2b écrite prt_17c6584cf001LBShKnBRVYNarr de hash initial 7b598b98c0821dc5a35425cfd82ac5b572e76f0749fb21468897254dca73ac35 puis corrigée prt_17c6d6202001rF3ukX3wTzioeK ; tests/unit/test_pa_native_builder.py SHA b0a2cc8927695771fcf99b8242345b03379fbc397f813a3043098ec5e2c090e4 écrite prt_17c663268001hziCDykmc3od83.

Preuves : syntaxe 4 initiale PASS prt_17c676c04001YZ9qOWHW6RyI7H ; essai 92 initial 0.620s avec 1 échec d'assertion attendue BOOTSTRAP_OBSERVATION contre réelle PA01_OBSERVATION prt_17c6816d6001CuMl37s9GQjsoH, 91 autres réussies. Correction de test seule prt_17c6d6202001rF3ukX3wTzioeK ; syntaxe 1 du fichier corrigé PASS prt_17c6fea66001kqQfO19xdUlvuR ; retest final 92 avec 40 générateur et 52 constructeur dont 6 nouvelles méthodes PASS, 0 échec, 0 erreur, 0 ignoré, 0.658s, sortie non tronquée prt_17c728ff3001X6UyKosz26YE3T. 26 dépendances importées stables. Ces 92 remplacent 86 courants, sans ajouter essai échec ou retest au compte distinct ; aucun total global qualifié pour sources externes anciennes modifiées.

Réalisation : garde unique partagée de composition de prépublication appelée dans l'inventaire vérifié et les précontrôles sources du constructeur avant outils, avec code PA01_BOOTSTRAP_PREPUBLICATION_COMPOSITION_INCOMPLETE. Absence de prépublication avec retour, source et nom réservé canoniques, opérations vides et unicité ; contrats, profil NV 7 et profil de ressources 24 de noms uniques avec rôles consommateurs couverts. Codec public donc union et rôle PZT admis, sans restriction système inventée, anciennes gardes privées intactes. Fixture d'alias non réservée et hachée atteignant la nouvelle garde, sans échec masquant de politique ; refus avant processus enfant et nominaux limités à outil indisponible en fixture, aucun outil réel.

Limites : sources et objets ELF synthétiques, aucune Cython, objet, liaison, produit natif qualifié ou effet NV, SQL, PZT, crypto, autorité ou admission. B-FIN, recette R0, plan, provenance, scanner, admission, retrait et S2b3b, S2b3c, S3 avec collecte restent dus, aucun épuisement. Aucun Git, archive, profil, valeur de production nouvelle ou coche 2 à 10. Validation OpenSpec stricte pour cet ajout relancée ensuite, pas encore annoncée.

### PA01 B-RECIPE — FORME ET LIAISONS AUX OBJETS FOURNIS SEULE

Portée : codec `BootstrapRecipe` + 22 tests, forme JSON stricte et liaisons
`PayloadLimits` / `BootstrapBase` / `BootstrapResourceProfile` fournis.
Aucune autorité, provenance, exécution, registre protégé ni qualification native.

Sources :
- `src/pixs/pa_native/bootstrap_recipe.py` SHA256 `696b19219b628679779af22abc3d8cf45af9b3c3a58b41f292348e66d5635845`, écriture `prt_17cd301fe001LLwrzgRHxs6wWM`.
- `tests/unit/test_pa_native_bootstrap_recipe.py` SHA256 `e03c1f1a8c8e8a760cd2b6121335b6d388528042501ed9338422fd44ad761d57`, écriture `prt_17cd390ca0016qw2u7pxbMiIIX`.

Vérifications :
- Syntaxe ciblée 2 fichiers : `prt_17cd45ff7001iMIdBxhZ8MtiZt`.
- Unité `tests.unit.test_pa_native_bootstrap_recipe` : `prt_17cd4eb3d001woCj91h3TXRNbu`, 22 méthodes, 0 échec, 0 erreur, 0 ignoré, 0.009s, non tronqué.
- 9 dépendances stables relues, non modifiées.

Règles prouvées :
- Pinning4 : `registry_ref`, `registry_generation_ref`, `epoch`, `sequence` égaux au `Resource24` fourni, plus plafonds `max_epoch/max_sequence`.
- Base : `encode_bootstrap_base` + égalité `bootstrap_base_binding`, altération contenue refusée.
- SHA : `SHA256(CANON recette entière)`, `recipe_binding {ref,version,sha256}` hors document, `recipe_version` externe distincte `schema_version`.
- Caps `Resource24` : `max_correlation_refs/max_causation_refs` effectivement utilisés par `Recipe`, refus `+1` chacun ; `PayloadLimits.max_observation_refs` non réemployé.
- Limites `PayloadLimits` : `max_json_bytes/max_ref_bytes` + oracle document exact `size` passe / `size-1` échoue recette seule.

Incident : demande initiale sans `timeout_seconds` rejetée `prt_17cd058c7001dQ66nosY5eNrJS`, sans fichier écrit ni effet, jamais rejouée ; reprise par mandats inédits exacts avec `timeout_seconds:45`.
Corrections de fixtures `UINT64_MAX`, `cap2/cap3`, plafond 106o, `epoch0/sequence0` explicites effectuées AVANT première exécution ; aucun test produit échoué pour ce codec.

Reste dû : graphe Recipe non raccordé, `Plan15/Provenance28/B-FIN/R0`, registre protégé `S2b3b/c/S3`, sans global/natif/autorité/SQL/TPM/PZT ni coche.
Validation OpenSpec stricte de cet ajout à exécuter ensuite, non prétendue passée ; `VALIDATION.md` courant conservé `edd063bfef5dd39136cf0ce7f317a6dcb9c48e735802f612fc17d20a1ed651fb`.
Aucun nouveau format/profil/détail `D-S1/D-R1/D-F1/D-SMIG`.

### PA01 B-RECIPE graphe — COMPOSITION DE MÉTADONNÉES SEULE

Portée : raccord `Recipe13` au générateur et constructeur, garde partagée
avant outil, sans exécution, compilation, provenance ou qualification native.

Sources :
- `src/pixs/pa_native/generator.py` SHA256 `f7c1dbe8b6261613511a48570c6ea3c57cdda0ab5ad3c6aff253f6e73e76b6de`, écriture `prt_17cdbd77c0014pM4c4ygHlR7kX`.
- `src/pixs/pa_native/builder.py` SHA256 `a64a854fad26fbdae1da1255e60053d2d6989b2701a2c26e8c97f4c3d5d1a1ac`, écriture `prt_17cdc6752001nghkZcz326Z4SX`.
- `tests/unit/test_pa_native_generator.py` SHA256 `cbe9ba9a0c5c5602041a6d227979b55ff821cc54ac840f830cac1c2985fd13f8`, écriture `prt_17cdd05bc001T8OhLEJmTI08v6`.
- `tests/unit/test_pa_native_builder.py` SHA256 `632c5e3825dbd8ad69f32ed2c345995d3b25833c4985ec06f0e151c3c597d9df`, écriture `prt_17cdd9bc8001gsRd4rYp0IBB0G`.

Vérifications :
- Syntaxe ciblée 4 fichiers : `prt_17cde84b9001XUv0DQ5q43XXH1`.
- Unité générateur + constructeur : `prt_17cdf60cf001w8n3gnpYP0sWgo`, 98 méthodes dont 43 + 55 avec 6 nouvelles, 0 échec, 0 erreur, 0 ignoré, 0.66s, non tronqué.
- 98 remplace 92 du même périmètre, sans additionner ; 26 dépendances stables ; aucune réussite globale ou native.
- Garde `Recipe` partagée appelée générateur/constructeur avant outil, détection par source canonique OU nom réservé puis exigence des DEUX canoniques, unicité et opérations vides, dépendances `PG/Base/Resource` couvrant rôles publics et `PZT`, anciennes gardes transitives inchangées.
- Cas isolés atteignent nouvelle garde, anciennes erreurs `Context` corrigées en proposition AVANT première exécution ; aucun test produit échoué pour ce lot.
- Fixtures sources et faux `ELF`, `Popen` simulé, nominal `TOOL_UNAVAILABLE` ne prouve pas compilation.

Reste dû : `Plan15/Provenance28/B-FIN/R0`, scanner, admission, retrait, registre `S2b3b/c/S3`, sans épuisement, coche, `Git` ou archive.
Validation OpenSpec stricte de cet ajout encore à exécuter ; `VALIDATION.md` courant conservé `965b9ca02d4e59b2020eeb33a8f93874cc0e8d4ae614633b5c5a2f98f23b2f82`.

### PA01 B-PLAN — FORME ET LIAISONS AUX PRODUCTEURS FOURNIS SEULE

Portée : codec `BootstrapPlan` + 22 tests, forme JSON stricte et liaisons
`PayloadLimits` / enveloppe `B-PUB` entière / `Policy14` / `Resource24` /
`Context8` / `Base8` / `Recipe13` embarquée. Aucune autorité, exécution,
admission, preuve matérielle ou qualification native.

Sources :
- `src/pixs/pa_native/bootstrap_plan.py` SHA256 `445a38f635ec81800702c0936b260ea1473ff71de39c64f5807ef9b5d5fbfa66`, écriture `prt_17cecbff9001IqG4PMM1x6MFyQ`.
- `tests/unit/test_pa_native_bootstrap_plan.py` SHA256 `3b085ca8e0dd570cc3f136808a05781d3efd225afc07d8399ef383c756fc74b6`, écriture `prt_17ced992f001m2EUb7u6rXjkia`.

Vérifications :
- Syntaxe ciblée 2 fichiers : `prt_17cf0bc40001qVzSAF1rWfpxSp`.
- Unité `tests.unit.test_pa_native_bootstrap_plan` : `prt_17cf15861001UNQmQtDAxzwhwn`, 22 méthodes, 0 échec, 0 erreur, 0 ignoré, 0.055s, non tronqué.
- 12 dépendances stables relues, non modifiées ; pas de total global.
- Binding `ref=plan_ref`, `version=plan_version` opaque externe, `sha256=SHA256(CANON plan entier)` hors document.
- 4 liens connus vérifiés entiers `ref/version/SHA` : `PUB` enveloppe entière signée, `Policy`, `Resource`, `Context` ; `Recipe13`/`Base8`/`NV7`/cibles/contextes cohérents aux objets fournis.
- 3 liens `authority/procedure/executor` opaques, formes seules, aucune autorité.
- Corrections imports `builtin`, fixtures, tautologie retirée et oracle budget effectuées AVANT première exécution 22 ; aucun test produit échoué pour ce lot.
- Incident demande syntaxe à manifeste divergent : erreur native `prt_17cee0bf7001Wu5dIF8vFheoL1`, puis même ID rejeté CGPT sans effet `prt_17cee1b2e00105gh1uky3ve3Lp`, sources préservées, nouvelle demande exacte et syntaxe réussie ; pas une erreur syntaxique.
- `readiness` réconcilié `prt_17cf022cb001KFgtXRvbZ5oRaG`.

Reste dû : graphe `Plan` non raccordé, `Provenance28/B-FIN/R0`, scanner, collecte, admission, retrait, registre `S2b3b/c/S3`, sans épuisement, coche, natif, `SQL/TPM/PZT`, crypto, `Git` ou archive.
Validation OpenSpec stricte de cet ajout à exécuter ensuite, non prétendue passée ; `VALIDATION.md` courant conservé `b3599c3565d5174a1783031ef4c00bfe0c99450e3b97735754089882637b29bc`.

### PA01 B-PLAN GRAPHE — COMPOSITION DE MÉTADONNÉES SEULE

Portée : garde `BootstrapPlan` partagée générateur/constructeur + 6 nouvelles méthodes, sans compilation ni qualification native.

Sources :
- `src/pixs/pa_native/generator.py` SHA256 `a9cb90a7bd6dd2153004baea1193ae6c1ba9e5f6fa3604a19b92bddeaaa780f2`, écriture `prt_17cf8b94c0012wXeyCQwjzaAh9`.
- `src/pixs/pa_native/builder.py` SHA256 `695ef0eb156e31cee5ac1ae322db7589d8b93c2ec2062d819adbd165f21a9951`, écriture `prt_17cf95fea001Hu8P3phf3ly6LA`.
- `tests/unit/test_pa_native_generator.py` SHA256 `f68b4226701212eddfddceda8c54fe7632cbfd0dab3678231d616b810d6a33c7`, écriture `prt_17cf9ed56001CxNlwTvdQ7ISnU`.
- `tests/unit/test_pa_native_builder.py` SHA256 `5139da2063aaca7db57c0b45d33bd8761914226faf5f4823dc33daff343885f1`, écriture `prt_17cfa836d001jqvlhG7XgcnXQ7`.

Vérifications :
- Syntaxe ciblée 4 fichiers : `prt_17cfb5781001K8q6i4ihjJ732v`.
- Unité générateur + constructeur : `prt_17cfbef320013PmMxjglAfKU0C`, 104 méthodes `46+58` dont 6 nouvelles, 0 échec, 0 erreur, 0 ignoré, 0.744s, non tronqué, résultats réels.
- 26 dépendances stables relues, non modifiées ; 104 REMPLACE 98 dans même périmètre sans addition et aucun total global.
- Garde Plan partagée avant outils, détection source OU module réservé puis couple canonique unique et opérations vides, 8 dépendances directes `PG/Base/Context/NV/Policy/PUB/Recipe/Resource` couvrant chaque rôle Plan, `INIT` transitif via `Base` gardes conservées, public/`PZT`/union sans `System-only`.
- Fixtures `INIT` corrigées avant première exécution, zéro test produit échoué.
- Nouveaux refus Plan distingués des anciens `Context/Base/Policy/Recipe`, `Popen` mock non appelé/`TOOL_UNAVAILABLE`/faux `ELF` métadonnées : pas compilation ni qualification native.

Reste dû : `Provenance28/B-FIN/R0`, scanner, collecte, admission, retrait, registre `S2b3b/c/S3`, sans épuisement, `Git`, archive, coche, `SQL/TPM/PZT`, crypto.
Validation OpenSpec stricte après ajout encore à exécuter, non prétendue passée ; `VALIDATION.md` courant conservé `9900ccdfe54211f7880637ba29eafef463fcb58587d5bff1f9d48664a217dd1c`.

### PA01 B-R0 — FORME, LIAISONS, RECONSTITUTION ET CALCULS ATTENDUS SEULS

Portée : codec `BootstrapInitialRecord` 7 API aux 8 kwargs réels obligatoires, 19 champs déterministes depuis `Plan+Recipe/Base`, sans journal réel, `HMAC`, `Extend`, signature cryptographique vérifiée (SHA256 attendus calculés), autorité observée, `TPM/SQL/PZT` ni qualification native.

Sources :
- `src/pixs/pa_native/bootstrap_initial_record.py` SHA256 `a51df456453f866d758d9f3d2d9cca532fe5d3ff5f8c1140be9c4338b9ab85da`, écriture `prt_17d1b92b0001NcpYWLXuCZ9Mkv`.
- `tests/unit/test_pa_native_bootstrap_initial_record.py` SHA256 `c3680a3505f48774aa84c3db4018233b2f760a65952ca459ba9d05a52fe5be4f`, écriture `prt_17d1cecf60010LdG1Kh73Nh2TX`.

Vérifications :
- Syntaxe ciblée 2 fichiers : `prt_17d1dff09001Hqp6wVlPYQaIAf`.
- Unité `tests.unit.test_pa_native_bootstrap_initial_record` : `prt_17d1eb04e001SalVRMlRsfIR0W`, 15 méthodes, 0 échec, 0 erreur, 0 ignoré, 0.177s, non tronqué.
- 13 dépendances stables relues, non modifiées ; aucun compte global.
- 19 champs reconstitués depuis `Plan+plan.recipe`, bindings `Plan/Recipe` recalculés en interne, limites producteurs distinctes R0 `min(r0_limits.max_json_bytes/Resource.payload_max_json_bytes/Resource.max_record)` et refs `min(r0_limits.max_ref_bytes/Resource.payload_max_ref_bytes)` ; gros Plan accepté avec petit record, zéro `epoch/seq`/plafonds EXPLICITES, `bool==0/1` refusé même après mutation, `unknown/duplicate`/types/`UTF8` oracles réels.
- Binding `ref=transition_ref`, `version=schema_version`, `sha256=SHA256(CANON)` hors document ; tête `SHA256(ASCII PIXS:PA:BOOTSTRAP:INITIAL_RECORD:1.0.0 + LF + CANON)` ; reçu physique attendu `SHA256(ASCII PIXS:PA:JOURNAL:RECORD:1.0.0 + LF + 32 zéros prédécesseur DE TRAME + uint32BE(len) + payload)` ; NV attendu `SHA256(Base32 || têteB32)` ; 3 préimages distinctes sans inégalité de hashs.
- Corrections des propositions/fixtures AVANT première exécution 15, aucun essai test produit échoué.
- Détails `D-S1/D-R1/D-F1/D-SMIG` ADOPTÉS DOCUMENTAIREMENT relus, strict courant `prt_17d0a5f540016rmVHIk2fZC3KK`, 17 exigences 34 scénarios deltas NON SYNCHRONISÉS, réalisations/preuves manquantes et `P-SRF01..18` NON EXÉCUTÉS, sans implémentation de ces détails dans R0.

Reste dû : graphe R0 non raccordé, scanner, `Provenance28/B-FIN`, collecte, admission, retrait, registre `S2b3b/c/S3`, sans épuisement, coche, `Git` ou archive.
Validation OpenSpec stricte de cet ajout à exécuter ensuite, non prétendue passée ; `VALIDATION.md` courant conservé `802086ded9698a7c8a68378f6802be39a3717e87f870f16cc79545044966d0b8`.

### PA01 B-R0 graphe — composition métadonnées seule (110 méthodes)

- Sources écrites (contenus relus CGPT, snapshot courant) :
  - `src/pixs/pa_native/generator.py` `dc040c87afa9a7721b9527afc8c767267ac52afaa7ead58123433241dd7d4245` preuve `prt_17d30f774001EvYFrmqaQOPscs`
  - `src/pixs/pa_native/builder.py` `89ca0736a8d6a4ae4bf361ea225c92ed5b09cfeda44f8ac7bb0d7743c50dfa38` preuve `prt_17d319ba5001CL12wq4BS4VEpR`
  - `tests/unit/test_pa_native_generator.py` `8ed78677af57832c753a05d9acd40b1d01d394288464b6786fd2c94432824d09` preuve `prt_17d323f0a0012pkHNv466zu0KM`
  - `tests/unit/test_pa_native_builder.py` `13b2f8caeb2e22fa43ce8194b4470d853e337df713789420078b5be6d0df21d8` preuve `prt_17d32da81001haRnUpD0YiN3Rz`
- Syntaxe ciblée 4 fichiers : PASS preuve `prt_17d33fd1b001DxooGW3bW5cYa9`.
- Unitaire : `110 PASS (49 générateur + 61 constructeur, dont 6 nouvelles R0)`, `0.894s`, `failures 0 / errors 0 / skipped 0 / truncated false`, preuve `prt_17d34a6c9001jiqEwb6baWq3h2`, `26 dépendances stables`.
- `110 REMPLACE 104`, même périmètre graphe, pas d’addition globale.
- Garde partagée `_check_bootstrap_initial_record_composition` après Plan dans les deux chemins avant outils, code `PA01_BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE` ; 9 imports `PG/Base/Context/NV/Plan/Policy/PUB/Recipe/Resource` canoniques uniques, rôles couvrants public PZT/union ; détection source OU module puis deux canoniques/unicité/ops vides ; INIT transitif, gardes anciennes inchangées ; helper `plan_graph` réutilisé.
- Refus nouveaux : R0 isolé sans PG, Plan manquant, Plan non couvrant, alias `initial_record_alias_fixture.py`, autres défauts antérieurs exacts ; Builder `Popen` mock not called / `ToolUnavailable`, générateur ELF synthétique seul ; pas de compilation/qualif native.
- Lecture code agent depuis snapshot courant 4 fichiers et SHA fournis CGPT, outil `read` natif OC non exposé ; ne prétend pas `read` natif OC exécuté.
- Autorat deltas OpenCode, relus CGPT inchangés ; aucun incident produit / test échoué pour ce lot.
- Reste : scanner mixte, Provenance28, B-FIN, registre `S2b3b/c/S3`, collecte/admission/retrait/fournisseurs réels ; pas d’épuisement/coche/Git/archive ni SQL/TPM/PZT effectif.
- D-S1/R1/F1/SMIG adoptés documentairement seuls, non synchronisés, preuves manquantes, pas de réalisation déduite.
- Strict de cet ajout encore à exécuter ; `VALIDATION.md` courante `0392630e45ce1de686199a5c251b68a26abf5467854147c6a5a9d91bd5a0343d`.

### PA01 B-HISTORY scanner — comparaison d’octets fournis et maths seule (14 méthodes)

- Sources écrites (snapshot CGPT, `read` OC non exposé, aucun `native read` prétendu) :
  - `src/pixs/pa_native/bootstrap_history.py` `2dde7c1f63c1bf30370fd866cc132fe06f0db4ce8896fe284aa9f1b046419983` preuve `prt_17d4e5d7e0019EdAtj7A3cvSMC`
  - `tests/unit/test_pa_native_bootstrap_history.py` `e80c16efe0bac0aa939a614feb847b5d73867b73da0a150e08f0d79cb0d75646` preuve `prt_17d4f0c41001QrzvF9CKw6HqfJ`
- Syntaxe ciblée 2 fichiers : PASS preuve `prt_17d5023890011YFN3DUQy7df46`.
- Unitaire : `14 PASS 0.408s`, `failures 0 / errors 0 / skipped 0 / truncated false`, preuve `prt_17d50d1fd001wrz4PJv16mqbNb`, `15 dépendances stables` dont fixture R0 réelle importée explicitement ; aucune agrégation globale.
- Byte exact journal `header22/frames uint32 len/SHA chain/EOF/caps avant copies` ; R0 reconstitué depuis vrais `Plan/Recipe/Base` et comparé `CANON` littéral, puis PG1.0 `decode/encode` publics normes inchangées / `canon byte exact` ; `contexte5/seq+1 sans overflow/transrefs uniques/previous head+NV/tail NV FOURNI comparé ATTENDU` ; B seul `NV_B`, PG tail dernier pas ancienne Base.
- `0/7/MAX`, snapshots TPM pas lus, `no IO`, pas d’autogenèse/migration/réinitialisation ni adoption par candidat, pas d’antirecréation physique/provenance authentique prétendue ; canon PG source inchangé.
- Tests : propositions vides/skip/défauts budgets masqués corrigés AVANT PREMIÈRE EXÉCUTION 14, pas de produit `UnitTest` échoué ; reçus physiques recalculés pour les cas sémantiques, données synthétiques sans journal réel ; snapshot public CGPT + fixture R0 `c368…` reçus.
- Reste : graphe scanner pas raccordé, Provenance28/B-FIN, collecte/admission/retrait registre `S2b3b/c/S3` et vrais fournisseurs encore dus ; pas d’épuisement/coche/Git/archive/native qualified/SQL/TPM/PZT effet/D-S1 new code ; détails adoptés doc seuls NON sync, preuves manquantes.
- Strict de cet ajout encore à exécuter ; `VALIDATION.md` courante `925b3c31959b2a6d46d839bea55f9b9f4f3d680aacf803b4c2fd2af2f2087efc`.

### Graphe Scanner History — 116 PASS 52+64 dont 6 nouvelles / 0.894s / 26 deps stables — 2026-10-27 — COMPOSITION DE MÉTADONNÉES SEULE — REMPLACE 110 même périmètre
- Sources : `src/pixs/pa_native/generator.py c56dea1606028e23bec8fa509540f55c43784dda71145d94792ad9e2323b4cf9 prt_17d58ac450017ua8vyLW6SPLtg` ; `src/pixs/pa_native/builder.py 53d537421c586bbc8dfc39406ff07b47f935924fbb79bc985e0d8b8bbe8e6520 prt_17d596443001o2eZxR86PCPZHN` ; `tests/unit/test_pa_native_generator.py b69855160cc7599567b4f35bf44c7df270f67136ed58daa715a7085c90a0271f prt_17d5a1d9e0016pCbhg9i5VNJUZ` ; `tests/unit/test_pa_native_builder.py 9d6b5ef78d8d9f05c8af3b5ba617d978716acb3a6210264c8931f804b44c42cb prt_17d5ae8f7001XEt9E6zbH5mwwo`.
- Preuves : syntaxe 4 `prt_17d5bbeed001CTpIvpdwIIGds3` ; unité `116 distinct 52+64 dont 6 nouvelles failures 0 errors 0 skipped 0 truncated false 0.894s prt_17d5c8477001vtJ7rEB9AubGoK` ; deps 26 stables ; base `VALIDATION b92a71a22452bd8b5a7161a4b82ca466e48fa1c391072f4ea2be58d262fa8144`.
- Garde partagée History après R0 dans deux voies avant outils, 8 deps directes `PG/Base/Context/R0/Plan/Policy/PUB/Resource` rôles publics ; détection source OU module puis canonique unique / `operations==()` , anciennes gardes Plan/R0 inchangées.
- Helpers `plan_graph` et fixture R0 réel réutilisés ; faux ELF / `Popen not called`, aucune compilation native.
- Propositions tests vides précédentes jamais exécutées ; 14 tests complets ensuite corrigés avant première exécution, aucun test produit échoué.
- Détails `D-S1/R1/F1/SMIG` adoptés doc seuls / non sync / preuves manquantes.
- Reste `Provenance28/B-FIN/collecte/admission/retrait/S2b3b/S3`, sans global/épuisement/coche/Git/archive.
- Strict de cet ajout à exécuter ensuite.

### PA01 Provenance28 — formes, liaisons et calculs attendus sur données fournies — 22 PASS / 0.902s — 2026-10-29
- Source : `src/pixs/pa_native/bootstrap_provenance.py` SHA `bd31971315058d32e03f333628985b44ed42e297df14778e6a1f9c26aa6fa997`, 969 lignes, DTO 28 champs, NV 6 champs, 12 paramètres contexte keyword-only.
- Test : `tests/unit/test_pa_native_bootstrap_provenance.py` SHA `dd3542ba2b89a3f7c9e2e619ef4be8402084f9f0d6e786863bea6bca4f4a28d9`, 537 lignes, 22 méthodes distinctes de ce seul module ; aucun total avec les 116 graphes.
- Preuves natives : écriture source `call_01a186daf0cd719b977094f685ec422b` completed `opencode-go/muse-spark-1.3-contributor/medium` conforme au SHA source ; écriture test `call_01a186dfff247429b248eb320943d34a` completed conforme au SHA du test `dd3542ba`, distinct du SHA source ; syntaxe `call_01a186e61138710ba96ee34c3d41b796` exit 0 sans sortie ; unités `call_01a186eadd53701b8ce7e911157e3280` exit 0, 22 pass, 0 failures, 0 errors, 0 skipped, 0.902s, première exécution, sortie 22 lignes `ok`.
- Fichiers et propositions produits et corrigés par OC AVANT première exécution 22 ; aucun test produit échoué. Aucune autorité ni observation réelle déduite du mot provenance ; sans collecteur, HMAC/TPM/SQL/PZT, signature vérifiée, graphe ni B-FIN ; sans coche globale, livraison, Git, archive, qualification native ou admission.
- Dépendances : 33 stables au contrôle post-tests daté ; `AGENTS.md`/`ORCHESTRATED_CODING.md` modifiés extérieurement ensuite et relus, sans modification du code ni des contrats Provenance ; ne pas déclarer 33 stables courants sans recontrôle.
- Caches avant : `src/pixs/pa_native/__pycache__/bootstrap_provenance.cpython-314.pyc` absent, `tests/unit/__pycache__/test_pa_native_bootstrap_provenance.cpython-314.pyc` absent ; deux pyc générés par ce seul lot puis nettoyage effectué exit 0, deux pyc absents vérifiés, preuve native `call_01a18732bdd476e9811d68da3f489fe3`, accès RELEASED.
- Reste après cet ajout : strict OpenSpec ciblé sur documents finaux ; nettoyage déjà effectué.
- Base `VALIDATION 63c0a166a4740a9f135536e41e02d107ca08dfd7c4b58d00c38aa413af954601`.
- Strict de cet ajout à exécuter ensuite.

### Graphe Provenance — composition métadonnées seule — 122 PASS / 0.918s — 2026-10-29
- `src/pixs/pa_native/generator.py` SHA `5584956298637b276066643ba062bb3cf39c27fca078f273b6f3ba981cbc2727` `call_01a1875f36237458bd5af96ff0833e77` ; `src/pixs/pa_native/builder.py` SHA `bc4b19b49ed175bb1116bb1dfb63c01f6c7ccdd23bc8adaefec968f12b5e56a7` `call_01a1876071b873b2ac06370eab4da0af`.
- `tests/unit/test_pa_native_generator.py` SHA `682d491f7b089307d1a28b1b12d4fb55c362136b2f470f448ce6f05a34223991` `call_01a18761b0f770b492b74c0a8805f8b9` ; `tests/unit/test_pa_native_builder.py` SHA `1644bd212463d0dc063d42cf232edc3dc488f47fb83ccceb64b8d89366ed7403` `call_01a18763691b7378a54ab0abd938aca2`.
- 122 REMPLACE 116 sur même périmètre (55+67, +6) ; ne s’additionne pas aux 22 Provenance ; 116 anciennes conservées, 6 ajoutées avant première exécution, 2 corrections avant écriture, aucun test produit échoué.
- Syntaxe `call_01a18765704f77de8527dd6f177c5e23` exit 0 py_compile 4 fichiers ; unités `call_01a18766972f72bfb40f5bd3ccb8f0f9` exit 0, 122 pass, 0 fail/error/skip, sortie complète.
- Garde partagée 11 imports directs/rôles System/PZT/union avant outils, History non requise, coexistence séparée ; sans TPM/SQL/PZT effectif, collecte, signature, B-FIN, qualification native ou admission.
- ELF synthétiques pour seules métadonnées ; builder Popen mocké `assert_not_called`, aucune compilation native qualifiée ; 42 dépendances stables, `output/tests/pa01-generator|builder` vides ; 4 pyc générés puis nettoyage `call_01a18767d6f1732dbaf68e3c396e31f8` exit 0, absence vérifiée.
- Base `VALIDATION 6a2ff50bd690407fab595dc3e8f9ece4db5b6522bec0b6248a5434dbd82d7cf5` conservée ; pas de coche globale/épuisement/Git/archive ; reste B-FIN puis unités indépendantes, collecte/admission/retrait/raccords/S2b3b-c-S3.
- Strict documentaire de cet ajout à exécuter ensuite.

### B-FIN — contrôles ciblés de forme et liaisons — 35 PASS — 2026-10-29
- Constat `2026-10-29T13:06:43.129453+00:00` : `PASS_35_FORMES_LIAISONS_DONNEES_SEULES`, 35 méthodes en 1.136s, 0 échec/erreur/skip, sortie complète non tronquée, `call_01a187c1dc9f71a18550f3878e5fd468` exit 0 ; première vraie exécution réussie, aucun test produit échoué.
- Codec 18 champs / contexte 5 / enveloppe 2, 6 API publiques et 14 kwargs obligatoires, familles `fin/provenance/producer` séparées ; 4 bindings recalculés, tête/séquence/contexte R0 rapprochés ; fenêtres FIN incluses dans PUB/POLICY, observations historiques égales à Provenance, span entier ; signature 64 octets de forme et octets à signer distincts de la liaison sur enveloppe entière.
- Fichiers : `src/pixs/pa_native/bootstrap_publication.py` 622l SHA `62b477669edec9b5646311d42a9d88379fcf9c351b4950a4f947f0967cbf294f` (`call_01a187ab22d67488b56953ea9efcba59`) ; `tests/unit/test_pa_native_bootstrap_publication.py` 560l SHA `cbfa4ef7a58f2ca7f17893de1d4cd19a109e330cb323bba0fc4d7583ca5ee6c2` (`call_01a187bc213872278448a0f22805aa42`).
- Syntaxe `call_01a187bf543e70d9a7983079c3774320` exit 0 non tronquée ; nettoyage `call_01a187c8278d76e2a41f92199bb4da94` exit 0, 2 pyc absents vérifiés : `src/pixs/pa_native/__pycache__/bootstrap_publication.cpython-314.pyc`, `tests/unit/__pycache__/test_pa_native_bootstrap_publication.cpython-314.pyc`.
- Base `VALIDATION.md` avant ajout : `66cabb68954c41da07d823944f9e3f298902d2090642b9ae004256337b385dcc` ; ces 35 restent distincts des 122 graphes, sans total global prétendu.
- Propositions factices refusées avant écriture/exécution : corrections statiques seules, exception `ifFalse`/`generator.throw` refusée jamais écrite ni exécutée, 35 méthodes réelles sans skip.
- Fraîcheur : source créée avant recontrôle de 2 références externes, puis 65 empreintes contrôlées par le pilote avant commande et recoupées stables après unité, `changed: []` après tests ; PZT diff exact RFC2119, ancien PROJECT intégral non recouvré, aucun diff exhaustif prétendu, absence de contradiction observée, aucun correctif source.
- Portée : pas de vérification de signature ni de provenance authentifiée prouvée par ce lot ; même limite pour autorité, admission et effets matériels (TPM/SQL/PZT/compilation native), adoptions humaines du 26/10 acquises.
- Reste : graphe FIN, admission/retrait/registre et vrais producteurs/raccords, sans épuisement, coches 2-10, Git ou archive ; Map puis strict sur documents finaux requis ensuite, non encore exécutés.

### Graphe FIN — fermeture Publication — 128 PASS — 2026-10-29
- Constat `2026-10-29T15:03:40.197992+00:00` : `128=58+70` en 1.125s, 0 échec/erreur/skip, sortie complète non tronquée, `call_01a1882f2fef7095990752630385c5ff` exit 0 ; première vraie exécution réussie, aucun test produit échoué.
- Garde partagée `PUBLICATION` après Provenance dans `generator.py`/`builder.py`, 10 dépendances directes canoniques, présence optionnelle, source OU module réservé, unicité canonique et `operations==()`, couverture rôles System/PZT/union ; History non requis comme dépendance, anciens codes `CONTEXT/R0/PROVENANCE/OBSERVATION` préservés.
- Fichiers : `src/pixs/pa_native/generator.py` 674l SHA `8a6685d1ca37707aa77cc186118433c2c86524a8d3a7ae79ba7b31b5f5a84a2d` (`call_01a18822ec14777aa6a0905703809f42`, `call_01a18824f8c473e3a498d32ab2e14f93`) ; `src/pixs/pa_native/builder.py` 595l SHA `0374458c2c5e79c17677bd16f9ab0d6b911452bfb5486478531b780487b86515` (`call_01a1882726a770e88644785e7cd7016c`, `call_01a18828cc8e70dfb2aa23cd705ed147`).
- Tests : `tests/unit/test_pa_native_generator.py` 1256l 58 méthodes SHA `6d467465fe3aa8b3aefd6fb5bbc81d79f4ec572eff06c967f388160a4055bae9` (`call_01a1882a4eed72d6bd1fb87f1a6f3283`) ; `tests/unit/test_pa_native_builder.py` 948l 70 méthodes SHA `a263819e9947f2b0048fa7dcd10caa93af0ff0ffd97a72a9dbc6d162b411640a` (`call_01a1882bea7470689bc13e944fe63f20`).
- Correction avant première exécution : cas Plan absent conserve R0 présent, `_check_bootstrap_initial_record_composition` avant Provenance, première erreur `BOOTSTRAP_INITIAL_RECORD_COMPOSITION_INCOMPLETE` comme suite Provenance existante.
- Syntaxe `call_01a1882da30676db987b9331a44f20be` exit 0 non tronquée ; 74 empreintes contrôlées stables, `changed: []`, `output/tests/pa01-generator|builder` vides ; ELF synthétiques et Popen mock non qualificatifs, sans Cython/link/native/admission/TPM/SQL/PZT/signature réelle.
- Nettoyage `call_01a18833f0e27584bb8a7cdeacc22838` exit 0, 4 pyc absents vérifiés : `src/pixs/pa_native/__pycache__/generator.cpython-314.pyc`, `src/pixs/pa_native/__pycache__/builder.cpython-314.pyc`, `tests/unit/__pycache__/test_pa_native_generator.cpython-314.pyc`, `tests/unit/__pycache__/test_pa_native_builder.cpython-314.pyc`.
- Base `VALIDATION.md` avant ajout : `15f8112785a9b9a641fe9948093e1fafb3cc1607058eef78bab646faa01aaa5f` ; ces 128 REMPLACENT 122 (55+67), sans addition aux 35 codec ni aux 22 Provenance.
- Portée : pas de qualification native ni admission prouvée ; mêmes limites TPM/SQL/PZT/compilation/livraison/activation, aucun correctif source.
- Reste : admission/retrait/registre et vrais producteurs/raccords à examiner, sans épuisement, coches 2-10, Git ou archive ; Map puis strict sur documents finaux requis ensuite, non encore exécutés.

### WithdrawalPlan16 — forme seule 16 champs — 48 PASS — 2026-10-29
- Fichiers : `src/pixs/pa_native/withdrawal_plan.py` 319l SHA `b58cd04244ad6159367bfe0473d76e0971a7ee10f650085390f386ebbb77d020` ; `tests/unit/test_pa_withdrawal_plan.py` 453l SHA `8347d9dde0b2a615e9346053959326821c4c3693026d4092ef8aed8b1b517120` 48 méthodes, écrits natifs HELD distincts, fidèles contenus relus.
- Preuves : syntaxe 2 exit 0 ; unité 48 PASS 0 fail/error/skip en 0.004s sortie complète 48 identifiants uniques ; 76 empreintes stables recoupées ; cleanup 2 exit 0 absences vérifiées.
- Réalisation : DTO 16 champs fermés, PayloadLimits PG externe réutilisé 3 champs sans nouveau profil, 3 API `encode/decode/binding` limites explicites, ContentBinding `{ref,version,sha256}` bornés, CANON `sort_keys/separators` UTF-8 octets, `{ref:plan_ref,version:plan_version,sha256:SHA256(CANON(plan entier))}` hors document, wildcards `* ? [ ]` refusés installation/target seuls, `%` littéral accepté.
- Limites : formes/liaisons sur données FOURNIES seulement ; seuls bindings structurels fournis, propre binding SHA canon entière calculé ; pas de vérification signature ni provenance authentifiée, aucune autorité, admission ou réalisation du retrait courant, pas de Cython/link/admission/retrait/TPM/SQL/PZT/livraison/activation ; Confirm17/Proofs18/Intent7, graphe Plan16 et vrais raccords restent dus.
- Contrôle OpenSpec strict ciblé à exécuter après ces écritures, non PASS annoncé ; résultat consigné au checkpoint avant nouvelle unité.

### NativeJournal21 — recette native 21 PASS — 2026-10-29
- Fichiers : `src/pixs/pa_native/nv_journal.pyx` 721l/26409o SHA `a97f97820129a407125f4b9c47eca4bafb072ddaa05bad53e9e5da073bb69418` ; `tests/native/test_nv_journal.py` 22706o SHA `2effbaeebc299b6b19d43c872348c4daf1c648988722559a29d12b23ff29f203` 21 méthodes ; `tests/native/fixtures/nv_journal_driver.c` 3493o SHA `44c48f87dbfbe2348398c2a8f2f8688b9941b001651023f583ea191146fdbcc2` inchangé.
- Première compilation Cython FAIL `370:33` conversion Python objet nogil avant tests ; correctif minimal cast `<uint64_t>0x7fffffffffffffff`, même borne positive64, sans nouveau plafond/API/droit/clé.
- Seconde compilation réelle PASS : py_compile test, Cython3.3.0/C11/cc/link sous CPython3.14.9 Py_GIL_DISABLED0/shared0/SOABI `cpython-314-x86_64-linux-gnu` ; SO 72824o SHA `dc6eeb684eab42353e7d665f173857fe1fc9a91a37043aaf3f7083a73c42674b`.
- Recette : 21 PASS 0 fail/error/skip en 1.0553551109915134s, 21 IDs uniques, log 5191o SHA `4100d11ee1f784329b930caf2f3c57db5ffa1471f705d1f2e5386f7103a10414` ; seul test modifié parmi les21 exécutés : profils `2**63` refus sans write, `2**63-1` open/close/cleanup validés.
- Nettoyage réel exit0 23 fichiers/23 dirs 763666o digest `d89fcb2844050d8c8d5d4d172abfa92569986d1206543cb0759cbf7f7c50355c` ; vérification distincte exit0 namespace/processus absents, outils conservés.
- Preuves : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-native-journal-short-b64-unit-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-native-journal-cleanup-staged-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-native-journal-verification-staged-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/native-journal-cycle2-final-test-release.json`.
- Limites : fichiers/flock/fsync physiques, horloge/pannes injectées ; pas TPM/ESAPI/TCTI/Extend/HMAC réel, autorité courante, SQL/PZT, quatre exécutables globaux, admission/retrait, livraison/activation ; 35/128/22/48 et 21 séparés, aucun total global ; anciens libellés noCython limités à leurs unités pures.
- Contrôle strict final encore à exécuter après docs, non PASS annoncé.

### Graph WithdrawalPlan16 — composition métadonnées seule — 135 PASS — 2026-10-29
- Fichiers : `src/pixs/pa_native/generator.py` 688l SHA `110f914d815b4346f2515fddcec559fdc278876b1f19a81296c3696c2771249e` ; `src/pixs/pa_native/builder.py` 597l SHA `9f2a1a11c18cdc8a4925815f3358b6f3685366d12fe255570463846d01e941f7` ; `tests/unit/test_pa_native_generator.py` 1335l SHA `7fe5da648b28d93e5b8184ea6ba3493a41ddc4911a3cc282d3cde4bf3cf9cf8b` ; `tests/unit/test_pa_native_builder.py` 993l SHA `5261013dc1554f3e77bca86856f90df7d15058e07f636ef0239dbcfa177c84f8` ; 6 edits natifs exacts HELD/once/completed/libérés sur 4 fichiers, propositions initiales corrigées AVANT exécution (renommage `withdrawal_plan_graph`, coexistence FIN graphe complet PG unique, nettoyage 4 pyc explicite), aucun échec unité 135.
- Preuves : syntaxe 4 exit 0 ; unité 135 PASS 0 fail/error/skip en 1.036s sortie native non tronquée 135 IDs uniques (62 générateur + 73 constructeur), 7 nouvelles méthodes (4 générateur + 3 constructeur) ; 80 SHA stables ; cleanup 4 pyc exit 0 absences vérifiées, répertoires fixtures revenus baseline sans glob ni runtime retiré.
- Preuves fichiers : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-withdrawal-plan-graph-syntax-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-withdrawal-plan-graph-unit-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-withdrawal-plan-graph-cleanup-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/withdrawal-plan-graph-unit-independent-review.json`.
- Réalisation : codec optionnel détecté par source OU module canonique `withdrawal_plan`, absent accepté, présent canonique unique/ops vides ; PG seul import canonique unique `postgresql_contracts`/rôles couvrants sans contrôle tuple(pg.operations)==(), 4 rôles publics `pixs-pa-system,pixs-pa-events,pixs-pa-session,pzt`/union dont PZT, aucun System-only ajouté ; même garde partagée `_check_withdrawal_plan_composition` dans inventaire générateur et précontrôles constructeur AVANT outils, code `PA01_WITHDRAWAL_PLAN_COMPOSITION_INCOMPLETE` ; anciens helpers `plan_graph`/tests Plan15 préservés AST.
- Refus : PG absent/renommé/alias source/non couvrant/dupliqué global antérieur, plan nom/alias source/dup/ops non vides, coexistence FIN graphe complet PG unique partagé, précédence refus observation `PA01_OBSERVATION_COMPOSITION_INCOMPLETE` ; nominaux constructeur arrêtés à `TOOL_UNAVAILABLE` simulé, aucun outil réel.
- Limites : forme/composition métadonnées SEULE ; aucun Cython/link, signature/authenticité/provenance courante/admission/retrait/TPM/SQL/PZT/livraison/activation ni 4 exécutables globaux qualifiés ; codec WithdrawalPlan16 et 48 PASS inchangés ; 35/22/48/21/135 séparés sans somme globale, 135 REMPLACE 128 (58+70) sans addition ; preuve Journal21 native indépendante et limites horloge/pannes injectées préservées.
- Contrôle strict final à exécuter après docs, en ATTENTE, non PASS annoncé ; résultat consigné au checkpoint natif avant nouvelle unité.

### Confirmation17 — forme seule 17 champs — 63 PASS — 2026-10-29
- Fichiers : `src/pixs/pa_native/withdrawal_confirmation.py` 336l SHA `3bb8656649967f7eadb5f9409c37632bc6e9e83f0d928e31a887992e6fd8b8ae` ; `tests/unit/test_pa_withdrawal_confirmation.py` 632l SHA `97ae756beca554b136a66f5f3f5eab1ea944df80eb4ac115f82fb820d5b1ebc7` ; 2 writes natifs fidèles HELD/once/completed/libérés, propositions 53 puis 61 corrigées en 63 AVANT premier essai (S via JSON, bytes via forgé, ModuleType sys.modules flat positif), aucun échec test produit.
- Preuves : syntaxe 2 exit 0 ; unité 63 PASS 0 fail/error/skip en 0.019s sortie non tronquée 63 IDs uniques (5+2+21+3+8+5+11+2+3+3) ; 82 SHA stables ; cleanup 2 pyc exit 0 absences 2 vérifiées, ancienne requête cleanup MCP altérée 1 caractère REJECTED avant décision/once/effet (get_approval natif REJECTED), nouvelle commande littérale exacte sans base64.
- Preuves fichiers : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-confirmation17-source-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-confirmation17-tests-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-confirmation17-syntax-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-confirmation17-unit-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-confirmation17-cleanup-literal-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/confirmation17-unit-independent-review.json`.
- Réalisation : 17 champs fermés littéraux c08 type/schema 1.0.0, 13 refs UTF-8/C0/DEL/surrogates/borne octets, PayloadLimits PG 3 champs explicites sans valeurs implicites, 3 API encode/decode/binding limits kwonly obligatoires ; plan_binding fourni et validé structurellement, sans producteur qualifié, propre ContentBinding `{ref=confirmation_ref,version=confirmation_version,sha256=SHA256(CANON(confirmation ENTIÈRE))}` hors objet ; UTC6 ASCII 27/calendrier 0001 valide 0000 invalide/bissextile/fraction 6 Z, aucun clock/fraîcheur/TTL/durée/grace/consommation ; frozen/slots/reprFalse revalidation chaque API objets forgés/limites/bindings ; branche package pixs.pa_native et flat PG builtin manquant refus/namespace étrangère, positif PG SIMULÉ seulement.
- Refus : wildcards `* ? [ ]` installation/cible seuls (1524-1525 + matrice 1626 mêmes valeurs PLAN16), `%` littéral et autres refs opaques conservés ; 17 manquants/refs 13 mauvais types/contrôles UTF8, binding extra/manquants/dupliqué/majuscule/non-hex/bool/null/int/forgé/membre absent, UTC forme/calendrier/forgé, limites falsifiées, contextes import simulés.
- Limites : forme/propre binding sur données FOURNIES seulement ; aucune origine C08/authentification/contexte/politique/droit/décision courante ou confirmation réelle, pas Cython/link/SQL/TPM/PZT/admission/retrait/livraison/activation/global qualifiés ; 35/22/48/21/135/63 séparés sans somme globale, 135 REMPLACE 128 historique, preuve Journal21 native indépendante.
- Contrôle strict ciblé final APRÈS documents encore NON EXÉCUTÉ, pas PASS annoncé ; résultat racine checkpoint avant nouveau lot.

### Graph Confirmation17 — composition métadonnées seule — 142 PASS — 2026-10-30
- Fichiers : `src/pixs/pa_native/generator.py` 702l SHA `fbc264ad24a8bf5a2a72a4e758dd679a518e269e4f8e90e56918a764833b7e23` ; `src/pixs/pa_native/builder.py` 599l SHA `9e87560863ac1bd67749d6f701dfed9ba2c2e48febbd58f7f6a58e2fd32c52eb` ; `tests/unit/test_pa_native_generator.py` 1414l SHA `f8afaecc8096316539529e3fb586e2723ae22d29d269b0ad5d6681c4c7c7edc3` ; `tests/unit/test_pa_native_builder.py` 1038l SHA `1d32b507544d8679f06418e0caf20db4b1fb367b4c67acccaf6dcf2f63b4a9a3` ; 6 edits natifs exacts HELD/once/completed/libérés sur 4 fichiers, aucun échec unité 142.
- Preuves : syntaxe 4 exit 0 ; unité 142 PASS 0 fail/error/skip en 1.113s sortie native non tronquée 142 IDs uniques (66 générateur + 76 constructeur), 7 nouvelles méthodes (4 générateur + 3 constructeur) ; 82 SHA stables ; cleanup 4 pyc exit 0 absences vérifiées.
- Preuves fichiers : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-confirmation17-graph-syntax-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-confirmation17-graph-unit-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-confirmation17-graph-cleanup-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/confirmation17-graph-unit-independent-review.json`.
- Réalisation : garde optionnelle commune `_check_withdrawal_confirmation_composition`, détecte source OU module réservé `withdrawal_confirmation`, absent accepté, présent canonique unique/ops vides du codec type ; PG canonique unique et rôles couvrants SEUL import, sans nouveau contrôle PG ops vide ; 4 rôles publics/PZT/union, pas System-only ajouté ; appel inventaire générateur/précontrôles constructeur AVANT outil après Plan16, code `PA01_WITHDRAWAL_CONFIRMATION_COMPOSITION_INCOMPLETE` ; anciens helpers et 135 méthodes AST inchangés.
- Refus : PG absent/renommé/alias/noncouvrant/dup global, codec nom/source alias/dup/ops mal attribuées échec antérieur générique correct ; coexistence Plan16 avec PG unique partagé et ordre observation d'abord ; nominaux constructeur stop `TOOL_UNAVAILABLE` simulé, ELF fixtures ne prouvent pas objets Cython.
- Limites : forme/composition métadonnées SEULE ; aucun Cython/builtinC/link/port C08/authentification/autorité/politique courante/retrait/SQL/TPM/PZT/livraison/activation/global qualifiés ; codec Confirmation17 source 336/tests 632/63 PASS forme et journal 21 NATIF indépendants conservés ; 35/22/48/21/142/63 séparés sans somme globale, 142 REMPLACE 135 (62+73) et 128 sans addition.
- Contrôle strict ciblé à exécuter après docs, en ATTENTE, non PASS annoncé ; résultat consigné au checkpoint natif avant nouveau lot.

### Proofs18 — forme seule 18 champs — 63 PASS — 2026-10-30
- Fichiers : `src/pixs/pa_native/withdrawal_proofs.py` 347l SHA `ac80ab9f25d22b6d60c7b326165da29dfaa0297f1e1faed1dbcde05318cb851c` ; `tests/unit/test_pa_withdrawal_proofs.py` 658l SHA `148322b58d686f03e72814ac977723d5623ca4b4f54d4eef07685d53e829155a` ; 2 writes natifs fidèles HELD/once/completed/libérés, 2 méthodes tests binding corrigées AVANT premier essai (objet neuf par subTest, ref unique par attache), aucun échec test produit.
- Preuves : syntaxe 2 exit 0 ; unité 63 PASS 0 fail/error/skip en 0.022s sortie non tronquée 63 IDs uniques (5+2+21+3+8+5+11+2+3+3) ; 84 SHA stables ; cleanup 2 pyc exit 0 absences 2 vérifiées, ancienne requête cleanup MCP altérée REJECTED avant any access/once/effet, nouvelle commande littérale courte exacte.
- Preuves fichiers : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-proofs18-source-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-proofs18-tests-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-proofs18-syntax-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-proofs18-unit-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-proofs18-cleanup-literal-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/proofs18-unit-independent-review.json`.
- Réalisation : 18 champs fermés, 12 refs UTF-8/C0/DEL/surrogates/borne octets, 3 ContentBindings FOURNIS `plan_binding`/`confirmation_binding`/`anchor_binding` PG seul import, PayloadLimits PG 3 champs explicites kwonly sans default, 3 API encode/decode/binding ; propre ContentBinding `{ref=proofs_ref,version=proofs_version,sha256=SHA256(CANON(bundle ENTIER))}` hors objet, CANON sort_keys/separators UTF-8 ensure_asciiFalse/allow_nanFalse sans LF final ; frozen/slots/reprFalse, revalidation chaque API objets forgés/limites/bindings ; `prepared_at` UTC6 ASCII 27/calendrier 0001-9999/bissextile/fraction 6 Z, sans clock/fraîcheur/TTL/grace/authenticité ; `installation_result_ref` opaque sans assimilation PK ni inégalité strings namespaces, `authorization_decision_ref`/operator/policy données seules ; wildcards installation/cible seuls norme PLAN16+matrice 1626, autres refs/`%` littéraux ; branche package pixs.pa_native et flat PG builtin manquant refus/namespace étrangère, positif PG SIMULÉ avec module enregistré sys.modules seulement, pas builtinC/Cython/link réels.
- Refus : 18 manquants/12 refs mauvais types/contrôles UTF-8, 3 bindings fermeture/type/doublons par attache/forgés/membre absent, PayloadLimits 3 champs falsifiés/revalidation, limites exactes/UTF-8 multioctets, UTC forme/calendrier/années forgés, imports pkg/flat PG missing/positif SIMULÉ/namespace étranger, aucune fraîcheur déduite ; sous-classe S/bytes testés constructeur/forgés, garde IO sur opérations codec seules.
- Limites : forme/propre binding sur données FOURNIES seulement ; aucune origine C08/résolveur/audit/SQL lookup/TPM/retrait/authentification/autorité courante/qualification globale prouvée, pas Cython/link/SQL/PZT/admission/livraison/activation/global qualifiés ; 35/22/48/21/142/63C17/63Proofs séparés sans somme globale, 142 REMPLACE 135 historique, preuves Journal21/Graphe142/Confirmation17 indépendantes.
- Contrôle strict ciblé APRÈS docs en ATTENTE, non exécuté ; résultat checkpoint avant nouveau lot.

### Intent7 — forme seule 7 champs — 54 PASS — 2026-10-30
- Fichiers : `src/pixs/pa_native/withdrawal_intent.py` 310l SHA `2f9c98a60ae742dafc1b369f8b39d3c8ccb43d5e42801537419e013ecc9b9918` ; `tests/unit/test_pa_withdrawal_intent.py` 587l SHA `ca1a1ee3e3a7b690dba7d42d48a8c5219dde1226908158b07a7470e71808bf95` ; 2 writes natifs fidèles HELD/once/completed/libérés, aucun échec test produit.
- Preuves : syntaxe 2 exit 0 ; unité 54 PASS 0 fail/error/skip en 0.012s sortie non tronquée 54 IDs uniques (5+2+21+3+10+5+2+3+3) ; 86 SHA stables ; cleanup 2 pyc exit 0 absences 2 vérifiées.
- Preuves fichiers : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-intent7-source-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-intent7-tests-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-intent7-syntax-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-intent7-unit-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-intent7-cleanup-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/intent7-unit-independent-review.json`.
- Réalisation : 7 champs fermés, 3 refs UTF-8/C0/DEL/surrogates/borne octets, 2 ContentBindings FOURNIS `request_binding`/`signed_mandate_binding` PG seul import, PayloadLimits PG 3 champs kwonly explicites sans défaut, 3 API encode/decode/binding ; relation positive `request_binding.ref==operation_id`, versions 2 bindings `1.0.0`, littéraux `pixs.agent.withdrawal_intent/v1`/`1.0.0` ; propre ContentBinding `{ref=operation_id,version=schema_version,sha256=SHA256(CANON(intention ENTIERE))}` hors objet, CANON sort_keys/separators UTF-8 ensure_asciiFalse/allow_nanFalse ; frozen/slots/reprFalse, revalidation chaque API objets forgés/limites/bindings ; wildcards installation/cible seuls norme PLAN16+matrice 1626, autres refs/`%` littéraux ; branche package pixs.pa_native et flat PG builtin manquant refus/namespace étrangère, positif PG SIMULE avec module enregistré sys.modules seulement, pas builtinC/Cython/link réels.
- Refus : 7 manquants/3 refs mauvais types/contrôles UTF-8, 2 bindings fermeture/type/doublons/forgés/membre absent, refus si `request_binding.ref` DIFFERENT de `operation_id` (l'égalité est la relation positive attendue), PayloadLimits 3 champs falsifiés/revalidation, limites exactes/UTF-8 multioctets, imports pkg/flat PG missing/positif SIMULE/namespace étranger ; sous-classe S/bytes testés, garde IO sur opérations codec seules.
- Limites : forme/propre binding sur données FOURNIES seulement ; aucune SHA requête/mandat réel vérifiée ni signature/provenance/autorité courante/C08/temps courant/journal/Extend/SQL/TPM/PZT/livraison/activation/global qualifiés ; 35/22/48/21/142/63C17/63Proofs/54Intent séparés sans somme globale, 142 REMPLACE 135 historique.
- Contrôle strict ciblé APRÈS docs en ATTENTE, non exécuté ; résultat checkpoint avant nouveau lot.

### Graphe Proofs18 — composition métadonnées seules — 149 PASS — 2026-10-30
- Fichiers : `src/pixs/pa_native/generator.py` 716l SHA `90004943b274dd46891a24b5902440674417c78fb8018d7b4904140ec4280881` ; `src/pixs/pa_native/builder.py` 601l SHA `02017b209ded92da22c379ec12400893780866b5d402c1f9dfad57cc70a3e297` ; `tests/unit/test_pa_native_generator.py` 1491l SHA `8db556f7cf9926323c4b42349868996a6ebcefeb54ec4d851ce7b2e21296af78` ; `tests/unit/test_pa_native_builder.py` 1083l SHA `922b2a24190c51f36995a1b5cfaafb4d7ef84b4206978a0b67ef1955ef30a451` ; six effets natifs exacts HELD/once/completed/libérés.
- Preuves : syntaxe 4 exit 0 ; unité 149 PASS 0 fail/error/skip en 1.114s sortie non tronquée 149 IDs uniques (70 générateur + 79 constructeur), 142 anciens conservés + 7 nouveaux (4 générateur + 3 constructeur) ; 85 SHA stables ; fixtures `output/tests/pa01-generator` et `output/tests/pa01-builder` mêmes dev/ino et vides ; cleanup 4 pyc exit 0 absences 4 vérifiées.
- Preuves fichiers : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-proofs18-graph-syntax-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-proofs18-graph-unit-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-proofs18-graph-cleanup-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/proofs18-graph-unit-independent-review.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/proofs18-graph-prewrite-review.json`.
- Réalisation : anciennes gardes Plan16/Confirmation17 et 142 tests conservés inchangés ; garde optionnelle `_check_withdrawal_proofs_composition` ajoutée, source OU module `withdrawal_proofs`, absent accepté, présent canonique unique/ops vides ; les fonctions d'inventaire générateur et de précontrôles constructeur reçoivent bien un appel nouveau après Plan16/Confirmation17 ; PG canonique unique `postgresql_contracts` seul import réel du codec, rôles réellement utilisés couverts, pas quatre rôles obligatoires ni System-only, sans Plan/Confirmation/Anchor imposés ; code `PA01_WITHDRAWAL_PROOFS_COMPOSITION_INCOMPLETE`, doublons `MODULE_INVALID` et ops `OPERATION_INVALID` via gardes existantes ; coexistence Plan16+Confirmation17+Proofs18 PG unique partagé, ordre observation d'abord ; 7 nouvelles méthodes listées en preuves.
- Refus : PG absent/renommé/alias/non-couvrant/dupliqué-global, proofs nom/alias/dupliqué/ops mal attribuées, ordre antérieur observation ; nominaux constructeur `TOOL_UNAVAILABLE` simulé, ELF/Popen simulés ne prouvent ni objets Cython ni exécution d'exécutables natifs PA/PZT, exécution Python des 149 tests réellement effectuée.
- Limites : forme/composition métadonnées seules ; aucun Cython/builtins/link/port C08/authentification/autorité/politique courante/retrait/SQL/TPM/PZT/livraison/activation/global qualifiés ; codec Proofs18 63 PASS et Confirmation17 63 PASS et Intent7 54 PASS et Journal21 21 NATIF indépendants conservés ; 35/22/48/21/149/63/63/54 séparés sans somme globale, 149 REMPLACE 142/135/128/122.
- Contrôle strict ciblé APRÈS docs en ATTENTE, non exécuté ; résultat checkpoint avant nouveau lot.

### Graphe Intent7 — composition métadonnées seules — 156 PASS — 2026-10-30
- Fichiers : `src/pixs/pa_native/generator.py` 730l SHA `c6d013e26675b9130ca3ef453d3c0121262f249955de35c1bd1f4ecad14e97a3` ; `src/pixs/pa_native/builder.py` 603l SHA `b5842edbfe7d80b8e70dc5e924871f8fab710e16bd3fbad427845518db332d02` ; `tests/unit/test_pa_native_generator.py` 1570l SHA `9af4a6460769fb5b01e55e1ba0175fcdc0ed701e9105502efa10b6e2ba670960` ; `tests/unit/test_pa_native_builder.py` 1129l SHA `8ff1fc23b97b35c33b4a4d624f946cea518a0d9347edbbad5404f69e42cebccc` ; six effets natifs exacts HELD/once/completed/libérés.
- Preuves : syntaxe 4 exit 0 ; unité 156 PASS 0 fail/error/skip en 1.164s sortie non tronquée 156 IDs uniques (74 générateur + 82 constructeur), 149 anciens conservés + 7 nouveaux (4 générateur + 3 constructeur) ; fixtures `output/tests/pa01-generator` et `output/tests/pa01-builder` mêmes dev/ino et vides ; cleanup 4 pyc exit 0 absences 4 vérifiées.
- Preuves fichiers : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-intent7-graph21121-syntax-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-intent7-graph21121-unit-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-intent7-graph21121-cleanup-native-proof.json`.
- Réalisation : anciennes gardes Plan16/Confirmation17/Proofs18 et 149 tests conservés inchangés ; garde optionnelle `_check_withdrawal_intent_composition` ajoutée, source OU module `withdrawal_intent`, absent accepté, présent canonique unique/ops vides ; les fonctions d'inventaire générateur et de précontrôles constructeur reçoivent bien un appel nouveau après Proofs18 ; PG canonique unique `postgresql_contracts` seul import réel du codec, rôles réellement utilisés couverts, pas quatre rôles obligatoires ni System-only, sans nv 5 modules imposés ; code `PA01_WITHDRAWAL_INTENT_COMPOSITION_INCOMPLETE`, doublons `MODULE_INVALID` et ops `OPERATION_INVALID` via gardes existantes ; coexistence Plan16+Confirmation17+Proofs18+Intent7 PG unique partagé, ordre observation d'abord ; 7 nouvelles méthodes listées en preuves.
- Refus : PG absent/renommé/alias/non-couvrant/dupliqué-global, intent nom/alias/dupliqué/ops mal attribuées, ordre antérieur observation ; nominaux constructeur `TOOL_UNAVAILABLE` simulé, ELF/Popen simulés ne prouvent ni objets Cython ni exécution d'exécutables natifs PA/PZT, exécution Python des 156 tests réellement effectuée.
- Limites : forme/composition métadonnées seules ; aucun Cython/builtins/link/port C08/authentification/autorité/politique courante/retrait/SQL/TPM/PZT/livraison/activation/global qualifiés ; codec Intent7 54 PASS et Proofs18 63 PASS et Confirmation17 63 PASS et Journal21 21 NATIF indépendants conservés ; 35/22/48/21/156/63/63/54 séparés sans somme globale, 156 REMPLACE 149/142/135/128/122.
- Contrôle strict ciblé APRÈS docs exécuté le 2026-10-30 : `Change 'add-pa-native-build-and-component-composition' is valid` exit 0, preuve `/home/devops/datas/cab/output/scm-discovery-ack/pa01-intent7-graph21121-final-strict-native-proof.json` ; résultat consigné au checkpoint avant nouveau lot.

### PA01-SL02 — Recette native nv_secret17 fixtures publiques — 17 PASS retest — 2026-10-30
- Périmètre : `src/pixs/pa_native/nv_secret.pyx` SHA `05bb3224b3af53cf6dff3f1b5cd055561c8ba68e9f96efa2c2f1f80a5f7120e8` inchangée ; `tests/native/test_nv_secret.py` SHA `488ce5a1621a5569531a5ae3b39b9d73a51eac86cd43acc33f74d10fdd5b1a83` 14844 octets, seule méthode concurrente corrigée (préallouer 4 pipes avant threads, 4 vrais appels C concurrents, statuts 0 / ref -1 / octets exacts / buffers distincts / preuve FD fermé, cleanup attempted/consumed sans forcer FD vivant) ; D12 lecteur + D13 formes publiques seules, sans API Python/capsule, `nv_secret.h` inventorié, `nv_secret_api.h`/capsules refusés ; fixtures publiques pipe/fichiers/FD seules, System-only produit maintenu.
- Campagne LXC CT100 hvp1 : CPython 3.14.9 GIL activé (Py_GIL_DISABLED=0), shared 0 / SOABI cpython-314-x86_64-linux-gnu / Cython 3.3.0 / C11 cc Debian 14.2.0-19 / OpenSSL 3.5.7 observés LXC ; namespace `/var/tmp/pixs-pa01-cismp7-nvsecret17-20261030-8f27b6c4` dev1792/ino262790/uid0/gid0/mode0700 ; 4 artefacts inchangés avant/après : C 263600 `ff799e1886b1a7dc1daa0ebc37ba4c83f8e8801f6dcd0d77e8fab941423da0b2` / H 2327 `78355ad7eac6cf44402e8d3adc564ee95066625f4fcfad860b42a63b9cf74adf` / O 42112 `d8ec48fd8904e67a2333bd80423e496b91a65bdcf6560ed824e40ba954ab39b6` / SO 48864 `037a03baf5a0e172e6efd7469428c2043018e3962a008f6e3108a041210c35a3`.
- Premier essai réel 17 run 0.076504661s : 16 OK / 1 FAIL `test_independent_calls_from_threads_do_not_share_a_buffer` (`OSError not raised` x2) à cause course test FD (réutilisation n° FD), valeurs retour non validées, conservé séparément, pas fuite produit prouvée ; log 5649 `bf519bccaccf6524f2c5def9fd143a5f782270e24bdfeaf075a49220b407c1d8`.
- Retest 17 PASS 0 failure/error/skip 0.076782632s, 17 IDs uniques, même binaire SO, log distinct 4754 `d0f9500a695e6021151377c96887113ad377606377269bb5510acdc07420d7bb` ; ancien log conservé.
- Cycle : lease `tests-pa01-nvsecret17-9be92571d7704f07a76ec65435dfd5d0` acquise/réconciliée (CAB 2.1.22/2.1.23) puis RELEASED fencing 12040 HTTP200 ; namespace LXC 17 fichiers/11 dirs inventoriés digest `54535016176cf7917c968c7bc83f57ea60d6840e48f399dc31a53d58b0562880` total 398892, supprimé puis absence vérifiée pids [] ; outils installés conservés ; conducteurs locaux 28 entrées vérifiées puis supprimés, sources intactes.
- Preuves : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvsecret17-compile-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvsecret17-retest-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvsecret17-update-test-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvsecret17-diagnostic-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/nvsecret17-testfix-21122-edit-0-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvsecret17-cleanup21123-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvsecret17-verify21123-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvsecret17-local-cleanup-v4-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvsecret17-local-verify-v4-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/nvsecret17-test-release-result.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvsecret17-retest-independent-review.json`.
- Limites : portée native nv_secret fixtures publiques prouvée (compilation Cython/import/test 17) ; composition/link des exécutables PA/PZT et autorité/TPM/HMAC/SQL/credential réel/produit restent non qualifiés ; 17 SL02 séparé sans somme globale avec 21/156/54.
- Contrôle strict ciblé APRÈS docs exécuté le 2026-10-30 : `Change 'add-pa-native-build-and-component-composition' is valid` exit 0, preuve `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvsecret17-doc-strict-native-proof.json` ; SL02 VALIDÉ scope 17 publics.

### PA01-SL03 libpq11 VALIDÉ 2026-10-30 — scope 11 publics sans connexion SQL
- Périmètre : `src/pixs/pa_native/libpq_inspection.pyx` inchangée fca075d728373afac9dc58e88eacce5c908e941a5ede6ace27d8f1da2beef747 20326 + `tests/native/test_libpq_inspection.py` a28b8b53e3880e2f642c2ae5ec2baa6e725dc36127c80a69145225ab63434f9d 5880, seul scénario PGHOST fixé via sys.argv[2] sans affaiblir assertions, 11 méthodes identiques, aucun connect SQL.
- Premier échec expliqué : 10 PASS 1 FAIL car marqueur public inclus dans source-c réimprimée par traceback Python 3.14, garde C ENV correcte PA01_SQL_ENVIRONMENT_FORBIDDEN levée, pas de fuite produit prouvée ; log premier essai 6225 c9b215e2fc9437e076c1770f9ae066c241bd256ca63cf7a1f0f3509b0a61fb0e conservé.
- Preuves : retest 11/11 PASS 0 fail/error/skip 0.08838331000879407s natif exit 0, même SO 9d97535023b4fef115c897f5e9281a9f22351e1becab8772a2f8439518586ba0 sans recompile, log retest 4497 1fab618c083ec12d1b663e80931cb1b4fea81a97033d65424bad8bc1c0eff816, manifest f5624bfc6b88b135750cdcb6aa4c87fc0072da30b2fea5c19aa2b7f33aa0847e ; toolchain CPython 3.14.9 GIL actif shared 0 / Cython 3.3.0 / C11 cc 14.2, headers 17.11 PG_VERSION_NUM 170011 + PQlibVersion 170011, fixture 160015 non serveur mesuré, pas de connexion SQL.
- Fichiers : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-libpq11-compile-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-libpq11-retest-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-libpq11-cleanup-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-libpq11-verify-cleanup-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-libpq11-local-cleanup-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/pa01-libpq11-local-verify-native-proof.json` ; `/home/devops/datas/cab/output/scm-discovery-ack/libpq11-test-release-result.json`.
- Nettoyage : LXC 17 files 11 dirs 2037410 digest f89f69b7e438c6db21c6cabe8d8aeda658a3ace01996faaafed0dfc47d72d04b exit 0 + vérification distincte exit 0 ENOENT/pids 0/CPython 2 headers libpq conservés ; lease tests-pa01-libpq11-72e5d1e508d648ffad40e3e6c57c21b5 RELEASED12413 20:09:45.831Z ; local 28 objets 19 files 9 dirs + parent propre supprimés, vérificateur distinct VERIFY_OK, 2 sources intactes.
- Limites : SQL/HBA/auth/TPM/PZT/binaire PA/global inchangées, 1/10 cases inchangées, 17 SL02 et 21 Journal et 156 graphe distincts sans somme ; strict ciblé APRÈS docs exécuté le 2026-10-30 : `Change 'add-pa-native-build-and-component-composition' is valid` exit 0, preuve `/home/devops/datas/cab/output/scm-discovery-ack/pa01-libpq11-doc-strict-native-proof.json` ; SL03 VALIDÉ scope 11 publics sans connexion SQL, aucune livraison ni épuisement prétendu.

### PA01-SL04 — Recette native nv_anchor34 et régression tcti26 (VALIDÉ 2026-10-31, strict ciblé APRÈS docs exécuté)
- Périmètre : 34 méthodes anchor (18 publiques + 16 authentifiées) et 26 méthodes tcti en deux essais séparés, quatre fichiers .pyx et postgresql_contracts.py soit cinq modules, production inchangée, ESAPI et TCTI entièrement simulés, vrais en-têtes TSS version 4.1.3 paquet libtss2-dev 4.1.3-1.2, sans TPM, HMAC, SQL, admission, retrait, autorité, PZT, binaire PA ou livraison.
- Compilation : premier échec CC conducteur conservé 2499o (2 macros TCTI conditionnelles), correctif fixture C deux locales tcti_ctx tx/rx bfb10819 23961o. Rebuild2 : 17 étapes PASS, 5C 4H 6O 1SO, SO 1059800o f3f0fcd7e99f21b8420ea780b7623756704e8634a6fe0f36a61732f2cd0d6b71, 107 exports, 5 imports avec rétention sans capsule, sans libtss2-esys ni TCTI.
- Premiers constats conservés : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvanchor34-first-unittest_anchor34.log` 14199o 5637e0334bab5dbd4b4104ceb2dbe9c50ef73a36c1cada68cc830462fbea0147 avec 34 exécutés et 2 échecs du même cas expiré et de son nettoyage, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvanchor34-first-unittest_tcti26.log` 12873o 5200639f5c0e4e736df592a7d2ed83d3c6e6d35e46744f1405ebc22702bb1aec avec 26 exécutés et 3 échecs payload de fixture, 0 erreur et 0 test ignoré. Aucun blanchiment par la production.
- Correctifs des deux essais seuls : valeur publique standard TCTI 0123456789abcdef répétée, nettoyage start réel 9 IN_DOUBT conservé puis Finish réel 0 avec erreur primaire EXPIRED 6 conservée et vrais compteurs de Flush 14 et 15, sans NV_Read, sans toucher aux cinq modules.
- Nouveaux essais séparés : anchor34 34/34 PASS 0 échec/erreur/saut, pid 1055, environ 0,32s, journal 12325o a8fc536660fbc930bb4478c15bc81a7a483d34efee62b89a3cd82c3ad97abde8. Tcti26 26/26 PASS 0 échec/erreur/saut, pid 1089, environ 0,39s, journal 9843o dfb27c74a9684127060da61a9ddfcaf5359252d1bfdd7a3e1aac087743a9a170. Même SO avant et après, PIDs distincts, pids[] après chaque essai, aucune somme globale.
- Restitution : nettoyage Root1 36 fichiers 11 répertoires 5984844o, nettoyage Root2 51 fichiers 11 répertoires 7211708o, vérification distincte des deux racines absentes avec 11 gardes installées, release bail 12645, local VERIFY_OK 34 fichiers 9 répertoires. Preuves principales : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvanchor34-compile2-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvanchor34-retest-anchor34-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvanchor34-retest-tcti26-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvanchor34-cleanup-first-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvanchor34-cleanup-rebuild2-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvanchor34-verify-both-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvanchor34-local-cleanup-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvanchor34-local-verify-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/nvanchor34-test-release-result.json`.
- Campagne : CPython 3.14.9 GIL activé shared0, Cython 3.3.0, C11 cc 14.2.0, OpenSSL 3.5.7. SL01, SL02 et SL03 VALIDÉS conservés. 1/10 PARTIELLEMENT RÉALISABLE inchangé. Strict ciblé APRÈS docs exécuté le 2026-10-31 : `Change 'add-pa-native-build-and-component-composition' is valid` exit 0, preuve `/home/devops/datas/cab/output/scm-discovery-ack/pa01-nvanchor34-doc-strict-native-proof.json`.

### PA01-SL05 — Prêt privé TLS, dix cas réels — VALIDÉ scope 10, strict observé
Les 3 sources sont inchangées et le SO de test `5d6c3e39380ee98a91ebd29af933927acb960c00efe07c0c1eb3a693c3d21da8` (186408o) porte les dix recettes réelles : 10/10, 0 échec, 0 erreur, 0 ignoré, durée 0.011263032 s, pid 1460, journal 4948o `7969ebb9d4a1aba1f02b22b9d893aa154a6715d9288d4b6dff7d540fee2bcf51`. La première commande exit 1 est conservée : la sonde initiale inventait `ready_for_transport`, la vraie API est `configuration()["ready_for_transport"]`, premier journal durable `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlslease10-first-import-probe.log` (1647o `fea8ef9b34e3ddbe28709d2fcdb371cd7faa9130f52241fa63a0cbb945fd19fb`). La reprise exit 0 est séparée, sans recompiler, avec `ready_for_transport` False, fonctions privées absentes de la surface Python, capsule absente. Artefacts C/H/O/SO, 8 symboles, NEEDED 3 et transitives normalisées constatés ; 4 artefacts et 8 journaux inchangés avant et après. Nettoyage LXC 16 fichiers 12 répertoires 1097797o `f0c5f814`, vérification distincte `verified_absent`, 15 gardes et 2 liens, release 12874, nettoyage local 16 fichiers 2 répertoires 18 objets et `VERIFY_OK`. Preuves : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlslease10-compile-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlslease10-compile-diagnostic-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlslease10-build-recovery-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlslease10-unit-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlslease10-cleanup-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlslease10-verify-cleanup-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlslease10-local-cleanup-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlslease10-local-verify-native-proof.json` et `/home/devops/datas/cab/output/scm-discovery-ack/tlslease10-test-release-result.json`. Limites : PKI, clé, certificat, socket, client Z12, transport, PID interprocessus, SQL, TPM, PZT et produit non qualifiés ; D13 complet non qualifié.

### PA01-SL06 — Contexte TLS13 E3 + primitive Ed25519 E4, 13/13 PASS
Les 2 sources sont inchangées (27285o, manifest `695d7c94837bff35191a6f67ea4f68f59eebe2bd36f83f409c6d8a517d7057b7`) et le SO `bfcb2cf8582995488eeef1e036dedd523d880d50fc4b38e5bf92defe07c8fe68` (185824o) porte les treize recettes réelles : 13/13, 0 échec, 0 erreur, 0 ignoré, durée 0.012543340009870008 s, pid 1690, journal 8002o `9c891f3602c03cf22a6ac6b3a65b130ade322a0a5991e21bcc8fb80cfd32eff6`. Compilation 7 étapes exit 0 : C 638253o, O 205368o, SO 185824o, 2 exports, NEEDED 3, import `configuration()["ready_for_transport"]` False, fonctions privées absentes de la surface Python, capsule absente, pid 1658. Nettoyage LXC 13 fichiers 12 répertoires 1069391o `9b071311e21ccaa9f617962ce8690a6b94b2ee6668504baaf7b5ad8bdf42acc3`, vérification distincte `verified_absent`, 15 gardes et 2 liens, release lease 13000 à 03:07:37.744Z, local `VERIFY_OK` namespace jamais créé et 2 sources intactes. Preuves : `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-inventory-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-copy-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-compile-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-unit-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-final-inventory-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-cleanup-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-verify-cleanup-native-proof.json`, `/home/devops/datas/cab/output/scm-discovery-ack/pa01-tlscontext13-local-verify-native-proof.json` et `/home/devops/datas/cab/output/scm-discovery-ack/tlscontext13-test-release-result.json`. Limites : sans PKI, clé privée, certificat, socket, handshake, transport, client Z12, autorité C08, SQL, TPM, PZT, binaire PA produit ; les 13 cas qualifient le contexte et la primitive Ed25519 seuls. Revue et strict documentaire finaux tracés dans le checkpoint du RUN, aucun résultat futur affirmé.

## Statut documentaire courant du lot B et du retrait — directive du développeur du 3 novembre 2026

Le principe B reste acquis ; les formats détaillés B et leur raccord au journal restent NON ADOPTÉS. Cette directive courante supersède les mentions historiques d’adoption de ces formats dans les anciens relevés. Le choix opérationnel INIT A, acquis séparément, ne vaut pas adoption du format INIT_A12, du plan extérieur, du mapping au journal ou des séquences B.

Les principes déjà adoptés concernant le signataire, le domaine et le droit de retrait restent distincts des formats détaillés de retrait, qui demeurent proposés sans adoption. C08 a jugé la proposition documentaire recevable sans l’adopter ; aucune adoption Z12 n’est déduite.

Les codecs et essais de forme déjà consignés restent des preuves historiques bornées à leur portée ; ils n’adoptent pas les formats et ne qualifient ni signature courante, admission, journal, retrait, effets TPM/SQL, livraison ou activation. Les tâches 1 et 2 conservent leur statut ; la tâche 3 reste ouverte et aucune nouvelle case n’est cochée par cette mise à jour. Aucun code B ou effet matériel/SQL n’est autorisé par le présent statut.

Cette correction de statut documentaire ne constitue ni test produit ni qualification Docker. La validation OpenSpec stricte du dossier final est réalisée séparément dans le même RUN.

## Statut de validation après adoption documentaire PA01 — 3 novembre 2026

Le développeur a validé le lot documentaire présenté le 3 novembre 2026. Les définitions détaillées listées dans design.md et contracts.md — PUB/FIN et ancrage, plan extérieur, Plan15, Recipe13, BASE8, R0, Policy14, Resource24, Context8, INIT_A12, Provenance28, scanner, admission par étapes, JournalTransition, séquences de publication, PLAN16, CONF17, PROOFS18, Intent7, AdminMandate27 et bindings — sont adoptées documentairement par PA01 dans leur contenu existant ; le présent statut supersède les mentions antérieures de non-adoption.

Cette adoption ne requalifie aucun codec, recette ni résultat historique et ne coche aucune tâche : les tâches 1 et 2 conservent leur statut, la tâche 3 reste ouverte. C08 n’a pas formellement adopté sa partie, aucune adoption Z12 n’est déduite, et aucun code B, effet TPM/SQL, qualification Docker/runtime, activation ou livraison n’est autorisé ou revendiqué. La validation stricte finale après cette note sera enregistrée séparément.

## Statut courant de validation B et retrait — décision développeur du 4 novembre 2026

La décision développeur du 4 novembre 2026 maintient le principe B acquis. Les formats détaillés B, le plan extérieur, INIT_A12, le raccord au journal JournalTransition et les séquences de publication restent NON ADOPTÉS. Le choix opérationnel INIT A demeure distinct et n’adopte aucun de ces formats ni raccords.

Les formats détaillés du retrait restent proposés sans adoption. C08 a jugé la proposition recevable sans adoption formelle ; aucune adoption Z12 n’est déduite.

Le présent statut corrige et supersède la section historique « Statut de validation après adoption documentaire PA01 — 3 novembre 2026 » sans la supprimer ni altérer les preuves antérieures. Les codecs et essais de forme consignés restent limités à leur portée et ne qualifient ni les formats, ni la signature, l’admission, le journal, le retrait, TPM/SQL, runtime/Docker, livraison ou activation. Les cases des tâches ne changent pas, aucune tâche n’est cochée et la tâche 3 reste ouverte. Cette correction est documentaire ; elle n’ajoute aucun test produit ni autorisation de code ou d’effet.

## PA01-SL09 — profil D1–D9 sélectionné et limites de preuve — 4 novembre 2026

La sélection documentaire D1–D9 déjà validée est consignée dans design.md et la présente section Tâche 2. Elle retient CPython 3.14.9 avec GIL et Cython 3.3.0 comme candidats de la campagne historique, une distribution en répertoire, Debian 13 x86_64 physique/VM et Docker local comme cibles distinctes, quatre exécutables avec leurs modes CLI obligatoires, un runtime statique chargé par PyConfig et un profil de build TOML fermé. Le choix développeur 1 du 23 octobre fixe le catalogue PA01 initial à inspect_postgresql, prepare_postgresql et get_postgresql_result 1.0.0 sous pixs.agent/system-daemon.

La procédure PREUVE_SELECTION_PA01.md reste documentaire et NON_IMPLÉMENTÉE : aucune nouvelle observation PyPI, aucun nouveau manifeste d’admission et aucune nouvelle campagne de sélection ne sont établis par cette note. La sélection historique Cython du 26 octobre ne prouve ni fermeture/ABI du runtime distribué, ni qualification physique/VM, ni recette Docker. Le LXC de test est distinct de Docker et ne qualifie pas cette cible.

Ce relevé confirme la sélection de profils et de dépendances, pas leur qualification, implémentation ou disponibilité opérationnelle. Aucune tâche n’est cochée ou modifiée ; aucun test produit ou effet PostgreSQL n’est exécuté. Les formats détaillés B, le raccord au journal et les formats de retrait restent NON ADOPTÉS, sans code B ni effet TPM/SQL.

## PA01-SL14 — correction du profil cible D9 — 4 novembre 2026

Le contrat D9 adopté fixe target.environments à physical, vm et docker comme cibles distinctes. Le parseur src/pixs/pa_native/build_profile.py refusait encore Docker ; sa comparaison fermée est alignée sur les trois valeurs. Le fixture tests/unit/test_pa_native_build_profile.py inclut maintenant Docker. Empreintes finales : build_profile.py SHA256 26e736ef358e2fab55807f88c72d2aff59201e2d89b49df5a70f9d8424f8b257 ; test_pa_native_build_profile.py SHA256 57e03444dbb2cf4665f09590869b1cc714b93af6d346c9ed5cc71faa4b47eda3.

Preuves courantes sous CAB :

- Edit du fixture : requestId fa2152dc-c9b7-4a3a-b2d1-9720ec16399d, RELEASED/COMPLETED, fencing 14050.
- Correction du parseur : requestId 9465e9d2-01b8-4c74-a16b-25d4512d7906, RELEASED/COMPLETED, fencing 14059.
- Test ciblé : PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest discover -s tests/unit -p test_pa_native_build_profile.py -v ; requestId 310eb72a-5174-4758-abb3-dd70316c683a, exit 0, 13 tests, 0 échec, 0 erreur, 0 saut, 0.012 s ; accès RELEASED/COMPLETED, fencing 14062. Une tentative préalable sans PYTHONPATH s’est arrêtée avant import par ModuleNotFoundError pixs ; aucune assertion n’a été exécutée, résultat non compté.
- Syntaxe : /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/pa_native/build_profile.py ; requestId 67823916-ca7f-4512-88d8-5f99837ef52b, exit 0 ; accès RELEASED/COMPLETED, fencing 14066.
- Strict ciblé après la correction : /home/devops/.local/npm/bin/openspec validate add-pa-native-build-and-component-composition --strict ; requestId e6085e2a-093c-4a50-a81e-e3b1da94e8db, exit 0, « Change add-pa-native-build-and-component-composition is valid » ; accès RELEASED/COMPLETED, fencing 14069.

Portée : le parseur accepte la cible déclarée et conserve son profil fermé. Ces tests structurels ne qualifient ni Docker local, ni physique/VM, ni runtime/ABI/dépendances, compilation, adaptateur, PZT ou recette produit. Docker et LXC restent distincts. Aucun code B, effet TPM/SQL, adoption C08/Z12, installation, livraison ou activation n’est réalisé ou déduit ; les tâches globales restent non cochées.

## PA01-SL14 — contrats PostgreSQL non-B vérifiés — 4 novembre 2026

Le contrôle ciblé `PostgresqlContractsTest` seul vérifie `NativeRequest`, `NativeResult` et `TechnicalPlan` : 12 tests, 0 échec, 0 erreur, 0 saut, durée 0.004 s, exit 0. Commande : `PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_native_postgresql_contracts.PostgresqlContractsTest -v`. Reçu CAB : requestId `0953067e-39b4-48e6-9841-9132ce3f72e3`, accès RELEASED/COMPLETED, fencing 14081.

Empreintes au contrôle : `src/pixs/pa_native/postgresql_contracts.py` SHA256 `137e6c110659a3fc1d85a72f499777bab2a15003fe06218552d0f54acae307fd` (39675 octets) ; `tests/unit/test_pa_native_postgresql_contracts.py` SHA256 `b9820c1ba69ee5dbc3d175bfbadfe9dc87eebb509b7743a9b0da0b732f923ac5` (27190 octets).

Limites : seules les méthodes de `PostgresqlContractsTest` ont été exécutées ; les classes `InitialMandateContractsTest`, `AnchorSnapshotContractsTest` et les tests `JournalTransition` n’ont pas été lancés. Aucun format B n’est adopté, testé ou qualifié par cette preuve. Aucune connexion SQL, autorité, TPM, C08/Z12, runtime/Docker, installation, livraison/activation ou effet réel n’est prouvé. Le sous-lot SL14 reste EN COURS et la tâche globale 4 non cochée.

## PA01-SL14 — Observation PostgreSQL non-B vérifiée — 4 novembre 2026

Le contrôle ciblé de `ObservationTest` vérifie uniquement le codec de forme/octets du manifeste Observation PostgreSQL 1.0.0 : 12 tests, 0 échec, 0 erreur, 0 saut, durée 0.006 s, exit 0. Commande : `PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_postgresql_observation.ObservationTest -v`. Reçu CAB : requestId `4de29b67-1ba9-4419-a438-e63d2185063f`, operationId `op-cismp7-pa01-sl14-observation-test-9f382808-1d91-4860-9f17-60cbe6458973`, accès RELEASED/COMPLETED, fencing 14106.

Empreintes au contrôle : `src/pixs/pa_native/postgresql_observation.py` SHA256 `3f635ca3ceeca7aa14b9c731aede1c06b68c1801de3cb1efb0cf70505870cbb3` (15468 octets) ; `tests/unit/test_pa_postgresql_observation.py` SHA256 `ff6312b1b613638dd869914655288d13defcddddfc575233b28a384b8a36f7d9` (18959 octets).

Limites : aucune base, SQL, autorité, horloge réelle, installation, Docker/runtime, TPM, C08/Z12, livraison ou activation n’est impliqué. Aucun format B, raccord JournalTransition ou format de retrait n’est adopté ni qualifié. SL14 reste EN COURS et la tâche globale 4 reste non cochée.

## PA01-SL14 — Préconditions PostgreSQL E5-PRE non-B vérifiées — 4 novembre 2026

Le test ciblé de `PreconditionsFormTest` vérifie le codec de forme du manifeste PostgreSQL E5-PRE 1.0.0 : 17 tests, 0 échec, 0 erreur, 0 saut, durée 0.009 s, exit 0. Commande : `PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_postgresql_preconditions.PreconditionsFormTest -v`. Reçu CAB : requestId `42931c78-6d7d-4639-a050-769d788864bf`, operationId `op-cismp7-pa01-sl14-preconditions-test-59c62df3-702d-47c5-b1ac-9d8510b44597`, accès RELEASED/COMPLETED, fencing 14126.

Empreintes au contrôle : `src/pixs/pa_native/postgresql_preconditions.py` SHA256 `27d290b104f3f723a4f8f96fb38665a91d131b9da23b5c1b3040d7d3120a44fb` (16988 octets) ; `tests/unit/test_pa_postgresql_preconditions.py` SHA256 `576350010b416d646fca110412b91657bed0e8d1c30f5061c9f55e45e53d01b1` (14019 octets).

Limites : codec seul ; aucun accès DB, requête SQL, service, autorité, TPM, C08/Z12, runtime/Docker, effet réel, livraison ou activation n’est testé ou déduit. Aucun format B, raccord JournalTransition ou format de retrait n’est adopté par cette recette. SL14 reste EN COURS et la tâche globale 4 non cochée.

## PA01-SL14 — Effets PostgreSQL E5-EFF non-B vérifiés — 4 novembre 2026

Le test ciblé de `EffectsTest` vérifie uniquement le codec de forme/octets du manifeste PostgreSQL E5-EFF 1.0.0 : 10 tests, 0 échec, 0 erreur, 0 saut, durée 0.002 s, exit 0. Commande : `PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_postgresql_effects.EffectsTest -v`. Reçu CAB : requestId `84f19eed-2e22-4385-a69d-4af263da1f4a`, operationId `op-cismp7-pa01-sl14-effects-test-fa8dc8ab-8394-45ab-89e4-71305c8d5f2f`, accès RELEASED/COMPLETED, fencing 14143.

Empreintes au contrôle : `src/pixs/pa_native/postgresql_effects.py` SHA256 `d15613ca8dee713563a1ad61604bf8094a472f4127e5575800f73226e187db5e` (11214 octets) ; `tests/unit/test_pa_postgresql_effects.py` SHA256 `d464f1f1a36aac70b39c7dc6aa623ed87c1d40ff0d8d33860ad62931b9e63d88` (10112 octets).

Limites : codec seul ; aucun accès DB, requête SQL, service, autorité, TPM, C08/Z12, runtime/Docker, effet réel, installation, livraison ou activation n’est testé ou déduit. Aucun format B, raccord JournalTransition ou format de retrait n’est adopté ni qualifié. SL14 reste EN COURS et la tâche globale 4 non cochée.

## PA01-SL14 — Mandat initial PostgreSQL E4 non-B vérifié — 4 novembre 2026

Le contrôle ciblé de `InitialMandateContractsTest` vérifie uniquement la représentation de forme/octets du mandat initial PostgreSQL E4 1.0.0 : 10 tests, 0 échec, 0 erreur, 0 saut, durée 0.008 s, exit 0. Commande : `PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_native_postgresql_contracts.InitialMandateContractsTest -v`. Reçu CAB : requestId `deb5ad0a-f3c0-407b-9d93-36eb2c9c6c75`, operationId `op-cismp7-pa01-sl14-initial-mandate-test-retry-50ee05c2-f408-4521-8350-e448130d2388`, accès RELEASED/COMPLETED, fencing 14160.

Empreintes au contrôle : `src/pixs/pa_native/postgresql_contracts.py` SHA256 `137e6c110659a3fc1d85a72f499777bab2a15003fe06218552d0f54acae307fd` (39675 octets) ; `tests/unit/test_pa_native_postgresql_contracts.py` SHA256 `b9820c1ba69ee5dbc3d175bfbadfe9dc87eebb509b7743a9b0da0b732f923ac5` (27190 octets).

Limites : les enveloppes utilisent uniquement des signatures factices de 64 octets ; aucune vérification Ed25519, provenance de clé, autorité, fraîcheur d’horloge ou droit n’est démontré. Aucune connexion/base PostgreSQL, requête SQL, TPM, PZT, C08/Z12, runtime/Docker, installation, livraison ou activation n’est impliqué. Aucun format B, ancrage AnchorSnapshot ou raccord JournalTransition n’est adopté ou qualifié par cette recette. SL14 reste EN COURS et la tâche globale 4 non cochée.

## PA01-SL14 — AnchorSnapshot D10–D12 : codec public synthétique vérifié — 4 novembre 2026

Le contrôle ciblé de `AnchorSnapshotContractsTest` vérifie uniquement la représentation de forme/octets d’instantanés publics synthétiques : 10 tests, 0 échec, 0 erreur, 0 saut, durée 0.003 s, exit 0. Commande : `PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_native_postgresql_contracts.AnchorSnapshotContractsTest -v`. Reçu CAB : requestId `8bb49b24-3797-4d20-b313-713bec6e3e87`, operationId `op-cismp7-pa01-sl14-anchor-snapshot-test-aedb58cd-4b81-4fb0-93b4-9959381ecc76`, accès RELEASED/COMPLETED, fencing 14176.

Empreintes au contrôle : `src/pixs/pa_native/postgresql_contracts.py` SHA256 `137e6c110659a3fc1d85a72f499777bab2a15003fe06218552d0f54acae307fd` (39675 octets) ; `tests/unit/test_pa_native_postgresql_contracts.py` SHA256 `b9820c1ba69ee5dbc3d175bfbadfe9dc87eebb509b7743a9b0da0b732f923ac5` (27190 octets).

Limites : formes/octet seulement, avec snapshots synthétiques ; aucune lecture ou écriture TPM/NV, vraie ancre, HMAC, provenance d’autorité, horloge courante, SQL/PostgreSQL, PZT, Docker/runtime, installation, livraison ou activation n’est qualifié. Le test n’adopte ni format B, mapping ou séquence de publication, ni JournalTransition et ne valide aucun retrait réel. SL14 reste EN COURS et la tâche globale 4 non cochée.

## PA01-SL14 — Profil PostgreSQL Unix/peer structurel non-B vérifié — 4 novembre 2026

Le test ciblé de `PeerProfileTest` vérifie le parseur TOML fermé du profil local PostgreSQL Unix/peer : 8 tests, 0 échec, 0 erreur, 0 saut, durée 0.002 s, exit 0. Commande : `PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_native_postgresql_profile.PeerProfileTest -v`. Reçu CAB : requestId `fe6712ab-4f77-4cf9-8d3f-9e7062a4fc9b`, operationId `op-cismp7-pa01-sl14-peer-profile-test-ef2c9605-9be4-40b1-901d-7d541134dedd`, accès RELEASED/COMPLETED, fencing 14188.

Empreintes au contrôle : `src/pixs/pa_native/postgresql_profile.py` SHA256 `a80280363730c35116d8b52e771b5f9cad205851887cfdc29f32028966bc438d` (4173 octets) ; `tests/unit/test_pa_native_postgresql_profile.py` SHA256 `3ad71746a63da25f5e010c9b0ff036f18d3dacb6d5ff3e0906e99cb16239961e` (4046 octets).

Limites : profil synthétique uniquement ; aucune ouverture de socket, connexion PostgreSQL, règle HBA peer actuelle, identité système courante, credential, environnement, SQL, TPM, PZT, C08/Z12, runtime/Docker, installation, livraison ou activation n’est vérifié. Aucun format B, ancrage matériel, JournalTransition ou effet réel n’est adopté ou qualifié. SL14 reste EN COURS et la tâche globale 4 non cochée.

## PA01 — validation stricte après l’addendum B/retrait — 4 novembre 2026

Le statut courant du 4 novembre a été ajouté à la fin de design.md, sans réécrire les mentions historiques du 3 novembre. Empreinte SHA256 finale de design.md : 50ffc72f1e1f43da42c469d734184aba1455b2a8bdbe63fb77dc407406628e55. contracts.md et tasks.md portaient déjà la décision courante et restent inchangés ; le statut existant de la présente VALIDATION.md est conservé.

Validation stricte : /home/devops/.local/npm/bin/openspec validate add-pa-native-build-and-component-composition --strict ; résultat exact : Change 'add-pa-native-build-and-component-composition' is valid ; exit 0. Reçu CAB : requestId cismp7-pa01-bstatus-design-strict-18e13bbc-832f-4553-aaa7-ac9baeb50ca5, operationId op-cismp7-pa01-bstatus-design-strict-18e13bbc-832f-4553-aaa7-ac9baeb50ca5, décision APPROVED, permission once acquittée, opération native COMPLETED/exit 0, accès RELEASED/RECONCILED fencing 14198.

Cette validation porte sur la cohérence OpenSpec ; aucun test produit ni qualification n’est ajouté. Le principe B reste acquis seul ; aucune case, aucun format détaillé, code B, effet TPM/SQL, adoption C08/Z12, qualification runtime/Docker, livraison ou activation n’est déduit.

## PA01-SL14 — D14 MainPID : recettes exécutées sur LXC — 5 novembre 2026

Le premier passage des 54 tests a échoué dans le sous-cas main0 de test_mpid_refusals : l’attendu du fixture était le stade 8, tandis que l’implémentation retourne le stade 10 avec PA01SO_STATE/ESRCH. La spécification exige le refus de MainPID zéro, sans fixer ce numéro de stade. Le second échec observé était la fermeture du fixture après cette assertion divergente. L’édition a corrigé uniquement l’attendu du test, de 8 à 10 ; aucun code produit n’a changé. Reçu d’édition : requestId req-3b2a7674-7043-4b62-b375-741a104bee91, operationId op-cismp7-pa01-d14-main0-stage-6d619da12ee8, appel natif call_01a1a8c7c4d47679937112886d9bd83e, exit 0.

Après transfert des trois sources aux empreintes relues par CAB, compilation et exécution sur CT100 : Ran 54 tests in 0.065s, OK, exit 0 ; 54 réussites, 0 échec, 0 erreur, 0 saut. Environnement observé : CPython 3.14.9 avec GIL, Cython 3.3.0, cc (Debian 14.2.0-19) 14.2.0. Reçu CAB : requestId req-3ee2108f-00ef-46d0-ad50-4d78d0604caf, operationId op-cismp7-pa01-sl14-d14-397dd3a2b4244462, appel natif call_01a1a8d021807493a5a75116167ff465, once acquittée, exit 0, accès RELEASED/COMPLETED, fencing 14289.

Empreintes des sources utilisées : src/pixs/pa_native/systemd_observation.pyx SHA256 5eab03f5db581f66814911f933458d14bba329d01119c5d5335781a147e1d787 (119195 octets) ; tests/native/test_systemd_observation.py SHA256 d9aad273a2dea120c15e6895160573552151ad365b5d1539d6f9cb3b063e3599 (64406 octets) ; tests/native/fixtures/systemd_observation_driver.c SHA256 b3c21cc93d0d0a35e43b12203934a5d82b9e2e69ac3330b61a482feb4fb9d562 (37149 octets).

Les deux répertoires temporaires de cette campagne ont été supprimés puis leur absence vérifiée sur CT100. Nettoyage : requestId req-98b8f9d8-6925-4ece-bdbd-c53aa7864465, operationId op-cismp7-pa01-sl14-clean-478e9b477a1240a5, exit 0, fencing 14296. Vérification : requestId req-f5057aae-ad5e-4a88-8dc4-6ca73970bc48, operationId op-cismp7-pa01-sl14-verify-clean-a903bd44661843dd, exit 0, fencing 14301. Les runtimes et bibliothèques installés ont été conservés ; la réservation test tests-pa01-toolchain-inventory-20261102-08f6c727-dee4-4ddb-8725-33022fe494f7 reste HELD pour la suite du même RUN.

Limites : le conducteur lie le code Cython réel à un SDK sd_bus simulé et utilise des sockets/pidfds locaux. Aucune bibliothèque libsystemd réelle ni aucun manager systemd n’a été lié ou utilisé ; ces 54 tests ne qualifient ni manager/unité réels, identité forte, politique, UTC ou gardien D13. Ils ne prouvent aucun accès TPM/NV, SQL, Docker, C08/Z12, format B, raccord JournalTransition, livraison ou activation. D14 n’est pas globalement achevé et la tâche globale 4 demeure non cochée.

### Recette live MainPID réelle — 5 novembre 2026

Une recette réelle unique SystemdManagerLiveMainPIDTest.test_live_transient_mainpid_self_and_invocation_id a réussi sur CT100/hvp1 dans l’unité pixs-pa01-d14-mainpid-9ab1fd14-33.service (bus /run/systemd/private, CPython 3.14.9 avec -I -B, systemd-run --wait --collect --pipe, RuntimeMaxSec=60s). Résultat : 1 test, 0 échec, 0 erreur, 0 saut, code 0 ; systemd SUCCESS, MainProcess exit 0, runtime 217 ms. Source tests/native/test_systemd_observation.py ; readelf -d a rapporté les dépendances directes libsystemd.so.0 et libc.so.6. Limites : cette seule recette ne qualifie pas identité forte, politique, cycle UTC, D13, TPM/NV, SQL, Docker, C08/Z12, formats B, JournalTransition, livraison ou activation.
### Inventaire runtime du paquet libsystemd0 — 6 novembre 2026

Un `dpkg-query -W -f='${Package} ${Version} ${Status}\n' libsystemd0` exécuté sur CT100/hvp1 via SSH (`StrictHostKeyChecking=yes`) a retourné `libsystemd0 257.13-1~deb13u1 install ok installed`, SSH exit 0 et commande native exit 0. Stage CAB scellé `stage-cismp7-pa01-libsystemd-c3c768192a8f46c8` (3352 octets, SHA-256 `4ba3fbd4d4a73078f6edfe1ffdd138032dd22e56cbd5ef0f6c898583a7cc05c4`) ; request `req-cismp7-pa01-libsystemd-c3c768192a8f46c8`, operation `op-cismp7-pa01-libsystemd-c3c768192a8f46c8`, appel natif `call_01a1ae1e4f88771f927f4cca25164e12`, permission `per_1ae1e56ad001Ckijz0ctYe9xtz`, `onceAcknowledged=true`, résultat `COMPLETED/exit 0`, accès `RELEASED` fencing 14602. La réservation de test LXC reste `HELD` fencing 13953. Cet inventaire porte sur `libsystemd0`, distinct de `libsystemd-dev` mentionné dans le relevé initial ; il ne prouve ni ABI, ni linkage, ni qualification complète du runtime ou d’un manager systemd. La tâche 4 reste non cochée.

### Test ciblé du codec JournalTransition PostgreSQL 1.0 — 6 novembre 2026

La commande `PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_native_journal_contracts.JournalContractTest -v` a terminé avec `Ran 24 tests in 0.006s` et `OK` : 24 réussites, 0 échec, 0 erreur, 0 saut, exit 0. Fichiers relus : `tests/unit/test_pa_native_journal_contracts.py` SHA-256 `f0d506b563ed4bd503685947b6fd015a484804835993da6c8795371dd22c82bf` ; `src/pixs/pa_native/postgresql_contracts.py` SHA-256 `137e6c110659a3fc1d85a72f499777bab2a15003fe06218552d0f54acae307fd`. Reçu CAB : request `req-cismp7-pa01-sl14-journal-test-ca86596730e44128`, operation `op-cismp7-pa01-sl14-journal-test-ca86596730e44128`, appel natif `call_01a1ae42514e76d693fdef233c6d1e00`, permission `per_1ae42547e001fq64CeKrgvyPIV`, `onceAcknowledged=true`, opération `COMPLETED/exit 0`, accès `RELEASED/COMPLETED` fencing 14622. Cette suite teste uniquement le codec synthétique en mémoire ; elle ne réalise ni connexion ou requête PostgreSQL, ni effet SQL, TPM/NV, LXC, ne qualifie pas ABI/runtime, et n’adopte pas B/C08/Z12. La tâche 4 reste non cochée.

### Recettes live D14 MainPID positive et refus MainPID=0 — 6 novembre 2026

Le fichier source tests/native/test_systemd_observation.py, modifié dans cette unité, compte 77107 octets et porte le SHA-256 e475627ccb7939af9b24d1e340b29a7adfdd3ecf2eb333d96b5833237c23783a. Il a été transféré dans l’espace de test temporaire de CT100/hvp1 et son SHA-256 distant a été vérifié identique. Le contrôle py_compile distant sous CPython 3.14.9 avec -I -B a terminé avec exit 0. Reçus distincts : transfert req-cismp7-pa01-sl14-test-transfer-20261106-02 / op-cismp7-pa01-sl14-test-transfer-20261106-02 / call call_01a1aebde16b75939acf8b98e737bf41 / permission per_1aebdeb48001m1LyAgFS1LF9h8 ; vérification SHA req-cismp7-pa01-sl14-test-transfer-verify-20261106-03 / op-cismp7-pa01-sl14-test-transfer-verify-20261106-03 / call call_01a1aec0b03f756dba3ca8f04a488a68 / permission per_1aec0ba1d001eZ8njWl7jvnfuP ; py_compile req-cismp7-pa01-sl14-remote-pycompile-20261106-01 / op-cismp7-pa01-sl14-remote-pycompile-20261106-01 / call call_01a1aec395ab7657abd45cd2a6adfaf1 / permission per_1aec39fa5001isSrba4vWFXJ15. Chaque opération a été approuvée, once acquittée et terminée avec exit 0.

| Recette réelle | Environnement et résultat observé | Reçu CAB |
|---|---|---|
| Positive test_live_transient_mainpid_self_and_invocation_id | Unité pixs-pa01-d14-positive-20261106-01.service, systemd Type=exec, CPython 3.14.9 -I -B : 1 test, 1 PASS, 0 fail/error/skip, 0.131 s ; systemd-run exit 0, runtime 566 ms. Vérifie la connexion, l’unité attendue, l’identité du processus MainPID et l’InvocationID. | request req-cismp7-pa01-sl14-positive-live-20261106-06 ; operation op-cismp7-pa01-sl14-positive-live-20261106-06 ; call call_01a1aec9b24c70d7980e4c02269a0bc7 ; permission per_1aec9be0f001niWapQPWtNFIQF ; once acquittée. |
| Refus MainPID=0 test_live_mainpid_zero_refused_state | Unité pixs-pa01-d14-mainpid0-20261106-01.service, Type=forking, GuessMainPID=no ; le processus de test est enfant dans le même cgroup. CPython 3.14.9 -I -B : 1 test, 1 PASS, 0 fail/error/skip, 0.042 s ; systemd-run exit 0. Branche rc4/stage10/errno.ESRCH/cleanup0 et close rc4 avec les mêmes diagnostics ; aucun mpid_snapshot après refus. Le lookup snapshot vérifie l’unité attendue et un InvocationID non nul. | request req-cismp7-pa01-sl14-mainpid0-live-20261106-07 ; operation op-cismp7-pa01-sl14-mainpid0-live-20261106-07 ; call call_01a1aed38c8b77b5bff54e520f431fe6 ; permission per_1aed39896001wykKE8j6m5TFT2 ; once acquittée. |

Les deux recettes ont chargé l’artefact systemd_observation.cpython-314-x86_64-linux-gnu.so de SHA-256 7b302290939db1eb828fbbd1d764257766d7326f2ed3c7ea962618a697ab4fcd. La copie distante du source de test et son .pyc temporaire ont ensuite été supprimés puis leur absence vérifiée ; l’artefact compilé et CPython 3.14.9 ont été conservés. Nettoyage et vérification : req-cismp7-pa01-sl14-test-cleanup-20261106-08 / op-cismp7-pa01-sl14-test-cleanup-20261106-08 / call call_01a1aeda0aec718f99984b6ee49d5a05 et req-cismp7-pa01-sl14-test-cleanup-verify-20261106-09 / op-cismp7-pa01-sl14-test-cleanup-verify-20261106-09 / call call_01a1aedd094d73cf95333d154863e5ea ; once acquittée dans les deux cas. Accès groupé RELEASED/COMPLETED fencing 14662 ; bail LXC HELD fencing 13953, reconciliationRequired=false.

Limites : ces deux cas live D14 ne qualifient pas toute l’ABI ni les dépendances transitives, l’identité forte, la politique, UTC, D13, TPM/NV, SQL, Docker, transport PZT ou les raccords C08/Z12. Ils n’adoptent aucun format B et ne prouvent ni livraison ni activation. La tâche globale 4 reste non cochée.

### Test ciblé NativeLinkerRefusalTest — 6 novembre 2026

`PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_native_linker -v` : 21 tests, 21 PASS, 0 échec, 0 erreur, 0 saut, 0.409 s, exit 0. Reçu `req-cismp7-pa01-sl14-native-linker-test-20261106-04 / op-cismp7-pa01-sl14-native-linker-test-20261106-04 / call_01a1af7c4e0f7301a524e5efe605ea0f / per_1af7c533c001Qs6bIVkFYKMVV9`, `once true`, accès `RELEASED/COMPLETED fencing14690`. Code `linker.py` SHA `bc3b2b42df72295fd122512d482a086be520ac98dfe09485b0d2df5bfb2934c0` ; test `test_pa_native_linker.py` SHA `6ef4fbf25815d7da7d750f4ae8afb76a5f752978dbd37ce4c14a675569fa1497`. `output/tests/pa01-linker` vide. Portée : fixtures synthétiques et mocks, aucun sous-processus ni liaison/compilation réelle ; chemin système/runpath accepté simulé. Ne prouve ni ABI/ELF/runtime ni qualification D14 globale. Aucun code source changé. Tâche 4 décochée, PA01 2/10.

### Inventaire du paquet de développement systemd — 6 novembre 2026

Le helper temporaire `output/cismp/cismp7-pixs-023c11510a274b19/qualification-pa01/pa01-libsystemd-dev-inventory.py` a interrogé à distance `/usr/bin/dpkg-query -W -f='${Package} ${Version} ${Status}' libsystemd-dev` sur CT100/hvp1 via SSH à hôte vérifié. Résultat exact : `libsystemd-dev 257.13-1~deb13u1 install ok installed`, exit SSH 0 et exit natif 0. Le code du helper SHA-256 `af228dbd5633e392f0587667fe797f99eab5e6e28dca1524051daa70e653456a` a utilisé `tests/native/pa01_ssh_probe.py` pour charger localement la configuration SSH ; aucune valeur de credential n’a été retournée. Reçu de l’inventaire : request `req-cismp7-pa01-sl14-lxc-libsystemd-dev-inventory-20261106-02`, operation `op-cismp7-pa01-sl14-lxc-libsystemd-dev-inventory-20261106-02`, call `call_01a1afc6f87175bab2d208b4757b026a`, permission `per_1afc6fc05001bsIobOARoILeU2`, `onceAcknowledged=true`, accès `RELEASED/COMPLETED fencing14711`, releaseDigest `c140a861eeec9dffba76e8fd98cfafe4f5986ba48c3f131bffe430a305627c75`. Création du helper : request `req-cismp7-pa01-sl14-lxc-inventory-helper-20261106-03`, call `call_01a1afc2f8a07570bba0c13cbc026416`, permission `per_1afc309de001aV7g1iYRi1aCqX`, accès `RELEASED/COMPLETED fencing14708`. Suppression du seul helper : request `req-cismp7-pa01-sl14-lxc-inventory-helper-cleanup-20261106-05`, call `call_01a1afcaea7375e4a86c7813460f1815`, permission `per_1afcaef9500160dAMwqUOfmfFH`, `rm` exit 0, accès `RELEASED/COMPLETED fencing14716` ; absence revérifiée. Le bail de test LXC reste `HELD` fencing13953.

Limites : cet inventaire confirme seulement l’état dpkg déclaré pour le paquet de développement. Il ne vérifie pas le contenu des en-têtes, ne compile ni ne lie de module Cython et ne prouve aucune ABI, runtime ou qualification produit. Aucun paquet n’a été installé ou modifié. Tâche 4 non cochée, PA01 2/10.

### Inventaire des en-têtes et métadonnées ELF de libsystemd-dev — 6 novembre 2026

Le premier lancement du helper temporaire s’est arrêté localement avec exit 2, status LOCAL_CONFIG et code OK, avant tout démarrage de SSH. La cause vérifiée était un contrat de données erroné : tests/native/pa01_ssh_probe.py retourne (host, user, password bytes), alors que le helper attendait un dictionnaire. Le helper a été corrigé selon ce tuple ; sa vérification de syntaxe py_compile sur le Python DevOps a réussi avec exit 0. Le cache temporaire py_compile a été supprimé et son absence vérifiée.

Une première émission shell du helper corrigé a été refusée avant once, car l’empreinte approuvée omettait workdir. La permission a été rejetée avec reçu ACKNOWLEDGED/HTTP 204 ; l’opération a été retirée avant once et l’accès libéré RECONCILED. Aucun SSH n’a démarré sur cette tentative. La nouvelle demande inclut l’objet natif complet command + workdir.

L’opération finale sur CT100/hvp1 a terminé avec helper status DONE, exit natif 0 et ssh_exit 0. Reçus CAB : request req-cismp7-pa01-sl14-lxc-systemd-dev-files-20261106-03 ; operation op-cismp7-pa01-sl14-lxc-systemd-dev-files-20261106-03 ; call call_01a1b0b54d92729e8a7068e06258e662 ; tool_input_sha256 4da955b1fef5f9f694b575ce1b199dca6c4869e9aafc24c01bfbe107c6b6a2a1 ; once acquittée ; nativeResult completed/exit 0 ; accès RELEASED/COMPLETED, fencing 14761, releaseDigest ed95bebdda327e8dc5c84ba02231c571d9c3e779afa7564694a3f493042fa1b9. Le bail de test LXC reste HELD, fencing 13953, reconciliationRequired=false.

| Vérification distante | Résultat observé |
|---|---|
| Architecture | x86_64 |
| En-têtes | /usr/include/systemd/sd-bus.h lisible, 30 597 octets ; /usr/include/systemd/sd-id128.h lisible, 8 657 octets |
| Fichier pkg-config | /usr/lib/x86_64-linux-gnu/pkgconfig/libsystemd.pc lisible, 560 octets |
| pkg-config | pcfiledir /usr/lib/x86_64-linux-gnu/pkgconfig ; libdir /usr/lib/x86_64-linux-gnu ; version 257 ; cflags sans sortie ; libs -lsystemd |
| Bibliothèque partagée | /lib/x86_64-linux-gnu/libsystemd.so.0 pointe vers libsystemd.so.0.40.0 ; SONAME libsystemd.so.0 |
| DT_NEEDED direct | libcap.so.2, libm.so.6, libc.so.6, ld-linux-x86-64.so.2 |

Le helper temporaire, SHA-256 c86ae59213e69e77a1006d2189fdb274420515c796a240c1667ad3d5ff72b1d0, a été supprimé après l’inventaire et son absence a été confirmée. L’opération n’a installé ni modifié de paquet ou fichier distant. Le relevé ne vérifie pas le lien de développement libsystemd.so, une compilation C/Cython, le linkage réel, l’ABI ou un runtime systemd complet ; il ne constitue pas une qualification D14/PA01 globale. La tâche globale 4 reste non cochée et PA01 reste à 2/10.

### Verrou Cython de la campagne et revue PyPI — 6 novembre 2026

La cible D1 actuelle et les sources de développement gardent Cython 3.3.0 : pyproject.toml déclare Cython==3.3.0 et DEVOPS.md observe 3.3.0. Le RUN courant a débuté le 22 octobre 2026. La page PyPI de Cython 3.3.0 date ce dernier au 22 août 2026 et ne le marque pas comme retiré ; PyPI indique l’absence de provenance pour ses fichiers. Les empreintes officielles consultées sont :
- cython-3.3.0.tar.gz : eed0d93fbca7087f143b42c34b05a825849bdf17f101572c2105acfa49aa88b8 ;
- cython-3.3.0-py3-none-any.whl : 9b24b5c8cd536946b62086fcafee6d5509d3f549f72d553d2336af87ffbe0da1 ;
- cython-3.3.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl : 82f94565b6001bab8e31bf52a0911672910b5735910612a2c0f772c719670006.

À la vérification PyPI du 6 novembre, Cython 3.3.1 est la dernière version classée Production/Stable, publiée le 1er novembre 2026. PyPI n’atteste pas la provenance des fichiers de cette version ; les empreintes publiées sont cython-3.3.1.tar.gz e0e45989e821bef6aa9ae15c7d583ab5e055f7406c4b3624e49e06d24e90375a et le wheel CPython 3.14 Linux x86_64 7a6c191617853f2e0d5936c73f5d5cd096548f4d9e0fa37612ef721591c42cb3. Les pages sources consultées : https://pypi.org/project/Cython/3.3.0/ et https://pypi.org/project/Cython/3.3.1/.

L’historique de publication PyPI montre 3.3.0 avant 3.3.1 ; il permet d’inférer que 3.3.0 était la dernière stable disponible au début du RUN le 22 octobre. Cette vérification du 6 novembre est rétrospective, pas un instantané archivé du 22 octobre. Le verrou 3.3.0 est conservé pour le RUN en cours selon D1 et la règle de conservation du verrou pendant une campagne ; 3.3.1 sera réévalué au début d’une campagne ultérieure. Aucun paquet n’a été téléchargé, installé ou mis à jour. Ces métadonnées ne qualifient pas une compilation Cython, l’ABI ou le runtime ; tâche 4 et PA01 restent non cochées à 2/10.

### Test unitaire ciblé du constructeur PA01 — 6 novembre 2026

La commande `PYTHONPATH=src:tests/unit /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest test_pa_native_builder -v` a terminé avec `Ran 82 tests in 0.663s OK`, exit 0. Reçu CAB : requestId `req-cismp7-pa01-sl14-builder-unit-rev-20261106-02`, operationId `op-cismp7-pa01-sl14-builder-unit-rev-20261106-02`, appel natif `call_01a1b1d9e4f671e6892f62957c15174e`, once acquittée, nativeResult completed/exit 0 ; accès RELEASED/COMPLETED fencing 14830. Sources observées : `src/pixs/pa_native/builder.py` SHA-256 `b5842edbfe7d80b8e70dc5e924871f8fab710e16bd3fbad427845518db332d02` ; `tests/unit/test_pa_native_builder.py` SHA-256 `8ff1fc23b97b35c33b4a4d624f946cea518a0d9347edbbad5404f69e42cebccc`. Le répertoire `output/tests/pa01-builder` était vide avant et après ; aucun artefact de test ne reste. Cette suite unitaire ne constitue pas une compilation Cython réelle, une liaison, une validation ABI ou un runtime produit. Aucune source de production n’a été modifiée ; tâche 4 reste ouverte et PA01 à 2/10.

