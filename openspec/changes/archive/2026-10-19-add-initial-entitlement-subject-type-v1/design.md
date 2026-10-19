# Conception du vocabulaire EntitlementSubjectType

## Contexte et décision

Le modèle logique Entitlement.subject_type de TECHNICAL.md §25.2 énumère INSTALLATION, PLATFORM, TENANT et SCOPE. QuotaPolicy.subject_scope possède sept portées et constitue un contrat différent. Le canon quotas-entitlements conserve toutes ses exigences, notamment l'absence d'élargissement par scope et l'exception applicative Super Admin.

Une Enum Python standard sans mixin str expose exclusivement ces quatre membres avec leurs valeurs identiques. L'import public est pixs.kernel.entitlement_subject_type. Le module déclare __all__ = ["EntitlementSubjectType"] ; la façade pixs.kernel reste inchangée. Le constructeur Enum refuse une valeur non déclarée sans normalisation ni alias.

## Limites

Le vocabulaire est passif. Il ne vérifie aucun rattachement, contexte, contrat, héritage ou droit. Le membre SCOPE ne rend jamais un scope enfant admissible de lui-même. Aucun validateur métier, provider, résolution, persistance, transition, accès Core, base, réseau, environnement ou processus n'est ajouté. Les droits applicatifs et dérogations restent hors de ce profil structurel. Aucun P0 complet ni O15 implémenté n'est annoncé.

## Validation

Tests unitaires du contrat fermé, des valeurs et types rejetés sans normalisation et de l'export public. Test d'import dans un processus isolé -I -B avec environnement synthétique, gardes et contrôles positifs d'écriture, réseau, processus, environnement, base et Core ; contrôle d'absence de lecture métier après import. Réutilisation du patron ComponentType existant. Compilation des trois fichiers, régression ciblée des vocabulaires voisins, validation OpenSpec ciblée et globale. PostgreSQL et frontend sont sans objet : aucun comportement les concernant n'est introduit.

## Livraison

Vérifier UTF-8/LF, contenu exact et absence d'effets hors périmètre. Archiver uniquement après preuves, sous mandat distinct ; produire et vérifier STATISTIQUES.md après publication technique et avant gate, livraison et arrêt ciblé de CISMP1. Aucun Git, déploiement ou change suivant.
