# Conception — C08

## Statut et périmètre autorisé

La reprise documentaire du 22 octobre 2026 en fin de fichier présente le cadrage courant et la décision d’adoption. Les sections antérieures conservent leurs dates et leurs limites de preuve.

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

Les [décisions C03 D15/D16](../archive/2026-10-21-add-initial-authentication-and-sessions/design.md) sélectionnent la clé publique personnelle préautorisée et une signature Ed25519 vérifiée avec cryptography. Le [delta C04 adopté le 20 octobre 2026](../archive/2026-10-21-integrate-runtime-authorization-and-super-admin/specs/authorization/spec.md) formalise le sujet opérateur pré-session et son mapping explicite. Les formulations R01 antérieures décrivent la frontière avant cette sélection ; le delta est désormais synchronisé au canon, sans réalisation de R01.

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
- [add-initial-authentication-and-sessions](../archive/2026-10-21-add-initial-authentication-and-sessions/proposal.md).
- [integrate-runtime-authorization-and-super-admin](../archive/2026-10-21-integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md).
- [activate-reference-runtime-composition](../archive/2026-10-21-activate-reference-runtime-composition/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Base absente/conforme/migrable/incompatible ; confirmations requises ; mots de passe différents refusés ; conservation du Super Admin existant ; reprise sans doublons ; marqueur invalide interdit NORMAL sans relancer implicitement INSTALLER.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil — état historique avant le complément PA/PZT

La préparation antérieure ne sélectionnait pas PA/PZT actifs ni Docker. Le complément 1.3 ci-dessous révise explicitement cette orientation pour le parcours de préparation PostgreSQL validé ; les contrats canoniques et qualifications antérieurs ne sont pas réputés modifiés ou exécutés. Le service DNS exécuté par PA et les autres options ne sont pas activés implicitement.


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


## Reprise documentaire C08 du 22 octobre 2026 — conception 1.2 après adoption

### Statut et portée

La rédaction documentaire initiale et l’alignement distinct de .openspec.yaml sont validés. Le développeur valide ensuite l’intégration exacte des quatre exigences et huit scénarios des deltas [secrets-providers](specs/secrets-providers/spec.md) et [installation-provisioning](specs/installation-provisioning/spec.md) dans leurs deux canons, avec alignement des quatre documents C08. Les exigences canoniques antérieures sont conservées.

La métadonnée conserve schema et created et ne déclare plus skip_specs. Son alignement a été réalisé sous autorisation distincte ; la validation ciblée stricte avant adoption a réussi. Le présent lot d’adoption ne réalise aucun code, migration, service ou archivage. Les constats et contrôles des sections antérieures restent historiques.

Le prévol du RUN `cismp1-pixs-02716fc18b3546c0` a prouvé modèle et raisonnement attendus, broker READY, demande et décision corrélées, permission native once et `/usr/bin/true` exit 0. Cela ne constitue aucune recette C08.

### Faits déterminants et dépendance de gouvernance

`src/pixs/backend/runtime_resolve.py:76` et `src/pixs/backend/systemd_secret_provider/provider.py:233` refusent hors INSTALLER. Le transport C01 est en lecture seule : publier des références ne prouve ni la création du credential correspondant ni sa disponibilité pour un workload autorisé.

`src/pixs/core/ports.py` définit `GovernanceProvider` ; `services_common.py` exige une attestation valide et `services_bootstrap.py` refuse sa dispense lors de CREATE_IDENTITY. Le producteur observé dans `tests/integration/core_pg_participants.py` est une fixture. Le contrat minimal avec C10 doit donc précéder la branche positive C08 ; ni le futur Super Admin ni le reçu C01 ne peuvent le remplacer.

### Plan privé et empreintes sans auto-référence

C08 possède un plan privé immuable, versionné et lié à l’identité d’opération, à l’installation/base, à l’état observé, à l’action de base, aux cibles et aux effets fermés. Sa sérialisation interne déterministe utilise UTF-8, clés triées et séparateurs compacts ; doublons, champs inconnus, NaN, coercitions et entrées hors bornes sont refusés. Les bornes sont déclarées par configuration protégée, sans recopier une valeur de fixture.

`plan_sha256` est calculé sur ces seuls octets de plan, avant confirmation. L’entrée du digest exclut son propre digest, signatures, preuves brutes, credentials et résultats de confirmation. Les confirmations sont enregistrées séparément et liées au digest courant ; un changement de plan invalide les confirmations. Une intention de credential est une référence privée opaque, liée à son préparé protégé ; ni mot de passe ni empreinte de mot de passe n’entre dans une empreinte ou représentation publique du plan.

La preuve C03 réutilise `canonical_bootstrap_bytes(facts, nonce)` et `verify_signed_bootstrap` existants. Elle contient le digest du plan déjà calculé ; son digest de challenge est distinct du digest du plan. Calculer le plan avec les octets de sa propre preuve créerait une auto-référence et est exclu. Les liaisons de `BootstrapActInput` et `CommandEnvelope`, notamment opération, corrélation, causalité, idempotence et contenu privé, restent vérifiées par Core.

### Confiance et autorité de l’opérateur

La politique de confiance versionnée est provisionnée par une procédure d’administration déclarée, indépendamment de la future base. Sa source protégée épingle propriétaire, identité/version et bornes ; chemin ou clé fourni par le demandeur ne s’autorise pas lui-même. L’identité OS est un contrôle technique de source, pas un mapping applicatif implicite.

Le mapping opérateur, la clé publique Ed25519, l’installation, l’action et les validités sont explicitement liés. La clé privée reste chez l’opérateur, hors des données et journaux Pixs. La vérification C03 et la décision/revalidation C04 restent distinctes. La fenêtre finale est exactement 600 secondes ; une préparation longue ne la prolonge pas et toute modification du plan exige une nouvelle autorisation.

### Propriété et transaction C08

La conception de code future prévoit des modules privés `src/pixs/backend/installation/` : `plan.py`, `checkpoint.py`, `marker.py`, `base_inspect.py` et `cli.py`. Cette liste est une orientation à recouper avant les mandats, pas une autorisation d’écrire ces sources.

Le port C08 `InstallationPlanSource` fournit vérification du plan et des liaisons, résolution des cibles, inspection du résultat, staging et vérification du résultat. Son état durable appartient à C08. Une migration propriétaire sera présentée avant réalisation ; aucune table privée Core/Auth/C05 n’est lue ou écrite directement.

La transaction propriétaire commune réunit effets Core, stamp du credential Auth, consommation de l’autorisation, audit C05 et résultat C08. Alias, connexion, transaction et preuves staged sont recoupés par les ports existants. Aucun commit autonome du checkpoint ni callback booléen n’atteste cet ensemble. L’identité d’opération, l’installation, la version/digest du plan, les références de décision/résultat et l’état de première configuration sont persistés sans credential ni assertion brute.

Une opération confirmée est inspectée et restituée sans second effet après contrôles actuels. Une même identité avec plan divergent est un conflit. Une issue inconnue exige inspection avant tout rejeu. Une panne avant commit annule l’ensemble ; après commit, seule l’étape externe manquante est reprise.

### Marqueur externe et modes

Le marqueur d’installation est un fichier privé versionné, distinct du marqueur de désactivation Super Admin et du résultat PostgreSQL. Il contient seulement identité d’installation, référence/version du résultat confirmé et métadonnées de format minimisées. Son chemin et son propriétaire sont explicitement déclarés par la configuration protégée ; les valeurs de tests ne deviennent pas des défauts.

Lecture et écriture refusent symlink, type non régulier, propriétaire ou droits divergents, liens multiples, contenu hors bornes, champs inconnus et identité incohérente. Les fichiers sont privés en mode 0600 ; les parents sont contrôlés. La publication suit fichier temporaire privé dans le même répertoire, fsync du fichier, remplacement atomique puis fsync du répertoire. Aucun succès durable n’est annoncé après une étape inconnue.

Le marqueur n’est publié qu’après inspection du commit confirmé et est rapproché de l’installation et du résultat persistants. Son absence, invalidité ou divergence bloque NORMAL et ne déclenche jamais INSTALLER. Un marqueur valide avec première configuration inachevée conduit à FIRST_CONFIGURATION et à l’authentification propre du Super Admin existant. La finalisation autorisée et auditée de l’état en base précède NORMAL. MAINTENANCE conserve une transition explicite ; elle n’est pas une dispense d’autorisation.

### Secrets après INSTALLER — delta adopté

Le transport LoadCredentialEncrypted et les preuves réelles UID/unité/workload C01 sont conservés. Une politique versionnée distincte doit autoriser explicitement mode, rôle, finalité, références, versions, validités et délais ; aucun rôle ou mode supplémentaire n’est admis par simple présence d’une référence.

FIRST_CONFIGURATION, NORMAL et MAINTENANCE ne sont jamais présentés comme INSTALLER pour contourner le contrôle actuel. Leur résolution suit désormais le delta adopté ; son raccord réel reste à réaliser et qualifier. Avant accès PostgreSQL, une preuve d’audit technique durable indépendante de cette base est exigée. Après ouverture vérifiée, les événements de cette invocation sont importés idempotemment dans C05 et le relais est rapproché avant disponibilité ; panne, doublon, ancienne invocation, journal scellé et reprise doivent être qualifiés sans réouvrir ni purger silencieusement un journal.

Ce démarrage technique n’obtient aucun droit de création de base, compte, tenant ou privilège R01. Rotation, révocation et arrêt attesté des consommateurs restent opposables. Les gabarits purs restent inchangés.

L’installateur ne devient pas writer C01 : la publication externe contrôlée du credential par l’administrateur reste distincte, avec identité, autorisation et procédure déclarées. C08 reçoit uniquement la référence et vérifie la version effectivement résolue et sa correspondance avec la cible courante, sans exposer la valeur. Tant que cette étape n’est pas prouvée, il reste non prêt ; il ne conserve aucune saisie pour la rejouer.

### Gouvernance initiale — delta adopté

Une source serveur protégée doit fournir un profil versionné complet et l’attestation requise par `GovernanceProvider` pour les données créées. Propriétaire, source de vérité, classes, confidentialité, données personnelles, finalités, rétention, suppression, consommateurs, processeurs, résidence/transfert, export et lignée suivent `data-governance`. Références et politiques sont explicites et contrôlées ; aucune durée de rétention, propriétaire ou valeur métier de fixture n’est inventée.

L’attestation est liée aux cibles et à la transaction courante, puis revalidée avant commit. Profil absent, révoqué, périmé, incompatible ou partiellement décrit : aucune création Core ni disponibilité. Le compte encore inexistant ne peut fournir sa propre dispense. Le seul contrat minimal requis est coordonné avec C10 ; purge, droits de demandes et gouvernance globale C10 ne sont pas réalisés par ce lot.

### Recettes supplémentaires et retour au cycle

S01–S04 et G01–G03 de `requirements.md` complètent B01–B10 : modes/workloads autorisés ou refusés, audit pré-base et relais après crash, publication externe absente/divergente, profil de gouvernance frais ou invalide et rollback commun. Toutes sont non exécutées.

Le lot d’adoption exige UTF-8/LF, liens valides, validation OpenSpec ciblée stricte du change et des deux canons, ainsi que contrôle de l’absence d’écriture hors des six fichiers autorisés pour cette intégration. L’adoption et la mise en cohérence de .openspec.yaml sont autorisées séparément et documentées ci-dessus. Après validation documentaire de l’intégration, le contrôle revient au cycle CISMP et au premier jalon C08 non prouvé. Le code ne commence qu’après vérification des contrats et dépendances et cadrage des mandats CAB unitaires ; l’archive et les statistiques restent des étapes futures.


## Complément PA/PZT du 22 octobre 2026 — conception 1.3 proposée

### Portée et statut

Le développeur valide la formalisation du parcours PA/PZT → PostgreSQL → PBO, sur physique/VM et dans Docker Pixs. Cette section recadre la proposition antérieure R02 autonome, qui n’a pas été adoptée. Elle prépare huit deltas, sans modifier les canons ni annoncer une implémentation. Les quatre exigences déjà intégrées dans secrets-providers et installation-provisioning restent acquises. Les analyses antérieures qui exigeaient Auth PostgreSQL pour obtenir la connexion à cette même base décrivent la circularité à résoudre ; elles ne sont pas une recette positive.

### Responsabilités et séquence

1. Une procédure locale explicitement lancée par l’opérateur provisionne PA et PZT : identité propre de chaque exécutant, origine vérifiée, ancrages, configuration minimale, références externes et politique technique protégée/versionnée. Elle ne dépend pas de la base Pixs ni d’une session future. Le premier PBO n’est jamais approuvé par simple découverte. Les fichiers de provisionnement ne sont pas un canal de management PBO–PA.
2. Le PA système possède une capacité PostgreSQL du catalogue fermé livré. Sur physique/VM, il installe et configure le service dans le périmètre autorisé ; dans Docker, le logiciel est déjà fourni et PA vérifie puis initialise seulement les ressources absentes. Ses accès SQL sont techniques (service, rôle et base explicitement prévus), distincts de ceux des workloads applicatifs. PA initie la première connexion technique et atteste l’état constaté, sans lire les tables métier ni se substituer à leurs propriétaires.
3. Tout échange PBO–PA, y compris préparation, inspection, diagnostic et résultat locaux, passe par un profil PZT local mTLS provisionné et vérifié. Ce profil borne les actions, cibles, validités, anti-rejeu, révocations et preuves ; il n’ouvre aucun réseau distant ni permission métier. Si PZT manque, les échanges sont bloqués. Une réparation locale par opérateur reste une procédure distincte et auditée, jamais un canal de substitution PBO–PA.
4. Les secrets techniques et applicatifs sont publiés par une procédure externe autorisée, distincte du provider de lecture. Le mandat PA seul n’autorise pas un writer générique ; C08 non plus. PZT transporte des références et métadonnées minimisées, pas des credentials. Le provider remet les valeurs uniquement au consommateur vérifié. Le mot de passe d’un futur Super Admin reste traité dans son contrat Auth privé ; il n’est pas un credential de service PA.
5. PBO vérifie la cible préparée, ouvre sa connexion sous l’autorité technique minimale définie ci-dessous, puis inspecte le schéma et utilise les contrats propriétaires de migration. Les quatre états de base et leurs confirmations sont conservés. L’acte R01 Core/Auth/Super Admin/tenant, la gouvernance initiale et le résultat C08 restent sous les contrôles et la transaction applicatifs définis en 1.2.
6. Les preuves de préparation, d’audit et de résultat sont rapprochées avec les propriétaires persistants ; les mandats techniques temporaires sont terminés avant admission du management ordinaire. PostgreSQL reprend l’autorité des états de contrôle applicatifs. Il n’existe pas deux sources concurrentes d’autorisation métier. Le marqueur externe suit le commit confirmé et FIRST_CONFIGURATION conserve l’authentification propre du compte.

### Démarrages suivants et autorité technique minimale

La disponibilité de PA et de PZT et la remise de la connexion PBO ne doivent pas dépendre d’Auth dans la base qu’ils doivent ouvrir. Le delta authorization propose donc une branche technique explicite fondée sur le provisionnement opérateur et des identités natives vérifiées. Elle n’invente aucun DigitalIdentity ni ScopeContext tenant. Sa politique protégée vérifie rôle, mode réel, finalité, installation/cible, action fermée, référence/version, validité, révocation et audit ; une donnée manquante ou une fraîcheur non vérifiable refuse l’admission.

À chaque redémarrage, cette branche ne permet que les actes techniques indispensables et, pour PBO, la remise de ses seuls secrets de connexion avant ouverture. Les décisions métier, les autres résolutions exigeant une autorité applicative et le management ordinaire attendent C03/C04 et PostgreSQL courants. NORMAL n’est pas renommé INSTALLER. C01 n’acquiert aucune extension implicite et R01 n’est ni prolongé ni utilisable comme autorité permanente. Le transport LoadCredentialEncrypted demeure le choix Debian local, avec ses garanties, rotation et arrêt attesté ; un raccord Docker ne prouve pas leur équivalence et doit sélectionner/qualifier son mécanisme avant distribution.

L’audit technique pré-base est durable et indépendant, lié à l’invocation, au workload et à l’opération. Le relais C05 est idempotent, rapproché et confirmé avant disponibilité. Une panne d’audit ou une issue de relais inconnue maintient non prêt, sans purger l’historique ni prolonger un mandat périmé. Les contrôles restent exécutables sans accès préalable à la base Pixs.

### États, frontières transactionnelles et reprise

Les phases opérateur, préparation PA, connexion PBO, migrations, acte applicatif et marqueur ont des propriétaires et résultats distincts. Le reçu PA porte opération, version/digest du plan, cible, état observé, résultat et métadonnées minimales, sans secret. Il n’atteste aucun commit Core/Auth. Un effet externe sur service, rôle ou base n’est pas atomique avec la transaction Core/Auth/C05/C08.

Après interruption, chaque propriétaire inspecte son état durable et la cible avant de poursuivre. Une issue inconnue est réconciliée avant rejeu. La même opération conforme est restituée sans duplication ; un plan divergent est refusé. Une compensation ne détruit aucune donnée existante sans un nouveau plan destructif explicitement autorisé. Un commit applicatif confirmé ne déclenche jamais de seconde création pour réparer un marqueur perdu. Le cluster Docker existant est conservé à chaque redémarrage et les réplicas n’en deviennent pas des propriétaires concurrents.

### Composition, Docker et qualification

Le parcours sélectionne explicitement PA système et PZT local. Réseau distant désactivé ne signifie pas PZT local absent. Le profil initial Debian doit être révisé et qualifié avec ces exécutants ; les profils ne les sélectionnant pas gardent leurs limites et ne revendiquent pas ce parcours. Les modes de session PA et le réseau distant ne sont pas activés par ce choix.

L’image Docker fournit le logiciel PostgreSQL, PBO/PFO et les exécutants PA/PZT déjà prévus ; ni cluster préinitialisé ni données, identité ou secret effectifs ne sont dans les couches. Le stockage PostgreSQL est persistant hors image et hors couche éphémère. Le profil d’exécution sélectionne les processus et déclare supervision, ordre, signaux, budgets communs, cible de persistance et propriétaire unique de préparation. Une réplication ne clone pas d’identité ni de propriétaire PZT/base. Aucun montage ou droit réel n’est modifié par cette conception.

Après adoption normative, BUILD §14 et §23 devront distinguer logiciel PostgreSQL inclus et données persistantes externes à l’image ; PROJECT et TECHNICAL devront renvoyer aux mêmes responsabilités. La sélection du mécanisme de secrets Docker, les paramètres de confiance et de fraîcheur, les versions/architectures, quotas et recettes réelles restent à déclarer et vérifier avant qualification, sans prendre une valeur de fixture pour un défaut d’exploitation.

### Vérification et décision suivante

Les cas P01–P10 de requirements.md précisent les preuves futures. Le lot documentaire est limité aux quatre documents C08, huit deltas et commentaire de .openspec.yaml. Il conserve schema/created, les canons et le code. Une validation OpenSpec stricte et les contrôles d’empreintes/UTF-8/LF/liens vérifient la préparation documentaire seulement. La revue de l’intégration des clauses modifiées et ajoutées précède leur adoption canonique ; aucun nouveau change, déploiement ou archivage n’est lancé.
