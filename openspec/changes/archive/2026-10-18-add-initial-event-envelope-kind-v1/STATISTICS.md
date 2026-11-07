# Statistiques — add-initial-event-envelope-kind-v1

RUN : cismp1-pixs-8819654ffc884cb7 ; contexte CAB : 281.

Session de production OpenCode : ses_eb3b8dd48ffeXxoMM3VIUqmRDz. Orchestrateur : 01a14c2a-27ab-7ec1-8b09-2af7796ee991.

Périmètre : un seul change, ses validations et son archivage. Collecte arrêtée après archive et avant rédaction de ce rapport ; écriture du présent rapport, gate et arrêt sont hors intervalle. La sélection et les sondes auxiliaires ne sont pas agrégées aux outils de production.

Sources : API natives OpenCode de cette session, agrégats CAB filtrés par RUN/contexte, mandats et contenus vérifiés dans le checkpoint autorisé. Aucun état Git ou journal exclu consulté.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | OpenCode 1.19.3 ; version LLM N/A | OpenCode Go | high | 1.724 s (sondes) | 767.148 (sondes texte) | N/A — génération active non exposée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex ; modèle exact non exposé | N/A | OpenAI / Codex | N/A | N/A — orchestrateur non sondé | N/A | N/A |

Les moyennes sont arithmétiques sur les sondes valides, hors production. La durée busy et les latences d’outils ne sont pas du temps de génération. Faute de durées actives comparables, le dénominateur du temps de service et les chevauchements d’agents restent N/A.

## 1. Statistiques générales et décisions

Convention : un outil completed est terminé dans le protocole natif, sous autorisation implicite ou explicite ; il ne prouve pas une approbation manuelle ni un résultat fonctionnel vert. Les éditions et commandes exécutées ont une décision CAB explicite et une permission once corrélée. Un refus CAB avant effet reste distinct d’un refus de permission native ; un abandon technique reste une erreur, jamais un refus inventé.

| Décision CAB | Nombre | Part |
|---|---|---|
| approved | 18 | 94,7 % |
| rejected | 1 | 5,3 % |
| needs_clarification | 0 | 0,0 % |
| pending | 0 | 0,0 % |
| Total | 19 | 100,0 % |

Permissions once : 17. Approbation invalidée sans consommation après accès STALE : 1. Demande supplémentaire annulée avant décision : 1. Aucun refus de permission native observé.

Les deux codes 1 du strict global correspondent à quatre WARNING de longueur sur deux canons ; ils ne sont pas des refus techniques ni des tests en échec. Tests : 47/47 (100,0 %) ; compilation : 3/3 (100,0 %) ; ciblé strict et global standard : code 0.

| Mesure native OpenCode | Valeur |
|---|---|
| total | 24838005 |
| input | 838602 |
| output | 32757 |
| reasoning | 6394 |
| cache_read | 23960252 |
| cache_write | 0 |
| Coût natif OpenCode (unité non exposée) | 0.13961090399999992 |
| Coût facturé / abonnement | N/A — non exposé |
| Compactions observées | 0 |

Les compteurs de tokens sont additionnés tels que fournis par l’API, sans conversion en monnaie ni reconstruction d’un total à partir du cache. Les statistiques de messages et d’outils propres à l’orchestrateur Codex ne sont pas exposées par cette connexion : N/A ; les décisions CAB de cet orchestrateur sont mesurées ci-dessus.

Sondes hors production : 3 valides (début, sonde supplémentaire et fin réelle après archive) ; 0 échouées. Relève périodique +30 min manquée : 1. Horodatage prévu et cause : [{"position": "+30 min", "scheduled_at": "2026-10-18T02:15:24.567265+02:00", "observed_at": "2026-10-18T02:16:18.953636+02:00", "cause": "Échéance franchie pendant coordination et traitement du rapport d’archivage ; aucune mesure rétroactive reconstruite"}]. La sonde finale actuelle ne reconstitue pas cette mesure.

| Position | Horodatage | TTMT texte | Débit texte | Tokens sortie | Statut |
|---|---|---|---|---|---|
| début | 2026-10-18T01:45:24.567265+02:00 | 2.323 s | 502.285 | 408 | success |
| fin des tâches de code (sonde supplémentaire) | 2026-10-18T02:10:38.154850+02:00 | 1.745 s | 963.191 | 408 | success |
| fin après archivage | 2026-10-18T02:16:18.953636+02:00 | 1.103 s | 835.967 | 409 | success |

Prompt identique : Sans outil, sans lire de fichier ni accéder au réseau, écris uniquement les nombres de 1 à 200, un par ligne, sans texte supplémentaire.

Le débit utilise les tokens de sortie réellement retournés et les deltas SSE texte corrélés à la session. Raisonnement distinct, sans assimilation aux fragments réseau. Min/max TTMT : 1.103/2.323 s ; min/max débit : 502.285/963.191 tokens/s.

Surcharge des sondes : 1225 tokens de sortie, 805 tokens de raisonnement ; durée cumulée 7.256 s. Coût attribuable N/A. Sessions : ses_eb3be7babffeXYSGvX7u6xhOT2, ses_eb3a76336ffeWticjd10IEc55e, ses_eb3a22fefffel5Ev3NFdYIBwIV.

Benchmark PLLM distinct : mode 1, high, palier 1024, TTFT 4.3005 s ; borne conservatrice du débit global 215.303. Critères valides au contrôle horodaté 2026-10-18T01:44:41+02:00.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---|---|
| assistant | 126 | 67,4 % |
| user | 61 | 32,6 % |
| Total | 187 | 100,0 % |

| Type de partie | Nombre | Part |
|---|---|---|
| reasoning | 109 | 17,5 % |
| step-finish | 125 | 20,1 % |
| step-start | 126 | 20,3 % |
| text | 152 | 24,4 % |
| tool | 110 | 17,7 % |
| Total | 622 | 100,0 % |

| Terminaison assistant | Nombre | Part |
|---|---|---|
| MessageAbortedError | 1 | 0,8 % |
| stop | 39 | 31,0 % |
| tool-calls | 86 | 68,3 % |
| Total | 126 | 100,0 % |

| Famille d’outil | Total / part | Terminé / taux | Refus permission / taux | Erreur technique / taux |
|---|---|---|---|---|
| bash | 9 / 8,2 % | 9 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| cab-mcp | 49 / 44,5 % | 48 / 98,0 % | 0 / 0,0 % | 1 / 2,0 % |
| glob | 9 / 8,2 % | 9 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| grep | 4 / 3,6 % | 4 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| read | 31 / 28,2 % | 31 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| write | 8 / 7,3 % | 8 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| Total | 110 / 100,0 % | 109 / 99,1 % | 0 / 0,0 % | 1 / 0,9 % |

Les décisions CAB sont ventilées dans la section 1. Le transport MCP peut terminer avec une réponse REJECTED : cette réponse est un refus CAB, pas un outil exécuté ni un refus de permission native. L’erreur technique MCP observée est l’interruption du mandat de test mal scopé ; son annulation CANCELLED a ensuite été vérifiée sans exécution.

## 3. Fichiers modifiés

Tentatives d’édition natives mesurées, hors mouvements d’archive. Chemins actuels après déplacement des quatre artefacts OpenSpec. Sept fichiers créés ; tasks.md a aussi reçu une mise à jour avec preuves.

| Chemin absolu complet | Écritures / part | Autorisées terminées / taux | Refusées / taux | Erreur / taux |
|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-event-envelope-kind-v1/.openspec.yaml | 1 / 12,5 % | 1 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-event-envelope-kind-v1/design.md | 1 / 12,5 % | 1 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-event-envelope-kind-v1/proposal.md | 1 / 12,5 % | 1 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-event-envelope-kind-v1/tasks.md | 2 / 25,0 % | 2 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| /home/devops/datas/pixs/src/pixs/backend/event_envelope_kind.py | 1 / 12,5 % | 1 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| /home/devops/datas/pixs/tests/integration/test_event_envelope_kind_integration.py | 1 / 12,5 % | 1 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| /home/devops/datas/pixs/tests/unit/test_event_envelope_kind.py | 1 / 12,5 % | 1 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| Total | 8 / 100,0 % | 8 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |

Le seul archivage autorisé a déplacé .openspec.yaml, proposal.md, design.md et tasks.md ; leurs quatre empreintes sont identiques avant/après. Aucun validateur, record, migration, façade ou canon existant n’a été modifié par ce RUN. Les trois caches Python de compilation sont régénérables et ne constituent pas des fichiers source livrés. Le présent STATISTIQUES.md est publié après la borne de collecte, sous un mandat propre ; il est exclu des huit éditions de production. Le checkpoint non versionné est suivi séparément, sans inventaire Git.

## 4. Commandes

Commandes réellement exécutées ; chaque libellé est limité à 100 caractères. Un code 1 de validation ne signifie pas un refus de permission.

| Commande | Occurrences / part | Codes observés |
|---|---|---|
| /home/devops/.local/npm/bin/openspec archive add-initial-event-envelope-kind-v1 --yes --skip-specs | 1 / 11,1 % | 0 × 1 |
| /home/devops/.local/npm/bin/openspec validate --all | 1 / 11,1 % | 0 × 1 |
| /home/devops/.local/npm/bin/openspec validate --all --strict | 2 / 22,2 % | 1 × 2 |
| /home/devops/.local/npm/bin/openspec validate add-initial-event-envelope-kind-v1 --strict | 1 / 11,1 % | 0 × 1 |
| /home/devops/datas/pixs/.venv/bin/python3 -m py_compile src/pixs/backend/event_envelope_kind.py tes… | 1 / 11,1 % | 0 × 1 |
| /usr/bin/true | 2 / 22,2 % | 0 × 2 |
| PYTHONPATH=src:tests/unit:tests/integration /home/devops/datas/pixs/.venv/bin/python3 -B -m unittes… | 1 / 11,1 % | 0 × 1 |
| Total | 9 / 100,0 % | Tous les effets natifs corrélés |

Commandes refusées CAB avant effet :

| Commande refusée | Nombre / part des refus | Motif |
|---|---|---|
| /home/devops/.local/npm/bin/openspec validate --all | 1 / 100,0 % | Révision OpenSpec modifiée par le pair ; nouvelle demande après relecture |

Commande annulée avant décision : même famille de tests, périmètre Kernel absent du manifeste initial ; une annulation CANCELLED, aucun effet. Nouvelle demande après extension de lecture et prévol frais. Une demande stricte postarchive a reçu APPROVED mais son accès est devenu STALE en attendant le rapport C2 : accès annulé, approbation invalidée sans consommation, aucun signal VERROU_ACQUIS ni commande ; nouvelle demande après relecture. Aucune compilation, écriture ni archive prouvée n’a été rejouée.

Autres incidents de pilotage : premier démarrage broker lent avec timeout de readiness, aucune récupération commune exécutée ; refus HTTP de clôture/lecture et de décision corrigés après réconciliation. Ces réponses HTTP ne sont pas des refus de permission native.

Échecs HTTP du contexte CAB : access-extension-while-held=1, decision-run-divergent=1, evidence-references-required=1, native-session-not-quiescent=1, operation-outside-reservation=3, resource-revision-stale=1.

## 5. Accès web

Agent de production : aucun webfetch/websearch ni URL visitée observé dans l’historique natif complet. Pas de simple requête de recherche transformée en visite.

| Accès web natif | Nombre | Taux |
|---|---|---|
| Autorisé terminé | 0 | N/A — total nul |
| Refusé | 0 | N/A — total nul |
| Erreur technique | 0 | N/A — total nul |
| Total | 0 | N/A — total nul |

Pilotage fournisseur distinct, autorisé par CISMP/PLLM : contrôles et benchmark sur https://opencode.ai/zen/go/v1/usage, https://opencode.ai/zen/go/v1/models et https://opencode.ai/zen/go/v1/responses. Les HTTP 401 antérieurs à la reprise n’étaient pas des visites réussies. Les appels natifs OpenCode et CAB utilisent la boucle locale. Le décompte exhaustif de ces appels d’orchestration est N/A ; il n’est pas assimilé aux outils web de production. Aucun secret, compte ou en-tête d’authentification publié.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début (session de production) | 2026-10-18T01:51:32.791000+02:00 |
| Fin — après archivage | 2026-10-18T02:21:51.629887+02:00 |
| Durée globale (pauses et attentes incluses) | 00 h 30 min 18 s |

Le RUN technique a connu une attente d’authentification avant cette session ; les durées ci-dessus portent sur le change réservé et sa session de production. Attentes CAB et coordination concurrente incluses ; aucune addition de durées simultanées.

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | N/A | N/A | N/A |
| Après — après archivage de la spécification | N/A | N/A | N/A |
| Différence après − avant | — | N/A | — |

N/A : outil natif get_usage_limits et identité de fenêtre codex/10080 minutes non exposés dans cette connexion. Aucun quota Go, restant, ancienne valeur ou estimation ne les remplace. Le compte Codex est partagé ; aucune consommation exclusive n’est attribuée à ce RUN.

| Domaine natif | Total / part globale | Terminé / taux | Refus permission / taux | Erreur technique / taux |
|---|---|---|---|---|
| Fichiers | 8 / 7,3 % | 8 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| Commandes | 9 / 8,2 % | 9 / 100,0 % | 0 / 0,0 % | 0 / 0,0 % |
| Web | 0 / 0,0 % | 0 / N/A | 0 / N/A | 0 / N/A |
| Autres outils | 93 / 84,5 % | 92 / 98,9 % | 0 / 0,0 % | 1 / 1,1 % |
| Total | 110 / 100,0 % | 109 / 99,1 % | 0 / 0,0 % | 1 / 0,9 % |

Totaux croisés : familles d’outils = domaines = 110 ; éditions 8 = outils write ; commandes 9 = outils bash. Arrondis à une décimale, donc certaines sommes de parts affichées peuvent différer de 100,0 % de 0,1 point.

Coordination propre au contexte : attente ressource 30.011 s ; détention partagée 428.540 s. Gels exceptionnels : {'GLOBAL_RECONCILIATION': 0, 'SHARED_MAINTENANCE': 0, 'GLOBAL_PAUSE': 0, 'GLOBAL_STOP': 0}. Ces durées peuvent se recouvrir et ne prouvent aucun gain causal. Busy n’est pas du codage productif.

Résultat livré au périmètre : EventEnvelopeKind DOMAIN/INTEGRATION passif, 47 tests OK, trois compilations OK ; ciblé strict et standard global verts. Strict global avant/après archive : code 1, seulement quatre WARNING historiques de longueur, zéro ERROR ; aucune réussite stricte globale revendiquée.

Archive unique vérifiée : /home/devops/datas/pixs/openspec/changes/archive/2026-10-18-add-initial-event-envelope-kind-v1. Publication technique CAB prouvée par reçu publish-e002a8f779544db8, référence 34. Ce reçu ne remplace pas la vérification du présent rapport ni le gate final.

Git non inspecté, aucun commit/push demandé ni réalisé. Aucun accès PostgreSQL ou navigateur nécessaire. Aucune donnée secrète dans les fichiers livrés ou preuves exposées observées ; authentification fournisseur traitée par le seul processus sécurisé autorisé. Après vérification du rapport : gate, désarmement/libération et arrêt ciblé CISMP1 ; aucun nouveau change et services partagés préservés.
