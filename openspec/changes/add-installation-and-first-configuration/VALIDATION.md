# VALIDATION — C08 Installation et première configuration

Clôture différée pour dépendances manquantes : validation maximale existante puis arrêt sans archive, sans surveillance ni réessai automatique. Le change reste ouvert, en attente de finalisation. Aucune réussite globale n’est déclarée et aucune reprise n’est automatique.

## 1. Bilan et références de preuves

Six cases sur dix-sept sont cochées : 1.1, 1.2, 1.3, 1.4, 1.5 et 1.6. Les tâches 1.1 à 1.5 conservent leur portée documentaire historique et la tâche 1.6 est une validation de conception documentaire seule, sans qualification de runtime. Deux cent trente-deux tests C08 sont PASS et zéro FAIL, soit cent dix-sept tests E5 acquis et cent quinze tests locaux neufs dans quinze suites distinctes. Contrôles syntaxiques ciblés réussis, dont dix-sept fichiers dans le dernier lot et le module de projection contrôlé précédemment. L’intégrité des sources examinées est stable en UTF-8 et fins de ligne Unix. Le nettoyage des quatre répertoires de test nouveaux est prouvé avec exit zéro et la restitution distincte est prouvée avec exit zéro et sortie attendue. Aucun Docker, conteneur, navigateur, service ou port réseau n’a été créé dans cette frontière et les accès métier sont libérés au moment du rapport. Aucun échec métier n’a été observé et les incidents CAB résolus sans effet restent séparés des tests. Git n’a été ni inspecté ni modifié et aucun secret n’a été lu ou transmis.

Les preuves sont : checkpoint output/cismp/cismp1-pixs-02716fc18b3546c0/state.json, clé reprise_1cismp1_20261026_0040 ; cent quinze tests, preuve native prt_1787be156001sSdr887ODVdxiH et rapport msg_1787bf729001TSgPIm7jGto5tC ; coche 1.6, rapport msg_17878a207001h6dxXPBb1YT5A6 ; contrôle strict avant cochage, rapport msg_178727758001gLKRT4qFzKw1HG ; restitution quatre sur quatre, rapport msg_1788737e7001jEpA6E0cVA7PRU ; confirmation C7 d’aucun port runtime consommable et qualifié, avec contrats PA courants SHA 2fe69fe6…928fa3 et sections 80-151, 861-863, 929-930 et 1512-1656 ; synthèse C08 à partir de tasks, requirements, design, projection-contract et du présent VALIDATION. L’absence de qualification observable est distincte d’une absence de fichiers : les sources et recettes existent et les fichiers de tests PostgreSQL écrits en fonctions et scripts existent, mais aucune recette PostgreSQL intégrée C08 n’a été exécutée ici et aucune panne PostgreSQL n’a été constatée. Aucun audit exhaustif du code voisin n’est prétendu.

## 2. Table des quinze suites : deux cent trente-deux tests

| Suite | Tests |
|---|---:|
| test_c08_exchange_envelope_1_1 | 21 |
| test_c08_planning_bundle | 20 |
| test_c08_exchange_response_1_1 | 15 |
| test_c08_postgresql_confirmation | 28 |
| test_c08_pre_confirmation_presentation | 12 |
| test_c08_planning_bundle_store | 21 |
| test_c08_technical_projection | 13 |
| test_c08_mode_values | 6 |
| test_c08_mode_commands | 14 |
| test_installation_act_content | 6 |
| test_installation_plan | 13 |
| test_installation_plan_storage | 13 |
| test_installation_marker | 20 |
| test_installation_checkpoint | 19 |
| test_installation_checkpoint_binding | 11 |
| Total | 232 |

Les cent quinze tests locaux valident la projection avec treize tests, les modes avec six et quatorze tests, le contenu d’acte avec six tests, le plan avec treize tests, le stockage du plan avec treize tests, le marqueur avec vingt tests, le checkpoint avec dix-neuf tests et la liaison avec onze tests. Ce sont des sous-unités locales avec vrais fichiers, verrous, processus joints et fautes injectées, et non des garanties de runtime. Les cent dix-sept tests E5 restent acquis avec leurs codecs, leur présentation, leur confirmation et leur stockage.

## 3. Revue 1.6 : conception complète, runtime réservé

La tâche 1.6 détaille le provisionnement opérateur indépendant de PostgreSQL, la capacité PostgreSQL du catalogue fermé PA et le profil PZT local mTLS. Les critères recoupés sont les identités, ancrages et politiques protégés, les actions et cibles fermées, la validité, la fraîcheur, la révocation, l’anti-rejeu et l’audit pré-base, l’absence de premier PBO auto-approuvé, de shell arbitraire, de repli hors PZT et de droit métier implicite, ainsi que la revue P03, P04, P07 et P09 avec transition vers l’autorité PostgreSQL et conservation de R01 et C01. Les textes courants E1 à E5, B, retrait et INIT A sont adoptés documentairement et le temps C6 est acquis, sans rouvrir aucun ancien vote et sans traiter un futur résolveur comme une nouvelle décision humaine. Les paramètres à qualifier et les vrais résolveurs restent identifiés avec propriétaires et refus, ce qui conditionne la phase 2 mais pas cette coche documentaire. Aucune implémentation 2.x ni aucun test TPM ou PZT n’était requis pour elle et le contrôle OpenSpec strict a réussi avant cochage.

## 4. Matrice des dix-sept tâches

| Tâche | Statut et preuves | Manque et phase | Condition de reprise |
|---|---|---|---|
| 1.1 | Validée : canon, huit deltas et limites C01-C07 recoupés | Rien, documentaire | Conserver |
| 1.2 | Validée : mécanismes R01, plan privé, marqueur et transaction | Rien, documentaire | Conserver |
| 1.3 | Validée : politiques, audit pré-base, relais C05 et publication | Rien, documentaire | Conserver |
| 1.4 | Validée : gouvernance minimale et catalogue protégé C10 | Rien, documentaire | Conserver |
| 1.5 | Validée : profils physique, VM et Docker déclarés | Rien, qualification ultérieure | Conserver |
| 1.6 | Cochée conception seule, preuve et contrôle strict ci-dessus | Rien pour la conception, runtime en 2.x | Conserver |
| 2.5 | Ouverte, non qualifiée | Vrais providers systemd et Docker, audit, relais et lifecycle ; tests et intégration | Livraison et qualification des providers et audits |
| 2.6 | Ouverte, contrat et raccords préparés | Aucune attestation ni revalidation G01-G03 qualifiée observée ici ; tests et intégration | Source réelle, attestation et revalidation sur PostgreSQL réel |
| 2.7 | Ouverte, E5 avec cent dix-sept tests locaux validés | Intégration et runtime PA et PZT non qualifiés, producteurs et résolveurs manquants ; réalisation et tests | Ports, observation, planning, préparation, résultat, origine et temps qualifiés |
| 2.1 | Partiellement réalisée, à tester et à intégrer | Persistance backend, transaction et reprise ; intégration | Raccord persistant et contrôles B06, B07, B10, P07 et P08 |
| 2.2 | Partiellement réalisée, à intégrer | CLI, quatre états et confirmations ; réalisation et tests | Confirmations et migrations propriétaires qualifiées |
| 2.3 | Partiellement réalisée, à intégrer | Composition réelle et commit commun ; réalisation et tests | Transactions, gouvernance, B01-B10, G01-G03, P08 et P09 |
| 2.4 | Ouverte | Recette intégrée B, S, G et P ; intégration et validation finale | Contrôles par tâche puis recette complète |
| 3.1 | Ouverte | Périmètre final incomplet ; validation finale | Réussir 2.4 puis contrôles globaux |
| 3.2 | Ouverte | Matrice finale incomplète ; validation finale | Réussir 3.1 puis conformité et secrets |
| 3.3 | Ouverte | Revue globale non réalisée ; validation finale | Réussir 3.2 puis périmètre et impacts |
| 3.4 | Ouverte | Clôture et archive non remplies ; clôture | Réussir 3.3 puis opération explicitement autorisée |

Les unités indépendantes déjà réalisées et disponibles dans cette frontière ont été contrôlées, notamment la projection, les modes, le plan, le contenu d’acte, le stockage, le marqueur, le checkpoint et la liaison. Aucune autre tâche COMPLÈTE des dix-sept n’est validable avant ses dépendances et prérequis explicités ci-dessus. Les succès locaux ne valident ni l’intégration des providers, ni la gouvernance transactionnelle, ni les raccords PA et PZT, ni l’acte R01 composé, ni la recette globale.

## 5. Clôture différée et reprise

Le cycle CISMP de huit cent cinquante et une lignes, SHA a2af8da0b88331d97501806515c3406b8515386b9db8a7b78d25788f7856441b, a été lu et appliqué, avec clôture différée sans surveillance et reprise explicitement demandée. Décision : clôture BLOQUÉE pour dépendances manquantes, sans attente des autres développements. Le change reste ouvert et en attente, sans archivage et sans statistiques d’archive fabriquées. Le gate, le désarmement et la libération de réservation sont les prochains actes Root et ne sont pas déclarés déjà effectifs. La reprise attend la livraison et la qualification des vrais ports, puis réexamine seulement les preuves affectées et les contrôles manquants, sans nouveau change, sans nouveau prompt et sans code voisin.
