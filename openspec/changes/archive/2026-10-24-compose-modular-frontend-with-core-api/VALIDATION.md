# Validation — C11

État : validation technique C11 acquise le 24 octobre 2026 après consolidation des preuves ci-dessous ; archivage et clôture administrative encore à réaliser. Le RUN cismp3-pixs-c4b2bfe2c6614f3f traite uniquement compose-modular-frontend-with-core-api. Le développeur a demandé les réalisations et artefacts de recette avant les tests/validations. La présence des sources ou d'une commande proposée ne constitue pas une preuve d'exécution.

Les contrôles requis MUST être exécutés avant validation des tâches et archivage. Une preuve obligatoire absente MUST rester ouverte ; N/A MUST être justifié par le rôle/capacité réellement non sélectionné et MUST NOT remplacer un contrôle manquant. Les sorties et empreintes natives du checkpoint du RUN MUST être recoupées pour la source effectivement testée.

## Matrice d’acceptation examinée

| ID | Tâches et exigences concernées | Contrôles attendus | État actuel |
|---|---|---|---|
| C11-A01 | 1.2, 2.1 ; API, frontend | Revue conception actuelle, syntaxe/structure OpenSpec, scopes opaques P/T/S, résolution publique, copies/époques, Query/Command et refus avant envoi | 133 Node et OpenSpec strict PASS dans leurs périmètres ; preuves et limites ci-dessous |
| C11-A02 | 2.2 ; modules, lifecycle, services, providers | Vrai Kernel validate/compose, sélection épinglée, couverture d'attestations authentifiées, provenance et octets capturés ; refus des entrées absentes/ambiguës | 106 Python et 6 raccords pipeline PASS ; attestations propriétaires recoupées pour recette DEVELOPMENT seulement |
| C11-A03 | 2.2 ; extension-contracts, frontend | Imports publics seulement, profils/trust, versions, collisions, refus obligatoire/isolement optionnel, dépendances/slots et chaîne512 | 75 AST/importeur/profil et 133 Node PASS ; 145 cas dans chacun des deux navigateurs PASS |
| C11-A04 | 2.2, 2.4 ; composition frontend au build | Module et sous-module ajoutés sans édition du shell, même sélection/politique en développement et bundle construit réellement chargé, rapport/pins, dérive et artefacts éligibles | PASS : module et sous-module imbriqués, vrai Kernel/Python/Vite et adapter React ; 8 chargements DOM dev/bundle dans Chromium/Firefox, rapports identiques, sans édition du shell. Routage de harnais et attestations synthétiques explicitement bornés ; vrais modules PZT/DNS dans le shell produit couverts séparément par C14. |
| C11-A05 | 2.2 ; design-system, internationalization, themes | Cinq champs typés, faux booléen/entier facultatif/listes et enregistrements LF/ordre/doublons, modèles et brouillons ; en/fr, Light/Dark et variantes fermées | Cinq champs et focus automatique DOM PASS ; 8 captures C14 Light, bureau1280/mobile390 relues dans les deux moteurs ; Dark, contrastes, zoom natif humain à 200 %, reflow et mouvements vérifiés dans le complément manuel ci-dessous. |
| C11-A06 | 2.3 ; frontend, API | PENDING/LOADED/CONFIRMED/REJECTED/UNKNOWN/INVALID distincts, clé et contenu conservés, reprises divergentes refusées, réponses périmées et purge avant notification | 133 unités Node et 145 cas par navigateur PASS sur doubles explicites de transport |
| C11-A07 | 2.3 ; Auth/API/autorisation/audit | C03/C04/C05 et PostgreSQL réels, grant absent/refus, expiration/révocation/contextes, exception Super Admin conforme, audit/gouvernance indisponibles et commit inconnu sans données partielles | Preuves propriétaires recoupées conservées ; c14 native Chromium msg_169bceb43001bWmg6gBXEY7G7l / prt_169bcf2ad001s5lXAoSw7oDJwZ et Firefox msg_169be6ccf001D2lN9YttLONQqh / prt_169be7545001LTo4AjVN3aqmn4 : PG16.14, PZT+DNS mutations persistantes/retrait, LF ordre/dup, en/fr/unknown, PLATFORM uniquement |
| C11-A08 | 2.3, 2.4 ; transport WEB | Cookie/CSRF/HTTPS/origine, Bearer séparé, garde X-Shell-Session-ID, liens Core/propriétaires explicites et zéro envoi après refus | 43 HTTP/PG propriétaires conservés ; c14 native 14 HTTP 200 par moteur, TLS loopback chiffré avec bypass chaîne profils jetables, cleanup true, ni P0 ni TLS déployé |
| C11-A09 | 2.2–2.4 ; accessibility | Clavier réel, focus/labels/sémantique, contraste Light/Dark, zoom/reflow/mouvements réduits, technologies d'assistance ; séparer automatique et manuel | PASS : clavier CUA sur shell réel et primitives réelles, Orca humain A à E, contraste Light/Dark mesuré, zoom natif 200 % humain, reflow320 et mouvements réduits ; provenance et limites ci-dessous |
| C11-A10 | 3.1, 3.2 | Syntaxe Python/JS, suites configurées Node/Python, npm test et build, Chromium/Firefox headless, non-régression et nettoyage des ressources/profils | Syntaxe16Python,133Node,106Python,75AST,6pipeline,145Chromium/145Firefox,2builds et recette additionnelle8DOM PASS ; périmètres distincts ci-dessous. |
| C11-A11 | 3.3 | Diff ciblé sans Git, fichiers autorisés seulement, UTF-8/LF/sans BOM, absence de secret, cohérence canon/cadrages/docs, sources/preuves réconciliées | Revue finale bornée : 271 fichiers comparés, dont66 C11 ; aucune dérive nouvelle, UTF-8/LF/sans BOM conformes. Drift apps.py et NUL historique conservés et explicités. Aucun Git ni fichier sensible exclu ouvert ; pas de recherche exhaustive de secrets. |
| C11-A12 | 3.4 | Archive unique C11 après validation, STATISTIQUES.md six sections/totaux, publication CAB durable, gate et libération ciblés | Autorisé pour le seul C11 ; à réaliser et prouver après cette validation. Aucune livraison P0 globale annoncée |

Les références exactes de clauses/scénarios sont celles de requirements.md et des canons qu'il désigne. Leur application MUST être contrôlée sur les versions courantes, sans transformer un statut de matrice historique en verdict présent. Les obligations de paquet Debian/profil installé C18/C17/C19 restent distinctes du bundle C11 en environnement isolé.

## Types de preuves

- Une unité sur double de transport démontre seulement le contrat et les refus observés du client. Elle ne qualifie pas C03/C04, PostgreSQL, les cookies ou TLS.
- Une recette HTTP en processus avec RequestFactory/ASGI ne démontre pas un serveur TLS réseau déployé.
- Une recette navigateur sur renderer double ne démontre pas le vrai renderer React ni le bundle composé.
- Une suite propriétaire ou Kernel/Core est réutilisable seulement avec commande/appel natif, suite/version, résultats, sources et limites recoupés. Les attestations de composition restent externes et n'impliquent jamais une qualification P0.
- Les métriques de génération/quotas et prévols CAB sont des preuves de pilotage, pas des tests produit C11.

## Matrice documentaire

| Fichier | Traitement C11 | Justification / preuve à recouper |
|---|---|---|
| README.md | Paragraphe modes autonome/composé et qualification en cours | Notes Agent/C14 et synthèse générale préservées |
| frontend/README.md | Modes, CLI opérateur/pins/budgets, session, champs et limites | Aucun chiffre de réussite nouvelle déduit du code |
| src/pixs/backend/api/README.md | Contexte Auth, résolveur injecté, module HTTP/OpenAPI et continuité WEB | Contrats Core/Bearer et preuves historiques distincts |
| CHANGELOG.md | Entrée Unreleased C11 | Aucune version, release ou publication Git créée |
| design.md | Précisions de réalisation dans le seul change C11 | Champs, limites et frontières ; canons non réécrits |
| tasks.md | Suivi de réalisation autorisée et organisation en deux phases | Aucune nouvelle case cochée sans preuve |
| PROJECT.md | Inchangé après revue ciblée | Frontend en lecture seule du ScopeContext et modularité commune déjà prescrits |
| TECHNICAL.md | Inchangé après revue ciblée | Contrats frontend publics/versionnés et isolation déjà prescrits ; pile inchangée |
| BUILD.md | Inchangé après revue ciblée | Composition récursive, refus et qualification de distribution déjà prescrits ; aucun paquet livré |
| DEVOPS.md | Relevé régénéré par le développeur, relu | Inventaire et chemins ne valent pas tests ; instance OpenCode existante préservée |
| AGENTS.md / ORCHESTRATED_CODING.md | Inchangés | Règles et protocole appliqués ; aucun changement d'autorité |
| openspec/config.yaml et canons | Inchangés | Aucun nouveau change ni profil canonique ajouté par ces précisions |

## Résultats et clôture

Les résultats ci-dessous consignent la seconde phase effectivement exécutée. Toute limite MUST être déclarée au niveau de la tâche affectée. Les contrôles manuels applicables ont été réalisés selon le complément ci-dessous. Les limites de couverture déclarées demeurent ; aucun archivage, statistique d’archive, publication ou gate terminal n’est prouvé par le présent document avant sa réalisation effective.

## Résultats exécutés le 23 octobre 2026

Les commandes exactes, sorties, identifiants natifs et empreintes figurent dans le [checkpoint du RUN](../../../output/cismp/cismp3-pixs-c4b2bfe2c6614f3f/state.json). Ce fichier trace les preuves et ne remplace pas les spécifications fonctionnelles.

| Contrôle | Résultat observé | Message natif / partie | Clé de preuve |
|---|---|---|---|
| Unités du shell et régression identité | 133/133, aucun échec | msg_169a20773001HdM3bBvOIANmR0 / prt_169a21120001i2y6calSWneOqK | phase2_node_test_requalified_result |
| Capture, sélection, faits et plan Python | 106 tests, OK | msg_169816891001wc413ornYrrgcy / prt_169817009001JHIYQXpdPDU2gR | phase2_python_unit_result |
| AST, importeur, profil, graphe intégré | 75/75, aucun échec | msg_1698364a2001Ro71aG5zpAPP3N / prt_16983700e001t65xP6iq1tbwsv | phase2_node_import_test_result |
| Syntaxe Python | 16 fichiers, exit 0 | msg_16980490b001OuY0YEoPc63RLc / prt_169805ae6001a8yGV8aeSCm4e6 | phase2_python_syntax_result |
| Pont réel Python/Kernel/Vite et rapports dev/bundle | 6/6, aucun échec ; requalifié après correctif main | msg_169a94a5a001A2DtndexaNzJd5 / prt_169a95344001Df2ozUWoA07XgD | phase2_composed_pipeline_requalified_result |
| OpenSpec strict ciblé | exit 0 ; skip_specs, zéro delta volontaire | msg_16984db1f0016TdeKdb7bBMjYe / prt_16984e20f0019hWLB5koH1IHyU | phase2_openspec_result |
| Construction STANDALONE configurée | exit 0 ; 3 artefacts | msg_169ab5905001S7xAQzAY7yo4V2 / prt_169ab6eef001Kw67sVgP30GqK5 | phase2_standalone_build_result |
| Construction COMPOSED configurée | exit 0 ; 4 artefacts et report.blocked=false | msg_169ad95ab001F66ASz0o1NsKR5 / prt_169ad9cdf001uvfffwVgy2Say9 | phase2_composed_build_result |
| Unités et vrais champs React/DOM dans les deux navigateurs | 145/145 Chromium et145/145 Firefox ; nettoyage complet | msg_169af60650011VonC1YqtOJwAY / prt_169af72c8001CfZWq6VeLybZzm | phase2_browser_test_result |

Les résultats se chevauchent : ils ne sont pas additionnés en un nombre de scénarios distincts. Les moteurs observés sont Chromium156.0.8078.47 et Firefox153.5.1esr. Le dernier harnais a prouvé fermeture des processus/serveur et suppression des profils et du vendor React temporaire. Les constructions conservent les avertissements TanStack MODULE_LEVEL_DIRECTIVE (« use client ») ; leurs codes de sortie sont0.

### Défaut réel et régression

La recette C14 a isolé COMPOSITION_CONTEXT_STALE après GET shell-context200. PresentationView retransmettait la copie de contexte produite par l’adapter à cinq ports privés. Ces closures state/submit/slot/component/onError capturent désormais le contexte authentique lexical. L’adapter conserve sa copie gelée et le runtime conserve WeakMap, révision de route et époque stricts.

Le main courant a pour SHA-256 cf6690165266332f73bb60ae7e48eb2f9221f19dc7a50d305e8d188752f583f8. Le cas « adapter runtime : contexte lie authentique, copies et perimes refuses » utilise le vrai adapter et le vrai runtime : copie et ports non liés refusés, rendu/état/soumission liés acceptés, contexte invalidé refusé. Ce cas unitaire utilise un renderer de structure et un transport doubles ; il ne remplace pas le chargement du vrai main dans le bundle C14.

### Historique de recette conservé

Le premier lancement navigateur a échoué avant tout cas sur l’entrée virtuelle du vendor React. Après correction, un cas sur144 échouait dans chaque navigateur car la recette conservait un bouton DOM remplacé par React. La référence courante a été rétablie, puis le nouveau cas d’identité ajouté ; le dernier lancement réussit145/145 dans chaque moteur. Les refus de schéma de mandats CAB sont consignés séparément : ils ont été interceptés avant enregistrement/exécution et ne sont pas des tests produit.

### Réutilisation bornée des preuves propriétaires

Les preuves C14 vérifiées comprennent988 cas purs sur83 modules Kernel/Core,200 cas PostgreSQL Core sur5familles,38 contrats,40 PZT PG,64 DNS PG,12 contrôles JS/AST propriétaires et43 HTTP/PG avec garde X-Shell-Session-ID. Leurs commandes, suites, versions, sources et limites restent celles des reçus natifs du checkpoint ; elles ne sont pas présentées comme de nouvelles exécutions Root.

Le dernier recoupement a relu les empreintes de191 fichiers (170 sources propriétaires et21 fichiers de recette). Le seul écart est le script test:node de frontend/package.json : remplacer en mémoire la nouvelle commande par l’ancienne reconstitue exactement son SHA initial. Aucune dépendance ni source propriétaire Kernel/Core/PZT/DNS n’a changé dans ce recoupement. Ces attestations sont admises pour la recette DEVELOPMENT épinglée ; aucune qualification P0, exécuteur DNS/PA ou PKI n’en découle.

### Barrières manuelles levées le 24 octobre 2026

Les recettes natives C14 Chromium/Firefox restent PASS dans leurs périmètres datés, avec snapshot des quatre artefacts identiques au build C11. Module/sous-module réels : voir complément 2.4. Les contrôles manuels précédemment non exécutés ont été réalisés ; les anciennes déclarations d’attente décrivent l’historique et sont remplacées par le verdict présent.

Le développeur a confirmé « A à E OK » puis « Navigateur intégré de Codex ». Il a fourni Orca48.1, AT-SPI2 2.56.2 et session GNOME Wayland sous Linux. La version exacte du moteur de ce navigateur est N/A : les API disponibles ne l’exposent pas ; les versions Chromium156/Firefox153 des recettes headless ne lui sont pas attribuées.

| Parcours humain demandé | Résultat confirmé |
|---|---|
| A — Nom de recette champ texte, Activer la recette case à cocher, changement d’état Espace annoncé | PASS humain |
| B — Ajout de ligne par Entrée, focus sur Lignes de texte2, retrait et retour sur une ligne restante | PASS humain |
| C — Groupe Enregistrements, champs Libellé/Note et boutons Ajouter/Supprimer compréhensibles | PASS humain |
| D — Confirmation, refus et issue inconnue annoncés distinctement sans recherche à la souris | PASS humain |
| E — Zoom natif200 %, libellés et actions lisibles/utilisables au clavier, retour100 % | PASS humain |

Cette preuve est le compte rendu explicite du développeur utilisant un lecteur d’écran réel. Root n’a pas prétendu écouter Orca ; les observations de l’arbre d’accessibilité sont distinctes de ce compte rendu.

### Contrôles interactifs et visuels Root

Le shell STANDALONE réel et un harnais local utilisant le vrai adapter, les cinq vrais champs React et le CSS du produit ont été chargés dans le navigateur intégré de Codex. Le contexte et l’enregistrement du harnais sont simulés ; ce parcours ne requalifie ni Auth ni PostgreSQL. La recette C14 du shell COMPOSED et les huit chargements MODULE/SUBMODULE restent les preuves d’intégration distinctes.

- Clavier natif : lien d’évitement visible puis MAIN#content ; saisie texte/checkbox/entier et LF, ajout/retrait de listes et enregistrements avec retour de focus ; soumission PENDING puis CONFIRMED ; focus continuant sur l’action suivante, refus et issue inconnue distincts. Aucun piège observé sur ces parcours. Un essai DOM forçant le focus sur body était non probant et a été remplacé par une entrée Tab native ; aucun défaut produit n’en est déduit.
- Shell : thèmes System/Light/Dark et langue FR/EN/FR au clavier, focus SELECT et ancre conservés ; préférences finales FR/System restaurées. Aucun compteur de rechargement non exposé n’est inventé.
- Contrastes calculés sur couleurs effectivement rendues : minimum texte Light6,236:1 et Dark8,694:1 ; bordures Light3,989:1 et Dark4,872:1 ; minimum focus Light6,643:1 et Dark10,362:1. Les échantillons texte dépassent4,5:1 et bordure/focus3:1 ; échantillons détaillés dans interactive-evidence.json, pas de certification exhaustive de toute interface tierce.
- Reflow à320×800 : scrollWidth305, zéro élément débordant observé. La capture instrumentée à échelle200 % reste distincte du zoom natif200 % confirmé humainement par E.
- Réduction des mouvements : préférence navigateur émulée reduce puis no-preference, matchMedia cohérent ; aucune animation/transition CSS non nulle observée dans les deux cas. Émulations et viewport réinitialisés ensuite.

Preuves persistantes : output/cismp/cismp3-pixs-c4b2bfe2c6614f3f/manual-accessibility/e1da7a1f4b/interactive-evidence.json et captures light-desktop.png, dark-desktop.png, dark-scale-200.png, light-mobile.png, shell-dark.png. Les empreintes et les reçus natifs sont conservés dans manual_accessibility_artifacts, manual_accessibility_complete et screen_reader_user_environment du checkpoint.

Les serveurs locaux e1da7a1f4b et e9d65e4984 sont fermés sur EXPLICIT_FINISH, avec server_closed=true, cache_removed=true et Bash natifs exit0. OpenCode et les services CAB partagés sont préservés. Aucune source produit n’a été modifiée pour ces contrôles. Le niveau cible WCAG2.2AA est vérifié sur le périmètre C11 livré par contrôles combinés ; il ne vaut pas certification exhaustive de contributions ou profils non sélectionnés.

### Recoupement des sources et limites de couverture

Le recoupement du soir est tracé par evening_source_freshness : 270 fichiers protégés en lecture, aucune dérive des 65 sources C11 recensées, aucune erreur UTF-8, aucun CR ni BOM. Le NUL préexistant de frontend/scripts/composition-imports-v1.mjs est préservé ; aucune normalisation hors périmètre. La revue est bornée aux fichiers déclarés et à leurs empreintes natives, sans Git ni ouverture des fichiers sensibles exclus. Elle ne constitue pas une recherche exhaustive de secrets sur le dépôt.

Les 31 sources des recettes C14 présentent un seul écart : src/pixs/backend/apps.py, f19ef37bf30125fb4d2fbb672572c5f6931bf470e5a6f052b882415fbc54b308 vers 935dd73eacf31ab1d251e31bee1dc510895243b131164df6e3bc833a2c0528fb. La fixture sélectionne explicitement les applications Auth/Core/PZT/DNS ; PixsBackendConfig reste hors de cette sélection. Ce constat statique conserve les résultats datés et leurs limites ; il ne prétend ni reconstituer les anciens octets ni réexécuter PostgreSQL contre le fichier courant.

Les cas Python test_module_and_submodule_empty_frontend et test_nested_module_submodule_and_private_child_claim gardent leur portée Kernel/capture. Le complément de recette ci-dessous prouve maintenant le chargement et le rendu d’un sous-module dans le bundle. Les recettes C14 conservent leur portée de vrais modules PZT/DNS dans le shell produit. Les contrôles manuels obligatoires sont désormais consignés ci-dessus ; leurs limites ne remplacent aucune preuve d’intégration.

### Complément 2.4 — sous-module frontend rendu dans le bundle

Le fichier frontend/tests/composed-submodule.test.mjs, SHA-256 a9c19ff202c9ca95c245573f2582f6ee55e9230c9281acc27c6d463155191a85, est exécuté par la commande suivante :

```bash
PATH=/home/devops/node/current/bin:/usr/bin:/bin /home/devops/node/current/bin/node --test frontend/tests/composed-submodule.test.mjs
```

Résultat natif : exit0, 1 test réussi, 8 chargements DOM réussis, aucun échec/skip. Message msg_16abf3e23001DTO7Y4XHLNrXIf / partie prt_16abf492e0011Y2u1E4OQSnHIn. Preuve complète : submodule_real_bundle_test_result dans le checkpoint du RUN.

La fixture sélectionne un MODULE acme.parent et un SUBMODULE acme.child réellement imbriqué et dépendant du parent, avec6 contributions publiques. Le vrai Kernel/Python, la capture épinglée et Vite construisent le graphe ; un pin altéré est réellement refusé. Les rapports de développement et du bundle sont identiques. Dans chaque moteur, le parent et l’enfant sont chargés une fois depuis Vite puis une fois depuis les octets du bundle construit ; les titres et marqueurs DOM, propriétaires, chemins, ordre et pins sont vérifiés. Le vrai React et le vrai adapter du shell rendent les arbres.

Les attestations et le contexte sont des données synthétiques de test ; le routage est celui du harnais. Ce contrôle ne qualifie ni Auth, ni PostgreSQL, ni le routage complet du shell, ni l’accessibilité manuelle. Les preuves C14 du vrai shell et des opérations HTTP/PG restent distinctes. Les profils courts, groupes de processus, serveurs, fixtures, bundle et cache temporaires ont été nettoyés ; main.js est resté inchangé.

### Revue visuelle et fraîcheur finales

Les appels C14 supplémentaires call_01a16aaaba3d774e93a80f78cac802ba et call_01a16aab9467709fbc1a3dc63e7dff23 sont recoupés dans c14_evening_additional_native_proofs. Leurs8 PNG (PZT/DNS, Chromium/Firefox,1280/390) ont leurs empreintes vérifiées puis leurs pixels relus par Root : texte, titres et focus visibles, sans débordement horizontal observé sur les cadres capturés. Les captures montrent Light et le haut des formulaires seulement. Le lien Sign in reste visible pendant Verified session/Sign out ; constat conservé sans modification C14. Aucun verdict de conformité AA, contraste mesuré, Dark ou lecteur d’écran n’est déduit de ces captures.

phase2_final_evening_review compare271 fichiers, dont66 fichiers C11 : aucune dérive nouvelle ni erreur UTF-8/CR/BOM. Cette comparaison est bornée aux empreintes et sources connues, sans Git, fichier sensible exclu ni recherche exhaustive de secrets. Le dernier contrôle OpenSpec strict sera consigné après cette édition ; la revue manuelle complémentaire ci-dessus permet la validation technique C11. L’archive et la publication doivent conserver leurs reçus propres.

### Requalification après modifications Core concurrentes

Le 24 octobre 2026, le contrôle final a détecté deux sources modifiées par le RUN propriétaire C08 : src/pixs/core/services_common.py et src/pixs/core/services_transactions.py. Les anciennes preuves propriétaires restent datées et ne sont pas attribuées aux nouveaux octets. Un premier contrôle de pins a terminé exit1 avant import/recettePG ; il n’est pas présenté comme un échec fonctionnel ni comme un succès de test.

Une nouvelle recette exécutée sur les sources protégées réussit dans Chromium et Firefox :15 critères par moteur,14 HTTP200 par moteur, vraies mutations PZT/DNS persistantes puis retrait, session WEB et contexte PLATFORM, LF/ordre/doublons, FR/EN et message UNKNOWN distinct. Les266 empreintes suivies sont identiques avant/après. Connexions, serveurs, groupes enfants, profils et fichiers temporaires sont nettoyés. TLS loopback chiffré avec bypass de chaîne dans les seuls profils jetables ; ni P0 ni TLS déployé qualifiés.

Preuve native : msg_16afeec55001JolUVa7gNEIDPL / prt_16afef35100124G7ONkWln0OSh ; clé c14_current_core_requalification_native_proof, résultat c14_current_core_requalification_result du checkpoint. Core services_common.py courant : f13a2b6024937948d4148e16d1d208193cae137b0d7514f3fa9a65bb8b906d9a ; services_transactions.py courant : d2eeb6a536d25d60c16e34c86b618a752513aaaa0ce21752fe00b6e8f2e32bbe. La revue271 est réconciliée avec ces deux changements et la seule édition documentaire VALIDATION.md ; aucune source produit C11 ne change.

