# Conception — C10

État courant : le développeur valide techniquement 1.1 sur sa portée documentaire ; sa case reste non cochée sur instruction explicite. 1.2 reste OUVERTE avec ses barrières. La [validation technique documentaire](design.md#validation-technique-documentaire-de-la-tâche-11) précise cette décision ; les mentions antérieures d’absence de validation complète ou de tâches ouvertes décrivent leurs états historiques, sans annuler cet acquis ni valoir qualification produit.

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

Le profil `pbo-p0-debian-local-v1` sélectionne PA système et PZT local pour
préparer PostgreSQL, conformément au [canon de composition](../../specs/reference-composition/spec.md).
Ce parcours local et ses exécutants doivent être qualifiés ; leur disponibilité
ne se déduit pas de la seule présence des modules PBO. Le réseau PZT distant,
les autres rôles PA, le service DNS exécuté par PA, l’image Docker et les
capacités optionnelles restent hors sélection, sauf obligation du profil
explicitement sélectionné. Cette délimitation ne vaut ni réalisation ni
qualification du parcours local.


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

## C10-CONCEPTION-R1 — revue du 28 octobre 2026

Validation explicite du développeur : D1 adopté, orientations D2/D3 adoptées et quatre écritures documentaires autorisées. Les constats sont des lectures de sources, sans recette produit ni disponibilité runtime prouvée. C00 reste un cadrage daté : aucune non-sélection historique de PA/PZT ne dispense d’une dépendance effectivement requise par une unité actuelle. Les décisions canoniques acquises sont conservées.

### Complément de revue CP-01 à CP-08

| Contrat | Sources et constat actuel | Raccord et qualification restant à préciser |
|---|---|---|
| CP-01 — Core | [GovernanceProvider](../../../src/pixs/core/ports.py) et [adaptateur initial](../../../src/pixs/backend/c10_governance_adapter.py) présents ; transitions refusées par l’adaptateur initial. | Séparer amorçage et opérations ordinaires ; mutations et CAS chez Core. Prouver attestation, lecture et transitions avec commit, rollback, savepoint et connexion divergente. |
| CP-02 — Auth | [Métadonnées](../../../src/pixs/auth/bootstrap_metadata.py), [réservation](../../../src/pixs/auth/bootstrap_session.py), [classification](../../../src/pixs/backend/installation/auth_classification.py) et [pont de création](../../../src/pixs/backend/installation/auth_creation_bridge.py) présents. | Ressource projetée distincte de ressource persistée ; propriétaire, contexte, version et réservation vérifiés ; aucun credential ni hash transféré à Core/C10. |
| CP-03 — autorisation | [Décideur propriétaire](../../../src/pixs/core/services_runtime_decider.py) avec governance_waived. | Conserver l’exception Super Admin dans ses tenants accordés et les refus ordinaires/intertenant. Une dérogation applicative ne fabrique ni audit requis, transaction, fraîcheur ni effet technique. |
| CP-04 — audit | [Ports](../../../src/pixs/core/ports.py), [AuditLifecyclePort](../../../src/pixs/core/audit_contracts.py), [maintenance](../../../src/pixs/core/audit_access.py) présents. | C05 garde mutations et purge. Préciser le fournisseur des faits courants de rétention, holds, références et projections ; vérifier mandat Job et reprise sans double effet. |
| CP-05 — idempotence | [IdempotenceParticipant](../../../src/pixs/core/ports.py) expose résultat conservé, conflit et réconciliation. | Relier les cinq demandes ACCESS/EXPORT/RECTIFY/ERASE/RESTRICT au sujet, contenu, contexte et résultat durable ; issue inconnue sans rejeu aveugle. Aucun Bulk complet implicite. |
| CP-06 — jobs/outbox | [C09OutboxRepository](../../../src/pixs/backend/c09_outbox_repository.py) reçoit un vérificateur de gouvernance ; refus C09_POLICY_UNRESOLVED si les éléments requis manquent, hors dérogation admissible. | Publication après commit, consommateurs déclarés, propagation et réconciliation à qualifier. Point d’injection présent distinct d’un vérificateur C10 intégré. |
| CP-07 — PZT/DNS et complément Agent | [PZT](../../../src/pixs/pzt/services.py), [DNS](../../../src/pixs/dns/services.py), [modèles Agent](../../../src/pixs/agent/models.py) persistants et [service Agent](../../../src/pixs/agent/service.py) consommant governance_port. | Étendre explicitement la couverture CP-07 à pixs.agent, sans nouveau numéro ni transfert de propriété. Classification, isolation, souhaité/appliqué et exécution PA/PZT restent distincts ; aucun exécutant activé. |
| CP-08 — C08/C16/N05 | [C08](../add-installation-and-first-configuration/design.md), [C16](../add-upgrade-backup-and-restore-contracts/design.md), [N05](../add-p0-post-restore-reconciliation-and-readmission/design.md) : responsabilités préparées, mécanisme commun ouvert. | C10 fournit les faits, C16 restaure, N05 coordonne la réadmission. Arrêter la source d’effacements/restrictions post-snapshot et ses preuves avant exposition ; G01–G03 et intégration encore à qualifier. |

### Registre des décisions et paramètres ouverts

| Décision | État validé | Paramètres OUVERTS et condition de passage |
|---|---|---|
| D1 — couverture | ADOPTÉE : inventaire des données effectivement persistées de Core, Auth, backend d’installation, audit/jobs, Agent, PZT et DNS, sous leurs propriétaires ; dérivés réellement présents seulement. | Arrêter ressources, consommateurs, opérations et première unité. Aucune sélection implicite de provider ou exécutant ; aucune obligation applicable supprimée par la limitation d’une unité. |
| D2 — politiques | ORIENTATION ADOPTÉE : politiques explicites versionnées liées au propriétaire, à la ressource et à l’opération ; C04/C05/C06 réutilisés ; exception Super Admin canonique conservée. | Par ressource : droits des cinq demandes, rétention, holds, suppression, purge et preuves. Durées, permissions, références et conditions d’éligibilité non arrêtées restent ouvertes, sans défaut de fixture. À arrêter avant chaque réalisation dépendante. |
| D3 — effacements et restauration | ORIENTATION ADOPTÉE : source durable couvrant les effacements et restrictions postérieurs au snapshot ; C10 fournit les faits, C16 restaure et N05 coordonne la réadmission. | Propriétaire, stockage, accès, conservation, preuve de complétude et fraîcheur à arrêter. Journal externe : option non sélectionnée. Aucune garantie de non-résurrection ni réadmission déduite du seul snapshot. |

Q1.4-GOV-SOURCE et Q1.4-C10-PUBLISH restent ADOPTÉS DOCUMENTAIREMENT : catalogue TOML protégé indépendant de la base à ouvrir et publication distinctement autorisée. Configuration protégée, éditeur durable, journal pré-base et relais C05 restent à fournir et qualifier. Le journal pré-base de publication est distinct de la source d’effacements D3.

### Passage des tâches 1.1 et 1.2

La revue couvre les 19 exigences et 20 scénarios des trois canons référencés ; leurs empreintes sont inchangées. La couverture des propriétaires Agent compris et les refus sont explicités, sans qualifier les raccords.

Les tâches 1.1/1.2 restent ouvertes, sans coche. D1 doit fixer l’inventaire exact et la première unité ; D2/D3 doivent arrêter les paramètres et contrats requis avant chaque réalisation dépendante. Les paramètres d’une phase ultérieure restent explicitement ouverts et empêchent sa propre réalisation, sans devenir des choix implicites. Aucun delta normatif nouveau n’est établi ; un comportement nouveau nécessiterait son delta préalable approuvé. Les tâches 2.x/3.x restent futures.

## C10-CONCEPTION-R2 — inventaire D1 et unité users/PLATFORM

Validation explicite du développeur après présentation : inventaire D1, première unité users/PLATFORM et orientations D2 adoptés ; seules les quatre écritures documentaires C10 sont autorisées. Les paramètres ouverts et les dix cases de tâches sont conservés. Cette section actualise les points D1 et le choix de première unité laissés ouverts par R1 ; elle ne transforme pas les orientations D2/D3 en configuration opérationnelle.

### Inventaire exact des modèles présents

Analyse statique des sources Python de core, auth, backend, agent, pzt et dns, hors migrations et caches ; héritage des modèles suivi, classes abstraites exclues et réexports non doublés. Total : 68 modèles Django concrets, dont 13 Bulk. Ce relevé de sources ne prouve ni schéma déployé, ni données présentes, ni disponibilité runtime. Les modèles de backend ne transfèrent pas les responsabilités métier de leurs contrats propriétaires.

| Source | Modèles concrets |
|---|---|
| [src/pixs/agent/models.py](../../../src/pixs/agent/models.py) | `AgentHead`, `AgentOperation`, `AgentFact` |
| [src/pixs/auth/models.py](../../../src/pixs/auth/models.py) | `AuthAccountGate`, `AuthBinding`, `AuthPasswordCredential`, `AuthPolicyRow`, `AuthSession`, `AuthToken`, `AuthOperation`, `AuthAuditPending`, `AuthBootstrapAuthorization`, `AuthLocalTrustSelection`, `AuthIdentityAssurance` |
| [src/pixs/backend/bulk_admission_identity_record.py](../../../src/pixs/backend/bulk_admission_identity_record.py) | `BulkAdmissionIdentityRecord` |
| [src/pixs/backend/bulk_command_idempotency_record.py](../../../src/pixs/backend/bulk_command_idempotency_record.py) | `BulkCommandIdempotencyRecord` |
| [src/pixs/backend/bulk_event_envelope_record.py](../../../src/pixs/backend/bulk_event_envelope_record.py) | `BulkEventEnvelopeRecord` |
| [src/pixs/backend/bulk_export_manifest_record.py](../../../src/pixs/backend/bulk_export_manifest_record.py) | `BulkExportManifestRecord` |
| [src/pixs/backend/bulk_inbox_receipt_record.py](../../../src/pixs/backend/bulk_inbox_receipt_record.py) | `BulkInboxReceiptRecord` |
| [src/pixs/backend/bulk_operation_record.py](../../../src/pixs/backend/bulk_operation_record.py) | `BulkOperationRecord` |
| [src/pixs/backend/bulk_outbox_publication_record.py](../../../src/pixs/backend/bulk_outbox_publication_record.py) | `BulkOutboxPublicationRecord`, `BulkOutboxScopeCounterRecord` |
| [src/pixs/backend/bulk_runtime_records.py](../../../src/pixs/backend/bulk_runtime_records.py) | `BulkOperationExecutionRecord`, `BulkCheckpointRecord`, `BulkJobBindingRecord`, `BulkJobScheduleRecord` |
| [src/pixs/backend/bulk_validation_report_record.py](../../../src/pixs/backend/bulk_validation_report_record.py) | `BulkValidationReportRecord` |
| [src/pixs/backend/c08_act_receipt_record.py](../../../src/pixs/backend/c08_act_receipt_record.py) | `C08ActReceiptRecord` |
| [src/pixs/backend/c08_installation_result_record.py](../../../src/pixs/backend/c08_installation_result_record.py) | `C08InstallationResultRecord` |
| [src/pixs/backend/c08_mode_operation_receipt_record.py](../../../src/pixs/backend/c08_mode_operation_receipt_record.py) | `C08ModeOperationReceiptRecord` |
| [src/pixs/backend/c08_mode_snapshot_record.py](../../../src/pixs/backend/c08_mode_snapshot_record.py) | `C08ModeSnapshotRecord` |
| [src/pixs/backend/c09_event_records.py](../../../src/pixs/backend/c09_event_records.py) | `C09SchedulerLeaseRecord`, `C09ScheduleRecord`, `C09OrderCursorRecord`, `C09EventEnvelopeRecord`, `C09OutboxStageRecord`, `C09OutboxPublicationRecord`, `C09DeliveryRecord`, `C09InboxReceiptRecord`, `C09OwnerUnitProofRecord`, `C09RuntimeInstanceRecord` |
| [src/pixs/backend/c09_job_records.py](../../../src/pixs/backend/c09_job_records.py) | `C09JobExtensionRecord` |
| [src/pixs/backend/c10_receipt_record.py](../../../src/pixs/backend/c10_receipt_record.py) | `C10ReceiptRecord` |
| [src/pixs/backend/models.py](../../../src/pixs/backend/models.py) | `FeatureFlagSourceSnapshotRecord`, `JobRecord` |
| [src/pixs/core/api_core_idempotency_record.py](../../../src/pixs/core/api_core_idempotency_record.py) | `CoreApiIdempotencyRecord` |
| [src/pixs/core/persistence/models_audit.py](../../../src/pixs/core/persistence/models_audit.py) | `CoreAuditEvent` |
| [src/pixs/core/persistence/models_authz.py](../../../src/pixs/core/persistence/models_authz.py) | `CorePermission`, `CoreRole`, `CoreRolePermission`, `CoreRoleAssignment`, `CorePolicy`, `CoreTombstoneRef` |
| [src/pixs/core/persistence/models_group.py](../../../src/pixs/core/persistence/models_group.py) | `CoreGroup`, `CoreUserGroupMembership`, `CoreIdentityTenantMembership` |
| [src/pixs/core/persistence/models_identity.py](../../../src/pixs/core/persistence/models_identity.py) | `CoreUser`, `CoreIdentity`, `CoreIdentityLink`, `CoreSuperAdminBinding`, `CoreSuperAdminTenantGrant` |
| [src/pixs/core/persistence/models_scope.py](../../../src/pixs/core/persistence/models_scope.py) | `CoreTenant`, `CoreScope` |
| [src/pixs/dns/models.py](../../../src/pixs/dns/models.py) | `DesiredDnsRecord`, `DnsNameRecord`, `DnsIdempotenceRecord` |
| [src/pixs/pzt/models.py](../../../src/pixs/pzt/models.py) | `DesiredPztRecord`, `PztIdempotenceRecord` |

### Ressources durables hors SQL identifiées

Les fichiers d’instance sensibles ne sont pas lus. Les chemins configurés, versions publiées et autorisations effectives restent non vérifiés. Les gardes de stockage restent des mécanismes techniques, pas des consommateurs ni des sources d’autorité implicites.

| Ressource | Interface et source |
|---|---|
| Catalogue TOML et profils de gouvernance | C10Catalog et baux : [c10_catalog.py](../../../src/pixs/backend/c10_catalog.py). |
| Plan d’installation | read_plan/publish_plan : [storage.py](../../../src/pixs/backend/installation/storage.py). |
| Checkpoint d’installation | read_checkpoint/publish_checkpoint : [checkpoint.py](../../../src/pixs/backend/installation/checkpoint.py). |
| Marqueur d’installation | read_installation_marker/publish_installation_marker : [marker.py](../../../src/pixs/backend/installation/marker.py). |
| Bundle de planification | read_bundle/publish_bundle : [planning_bundle_store.py](../../../src/pixs/backend/installation/planning_bundle_store.py). |
| Preuves et politique de confiance d’amorçage | FileProofSource.resolve/FileTrustSource.resolve : [bootstrap_file_sources.py](../../../src/pixs/auth/bootstrap_file_sources.py) ; publication d’autorisation : [bootstrap_publication.py](../../../src/pixs/auth/bootstrap_publication.py). |

### Consommateurs et opérations D1

Les chemins suivants sont observés dans le code ; ils ne sont pas des permissions de consommation. Les références exactes authorized_consumers, processeurs, garanties de transfert et identités de déploiement restent à arrêter dans D2. Aucun import ni nom de classe ne les remplace.

| Ressources | Consommateurs observés | Opérations à couvrir | Sources |
|---|---|---|---|
| Identité, groupes, périmètres et autorisation Core | Services Core, filtrage C04, façade HTTP ; CoreFactSource interne à la composition. | Création, liaison/déliaison, états, appartenances, rôles/politiques et lectures filtrées par domaine. | [services_queries.py](../../../src/pixs/core/services_queries.py), [query_source.py](../../../src/pixs/core/query_source.py), [catalogue HTTP](../../../src/pixs/backend/api_core_catalog.py). |
| Audit et idempotence Core | Services propriétaires et participants transactionnels C05/C06. | Stage/vérification, résultat conservé, restitution, conflit, réconciliation, lecture et maintenance audit. | [ports.py](../../../src/pixs/core/ports.py), [audit_access.py](../../../src/pixs/core/audit_access.py). |
| Auth | Service Auth, sources de requêtes API, lecteurs de métadonnées et ponts C08. | Authentification, renouvellement, révocation, changement/récupération, activité, réservation/création initiale. | [services.py](../../../src/pixs/auth/services.py), [api_request_source.py](../../../src/pixs/auth/api_request_source.py), [bootstrap_session.py](../../../src/pixs/auth/bootstrap_session.py). |
| C08 et C10 | Installateur, services de modes, lecteurs de résultats ; services Core via GovernanceProvider. | Inspection, publication plans/checkpoints/marqueurs, modes, reçus ; attest/stage_read/verify_staged. | [mode_service.py](../../../src/pixs/backend/installation/mode_service.py), [result_reader.py](../../../src/pixs/backend/installation/result_reader.py), [adaptateur C10](../../../src/pixs/backend/c10_governance_adapter.py). |
| Jobs/outbox/inbox | Repositories, scheduler, worker, dispatch et participants propriétaires. | Admission, baux, exécution, transition, publication, acquittement, consommation et réconciliation. | [jobs](../../../src/pixs/backend/c09_job_repository.py), [outbox](../../../src/pixs/backend/c09_outbox_repository.py), [inbox](../../../src/pixs/backend/c09_inbox_repository.py). |
| Fanions | Source PostgreSQL de snapshots. | Lecture versionnée ; administration dans son change propriétaire. | [feature_flag_postgres_source.py](../../../src/pixs/backend/feature_flag_postgres_source.py). |
| Agent | Service et repository Agent. | persist_desired, append_observation, confirm_observation, query_state, dispatch. | [service.py](../../../src/pixs/agent/service.py), [repository.py](../../../src/pixs/agent/repository.py). |
| PZT | PostgresPztService. | Déclaration/retrait souhaité et lectures propriétaires. | [services.py](../../../src/pixs/pzt/services.py). |
| DNS | PostgresDnsService. | declare_desired, retire_desired, declare_name, retire_name, get_desired, get_applied, resolve_view_policy. | [services.py](../../../src/pixs/dns/services.py). |
| Bulk | Repositories et orchestration Bulk, hors première unité. | Admission/validation/staging/checkpoints/baux/annulation/idempotence et échanges. | [bulk_runtime_repository.py](../../../src/pixs/backend/bulk_runtime_repository.py), [bulk_import_validate.py](../../../src/pixs/backend/bulk_import_validate.py). |

Les cinq demandes canoniques ACCESS, EXPORT, RECTIFY, ERASE et RESTRICT restent à couvrir selon applicabilité. Les opérations présentes ne prouvent pas leur implémentation complète. La présence des 13 modèles Bulk ne sélectionne ni n’active Bulk.

### Première unité retenue : users/PLATFORM

| Élément | Périmètre adopté |
|---|---|
| Ressource métier | CoreUser ; projection USER existante restituant user_id. |
| Entrée et action | users, contexte PLATFORM, action pixs.core.identity.read, selon le [catalogue existant](../../../src/pixs/backend/api_core_catalog.py). |
| Références | Collection calculée par collection_ref et références pixs.core.user:<UUID> selon [query_source.py](../../../src/pixs/core/query_source.py). Couverture individuelle explicite par le profil ; aucun joker implicite. |
| Consommation | Service serveur propriétaire de lecture Core ; façade HTTP Core après autorisation courante. Références réelles des consommateurs à arrêter. |
| Raccord à réaliser ultérieurement | Fournisseur de gouvernance ordinaire pour ce seul chemin ; réutiliser [query_core](../../../src/pixs/core/services_queries.py), filtrage source, attestation, stage_read et revalidation avant restitution. Le fournisseur initial reste limité à l’amorçage. |
| Effets | Lecture métier ; écritures techniques possibles d’audit et reçus transactionnels. Aucune création/rectification/restriction/suppression/purge métier ; aucune demande ACCESS complète ni export. |
| Preuves futures dans l’unité | Nominal, profil absent/révoqué/divergent, ressource non couverte, classification divergente, refus d’autorisation, rollback et perte de validité avant restitution ; intégration PostgreSQL réelle. |

### Orientations D2 adoptées pour users/PLATFORM

1. Classification CONFIDENTIAL / PERSONAL pour les identifiants utilisateurs de cette unité ; aucune généralisation automatique aux 67 autres modèles.
2. Consommation limitée au chemin serveur Core autorisé ; aucun consommateur externe, analytics, synchronisation ou export implicitement admis.
3. Profil publié versionné explicitement lié aux ressources couvertes, sans joker ni couverture déduite du préfixe.
4. Réutiliser C04/C05 et la transaction propriétaire ; conserver l’exception Super Admin dans son périmètre canonique.

Paramètres OUVERTS avant réalisation dépendante : références réelles du profil et des consommateurs, finalité, politiques référencées de rétention/suppression/export, résidence, processeurs éventuels et configuration protégée. Une lecture ne dispense pas de publier un profil complet. Aucun identifiant ou valeur de fixture ne vaut paramètre approuvé. Q1.4-GOV-SOURCE et Q1.4-C10-PUBLISH restent acquis ; publication autorisée et configuration effective restent à fournir et qualifier.

### Portée D3 et maintien des barrières

Aucune nouvelle source d’effacement à réaliser pour ce seul raccord de lecture. Aucune garantie de réadmission après restauration n’en découle. Propriétaire, stockage et preuves de complétude/fraîcheur de la source post-snapshot restent OUVERTS pour purge, restauration et réadmission avec C16/N05. Le journal de publication du catalogue ne remplace pas cette source. Les rétentions de l’audit et des reçus restent des paramètres D2 ; leur présence n’autorise aucune purge.

Inventaire D1 et première unité sont désormais consignés ; les mentions ouvertes de R1 décrivent l’état antérieur. Les consommateurs autorisés et paramètres D2/D3 non arrêtés restent ouverts dans leurs phases respectives. Les tâches 1.1/1.2 ne sont ni clôturées ni cochées, et les tâches 2.x/3.x restent futures. Cette édition documentaire ne lance aucune réalisation. Aucun delta normatif nouveau établi ; toute évolution normative démontrée nécessite un delta présenté et approuvé.

## D2-USERS-R1 — profil, consommateurs et politiques

Décision validée explicitement par le développeur le 28 octobre 2026 après présentation. Consignation limitée aux quatre documents C10 ; aucune publication, configuration effective, implémentation ou coche. Les noms et contenus ci-dessous sont adoptés documentairement pour users/PLATFORM seulement. Ils actualisent les mentions « références/finalité/politiques à arrêter » de R1/R2 ; leurs paramètres opérationnels restent ouverts comme indiqué ci-dessous.

### Références du profil et finalité

| Paramètre | Valeur adoptée documentairement | Sens et limite |
|---|---|---|
| profile_ref | pixs.core.governance.users.platform.read.v1 | Profil du seul raccord de lecture retenu. |
| profile_version | 1.0.0 | Version initiale, distincte de la version du catalogue. |
| data_asset_id | pixs.core.data.users | Ensemble logique des données utilisateurs Core ; compatibilité avec les lignes existantes à établir. |
| owner_component | pixs.core | Propriétaire existant, sans transfert de propriété au backend HTTP. |
| source_of_truth | pixs.core.source.postgresql.users.v1 | Source propriétaire CoreUser ; aucun droit d’accès SQL libre. |
| data_classes | Ensemble contenant user_reference | Identifiant utilisateur de la projection USER retenue. |
| confidentiality | CONFIDENTIAL | Choix déjà validé, limité à cette unité. |
| personal_data | PERSONAL | Choix déjà validé, limité à cette unité. |
| purpose_refs | Ensemble contenant pixs.core.purpose.users.administration.v1 | Consultation administrative des références utilisateurs sous autorisation courante. |
| lineage | pixs.core.lineage.users.platform.read.v1 | CoreUser → projection propriétaire USER → page Core autorisée. |

La finalité exclut de cette unité le profilage, les statistiques d’usage, l’enrichissement et la réutilisation des identifiants. Ces noms sont des références opaques : selon [ProfileBinding et le lecteur de catalogue](../../../src/pixs/backend/c10_catalog.py), leur structure ne prouve ni autorité, ni existence d’une politique, ni publication. Aucune nouvelle grammaire de référence ni variable de configuration n’est introduite par ces noms documentaires.

Le [lecteur Core](../../../src/pixs/core/services_queries.py) compare le data_asset_id du profil avec le governance_ref des lignes restituées. Avant consommation de ce profil, vérifier la compatibilité avec les classifications persistées. Une divergence nécessite une décision propriétaire explicite ; aucun reclassement, remplacement de référence ou traitement massif implicite.

### Consommateurs serveur

| Référence adoptée | Rôle et opération | Limite |
|---|---|---|
| pixs.core.consumer.query.users.platform.v1 | Service serveur Core exécutant la lecture propriétaire ; action pixs.core.identity.read et contexte PLATFORM. | Filtrage et revalidation existants ; aucune permission déduite du seul nom. |
| pixs.backend.consumer.http.core.users.v1 | Façade HTTP Core restituant la page après autorisation courante. | Aucun accès direct aux tables, réemploi analytique, synchronisation ou export supplémentaire. |

authorized_consumers contient ces deux références. Leur liaison aux composants et versions réellement composés reste à documenter et vérifier avant consommation effective. Elles ne constituent pas les identités des appelants finaux.

Le destinataire HTTP final reste OUVERT : une façade déclarée n’autorise pas n’importe quel navigateur, client ou destination. Déclarer et vérifier cette liaison avant qualification de restitution HTTP de bout en bout ; ne pas fabriquer de référence de destinataire à partir d’une fixture ou d’une simple connexion.

### Politiques adoptées et paramètres ouverts

| Champ | Référence adoptée | Contenu adopté et paramètres restant ouverts |
|---|---|---|
| retention_policy | pixs.core.retention.users.v1 | La lecture conserve la politique propriétaire, ne prolonge aucune durée et ne déclenche aucune purge. Durées, événements de départ et conditions de conservation OUVERTS. |
| deletion_policy | pixs.core.deletion.users.v1 | Aucune suppression dans cette unité ; opérations futures chez leurs propriétaires, suppression logique par défaut et purge explicitement autorisée selon le canon. Le raccord de lecture ne réalise aucune de ces opérations futures. |
| export_policy | pixs.core.export.users.v1 | Seule la restitution de lecture retenue entre dans l’unité ; aucun export dédié, Bulk ou consommateur supplémentaire sélectionné. Exception Super Admin canonique préservée. |
| residency_constraints | Ensemble contenant pixs.core.residency.users.platform.v1 | Persistance et traitements aux emplacements explicitement approuvés du déploiement ; hôtes, régions et éventuelles réplications OUVERTS. PLATFORM ne définit aucune géographie. |
| processor_refs | Ensemble vide | Aucun processeur externe sélectionné pour cette unité ; confronter ce choix au déploiement effectif avant activation. Tout processeur supplémentaire exige sa déclaration. |

Collection calculée par collection_ref(USER, contexte PLATFORM) et références individuelles pixs.core.user:<UUID> explicitement admises, selon [query_source.py](../../../src/pixs/core/query_source.py). Aucun joker ni couverture déduite du préfixe. Aucune liste d’UUID d’instance n’est obtenue ou publiée par cette édition.

### Profils techniques distincts et passage à la réalisation

Audit et reçus conservent leurs propres profils et politiques de conservation. Le profil utilisateur ne les absorbe pas ; l’[adaptateur initial](../../../src/pixs/backend/c10_governance_adapter.py) distingue déjà profils métier et métadonnées. Leurs paramètres ne sont pas fabriqués à partir de la classification de CoreUser.

Restent OUVERTS avant la phase concernée : compatibilité des governance_ref existants ; durées et critères de rétention des utilisateurs, audits et reçus ; emplacements approuvés et destinataire HTTP final ; liaisons réelles des deux consommateurs ; versions et empreintes de publication, autorités, bornes de fraîcheur et configuration protégée. Les choix Q1.4-GOV-SOURCE et Q1.4-C10-PUBLISH restent acquis ; aucun ancrage, chemin, UID/GID, délai ou secret fourni implicitement par les références adoptées.

D3 reste OUVERT pour restauration et réadmission : cette décision ne définit ni source durable post-snapshot ni garantie de non-résurrection. Les tâches 1.1/1.2 restent ouvertes, les dix cases inchangées et les tâches 2.x/3.x futures. Aucun comportement normatif nouveau établi par cette consignation ; toute évolution normative démontrée nécessite son delta présenté et approuvé avant réalisation.

## D2-USERS-COMPAT-R1 — compatibilité des classifications

C1–C5 sont validées explicitement par le développeur après présentation de la revue des sources. Cette décision complète D2-USERS-R1 sans modifier ses références. La consignation est limitée aux quatre documents C10 ; aucun code, accès aux données d’instance, reclassement, migration ou coche de tâche. L’inspection des données et le reclassement éventuel restent des points ouverts, sans autorisation d’exécution déduite de la validation des principes.

### Sources et portée des constats

| Source | Constat statique | Limite |
|---|---|---|
| [create_user](../../../src/pixs/core/services_identity.py) | La création enregistre governance_ref, confidentiality et personal depuis ctx.classification(). | Aucune valeur pixs.core.data.users imposée par ce chemin ; profil du producteur à vérifier. |
| [MutationContext.classification](../../../src/pixs/core/services_transaction_types.py) | Hors dérogation, governance_ref provient du data_asset_id du profil attesté ; sous dérogation établie, les trois valeurs sont None. | La dérogation ne constitue pas une preuve de compatibilité en lecture ordinaire. |
| [Amorçage Core](../../../src/pixs/core/services_bootstrap.py) | Les métadonnées créées reprennent également ctx.classification(). | Valeurs réellement créées non déduites de la seule source. |
| [CoreBase](../../../src/pixs/core/persistence/base.py) | Les champs de gouvernance acceptent NULL ; référence non vide lorsqu’elle est fournie. | NULL n’est pas une corruption par défaut ni une classification utilisable pour la lecture ordinaire cible. |
| [query_core](../../../src/pixs/core/services_queries.py) | Hors dérogation, comparaison exacte de chaque triplet restitué au profil attesté ; écart refusé par GOUVERNANCE_DIVERGENTE. | Une réussite sous dérogation ou une collection vide ne prouve pas la compatibilité des lignes ordinaires ou futures. |

Les fixtures examinées, notamment [test_core_postgres_queries.py](../../../tests/integration/test_core_postgres_queries.py), comportent des références synthetic:* ; ce sont des données de recette, pas des valeurs d’exploitation constatées. Aucune conversion nommant pixs.core.data.users n’a été trouvée dans les opérations de migration Core/backend examinées. Ce constat ciblé n’exclut pas d’autres écritures ou opérations historiques ; aucune base ni configuration privée consultée pour la revue.

### Décisions C1–C5 adoptées

| Décision | Règle adoptée documentairement | Conditions et portée |
|---|---|---|
| C1 — critère | Lecture ordinaire : égalité exacte de governance_ref avec pixs.core.data.users, confidentiality avec CONFIDENTIAL, personal avec PERSONAL. | Aucun alias, normalisation ou remplacement à la volée. Conserver l’exception Super Admin canonique ; ne pas l’utiliser comme preuve de compatibilité ordinaire. |
| C2 — lignes compatibles | Réutiliser sans modification les lignes correspondant au triplet cible. | Profil publié couvrant les ressources, autorisation courante et autres contrôles restent nécessaires. Compatibilité effective encore à observer. |
| C3 — écart ou absence | Conserver les données avec référence différente, classification différente ou NULL et le refus ordinaire existant. | Aucun remplacement automatique par pixs.core.data.users ; NULL n’est pas déclaré corrompu par défaut. Aucune omission silencieuse d’un résultat divergent pour fabriquer une réussite. |
| C4 — producteurs futurs | Exiger une cohérence du profil consommé par le producteur des nouvelles lignes avec celui de lecture. | Un profil de lecture ne garantit pas la classification des futures créations ; examiner séparément toute adaptation du chemin de création, hors du périmètre users/PLATFORM actuellement documentaire. |
| C5 — reclassement éventuel | Préparer, si nécessaire, une opération propriétaire distincte avec autorisation explicite. | Arrêter périmètre, justification, concurrence, audit, références dérivées et reprise. Aucun SQL massif, migration ou reclassement implicite. Nécessité et réalisation restent OUVERTES. |

### Inspection propriétaire proposée, non exécutée

Sur une cible explicitement autorisée, inspection en lecture seule bornée produisant des agrégats : nombre de lignes avec triplet cible, référence différente, classification différente ou valeurs absentes ; ventilation par état de persistance ; périmètre et date. Les catégories doivent être définies sans double comptage, avec total de contrôle. Les états non restitués par une lecture donnée restent recensés pour anticiper réactivation/restauration.

Aucun UUID utilisateur, contenu métier ou ancienne référence personnalisée n’est nécessaire au premier diagnostic : catégories cible/autre/absent et comptes suffisent. Une méthode d’accès propriétaire autorisée reste à définir ; cette proposition n’autorise ni accès direct libre, ni lecture de secrets, ni exécution de l’inspection. Sans preuve de la cible, les valeurs réellement persistées et la compatibilité opérationnelle restent NON VÉRIFIÉES.

### Conséquence pour la première unité et points ouverts

Maintenir users/PLATFORM avec deux conditions distinctes : qualifier ultérieurement le raccord sur un jeu explicitement classifié pour le profil cible ; obtenir l’observation des données de la cible avant de revendiquer leur compatibilité. Des fixtures compatibles ne remplacent pas cette observation ; celle-ci ne qualifie pas à elle seule le raccord.

Points OUVERTS : cible, méthode et périmètre autorisés d’inspection ; répartition réelle des classifications ; nécessité d’un reclassement ; plan et autorisation propres de ce reclassement ; cohérence des producteurs futurs. Les références du profil D2-USERS-R1 restent acquises, sans garantir les valeurs existantes. Les durées/politiques opérationnelles, liaisons consommateurs, destinataire HTTP final, résidence, publication/configuration protégée et D3 restent ouverts selon leurs décisions respectives. Les dix cases restent ouvertes, sans implémentation ni validation complète de 1.1/1.2. Aucun delta normatif nouveau établi par cette consignation ; toute évolution normative démontrée nécessiterait un delta présenté et approuvé.

## C10-INSPECTION-R1 — plan d’inspection agrégée

Plan et bornes validés explicitement par le développeur ; consignation autorisée dans les seuls quatre documents C10. Aucun accès à la base, implémentation ou coche. La méthode et ses bornes sont désormais adoptées documentairement ; elles actualisent les mentions de méthode à définir des sections précédentes. Cible, accès et preuve de visibilité restent OUVERTS ; l’exécution de l’inspection n’est pas engagée.

### Cible candidate et préconditions ouvertes

| Élément | Candidat ou périmètre proposé | État |
|---|---|---|
| Serveur | PostgreSQL déclaré à 127.0.0.1:5432 dans [DEVOPS.md](../../../DEVOPS.md). | Déclaration documentaire seulement ; aucune connexion vérifiée. |
| Base / environnement | Base applicative Pixs contenant les données à qualifier. | Nom et environnement OUVERTS ; base de tests distincte d’une preuve sur la cible applicative. |
| Schéma | Schéma propriétaire effectif de Core. | OUVERT ; ne pas supposer public. |
| Relation | pixs_core_user, déclarée par [CoreUser](../../../src/pixs/core/persistence/models_identity.py). | Nom vérifié dans les sources, présence sur la cible non vérifiée. |
| Périmètre | Toutes les lignes visibles de cette relation, tous états de persistance. | Visibilité complète à établir avant tout verdict global. |
| Accès | Rôle existant approuvé pour cette inspection. | Référence, droits et mécanisme local d’accès OUVERTS ; aucune création de rôle. |

Une base de tests pourra qualifier la méthode, sans prouver les classifications de la cible applicative. Aucun rattachement à un déploiement ou à des données réelles n’est déduit du seul endpoint. Ni project.env ni configuration privée ne sont lus par cette consignation ; aucune autorisation générale de lecture de ces fichiers n’est impliquée par le plan.

### Méthode adoptée, non exécutée

Client PostgreSQL existant, session dédiée sans chargement de configuration personnelle et arrêt sur toute erreur. Transaction READ ONLY avec isolation REPEATABLE READ ; relation qualifiée par son schéma, sans dépendance au search_path ; paramètres liés pour le triplet cible. Aucune migration, initialisation Django, table temporaire, fonction applicative ou maintenance. Fermer transaction et connexion après restitution ou échec.

Les accès nécessitent un mécanisme local approuvé, sans secret dans les arguments, sorties ou conversation. Le rôle et les politiques de visibilité sont contrôlés, sans élévation ni contournement automatique de RLS. La transaction en lecture seule interdit les écritures applicatives ; le plan ne prétend pas supprimer les effets internes normaux du serveur PostgreSQL.

### Agrégats et minimisation

| Champ | CIBLE | ABSENT | AUTRE |
|---|---|---|---|
| governance_ref | pixs.core.data.users | NULL | Toute autre valeur. |
| confidentiality | CONFIDENTIAL | NULL | Toute autre valeur. |
| personal | PERSONAL | NULL | Toute autre valeur. |

Chaque ligne appartient à une seule combinaison des trois catégories, sans normalisation ni alias. Compter les combinaisons par état de persistance ; les états hors vocabulaire sont regroupés dans une catégorie dédiée sans reproduire leur valeur. Les catégories de classification restent disjointes même si plusieurs champs divergent. Aucun état non restitué par la lecture métier n’est omis de l’inspection.

Restitution prévue : total des lignes inspectées ; total CIBLE/CIBLE/CIBLE ; total incompatible ou incomplet ; ventilation par état de persistance ; date, cible approuvée et portée de visibilité. Les sommes de toutes les combinaisons et la somme compatibles/autres correspondent au total du même snapshot. Aucun LIMIT sur les lignes sources ni échantillonnage présenté comme exhaustif. Aucun UUID, contenu utilisateur ou ancienne référence personnalisée sélectionné pour restitution ; catégories et comptes seulement.

### Contrôles prévus

| Contrôle | Critère |
|---|---|
| Identité de cible | Base, schéma et relation conformes au périmètre approuvé avant inspection. |
| Visibilité | Droits et éventuelles politiques RLS ne masquent pas silencieusement des lignes ; preuve de visibilité complète à définir. |
| Structure | Colonnes et types attendus présents ; arrêt sur écart, sans correction automatique. |
| Lecture seule | Transaction effectivement en lecture seule ; aucune élévation de privilèges. |
| Cohérence | Somme des catégories = total ; compatibles + autres = total, dans le même snapshot. |
| Exhaustivité | Aucune limitation ni échantillonnage silencieux des lignes sources. |
| Confidentialité | Catégories/comptes seulement ; erreur restituée sans données de connexion ni valeurs utilisateur. |
| Interprétation | Table vide, visibilité partielle ou interruption ne constituent pas une compatibilité globale démontrée. |

### Bornes adoptées

| Borne de cette inspection | Valeur validée |
|---|---|
| Attente de verrou | 1 seconde. |
| Durée maximale d’une instruction | 5 secondes. |
| Abandon de l’opération complète | Après 15 secondes. |
| Réessai automatique | Aucun. |

Ces bornes concernent uniquement cette inspection, pas les budgets généraux du produit. Expiration ou interruption : résultat NON CONCLUANT, aucune augmentation automatique des bornes ni substitution d’un échantillon. Visibilité partielle : résultat PARTIEL avec limite explicite, aucun contournement RLS. L’implémentation future devra assurer l’abandon global et la fermeture des ressources ; aucun mécanisme d’annulation n’est réalisé ici.

### Points ouverts et conditions de reprise

Restent OUVERTS : base applicative et environnement, schéma Core, référence du rôle existant et mécanisme local d’accès, preuve attendue de visibilité complète, périmètre autorisé de restitution. Les bornes et la méthode sont adoptées mais non configurées ni exécutées. Reprendre l’examen de la cible et des accès avant tout accès à la base ; ne pas déduire une permission d’exécution du seul plan documentaire.

La répartition réelle des classifications, la nécessité d’un reclassement, son plan et son autorisation propre restent OUVERTS. L’inspection ne qualifierait ni le raccord users/PLATFORM ni les producteurs futurs. C1–C5 et D2-USERS-R1 sont conservés ; D3 et les autres paramètres opérationnels restent ouverts selon leur phase. Les dix tâches restent non cochées, aucune validation complète de 1.1/1.2 ni réalisation 2.x/3.x. Aucun delta normatif nouveau établi par cette consignation ; toute évolution normative démontrée nécessiterait un delta présenté et approuvé.

## C10-INSPECTION-CIBLE-R1 — cible et accès

Décision validée par le développeur pour consignation documentaire uniquement, dans les quatre documents C10. Aucun accès à la base, lecture de secrets, implémentation ni coche. Les principes de sélection de cible et d’accès sont adoptés ; leurs valeurs effectives non fournies restent OUVERTES.

### Éléments établis et informations manquantes

Les sources établissent un candidat PostgreSQL 127.0.0.1:5432 et le client /usr/bin/psql, selon [DEVOPS.md](../../../DEVOPS.md), et le nom de table pixs_core_user selon [CoreUser](../../../src/pixs/core/persistence/models_identity.py). Ces éléments ne constituent ni une cible exécutable ni une connexion vérifiée. Le renvoi de DEVOPS à project.env ne permet aucune lecture de ce fichier.

| Information non secrète manquante | Décision adoptée | Valeur effective |
|---|---|---|
| Environnement | Désigner développement, qualification, préproduction ou production dont les données sont à qualifier ; tests distincts des données applicatives. | OUVERTE. |
| Machine d’exécution | Identifier la machine depuis laquelle la connexion serait ouverte ; 127.0.0.1 désigne cette machine et ne prouve pas l’identité du serveur décrit par DEVOPS. | OUVERTE. |
| Base et schéma Core | Fournir leurs noms exacts ; relation attendue pixs_core_user, aucun schéma public supposé. | OUVERTS. |
| Identité du déploiement | Associer une référence non secrète d’installation/déploiement à la cible pour distinguer les bases semblables. | OUVERTE. |
| Référence d’accès approuvée | Désigner un accès existant par une référence non secrète ; aucun compte, rôle ou privilège nouveau pour cette inspection. | OUVERTE. |
| Mode de connexion | Désigner le profil approuvé et ses garanties de transport/authentification ; aucun réglage déduit du seul caractère local de l’adresse. | OUVERT. |
| Visibilité attendue | Autoriser explicitement les agrégats sur toute la relation, tous états compris ; désigner le responsable de l’attestation de portée. | Autorisation de périmètre et responsable OUVERTS. |
| Restitution | Confirmer si les agrégats peuvent être restitués dans la conversation, avec désignation non secrète de la cible. | OUVERTE. |

### Voie d’accès recommandée et alternative conditionnelle

Voie recommandée pour la première inspection : exécution par un opérateur autorisé utilisant son accès existant. Résultat attendu : rapport agrégé C10-INSPECTION-R1 accompagné des contrôles de cible et de visibilité. Ni opérateur effectif ni référence d’accès ne sont désignés par cette recommandation.

Une exécution future par l’agent reste envisageable seulement si un mécanisme de connexion existant maintient les secrets hors de ses lectures et sorties. Ce mécanisme n’est pas établi ; aucun raccord, développement ou accès n’est lancé ici. La validation du plan ne fournit pas les informations manquantes et ne vaut pas permission de connexion.

### Preuve de visibilité à établir

Avant un verdict global, établir la bonne base, le bon schéma et la bonne relation ; les droits nécessaires du rôle effectif ; l’application éventuelle de RLS et sa portée ; l’absence de filtre ou périmètre de connexion réduisant silencieusement les lignes visibles. Les modalités et preuves effectives restent OUVERTES.

Sans preuve de visibilité complète, le résultat reste PARTIEL même si toutes les lignes visibles correspondent au triplet cible. Aucun changement de rôle ou contournement automatique de RLS. L’inspection n’est pas une lecture métier ordinaire implicitement autorisée par users/PLATFORM.

### Descriptif non secret attendu et état de reprise

Le descriptif à compléter comprend : environnement et référence du déploiement ; machine d’exécution ; serveur/port approuvés ; nom de base ; schéma Core ; référence non secrète d’accès ; exécution par opérateur ou mécanisme existant ; responsable de preuve de visibilité ; autorisation ou refus de restitution dans la conversation. Aucun mot de passe, jeton, chaîne de connexion contenant un secret ou contenu de fichier d’accès n’est demandé.

Toutes ces informations restent à fournir ou confirmer. Les bornes 1 s / 5 s / 15 s, l’absence de réessai, la transaction en lecture seule et la méthode agrégée C10-INSPECTION-R1 restent acquises, sans exécution. Inspection réelle, compatibilité des données et besoin de reclassement restent ouverts ; aucune réalisation 2.x/3.x ni validation complète de 1.1/1.2. Les dix cases sont conservées. Aucun changement de canon ni delta normatif nouveau établi par cette consignation.

## C10-INSPECTION-VISIBILITE-R1 — preuve de visibilité

Validation explicite du développeur pour les quatre écritures documentaires C10. Ce protocole complète C10-INSPECTION-R1 et C10-INSPECTION-CIBLE-R1 ; il ne fournit ni cible, ni accès, ni constat de base. Aucune connexion, lecture de secrets, implémentation ou coche. Les points non établis restent OUVERTS et aucune preuve n’est présentée comme acquise.

La recherche ciblée dans les migrations et sources Core examinées n’avait trouvé aucune déclaration RLS pour CoreUser. Ce constat de sources ne prouve pas l’absence de RLS déployée : des opérations extérieures aux migrations peuvent modifier la configuration. La relation attendue reste celle de [CoreUser](../../../src/pixs/core/persistence/models_identity.py), pas un objet choisi par son seul nom non qualifié.

### Contrôles adoptés pour une inspection future

| Contrôle | Preuve attendue | Limite et point ouvert |
|---|---|---|
| Relation exacte | Résoudre schéma et pixs_core_user en une identité de relation précise ; vérifier la table attendue sans vue intermédiaire. | Cible effective et identité OUVERTES. Vue, partitionnement, héritage ou table étrangère inattendus imposent un réexamen du périmètre. |
| Identité de session | Comparer localement rôle de connexion, rôle effectif et accès approuvé ; rapporter la concordance sous la référence non secrète approuvée. | Aucune exposition des identifiants de connexion ; rôle et accès effectifs OUVERTS. |
| Droits effectifs | Vérifier connexion à la base, accès au schéma et droits de lecture nécessaires sur governance_ref, confidentiality, personal et persistence_state ; considérer les droits effectifs et non les seules attributions directes. | Droits réellement disponibles OUVERTS ; aucun droit ajouté par cette inspection. |
| Contexte d’exécution | Aucun changement de rôle pendant l’inspection ; aucune fonction applicative, vue ou fonction SECURITY DEFINER comme intermédiaire. | Mécanisme effectif à vérifier ; aucun contournement par un chemin indirect. |
| État RLS | Relever activation et forçage sur la relation, puis déterminer l’application effective de RLS au rôle courant. | Indicateurs, rôle et application réelle OUVERTS ; activation seule insuffisante. |
| Politiques applicables | Si RLS s’applique : examiner politiques SELECT/ALL, rôles, prédicats et combinaison permissive/restrictive. | Une politique permissive ne démontre pas la visibilité totale si une politique restrictive réduit la portée. Dépendances et contexte des prédicats à établir. |
| Stabilité | Associer contrôles et agrégats à la même session/transaction ; documenter la stabilité administrative attendue pendant l’opération. | Un changement de rôle, droits ou politiques rend la conclusion à réexaminer ; le snapshot ne remplace pas cette preuve. |

Références techniques de préparation PostgreSQL 16 : [fonctions d’information et d’examen des privilèges](https://www.postgresql.org/docs/16/functions-info.html), dont row_security_active ; [RLS](https://www.postgresql.org/docs/16/ddl-rowsecurity.html) ; [catalogue pg_policy](https://www.postgresql.org/docs/16/catalog-pg-policy.html). Ces références décrivent des contrôles possibles, non une interrogation exécutée.

### Propriétaire et rôles privilégiés

Identifier les exemptions RLS déjà effectives : superutilisateur, BYPASSRLS ou propriétaire selon les conditions applicables. PostgreSQL exempte superutilisateurs et rôles BYPASSRLS ; le propriétaire est normalement exempté sauf forçage RLS. Constater ces caractéristiques sans les modifier, puis vérifier leur concordance avec l’accès expressément approuvé. Une exemption technique n’est pas une autorisation d’inspection.

Aucune élévation ou changement de rôle pour obtenir une sortie complète ; aucune modification de politique ou contournement automatique de RLS. Le mécanisme existant et la preuve de concordance restent à fournir ; la validation documentaire ne les crée pas.

### Conclusions admises

| Situation constatée ultérieurement | Conclusion autorisée |
|---|---|
| Table attendue, droits suffisants, absence de filtrage RLS effectif et périmètre complet établi | Visibilité complète démontrée pour cette cible et ce constat seulement. |
| RLS effectivement active | Conclusion complète seulement après preuve que les politiques applicables couvrent toute la relation pour le rôle et le contexte observés. |
| Prédicats, dépendances ou portée des politiques non établis | Visibilité complète non démontrée ; agrégats au plus PARTIELS. |
| Mauvaise cible, droits insuffisants, erreur ou expiration | NON CONCLUANT ; arrêt sans réessai automatique. |

Deux comptes identiques sous le même filtrage ne prouvent pas l’exhaustivité. Un total nul ne prouve pas à lui seul que la table est vide. Une visibilité complète peut révéler des classifications incompatibles : ne pas confondre visibilité, compatibilité des données et qualification du raccord users/PLATFORM.

### Preuve minimale et points ouverts

Restitution prévue : référence approuvée de cible et d’accès, date, identité de relation, concordance du rôle, droits suffisants/insuffisants, application de RLS, éventuelle exemption, portée démontrée et limites. Les prédicats détaillés peuvent être examinés localement par l’opérateur responsable sans copie de contenu sensible dans la conversation ; son identité et cette preuve restent à arrêter. Aucune collecte de secrets ou de données utilisateur n’est demandée par ce protocole.

Restent OUVERTS : cible et schéma, accès approuvé et droits effectifs, opérateur/responsable de preuve, structure réelle de la relation, RLS et politiques déployées, conditions de stabilité et preuves de portée, autorisation effective de restitution. Les bornes 1 s / 5 s / 15 s et l’absence de réessai restent acquises ; aucun contrôle réel ni inspection exécuté. Besoin de reclassement, autres paramètres D2 et D3 restent ouverts selon leur phase. Les dix tâches demeurent non cochées ; aucune validation complète de 1.1/1.2 ni réalisation 2.x/3.x. Aucun delta normatif nouveau établi ; toute évolution normative démontrée nécessiterait son delta présenté et approuvé.

## C10-INSPECTION-RAPPORT-R1 — format du rapport

Format Markdown validé par le développeur pour consignation dans les seuls quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Aucun rapport de résultats ni fichier supplémentaire créé. Le format sépare exécution, visibilité, cohérence des comptes et compatibilité ; aucun résultat inventé. Il reprend les décisions d’inspection et leur minimisation sans modifier le canon.

### 1. Identification et portée

| Champ | Contenu attendu |
|---|---|
| Référence du rapport | Identifiant documentaire de l’inspection à renseigner. |
| Référentiel | Versions des décisions d’inspection appliquées. |
| Cible | Référence non secrète de déploiement, environnement, base et relation approuvés. |
| Accès | Référence non secrète de l’accès et de l’opérateur responsable. |
| Période | Début et fin UTC. |
| Périmètre | Relation exacte, tous états de persistance et éventuelles restrictions. |
| Bornes | Verrou 1 s, instruction 5 s, opération 15 s ; aucun réessai automatique. |
| Exécution | NON EXÉCUTÉE, ACHEVÉE, INTERROMPUE ou ÉCHOUÉE selon le constat. |

Désignation effective de cible et informations de connexion soumises aux règles de restitution adoptées. Les champs inconnus restent « À établir », jamais remplacés par des valeurs de test ou par une cible supposée.

### 2. Preuve de visibilité

| Contrôle | Résultat initial, sans inspection | Référence de preuve et limite attendues |
|---|---|---|
| Cible et identité exacte de relation | À établir. | À fournir. |
| Structure conforme au périmètre | À établir. | À fournir. |
| Concordance accès/rôle effectif | À établir. | Référence approuvée, sans identifiant de connexion exposé. |
| Droits effectifs suffisants | À établir. | Base, schéma et colonnes nécessaires. |
| Activation/forçage RLS | À établir. | À fournir. |
| RLS effectivement applicable au rôle | À établir. | À fournir. |
| Exemption éventuelle conforme à l’accès approuvé | À établir. | Aucune modification effectuée. |
| Portée des politiques applicables | À établir. | Conclusions minimales, sans prédicats sensibles copiés. |
| Stabilité du contexte pendant l’inspection | À établir. | À fournir. |
| Même session/transaction pour les constats requis | À établir. | À fournir. |

Résultats unitaires prévus : ÉTABLI, NON ÉTABLI, NON VÉRIFIÉ, NON APPLICABLE. Tout NON APPLICABLE nécessite justification ; il ne remplace pas une preuve manquante. « À établir » désigne l’absence actuelle de contrôle, pas son succès.

Verdict de visibilité : COMPLÈTE DÉMONTRÉE si tous les éléments nécessaires établissent la portée totale ; PARTIELLE si une restriction est identifiée ; NON DÉMONTRÉE si les éléments ne permettent pas de conclure. Les critères C10-INSPECTION-VISIBILITE-R1 restent applicables.

### 3. Agrégats

| État de persistance | governance_ref | confidentiality | personal | Nombre |
|---|---|---|---|---|
| État constaté ou catégorie AUTRE | CIBLE / ABSENT / AUTRE | CIBLE / ABSENT / AUTRE | CIBLE / ABSENT / AUTRE | À établir ; entier ≥ 0 si résultat disponible. |

États reconnus : ACTIVE, ARCHIVED, SOFT_DELETED, PURGE_PENDING. Toute valeur hors vocabulaire, absence éventuelle comprise, est regroupée dans AUTRE sans reproduire sa valeur. Cette catégorie d’état est distincte des catégories de classification de chaque champ. Le triplet cible est pixs.core.data.users / CONFIDENTIAL / PERSONAL, ABSENT signifie NULL et AUTRE toute autre valeur, sans normalisation ni alias.

| État de persistance | Total observé | Triplet cible | Autres triplets |
|---|---|---|---|
| Chaque catégorie observée | À établir. | À établir. | À établir. |
| Total | À établir. | À établir. | À établir. |

Le tableau détaillé ne contient que les combinaisons observées. Une combinaison omise équivaut à zéro uniquement si l’agrégation est achevée et cohérente dans son périmètre déclaré. Un résultat indisponible est N/A avec motif, jamais zéro. Sous visibilité restreinte, les comptes décrivent seulement les lignes visibles. Aucun pourcentage par défaut : les comptes suffisent au diagnostic. Aucun UUID, valeur brute de classification ou contenu utilisateur dans la restitution.

### 4. Contrôles de cohérence

| Contrôle | Critère |
|---|---|
| Dénombrement | Somme des combinaisons = total observé. |
| Ventilation | Somme des états = total observé. |
| Classification | Triplets cibles + autres triplets = total observé. |
| Unicité | Chaque ligne contribue à une seule combinaison. |
| Périmètre | Aucun échantillonnage, état omis ou limitation silencieuse. |
| Exécution | Aucun résultat incomplet présenté comme agrégation achevée. |
| Confidentialité | Sortie limitée aux métadonnées approuvées et agrégats. |

Verdict des agrégats : COHÉRENTS, INCOHÉRENTS ou NON VÉRIFIÉS. Les contrôles portent sur le même snapshot ; des comptes cohérents ne démontrent pas une visibilité complète.

### 5. Verdicts séparés et interprétation

| Dimension | Valeurs prévues |
|---|---|
| Visibilité | COMPLÈTE DÉMONTRÉE / PARTIELLE / NON DÉMONTRÉE. |
| Agrégats | COHÉRENTS / INCOHÉRENTS / NON VÉRIFIÉS. |
| Classification | TRIPLET CIBLE SUR TOUTES LES LIGNES OBSERVÉES / ÉCARTS OBSERVÉS / AUCUNE LIGNE OBSERVÉE / NON ÉVALUABLE. |
| Inspection globale | CONCLUANTE / PARTIELLE / NON CONCLUANTE / NON EXÉCUTÉE. |

- Écarts avec visibilité complète et comptes cohérents : inspection concluante révélant une incompatibilité ; aucun reclassement automatique.
- Triplet cible partout, visibilité complète et comptes cohérents : compatibilité constatée pour cette cible, ce périmètre et cet instant seulement.
- Visibilité partielle ou non démontrée : aucun verdict global de compatibilité ; inspection au plus PARTIELLE même si toutes les lignes observées correspondent au triplet.
- Zéro ligne : aucune classification évaluée ; table vide affirmable seulement avec visibilité complète démontrée. Une inspection complète peut conclure sur le dénombrement sans démontrer une compatibilité de classifications absentes.
- Erreur, expiration ou incohérence : inspection NON CONCLUANTE ; aucun résultat incomplet utilisé comme preuve globale. Une inspection non lancée reste NON EXÉCUTÉE.
- Aucun verdict ne qualifie le raccord users/PLATFORM, les producteurs futurs ou la réadmission après restauration.

### 6. Limites et suites

Terminer par les preuves manquantes, restrictions de portée, paramètres D2/D3 encore ouverts et décisions éventuellement nécessaires. Distinguer faits observés, interprétations justifiées et actions proposées ; une action proposée n’est pas déclarée autorisée. Nécessité et autorisation du reclassement restent séparées.

État actuel du futur rapport : NON EXÉCUTÉE ; aucune donnée ni preuve de visibilité disponible. Cible, accès, opérateur/responsable de preuve, autorisation de restitution et preuves effectives restent OUVERTS. Les bornes et méthodes adoptées ne valent pas autorisation de connexion. Les dix cases restent ouvertes ; aucune réalisation 2.x/3.x ni validation complète de 1.1/1.2. Aucun delta normatif nouveau établi par cette consignation.

## C10-INSPECTION-ACCEPTATION-R1 — critères du rapport

Décision explicitement validée par le développeur pour consignation dans les seuls quatre documents C10. Aucun accès à la base, lecture de secrets, implémentation ni coche. Les cas A01–A16 ci-dessous sont des critères de vérification future du format adopté, pas des observations ni de nouveaux scénarios normatifs canoniques.

### Recevabilité commune

Distinguer rapport recevable et inspection concluante. Un rapport d’échec ou de visibilité partielle peut être recevable si son contenu et ses conclusions respectent les limites des preuves. La recevabilité ne transforme pas ce résultat en réussite.

Le rapport comporte les six parties adoptées, cible/période/périmètre et références de preuve ; sépare exécution, visibilité, cohérence et classification ; justifie tout N/A sans le remplacer par zéro ; conserve limites, points ouverts et suites. Aucun secret, UUID utilisateur, ancienne référence personnalisée ou contenu métier dans la restitution. Une suite proposée n’est pas déclarée autorisée ou réalisée. Les informations manquantes restent identifiées comme telles, sans résultat inventé.

### Cas nominaux

| Cas | Situation future à vérifier | Résultat attendu |
|---|---|---|
| A01 — triplet cible partout | Exécution achevée, visibilité complète démontrée, total strictement positif, tous triplets cibles et comptes cohérents. | CONCLUANTE ; compatibilité constatée pour cette cible, ce périmètre et cet instant seulement. |
| A02 — écarts de classification | Même couverture, au moins un champ AUTRE ou ABSENT. | CONCLUANTE avec ÉCARTS OBSERVÉS ; catégories et comptes conservés, aucun reclassement automatique. |
| A03 — table vide démontrée | Visibilité complète, dénombrement achevé et cohérent à zéro. | Conclusion sur le dénombrement ; AUCUNE LIGNE OBSERVÉE, aucune compatibilité de classification affirmée. |
| A04 — plusieurs états | Lignes réparties entre plusieurs états de persistance. | Tous les états contribuent une fois aux sommes ; états hors vocabulaire regroupés sous AUTRE et signalés sans valeur brute ni omission. |

### Cas partiels

| Cas | Situation future à vérifier | Résultat attendu |
|---|---|---|
| A05 — filtrage identifié | Agrégation achevée/cohérente avec restriction RLS ou autre périmètre établi. | PARTIELLE ; comptes limités aux lignes visibles, sans compatibilité globale. |
| A06 — visibilité non démontrée | Comptes disponibles, preuve insuffisante de politiques, droits ou portée. | Au plus PARTIELLE, visibilité NON DÉMONTRÉE ; nommer les preuves manquantes. |
| A07 — zéro sous restriction | Aucune ligne visible sans preuve de portée totale. | Ne pas déclarer la table vide ; AUCUNE LIGNE OBSERVÉE dans le seul périmètre visible. |
| A08 — écarts dans un sous-ensemble | Divergences observées sous visibilité partielle. | Écarts établis pour les lignes observées seulement ; aucune extrapolation du nombre ou de la proportion au reste. |

### Cas non concluants

| Cas | Situation future à vérifier | Résultat attendu |
|---|---|---|
| A09 — cible/structure/accès incorrects | Contrôle tenté révélant mauvaise relation, structure inattendue ou droits insuffisants. | Arrêt, NON CONCLUANTE ; aucun changement de rôle ou correction automatique. |
| A10 — erreur/expiration | Erreur, interruption, dépassement de borne ou résultat incomplet. | NON CONCLUANTE ; résultat manquant N/A motivé, sans réessai ni augmentation automatique des bornes. |
| A11 — comptes incohérents | Sommes divergentes, doublons de combinaison, compte négatif ou non entier. | Agrégats INCOHÉRENTS ; NON CONCLUANTE sans correction silencieuse. |
| A12 — preuves non raccordables | Contrôles et agrégats de contextes différents ou changement administratif invalidant leur rapprochement. | NON CONCLUANTE tant que la cohérence de portée manque ; aucun assemblage présenté comme constat unique. |

### Contrôles du rapport lui-même

| Cas | Critère d’acceptation future |
|---|---|
| A13 — inspection non lancée | NON EXÉCUTÉE, aucun compte inventé, informations manquantes ouvertes. |
| A14 — combinaisons omises | Omission interprétable comme zéro uniquement après agrégation achevée et cohérente dans sa portée déclarée. |
| A15 — non-applicabilité | Chaque NON APPLICABLE justifié ; aucune preuve nécessaire manquante ainsi masquée. |
| A16 — confidentialité/extrapolation | Rapport non recevable s’il expose des éléments interdits ou affirme à partir des seuls agrégats une qualification du raccord, des producteurs futurs ou de la restauration. |

### Priorité des verdicts

1. Inspection non lancée : NON EXÉCUTÉE.
2. Erreur, incohérence ou preuve invalidée : NON CONCLUANTE, même si une partie des comptes est disponible.
3. Agrégation exploitable mais visibilité limitée ou non démontrée : PARTIELLE.
4. Exécution achevée, comptes cohérents et visibilité complète : CONCLUANTE, avec triplet cible, écarts ou absence de lignes explicitement distingués.

Ces règles s’appliquent à la portée réellement prouvée. La recevabilité documentaire d’un rapport n’efface pas son verdict défavorable ; un total nul ne prouve pas une classification compatible. Les contrôles C10-INSPECTION-RAPPORT-R1 et C10-INSPECTION-VISIBILITE-R1 restent applicables. Aucune preuve de disponibilité ou autorité déduite d’un agrégat.

### État actuel et points ouverts

Les seize cas sont NON EXÉCUTÉS ; aucune fixture, recette, connexion ni mesure réalisée par cette consignation. L’inspection actuelle reste NON EXÉCUTÉE. Cible, accès, opérateur, preuve de visibilité, autorisation de restitution, données réelles et paramètres D2/D3 non arrêtés restent OUVERTS. Nécessité et autorisation du reclassement restent distinctes et ouvertes. Bornes 1 s / 5 s / 15 s sans réessai conservées ; dix cases ouvertes et aucune réalisation 2.x/3.x ou validation complète de 1.1/1.2. Aucun delta normatif nouveau établi : ces critères documentaires ne modifient pas les exigences/scénarios du canon ; toute évolution normative démontrée nécessiterait un delta présenté et approuvé.

## C10-INSPECTION-SYNTHETIQUES-R1 — maquettes documentaires

Validation explicite du développeur pour consignation dans les seuls quatre documents C10. Toutes les données, cibles, accès et preuves supposées ci-dessous sont FICTIFS. Ce sont des maquettes documentaires, pas des rapports d’inspection réelle, des fixtures exécutables ou des tests exécutés. Exécution réelle des seize cas : NON EXÉCUTÉE. Aucun accès à la base, lecture de secrets, implémentation ni coche.

### Enveloppe commune aux seize maquettes

1. Identification : référence SYNTH-Axx, cible et accès fictifs, mention MAQUETTE — NON EXÉCUTÉE ; aucune identité de connexion ou cible réelle supposée.
2. Visibilité : preuves supposées pour le cas, marquées FICTIVES.
3. Agrégats : nombres synthétiques ou N/A avec motif.
4. Cohérence : sommes vérifiables ou anomalie volontaire identifiée.
5. Verdicts attendus : sous les hypothèses de la maquette, sans résultat observé.
6. Limites/suites : aucune conclusion sur les données Pixs réelles ni action autorisée.

Les états d’exécution employés dans les hypothèses décrivent uniquement l’exécution simulée par la maquette. Ils ne remplacent jamais l’état réel NON EXÉCUTÉE. Les références de preuve des six parties restent fictives et ne sont pas assimilées à une attestation disponible. Les tables suivantes condensent leur contenu et renvoient à cette enveloppe commune.

### A01–A04 — maquettes nominales

| Maquette | Agrégats fictifs | Visibilité supposée fictive | Verdict attendu sous ces hypothèses |
|---|---|---|---|
| SYNTH-A01 | Total 10 ; cible 10 ; autres 0. | Complète ; même cible/session/transaction, droits et portée établis. | COHÉRENTS ; TRIPLET CIBLE SUR TOUTES LES LIGNES OBSERVÉES ; CONCLUANTE. |
| SYNTH-A02 | Total 10 ; cible 7 ; autres 3. | Complète. | COHÉRENTS ; ÉCARTS OBSERVÉS ; CONCLUANTE révélant une incompatibilité. |
| SYNTH-A03 | Total 0 ; cible 0 ; autres 0. | Complète. | COHÉRENTS ; AUCUNE LIGNE OBSERVÉE ; concluante pour le dénombrement seulement, aucune classification compatible affirmée. |
| SYNTH-A04 | Total 12 ; cible 9 ; autres 3. | Complète. | COHÉRENTS ; ÉCARTS OBSERVÉS ; CONCLUANTE avec anomalie d’état signalée. |

Détail FICTIF de SYNTH-A02 :

| Persistance | Référence | Confidentialité | Données personnelles | Nombre fictif |
|---|---|---|---|---:|
| ACTIVE | CIBLE | CIBLE | CIBLE | 7 |
| ACTIVE | AUTRE | CIBLE | CIBLE | 2 |
| ACTIVE | ABSENT | ABSENT | ABSENT | 1 |

Détail FICTIF de SYNTH-A04 :

| Persistance | Référence | Confidentialité | Données personnelles | Nombre fictif |
|---|---|---|---|---:|
| ACTIVE | CIBLE | CIBLE | CIBLE | 5 |
| ARCHIVED | CIBLE | CIBLE | CIBLE | 2 |
| SOFT_DELETED | CIBLE | CIBLE | CIBLE | 1 |
| PURGE_PENDING | CIBLE | CIBLE | CIBLE | 1 |
| ARCHIVED | AUTRE | CIBLE | CIBLE | 1 |
| AUTRE | ABSENT | ABSENT | ABSENT | 2 |

L’état AUTRE est signalé sans valeur brute. La conclusion A04 porte sur les classifications et le dénombrement, pas sur la conformité du cycle de vie. La conclusion A01 reste bornée à la cible, au périmètre et à l’instant fictifs du cas.

### A05–A08 — maquettes partielles

| Maquette | Agrégats fictifs | Limite supposée | Verdict attendu sous ces hypothèses |
|---|---|---|---|
| SYNTH-A05 | Total visible 6 ; cible 6 ; autres 0. | Restriction RLS identifiée ; nombre masqué inconnu. | Visibilité PARTIELLE ; comptes COHÉRENTS sur les lignes visibles ; PARTIELLE, sans compatibilité globale. |
| SYNTH-A06 | Total observé 8 ; cible 8 ; autres 0. | Portée d’une politique non établie ; agrégation achevée, sommes cohérentes, sans erreur ni interruption. | Visibilité NON DÉMONTRÉE ; agrégats COHÉRENTS dans le périmètre observé ; PARTIELLE ; preuve manquante nommée. |
| SYNTH-A07 | Total visible 0 ; cible 0 ; autres 0. | Restriction de visibilité connue. | AUCUNE LIGNE OBSERVÉE ; PARTIELLE ; ne pas écrire table vide. |
| SYNTH-A08 | Total visible 6 ; cible 4 ; autres 2. | Visibilité partielle. | ÉCARTS OBSERVÉS sur deux lignes visibles ; PARTIELLE ; aucune extrapolation au reste. |

Formulation recevable pour A05, entièrement fictive : « Maquette : les six lignes visibles correspondent au triplet cible. La visibilité étant restreinte, la compatibilité de l’ensemble de la relation n’est pas démontrée. »

### A09–A12 — maquettes non concluantes

| Maquette | Contenu fictif | Verdict et restitution attendus |
|---|---|---|
| SYNTH-A09 | Contrôle de relation ne correspondant pas à la cible approuvée fictive ; agrégation non lancée. | Inspection tentée puis arrêtée : NON CONCLUANTE ; agrégats NON VÉRIFIÉS ; comptes N/A — cible incorrecte. |
| SYNTH-A10 | Agrégation interrompue par la borne de 5 secondes. | NON CONCLUANTE ; comptes N/A — expiration ; aucune tentative supplémentaire. |
| SYNTH-A11 | Total annoncé 10 ; cible 7 ; autres 4. | INCOHÉRENTS car 7 + 4 ≠ 10 ; classification NON ÉVALUABLE ; NON CONCLUANTE sans corriger les nombres. |
| SYNTH-A12 | Comptes 10/10/0 arithmétiquement cohérents ; preuves et agrégats de contextes différents. | Somme arithmétique correcte ; agrégats NON VÉRIFIÉS faute de rapprochement valide des contextes ; classification NON ÉVALUABLE ; NON CONCLUANTE. |

A10 : des fragments de sortie ne deviennent pas une agrégation partielle exploitable ; expiration prioritaire. A12 : l’égalité des comptes ne répare pas l’absence de preuve commune. Ces rapports peuvent être recevables en décrivant correctement leur résultat défavorable ; aucun verdict global compatible.

### A13–A16 — recevabilité des maquettes

| Maquette | Variante fictive | Résultat attendu |
|---|---|---|
| SYNTH-A13 | Cible et accès non renseignés ; aucun contrôle tenté. | Recevable : NON EXÉCUTÉE ; visibilité NON DÉMONTRÉE ; agrégats NON VÉRIFIÉS ; classification NON ÉVALUABLE ; comptes N/A — inspection non lancée. |
| SYNTH-A14 | A01 ne présente que sa combinaison observée, les autres omises. | Recevable si achèvement/cohérence/portée établis. Variante négative : sortie interrompue ne permettant pas d’assimiler les combinaisons absentes à zéro. |
| SYNTH-A15 | Examen détaillé de politiques NON APPLICABLE, avec preuve fictive que RLS n’est pas active pour la relation. | Recevable si les autres contrôles sont établis. Variante négative irrecevable : politiques non accessibles donc déclarées non applicables. |
| SYNTH-A16 | Description d’un rapport avec champ de donnée individuelle interdit, ou qualification du raccord déduite des seuls agrégats. | Rapport non recevable ; aucun verdict global accepté sur ce document tant qu’il n’est pas corrigé. |

Pour A16, aucune valeur interdite n’est reproduite : seule la violation est décrite. Affirmation volontairement erronée à rejeter, et non conclusion du présent document : « Tous les comptes correspondent au triplet ; le raccord users/PLATFORM est donc qualifié. »

### Vérification documentaire transversale et limites

Pour chaque maquette, distinguer recevabilité du rapport acceptée/rejetée avec motif, verdict d’inspection attendu selon la priorité adoptée, et limites sans extrapolation, qualification ou autorisation implicite. Les tableaux A01–A16 n’enregistrent que des attentes, aucun résultat de test. La validation de ces supports ne démontre ni leur exécution ni une inspection réelle.

L’inspection réelle reste NON EXÉCUTÉE ; cible, accès, opérateur, visibilité, restitution, données réelles et paramètres D2/D3 non arrêtés restent OUVERTS. Les besoins et autorisations de reclassement restent distincts. Les dix cases sont conservées ouvertes, bornes 1 s / 5 s / 15 s sans réessai inchangées ; aucune réalisation 2.x/3.x ou validation complète de 1.1/1.2. Aucun rapport de résultats ou fichier de tests produit créé. Aucun delta normatif nouveau établi ; la couverture canonique n’est pas modifiée par ces maquettes.

## C10-INSPECTION-SYNTHETIQUES-REVUE-R1 — maquettes complétées

Corrections validées par le développeur ; quatre documents C10 uniquement. Aucune inspection, lecture de secrets, implémentation ou coche. Tous les nombres, références, cibles, accès, rôles abstraits et fenêtres temporelles ci-dessous sont FICTIFS. Les six parties complétées explicitent les tableaux condensés antérieurs et font référence à leurs nombres conservés. A12 est corrigée directement dans la synthèse initiale.

### Convention commune et portée des preuves fictives

État réel de chaque maquette et variante : MAQUETTE — NON EXÉCUTÉE. Le champ « exécution simulée » ne remplace jamais cet état. Références documentaires inventées pour la maquette seulement, sans réservation de cible ou d’accès réel. Les instants UTC de l’année 2000 sont fictifs ; aucune chronologie d’exploitation n’est alléguée. Les preuves SYNTH-PREUVE-Axx décrivent les hypothèses ci-dessous, pas une attestation disponible.

Pour A01–A04, A14 positive et A15 positive : hypothèses fictives de cible/structure/accès conformes, droits suffisants, même session/transaction et stabilité établies, agrégation achevée sans erreur. Pour A05–A08 : mêmes hypothèses d’achèvement et cohérence des comptes dans le périmètre visible, mais preuve de visibilité limitée selon le cas. Ces hypothèses justifient les verdicts attendus, sans prouver le comportement produit.

Pour A15 positive, la preuve fictive porte sur la désactivation RLS pour la relation ; seul l’examen détaillé des politiques est NON APPLICABLE avec cette justification. Identité, rôle, droits, état RLS et autres contrôles restent établis dans l’hypothèse.

### Ventilations explicites complémentaires

Les trois colonnes de classification suivent CIBLE/ABSENT/AUTRE sans valeurs brutes. A02 et A04 conservent leurs détails précédents. A03 et A07 n’ont aucun groupe observé ; synthèse 0/0/0, avec visibilité complète pour A03 et partielle pour A07.

| Maquette | Persistance | Référence | Confidentialité | Données personnelles | Nombre fictif |
|---|---|---|---|---|---:|
| SYNTH-A01 | ACTIVE | CIBLE | CIBLE | CIBLE | 10 |
| SYNTH-A05 | ACTIVE | CIBLE | CIBLE | CIBLE | 6 |
| SYNTH-A06 | ACTIVE | CIBLE | CIBLE | CIBLE | 8 |
| SYNTH-A08 | ACTIVE | CIBLE | CIBLE | CIBLE | 4 |
| SYNTH-A08 | ACTIVE | AUTRE | CIBLE | CIBLE | 2 |

A06 : l’agrégation est supposée achevée et cohérente sans erreur ni interruption ; seul manque l’établissement de portée d’une politique. Sans ces hypothèses, PARTIELLE ne serait pas justifié. A04 : état AUTRE signalé sans valeur brute et sans conclusion de conformité du cycle de vie.

### Six parties complétées pour chaque maquette

#### SYNTH-A01 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A01, accès SYNTH-ACCES-A01, responsable SYNTH-OPERATEUR-A01, rôle abstrait SYNTH-ROLE-A01, relation SYNTH-RELATION-A01 : tous FICTIFS. Session SYNTH-SESSION-A01, transaction SYNTH-TX-A01 (hypothèses seulement). Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : ACHEVÉE.
2. Visibilité : COMPLÈTE DÉMONTRÉE (hypothèse fictive) Référence documentaire fictive SYNTH-PREUVE-A01, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. 10/10/0 ; ventilation ACTIVE détaillée ci-dessus.
4. Cohérence : verdict attendu COHÉRENTS. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification TRIPLET CIBLE SUR TOUTES LES LIGNES OBSERVÉES ; inspection CONCLUANTE ; recevabilité Recevable : six parties et preuves fictives cohérentes ; compatibilité bornée au constat fictif.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A02 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A02, accès SYNTH-ACCES-A02, responsable SYNTH-OPERATEUR-A02, rôle abstrait SYNTH-ROLE-A02, relation SYNTH-RELATION-A02 : tous FICTIFS. Session SYNTH-SESSION-A02, transaction SYNTH-TX-A02 (hypothèses seulement). Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : ACHEVÉE.
2. Visibilité : COMPLÈTE DÉMONTRÉE (hypothèse fictive) Référence documentaire fictive SYNTH-PREUVE-A02, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. 10/7/3 ; détail initial A02 conservé.
4. Cohérence : verdict attendu COHÉRENTS. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification ÉCARTS OBSERVÉS ; inspection CONCLUANTE ; recevabilité Recevable : incompatibilité correctement décrite, sans reclassement.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A03 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A03, accès SYNTH-ACCES-A03, responsable SYNTH-OPERATEUR-A03, rôle abstrait SYNTH-ROLE-A03, relation SYNTH-RELATION-A03 : tous FICTIFS. Session SYNTH-SESSION-A03, transaction SYNTH-TX-A03 (hypothèses seulement). Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : ACHEVÉE.
2. Visibilité : COMPLÈTE DÉMONTRÉE (hypothèse fictive) Référence documentaire fictive SYNTH-PREUVE-A03, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. 0/0/0 ; tableau détaillé vide, aucun groupe observé.
4. Cohérence : verdict attendu COHÉRENTS. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification AUCUNE LIGNE OBSERVÉE ; inspection CONCLUANTE pour le dénombrement ; recevabilité Recevable : aucune compatibilité de classifications absentes affirmée.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A04 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A04, accès SYNTH-ACCES-A04, responsable SYNTH-OPERATEUR-A04, rôle abstrait SYNTH-ROLE-A04, relation SYNTH-RELATION-A04 : tous FICTIFS. Session SYNTH-SESSION-A04, transaction SYNTH-TX-A04 (hypothèses seulement). Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : ACHEVÉE.
2. Visibilité : COMPLÈTE DÉMONTRÉE (hypothèse fictive) Référence documentaire fictive SYNTH-PREUVE-A04, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. 12/9/3 ; détail initial A04 conservé.
4. Cohérence : verdict attendu COHÉRENTS. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification ÉCARTS OBSERVÉS ; inspection CONCLUANTE ; recevabilité Recevable : anomalie d’état signalée, aucune conformité du cycle de vie déduite.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A05 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A05, accès SYNTH-ACCES-A05, responsable SYNTH-OPERATEUR-A05, rôle abstrait SYNTH-ROLE-A05, relation SYNTH-RELATION-A05 : tous FICTIFS. Session SYNTH-SESSION-A05, transaction SYNTH-TX-A05 (hypothèses seulement). Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : ACHEVÉE.
2. Visibilité : PARTIELLE ; restriction RLS identifiée, nombre masqué inconnu. Référence documentaire fictive SYNTH-PREUVE-A05, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. 6/6/0 visibles ; ACTIVE détaillé ci-dessus.
4. Cohérence : verdict attendu COHÉRENTS dans le périmètre visible. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification TRIPLET CIBLE SUR TOUTES LES LIGNES OBSERVÉES ; inspection PARTIELLE ; recevabilité Recevable : aucune compatibilité globale ; couverture des lignes masquées inconnue.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A06 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A06, accès SYNTH-ACCES-A06, responsable SYNTH-OPERATEUR-A06, rôle abstrait SYNTH-ROLE-A06, relation SYNTH-RELATION-A06 : tous FICTIFS. Session SYNTH-SESSION-A06, transaction SYNTH-TX-A06 (hypothèses seulement). Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : ACHEVÉE.
2. Visibilité : NON DÉMONTRÉE ; portée de la politique fictive non établie. Référence documentaire fictive SYNTH-PREUVE-A06, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. 8/8/0 observés ; ACTIVE détaillé ci-dessus.
4. Cohérence : verdict attendu COHÉRENTS dans le périmètre observé. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification TRIPLET CIBLE SUR TOUTES LES LIGNES OBSERVÉES ; inspection PARTIELLE ; recevabilité Recevable : preuve de portée manquante nommée ; aucune autre erreur simulée.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A07 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A07, accès SYNTH-ACCES-A07, responsable SYNTH-OPERATEUR-A07, rôle abstrait SYNTH-ROLE-A07, relation SYNTH-RELATION-A07 : tous FICTIFS. Session SYNTH-SESSION-A07, transaction SYNTH-TX-A07 (hypothèses seulement). Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : ACHEVÉE.
2. Visibilité : PARTIELLE ; restriction connue. Référence documentaire fictive SYNTH-PREUVE-A07, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. 0/0/0 visibles ; tableau détaillé vide.
4. Cohérence : verdict attendu COHÉRENTS dans le périmètre visible. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification AUCUNE LIGNE OBSERVÉE ; inspection PARTIELLE ; recevabilité Recevable : ne pas déclarer table vide.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A08 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A08, accès SYNTH-ACCES-A08, responsable SYNTH-OPERATEUR-A08, rôle abstrait SYNTH-ROLE-A08, relation SYNTH-RELATION-A08 : tous FICTIFS. Session SYNTH-SESSION-A08, transaction SYNTH-TX-A08 (hypothèses seulement). Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : ACHEVÉE.
2. Visibilité : PARTIELLE ; portée restreinte. Référence documentaire fictive SYNTH-PREUVE-A08, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. 6/4/2 visibles ; détail ci-dessus.
4. Cohérence : verdict attendu COHÉRENTS dans le périmètre visible. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification ÉCARTS OBSERVÉS ; inspection PARTIELLE ; recevabilité Recevable : deux écarts visibles, aucune extrapolation.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A09 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A09, accès SYNTH-ACCES-A09, responsable SYNTH-OPERATEUR-A09, rôle abstrait SYNTH-ROLE-A09, relation SYNTH-RELATION-A09 : tous FICTIFS. Session SYNTH-SESSION-A09, transaction SYNTH-TX-A09 (hypothèses seulement). Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : ÉCHOUÉE — contrôle tenté puis arrêt.
2. Visibilité : NON DÉMONTRÉE ; cible contrôlée incorrecte. Référence documentaire fictive SYNTH-PREUVE-A09, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. N/A — cible incorrecte ; agrégation non lancée.
4. Cohérence : verdict attendu NON VÉRIFIÉS. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification NON ÉVALUABLE ; inspection NON CONCLUANTE ; recevabilité Recevable : arrêt explicite et absence de nombres fabriqués ; variantes ci-dessous.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A10 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A10, accès SYNTH-ACCES-A10, responsable SYNTH-OPERATEUR-A10, rôle abstrait SYNTH-ROLE-A10, relation SYNTH-RELATION-A10 : tous FICTIFS. Session SYNTH-SESSION-A10, transaction SYNTH-TX-A10 (hypothèses seulement). Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:05Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : INTERROMPUE — expiration.
2. Visibilité : NON DÉMONTRÉE dans cette maquette. Référence documentaire fictive SYNTH-PREUVE-A10, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. N/A — expiration, aucune agrégation complète.
4. Cohérence : verdict attendu NON VÉRIFIÉS. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification NON ÉVALUABLE ; inspection NON CONCLUANTE ; recevabilité Recevable : pas de fragments exploités, réessai ou relèvement de borne.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A11 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A11, accès SYNTH-ACCES-A11, responsable SYNTH-OPERATEUR-A11, rôle abstrait SYNTH-ROLE-A11, relation SYNTH-RELATION-A11 : tous FICTIFS. Session SYNTH-SESSION-A11, transaction SYNTH-TX-A11 (hypothèses seulement). Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : ACHEVÉE — sortie de comptes reçue, validation documentaire négative.
2. Visibilité : COMPLÈTE DÉMONTRÉE supposée, sans réparer les comptes. Référence documentaire fictive SYNTH-PREUVE-A11, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. Total annoncé 10 ; cible 7 ; autres 4, valeurs volontairement contradictoires.
4. Cohérence : verdict attendu INCOHÉRENTS. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification NON ÉVALUABLE ; inspection NON CONCLUANTE ; recevabilité Recevable comme rapport de défaut : incohérence signalée sans corriger les nombres.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A12 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A12, accès SYNTH-ACCES-A12, responsable SYNTH-OPERATEUR-A12, rôle abstrait SYNTH-ROLE-A12, relation SYNTH-RELATION-A12 : tous FICTIFS. Session SYNTH-SESSION-A12, transaction SYNTH-TX-A12 (hypothèses seulement). Preuve fictive rattachée à SYNTH-SESSION-A12-X / SYNTH-TX-A12-X, distincts des agrégats ; aucun rapprochement valide. Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : ACHEVÉE — agrégation reçue, rapprochement de preuve invalide.
2. Visibilité : NON DÉMONTRÉE pour le contexte des agrégats. Référence documentaire fictive SYNTH-PREUVE-A12, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. 10/10/0 ; égalité arithmétique seule.
4. Cohérence : verdict attendu NON VÉRIFIÉS — contextes non raccordables. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification NON ÉVALUABLE ; inspection NON CONCLUANTE ; recevabilité Recevable : somme correcte distinguée du verdict de cohérence global ; preuve commune absente.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A13 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible/accès À établir dans le scénario ; aucun rôle/session/transaction ouvert. Période N/A — scénario sans exécution. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : NON EXÉCUTÉE.
2. Visibilité : NON DÉMONTRÉE ; aucun contrôle tenté. Référence documentaire fictive SYNTH-PREUVE-A13, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. N/A — inspection non lancée, pas zéro.
4. Cohérence : verdict attendu NON VÉRIFIÉS. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification NON ÉVALUABLE ; inspection NON EXÉCUTÉE ; recevabilité Recevable : cible et accès restent À établir même dans le scénario.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A14 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A14, accès SYNTH-ACCES-A14, responsable SYNTH-OPERATEUR-A14, rôle abstrait SYNTH-ROLE-A14, relation SYNTH-RELATION-A14 : tous FICTIFS. Session SYNTH-SESSION-A14, transaction SYNTH-TX-A14 (hypothèses seulement). Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : ACHEVÉE — variante positive.
2. Visibilité : COMPLÈTE DÉMONTRÉE (hypothèse fictive) Référence documentaire fictive SYNTH-PREUVE-A14, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. 10/10/0 ; reprendre la seule combinaison observée d’A01.
4. Cohérence : verdict attendu COHÉRENTS. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification TRIPLET CIBLE SUR TOUTES LES LIGNES OBSERVÉES ; inspection CONCLUANTE ; recevabilité Recevable positive : autres combinaisons omises valent zéro dans la portée démontrée ; variante négative distincte ci-dessous.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A15 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A15, accès SYNTH-ACCES-A15, responsable SYNTH-OPERATEUR-A15, rôle abstrait SYNTH-ROLE-A15, relation SYNTH-RELATION-A15 : tous FICTIFS. Session SYNTH-SESSION-A15, transaction SYNTH-TX-A15 (hypothèses seulement). Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : ACHEVÉE — variante positive.
2. Visibilité : COMPLÈTE DÉMONTRÉE (hypothèse fictive) ; RLS désactivée supposée pour la relation. Référence documentaire fictive SYNTH-PREUVE-A15, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. 10/10/0 ; reprendre les agrégats d’A01.
4. Cohérence : verdict attendu COHÉRENTS. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification TRIPLET CIBLE SUR TOUTES LES LIGNES OBSERVÉES ; inspection CONCLUANTE ; recevabilité Recevable positive : seul examen détaillé des politiques NON APPLICABLE avec justification ; autres contrôles nécessaires conservés.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

#### SYNTH-A16 — complément en six parties

1. Identification : MAQUETTE — NON EXÉCUTÉE réellement. Cible SYNTH-CIBLE-A16, accès SYNTH-ACCES-A16, responsable SYNTH-OPERATEUR-A16, rôle abstrait SYNTH-ROLE-A16, relation SYNTH-RELATION-A16 : tous FICTIFS. Session SYNTH-SESSION-A16, transaction SYNTH-TX-A16 (hypothèses seulement). Période 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z, FICTIF. Référentiel : décisions d’inspection R1 et présente revue. Exécution simulée : ACHEVÉE supposée dans le rapport candidat incorrect.
2. Visibilité : COMPLÈTE DÉMONTRÉE (hypothèse fictive) prétendue dans le candidat, aucun verdict accepté. Référence documentaire fictive SYNTH-PREUVE-A16, à interpréter selon les hypothèses de ce cas et les limites communes ; aucune attestation réelle.
3. Agrégats : ordre des synthèses total/cible/autres. Reprendre 10/10/0 d’A01 pour isoler le défaut de rapport.
4. Cohérence : verdict attendu Sommes arithmétiques correctes, sans valider la recevabilité. Les seules égalités arithmétiques ne suffisent pas à démontrer portée et unicité.
5. Verdicts attendus : classification Verdict candidat non accepté ; inspection Aucun verdict global accepté sur ce document incorrect ; recevabilité Non recevable : variantes confidentialité/extrapolation ci-dessous, sans valeur interdite reproduite.
6. Limites/suites : aucune donnée Pixs réelle, inspection ou test exécuté ; cible/accès/preuves réels et paramètres D2/D3 restent ouverts. Aucune qualification de raccord/producteur/restauration, aucun reclassement ni action autorisés.

### Variantes négatives et bornes explicites

Toutes ces variantes restent fictives et NON EXÉCUTÉES réellement ; elles héritent des six parties du cas parent, avec les substitutions ci-dessous. Leur verdict attendu ne constitue pas un résultat de test.

| Variante | Substitution dans la maquette parent | Verdict et recevabilité attendus |
|---|---|---|
| A09-a | Mauvaise relation, comme cas parent ; aucun agrégat. | NON CONCLUANTE ; agrégats NON VÉRIFIÉS, classification NON ÉVALUABLE, comptes N/A — cible incorrecte ; recevable si arrêt décrit. |
| A09-b | Cible correcte mais droits nécessaires insuffisants ; arrêt. | NON CONCLUANTE ; agrégats NON VÉRIFIÉS, classification NON ÉVALUABLE, N/A — droits insuffisants ; aucun rôle changé ; recevable. |
| A09-c | Structure inattendue détectée ; arrêt sans correction automatique. | NON CONCLUANTE ; agrégats NON VÉRIFIÉS, classification NON ÉVALUABLE, N/A — structure inattendue ; recevable. |
| A10-a | Attente de verrou atteint la borne 1 s ; arrêt. Fenêtre fictive 2000-01-01T00:00:00Z à 2000-01-01T00:00:01Z. | INTERROMPUE ; NON CONCLUANTE ; NON VÉRIFIÉS, NON ÉVALUABLE, comptes N/A — borne de verrou ; recevable sans réessai. |
| A10-b | Instruction atteint la borne 5 s ; arrêt, comme cas parent. | INTERROMPUE ; NON CONCLUANTE ; NON VÉRIFIÉS, NON ÉVALUABLE, N/A — borne d’instruction ; recevable sans réessai. |
| A10-c | Opération atteint la borne globale 15 s après plusieurs étapes individuellement sous leurs bornes ; abandon. Fenêtre fictive 2000-01-01T00:00:00Z à 2000-01-01T00:00:15Z. | INTERROMPUE ; NON CONCLUANTE ; NON VÉRIFIÉS, NON ÉVALUABLE, N/A — borne globale ; pas de fragments promus en résultat ni prolongation ; recevable. |
| A11-a | Total 10, cible 7, autres 4 ; somme 11, incohérence volontaire initiale. | INCOHÉRENTS ; NON ÉVALUABLE ; NON CONCLUANTE, recevable comme défaut signalé. |
| A11-b | Deux lignes identiques de combinaison ACTIVE/CIBLE/CIBLE/CIBLE, comptes 7 et 3 ; synthèse 10/10/0. | Somme correcte mais clé de groupe dupliquée : INCOHÉRENTS ; NON ÉVALUABLE ; NON CONCLUANTE, recevable comme défaut signalé. |
| A11-c | Total 10, cible 11, autres -1, volontairement invalide. | Somme correcte mais compte négatif : INCOHÉRENTS ; NON ÉVALUABLE ; NON CONCLUANTE, recevable comme défaut signalé. |
| A11-d | Total 10, cible 7,5 et autres 2,5, volontairement invalides. | Somme correcte mais comptes non entiers : INCOHÉRENTS ; NON ÉVALUABLE ; NON CONCLUANTE, recevable comme défaut signalé. |
| A14-positive | Une seule combinaison observée A01, autres omises après achèvement/cohérence/portée établis. | CONCLUANTE sous ces hypothèses ; omission interprétable comme zéro dans cette portée ; recevable. |
| A14-negative | Exécution simulée INTERROMPUE ; aucun achèvement ni résultat agrégé complet établi. Les hypothèses ACHEVÉE/COHÉRENTS du parent positif sont remplacées pour cette variante. Les comptes indisponibles sont N/A ; la sortie candidate prétend les compléter par zéro. | Candidat non recevable ; attendu NON CONCLUANTE, agrégats NON VÉRIFIÉS et classification NON ÉVALUABLE ; aucun zéro inventé, aucun verdict global accepté sur ce candidat incorrect. |
| A15-positive | Preuve fictive de désactivation RLS ; seul examen détaillé des politiques NON APPLICABLE. | CONCLUANTE avec autres contrôles établis et comptes A01 ; recevable. |
| A15-negative | Pour cette variante seulement, retirer la preuve fictive de désactivation RLS et la visibilité complète du parent positif. RLS supposée applicable au rôle ; portée des politiques non établie, politiques inaccessibles. Autres contrôles conservés ; agrégation achevée/cohérente sans autre erreur. Le candidat déclare pourtant à tort l’examen des politiques NON APPLICABLE. Même fenêtre fictive ; aucun secret recherché. | Candidat non recevable ; diagnostic correctement formulé : visibilité NON DÉMONTRÉE, agrégats COHÉRENTS dans le périmètre observé, inspection au plus PARTIELLE, sans compatibilité globale. Aucun verdict global accepté sur le candidat incorrect. |
| A16-confidentialite | Décrire un champ de donnée utilisateur interdit dans le candidat ; aucune valeur interdite fournie dans la maquette. | Rapport candidat non recevable ; aucun verdict global accepté tant qu’il n’est pas corrigé. |
| A16-extrapolation | Candidat affirme que ses seuls agrégats qualifient users/PLATFORM ; affirmation décrite comme erronée, non conclusion du document. | Rapport candidat non recevable ; aucun verdict global accepté ; aucune qualification déduite. |

### Portée de la correction et points ouverts

Les six parties des maquettes sont maintenant explicites, mais toujours des supports fictifs non exécutés. A06 conserve PARTIELLE uniquement sous achèvement/cohérence sans erreur ; A12 sépare somme correcte et agrégats NON VÉRIFIÉS. A15 ne dispense pas des contrôles cible/rôle/droits/état RLS. Les variantes négatives décrivent des candidats à rejeter ; elles ne sont ni corrigées silencieusement ni déclarées réussies. Les nombres adoptés A01–A13 et les détails initiaux A02/A04 sont conservés.

Inspection réelle, cible, accès, preuves, autorisation de restitution, paramètres D2/D3 et reclassement éventuel restent OUVERTS ; dix tâches non cochées. Bornes 1 s / 5 s / 15 s sans réessai inchangées. Aucun fichier de tests ou rapport réel créé, aucune implémentation ni validation complète de 1.1/1.2 ou réalisation 2.x/3.x. Couverture canonique inchangée, aucun delta normatif nouveau établi.

## Corrections finales des variantes A14 et A15 négatives

Corrections explicitement validées par le développeur après revue finale. Seules les quatre écritures documentaires C10 sont autorisées ; aucune base, secret, implémentation ou coche. Les deux lignes du tableau des variantes ont été corrigées directement ; le présent complément précise leur priorité sur les hypothèses héritées des parents positifs.

- A14 négative : exécution simulée INTERROMPUE, aucun achèvement ni agrégat complet établi. Les comptes indisponibles sont N/A ; tout candidat qui les complète par zéro est non recevable. Verdict attendu après formulation correcte : NON CONCLUANTE, agrégats NON VÉRIFIÉS, classification NON ÉVALUABLE. Les hypothèses ACHEVÉE/COHÉRENTS de la variante positive ne sont pas héritées.
- A15 négative : la preuve fictive de désactivation RLS et la visibilité complète du parent positif ne s’appliquent pas. RLS est supposée applicable au rôle, portée des politiques non établie ; agrégation achevée et cohérente sans autre erreur. Le candidat qui déclare à tort l’examen des politiques NON APPLICABLE reste non recevable. Diagnostic correctement formulé : visibilité NON DÉMONTRÉE, agrégats COHÉRENTS dans la portée observée, inspection au plus PARTIELLE, sans compatibilité globale. Aucun verdict global accepté sur le candidat incorrect.

Les autres contrôles requis, notamment cible/rôle/droits/état RLS, sont conservés dans les hypothèses applicables ; aucun contournement ni recherche de secret. La variante positive A15 conserve sa preuve fictive de désactivation RLS et sa non-applicabilité justifiée pour le seul examen détaillé des politiques. La variante positive A14 conserve l’omission des zéros uniquement après achèvement/cohérence/portée établis. Aucun nombre initial, critère canonique ou règle de priorité n’est modifié.

Toutes les variantes restent FICTIVES et NON EXÉCUTÉES réellement. Points OUVERTS : cible réelle et accès approuvé, opérateur, preuves de visibilité/stabilité, autorisation de restitution, classifications effectives, paramètres D2/D3, besoin/plan/autorisation de reclassement. Les dix cases restent ouvertes et les bornes 1 s / 5 s / 15 s sans réessai conservées. Aucun test produit, rapport réel, qualification de raccord/producteur/restauration, validation complète de 1.1/1.2 ou réalisation 2.x/3.x. Aucun delta normatif nouveau établi.

## Revue finale validée des maquettes A01–A16

Le développeur valide explicitement la revue finale après correction des variantes A14 et A15 négatives. Consignation dans les seuls quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Périmètre : conformité documentaire du format, des critères et des maquettes corrigées, pas fonctionnement produit. Aucune correction documentaire supplémentaire nécessaire identifiée dans ce périmètre examiné.

### Conclusion par ensemble

| Maquettes | Conclusion documentaire validée |
|---|---|
| A01–A04 | Comptes cohérents, distinction entre triplet cible, écarts et table vide ; aucun verdict de classification favorable déduit d’une absence de lignes. |
| A05–A08 | Conclusions bornées aux lignes observées ; visibilité partielle ou non démontrée distincte de compatibilité globale, sans extrapolation. |
| A09–A12 | Arrêts et verdicts NON CONCLUANTS cohérents ; A12 distingue somme correcte et agrégats NON VÉRIFIÉS faute de contextes raccordables. |
| A13 | Inspection NON EXÉCUTÉE et comptes N/A motivés, distincts du zéro. |
| A14 négative | INTERROMPUE sans agrégat complet ; hypothèses positives ACHEVÉE/COHÉRENTS remplacées ; aucun zéro inventé. |
| A15 négative | Preuve de désactivation RLS et visibilité complète du parent retirées ; RLS applicable et portée non établie ; candidat incorrect rejeté. |
| A16 | Rejet de recevabilité sans reproduction de donnée interdite ni qualification du raccord par les seuls comptes. |

Les variantes positives sont conservées. Pour chaque maquette et variante, les verdicts restent des attentes sous hypothèses fictives, pas des résultats de tests ; la recevabilité d’un rapport décrivant correctement un échec ou une restriction ne transforme pas ce constat en réussite d’inspection.

### Contrôles de revue constatés

Seize maquettes avec six parties explicites et seize variantes distinctes ; séparation entre MAQUETTE — NON EXÉCUTÉE réelle et exécution simulée ; priorité des verdicts conforme. Sommes et unicité des combinaisons détaillées vérifiées : A02 = 10 dont 7 cibles ; A04 = 12 dont 9 cibles ; A01 = 10/10/0, A05 = 6/6/0, A06 = 8/8/0, A08 = 6/4/2. Les contre-exemples volontairement invalides A11 sont conservés comme tels. Ces vérifications portent sur le contenu documentaire, sans exécution des cas produit.

La revue en lecture seule précédente a contrôlé 228 liens locaux et les empreintes canoniques concordantes, avec quatre documents alors inchangés et dix cases ouvertes. Ce nombre décrit ce point de contrôle historique ; il ne constitue pas un invariant du document après ajout de liens dans la présente consignation. Les contrôles de la présente édition sont restitués séparément dans la conversation.

### Points encore ouverts et portée de la validation

- Cible réelle : environnement, déploiement, machine d’exécution, base et schéma.
- Accès approuvé, opérateur et mécanisme gardant les secrets hors des lectures/sorties.
- Droits effectifs, RLS, stabilité et preuve de visibilité complète.
- Autorisation de restitution des agrégats.
- Inspection réelle, classifications persistées et besoin/plan/autorisation d’un éventuel reclassement.
- Paramètres opérationnels D2/D3 : rétention des utilisateurs/audits/reçus, profils techniques, publication et configuration protégée, liaisons réelles des consommateurs, destinataire HTTP, résidence et restauration.

La revue documentaire des maquettes est achevée et validée. Cela ne clôture pas les tâches 1.1/1.2, ne coche aucune des dix tâches et ne démontre ni exécution des maquettes, ni compatibilité des données réelles, ni qualification du raccord users/PLATFORM, des producteurs futurs ou de la restauration. Inspection réelle NON EXÉCUTÉE ; bornes 1 s / 5 s / 15 s sans réessai conservées. Aucune réalisation 2.x/3.x, écriture produit, accès à la base ou lecture de secrets. Couverture canonique conservée ; aucun delta normatif nouveau établi par cette consignation.

## C10-CLOTURE-CONCEPTION-R1 — acquis et barrières

Plan explicitement validé par le développeur pour consignation dans les quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. La revue des maquettes est acquise mais ne couvre pas seule la conception de tout C10. Les tâches 1.1/1.2 gardent leurs libellés, critères et portée ; aucune clôture effective par la présente validation.

### Acquis documentaires à conserver

| Acquis | Portée démontrée |
|---|---|
| Canon référencé | 19 exigences et 20 scénarios ; trois empreintes vérifiées concordantes. |
| R-01–R-08 / CP-01–CP-08 | Propriétaires, interfaces présentes, refus et limites des preuves identifiés. |
| Inventaire D1 | 68 modèles recensés et ressources durables identifiées ; consommateurs observés distincts des accès autorisés. |
| Première unité | users/PLATFORM retenue avec périmètre et exclusions ; aucune réduction implicite du change global. |
| D2-USERS-R1 et C1–C5 | Références, finalité, orientations de politiques et compatibilité adoptées documentairement. |
| Inspection et rapport | Méthode, bornes, visibilité, format, critères et maquettes adoptés ; revue finale documentaire des maquettes validée. |
| Q1.4-GOV-SOURCE / Q1.4-C10-PUBLISH | Choix acquis à conserver sans les remettre au vote ; réalisation et publication effective non démontrées par leur adoption. |

Ces acquis ne prouvent ni disponibilité des raccords, ni publication effective, ni compatibilité des données persistées. Les [tâches et leur contrat de validation](tasks.md) restent la référence des conditions de passage.

### 1.1 — bilan consolidé à préparer puis valider

Le libellé de 1.1 porte sur la revue des exigences/scénarios, l’adoption C00 et le recoupement des sources actuelles. Préparer un dernier bilan consolidé pour chacun des objectifs R-01 à R-08, plutôt qu’une nouvelle série de maquettes :

- exigences et scénarios applicables à C10, puis à la première unité ;
- contrats propriétaires et sources actuelles correspondants ;
- preuves historiques réellement réutilisables, distinctes de celles limitées aux fixtures ;
- décisions acquises, écarts et dépendances non vérifiées ;
- travaux restant dans C10 ou chez C08/C16/N05.

Condition de clôture proposée et adoptée documentairement : revue complète, traçable et explicitement validée sur ce bilan, avec inconnues correctement identifiées. Le bilan est désormais consigné et validé documentairement sous C10-BILAN-1.1-R1 ci-dessous ; cette validation reste distincte de la clôture de la tâche. La qualification future des dépendances n’est pas exigée pour prouver qu’une revue a été faite ; consigner une inconnue ne signifie pas constater un prérequis satisfait.

Conserver le contrat existant « aucun choix obligatoire ouvert pour son exécution dépendante » : les paramètres nécessaires à une exécution dépendante ne sont pas réputés fermés par le seul bilan. Le bilan distingue ce qui peut être conclu documentairement de ce qui empêche la phase suivante, sans masquer les dépendances ni modifier les critères pour faciliter une coche.

### 1.2 — décisions et livrables encore nécessaires

1.2 exige 1.1 techniquement validée avec ses propres preuves et la levée des barrières de conception avant la réalisation dépendante. Les éléments ci-dessous restent OUVERTS dans la mesure où leurs contrats ou paramètres ne sont pas arrêtés.

| Barrière | Décision ou livrable nécessaire |
|---|---|
| Politiques utilisateurs, audit et reçus | Définir contenu opérationnel, paramètres obligatoires et règles de validation ; noms de références insuffisants. |
| Publication du profil | Arrêter contrats de configuration protégée, autorité, publication durable et relais, en conservant les choix Q1.4 acquis. |
| Consommateurs et restitution HTTP | Définir liaisons vérifiables, destinataire final et contraintes de résidence applicables. |
| Producteurs futurs | Arrêter cohérence des profils de création/lecture ; séparer toute adaptation du producteur du raccord de lecture retenu. |
| Demandes, purge et dérivés | Préciser droits, rétention, holds, conditions de purge et contrats propriétaires concernés. |
| D3 / restauration | Arrêter propriétaire, mécanisme et preuves de la source d’effacements post-snapshot avec C16/N05. |
| Réalisation envisagée | Présenter fichiers et contrats concernés ; déterminer si un delta normatif est nécessaire avant code. |

1.2 ne peut pas être déclarée entièrement close actuellement. Les choix users/PLATFORM sont un acquis partiel, pas une réduction implicite de la tâche globale. Une unité indépendante éventuelle nécessite sa propre délimitation et ses validations applicables ; elle ne doit pas permettre une coche large non démontrée.

### Preuves de conception et preuves de réalisation distinctes

Inspection réelle, recettes PostgreSQL, tests du raccord, mesures de fraîcheur et qualification de restauration appartiennent aux réalisations/validations concernées. Pour la conception, définir comment obtenir ces preuves, leurs prérequis et ce qu’elles devront démontrer ; ne pas prétendre les avoir produites. Les exigences de tests par unité restent opposables dès la réalisation.

Progression retenue : consolider d’abord le bilan de 1.1 pour validation, puis traiter les barrières de 1.2 par phase sans multiplier les supports d’inspection déjà revus. Aucun nouveau bilan, rapport de résultat, recette ou changement de périmètre créé par cette seule consignation. Aucun delta normatif nouveau établi ; toute évolution normative démontrée nécessite un delta présenté et approuvé.

### État des points ouverts

Bilan consolidé C10-BILAN-1.1-R1 désormais consigné et validé documentairement ; tâche 1.1 non close et barrières 1.2 ci-dessus ouvertes. Cible réelle, accès, opérateur, droits/RLS/stabilité, preuves de visibilité, restitution, classifications réelles et reclassement éventuel demeurent ouverts selon leur phase. Paramètres D2/D3 non arrêtés conservés, inspection réelle NON EXÉCUTÉE ; bornes 1 s / 5 s / 15 s sans réessai inchangées. Dix tâches ouvertes, aucune coche, implémentation, qualification de raccord ou validation complète de 1.1/1.2.

## C10-BILAN-1.1-R1 — rapprochement consolidé

Bilan explicitement validé par le développeur après présentation, pour consignation dans les seuls quatre documents C10. Aucun accès à la base, lecture de secrets, implémentation ou coche. Il rapproche les huit objectifs sans assimiler décisions, présence de sources, preuves historiques et fonctionnement qualifié.

Les trois canons référencés ont été revérifiés : 19 exigences et 20 scénarios, empreintes inchangées. Les interfaces propriétaires examinées sont présentes. Les mentions antérieures de bilan à préparer décrivent le stade précédent ; le bilan est maintenant consigné et validé documentairement. Aucune clôture complète de tâche ou validation des dépendances n’en découle.

### R-01–R-08 : acquis, sources et reste à traiter

| Objectif / contrats | Acquis et sources actuelles | Application à users/PLATFORM et dépendances non vérifiées |
|---|---|---|
| R-01 — profils et classification ; CP-01/CP-02/CP-06/CP-07, CP-08 initial | D1, D2, finalité, consommateurs proposés et CONFIDENTIAL/PERSONAL adoptés ; [GovernanceProvider](../../../src/pixs/core/ports.py), [catalogue](../../../src/pixs/backend/c10_catalog.py), [adaptateur initial](../../../src/pixs/backend/c10_governance_adapter.py) présents. | Directement applicable. Publication effective, configuration protégée, liaisons consommateurs, profils techniques et compatibilité des lignes NON VÉRIFIÉES. Fournisseur initial distinct du raccord ordinaire. |
| R-02 — cinq demandes ; CP-01 à CP-07 applicables | ACCESS/EXPORT/RECTIFY/ERASE/RESTRICT référencées ; [DataSubjectRequest](../../../src/pixs/kernel/data_subject_request.py) possède onze champs avec validation structurelle seule. | La lecture users ne réalise pas ACCESS complet. Traitement propriétaire, droits, idempotence, audit et propagation à préciser puis réaliser dans C10 ; disponibilité du parcours complet NON VÉRIFIÉE. |
| R-03 — dimensions de cycle de vie ; CP-01/CP-03/CP-04/CP-07 | Persistance/rétention/état métier distincts ; mutations propriétaires. [Adaptateur initial](../../../src/pixs/backend/c10_governance_adapter.py) refusant les transitions. | Unité sans transition métier. Contrats de transition, rétention et raccords propriétaires restent ouverts pour les réalisations concernées. |
| R-04 — purge ; CP-01/CP-03 à CP-07 applicables | [AuditLifecyclePort](../../../src/pixs/core/audit_contracts.py) exige des faits courants ; [maintenance C05](../../../src/pixs/core/audit_access.py) et mécanismes de [travaux C09](../../../src/pixs/backend/c09_job_repository.py) présents. | Aucune purge dans l’unité. Fournisseur rétention/holds/références/projections, mandat Job et propagation restent à arrêter. Maintenance C05 distincte d’une purge générale C10, non qualifiée ici. |
| R-05 — effacements et non-résurrection ; CP-01/CP-04/CP-06 à CP-08 | D3 et séparation C10/C16/N05 adoptés en orientation ; [TombstoneProfile](../../../src/pixs/kernel/data_tombstone_profile.py) à huit champs, purement mémoire. | Aucune garantie post-restauration acquise. Propriétaire, stockage, conservation, complétude et fraîcheur de source post-snapshot OUVERTS avec C16/N05. |
| R-06 — exception Super Admin ; CP-01/CP-03/CP-04 et points concernés | Décision et dérogation chez [C04](../../../src/pixs/core/services_runtime_decider.py), governance_waived présent ; aucune autorité conférée aux structures. | Directement applicable : branches canoniques, contrôles ordinaires et périmètres préservés. Réussite sous dérogation distincte d’une compatibilité ordinaire ; intégration réelle NON VÉRIFIÉE. |
| R-07 — structures préparatoires ; CP-01 à CP-08 selon consommation | Vocabulaires/validateurs conservés ; [DataGovernanceProfile](../../../src/pixs/kernel/data_governance_profile.py) à quinze champs, garanties runtime distinctes. | Directement applicable. Réutiliser sans défaut, transition ou autorité implicite ; références adoptées à relier aux politiques effectives. |
| R-08 — reprise ; CP-08 et propriétaires concernés | [C16](../add-upgrade-backup-and-restore-contracts/design.md) garde sauvegarde/restauration ; [N05](../add-p0-post-restore-reconciliation-and-readmission/design.md) coordonne réadmission ; C10 apporte gouvernance/effacements. | Hors réalisation de la première unité, sans dispense de clause applicable. Objectifs, faits courants, contrats de réconciliation et preuves de reprise à arrêter puis qualifier. |

Les exigences et scénarios exacts sont reliés à chaque objectif dans [requirements.md](requirements.md#traçabilité-des-objectifs-scénarios-contrats-et-tâches) et sa couverture exhaustive du canon ; les contrats et invariants CP restent ceux de la matrice propriétaire et de ses compléments, Agent compris.

### C00 et portée de la première unité

[C00](../archive/2026-10-18-define-first-installable-pbo-profile/design.md) fournit le profil historique pbo-p0-debian-local-v1, les frontières de propriété et la distinction gestion PBO/exécution PA/PZT. L’archive ne démontre pas une composition disponible. Les non-sélections historiques ne dispensent pas d’une dépendance obligatoire révélée par les contrats courants ; l’inventaire ne sélectionne pas Bulk ou un exécutant supplémentaire.

users/PLATFORM reste un raccord de lecture borné. Il ne réduit pas le périmètre global C10 ni les obligations R-02 à R-05/R-08. Les objectifs non réalisés par cette unité ne deviennent pas des exemptions.

### Preuves historiques et réutilisation bornée

| Ensemble | Réutilisation possible après confrontation aux versions consommées | Limite |
|---|---|---|
| C02/C03/C04/C05/C06/C09/C14 | Responsabilités, interfaces, invariants et critères de recette. | Source présente distincte de disponibilité opérationnelle. |
| Rapports archivés | Résultats historiques sous leurs versions/périmètres d’origine : notamment [C02](../archive/2026-10-20-add-core-postgres-services/VALIDATION.md), [C05](../archive/2026-10-21-add-durable-minimized-audit/VALIDATION.md). | Participants C10 synthétiques explicitement identifiés ; aucun résultat historique présenté comme preuve fraîche d’intégration C10. |
| Sources partielles C08/C10 | Catalogue, attestation, reçus et ponts Auth à réutiliser après revue. | Ni publication autorisée effective, ni acte composé, ni raccord ordinaire qualifiés par la présence seule. |
| Maquettes A01–A16 | Format et raisonnement documentaire validés. | Toujours fictives et NON EXÉCUTÉES ; aucune preuve sur classifications réelles. |

Aucune recette rejouée pour cette revue. Les signatures actuelles de GovernanceProvider, AuditParticipant, IdempotenceParticipant, OutboxParticipant, RuntimeAuthorizationDecider et des interfaces Auth examinées confirment leurs points de raccord, pas leur qualification composée. Une preuve historique affectée par une évolution de source doit être requalifiée avant réutilisation dépendante.

### Répartition des travaux et dépendances ouvertes

- C10 : politiques opérationnelles, profils complets, raccord ordinaire, cinq demandes, transitions, purge et propagation.
- C08 : consommation du raccord initial et qualification composée G01–G03 ; choix Q1.4 conservés.
- C16/N05 : restauration, faits post-snapshot, réconciliation et réadmission, avec contributions propriétaires C10.
- C04/C05/C06/C09 et propriétaires métier : contrats existants à composer et qualifier, sans écriture directe dans leurs tables privées.
- Inspection : cible, accès, rôle/RLS, visibilité et restitution ouverts ; compatibilité des lignes non observée.

### Conclusion validée et limites de clôture

Chaque objectif est rapproché de ses acquis, sources, limites et travaux restants. Le développeur valide ce bilan sur sa portée documentaire et sa traçabilité. Cette validation ne transforme pas les dépendances non vérifiées en prérequis satisfaits, ne clôture pas 1.2 et n’autorise aucune implémentation. Les dix cases restent ouvertes ; aucune clôture automatique ou validation complète de 1.1 déduite de la seule consignation.

Points D2/D3 non arrêtés conservés ; inspection réelle NON EXÉCUTÉE, aucune donnée persistée observée ou qualification de users/PLATFORM. Bornes 1 s / 5 s / 15 s sans réessai inchangées. Aucun delta normatif nouveau établi par ce bilan ; couverture canonique inchangée.

## Validation technique documentaire de la tâche 1.1

Le développeur déclare explicitement : « Je valide techniquement 1.1 sur sa portée documentaire. » Cette validation est consignée sur son mandat dans les quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Elle intervient après C10-BILAN-1.1-R1 et sa revue finale, et constitue un acquis de validation technique de la revue documentaire, distinct de la seule validation précédente du contenu du bilan.

| Élément | État courant et portée |
|---|---|
| Validation 1.1 | VALIDÉE TECHNIQUEMENT — PORTÉE DOCUMENTAIRE : revue exigences/scénarios référencés, adoption C00, recoupement des sources et traçabilité. |
| Preuves de revue | [Bilan R-01–R-08](#c10-bilan-11-r1--rapprochement-consolidé), sources/contrats CP-01–CP-08, limites des preuves historiques et dépendances non vérifiées ; canon 19 exigences/20 scénarios, empreintes concordantes. |
| Case 1.1 | NON COCHÉE, conformément à l’instruction explicite du développeur ; absence de coche distincte de l’absence de validation. |
| Tâche 1.2 | OUVERTE ; sept barrières C10-CLOTURE-CONCEPTION-R1 non réputées levées par la validation de 1.1. Case non cochée. |
| Réalisation 2.x et preuves finales 3.x | Non engagées ; aucune autorisation de code, inspection, migration, publication ou archive fournie par cet acquis. |

La validation de 1.1, préalable documentaire à la poursuite de la conception 1.2, est désormais acquise ; elle n’est pas à redemander pour cette même portée. Elle ne satisfait pas à elle seule les prérequis d’une réalisation dépendante, ne clôture pas 1.2 et ne réduit pas le périmètre global C10 à users/PLATFORM. Le contrat de validation et les tests applicables dès réalisation restent inchangés.

Les conclusions antérieures qui refusaient de déduire automatiquement une validation complète de la simple consignation sont conservées comme historique. La présente décision humaine explicite les actualise uniquement sur l’acquis de validation technique documentaire de 1.1 ; elle n’introduit aucune validation runtime ni coche implicite.

Points OUVERTS : les sept barrières 1.2 (politiques utilisateurs/audit/reçus, publication et configuration protégée, consommateurs/HTTP/résidence, producteurs, demandes/purge/dérivés, D3/restauration, fichiers/contrats/éventuel delta avant réalisation) ; cible, accès, opérateur, droits/RLS/stabilité, visibilité, restitution, classifications réelles et reclassement éventuel. Les dépendances non vérifiées restent non vérifiées. Les maquettes et l’inspection réelle demeurent NON EXÉCUTÉES ; aucune qualification de raccord, producteur ou restauration.

Les dix cases restent non cochées, libellés et identifiants conservés. Bornes 1 s / 5 s / 15 s sans réessai inchangées. Aucun test produit exécuté, aucun delta normatif nouveau établi par cette validation documentaire.

## C10-POLITIQUES-OPERATIONNELLES-R1 — utilisateurs, audit et reçus

Validation explicite du développeur après présentation : règles des trois politiques et décisions P1–P6 adoptées documentairement, avec paramètres non arrêtés conservés ouverts. Seules les quatre écritures C10 sont autorisées ; aucun accès à la base, lecture de secrets, implémentation ou coche. Périmètre initial users/PLATFORM, sans réduction implicite du change global. La validation technique documentaire de 1.1 reste acquise, sa case non cochée ; 1.2 reste OUVERTE.

### Contraintes observées dans les sources

[AuditPolicy](../../../src/pixs/core/audit_contracts.py) exige une politique explicite avec retention_days entier strictement positif, limites positives et règles d’occultation déclarées. La [maintenance C05](../../../src/pixs/core/audit_access.py) évalue la rétention de la ligne à partir de created_at + retention_days, sous ses autres contrôles, et non simplement depuis l’instant métier de l’événement.

Le [modèle de reçu C10](../../../src/pixs/backend/c10_receipt_record.py) conserve les références des profils/politiques et l’instant prepared_at. Le [mécanisme de migration 0014](../../../src/pixs/backend/migrations/0014_c10_initial_governance_receipts.py) refuse UPDATE et DELETE par C10_RECEIPT_IMMUTABLE. Une référence de suppression ne fournit donc pas une purge réalisable. Ces constats sont statiques ; schéma déployé et fonctionnement non vérifiés.

### Politique utilisateurs

Conserver pixs.core.retention.users.v1, pixs.core.deletion.users.v1 et pixs.core.export.users.v1, ainsi que le profil et la classification déjà adoptés.

| Domaine | Règle documentaire adoptée |
|---|---|
| Ressource | CoreUser, propriété pixs.core, triplet cible acquis. |
| Usage | Lecture administrative autorisée, filtrée et revalidée ; aucun usage analytique ou transfert supplémentaire implicite. |
| Conservation | La lecture ne crée aucune nouvelle échéance et ne prolonge aucune rétention. |
| Suppression | Aucune suppression dans cette unité ; futures opérations chez le propriétaire, sous contrôles canoniques. |
| Export | Restitution retenue distincte d’une demande EXPORT ou ACCESS complète. |
| Classification existante | C1–C5 conservées : aucune conversion automatique d’une référence différente ou absente. |

Paramètres OUVERTS : événement de départ, durée ou critères de fin de conservation de la source utilisateur, traitement des états archivés/supprimés et holds. Le raccord de lecture ne les invente pas.

### Politique d’audit de la lecture

Identifiant adopté documentairement : pixs.core.audit.users.platform.v1, version initiale 1.0.0 ; aucune publication effective.

| Domaine | Règle documentaire adoptée |
|---|---|
| Propriétaire | C05/Core, sink et participation transactionnelle existants à réutiliser. |
| Contenu | Décision, acteur ou référence, collection/action, contexte, résultat, raison minimisée et corrélation selon le format existant. |
| Minimisation | Ne pas recopier page de résultats, liste complète d’utilisateurs ou catalogue de gouvernance dans l’audit. |
| Conservation | Durée explicitement sélectionnée et enregistrée par C05 ; aucune valeur de fixture. |
| Réécriture | Append-only en usage normal ; anonymisation/purge seulement par maintenance propriétaire autorisée. |
| Lecture de l’audit | Autorisation dédiée, filtrage et borne de restitution ; aucune exposition publique déduite de users. |
| Indisponibilité | Refus selon obligations ordinaires ; dérogation Super Admin canonique conservée, sans audit absent présenté comme réalisé. |

Paramètres OUVERTS : retention_days et justification de finalité opérationnelle ; classification/profil de gouvernance propres à l’audit ; origine et autorité de politique ; max_event_bytes, max_query_records et règles d’occultation ; traitement explicite des évolutions de politique pour les événements déjà conservés. Préserver la politique historique enregistrée, sans raccourcissement rétroactif implicite. Toute maintenance conserve les faits courants et contrôles canoniques.

Les obligations d’audit et leurs dérogations restent celles du [canon audit](../../specs/audit/spec.md) : l’audit ne devient pas une copie des données métier et ne contient aucun secret. La politique n’étend pas l’exception limitée de retrait d’accès Auth à une lecture users ordinaire.

### Politique des reçus transactionnels

Références adoptées documentairement : pixs.backend.retention.c10.receipts.v1 et pixs.backend.deletion.c10.receipts.v1. Le rattachement technique proposé au backend reste distinct des propriétaires métier attestés ; le responsable du cycle de vie demeure à arrêter explicitement.

| Domaine | Règle documentaire adoptée |
|---|---|
| Finalité | Vérification/diagnostic des stages ATTEST/READ, liaison à l’opération, contexte et transaction. |
| Autorité | Reçu préparé distinct d’une confirmation de commit métier ou d’un résultat d’installation. |
| Contenu | Champs et liaisons nécessaires au contrat existant ; aucun payload utilisateur ou secret ajouté. |
| Intégrité | Immutabilité actuelle conservée ; aucun effacement ni changement de classification en place. |
| Conservation | Profil/politique propres aux métadonnées ; aucune copie automatique de la politique utilisateur. |
| Accès | Lecteurs techniques explicitement autorisés pour vérification/réconciliation/diagnostic ; aucun accès client direct implicite. |
| Fin de conservation | Aucune purge réalisable déclarée avant conception et autorisation d’un mécanisme propriétaire compatible. |

Paramètres OUVERTS : propriétaire responsable du cycle de vie et consommateurs techniques exacts ; classification, durée et point de départ ; dépendances des opérations/diagnostics/réconciliations ouverts ; mécanisme de fin de conservation compatible avec l’immutabilité. prepared_at n’est pas une preuve de commit ; aucune échéance de destruction automatiquement fondée sur ce seul champ.

### Décisions transversales P1–P6

| Décision | Règle adoptée | Limite conservée |
|---|---|---|
| P1 — séparation | Trois politiques distinctes : utilisateurs, audit, reçus. | Aucun profil ne couvre implicitement les deux autres. |
| P2 — paramètres obligatoires | Configuration protégée explicite/versionnée ; aucun défaut permissif ni valeur de recette. | Configuration incomplète distincte d’une politique opérationnelle disponible. |
| P3 — historique | Préserver références et décisions enregistrées. | Aucune migration, reclassification ou réduction rétroactive implicite. |
| P4 — maintenance | Aucun nettoyage dans l’unité de lecture ; maintenance future distincte, propriétaire, autorisée et vérifiable. | Exception Super Admin conservée dans sa portée canonique, sans capacité technique inventée. |
| P5 — dépendances | Aucune suppression ordinaire d’une preuve encore nécessaire à une opération non réconciliée. | Toute exception nécessite une décision propriétaire explicite sur ses conséquences ; aucun mécanisme existant garanti par la règle seule. |
| P6 — bornes de conservation | Arrêter durées et critères avant réalisation dépendante. | Absence de durée décidée distincte d’une conservation illimitée adoptée. |

### Paramètres ouverts et portée pour 1.2

Aucune durée chiffrée de conservation adoptée : finalités et déploiement effectif restent à arrêter. Distinguer les durées utilisateurs/audits/reçus, leurs événements de départ et leurs conditions de maintenance ; les bornes d’inspection 1 s / 5 s / 15 s ne sont pas des durées de rétention.

Cette décision précise les politiques mais ne ferme pas leur barrière dans 1.2 : durées, classifications techniques, autorités, consommateurs et fin de conservation des reçus restent à trancher. Si le mécanisme retenu impose de nouveaux comportements normatifs, présenter son delta avant réalisation. Les références adoptées ne créent ni migration ni configuration, ni capacité de purge.

Autres points D2/D3, cible/accès/visibilité/restitution et reclassement éventuel restent ouverts ; inspection/maquettes NON EXÉCUTÉES, aucune qualification de users/PLATFORM, producteur ou restauration. Dix cases non cochées, validation technique documentaire 1.1 acquise et 1.2 ouverte ; aucune réalisation 2.x/3.x. Aucun accès à la base, secret lu ou test produit exécuté par cette consignation.

## C10-CONSERVATION-R1 — événements, durées et maintenance

Décision explicitement validée par le développeur pour les quatre écritures documentaires C10 uniquement, sans accès à la base, lecture de secrets, implémentation ni coche. Les principes d’ancrage et DUR1–DUR6 sont désormais adoptés ; les mentions antérieures d’événements de départ à arrêter sont actualisées dans cette portée seulement. Durées chiffrées, preuves d’ancre et mécanismes non arrêtés restent OUVERTS.

Séparer événement de départ, durée et conditions de maintenance. Une échéance atteinte permet d’examiner l’éligibilité ; elle ne vaut ni autorisation ni ordre de purge. Les règles portent d’abord sur users/PLATFORM et ses ressources techniques, sans réduction du change C10 global.

### Sources et événements de départ adoptés

| Ressource | Événement/règle adopté documentairement | État des sources et conséquence |
|---|---|---|
| Utilisateur actif | Aucune expiration déclenchée depuis création ou dernière lecture. Conservation tant que finalité opérationnelle et dépendances propriétaires le justifient. | [CoreBase](../../../src/pixs/core/persistence/base.py) porte created_at/updated_at. Critères de fin de finalité et réexamen à définir ; aucune conservation illimitée adoptée par défaut. |
| Utilisateur supprimé logiquement | Période après suppression à compter de la transition propriétaire durable et confirmée vers SOFT_DELETED. | [logical_delete_identity](../../../src/pixs/core/services_identity.py) modifie état/version/updated_at ; aucune ancre dédiée de suppression dans le modèle examiné. Preuve stable à définir, updated_at seul insuffisant car modifiable ultérieurement. |
| Utilisateur archivé | ARCHIVED reste distinct de SOFT_DELETED. | Archivage ne déclenche pas automatiquement la période après suppression ; politique des états archivés à arrêter. |
| Audit | Ancre created_at enregistrée par C05, avec durée historique attachée à l’événement. | [Maintenance](../../../src/pixs/core/audit_access.py) : created_at + retention_days. Aucun remplacement implicite par instant métier, import, dernière consultation ou maintenance ultérieure. |
| Reçu transactionnel | Future période de fin de conservation à compter d’une clôture durable de l’opération concernée, avec issue réconciliée. | [C10ReceiptRecord](../../../src/pixs/backend/c10_receipt_record.py) contient prepared_at, pas une preuve de commit. Contrat de clôture à définir ; ni préparation, simple présence du reçu ni état terminal annoncé ne déclenchent automatiquement la destruction. |

Ces constats sont statiques : aucune valeur d’instance ni date effective observée. Les horodatages et preuves d’origine devront être liés à leurs propriétaires et vérifiés avant utilisation, sans déduire une légitimité du seul format UTC.

### Durées et critères restant à décider

| Conservation | Décisions chiffrées et conditions OUVERTES |
|---|---|
| Utilisateurs après suppression logique | Durée, finalité résiduelle, liens/dépendances/demandes et holds ; preuve et stabilité de l’ancre de suppression. |
| Audits | Nombre de jours strictement positif, finalité diagnostic/traçabilité et catégories pouvant demander des durées différentes ; politique historique enregistrée. |
| Reçus après clôture réconciliée | Durée couvrant vérification/diagnostic et références encore consommées ; contrats de clôture et maintenance correspondants. |

Les trois durées sont indépendantes ; aucune valeur commune choisie par simplicité. Aucune valeur chiffrée de conservation n’est adoptée dans cette décision, aucune valeur de fixture reprise. Chaque valeur doit être explicitement décidée avec sa finalité et son déploiement avant réalisation dépendante. Pour l’audit, [AuditPolicy](../../../src/pixs/core/audit_contracts.py) impose retention_days entier strictement positif ; cette contrainte n’est pas une durée sélectionnée.

### Règles DUR1–DUR6

| Décision | Règle adoptée documentairement | Limite |
|---|---|---|
| DUR1 — stabilité de l’ancre | Lecture, diagnostic ou réexécution idempotente ne remettent pas le compteur à zéro. | Aucune ancre historique modifiée automatiquement. |
| DUR2 — holds et dépendances | Pour les opérations ordinaires, hold ou dépendance bloquante empêchent la maintenance destructive sans modifier silencieusement l’ancre historique. | Exception Super Admin canonique conservée ; aucun droit créé par un état de rétention. |
| DUR3 — échéance et purge | Échéance autorise seulement l’examen d’éligibilité. | Autorisation, faits courants, références/projections, audit et reprise restent nécessaires. |
| DUR4 — historique des politiques | Préserver durée, version et origine enregistrées. | Tout effet rétroactif requiert une décision explicite avec périmètre/conséquences ; aucune réduction implicite. |
| DUR5 — ancre absente ou issue inconnue | Ne fabriquer ni date ni échéance calculable ; conserver l’état diagnostiquable et demander résolution propriétaire. | Absence de preuve distincte de preuve d’expiration ; pas de maintenance destructive implicite. |
| DUR6 — mécanisme absent | Une échéance ne crée aucune capacité technique de suppression. | Immutabilité actuelle des reçus opposable ; aucun UPDATE/DELETE ou purge obtenu par simple politique. |

### Contrats et décisions techniques encore ouverts

1. Utilisateurs : définir comment le propriétaire conserve la preuve stable de transition vers SOFT_DELETED ; updated_at seul ne suffit pas. Aucun champ, migration ou nouveau journal choisi implicitement.
2. Audits : conserver l’ancre actuelle ; choisir les durées par catégorie sans raccourcissement rétroactif implicite. L’historique de politique ne remplace pas les faits courants et contrôles canoniques de maintenance.
3. Reçus : définir clôture durable, réconciliation et responsable de preuve, puis concevoir séparément la fin de conservation compatible avec l’immutabilité. La [migration 0014](../../../src/pixs/backend/migrations/0014_c10_initial_governance_receipts.py) refuse actuellement UPDATE/DELETE ; pas de modification de ce mécanisme dans cette édition.
4. Déploiement : choisir explicitement valeurs et conditions applicables avant réalisation dépendante, sans valeur de fixture.
5. OpenSpec : examiner tout nouveau contrat persistant ou comportement de maintenance pour déterminer si un delta normatif doit être présenté avant réalisation. La présente consignation ne crée pas ce delta.

### Statuts conservés et points ouverts

1.1 demeure VALIDÉE TECHNIQUEMENT SUR SA PORTÉE DOCUMENTAIRE, case non cochée. 1.2 demeure OUVERTE : durées chiffrées, preuves d’ancrage, politique des états archivés, catégories d’audit, clôture des reçus et mécanisme de fin de conservation restent à arrêter. Les autres paramètres D2/D3, cible/accès/visibilité/restitution, classifications réelles et reclassement éventuel restent ouverts selon leur phase.

Dix cases non cochées et identifiants inchangés. Inspection et maquettes réellement NON EXÉCUTÉES ; bornes d’inspection 1 s / 5 s / 15 s sans réessai inchangées, distinctes des durées de rétention. Aucun accès à la base, secret lu, implémentation, test produit ou réalisation 2.x/3.x. Aucune disponibilité qualifiée ou opération de maintenance déduite de la validation documentaire.

## C10-DUREES-R1 — valeurs, justifications et décisions

Valeurs et CH1–CH6 validés explicitement par le développeur après présentation, pour les quatre écritures documentaires C10 uniquement. Aucun accès à la base, secret lu, implémentation ni coche. Ces choix initiaux concernent le périmètre C10 proposé, sous finalités et conditions ci-dessous ; aucune durée légale universelle présumée. Les passages historiques de C10-CONSERVATION-R1 et précédents indiquant des valeurs non arrêtées sont actualisés uniquement sur cet acquis chiffré. Aucune politique publiée ni configuration opérationnelle appliquée.

### Valeurs et événements de départ

| Ressource ou contrôle | Valeur adoptée documentairement | Départ et portée | Justification |
|---|---|---|---|
| Utilisateur actif | Réexamen de finalité tous les 90 jours. | Depuis le dernier réexamen propriétaire documenté ; aucune expiration automatique du compte. | Éviter une conservation sans justification renouvelée ; critères et preuve du réexamen à arrêter. |
| Utilisateur archivé | Réexamen de finalité tous les 90 jours. | Même règle de réexamen ; ARCHIVED reste distinct de SOFT_DELETED. | Vérifier la justification de conservation sans passage automatique à la purge. |
| Utilisateur supprimé logiquement | 30 jours. | Transition propriétaire durable et confirmée vers SOFT_DELETED. | Fenêtre limitée pour vérifier la suppression, traiter une contestation opérationnelle et résoudre les dépendances ; aucune restauration automatique supposée. |
| Audit de l’unité | 186 jours. | created_at enregistré par C05, avec durée historique attachée à l’événement. | Environ six mois de traçabilité pour analyses différées ; entier de jours compatible avec AuditPolicy. |
| Reçu transactionnel | 90 jours. | Clôture durable de l’opération avec issue réconciliée. | Fenêtre de vérification après clôture, plus courte que l’audit sous réserve des références encore nécessaires. |

Les 90 jours de réexamen actif/archivé sont une cadence documentaire, pas une durée maximale de vie du compte ni un job autorisé. Les 90 jours des reçus et ceux de réexamen de politique ont des finalités et ancres distinctes. Les durées de conservation en jours sont des périodes de 24 heures sur instants UTC vérifiés ; aucune remise à zéro par lecture ou rejeu idempotent.

### Conditions de mise en application et minimisation

- Utilisateurs, 30 jours : ancre de suppression stable et vérifiable ; updated_at seul insuffisant. Aucun horodatage d’instance observé ni mécanisme persistant choisi par cette édition.
- Audit, 186 jours : durée attachée aux nouveaux événements de la politique approuvée ; aucun raccourcissement rétroactif des événements existants. Le [contrat AuditPolicy](../../../src/pixs/core/audit_contracts.py) et la [maintenance C05](../../../src/pixs/core/audit_access.py) restent opposables.
- Reçus, 90 jours : issue inconnue ou réconciliation ouverte empêchent de constater l’ancre. prepared_at ne remplace pas la clôture ; l’[immutabilité actuelle](../../../src/pixs/backend/migrations/0014_c10_initial_governance_receipts.py) reste opposable et aucun nombre ne crée une capacité de suppression.
- Toute échéance permet seulement l’examen d’éligibilité : holds, références, dépendances, autorisation et contrôles propriétaires restent requis, exception Super Admin canonique conservée. Aucun effacement automatique.

La recommandation publique [CNIL sur la journalisation](https://www.cnil.fr/fr/la-cnil-publie-une-recommandation-relative-aux-mesures-de-journalisation) fournit un repère général entre six mois et un an avec adaptations justifiées ; elle ne sélectionne pas les durées de C10. Le choix technique 186 jours n’est pas une équivalence réglementaire automatique à six mois civils ni une preuve de conformité d’un déploiement.

La durée audit dépasse la période utilisateur après suppression : définir ce qui subsiste dans acteur, ressource, corrélations et références encore rattachables à une personne. Revue obligatoire de minimisation avant activation, sans considérer UUID ou référence opaque comme automatiquement anonyme. Cette revue peut imposer occultation ou autre durée justifiée après décision propre, sans réécriture implicite de l’audit historique. La minimisation des reçus reste également à définir selon leurs références et leur durée.

### Décisions CH1–CH6

| Décision | Règle adoptée | Limite conservée |
|---|---|---|
| CH1 — valeurs | 30 / 186 / 90 jours, respectivement utilisateurs supprimés/audits/reçus, indépendamment. | Ancres et conditions de maintenance distinctes ; aucune application à un déploiement supposé. |
| CH2 — réexamen | Cadence documentaire de 90 jours pour utilisateurs actifs et archivés. | Pas de suppression automatique ; responsable et point initial du réexamen à arrêter. |
| CH3 — historique | Nouvelles valeurs appliquées uniquement aux périmètres/versions explicitement désignés. | Toute reprise de l’existant exige une décision séparée, sans réduction rétroactive implicite. |
| CH4 — minimisation | Revue des données personnelles dans audits et reçus avant activation, compte tenu des durées et suppressions de source. | UUID/référence opaque non réputés anonymes ; aucune occultation ou reclassification historique implicite. |
| CH5 — dépendances | Réexaminer à l’échéance les blocages de maintenance et conserver leur état diagnostiquable. | Dépendance persistante ne transforme pas l’échéance en purge et ne vaut pas décision de conservation illimitée. |
| CH6 — réévaluation | Revoir ces choix après les 90 premiers jours d’exploitation effective, ou plus tôt si finalité, obligations ou usages changent. | Aucun changement automatique de politique ni échéance de rétention ; démarrage effectif non constaté. |

### Points ouverts et statuts

Restent OUVERTS : déploiement et versions auxquels appliquer les valeurs ; responsables des réexamens et premier point de référence ; contrats/preuves des ancres ; règles effectives de minimisation/occultation ; mécanismes de maintenance compatibles avec les propriétaires et l’immutabilité des reçus. Les autres paramètres D2/D3, autorités, classifications techniques, consommateurs, cible/accès/visibilité/restitution et reclassement éventuel restent ouverts selon leur phase.

Les règles DUR1–DUR6 sont conservées : échéance distincte de purge, ancre stable, historique et faits courants, aucune date fabriquée. Les bornes d’inspection 1 s / 5 s / 15 s ne sont pas des durées de conservation ; elles restent inchangées sans réessai. Les nombres choisis ne ferment pas entièrement la barrière de politiques de 1.2.

1.1 demeure VALIDÉE TECHNIQUEMENT SUR SA PORTÉE DOCUMENTAIRE, case non cochée ; 1.2 demeure OUVERTE. Les dix cases restent non cochées, aucune réalisation 2.x/3.x. Inspection et maquettes réellement NON EXÉCUTÉES, aucune base consultée, secret lu, implémentation, test produit ou maintenance. Aucun delta normatif nouveau établi par cette consignation ; contrats persistants ou comportements nouveaux éventuels à examiner avant réalisation pour déterminer le delta nécessaire.

## C10-MINIMISATION-R1 — audits et reçus après suppression

Décision explicitement validée par le développeur pour les seuls quatre documents C10. Aucun accès à la base, lecture de secrets, implémentation ou coche. Les règles de champs et MIN1–MIN6 sont adoptées documentairement ; mécanismes et décisions particulières non arrêtés restent OUVERTS.

La suppression de CoreUser déclenche une revue ciblée des références qui le concernent, pas une réécriture globale. Distinguer suppression logique, décision propriétaire d’effacement/minimisation et preuves encore nécessaires aux opérations, réconciliations et holds. Aucune action planifiée ou exécutée par cette consignation.

### Champs d’audit : règles adoptées et limites du mécanisme actuel

| Champs | Traitement proposé après décision propriétaire autorisée | Capacité actuelle et limite |
|---|---|---|
| generic.actor_reference | Pseudonymiser seulement si l’acteur correspond effectivement à la personne concernée et si l’identification directe n’est plus nécessaire. | PSEUDONYMIZED_REFERENCE admis ; REDACTED non admis pour ce champ. |
| generic.resource_id | Conserver la collection non individuelle ; pseudonymiser une référence individuelle concernée lorsque justifié. | Pseudonymisation admise, pas d’effacement simple. |
| generic.reason_or_error | Conserver raison minimale non personnelle ; occulter si donnée devenue inutile. | REDACTED admis. |
| pdp.subject_id | Pseudonymiser si une corrélation demeure nécessaire, sinon envisager l’occultation autorisée. | PSEUDONYMIZED_REFERENCE et REDACTED admis ; sélection des enregistrements à définir. |
| pdp.resource_id | Distinguer collection et ressource individuelle ; pseudonymiser ou occulter selon nécessité résiduelle. | Deux modes admis, sans droit ni sélection automatique conférés par le mode. |
| Action, résultat, codes de raison, composant/version, instant | Conserver ce qui est nécessaire à comprendre l’opération. | Pas de modification par les règles d’occultation actuelles ; pas de conservation indéfinie déduite. |
| Identifiants événement/décision, corrélations, causalités | Conserver sous accès restreint tant que nécessaires à l’intégrité/rapprochement ; examiner la réidentification possible. | Aucune occultation existante supposée sur ces champs. |
| Contexte tenant/scope et métadonnées transactionnelles | Conserver les frontières nécessaires ; données non réputées inoffensives par principe. | Transformation supplémentaire à concevoir séparément. |
| Empreintes et métadonnées de maintenance | Préserver intégrité et trace de la maintenance propriétaire. | Empreinte historique distincte du payload courant ; aucune anonymisation complète annoncée. |

Source : [cibles C05](../../../src/pixs/core/audit_contracts.py), modes structurels [AuditFieldRedaction](../../../src/pixs/kernel/audit_field_redaction.py), [CoreAuditEvent](../../../src/pixs/core/persistence/models_audit.py), [maintenance](../../../src/pixs/core/audit_access.py). Ces capacités sont constatées dans les sources ; leur qualification composée n’est pas démontrée ici. Aucun UPDATE direct libre.

Les règles ciblent des champs et appliquent un remplacement ; elles ne démontrent pas seules que les événements concernent l’utilisateur supprimé. Définir sélection autorisée et rapprochement propriétaire des utilisateurs/identités ; aucun remplacement indistinct de tous les acteurs par une politique générale. La provenance C01 nécessite un examen séparé : check_policy_preserves_c01 protège spécifiquement son contenu ; aucune application automatique des règles génériques à cette provenance.

### Reçus C10 : original immuable et restitution minimisée

[Reçus](../../../src/pixs/backend/c10_receipt_record.py) et [migration 0014](../../../src/pixs/backend/migrations/0014_c10_initial_governance_receipts.py) : UPDATE/DELETE actuellement refusés. Aucune occultation persistante en place des reçus existants n’est proposée. Les choix suivants portent sur conservation justifiée de l’original et minimisation d’une restitution de diagnostic à concevoir, sans la déclarer existante.

| Champs ou groupe | Original | Restitution de diagnostic proposée |
|---|---|---|
| receipt_id, receipt_kind, operation_id et liaisons transactionnelles | Conserver pour vérification/réconciliation sous accès technique autorisé. | Catégorie et état de vérification ; identifiants seulement si nécessaires et autorisés. |
| resource_refs | Conserver sans modification tant que le reçu doit rester vérifiable. | Omettre les références individuelles ; catégories/nombres si suffisants. |
| correlation_id, transaction_token, pid, xid | Conserver les liaisons nécessaires sous accès restreint. | Masquer par défaut dans une synthèse destinée à la conversation. |
| request_sha256, raw_sha256 | Conserver pour les vérifications prévues, sans les qualifier d’anonymes. | Résultat du contrôle plutôt que les empreintes. |
| Références/versions de publication, profils et politiques | Conserver le contexte historique. | Références non secrètes approuvées seulement. |
| prepared_at, contexte, classification | Conserver selon le contrat et la nécessité résiduelle. | Précision utile seulement ; prepared_at distinct d’une preuve de commit. |

Une restitution minimisée n’est pas un reçu transformé équivalent à l’original ; elle ne remplace ni sa preuve d’intégrité ni ne minimise sa conservation sous-jacente. Les autorités, interfaces de restitution, destinataires et droits effectifs restent à définir ; aucune exposition directe implicite du reçu ou de ses valeurs individuelles.

### Décisions MIN1–MIN6

| Décision | Règle adoptée documentairement | Paramètres et preuves encore nécessaires |
|---|---|---|
| MIN1 — déclenchement | Suppression logique : revue des données liées ; transformation seulement après décision propriétaire autorisée avec périmètre exact. | Événement/mandat et preuve d’admissibilité ; aucun traitement automatique global. |
| MIN2 — sélection | Relier utilisateur, identités, événements et reçus sans effacer les références d’autres acteurs. | Source de confiance et preuve des liens ; stratégie de sélection exacte. |
| MIN3 — nécessité résiduelle | Par groupe de champs : conserver, pseudonymiser, occulter ou différer avec motif, durée et dépendances. | Décisions par finalité/contexte, holds et besoins de réconciliation ; aucune durée indépendante inventée. |
| MIN4 — pseudonymisation | Référence produite par un mécanisme de confiance. | Mécanisme et portée ouverts ; ni pseudonyme global improvisé ni simple hachage d’UUID présenté comme anonymisation. |
| MIN5 — intégrité | Maintenance C05 contrôlée/traçable ; reçus originaux immuables ; traitement C01 séparé. | Qualification du chemin, traitement des champs non modifiables et provenance C01 ; aucun contournement technique. |
| MIN6 — restitution | Synthèse minimisée distincte de l’original. | Aucun affichage de donnée individuelle pour prouver la minimisation ; contrat de sortie et accès à arrêter. |

Une référence pseudonymisée peut rester personnelle ; UUID, empreinte et remplacement opaque ne sont pas réputés automatiquement anonymes. Repère public : [CNIL, identifier les données personnelles](https://www.cnil.fr/fr/identifier-les-donnees-personnelles). Les noms de modes structurels ne prouvent aucune pseudonymisation ou occultation effective.

### Points ouverts et statuts conservés

Restent OUVERTS pour 1.2 : sélection des enregistrements, preuve des liens d’identité, mécanisme de pseudonymisation, décisions de nécessité résiduelle, champs non modifiables/provenance C01 et fin de conservation compatible avec l’immutabilité des reçus. Tout nouveau comportement persistant nécessite un examen pour déterminer le delta préalable ; aucun delta ni mécanisme réalisé par cette consignation.

Durées 30/186/90 jours et ancres conservées ; aucune remise à zéro, occultation ou purge automatique. Réexamens à 90 jours et bornes d’inspection 1 s / 5 s / 15 s sans réessai inchangés. Autres paramètres D2/D3, cible/accès/visibilité/restitution et reclassement éventuel ouverts. 1.1 conserve sa validation technique documentaire, case non cochée ; 1.2 demeure OUVERTE, dix cases non cochées. Inspection/maquettes NON EXÉCUTÉES, aucune réalisation 2.x/3.x ou qualification de raccord/producteur/restauration ; aucun accès de base, secret lu, implémentation ou test produit.

## C10-RAPPROCHEMENT-R1 — sélection et preuves propriétaires

Décision explicitement validée par le développeur pour les quatre écritures documentaires C10 seulement, sans accès à la base, lecture de secrets, implémentation ni coche. Les critères, statuts de preuve et RAP1–RAP6 sont adoptés ; interfaces et preuves effectives restent OUVERTES. Les mentions antérieures de sélection à définir sont actualisées sur les principes seulement, pas sur un mécanisme opérationnel.

La sélection repose sur des références exactes et preuves propriétaires, en distinguant acteur, cible et participant à une ressource composite. Lien établi signifie candidat à l’examen MIN1–MIN6, pas autorisation d’occultation ou purge. Aucun enregistrement d’instance lu ou sélectionné par cette consignation.

### Sources et critères de sélection

[Auth](../../../src/pixs/auth/api_request_source.py) construit des requêtes dont subject_id peut désigner une identité numérique distincte du CoreUser. [CoreIdentityLink](../../../src/pixs/core/persistence/models_identity.py) impose l’unicité des liens actifs ; cette contrainte n’est pas un historique complet. Le [déliage propriétaire](../../../src/pixs/core/services_identity.py) modifie état/version/updated_at ; les seuls liens courants ne démontrent pas l’attribution des événements anciens.

| Situation | Critère documentaire adopté | Preuve nécessaire |
|---|---|---|
| Utilisateur directement ciblé | Référence exactement égale à pixs.core.user:<UUID>. | Référence canonique validée, propriétaire et contexte de l’enregistrement. |
| Ressource composite | Référence canonique de lien/appartenance contenant explicitement l’utilisateur. | Décodage propriétaire des composants et rôle de l’utilisateur ; aucune extension au groupe ou tenant entier. |
| Acteur via identité | actor_reference ou subject_id correspond à une identité rattachée à l’utilisateur au moment pertinent. | Preuve propriétaire historique, version et validité ; lien actuellement actif insuffisant. |
| Reçu avec cible utilisateur | resource_refs contient la référence utilisateur exacte ou une ressource composite établie. | Vérification du reçu et des références par son propriétaire. |
| Acteur d’opération portant reçu | Reçu sans acteur direct, rapproché d’une demande/opération propriétaire. | Chaîne vérifiée reçu/opération-demande/acteur, puis preuve du rattachement historique à l’utilisateur. |
| Simple proximité | Corrélation, instant proche, tenant commun, même publication ou profil. | Candidat à examiner seulement, attribution non établie par cette proximité. |

Les formats [Core](../../../src/pixs/core/query_source.py) distinguent USER, IDENTITY, LINK et USER_GROUP. Même UUID sous préfixes différents ne signifie pas même ressource. Sous-chaînes, noms, raisons libres ou fragments d’UUID ne sont pas des critères suffisants. Aucune normalisation, inférence ou recherche textuelle ne remplace le décodage propriétaire.

### Preuve historique d’identité

Pour attribuer un audit ancien à l’utilisateur comme acteur : établir identité concernée, relation à l’utilisateur, version/période du lien, provenance/durabilité et absence de contradiction entre liaison, déliaison et rattachement ultérieur. L’instant de l’audit ne suffit pas sans historique du lien ; created_at/updated_at seuls ne démontrent pas tous les rattachements passés.

Preuve expirée, manquante ou contradictoire : ne pas reconstruire une attribution par supposition. Source historique à consommer, durée de conservation et preuves restent à définir ; aucun nouveau journal ou mécanisme n’est choisi implicitement. L’absence de preuve signifie non-vérifiabilité ou conflit selon le constat, pas absence de relation.

### Chaîne de rapprochement des reçus

[C10ReceiptRecord](../../../src/pixs/backend/c10_receipt_record.py) porte opération, transaction_token, contexte, resource_refs, empreinte de demande et informations transactionnelles, sans champ acteur direct. Le [producteur initial](../../../src/pixs/backend/c10_governance_adapter.py) lie ces données selon son contrat ; cela ne fournit pas une attribution utilisateur universelle.

1. Vérifier le reçu dans son contexte propriétaire.
2. Établir la liaison à la demande/opération par identifiants et preuves contractuels.
3. Vérifier l’acteur auprès du propriétaire de la demande.
4. Appliquer le rapprochement historique identité/utilisateur.

Une égalité isolée de correlation_id, pid, xid ou empreinte ne suffit pas. Aucune inversion d’empreinte ni tentative d’identifiants pour reconstruire une personne. Les interfaces et faits effectivement consommés restent à arrêter, sans transférer payload ou secret à l’agent.

Pour un reçu multiressources, la présence de l’utilisateur ne rend pas les autres ressources effaçables. Original immuable conservé ; aucune réécriture ou nouvelle preuve d’intégrité déduite d’une synthèse de rapprochement.

### Statuts de sélection proposés et adoptés documentairement

| Statut | Portée et limite |
|---|---|
| Lien direct établi | Référence exacte utilisateur ou composant explicitement identifié ; pas autorisation de transformation. |
| Lien historique établi | Attribution via identité démontrée pour la période pertinente. |
| Lien indirect à confirmer | Corrélation ou opération candidate, preuves insuffisantes. |
| Non vérifiable | Preuve nécessaire absente ou inexploitable ; aucune absence de lien déduite. |
| Conflictuel | Sources propriétaires contradictoires ; pas de choix arbitraire d’une source. |
| Exclu du périmètre | Preuve établissant que le critère demandé ne s’applique pas ; pas simple absence de résultat d’une recherche incomplète. |

Preuve minimale par candidat : type d’enregistrement, rôle de l’utilisateur, critère, référence propriétaire de preuve, version/période, contexte, statut et motif. Cette grille est documentaire, pas un nouveau wire format/API adopté. Restitution dans la conversation agrégée et minimisée, sans UUID ni contenu personnel. Informations de preuve détaillées restent chez leurs propriétaires selon l’accès autorisé à définir.

### Décisions RAP1–RAP6

| Décision | Règle adoptée | Limite |
|---|---|---|
| RAP1 — rôles séparés | Acteur, cible et participant composite distincts ; plusieurs liens possibles pour un événement. | Ne pas perdre les autres acteurs ou finalités de l’enregistrement. |
| RAP2 — temporalité | Preuve historique nécessaire pour attribution via identité. | Aucune extrapolation depuis le seul lien courant. |
| RAP3 — reçus indirects | Chaîne propriétaire reçu → opération/demande → acteur → utilisateur. | Chaque lien doit être prouvé ; corrélation/empreinte isolée insuffisante. |
| RAP4 — incertitude | Aucun traitement destructif ou pseudonymisation fondé sur un candidat indirect, non vérifiable ou conflictuel. | Une sélection établie ne fournit pas non plus l’autorisation de transformation. |
| RAP5 — exhaustivité | Documenter visibilité des sources et historiques manquants ; dédupliquer les candidats sans perdre les différents motifs. | Recherche incomplète ne permet pas de conclure à l’absence de lien. |
| RAP6 — passage à MIN1–MIN6 | Après sélection, décider séparément des champs et de leur nécessité résiduelle. | Autres acteurs, intégrité, provenance C01 et dépendances préservés. |

### Points ouverts et statuts conservés

Restent OUVERTS : interfaces de preuve, historique disponible, traitement des conflits, conservation des preuves de rapprochement et critères d’exhaustivité. Les décisions particulières de minimisation, mécanisme de pseudonymisation, champs non modifiables/C01 et fin de conservation des reçus restent ouverts selon MIN1–MIN6 ; aucun lien établi sur données réelles.

Durées 30/186/90 jours, ancres et cadences de réexamen conservées ; aucun changement de conservation implicite des nouvelles preuves à définir. Autres paramètres D2/D3, cible/accès/visibilité/restitution et reclassement éventuel ouverts. Validation technique documentaire 1.1 acquise, case non cochée ; 1.2 demeure OUVERTE, dix cases inchangées. Bornes d’inspection 1 s / 5 s / 15 s sans réessai conservées, inspection/maquettes NON EXÉCUTÉES. Aucun accès à la base, secret lu, implémentation, test produit ou réalisation 2.x/3.x. Tout nouveau contrat persistant ou comportement normatif éventuel à examiner avant réalisation ; aucun delta nouveau établi par cette consignation.

## C10-HISTORIQUE-LIENS-R1 — sources et contrôles historiques

Décision explicitement validée par le développeur pour les quatre écritures documentaires C10 seulement, sans accès à la base, lecture de secrets, implémentation ou coche. Sources, contrôles et HIST1–HIST6 adoptés ; preuves historiques réellement disponibles et mécanismes non arrêtés restent OUVERTS. Ce complément porte notamment sur l’attribution historique via identité selon RAP2, pas sur une autorisation de minimisation.

### Constats de sources et sources candidates

[link_identity](../../../src/pixs/core/services_identity.py) crée un lien avec version calculée pour le couple utilisateur–identité ; unlink_identity transforme le lien actif en SOFT_DELETED et incrémente sa version. Le [chemin transactionnel](../../../src/pixs/core/services_transactions.py) prévoit résultat idempotent, audit et outbox, avec réconciliation d’issue incertaine. Les mécanismes sont présents dans les sources, sans disponibilité historique réelle observée.

| Source candidate | Apport possible | Limite à préserver |
|---|---|---|
| CoreIdentityLink conservés, actifs/supprimés | Couple, état, version et horodatages propriétaires : [modèle](../../../src/pixs/core/persistence/models_identity.py). | État courant distinct de toutes les transitions passées ; versions non globales entre couples différents. |
| Résultat propriétaire confirmé / idempotence Core | Opération, référence de lien, version et état résultant sous contrat consommé : [enregistrement](../../../src/pixs/core/api_core_idempotency_record.py), [ports](../../../src/pixs/core/ports.py). | Résultat préparé, IN_PROGRESS ou empreinte de commande ne prouvent pas l’effet committé. |
| Audit C05 | Action, acteur, référence composite, contexte et corrélation : [contrats](../../../src/pixs/core/audit_contracts.py). | ALLOW/ALLOWED seuls insuffisants ; audit pouvant être absent sous dérogation canonique. |
| Outbox / preuves propriétaires C09 | Références, causalité et liaison à l’unité propriétaire : [participant outbox](../../../src/pixs/core/c09_outbox_participant.py), [participant propriétaire](../../../src/pixs/core/c09_owner_participant.py). | Publication/livraison/consommation distinctes du commit métier ; aucune datation automatique de prise d’effet. |
| Sauvegarde ou instantané identifié | État de lien dans un état conservé et daté, sous le contrat propriétaire de reprise applicable. | Ni transitions intermédiaires ni absence de changement ultérieur démontrées par l’instantané seul ; aucun instantané disponible présumé. |
| Preuve historique fournie par Core | Synthèse vérifiée des faits précédents, avec provenance, portée temporelle et limites. | Interface à définir, pas une source exhaustive existante présumée. |

Privilégier une preuve fournie ou validée par Core à partir des faits vérifiables. Examiner le besoin d’un nouveau journal seulement si les sources existantes ne suffisent pas ; aucun nouveau journal, table, format public ou service choisi par cette décision.

### Contrôles de la preuve

| Contrôle | Critère documentaire adopté |
|---|---|
| Identité exacte | Références canoniques et couple vérifiés ; aucun rapprochement par nom, sous-chaîne ou UUID sous un autre préfixe. |
| Provenance | Propriétaire, déploiement/base logique, version de contrat et référence de preuve identifiés. |
| Effet confirmé | Distinguer demande, autorisation, stage, commit confirmé et issue inconnue ; propriétaire responsable de résoudre l’inconnu. |
| Versions | Cohérence du couple concerné ; aucune comparaison naïve entre versions de couples différents. |
| Temporalité | Période ou ordre causal pertinent établi ; created_at/updated_at/instant d’audit non assimilés à date certaine de commit. |
| Rejeu | Regrouper les traces d’une même exécution confirmée ; restitution idempotente distincte d’une nouvelle liaison. |
| Complétude | Examiner liaisons/déliages, rattachements ultérieurs, visibilité des sources, expirations, occultations et historiques manquants. |
| Contradictions | Ne pas arbitrer automatiquement entre sources divergentes ; conserver le conflit et demander résolution propriétaire. |

L’événement à attribuer doit lui-même avoir un moment pertinent défini par son contrat : autorisation, exécution ou autre étape concernée. Proximité des horodatages insuffisante. Si une source ne prouve qu’un ordre causal ou des bornes, ne pas inventer un instant exact ni une période entièrement déterminée.

### Preuve minimale propriétaire proposée

Pour un rapprochement : utilisateur/identité dans le périmètre privé autorisé ; transitions et résultats confirmés retenus ; versions et références des preuves ; bornes temporelles ou ordre causal réellement établis ; visibilité/complétude ; inconnues, contradictions ou pertes ; conclusion limitée à la période démontrée. Cette grille reste documentaire, interface propriétaire à définir ; aucune donnée individuelle d’instance collectée ou transmise à l’agent.

Restitution conversation agrégée sans UUID ni contenu individuel. Les références internes de preuve, identités et relations détaillées restent chez les propriétaires selon accès à arrêter ; aucune publication de ces faits pour démontrer une sélection.

### Décisions HIST1–HIST6

| Décision | Règle adoptée | Limite |
|---|---|---|
| HIST1 — autorité | Core fournit ou valide la preuve historique ; autres sources comme corroborations bornées. | Aucune source exhaustive déclarée disponible sans constat. |
| HIST2 — commit | Attribution historique sur faits d’effet confirmé. | Autorisation, stage ou livraison seuls insuffisants ; issues inconnues à résoudre. |
| HIST3 — temps | Bornes ou relations causales démontrées seulement. | Temporalité insuffisante : Non vérifiable ; aucune date inventée. |
| HIST4 — rejeu | Une opération confirmée restituée reste une transition malgré plusieurs traces d’audit. | Déduplication contractuelle à définir ; pas de nouvelle liaison déduite du nombre d’événements. |
| HIST5 — couverture | Historique incomplet, expiré ou occulté explicitement signalé. | Absence de trace distincte d’absence de lien. |
| HIST6 — conflit/conservation | Conflit non résolu : Conflictuel ; conservation et minimisation des preuves historiques séparément définies. | Aucune durée ou résolution arbitraire de conflit. |

### Points ouverts et statuts

Restent OUVERTS : interface propriétaire de preuve, faits réellement disponibles, précision temporelle, exhaustivité, règle de déduplication contractuelle, traitement des conflits et durée de conservation des preuves. Les durées 30/186/90 jours ne s’étendent pas automatiquement à une nouvelle source historique. Autres décisions RAP1–RAP6, MIN1–MIN6 et DUR1–DUR6 conservées dans leurs portées, sans traitement réel ou mécanisme de pseudonymisation réalisé.

Validation technique documentaire 1.1 acquise, case non cochée ; 1.2 demeure OUVERTE, dix cases inchangées. Paramètres D2/D3, cible/accès/visibilité/restitution et reclassement éventuel ouverts ; inspection/maquettes NON EXÉCUTÉES, bornes 1 s / 5 s / 15 s sans réessai conservées. Aucun accès à la base, lecture de secrets, implémentation, recette produit ou réalisation 2.x/3.x. Tout comportement normatif ou contrat persistant nouveau éventuel à examiner pour son delta préalable ; aucun delta créé par cette consignation.

## C10-1.2-PUBLICATION-CADRE-R2 — cadrage checklist, sans levée de barrière

Cadrage seul de la barrière 2, sans publication effective, sans configuration effective, sans implémentation ni coche. Q1.4-GOV-SOURCE et Q1.4-C10-PUBLISH acquis, non modifiés, selon [Contrat minimal 1.4](../add-installation-and-first-configuration/design.md#contrat-minimal-14--catalogue-local-protégé-hors-base-à-ouvrir-choix-validé) et [Proposition Q1.4-C10-PUBLISH](../add-installation-and-first-configuration/design.md#proposition-q14-c10-publish--autorisation-distincte-de-publication). CH1–CH6 et 30/186/90 rappelés acquis, non redécidés.

| Source existante | Condition acquise | Élément ouvert | Preuve future, sans valeur inventée |
|---|---|---|---|
| C08 design Contrat 1.4 + catalogue `c10_catalog.py` | Catalogue TOML protégé hors base, raccord minimal C10 | Chemin/ancrage/propriétaire/validités/refs politique de publication | Config protégée présentée et relecture effective, sans valeur prod inventée |
| C08 design Q1.4-C10-PUBLISH `pixs.c10.catalog.publish.v1` | Mandat privé distinct R01/PA, journal pré-base + relais C05 requis | Autorité effective, garde exclusive, procédure opérateur, versions/empreintes publication, fraîcheur | Mandat/éditeur/journal/relais qualifiés sur faits courants, sans UID/GID/format/API/quorum/fraîcheur inventés |
| CP-01/CP-08, R-01/R-08 | Attestation/stage/verify, profils propriétaires | Liaisons consommateurs, profils techniques audit/reçus | Refus absence/divergence conservés, revalidation démontrée en réalisation |

Portée : checklist de cadrage. Aucune levée de barrière 2, aucune autorisation de publier, aucune config effective.
