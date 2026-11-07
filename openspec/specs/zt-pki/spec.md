# zt-pki Specification

## Purpose

PKIZT porte la certification opérationnelle du ZT, sa reprise de clés chiffrées et les certificats publics ACME.

Cible documentaire du cadrage validé du 31 octobre 2026 (PROJECT.md §45, TECHNICAL.md §46 et BUILD.md §49), sans disponibilité fonctionnelle déduite.

## Requirements

### Requirement: PKI propre et autorités multiples

Chaque ZT MUST disposer d'une PKI propre avec racine protégée hors ligne et au moins un PKIZT exécuté par PZT. Au moins une autorité opérationnelle MUST être initialisée ; plusieurs autorités MAY être ajoutées explicitement avec identité, clé, périmètre et politiques propres. Ajouter un membre ou une organisation MUST NOT créer implicitement une autorité.

#### Scenario: Deux Domaines partagent ZT

- **WHEN** le même ZT dessert deux Domaines
- **THEN** la PKI reste propre au ZT et les autorités supplémentaires sont créées explicitement selon les besoins.

### Requirement: PG propre et clés opérationnelles répliquées

PKIZT MUST conserver données et clés privées des autorités opérationnelles chiffrées dans une PG indépendante de PBO/CZT/DZT et bases Instance/Domaine, synchronisée selon les garanties PG zt-controller. Un PKIZT habilité MUST pouvoir reprendre la même autorité avec la même clé et son état courant d'émission/révocation.

#### Scenario: Reprise d’autorité

- **WHEN** le secours habilité reprend une autorité admissible
- **THEN** il retrouve la même clé protégée et l’état cohérent au lieu de créer systématiquement une nouvelle autorité.

### Requirement: Protection individualisée et habilitations séparées

Les enveloppes des clés chiffrées MUST être répliquées avec protection individualisée par PKIZT. Chaque PKIZT MUST conserver son propre moyen protégé de déverrouillage. Les droits d'administration, déchiffrement et émission MUST être séparés par autorité ; l'accès à PG MUST NOT suffire à utiliser une clé.

#### Scenario: Réplique non habilitée

- **WHEN** un membre possède la copie PG mais aucune habilitation de déchiffrement d’une autorité
- **THEN** il ne peut pas déverrouiller ou utiliser sa clé.

### Requirement: Émetteur unique et secours encadré

Une autorité MUST posséder un émetteur actif unique. L'activation du secours MAY être automatique sous politique/mandat, avec contrôles de reprise et exclusion de l'ancien émetteur. L'habilitation d'une autre autorité MUST NOT suffire et un ancien état restauré MUST être réconcilié avant émission.

#### Scenario: Ancien signataire non exclu

- **WHEN** le secours ne peut prouver que l’ancien émetteur est empêché d’émettre
- **THEN** la reprise d’autorité n’est pas engagée.

### Requirement: ACME public et génération de clés

PKIZT MUST pouvoir gérer des certificats publiquement reconnus via ACME selon les profils autorisés. La clé privée MUST être générée/protégée côté PKIZT ; compte ACME et clés de certificats MUST suivre leurs protections chiffrées et synchronisées. L'autorité publique MUST NOT être présentée comme fournisseur de la clé privée.

#### Scenario: Demande publique

- **WHEN** un profil autorise un certificat ACME
- **THEN** PKIZT conserve la clé privée et soumet la demande contenant la clé publique à signer.

### Requirement: Challenges et coordination ACME

DNS-01, HTTP-01 et TLS-ALPN-01 MUST être sélectionnables par profil avec orchestration autorisée DZT/RPZT. Un certificat MUST avoir un coordonnateur ACME actif unique et un état durable permettant la reprise sans double opération non maîtrisée.

#### Scenario: Deux coordonnateurs

- **WHEN** deux PKIZT tentent de gérer le même certificat
- **THEN** un seul est admissible à coordonner les opérations courantes.

### Requirement: Renouvellement anticipé et déploiement vérifié

Le renouvellement MUST être automatique et anticipé selon le profil, avec ARI lorsqu'il est disponible. La réussite MUST distinguer obtention du certificat, distribution et activation réellement vérifiée sur les services ; l'émission MUST NOT prouver le déploiement.

#### Scenario: Certificat non servi

- **WHEN** un certificat renouvelé existe mais RPZT sert encore l’ancien
- **THEN** le déploiement reste incomplet et ne peut être annoncé réussi.

### Requirement: Remise TLS ciblée aux RPZT

Les éléments TLS MUST être distribués uniquement aux RPZT habilités, avec protection individualisée. Un certificat/clé distinct par RPZT MUST être le défaut ; un partage MAY être choisi explicitement par publication. Les secrets MUST NOT être exposés dans les consultations, diagnostics ou artefacts.

#### Scenario: Publication partagée explicitement

- **WHEN** un profil choisit la même clé pour plusieurs RPZT
- **THEN** chaque destinataire habilité reçoit sa propre protection sans rendre la clé lisible aux autres acteurs.

### Requirement: Récupération par autorité et racine distincte

Chaque autorité MUST choisir sa procédure de récupération par profil. Les protections de racine hors ligne et de rotation normale MUST rester distinctes de la reprise d'une autorité opérationnelle. Une compromission suspectée MUST empêcher la réutilisation non vérifiée de la même clé.

#### Scenario: Clé compromise

- **WHEN** une clé de secours est suspectée compromise
- **THEN** la réplication ne la rend pas admissible et la procédure autorisée traite le renouvellement ou retrait nécessaire.

### Requirement: Confiance d'amorçage distincte et retrait vérifié

La PKI normale MUST être distincte de la confiance technique pré-PostgreSQL de C08/Z12. Cette confiance initiale MUST rester limitée et bornée, puis être retirée après établissement et vérification de la PKI normale et de ses usages requis. La transition MUST conserver la traçabilité des identités, les retraits connus et des preuves de bascule, sans exporter les clés matérielles initiales pour en faire des clés opérationnelles PG.

#### Scenario: Confiance technique encore seule disponible

- **WHEN** PostgreSQL est disponible mais la PKI normale ou ses usages n'ont pas été vérifiés
- **THEN** la transition reste incomplète dans ses bornes d'amorçage et aucun justificatif initial n'est promu implicitement en justificatif normal

#### Scenario: Réutilisation après retrait

- **WHEN** une ancienne confiance d'amorçage est invoquée après son retrait attesté
- **THEN** elle est refusée même en cas de panne de la PG opérationnelle
