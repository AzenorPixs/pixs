# Design — Déclaration passive d’enregistrement d’événement v1

## Contexte

Les trois exigences préparatoires de `openspec/specs/events/spec.md` font autorité. Le change les implémente sans ajouter de norme. Les comportements runtime et les garanties transactionnelles existantes restent hors de cette unité.

## API et représentation

Le seul module neuf exporte exactement `EventRegistrationDeclarationV1` et `validate_event_registration_declaration`. La dataclass utilise `frozen=True` et `slots=True`, sans défaut, conversion ou `__post_init__`. Ses seuls champs, dans cet ordre, sont `owner_id: str`, `entry_id: str`, `event_contract: DomainEventContract | IntegrationEventContract`. Les objets portés sont conservés par identité.

Les valeurs peuvent être construites par un appelant de confiance ou des fixtures synthétiques ; la validation est explicite et séparée de la construction. Les exports de `pixs.kernel` et les modules existants ne sont pas modifiés.

## Validation fermée

Vérifier le type exact de la déclaration avant toute lecture d’attribut. Vérifier chaque identifiant par type exact `str` non vide, sans coercition ni normalisation ; les chaînes d’espaces sont conservées et restent non vides. Aucune existence, grammaire, longueur maximale ou convention d’identifiant supplémentaire n’est imposée.

Vérifier le type exact du contrat porté, puis appeler uniquement `validate_domain_event_contract` ou `validate_integration_event_contract` selon ce type. Les sous-classes et objets étrangers sont refusés avant tout accès à leurs attributs ou callbacks. Ne pas extraire les cinq champs du contrat, importer de parseur SemVer dans ce module ni affaiblir les validateurs existants. Leurs exceptions inattendues sont propagées, sans capture générale.

## Diagnostics

Les refus propres à la déclaration utilisent `Diagnostic` et `VALIDATE`, avec des textes fixes pour `event_registration.declaration`, `event_registration.owner_id`, `event_registration.entry_id` et `event_registration.event_contract`. Les diagnostics rendus par le validateur du contrat sont conservés. Retourner une liste fraîche, triée et dédupliquée par `(element, constraint, message)`. Aucune valeur brute, conversion de l’entrée ni état mutable partagé.

## Tests et effets

Les tests unitaires couvrent les deux natures de contrat, les trois champs figés, la préservation des objets, les identifiants exacts, les étrangers et sous-classes hostiles, le contrat invalide, la réutilisation des validateurs, les diagnostics stables et l’absence de callback ou d’écho. Les régressions rejouent les deux modules EventContract existants, sans annoncer leur nombre avant exécution.

Un test en processus Python neuf vérifie la construction et la validation sous gardes explicites d’IO, réseau, environnement, horloge et processus, et l’absence d’import de fournisseur de base de données. Les chargements physiques normaux nécessaires à l’import ne sont pas assimilés à une IO applicative ; la portée exacte des gardes est déclarée et leurs sondes sont éprouvées. Aucun PostgreSQL réel ni secret n’est nécessaire.

## Compatibilité et périmètre

Bibliothèque standard et contrats publics existants seulement, Python `>=3.12`. Préserver les empreintes des contrats, diagnostics, SemVer, registre, exports du Kernel, anciens tests et canon `events`. Aucun changement de P0/B11, dépendance, configuration, README, autre source ou Git. La validité structurelle n’est jamais présentée comme un enregistrement ou un bus livré.
