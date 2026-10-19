# Références normatives — Z02

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 146 | [Continuité sans PBO et reprise locale PZT](../../specs/pixs-agent/spec.md#L146) | ND | CANDIDAT_PROFIL_PA |
| pzt / 39 | [Autorités, politiques et délégations distinctes](../../specs/pzt/spec.md#L39) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 66 | [Expiration, révocation et protection indépendante](../../specs/pzt/spec.md#L66) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 188 | [Contrat A05b — Objectifs initiaux validés, qualification requise](../../specs/pzt/spec.md#L188) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--aacfb93718

Source : `openspec/specs/pixs-agent/spec.md`, ligne 146. SHA-256 du bloc : `8665641b1007fe45d2b73eb02d5a74fbfbac235ce440d82853ca6540720fbe11`.

~~~~text
### Requirement: Continuité sans PBO et reprise locale PZT

Sans PBO joignable, PA MUST se limiter aux capacités explicitement provisionnées, éligibles et encore valides ; une décision en ligne indisponible MUST bloquer l'action concernée. Diagnostic et reprise depuis PBO MUST passer par PZT, y compris local. Si PZT est entièrement indisponible, une réparation interne/opérateur MUST suivre sa procédure distincte, sans canal de substitution PBO–PA.

#### Scenario: Continuité sans PBO et reprise locale PZT

- **WHEN** PZT est entièrement arrêté
- **THEN** PBO ne reçoit aucun canal de contrôle local de contournement
~~~~

### Référence pzt--95cfbef9df

Source : `openspec/specs/pzt/spec.md`, ligne 39. SHA-256 du bloc : `f1987b9216a3f46255e32ac5aae8ba18a9ac0c2c66f476b0cc8f0fcc810d5c25`.

~~~~text
### Requirement: Autorités, politiques et délégations distinctes

PZT MUST distinguer identité, permission réseau et permission métier ; une position hiérarchique, clé, adresse ou certificat MUST NOT donner un accès implicite. Les relations verticales/horizontales MUST avoir périmètres et sens déclarés. Une délégation MUST identifier émetteur, bénéficiaire, actions, cible, version, validité, révocation et redélégation ; elle MUST NOT transmettre un pouvoir absent de l'émetteur.

#### Scenario: Autorités, politiques et délégations distinctes

- **WHEN** un pair possède une clé valide sans mandat pour le service
- **THEN** le trafic concerné reste refusé
~~~~

### Référence pzt--36bde46b8d

Source : `openspec/specs/pzt/spec.md`, ligne 66. SHA-256 du bloc : `b219ac819e98d78acee76394f5d430a65cb534e017dd32fc8795a6ddf942dbcc`.

~~~~text
### Requirement: Expiration, révocation et protection indépendante

Les autorisations MUST être bornées, réutilisables seulement selon leur classe et retirées dès révocation connue. Les objectifs initiaux A05b MUST être qualifiés par profil : révocation en 5 s maximum lorsque PA est joignable et fermeture après panne PA en 10 s maximum, détection comprise, avec toute échéance antérieure prioritaire. Une interface noyau persistante après crash MUST NOT prolonger un accès.

#### Scenario: Expiration, révocation et protection indépendante

- **WHEN** PA plante alors que WireGuard reste actif dans le noyau
- **THEN** la protection indépendante ferme les accès dans le budget qualifié
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

