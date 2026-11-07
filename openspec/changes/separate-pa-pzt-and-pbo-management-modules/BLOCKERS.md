# PA10 — Blocages 2.2 à 2.4 au 30/10/2026

Statut : BLOQUÉ pour finalisation — change ouvert — dépendances manquantes — archivage en attente. SL11 EN COURS, 10/13. La phase SL11 en cours n’est pas confondue avec un retour RUN. Les objets 2.2 à 2.4 restent ouverts, non cochés ni renumérotés. Aucune unité indépendante utile restante n’est identifiée sans stub ni nouveau change.

Douze unités locales sont validées sur leur seul périmètre, sept pures et cinq PG. Les preuves locales sont conservées : 209 tests unitaires Agent PASS, 97 critères PG en 7 suites soit 14 store, 14 relay, 12 binding, 12 provenance, 11 document, 20 stockage et 14 adapter. Syntaxe 0, une requête capturée pour le store, W045 connu côté relay avec zéro erreur, caches et schémas nettoyés. Le schéma TEST compte 11 tables et 5 migrations, TEST SEULEMENT. Le manifest 0.1.0 et migration_lock sont inchangés. L’extension S1 et Agent2 n’est pas activée sur des données métier. Le comportement v1 est préservé, sans activation live revendiquée.

Les incidents sont conservés : contrôle store q80 en échec sur cap.queries puis corrigé en captured_queries et q90 à 14 PASS, contrôle adapter q86 REJECTED pour seul titre divergent avant GO et once puis nouvelle demande exacte q91 à 14 PASS, q49 stale annulé, demande composition54 en erreur MCP Connection closed puis lookup PENDING avec notification FAILED et annulation CANCELLED, prévol28 avec natif deny constaté puis pilote qui restaure ask avec nouvelle identité true once exit 0 et READY28 vérifié. Aucun true rejoué.

## 2.2 — Contrats PA et PZT avec PA01, PA03 et C14

Objet : [tasks.md ligne 38](tasks.md), section 2 Réalisation future. Prérequis GSCM ligne 65 : tâche 2.1e validée avec ses preuves.

Décisions acquises : A1 à A5 validées selon [RACCORDS.md §§17-19](RACCORDS.md), détails D-S1, D-R1, D-F1 et D-SMIG validés selon [DETAIL_S1_R1_F1.md §§3-6](../add-pa-native-build-and-component-composition/DETAIL_S1_R1_F1.md). Contrats, DTO et projections existent. Les anciennes mentions ouvertes ne rouvrent pas ces choix.

Constat : [RACCORDS.md §4 R01-R09](RACCORDS.md) montre le catalogue PA01 adopté et les DTO écrits, avec une qualification opérationnelle des fournisseurs, handlers et raccords requis non établie pour PA10. Les écritures d’autres lots ne valent pas qualification. [RACCORDS.md §§11-14](RACCORDS.md) confirme les réponses PA01, C08 et Z12 comme inventaires, avec une qualification opérationnelle des producteurs et résolveurs non établie pour PA10. [DETAIL_S1_R1_F1.md §4.1](../add-pa-native-build-and-component-composition/DETAIL_S1_R1_F1.md) définit stage_submission et observe_commit avec relecture sur base primaire, [DETAIL_S1_R1_F1.md §4.2](../add-pa-native-build-and-component-composition/DETAIL_S1_R1_F1.md) impose le commit externe et la réconciliation avant réémission, [DETAIL_S1_R1_F1.md §4.3](../add-pa-native-build-and-component-composition/DETAIL_S1_R1_F1.md) exige un profil serveur versionné sans valeur par défaut. Les colonnes claim_id, claim_epoch et worker_ref existent dans [models.py](../../../src/pixs/agent/models.py), mais la réservation et l’usage sûr restent à prouver. Les Protocols de [ports.py](../../../src/pixs/agent/ports.py) lignes 126-171 ne sont pas les nouveaux fournisseurs. [DETAIL_S1_R1_F1.md §5.2](../add-pa-native-build-and-component-composition/DETAIL_S1_R1_F1.md) nomme AgentOwnerAuthorityProvider, InitialPaAuthorityProvider et AgentPztTransport comme réalisations futures. [DETAIL_S1_R1_F1.md §5.4](../add-pa-native-build-and-component-composition/DETAIL_S1_R1_F1.md) conserve TimeProducer 2.0.0 à quatre méthodes et interdit now, qui n’est donc pas un manque.

Dépendances : PA01 pour catalogue et résultat durable, C08 pour projection et confirmation, Z12 pour identité et confiance, PA03 pour exécutants et lifecycle. Les cas [RECETTE_RACCORDS.md §§9-11](RECETTE_RACCORDS.md) C05, C07 et C14-C19 restent NON EXÉCUTÉS au sens runtime, même si les 12 unités couvrent des aspects locaux.

Phase empêchée : reserve_next, prepare_attempt, submit_attempt, record_observation, reconcile_submission et pause_or_cancel vers CANCELLED, ainsi que les mutations et observe_commit. Ces opérations sont examinées mais non approuvées faute de profil versionné, de staging authentique avec octets attendus, de jeton vérifié et de preuves propriétaires indépendantes.

Reprise : livrer le profil versionné, les fournisseurs authentiques pour le résultat, l’origine, la confirmation et le temps, la composition et les vérifications au point d’usage selon [DETAIL_S1_R1_F1.md §5.2](../add-pa-native-build-and-component-composition/DETAIL_S1_R1_F1.md) et [DETAIL_S1_R1_F1.md §5.4](../add-pa-native-build-and-component-composition/DETAIL_S1_R1_F1.md), le staging séparé et observe_commit prouvé, puis exécuter les repères P-SRF05 à P-SRF14 applicables. Seule la validation technique de 2.1e puis de 2.2 est requise, sans archive.

## 2.3 — Contenus Debian et Docker avec PA09 et X01

Objet : [tasks.md ligne 39](tasks.md), section 2 Réalisation future. Prérequis GSCM ligne 66 : tâche 2.2 validée avec ses preuves.

Constat : [RACCORDS.md §4 R10](RACCORDS.md) demande trois PA plus PZT pour Debian et deux PA plus PZT pour Docker, sans PBO local imposé. La qualification opérationnelle des artefacts utiles PA09 et X01 pour ce périmètre n’est pas établie pour PA10. [RECETTE_RACCORDS.md §2](RECETTE_RACCORDS.md) C25-C27 reste NON EXÉCUTÉ.

Phase empêchée : intégration build et plateforme, frontières de supervision distribuée.

Reprise : 2.2 validée, artefacts utiles livrés, cas C25-C27 exécutés avec commandes et résultats conservés.

## 2.4 — Scénarios propriétaires et livraison

Objet : [tasks.md ligne 40](tasks.md), section 2 Réalisation future. Prérequis GSCM ligne 67 : tâche 2.3 validée avec ses preuves.

Constat : [RECETTE_RACCORDS.md ligne 3](RECETTE_RACCORDS.md) garde C01-C28 NON EXÉCUTÉS. Le §7 P1 à 17 méthodes ne qualifie aucun runtime. [RECETTE_RACCORDS.md §§11-12](RECETTE_RACCORDS.md) et [DETAIL_S1_R1_F1.md §7](../add-pa-native-build-and-component-composition/DETAIL_S1_R1_F1.md) gardent P-SRF01 à P-SRF18 PRÉVUS NON EXÉCUTÉS. Les 12 unités qualifient leur périmètre local, pas le parcours réel.

Phase empêchée : qualification complète et revendication de livraison.

Reprise : 2.3 validée, scénarios locaux et distants, panne, sécurité et compositions exécutés sur dépendances réelles, preuves conservées. Les statistiques suivront depuis le 17/10, heure inconnue, sans donnée inventée ici.
