# Conception — JobDeduplicationReferenceV1

## Contrat

Le module interne expose seulement `JobDeduplicationReferenceV1` et `validate_job_deduplication_reference`. Dataclass frozen, exactement `deduplication_key: str` puis `perimeter_reference: str`, sans valeur par défaut. Le constructeur représente les données ; le validateur contrôle la frontière.

Le candidat est contrôlé par type exact avant lecture d'attribut. Chaque champ est une chaîne exacte non vide avant tout appel de méthode. Aucune coercition, normalisation, limite de longueur ou comparaison d'unicité. Espaces, Unicode et casse sont préservés.

Les diagnostics existants utilisent VALIDATE, des éléments statiques sous `job_deduplication_reference.`, des contraintes/messages fixes, triés et dédupliqués sans écho. Aucune méthode d'une valeur étrangère, aucun I/O, environnement, processus, DB, envoi, Job, résolution de périmètre, rétention, réessai ni autorisation.

## Preuves

Tests unitaires : types étrangers et sous-classes, objets hostiles et sonde d'attributs, vides, conservation exacte, immuabilité, diagnostics stables et sans écho. Deux références identiques restent structurellement valides.

Intégration : processus frais -I -B sous environnement minimal ; gardes d'écriture, réseau, processus, environnement et imports DB, avec contrôles positifs avant remise à zéro. Aucun effet pendant import/validation. Artefacts temporaires dans la racine autorisée et nettoyés.

Trois compilations et tests unittest avec le Python déclaré dans DEVOPS.md. Régressions des profils JobCorrelation, JobState et notifications. Pas de PostgreSQL ou navigateur, aucune fonctionnalité persistante ni interface modifiée.

## OpenSpec et clôture

Le delta MODIFIED reproduit exactement les trois exigences jobs adoptées par la RSMP. Strict ciblé jobs et change requis sans erreur ni nouveau warning. Conserver les codes réels du standard global et du strict global, ainsi que les warnings préexistants de longueur sans les masquer. Aucun ERROR nouveau admis.

Après tâches prouvées et cochées, archiver avec --skip-specs sous mandat distinct. Revalider le référentiel après archive et publier par /publish sous les seuls accès utiles CAB resource-scoped-v1. Rapport STATISTIQUES.md sous son propre mandat après publication, six sections, UTF-8/LF, totaux vérifiés, puis gate, désarmement, libération et arrêt ciblé. Aucun commit ni push.
