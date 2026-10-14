# Proposition — Représentation déclarative interne partielle du contrat de notification

## Why

L'exigence canonique « Contrats et préférences déclarés » impose : « Chaque notification MUST suivre un contrat versionné avec destinataires, canaux, préférences et périmètre ; aucun canal implicite ni destinataire élargi sans règle déclarée. » (openspec/specs/notifications/spec.md). Le vocabulaire `NotificationChannel`, le vocabulaire `NotificationDeliveryState` et les deux contrôles déclaratifs de refus (canal, destinataire) sont livrés dans le Kernel ; aucune représentation structurelle du contrat versionné lui-même n'existe dans le code. Le versionnement de la représentation suit l'exigence canonique « Versionnement SemVer indépendant » (openspec/specs/contracts/spec.md). La présente unité est une représentation déclarative interne, partielle et en mémoire ; elle ne constitue ni un `ContractDescriptor` public enregistré, ni la preuve d'un runtime notifications complet.

## What Changes

- Ajouter `src/pixs/kernel/notification_contract.py` : dataclass `frozen` interne `NotificationContract` à cinq champs (version, destinataires, canaux, référence de préférence, référence de périmètre) et validateur structurel `validate_notification_contract` retournant des diagnostics fixes, selon le contrat technique détaillé dans design.md ;
- Ajouter un test unitaire et un test d'intégration borné ;
- Delta `specs/notifications/spec.md` MODIFIED reproduisant mot pour mot l'exigence « Contrats et préférences déclarés » et ses deux scénarios canoniques existants, sans scénario ajouté ni norme nouvelle.

## Impacts

- Aucun comportement runtime existant modifié et aucune source, test ou façade notification existant touché ; cette unité ne livre que la représentation déclarative interne et partielle du contrat, sans préférence riche, périmètre résolu, envoi, réessai, déduplication, lettre morte, audit réel ni classification de sensibilité ;
- Le changement canonique effectif attendu est nul (+0/~0/-0/→0) ; les exigences « Asynchronisme avec réessais bornés » et « Confidentialité et audit » restent non couvertes et non prouvées par ce change.
