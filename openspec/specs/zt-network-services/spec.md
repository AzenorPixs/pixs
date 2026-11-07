# zt-network-services Specification

## Purpose

Les rôles PZT de signalisation, découverte, relais, passerelle, sortie et publication ont des périmètres et états distincts.

Cible documentaire du cadrage validé du 31 octobre 2026 (PROJECT.md §45, TECHNICAL.md §46 et BUILD.md §49), sans disponibilité fonctionnelle déduite.

## Requirements

### Requirement: SZT obligatoire et actifs coopérants

Chaque ZT MUST disposer d'au moins un SZT pour mettre les pairs en relation. Plusieurs SZT actifs MUST pouvoir coopérer pour des pairs raccordés à des SZT différents. L'état de présence/négociation MUST être temporaire en RAM, reconstruit au démarrage, sans PG propre.

#### Scenario: Pairs sur deux SZT

- **WHEN** deux pairs autorisés sont raccordés à des SZT différents
- **THEN** la signalisation permet leur mise en relation sans créer une nouvelle permission.

### Requirement: RZT obligatoire et relais commun

Chaque ZT MUST disposer d'au moins un RZT relayant le trafic chiffré. Plusieurs RZT MAY être actifs et les pairs MUST pouvoir choisir un relais commun admissible. Connexions, associations et tampons MUST rester temporaires en RAM sans PG propre ; la panne MUST permettre une reconnexion autorisée sans promettre la conservation transparente des sessions.

#### Scenario: Panne du relais

- **WHEN** le RZT d’une communication tombe
- **THEN** les pairs rétablissent un chemin admissible et les interruptions sont rapportées sans succès fictif.

### Requirement: STZT obligatoire sans primaire

Chaque ZT MUST disposer d'au moins un STZT pour la découverte des adresses et ports observés. Plusieurs STZT actifs indépendants MUST être possibles, avec état temporaire RAM sans PG propre ni réplication de cet état.

#### Scenario: STZT redémarré

- **WHEN** un STZT perd ses observations RAM
- **THEN** les pairs peuvent refaire une découverte sans réadmission d’identité ni remise à zéro des autorisations.

### Requirement: Identités durables et audit des rôles RAM

L'absence de PG propre MUST NOT supprimer les identités, références de démarrage et clés protégées des PZT ni l'audit durable applicable. Les politiques MUST rester sous CZT et l'état temporaire MUST NOT devenir source d'autorisation indépendante.

#### Scenario: Rôle RAM redémarré

- **WHEN** SZT ou RZT reconstruit son état
- **THEN** il vérifie les autorisations courantes sans inventer de droits à partir des anciennes connexions.

### Requirement: GZT facultatif et périmètre de routage

GZT MUST être optionnel et désactivé par défaut, exécuté par PZT pour les destinations sans PZT explicitement autorisées. Sa référence MUST être dans CZT et son état opérationnel en RAM sans PG propre. Un GZT actif unique par périmètre MUST être assuré avec répartition des périmètres et secours à bascule automatique encadrée.

#### Scenario: Passerelle de secours

- **WHEN** un GZT est remplacé pour son périmètre
- **THEN** le secours n’achemine qu’après vérification de son autorité et des conditions de reprise.

### Requirement: Traduction source explicite

La traduction d'adresse source GZT MUST être désactivée par défaut et activable explicitement par périmètre. Sans traduction, les routes de retour MUST être vérifiées ; le dernier segment hors PZT MUST disposer des protections exigées par le périmètre.

#### Scenario: Route retour absente

- **WHEN** une ressource sans PZT n’a pas de retour autorisé vers la source conservée
- **THEN** l’accès n’est pas déclaré fonctionnel et NAT n’est pas activé implicitement.

### Requirement: EZT distinct facultatif et groupes

EZT MUST être un rôle distinct optionnel et désactivé par défaut, avec référence CZT et état RAM sans PG propre. Les politiques de sortie MUST pouvoir désigner des groupes avec niveaux de priorité et membres explicitement autorisés, y compris externes par approbation sans changement d'appartenance.

#### Scenario: EZT externe

- **WHEN** un groupe référence un EZT d’un autre ZT
- **THEN** son inclusion et son usage exigent les autorisations applicables sans le rendre membre local.

### Requirement: Répartition et continuité EZT

Les nouvelles connexions MUST être réparties entre les EZT admissibles du meilleur niveau disponible, avec poids configurables égaux par défaut. Chaque connexion MUST conserver son EZT tant que possible ; retour au préféré MUST être configurable avec maintien des connexions par défaut. L’absence de membre utilisable MUST conduire au blocage, sans sortie directe implicite.

#### Scenario: Groupe indisponible

- **WHEN** aucun EZT du groupe autorisé n’est utilisable
- **THEN** le trafic concerné reste bloqué sans utiliser une sortie non autorisée.

### Requirement: Santé par chemin et famille IP

Les groupes EZT MUST avoir critères de santé configurables par chemin et famille IP, avec temporisations d'exclusion et réadmission. La santé IPv4 MUST NOT suffire à qualifier le chemin IPv6 ni un simple processus vivant à qualifier la sortie.

#### Scenario: Sortie IPv6 rompue

- **WHEN** un EZT fonctionne en IPv4 mais échoue aux critères IPv6
- **THEN** son admissibilité IPv6 est traitée séparément.

### Requirement: RPZT facultatif et actifs multiples

RPZT MUST publier les services HTTP/HTTPS/WebSocket explicitement autorisés, être optionnel et désactivé par défaut, avec référence CZT et RAM sans PG propre. Plusieurs RPZT MAY être actifs pour une publication ; l'orientation des clients et ses effets MUST être qualifiés.

#### Scenario: Deux RPZT

- **WHEN** deux exécutants portent une publication
- **THEN** la présence des deux ne prouve pas à elle seule une orientation ou bascule fonctionnelle.

### Requirement: Authentification au service cible

RPZT MUST assurer publication, acheminement et restrictions techniques sans authentifier les utilisateurs. Le service cible MUST assurer l'authentification et les droits applicatifs par défaut ; une publication publique MUST être déclarée et autorisée explicitement.

#### Scenario: Service public non déclaré

- **WHEN** une publication vise un service sans authentification sans autorisation publique
- **THEN** elle n’est pas admise comme publication protégée par le seul RPZT.

### Requirement: TLS par publication et distribution PKIZT

Chaque publication MUST choisir terminaison TLS au RPZT ou passage chiffré jusqu'au service. En terminaison, PKIZT MUST assurer le cycle des certificats et la remise ciblée/protégée selon zt-pki. Un mode TLS MUST NOT créer une responsabilité d'authentification utilisateur au RPZT.

#### Scenario: TLS passthrough

- **WHEN** une publication transmet TLS jusqu’au service
- **THEN** le service termine TLS et RPZT ne prétend pas authentifier l’utilisateur.
