# zt-dns-dhcp Specification

## Purpose

DZT exécute DNS IPv4/IPv6 et DHCPv4/v6, avec configuration de référence commune et responsabilités PA/PZT séparées.

Cible documentaire du cadrage validé du 31 octobre 2026 (PROJECT.md §45, TECHNICAL.md §46 et BUILD.md §49), sans disponibilité fonctionnelle déduite.

## Requirements

### Requirement: DZT obligatoire et base commune indépendante

Chaque ZT MUST disposer d'au moins un DZT exécuté par PZT. BIND 9 MUST fournir DNS v4/v6 et ISC DHCP MUST fournir DHCPv4 et DHCPv6 par processus distincts. Une PG DZT MUST conserver la référence commune à ces fonctions, indépendante de CZT, PKIZT et PBO, avec réplication synchrone et primaire unique selon zt-controller et brick-redundancy.

#### Scenario: Plusieurs DZT

- **WHEN** une réplique DZT est ajoutée
- **THEN** elle rejoint le même référentiel logique sans source de configuration concurrente.

### Requirement: Préparation et mise à jour PA configuration PZT

PA MUST assurer préparation, installation, maintenance système et mise à jour des logiciels DNS/DHCP. PZT/DZT MUST assurer configuration et maintenance logicielle du fonctionnement, validation, application et contrôle des services. PBO MUST administrer séparément les périmètres. Ces interventions MUST être coordonnées et leurs résultats distingués.

#### Scenario: Mise à jour BIND

- **WHEN** PA termine une mise à jour autorisée
- **THEN** DZT revalide la compatibilité, réapplique si nécessaire la configuration et vérifie le fonctionnement avant succès du service.

### Requirement: Configuration entièrement régénérable

DZT MUST produire et pouvoir rejouer intégralement les configurations depuis une révision cohérente de sa PG, sans traiter les modifications manuelles des fichiers comme vérité. Baux, mises à jour dynamiques, journaux nécessaires et clés DNSSEC MUST être préservés par des contrats de durabilité/reprise explicites.

#### Scenario: Régénération après panne

- **WHEN** les fichiers générés sont reconstruits
- **THEN** l’état natif durable n’est ni effacé ni supposé recréé par la configuration seule.

### Requirement: Vues dédiées et indépendantes

BIND MUST permettre au moins une vue dédiée au ZT, plusieurs vues ZT et des vues hors ZT administrées séparément par PBO. Plusieurs DZT MAY être actifs et servir une même vue pour la redondance ; les droits, zones, visibilité et délégations MUST rester propres au périmètre.

#### Scenario: Vue externe au ZT

- **WHEN** une vue hors ZT partage un BIND avec les vues ZT
- **THEN** elle conserve ses politiques et ne devient pas accessible aux acteurs ZT par cohébergement.

### Requirement: Continuité par vue

Chaque vue MUST déclarer ses conditions et limites de continuité/fraîcheur. Les données déjà appliquées MAY être servies dans ces limites ; une expiration MUST arrêter le service concerné, sans nouvelle modification ou validité déduite de l'indisponibilité. Les autres vues encore admissibles MUST rester indépendantes.

#### Scenario: Contrôle indisponible

- **WHEN** la validité d’une vue expire tandis qu’une autre reste admissible
- **THEN** la première cesse d’être servie sans arrêt injustifié de la seconde.

### Requirement: Domaine technique et noms stables

Chaque ZT MUST déclarer à l'initialisation au moins un domaine DNS dédié. Les cibles MUST avoir des noms techniques stables et MAY posséder des alias lisibles administrés depuis PBO. Un changement d'adresse ou d'alias MUST NOT changer l'identité canonique. Le partage avec les Domaines MUST respecter pixs-domains.

#### Scenario: Alias renommé

- **WHEN** un alias lisible est modifié
- **THEN** la cible conserve son identité et les politiques vérifient toujours la destination attendue.

### Requirement: Activation DHCP indépendante et désactivée par défaut

DHCPv4 et DHCPv6 MUST être désactivés par défaut et activés explicitement, indépendamment par réseau, depuis PBO. La présence obligatoire du DZT MUST NOT démarrer l'attribution DHCP sur un réseau non autorisé.

#### Scenario: DZT initialisé

- **WHEN** un DZT est initialisé sans réseau DHCP activé
- **THEN** aucun bail DHCPv4 ou DHCPv6 n’est attribué.

### Requirement: Adressage coordonné et propriétaire par pool

CZT MUST gérer l'adressage des pairs PZT ; DZT MUST gérer les réseaux DHCP avec coordination des préfixes/pools. Un pool MUST avoir un seul DZT autorisé à attribuer ou renouveler ses baux à un instant donné ; les pools MAY être répartis. La reprise MUST vérifier les baux et exclure l'ancien propriétaire.

#### Scenario: Reprise sans baux fiables

- **WHEN** un secours ne peut vérifier l’état des baux du pool
- **THEN** il ne devient pas allocateur actif sur la seule panne de l’ancien DZT.

### Requirement: Liaison DHCP DNS configurable

Le lien DHCP–DNS MUST pouvoir être automatique et configurable par périmètre. Le bail et son état de publication DNS MUST être suivis séparément, avec idempotence, retrait et reprise selon leurs politiques ; la réussite de l'un MUST NOT prouver celle de l'autre.

#### Scenario: Publication échouée

- **WHEN** un bail est accordé mais sa publication DNS échoue
- **THEN** les deux états sont visibles et la reprise ne réattribue pas aveuglément le bail.

### Requirement: Zones administrables centralement ou par délégation

Dans un ZT partagé, les zones MUST pouvoir être administrées centralement ou déléguées selon des habilitations explicites. Une délégation MUST préciser ses zones et actions et MUST NOT autoriser une modification des zones des autres Domaines.

#### Scenario: Délégué de zone

- **WHEN** un administrateur d’association.pixs.fr tente de modifier recherche.pixs.fr
- **THEN** la modification est refusée sans délégation correspondante.

### Requirement: Projections DNS autorisées et bornées

La résolution entre ZT approuvés MUST exiger une permission DNS précisant bénéficiaires, noms/zones et sens. Le destinataire MUST conserver une projection séparée, versionnée, liée à son origine et à une échéance renouvelable seulement par autorisation de l'origine. TTL MUST être bornés par cette échéance et révocations connues MUST être appliquées.

#### Scenario: Projection expirée

- **WHEN** le propriétaire reste injoignable après échéance de sa projection
- **THEN** DZT cesse de servir ces données sans prolongation par cache ou TTL.

### Requirement: Notifications réconciliation et retransmission DNS

La synchronisation MUST utiliser notifications, réconciliation et contrôle périodique complémentaire, avec état complet si une révision manque. La retransmission MAY être autorisée explicitement si toute la chaîne conserve origine, portée, restrictions, profondeur et échéances. Une notification MUST NOT suffire à prouver mise à jour ou renouvellement.

#### Scenario: Projection retransmise

- **WHEN** un intermédiaire est habilité à retransmettre un sous-ensemble
- **THEN** il préserve l’origine et ne prolonge aucune limite du propriétaire.
