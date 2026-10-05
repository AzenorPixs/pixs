## 1. Modèle et migration backend

- [x] 1.1 Publier `src/pixs/backend/models.py` contenant uniquement `FeatureFlagSourceSnapshotRecord`, avec exactement `configuration_version = models.TextField(primary_key=True)` et `snapshot = models.JSONField()` ; vérifier par les tests que le modèle expose les deux champs prévus, sans `id`, horodatage, statut, tenant, scope, audit, index personnalisé ou champ PostgreSQL supplémentaire.
- [x] 1.2 Publier `src/pixs/backend/migrations/__init__.py` et `src/pixs/backend/migrations/0001_feature_flag_source_snapshot.py` comme migration `initial` contenant un `CreateModel` Django standard, automatiquement réversible, sans `DeleteModel`, `RunSQL`, SQL PostgreSQL, option de schéma ou dépendance inventée.
- [x] 1.3 Vérifier dans un subprocess Django synthétique, avec gardes réelles sur `psycopg`, `DatabaseWrapper.get_new_connection` et sockets, que l’app implicite installée par `pixs.backend` conserve `name == pixs.backend` et `label == backend`, que le registre est prêt, que la migration publiée est découverte pour l’app `backend` et que zéro connexion est établie.

## 2. Chargeur PostgreSQL en lecture

- [x] 2.1 Publier `src/pixs/backend/feature_flag_postgres_source.py` avec l’API publique `FeatureFlagSourceLoadError(ValueError)` et `load_feature_flag_source_snapshot(expected_configuration_version: str) -> FeatureFlagSourceSnapshot`.
- [x] 2.2 Vérifier que le module du chargeur s’importe sans `settings.configure`, `django.setup`, import de modèle, connexion PostgreSQL, environnement, I/O, horloge ou cache, et que le modèle est chargé paresseusement uniquement après validation de la version.
- [x] 2.3 Valider la version attendue exactement par `type(expected_configuration_version) is str and bool(expected_configuration_version)` ; rejeter seulement `''` et les types non `str`, accepter une chaîne composée d’espaces comme opaque, et ne jamais appeler `strip()`, normaliser ou transformer la valeur utilisée pour la sélection.
- [x] 2.4 Effectuer une unique sélection par clé primaire `pk=expected_configuration_version`, vérifier que la clé primaire renvoyée est de type exact `str` et strictement égale à la version demandée, puis transmettre `record.snapshot` au codec existant.
- [x] 2.5 Décoder et valider l’ensemble du lot canonique via `decode_feature_flag_source_snapshot`, vérifier que le snapshot retourné est de type exact `FeatureFlagSourceSnapshot`, que sa `configuration_version` interne est strictement égale à la version demandée et retourner ce snapshot, sans retourner une évaluation.
- [x] 2.6 Normaliser seulement les erreurs attendues : absence via `DoesNotExist` du modèle, `django.db.utils.DatabaseError` et `FeatureFlagSnapshotCodecError`, avec le message fixe `Source de fanions indisponible` ; ne capturer aucune erreur générale, propager toute exception inattendue, sans journaliser ou divulguer valeur, SQL, schéma, table, cause technique, credential ou traceback.

## 3. Tests unitaires du contrat de lecture

- [x] 3.1 Publier `tests/unit/test_feature_flag_postgres_source.py` et vérifier l’API publique, l’import pur sans réglage/setup/modèle/connexion/I/O, ainsi que le refus exact des versions de mauvais type et de la chaîne vide, avec acceptation d’une chaîne d’espaces opaque transmise sans modification.
- [x] 3.2 Vérifier avec un gestionnaire de modèle instrumenté que chaque version valide produit exactement une lecture par clé primaire, que la version est transmise sans normalisation et qu’aucun filtre, écriture, suppression, DDL ou cache n’est effectué.
- [x] 3.3 Vérifier le round-trip complet de documents canoniques, notamment la préservation exacte des scalaires `False`, des chaînes opaques et des entiers, ainsi que la validation réelle du codec et du contrat source.
- [x] 3.4 Vérifier les refus normalisés pour une absence de ligne, une divergence entre clé primaire et version interne, un document incomplet, un lot invalide, un `DatabaseError` attendu, et la propagation d’une erreur inattendue.
- [x] 3.5 Vérifier que l’exception normalisée conserve la classe publique `FeatureFlagSourceLoadError`, hérite de `ValueError`, expose le message fixe sans valeur d’entrée et ne chaîne pas une cause technique.

## 4. Intégration sûre en processus frais

- [x] 4.1 Publier exactement `tests/integration/test_feature_flag_postgres_source_integration.py` ; aucun autre chemin d’intégration de ce change n’est autorisé.
- [x] 4.2 Installer une configuration Django synthétique pour l’app `pixs.backend` et prouver que les gardes d’import, de setup, de `psycopg`, de `DatabaseWrapper`, de sockets et d’I/O sensibles sont réellement armées, puis vérifier que le chargeur s’importe avant toute configuration sans importer le modèle. Le setup Django explicite charge ensuite le modèle prévu dans le registre, sans connexion ni SQL ; les gardes distinguent ces deux phases autorisées.
- [x] 4.3 Vérifier la découverte effective de l’app, du label, du modèle à deux champs et de la migration initiale dans le processus frais, avec zéro connexion PostgreSQL, sans hypothèse de base, de schéma ou de credential réel.
- [x] 4.4 Tester la composition réelle `evaluate_feature_flag_source_snapshot` sur un snapshot rechargé en simulant seulement la lecture ORM, en couvrant la sélection C2, l’appartenance et l’exclusion de cohorte, le repli `DENY`, le repli `DEFAULT` non sensible, l’expiration de définition et la version canonique incompatible.

## 5. Commande PostgreSQL réelle et isolation destructive maîtrisée

- [x] 5.1 Préparer dans le fichier d’intégration une entrée de commande dédiée, exécutée uniquement par mandat distinct, dont le processus réel est seul autorisé à charger `project.env`, sans exposer les valeurs en stdout, stderr, journal, assertion, diagnostic ou sortie de métrique.
- [x] 5.2 Vérifier avant toute création qu’aucune base, aucun rôle et aucun droit ne sont créés ou modifiés ; refuser immédiatement toute collision de schéma sans appropriation, nettoyage ni modification d’un objet préexistant, puis créer un schéma unique borné par des identifiants psycopg sûrs et restreindre le `search_path` à ce seul schéma.
- [x] 5.3 Exécuter la migration initiale backend dans ce schéma isolé, insérer un snapshot canonique synthétique encodé, relire ce snapshot via l’API publique et comparer exactement la valeur restaurée après round-trip PostgreSQL réel.
- [x] 5.4 Vérifier les refus réels pour une version absente, une clé/contenu divergents et un document stocké corrompu, puis prouver qu’une lecture fonctionnelle du chargeur après setup produit exactement une catégorie `SELECT` et aucune catégorie `INSERT`, `UPDATE`, `DELETE` ou DDL, avec capture des requêtes seulement en mémoire privée.
- [x] 5.5 Prouver la réversibilité de la migration en exécutant le rollback `backend` vers zéro dans le même schéma éphémère, puis supprimer ce schéma uniquement, fermer la connexion et confirmer un nettoyage total en cas de succès comme d’échec.
- [x] 5.6 Si une étape ou le nettoyage échoue, sortir une erreur fixe et explicite sans masquer l’échec initial, sans SQL, sans secret et sans valeur d’environnement ; la suite sûre par défaut doit rester exécutable sans cette commande.

## 6. Documentation et exécution des tests

- [x] 6.1 Compléter `src/pixs/backend/README.md` par append seulement, pour documenter l’app implicite, la table/migration, le chargeur en lecture, les préconditions de confiance serveur et l’absence d’admin, audit, corrélation, cache, route, API HTTP, activation runtime, convergence des trois rôles, garde de build et contrôle multi-tenant.
- [x] 6.2 Compiler chaque fichier Python ajouté ou modifié, y compris modèle, package de migration, migration et chargeur, avec des mandats séparés et des exit codes réels, Les fichiers __pycache__ produits par py_compile sont des artefacts régénérables de cette validation ; aucune source supplémentaire n’est créée.
- [x] 6.3 Exécuter les tests unitaires et d’intégration sûrs de ce change, puis l’ensemble de la suite existante afin de préserver les `154` tests de régression et d’ajouter uniquement les nouveaux tests effectivement nécessaires à ces comportements.
- [x] 6.4 Exécuter séparément la commande PostgreSQL réelle sous mandat distinct, contrôler sa sortie fermée, ses compteurs, son rollback, son drop de schéma éphémère et sa fermeture de connexion sans exposer de secret ni SQL brut.

## 7. Conformité de périmètre et validations avant cochage

- [x] 7.1 Vérifier que les `38` baselines attendues sont respectées : `37` fichiers inchangés et `src/pixs/backend/README.md` modifié uniquement par append, avec aucun autre fichier source, test, configuration, dépendance ou artefact OpenSpec non prévu.
- [x] 7.2 Vérifier que les six nouveaux fichiers prévus correspondent exactement aux chemins publiés, que `tests/integration/test_feature_flag_postgres_source_integration.py` est le seul chemin d’intégration ajouté et qu’aucun modèle, réglage, app, migration ou test inventé hors périmètre n’apparaît.
- [x] 7.3 Vérifier que tous les fichiers texte produits sont UTF-8, utilisent des fins de ligne LF et ne contiennent aucun secret, credential, valeur de connexion, donnée réelle ou sortie SQL sensible.
- [x] 7.4 Vérifier la cohérence entre proposal, design, tâches, code, tests et README, en confirmant que ce change reste une première livraison partielle de `R4` sans revendiquer administration, audit, corrélation, convergence des rôles, runtime activation, garde de build ou accès multi-tenant.
- [x] 7.5 Exécuter la validation stricte du change avant cochage, corriger seulement en cas d’échec réel, puis exécuter la validation stricte canonique et vérifier qu’aucune norme `feature-flags` n’est ajoutée ou modifiée.

Note de séquencement : cocher chaque case seulement après preuve observée ; après tous les cochages, exécuter le strict post-cochage, obtenir une autorisation distincte pour l’archive, exécuter le mandat d’archive, produire et vérifier le `STATISTIQUES.md` post-archive avec un mandat séparé, puis seulement déclarer le cycle `TERMINÉ`. Aucun archivage ni rapport statistique ne fait partie d’une case pré-cochage.
