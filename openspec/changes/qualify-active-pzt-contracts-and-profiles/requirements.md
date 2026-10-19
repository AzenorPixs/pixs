# Références normatives — Z26

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 147 | [Audit applicable et faits réellement établis](../../specs/pzt/spec.md#L147) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 156 | [Portée des contrats techniques et valeurs ouvertes](../../specs/pzt/spec.md#L156) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 165 | [Qualification et état de spécification distincts](../../specs/pzt/spec.md#L165) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 174 | [Lecture normative des contrats de décision intégrés](../../specs/pzt/spec.md#L174) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 188 | [Contrat A05b — Objectifs initiaux validés, qualification requise](../../specs/pzt/spec.md#L188) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--82a0e6c439

Source : `openspec/specs/pzt/spec.md`, ligne 147. SHA-256 du bloc : `bc7545fffd89f97f8278ddfd75e3a0e388c7291bebe64612552dc59554458b29`.

~~~~text
### Requirement: Audit applicable et faits réellement établis

Les contrôles applicatifs PZT MUST suivre security, authorization, initial-administration et audit, y compris l'exception Super Admin dans son seul périmètre reconnu. Aucun worker MUST recevoir ses credentials ou devenir Super Admin. Une dérogation MUST NOT fabriquer un dossier, audit, contrôle, signature, mesure ou effet absent ; les contrats structurels et d'exécution MUST rester distincts.

#### Scenario: Audit applicable et faits réellement établis

- **WHEN** une opération utilise une dérogation sans audit persistant
- **THEN** l'absence est déclarée et aucune preuve d'audit effectuée n'est annoncée
~~~~

### Référence pzt--ba5864bec8

Source : `openspec/specs/pzt/spec.md`, ligne 156. SHA-256 du bloc : `3b1191a78ab9589699a204e87a7e1f9bbb48d846a974c11378d8710fa1afa1a1`.

~~~~text
### Requirement: Portée des contrats techniques et valeurs ouvertes

Les contrats A05b–A12g ci-dessous MUST s'appliquer seulement aux rôles et traitements désignés : validateur, auxiliaire temporel, autorité, collecteur, purge ou réarmement. Leurs plafonds MUST NOT être extrapolés en limite globale PA/PBO ni imposer ces services à chaque PA ordinaire. Les valeurs non décidées, candidats et méthodes à qualifier MUST rester ouverts ; les indications historiques de rédaction MUST NOT devenir des effets réalisés.

#### Scenario: Portée des contrats techniques et valeurs ouvertes

- **WHEN** un plafond de l'auxiliaire temporel est consulté
- **THEN** il n'est pas présenté comme un budget global de tous les binaires PA
~~~~

### Référence pzt--7794d08725

Source : `openspec/specs/pzt/spec.md`, ligne 165. SHA-256 du bloc : `d3476abc88e4c8f2595780a249efb0d22ce0ee0a13709113159fca64c4e37f6a`.

~~~~text
### Requirement: Qualification et état de spécification distincts

PZT MUST disposer de recettes de contrat, sécurité, reprise, plateformes, transport, isolation, administration PBO et ressources par profil avant de revendiquer ces garanties. Les spécifications MUST distinguer objectifs validés, valeurs à mesurer, opérations effectuées et scénarios non exécutés. La déclaration OpenSpec MUST NOT activer PZT, construire les binaires ou annoncer une livraison fonctionnelle.

#### Scenario: Qualification et état de spécification distincts

- **WHEN** le change documentaire est archivé sans code
- **THEN** PZT reste spécifié et non implémenté, sans recette runtime revendiquée
~~~~

### Référence pzt--fa8c14eb09

Source : `openspec/specs/pzt/spec.md`, ligne 174. SHA-256 du bloc : `d55d36fc2a2dc229755281fc65b5fbb5e94361c14f02608097830f1b17286f14`.

~~~~text
### Requirement: Lecture normative des contrats de décision intégrés

Les contrats intégrés MUST conserver conditions, bornes, rôles et résultats.
Une alternative rejetée MUST NOT être activée ; une valeur non décidée MUST NOT
recevoir de défaut implicite. Une indication historique MUST NOT devenir un
effet réalisé. Les précisions ultérieurement validées MUST résoudre les renvois
anciens sans rouvrir leurs choix ; les exceptions applicatives et contrats
structurels demeurent applicables.

#### Scenario: Paramètre ancien précisé par une décision ultérieure

- **WHEN** un contrat ancien renvoie à un algorithme ou une limite ensuite validé dans ce registre
- **THEN** la décision ultérieure applicable est respectée et aucune nouvelle valeur n’est inventée
~~~~

### Référence pzt--4b8f11c8f2

Source : `openspec/specs/pzt/spec.md`, ligne 188. SHA-256 du bloc : `a99a9136e3e01efb3750e0bab2dd913bcdaae49a9d3a7accad8d14b60e5c9695`.

~~~~text
### Requirement: Contrat A05b — Objectifs initiaux validés, qualification requise

Le rôle chargé du traitement A05b MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A05b

Le développeur a validé le premier jet ci-dessous le 5 octobre 2026. Ces
valeurs sont les objectifs initiaux du cadrage, à mesurer sur chaque profil ;
elles ne sont ni des performances démontrées ni des valeurs imposées par
WireGuard ou NetBird. Elles sont des paramètres documentés par profil dans
les limites retenues ; leur modification nécessite une décision explicite.
L'affectation détaillée des communications aux classes reste à spécifier.

| Cas | Objectif initial validé | Portée et mesure |
| --- | --- | --- |
| Courant | Validité maximale 5 minutes ; renouvellement visé toutes les 60 secondes. | Du début de validité émis par l'autorité à la fin effective de l'accès ; pas de prolongation hors ligne. |
| Protégé | Validité maximale 60 secondes ; renouvellement visé toutes les 20 secondes. | Même borne ; conditions renforcées du profil maintenues. |
| Critique | Décision en ligne pour la session ou l'opération protégée selon la politique ; aucun nouveau lancement hors ligne. | Le canal préexistant ne vaut pas autorisation ; durée d'exécution et interruption déclarées dans le mandat. |
| Révocation, PA joignable | Fermeture des accès concernés en 5 secondes maximum. | De l'engagement autoritatif de la révocation à sa prise d'effet ; objectif valable sur un chemin de contrôle qualifié. En partition, les échéances et exigences de fraîcheur restent opposables. |
| Crash ou blocage de PA | Fermeture de protection en 10 secondes maximum. | De la perte de fonctionnement de PA à la fermeture effective ; détection et action du mécanisme indépendant incluses. Une échéance antérieure reste prioritaire. |

Les renouvellements exigent une nouvelle décision valide ; la répétition d'une
ancienne preuve ne remet pas un compteur à zéro. L'expiration n'ajoute aucune
période de grâce. L'UTC contractuel et la confiance temporelle restent requis.
Pause, reprise, snapshot et restauration doivent empêcher la réactivation
d'un accès périmé avant toute reprise des échanges. Un profil qui ne démontre
pas les délais retenus n'est pas déclaré conforme ; leur modification exige
une décision explicite documentée.

##### Application au PA — A05b

Le développeur a validé le premier jet ci-dessous le 5 octobre 2026, commun
avec le cadrage PZT. Ces objectifs doivent être mesurés sur chaque profil Linux,
Windows, VM, Docker et LXC ; aucune performance n'est présumée démontrée.
Ils sont des paramètres documentés par profil dans les limites retenues ;
leur modification nécessite une décision explicite. L'affectation détaillée
des communications aux classes reste à spécifier.

| Cas | Objectif initial validé | Portée et mesure |
| --- | --- | --- |
| Courant | Validité maximale 5 minutes ; renouvellement visé toutes les 60 secondes. | Du début de validité émis par l'autorité à la fin effective de l'accès ; pas de prolongation hors ligne. |
| Protégé | Validité maximale 60 secondes ; renouvellement visé toutes les 20 secondes. | Même borne ; conditions renforcées du profil maintenues. |
| Critique | Décision en ligne pour la session ou l'opération protégée selon la politique ; aucun nouveau lancement hors ligne. | Le canal préexistant ne vaut pas autorisation ; durée d'exécution et interruption déclarées dans le mandat. |
| Révocation, PA joignable | Fermeture des accès concernés en 5 secondes maximum. | De l'engagement autoritatif de la révocation à sa prise d'effet ; objectif valable sur un chemin de contrôle qualifié. En partition, les échéances et exigences de fraîcheur restent opposables. |
| Crash ou blocage de PA | Fermeture de protection en 10 secondes maximum. | De la perte de fonctionnement de PA à la fermeture effective ; détection et action du mécanisme indépendant incluses. Une échéance antérieure reste prioritaire. |

PA ne prolonge aucune échéance en rejouant une preuve et n'ajoute aucune
période de grâce. Pause, reprise, snapshot et restauration doivent empêcher
la réactivation d'un accès périmé avant toute reprise des échanges. La confiance
temporelle reste requise ; un profil sans preuve des délais retenus n'est pas
déclaré conforme. Leur modification exige une décision explicite documentée.

#### Scenario: Conformité du traitement A05b

- **WHEN** un profil revendique le traitement A05b et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

