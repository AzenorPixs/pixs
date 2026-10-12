## Context
Le validateur pur canonique est livré par le change précédent du même RUN. Le second change ajoute seulement sa persistance préparatoire approuvée.

## Goals / Non-Goals
Neuf TextField, operation_id PK locale, trois NULL seulement, aucun défaut métier ni relation FK. from_values accepte un dict exact explicite, en fait un snapshot validé et retourne un objet non sauvegardé. full_clean contrôle les neuf valeurs avant conversion, même sous exclude ; erreurs statiques sans écho. save conserve le comportement Django sans validation implicite. Aucun worker, transition, bail, retry, autorisation, résolution, Job, staging, import/export ou applicabilité par variante.

## Decisions
Classe dans bulk_operation_record.py, enregistrée par un seul import dans models.py ; __all__ préexistant inchangé. Migration 0003 dépendant de 0002, CreateModel seulement, enums gelés en littéraux. Neuf CHECK pour non-vide et appartenance, NOT NULL et PK ; le SQL ne prouve pas la grammaire SemVer ni un type Python exact.

## Validation
Cinq compilations, deux tests en processus frais sous gardes positives (ORM offline et inertie du harnais PG), 128 régressions. Deux commandes PG réelles distinctes : nouveau modèle et régression JobRecord. Secrets chargés exclusivement à l’intérieur des tests via les aides existantes, sortie JSON fermée sans exception/valeur ; schémas synthétiques possédés, search_path excluant public, migrations 0002→0003→0002, identités des deux anciennes tables inchangées, contrôle public, suppression et fermeture prouvées. Version serveur numérique mesurée. Strict du change avant/après, conformité et empreintes sans Git.

## Risks / Trade-offs
La validation Python doit rester explicite : save peut stocker une chaîne SemVer invalide mais non vide ; preuve négative DB et rejet full_clean attendus. La clé est locale à la table, sans promesse globale. Les aides PG réutilisent leur préfixe synthétique historique job_record_ sans association métier.

## Rollback
Revenir de 0003 à 0002 retire seulement la nouvelle table ; toute exécution sur des données réelles exige une autorisation distincte. Les tests limitent le retour à leur schéma synthétique.
