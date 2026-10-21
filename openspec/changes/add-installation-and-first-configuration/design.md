# Conception — C08

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 a été adopté et archivé le 18 octobre 2026 ; ses précisions normatives sont intégrées au canon. Les arbitrages propres au présent change restent à lever avant réalisation.

Le complément R01 du 19 octobre 2026 précise le contrat d’amorçage C08/C02 et sa recette. Il conserve les options A de D01–D04 de C02 et les limites de C01. Il autorise uniquement les documents concernés ; aucune implémentation, production de code, migration ou recette produit n’est lancée. Les mécanismes concrets d’authentification, de marqueur et de reprise restent à détailler dans les lots propriétaires.

## État actuel vérifié

Constat : manage.py est une entrée Django sans réglage par défaut ; aucun parcours INSTALLER/première configuration complet n’est démontré.

Sources consultées et empreintes recoupées avec la matrice :

- [manage.py](../../../manage.py).
- [src/pixs/backend/README.md](../../../src/pixs/backend/README.md).
- [src/pixs/backend/settings.py](../../../src/pixs/backend/settings.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Séparer marqueur externe d’installation et état FIRST_CONFIGURATION en base. La CLI présente les plans, confirme toute création/migration/destruction concernée et reprend l’état persistant. Authentifier explicitement l’opérateur d’amorçage sans dépendre circulairement d’une session pas encore créée ; valeurs saisies remplacées par références privées.

Le [cadrage Auth essentiel](../define-essential-autonomous-auth-module/design.md) est adopté au canon le 20 octobre 2026 pour ses trois deltas d'architecture. C08 devra sélectionner explicitement le profil local PostgreSQL et provisionner le premier moyen via les contrats Core/Auth, sans session préalable du compte cible ni dépendance à LDAP/Kerberos. La recette future vérifiera l'absence de justificatif universel par défaut, des connecteurs externes installés et des services LDAP/KDC/AD ou d'émission IdP activés implicitement. R01, l'identité opérateur, le compte de secours unique et ses exemptions canoniques restent préservés. Les méthodes détaillées et l'enrôlement conservent leurs propositions distinctes ; aucun mécanisme ni recette n'est réalisé par cet alignement.

## R01 — Contrat d’autorité d’amorçage C08/C02

Ce contrat de travail précise l’application des exigences existantes de [provisionnement](../../specs/installation-provisioning/spec.md), de [création/réutilisation du compte](../../specs/initial-administration/spec.md) et d’[autorisation](../../specs/authorization/spec.md). Il décrit des informations logiques, sans nouveau wire format, enum public, provider, protocole d’authentification ou valeur de configuration. C08 possède l’acte de provisionnement et son autorisation ; C02 possède les écritures Core et leurs contraintes. C03/C04 produisent les faits d’identité et d’autorisation vérifiables nécessaires à cet acte ; C05 conserve l’audit applicable.

### Acteur, compte cible et contrôle de confiance

L’opérateur est l’acteur qui présente un plan d’installation ; le Super Admin à créer ou à réutiliser en est une cible explicite. La connaissance des credentials PostgreSQL, deux saisies de mot de passe identiques, le mode INSTALLER, UID 0 ou la seule présence d’un marqueur ne prouvent ni l’identité de l’opérateur ni son droit de provisionner.

C08 demande à la chaîne de confiance déclarée C03/C04 une preuve d’identité et une décision d’autorisation rattachées à cette opération et à cette installation. La vérification préalable ne requiert pas de session Pixs déjà créée ni d’utilisateur nominatif local. Elle peut consommer des preuves et une politique d’installation explicitement provisionnées hors de la base en cours d’initialisation ; cela ne sélectionne aucun provider concret ni source d’identité métier parallèle. La référence de sujet applicatif et son mapping explicite sont établis par cette chaîne, sans déduire une DigitalIdentity ou un niveau d’assurance d’un compte OS. Le mécanisme et les références de confiance effectivement retenus font partie du contrat C03/C04 avant réalisation de cette branche.

Le compte cible n’est pas utilisé comme acteur déjà authentifié avant sa création. Une référence d’acteur, une structure d’identité valide ou un booléen `verified` fourni par l’appelant ne remplace pas une preuve vérifiée. Si la chaîne ne peut produire le sujet et l’autorisation conformes au canon pour l’amorçage pré-session, la branche reste refusée ; une précision normative éventuellement nécessaire est présentée avant toute réalisation, sans inventer une exception supplémentaire dans ce document.

C01 reste limité à ses actions techniques de secrets et à son audit INSTALLER. Son identité native, sa politique et ses reçus ne sont pas une permission de créer une base, une identité, un compte ou un tenant. Le journal C01 ne devient pas le sink des mutations Core. Aucun droit métier n’est transféré de C01 au port d’initialisation C02.

### Entrées logiques et vérifications du port

Le raccordement est un port propriétaire d’initialisation borné, distinct d’une Command Core ordinaire ouverte aux façades. Il n’expose ni SQL, ni modèles privés, ni action générique arbitraire. Les éléments sont fournis par les producteurs de confiance puis vérifiés par C02 ; un dictionnaire reçu d’un client ou un acquittement mémoire de C08 n’a pas cette autorité.

| Information liée à l’acte | Producteur et contrôle | Refus attendu |
|---|---|---|
| Identité d’opération, version du plan et identité de l’installation/base cible | C08 ; liaison stable entre confirmations, cible, état observé et reprise | Référence absente, plan remplacé, autre installation ou état de base divergent : aucun effet Core. |
| Mode INSTALLER explicite et éligibilité courante | C08 ; vérification du marqueur externe, de l’état de base et de la procédure déclarée | Un marqueur absent/invalide ne déclenche pas seul INSTALLER ; absence d’éligibilité vérifiable ou mode NORMAL : refus de cette voie. |
| Référence d’opérateur, preuve vérifiée et mapping de sujet | C03/C04 selon le mécanisme approuvé, indépendamment d’une session préexistante | Preuve absente, expirée, révoquée, ambiguë ou d’une source non approuvée ; UID 0 ou compte cible présentés seuls : refus. |
| Décision d’autorisation, politique/version et finalité | C04 pour le plan propriétaire C08 ; contrôle du sujet, des ressources/actions et des validités | Décision périmée, finalité étrangère ou action non prévue : refus, sans extension de l’exception C01. |
| Ensemble fermé d’effets et de références cibles | C08 ; compte fonctionnel, identité cible, premier tenant et accords explicitement désignés dans le plan | Champ ou effet non déclaré, deuxième compte, tenant supplémentaire ou accord implicite : refus. La présence d’un tenant dans le plan ne lui accorde pas automatiquement l’accès Super Admin. |
| Confirmations du plan et intention de credential | C08/C03 ; confirmations liées au plan courant et vérification des deux saisies lorsqu’une création/recréation l’exige | Confirmation ancienne/absente ou saisies différentes : aucune création. Le mot de passe ne sert pas de preuve d’habilitation de l’opérateur. |
| Contexte et corrélation | C08/C04 ; contexte PLATFORM explicite pour l’administration de l’installation, cibles tenant distinctes, corrélation et causalité conservées | Un contexte PLATFORM ne vaut pas permission ; un tenant ou scope injecté ne change pas la cible autorisée. Les données créées reçoivent leur propriété tenant canonique. |
| État attendu, identité d’idempotence et preuve d’audit applicable | C08/C02/C05 ; inspection persistante, exclusion concurrente et preuve liée à l’effet/refus | Ancien état, rejeu divergent, audit requis indisponible ou issue précédente inconnue : refus ou réconciliation, sans succès supposé. |

Les preuves et décisions sont liées au plan, à sa cible, aux actions, au sujet et à leur validité ; elles ne sont pas un justificatif réutilisable pour une autre installation ou une opération ordinaire. La durée de validité, le mécanisme d’authentification, le stockage du plan et la protection contre substitution sont déclarés avant réalisation, sans valeur issue d’une fixture. Aucun jeton public de bootstrap, mot de passe par défaut ou compte de service d’installation permanent n’est introduit.

### Séquence et fin de l’autorité d’initialisation

1. C08 vérifie explicitement le mode, l’opérateur, la politique et l’état de l’installation avant de présenter un plan lié à la cible. Toute création, migration ou recréation destructive de base reste une étape confirmée propre à C08, hors de la transaction de données Core et hors de C01.
2. Après disponibilité du schéma et des ports obligatoires, C08 demande l’acte Core avec les preuves et décisions liées au plan. C02 en contrôle la provenance et les correspondances ; le plan ne constitue pas un appel ORM direct ni une dispense d’autorisation. L’identité et le droit de l’opérateur sont vérifiés sans authentifier par avance le compte cible.
3. C02 ouvre une transaction propriétaire, acquiert l’exclusion de l’opération/installation selon D03-A et recontrôle l’état attendu. Il crée l’identité explicite, la liaison fonctionnelle unique et le tenant seulement si le plan autorisé les demande. C03 apporte uniquement l’empreinte sécurisée du credential par son contrat ; aucun secret, hash de mot de passe ou preuve sensible n’entre dans l’audit, la corrélation ou une empreinte publique de plan. C08 écrit son résultat d’opération par son port propriétaire participant à la même frontière que les écritures Core liées. C02 n’écrit pas directement dans les tables privées C03/C05/C08 ; leur participation transactionnelle est définie par les ports communs.
4. C05 fournit l’audit applicable de l’opérateur, des actions et du résultat ; le compte futur ne donne aucune dérogation anticipée. Pour une base conservée, seule une exception du Super Admin existant effectivement authentifié peut suivre les règles canoniques, sans prétendre qu’un audit absent a eu lieu. Les éventuels événements ne deviennent publiables qu’après commit selon C09.
5. Après commit vérifié, C08 produit ou fait valider le marqueur externe et inspecte l’état FIRST_CONFIGURATION. Le marqueur ne fait pas partie de la transaction PostgreSQL. Le compte créé doit ensuite s’authentifier par C03 pour poursuivre la première configuration ; la preuve de l’opérateur n’est pas une session de ce compte. Aucun MFA interdit par le canon n’est ajouté.
6. Le résultat confirmé clôt les effets de l’acte d’initialisation. Une reprise autorisée consulte ce résultat ; elle ne réutilise pas une ancienne décision pour muter d’autres ressources. Les opérations ordinaires passent ensuite par leurs contrats C03/C04/C05. Le maintien d’INSTALLER ne garde pas un droit permanent de création ou de réinitialisation.

Une base conforme conservée réutilise le compte existant ; l’acte ne réinitialise pas son mot de passe, ne crée pas un second compte et n’invente pas un tenant manquant. Toute action supplémentaire relève d’un plan distinct et de son autorisation propre. Une recréation de base incompatible conserve ses confirmations et sa portée explicites ; elle n’est pas assimilée à un simple rejeu d’installation.

### Reprise, concurrence et résultats

L’inspection distingue refus sans effet, résultat confirmé, conflit et issue à réconcilier ; ce sont des résultats logiques à mapper aux états/erreurs existants, sans nouvel enum public. Même identité d’opération et même plan courant : le résultat confirmé est restitué après autorisation actuelle, sans nouvelle identité ni réécriture de credential. Même identité avec cible/plan/intention différents : conflit explicite. Un secret ou son empreinte ne sert pas de clé publique d’idempotence.

Deux exécutions concurrentes ne peuvent confirmer deux comptes fonctionnels ou deux premiers tenants pour le même acte : exclusion, unicité et état attendu sont contrôlés dans PostgreSQL. Avant commit, une panne annule les effets de données liés. Après commit et avant réponse ou marqueur, la reprise retrouve les références confirmées, renouvelle les vérifications nécessaires et termine la seule étape manquante, sans recréer de compte. Une issue de commit inconnue n’autorise pas un rejeu aveugle ; une inspection propriétaire établit d’abord les effets réels.

Le checkpoint C08 et les références d’opération ne stockent ni mot de passe, ni assertion brute, ni valeur de secret. Les métadonnées minimisées d’opérateur restent distinctes de l’identité cible. Avant disponibilité du stockage requis, aucune mutation Core ne commence. Une perte de preuve ou un marqueur incohérent garde l’état non prêt ; NORMAL et le trafic métier restent interdits sans relancer implicitement INSTALLER.

### Recette R01 et responsabilité des preuves

Les dix cas suivants sont des critères futurs, non des scénarios ajoutés au canon ni des tests exécutés. C02 démontre localement les gardes, l’intégrité et les raccordements ; C08 démontre le parcours complet avec C03/C04/C05 et les effets réels. Les références canoniques et tâches sont reliées dans `requirements.md`.

| Cas | Entrée ou interruption | Résultat attendu | Tâches C08 et contribution C02 |
|---|---|---|---|
| B01 | Première installation sans session Pixs préexistante, opérateur et plan réellement vérifiés | L’acte borné est admissible après contrôle des preuves ; aucune session préalable du compte cible ni autorité C01 métier requise. Si le mapping conforme au canon manque, refus avant écriture. | C08 1.2/2.1/2.3/2.4 ; C02 1.2/2.3, V05/V07. |
| B02 | Preuve absente/expirée/révoquée/substituée ; source non approuvée ; UID 0 ou booléen client seuls | Aucun compte, identité, tenant ou droit créé ; refus et audit applicable sans secret. | C08 2.3/2.4 ; C02 2.3/2.4, V04/V05/V07. |
| B03 | Base créée/recréée confirmée, saisies identiques et plan courant ; accord tenant explicitement sélectionné ou absent | Un seul compte et une identité explicite, empreinte privée C03, propriétaire tenant cohérent ; aucun accord déduit de la simple création. | C08 2.2/2.3/2.4 ; C02 2.1/2.2/2.4, V01/V03/V05. |
| B04 | Saisies différentes, confirmation ancienne/absente, cible/plan/actions modifiés | Aucun effet Core ; aucun secret ou hash de mot de passe dans les sorties. | C08 2.2/2.3/2.4 ; C02 2.3/2.4, V05/V12. |
| B05 | Base conforme conservée avec compte existant | Réutilisation après contrôles courants ; aucun second compte, reset de credential ou tenant créé implicitement. | C08 2.2/2.3/2.4 ; C02 2.1/2.4, V05. |
| B06 | Deux exécutions concurrentes ou même opération rejouée | Au plus un effet confirmé ; même plan rendu sans doublon après contrôle actuel, plan divergent refusé. | C08 2.3/2.4 ; C02 2.2/2.4, V02/V05/V07. |
| B07 | Crash avant commit, puis après commit avant réponse ou marqueur ; résultat du commit inconnu | Avant commit : pas d’effet partiel. Après commit : reprise du seul reste sans seconde identité. Issue inconnue : inspection avant rejeu. | C08 2.1/2.4 ; C02 2.2/2.3/2.4, V05/V07/V09. |
| B08 | Sink C05 indisponible lors de première création ; présentation d’un reçu ou journal C01 comme substitut | Aucun privilège anticipé du compte futur ; pas de confirmation sans garantie obligatoire ; C01 ne reçoit aucun audit métier. Dérogation existante authentifiée traitée séparément selon canon. | C08 2.3/2.4 ; C02 2.3/2.4, V07/V12. |
| B09 | Preuve rejouée sur autre installation/tenant, mode NORMAL, plan déjà terminé ou actions hors ensemble fermé | Voie d’initialisation refusée ; aucune autorité durable ni transfert de l’exception Super Admin. | C08 2.3/2.4 ; C02 2.3/2.4, V04/V05/V07. |
| B10 | Marqueur absent/invalide/incohérent après effet confirmé ; première configuration inachevée | État inspectable non prêt ; aucune création en boucle ni démarrage NORMAL implicite. Après rapprochement autorisé, authentification propre du compte pour FIRST_CONFIGURATION. | C08 2.1/2.4 ; C02 V05/V07, C03/C04 et reprise C08. |

La preuve intégrée conserve version du contrat, plan, environnement, commandes, résultats et effets contrôlés sans secret. Elle ne sera pas déduite de booléens simulés. Aucun cas B01–B10 n’est déclaré réussi par sa rédaction ; aucun code ni test n’est produit par ce complément.

## Sélection de la preuve R01 du 20 octobre 2026

Les [décisions C03 D15/D16](../add-initial-authentication-and-sessions/design.md) sélectionnent la clé publique personnelle préautorisée et une signature Ed25519 vérifiée avec cryptography. Le [delta C04 adopté le 20 octobre 2026](../integrate-runtime-authorization-and-super-admin/specs/authorization/spec.md) formalise le sujet opérateur pré-session et son mapping explicite. Les formulations R01 antérieures décrivent la frontière avant cette sélection ; le delta est désormais synchronisé au canon, sans réalisation de R01.

Clé publique, opérateur et droits d’installation sont établis par une procédure de confiance explicite, indépendante de la future session du Super Admin. La clé privée reste sous contrôle de l’opérateur. Une clé fournie par le demandeur ne s’autorise pas elle-même ; UID 0, accès PostgreSQL, confirmations de mot de passe et reçu C01 ne remplacent pas la chaîne C03/C04.

L’autorisation finale vaut 10 minutes à partir de la validation du plan final, pour une installation, sa version de plan et les seuls effets fermés. Sa consommation est liée au commit des effets propriétaires ; elle n’est pas consommée par un simple succès mémoire et ne permet pas de second effet. La préparation complète de l’installation n’est pas limitée par ce délai. Plan/cible changés, expiration ou preuve révoquée exigent une nouvelle autorisation. Une reprise inspecte le résultat committé ; le marqueur externe reste réconcilié séparément, sans nouvel acte de création.

La transaction commune de l’effet d’amorçage et de son audit reste obligatoire. L’exception D14 est limitée au retrait d’accès Auth et ne dispense aucune création de compte, identité, tenant ou droit de son audit. Les scénarios R01 B01–B10 devront inclure signature, validité, concurrence et réponse perdue. Versions, sérialisation du plan, ancrage de confiance, mapping exact, marqueur et checkpoint restent à qualifier avant code ; aucun cas n’est exécuté ici.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Le contrat R01 ci-dessus fixe les informations vérifiées, actions fermées et critères de reprise du raccordement C08/C02. Restent à détailler avant réalisation le mécanisme déclaré de preuve et son mapping de sujet C03/C04, les paramètres de validité, le format/propriétaire du marqueur et du checkpoint, et l’intégration transactionnelle C05. Si un mécanisme ne satisfait pas le canon, il reste refusé jusqu’à clarification normative autorisée ; aucun bypass local n’est accepté. D01–D04 restent acquis. Aucun effacement, stockage de secret ou manipulation de base pendant cette préparation.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [add-pbo-runtime-secret-provider](../archive/2026-10-19-add-pbo-runtime-secret-provider/proposal.md).
- [add-core-postgres-services](../archive/2026-10-20-add-core-postgres-services/proposal.md).
- [add-initial-authentication-and-sessions](../add-initial-authentication-and-sessions/proposal.md).
- [integrate-runtime-authorization-and-super-admin](../integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md).
- [activate-reference-runtime-composition](../activate-reference-runtime-composition/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Base absente/conforme/migrable/incompatible ; confirmations requises ; mots de passe différents refusés ; conservation du Super Admin existant ; reprise sans doublons ; marqueur invalide interdit NORMAL sans relancer implicitement INSTALLER.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

Cette section conserve son état historique. R01 précise désormais le raccordement C08/C02 ci-dessus ; les mentions historiques de contrat à compléter ne donnent aucune autorité métier à C01 et ne prouvent aucune réalisation.

### T03 — Réadmission après état restauré

La restauration cohérente de données ne prouve ni fraîcheur de révocations/incidents ni admissibilité des effets différés. N05 dédié et delta ciblé validés ; faits nécessaires et revalidation détaillée à définir avant code.

Contrôles à intégrer : Snapshot antérieur à révocation/rotation/incident ; Effet déjà engagé dont réponse perdue ; Marqueur externe incohérent ; Interruption puis reprise de réconciliation sans réémission automatique.

### T05 — SecretProvider et opérateur avant première session

L’opérateur initial, le workload et la conversion des saisies en références ne doivent dépendre ni d’une session inexistante ni d’une base déjà initialisée. Compléter le contrat d’amorçage C01/C08 ; pas de nouveau provider imposé.

Contrôles à intégrer : Provider en lecture seule : procédure explicite de fourniture de référence ; Panne entre saisie et référence confirmée sans fuite ; Opérateur non vérifiable refusé avant mise en service.

### T06 — Marqueurs externes et états PostgreSQL

Marqueur d’installation et marqueur de désactivation Super Admin ont des fonctions différentes et ne sont pas une transaction atomique avec PostgreSQL. Compléter C08 et les contrats C03/C04/C09 ; N05 vérifie le rapprochement après restauration.

Contrôles à intégrer : Commit base avant marqueur : reprise sans second compte ; Marqueur absent/invalide interdit NORMAL sans relancer INSTALLER ; Désactivation non dérogée refuse nouvelles actions/reprises, transaction engagée préservée ; Secours propre sans MFA imposé.

### T15 — Langues, thèmes et accessibilité de tous les parcours

Les parcours CLI, erreurs API, management et secours font aussi partie des textes utilisateur ; couverture ne se limite pas à la page du shell. Compléter la matrice C12/C17 et les contrats de messages ; codes stables non localisés.

Contrôles à intégrer : Deux navigateurs déclarés, clavier/zoom/lecteur d’écran ; Erreurs et confirmations d’installation/exploitation localisées ; Thème/session/tenant sans fuite d’état.

Voir [audit transversal durable](../archive/2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.

## Contrôles documentaires R01 du 19 octobre 2026

Les validations OpenSpec ciblées strictes de `add-core-postgres-services` et `add-installation-and-first-configuration`, avec l’exécutable déclaré dans DEVOPS.md et télémétrie désactivée, ont retourné exit 0. L’information native `skip_specs` accepte zéro delta ; ce résultat ne valide ni un mécanisme d’authentification ni une recette produit.

Les références, titres, lignes et listes de scénarios ont été contrôlés : C02 contient 72 exigences / 89 références de scénarios et conserve V01–V12 ; C08 contient 36 exigences / 44 références de scénarios, reliées notamment aux dix cas B01–B10. Les empreintes canoniques, l’encodage UTF-8/LF, les cibles de liens et les tâches sont contrôlés séparément des preuves fonctionnelles. Les vingt tâches de réalisation des deux changes restent non cochées. Aucun cas de recette, code, migration ou archivage n’est exécuté par ce complément.
