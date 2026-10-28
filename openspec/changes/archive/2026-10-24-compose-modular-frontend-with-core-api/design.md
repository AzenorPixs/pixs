# Conception — C11

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 a été adopté et archivé le 18 octobre 2026 ; ses précisions normatives sont intégrées au canon. Les arbitrages propres au présent change restent à lever avant réalisation.

## État actuel vérifié

Constat : Le shell est autonome ; les facettes frontend sont des déclarations immuables sans composition récursive de modules opérationnelle.

Sources consultées et empreintes recoupées avec la matrice :

- [frontend/src/main.js](../../../frontend/src/main.js).
- [frontend/README.md](../../../frontend/README.md).
- [src/pixs/kernel/frontend_contribution_declarations.py](../../../src/pixs/kernel/frontend_contribution_declarations.py).
- [src/pixs/kernel/manifest/models.py](../../../src/pixs/kernel/manifest/models.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Composer au build depuis manifests et contrats publics, sans registre/lifecycle frontend parallèle. Résoudre récursion et dépendances, collisions et façades ; le shell fournit session/contexte et consomme les API. Une intention UI ne devient un effet confirmé qu’après réponse serveur ; invalidation sous tenant courant.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

API publique du shell et points de contribution, frontières de build et catalogue de routes à formaliser ; conserver JavaScript existant sans conversion TypeScript implicite ni téléchargement runtime.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [add-protected-core-http-commands-and-queries](../archive/2026-10-22-add-protected-core-http-commands-and-queries/proposal.md).
- [activate-reference-runtime-composition](../archive/2026-10-21-activate-reference-runtime-composition/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Module et sous-module ajoutés sans éditer le shell ; collision et import privé refusés ; navigation/session/tenant corrects ; annulation ou refus de mutation visibles ; ordre identique entre développement et artefact.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T02 — PBO/PFO réellement servi par le paquet

Le serveur/bundle/routage et la frontière HTTP distribuée ne sont pas détaillés par un propriétaire commun. N04 dédié et deltas ciblés validés ; décisions de serveur/session/transport encore ouvertes.

Contrôles à intégrer : Navigation directe du shell via service livré ; Erreur API sans fallback HTML ; Hôtes/origines/en-têtes non fiables, CSRF si cookie ; Management et rôles non publics.

### T07 — Administration utile avec compte ordinaire

Les grandes rubriques existent ; il faut arrêter le catalogue minimal d’actions et prouver le parcours ordinaire, pas seulement celui du Super Admin. Compléter critères de C06/C13 et recette C17 ; aucun module métier ajouté.

Contrôles à intégrer : Créer identité/utilisateur/groupe/appartenance selon droits ; Lire/modifier ACL sans élargir tenant/scope ; Accès interdit invisible et inexécutable ; API utilisable sans PFO.

### T08 — Audit exhaustif du panneau et navigation SPA

L’audit de chaque activité du panneau inclut navigation/lecture ; des logs ou un acquittement mémoire n’en prouvent pas la persistance. Compléter protocole C05/C13 et critères de volumétrie/minimisation C15 ; préserver exception Super Admin.

Contrôles à intégrer : Panne sink avant affichage/action ordinaire refusée selon contrat ; Dérogation root sans audit annoncé à tort ; Navigation SPA reliée à une preuve serveur et aucune donnée sensible copiée.

### T09 — Contexte tenant et réponse retardée du navigateur

L’invalidation est prévue ; les réponses en vol, onglets et changements de session doivent être inclus dans le contrat de concurrence UI. Compléter C11 et sa recette ; pas d’offline, cache distribué ou client natif imposé.

Contrôles à intégrer : Réponse du tenant précédent n’alimente pas la vue courante ; Déconnexion et révocation invalident contexte ; Identifiant/header fourni ne remplace pas le tenant canonique.

### T14 — PZT/DNS gérés sans exécution PA

La table 193 clauses reste conditionnelle et exige revue par rôle avant adoption ; classement exécutant ne retire pas les clauses PBO de gestion. Conserver C14 comme propriétaire, contrats/schémas/valeurs administrées explicités avant code ; aucun nouveau change exécutant sélectionné.

Contrôles à intégrer : Modules essentiels présents même réseau désactivé ; État souhaité distinct de mesure/appliqué ; Suffixe/droits/conflits des données gérées conformes ; Aucune publication DNS/réseau ni modification hôte inventée.

Voir [audit transversal durable](../archive/2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.

## Réconciliation documentaire du 22 octobre 2026

C06 est livré : le catalogue HTTP et OpenAPI porte la version de contrat `1.0.0` et couvre 156 opérations. Ses preuves finales sont consignées dans [son design](../archive/2026-10-22-add-protected-core-http-commands-and-queries/design.md#preuves-finales-examinées) et [ses statistiques](../archive/2026-10-22-add-protected-core-http-commands-and-queries/STATISTIQUES.md) ; aucun fichier supplémentaire nommé `VALIDATION.md` n’est nécessaire pour identifier ces preuves historiques. C07 fournit le [socle intermédiaire qualifié](../archive/2026-10-21-activate-reference-runtime-composition/VALIDATION.md), sans prétendre livrer la composition frontend. Ces sources ne remplacent pas les contrôles actuels requis par C11.

C11 applique les deux clauses API adoptées : façade web à session serveur, cookie protégé inaccessible au JavaScript et CSRF, distincte de l’API Bearer ; aucun jeton persistant accessible au JavaScript. Les justificatifs ambigus suivent le contrat explicite des routes, sans élargissement de l’admission. Les références et scénarios sont actualisés dans `requirements.md`, sans modification du canon.

Les contrôles C11 comparent la composition en développement au bundle effectivement construit et chargé dans un environnement d’intégration isolé. Ils couvrent les refus et interactions exigés par chaque tâche sans les différer. La qualification du paquet Debian et de sa distribution demeure obligatoire dans C18/C17/C19 ; elle ne devient pas un prérequis inverse à C11. Cette distinction ne dispense aucune garantie applicable à l’artefact final.

Les barrières de conception de la tâche 1.2 restent à traiter avant code. Les profils structurels frontend v1 sont conservés avec leurs limites ; leur reconnaissance seule ne compose ni n’active une contribution. Aucun choix technique encore ouvert n’est réputé validé par cette réconciliation.

## Conception 1.2 retenue par CGPT pour C11

Ces choix concrétisent le canon frontend/API existant. Ils ne changent ni les profils structurels v1 ni les règles d’autorisation. Ils ne valent pas preuve d’implémentation ; chaque tâche suivante conserve ses propres tests et son mandat.

### Composition et provenance au build

Le pont reçoit les textes TOML de manifests explicitement sélectionnés et les paramètres communs official_ids, required_ids, configured_providers et attestations. Il utilise les interfaces publiques validate(texts, ...) et compose(manifest_texts, ...) sur les mêmes textes. Il associe les ComponentManifest validés à CompositionResult.order et edges, puis projette leurs facettes frontend. capability_descriptors ne contient pas ces facettes et ne les remplace pas. Les diagnostics et avertissements restent conservés ; globally_compatible reste faux. Aucun registre, découverte implicite ou lifecycle de composants parallèle n’est ajouté.

Une politique BuildLimits explicite fournie par l’appelant borne nombre de manifests, taille par manifest et taille totale ; aucune valeur implicite n’est retenue. Les sources autorisées lient propriétaire, version, racine physique, provenance et empreintes attendues. Les chemins d’entrée sont confinés physiquement au composant et vérifiés avant chargement. Une attestation de conformité ne prouve pas à elle seule les octets JS. Le build contrôle les sources et leurs imports, capture les octets vérifiés et construit depuis ces mêmes octets ; un changement de source ou de politique invalide le plan. Il ne fabrique ni attestation ni confiance. La qualification de l’identité de distribution demeure distincte en C19.

Le pont Python utilise la bibliothèque standard et les interfaces Kernel existantes, sans nouvelle dépendance ni modification de leurs validateurs purs. Son plan intermédiaire déclaré est généré sous frontend/.generated/composition.json ; le build composé le consomme puis publie frontend/dist/composition.json avec le bundle. Le nettoyage de dist ne doit pas supprimer l’unique entrée avant lecture. Le mode shell autonome existant reste identifié comme tel ; un plan absent ou invalide ne devient pas une composition intégrée prête. Les modes composé en développement et en build utilisent les mêmes entrées et politiques explicites.

### Déclarations opérationnelles et façades publiques

component.toml demeure la source déclarative unique des composants et des contributions sélectionnées. Aucun sidecar de composant n’est découvert par convention. Le point entry déjà déclaré expose un descripteur JS public, de schéma fermé version 1.0.0. Il relie les contributions explicitement référencées par leurs identifiants à leur type, version, scope et requires, au point d’extension cible versionné, à leurs permissions d’affichage déclarées, à leur niveau de confiance et à leur caractère obligatoire ou optionnel. Ces valeurs doivent concorder avec la facette v1 ; aucune contribution supplémentaire n’est activée parce qu’elle existe dans un fichier. Les charges de présentation sont propres au type : route et mode CSR, export de page/composant/formulaire, navigation par route et clé de traduction, catalogues, hint UI ou slot public namespacé. Leur schéma exécutable fermé et leurs refus sont définis et testés dans 2.1, sans grammaire parallèle aux dépendances communes.

Les points du shell sont versionnés 1.0.0 : routes, navigation, traductions et slots pixs.shell.header, pixs.shell.navigation, pixs.shell.main et pixs.shell.footer. Une collision de route ou le masquage d’une route protégée est refusé. Les compositions multiples autorisées ont un ordre déclaré, fondé sur le graphe commun puis l’identifiant de contribution ; aucune priorité de découverte ou override implicite. Les dépendances de contributions sont contrôlées sans refaire le registre des composants. Une contribution optionnelle incompatible est isolée avec diagnostic ; une contribution obligatoire invalide bloque le périmètre. SANDBOXED n’est jamais déclaré isolé sans adapter effectif : l’absence de support conduit au refus ou à l’isolement optionnel, sans exécution non confinée. DEVELOPMENT est refusé en production.

L’import public du shell est pixs-shell/v1, mappé au build. Les exports retenus sont SHELL_API_VERSION, ShellContextProvider, useShellContext, QueryClient, CommandClient, navigate et invalidateScope, ainsi que les interfaces publiques de traduction et d’adapter de présentation nécessaires aux contributions. Les modules ne consomment ni store privé, token brut, moteur de style direct ni import relatif profond du shell ou d’un composant frère. Le build contrôle les imports par le graphe syntaxique et les façades déclarées, sans se limiter à des expressions régulières. Aucun téléchargement ou évaluation de code distant n’active une contribution.

Les routes propres du shell sont /, /login, /platform, /tenants/{tenant_id} et /tenants/{tenant_id}/scopes/{scope_id}, avec le traitement des routes inconnues existant. Elles fournissent le shell et son contexte ; elles ne réalisent pas le panneau C13. Les contributions ajoutent leurs routes publiquement déclarées sans éditer le shell. QueryClient lit par les API publiques ; CommandClient traite les intentions comme provisoires jusqu’au résultat serveur connu, conserve corrélation et idempotence et ne transforme pas une issue inconnue en succès.

### Contexte courant : propriétaire Auth et frontière serveur

Le raccord est explicitement possédé par Auth et porte un contrat indépendant version 1.0.0. Sa surface WEB à cookie comprend GET /api/v1/web/platform/shell/context, GET /api/v1/web/tenants/{tenant_id}/shell/context et GET /api/v1/web/tenants/{tenant_id}/scopes/{scope_id}/shell/context. Le contrat HTTP et ses protections sont publiés explicitement. Il n’accepte pas Authorization comme substitut du cookie ; l’API Bearer C06 et ses routes restent distinctes. Les protections de transport HTTPS, hôte, origine et CSRF applicables à la méthode suivent les frontières existantes. Le contexte vient du chemin canonique serveur ; une indication client contradictoire reste refusée.

Le producteur serveur consomme les ports publics Auth/C04/C05 dans leur transaction et leur périmètre. resolve_token est une orientation liée aux enregistrements, pas une preuve suffisante de validité courante. Avant exposition, la source d’invocation revalide effectivement AuthenticationContext et RevocationStatus, sujet, session, contexte, fraîcheur, confiance et révocation ; l’autorisation et les garanties d’audit/gouvernance sont vérifiées puis recontrôlées à la frontière requise. Aucun témoin antérieur ne devient une autorisation de restitution. La source reste côté serveur et est fermée après traitement.

L’action déclarée est pixs.auth.session.context.read sur la référence de session courante déterminée par le serveur. Elle est déclarée et, si nécessaire, accordée par les mécanismes propriétaires existants ; C11 ne crée aucun grant ni règle ALLOW implicite. Le client ne choisit pas une autre session à inspecter. Une action non déclarée, une politique absente ou un contrôle ordinaire refusé ne produit pas de contexte autorisé. L’exception Super Admin s’applique uniquement dans ses conditions canoniques, sans fabrication de fait structurel ni extension de tenant. Les garanties C10/C09 non encore livrées ne sont pas simulées silencieusement ; les ports et doubles de recette sont explicitement distingués.

La projection est une liste blanche : identity_ref, ScopeContext canonique, identifiant de session, catégorie et façade ; authentication_time et expires_at en UTC ; niveaux identity_assurance et authentication_assurance déjà calculés par le C03 vérifié. Elle ne renvoie ni provider, issuer, external_subject, credential_id, cookie, jeton, preuve brute ou policy interne. Les hints UI ne proviennent que de décisions serveur liées aux actions et ressources déclarées du contexte ; leur indisponibilité est explicite et ne crée aucun droit. Leur présence ne remplace jamais l’autorisation d’une Command ou Query. Aucun ACL n’est reconstruit dans le navigateur depuis des listes de rôles/appartenances.

Les réponses sont typées et no-store, avec corrélation et refus explicites selon les contrats existants. Une panne ou issue inconnue n’expose aucun contexte partiel. Un GET de contexte ne prolonge pas l’activité de session. La configuration interactive_commands C06 reste explicite et inchangée. Les seuls cookies d’authentification sont ceux du propriétaire Auth, protégés et inaccessibles au JavaScript ; aucun token d’accès ou renouvellement n’est persisté par le shell.

Le shell ne rend actif un nouveau contexte qu’après vérification serveur. Au changement de tenant/scope, à la déconnexion ou révocation, il invalide immédiatement les requêtes et états dépendants ; une réponse retardée d’une époque antérieure est ignorée. Si la session n’est pas liée au nouveau contexte, une réauthentification serveur est requise. Les échanges d’invalidation entre onglets ne transportent aucun secret et ne donnent aucun droit. Les garanties hors ligne, cache distribué et client natif ne sont pas activées.

### Réalisation, fichiers et preuves séquentielles

2.1 définit et teste les contrats des façades, descripteurs et du pont, leurs entrées/sorties immuables, versions, provenance et refus. Le pont est placé dans frontend/scripts/build_frontend_composition.py et les façades dans frontend/src/shell/api-v1.js ; les tests propres à ces contrats accompagnent cette tâche. Les validateurs Kernel v1 sont réutilisés sans leur ajouter IO, composition ou activation.

2.2 réalise la résolution et le build composé : frontend/vite.config.js, frontend/src/main.js et les modules de composition nécessaires sous frontend/src/shell/ et frontend/scripts/, avec tests ciblés par fichier proposé. Il prouve immédiatement récursion MODULE/SUBMODULE, dépendances, imports publics, refus de collisions/trust, conservation des octets et comportement du bundle construit dans Chromium et Firefox, sans attendre 2.4. Les sources de fixtures sont déclarées et ne deviennent pas des modules de production implicites.

2.3 réalise le producteur Auth de contexte et son adapter HTTP, proposés sous src/pixs/auth/shell_context.py et src/pixs/backend/api_shell_context.py, puis le transport et les états de session du shell. Une extension additive publique de frontière dans src/pixs/backend/api_core_views.py peut être proposée séparément pour réutiliser les contrôles existants sans import privé client ni modification du comportement C06. Les raccords exacts supplémentaires et tests sont présentés avant écriture. La recette utilise les véritables C03/C04/C05/Core/C06 avec PostgreSQL et identifie tout port encore fourni par un double. Elle couvre identité/session révoquée ou expirée, absence de grant, contexte substitué, panne d’audit/gouvernance, exception Super Admin conforme, cookie/Bearer/CSRF, concurrence et réponses retardées ; elle ne revendique aucune garantie externe non exécutée.

2.4 complète les preuves transversales : ajout d’un module et sous-module sans éditer le shell, versions, déterminisme et équivalence développement/bundle construit. Elle ne remplace pas les tests exigés par 2.1 à 2.3. La qualification du paquet Debian reste C18/C17/C19.

Chaque interface touchée reçoit ses contrôles clavier/focus, sémantique et noms accessibles, technologies d’assistance, contraste Light/Dark, zoom/reflow et réduction des mouvements, avec séparation des vérifications automatisées et manuelles. Un contrôle requis non disponible reste une preuve manquante et bloque la validation de la tâche concernée ; il n’est pas masqué par le build. Les tâches 3.x consolident syntaxe, suites configurées, non-régression C06/C07, conformité OpenSpec, encodage et périmètre. Aucun archivage ni déclaration P0 globale ne précède ces preuves.

### Réconciliation 1.2 du 23 octobre 2026 — périmètres, transport et saisies

Les références tenant_id et scope_id suivent ScopeContext Core : chaînes non vides opaques, conservées à l'identique, sans contrainte UUIDv7. PLATFORM ne porte aucune de ces références ; TENANT exige tenant_id et admet scope_id absent. La sérialisation HTTP encode chaque référence comme un segment unique, sans normalisation ni découpage de son contenu ; une référence non représentable dans le transport reçoit un refus typé sans envoi. Le format UUIDv7 de session_id demeure celui du contrat Auth. La structure ne vaut jamais authentification ni autorisation.

QueryClient et CommandClient utilisent un résolveur de transport public injecté explicitement par la composition de confiance. Son contrat de version 1.0.0 est fermé et immuable : chaque liaison désigne le nom exact, le genre QUERY ou COMMAND, le propriétaire, la version du contrat propriétaire, les contextes admis et les segments littéraux du suffixe HTTP publié. Le couple genre/nom est unique ; une collision est refusée, sans remplacement silencieux. L'adapter Core conserve ses 15 collections et 22 commandes publiques C06 avec leurs contextes admis. Les autres propriétaires fournissent leurs liaisons publiques explicitement ; aucune route n'est déduite d'un nom, transformée de snake_case en kebab-case ou découverte par scan. Une liaison absente ou incompatible est refusée avant tout envoi. Les liaisons C14 PZT/DNS non publiées ne sont ni inventées ni qualifiées par C11 ; leur absence ne se transforme pas en capacité disponible.

Le résolveur ne reçoit pas d'URL arbitraire d'une contribution : la racine WEB canonique est construite depuis le contexte courant vérifié, puis les segments de la liaison contrôlée sont encodés séparément. Origines externes, parcours parent, suffixes ambigus, fragments, paramètres de requête intégrés et tentative d'accès aux surfaces réservées Auth/CSRF/contexte sont refusés. Le transport reste celui de la façade WEB à cookie protégé et CSRF ; aucun mode Bearer, jeton brut ou autorisation implicite n'est ajouté. Snapshot, époque, refus des réponses retardées, corrélation et idempotence conservent leurs garanties existantes. Une liaison de route ne prouve ni disponibilité serveur ni droit d'accès.

Les paramètres de QueryClient sont typés selon le contrat propriétaire. Pour Core, limit est un entier sûr strictement positif soumis aux bornes explicites de l'API, cursor reste une chaîne opaque, et ref une liste dense de chaînes sérialisée en clés répétées. Les doublons Core sont refusés ; le tri Core appartient au serveur et n'est pas appliqué aux listes ordonnées des autres propriétaires. Les champs de présentation nécessaires sont texte, booléen strict, entier sûr et liste ordonnée de chaînes ; aucune conversion implicite de texte en booléen ou nombre, ni valeur par défaut ou borne métier nouvelle. Les contrôles de plage et de cardinalité viennent du contrat propriétaire explicite. Ordre et répétitions des listes sont conservés sauf interdiction propre à ce contrat. Les arbres et ports existants gardent leur validation fermée, leurs limites explicites et leurs contrôles d'accessibilité.

La tâche 2.1 corrige et teste les façades et le résolveur dans frontend/src/shell/api-v1.js avec leurs tests de contrat, sans modifier Core, Auth ou C14. La tâche 2.2 reprend seulement après revalidation de 2.1 ; elle complète les primitives de présentation, leurs validateurs/adapters et tests, puis le pipeline de composition et le raccord réel au bundle. Les tests couvrent scopes opaques et encodage, session Auth UUIDv7, route propriétaire explicitement injectée, absence/collision/version/contexte interdits, absence d'envoi après refus, paramètres Core sans coercition, états provisoires et réponses retardées. Les saisies typées et leurs refus ont leurs propres unités et recettes navigateur avant validation de 2.2 ; aucune garantie HTTP C14 ni qualification de paquet Debian n'est annoncée. Cette décision d'implémentation ne modifie aucun canon ni profil structurel v1.


### Précisions de réalisation C11 — 23 octobre 2026

Ces précisions restent dans le change C11 validé et n'ajoutent ni provider d'exécution, ni qualification P0. Les mots-clés MUST, MUST NOT et MAY gardent leur sens RFC 2119. L'organisation en deux phases demandée dans tasks.md prévaut sur le séquencement élémentaire historique : réaliser et préparer les recettes, puis exécuter les contrôles avant validation et archivage.

**Entrées du build.** Le chemin nominal MUST recevoir une sélection LOCAL_OPERATOR_SELECTION, schéma pixs.frontend.selection/1.0.0, et un document de politique pixs.frontend.build-policy/1.0.0 à clés fermées schema/policy/limits. La sélection, ses attestations externes et la politique MUST être épinglées par leurs octets originaux. L'appelant MUST authentifier les preuves de conformité et les lier aux composants/cibles et versions exactes ; le pont MUST NOT fabriquer un verdict ou assimiler une preuve partielle à une qualification globale.

Les sept groupes de limites MUST être fournis sans valeur implicite. Leurs compteurs sont des entiers sûrs strictement positifs :

| Groupe | Champs fermés |
|---|---|
| selection | max_selection_bytes, max_owners, max_files_per_owner, max_total_files, max_bytes_per_file, max_total_bytes |
| requirements | max_contributions, max_requirements_per_contribution, max_total_requirements |
| imports | maxSourceBytes, maxTotalSourceBytes, maxModules, maxImports, maxBindings, maxResolutions, maxInputNodes, syntaxLimits |
| imports.syntaxLimits | maxSourceBytes, maxAstNodes, maxDescriptorCount, maxTextLength, maxLiteralItems, maxLiteralDepth |
| graph | maxContributions, maxFacts, maxEdges, maxInputNodes, descriptorLimits |
| graph.descriptorLimits | maxTextLength, maxRequires, maxPermissions, maxPoints, maxLocales, maxCatalogKeys |
| sourceProfile | maxSourceBytes, maxAstNodes, maxBindings, maxTextLength, maxScopeDepth |
| presentation | maxNodes, maxDepth, maxChildren, maxTextLength, maxParams, maxFields, maxBindings, maxDataNodes, maxBodyDepth, maxBodyNodes |
| wire | maxPolicyBytes, maxWireBytes, maxPolicyNodes |

syntaxLimits et descriptorLimits sont des groupes, pas des compteurs. Les bornes wire MUST concorder avec les arguments CLI. La politique MUST expliciter admissions, imports/façades étrangères, points modulaires, locales et fusion ; une configuration absente ou ambiguë MUST refuser le montage.

La CLI run_frontend_build.mjs MUST recevoir mode et command ; COMPOSED exige aussi selection/selection-sha256, policy/policy-sha256, max-policy-bytes/max-wire-bytes et python absolu. STANDALONE MUST refuser ces paramètres inutilisés. Les chemins JSON opérateur MUST rester relatifs au projet, confinés et sans source exclue ou lien symbolique. Le lancement MUST NOT lire un env ou découvrir une configuration par défaut.

Pour ce chemin nominal, la sélection capturée, le plan Kernel, les faits et le graphe circulent en mémoire dans prepareFrontendComposition ; cette précision remplace l'obligation antérieure d'un fichier intermédiaire .generated/composition.json. Les anciens producteurs de plan restent des outils distincts et ne constituent pas une entrée nominale implicite. Le plugin MUST n'accepter qu'une composition préparée par ce chemin, compiler les octets capturés et les tables d'import contrôlées, puis produire le rapport public composition.json avec le bundle. Les mêmes entrées MUST être contrôlées en développement et en build ; toute dérive MUST produire un refus avant acceptation de l'artefact. Les points, factories et paramètres privés du renderer MUST NOT être transmis comme moteur aux contributions.

**Présentation et actions.** La primitive record-list complète les quatre champs décrits plus haut pour représenter une liste ordonnée d'enregistrements à colonnes déclarées. Chaque colonne contient exactement name/key/params/required ; les lignes contiennent exactement les noms déclarés et des chaînes. initial/minItems/maxItems sont explicites. Un champ string-list conserve initial/minItems/maxItems/itemRequired ; integer conserve initial/minimum/maximum. Un entier facultatif vide vaut null, sans coercition de texte ; false MUST rester un booléen valide. Les bornes et colonnes MUST venir du contrat propriétaire. Une zone multiligne par valeur/cellule MUST conserver LF, ordre et doublons sans trim/split/parse JSON. Les ajouts/suppressions MUST garder noms accessibles et parcours clavier.

Une factory de vue MUST être synchrone et retourner {schema:"pixs.presentation/1.0.0",root}. Elle reçoit seulement api/context/routeParams/state, avec données gelées et état actions/fields isolé par propriétaire et contribution. La ROUTE désigne son export JS par payload.page ; les autres rendus par payload.export. Le rendu MUST valider l'arbre et les références publiques ; un composant ou slot privé/non déclaré ou un cycle MUST être refusé. Un rendu MUST NOT provoquer de réseau, commande, navigation ou invalidation. Une révision explicite d'action/contexte ou de présentation MAY relancer la factory pure avec les nouvelles données ; cela MUST NOT rejouer une intention.

Les actions et champs MUST être isolés par couple propriétaire/contribution et identifiant local. Les actions retirées d'un nouvel arbre MUST cesser d'être exécutables. Query utilise LOADED ; Command n'utilise CONFIRMED qu'après résultat serveur. Une saisie invalide MUST rester distincte d'un résultat confirmé ; un nouvel événement d'erreur MUST NOT remplacer un UNKNOWN par un faux refus définitif. PENDING MUST interdire le double envoi. En UNKNOWN, le runtime MUST conserver clé d'idempotence, empreinte SHA-256 du contenu et liaison de contexte/session, sans relance automatique. Un contenu ou contexte différent MUST refuser la reprise. Une issue antérieure inconnue MUST NOT être résolue par un cache ou par un refus qui ne prouve pas son résultat.

Un changement d'époque/contexte/route MUST purger les données dépendantes avant notification et ignorer les réponses retardées. Les brouillons MUST suivre modelKey et l'époque ; une simple progression d'action MUST NOT les remonter arbitrairement. Les composants publics et slots MUST respecter les dépendances exactes et les points du graphe. Sans correspondance positive UI action/ressource spécifiée, les display_permissions demandées restent indisponibles de façon conservatrice ; aucune permission ni garantie de sandbox MUST être déduite du code client.

**Raccord serveur et continuité.** Le propriétaire Auth fournit PostgresShellContextService et l'adapter WEB de contexte ; les gardes C03/C04/C05 et les ports complémentaires nécessaires MUST être réels ou explicitement identifiés comme doubles de recette. Les bindings propriétaires MUST être injectés explicitement par module_bindings. Les opérations Core et les bindings admis sont projetés dans meta.transport_resolver, séparés des données Auth et hints ; ils MUST NOT créer de droit ni être découverts depuis le nom d'une commande. La fabrique module HTTP/OpenAPI MUST préserver les gardes communes et les contrôles propriétaires, sans affaiblir le validateur documentaire Core.

Le client du shell MUST envoyer X-Shell-Session-ID pour ses requêtes WEB authentifiées Query/Command/logout, avec l'identifiant de son contexte vérifié. Le serveur MUST comparer cette indication à la session résolue du cookie avant dispatch et refuser CONTEXT_MISMATCH en cas de différence. L'en-tête reste optionnel dans le contrat HTTP général : les clients legacy sans indication et la façade Bearer conservent leur comportement. Bootstrap contexte, login et CSRF MUST NOT réutiliser une ancienne indication. Cette garde MUST NOT accorder d'autorisation.

Le runtime MUST conserver HTTPS, cookie protégé et CSRF, et MUST NOT lire/persister un jeton ou justificatif dans un stockage navigateur. Une expiration, indisponibilité réseau ou de canal inter-onglets MUST être explicite ; un échec de canal MUST notifier la purge avant propagation. Un 401/403 MUST NOT être présenté comme preuve de révocation. Les timers, requêtes et abonnements propres MUST être libérés ; aucune fermeture de service partagé n'est impliquée.

**Preuves à produire.** Ces décisions et les sources réalisées ne valent pas réussite des recettes. La phase 2 MUST exécuter syntaxe, suites ciblées/non-régression, build réel, équivalence développement/bundle, refus de provenance/import/trust/collisions/dérive, session HTTP/PostgreSQL et contrôles navigateur/accessibilité applicables. Les temporaires, doubles, versions et empreintes MUST être identifiés ; une preuve obligatoire manquante MUST rester ouverte et bloquer la validation concernée. L'archivage et son STATISTIQUES.md MUST suivre ces preuves et ne qualifient pas C18/C17/C19 par anticipation.
