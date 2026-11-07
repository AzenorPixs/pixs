# Conception — C08

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Installation pré-domaine, amorçage technique distinct puis transition Domaine raccordée à C97/C96 ; le transfert ne réactive pas les anciennes identités.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [installation-provisioning](../../specs/installation-provisioning/spec.md).
- [initial-administration](../../specs/initial-administration/spec.md).
- [pixs-instance](../../specs/pixs-instance/spec.md).
- [zt-pki](../../specs/zt-pki/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## État courant — adoption C08 du 22 octobre 2026

La conception 1.3 et ses huit deltas sont adoptés au canon : six exigences nouvelles, six modifiées, vingt-sept scénarios nets (dont quatre de présentation des garanties) ; les quatre ajouts précédents restent acquis. PROJECT, TECHNICAL et BUILD sont alignés. Les étapes antérieures datées conservent leurs preuves et limites historiques ; les passages qui attendaient cette adoption ne sont plus des barrières normatives actuelles. Les choix de paramètres, providers et recettes demeurent des prérequis de réalisation. Aucun code, service, migration réelle ou qualification produit n’est livré par cette adoption.

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

### Précisions opératoires de la tâche 1.2

Le raccord privé C08 conserve trois rôles de digest : le digest du plan protégé est porté par `BootstrapOperatorFacts.plan_sha256` et signé par C03 ; `BootstrapActInput.content_sha256` et `CommandEnvelope.content_sha256` décrivent le contenu fermé et versionné de l’acte ; le challenge C03 provient de `canonical_bootstrap_bytes` et reste distinct. `check_act_binding` ne compare que les dix liaisons communes et ne réalise pas ce pont de digest. Le producteur C08 `InstallationPlanSource` doit recalculer le digest du plan protégé pour le comparer aux faits signés, vérifier le digest du contenu fermé attendu contre l’acte et l’enveloppe, et vérifier cibles, version, confirmations et effets fermés. Son `verify_operator_binding` est refusant par défaut ; il doit être réalisé par C08 avant le parcours positif. Aucune égalité des deux digests n’est ajoutée au contrat générique Core ; D01–D04 restent inchangés. Un plan inconnu, substitué, un contenu divergent ou un port absent refuse avant effet.

La revue de 1.2 ne trouve aucun éditeur de `AuthBootstrapAuthorization` dans les sources applicatives : `AuthBootstrapBackend._row` consomme une ligne ACTIVE ; `BootstrapProofSource`, `BootstrapTrustPolicySource` et `BootstrapClassificationSource` ne font que résoudre leurs données. Le point d’entrée propriétaire Auth prévu est `src/pixs/auth/bootstrap_authorization.py`, à réaliser dans le raccord R01 de 2.3 avant ce consommateur, jamais par accès ORM privé C08 ni SQL administratif de contournement. Le contrat de conception retenu reçoit des faits attendus issus du plan serveur protégé, la preuve Ed25519 et son nonce, la politique courante préautorisée, la classification obligatoire, le credential préparé privé, l’alias et l’horloge. Le propriétaire vérifie opérateur, cibles, plan, effets et autorisation R01 fermée et fraîche ; il publie une autorité traçable et auditée et ne retourne que les références opaques utilisables par le backend public Auth. Une divergence est un conflit, un rejeu identique ne crée pas de seconde autorité et la fenêtre finale de 600 secondes n’est pas prolongée. La publication préparatoire ne vaut ni consommation ni commit de l’acte : la consommation reste liée au commit commun Core/Auth/C05/C08. UID 0, clé fournie par l’appelant ou booléen ne constituent pas une autorisation. Les providers de lecture demeurent distincts de cet éditeur à réaliser.

Le plan, le checkpoint, le résultat et le marqueur restent propriétaires C08 ; identité et données Core restent C02, autorité et credential C03, décision C04, audit C05 et attestation de gouvernance C10. Les fichiers privés C08 déjà identifiés ci-dessous et le point d’entrée Auth prévu sont des cibles de réalisation futures à présenter par mandat avant code. Chemins, propriétaires natifs, ancrages et bornes obligatoires proviennent d’une configuration protégée sans défaut de production issu des fixtures ; leurs valeurs et leur qualification ne sont pas fabriquées par cette conception.

### Précisions opératoires de la tâche 1.3

La politique du workload PBO, versionnée, protégée et relue à chaque usage, conserve INSTALLER et n'admet FIRST_CONFIGURATION/NORMAL/MAINTENANCE que si explicitement sélectionnés. Elle lie mode, workload PBO vérifié, UID/unité natifs, rôle fermé existant, finalité connexion, cible installation/base, références opaques, versions credential/politique, validités, révocation, bornes max_ttl/max_revocation/max_stop/max_restart/max_event/max_journal/max_credential, journal pré-base, rétention/holds et audit. Aucun rôle ni prestataire nouveau par défaut. Les identités et politiques PA/PZT restent distinctes sous branche authorization PA/PZT PLATFORM sans tenant/scope, sans DigitalIdentity/ScopeContext métier, sans appel C03/C04/Auth sur la base à ouvrir. UID 0, proximité, clé ou reçu C01 seuls ne suffisent jamais. Donnée obligatoire manquante, politique absente/périmée/révoquée, fraîcheur invérifiable, référence divergente, version non publiée, consommateur non vérifié ou reçu durable manquant gardent le composant non prêt, en échec fermé sans secret ni valeur par défaut ; NORMAL n’est jamais réétiqueté INSTALLER.

L'exception canonique du Super Admin existant est conservée. Une dispense éventuelle ne vaut jamais preuve d'import ni suppression du relais confirmé avant disponibilité.

Pont sans circularité : avant PG seul l'audit technique C01 OPEN lié invocation + workload + opération, append + verify_receipt avant remise. La création R01 s'exécute dans la transaction Core/Auth/C05/C08 avec son audit métier C05 propre, distinct du journal C01. Après commit C08 inspecté, le compte actif authentifié C03 avec binding unique C02 courant porte l'autorité applicative courante. Le Catalogue serveur C07 déclare action pixs.core.audit.bootstrap_import, ressource bootstrap-journal:<id> et ownership C05 PLATFORM ; la politique/version courante C04, factsProvider/decider propriétaires et gouvernance C10 fournissent faits et décision. Après ouverture, la procédure autorisée scelle le journal à rétention et holds identiques. Le lot complet conserve ordre, séquences et empreintes ; l'import C05 est idempotent sous allow et published_profile frais, puis revalidés sous verrous avant commit. verify_committed_import vérifie le marqueur de lot et les événements ou tombstones attendus par connexion indépendante sur la même base, avant disponibilité. R01 ne donne pas l'action d'import et le compte futur ne vaut aucune autorité anticipée. Le raccord et le catalogue réels sont réalisation future 2.5/2.7, C07 composition, C04 décision, C05 import ; aucune autorisation automatique dérivée de C01/R01 ni état ready requis pour l'authentification CLI restreinte.

Un journal SEALED n'est jamais rouvert, purgé ni réécrit. L'invocation suivante utilise un journal neuf créé par procédure externe autorisée, jamais par resolve, après conservation et identification du précédent et de son état de relais. Un ancien journal scellé encore en attente est préservé puis rapproché après ouverture par la nouvelle invocation auditée, avant disponibilité, sans exiger un import PostgreSQL déjà confirmé pour obtenir la connexion nécessaire à cette reprise. Après seal, toute consommation sur ce journal refuse ; la nouvelle invocation exige ses propres preuves natives, sa politique courante et son audit. Aucun ancien mandat ni copie de secret ne prolonge l'accès.

La publication externe suit l'ordre : identité et autorisation vérifiées, credentials par canal privé hors LLM, validation cible/version, préparation privée des nouvelles sources chiffrées et politiques protégées, arrêt attesté des consommateurs (ou absence vérifiée pour une publication initiale), remplacement atomique cohérent avec fsync, redémarrage contrôlé et vérification du consommateur. Aucun remplacement actif ne précède cet arrêt attesté. PA ne devient pas writer générique et C08 ne devient pas writer. PZT ne porte que références et métadonnées minimisées. C08 remplace les saisies par références, vérifie version/cible courante, ne conserve que références non secrètes. S01 modes/workloads/finalités autorisés/refusés, S02 audit pré-base + relais après crash, S03 publication absente/divergente non prête, S04 cycle C01 sans bypass, P05 seule remise connexion PBO en NORMAL sans Auth préalable, P06 publication/consommateur vérifiés avec audit/relais rapprochés.

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


### Réalisation partielle 2.1 — plan privé, à tester

`src/pixs/backend/installation/plan.py` et `tests/unit/test_installation_plan.py` sont écrits sous CAB. Ils fournissent la structure privée fermée `InstallationPlan`, sa sérialisation JSON UTF-8 déterministe, le SHA-256 recalculé sur les seuls octets canoniques, le parseur strict et les liaisons structurelles aux faits/confirmations. Aucun stockage protégé du plan, checkpoint, éditeur d'autorité ou résultat PostgreSQL n'est fourni par ce sous-lot.

`PlanLimits` exige `max_bytes`, `max_ref_len`, `max_effects`, `allowed_schema_versions` et `allowed_plan_versions`, fournis par la composition protégée sans valeur de production inventée. Les cibles réutilisent `BootstrapTargetSpec` et les UUIDv7/enums Core exacts ; effets fermés de `BOOTSTRAP_EFFECTS`, types, références, versions et bornes sont contrôlés sans coercition. Plan, installation/base, opération, acteur, cibles, effets et intention opaque de credential sont liés. Le plan ne sérialise ni son propre digest, ni signature, preuve brute, résultat de confirmation, mot de passe ou empreinte de mot de passe.

Le lien de confirmation est séparé du digest : un changement du plan invalide sa liaison. Le pont avec `BootstrapOperatorFacts` recalcule le digest et compare notamment opération, installation, version, opérateur, cibles et effets. Ce contrôle structurel ne vérifie pas une signature et n'accorde aucune autorisation ; les propriétaires C03/C04 conservent vérification cryptographique, validité finale de 600 secondes et décision/revalidation. Le format reste privé C08 ; il ne devient pas une API de plan technique PA.

Syntaxe et tests ne sont pas exécutés à ce stade. Les recettes préparées couvrent déterminisme, schéma fermé/auto-référence, JSON ambigu, types et bornes, cibles et effets, réutilisation sans reset, liaison des confirmations et recomposition du digest. Les fichiers ne réalisent pas l'acte R01 ni un provider de confiance déployé. La tâche 2.1 demeure incomplète et non cochée.


### Réalisation partielle 2.1 — marqueur privé, à tester

Le sous-lot fichier est écrit dans `src/pixs/backend/installation/marker.py`, avec ses recettes `tests/unit/test_installation_marker.py`. Cette réalisation partielle ne valide pas 2.1 : plan/checkpoint, résultat transactionnel PostgreSQL, sélection des modes et lecteur propriétaire réel restent à réaliser ou raccorder. La syntaxe et les tests n'ont pas encore été exécutés ; ils appartiennent à la seconde phase demandée par le développeur.

`MarkerConfig` reçoit obligatoirement `path`, `owner_uid`, `owner_gid`, `max_bytes`, `max_ref_len`, `allowed_format_versions` et `parent_identities` depuis la composition protégée. Aucun chemin, propriétaire, taille, format admis ou identité native de production ne possède de valeur initiale inventée. `parent_identities` fixe les couples UID/GID admis pendant le parcours des parents ; le dernier parent reste privé en 0700, et le fichier en 0600 avec un lien unique. Ces contrôles techniques ne valent ni identité opérateur ni permission métier.

Le schéma privé fermé contient seulement `format_version`, `installation_ref`, `result_ref` et `result_version`. Les références et la taille sont bornées ; types stricts, champs inconnus, clés JSON dupliquées et constantes non finies sont refusés. Les parents et fichiers sont ouverts par descripteurs sans suivi de liens ; types, identités, droits, liens et empreintes d'observation sont rapprochés. Un FIFO ne provoque pas d'ouverture bloquante.

L'entrée de publication consomme le port privé `ConfirmedResultSource.guard_confirmed`, fourni par la composition serveur : son propriétaire doit inspecter un résultat committé et conserver l'exclusion interprocessus sur l'installation jusqu'à la fin des fsync et de la relecture. Un DTO, un booléen ou un verrou mémoire ne remplace pas ce lecteur. Son implémentation PostgreSQL n'est pas fournie par le sous-lot fichier. La publication utilise un temporaire exclusif dans le parent épinglé, fsync du fichier, remplacement atomique et fsync du répertoire ; un résultat divergent ne remplace pas le marqueur existant. Une panne de durabilité ou une substitution constatée conserve une issue inconnue à réconcilier, sans annoncer succès ou rollback.

Les recettes préparées utilisent le filesystem réel sous `output/tests/c08-marker/` et des doubles limités au contrat du lecteur. Elles couvrent lectures/refus, idempotence/divergence, types/liens/droits/parents, schéma et bornes, garde maintenue et interruptions de fsync/remplacement. Elles ne qualifient ni le commit PostgreSQL ni l'acte Core/Auth et restent à exécuter. Aucun état NORMAL, INSTALLER ou disponibilité n'est déduit de ce fichier seul.

### Secrets après INSTALLER — delta adopté

Le transport LoadCredentialEncrypted et les preuves réelles UID/unité/workload C01 sont conservés. Une politique versionnée distincte doit autoriser explicitement mode, rôle, finalité, références, versions, validités et délais ; aucun rôle ou mode supplémentaire n’est admis par simple présence d’une référence.

FIRST_CONFIGURATION, NORMAL et MAINTENANCE ne sont jamais présentés comme INSTALLER pour contourner le contrôle actuel. Leur résolution suit désormais le delta adopté ; son raccord réel reste à réaliser et qualifier. Avant accès PostgreSQL, une preuve d’audit technique durable indépendante de cette base est exigée. Après ouverture vérifiée, les événements de cette invocation sont importés idempotemment dans C05 et le relais est rapproché avant disponibilité ; panne, doublon, ancienne invocation, journal scellé et reprise doivent être qualifiés sans réouvrir ni purger silencieusement un journal.

Ce démarrage technique n’obtient aucun droit de création de base, compte, tenant ou privilège R01. Rotation, révocation et arrêt attesté des consommateurs restent opposables. Les gabarits purs restent inchangés.

L’installateur ne devient pas writer C01 : la publication externe contrôlée du credential par l’administrateur reste distincte, avec identité, autorisation et procédure déclarées. C08 reçoit uniquement la référence et vérifie la version effectivement résolue et sa correspondance avec la cible courante, sans exposer la valeur. Tant que cette étape n’est pas prouvée, il reste non prêt ; il ne conserve aucune saisie pour la rejouer.

### Gouvernance initiale — delta adopté

Une source serveur protégée doit fournir un profil versionné complet et l’attestation requise par `GovernanceProvider` pour les données créées. Propriétaire, source de vérité, classes, confidentialité, données personnelles, finalités, rétention, suppression, consommateurs, processeurs, résidence/transfert, export et lignée suivent `data-governance`. Références et politiques sont explicites et contrôlées ; aucune durée de rétention, propriétaire ou valeur métier de fixture n’est inventée.

L’attestation est liée aux cibles et à la transaction courante, puis revalidée avant commit. Profil absent, révoqué, périmé, incompatible ou partiellement décrit : aucune création Core ni disponibilité. Le compte encore inexistant ne peut fournir sa propre dispense. Le seul contrat minimal requis est coordonné avec C10 ; purge, droits de demandes et gouvernance globale C10 ne sont pas réalisés par ce lot.

#### Contrat minimal 1.4 — catalogue local protégé hors base à ouvrir (CHOIX VALIDÉ)

> Choix Q1.4-GOV-SOURCE validé par le développeur : catalogue TOML local protégé et raccord minimal propriétaire C10, consommé C08 en 2.6. Choix adopté sans réalisation ni provider déployé. Aucune table privée C08 ne vaut autorité C10. Purge et demandes C10 globales hors périmètre.

Contrat consommation C08 existant conservé : `GovernanceProvider` reste `C10 seul` (`ports.py`), `GovernanceAttestation` exacte (`dto.py`), `published_profile` sous verrous (`services_common.py`), `DEROGATION_BOOTSTRAP_REFUSEE` si `CREATE_IDENTITY` (`services_bootstrap.py`), `classification/result_ref/payload ⊆ resource_refs` + `verify_staged` + recheck `policy_version` (`services_transactions.py`). Aucun contrat C02 modifié, aucun DTO ajouté.

Tableau 15 champs `DataGovernanceProfile` — exigence/source/propriétaire :

| Champ | Exigence | Source exigible | Propriétaire |
|---|---|---|---|
| `profile_version` | SemVer 2.0.0 complète exacte | déclaration composant, catalogue protégé | C10 |
| `data_asset_id` | référence opaque exacte non vide | déclaration composant, catalogue protégé | `pixs.core` pour données bootstrap Core |
| `owner_component` | `str` exact, `pixs.core` exigé pour bootstrap Core par `published_profile` | déclaration composant | `pixs.core` |
| `source_of_truth` | référence opaque exacte non vide | déclaration composant, catalogue protégé | C10 |
| `data_classes` | `frozenset` exact `str` non vides | déclaration composant | C10 |
| `confidentiality` | membre canonique `ConfidentialityLevel` identité `is` | déclaration du composant utilisant les dimensions canoniques de `data-governance` | C10 |
| `personal_data` | membre canonique `PersonalDataLevel` identité `is` | déclaration du composant utilisant les dimensions canoniques de `data-governance` | C10 |
| `purpose_refs` | `frozenset` exact `str` non vides | déclaration composant | C10 |
| `retention_policy` | référence opaque exacte, sans durée inventée ici | déclaration composant, à qualifier C10 | C10 |
| `deletion_policy` | référence opaque exacte | déclaration composant, à qualifier C10 | C10 |
| `residency_constraints` | `frozenset` exact `str` non vides | déclaration composant | C10 |
| `authorized_consumers` | `frozenset` exact `str` non vides, `consumer ∈` contrôlé si outbox | déclaration composant | C10 |
| `processor_refs` | `frozenset` exact `str` non vides | déclaration composant | C10 |
| `export_policy` | référence opaque exacte | déclaration composant | C10 |
| `lineage` | référence opaque exacte | déclaration composant | C10 |

Les composants conservent la propriété et la déclaration de leurs données ; C10 authentifie leur publication et atteste leur cohérence, sans autorité métier nouvelle. Ce tableau porte le profil Core pour l’attestation C02. Les classifications Auth, C05 et C08 restent sous leurs propriétaires respectifs et sont rapprochées de leurs propres profils ; aucune propriété de données C03 n’est transférée à Core.

Cibles/opération liées par reçus privés C10 : `request.resource_id=bootstrap_ref(installation)` + `payload_refs` ⊆ `attestation.resource_refs`, `context PLATFORM == attestation.context`, `operation_id/alias/transaction_token` liés par `StagedRef stage_read/authorize_state_change` + `verify_staged` dans même `TransactionProof`, même connexion physique et savepoints via transaction propriétaire `execute_mutation`. Pas d’ajout DTO.

Source/validité/révocation/TTL obligatoires : catalogue local protégé hors base à ouvrir, format TOML avec parseur standard Python existant sans dépendance nouvelle, chemin/ancrage/propriétaire/validités/références déclarés par configuration protégée sans valeurs prod inventées. Publication exclusive par opérateur autorisé distinct à partir profils déclarés par composants, sur garde stable. `attest` en lecture partagée, profil épinglé `published_version==profile_version` jusque barrière commit. Révocations/version/fraîcheur recontrôlées sous verrous avant commit, avec protection publication concurrente : l’éditeur acquiert une garde exclusive stable après fin des lecteurs protégés par commit ou rollback, dans une borne d’attente obligatoire, puis publie par remplacement atomique avec fsync et relecture. La garde partagée de l’attestation est liée à la transaction et sa libération est garantie ; toute divergence de version, validité ou révocation refuse. Aucune exigence d’arrêt des consommateurs C01 ni extension des droits d’infrastructure n’est déduite de cette publication C10.

Revalidation avant commit : `lock_scopes → allow under_locks → attest frais → MutationContext → apply → verify_staged gouvernance → recheck policy_version`, sinon refus fermé `GOUVERNANCE_ABSENTE/ATTESTATION_INVALIDE,DIVERGENTE,FUTURE/GOUVERNANCE_DIVERGENTE/RESSOURCE_NON_COUVERTE/PAYLOAD_NON_COUVERT/VERSION_DIVERGENTE`. Rollback/reprise `G01-G03` : panne avant commit annule tout, après commit seule étape externe manquante reprise, issue inconnue `restore_only` + réconciliation, sans seconde création, sans dispense futur compte. Exceptions Super Admin existantes conservées dans leur seul périmètre canonique, distinctes des profils purs.

Choix développeur adopté : catalogue local protégé + adaptateur minimal propriétaire C10 pour `attest/verify_staged`, consommé C08 en `2.6` sans réaliser purge/demandes/effacement C10 globaux. Chemin, ancrage, propriétaire, TTL/fraîcheur, révocation, versions épinglées et procédure opérateur restent à fournir/qualifier avant réalisation, sans exiger ici 15 valeurs prod ni secret.

### Recettes supplémentaires et retour au cycle

S01–S04 et G01–G03 de `requirements.md` complètent B01–B10 : modes/workloads autorisés ou refusés, audit pré-base et relais après crash, publication externe absente/divergente, profil de gouvernance frais ou invalide et rollback commun. Toutes sont non exécutées.

Le lot d’adoption exige UTF-8/LF, liens valides, validation OpenSpec ciblée stricte du change et des deux canons, ainsi que contrôle de l’absence d’écriture hors des six fichiers autorisés pour cette intégration. L’adoption et la mise en cohérence de .openspec.yaml sont autorisées séparément et documentées ci-dessus. Après validation documentaire de l’intégration, le contrôle revient au cycle CISMP et au premier jalon C08 non prouvé. Le code ne commence qu’après vérification des contrats et dépendances et cadrage des mandats CAB unitaires ; l’archive et les statistiques restent des étapes futures.


## Complément PA/PZT du 22 octobre 2026 — conception 1.3 adoptée

### Portée et statut

Le parcours PA/PZT → PostgreSQL → PBO est adopté sur physique/VM et dans Docker Pixs. Cette section recadre la proposition antérieure R02 autonome, qui n’a pas été adoptée. Les huit deltas sont intégrés aux canons, sans implémentation. Les quatre exigences déjà présentes dans secrets-providers et installation-provisioning restent acquises. Les analyses antérieures qui exigeaient Auth PostgreSQL pour obtenir la connexion à cette même base décrivent la circularité désormais traitée par la branche technique normative ; elles ne sont pas une recette positive.

### Responsabilités et séquence

1. Une procédure locale explicitement lancée par l’opérateur provisionne PA et PZT : identité propre de chaque exécutant, origine vérifiée, ancrages, configuration minimale, références externes et politique technique protégée/versionnée. Elle ne dépend pas de la base Pixs ni d’une session future. Le premier PBO n’est jamais approuvé par simple découverte. Les fichiers de provisionnement ne sont pas un canal de management PBO–PA.
2. Le PA système possède une capacité PostgreSQL du catalogue fermé livré. Sur physique/VM, il installe et configure le service dans le périmètre autorisé ; dans Docker, le logiciel est déjà fourni et PA vérifie puis initialise seulement les ressources absentes. Ses accès SQL sont techniques (service, rôle et base explicitement prévus), distincts de ceux des workloads applicatifs. PA initie la première connexion technique et atteste l’état constaté, sans lire les tables métier ni se substituer à leurs propriétaires.
3. Tout échange PBO–PA, y compris préparation, inspection, diagnostic et résultat locaux, passe par un profil PZT local mTLS provisionné et vérifié. Ce profil borne les actions, cibles, validités, anti-rejeu, révocations et preuves ; il n’ouvre aucun réseau distant ni permission métier. Si PZT manque, les échanges sont bloqués. Une réparation locale par opérateur reste une procédure distincte et auditée, jamais un canal de substitution PBO–PA.
4. Les secrets techniques et applicatifs sont publiés par une procédure externe autorisée, distincte du provider de lecture. Le mandat PA seul n’autorise pas un writer générique ; C08 non plus. PZT transporte des références et métadonnées minimisées, pas des credentials. Le provider remet les valeurs uniquement au consommateur vérifié. Le mot de passe d’un futur Super Admin reste traité dans son contrat Auth privé ; il n’est pas un credential de service PA.
5. PBO vérifie la cible préparée, ouvre sa connexion sous l’autorité technique minimale définie ci-dessous, puis inspecte le schéma et utilise les contrats propriétaires de migration. Les quatre états de base et leurs confirmations sont conservés. L’acte R01 Core/Auth/Super Admin/tenant, la gouvernance initiale et le résultat C08 restent sous les contrôles et la transaction applicatifs définis en 1.2.
6. Les preuves de préparation, d’audit et de résultat sont rapprochées avec les propriétaires persistants ; les mandats techniques temporaires sont terminés avant admission du management ordinaire. PostgreSQL reprend l’autorité des états de contrôle applicatifs. Il n’existe pas deux sources concurrentes d’autorisation métier. Le marqueur externe suit le commit confirmé et FIRST_CONFIGURATION conserve l’authentification propre du compte.

### Démarrages suivants et autorité technique minimale

La disponibilité de PA et de PZT et la remise de la connexion PBO ne doivent pas dépendre d’Auth dans la base qu’ils doivent ouvrir. La capacité authorization définit donc une branche technique explicite fondée sur le provisionnement opérateur et des identités natives vérifiées. Elle n’invente aucun DigitalIdentity ni ScopeContext tenant. Sa politique protégée vérifie rôle, mode réel, finalité, installation/cible, action fermée, référence/version, validité, révocation et audit ; une donnée manquante ou une fraîcheur non vérifiable refuse l’admission.

À chaque redémarrage, cette branche ne permet que les actes techniques indispensables et, pour PBO, la remise de ses seuls secrets de connexion avant ouverture. Les décisions métier, les autres résolutions exigeant une autorité applicative et le management ordinaire attendent C03/C04 et PostgreSQL courants. NORMAL n’est pas renommé INSTALLER. C01 n’acquiert aucune extension implicite et R01 n’est ni prolongé ni utilisable comme autorité permanente. Le transport LoadCredentialEncrypted demeure le choix Debian local, avec ses garanties, rotation et arrêt attesté ; un raccord Docker ne prouve pas leur équivalence et doit sélectionner/qualifier son mécanisme avant distribution.

L’audit technique pré-base est durable et indépendant, lié à l’invocation, au workload et à l’opération. Le relais C05 est idempotent, rapproché et confirmé avant disponibilité. Une panne d’audit ou une issue de relais inconnue maintient non prêt, sans purger l’historique ni prolonger un mandat périmé. Les contrôles restent exécutables sans accès préalable à la base Pixs.

### États, frontières transactionnelles et reprise

Les phases opérateur, préparation PA, connexion PBO, migrations, acte applicatif et marqueur ont des propriétaires et résultats distincts. Le reçu PA porte opération, version/digest du plan, cible, état observé, résultat et métadonnées minimales, sans secret. Il n’atteste aucun commit Core/Auth. Un effet externe sur service, rôle ou base n’est pas atomique avec la transaction Core/Auth/C05/C08.

Après interruption, chaque propriétaire inspecte son état durable et la cible avant de poursuivre. Une issue inconnue est réconciliée avant rejeu. La même opération conforme est restituée sans duplication ; un plan divergent est refusé. Une compensation ne détruit aucune donnée existante sans un nouveau plan destructif explicitement autorisé. Un commit applicatif confirmé ne déclenche jamais de seconde création pour réparer un marqueur perdu. Le cluster Docker existant est conservé à chaque redémarrage et les réplicas n’en deviennent pas des propriétaires concurrents.

### Composition, Docker et qualification

Le parcours sélectionne explicitement PA système et PZT local. Réseau distant désactivé ne signifie pas PZT local absent. Le profil initial Debian doit être révisé et qualifié avec ces exécutants ; les profils ne les sélectionnant pas gardent leurs limites et ne revendiquent pas ce parcours. Les modes de session PA et le réseau distant ne sont pas activés par ce choix.

L’image Docker fournit le logiciel PostgreSQL, PBO/PFO et les exécutants PA/PZT déjà prévus ; ni cluster préinitialisé ni données, identité ou secret effectifs ne sont dans les couches. Le stockage PostgreSQL est persistant hors image et hors couche éphémère. Le profil d’exécution sélectionne les processus et déclare supervision, ordre, signaux, budgets communs, cible de persistance et propriétaire unique de préparation. Une réplication ne clone pas d’identité ni de propriétaire PZT/base. Aucun montage ou droit réel n’est modifié par cette conception.

BUILD §14 et §23 distinguent désormais logiciel PostgreSQL inclus et données persistantes externes à l’image ; PROJECT et TECHNICAL renvoient aux mêmes responsabilités adoptées. Les choix D1–D3 ci-dessous déclarent le mécanisme Docker, les cibles et la supervision ; les paramètres de confiance et de fraîcheur, dépendances verrouillées, quotas et recettes réelles restent à fournir et vérifier avant qualification, sans prendre une valeur de fixture pour un défaut d’exploitation.

#### Profils 1.5 — trois arbitrages adoptés le 23 octobre 2026

> Décision explicite du développeur : « Valider les trois choix et le lot documentaire ». D1–D3 et les dix fichiers ci-dessous sont adoptés ; aucune image, installation, infrastructure ou implémentation n’est produite. La tâche 1.5 reste ouverte jusqu’à validation technique de ses preuves et cochage distinct. Les choix déjà adoptés PBO Nuitka standalone, PA/PZT Cython, PA système et PZT local mTLS sont conservés.

Les deux profils gardent PostgreSQL distinct du processus PBO. Sur physique/VM, PA prépare le service et initie sa première connexion technique ; dans Docker, le logiciel est fourni sans cluster et PA initialise uniquement le stockage manquant. PBO possède ses migrations et l’acte R01. Tous les échanges PBO–PA passent par PZT ; l’absence de réseau distant n’enlève pas ce transport local. Debian colivre trois binaires PA et PZT ; Docker contient seulement les deux binaires PA système/événements et PZT, sans sessions utilisateur. Un rôle applicatif PBO par conteneur peut avoir plusieurs processus bornés ; leur nombre n’est pas le nombre de binaires.

Les contrats PA01/C14 et les références de build restent des prérequis à recouper. Leurs décisions documentaires, les profils purs, le relevé DEVOPS et les preuves C00 sans PA/PZT ne qualifient aucun exécutant actuel.

| Arbitrage | Choix adopté | Alternative et conséquences |
|---|---|---|
| D1 — Cibles et base | Première qualification Debian 13 x86_64 sur physique/VM et Docker Linux amd64. Candidat Docker Official Image `postgres:16.15-trixie`, par digest immutable à résoudre et verrouiller avant build. CPython 3.14.9 avec GIL et Cython 3.3.0 sont les candidats PA01 à qualifier ; minimum Python >=3.12 conservé, dépendances Django/psycopg selon pyproject. Versions Nuitka, ABI et bibliothèques sont figées par les propriétaires de build avant recette. | Une base Debian 13-slim avec PostgreSQL 16 fourni par une source de paquets explicitement déclarée impose sa propre fermeture de dépendances et de confiance. Une autre architecture étend la matrice de qualification. Windows/LXC/arm64 restent hors de cette première recette, sans supprimer leur périmètre de conception produit. |
| D2 — Supervision Docker | Init Docker `--init` et `supervisord` au premier plan, paquet Debian trixie `supervisor 4.2.5-3` et dépendances système verrouillées : **nouvelle dépendance adoptée pour l’image seulement, non installée**. La supervision systemd du profil Debian local est conservée. | systemd dans Docker demanderait son profil propre de cgroups et de droits ; un superviseur interne demanderait une réalisation et des preuves spécifiques. Aucun choix ne dispense du lifecycle Pixs, de ses admissions, des limites, des signaux et de la readiness. |
| D3 — Secrets Docker | Fournisseur Docker explicitement distinct de C01 systemd, transport de fichiers versionnés montés en lecture seule au runtime sous Compose/Linux, publication externe contrôlée, preuve native du workload, politique fraîche et contrôleur de lifecycle à réaliser et qualifier. Aucun secret par environnement, argv ou message PZT. | Un autre fournisseur externe demanderait son contrat et sa qualification. Reporter ce choix laisse le profil Docker non prêt. La seule présence d’un fichier, un UID ou une assertion appelante ne suffit pas à choisir ou qualifier un fournisseur. |

D1 vise une base qui fournit déjà le logiciel PostgreSQL. Son tag et ses architectures sont publiés dans le [registre Docker Official Images](https://github.com/docker-library/official-images/blob/master/library/postgres). Ce n’est ni une image Pixs construite ni un digest actuellement vérifié. Le [Dockerfile de référence consulté](https://github.com/docker-library/postgres/blob/9d15534160ade17f2b6c455a39ee967c49b1937d/16/trixie/Dockerfile) comporte ENTRYPOINT, CMD, STOPSIGNAL et VOLUME hérités : la construction Pixs devra les traiter explicitement. L’entrypoint PostgreSQL d’origine ne doit pas initialiser le cluster. Seuls une cible et un stockage persistant déclarés sont admis ; un volume anonyme créé accidentellement ne prouve pas leur admission. PostgreSQL 16.14 inventorié dans DEVOPS décrit un environnement local à vérifier, distinct du candidat Docker 16.15 ; ce choix ne migre ni ne réinstalle un serveur existant.

D2 utilise les possibilités documentées de [gestion de plusieurs processus Docker](https://docs.docker.com/engine/containers/multi-service_container/), du [paquet Debian](https://packages.debian.org/trixie/supervisor) et des [signaux et groupes Supervisor](https://supervisord.org/configuration.html). Le choix d’un gestionnaire ne constitue pas une preuve de readiness. PZT/PA sont admis sous leurs politiques ; PostgreSQL ne démarre qu’après la préparation autorisée de PA ; PBO vérifie sa connexion, réalise ses opérations propriétaires et rapproche les audits avant disponibilité. L’arrêt draine PBO avant la fermeture PostgreSQL, avec canaux PA/PZT conservés aussi longtemps que leurs étapes déclarées le nécessitent. PBO et PostgreSQL ont des comptes dédiés non root ; droits PA/supervision, signaux, comptes et répertoires sont déclarés et testés. Aucun serveur de contrôle HTTP public, mode privilégié, socket Docker, namespace hôte, montage de cgroups ou privilège sur l’hôte n’est ajouté par ce choix.

Les rôles actifs, processus, concurrence, files, buffers, budgets CPU/mémoire, connexions PostgreSQL, marge système et bornes de drain sont obligatoires dans un plan de ressources accordé/versionné, puis mesurés avant qualification. Il n’existe pas de budget universel implicite. Les réplicas partagent leurs plafonds cumulés ; un propriétaire de préparation PostgreSQL et un propriétaire réseau PZT admissibles restent uniques par périmètre. Une recréation ne clone ni identité, ni clé, ni propriétaire de cluster et ne réinitialise pas le stockage.

D3 s’appuie sur le [transport de fichiers des secrets Compose](https://docs.docker.com/compose/how-tos/use-secrets/) et son [modèle de confiance](https://docs.docker.com/compose/trust-model/). Ce transport n’apporte pas le chiffrement Swarm, une réécriture garantie des UID/modes ou l’autorisation applicative Pixs. Le fournisseur doit vérifier identité native, mode réel, rôle, finalité, installation/base cible, références/versions, validité, révocation, bornes et audit sans appel préalable à Auth dans la base à ouvrir pour la seule remise technique de connexion. Les autres résolutions gardent l’autorité applicative courante. Les valeurs restent dans le seul processus consommateur ; aucune donnée privée n’est lue par les agents. Rotation/révocation exigent arrêt attesté des consommateurs et remplacement/remontage ou recréation contrôlée, avec stockage PostgreSQL conservé, sans reconstruction d’image. Le journal pré-base et son relais C05 idempotent sont rapprochés avant disponibilité. Le fournisseur C01 LoadCredentialEncrypted Debian, SecretReference et les gabarits purs restent inchangés ; aucune preuve systemd ne qualifie Docker.

##### Texte normatif adopté — deltas et canons synchronisés

Les corps normatifs complets sont présentés dans le premier scénario de chaque exigence, auquel son énoncé renvoie obligatoirement pour toute phase concernée. Cette correction de présentation répond à la limite de longueur du validateur strict ; toutes les garanties adoptées sont conservées, avec deux exigences et cinq scénarios.

Le bloc suivant est adopté au delta C08 `docker-image` et au seul canon correspondant :

```markdown
### Requirement: Profil Docker initial déclaré et supervisé

Le profil Docker initial C08 MUST respecter l’intégralité du contrat normatif du scénario « Démarrage du profil Docker déclaré » pour toute construction, préparation, exécution et tout arrêt du profil. Les garanties de processus, supervision, stockage, ressources et droits y sont indissociables ; leur déclaration MUST NOT constituer une qualification.

#### Scenario: Démarrage du profil Docker déclaré

- **WHEN** le profil initial est demandé avec son artefact, sa configuration et son stockage déclarés
- **THEN** PZT et PA sont admis sous leurs contrôles, PA prépare seulement les ressources PostgreSQL manquantes et PBO conserve ses migrations et initialisations
- **AND** aucun entrypoint hérité ni volume anonyme accidentel n’autorise une initialisation ou une disponibilité
- **AND** Le profil Docker initial C08 MUST déclarer Debian 13 Linux amd64, la base Docker Official Image postgres:16.15-trixie verrouillée par digest avant construction, le paquet Supervisor 4.2.5-3 et ses dépendances système verrouillées, l’init Docker et la supervision au premier plan. Il MUST traiter explicitement ENTRYPOINT, CMD, STOPSIGNAL et VOLUME hérités, sans initialisation automatique PostgreSQL. Il MUST sélectionner un rôle applicatif PBO, les exécutants PA système/événements et PZT indépendant et un service PostgreSQL distinct, sous un plan de ressources et un stockage persistant déclarés. Le lifecycle MUST contrôler ordre, readiness, comptes, signaux et drain ; PostgreSQL MUST attendre sa préparation autorisée par PA. Le profil MUST NOT ajouter implicitement privilège, socket Docker, namespace hôte ou montage de cgroups. Les droits de l’hôte et les données persistantes MUST rester préservés ; une métadonnée d’image ou une dépendance installée MUST NOT valoir qualification.

#### Scenario: Arrêt des processus cohébergés

- **WHEN** le conteneur reçoit son signal d’arrêt déclaré
- **THEN** le lifecycle draine PBO avant fermeture PostgreSQL et conserve PA/PZT jusqu’aux étapes qui les requièrent, dans les bornes accordées
- **AND** une étape inconnue ou interrompue reste non prête et inspectable sans perte silencieuse ni réinitialisation du stockage
```

Le bloc suivant est adopté au delta C08 `secrets-providers` et au seul canon correspondant :

```markdown
### Requirement: Secrets Docker par fichiers versionnés

Le fournisseur Docker distinct de C01 MUST respecter l’intégralité du contrat normatif du scénario « Workload Docker et politique courants » pour toute résolution, rotation, révocation et reprise. Les garanties de confiance, confidentialité, lifecycle et audit y sont indissociables ; une garantie absente ou inconnue MUST maintenir l’échec fermé.

#### Scenario: Workload Docker et politique courants

- **WHEN** un workload prouvé demande des références et versions autorisées pour son mode, sa finalité et sa cible avec audit durable confirmé
- **THEN** seules les valeurs admissibles sont remises au consommateur vérifié et leur relais C05 reste requis avant disponibilité
- **AND** aucun credential ne transite dans les messages de management PZT
- **AND** Le profil Docker local MUST sélectionner un fournisseur distinct du transport systemd C01 pour résoudre des références par fichiers versionnés montés en lecture seule au runtime. Il MUST vérifier une preuve native du workload et une politique protégée courante liant mode réel, rôle, finalité, cible, références, versions, validité, révocation, bornes et audit. Pour la seule remise technique de connexion PBO, ces contrôles MUST être vérifiables sans Auth dans la base à ouvrir ; les autres résolutions MUST conserver leur autorité applicative courante. UID, présence ou propriété d’un fichier, variable d’environnement et déclaration appelante MUST NOT suffire comme identité ou autorisation. La publication externe MUST rester distincte de la lecture. Les valeurs MUST rester dans le processus consommateur, hors environnement, argv, PZT, artefacts, journaux et checkpoints. Le lifecycle MUST assurer l’arrêt attesté des consommateurs avant remplacement puis remontage ou recréation contrôlée, sans prolongation de copie, perte PostgreSQL ou reconstruction d’image. L’audit durable pré-base et le relais C05 idempotent MUST être rapprochés avant disponibilité ; une garantie absente ou inconnue MUST maintenir l’échec fermé. C01 Debian, SecretReference et les gabarits purs MUST rester inchangés ; une preuve systemd MUST NOT qualifier ce fournisseur Docker ni lui donner un droit métier ou R01.

#### Scenario: Fichier présent sans identité fiable

- **WHEN** un fichier existe mais que la preuve native, la politique, la version ou la fraîcheur du consommateur ne peut être vérifiée
- **THEN** aucune valeur ni disponibilité n’est annoncée, sans repli vers INSTALLER ni autorisation déduite du fichier ou de l’UID

#### Scenario: Rotation ou relais non confirmé

- **WHEN** une version doit être remplacée alors qu’un ancien consommateur n’est pas arrêté ou que le relais d’audit reste inconnu
- **THEN** aucune rotation achevée ni disponibilité conforme n’est annoncée
- **AND** la reprise exige arrêt attesté, remplacement et remontage ou recréation contrôlés, revalidation et rapprochement C05 sans perte du stockage PostgreSQL ni reconstruction de l’image
```

L’intitulé de la tâche 2.5 est remplacé, sans nouvel identifiant ni déplacement de tâche, par : « Réaliser le raccord post-INSTALLER du provider systemd existant, le fournisseur Docker explicitement adopté et la remise technique minimale de connexion PBO. » Ses critères et contrôles restent exécutés dans cette tâche sur le fournisseur réel de chaque profil, y compris identité native, rotation/révocation, consommateur actif, audit indisponible, crash/reprise et préservation des gabarits ; aucune qualification Docker n’est déduite d’un double.

##### Périmètre RSMP validé du lot

Les seules écritures d’adoption validées concernent dix fichiers :

| Fichier | Modification limitée |
|---|---|
| `openspec/changes/add-installation-and-first-configuration/.openspec.yaml` | Commentaire de statut, sans changer schema ou created. |
| `openspec/changes/add-installation-and-first-configuration/proposal.md` | Portée D1–D3, dépendance image et fournisseur distinct, sans réalisation affirmée. |
| `openspec/changes/add-installation-and-first-configuration/design.md` | Adoption des trois choix validés et conservation des limites. |
| `openspec/changes/add-installation-and-first-configuration/requirements.md` | Deux exigences et cinq scénarios supplémentaires reliés aux tâches et P01/P02/P10/S01–S04 ; compteurs historiques préservés comme tels. |
| `openspec/changes/add-installation-and-first-configuration/tasks.md` | Précision 2.5 pour les deux fournisseurs et contrôles nécessaires, mêmes identifiants, ordre et cases tant que non validées. |
| `openspec/changes/add-installation-and-first-configuration/specs/docker-image/spec.md` | Ajout exact du requirement Docker et de ses deux scénarios ci-dessus. |
| `openspec/changes/add-installation-and-first-configuration/specs/secrets-providers/spec.md` | Ajout exact du requirement fournisseur Docker et de ses trois scénarios ci-dessus. |
| `openspec/specs/docker-image/spec.md` | Synchronisation de ce seul ajout validé, clauses existantes conservées. |
| `openspec/specs/secrets-providers/spec.md` | Synchronisation de ce seul ajout validé, C01 et branche technique existante conservés. |
| `BUILD.md` | Un paragraphe de renvoi aux choix D1–D3 adoptés, sans build, installation ni droits supplémentaires. |

Le change de construction `build-and-qualify-pixs-docker-image`, PA01, C14, les autres canons, PROJECT et TECHNICAL ne sont pas modifiés par ce lot. Aucun paquet n’est installé, aucune image n’est téléchargée ou construite, aucun volume/service/hôte n’est modifié, aucun code, migration, Git ou déploiement n’est autorisé par cette adoption documentaire.

Avant validation de 1.5 : choix explicites, cohérence du périmètre, strict C08 et deux canons concernés, revue P01/P02/P10 et unités pures de profils avec leurs limites. Avant les réalisations dépendantes : artefacts/ABI/versions épinglés, paramètres de ressources et confiance fournis, exécutants/stockages/supervision/fournisseurs réels et recettes applicables prouvés. Les données à mesurer ne deviennent pas des garanties et aucune valeur d’exploitation ou promesse HA n’est inventée.


#### Préparation 1.6 — décisions adoptées, réalisation et qualification requises

La première installation doit être totalement autonome : aucun Pixs, PostgreSQL Pixs ou PKI PZT préexistants, ni paquet d'identités/certificats préémis ailleurs. Le terme applicable est **hôte**. L'autonomie ne donne aucune autorité au premier PBO, à UID 0, à un fichier présent ou à un certificat seul.

| Choix | Décision et source | Limites de réalisation |
|---|---|---|
| E1 — Confiance initiale | Z12 est l'unique producteur de la cérémonie locale isolée, des primitives CA et de l'état PKI ; C08 orchestre et consomme son [contrat initial documentaire 1.0.0, §12](../add-pzt-ca-hierarchy-rotation-and-recovery/contracts.md). D4/D5/D6 et les deux clauses initiales PZT/autorisation sont publiés par leur propriétaire sous référence CAB 69. | Les clés CA matérielles non exportables, la racine hors ligne et la séparation des usages sont conservées. Schémas sérialisés, API/runtime initial, ancrage TPM NV, adoption/retrait et intégration A07/A12 restent à réaliser et qualifier. Aucune écriture NV sur l'hôte actuel n'est autorisée par cette adoption. |
| E2 — Catalogue technique PA | [PA01](../add-pa-native-build-and-component-composition/design.md) a adopté et publié sous référence CAB 70 les seules opérations `inspect_postgresql`, `prepare_postgresql`, `get_postgresql_result`, version `1.0.0`, propriétaire `pixs.agent`, seul mode `system-daemon`. Préparation Critique sans hors ligne, validation courante avant chaque effet ; lectures Protégé sous les contrôles et bornes existants. | Schémas de paramètres/résultats, résolution du plan technique confirmé, exécutants et état durable PA restent à réaliser. Aucun shell, SQL ou chemin exécutable arbitraire reçu ; aucune migration ni table métier. L'adoption du catalogue ne prouve aucun handler disponible. |
| E3 — PZT local | Le développeur a explicitement répondu « Valider le choix E3 documenté » : HTTP/JSON sur TCP IPv4 loopback, sous PZT dans la même frontière hôte/VM/conteneur ; TLS 1.3+mTLS, terminaux ECDSA P-256 selon le canon, suite A10h explicitement fournie sans valeur initiale inventée, 0-RTT interdit. Adaptateur Cython vers `libssl`/`libcrypto` OpenSSL 3, nouvelle dépendance runtime PZT adoptée, sans bibliothèque Python TLS supplémentaire. | L'accord ne vaut ni installation sur l'hôte actuel, ni binaire/runtime/transport qualifié. Versions exactes, provenance, ABI, providers et empreintes sont à déclarer et verrouiller avant build/recette. Aucun endpoint, port, groupe, matériel/provider de clé, budget ou compte n'est deviné. |

Le relevé protégé du 23 octobre 2026 a confirmé Z12 `contracts.md` SHA-256 `8c4c3502c8ec6b653fb266b14334bf6f28639789ad15e18ad6bb8a02575a7fb5`, révision 5950, et PA01 `design.md` SHA-256 `8ef9c3cdfcea8dbaebc0f64d23f8fd475a8816742a6e744aed01d7645cebcf02`, révision 6018. Ces références identifient les textes examinés, sans figer les travaux propriétaires suivants ni démontrer une API disponible.

Les ports initiaux Z12 exacts sont `prepare_initial_trust`, `inspect_initial_trust`, `reconcile_initial_trust`, `adopt_initial_trust` et `retire_initial_authority`. Ils ne sont pas les ports ordinaires de certification et ne créent pas de seconde PKI C08. Création locale initiale, adoption publique sous l'autorité courante, retrait initial attesté et admission ordinaire restent des étapes distinctes. Aucune clé privée ou credential PG n'est transporté par C08/PZT. Un DTO, une référence ou un ACK ne prouve ni effet, ni autorité actuelle, ni commit.

Le plan applicatif privé R01 C08 reste distinct du plan technique PostgreSQL résolu par PA : il contient des cibles et effets Core/Auth et une intention de credential opaque, qui ne sont pas envoyés à PA. Le raccord technique ne reçoit que les références de sa projection fermée, liée au mandat/opérateur, à la cible et au plan courants par les propriétaires vérifiés. Aucun producteur/résolveur de ce plan technique ou format public n'est déduit du seul code de sérialisation applicative. La proposition de schéma PA01 reste à convenir avant branchement, sans API concurrente C08.

Le parcours conserve : admission locale opérateur/politique/mandat vérifiés ; préparation de la confiance initiale par Z12 ; transport PZT des seules actions techniques admises ; PA prépare service/rôle/base sur physique/VM ou initialise le seul manquant dans Docker avec stockage conservé ; PBO réalise migrations et actes propriétaires ; résultats/audits rapprochés ; adoption et retrait initiaux prouvés avant admission ordinaire. Les identités et classes viennent des sources serveur vérifiées, jamais de labels ou booléens appelants. PLATFORM sans tenant/scope métier ; mTLS ne remplace ni attestation ni autorisation.

Le handler PA est fermé et verrouillé par profil avant effet, sans installation/commande/SQL fournis par l'appelant. La préparation externe PG n'est pas atomique avec le commit Core/Auth/C05/C08. Réponse perdue, concurrence, plan divergent ou issue inconnue exigent inspection et réconciliation avant tout rejeu ; aucune nouvelle base, seconde PKI ou compensation destructive implicite. Après passage, PostgreSQL reprend l'autorité applicative et les pouvoirs temporaires sont retirés, sans autorité métier parallèle.

DEVOPS inventorie OpenSSL 3.5.7 pour la CLI ; cela ne prouve pas la bibliothèque liée, son ABI ou ses providers. Les sources primaires [CPython 3.14 ssl](https://docs.python.org/3.14/library/ssl.html) et [OpenSSL SSL_CTX_set_ciphersuites](https://docs.openssl.org/3.5/man3/SSL_CTX_set_cipher_list/) distinguent la configuration des suites TLS 1.3 des seules suites antérieures. Le choix E3 adopté ne transforme pas ce constat documentaire en qualification de l'adaptateur ni de la clé matérielle.

La tâche 1.6 reste ouverte jusqu'à ses contrôles de conception dans la phase de validation ; E1/E2/E3 ne sont plus des votes en attente. Les paramètres et capacités réellement nécessaires restent à réaliser/fournir/qualifier avant leurs recettes dépendantes. Les contrôles P03/P04/P07/P09, révocation/fraîcheur, refus du premier PBO auto-approuvé, perte de réponse/reprise et transfert d'autorité restent requis. C01, R01 Ed25519/600 secondes, gabarits purs, D1–D3 et raccord minimal C10 sont préservés ; la fenêtre R01 finale ne borne pas toute la préparation.

Les réalisations C08 continuent sur instruction du développeur, puis tests et validation dans un second temps. Aucun build, installation, certificat, clé, volume, service, droit d'infrastructure, Git ou archive n'est réalisé par cette mise à jour documentaire. La réalisation de deux sous-lots purs 2.1 ne livre pas les raccords PA/Z12/PostgreSQL et n'est pas une qualification P0.


### Vérification et décision suivante

Les cas P01–P10 de requirements.md précisent les preuves futures. L’adoption porte sur huit canons, les quatre documents C08 et l’alignement de PROJECT/TECHNICAL/BUILD ; les deltas conservent la trace normative. La métadonnée conserve schema et created ; seul son commentaire est aligné sur l’adoption. Le code reste inchangé. Les validations OpenSpec et contrôles d’empreintes/UTF-8/LF/liens vérifient la cohérence documentaire seulement. Chaque tâche future inclut désormais ses critères et contrôles ciblés avant la suivante ; aucun nouveau change, déploiement ou archivage n’est lancé.

## E4 — admission technique PA avant PostgreSQL, adoptée le 23 octobre 2026

### Constat et décision nécessaire

E3 est adopté ; il définit le transport TLS, pas le droit de préparer PostgreSQL.
PA01 a confirmé le 23 octobre 2026 qu'aucun producteur/résolveur concret de mandat
prébase, ni registre durable de consommation/réconciliation PA, n'est livré.
Z12 ne fournit pas cette autorité de préparation PostgreSQL : ses pouvoirs
initiaux restent limités à la PKI. Les preuves privées R01, C01, un certificat,
une référence de confirmation ou un premier PBO ne remplacent pas l'admission.

Le développeur a explicitement validé le lot E4 le 23 octobre 2026 :
usage technique supplémentaire de la clé personnelle Ed25519 préautorisée,
mandat lié au plan PostgreSQL et à sa confirmation, registre durable PA avec
ancrage TPM NV dédié distinct de la PKI Z12. La réponse humaine est conservée
au checkpoint (call_1323e2529c644170b21c323c4bd06bb9/0).
Cette adoption documentaire couvre seulement ce design, proposal.md et
requirements.md du C08 existant. Elle ne modifie aucun canon, ne produit
aucune autorité exécutable et ne qualifie aucun runtime ou effet matériel.

### E4-A — mandat technique signé, distinct de R01

Réutiliser la clé publique personnelle Ed25519 déjà préautorisée de l'opérateur
comme ancrage d'un **usage supplémentaire explicitement adopté**, avec politique
technique native séparée de R01. Ne réutiliser ni payload, ni nonce/preuve, ni
autorisation R01 ; ne jamais utiliser une clé TLS ou CA pour cet acte.
L'alternative est une clé opérateur Ed25519 dédiée, avec provisionnement et
révocation distincts ; elle n'est pas sélectionnée implicitement.

La clé privée reste sous contrôle de l'opérateur, hors des agents, des journaux
et du dépôt. La source locale protégée lie explicitement opérateur, référence
de clé publique, procédure de préautorisation, lanceur natif et identités
techniques admises. Une clé fournie par le demandeur, UID 0 ou un fichier présent
ne peut publier sa propre autorité. Cette procédure locale ne requiert aucun
Pixs ou paquet de certificats préexistant.

C08 possède la projection technique et la présentation/confirmation opérateur.
PA01 possède la résolution courante, la décision technique, son plan, ses effets
et leur registre durable. PZT transporte l'acte sans accorder de droit.
Le vérificateur PA proposé utilise libcrypto OpenSSL 3 dans le contexte privé
déjà sélectionné ; son fonctionnement et le provider Ed25519 restent à qualifier.
La [documentation OpenSSL Ed25519](https://docs.openssl.org/3.5/man7/EVP_SIGNATURE-ED25519/)
décrit la primitive ; elle ne constitue aucune preuve d'intégration PA.

### E4-B — principes de représentation adoptés, détail propriétaire à figer

La projection C08 ne contient que l'intention service/rôle/base, leurs références
et versions, l'installation/cible, le profil technique, les préconditions et les
corrélations nécessaires. Elle exclut le plan R01, les cibles Core/Auth/tenant,
les credentials et toute instruction SQL, shell ou code reçu. Sa sérialisation
proposée est JSON UTF-8, clés triées, séparateurs compacts, valeurs strictes,
champs fermés, doublons et constantes non finies refusés ; SHA-256 hexadécimal
minuscule sur ces seuls octets, sans son propre digest ni signature.

PA dérive son TechnicalPlan propriétaire depuis cette projection protégée.
La projection exclut le digest du futur plan PA et le résultat de confirmation,
afin de ne pas créer de cycle d'empreintes. La référence de confirmation peut
être allouée avant le plan PA ; sa présence ne signifie pas qu'elle est confirmée.
L'acte signé confirme ensuite explicitement les deux digests et les effets
présentés. Un changement invalide la confirmation.

Le document de mandat proposé porte une version 1.0.0 et un domaine
PA_POSTGRESQL_INITIAL. Les octets signés sont le préfixe ASCII
PIXS:PA:POSTGRESQL:INITIAL:1.0.0 suivi d'un LF puis les octets JSON canoniques.
Ed25519 porte directement sur ces octets, sans préhachage applicatif.
L'enveloppe fermée contient seulement ce document et sa signature Ed25519
encodée en base64 canonique ; aucune clé embarquée ne s'auto-autorise.

Le document lie obligatoirement référence de mandat/invocation, opérateur et clé,
politique/version, installation/cible, identités terminales appelante/exécutante
et relation PZT, opération/version/classe, corrélation/causalité/idempotence,
instants UTC de création/début/expiration, ancrage courant et références des
objets protégés résolus par PA. Pour prepare_postgresql il lie en plus projection,
plan PA, préconditions et confirmation par références/versions/digests, et
l'ensemble fermé d'effets service/rôle/base. Les lectures ne reçoivent aucun
effet de préparation ; get_postgresql_result lie l'opération consultée et exige
une autorité de lecture actuelle. Les schémas exacts conditionnels, champs,
bornes et résolveurs propriétaires doivent être figés avec PA01 avant leur code.

La validité est bornée par la politique technique explicite et une référence UTC
fiable. La fenêtre finale R01 de 600 secondes ne borne pas toute la préparation.
Chemins, propriétaires, tailles, délais, ports et budgets restent obligatoires,
sans valeur de production issue de fixtures ni valeur supposée par l'agent.

### E4-C — registre durable et ancrage PA adoptés, réalisation à qualifier

PA01 possède un journal technique protégé, indépendant de PostgreSQL, avec
exclusion native, écritures durables et états de préparation/effet/résultat.
Un ancrage TPM NV dédié à cette autorité PA est proposé, séparé de l'ancrage PKI
Z12. Le candidat est un index NV de type extend, SHA-256, liant la chaîne des
enregistrements ; aucun index, attribut d'autorisation, secret NV ou matériel
n'est créé ni choisi sur l'hôte actuel. La
[documentation du propriétaire tpm2-tools](https://github.com/tpm2-software/tpm2-tools/blob/master/man/tpm2_nvextend.1.md)
décrit l'extension NV ; elle ne prouve ni protection contre redéfinition ni
qualification du journal proposé.

La définition/protection de l'index, sa provenance, ses droits, la perte ou
redéfinition de l'index, les budgets d'écriture/endurance et la qualification
matérielle restent des conditions explicites à arrêter par PA01 avant effet.
L'absence de fichier, de base ou d'ancrage ne prouve jamais une installation neuve.
Un stockage restauré divergent de l'ancrage garde le parcours bloqué.

Avant chaque effet, PA revalide identité, signature, politique/révocation,
fraîcheur, cible, plan dérivé, confirmation, préconditions et état de consommation.
Préparation du journal, fsync, évolution NV et effet PostgreSQL sont des frontières
distinctes : aucune atomicité globale n'est prétendue. Une issue inconnue interdit
le rejeu ; PA inspecte les effets réels puis réconcilie sous autorité actuelle.
Le détail de cette machine durable et de ses points de crash précède son code.
Un ancien mandat consommé ne devient pas le droit de recommencer. Les privilèges
temporaires sont retirés après résultat rapproché ; le retrait est attesté avant
admission ordinaire. L'audit technique n'est pas un substitut à C05/R01.

### Contrôles et limites de l’adoption documentaire

Les contrôles à préparer couvrent mauvais opérateur ou lanceur, clé inconnue ou
révoquée, substitution de projection/plan/confirmation, identité TLS correcte
mais mandat absent, ancien état restauré, concurrence, perte de réponse, crash
autour des fsync/NV/effets, lecture étrangère, retrait d'autorité et absence
d'audit. Aucun de ces contrôles n'est déclaré exécuté.

Les choix E4 sont acquis ; les formats conditionnels, résolveurs, politiques,
protection matérielle et machine durable restent à arrêter et qualifier dans
les périmètres propriétaires. La continuation du change conserve ses mandats
CAB unitaires ; cet accord documentaire n'est aucune décision ou écriture
pour un autre RUN. Il ne vaut ni qualification, ni installation, ni accès
TPM/NV, ni modification des services ou permissions de l'hôte. Toute
dépendance nouvelle non couverte reste soumise à AGENTS.md §17.
Le profil X.509 et le TrustStore terminaux restent un chantier Z12/PA01 distinct,
sans SAN/OID ou port numérique inventé par C08.

## Réalisation partielle C08 — 23 octobre 2026, avant phase de tests

Les sources de marqueur, plan, stockage privé et contenu fermé de l'acte sont
écrites sous CAB. Le catalogue local C10, son adaptateur initial, son modèle et
la migration 0014 sont écrits. Le modèle C08InstallationResultRecord, sa
migration additive 0015 et son import Django sont également écrits. Les
empreintes et fins natives des écritures sont au checkpoint du même RUN.

Aucun test produit, import de qualification, migration SQL ni effet
d'infrastructure n'a été exécuté par cette reprise. Le résultat C08 ne dispose
pas encore de son écrivain/lecteur propriétaire intégré ; le checkpoint durable,
la machine de modes, la CLI, le raccord R01 et les raccords techniques restent
à compléter. Une ligne préparée dans une transaction ne prouvera jamais son
commit ; le lecteur du marqueur devra utiliser la même exclusion installation
que Core, sur la même base et le même schéma.

Les tâches demeurent ouvertes après 1.5. La phase de tests/validation demandée
par le développeur reste séparée, puis la clôture exige cohérence, recette,
archive et statistiques prouvées. Aucune archive ni disponibilité C08 n'est
déclarée.

## Projection PostgreSQL vers PA01 — contrat de travail C08

Le [contrat propriétaire de projection](projection-contract.md) ferme les
intentions service/rôle/base, leurs actions et effets, les références de profils
et d'observation PA, la sérialisation et la liaison au plan/confirmations E4.
Il ne remplace ni les profils/résolveurs PA01 ni les producteurs réels. Les
migrations et l'acte R01 restent PBO. Le participant transactionnel du résultat
C08 est écrit sous CAB ; son raccord complet et ses tests restent à réaliser.

## Lecteur privé du résultat C08 — réalisation préparée avant tests

C08TransactionalResultWriter et C08ResultReader partagent les seules liaisons
privées du reçu C08. Le profil C10 propre au backend doit couvrir la ressource
bootstrap courante. Le lecteur ne confère aucune permission, ne lit pas les
tables privées Core/Auth/C05 et ne sélectionne aucun mode.

inspection_using est un alias Django privé obligatoire, distinct de using,
configuré par la composition serveur avec les mêmes paramètres de cible et
de connexion ; aucun alias libre n'est reçu d'un client. Les valeurs privées
restent en processus, sans empreinte publique ni diagnostic. La lecture
post-commit ouvre une transaction native read-only sur connexion/PID distincts,
vérifie base/schéma, tient le même verrou Core installation en partagé jusqu'aux
fsync puis recontrôle résultat, connexion, plan, profil et validité.

inspect_confirmed accepte son appel dans la transaction Core et hors transaction.
Une ligne du XID courant n'est jamais déclarée committée. Seule une absence de
ligne réellement inspectée donne None ; une cible/connexion/liaison/politique
invérifiable reste un refus. L'erreur après début de publication ou le nettoyage
non prouvé garde une issue inconnue. Les deux connexions ne sont jamais
substituées ; le lecteur ferme son alias dédié et la connexion source seulement
s'il l'a ouverte lui-même. L'entrée R01/CLI conserve ses contrôles d'autorité.

AuthBootstrapBackend vérifie déjà son propre stage natif lors de la revalidation
dans la transaction courante ; aucun changement Core/Auth n'est nécessaire pour
ne pas confondre ce préparé avec un commit C08. Visibilité après commit, rollback,
savepoints, exclusion, substitution de connexion/XID/cible, profil expiré ou hors
ressource, reprise après marqueur perdu et nettoyage restent à qualifier dans la
seconde phase. Aucune réussite de ces contrôles n'est déclarée par cette source.


### Raccord PA01 courant — limites de la projection

Le [contrat de projection](projection-contract.md) est rapproché des capacités
PA01 actuellement sélectionnées : Debian 13 x86_64 physique/VM avec conservation
des données. RECREATE/DATABASE_DROP font refuser le plan entier avant tout effet,
sans conversion en CREATE. Leur réalisation demanderait une adoption normative
PA distincte. Docker reste une cible C08 adoptée à réaliser et qualifier ; le
profil PA01 courant ne l'admet pas, y compris INITIALIZE_START. Ce constat ne
réduit aucune exigence C08 ni aucun critère de clôture. Les tableaux A07
correlation_ids/causation_ids sont conservés intégralement, dans l'ordre avec
leurs doublons, distinctement des identifiants scalaires. Cette mise au point
n'ajoute ni capacité PA, ni qualification, ni test exécuté.


### Réalisation partielle 2.1 — checkpoint durable privé, écrit à tester

`src/pixs/backend/installation/checkpoint.py` et
`tests/unit/test_installation_checkpoint.py` sont écrits sous CAB, à tester
pendant la seconde phase. Le checkpoint est un fichier privé versionné
distinct du résultat PostgreSQL et du marqueur. Il enregistre seulement des
observations et références : il ne prouve ni plan, ni autorisation, ni commit,
ni résultat, et ne sélectionne aucun mode ou effet externe.

La configuration protégée fournit `CheckpointConfig` (`io`, `lock_basename`,
`limits`) et tous les paramètres `CheckpointLimits` (`max_bytes`,
`max_ref_len`, `max_confirmations`, `allowed_format_versions`, `allowed_phases`).
Aucun chemin, identité native ou borne de production n'est initialisé ici.
Les phases privées admises sont un sous-ensemble explicite de `PLAN_RECORDED`,
`PROOF_LINK_OBSERVED`, `INSPECTION_OBSERVED`, `RECOVERY_NOTE_RECORDED` ; aucun
mode d'exécution n'en est déduit.

Le schéma fermé contient format, installation/base/opération, version et
SHA-256 du plan, corrélation/causalité/idempotence, révision positive, phase et
références de confirmation bornées. Ces liaisons sont structurelles et restent
à rapprocher du plan immuable et des sources propriétaires actuelles par le
futur consommateur ; un fichier restauré ne remplace aucune inspection PA/PG.
Format et identité d'opération restent immuables pendant les mises à jour.
Un rejeu identique est idempotent ; toute autre écriture exige la révision
suivante sous garde interprocessus non bloquante.

Parents, propriétaire, droits, types, liens et garde sont vérifiés. La
publication réutilise `marker._publish` avec son temporaire privé
`.c08-marker-<identifiant>` dans le même répertoire, fsync du fichier,
remplacement, fsync du répertoire et relecture. Une disparition après ouverture,
une substitution ou une panne de durabilité conserve une issue inconnue :
aucun succès ou rollback PostgreSQL n'en est inféré. Une absence ou une donnée
invalide n'ouvre ni INSTALLER ni NORMAL.

Les recettes préparées couvrent CAS entre deux processus, rejou/révision,
identité/format, JSON fermé/types/bornes, liens/droits et pertes pendant les IO.
Elles ne sont pas exécutées. Le raccord au plan courant, la machine de modes,
la CLI et la composition réelle PA/PZT/PG restent à réaliser ; aucune coche,
qualification ou clôture n'est produite par ce sous-lot.


### Réalisation partielle 2.1 — checkpoint lié au plan courant, écrit à tester

Le port privé C08CheckpointBinding et ses recettes sont écrits dans
checkpoint_binding.py et test_installation_checkpoint_binding.py. Ils restent
à tester pendant la seconde phase. La composition fournit obligatoirement les
configurations distinctes du plan et du checkpoint, ainsi que format_version ;
aucune valeur de production n'est initialisée.

Le constructeur lit le plan réellement publié et épingle son digest canonique
complet. L'initialisation de la seule garde checkpoint, la lecture et
l'enregistrement conservent la garde SH du plan jusqu'après les IO, avec
relecture et contrôle du digest. Le contenu est dérivé du plan courant,
sans identités libres fournies à record. Les PlanConfirmationLink sont vérifiés
par check_confirmation_link et seules leurs références sont persistées :
cette liaison structurelle ne prouve ni signature, ni habilitation, ni consentement.

Un autre plan, une identité ou un format divergents ne deviennent pas une absence.
Le verrou occupé reste Busy ; une perte ou modification observée conserve une
issue inconnue. La lecture et la publication réutilisent les contrôles IO
propriétaires ; les quatre noms de fichiers/gardes doivent être distincts.
Les recettes préparées utilisent de vrais fichiers, un écrivain plan dans un
autre processus pendant la publication checkpoint et une modification réelle
du plan pour simuler une perte de cohérence. Aucune recette n'est exécutée.

Ce raccord ne fournit aucune autorité R01, aucun commit PostgreSQL, aucun mode,
ni résultat PA/Z12. La machine de modes, la CLI et la composition intégrée
restent à réaliser et qualifier ; aucune coche ni clôture n'est ajoutée.


### Réalisation partielle 2.1 — règles de modes pures, écrites à tester

`installation/mode_values.py` et `tests/unit/test_c08_mode_values.py`
sont écrits sous CAB, sans syntaxe ni tests exécutés à ce stade.
`ConfigurationState` (`PENDING`, `CONFIGURED`) et `ModeOperationKind`
(`FINALIZE_CONFIGURATION`, `ENTER_MAINTENANCE`, `EXIT_MAINTENANCE`) sont
des types privés C08. Ils réutilisent `StartupMode` sans le modifier.
`validate_state_pair` exige les types exacts et admet seulement
PENDING/FIRST_CONFIGURATION, PENDING/MAINTENANCE, CONFIGURED/NORMAL et
CONFIGURED/MAINTENANCE. INSTALLER n'est pas un état installé.

`transition_state` calcule une paire désirée : finaliser configure et rejoint
NORMAL sauf en MAINTENANCE, qui reste conservée ; entrer en maintenance garde
l'avancement ; sortir explicitement rejoint FIRST_CONFIGURATION ou NORMAL
selon cet avancement. Répéter une opération pure garde le même résultat.
Aucun acteur, acquittement, callback, IO, SQL, horloge, Django, état courant,
permission ou disponibilité n'est produit. Le futur service devra utiliser
les producteurs réels C03/C04/C05/C10, la transaction, l'idempotence et la
version attendue avant d'appliquer ces valeurs.

Les tests unittest préparés couvrent les douze combinaisons nominales, la
distinction des dimensions, les refus de types/paires et le diagnostic fermé.
Ils ne qualifient ni stockage, ni autorité, ni runtime. Les instantanés et
reçus C08, leur migration et les raccords réels restent à réaliser.


### Réalisation partielle 2.1 — structures de stockage des modes, écrites à tester

`C08ModeSnapshotRecord` et `C08ModeOperationReceiptRecord` sont définis dans
les deux sources backend dédiées, sans migration appliquée, import de
qualification ou tests exécutés. Ils ne fournissent encore ni writer,
participant d'idempotence, finaliseur, lecteur de commit ou inspecteur.

Les identifiants UUID sont explicitement fournis ; leur version UUIDv7
reste à contrôler par le producteur et les gardes SQL. Les snapshots sont
liés par FK aux seuls objets C08 et uniques par installation/version.
La première version est PENDING/FIRST_CONFIGURATION, origine R01_INITIAL,
sans prédécesseur ni reçu de transition et sans dérogation de gouvernance.
Les versions suivantes ont prédécesseur et reçu. Les quatre paires de
`mode_values` séparent configuration et mode ; les liens entre lignes,
l'absence de downgrade et l'immuabilité restent à vérifier en SQL/runtime.

Les reçus lient opération, acteur, contexte PLATFORM, kind, version attendue,
digest/sérialiseur/idempotence, corrélations et provenance native.
IN_PROGRESS n'a aucun résultat ; SUCCEEDED exige un résultat complet,
une version positive et une date de fin cohérente. Le résultat peut désigner
un nouveau snapshot ou un historique sans effet ; il ne vaut pas mode courant.
Les dimensions d'idempotence et l'identité d'opération sont uniques.

Chaque groupe de métadonnées est complet sous GOVERNED, propriétaire
pixs.backend, et entièrement nul sous WAIVED. Ces dispositions structurelles
ne vérifient aucun droit : seule une dérogation C04 réelle après authentification
pourra les alimenter ; le R01 initial reste sans dispense du futur compte.

La migration additive, l'enregistrement/import des modèles, les producteurs
réels, leurs revalidations et les tests PostgreSQL sont des sous-lots suivants.
Aucune table n'est créée, aucun mode réel ou trafic métier n'est admis ici.


### Réalisation partielle 2.1 — enregistrement explicite du stockage backend

Les imports des deux nouveaux modèles C08 sont ajoutés à backend/models.py.
PixsBackendConfig est défini dans backend/apps.py avec name pixs.backend,
label backend et default False. Ses classes se déclarent sans IO SQL et sans
activation opérationnelle. Les configurations Kernel/Core/Exemple existantes
sont conservées ; aucune sélection implicite du nouvel AppConfig n'est ajoutée.

Cette définition permet à un assemblage C08 de sélectionner explicitement
l'application qui porte ses modèles et migrations. Le raccord du profil hôte,
la migration additive et ses gardes, les producteurs et tests réels restent à
réaliser. Les imports ne prouvent ni migration appliquée, ni état committé,
ni permission, mode ou disponibilité. Aucun import de qualification n'est
exécuté par ce sous-lot ; les contrôles sont réservés à la seconde phase.


### Avancement 2.1 du 24 octobre 2026 — stockage et lecture du mode installé

La migration additive `0016_c08_mode_storage.py` est écrite, sans application à PostgreSQL. Elle définit les deux tables C08, leurs contraintes figées et les gardes de provenance native, UUIDv7, version attendue, immuabilité et fin transactionnelle. Le retour est refusé si une des deux tables contient des données. La présence de cette source ne prouve ni la création des tables ni l'exécution des gardes.

Deux sources de tests PostgreSQL sont préparées : `tests/integration/test_c08_mode_storage_postgres.py` pour les douze combinaisons état/opération, l'isolation, l'historique, l'immuabilité de base, les contrôles différés et le retour de migration ; `tests/integration/test_c08_mode_storage_inputs_postgres.py` pour dix-neuf refus UUID, provenance et origine initiale. Elles utilisent un schéma de qualification possédé et des fixtures explicites ; elles n'ont pas été exécutées. Les refus de liens, résultats et gouvernance, la concurrence et les autres contrôles requis restent à compléter puis à exécuter en seconde phase.

Le writer initial `installation/result_writer.py` prépare désormais le résultat C08 et le premier snapshot dans la même transaction propriétaire : version 1, PENDING/FIRST_CONFIGURATION, origine R01_INITIAL, UUIDv7 Core, profil C10 courant et provenance identique au résultat. Il conserve la frame et revalide les deux lignes. Ce chemin refuse REUSE_EXISTING ; il ne réalise pas encore la réutilisation d'une base conservée et ne doit pas être utilisé pour réinitialiser son état.

`installation/mode_reader.py` définit un lecteur privé du mode installé. Sa lecture rapproche le marqueur protégé, le résultat initial, la racine, la dernière version et, si nécessaire, le prédécesseur et le reçu de transition. Elle utilise une connexion d'inspection distincte en lecture seule et le verrou partagé Core de l'installation, puis recontrôle les lignes et le marqueur. Elle ne requiert pas l'ancien plan R01, sa fenêtre d'autorisation ou son ancien lease de gouvernance. Les valeurs retournées ne donnent aucun droit et ne déclarent aucune disponibilité globale.

Ces réalisations restent non testées et ne sont pas encore raccordées à la sélection effective du mode. Les commandes de transition, leur participant d'idempotence concret, les contrôles C03/C04/C05/C10, le chemin R01 de réutilisation, la CLI et les raccords PA/PZT/Z12 restent à réaliser ou à consolider. Les exigences physique/VM et Docker sont conservées. Aucune tâche supplémentaire n'est cochée, aucun canon n'est réappliqué et aucun archivage n'est effectué à ce jalon.

### Réalisation prévue R01 — reçu d'acte et idempotence propriétaires C08

Le header initial reste le résultat durable de la première installation et la
source du marqueur INITIAL. Les reçus de modes restent distincts. Un reçu
d'acte C08 par opération doit fournir le participant d'idempotence R01
INITIAL/REUSE dans la transaction Core existante. Le participant C06 de l'API
Core ordinaire n'admet pas la commande privée
`pixs.core.bootstrap.apply:v1` ; ni ses listes publiques ni les gardes Core ne
sont élargies pour ce raccord.

Le reçu lie installation et cible de base, opérateur et preuve, plan et
confirmations, acte et digest/sérialiseur, clé d'idempotence, contexte PLATFORM,
corrélations, versions CAS attendues, transaction et provenance native. Les
dimensions installation/opérateur/commande/clé sont uniques, ainsi que
l'identité d'opération. Le digest R01 inclut déjà opération et corrélations :
changer ces données ne constitue pas un rejeu identique. Aucun TTL ou retrait
automatique n'est ajouté.

Le check prépare IN_PROGRESS sous les verrous d'installation Core, avec le
profil de métadonnées C08 courant protégé et revalidé. Ce staging ne confirme
rien : la relation au header INITIAL doit être réellement différée et
contrôlée à la fin de la transaction. INITIAL crée ensuite les objets
Core/Auth et le header/snapshot initial ; REUSE conserve compte, credential,
tenant, header, marqueur et modes, après les contrôles CAS du propriétaire
Core. Le résultat du REUSE porte la version courante du binding validée par
Core, sans la remplacer par la version historique du header.

La restauration d'un reçu SUCCEEDED intervient avant apply. Un reçu
IN_PROGRESS ne retourne None à inspect_confirmed que pour le staging courant
exactement rapproché du participant, de l'acte et de la transaction native.
Un IN_PROGRESS ancien, incomplet ou invérifiable garde l'issue inconnue.
L'inspection indépendante après réponse de commit perdue n'autorise aucun
rejeu aveugle du callback. Le garde Core refusant une confirmation incohérente
avant apply reste inchangé.

Les métadonnées historiques sont immuables ; elles restent distinctes des
contrôles et attestations de l'invocation courante. L'opérateur R01 pré-session
ne bénéficie d'aucune dispense de gouvernance ou d'audit du compte cible.
La création du reçu ne donne aucune autorité et ne remplace pas les
producteurs réels C03/C04/C05/C10. Le participant doit être composé avec le
writer C08 lié au plan/acte/enveloppe/bail et un alias d'inspection distinct.
Le PlanSource inspectera l'opération via ce participant ; le ResultReader
initial restera la source de données du marqueur.

Le lot commence par `c08_act_receipt_record.py`. L'enregistrement, la
migration additive et ses gardes SQL, `installation/act_idempotence.py`,
les raccords writer/PlanSource et la composition concrète sont des sous-lots
suivants. Le modèle seul ne fournit ni vérification de provenance ou
d'immutabilité SQL, ni relation différée exécutée, ni participant, ni effet
Core/Auth, ni mode ou preuve de disponibilité. Aucun import de qualification,
migration ou test n'est exécuté par cette préparation ; les cases demeurent
ouvertes jusqu'aux preuves de la seconde phase.

La consommation de l'autorité opérateur reste propriétaire Auth. Le backend
actuel la réalise pendant le stamp du credential INITIAL ; ce stamp n'est
pas un moyen de consommer REUSE sans modifier le credential. Le raccord
propriétaire correspondant doit être réalisé et vérifié, sans écrire les
tables Auth depuis C08 ni traiter un reçu C08 comme substitut de consommation.

### Réalisation prévue REUSE — consommation propriétaire Auth distincte du credential

La réutilisation ne passe pas par stamp ni par ctx.stamp_credential : ces
opérations INITIAL créent le credential et ne doivent pas servir de façade
à une consommation sans création. Auth reçoit une consommation REUSE
distincte, avec un stage privé et une référence
bootstrap-authorization-consumption vérifiable dans la transaction commune.
La signature, la politique, la fenêtre, la cible et la provenance native
restent recontrôlées. La projection non consommée n'est valable que pour
son propre staging exact ; une lecture hors transaction voit la consommation.

Le champ privé existant credential_prepared_digest peut porter, pour REUSE
seulement, le SHA-256 d'un inventaire Auth canonique sous domaine versionné
pixs.auth.reuse.inventory.v1. Le publisher protégé et le consumer propriétaire
doivent employer le même helper. L'inventaire inclut installation/cible,
plan/clé/politique, IDs et liens, versions/états, enabled et générations
actuelles du gate, des bindings et credentials. Les générations ne sont
jamais ramenées à 1. La projection ne lit ni n'exporte password_hash.
Le digest et les données privées ne sont pas restitués à C08.

Le consumer relit cet état sous verrous, refuse toute divergence et modifie
seulement AuthBootstrapAuthorization : signature vérifiée, consommation,
provenance et version. Il ne crée, réinitialise ou modifie aucun gate,
binding ou credential. Le chemin INITIAL reste conservé. Aucune sentinelle,
valeur de production, TTL ou migration de schéma n'est ajouté.

Le code de consommation seul ne fournit ni publisher protégé ni composition
C08 complète. Ces raccords, leurs références effectives et les tests réels
de conservation, concurrence, retrait et rollback restent requis avant
qualification ; un reçu C08 ne remplace aucune preuve du propriétaire Auth.


### Raccord propriétaire REUSE et lecture du résultat conservé

Le chemin REUSE utilise un participant privé C08 distinct de l'écrivain du
résultat initial. Core conserve ses contrôles de liaison, de cible et de
versions ; aucune extension de sa liste publique de commandes ni appel à
`stamp_credential` n'est ajouté. Le participant C08 demande à l'instance Auth
vérifiée de consommer son autorisation courante dans la transaction réelle.
Il conserve la référence de stage effectivement retournée par Auth ; la
vérification finale lui transmet cette référence avec la preuve finale neuve
produite par Core, sans inventer un stage de credential.

Le résultat C08 initial et le dernier snapshot de configuration sont lus sous
le domaine d'exclusion de l'installation, puis relus sans modification. Ils
doivent préexister à la transaction courante et rester identiques pendant
l'acte. Le reçu propre à l'acte REUSE enregistre son résultat et sa version CAS ;
il ne réécrit ni le reçu initial, ni le mode, ni le credential ou ses générations.

Le lecteur du marqueur ne compare pas l'ancien résultat initial au nouveau
plan REUSE. Il exige le reçu committé correspondant à l'opération courante,
vérifie ses liaisons via le participant d'idempotence C08, puis le rapproche du
résultat initial conservé. La référence et la version initiales du marqueur
restent distinctes de la version CAS du résultat du nouvel acte. Une absence,
un état en cours, une connexion/transaction divergente ou un rapprochement
incertain ferme la lecture ; aucune preuve structurée ne remplace le commit.

Ces raccords restent des sources à qualifier. La publication propriétaire des
preuves/politiques Auth et la composition opérationnelle complète R01 restent
à réaliser ; leur présence n'est pas déduite de ces participants.


### Lecture propriétaire des métadonnées Auth et pont vers C10

Le lecteur des métadonnées R01 appartient à Auth. Il consulte la ligne
AuthBootstrapAuthorization réellement persistée, vérifie la preuve, la
politique, le challenge stocké et leur validité courante, puis rapproche les
faits avec l'acte attendu. La ressource retournée est
`pixs.auth.bootstrap:<clé primaire UUIDv7>`, selon le namespace Auth existant ;
elle n'est pas construite depuis l'identifiant d'opération. PLATFORM découle
du modèle propriétaire non scoped et ne crée aucun Subject, compte Core ou
mandat applicatif pour l'opérateur initial.

Ce lecteur reste lié à l'acte, à l'alias et à la transaction PostgreSQL native,
au processus et au thread de l'invocation. Il ne prépare aucune écriture :
les savepoints imbriqués légitimes du participant Auth conservent le même
cadre natif. Il stabilise la ligne lue et ne retourne ni credential, signature,
nonce, clé ou paramètres privés de connexion. Sa liaison publique readonly
sert uniquement à vérifier le câblage de composition.

Le pont de classification est placé dans backend/installation, sans
dépendance Auth vers backend. Il consomme ce lecteur Auth et un bail réel du
catalogue C10, exige le propriétaire pixs.auth, la couverture de la ressource
persistée et l'égalité de son triplet de classification avec le profil publié.
Publication, version, empreinte et profil sont pinés puis revalidés à chaque
résolution ; une rotation ou révocation invérifiable ferme le raccord.

Ces sources lisent une autorisation existante. Elles ne publient pas la
politique, l'autorisation initiale ou le credential préparé et ne démontrent
pas l'origine de sources de confiance injectées. Leurs producteurs protégés
et la composition R01 complète restent nécessaires. Les tests PostgreSQL,
de signature courante, de catalogue et de reprise restent dans la phase 2.


### Codec privé de projection technique 1.0.0 — réalisation avant tests

Le codec C08 de technical_projection.py représente le document fermé déjà
défini dans projection-contract.md. Il utilise uniquement la bibliothèque
standard et peut être chargé avant PostgreSQL ; il ne dépend ni de Core/Auth,
ni de Django ou du runtime PA, et ne construit aucun sujet ou contexte métier.

ProjectionLimits impose max_bytes, max_ref_bytes, max_correlation_refs et
max_causation_refs sans défaut de production. Les références sont bornées en
octets UTF-8. Le parseur refuse types étrangers, clés inconnues ou dupliquées,
nombres/non-finis, représentation JSON non canonique et ensembles d'effets
incohérents. Les tableaux A07 conservent leur ordre et leurs doublons. Le dump
et le SHA-256 revalident le document et les limites ; aucun digest de soi-même,
plan, confirmation ou signature n'entre dans la projection.

Le codec refuse INITIALIZE_START, RECREATE et DATABASE_DROP selon les
capacités PA actuellement sélectionnées. Il ne qualifie pas un profil opaque
ni l'absence réelle d'un cluster : ces faits restent propriétaires PA. Les
sources de tests unitaires préparent cas nominaux, bornes et refus, sans
exécution pendant cette phase. Aucun transport, publication, autorisation ou
producteur E4 positif n'est livré par ce seul codec. La proposition de raccord
1.1 reste distincte et n'est pas adoptée par cette réalisation.


### Lecteurs matériels des fichiers R01 — sans publication d'autorité

bootstrap_file_sources.py fournit deux lecteurs concrets pour les ports R01
existants : FileProofSource.resolve(proof_ref) et
FileTrustSource.resolve(version). Le premier relit le message canonique R01
existant, préfixe inclus, et une signature détachée brute de 64 octets ; il
reconstruit les faits et recontrôle les octets canoniques, sans vérifier à sa
place l'autorisation cryptographique courante d'AuthBootstrapBackend.

ProtectedSourceFile impose path, expected_sha256, owner_uid, owner_gid,
directory_uid, directory_gid, parent_identities et max_bytes.
FileProofSourceConfig impose message, signature, proof_ref et challenge_sha256 ;
le plafond du message reste celui du profil R01 existant (128 Kio), la signature
reste exactement 64 octets. FileTrustSourceConfig impose policy, policy_ref,
policy_version, publication_ref et max_keys. Aucune valeur de déploiement,
propriétaire, référence, empreinte ou taille n'est fournie par défaut.

La politique publique utilise un format JSON privé fermé
schema=pixs.auth.bootstrap-trust.v1, policy_ref, publication_ref et policy ;
policy contient version et keys. Chaque clé reprend les seuls champs
BootstrapTrustKey, avec public_key_hex de 32 octets, dates UTC à six décimales
et revoked booléen strict. Aucun matériau de clé privée, certificat PEM ou
payload PZT nouveau n'est introduit. Les faits consommés restent serveur et
n'entrent jamais dans le message signé.

Chaque résolution refait le parcours dir_fd sans lien symbolique, contrôle
parents autorisés, répertoire final 0700, fichier régulier 0600 de propriétaire
attendu et lien unique, puis bornes, empreintes et identité fd/chemin/parent
avant-après. Aucun fichier n'est créé et aucun verrou long ne bloque une
publication de révocation. Remplacement visible ou empreinte divergente ferme
la source ; les diagnostics n'affichent ni chemin ni contenu.

Ces lecteurs n'établissent pas l'origine de leur configuration. Elle provient
obligatoirement de la composition protégée et de la procédure externe de
préautorisation, jamais d'un corps appelant. Ni fichier, UID 0, empreinte,
clé ou dataclass seuls ne créent une autorité. La publication initiale, l'état
d'autorité courant, la protection contre restauration et la sélection du
propriétaire après D6 restent à raccorder et qualifier. Les tests fichiers,
signature courante, substitution et reprise restent différés à la phase 2.


### Session privée R01 Auth — réservation, intention et challenge sans cycle

AuthBootstrapSession réserve un PK UUIDv7 et les références Auth avant le
calcul du plan. Elle ne crée aucune ligne SQL, identité ou autorité.
prepare_initial compare deux valeurs privées concordantes et utilise le
hash_password existant ainsi qu'une InitialLocalAuthSelection complète.
external_subject est explicite ; provider et issuer viennent du profil choisi.
Aucun nom, règle, assurance, mot de passe ou profil n'est inventé. Seule une
référence d'intention opaque sort vers le plan ; le préparé reste dans Auth.
REUSE refuse toute préparation de credential.

Le plan C08 est construit avec cette référence. bind_plan lie ensuite une
seule fois l'acte et son empreinte, rapproche les références/opération/
installation/cible/effets, puis produit les faits R01 depuis l'acte réel :
sujet opérateur, version de plan et tenant sont conservés. Le nonce de 32 octets
et la fenêtre R01 existante de 600 secondes sont créés avant signature ; un
appel répété identique restitue le même challenge encore valide, sans remise
à zéro. Une divergence ou expiration ferme la session.

alias, clock et max_password_bytes sont des paramètres obligatoires de
composition protégée. La session possède une seule réservation réellement
émise, contrôlée par identité d'objet, processus et thread ; un draft équivalent
construit par un appelant n'est pas accepté. Le descripteur public porte
CREATION_INTENT, jamais une ressource existante. Le futur bridge C10 doit
vérifier cette intention et le PK prévu avant INSERT.

Les méthodes de claim/fin/quarantaine sont privées au publisher Auth.
La transition PUBLISHED n'est pas une preuve de commit : seul le futur
publisher l'appelle après son commit connu, et AuthBootstrapBackend relit
encore la vraie ligne et les sources courantes avant tout effet métier.
Aucune donnée ou booléen client ne prouve un commit. La perte du préparé avant
résultat métier exige un nouveau plan/confirmation ; une issue déjà committée
se restaure par inspection autoritative sans nouveau secret. Fermer la session
libère les références mais ne garantit pas l'effacement des str Python.

La publication SQL, le bridge de création C10, le raccord C08 au plan protégé
et la source d'interaction privée restent à réaliser. Cette session seule
ne démontre ni leur disponibilité ni la provenance de leurs configurations.
Les tests de cycle, objets forgés, bornes UTF-8, fenêtre figée, REUSE, fermeture,
quarantaine et publication réelle demeurent en phase 2.


### Bridge C10 de création Auth et inventaire propriétaire partagé

C10AuthCreationBridge consomme une réservation réellement émise par
AuthBootstrapSession, son PK prévu et un bail réel du catalogue C10. Il
vérifie CREATION_INTENT, le namespace Auth, les liaisons de la session et
la couverture exacte de la référence par un profil propriétaire pixs.auth.
Il ne déclare aucune ligne existante et ne détourne pas le resolver ordinaire
Auth ni le lecteur de métadonnées post-publication. using, session, draft et
metadata_lease sont obligatoires. Le triplet retourné est celui du profil
courant, dont publication, version et empreinte sont pinées puis revalidées.

Pour permettre au futur publisher de calculer REUSE avant la création de la
ligne d'autorisation, _target et _reuse_target_inventory délèguent à deux
helpers privés dans le même module Auth : _read_bootstrap_target et
_read_reuse_target_inventory. Les requêtes, colonnes, conditions ACTIVE,
versions et octets de l'inventaire canonique restent inchangés. Les wrappers
du consommateur existant sont conservés ; aucun digest reçu du client,
copié d'INITIAL ou inventé n'est introduit, et aucun faux backend n'est
construit pour accéder à cet inventaire.

Le publisher SQL, son contrôle de publication/commit, le raccord depuis le
plan protégé et la composition R01 complète restent à réaliser. Ni ce bridge
ni un helper d'inventaire ne vérifient à leur place l'autorisation d'installation.
Les contrôles de création/mauvais propriétaire/draft forgé/catalogue périmé,
les régressions Auth INITIAL/REUSE et la concurrence PostgreSQL restent
différés à la seconde phase.

### Publication propriétaire de l'autorisation R01 Auth — sources à qualifier

Le publisher privé Auth enregistre une réservation réellement émise par
AuthBootstrapSession, après vérification de la signature courante avec les
lecteurs de preuve et de confiance protégés. Les faits attendus, le nonce,
le challenge et la fenêtre proviennent de la session serveur. La publication
ne renouvelle aucun de ces éléments et ne publie pas l'autorité des fichiers
de confiance. La composition fournit le lecteur Core, le bridge de création
C10, le participant C05 et une version de composant explicite.

La publication utilise une transaction PostgreSQL durable propre, distincte
de l'acte métier Core. Elle refuse une transaction englobante ou une connexion
non saine. Avant toute ligne Auth, elle prend les mêmes gardes Core
installation, binding, UUID cible, opération et tenant ciblé le cas échéant.
La garde opération sérialise les publications coopérantes, car operation_ref
n'est pas unique tant que l'autorisation n'est pas consommée. Une collision
sur PK, référence d'autorisation, référence de preuve ou opération ferme
cette entrée, même si la ligne paraît identique. Aucun ancien résultat n'est
annoncé comme restauré par cette fonction.

Le bridge C10 vérifie les métadonnées de l'intention avant l'insertion et
à la barrière finale. Le digest privé INITIAL vient du credential préparé
par Auth ; REUSE relit l'inventaire réel sous les gardes propriétaires.
Aucune empreinte privée ne sort dans la référence publique retournée.
L'insertion conserve le PK prévu, les faits et dates exacts, la version 1,
ACTIVE/RETAINED et les métadonnées C10 courantes. Les champs de consommation,
de signature vérifiée et de vérification restent nuls ; Auth les contrôle
de nouveau lors de l'acte Core.

Un événement générique C05 décrit cette publication dans la même transaction.
Il porte l'acteur R01 effectivement vérifié, la ressource Auth, la corrélation
et la causalité de l'acte et le composant pixs.auth. Son contexte PLATFORM
conserve tenant_reference nul, même si l'acte cible un tenant. Il ne contient
ni preuve brute, signature, mot de passe, digest de credential ni politique
brute, et ne simule aucune décision ALLOW. Le publisher utilise le retour
CoreAuditEvent réel de stage_generic, puis le contrôle transactionnel C05.
La relecture exacte Auth et audit, la politique C05, la classification, la
signature, la sélection ou l'inventaire et l'identité physique de transaction
sont contrôlés avant la sortie durable.

La session n'est marquée publiée qu'après une sortie de transaction connue
et une connexion saine. Les erreurs après le claim mettent ses références
privées en quarantaine ; aucune issue inconnue ne déclenche de réessai caché.
Un échec de remise après commit connu reçoit le code distinct
AUTH_BOOTSTRAP_PUBLICATION_COMMITTED_UNAVAILABLE ; l'état privé de quarantaine
ne transforme pas ce commit en rollback ni en constat SQL inconnu.
Une référence de publication ne prouve ni décision Core, ni création de
compte, ni résultat métier. L'inspection après publication existante ou
commit inconnu, la composition complète et la preuve de provenance des
publications protégées restent des raccords distincts à réaliser.
La propriété clock de la session expose seulement son horloge protégée sous
sa garde existante, sans credential ni état privé.

Les recettes de phase 2 couvrent signatures absentes, divergentes, expirées
ou révoquées, draft/session substitués, catalogue périmé, collisions et
concurrence d'opération, inventaire REUSE modifié, sélection expirée, erreur
C05 et rollback commun, rupture de connexion et réponse perdue au commit.
Ces sources ne sont ni compilées ni testées par leur écriture.

### Liaison du plan protégé C08 au challenge Auth — sources à qualifier

C08AuthPlanBinding réutilise le writer C08 réel, son stockage privé du plan,
son acte, son enveloppe, ses confirmations et son bail de métadonnées C10.
Il ne lit aucune ligne Auth et ne reçoit ni credential préparé ni digest
privé. Sa construction vérifie les instances propriétaires, l'alias, le
processus, le thread et l'horloge partagée. Elle relit le plan protégé,
vérifie les liaisons existantes puis appelle bind_plan avec le digest du
plan et son intention de credential. Elle conserve l'instance de challenge
réellement retournée par Auth.

L'ordre de composition est explicite : réservation et préparation Auth,
publication du plan, construction du writer puis du raccord, présentation
et signature du challenge, enfin publisher. Le raccord lie donc le challenge
avant le claim de publication, sans dépendre d'une ligne Auth encore absente.
Chaque résolution relit le plan courant et ses confirmations via le writer,
contrôle la liaison des faits et exige le même challenge sans renouveler
nonce ou fenêtre. Un plan changé, un propriétaire substitué ou un contexte
de processus différent ferme le raccord.

Le publisher exige ce port sans défaut ni repli. Avant chacune de ses trois
vérifications cryptographiques, il contrôle la liaison exacte session/draft/
alias et exige le retour de l'instance de challenge de son matériau privé.
Auth ne dépend pas du backend et ne consulte pas ses détails de stockage.
Les gardes PostgreSQL, métadonnées, écritures, audit, relectures et traitements
de commit du publisher restent ceux du sous-lot précédent.

Ces liens structurels ne constituent pas un consentement et ne remplacent
pas la signature réelle de l'opérateur. Le raccord ne publie aucune confiance,
ne crée aucune confirmation et ne réalise ni la CLI complète, ni l'inspection
de reprise d'une publication existante, ni le transport PA/PZT. Les recettes
de phase 2 vérifieront plan et intention modifiés, confirmations divergentes,
mauvais alias/draft/horloge/processus, challenge remplacé et péremption entre
liaison et commit. Aucune exécution produit n'est déduite de ces sources.

#### Proposition Q1.4-C10-PUBLISH — autorisation distincte de publication

Statut : adopté documentaire sur accord humain. Le catalogue TOML et le raccord minimal C10
restent les choix déjà validés. Ce complément choisit le mécanisme permettant
à l'opérateur autorisé de publier les déclarations des composants pendant
une première installation autonome, sans Pixs préexistant.

La même clé personnelle Ed25519 déjà préautorisée pour l'opérateur peut être
employée uniquement si sa préautorisation courante accorde explicitement
la finalité de publication C10 pour cette installation et ces cibles.
Cette permission est distincte de R01 et du mandat technique PA. Ni une
signature R01/E4, UID 0, une clé nouvellement présentée par PBO, une clé SSH,
la propriété d'un fichier ou son empreinte ne crée cette permission.

Le mandat privé C10 possède un domaine canonique séparé,
pixs.c10.catalog.publish.v1. Il lie l'identité et la clé de l'opérateur,
l'installation, l'opération, les octets exacts du catalogue TOML, les
déclarations et profils composants concernés, les ressources couvertes,
les versions, la publication précédente attendue ou son absence initiale
explicite, les références de politique et les validités. Son contenu ne
contient aucun secret. Les paramètres, bornes, références et permissions
proviennent de la configuration protégée ; aucune valeur de production
n'est inventée. La préautorisation et sa source courante restent distinctes
du mandat présenté ; le signataire ne publie pas sa propre confiance.

L'éditeur vérifie signature, autorité et révocation courantes, cibles,
validités et ancienne publication avant tout effet, sous la garde exclusive
du catalogue et à la barrière de publication. Il valide les profils selon
leurs propriétaires, attend la fin des lecteurs dans la borne configurée,
puis réalise temporaire privé, fsync, remplacement atomique et relecture.
Un conflit, une politique périmée ou une issue de durabilité inconnue ferme
la publication ; aucun ancien mandat n'est rejoué automatiquement. Le
journal durable pré-base et son relais C05 restent requis avant disponibilité
et conservent le propriétaire C10 de l'événement. Leurs raccords réels sont
à réaliser et qualifier, sans assimiler ce catalogue au service C10 complet.

Ce choix ne crée aucun nouveau droit R01 ou PA, fournisseur distant, service
d'infrastructure, index NV ni opération TPM. Il ne prétend pas apporter une
protection générale contre restauration par la seule signature ou le fichier.
Les garanties de provenance, de fraîcheur et de reprise requises restent
à prouver selon leurs propriétaires. L'adoption documentaire porte sur ce
seul paragraphe de design.md C08 ; les exigences canoniques de publication
autorisée et de gouvernance restent inchangées.

### Saisie locale privée du compte initial Auth — sources à qualifier

L'adaptateur prepare_initial_from_tty demande l'identifiant et les deux
mots de passe sur le terminal de contrôle local /dev/tty. Il utilise la
session Auth, le draft réellement réservé et la sélection locale explicite,
puis appelle le propriétaire prepare_initial. Seule la référence d'intention
opaque est retournée. Cette saisie ne crée aucun compte et ne prouve aucune
identité ni autorisation R01.

Le raccord est réservé au thread principal, avec exclusion locale non
bloquante sur la ressource terminal. Il refuse REUSE avant toute ouverture
ou question de mot de passe. Type caractère, isatty, groupe au premier plan,
ICANON et ISIG sont exigés. L'écho et l'écho de fin de ligne sont désactivés
avant les prompts constants ; les valeurs ne passent ni par stdin, argv,
l'environnement, PZT, un journal ou un fichier. La limite observée du terminal
PC_MAX_CANON, avec place réservée au terminateur, est combinée à la borne
privée Auth sans la relâcher. Cette limite décrit ce canal et ne constitue
pas une nouvelle politique universelle de mot de passe.

Les lectures sont bornées, exigent une ligne complète et UTF-8 strict et
ne retirent que le LF final. Aucun strip ou autre normalisation du secret
n'est appliqué. Le propriétaire Auth conserve la comparaison des deux
saisies, la validation de l'identifiant et le hachage existant. Un terminal
absent, un contexte divergent, un dépassement, EOF ou des valeurs refusées
ne déclenche aucun repli de saisie.

Le bloc finally commun restaure les attributs exacts avec TCSAFLUSH,
ferme le descripteur et libère le verrou, pour le succès comme pour les
exceptions prises en charge. La file d'entrée est vidée afin de ne pas
réafficher un reste privé sous l'écho restauré. Chaque échec de libération
est conservé ; une erreur ou une annulation ferme la session Auth et aucun
intent utilisable n'est annoncé. Les erreurs inattendues restent propagées.
L'effacement garanti des chaînes Python et la restauration après signal
non interceptable ne sont pas annoncés.

La bibliothèque standard suffit au profil Debian/Unix et au minimum Python
3.12 du projet. Le repli warning/stdin documenté par
[getpass](https://docs.python.org/3.13/library/getpass.html) est écarté ;
les opérations de terminal suivent l'interface
[termios](https://docs.python.org/3.13/library/termios.html), sans modifier
des gestionnaires de signaux ou des filtres globaux d'avertissement.

Les recettes PTY de phase 2 doivent contrôler l'absence d'écho de chaque
valeur, le retour de l'intention seule, la restauration du terminal et
l'absence de fuite après succès, divergence, dépassement, EOF, SIGINT ou
erreur de libération. Les bornes UTF-8, REUSE sans prompt et le refus d'un
autre thread ou terminal restent requis. Aucune recette n'est exécutée par
l'écriture de ces sources ; la CLI complète reste un raccord distinct.

## Retrait de la préparation initiale PA — principes adoptés

Le retrait supprime irréversiblement la nouvelle préparation initiale PA. Il conserve la remise technique minimale canonique de connexion au workload PBO et n'invente aucune autorité ordinaire déjà admise.

L'action withdraw_initial_authority est de classe Critique, dans le domaine PA_POSTGRESQL_WITHDRAWAL, sous la permission WITHDRAW_PA_INITIAL. Le mandat correspondant est un document fermé et versionné, signé par la clé privée personnelle Ed25519 de l'opérateur, conservée hors runtime et hors agents. Ce mandat est distinct des mandats R01 et E4, par son domaine, sa finalité, ses références et sa validité propres. La clé d'administration PA et les clés de la PKI et du TLS Z12 ne sont jamais réutilisées implicitement.

C08 présente et confirme ce retrait à partir du plan et de la projection courants. La confirmation utilise les contrats courants C03 et C04, avec un mapping explicitement vérifié vers le signataire. Aucun booléen verified fourni par l'appelant et aucun SuperAdmin auto-attribué ne vaut confirmation ou autorisation.

Avant tout effet de retrait, PA vérifie la signature et la clé, la politique courante, l'absence de révocation, la validité et la fraîcheur UTC fondée sur une référence fiable, les identités natives de l'appelant et de l'exécutant et leur relation PZT, l'installation et la cible, le plan, l'opération, la corrélation et le contexte, ainsi que l'absence de consommation antérieure du même mandat. PA vérifie ensuite la quiescence des effets de préparation concernés, puis ancre durablement et irréversiblement le retrait. Un DTO à l'état RETIRED, un résultat PG_SUCCEEDED, un mode NORMAL ou D6 seul ne prouvent pas ce retrait.

Le retrait appartient à une famille administrative distincte des trois opérations PostgreSQL conservées inspect_postgresql, prepare_postgresql et get_postgresql_result. Aucun quatrième ajout n'est apporté à leur catalogue 1.0. Aucune inspection administrative n'est réalisée via get_postgresql_result. L'inspection administrative Protégé reste disponible sous l'autorisation courante de son propriétaire. Elle ne rouvre ni extension, ni préparation, ni retrait rejoué.

Les contrats de topologie D8/D6, de wire et de résolveurs restent à fermer en revue commune avant leur code, les qualifications réelles en phase 2 après réalisation, sans élargir les accords par ce texte. Le retrait suppose les prérequis applicatifs, les migrations, R01, Core, Auth et les audits rapprochés, sans exiger que l'autorité ordinaire PA soit déjà active pour retirer l'autorité initiale. Les propriétaires PA et Z12 et leurs deux retraits restent distincts. Aucun ordre nouveau et aucun wire exact ne sont adoptés ici. L'adoption des principes ne vaut pas réalisation ; les résolveurs et les preuves restent à produire et qualifier.

## Raccord exact d'audit C05 pour la publication R01

La relecture exacte passe par le reçu public GenericAuditReceipt et le port verify_generic_exact, en même transaction, avec événement déterminé, octets canoniques, redactions et digest sous politique courante, et contexte, alias, opération, token et XID courants. Le reçu ne contient que des métadonnées non secrètes, aucun objet ORM, et aucune valeur ne confère autorité. Les consommateurs existants de stage_generic restent inchangés.

### E5 adopté documentairement, non réalisé ni qualifié

L'échange 1.1, l'observation, le planning, les préconditions stagiées, les effets et la confirmation décrits dans la projection et les contrats PA01 sont adoptés documentairement et restent non réalisés ni qualifiés. La séquence explicite est OBSERVE, puis observation PA reçue et vérifiée, puis projection C08 immuable liée à cette observation, puis PREPARE_PLAN avec retour du bundle vérifié, puis présentation et confirmation C08, puis nouvelle PREPARE critique signée, puis READ_RESULT distincte. Les raccords à fournir sont les producteurs et résolveurs propriétaires, le transport PZT et A07 avec corrélations et causalités complètes, la persistance des plans et résultats, les handlers et la réconciliation, avant toute activation. Les critères à prouver en phase 2 sont les refus d'action et d'effet inconnus, les divergences d'observation et de plan, les préconditions et confirmations manquantes ou périmées, la conservation de l'ordre et des doublons A07, et les effets réels sur les seuls environnements autorisés. Le statut Q1.4 adopté documentairement est conservé sans changement.

### Entrée Core publique modes C08 et fabrique C08 fermée

L'entrée Core publique execute_modes_transition et la fabrique C08 build_modes_transition conservent les gardes et propriétaires existants sans nouvelle capacité ni dépendance. La fabrique construit seule participant, ports, apply et scopes avec la borne protégée du propriétaire. Core sélectionne cette fabrique connue, re-dérive l'ensemble avec la borne fournie et appelle la transaction avec owner littéral pixs.backend. Aucune qualification produit ni coche n'est apportée par ce texte.

## Réalisation partielle E5 du 26 octobre 2026 — sources à tester

Le présent ajout est strictement documentaire, sans nouveau choix normatif, sans effacement ni modification du texte historique. Il constate l'état des sources et des jalons restants.

Sources E5 aujourd'hui écrites à tester, zéro exécutées : quatre codecs `src/pixs/backend/installation/exchange_envelope_1_1.py`, `planning_bundle.py`, `exchange_response_1_1.py`, `postgresql_confirmation.py` ; fixture `tests/unit/c08_e5_fixtures.py` ; quatre suites totalisant 84 méthodes `test_c08_exchange_envelope_1_1.py`, `test_c08_planning_bundle.py`, `test_c08_exchange_response_1_1.py`, `test_c08_postgresql_confirmation.py` ; présentation privée `src/pixs/backend/installation/pre_confirmation_presentation.py` et sa suite `tests/unit/test_c08_pre_confirmation_presentation.py` de 12 méthodes ; soit 96 méthodes préparées non exécutées. Aucun import de qualification, contrôle syntaxique, test produit, accès PostgreSQL ou effet TPM/NV exécuté pour ces sources à ce jalon ; aucun nouveau cochage, archivage ou changement canon/Git.

Présentation pure à codecs publics : affiche actions, effets, observations, préconditions et bindings, chaînes `json.dumps ensure_ascii=True` échappées, confirmation facultative rapprochée seule sans autorité. La présentation ne collecte pas consentement, ne signe, ne lit fichiers/réseau/horloge et ne remplace pas CLI intégrée.

Restent à réaliser ou qualifier, sans déduire tous écrits depuis DTO : séquence runtime OBSERVE/PREPARE_PLAN/PREPARE/READ_RESULT, producteurs, résolveurs et persistance relevant des documents E5 ; signature E4 1.1, PZT, A07 avec corrélations et causalités complètes, réconciliation, handlers, CLI intégrée.

Retrait PA : quatre formats proposés non adoptés en revue C7, contrats propriétaires distincts, aucun code retrait.

Temps : reprise du temps C6 adoptée documentairement, pas de correction normative C08 indispensable identifiée et aucune qualification runtime déduite.

### Stockage bundle E5 — conception retenue, non réalisé

Le présent ajout fixe la conception du stockage privé immuable du seul `PlanningBundle`, sans nouveau choix fonctionnel, sans modification de l'historique ni des fichiers existants. Source et tests non encore écrits ni exécutés, aucun artefact PG. `Confirmation` hors lot. Configuration privée fournie par la future composition protégée, aucune `env`/valeur par défaut.

Fichier prévu : `src/pixs/backend/installation/planning_bundle_store.py`, privé C08. Signatures : `PlanningBundleStoreConfig`, `PlanningBundleStoreRefused/Unknown/Busy/Conflict/IssueUnknown`, `initialize_bundle_guard(config)`, `publish_bundle(config, bundle) -> str`, `read_bundle(config) -> PlanningBundle`. Octets exacts `dump_planning_bundle/parse_planning_bundle`, liaison exacte `planning_bundle_binding`, digest exact `planning_bundle_sha256`.

Champs `Config` : `io: MarkerConfig` sept champs existants `path/owner_uid/owner_gid/max_bytes/max_ref_len/allowed_format_versions/parent_identities` ; `lock_basename: str` ; `bundle_limits: PlanningBundleLimits` quatre champs `payload/projection_limits/preconditions_limits/max_bundle_bytes`. Garde unique stable partagée par chemin de document. `io.max_bytes >= max_bundle_bytes`, lecture bornée à `max_bundle_bytes+1`. `max_ref` bundle et `io` non forcés égaux, objets différents. Schéma bundle `1.0.0` fixe admis par `io.allowed_format_versions`, seul `plan_version` opaque préservé.

`_publish` par `os.replace` seulement si absent sous garde `EX`, octets existants divergents jamais remplacés, `Conflict` fermé, idempotent si identiques. `read_bundle` durable pour inspection, puis comparaison `binding`/octets attendus par le propriétaire après issue inconnue avant toute publication nouvelle, jamais boucle de retry. Couche lecteur privé, pas résolveur signé ni autorité, sans preuve de provenance/consentement/politique/fraîcheur/`PZT`.
