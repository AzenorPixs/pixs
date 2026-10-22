# Validation locale — C07

RUN : `cismp4-pixs-04b6968c4b2249d8`. Change : `activate-reference-runtime-composition`. Revue du 2026-10-21T20:51:24.088Z.

## Décision et limites

Le socle hôte intermédiaire C07 satisfait ses critères locaux de conception, raccordement et refus fermé. La tâche 2.4 a été clarifiée par RSMP explicitement autorisée : l’intégration finale est portée par C14. Cette validation ne certifie pas le P0, le paquet C18, la recette C17 ni l’identité C19 ; `globally_compatible=False` et les dimensions non évaluées sont conservés. L’archive est désormais prouvée ci-dessous ; STATISTIQUES.md, la publication CAB et le gate restent des preuves distinctes.

Le périmètre comprend six sources hôte, sept recettes et un helper PostgreSQL de test. Aucun canon, modèle/migration métier, frontend, configuration OpenCode ou dépendance n’est modifié par ce jalon. Les changements préexistants C06 sont préservés ; sa cible Core 0003 n’est utilisée que structurellement dans une recette et ne livre pas C06. Aucun Git, déploiement, serveur d’écoute ni second change n’est autorisé ou exécuté.

## Résultats exécutés

Les effectifs ci-dessous désignent les cas/contrôles des enfants et recettes, sans additionner leurs wrappers unittest ni les 24 préparations C03. Total : **80 cas/contrôles distincts du socle**, plus **une recette native C01 à 17 contrôles**. Tous réussis aux empreintes ci-dessous.

| Réf. | Recette | Résultat et preuve native | Limite |
|---|---|---|---|
| R1 | Transport ASGI | 8 cas enfant, `call_01a15cb19e75756b8513e6d47ecb973f`, sortie suite_exit=0 | Routes/contexte de recette ; pas de drain HTTP en cours. |
| R2 | Raccord Auth/Core/audit et lifespan PG | 5 + 7 contrôles, `call_01a15f78052b7256b636d4d633ed6687`, deux sorties test_exit=0 ; PostgreSQL 16.14, Django 6.1.2 | Plans/clés C08 et classification C10 fixtures ; schémas jetables nettoyés, connexions fermées. |
| R3 | Plan/Kernel/registres/configuration | 15 tests, `call_01a15f8805b274dfb9596f717719a21d`, test_exit=0 | Manifests Kernel/Core/Auth réels ; Agent/PZT et attestations synthétiques, port serveur de confiance requis en production. |
| R4 | Lifecycle générique | 20 tests, `call_01a15f9b8a4870b79548ebc55b8d7840`, test_exit=0 | Adapters explicites de recette ; pas d’installation/migration/purge implicite. |
| R5 | Entrée et frontière HTTP | 17 gardes + 8 HTTP, `call_01a15faf1eca716a8d8517cf9f3200cf`, test_exit=0 | Double résolveur pour refus avant effet ; configuration Django de recette sans base ouverte. |
| R6 | Entrée native systemd/C01 | 17 contrôles vrais, reçu hôte attesté ci-dessous ; compilation source `call_01a1601ea56b75248150cd863eb39e2b` | Exception humaine distincte au pilotage OC ; ne pas présenter le banc comme un appel Bash natif OC. |

Les compilations des fichiers modifiés, leur UTF-8/LF et leurs SHA sont présentes dans les reçus natifs des recettes ; la compilation du banc final est distincte. Aucun comportement modifié après ces succès. Les erreurs attendues sont testées : dépendances/versions/ports/adapters absents ou ambigus, table manquante, contexte partiel, annulations, mauvais hôte/origine/route et mode non INSTALLER. Liveness ne prouve aucune disponibilité applicative.

## Attestation de la recette hôte C01

CGPT a lu les seuls reçus publics de l’exception autorisée, depuis l’UID hôte 1000. Le contrôleur de recette UID 0 utilise uniquement l’unité `pixs-c07-c4-entry-0593a443.service`, RuntimeMaxSec=45, consommateur UID 1000 PID 2195873, invocation `44d3fa765eb242b697f56763487dc5cf`. Le handshake de l’unité et sa SelfProof précèdent la résolution. Le vrai provider C01 et sa politique publique sont consommés, le journal est initialisé par son API publique et les quatre événements `secret.resolve` / `secret.resolve.consume` sont confirmés. Le vrai Django est construit puis son lifecycle est arrêté ; aucune connexion PostgreSQL.

Contrôles vrais : `c01_audit_confirmed`, `host_closed`, `journal_initialized`, `lifespan_stopped`, `liveness_get`, `liveness_head`, `liveness_post`, `loaded_gate`, `native_self`, `no_database_connection`, `origin_closed`, `policy_loaded`, `private_closed`, `real_c01_entry_constructed`, `runtime_context_active`, `unit_quiescent`, `unknown_closed`.

L’arrêt natif est attesté avant libération de la lease ; constat final unité absente, PID 0, groupe de processus vide. Authentification sudo standard et invalidation finale : auth_exit=0, bench_exit=0, sudo_invalidate_exit=0. Aucun mot de passe enregistré ; fixtures publiques uniquement, chiffrement `null` fonctionnel. Aucune protection cryptographique de production `host+tpm2` ni readiness P0 n’est attestée. OpenCode, CAB et les autres services sont préservés.

| Reçu local (non autorité canonique) | SHA-256 |
|---|---|
| `/home/devops/datas/pixs/output/cismp/cismp4-pixs-04b6968c4b2249d8/entry-systemd-system-journal/0593a443/parent-result.json` | `8aca8ac472dfff823e23bf50410bea4ed9a522d028b1a6dc101bbdd3638e4e60` |
| `/home/devops/datas/pixs/output/cismp/cismp4-pixs-04b6968c4b2249d8/entry-systemd-system-journal/0593a443/result.json` | `278a2f842c120646abce3d560dbeaf579244d7f3ca309d1bafcaac115d228035` |
| `/home/devops/datas/pixs/output/cismp/cismp4-pixs-04b6968c4b2249d8/entry-systemd-system-journal/0593a443/ready.json` | `935cf7d89e919113a153c265a3201baa62fa403096c55ab10f678ba0d7c0c9f6` |
| `/home/devops/datas/pixs/output/cismp/cismp4-pixs-04b6968c4b2249d8/entry-systemd-journal-terminal-result.json` | `3e6e0c9a98b423d8f7f682521fdae2de05c924294e9eeba242ae479cb009b8c5` |

Les anciens essais demeurent conservés dans les dossiers `entry-systemd`, `entry-systemd-system`, `entry-systemd-system-root` : refus du mode utilisateur/null, identité du contrôleur et journal non initialisé. Le succès final réside dans `entry-systemd-system-journal/0593a443`. Les reçus UID 1000 mode 0600 ne sont pas lus par OpenCode UID 1002 ; l’attestation CGPT et leurs empreintes assurent la provenance, sans relâcher leurs permissions.

## Traçabilité et application des scénarios

[requirements.md](requirements.md) référence exactement 107 exigences, 131 scénarios et 19 empreintes canoniques. Sa table est une traçabilité, pas 131 succès. La disposition de chaque ligne est précisée ci-dessous : **L** preuve locale bornée par R1–R6 ; **P** couverture partielle, reste explicitement non exécuté ; **H** scénario propriétaire/produit non exécuté dans ce socle. Une limite ne retire aucun MUST du canon. Les conditions finales non remplies maintiennent le P0 non prêt et n’empêchent pas l’hôte intermédiaire autorisé par le canon. Aucun producteur Agent/PZT ou authentificateur d’attestation de production n’est livré par les doubles.

| Exigence source | Application locale et preuve / reste non exécuté |
|---|---|
| authentication / 40 — Module essentiel autonome pixs.auth | L — R3/R4 exigent Auth ; fixture structurelle distincte. |
| authentication / 52 — Autonomie locale et PostgreSQL par défaut | P — R2/R3 consomment les producteurs ; installation autonome et confiance distribuée non qualifiées par C07. |
| authentication / 64 — Propriété des données Auth et protection des justificatifs | L — R2 persiste puis retire une session via producteurs publics ; audit confirmé. |
| authentication / 76 — Sous-modules Auth composés par les mécanismes communs | P — R2/R3 consomment les producteurs ; installation autonome et confiance distribuée non qualifiées par C07. |
| capabilities / 8 — Descripteur de capacité résolu à la composition | L — R3 vrai pipeline Kernel et registres ; R4 observations liées aux adapters, ambiguïté/absence/incompatibilité refusées. Couverture bornée aux assertions R3/R4. |
| capabilities / 17 — États de disponibilité distincts | L — R3 vrai pipeline Kernel et registres ; R4 observations liées aux adapters, ambiguïté/absence/incompatibilité refusées. Couverture bornée aux assertions R3/R4. |
| capabilities / 28 — Fanion ne remplace pas la résolution | L — R3 vrai pipeline Kernel et registres ; R4 observations liées aux adapters, ambiguïté/absence/incompatibilité refusées. Couverture bornée aux assertions R3/R4. |
| capabilities / 37 — Résolution sur version déclarée | L — R3 vrai pipeline Kernel et registres ; R4 observations liées aux adapters, ambiguïté/absence/incompatibilité refusées. Couverture bornée aux assertions R3/R4. |
| capabilities / 51 — Sélection du fournisseur sur la version de capacité | L — R3 vrai pipeline Kernel et registres ; R4 observations liées aux adapters, ambiguïté/absence/incompatibilité refusées. Couverture bornée aux assertions R3/R4. |
| compatibility / 8 — Contraintes de version déclarées et vérifiées | L — R3 valide les preuves via port serveur et refuse version/port absents ; dimensions non évaluées et verdict global conservés. Authentification de production non fournie par les doubles. |
| compatibility / 17 — Aucune compatibilité présumée | L — R3 valide les preuves via port serveur et refuse version/port absents ; dimensions non évaluées et verdict global conservés. Authentification de production non fournie par les doubles. |
| compatibility / 26 — Matrice de compatibilité globale | L — R3 valide les preuves via port serveur et refuse version/port absents ; dimensions non évaluées et verdict global conservés. Authentification de production non fournie par les doubles. |
| compatibility / 35 — Compatibilité déclarative distincte de la conformité comportementale | L — R3 valide les preuves via port serveur et refuse version/port absents ; dimensions non évaluées et verdict global conservés. Authentification de production non fournie par les doubles. |
| compatibility / 44 — Coexistence pendant les montées de version | H — Aucune montée de version ni suppression ; coexistence interversions non exécutée. |
| compatibility / 123 — Responsabilités de l'appelant et du noyau pour les preuves | L — R3 valide les preuves via port serveur et refuse version/port absents ; dimensions non évaluées et verdict global conservés. Authentification de production non fournie par les doubles. |
| component-model / 8 — Types de composants unifiés | P — Manifest réel consommé par R3 ; facette frontend non exercée, aucun nouveau type de composant. |
| component-model / 54 — États de composition, installation et santé distincts | L — R3/R4 distinguent composition, observations et disponibilité ; aucune readiness P0 déduite. |
| configuration / 8 — Schémas typés validés avant activation | L — R3 ferme configuration/snapshots et références typées ; R6 consomme C01 réel dans INSTALLER. |
| configuration / 17 — Priorité déterministe des sources | L — R3 ferme configuration/snapshots et références typées ; R6 consomme C01 réel dans INSTALLER. |
| configuration / 28 — Secrets par référence hors artefacts | L — R3 ferme configuration/snapshots et références typées ; R6 consomme C01 réel dans INSTALLER. |
| contracts / 17 — Versionnement SemVer indépendant | H — Aucun contrat versionné ni retrait modifié ; scénarios d’évolution de contrat non réexécutés par ce socle. |
| contracts / 26 — Dépréciation et retrait encadrés | H — Aucun contrat versionné ni retrait modifié ; scénarios d’évolution de contrat non réexécutés par ce socle. |
| core / 8 — Module obligatoire au-dessus du noyau | L — R3 refuse Core absent. |
| core / 116 — Frontière Core Auth et dépendance unidirectionnelle | L — R2 relit les faits Core et refuse le jeton après retrait ; propriété des tables préservée. |
| dependencies / 37 — Graphe frontend récursif et façades publiques | H — Aucun graphe frontend, extension, slot, code distant ou route contributive livré ; mécanismes canoniques inchangés, scénarios dédiés non réexécutés. |
| extension-contracts / 8 — Points d'extension publics versionnés | H — Aucun graphe frontend, extension, slot, code distant ou route contributive livré ; mécanismes canoniques inchangés, scénarios dédiés non réexécutés. |
| extension-contracts / 17 — Contributions déclarées et isolées | H — Aucun graphe frontend, extension, slot, code distant ou route contributive livré ; mécanismes canoniques inchangés, scénarios dédiés non réexécutés. |
| extension-contracts / 26 — Niveau de confiance des extensions | H — Aucun graphe frontend, extension, slot, code distant ou route contributive livré ; mécanismes canoniques inchangés, scénarios dédiés non réexécutés. |
| extension-contracts / 38 — Collisions et composition déterministe | H — Aucun graphe frontend, extension, slot, code distant ou route contributive livré ; mécanismes canoniques inchangés, scénarios dédiés non réexécutés. |
| extension-contracts / 47 — Composition interface au build | H — Aucun graphe frontend, extension, slot, code distant ou route contributive livré ; mécanismes canoniques inchangés, scénarios dédiés non réexécutés. |
| extension-contracts / 56 — Frontières publiques des composants frontend imbriqués | H — Aucun graphe frontend, extension, slot, code distant ou route contributive livré ; mécanismes canoniques inchangés, scénarios dédiés non réexécutés. |
| initial-application-bootstrap / 11 — Composition Django initiale déclarée | L — R1/R5/R6 vrai Django, liveness seule publique, routes privées/host/origin fermés ; aucune façade livrée. |
| initial-application-bootstrap / 27 — Configuration sensible de la composition Django initiale | L — R6 vrai C01 vers paramètres Django ; sans connexion PostgreSQL dans ce banc. |
| initial-application-bootstrap / 39 — Surface HTTP initiale minimale | L — R1/R5/R6 vrai Django, liveness seule publique, routes privées/host/origin fermés ; aucune façade livrée. |
| initial-application-bootstrap / 54 — Shell TanStack initial intégré | H — Shell frontend hors des fichiers et routes livrés ici ; intégration façade/paquet ultérieure. |
| kernel / 8 — Noyau sans logique métier | L — R3 vrai pipeline Kernel et registres ; R4 observations liées aux adapters, ambiguïté/absence/incompatibilité refusées. Couverture bornée aux assertions R3/R4. |
| kernel / 17 — Noyau fournit des registres génériques | L — R3 vrai pipeline Kernel et registres ; R4 observations liées aux adapters, ambiguïté/absence/incompatibilité refusées. Couverture bornée aux assertions R3/R4. |
| kernel / 26 — Noyau agnostique aux fournisseurs | L — R3 vrai pipeline Kernel et registres ; R4 observations liées aux adapters, ambiguïté/absence/incompatibilité refusées. Couverture bornée aux assertions R3/R4. |
| kernel / 35 — Composition ambiguë refusée explicitement | L — R3 vrai pipeline Kernel et registres ; R4 observations liées aux adapters, ambiguïté/absence/incompatibilité refusées. Couverture bornée aux assertions R3/R4. |
| lifecycle / 8 — États de cycle de vie distincts | L — R1/R2/R4 acquisition ordonnée, admission fermée, arrêt inverse, erreurs et annulations propagées ; drain des requêtes en cours non qualifié. |
| lifecycle / 17 — Transitions autorisées et refusées | P — R4 configure/start uniquement ; install/migrate/purge implicites refusés, désactivation produit hors recette. |
| lifecycle / 26 — Ordre déterministe des hooks | L — R1/R2/R4 acquisition ordonnée, admission fermée, arrêt inverse, erreurs et annulations propagées ; drain des requêtes en cours non qualifié. |
| lifecycle / 35 — Idempotence des opérations | P — R1 traite séquences et arrêts répétés ; aucun rejeu métier C06 qualifié. |
| lifecycle / 44 — Diagnostic des échecs | L — R1/R2/R4 acquisition ordonnée, admission fermée, arrêt inverse, erreurs et annulations propagées ; drain des requêtes en cours non qualifié. |
| migrations / 8 — Contrat de migration | H — Aucun moteur ou plan de migration C07 livré ; R2 relit les schémas et refuse table manquante. Migrations de fixtures propriétaires isolées seulement, pas de migration automatique à l’entrée. |
| migrations / 17 — Planification et ordre déterministes | H — Aucun moteur ou plan de migration C07 livré ; R2 relit les schémas et refuse table manquante. Migrations de fixtures propriétaires isolées seulement, pas de migration automatique à l’entrée. |
| migrations / 26 — Compatibilité pendant l'application | H — Aucun moteur ou plan de migration C07 livré ; R2 relit les schémas et refuse table manquante. Migrations de fixtures propriétaires isolées seulement, pas de migration automatique à l’entrée. |
| migrations / 35 — Reprise idempotente | H — Aucun moteur ou plan de migration C07 livré ; R2 relit les schémas et refuse table manquante. Migrations de fixtures propriétaires isolées seulement, pas de migration automatique à l’entrée. |
| migrations / 44 — Contraction contrôlée | H — Aucun moteur ou plan de migration C07 livré ; R2 relit les schémas et refuse table manquante. Migrations de fixtures propriétaires isolées seulement, pas de migration automatique à l’entrée. |
| modules / 8 — Manifest lisible obligatoire | L — R3 utilise les manifests Kernel/Core/Auth réels ; R2 consomme les API publiques. Agent/PZT de recette restent des doubles. |
| modules / 17 — Frontière API publique et privée | L — R3 utilise les manifests Kernel/Core/Auth réels ; R2 consomme les API publiques. Agent/PZT de recette restent des doubles. |
| modules / 26 — Propriété des données et migrations associées | P — R2 préserve propriétaires et vérifie les schémas ; aucun changement de modèle/migration C07. |
| modules / 35 — Chargement contrôlé déterministe | L — R3 utilise les manifests Kernel/Core/Auth réels ; R2 consomme les API publiques. Agent/PZT de recette restent des doubles. |
| modules / 44 — Propriété des contributions frontend modulaires | H — Contributions frontend non sélectionnées dans le socle. |
| providers / 8 — Déclaration lisible des fournisseurs | L — R3 vrai pipeline Kernel et registres ; R4 observations liées aux adapters, ambiguïté/absence/incompatibilité refusées. Couverture bornée aux assertions R3/R4. |
| providers / 17 — Sélection explicite sans choix implicite | L — R3 vrai pipeline Kernel et registres ; R4 observations liées aux adapters, ambiguïté/absence/incompatibilité refusées. Couverture bornée aux assertions R3/R4. |
| providers / 26 — Conformité contractuelle vérifiable | L — R3 vrai pipeline Kernel et registres ; R4 observations liées aux adapters, ambiguïté/absence/incompatibilité refusées. Couverture bornée aux assertions R3/R4. |
| providers / 35 — Dégradation contrôlée et diagnostic | L — R3 vrai pipeline Kernel et registres ; R4 observations liées aux adapters, ambiguïté/absence/incompatibilité refusées. Couverture bornée aux assertions R3/R4. |
| reference-composition / 10 — Qualification du binaire commun et des profils de ressources P0 | H — Qualification du produit distribué, binaire, parcours installable et reproductibilité finale reportés aux lots propriétaires C14/C17/C18/C19 ; aucun succès produit déduit des recettes. |
| reference-composition / 24 — Capacités obligatoires du P0 | L — R3/R4 refusent obligations manquantes ; R6 preuve C01 INSTALLER fonctionnelle. P0 maintenu non prêt, aucun NORMAL ni qualification cryptographique host+tpm2. |
| reference-composition / 33 — Capacités hors P0 explicites | P — Aucune option/connecteur externe sélectionné ; absence ne dispense pas des obligations essentielles. |
| reference-composition / 44 — Preuve reproductible | H — Qualification du produit distribué, binaire, parcours installable et reproductibilité finale reportés aux lots propriétaires C14/C17/C18/C19 ; aucun succès produit déduit des recettes. |
| reference-composition / 55 — Profil initial PBO PFO Debian local v1 | H — Qualification du produit distribué, binaire, parcours installable et reproductibilité finale reportés aux lots propriétaires C14/C17/C18/C19 ; aucun succès produit déduit des recettes. |
| reference-composition / 64 — Garanties du socle conservées dans le profil initial | L — R3/R4 refusent obligations manquantes ; R6 preuve C01 INSTALLER fonctionnelle. P0 maintenu non prêt, aucun NORMAL ni qualification cryptographique host+tpm2. |
| reference-composition / 73 — Parcours installable et utilisable du profil initial | H — Qualification du produit distribué, binaire, parcours installable et reproductibilité finale reportés aux lots propriétaires C14/C17/C18/C19 ; aucun succès produit déduit des recettes. |
| reference-composition / 82 — Capacités non sélectionnées du profil initial | P — Aucune option/connecteur externe sélectionné ; absence ne dispense pas des obligations essentielles. |
| reference-composition / 91 — Preuve de la composition effectivement distribuée | H — Qualification du produit distribué, binaire, parcours installable et reproductibilité finale reportés aux lots propriétaires C14/C17/C18/C19 ; aucun succès produit déduit des recettes. |
| reference-composition / 100 — Choix C01 systemd et exception d’amorçage du profil Debian local | L — R3/R4 refusent obligations manquantes ; R6 preuve C01 INSTALLER fonctionnelle. P0 maintenu non prêt, aucun NORMAL ni qualification cryptographique host+tpm2. |
| reference-composition / 114 — Qualification et source de vérité après amorçage | L — R3/R4 refusent obligations manquantes ; R6 preuve C01 INSTALLER fonctionnelle. P0 maintenu non prêt, aucun NORMAL ni qualification cryptographique host+tpm2. |
| reference-composition / 128 — Profil Auth standard sans connecteur externe installé | P — Aucune option/connecteur externe sélectionné ; absence ne dispense pas des obligations essentielles. |
| reference-runtime / 12 — Binaire PBO commun et socle modulaire | H — Compilation Nuitka/Cython, binaire distribué et exécutants PA/PZT hors recette ; contrat canonique conservé. |
| reference-runtime / 26 — Compilation PBO Nuitka standalone | H — Compilation Nuitka/Cython, binaire distribué et exécutants PA/PZT hors recette ; contrat canonique conservé. |
| reference-runtime / 40 — Cython ciblé et mesuré dans PBO | H — Compilation Nuitka/Cython, binaire distribué et exécutants PA/PZT hors recette ; contrat canonique conservé. |
| reference-runtime / 54 — Qualification du binaire PBO | H — Compilation Nuitka/Cython, binaire distribué et exécutants PA/PZT hors recette ; contrat canonique conservé. |
| reference-runtime / 63 — Pile de référence unique | P — ASGI Django et adapters explicites retenus ; aucun runtime alternatif installé. R1–R6 bornent cette pile, pas le produit. |
| reference-runtime / 77 — Adapter explicite | P — ASGI Django et adapters explicites retenus ; aucun runtime alternatif installé. R1–R6 bornent cette pile, pas le produit. |
| reference-runtime / 88 — Absence de sélection cachée | P — ASGI Django et adapters explicites retenus ; aucun runtime alternatif installé. R1–R6 bornent cette pile, pas le produit. |
| reference-runtime / 98 — Version stable actuelle de Django | P — Python 3.14.8/Django 6.1.2 observés dans les recettes ; aucun changement de dépendance. Qualification du graphe/build complet non revendiquée. |
| reference-runtime / 111 — Adaptation complète à la stable Django ciblée | P — Python 3.14.8/Django 6.1.2 observés dans les recettes ; aucun changement de dépendance. Qualification du graphe/build complet non revendiquée. |
| reference-runtime / 122 — Relevé et qualification de la stable courante | P — Python 3.14.8/Django 6.1.2 observés dans les recettes ; aucun changement de dépendance. Qualification du graphe/build complet non revendiquée. |
| reference-runtime / 135 — Qualification reproductible et politique sans dérogation | P — Python 3.14.8/Django 6.1.2 observés dans les recettes ; aucun changement de dépendance. Qualification du graphe/build complet non revendiquée. |
| reference-runtime / 149 — Dépendances Python les plus récentes compatibles avec Django | P — Python 3.14.8/Django 6.1.2 observés dans les recettes ; aucun changement de dépendance. Qualification du graphe/build complet non revendiquée. |
| reference-runtime / 161 — Versions exactes, plages et bornes minimales Django | P — Python 3.14.8/Django 6.1.2 observés dans les recettes ; aucun changement de dépendance. Qualification du graphe/build complet non revendiquée. |
| reference-runtime / 172 — Qualification du graphe Python et incompatibilités explicites | P — Python 3.14.8/Django 6.1.2 observés dans les recettes ; aucun changement de dépendance. Qualification du graphe/build complet non revendiquée. |
| reference-runtime / 186 — Absence d'installation forcée ou de recul Django | P — Python 3.14.8/Django 6.1.2 observés dans les recettes ; aucun changement de dépendance. Qualification du graphe/build complet non revendiquée. |
| reference-runtime / 197 — Compatibilité avec le Python actuel du projet | P — Python 3.14.8/Django 6.1.2 observés dans les recettes ; aucun changement de dépendance. Qualification du graphe/build complet non revendiquée. |
| reference-runtime / 221 — Couche exécutable PA séparée | H — Compilation Nuitka/Cython, binaire distribué et exécutants PA/PZT hors recette ; contrat canonique conservé. |
| reference-runtime / 234 — Modules de gestion pixs.agent et pixs.pzt dans PBO | H — Compilation Nuitka/Cython, binaire distribué et exécutants PA/PZT hors recette ; contrat canonique conservé. |
| runtime / 23 — Modes d'exploitation PBO Standalone et ZT | H — Processus, budgets, scheduler/lease, topologies et exécutants PA/PZT non lancés par C07 ; scénarios produit non exécutés, obligations conservées. |
| runtime / 42 — Profil de ressources par environnement d'exécution | H — Processus, budgets, scheduler/lease, topologies et exécutants PA/PZT non lancés par C07 ; scénarios produit non exécutés, obligations conservées. |
| runtime / 56 — Dimensionnement explicite et borné des processus | H — Processus, budgets, scheduler/lease, topologies et exécutants PA/PZT non lancés par C07 ; scénarios produit non exécutés, obligations conservées. |
| runtime / 70 — Proposition de dimensionnement sous configuration | H — Processus, budgets, scheduler/lease, topologies et exécutants PA/PZT non lancés par C07 ; scénarios produit non exécutés, obligations conservées. |
| runtime / 84 — Ressources détectées demandées et appliquées distinctes | H — Processus, budgets, scheduler/lease, topologies et exécutants PA/PZT non lancés par C07 ; scénarios produit non exécutés, obligations conservées. |
| runtime / 93 — Reconfiguration contrôlée des ressources | H — Processus, budgets, scheduler/lease, topologies et exécutants PA/PZT non lancés par C07 ; scénarios produit non exécutés, obligations conservées. |
| runtime / 107 — Budgets compatibles avec les garanties du profil | H — Processus, budgets, scheduler/lease, topologies et exécutants PA/PZT non lancés par C07 ; scénarios produit non exécutés, obligations conservées. |
| runtime / 116 — Supervision et qualification des profils de ressources | H — Processus, budgets, scheduler/lease, topologies et exécutants PA/PZT non lancés par C07 ; scénarios produit non exécutés, obligations conservées. |
| runtime / 130 — Profils distincts d'un même artefact | P — R5 refuse modes/rôles non admis ; aucune activation Standalone/ZT ou profil produit qualifiée. |
| runtime / 139 — Profils de déploiement déclarés | P — R5 refuse modes/rôles non admis ; aucune activation Standalone/ZT ou profil produit qualifiée. |
| runtime / 151 — Exposition minimale par défaut | L — R5/R6 entrée web minimale ; worker/scheduler refusés par la fabrique, management privé fermé. |
| runtime / 160 — Processus stateless et coordination persistante | H — Processus, budgets, scheduler/lease, topologies et exécutants PA/PZT non lancés par C07 ; scénarios produit non exécutés, obligations conservées. |
| runtime / 174 — Lease du scheduler avec clôture de péremption | H — Processus, budgets, scheduler/lease, topologies et exécutants PA/PZT non lancés par C07 ; scénarios produit non exécutés, obligations conservées. |
| runtime / 183 — Arrêt, drain et reprise contrôlés | P — R1/R4/R6 fermeture admission et ressources prouvée ; drain des requêtes et reprise d’effets non exécutés, lots C09/C15/C18. |
| runtime / 192 — États techniques PA et PZT distincts du runtime PBO | H — Processus, budgets, scheduler/lease, topologies et exécutants PA/PZT non lancés par C07 ; scénarios produit non exécutés, obligations conservées. |
| runtime / 205 — Topologies locales et distantes PA PZT | H — Processus, budgets, scheduler/lease, topologies et exécutants PA/PZT non lancés par C07 ; scénarios produit non exécutés, obligations conservées. |
| services / 8 — Enregistrement contractuel des services | L — R3 sélection déterministe ; R5 refuse exposition privée et routes inconnues. Pas de publication de service supplémentaire. |
| services / 17 — Résolution déterministe du fournisseur | L — R3 sélection déterministe ; R5 refuse exposition privée et routes inconnues. Pas de publication de service supplémentaire. |
| services / 28 — Traçabilité et sécurité des appels | L — R2 contexte par invocation et audit durable confirmé ; R5 ferme la surface privée. |

Les scénarios frontend/slots/extensions, mises à niveau/retrait de contrats, moteur de migration, scheduler, budgets/compilation, topologies PA/PZT, drain/reprise d’effets et parcours installé ne sont pas exécutés par ces recettes. Aucun changement de ces fonctions n’est inclus. Les preuves de leurs propriétaires restent exigées avant toute revendication finale. Le test PG ne qualifie ni environnement productif ni service réseau.

## Matrice des tâches locales

| Tâche | Preuve locale / condition |
|---|---|
| 1.1 | Canon 107/131/19 recoupé, dépendances C01/C02/C03/C04/C05 livrées, matrices de conception et cadrage relues. |
| 1.2 | Contrats et fichiers présentés avant mandats ; ASGI choisi, adapters explicites, entrée INSTALLER/web fermée, port d’attestation serveur ; aucun nouveau canon. |
| 2.1 | R1/R2/R5/R6 hôte Django et points de branchement publics. |
| 2.2 | R2/R3/R4/R6 configuration, registres, contexte, provider C01 et lifecycle communs. |
| 2.3 | R3/R4 refus des modules/ports/preuves absents, observations invalides et versions incompatibles ; P0 non prêt. |
| 2.4 | R1/R3/R4 démarrage/arrêt isolés, ordre et ambiguïtés ; R6 entrée native et arrêt attesté ; C14 reste final après RSMP humaine limitée. |
| 3.1 | Compilations et 80 cas/contrôles + recette native 17 vrais, reçus ci-dessus ; contrôle documentaire natif `call_01a1603cdfce77519e54896de4a1e3cd` réussi (4 docs, 107/131/19, 14 compilations mémoire), puis OpenSpec strict `call_01a1603e751574ffa1bf03aafb74c045` réussi après coches. |
| 3.2 | Isolation/nettoyage PG, annulations et refus fermés ; fixtures publiques, absence de secret réel ; matrice ci-dessus distingue tous les scénarios non exécutés. |
| 3.3 | Empreintes des 14 fichiers après tests, cadrages inchangés, C06 préservé, aucun fichier hors périmètre ; comparaison des contenus préparés sans opération Git. |
| 3.4 | Garde procédurale : aucun Git/déploiement, archive et publication seulement dans le cycle CISMP autorisé. STATISTIQUES.md requis après archive réussie ; sa preuve reste obligatoire avant gate, aucune coche ne la remplace. |

## Empreintes et cadrages

Recontrôle après tests : 2026-10-21T20:41:29.144Z.

| Fichier modifié | SHA-256 |
|---|---|
| `src/pixs/backend/host_asgi.py` | `b3624320d5c8ed81f05a06dd8f1d66619062b56d16f6baa46fc36ea66de793ef` |
| `src/pixs/backend/host_composition.py` | `1f839c4a3f4971b7ecf24038779319e995379282520d497b5c19ae9f606a63f9` |
| `src/pixs/backend/host_lifespan.py` | `009d520c3eada82401cd8261799c4e4dc9bfe86bfe30e0f5a837b6b090477310` |
| `src/pixs/backend/host_plan.py` | `da0088bc15e41a76ba892bc613ba9b923ebbe512fad9a0ee0218c33e5a265bc1` |
| `src/pixs/backend/host_runtime.py` | `7d5de36c83cf0969d89b9f1a899eb69732b083c1f797a19b1fbe063bd8dbec55` |
| `src/pixs/backend/host_entry.py` | `778dc5455ab4b652f99ecda35d4af4617dfc7af9cd1b596bbe71666305d132e0` |
| `tests/integration/test_backend_host_asgi_closed.py` | `edeb38bb09d7bce1de11582c7694b0bbfd2da3b14290d1feef3621af8e6f90a7` |
| `tests/integration/test_backend_host_composition_postgres.py` | `792275b135df7b51ed161910e3c257e1671c084fb8d5459d163c6d73fbbcc885` |
| `tests/integration/test_backend_host_lifespan_postgres.py` | `171c67e64b877b4a7c2e0f312ac70b7ecd422beeebf5b02dd6c98bf8db61a25f` |
| `tests/unit/test_backend_host_plan.py` | `e2434351306bf78a729d70058fd22c59ba83cb54fd81449324151e45ad1f4acb` |
| `tests/unit/test_backend_host_runtime.py` | `67c74a859fb2f281308024821506ab81bf0f5297027970395b50d515939f4a75` |
| `tests/integration/test_backend_host_entry_guards.py` | `ac01a5bb80929e7d390d84f2fcd5680a228e29cc28e9e6b63f0d594f80159866` |
| `tests/integration/test_backend_host_entry_systemd.py` | `c5d6f3c6f134b621c8db59e92a7be324f6c49d8891a47514c4744cb1af5a19b3` |
| `tests/integration/auth_pg_test_support.py` | `593228cc37091307391bd195c9c23e09093fe24dae0d950c624b9c52a07b3e7e` |

Les cadrages ci-dessous ont été relus et restent cohérents avec ce socle intermédiaire. Aucune mise à jour nécessaire : C01 fonctionnel distinct de la protection host+tpm2 ; serveur/distribution, ressources et P0 gardent leurs propriétaires.

| Cadrage inchangé | SHA-256 |
|---|---|
| `AGENTS.md` | `1dd65acb8b666e8ca5c1519a398ff8fe1361e50db54a23945dbd5ff88263ce8e` |
| `PROJECT.md` | `ab1c2307796f24bee31753f3c7fe1375dbbf941c74da9b215690621726b3fdb6` |
| `TECHNICAL.md` | `35712fad11db4b2765e48fc2f19a0f198da741c7f663b4ec91cb3dd9f33e0bd9` |
| `BUILD.md` | `a56e0e39c435a0da93a94c99ae7178ca993a72b414f933c808c4053c0f5c9d30` |
| `DEVOPS.md` | `8af03eaf74db3ceef1f3fcd0cddca544cdf82dddbd5cba5d343d9d0a3a93ba78` |
| `README.md` | `a9919c3d333eec23eae17b9463fdfef0cf991fa6169a6c17b9297d23fb22232a` |

Raccordement final : C14 porte le raccordement final aux obligations essentielles PZT/DNS ; les producteurs Agent/PZT gardent leurs contrats propriétaires ; C17 agrège la recette installable, C18 le paquet/binaire, C19 son identité. Les lots serveur/drain et ressources gardent leurs obligations. Aucun nom de module DNS ni mécanisme de remplacement n’est inventé ici.

## Archivage observé

Archive unique réussie le 2026-10-21T20:55:56.303Z par l’appel natif `call_01a1603f8eed7667ac86418fe021906d`, exit 0 : `2026-10-21-activate-reference-runtime-composition`. Les six fichiers ont conservé leurs empreintes au déplacement, la source active est absente, le verrou de claim est relâché et aucun canon n’est modifié (`specsUpdated=false`, `skip_specs` explicite). Les dix cases locales sont cochées. Les renvois relatifs des trois documents ont ensuite été ajustés sous mandats unitaires sans changer les textes normatifs. Aucun réarchivage. Le rapport STATISTIQUES.md doit être produit et vérifié avant publication de la clôture ; sa présence ne doit pas être déduite de la case procédurale 3.4.
