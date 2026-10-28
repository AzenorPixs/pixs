# Conception — C10

## Statut et périmètre autorisé

RÉCONCILIATION_DOCUMENTAIRE au 26 octobre 2026, sur validation explicite du développeur après audit ACSM. Les quatre documents actifs C10 sont seuls modifiables ; les archives, le canon et les sources sont préservés. Des raccords initiaux C10 existent dans le périmètre C08, sans preuve ici de qualification intégrée ni de livraison complète C10. Les dix tâches restent non cochées. C00 a été adopté et archivé le 18 octobre 2026 ; ses précisions normatives sont intégrées au canon. Les sections de préparation conservées ci-dessous gardent leur portée historique ; l'état courant, les décisions acquises et les barrières restantes sont explicités dans la réconciliation datée.

## État actuel vérifié

Constat de préparation : Profils de gouvernance, vocabulaires de rétention et tombstone-v1 sont déclaratifs ; ils ne prouvent ni purge ni propagation durable. Ce constat reste valable pour les structures pures ; il ne constitue plus un inventaire exhaustif des raccords présents. Voir l'inventaire daté ci-dessous.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/kernel/data_governance_profile.py](../../../src/pixs/kernel/data_governance_profile.py).
- [src/pixs/kernel/data_tombstone_profile.py](../../../src/pixs/kernel/data_tombstone_profile.py).
- [src/pixs/kernel/data_subject_request.py](../../../src/pixs/kernel/data_subject_request.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Déclarer les profils des données Core/PZT/DNS et appliquer politiques dans leurs services propriétaires. Demandes d’accès/export/rectification/effacement/restriction et purge restent des Commands autorisées, auditées et idempotentes. Les dérivés présents et les sauvegardes C16 réappliquent tombstones et holds ; pas de dépendance implicite au service Bulk complet.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Rétentions, droits de demandes, contrats des dérivés et procédure de purge à revoir ; valeurs existantes du canon conservées et exception Super Admin distincte des profils purs.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [add-core-postgres-services](../archive/2026-10-20-add-core-postgres-services/proposal.md).
- [integrate-runtime-authorization-and-super-admin](../archive/2026-10-21-integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md).
- [add-reference-worker-scheduler-and-event-delivery](../archive/2026-10-23-add-reference-worker-scheduler-and-event-delivery/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Donnée non classifiée non exposée ; purge ordinaire prématurée refusée ; demande rejouée sans double effet ; dérivés réellement présents traités ; tombstone préservé à la restauration ; exception Super Admin conforme et distincte des structures.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T03 — Réadmission après état restauré

La restauration cohérente de données ne prouve ni fraîcheur de révocations/incidents ni admissibilité des effets différés. N05 dédié et delta ciblé validés ; faits nécessaires et revalidation détaillée à définir avant code.

Contrôles à intégrer : Snapshot antérieur à révocation/rotation/incident ; Effet déjà engagé dont réponse perdue ; Marqueur externe incohérent ; Interruption puis reprise de réconciliation sans réémission automatique.

### T12 — Effacement et restauration des dérivés présents

Un snapshot peut précéder l’effacement ; un tombstone présent seulement dans le même snapshot ne prouve pas l’absence de résurrection. Préciser source des effacements applicables et preuve avant exposition dans C10/C16/N05 ; refuser la garantie si faits absents.

Contrôles à intégrer : Restauration après effacement confirmé ; Hold/retenue et rétention selon canon ; Aucun export/demande exigeant implicitement tout Bulk ou stockage objet.

### T16 — Options, profils structurels et renvois Bulk

Un rattachement à un lot P0 n’active pas tout le domaine : Bulk, LDAP, flags avancés, quotas, SDK, sandbox et intégrité avancée restent conditionnés. Déclarer sélection/absence et maintenir les profils structurels existants ; ne pas traiter la non-sélection comme dispense d’une clause applicable.

Contrôles à intégrer : Absent représenté sans readiness fictive ; Contrat consommé réutilisé sans activer tout le catalogue ; Aucun code distant ni composant DEVELOPMENT en production ; Pas de promesse universelle de performance/HA.

Voir [audit transversal durable](../archive/2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.

## Réconciliation documentaire du 26 octobre 2026

### Mandat et portée des constats

La validation humaine couvre la réconciliation documentaire, la matrice des contrats propriétaires, le lien C09 et les empreintes. Elle ne valide aucun comportement produit, aucune tâche de livraison, aucune levée globale des barrières et aucune opération sur une archive. Les références archivées sont consultées comme contrats et preuves historiques, sans réouverture ni modification. Les lectures de code éclairent l'état présent ; aucune recette applicative n'est exécutée par ce mandat.

L'audit ACSM a identifié une traçabilité incomplète entre la préparation C10 et les sources partielles suivies par C08. Les tableaux suivants rapprochent ces sources des obligations déjà canoniques ; ils n'ajoutent aucun contrat normatif, paramètre d'exploitation, droit, durée de rétention ou provider. Les exigences et scénarios restent ceux de [requirements.md](requirements.md).

### Inventaire des sources partielles et des preuves

| Ensemble observé | Sources présentes | Responsabilité et limite | Tâches C10 concernées |
|---|---|---|---|
| Structures préparatoires | [DataGovernanceProfile](../../../src/pixs/kernel/data_governance_profile.py), [DataSubjectRequest](../../../src/pixs/kernel/data_subject_request.py), [tombstone-v1](../../../src/pixs/kernel/data_tombstone_profile.py) | Représentations et validations structurelles ; aucune exécution de demande, purge, persistance ou propagation déduite de ces structures. | 1.1, 2.1–2.3 |
| Catalogue initial | [c10_catalog.py](../../../src/pixs/backend/c10_catalog.py) | Lecteur TOML protégé, profils épinglés, garde partagée, contrôle de validité et révocation. La configuration et le digest ne prouvent pas l'autorisation de publication ; ce lecteur ne fournit pas l'éditeur. | 1.2, 2.1 |
| Attestation et reçus initiaux | [c10_governance_adapter.py](../../../src/pixs/backend/c10_governance_adapter.py), [c10_receipt_record.py](../../../src/pixs/backend/c10_receipt_record.py), [migration 0014](../../../src/pixs/backend/migrations/0014_c10_initial_governance_receipts.py) | Adaptateur initial Core limité à l'action d'amorçage et au contexte PLATFORM ; reçus ATTEST/READ liés à opération, token et transaction PostgreSQL native. authorize_state_change refuse les transitions. La présence d'un reçu préparé ne prouve pas le commit composé Core/Auth/C08. | 1.2, 2.1 ; ne réalise pas 2.2–2.3 |
| Ponts de classification et modes C08 | [auth_classification.py](../../../src/pixs/backend/installation/auth_classification.py), [auth_creation_bridge.py](../../../src/pixs/backend/installation/auth_creation_bridge.py), [mode_governance.py](../../../src/pixs/backend/installation/mode_governance.py) | Rapprochement de métadonnées Auth via ses interfaces propriétaires et de profils backend pour les opérations de modes déclarées. Aucun droit, publication autorisée, demande de données ou purge générale n'est fourni par ces ponts. | 1.2, 2.1, 2.4 |
| Sources de vérification dédiées | [test_c10_catalog_files.py](../../../tests/unit/test_c10_catalog_files.py), [test_initial_governance_postgres.py](../../../tests/integration/test_initial_governance_postgres.py) | Tests de fichiers/catalogue et recette de migration/reçus PostgreSQL présents. Les catalogues de recette sont des fixtures explicites ; ces fichiers ne prouvent ni leur exécution réussie, ni le publisher autorisé, ni l'acte C08 complet. | 2.1, 2.4, 3.1–3.2 |

La [réalisation partielle C08 du 23 octobre](../add-installation-and-first-configuration/design.md#réalisation-partielle-c08--23-octobre-2026-avant-phase-de-tests) documente l'écriture du catalogue, de l'adaptateur, du modèle et de la migration 0014. Le [bilan courant C08](../add-installation-and-first-configuration/VALIDATION.md) conserve 2.6 ouverte : attestation et revalidation G01–G03 non qualifiées dans les preuves consultées. Ses 232 succès locaux historiques ne remplacent pas cette preuve. La réconciliation présente n'affirme ni absence physique de code ni absence de toute exécution antérieure ; elle distingue les preuves effectivement référencées des résultats non établis.

### Décisions acquises et publication autorisée

Le choix [Q1.4-GOV-SOURCE](../add-installation-and-first-configuration/design.md#contrat-minimal-14--catalogue-local-protégé-hors-base-à-ouvrir-choix-validé) est adopté : catalogue TOML protégé indépendant de la base à ouvrir et raccord minimal propriétaire C10 consommé par C08/2.6. Les profils et la déclaration des données restent sous leurs propriétaires ; l'attestation C10 ne transfère aucune autorité métier et le futur compte initial ne peut fournir sa propre dérogation.

Le complément [Q1.4-C10-PUBLISH](../add-installation-and-first-configuration/design.md#proposition-q14-c10-publish--autorisation-distincte-de-publication) est également adopté documentairement. La finalité de publication du catalogue est distincte de R01 et du mandat technique PA. Le domaine privé pixs.c10.catalog.publish.v1 lie opérateur préautorisé, installation, opération, octets et profils exacts, ressources, versions, publication précédente attendue, politique et validités. L'éditeur contrôle signature, autorité et révocation courantes sous garde exclusive, puis applique publication durable et relecture ; journal pré-base et relais propriétaire C05 restent requis avant disponibilité. Ces choix ne sont pas remis au vote et leur adoption ne prouve aucune réalisation ou qualification du publisher.

Les chemins, ancrages, propriétaires natifs, bornes de validité/fraîcheur et références de politique proviennent d'une configuration protégée à fournir et qualifier. Aucun défaut de production n'est repris des fixtures. Les rétentions, droits des demandes, contrats de dérivés et conditions de purge encore ouverts restent à déterminer dans le canon applicable avant leur réalisation dépendante.

### Matrice des contrats propriétaires

Chaque ligne identifie le propriétaire, les entrées/sorties ou points d'application existants, les refus à préserver et les preuves futures nécessaires. Les identifiants CP-01 à CP-08 servent uniquement à la traçabilité documentaire ; ils ne déclarent aucune interface nouvelle. Les raccords déjà présents restent réutilisables après relecture et qualification des preuves affectées.

| Réf. / propriétaire et source | Contrat consommé ou point d'application | Invariants et refus à préserver | État observé et critère de qualification future | Tâches |
|---|---|---|---|---|
| CP-01 — C02/Core ; [archive et validation](../archive/2026-10-20-add-core-postgres-services/VALIDATION.md), [ports actuels](../../../src/pixs/core/ports.py) | GovernanceProvider.attest retourne GovernanceAttestation ; stage_read et authorize_state_change retournent StagedRef ; verify_staged contrôle TransactionProof. Les mutations restent exécutées par les services Core. | Profil du propriétaire, couverture des ressources, contexte, version publiée, connexion/transaction et politique courantes ; absence ou divergence ferme la voie. Le CAS et l'état réel ACTIVE/ARCHIVED de la ressource sont conservés. | L'adaptateur initial ne couvre pas les opérations Core ordinaires et refuse toute transition. Qualifier attestation/lecture/transitions sur les opérations retenues avec commit, rollback, savepoint et connexion substituée, sans écriture C10 directe dans les tables métier Core. Les ports C10 des preuves archivées C02 étaient synthétiques. | 1.1–1.2, 2.1–2.4 |
| CP-02 — C03/Auth ; [limites archivées](../archive/2026-10-21-add-initial-authentication-and-sessions/VALIDATION.md), [lecteur de métadonnées](../../../src/pixs/auth/bootstrap_metadata.py), [session de création](../../../src/pixs/auth/bootstrap_session.py) | BootstrapAuthorizationMetadataReader.read expose les métadonnées propriétaires ; AuthBootstrapSession.describe expose PlannedBootstrapResource pour la réservation de création ; les ponts C10 retournent AuthDataClassification. | Propriétaire pixs.auth, ressource, contexte, opération, session/draft et classification correspondent au profil courant. Une intention de création ne vaut pas ligne existante ; aucun credential ni hash n'est transféré sous Core/C10. | Ponts présents ; leur intégration réelle reste à qualifier avec réservation effectivement émise, propriétaire/cible divergents, catalogue périmé/révoqué et rollback. L'archive C03 utilise des classifications C10 de fixture ; les interfaces ajoutées depuis l'archive sont recoupées avec le design C08 courant, sans leur attribuer les anciennes preuves. | 1.1–1.2, 2.1, 2.4 |
| CP-03 — C04/autorisation ; [validation archivée](../archive/2026-10-21-integrate-runtime-authorization-and-super-admin/VALIDATION.md), [décideur actuel](../../../src/pixs/core/services_runtime_decider.py) | RuntimeAuthorizationDecider fournit décision, revalidation sous verrous et governance_waived ; les points d'application propriétaires exécutent les obligations. | Dérogation réservée au compte et au périmètre canoniques, autorité courante et tenant accordé ; aucun droit déduit d'un profil, d'un ancien ALLOW ou du futur compte initial. | Conserver les contrôles ordinaires et qualifier les dérogations applicables de gouvernance/rétention/hold, leurs refus intertenant et leur révocation avant effet. Les preuves C04 ne qualifient pas les effets C10. | 1.1–1.2, 2.1–2.4 |
| CP-04 — C05/audit ; [validation archivée](../archive/2026-10-21-add-durable-minimized-audit/VALIDATION.md), [contrats actuels](../../../src/pixs/core/audit_contracts.py), [maintenance propriétaire](../../../src/pixs/core/audit_access.py) | AuditParticipant stage/verify_staged/reconcile_unknown ; AuditLifecyclePort.authorize_maintenance reçoit requête, référence, politique, alias, opération, job et mode. | Audit durable dans la frontière propriétaire ; mandat Job, rétention/holds/références/projections courants, dérogation canonique explicite et maintenance idempotente. L'audit reste propriétaire de sa purge et de ses tombstones. | Maintenance C05 présente, ports C10/Jobs des preuves archivées synthétiques. Qualifier leur raccord effectif et l'absence de double effet après réponse perdue ; ne pas réimplémenter cette purge comme une écriture C10 dans les tables C05. | 1.2, 2.2–2.4 |
| CP-05 — C06/idempotence ; [design archivé](../archive/2026-10-22-add-protected-core-http-commands-and-queries/design.md), [IdempotenceParticipant](../../../src/pixs/core/ports.py) | check_or_stage, stage_result, verify_staged, restore_confirmed et reconcile_unknown lient commande, contenu, sujet et contexte au résultat durable. | Rejeu identique sans double effet ; contenu divergent refusé ; issue inconnue réconciliée sans réexécuter la mutation. Aucun recours implicite au service Bulk complet. | Mécanismes propriétaires livrés selon l'archive, avec C10 synthétique dans ses recettes. Le traitement des cinq opérations DataSubjectRequest et son raccord restent à réaliser/qualifier ; vérifier concurrence, conflit, rollback et commit dont la réponse est perdue. | 1.2, 2.2–2.4 |
| CP-06 — C09/jobs et événements ; [design archivé](../archive/2026-10-23-add-reference-worker-scheduler-and-event-delivery/design.md), [outbox actuelle](../../../src/pixs/backend/c09_outbox_repository.py) | OutboxParticipant et vérificateur de gouvernance injecté à C09OutboxRepository : requête/décision, alias/opération/token, contexte, payload_refs, consommateurs, déclarations sortantes et governance_ref ; retour None attendu du vérificateur. | Consommateur et garanties déclarés, profil courant, transaction propriétaire et publication après commit ; absence d'une gouvernance requise produit C09_POLICY_UNRESOLVED. Baux/fencing, reprises et déduplication restent C09. | L'adaptateur initial C08 ne fournit pas ce vérificateur. Qualifier le raccord des jobs de purge et des tombstones aux dérivés réellement présents, refus de destination non déclarée, rollback sans publication et reprise sans double effet. Les ports C10 de la recette archivée sont synthétiques. | 1.2, 2.1, 2.3–2.4 |
| CP-07 — C14/PZT et DNS ; [design archivé](../archive/2026-10-23-add-essential-pbo-pzt-and-dns-modules/design.md), [services PZT](../../../src/pixs/pzt/services.py), [services DNS](../../../src/pixs/dns/services.py) | PztManagementPolicy/DnsManagementPolicy fournissent le profil propriétaire ; PostgresPztService/PostgresDnsService appliquent Commands/Queries et retraits logiques. | Propriétés pixs.pzt et pixs.dns distinctes, classification, isolation et CAS conservés ; aucun accès C10 aux tables privées et aucune activation d'exécutant déduite du retrait souhaité. | Services présents ; le catalogue initial limité à Core ne prouve pas leur gouvernance C10. Définir les raccords utiles aux profils/demandes/effacements, puis qualifier leurs services propriétaires avec refus de mauvais propriétaire, contexte et version, sans promettre purge ou DNS/réseau actifs depuis C14. | 1.1–1.2, 2.1–2.4 |
| CP-08 — relations actives C08/C16/N05 ; [C08](../add-installation-and-first-configuration/design.md), [C16](../add-upgrade-backup-and-restore-contracts/design.md), [N05](../add-p0-post-restore-reconciliation-and-readmission/design.md) | C08 consomme le raccord initial C10 en 2.6 ; C16 restaure et réapplique les gouvernances ; N05 coordonne les faits courants et la réadmission. Leurs contrats concrets restant ouverts ne sont pas inventés par cette matrice. | Pas de dispense par le futur Super Admin ; résultat préparé distinct d'un commit composé. Après restauration, effacements/holds et autorités applicables sont vérifiés avant exposition ou départ des traitements. | G01–G03 restent à qualifier dans le bilan C08 consulté. Définir avec C16/N05 la source des effacements et restrictions postérieurs au snapshot, puis prouver leur réapplication et le blocage en cas de faits invérifiables. C08/C16/N05 restent actifs ; ils ne sont pas des contrats propriétaires archivés. | 1.2, 2.1, 2.4, 3.2 |

La disponibilité de contrats archivés ne qualifie pas leurs raccordements C10. Les métadonnées des nouveaux reçus, résultats, checkpoints et dérivés effectivement livrés relèvent elles-mêmes des profils de leurs propriétaires ; leur couverture reste à vérifier dans les tâches concernées. La matrice n'autorise pas à réécrire leurs modèles, migrations ou archives. Les opérations fonctionnelles encore absentes restent dans les tâches C10 existantes ; toute modification normative nécessaire appelle le delta et la validation déjà prévus par proposal.md.

### Barrières restantes et état de livraison

Avant la réalisation dépendante, préciser les politiques et droits des demandes, les références et conditions de rétention/purge, les raccords CP-01 à CP-08 applicables et la source d'effacements courants indépendante du seul snapshot. Pour la publication initiale, fournir/qualifier préautorisation, configuration protégée, éditeur durable, journal pré-base et relais C05 selon le choix acquis. Aucune de ces absences de preuve n'est transformée en nouvelle valeur d'exploitation ou en remise au vote d'une décision adoptée.

Les tâches 1.1 et 1.2 restent ouvertes : cette réconciliation ne prouve ni leur revue complète ni la levée de leurs barrières. Les tâches 2.x et 3.x restent également ouvertes. La validation future associe à chaque unité ses contrats, scénarios, versions, commandes, résultats et limites avant cochage ; elle conserve la séparation entre source écrite, test exécuté, intégration qualifiée et livraison. Aucun P0 complet, archivage, activation ou publication n'est déclaré par cette mise à jour.
