# Tâches — Z12

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Maintien ciblé des unités — ACL-PIXS-2026-10-31-E3-R1

Périmètre courant : PKIZT et même clé d’autorité chiffrée répliquée, droits séparés, émetteur unique et confiance d’amorçage distincte retirée après bascule vérifiée.

Les tâches, libellés, cases et sous-lots existants sont conservés. Lorsque leur texte mentionne une orientation remplacée, il reste un repère historique ; la réalisation future suit la cible courante indiquée ci-dessus et ses scénarios. Une ancienne case cochée n'est pas une validation de cette nouvelle version. Chaque unité future vérifie ses contrats, nominal/refus, persistance, autorisation et reprise nécessaires avant sa propre validation ; aucun test produit n'est exécuté par ce maintien.

Sources : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md).

| Unité existante | Correspondance | Critères à relier lors de la réalisation future |
|---|---|---|
| Z12-SL01 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z12, sans nouvelle qualification de la case historique |
| Z12-SL02 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z12, sans nouvelle qualification de la case historique |
| Z12-SL03 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z12, sans nouvelle qualification de la case historique |
| Z12-SL04 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z12, sans nouvelle qualification de la case historique |
| Z12-SL05 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z12, sans nouvelle qualification de la case historique |
| Z12-SL06 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z12, sans nouvelle qualification de la case historique |
| Z12-SL07 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z12, sans nouvelle qualification de la case historique |
| Z12-SL08 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z12, sans nouvelle qualification de la case historique |
| Z12-SL09 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z12, sans nouvelle qualification de la case historique |
| Z12-SL10 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z12, sans nouvelle qualification de la case historique |

La liste ci-dessus n'est pas une nouvelle séquence : les anciens rattachements aux tâches et alias restent ceux des sections conservées. Aucun identifiant n'est attribué à une unité historique absente ou ambiguë.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Les tâches 1–2 restent historiquement validées. Les tâches 3–4 avaient été validées sur le périmètre ordinaire D1/D2/D3 ; l’extension D4/D5/D6 de première installation avant PostgreSQL impose leur réexamen et leurs cases sont rouvertes. Les preuves des réalisations déjà effectuées sont conservées, sans validation de l’extension. La tâche 5 reste non validée ; aucune tâche nouvelle n’est cochée.

- [x] 1. Auditer les blocs normatifs et renvois de requirements.md, l’implémentation actuelle et ses preuves ; décider du complément réellement manquant sans recréer l’existant.
- [x] 2. Confirmer la sélection de la capacité, les rôles/plateformes/ressources applicables et les dépendances obligatoires ; ne pas transformer une non-sélection en réussite de test.
- [ ] 3. Lever les barrières de conception de design.md et faire valider les choix encore ouverts avant réalisation ; présenter tout delta normatif ou dépendance supplémentaire nécessaire.
- [ ] 4. Définir les contrats, schémas, propriétaires et adapters du périmètre : A10i6–A10i20 : PKI dédiée, intermédiaires, protection des clés, secours, exclusion/bascule, algorithmes et successions racine.
- [ ] 5. Réaliser le complément ciblé et son branchement aux dépendances, en conservant les structures déjà livrées.
- [ ] 6. Traiter les échecs, concurrence, limites et interruptions propres au lot ; états incertains explicités et reprise sous autorité/contexte courants.
- [ ] 7. Exécuter syntaxe, contrôles configurés et unités/négatifs applicables, en rapportant les résultats natifs sans données sensibles.
- [ ] 8. Exécuter les intégrations/conformités du profil : Bornes exactes et juste au-delà, types/champs étrangers, rôle/contexte/mandat inadmissibles, échéance/révocation, concurrence, réponse perdue, crash/reprise, état ancien et ressources réellement libérées. Mesurer seulement le traitement concerné et ne pas extrapoler ses plafonds au PA/PBO entier.
- [ ] 9. Vérifier la sortie attendue : Signataire exclu avant succession ; perte traitée par nouvelles clés/recertification ; coexistence et durées bornées ; pas de confiance par snapshot.
- [ ] 10. Relier chaque scénario applicable aux preuves/version/artefact, examiner le diff et les limites ; Git, synchronisation, archive, installation et publication restent soumis à leur autorisation propre.

## Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026

Les identifiants et cases ci-dessus sont conservés. Ce contrat précise les critères et contrôles à réaliser **dans chaque tâche**, avant de commencer la suivante. Les tâches de test ou de preuve placées plus loin consolident la couverture et ne reportent jamais les vérifications nécessaires à une tâche antérieure. Une tâche de réalisation comprend donc ses unités, refus et intégrations indispensables dès sa propre exécution ; elle ne peut être validée en attendant qu’une tâche suivante la rende testable.

Les tâches cochées conservent leur statut historique ; leurs preuves doivent être recoupées avant réutilisation si les sources ont changé. Pour les tâches futures, les prérequis externes sont ceux de design.md et des exigences applicables ; un propriétaire, provider, exécutant, contrat adopté ou environnement requis manquant bloque la tâche concernée. La préparation du dossier ne les déclare pas livrés. Les choix ouverts restent à décider avant leur réalisation ; les deltas déjà adoptés ne sont pas réappliqués.

### Périmètre et cas de contrôle propres au lot

- Objet : A10i6–A10i20 : PKI dédiée, intermédiaires, protection des clés, secours, exclusion/bascule, algorithmes et successions racine.
- Résultat de référence : Signataire exclu avant succession ; perte traitée par nouvelles clés/recertification ; coexistence et durées bornées ; pas de confiance par snapshot.
- Cas de contrôle du profil : Bornes exactes et juste au-delà, types/champs étrangers, rôle/contexte/mandat inadmissibles, échéance/révocation, concurrence, réponse perdue, crash/reprise, état ancien et ressources réellement libérées. Mesurer seulement le traitement concerné et ne pas extrapoler ses plafonds au PA/PBO entier.

Chaque contrôle est relié au texte complet de l’exigence et à son scénario, dans requirements.md lorsqu’il existe, sinon dans les deltas et le canon référencés par la proposition. Une simple égalité de titre ne prouve pas la couverture. Les cas conditionnels sont appliqués selon le rôle effectivement sélectionné ; une non-applicabilité est motivée sans remplacer une preuve obligatoire. Aucun paramètre numérique ou provider nouveau n’est déduit de ce contrat.

### Critères et contrôles par tâche future

| Tâche existante | Prérequis immédiat | Critère observable de validation | Contrôles exigés dans cette tâche et preuve |
|---|---|---|---|
| 1 | Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées | Inventaire daté des exigences/scénarios et de l’existant ; écarts réels séparés des réalisations historiques et des inconnues. | Recouper les textes complets, leurs versions et preuves ; vérifier liens et absence de doublon, conserver la liste des écarts. |
| 2 | Tâche 1 techniquement validée avec ses propres preuves | Profil, rôles, cibles, ressources, capacités et dépendances obligatoires explicitement sélectionnés ; aucune absence convertie en réussite. | Vérifier manifests/profil et graphe déclaré contre les contrats ; documenter absence, incompatibilité et non-sélection avant effet. |
| 3 | Tâche 2 techniquement validée avec ses propres preuves | Contrats, propriétaires, choix et paramètres nécessaires à la prochaine réalisation arrêtés ; aucun arbitrage bloquant remplacé par une hypothèse. | Revue de conception et des cas nominaux/refus du profil ; validation documentaire requise et preuve des décisions avant code. |
| 4 | Tâche 3 techniquement validée avec ses propres preuves | Contrats et schémas versionnés du seul objet du lot vérifiables indépendamment de la réalisation suivante ; entrées, sorties, refus, limites et propriétaires explicites. | Si contrats documentaires : revue des invariants et structure ; si représentations exécutables : syntaxe et tests de types/versions/champs/bornes et refus sans effets. Aucun adapter futur ne remplace cette preuve. |
| 5 | Tâche 4 techniquement validée avec ses propres preuves | Chemin nominal du complément et branchement public observés ; refus indispensables de types, contexte, droits et dépendances déjà traités ; résultat réel distingué du reçu. | Exécuter syntaxe, unités et intégrations nécessaires au branchement nominal et à ses refus dans le périmètre du lot ; utiliser le propriétaire réel si persistance ou effet réel est requis. Les tests nécessaires de 7/8 sont effectués dès ici. |
| 6 | Tâche 5 techniquement validée avec ses propres preuves | Pannes, concurrence, limites et interruptions du complément traitées avec état inspectable, reprise et absence de double effet ou droit restauré. | Injecter panne, concurrence, expiration/révocation, réponse perdue et interruption/reprise selon les cas du profil ; vérifier état durable et ressources libérées lorsque requis, avant la tâche suivante. |
| 7 | Tâche 6 techniquement validée avec ses propres preuves | Résultats des contrôles exécutés dans les tâches 4–6 disponibles, cohérents avec les fichiers courants et exempts de donnée sensible. | Consolider commandes, résultats et versions déjà prouvés ; réexécuter seulement les contrôles invalidés par modification ou les compléments justifiés sur les fichiers finaux. |
| 8 | Tâche 7 techniquement validée avec ses propres preuves | Scénarios d’intégration/conformité du profil reliés à la dépendance et à l’artefact réels ; garanties et limites mesurées sans extrapolation. | Exécuter les cas du profil listés ci-dessus et les scénarios complets applicables ; comparer résultats, bornes et refus avec le canon. Les mocks ne qualifient pas une dépendance réelle ; rapporter non exécuté/échec séparément. |
| 9 | Tâche 8 techniquement validée avec ses propres preuves | Signataire exclu avant succession ; perte traitée par nouvelles clés/recertification ; coexistence et durées bornées ; pas de confiance par snapshot. | Revue croisée du résultat de référence ci-dessus, des scénarios et preuves actuelles ; réexécuter seulement les preuves invalidées, pas une recette déjà valide sans motif. |
| 10 | Tâche 9 techniquement validée avec ses propres preuves | Matrice de preuves reliée aux versions/artefacts et périmètre relu ; aucune opération finale sans son autorisation distincte. | Examiner fichiers et preuves, invariance des archives et périmètre ; appliquer les contrôles propres à l’opération finale seulement si elle est ensuite autorisée. |

Les vérifications utilisent les outils et versions du projet selon [AGENTS.md](../../../AGENTS.md) et [DEVOPS.md](../../../DEVOPS.md). Pour un changement Python, inclure la compilation syntaxique et les suites configurées ; pour une interface web, inclure tests et build frontend ainsi que Chromium et Firefox headless, et les contrôles visuels/manuels applicables. Les tests matériels, réseau, stockage, packaging et restauration exigent leur environnement autorisé. La syntaxe seule ne valide aucun comportement. Aucun de ces contrôles n’est exécuté par la présente préparation documentaire.

Pour chaque tâche, conserver identifiant, prérequis, fichiers, commandes, résultats natifs, critère/scénario, versions/artefact, limites et prochaine action ; cocher uniquement après validation technique. Un échec ou une preuve obligatoire indisponible interdit la tâche suivante. Une modification concurrente invalide seulement les preuves affectées et impose leur réconciliation avant reprise.

## Ordre de travail demandé le 23 octobre 2026

L’instruction explicite récente du développeur demande de réaliser les tâches autorisées, puis de procéder aux tests et à la validation dans une seconde phase. Pour ce RUN, cet ordre remplace le verrou antérieur imposant la réussite des tests de chaque tâche avant la réalisation suivante. Les critères, dépendances et preuves requises du présent fichier restent obligatoires : aucune tâche ne reçoit de coche avant ses propres tests/contrôles réussis. Les validations documentaires nécessaires à la cohérence OpenSpec sont effectuées pendant la rédaction ; les essais produit et validations de réalisation sont regroupés dans la seconde phase. CAB unitaire, limites de ressources et autorisations d’effets restent requis.

L’extension ajoute aux tâches 3–6 la conception D4/D5/D6, les cinq ports et l’état initial du §12 de contracts.md, leur réalisation, les refus et la reprise ; aux tâches 7–9, les scénarios initiaux complets et le passage adoption/retrait/admission réelle. La tâche 10 consolide leurs preuves avant toute clôture. Le profil NV dédié doit être conçu et qualifié ; aucune écriture NV actuelle ne fait partie du lot documentaire. Le passage au contrôle ordinaire n’est pas qualifié par le seul smoke TPM2.

## Complément de portée D7/D8 — 23 octobre 2026

L'ordre de réalisation puis tests/validation de la section précédente reste applicable ; aucune case n'est modifiée par ce complément documentaire. Les tâches 3 et 4 doivent réexaminer le profil terminal, les deux schémas fermés et le port propriétaire local du §13 de [contracts.md](contracts.md), avec leurs propriétaires réels et leur articulation D4/D6. Les tâches de réalisation 5 et 6 incluent leurs validateurs, la résolution privée dans le même OSSL_LIB_CTX, les liaisons et refus, la durée de vie des ressources et la fermeture des capacités initiales ; un nom d'interface, un mock ou une référence opaque n'est pas une réalisation du propriétaire.

Les tâches 7 et 8 couvrent les deux usages matériels distincts, profil fermé feuille/CA, URI canonique et IP exacte indépendamment de la chaîne/EKU, refus de CN/DNS/ancres/chemins ou références CA étrangers, preuve matérielle et possession absentes, substitutions de clé/contexte, état/politique/époque/révocation périmés, ancrage restauré ou invérifiable, refus avant chargement/transport et libération native après échec. Elles incluent adoption/retrait partiels, crash/réponse perdue, conservation des références et âges, fermeture initiale et panne PostgreSQL après D6 sans réouverture. Les tests et validations produit sont exécutés seulement en seconde phase avec les environnements et effets explicitement autorisés ; les contrôles stricts de cohérence documentaire restent applicables pendant la rédaction.

Les tâches 9 et 10 relient les deux exigences et quatre scénarios D7/D8 aux preuves natives actuelles, versions/artefacts et propriétaires effectivement disponibles, sans qualifier une dépendance par un mock. Le profil X.509 et la résolution ne valent ni admission applicative ni mandat technique PostgreSQL. Toute preuve obligatoire manquante conserve la tâche ouverte ; aucune coche, archive ou déclaration de qualification ne résulte du lot documentaire. Le plan exact NV et son autorisation distincte restent nécessaires avant tout effet, et le NV technique PA ne remplace pas l'ancrage PKI Z12.

## Complément D9/D10 — 23 octobre 2026

Ce complément précise les tâches 3–10 existantes, sans en ajouter et sans modifier de coche. L’ordre explicite réalisation puis tests/validation en seconde phase demeure applicable ; les contrôles documentaires stricts restent exécutables pendant la rédaction. Les critères D1–D8 sont conservés.

- Tâche 3 : intégrer les propriétaires et frontières D9/D10, le provisionnement NV extérieur, la suppression matérielle indépendante et le composant CA natif construit séparément des trois PA ; expliciter les domaines de panne et les sources natives/temps/politique.
- Tâche 4 : examiner les contrats fermés/versionnés du §14 de [contracts.md](contracts.md), les liens du mandat PKI personnel, les séquences, ressources privées, refus et réconciliation ; aucune référence ou déclaration client ne vaut preuve.
- Tâches 5–6 : réaliser le propriétaire initial, son admission opérateur, le fournisseur CA privé, le gardien NV et les raccords D8/D6 auprès des vraies sources, avec fermeture des secrets/FD/sessions/capacités. Un nom de port, un schéma ou un mock ne prouve aucune réalisation. Déclarer le chemin natif, les dépendances, l’ABI et le build indépendant avant exécution ; aucune dépendance ou installation implicite.
- Tâches 7–8 : écrire puis exécuter en seconde phase les contrôles de signature personnelle et domaine/challenge/liaisons/temps, politique révoquée ou ancienne, source native substituée, secret par mauvais canal, session PW ou mauvais index/Name, absence de genesis, anciens journal/valeur/époque et concurrence. La recette NV réelle inclut attributs/politique, écritures et vérifications authentifiées, suppression/redéfinition refusées aux signataires, coupure/réponse perdue/réconciliation et retrait D6 des ressources déjà ouvertes. Chaque effet exige sa cible et son autorisation exactes ; aucun essai destructif n’est présumé autorisé sur hvp1.
- Tâche 9 : relier les critères D9/D10, ceux de D1–D8 et les scénarios OpenSpec aux preuves natives de la seconde phase, avec versions et artefacts ; distinguer tests de structure, contrôle documentaire et qualification intégrée.
- Tâche 10 : vérifier l’ensemble des preuves, le passage adoption/retrait/admission, l’indépendance PA/PKI et les limites encore ouvertes avant toute clôture. Aucun contrôle obligatoire absent ne reçoit de coche ou de qualification.

Le présent lot porte uniquement sur .openspec.yaml, proposal.md, design.md, contracts.md et tasks.md du change Z12. Canons, deltas et requirements.md restent inchangés, ainsi que C08/PA01/Auth. Aucun effet TPM/NV, clé, installation ou essai produit n’en résulte. Le plan exact D5 et son autorisation distincte restent requis ; hvp1 est l’hôte actuel et ne prouve pas la disponibilité d’un TPM de laboratoire distinct.

## Complément de réalisation D14/D15 — 24 octobre 2026

Les seules coches historiques 1–2 et les critères D1–D10 restent intacts. Ce complément précise les tâches existantes sans en créer ni en cocher. L’ordre humain prévaut : réalisation des sources en première phase ; constructions, tests et validation produit en seconde phase. Les contrôles documentaires stricts ont lieu pendant la rédaction.

- Tâche 3 : revoir propriétaires, placement des unités et domaines de panne D14/D15, sources natives libsystemd/chrony, politique protégée/versionnée et secret host+tpm2 ; distinguer observations préliminaires, admission et effet.
- Tâche 4 : vérifier les demandes et résultats fermés/versionnés du §15 de [contracts.md](contracts.md), types/unités, sources avant PG et après D6, séquences, refus, propriétaire des FD et libération ; conserver §12–14.
- Tâches 5–6, première phase : réaliser observateurs natifs, application du temps vérifié aux mandats et TLS/X509, gardien PKI distinct du CA et remise privée au seul C.Z12_NV_GUARD/v1 authentifié. Réaliser les contrôles courants et fermetures sans transformer une référence, un DTO ou un mock en source positive.
- Tâches 7–8, seconde phase : construire les artefacts et exécuter les scénarios §15.5 sur les sources et propriétaires réels, avant PG et après adoption/retrait ; prouver bornes UTC 1 seconde/600 secondes, authentification NTS et vérifications TLS, provenance/destinataire, facteurs effectifs, FD/sessions/secrets et retrait après redémarrage/récupération. Les effets TPM/NV gardent le plan exact et l’autorisation D5 distincts.
- Tâche 9 : relier exigences/scénarios aux preuves réellement exécutées, sources/versions/artefacts et environnements observés ; distinguer contrôle documentaire, tests de structure, compilation et qualification intégrée.
- Tâche 10 : vérifier toutes les preuves et dépendances applicables, D6, limites, indépendance PA/PKI et nettoyage avant clôture ; aucune garantie manquante n’est cochée ou réputée non applicable pour permettre une archive.

Avant construction, actualiser le manifeste des sources et empreintes : le digest historique a7475b39fc528f27b36566aaa4b706b6315908ae30557f241489ae48dfcd20d4 ne couvre pas les inclusions et tests modifiés, ni les réalisations suivantes. Les versions et limites de build sont dans [design.md](design.md). Le LXC CT 100 autorisé se coordonne techniquement entre RUN pour services communs, essais incompatibles et remises à zéro, sans nouvelle demande d’approbation pour ses seules opérations internes ; hôte, Git/OpenSpec hôte, Proxmox et TPM physique partagé conservent leurs périmètres. Le snapshot ne restaure pas le TPM. Aucun essai produit, installation, clé ou effet TPM/NV ne résulte de ce lot documentaire de cinq fichiers.


## Complément de réalisation D16 — 24 octobre 2026

Les seules coches 1–2 restent intactes. Les tâches existantes intègrent le §16 de [contracts.md](contracts.md), sans nouvelle tâche ni validation de réalisation par la transcription.

- Tâches 3–4 : revoir propriétaires et contrats privés fermés/versionnés des autorisations CA/parent/terminales, sources host+tpm2 et FD racine hors ligne, séparation NV/PA/PG, destinataires/contextes, tailles/encodages explicites, refus et durée de vie.
- Tâches 5–6, première phase : réaliser les lecteurs/remises et callbacks natifs auprès des vraies sources et destinataires, contrôles courants et effacement/libération ; aucune valeur secrète implicite ou transposition de D15 en preuve CA/terminale.
- Tâches 7–8, seconde phase : construire puis vérifier facteurs réels, mauvais destinataire/matériel/usage, credential/FD ancien ou inadmissible, absence de secret, octets NUL et bornes de longueur, contexte substitué, erreurs et ressources réellement transférées/libérées, récupération/redémarrage et retrait D6. Aucun mock ou nom de port ne qualifie le fournisseur.
- Tâches 9–10 : relier scénarios, producteurs/destinataires, versions et artefacts aux preuves exécutées avant toute clôture ; conserver les clés et âges adoptés sans réouverture initiale.

Le lot autorisé porte uniquement sur .openspec.yaml, proposal.md, design.md, contracts.md et tasks.md. Canons/deltas, requirements.md et fichiers PA/C08/Auth sont hors de ce lot. Aucun code, secret actuel, installation, test produit ou effet TPM/NV n’en résulte. Réalisation puis qualification en seconde phase et autorisation d’effets D5 restent distinctes.


## Complément D17 — 25 octobre 2026

Seules coches 1 et 2 conservées, sans nouvelle tâche numérotée ni coche. Ce complément précise les tâches existantes pour l'attente M1 et le §17 de contracts.md, fourni dans ce lot. Il utilise les types du §1 de contracts.md et les primitives du §14.3 de contracts.md.

- Tâches 3 et 4 : revoir profil natif privé et copie d'audit sans capacité, politique et plan comme contenus extérieurs distincts, constantes de domaine exactes, prépublication puis publication avec codecs exacts, enveloppe fermée sans clé candidate, représentation exacte de binding_sha256, bornes de vie et époques, propriétaires initial puis ordinaire, cycle du pin sous procédure extérieure.
- Tâches 5 et 6, première phase : réaliser remises et vérifications natives auprès des vraies sources et destinataires, contrôles courants, fencing, fermeture et effacement, sans transformer DTO, booléen ou mock en preuve.
- Tâches 7 et 8, seconde phase : construire puis vérifier mauvais destinataire, canal, contexte, époques, ancrage, NTS et bornes, octets réels et limites, récupération, redémarrage et retrait D6 sans réouverture initiale.
- Tâches 9 et 10 : relier exigences, scénarios, versions et artefacts aux preuves réellement exécutées, conserver D1 à D16, clés, chaînes, âges et retraits, TCB et limites, avant toute clôture.

## Complément D18 du 25 octobre 2026

Coches 1 et 2 conservées, sans nouvelle tâche ni coche. Le §18 de `contracts.md` fait foi.

Tâches 3 et 4 : revoir propriétaires, attente de clé D10, vingt-deux champs, codec, enveloppe fermée quatre champs signature 64, défi volatile, mesure extérieure, lien avec l’horloge TLS réelle, condition `chrony` bloquante et refus.

Tâches 5 et 6, première phase : réaliser le constat natif, le cycle à usage unique, la vérification de signature et des liaisons, avec fermeture, sans effet de clé, d’heure, de TPM ou de NV.

Tâches 7 et 8, seconde phase : exécuter nominal, bornes exactes et juste au-delà, rejeu, suspension, redémarrage, restitution, dérive, TLS sans chaîne admissible et élargissement conservateur.

Tâches 9 et 10 : relier exigences, scénarios, versions et artefacts aux preuves exécutées, conserver D1 à D17 et D6 sans réouverture. Aucun effet actuel.
## Complément temps v2 : critères sans coche — 26 octobre 2026

Les coches 1 et 2 restent seules acquises. Ce complément précise les tâches existantes, sans tâche nouvelle et sans coche.

- Tâches 3 et 4 : réexaminer propriétaires, contrats fermés, champs, incertitude U(t), âge de 600 secondes, modes SYNCHRONISE, HORS_LIGNE et INVERIFIABLE, modèle qualifié, provenance qualifiée et continuité qualifiée pour HORS_LIGNE, profil valide et acquisition actuelle, refus, serveurs amont et locaux, et articulation avec D1 à D18 sans réouverture au titre de D6.
- Tâches 7 et 8 : construire puis exécuter en seconde phase les contrôles sur sources et environnements réels, bornes exactes et juste au-delà de 600 secondes et de 1 seconde, suspension et reprise, restitution et incohérences, TLS sans chaîne admissible, sans transformer un contrôle documentaire en qualification.
- Tâches 9 et 10 : relier scénarios, preuves, versions et artefacts effectivement exécutés, conserver D1 à D18 et les limites ouvertes, sans clôture anticipée.

## Précision T0 — tâches 3 à 10 existantes

Numéros 1 à 10 et coches 1 et 2 conservés, aucune coche ni numéro nouveau. T0 porte les huit documents sans qualification : `design.md`, `contracts.md`, `tasks.md`, nouveau `RACCORDS_TEMPS_V2.md`, nouveau `RECETTE_TEMPS_V2.md`, `specs/runtime/spec.md`, `requirements.md` dans Z12 et canon `openspec/specs/runtime/spec.md`. Contrôles documentaires ciblés Z12 et runtime, puis globaux standard et strict, avec 23 copies actualisées. T1, T2, T3 réalisent, testent, corrigent, retestent et valident par unité avant suivante, avec sources et tests de chaque unité future ; T4 réalise qualification intégrée et contrôle global final distinct. Cette consigne actuelle remplace les formules historiques en deux phases pour la suite. Aucun accord de code, installation ou activation dans T0.

Voir [BLOCKERS.md](./BLOCKERS.md) — bilan 2026-10-26T16:50:33.314075+00:00 RUN cismp6-pixs-9dd1542d4c0542f2, tâches 3-10 non validées.

Voir aussi [STATISTICS.md](./STATISTICS.md) — rapport cumulé depuis le 2026-10-17 (change ouvert — dépendances manquantes — archivage en attente).

## Sous-lots normalisés

Relevé documentaire du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md), [contracts.md](contracts.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Contrat de validation élémentaire — préparation GSCM du 22 octobre 2026 » ; « Périmètre et cas de contrôle propres au lot » ; « Critères et contrôles par tâche future ».

### Z12-SL01 — Auditer les blocs normatifs et renvois de requirements.md, l’implémentation actuelle et ses preuves ; décider du complément réellement manquant sans recréer l’existant.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tâches — Z12 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 34 du texte conservé.
  - Prérequis immédiat : Sources, décisions et prérequis externes vérifiés ; tâches historiques pertinentes recoupées
  - Critère observable de validation : Inventaire daté des exigences/scénarios et de l’existant ; écarts réels séparés des réalisations historiques et des inconnues.
  - Contrôles exigés dans cette tâche et preuve : Recouper les textes complets, leurs versions et preuves ; vérifier liens et absence de doublon, conserver la liste des écarts.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z12-SL02 — Confirmer la sélection de la capacité, les rôles/plateformes/ressources applicables et les dépendances obligatoires ; ne pas transformer une non-sélection en réussite de test.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tâches — Z12 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 35 du texte conservé.
  - Prérequis immédiat : Tâche 1 techniquement validée avec ses propres preuves
  - Critère observable de validation : Profil, rôles, cibles, ressources, capacités et dépendances obligatoires explicitement sélectionnés ; aucune absence convertie en réussite.
  - Contrôles exigés dans cette tâche et preuve : Vérifier manifests/profil et graphe déclaré contre les contrats ; documenter absence, incompatibilité et non-sélection avant effet.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z12-SL03 — Lever les barrières de conception de design.md et faire valider les choix encore ouverts avant réalisation ; présenter tout delta normatif ou dépendance supplémentaire nécessaire.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tâches — Z12 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 36 du texte conservé.
  - Prérequis immédiat : Tâche 2 techniquement validée avec ses propres preuves
  - Critère observable de validation : Contrats, propriétaires, choix et paramètres nécessaires à la prochaine réalisation arrêtés ; aucun arbitrage bloquant remplacé par une hypothèse.
  - Contrôles exigés dans cette tâche et preuve : Revue de conception et des cas nominaux/refus du profil ; validation documentaire requise et preuve des décisions avant code.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z12-SL04 — Définir les contrats, schémas, propriétaires et adapters du périmètre : A10i6–A10i20 : PKI dédiée, intermédiaires, protection des clés, secours, exclusion/bascule, algorithmes et successions racine.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tâches — Z12 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 37 du texte conservé.
  - Prérequis immédiat : Tâche 3 techniquement validée avec ses propres preuves
  - Critère observable de validation : Contrats et schémas versionnés du seul objet du lot vérifiables indépendamment de la réalisation suivante ; entrées, sorties, refus, limites et propriétaires explicites.
  - Contrôles exigés dans cette tâche et preuve : Si contrats documentaires : revue des invariants et structure ; si représentations exécutables : syntaxe et tests de types/versions/champs/bornes et refus sans effets. Aucun adapter futur ne remplace cette preuve.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z12-SL05 — Réaliser le complément ciblé et son branchement aux dépendances, en conservant les structures déjà livrées.

- Ancien repère et tâche rattachée : tâche 5 ; section « Tâches — Z12 », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 38 du texte conservé.
  - Prérequis immédiat : Tâche 4 techniquement validée avec ses propres preuves
  - Critère observable de validation : Chemin nominal du complément et branchement public observés ; refus indispensables de types, contexte, droits et dépendances déjà traités ; résultat réel distingué du reçu.
  - Contrôles exigés dans cette tâche et preuve : Exécuter syntaxe, unités et intégrations nécessaires au branchement nominal et à ses refus dans le périmètre du lot ; utiliser le propriétaire réel si persistance ou effet réel est requis. Les tests nécessaires de 7/8 sont effectués dès ici.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z12-SL06 — Traiter les échecs, concurrence, limites et interruptions propres au lot ; états incertains explicités et reprise sous autorité/contexte courants.

- Ancien repère et tâche rattachée : tâche 6 ; section « Tâches — Z12 », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 39 du texte conservé.
  - Prérequis immédiat : Tâche 5 techniquement validée avec ses propres preuves
  - Critère observable de validation : Pannes, concurrence, limites et interruptions du complément traitées avec état inspectable, reprise et absence de double effet ou droit restauré.
  - Contrôles exigés dans cette tâche et preuve : Injecter panne, concurrence, expiration/révocation, réponse perdue et interruption/reprise selon les cas du profil ; vérifier état durable et ressources libérées lorsque requis, avant la tâche suivante.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z12-SL07 — Exécuter syntaxe, contrôles configurés et unités/négatifs applicables, en rapportant les résultats natifs sans données sensibles.

- Ancien repère et tâche rattachée : tâche 7 ; section « Tâches — Z12 », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 40 du texte conservé.
  - Prérequis immédiat : Tâche 6 techniquement validée avec ses propres preuves
  - Critère observable de validation : Résultats des contrôles exécutés dans les tâches 4–6 disponibles, cohérents avec les fichiers courants et exempts de donnée sensible.
  - Contrôles exigés dans cette tâche et preuve : Consolider commandes, résultats et versions déjà prouvés ; réexécuter seulement les contrôles invalidés par modification ou les compléments justifiés sur les fichiers finaux.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z12-SL08 — Exécuter les intégrations/conformités du profil : Bornes exactes et juste au-delà, types/champs étrangers, rôle/contexte/mandat inadmissibles, échéance/révocation, concurrence, réponse perdue, crash/reprise, état ancien et ressources réellement libérées. Mesurer seulement le traitement concerné et ne pas extrapoler ses plafonds au PA/PBO entier.

- Ancien repère et tâche rattachée : tâche 8 ; section « Tâches — Z12 », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 41 du texte conservé.
  - Prérequis immédiat : Tâche 7 techniquement validée avec ses propres preuves
  - Critère observable de validation : Scénarios d’intégration/conformité du profil reliés à la dépendance et à l’artefact réels ; garanties et limites mesurées sans extrapolation.
  - Contrôles exigés dans cette tâche et preuve : Exécuter les cas du profil listés ci-dessus et les scénarios complets applicables ; comparer résultats, bornes et refus avec le canon. Les mocks ne qualifient pas une dépendance réelle ; rapporter non exécuté/échec séparément.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z12-SL09 — Vérifier la sortie attendue : Signataire exclu avant succession ; perte traitée par nouvelles clés/recertification ; coexistence et durées bornées ; pas de confiance par snapshot.

- Ancien repère et tâche rattachée : tâche 9 ; section « Tâches — Z12 », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 42 du texte conservé.
  - Prérequis immédiat : Tâche 8 techniquement validée avec ses propres preuves
  - Critère observable de validation : Signataire exclu avant succession ; perte traitée par nouvelles clés/recertification ; coexistence et durées bornées ; pas de confiance par snapshot.
  - Contrôles exigés dans cette tâche et preuve : Revue croisée du résultat de référence ci-dessus, des scénarios et preuves actuelles ; réexécuter seulement les preuves invalidées, pas une recette déjà valide sans motif.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z12-SL10 — Relier chaque scénario applicable aux preuves/version/artefact, examiner le diff et les limites ; Git, synchronisation, archive, installation et publication restent soumis à leur autorisation propre.

- Ancien repère et tâche rattachée : tâche 10 ; section « Tâches — Z12 », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Critères et contrôles par tâche future », ligne 43 du texte conservé.
  - Prérequis immédiat : Tâche 9 techniquement validée avec ses propres preuves
  - Critère observable de validation : Matrice de preuves reliée aux versions/artefacts et périmètre relu ; aucune opération finale sans son autorisation distincte.
  - Contrôles exigés dans cette tâche et preuve : Examiner fichiers et preuves, invariance des archives et périmètre ; appliquer les contrôles propres à l’opération finale seulement si elle est ensuite autorisée.
- Preuves disponibles à recouper : [BLOCKERS.md](BLOCKERS.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
