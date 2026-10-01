## Context

Les exigences reference-runtime et runtime fixent Django/PostgreSQL et les rôles web, worker et scheduler d'un même artefact. Le socle actuel est une bibliothèque Python sans backend Django. Le développeur a autorisé les dépendances directes Django et psycopg ; cette autorisation ne couvre pas PostgreSQL, les secrets ou le déploiement.

## Goals / Non-Goals

Préparer une fondation vérifiable hors base : dépendances déclarées, configuration explicite, paquet unique, limites inspectables et tests synthétiques. Préserver Python >=3.11 et les fondations existantes.

Ne pas réaliser de modèles métier, migrations, vues, API, traitements worker/scheduler, frontend ou provisionnement. Ne pas présenter un contrôle Django hors base comme une preuve de service opérationnel, de persistance ou de conformité globale P0.

## Decisions

- Dépendances directes proposées : Django==5.2.17, série LTS compatible Python 3.11 et 3.14 ; psycopg==3.3.5, version documentée dans DEVOPS.md. Toute installation est un mandat distinct dans un environnement isolé du projet, jamais globale.
- Un seul paquet src/pixs/backend. Les seuls rôles acceptés sont web, worker et scheduler. local est un profil de déploiement et ne fait pas partie de cette sélection de rôles.
- PIXS_PROFILE désigne la sélection explicite du rôle dans la configuration fournie au backend. Aucun rôle par défaut, déduction depuis les imports ou choix de pile selon les paquets installés.
- La configuration Django utilise exclusivement le moteur PostgreSQL. Aucun fallback SQLite ou stockage mémoire. Les tests ne doivent ouvrir aucune connexion PostgreSQL.
- Aucun fichier .env ou project.env n'est chargé. Les tests fournissent uniquement une configuration synthétique en mémoire et des gardes contre toute connexion. Aucune variable sensible réelle de l'environnement n'est inspectée.
- La résolution des références externes de secrets et le provisionnement réel restent exclus. Aucune valeur de secret réelle ne doit apparaître dans le code, les diagnostics ou les rapports. Une configuration obligatoire absente échoue fermé, sans défaut de secret ni reprise de sa valeur dans un message.
- L'inspection des rôles présente les capacités non implémentées comme indisponibles ; elle ne doit pas déclarer de serveur, worker, scheduler, API ou persistance opérationnels sur la seule base d'un profil sélectionné.
- Les deltas OpenSpec reprennent les exigences canoniques concernées sans nouvelle exigence normative. Les détails ci-dessus sont les décisions d'implémentation de cette fondation partielle, pas de nouveaux profils ou garanties de production.

### Précision de la frontière préparatoire

La fondation expose `SettingsTemplate` et `build_settings_template(*, profile, database, allowed_hosts, secret_key_ref, database_password_ref)`. Le rôle fourni explicitement correspond à la configuration `PIXS_PROFILE` ; aucun environnement réel n'est consulté. Le mapping non secret `database` contient uniquement `name`, `user`, `host` (chaînes non vides) et `port` (entier de 1 à 65535, hors booléen). `allowed_hosts` est une séquence explicite non vide de noms sans wildcard. Une entrée absente, inconnue ou mal typée est refusée sans reproduire de valeur.

Les références obligatoires réutilisent `SecretReference` du Kernel, restent distinctes et séparées des valeurs Django `SECRET_KEY` et `PASSWORD`. Le gabarit est immuable, validé à la construction et porte un état `ready` toujours faux. Son moteur est exclusivement `django.db.backends.postgresql` ; les réglages non secrets fixent `DEBUG=False`, `USE_TZ=True`, `TIME_ZONE=UTC` et `INSTALLED_APPS=()`. Aucun fournisseur ni résolution de secret n'est ajouté.

Les fonctions publiques `check_template` et `inspect_roles` restent pures et décrivent les rôles web, worker et scheduler comme indisponibles. Elles ne révèlent aucune valeur de configuration et ne modifient pas l'état global Django. La conversion du gabarit vers des réglages Django avec valeurs synthétiques est réservée au harnais de tests, sans fonction publique de conversion dans le paquet backend. Chaque vérification Django s'exécute dans un sous-processus neuf avec `settings.configure`, `django.setup` et des gardes vérifiables contre toute connexion. Cette preuve hors base ne démontre aucune résolution de secret, persistance ou disponibilité de service.

## Validation

Tests unitaires et d'intégration dédiés avec configurations synthétiques, garde d'absence de connexion et rejet des profils/configurations incomplets ; vérifications Django hors base, syntaxe AST, UTF-8/LF, régressions du projet et validation OpenSpec stricte. Aucun résultat n'est présumé ; les commandes exactes seront soumises individuellement à CAB avec les exécutables DEVOPS.

## Risks / Trade-offs

Cette première fondation ne prouve pas les transactions, migrations, processus séparés ou références externes de secrets. Les changements ultérieurs nécessitent leurs propres spécifications et mandats. Une opération PostgreSQL requiert une autorisation explicite distincte, incluant le chargement de ses variables par le seul processus concerné si nécessaire.

## Migration / Rollback

Aucune migration de données et aucune opération externe dans ce change. Les seules modifications prévues concernent les dépendances, le nouveau paquet backend, sa documentation et ses tests ; les fondations existantes sont conservées. Un retour arrière des artefacts versionnés reste soumis aux autorisations applicables.

## Open Questions

L'implémentation et ses preuves restent à effectuer après préparation complète et validation stricte du change. La session s'arrête à 06h Europe/Paris ; un artefact préparatoire ne vaut ni tâche achevée ni autorisation d'archivage.
