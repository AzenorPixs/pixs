## ADDED Requirements

### Requirement: Quatre binaires et sept modes explicitement répartis

PA MUST comporter exactement quatre binaires dédiés : démon système pour system-daemon ; événements système pour system-start et system-stop ; sessions utilisateur pour session-start, session-stop et session-daemon ; exécution PZT pour pzt-daemon. Les noms d'exécutables, chemins et options CLI restent à spécifier. Le découpage MUST NOT créer un cinquième binaire pour le démon de session.

#### Scenario: Quatre binaires et sept modes explicitement répartis

- **WHEN** une distribution PA complète décrit ses exécutables
- **THEN** elle identifie les quatre responsabilités et les sept modes sans les confondre

### Requirement: Compilation différenciée validée

Les binaires démon système, événements système et sessions utilisateur MUST être compilés avec Nuitka ; le binaire PZT MUST être compilé avec Cython. La chaîne MUST partir des sources Python, générer du C puis des exécutables natifs avec runtime et dépendances déclarés. Versions exactes et compatibilité MUST être qualifiées avant construction ; cette décision MUST NOT installer une dépendance ni prouver un gain de performance.

#### Scenario: Compilation différenciée validée

- **WHEN** la matrice de compilation est déclarée
- **THEN** les trois premiers binaires utilisent Nuitka et celui de PZT utilise Cython

### Requirement: Plateformes demandées et qualification progressive

PA MUST conserver le périmètre Linux et Windows physiques, VM Linux et Windows, Docker et LXC sous Proxmox. La première qualification MUST cibler Debian/Linux et Docker locaux, puis les autres cibles ; une cible non qualifiée MUST être indiquée comme telle. Versions OS/CPU, topologies Docker dans VM ou LXC, droits, bureaux et vTPM MUST être déclarés par profil ; aucun support MUST être inféré du seul environnement de développement.

#### Scenario: Plateformes demandées et qualification progressive

- **WHEN** seuls Debian et Docker disposent de preuves de recette
- **THEN** Windows et les autres profils restent demandés et explicitement non qualifiés

### Requirement: Indépendance d'installation et autorité applicative

Les binaires PA MUST pouvoir être installés sans PBO, PFO ou navigateur locaux et joindre un PBO distant autorisé. PA MUST NOT embarquer Django/PostgreSQL comme autorité métier, accéder directement aux tables métier ni confirmer une mutation de sa propre initiative. PBO/Django MUST conserver les décisions applicatives et PostgreSQL leur persistance de référence.

#### Scenario: Indépendance d'installation et autorité applicative

- **WHEN** PA est installé seul sur une cible
- **THEN** ses opérations restent liées à leurs mandats et à l'autorité PBO compétente

### Requirement: Composition au build et catalogue fermé

Chaque capacité PA MUST déclarer identité, version, propriétaire, contrats, dépendances, configuration, sécurité et permissions selon le modèle de composants. La composition initiale MUST se faire au build ; instructions et mandats MUST sélectionner seulement des opérations déjà livrées. PA MUST NOT télécharger ou charger implicitement du code, évaluer du Python ou ouvrir un shell privilégié à partir d'une instruction réseau.

#### Scenario: Composition au build et catalogue fermé

- **WHEN** une instruction demande une opération absente du catalogue livré
- **THEN** elle est refusée sans téléchargement ou exécution de code arbitraire

### Requirement: Démarrage système et session borné

system-daemon et session-daemon MUST avoir des délais indépendants, configurables et non négatifs, des préconditions et attentes maximales déclarées. pzt-daemon MUST être lancé sans ces délais au démarrage du système ou du conteneur ; il MUST exécuter PZT seulement s'il est activé/configuré, sinon se fermer. L'arrêt pendant un délai MUST annuler le lancement différé. Une mesure temporelle de démarrage MUST NOT tenir lieu de validité d'autorisation.

#### Scenario: Démarrage système et session borné

- **WHEN** le système s'arrête pendant le délai du démon système
- **THEN** ce lancement est annulé sans modifier la validité des mandats

### Requirement: Provisionnement distinct du canal de contrôle

Le provisionnement MUST établir configuration minimale, identité, ancrages et références de secrets avant le premier échange PBO–PA, avec états inspectables non provisionné, en cours, prêt ou échoué. L'origine et l'autorisation MUST être vérifiées ; le premier PBO rencontré MUST NOT être approuvé automatiquement. La reprise MUST éviter de dupliquer identité ou autorisation ; des fichiers de provisionnement MUST NOT devenir un canal continu hors PZT.

#### Scenario: Provisionnement distinct du canal de contrôle

- **WHEN** l'ancrage requis est absent au premier démarrage
- **THEN** les échanges dépendants restent bloqués avec un état de provisionnement explicite

### Requirement: Arrêt contrôlé et résultats réellement observés

Les traitements system-stop et session-stop MUST avoir un budget maximal, un ordre déclaré avec les démons et dépendances, et une protection contre les doublons. PZT MUST être conservé tant que des échanges nécessaires et autorisés restent possibles dans le budget d'arrêt. Panne électrique, arrêt forcé et perte du processus MUST NOT être présentés comme une fermeture exécutée ou un résultat livré.

#### Scenario: Arrêt contrôlé et résultats réellement observés

- **WHEN** le conteneur disparaît avant confirmation du traitement d'arrêt
- **THEN** le résultat reste incomplet ou inconnu et aucun succès n'est inventé

### Requirement: Isolation des sessions et des privilèges

Le binaire utilisateur MUST fonctionner avec l'identité et les droits de la session réelle, distincte du compte utilisateur ; sessions concurrentes MUST être isolées. Fermer une session MUST arrêter son démon sans affecter les autres ; verrouillage ou suspension MUST NOT valoir fermeture. Le démon système et le binaire PZT MUST conserver leurs comptes, clés et frontières déclarés, sans élévation implicite depuis une session.

#### Scenario: Isolation des sessions et des privilèges

- **WHEN** une session demande une clé ou un droit réservé au système
- **THEN** l'accès est refusé selon les contrôles applicables sans transfert de privilège

### Requirement: Contrat public des instructions et revalidation

Une instruction MUST identifier émetteur, acteur initial, exécuteur, opération/version, cible, plateforme, tenant/scope, paramètres typés/bornés, mandat, validité, fraîcheur, corrélation et idempotence lorsqu'applicables. PA MUST vérifier ces éléments à l'exécution, y compris après attente ou reprise. Une permission de lecture/surveillance MUST NOT accorder une reconfiguration ; un canal authentifié MUST NOT accorder un droit métier.

#### Scenario: Contrat public des instructions et revalidation

- **WHEN** une instruction admise expire avant son exécution
- **THEN** elle n'est pas exécutée sur la seule base de son admission passée

### Requirement: Plusieurs PBO et conflits explicites

Chaque relation PBO–PA MUST déclarer son périmètre et ses versions ; plusieurs connexions MUST NOT permettre l'administration libre d'une même ressource. Les autorités, délégations et priorités MUST être définies avant activation ; des commandes incompatibles MUST être bloquées sans règle du dernier message reçu. Les résultats, identités et configurations d'une relation MUST NOT être exposés à une autre sans accord explicite.

#### Scenario: Plusieurs PBO et conflits explicites

- **WHEN** deux instructions incompatibles ciblent la même ressource
- **THEN** le conflit est déclaré et aucune autorité n'est choisie implicitement

### Requirement: Exécution locale et états indéterminés

Chaque opération MUST déclarer préconditions, postconditions, effets, codes stables, caractère rejouable et stratégie d'erreur. Après crash entre effet et persistance du résultat, PA MUST vérifier la postcondition ou demander une intervention autorisée avant réexécution. Simulation, préparation, exécution et confirmation MUST rester distinctes ; une simulation MUST NOT produire de mutation.

#### Scenario: Exécution locale et états indéterminés

- **WHEN** un crash survient après un effet système avant son enregistrement
- **THEN** la reprise distingue l'effet inconnu et évite une réexécution aveugle

### Requirement: Plans sensibles et compensation préautorisée

Une reconfiguration sensible MUST utiliser un plan versionné, borné, autorisé et encore courant, avec confirmation ou assurance renforcée lorsque requise. Une compensation après perte de contrôle MUST rester dans le plan préautorisé, sans restaurer une permission révoquée ni ouvrir un canal hors PZT. Un plan obsolète ou hors mandat MUST NOT être appliqué.

#### Scenario: Plans sensibles et compensation préautorisée

- **WHEN** une modification coupe le canal de contrôle
- **THEN** l'état est diagnostiqué et seule une compensation encore autorisée peut être tentée

### Requirement: Configuration souhaitée et appliquée distinctes

PBO MUST conserver la configuration souhaitée et PA MUST rapporter version, résultat et état réellement appliqués. Validation de schéma, compatibilité, préconditions et concurrence MUST précéder l'application ; application partielle et conflit MUST être déclarés. Envoyé ou reçu MUST NOT être présenté comme appliqué ; un feature flag MUST NOT supprimer une capacité requise ni élargir un droit.

#### Scenario: Configuration souhaitée et appliquée distinctes

- **WHEN** PA a reçu une configuration mais son application échoue
- **THEN** PBO conserve la distinction souhaité/appliqué et affiche l'échec

### Requirement: Persistance technique locale bornée

Les seuls états techniques locaux nécessaires à l'exécution, déduplication, résultats en attente et reprise MUST avoir un propriétaire, un contrat de durabilité, des limites, une rétention, une protection et une stratégie de corruption/restauration déclarés. Ils MUST NOT devenir une source de vérité métier. Un stockage requis plein ou corrompu MUST bloquer les opérations sans preuve durable ; en conteneur il MUST NOT dépendre du filesystem éphémère.

#### Scenario: Persistance technique locale bornée

- **WHEN** l'état durable de reprise est corrompu
- **THEN** les traitements dépendants restent bloqués sans état remis à zéro implicitement

### Requirement: Continuité sans PBO et reprise locale PZT

Sans PBO joignable, PA MUST se limiter aux capacités explicitement provisionnées, éligibles et encore valides ; une décision en ligne indisponible MUST bloquer l'action concernée. Diagnostic et reprise depuis PBO MUST passer par PZT, y compris local. Si PZT est entièrement indisponible, une réparation interne/opérateur MUST suivre sa procédure distincte, sans canal de substitution PBO–PA.

#### Scenario: Continuité sans PBO et reprise locale PZT

- **WHEN** PZT est entièrement arrêté
- **THEN** PBO ne reçoit aucun canal de contrôle local de contournement

### Requirement: Observation des dérives et corrections distinctes

PA MUST distinguer constat de dérive et correction. La surveillance MUST produire des états et diagnostics autorisés ; une correction MUST disposer de sa politique et de son mandat propres. Référentiels, fréquences, budgets et catalogue de corrections MUST être spécifiés et qualifiés avant activation, sans valeurs implicites.

#### Scenario: Observation des dérives et corrections distinctes

- **WHEN** une dérive est détectée sans mandat de correction
- **THEN** le constat est rapporté sans engager de modification non autorisée

### Requirement: Supervision PBO et collecte PA

Configuration, visualisation, supervision et monitoring PZT MUST toujours relever de PBO. PA MUST collecter et remonter les mesures et états réellement observés via PZT. Vivacité, disponibilité, démarrage, diagnostic et résultat métier MUST rester distincts ; une mesure ancienne MUST être datée et MUST NOT devenir un état courant par absence de nouvelle information.

#### Scenario: Supervision PBO et collecte PA

- **WHEN** la collecte est interrompue alors que le dernier état était sain
- **THEN** PBO signale les mesures périmées et ne déduit pas une disponibilité actuelle

### Requirement: Maintenance et quarantaine sans nouveaux droits

Les profils MUST déclarer états normal, surveillance seule, maintenance et quarantaine avec portées, actions permises/interdites et conditions de sortie. Drainage et arrêt MUST être bornés ; les nouvelles modifications incompatibles MUST être refusées. Ces états MUST NOT accorder de droit supplémentaire ni supprimer les contrôles applicables.

#### Scenario: Maintenance et quarantaine sans nouveaux droits

- **WHEN** la cible entre en maintenance pendant une opération
- **THEN** son drainage suit le contrat et les nouvelles mutations incompatibles sont refusées

### Requirement: Audit, confidentialité et exception Super Admin

PA et PBO MUST appliquer les obligations ordinaires de security, authorization et audit sous réserve de l'exception unique définie par initial-administration. Une requête Super Admin MUST conserver acteur initial et tenant explicitement accordé, sans credentials ou exception transférés à un worker/autre compte. Audit ou contrôle dérogé/non réalisé MUST NOT être présenté comme effectué ; profils structurels et contrats d'exécution MUST rester distincts.

#### Scenario: Audit, confidentialité et exception Super Admin

- **WHEN** le Super Admin utilise une dérogation d'audit dans son tenant accordé
- **THEN** l'audit absent n'est pas revendiqué comme réalisé et aucun autre compte n'hérite de la dérogation

### Requirement: Interfaces et messages cohérents

Les interfaces CLI et les contributions PBO/PFO MUST utiliser les contrats publics, des erreurs stables et les traductions des composants propriétaires ; codes et champs MUST rester non localisés. PFO MUST adresser ses demandes à PBO ; aucune liaison directe PFO–PA MUST être introduite par ces spécifications. Les interfaces MUST respecter accessibilité, thèmes et confidentialité déclarés.

#### Scenario: Interfaces et messages cohérents

- **WHEN** une action est présentée dans PFO
- **THEN** son autorisation reste évaluée par PBO avant transmission éventuelle à PA via PZT

### Requirement: Qualification des quatre binaires et de la composition

Chaque binaire livré MUST disposer de preuves correspondant à son OS/CPU, runtime embarqué, dépendances/ABI, modes et composition. Les critères R01–R68 du cadrage MUST être couverts par une matrice de recette ; les cas de session MUST être déclarés non applicables à Docker et leur absence contrôlée. Une compilation réussie MUST NOT tenir lieu de recette ni prouver un gain CPU/RAM.

#### Scenario: Qualification des quatre binaires et de la composition

- **WHEN** une compilation réussit sans recette Windows
- **THEN** aucune compatibilité Windows qualifiée n'est annoncée

### Requirement: Publications locales expérimentales et sécurité de distribution

La première livraison envisagée MUST rester locale sur canal expérimental, avec capacités, versions, limites et preuves déclarées. Elle MUST satisfaire artifact-publication, notamment signature, provenance, inventaire, intégrité, immuabilité et révocation ; locale ou expérimentale MUST NOT dispenser de ces garanties ni autoriser une clé secrète dans un artefact. La présente formalisation MUST NOT construire, signer ou publier un artefact.

#### Scenario: Publications locales expérimentales et sécurité de distribution

- **WHEN** un artefact local expérimental ne dispose pas d'une signature admissible
- **THEN** il ne peut pas être déclaré publiable ou installable conformément à artifact-publication

### Requirement: Paramètres ouverts et absence d'implémentation implicite

Les noms/versions de paquets et exécutables, bibliothèques, formats non arrêtés, topologies, comptes, quotas manquants et seuils à mesurer MUST rester explicitement ouverts jusqu'à décision ou qualification appropriée. Les versions de Nuitka/Cython et leur graphe MUST être qualifiés avant installation. La rédaction de ces spécifications MUST NOT être présentée comme du code, un test runtime, une plateforme supportée ou un artefact livré.

#### Scenario: Paramètres ouverts et absence d'implémentation implicite

- **WHEN** seules les spécifications sont déclarées
- **THEN** les états d'implémentation, qualification et publication restent explicitement non réalisés

### Requirement: Matrice de recette PA complète par profil

La recette PA MUST couvrir R01–R68 selon les fonctions livrées. R05–R08 et R30
MUST être justifiés non applicables à Docker ; l’absence du binaire utilisateur
MUST y être contrôlée. Chaque résultat MUST être déclaré exécuté/réussi,
exécuté/échoué, non exécuté, non disponible ou non applicable justifié,
sans test implicitement réalisé.

##### Critères normatifs R01–R68

| Référence | Scénario à vérifier | Résultat attendu |
| --- | --- | --- |
| R01 | Installation sans Pixs Frontoffice ni Pixs Backoffice | Les binaires PA fonctionnent avec leurs seules dépendances déclarées et joint une instance distante autorisée via PZT. |
| R02 | Démarrage du système ou du conteneur | `system-start` exécute les opérations déclarées et restitue leur résultat. |
| R03 | Arrêt contrôlé du système ou du conteneur | `system-stop` réalise ou interrompt explicitement les opérations dans le budget prévu. |
| R04 | Démarrage différé système | `system-daemon` respecte le délai, les préconditions et l'annulation en cas d'arrêt anticipé. |
| R05 | Ouverture de session graphique | `session-start` utilise l'identité et les droits de la session concernée. |
| R06 | Fermeture contrôlée de session graphique | `session-stop` produit un résultat borné et le démon concerné s'arrête. |
| R07 | Démarrage différé de session | `session-daemon` respecte le délai et ne survit pas à la fermeture de sa session. |
| R08 | Sessions concurrentes et déclenchements répétés | Les sessions restent isolées et les invocations répétées ne produisent pas de doublon incontrôlé. |
| R09 | Requête utilisateur exigeant des droits système | L'élévation implicite est refusée et diagnostiquée. |
| R10 | Agent dans un conteneur | Aucun accès à l'hôte n'est possible au-delà du périmètre explicitement accordé. |
| R11 | Identité, autorisation ou fraîcheur invalide | L'action concernée est refusée sans repli permissif. |
| R12 | Relations avec plusieurs instances Pixs | Les périmètres sont isolés et les instructions contradictoires sont bloquées selon la politique. |
| R13 | Coupure réseau, expiration ou révocation | Les opérations non autorisées cessent et seules les capacités locales explicitement éligibles restent possibles. |
| R14 | Rejeu, crash et redémarrage | La reprise respecte l'idempotence et distingue les effets dont le résultat est inconnu. |
| R15 | Dérive détectée | Un constat traçable est produit ; aucune correction non autorisée n'est engagée. |
| R16 | Configuration ou contrat incompatible | La capacité concernée reste inactive avec un diagnostic exploitable. |
| R17 | Binaire compilé sur une cible supportée | Les modes livrés par les quatre binaires conservent leur comportement et les performances respectent les budgets validés ; dans Docker, les modes de session sont explicitement exclus. |
| R18 | Inspection des artefacts et diagnostics | Aucun secret ni donnée personnelle interdite n'est présent. |
| R19 | Arrêt forcé ou disparition brutale de session | L'agent ne prétend pas avoir exécuté un traitement de fermeture non observé. |
| R20 | Mise à niveau du composant | Configuration et reprise compatibles ; A10f : références signées/versionnées, transition bornée, ensembles cohérents, retrait à échéance, refus du rejeu et des références révoquées, nouvelle preuve après modification des mesures ; rollback uniquement autorisé par la politique courante. |
| R21 | PBO et PA sur le même hôte ou dans le même conteneur | Tous leurs échanges, dans les deux sens, passent par PZT avec ses contrôles et son chiffrement. |
| R22 | Tentative de communication PBO–PA hors PZT | Le canal de contournement est refusé, même si les permissions locales permettraient son utilisation. |
| R23 | Canal PZT requis indisponible, non initialisé ou preuves invalides | La communication PBO–PA concernée est bloquée sans repli hors PZT, y compris pendant l'amorçage. |
| R24 | Premier démarrage sans PBO joignable | PA se limite aux capacités et opérations locales explicitement provisionnées, éligibles et encore autorisées. |
| R25 | Réseau distant indisponible et profil local PZT disponible | Le diagnostic et la reprise depuis PBO utilisent PZT avec les mêmes contrôles ; une décision en ligne indisponible bloque l'action qui l'exige. |
| R26 | PZT entièrement arrêté | Aucun échange PBO–PA n'est possible ; une éventuelle réparation système suit la procédure opérateur distincte et auditée. |
| R27 | Profil de pilotage PZT sans module officiel requis | La composition PBO est refusée ; une extension ne peut ni retirer le socle ni affaiblir ses contrôles. |
| R28 | Capacité incompatible ou ajout de code demandé par message | L'activation ou le chargement est refusé ; seules les opérations livrées par une composition vérifiée sont sélectionnables. |
| R29 | Mandat hors cible, périmètre, validité ou obligations | L'instruction est refusée au moment de l'exécution, même sur un canal PZT valide et après attente ou reprise. |
| R30 | Instance de session demandant un secret ou un droit système | L'accès est refusé ; les identités, clés et privilèges des fonctions séparées restent isolés. |
| R31 | Stockage technique plein, indisponible ou corrompu | Les opérations dont les garanties durables ne peuvent être tenues sont bloquées et l'écart est diagnostiqué sans perte silencieuse. |
| R32 | Crash après effet système mais avant enregistrement du résultat | L'état indéterminé conduit à une vérification de postcondition ou une intervention autorisée, sans réexécution aveugle. |
| R33 | Simulation ou plan expiré ou devenu obsolète | La simulation reste sans mutation ; l'application d'un plan invalide est refusée jusqu'à nouvelle validation. |
| R34 | Reconfiguration réseau interrompant le contrôle | L'échec est diagnostiqué et la compensation suit le plan préautorisé, sans réactiver un droit révoqué ni ouvrir un canal hors PZT. |
| R35 | Restauration d'un ancien état technique | Les droits révoqués et mandats expirés restent refusés et les préconditions sont réévaluées avant reprise. |
| R36 | Maintenance, surveillance seule ou quarantaine | Les actions interdites restent bloquées, le drainage est borné et la sortie contrôle les préconditions avant réactivation. |
| R37 | Action privilégiée soumise à une obligation d'audit | L'acteur, l'exécuteur, le mandat, la cible et le résultat sont corrélés ; une obligation non satisfaite empêche l'autorisation. |
| R38 | Changement de langue et appel non interactif | Les messages humains sont traduits tandis que codes de sortie, codes d'erreur et structures contractuelles restent stables. |
| R39 | Profil de déploiement qualifié | Les comptes, signaux, persistance, réseaux et limites correspondent au profil ; le conteneur commun ne lance pas implicitement plusieurs rôles PBO. |
| R40 | Versions PBO–PA–PZT incompatibles | La capacité est bloquée ou suit la migration déclarée, sans compatibilité déduite du seul numéro de version. |
| R41 | Binaire sur une cible OS/CPU déclarée | Le runtime embarqué et les bibliothèques natives sont qualifiés et les modes disponibles passent leurs tests applicables. |
| R42 | Artefact altéré ou révoqué | La vérification de signature, d'intégrité, de confiance et de provenance empêche son activation. |
| R43 | Arrêt contrôlé pendant une opération et livraison du résultat | Le séquencement conserve PZT dans le budget prévu et distingue exécution, résultat en attente et confirmation par PBO. |
| R44 | Configuration reçue, concurrente ou partiellement appliquée | L'état souhaité reste distinct de l'état appliqué ; les conflits et interruptions sont explicites et aucune réussite n'est déduite de la réception. |
| R45 | Référence temporelle d'autorisation non fiable | L'opération concernée est refusée ; les délais monotones ne servent pas de preuve de validité du mandat. |
| R46 | Démarrage du système ou du conteneur avec `pzt-daemon` | Le mode démarre sans délai et assure la convergence et la réconciliation de PZT lorsque celui-ci est activé et configuré sur ce PA ; sinon, il se ferme. |
| R47 | Backend WireGuard du profil retenu | PA pilote le backend qualifié, sans réimplémenter la cryptographie ; dépendances et privilèges correspondent au profil. |
| R48 | Carte ou delta altéré, périmé, hors destinataire, dupliqué ou de base incompatible ; séquence manquante et reprise | La configuration invalide est refusée ; un doublon ne produit aucun double effet et ne prolonge aucune permission. Une base incompatible, un trou ou un historique hors rétention déclenche un état complet vérifié. La réconciliation contrôle l'état effectivement appliqué et ne réintroduit aucun droit expiré ou retiré ; les objectifs A05b restent opposables. |
| R49 | AllowedIPs ou route présents sans permission du service | Les adapters nftables Linux et Windows Filtering Platform Windows appliquent les politiques PZT du profil et vérifient leur état ; les flux non autorisés sont bloqués, le tunnel ne donne pas accès aux services voisins et les ressources gérées restent distinctes des règles de l’opérateur. |
| R50 | PBO, sessions et modes ponctuels utilisant le même PA | Le propriétaire des ressources réseau évite les écritures concurrentes ; aucune session ne reçoit de clé ou privilège système. |
| R51 | Admission automatisée, demande hors mandat ou preuves invalides, jeton expiré/révoqué/consommé, concurrence et reprise après crash | A11a : identité, contexte et preuves A10 vérifiés, aucune gestion ou exposition métier avant admission, arbitrage opérateur hors mandat sans dispense de preuve ; A11b : jeton à usage unique par instance, engagement atomique et reprise sans double identité ni consommation ; nouvelles admissions invalides refusées, secrets non exposés et retrait des pairs existants distinct. |
| R52 | Échéance d'un pair éphémère encore présent, renouvellement concurrent, fin de charge, partition et restauration | A11c : échéance finie sans report sur présence ; renouvellement autorisé avant échéance avec contrôles courants, blocage/retrait sans résurrection après échéance ou retrait engagé ; nettoyage par génération avec audit/tombstones et suivi des échecs, aucune suppression de VM/conteneur/volume ; nouvelle admission avec nouveau jeton et preuves après retrait. |
| R53 | Connectivité ICE/STUN, relais QUIC DATAGRAM et secours WSS | Signalisation protégée, sondes encadrées, candidats et mapping réel WireGuard vérifiés ; direct puis QUIC DATAGRAM et secours WSS selon la politique autorisée, sans contournement ni prolongation des droits. Support DATAGRAM, tailles, MTU, pertes, reprise et backends qualifiés ; le relais ne déchiffre pas WireGuard. Sans chemin admis, échec explicite. |
| R54 | Changement d'endpoint ou de contexte réseau | L'identité demeure stable et les conditions de posture concernées sont réévaluées selon le profil. |
| R55 | Activation/désactivation IPv6 PZT, DNS administré et chevauchement d'adresses ou de routes | Le réglage unique retire les ressources IPv6 PZT, les AAAA propres à PZT et les échanges/endpoints IPv6 WireGuard/TLS concernés sans désactiver l'IPv6 hôte. Les sessions et états souhaité/appliqué sont vérifiés ; aucune réussite n'est annoncée sans preuve, aucun repli hors PZT ni droit périmé restauré. Les familles actives appliquent les garanties PZT ; les conflits bloquent le périmètre concerné sans écraser la configuration de l'hôte sans mandat. |
| R56 | DNS Pixs via module essentiel PBO : publication, consultation, panne et destination inattendue | Les contrats publics et droits distincts de publication/consultation sont vérifiés pour chaque contexte PA ; retraits et caches gérés respectent la validité, avec aucune fuite par repli public en panne. Dépendance essentielle, état appliqué et continuité sans PBO sont qualifiés selon le profil. Une résolution DNS seule n'accorde aucun accès ; une destination dont l'identité ou la clé diffère de celle attendue est refusée. |
| R57 | Posture modifiée, reconnexion PA, preuve TPM absente, expirée ou rejouée | A10c : preuve fraîche à chaque connexion/reconnexion puis sur événement ou expiration, bornée par génération/contexte ; A10e : PA chargé, runtime, dépendances, collecteur et paramètres requis mesurés par chaîne qualifiée, journaux et références vérifiés. Contrôles des services conservés ; preuves manquantes/incohérentes refusées, sans simple déclaration ni renouvellement implicite des droits. |
| R58 | Crash ou blocage de PA avec tunnel et flux déjà actifs dans le noyau | La protection indépendante ferme les accès en 10 secondes maximum, détection et action comprises, sans prolonger une permission ni en créer ; une échéance antérieure reste prioritaire. Une révocation connue n'attend pas l'expiration et prend effet en 5 secondes maximum si PA est joignable sur le chemin de contrôle qualifié. La reprise vérifie l'état courant avant réactivation ; les objectifs A05b doivent être démontrés sur chaque profil. |
| R59 | Rotation d'une clé WireGuard | Identité Pixs stable et certificat X.509 encore valide conservés ; nouvelle liaison séparée JWS vérifiée, incohérences ou signatures invalides refusées et ancienne liaison retirée conformément à la politique, sans renouvellement implicite des droits. |
| R60 | Ressource sans PA derrière une passerelle déclarée | La permission ne donne pas accès aux services locaux de la passerelle ; le dernier segment respecte la protection du profil. |
| R61 | Basculement du profil passerelle ultérieur sans NAT | Une seule passerelle est active par périmètre de routage cohérent ; sélection déterministe, mandat valide, retours convergents et retrait des décisions obsolètes sont vérifiés. Le profil qualifie conservation des sources, sessions et traçabilité ; aucune continuité non démontrée ni prolongation des droits n'est annoncée. |
| R62 | Démarrage à froid, admission, renouvellement et basculement sans accès à l'éditeur | Les services PZT exploités par l'opérateur suffisent lorsque les dépendances déclarées du profil sont disponibles. |
| R63 | TLS d'amorçage A02 et TLS mutuel local A03 validés | L'amorçage vérifie l'autorité à partir de l'ancrage préalable et refuse l'admission si les preuves requises sont invalides ; aucun accès métier avant admission. Le profil local sur le même hôte d'exécution vérifie les deux identités et les contrôles PZT ; identité, permission ou preuve requise invalides bloquent l'échange sans repli hors PZT. Endpoints, isolation et frontières des VM/conteneurs sont qualifiés par profil. |
| R64 | Propriété, réconciliation et retrait des ressources réseau | pzt-daemon gère les ressources PZT de son périmètre ; les six autres modes soumettent leurs demandes autorisées sans écritures directes, y compris après indisponibilité du propriétaire. PA ne retire que les ressources dont il possède la gestion ; une application partielle est rapportée sans fenêtre permissive. |
| R65 | Handshake récent et service indisponible | Le diagnostic distingue transport, joignabilité, readiness, autorisation et résultat métier. |
| R66 | PA Linux et Windows sur machines physiques et virtuelles | Chaque cible demandée dispose d'un backend, d'adapters système/session, de réseau, DNS et filtrage qualifiés ; aucune exclusion n'est déduite de l'environnement Debian du projet. |
| R67 | PA Docker et LXC sous Proxmox | Le profil vérifie le noyau effectif, le placement, les droits minimaux et l'isolation ; aucun repli en espace utilisateur ne suppose des privilèges absents. |
| R68 | Snapshot, clone, restauration ou migration d'une VM ou d'un conteneur | Les identités, liaisons de clés et preuves TPM/vTPM sont réévaluées ; aucun accès ni identité clonée n'est accepté implicitement. |

#### Scenario: Profil Docker sans recette de session

- **WHEN** la matrice de recette est produite pour l’image Docker
- **THEN** les cas utilisateur exclus sont justifiés non applicables et l’absence du binaire est contrôlée
