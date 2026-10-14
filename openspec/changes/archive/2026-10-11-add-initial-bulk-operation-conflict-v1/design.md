## Context

Le canon bulk-operations ferme BulkOperationConflict v1 : exactement operation_id et conflict_strategy, explicitement fournis, immuables et purement mémoire. BulkConflictStrategy existe déjà avec REJECT, CREATE_ONLY, UPDATE_ONLY et UPSERT. Le patron BulkOperationFormat fournit une validation pure réutilisable sans modification des anciens profils.

## Goals / Non-Goals

Représenter et valider seulement les deux champs structurels. Aucun choix ou application de stratégie, résolution de référence ou de conflit, entrée/sortie, mutation, idempotence, autorisation, persistance, commande ou runtime import/export. Le contrat général d’import, dont le rejet par défaut, reste intégralement applicable. PA/PZT hors périmètre.

## Decisions

1. Créer un module interne avec dataclass frozen à deux champs sans défaut et deux exports locaux ; aucun registre, façade ou __init__ existant modifié.
2. Refuser tout candidat de type étranger ou dérivé avant lecture des attributs. Une sentinelle privée _MISSING représente les champs absents sans défaut de données.
3. Vérifier str exacte avant vérité, sans normalisation ni UUID ; vérifier BulkConflictStrategy exact puis identité avec les quatre membres canoniques, sans conversion ni égalité étrangère. Un objet fabriqué de même type hors membres est refusé.
4. Produire uniquement des diagnostics statiques VALIDATE, triés et dédupliqués, sans écho, mutation ou effet.
5. Neuf tests unitaires couvrent membres canoniques, opacité, champs obligatoires, immutabilité, objets étrangers/dérivés/hostiles/forgés/absents, ordre, indépendance et non-écho des diagnostics.
6. Un test en processus Python frais sous gardes à contrôles positifs vérifie absence d’écriture/lecture métier, réseau, processus, environnement, base et import concret pixs.core. Aucun changement des tests existants.

## Risks / Trade-offs

Ce profil ne prouve aucun comportement runtime. Les deux champs doivent rester explicites ; aucune stratégie par défaut n’est introduite dans ce profil. Le vocabulaire et tous les profils existants sont préservés. Python >=3.12, aucun outil ou dépendance ajouté.

## Migration Plan

Aucune migration ni activation. Trois compilations séparées, tests ciblés puis régressions et validation stricte du change. Delta identique au canon : archivage distinct --skip-specs après preuves, suivi d’un STATISTIQUES.md distinct avec six sections et totaux vérifiés.
