# Tâches — Unité de persistance JobRecord pour les travaux

## 1. Persistance JobRecord

- [x] 1.1 Valider strictement le change, les 76 spécifications canoniques et les éléments OpenSpec avant le code.
- [x] 1.2 Éditer models.py selon le contrat et les frontières de design.md : JobRecord treize champs, _validate_job_version, Meta constraints, __all__ ; classe des fanions préservée octet pour octet.
- [x] 1.3 Ajouter migrations/0002_job_record.py dépendant de 0001, CreateModel réversible avec PK serialize=False et constraints.
- [x] 1.4 Ajouter et exécuter les tests unitaires offline (cas ciblés, validate_unique=False et validate_constraints=False, preuve zéro connexion, save sans full_clean, message fixe sans écho).
- [x] 1.5 Ajouter et exécuter le test d'intégration PostgreSQL réel : loader borné du processus de test, schéma unique, forward 0001/0002, roundtrip JSON, refus CHECK, limite SemVer DB, reverse 0002, tables FeatureFlag d'origine inchangées, cleanup et connexions fermées, résultat fermé `real_pg=True` distinct du marqueur du harnais sûr.
- [x] 1.6 Adapter la seule assertion d'inventaire du harnais fanions aux deux modèles ; compiler les cinq fichiers Python ; exécuter la régression des 20 modules (111 tests), les deux tests PG existants et les nouveaux tests (comptes natifs séparés) ; vérifier UTF-8/LF et l'intégrité byte à byte de settings.py, apps.py, 0001 et de la classe des fanions, ainsi que les 120 empreintes de référence inchangées hors models.py et hors l'assertion du harnais fanions adaptée sous mandat distinct.
- [x] 1.7 Valider strictement le change, les spécifications canoniques (76) et les éléments OpenSpec après le code et les tests, avec effet jobs attendu +0/~0/-0/→0.

L'archivage et STATISTIQUES.md nécessitent des décisions et mandats CGPT distincts après preuve des tâches.
