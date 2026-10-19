# Conception — B09

## Statut

PRÉPARATION_DOCUMENTAIRE_CONDITIONNELLE. Le dossier est demandé ; ses choix encore ouverts et son implémentation ne sont pas approuvés implicitement. La présence des fichiers ne signifie pas prêt à coder.

## Contexte actuel

Des structures, dépôts PostgreSQL et façades bornées existent ; le dernier sous-lot couvre IMPORT ATOMIC_PER_CHUNK/REJECT. Le catalogue prévoit un complément du runtime, pas une recréation des profils ou records déjà livrés.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

Sources et périmètres consultés :

- [src/pixs/backend/README.md](../../../src/pixs/backend/README.md).
- [src/pixs/backend/bulk_server_apply.py](../../../src/pixs/backend/bulk_server_apply.py).
- [src/pixs/backend/bulk_runtime_repository.py](../../../src/pixs/backend/bulk_runtime_repository.py).
- [src/pixs/backend/bulk_server_admission.py](../../../src/pixs/backend/bulk_server_admission.py).
- [src/pixs/backend/bulk_streaming_import.py](../../../src/pixs/backend/bulk_streaming_import.py).
- [src/pixs/backend/bulk_outbox_publication_repository.py](../../../src/pixs/backend/bulk_outbox_publication_repository.py).
- [src/pixs/backend/models.py](../../../src/pixs/backend/models.py).
- [src/pixs/kernel/jobs.py](../../../src/pixs/kernel/jobs.py).
- [src/pixs/kernel/event_registration.py](../../../src/pixs/kernel/event_registration.py).
- [src/pixs/kernel/event_contract.py](../../../src/pixs/kernel/event_contract.py).
- [src/pixs/core/command_metadata.py](../../../src/pixs/core/command_metadata.py).

## Architecture et frontières

Compléter les façades et dépôts Bulk existants par les ports propriétaires et transactions déclarés. Réutiliser les profils, records, migrations, baux et checkpoints livrés ; distinguer validation, admission, effet et résultat durable. Rattacher chaque effet à autorité/gouvernance/tenant courants, conserver atomicité du mode choisi et reprise idempotente.

Périmètre propre à ce lot : Admission, progression, annulation/résultats sous contrats publiés, idempotence durable et tenant ; modes qualifiés seulement.

## Choix déjà fixés et alternatives

Les décisions validées dans les contrats sources sont conservées, y compris formats, algorithmes, valeurs, rôles et alternatives rejetées. Elles ne sont pas rouvertes sous prétexte d’un nouveau dossier. Les plafonds d’un auxiliaire, collecteur, validateur ou travail ne deviennent pas un budget général du PA/PBO.

Les modalités concrètes encore ouvertes ne reçoivent pas de valeur de défaut inventée. Une bibliothèque, un provider ou une dépendance présent dans DEVOPS n’est ni sélectionné ni qualifié. Les références normatives complètes sont dans requirements.md ; les mentions historiques qu’elles contiennent ne décrivent pas des effets réalisés pendant cette préparation.

## Barrières de conception avant réalisation

Routes/schémas/API majeures et conditions d’exposition ; annoncer seulement les modes effectivement qualifiés.

Ces barrières n’empêchent pas la rédaction conditionnelle du dossier. Avant tout code, les choix ayant un impact réel sur sécurité, périmètre, compatibilité, exploitation ou ressources devront être soumis avec conséquences et recommandation ; pour PA/PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages. Les paramètres déjà décidés sont à qualifier, pas à remplacer par une nouvelle décision supposée.

## Dépendances et interfaces

- [add-protected-core-http-commands-and-queries](../add-protected-core-http-commands-and-queries/proposal.md).
- [complete-bulk-owner-admission-and-import-mapping](../complete-bulk-owner-admission-and-import-mapping/proposal.md).
- [integrate-bulk-worker-jobs-and-cancellation](../integrate-bulk-worker-jobs-and-cancellation/proposal.md).



Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent explicitement incomplètes tant que les obligations manquent.

## Vérification future

PostgreSQL isolé réel, succès/refus du propriétaire, modes et conflits applicables, rejeu, annulation concurrente, perte de bail, commit incertain, source/mapping modifiés et résultats réautorisés sans fuite.

Sortie du lot : Rejeu et réponse cohérents ; accès hors contexte refusé ; en cours distinct de succès ; mode absent non annoncé.

Exercer tous les scénarios et clauses applicables des blocs sources, y compris renvois normatifs ; un scénario non applicable doit être motivé par le profil réel. Les contrôles applicatifs suivent l’exception Super Admin du canon dans son seul périmètre, sans fabriquer audit, mesure, signature ou effet absent.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données/états doit préciser propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation/restauration. Aucun retour arrière destructeur, remise à zéro, arrêt de service ou changement de droits implicites.

## Limites du dossier

Pas de PASS actuel ni d’achèvement produit revendiqué. L’autorisation de préparation ne permet ni d’activer la capacité dans P0 ni d’utiliser un compte connecté, publier un artefact ou envoyer une notification réelle.
