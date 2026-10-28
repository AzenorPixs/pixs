# Validation C14 — campagne en cours

## État et portée

Relevé du 2026-10-23T13:03:34.360394+00:00.
Le RUN CISMP4 porte uniquement sur add-essential-pbo-pzt-and-dns-modules.
Les tâches 1.1,1.2,2.1,2.2 conservent leurs validations historiques ; 2.3
reste non cochée. Les réalisations propres sont écrites. Le build et le rendu
frontend réellement composés avec C11 restent à prouver avant validation de2.3.
Aucun archivage ni déploiement n'est réalisé par ce rapport.

Le développeur a demandé les réalisations d'abord, puis les tests et la
validation. Les coches ne sont pas des preuves. Les contrôles ci-dessous
rapportent des sorties natives observées ; leurs limites restent applicables.

## Preuves courantes exécutées

| Contrôle | Volume observé | Appel natif | Résultat |
|---|---|---|---|
| DTO/catalogue/OpenAPI et fragments dans le vrai validateur commun | 20 tests | call_01a168d8f70c7585879daf018e54c5c8 | PASS |
| Profil AST des deux sources réelles | 2 tests | call_01a1686ff72372b488718853be723420 | PASS |
| Pages et adapter public, moteur double explicite | 10 tests Node | call_01a1686ff72372b488718853be723420 | PASS |
| Même suite dans les navigateurs déclarés | 10 Chromium + 10 Firefox | call_01a168760104719688218cd979931d79 | PASS |
| Manifests actuels, composition et refus essentiels | 41 tests | call_01a1684149b1752aa9a827c257a0bc2f | PASS |
| HTTP C14 avec C03/C04/C05, contexte WEB C11, garde inter-onglets et PostgreSQL réels | 43 cas | call_01a168d9a84876eb994c6a7e6ffdb4f8 | PASS |
| Catalogue Python réel vers clients publics JavaScript | 4 critères,33 chemins,33appels,11refus | call_01a168b2602974dd8805e485fc48f8f3 | PASS |
| Syntaxe Python/JavaScript initiale du périmètre | 38 Python + 5 JavaScript | call_01a1684037c075809438c1e314dedb35 | PASS |
| Recompilation des quatre Python corrigés | 4 Python, 3.14.9 | call_01a1685fd7ad7656ab801c18a45869f3 | PASS |
| Références canoniques courantes | 21 références,25liens,2SHA | call_01a1685eb07774579db2eab8ef076cc2 | PASS |


Le contrôle OpenSpec strict a réussi le23octobre sous
call_01a168424a42732e931a5c7f9618914d. Son information skip_specs confirme
l'absence de delta de spécification de ce change. Les ajouts documentaires
postérieurs doivent être recoupés dans la validation finale, sans déduire
de ce strict une validité fonctionnelle.

La recette HTTP utilise Django6.1.2 et PostgreSQL16.14 réels dans un schéma
jetable dont l'identité et le propriétaire sont vérifiés. Les migrations
Auth/Core/PZT/DNS sont effectivement appliquées. Les43cas retournent true ;
cleanup et conns_closed valent true. Le provisionnement opérateur/C10 de
l'amorçage de fixture ne constitue pas une qualification de ces propriétaires.

Les gardes applicatives HTTPS, Host, Origin et CSRF sont exercées par
RequestFactory. Aucun TLS déployé n'est qualifié. Les onze opérations
propriétaires et les documents publics passent par les frontières communes.
Les demandes ordinaires de dispense ne retirent pas l'audit persisté.
Une révocation ferme la lecture sans data ; le service C14 peut normaliser
les faits Auth illisibles en503 SERVICE_UNAVAILABLE. Ce résultat n'est pas
présenté comme un401 ni comme une panne d'exécutant.

Le contexte WEB est désormais éprouvé avec le vrai producteur C03 et la
façade C11 : 48 liaisons exactes (37 Core et 11 C14) dans la métadonnée
transport, sans ajout de permissions ni d'activité de session. Le mode
Core seul expose 37 liaisons ; les déclarations de bindings incohérentes
sont refusées. Quatre critères de contexte et quatre de garde inter-onglets complètent
les35critères précédents, tous réexécutés avec succès. La compilation du test modifié est réussie
dans le même appel ; le cache propre est supprimé et son absence confirmée.

La garde optionnelle X-Shell-Session-ID est éprouvée avec deux sessions
WEB C03 réellement persistées : cookieB/indicationA est refusé en400
CONTEXT_MISMATCH sans modification de configuration, audit ou idempotence
propriétaires. CookieB/indicationB et absence d'en-tête sont admis ; le
Bearer reste hors champ. L'en-tête ne vaut aucune autorisation.
Les33opérations WEB OpenAPI le déclarent optionnel avec le pattern UUIDv7
public ; les33opérations Bearer ne le déclarent pas. Les index/fragments
passent le vrai validateur de montage ; aucun profil partagé n'est élargi.
Les deux Python OpenAPI et la recette HTTP modifiés passent py_compile,
avec caches propres supprimés et absence confirmée.

Deux essais43ont été interrompus avant verdict : un provisionnement de
seconde session via un catalogue de fixture incomplet, puis un attribut
description de paramètre non admis par le profil documentaire fermé.
Chaque schéma et connexion a été nettoyé ; aucun cas de ces essais n'est
compté comme réussi. Le provisionnement a été déplacé avant les politiques
C14 et l'attribut retiré ; le contrôle des fragments utilise désormais le
vrai consommateur. Les prévols frais call_01a168c62022756cb6cc633a72064f30
et call_01a168cbe5d177579fe5d3242bb245d7 sont conservés.
Une protection ultérieure20est devenue STALE pendant l'écriture C11 de
api_core_openapi.py ; elle a été annulée sans HELD ni commande, puis le
contrôle a réussi sous mandat inédit sur révisions fraîches.

Le résolveur produit par le helper Python réel à partir des onze bindings
C14 a été transmis en mémoire aux clients publics JavaScript. Les quatre
critères réussissent : projection48acceptée,33chemins P/T/S aux identifiants
opaques,33appels Query/Command avec entrées conservées et11refus de liaison
absente avant tout envoi. Le fichier de recette passe node --check.
Son port HTTP est un double explicite ; ce contrôle de contrat entre
langages ne qualifie aucun renderer, transport ni serveur supplémentaire.

Une première soumission de ce contrôle a été rejetée avant admission MCP :
la révision de ressource PostgreSQL avait été omise par l'agent. Aucune
commande ni permission n'avait été exécutée. L'incident est réconcilié,
avec source inchangée, cache absent et aucun effet en suspens ; un prévol
natif neuf a réussi sous call_01a168ac0fd17763aaba4da55803e5fa avant le
mandat inédit qui porte les39résultats. Le rejet n'est pas compté comme test.

Les index PZT/DNS référencent respectivement deux et trois fragments, avec
SHA-256 et octets vérifiés sur les réponses HTTP réelles. Le plus grand
fragment fait65445octets, sous la limite65536 ; la couverture agrégée reste
de24chemins PZT et42DNS. Aucun schéma ou réponse n'est retiré pour tenir la borne.

Chromium156.0.8078.47 et Firefox153.5.1esr ont exécuté chacun les dix cas actualisés.
Les profils et processus sont retirés, le collecteur est fermé, sans violation
de son protocole. Chromium a produit des diagnostics système DBus/zygote
sur stderr pendant sa fermeture ; ils ne sont pas effacés des preuves brutes.
Ces tests utilisent le vrai contrat et adapter de présentation avec un port
moteur double explicite : ils ne prouvent pas le renderer React final.

Les preuves antérieures de2.2 incluent notamment les40cas PZT et58cas DNS
sur PostgreSQL réel et le lifecycle propriétaire. Les40fichiers de2.2 non
modifiés conservent leurs SHA ; les cinq changements attendus touchent les
trois documents de suivi et les deux manifests frontend. Les41contrôles
courants de composition recoupent ces manifests. Les22cas de la factory
publique C03,42régressions Auth et10régressions Core/HTTP réellement exécutés
avant ce phasage restent conservés au checkpoint avec leurs limites.

## Revue documentaire et limites

| Document | Action C14 | Motif |
|---|---|---|
| AGENTS.md | Conserver la version régénérée | Règles actuelles lues ; aucun changement de sécurité demandé |
| PROJECT.md | Conserver | Modules de gestion essentiels et exécutants séparés restent conformes |
| TECHNICAL.md | Conserver | Contrats HTTP, contexte opaque, C03/C04/C05 et refus fermés conservés |
| BUILD.md | Conserver | Aucun artefact installé, binaire ou packaging P0 qualifié par C14 |
| DEVOPS.md | Conserver la version régénérée | Outils existants utilisés, aucune dépendance ajoutée |
| README.md | Paragraphe C14 ajouté, apports PA10 conservés | Sources réalisées et qualifications distinctes ; inventaires historiques non assimilés à l'état courant |
| CHANGELOG.md | Entrée Unreleased C14 | Aucun numéro de livraison ni date de release inventés ; entrée Agent conservée |
| Backend README | Assemblage et index documentaires | Politiques explicites, montage avant catchall Core, bornes et limites |
| requirements.md/design.md/tasks.md | Recoupement et phasage | Canon PZT courant, séparation Z12/C08 et preuves sans coches anticipées |

DEVOPS.md régénéré au relevé2026-10-23T12:53:55Z a été relu et transmis
à OpenCode, SHA3690d6b0c661a79898c60dc328be1fd4812d10c885b6c75e7337b68f9b36143b.
Les versions utiles aux recettes C14 restent inchangées. La mention de
binaire OpenCode absent dans l'inventaire ne décrit pas son état constaté
ensuite : le chemin déclaré est présent et l'API1.19.3 répond healthy.
Aucune installation, réinitialisation de quota ou relance de service n'en
découle ; cet inventaire ne vaut pas qualification fonctionnelle.

Le canon PZT courant contient l'amorçage PKI initial Z12 consommé par C08.
Les21ancrages C00 restent résolus et les deux empreintes sont vérifiées.
C14 n'émet aucune confiance initiale et n'implémente aucun des cinq ports
initiaux Z12. L'adoption PostgreSQL, le retrait initial et l'admission
ordinaire demeurent des étapes propriétaires à prouver.

Aucun transport PBO–PA, exécutant réseau, serveur DNS actif, qualification
locale/distante, secret Docker/systemd, ancrage TPM/NV ou P0 installé n'est
déduit de ces suites. Les plans API ne valent pas disponibilité d'un hôte.
Aucun Git n'est exécuté dans cette reprise.

## Contrôles restant obligatoires

Le pipeline/build et le runtime frontend C11 doivent être effectivement
disponibles. Il faut alors vérifier la composition des vraies contributions
C14, le resolver des onze opérations et le renderer/les champs typés sur
l'artefact réellement construit, sous les navigateurs déclarés, avec les
contrôles interactifs, de contexte et d'accessibilité applicables.
Les budgets de recette AST64Kio ne sont pas une décision de production D3.

La tâche2.3 ne sera validée qu'après ces preuves. Viennent ensuite2.4 et les
validations3.1–3.3, la fidélité finale des fichiers, les contrôles OpenSpec
globaux requis et la matrice de périmètre. L'archive unique autorisée,
STATISTIQUES.md, publication CAB, gate, désarmement et libération restent
distincts et non réalisés à cet instant.

## Empreintes des dépendances communes examinées

Les empreintes suivantes identifient les lectures et preuves ci-dessus.
Toute modification ultérieure invalide les seuls contrôles affectés.

| Source | SHA-256 |
|---|---|
| src/pixs/backend/api_module_views.py | 3e4c31970796be9ab3e10596e4aefccf37f4c81e668fbcfdeac91fc41daa8dd7 |
| src/pixs/backend/api_module_openapi.py | 92733f765c51592fa6c0a4b37b8a9cdd912af03c0a9311ad1854fd8163e6b037 |
| src/pixs/backend/api_core_views.py | a137f1d552022640f28df8eb42d58bf52cb77f8953da72d1652c95860a08ebd1 |
| src/pixs/backend/api_core_openapi.py | 14462bb90a15cccffa5cdeb5bee8c25918ac1aed4ce822686b393c0437232b30 |
| frontend/src/shell/api-v1.js | 75012fdb57235681698433d1b8a133eca61d0729ada31324e742cde3240f4bb3 |
| frontend/src/shell/presentation-contract-v1.js | 50ef4e6c587d9a348cb270686e03fff96a0f9e507ab5edac025d99fc23551ed6 |
| frontend/src/shell/presentation-adapter-v1.js | 1c40419c0ab7b349bac0ba724f7ccb7b5583c2c19e02be24817959a6c45c0d34 |
| frontend/scripts/presentation-profile-v1.mjs | 439c1901a868b1fb374f931bd0e53b6e0c4dbed246d7ad252147c07a866be1f9 |
| src/pixs/backend/api_shell_transports.py | 93b2ce2a5aadcbe7fa97caf6bd639a582ea53b3b0d8094e47a885126bc9c61d4 |
| src/pixs/backend/api_shell_context.py | d31344a60bb4f4a7c3ee4d44b707ad8e5b813f5b5f50bddf531c975fad0edd2e |

### Revalidation frontend après revue du retrait logique

Les deux sources affichent explicitement DECLARED/RETIRED et la
persistance/conservation. Les actions DNS inapplicables à un profil retiré
sont masquées ; la redéclaration reste explicite. Les dix cas de pages et
les deux contrôles AST ont réussi, puis les dix cas ont réussi dans chacun
des deux navigateurs déclarés. Les anciens résultats à neuf cas restent
historiques. Ces moteurs doubles ne prouvent toujours pas le renderer composé.

### Choix BIND 9 demandé séparément

Le développeur a confirmé BIND 9 fourni par Debian et inclus dans l'image
Docker Pixs, installé et configuré par le PA ; l'activation est ultérieure.
Le [dossier distinct BIND 9](../../adopt-bind9-managed-dns-and-packaging/proposal.md)
porte trois deltas proposés pour pzt, deb-package et docker-image.
Son strict OpenSpec a réussi sous call_01a1688c2532713cad9b3ff21bfdc521.
Son audit final des neuf fichiers a réussi sous
call_01a1689366167318bcbb29516b1cfa1f : trois exigences, neuf scénarios,
quinze liens résolus, trois empreintes canoniques inchangées et UTF-8/LF.
Cette préparation ne synchronise aucun canon et ne réalise pas le service.
C14 conserve le DNS actif non sélectionné ; Z05 garde la réalisation DNS.

### Requalification des fournisseurs avant le build composé

Les preuves suivantes ont été exécutées sur leurs ensembles de sources
épinglés. Elles préparent la revue des attestations externes ; elles ne
constituent ni un résultat du renderer React composé ni une qualification P0.

| Suite versionnée | Résultat réellement observé | Appel natif |
|---|---|---|
| pixs.c14.frontend-build.kernel-core-conformity 1.1.0 | 988 tests de 83 modules, zéro erreur/échec/skip ; configuration, lifecycle et déclarations frontend inclus ; ensemble courant Kernel/Core sans ajout, retrait ni empreinte modifiée au recoupement | call_01a16919ba2c739d8401f0cb151498ff |
| pixs.c14.frontend-build.core-postgres-conformity 1.0.0 | 200 cas PostgreSQL réels : transactions 14, identité 20, topologie/autorisation 46, Queries 62, bootstrap 58 ; 150 fichiers épinglés ; participants externes synthétiques déclarés | call_01a169163738714c9da553901b824a38 |
| Gestion PZT/DNS 1.1.1 : pixs.c14.management.contract-conformity, pixs.pzt.management.conformity, pixs.dns.management.conformity | 38 tests de contrats et 104 cas PostgreSQL réels, répartis PZT 40 et DNS 64 ; migrations, nettoyage, connexions fermées et sources inchangées confirmés | call_01a1694299fb743288b2e266f41b0b78 |
| pixs.c14.frontend.presentation.conformity 1.0.0 | 12 tests : dix comportements de pages sur moteur/ports de recette explicites, deux contrôles AST ; huit sources épinglées ; zéro erreur/échec/skip ; renderer et transport non qualifiés | call_01a16944cfe87218a763f6a1c8a4032c |

Les cas DNS ciblés lient pixs.dns.views.query à GetDesiredDns :
ordre des vues souhaitées, révision et dimension métier, refus d'accès
courant et séparation de tenant/périmètre. pixs.dns.policy.query est lié à
ResolveViewPolicy : cibles souhaitées distinctes selon la vue, état
UNVERIFIED, application UNKNOWN, plafonds TTL zéro conservés, absence de
nom distincte de NXDOMAIN, vue inconnue/zone extérieure/autorisation refusées.
Ces trois refus conservent chacun un audit DENIED précis après rollback et
ne modifient ni configuration, ni noms, ni idempotence.

La première exécution des six assertions complémentaires avait exigé à tort
l'absence d'audit de refus : trois cas ont échoué sous
call_01a1693b4ff775aeb7499e5534e28fd9, avec nettoyage et connexions fermées
confirmés. Seule la recette a été corrigée ; aucun service produit n'a été
modifié. Le résultat 1.1.1 ci-dessus remplace cette tentative pour la
validation courante, qui reste conservée dans l'historique de preuve.

### Préparation de la recette HTTPS et navigateur

La fixture de composition réelle C14/C03/C04/C05 est écrite dans
tests/integration/c14_composed_browser_fixture.py. Sa compilation et trois
contrôles sur PostgreSQL ont réussi : construction de la composition, CSRF
via la vraie frontière C11 et contexte WEB via le vrai service Auth.
Preuve : call_01a16924a01574138a2c66bc7bbd6402, avec nettoyage et fermeture
des connexions. Ces trois contrôles utilisent encore RequestFactory :
ils ne prouvent pas le transport TLS.

Le serveur de recette test_c14_composed_browser_postgres.py et le pilote
frontend/tests/c14-composed-browser.mjs sont écrits. Leur compilation
Python et contrôle syntaxique Node ont réussi sous
call_01a16937a4f67372b7b8a501e0582d2b, avec empreintes inchangées et cache
transitoire supprimé. Leur exécution sur le bundle COMPOSED reste en attente.
Le serveur transmet les requêtes WSGI complètes sous TLS loopback réel ;
le pilote prévoit Chromium CDP et Firefox WebDriver BiDi dans des profils
éphémères. La confiance du certificat d'autotest ne qualifie aucun TLS
de déploiement. Aucune recette navigateur n'est déclarée réussie ici.

Les six liaisons d'attestation ont ensuite été authentifiées et acceptées
en revue technique C11 pour la seule recette DEVELOPMENT. La sélection
c14-composed-selection.json porte les neuf champs canoniques de chaque
attestation PASS, avec références natives et ensembles SHA-256 vérifiés.
Elles ne qualifient aucun P0 global, exécutant réseau/PA, service DNS actif
ou artefact installé.

### Recette réelle du bundle composé — tâche 2.3

Le profil de recette a été corrigé avant construction : quatre propriétaires
capturés, six navigations optionnelles conformes aux descripteurs et 132 clés
de catalogue par module, pour 66 clés dans chacune des deux langues. Ces
bornes de recette ne définissent aucun budget D3 de production. Les refus
IMPORT_ENVELOPE_INVALID et GRAPH_BLOCKED ont précédé ces corrections du seul
profil ; aucun validateur n'a été assoupli.

Une première charge du vrai bundle a révélé COMPOSITION_CONTEXT_STALE, avec
GET shell/context 200. Le raccord C11 a été corrigé dans main.js : cinq
ports capturent le contexte authentique original ; la copie de présentation,
le WeakMap et les contrôles d'epoch restent stricts. L'empreinte de ce main.js
est cf6690165266332f73bb60ae7e48eb2f9221f19dc7a50d305e8d188752f583f8.
Cette correction appartient au RUN C11 ; aucune copie de contexte n'est
acceptée comme autorité.

| Preuve | Résultat natif | Appel |
|---|---|---|
| Build COMPOSED après le raccord | exit 0, quatre artefacts, sources inchangées, graphe de seize contributions sans diagnostic ni blocage | call_01a169a204f474c6a361ca4f435b65b6 |
| Copie isolée de ces artefacts | quatre SHA-256 strictement identiques aux octets construits ; aucun déplacement de dist | call_01a169a4428077d18fd700a106b7c06b |
| Chromium réel, sans pause de debugger | quinze critères vrais ; vrais clients, renderer React, vues C14/C03/C04/C05 et PostgreSQL | call_01a169bcf17272ebbf540c33af2640d7 |
| Firefox réel, sans pause de debugger | mêmes quinze critères vrais sur un nouveau schéma isolé | call_01a169be739c77e89e8bd39453f4b0ad |

Chaque navigateur a exercé les deux pages, les mutations et relectures
confirmées, le retrait logique et sa possibilité explicite de redéclaration,
les états UNKNOWN/UNMEASURED honnêtes, les langues en/fr et les références
ordonnées A/B/A avec doublons et LF conservés dans le DOM puis en PostgreSQL.
Le serveur a relevé quatorze réponses HTTP 200 par navigateur, incluant
contexte, CSRF, quatre mutations et leurs Queries. Aucun message console
d'erreur n'a été observé. Le profil, les fichiers temporaires, le groupe de
processus vivant, le serveur, les connexions et le schéma PostgreSQL ont
été fermés ou supprimés avec preuve. Ces recettes sont PLATFORM ; les
preuves de séparation tenant/scope du domaine PostgreSQL restent distinctes.

Le TLS de recette chiffre réellement le loopback et transporte des cookies
Secure. Chromium utilise --ignore-certificate-errors et Firefox
acceptInsecureCerts:true dans leurs seuls profils jetables : la vérification
de chaîne est contournée. Ni validation de certificat, ni PKI, ni TLS
déployé ne sont qualifiés. Aucun exécuteur PA/PZT ni service DNS actif n'est
installé ou activé par ces tests.

Les tentatives de pilote antérieures restent en échec dans l'historique :
chemin de socket trop long, délais de workflow, puis observateur de nettoyage.
Un profil de recette résiduel a été supprimé sous
call_01a169ae156a767f9f87405794b3f537 après vérification des processus.
Le parent possède désormais le profil et vérifie indépendamment sa
quiescence et sa suppression. Les quinze critères des deux appels verts
ci-dessus ont été exécutés après ces corrections ; aucun échec n'est
compté comme un succès.


### Tâche 2.4 — garde essentielle et obligations de gestion

Quatre contrôles nouveaux ont réussi sous
call_01a169c577dc7195ade8870a436c4511, sur les manifests réels courants :
composition de recette à quatre composants et preuves authentifiées ;
absence de PZT ou DNS refusée par le plan hôte avant lecture du port de
preuves ; hôte complet à six responsabilités refusé sans conformité fournie.
Aucun hook, exécuteur ou service DNS actif n'a été activé.

Les suites de gestion 1.1.1 ont ensuite été réexécutées pour cette tâche
sous call_01a169c8761370ce909c7c20f0ef5508 : 38 tests de contrats et
104 cas PostgreSQL réels, PZT 40/DNS 64, tous réussis, sources inchangées,
schémas supprimés et connexions fermées. Les cas comprennent l'absence
essentielle bloquante avant hooks, la gestion disponible sans exécutant,
le refus d'opération exigeant cet exécutant, la fermeture après sortie
du lifecycle, les observations non vérifiées refusées, UNKNOWN/UNMEASURED
distincts de zéro, l'audit et les waivers contrôlés, l'isolation, les CAS,
la concurrence et la réconciliation des issues inconnues.

Ces preuves de lifecycle et du domaine PostgreSQL sont distinctes des
quinze critères de chacun des deux navigateurs. Elles n'annoncent ni PA/PZT
installé, ni transport PBO–PA, ni DNS actif, ni profil P0 qualifié. La tâche
2.4 est techniquement validée dans ce périmètre ; 3.1 à 3.4 restent ouvertes.

## Consolidation finale 3.1 et 3.2 — 23 octobre 2026

Le contrôle natif call_01a16aa836db737c844a192dad35611c a compilé 55
fichiers Python, vérifié 41 fichiers JavaScript, exécuté les 145 cas
configurés dans chacun de Chromium 156.0.8078.47 et Firefox 153.5.1esr,
puis construit le frontend STANDALONE : exit 0, 103 sources inchangées.
Les profils, le serveur de test et le vendor React temporaire sont supprimés.
Les avertissements TanStack MODULE_LEVEL_DIRECTIVE restent visibles ; aucune
dépendance ni limite de validateur n'est modifiée pour obtenir ce résultat.

Les recettes composées complémentaires sont call_01a16aaaba3d774e93a80f78cac802ba
(Chromium) et call_01a16aab9467709fbc1a3dc63e7dff23 (Firefox), quinze
critères vrais chacune, quatorze HTTP 200 et deux mutations persistées.
Le pilote de recette a été instrumenté dans un répertoire jetable, sans
modifier les sources ni le bundle isolé. Huit PNG ont été produits puis
relus par l'orchestrateur : PZT et DNS, 1280×900 et 390×844, dans les deux
navigateurs. Aucun débordement horizontal n'est mesuré ; les seize contrôles
de formulaire sont étiquetés, le focus programmatique est atteignable et
les titres sont visibles. Les captures conservent le focus visible et le
repli des libellés sur écran étroit. Les artefacts et SHA-256 sont conservés
sous output/cismp/cismp4-pixs-86551e9b05914e67/visual-20261023-chromium/
et visual-20261023-firefox/. Cette revue ne constitue pas un audit manuel
exhaustif au clavier ou avec technologie d'assistance. Le lien générique
Sign in restant visible avec une session vérifiée a été signalé au propriétaire
C11 ; la navigation commune n'est pas modifiée par C14.

La première tentative visuelle call_01a16aa9c5297189b8484ba9ba2a64f0
s'est arrêtée avant toute écriture sur une empreinte backend différente.
La reconstruction exacte de l'ancienne source apps.py retrouve
f19ef37bf30125fb4d2fbb672572c5f6931bf470e5a6f052b882415fbc54b308 ;
seuls la classe PixsBackendConfig et son export ont été ajoutés dans la
source courante 935dd73eacf31ab1d251e31bee1dc510895243b131164df6e3bc833a2c0528fb.
Cette classe n'est pas sélectionnée par la fixture. Les campagnes vertes
suivantes sont épinglées sur la source réconciliée ; aucune nouvelle fonction
backend n'est qualifiée par cette réconciliation.

### Matrice d'application et limites de garantie

| Exigences / scénarios | Preuves et portée effective |
|---|---|
| Modules PZT et DNS essentiels, gestion réseau désactivée, A06c | Manifests/contrats, composition à quatre composants et quatre gardes 2.4 ; absence essentielle fermée avant hooks. L'hôte P0 sans toutes ses preuves reste refusé. |
| Configuration souhaitée, versions, gouvernance, valeurs ouvertes | Contrats et 104 cas PostgreSQL PZT/DNS ; DTO fermés, révisions CAS, listes ordonnées avec LF et doublons, noms/vues/suffixe et plafonds TTL. Aucun paramètre ouvert n'est inventé. |
| Audit applicable, autorisation et faits établis | Audit C05 et autorisation C04 réels, refus audités, isolation tenant/scope, concurrence, idempotence, rapprochement des issues inconnues ; 43 cas HTTP/PG PLATFORM avec Auth C03 et contrôle de session. |
| Gestion conservée sans exécutant, qualification distincte de spécification | UNKNOWN/UNMEASURED distincts de zéro, refus sans exécutant et après arrêt lifecycle ; recettes GUI réelles et PostgreSQL, sans émission d'état appliqué client. |
| Contrats intégrés et décisions ultérieures | Sept contrats métier 1.0.0, deux plans API distincts, 66 chemins OpenAPI répartis en index/fragments de 64 Kio maximum et validés par le consommateur commun. |
| Pile de référence et adapters explicites | Aucun runtime ni provider nouveau, dépendances exactes du projet inchangées ; syntaxe et tests exécutés avec Python/Django/PostgreSQL et navigateurs du contexte courant. Les qualifications de distribution, de migration de version et de reproductibilité P0 restent aux lots propriétaires C08/C17/C18/C19. |
| Couche PA séparée et réseau désactivé | Aucun exécuteur, socket de substitution, préparation hôte, transport PBO–PA, autorité initiale PKI ou DNS actif ajouté. Les ports externes de tests du domaine sont explicitement synthétiques ; ils ne qualifient aucune exécution PA. |

Les tables historiques C00 restent des références de clauses, sans verdict
global ajouté. Les tests de domaine couvrent les contextes tenant/scope ;
les HTTP et GUI réels ici sont PLATFORM. Les projections interlangages
P/T/S ne sont pas une campagne GUI tenant/scope. L'installation Debian,
l'image Docker installée, les capacités matérielles, la PKI et les ports
initiaux C08/Z12, le transport mTLS et le service BIND 9 actif ne sont pas
exécutés dans C14 : ils dépendent des parcours et lots propriétaires.
L'activation DNS demeure ultérieure, selon le choix explicite du développeur.
Les tests emploient des références synthétiques ; les valeurs privées de
recette restent locales, sans sortie de cookie, clé ou credential. Aucun
fichier sensible n'est indexé ni transmis au modèle.
