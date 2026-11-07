# C10 — Gouvernance et cycle de vie effectifs

État courant : le développeur valide techniquement 1.1 sur sa portée documentaire ; sa case reste non cochée sur instruction explicite. 1.2 reste OUVERTE avec ses barrières. La [validation technique documentaire](design.md#validation-technique-documentaire-de-la-tâche-11) précise cette décision ; les mentions antérieures d’absence de validation complète ou de tâches ouvertes décrivent leurs états historiques, sans annuler cet acquis ni valoir qualification produit.

## Pourquoi

Profils de gouvernance, vocabulaires de rétention et tombstone-v1 sont déclaratifs ; ils ne prouvent ni purge ni propagation durable.

La réconciliation documentaire du 26 octobre 2026 constate également des sources de raccord initial C10 écrites dans le périmètre C08 : catalogue protégé, attestation et reçus transactionnels, ponts de classification Auth et gouvernance des modes. Leur présence ne démontre pas la livraison de C10 ni leur qualification intégrée. L'inventaire, les décisions déjà adoptées et les limites sont distingués dans [design.md](design.md#réconciliation-documentaire-du-26-octobre-2026).

## Modifications proposées

Publier les profils des données réellement livrées ; appliquer classification, demandes d’accès/export/rectification/effacement/restriction, rétention, holds, suppression logique et purge explicite avec tombstones durables. Pas de dépendance implicite au Bulk optionnel pour les demandes exigées.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions du profil C00 adoptées le 18 octobre 2026 et intégrées au canon.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `add-core-postgres-services`.
- `integrate-runtime-authorization-and-super-admin`.
- `add-durable-minimized-audit`.
- `add-reference-worker-scheduler-and-event-delivery`.

Les contrats archivés C03, C06 et C14 et les relations avec les changes actifs C08, C16 et N05 sont explicités dans la [matrice des contrats propriétaires](design.md#matrice-des-contrats-propriétaires). Cette cartographie décrit les raccordements nécessaires aux tâches existantes ; elle ne sélectionne aucune capacité optionnelle et ne crée pas de dépendance circulaire de réalisation entre C08 et C10.

## Impact

Périmètre de réalisation futur : Déclarer les profils des données effectivement persistées de Core, Auth, backend d’installation, audit/jobs, Agent, PZT et DNS, et appliquer les politiques dans leurs services propriétaires. Seuls les dérivés réellement présents sont inventoriés ; aucune sélection d’exécutant ou de provider supplémentaire n’en découle. Demandes d’accès/export/rectification/effacement/restriction et purge restent des Commands autorisées, auditées et idempotentes. Les dérivés présents et les sauvegardes C16 réappliquent tombstones et holds ; pas de dépendance implicite au service Bulk complet.

La validation du 26 octobre 2026 autorise uniquement la réconciliation des quatre documents de ce dossier et la matrice des contrats propriétaires, avec correction du lien C09 et des empreintes. Aucun code, test applicatif, migration, dépendance, configuration runtime, Git, déploiement, publication ou archive n'est modifié ou exécuté par cette réconciliation. Les sources partielles préexistantes sont inventoriées sans validation de tâche ni lancement d'une réalisation supplémentaire.

## Critères de sortie de réalisation future

Donnée non classifiée non exposée ; purge ordinaire prématurée refusée ; demande rejouée sans double effet ; dérivés réellement présents traités ; tombstone préservé à la restauration ; exception Super Admin conforme et distincte des structures.

## Barrière de conception

Rétentions, droits de demandes, contrats des dérivés et procédure de purge à revoir ; valeurs existantes du canon conservées et exception Super Admin distincte des profils purs.

## C10-CONCEPTION-R1 — décision du 28 octobre 2026

Le développeur valide D1 et les orientations D2/D3 ainsi que les quatre écritures documentaires C10, sans implémentation ni coche de tâche. Cette validation ne clôture pas 1.1/1.2 et conserve leurs paramètres non arrêtés comme décisions ouvertes.

D1 complète le périmètre par les données effectivement persistées de pixs.agent. D2 conserve les politiques explicites versionnées et les contrôles propriétaires C04/C05/C06. D3 exige des faits durables d’effacement et de restriction postérieurs au snapshot ; C10 fournit les faits, C16 restaure et N05 coordonne la réadmission. Le mécanisme et le propriétaire restent ouverts ; aucun journal externe n’est sélectionné.

Voir le [registre des décisions](design.md#c10-conception-r1--revue-du-28-octobre-2026) et la [couverture exhaustive du canon](requirements.md#c10-conception-r1--couverture-exhaustive-du-canon). Q1.4-GOV-SOURCE et Q1.4-C10-PUBLISH restent acquis. Aucun delta normatif nouveau établi ; toute évolution normative démontrée nécessite un delta présenté et approuvé avant réalisation.

## C10-CONCEPTION-R2 — inventaire D1 et unité users/PLATFORM

Le développeur valide l’inventaire D1, l’unité users/PLATFORM et les orientations D2 présentées après R1. La validation autorise leur consignation dans les quatre documents C10, sans implémentation ni coche de tâche. Les paramètres non arrêtés restent ouverts.

L’[inventaire D1 vérifié](design.md#c10-conception-r2--inventaire-d1-et-unité-usersplatform) recense 68 modèles Django concrets et les ressources durables hors SQL identifiées dans les six domaines examinés. Il distingue consommateurs observés dans le code et consommateurs effectivement autorisés. Les 13 modèles Bulk présents ne sélectionnent pas cette capacité.

La première unité retenue prépare le raccord de gouvernance de CoreUser via la collection users, le contexte PLATFORM et l’action existante pixs.core.identity.read. Le chemin Core de lecture et ses contrôles sont réutilisés, sans changement de format des références. La classification CONFIDENTIAL/PERSONAL et les orientations D2 sont adoptées pour cette unité. La lecture métier peut produire des écritures techniques d’audit et de reçus ; elle ne réalise ni mutation métier, ni demande ACCESS complète, ni export.

Cette édition ne lance pas l’unité. Les références réelles du profil et des consommateurs, les politiques et la configuration protégée restent à arrêter avant réalisation dépendante. D3 reste ouvert pour purge/restauration/réadmission ; aucune nouvelle source d’effacements n’est réalisée pour ce seul raccord de lecture et aucune garantie post-restauration n’en est déduite.

## D2-USERS-R1 — adoption documentaire du 28 octobre 2026

Le développeur valide D2-USERS-R1 pour l’unité users/PLATFORM et autorise sa consignation dans les quatre documents C10, sans implémentation ni coche de tâche. Les références du profil et des deux consommateurs serveur, la finalité et les politiques sont désormais adoptées documentairement, selon le [registre détaillé](design.md#d2-users-r1--profil-consommateurs-et-politiques).

Le profil proposé devient le choix documentaire pixs.core.governance.users.platform.read.v1, version 1.0.0, pour pixs.core.data.users sous propriété pixs.core. Cette adoption n’est ni une publication de catalogue, ni une configuration effective, ni une autorisation d’accès. Compatibilité avec les governance_ref existants, liaisons effectives des consommateurs et destinataire HTTP final restent à établir avant leur consommation réelle.

Les durées et critères de rétention, emplacements, versions et empreintes de publication, autorités, bornes de fraîcheur et configuration protégée restent ouverts. Les profils et politiques de l’audit et des reçus restent distincts du profil utilisateur. D3 reste ouvert pour restauration/réadmission ; aucune mise à jour massive des classifications ni qualification de fonctionnement n’est déduite de cette adoption.

## D2-USERS-COMPAT-R1 — décisions de compatibilité

Le développeur valide C1–C5 et leur consignation dans les quatre documents C10, sans implémentation ni coche. Le [registre de compatibilité](design.md#d2-users-compat-r1--compatibilité-des-classifications) conserve pixs.core.data.users et le triplet cible CONFIDENTIAL/PERSONAL pour la lecture ordinaire, sans alias ni conversion implicite.

Les lignes compatibles seraient réutilisées sans modification, sous les autres contrôles requis. Les classifications différentes ou absentes sont conservées avec le refus ordinaire existant ; la présence de NULL ne vaut pas corruption par défaut. La cohérence des producteurs futurs doit être examinée séparément du raccord de lecture. Tout reclassement éventuel nécessite son périmètre propriétaire et une autorisation distincte.

Compatibilité contractuelle possible ne signifie pas compatibilité des données existantes démontrée. L’inspection propriétaire agrégée des données et la nécessité d’un reclassement restent OUVERTES ; aucune inspection de base, modification de classification ou migration n’est engagée par cette consignation. Les autres paramètres D2 et D3 demeurent ouverts selon leurs phases.

## C10-INSPECTION-R1 — plan documentaire adopté

Le développeur valide C10-INSPECTION-R1 et ses bornes : attente de verrou 1 seconde, instruction 5 secondes, abandon de l’opération complète après 15 secondes, sans réessai automatique. Il autorise uniquement la consignation du plan dans les quatre documents C10, sans accès à la base, implémentation ni coche de tâche.

L’[inspection agrégée CoreUser](design.md#c10-inspection-r1--plan-dinspection-agrégée) est prévue en transaction PostgreSQL READ ONLY / REPEATABLE READ, avec catégories CIBLE/ABSENT/AUTRE par champ et ventilation par état de persistance. Base, environnement, schéma, rôle, mécanisme d’accès et preuve de visibilité restent OUVERTS. Le serveur déclaré dans DEVOPS constitue un candidat, pas une cible vérifiée ou une autorisation de connexion.

Le plan ne réalise ni inspection ni qualification de compatibilité. Le besoin et l’autorisation propre d’un éventuel reclassement restent ouverts. Aucun secret, UUID utilisateur ou ancienne référence personnalisée n’est à restituer ; un résultat incomplet ou interrompu ne devient pas une preuve de compatibilité.

## C10-INSPECTION-CIBLE-R1 — adoption documentaire

Le développeur valide C10-INSPECTION-CIBLE-R1 et sa consignation dans les quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Le [cadrage de cible et d’accès](design.md#c10-inspection-cible-r1--cible-et-accès) distingue les éléments déclarés des informations non secrètes encore manquantes ; aucune valeur manquante n’est inventée.

L’exécution future par un opérateur autorisé utilisant un accès existant est la voie recommandée adoptée documentairement. Une éventuelle exécution par l’agent nécessiterait un mécanisme existant préservant les secrets, non établi à ce stade. Les informations de cible, accès, visibilité et restitution restent OUVERTES. Aucune autorisation de connexion ou de lecture de project.env ne découle de cette validation. C10-INSPECTION-R1 et les bornes 1 s / 5 s / 15 s sans réessai restent acquis.

## C10-INSPECTION-VISIBILITE-R1 — adoption documentaire

Le développeur valide C10-INSPECTION-VISIBILITE-R1 pour consignation dans les quatre documents C10 uniquement, sans accès à la base, lecture de secrets, implémentation ni coche. Le [protocole de preuve de visibilité](design.md#c10-inspection-visibilite-r1--preuve-de-visibilité) porte sur la relation exacte et le rôle effectif de la future session d’inspection ; il reste distinct des agrégats et du verdict de classification.

Les contrôles d’identité de relation, rôle, droits effectifs, contexte, RLS et stabilité sont adoptés documentairement. Sans preuve de visibilité complète, un agrégat compatible sur les seules lignes visibles ne vaut pas compatibilité globale. Cible, accès, opérateur, politiques effectivement appliquées et preuves restent OUVERTS. Aucune exemption, élévation ou modification de rôle/RLS n’est autorisée par cette décision. Les bornes 1 s / 5 s / 15 s et l’absence de réessai sont conservées.

## C10-INSPECTION-RAPPORT-R1 — adoption du format

Le développeur valide la consignation du format de rapport dans les seuls quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Le [format adopté](design.md#c10-inspection-rapport-r1--format-du-rapport) sépare exécution, visibilité, cohérence des agrégats et compatibilité ; aucun champ n’est prérempli avec un résultat supposé.

Les six parties sont identification/portée, preuve de visibilité, agrégats, contrôles de cohérence, verdicts et limites/suites. Inspection actuelle NON EXÉCUTÉE ; aucune donnée ni preuve de visibilité disponible. Cible, accès, visibilité effective, restitution et autres paramètres D2/D3 restent ouverts. Le format ne crée pas un rapport de résultats, n’autorise aucune inspection ou reclassement et ne qualifie pas users/PLATFORM. Les bornes 1 s / 5 s / 15 s sans réessai sont conservées.

## C10-INSPECTION-ACCEPTATION-R1 — adoption documentaire

Le développeur valide les critères d’acceptation du rapport et leur consignation dans les quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. La [grille A01–A16](design.md#c10-inspection-acceptation-r1--critères-du-rapport) distingue recevabilité du rapport et caractère concluant de l’inspection : un rapport décrivant correctement un échec ou une visibilité partielle peut être recevable, sans devenir une réussite d’inspection.

Les cas nominaux, partiels, non concluants et contrôles du rapport, ainsi que la priorité des verdicts, sont adoptés documentairement. Aucun cas n’est déclaré exécuté. Inspection actuelle NON EXÉCUTÉE ; cible, accès, visibilité, restitution, données effectives et paramètres D2/D3 restent ouverts. Les bornes 1 s / 5 s / 15 s sans réessai sont conservées. Aucun rapport de résultats créé, reclassement autorisé ou raccord qualifié par cette consignation.

## C10-INSPECTION-SYNTHETIQUES-R1 — adoption documentaire

Le développeur valide la consignation des [maquettes SYNTH-A01 à SYNTH-A16](design.md#c10-inspection-synthetiques-r1--maquettes-documentaires) dans les seuls quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Leurs nombres et preuves sont entièrement fictifs ; les verdicts sont attendus sous les hypothèses de chaque cas, pas observés sur Pixs.

Les maquettes reprennent les six parties du format et distinguent recevabilité documentaire, verdict attendu et limites de conclusion. Elles ne créent ni rapport de résultats, ni fichiers de tests, ni preuve d’exécution A01–A16. L’inspection réelle reste NON EXÉCUTÉE, les informations de cible/accès/visibilité/restitution et paramètres D2/D3 non arrêtés restent ouverts ; aucun reclassement autorisé ou raccord qualifié. Les dix cases et bornes 1 s / 5 s / 15 s sans réessai sont conservées.

## C10-INSPECTION-SYNTHETIQUES-REVUE-R1 — corrections documentaires

Le développeur valide les corrections des maquettes dans les quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Les [compléments par cas](design.md#c10-inspection-synthetiques-revue-r1--maquettes-complétées) explicitent six parties, métadonnées et preuves fictives, états simulés et recevabilité ; nombres déjà adoptés conservés. A12 distingue somme correcte et agrégats NON VÉRIFIÉS faute de contextes raccordables.

Les ventilations manquantes et variantes A09/A10/A11/A14/A15/A16 sont consignées. Les références et fenêtres temporelles sont entièrement fictives, sans lien avec une base, un rôle ou une inspection réelle. Tous les cas restent NON EXÉCUTÉS réellement ; cible, accès, preuves, restitution et paramètres D2/D3 restent ouverts, aucune réalisation ou coche.

## Corrections finales des variantes A14 et A15 négatives

Le développeur valide ces deux corrections dans les quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Les [substitutions finales](design.md#corrections-finales-des-variantes-a14-et-a15-négatives) retirent les hypothèses positives incompatibles : interruption explicite en A14 négative ; preuve de désactivation RLS retirée et RLS applicable avec portée non établie en A15 négative. Les candidats erronés restent non recevables, sans verdict global accepté.

Nombres et cas positifs conservés. Toutes les maquettes restent fictives et NON EXÉCUTÉES ; cible, accès, preuves, restitution, paramètres D2/D3 et reclassement éventuel ouverts. Les dix cases et bornes 1 s / 5 s / 15 s sans réessai sont inchangées ; aucune qualification du raccord ou des données réelles.

## Revue finale validée des maquettes A01–A16

Le développeur valide la revue finale après correction d’A14/A15 négatives et autorise sa consignation dans les quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. La [conclusion de revue](design.md#revue-finale-validée-des-maquettes-a01a16) constate la conformité documentaire des seize maquettes et de leurs variantes aux critères examinés ; aucune correction supplémentaire nécessaire identifiée dans ce périmètre.

Cette revue documentaire est achevée et validée ; aucune maquette, inspection ou recette produit n’est exécutée. Les dix tâches, dont 1.1/1.2, restent ouvertes. Cible, accès, preuves de visibilité, restitution, données réelles, paramètres D2/D3 et reclassement éventuel restent ouverts. Aucun raccord users/PLATFORM, producteur ou restauration qualifié, aucune opération réelle autorisée par cette conclusion.

## C10-CLOTURE-CONCEPTION-R1 — conditions de clôture documentaire

Le développeur valide la consignation du plan de clôture des tâches 1.1/1.2 dans les seuls quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Les [conditions distinctes de clôture](design.md#c10-cloture-conception-r1--acquis-et-barrières) séparent bilan de revue de conception, décisions restantes et qualification future. Cette validation du plan ne clôture aucune tâche.

Pour 1.1, préparer un bilan consolidé R-01 à R-08 reliant canon/C00, contrats, sources, preuves réutilisables ou limitées aux fixtures, décisions et inconnues ; le soumettre à validation documentaire explicite. Pour 1.2, la validation préalable de 1.1 et la levée des choix obligatoires pour l’exécution dépendante restent nécessaires. Les acquis users/PLATFORM ne réduisent pas implicitement la portée globale de C10.

La qualification des raccords et des données n’est pas la preuve que la revue documentaire a été faite ; inversement une inconnue consignée ne vaut pas prérequis satisfait. Les dix tâches restent ouvertes. Cible/accès/visibilité/restitution, paramètres D2/D3 et reclassement éventuel restent ouverts selon leur phase ; aucun lancement de réalisation ou inspection.

## C10-BILAN-1.1-R1 — bilan documentaire validé

Le développeur valide le bilan consolidé 1.1 et sa consignation dans les seuls quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Le [bilan par objectif R-01–R-08](design.md#c10-bilan-11-r1--rapprochement-consolidé) rapproche acquis, canon/C00, contrats et sources actuelles, preuves historiques et dépendances non vérifiées.

La validation porte sur la revue documentaire et sa traçabilité, pas sur la satisfaction des prérequis de réalisation. Le bilan n’est plus à préparer ou à faire valider documentairement ; les dix tâches restent toutefois ouvertes, sans clôture automatique de 1.1 ni levée des barrières de 1.2. users/PLATFORM reste une unité de lecture bornée, sans réduction implicite du périmètre global C10. Aucune inspection ni qualification réelle déduite des sources, archives ou maquettes.

## Validation technique documentaire de la tâche 1.1

Le développeur valide explicitement et techniquement 1.1 sur sa portée de revue documentaire, à l’issue du bilan consolidé et de sa revue finale. Il autorise uniquement la consignation dans les quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Cette validation de tâche est distincte de la seule adoption antérieure du bilan.

Acquis : revue et traçabilité R-01–R-08, canon/C00, contrats propriétaires, sources et limites des preuves. La case 1.1 demeure non cochée sur instruction expresse. 1.2 reste ouverte ; ses sept barrières, les paramètres D2/D3 et dépendances non vérifiées sont conservés. Aucun lancement 2.x/3.x ni autorisation d’implémentation ; la validation documentaire n’établit pas la disponibilité des raccords, les classifications persistées ou la qualification de users/PLATFORM.

## C10-POLITIQUES-OPERATIONNELLES-R1 — adoption documentaire

Le développeur valide les politiques proposées pour utilisateurs, audit et reçus de users/PLATFORM et leur consignation dans les quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Les [règles et décisions P1–P6](design.md#c10-politiques-operationnelles-r1--utilisateurs-audit-et-reçus) sont adoptées documentairement, sans publication ni configuration effective.

Les références utilisateurs acquises sont conservées. Politique d’audit proposée désormais adoptée documentairement : pixs.core.audit.users.platform.v1, version 1.0.0 ; références des reçus : pixs.backend.retention.c10.receipts.v1 et pixs.backend.deletion.c10.receipts.v1. Ces noms ne prouvent aucune capacité de purge : les reçus sont actuellement immuables dans le mécanisme de migration examiné.

Durées, événements de départ, classifications techniques, autorités, consommateurs techniques, limites d’audit et mécanisme de fin de conservation des reçus restent OUVERTS selon le détail du design. 1.1 demeure validée techniquement sur sa portée documentaire, case non cochée ; 1.2 reste ouverte, sa barrière de politiques n’est pas entièrement levée. Aucun nouveau défaut de production, conservation illimitée, opération de maintenance ou implémentation autorisés par cette consignation.

## C10-CONSERVATION-R1 — adoption des règles de conservation

Le développeur valide C10-CONSERVATION-R1 pour consignation dans les seuls quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Les [événements de départ et DUR1–DUR6](design.md#c10-conservation-r1--événements-durées-et-maintenance) sont adoptés documentairement ; les durées chiffrées, preuves d’ancrage et paramètres non arrêtés restent ouverts.

La conservation distingue source utilisateur active, période après suppression logique, audit depuis created_at et reçus après clôture durable réconciliée de l’opération. Les lectures ne remettent pas les compteurs à zéro. Une échéance atteinte n’est pas un ordre de purge et aucun mécanisme nouveau de suppression n’est fourni par ces règles.

La validation technique documentaire 1.1 reste acquise, case non cochée ; 1.2 reste ouverte. Contrats d’ancrage, rétention chiffrée et fin de conservation compatible avec l’immutabilité des reçus restent à arrêter avant réalisation dépendante. Aucune conservation illimitée, migration, réduction rétroactive ou qualification de données réelles déduite de cette consignation.

## C10-DUREES-R1 — valeurs initiales adoptées documentairement

Le développeur valide les valeurs et CH1–CH6, pour consignation dans les seuls quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Les [valeurs et conditions](design.md#c10-durees-r1--valeurs-justifications-et-décisions) sont désormais choisies documentairement pour le périmètre C10 proposé : 30 jours après suppression logique utilisateur durable/confirmée, 186 jours d’audit depuis created_at, 90 jours pour reçus après clôture durable réconciliée. Réexamen de finalité des utilisateurs actifs/archivés tous les 90 jours, distinct d’une expiration automatique.

Ces valeurs actualisent les mentions antérieures de durées chiffrées non choisies, sans publier ni appliquer une politique. Déploiement applicable, responsables, contrats d’ancrage, minimisation et mécanismes de maintenance restent OUVERTS. CH6 prévoit une réévaluation après les 90 premiers jours d’exploitation effective ou plus tôt si les conditions changent, sans modification automatique.

1.1 conserve sa validation technique documentaire et sa case non cochée ; 1.2 reste ouverte. Aucune rétroactivité implicite, purge, scheduler ou conservation illimitée autorisés par l’adoption des nombres. Les dépendances et exceptions canoniques sont conservées ; aucune qualification de données ou raccord réelle.

## C10-MINIMISATION-R1 — adoption documentaire

Le développeur valide la consignation des champs et décisions MIN1–MIN6 dans les seuls quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. La [minimisation ciblée](design.md#c10-minimisation-r1--audits-et-reçus-après-suppression) distingue suppression logique, décision propriétaire d’effacement/minimisation et preuves encore nécessaires. Aucune réécriture automatique des audits ou reçus d’un utilisateur supprimé.

Les audits utilisent uniquement la maintenance propriétaire C05 et ses cibles d’occultation admises ; le rapprochement des personnes/enregistrements, la nécessité résiduelle et le mécanisme de pseudonymisation restent ouverts. Les reçus existants restent immuables : minimiser leur restitution n’altère pas l’original et ne remplace ni sa preuve d’intégrité ni sa conservation sous-jacente. Provenance C01 examinée séparément.

Durées 30/186/90 jours et ancres conservées sans remise à zéro ni purge automatique. Validation technique documentaire de 1.1 acquise, case non cochée ; 1.2 ouverte avec mécanismes et autres paramètres D2/D3 non arrêtés. Aucune minimisation effective, anonymisation complète, publication ou qualification produit déclarée.

## C10-RAPPROCHEMENT-R1 — adoption documentaire

Le développeur valide C10-RAPPROCHEMENT-R1 pour consignation dans les seuls quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Les [critères et RAP1–RAP6](design.md#c10-rapprochement-r1--sélection-et-preuves-propriétaires) distinguent utilisateur acteur, cible ou participant composite ; rapprochement exact, preuve historique d’identité et chaîne propriétaire des reçus sont adoptés documentairement. Un lien établi ouvre l’examen de minimisation, sans autoriser une transformation.

Une corrélation ou proximité seule reste insuffisante ; lien courant distinct d’un rattachement historique, sélection incomplète distincte d’absence de lien. Interfaces de preuve, historique disponible, conflits, conservation des preuves et exhaustivité restent OUVERTS. Aucun mécanisme ou enregistrement rapproché réellement. Durées 30/186/90 jours et MIN1–MIN6 conservées ; validation technique documentaire 1.1 acquise et 1.2 ouverte, dix cases non cochées.

## C10-HISTORIQUE-LIENS-R1 — adoption documentaire

Le développeur valide les sources candidates, contrôles et HIST1–HIST6 pour consignation dans les seuls quatre documents C10, sans accès à la base, lecture de secrets, implémentation ni coche. Le [contrat documentaire de preuve historique](design.md#c10-historique-liens-r1--sources-et-contrôles-historiques) privilégie des faits fournis ou validés par Core ; état courant, audit isolé ou proximité temporelle ne valent pas historique complet.

Sources existantes à confronter : liens conservés, résultats propriétaires confirmés/idempotence, audit C05, outbox/preuves C09 et instantanés identifiés. Aucune disponibilité historique réellement observée ; aucune source exhaustive ou nouvelle journalisation choisie implicitement. Interfaces, faits disponibles, précision temporelle, exhaustivité, déduplication, conflits et conservation restent OUVERTS.

1.1 conserve sa validation technique documentaire, case non cochée ; 1.2 ouverte avec ses dépendances non vérifiées. Durées 30/186/90 jours et principes de rapprochement/minimisation conservés, sans extension automatique à une nouvelle source historique. Aucun lien d’instance établi ni traitement de données autorisé par cette consignation.
