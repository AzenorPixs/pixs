# Tasks

## 1. Bootstrap du paquet Python et structure du noyau

- [x] 1.1 Créer `pyproject.toml` conforme PEP 621 déclarant uniquement la stdlib (aucune dépendance externe ajoutée) — vérification : le fichier existe à la racine, est parseable par tomllib, et `python -m compileall src/` sort code 0
- [x] 1.2 Créer l'arborescence `src/pixs/kernel/` avec sous-paquets `manifest`, `registry`, `resolver`, `lifecycle`, `config`, `diagnostics` — vérification : l'arborescence attendue est listée et l'import `pixs.kernel` réussit sans erreur
- [x] 1.3 Mettre en place la découverte de tests stdlib `unittest` avec répertoires séparés `tests/unit` et `tests/integration` — vérification : `python -m unittest discover` s'exécute sans erreur de collection sur les deux niveaux

## 2. Modèles déclaratifs et validation des manifests

- [x] 2.1 Implémenter le modèle déclaratif de manifest (identifiant, type parmi les six, version SemVer, dépendances obligatoires/optionnelles, capacités fournies/requises, contrats, `schema_version`) — preuve à renouveler au schéma 1 : capacités et contrats fournis en tables versionnées (voir 6.5) — vérification : tests unitaires de construction depuis une fixture TOML valide et de rejet champ par champ avec diagnostic nommant le champ manquant
- [x] 2.2 Implémenter le parsing `component.toml` via `tomllib` et le contrôle de `schema_version` — vérification : test unitaire « version de schéma inconnue » passe, le composant reste non validé avec un diagnostic indiquant la version concernée
- [x] 2.3 Implémenter le refus des secrets et logiques exécutables dans les manifests — vérification : tests unitaires sur fixtures « secret embarqué » et « expression à évaluer » passent, composition refusée avec diagnostic explicite
- [x] 2.4 Implémenter les règles d'identifiants namespacés (`pixs.*` réservés) et la détection de collisions — vérification : tests unitaires de rejet d'un composant externe usurpant `pixs.*` et de deux composants au même identifiant bloquant l'activation avant chargement

## 3. Pipeline de composition, graphe déterministe et diagnostics

- [x] 3.1 Implémenter les étapes `discover → validate → resolve → activate` en pipeline ordonné et idempotent — vérification : test d'intégration exécutant deux fois le pipeline sur la même fixture, avec graphe, ordre et diagnostics identiques et absence d'effet dupliqué
- [x] 3.2 Implémenter le tri topologique à départage déterministe par identifiant canonique et la détection de cycles — vérification : tests unitaires A→B→C (ordre stable identique entre exécutions) et A→B→A (composition invalidée, cycle identifié dans le diagnostic)
- [x] 3.3 Implémenter la résolution de fournisseurs : fournisseur configuré, sinon candidat compatible unique, sinon composition invalide — preuve à renouveler sur versions déclarées : configuré compatible sinon refus, évaluation SemVer des capacités (voir 6.6) — vérification : test unitaire du scénario deux fournisseurs sans sélection, refus avec diagnostic d'ambiguïté et absence de dépendance à l'ordre de découverte
- [x] 3.4 Structurer les diagnostics de composition typés (élément, contrainte, étape) — vérification : tests unitaires asserting pour chaque classe d'échec que le message identifie l'élément et la contrainte violés, sans valeur sensible

## 4. Registres génériques, configuration par références et règle data-driven

- [x] 4.1 Implémenter les sept registres génériques (modules, dépendances, cycle de vie, services, événements, configuration, extensions) alimentés uniquement par des modèles validés — vérification : tests unitaires démontrant le refus d'enregistrement d'une contribution non déclarée et l'idempotence d'un double enregistrement
- [x] 4.2 Implémenter la résolution de configuration par priorité déclarée (schéma, défauts, statique, runtime, références de secrets) — vérification : tests unitaires de surcharge d'une même clé avec valeur gagnante reproductible ; le noyau ne résout aucune valeur de secret, test de contrôle de la face publique
- [x] 4.3 Implémenter le jeu de composants requis porté en données de composition validées — preuve à renouveler avec composants requis contraints (`"id [comparateurs]"`, voir 6.6) — vérification : test d'intégration déclarant `pixs.core` comme requis en données seulement ; l'absence invalide l'activation avant chargement avec diagnostic, et un test vérifie l'absence de tout nom de concept métier codé en dur dans le code du noyau

## 5. Cycle de vie mécanique et interfaces publiques

- [x] 5.1 Implémenter les états installed, enabled, configured, ready, healthy et les opérations mécaniques `discover`, `validate`, `install`, `enable`, `configure`, `start`, `disable` — vérification : tests unitaires d'états non confondus (installé-désactivé ≠ prêt) et de refus explicite de `migrate`, `upgrade`, `uninstall`, `purge` hors périmètre
- [x] 5.2 Implémenter les hooks de cycle de vie ordonnés par le graphe résolu — vérification : test d'intégration comparant deux exécutions complètes, ordre des hooks et du chargement identiques
- [x] 5.3 Exposer l'interface publique du noyau par les façades de paquet et borner l'export — vérification : un test d'intégration importe exclusivement l'API déclarée et asserte que les modules privés ne figurent pas dans les façades exportées

## 6. Tests et contrôles finaux

- [x] 6.1 Compléter la suite unitaire couvrant chaque scénario normé du périmètre (kernel, component-model, dependencies, capabilities, configuration, compatibility pour la partie déclarative) — preuve à renouveler aux exigences RSMP versions/preuves (voir 6.5–6.7) — vérification : `python -m unittest discover -s tests/unit` passe et la correspondance scénario-test est listée dans le rapport de session
- [x] 6.2 Compléter la suite d'intégration sur compositions synthétiques (résolution complète, ambiguïtés, cycles, composant requis absent, deux ordres de découverte) — vérification : `python -m unittest discover -s tests/integration` passe avec preuves reproductibles
- [x] 6.3 Vérifier l'absence de secret et de donnée de production dans fixtures, rapports et diagnostics — périmètre : scan exclusivement des artefacts synthétiques de tests et diagnostics et des rapports de test autorisés ; AUCUN parcours des sources exclues par AGENTS.md ni lecture de secret ; les fixtures sentinelles (placeholders volontaires prouvant la détection) sont évaluées séparément du contrôle des sorties moteur — vérification : test automatisé de motifs sensibles sur tout artefact de test du périmètre, suite passant sans fuite détectée
- [x] 6.4 Exécuter les contrôles finaux du change : `python -m compileall src/`, suite complète `unittest`, `bash -n` et `shellcheck` sur tout script auxiliaire éventuellement produit — vérification : chaque commande sort code 0 et la sortie est consignée dans le rapport de session
- [x] 6.5 Schéma capacités/contrats versionnés et adaptation des fixtures : manifests `[provides].capabilities` et `[implements].contracts` en tables `{id, version, …}` schéma 1, refus des anciennes chaînes sans version avec diagnostic, fixtures historiques adaptées, version du composant jamais proxy — vérification : tests unitaires de validation (construction valide, rejet sans version nommant champ et entrée) et suite existante adaptée passant
- [x] 6.6 Contraintes composants/capacités/contrats/requis : six comparateurs (`== != >= <= > <`), conjonctions, préversions ordre SemVer standard, métadonnées de build ignorées en précédence, syntaxes malformées refusées, évaluation sur versions propres (jamais la version du composant pour une capacité ou un contrat), composants requis contraints, sélection configurée incompatible refusée — vérification : tests unitaires et d'intégration (contrainte insatisfaite, malformée, mismatch de version, déterminisme deux ordres) passant avec diagnostics nommant consommateur, cible, contrainte et version trouvée
- [x] 6.7 Preuves externes et portée P0 : `ConformityAttestation` en mémoire hors manifest (absence, mismatch de fournisseur/version/build, échec, malformée, ambiguïté refusés ; couverture complète PASS autorisant ; composition déterministe préservée), doubles de preuves clairement nommés limités aux fixtures, exposition P0 limitée aux dimensions connues sans prétention globale — vérification : tests d'intégration de chaque cas passant avec diagnostics non sensibles

Note : les 35 tests d'intégration validés avant RSMP restent acquis comme preuve de déterminisme et de refus fermé, mais ne constituent pas une preuve des nouveaux critères versions/preuves (6.5–6.7).

Hors périmètre (voir proposal.md — Impact) : primitives fonctionnelles de `pixs.core` (utilisateurs, groupes, appartenances, tenants, rôles, ACL, permissions), surface API HTTP, frontend TanStack et graphe frontend récursif, providers concrets, résolution effective de secrets, suites de conformité provider, opérations effectives `migrate`/`upgrade`/`uninstall`/`purge`, et composition de référence intégrale `reference-composition`.
