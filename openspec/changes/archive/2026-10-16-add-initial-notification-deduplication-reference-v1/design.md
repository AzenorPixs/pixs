# Conception — NotificationDeduplicationReferenceV1

## Forme et frontière

Un module interne nouveau expose uniquement NotificationDeduplicationReferenceV1 et validate_notification_deduplication_reference. Le profil est une dataclass frozen=True, sans défaut ni méthode applicative, avec deduplication_key: str puis perimeter_reference: str. Le constructeur reste structurel ; le validateur ferme la frontière. Python >=3.12 et bibliothèque standard uniquement, avec les diagnostics existants.

## Validation

Le candidat doit être du type exact du profil, avant toute lecture d'attribut. Chaque champ doit être une str exacte non vide, avant toute méthode sur sa valeur. Les sous-classes sont refusées. Espaces, Unicode et casse sont conservés ; aucune normalisation, limite de longueur ou unicité n'est ajoutée. Deux profils aux mêmes références restent structurellement valides.

Les diagnostics utilisent VALIDATE, des éléments statiques sous notification_deduplication_reference., et des messages fixes sans écho. Ils sont triés et dédupliqués. Aucun appel de méthode d'une valeur étrangère, aucune résolution de périmètre, aucun I/O, environnement, processus, DB, envoi, Job, stockage ou garantie d'effet unique. Les modules et contrats existants restent inchangés.

## Tests et preuves

Les tests unitaires couvrent les références exactes, vides, étrangères et sous-classes, les objets hostiles, l'immuabilité, l'ordre et l'unicité des diagnostics, leur stabilité et l'absence d'écho. Ils vérifient des frontières fonctionnelles et ne recopient pas le validateur.

L'intégration lance un processus frais -I -B, sous environnement minimal, avec gardes d'écriture, réseau, processus, environnement et imports DB. Des contrôles positifs prouvent que ces gardes bloquent, puis leurs compteurs sont remis à zéro avant l'import et les validations ; un marqueur fixe confirme la réussite. Les artefacts éphémères restent dans la racine du projet et sont nettoyés.

Trois compilations Python sont mandatées séparément. Les tests utilisent unittest via le Python du projet et des PYTHONPATH explicites, sans installation. Les suites existantes de notifications constituent les régressions applicables. Chaque commande et fichier garde un mandat CAB unitaire et une preuve native.

## OpenSpec et publication

Le delta MODIFIED reproduit exactement les deux exigences du canon publié ; aucun texte canonique n'est modifié par ce change. Strict ciblé du change et de notifications : code 0 requis. Le global standard et le global strict sont conservés avec leurs codes réels. Les avertissements de longueur déjà présents dans la référence commune avant les travaux restent signalés, sans prétendre à une réussite stricte CLI lorsqu'elle retourne 1 ; la longueur n'est pas un critère de qualité selon le prompt. Aucun ERROR nouveau ni divergence normative n'est admissible.

Après preuves et tâches cochées, acquérir l'exclusion d'intégration, revalider la référence combinée, puis archiver avec --skip-specs. Vérifier l'archive et publier avant de libérer l'exclusion. Produire ensuite STATISTIQUES.md par mandat distinct, avec six sections, UTF-8/LF et totaux cohérents, avant le gate de livraison.
