## Why

La pile de référence validée impose Django et PostgreSQL, tandis que le socle actuel ne contient pas encore de backend Django. Le développeur a explicitement autorisé Django et psycopg pour le backend P0. Cette évolution prépare une fondation minimale, sans prétendre réaliser l'ensemble du backend P0.

## What Changes

- Déclarer Django 5.2 LTS et psycopg 3 dans pyproject.toml en préservant la compatibilité Python >=3.11.
- Préparer un paquet backend Django commun aux rôles web, worker et scheduler, sélectionnés explicitement et inspectables, sans profil implicite.
- Documenter PIXS_PROFILE comme choix d'implémentation dans le design OpenSpec.
- Vérifier les réglages et limites avec des données synthétiques, sans connexion PostgreSQL, secret réel ou stockage de substitution.
- Préserver les invariants et les fondations déjà validées. Aucun modèle métier, migration, vue API ou traitement worker/scheduler n'est réalisé dans ce périmètre.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- reference-runtime : préparer la fondation de la pile Django/PostgreSQL déjà exigée, sans modifier l'exigence canonique.
- runtime : préparer la configuration explicite des trois rôles d'un même artefact, sans ajouter de rôle ni déclarer un runtime de production achevé.

## Impact

Fichiers d'implémentation prévus : pyproject.toml, src/pixs/backend/__init__.py, src/pixs/backend/settings.py, src/pixs/backend/checks.py, documentation ciblée du backend et tests unitaires/intégration correspondants. Les dépendances directes proposées sont Django==5.2.17 et psycopg==3.3.5 ; toute installation reste un mandat distinct, dans un environnement isolé du projet.

Exclusions : project.env, lecture de secrets réels, opération PostgreSQL, déploiement, installation globale, SQLite, Git, frontend, API, modèles et migrations. Les contrôles hors base ne prouvent ni la persistance ni le provisionnement de production. Aucun archivage ne sera autorisé avant les preuves applicables.
