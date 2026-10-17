# Références normatives — PA08

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 29 | [Plateformes demandées et qualification progressive](../../specs/pixs-agent/spec.md#L29) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 200 | [Qualification des quatre binaires et de la composition](../../specs/pixs-agent/spec.md#L200) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 227 | [Matrice de recette PA complète par profil](../../specs/pixs-agent/spec.md#L227) | ND | CANDIDAT_PROFIL_PA |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--aafe7868a8

Source : `openspec/specs/pixs-agent/spec.md`, ligne 29. SHA-256 du bloc : `3b5eeb1e49d787e2e34f1fe0ce7bf4f3b08c0edf408e3b82429509ea4deeafdd`.

~~~~text
### Requirement: Plateformes demandées et qualification progressive

PA MUST conserver le périmètre Linux et Windows physiques, VM Linux et Windows, Docker et LXC sous Proxmox. La première qualification MUST cibler Debian/Linux et Docker locaux, puis les autres cibles ; une cible non qualifiée MUST être indiquée comme telle. Versions OS/CPU, topologies Docker dans VM ou LXC, droits, bureaux et vTPM MUST être déclarés par profil ; aucun support MUST être inféré du seul environnement de développement.

#### Scenario: Plateformes demandées et qualification progressive

- **WHEN** seuls Debian et Docker disposent de preuves de recette
- **THEN** Windows et les autres profils restent demandés et explicitement non qualifiés
~~~~

### Référence pixs-agent--f085ebdb93

Source : `openspec/specs/pixs-agent/spec.md`, ligne 200. SHA-256 du bloc : `26d78a1b75d4e99183b2154bde8d74d5c1b413ec713e2f783351de1547bc963d`.

~~~~text
### Requirement: Qualification des quatre binaires et de la composition

Chaque binaire livré MUST disposer de preuves correspondant à son OS/CPU, runtime embarqué, dépendances/ABI, modes et composition. Les critères R01–R68 du cadrage MUST être couverts par une matrice de recette ; les cas de session MUST être déclarés non applicables à Docker et leur absence contrôlée. Une compilation réussie MUST NOT tenir lieu de recette ni prouver un gain CPU/RAM.

#### Scenario: Qualification des quatre binaires et de la composition

- **WHEN** une compilation réussit sans recette Windows
- **THEN** aucune compatibilité Windows qualifiée n'est annoncée
~~~~

### Référence pixs-agent--0d84925f92

Source : `openspec/specs/pixs-agent/spec.md`, ligne 227. SHA-256 du bloc : `5a06181d0c5a07a5c9b6b95c555cd7f4d87812097b0ff7192ee4955a674b6447`.

~~~~text
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
~~~~

