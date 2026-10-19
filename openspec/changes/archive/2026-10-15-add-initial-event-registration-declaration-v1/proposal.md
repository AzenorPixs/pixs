# Proposition — Déclaration passive d’enregistrement d’événement v1

## Why

La norme canonique `events`, validée et publiée en référence 15, définit le profil préparatoire `EventRegistrationDeclarationV1`. L’inventaire borné ne trouve pas sa représentation dans les sources événementielles examinées. Les contrats de domaine et d’intégration, leurs validateurs et les diagnostics sont déjà présents.

## What Changes

- Ajouter `src/pixs/kernel/event_registration.py` avec la déclaration figée à trois champs et son validateur structurel fermé.
- Conserver exactement `owner_id`, `entry_id` et l’objet `event_contract`, sans recopier les cinq champs du contrat porté.
- Réutiliser les deux validateurs publics de contrats existants ; aucune grammaire, convention de nommage ou validation SemVer parallèle.
- Produire des diagnostics `VALIDATE` stables, triés, sans valeur brute ni effet de bord.
- Ajouter deux fichiers de tests dédiés, unitaires et en processus frais.

## Capabilities

### Modified Capabilities

- `events` : qualification d’implémentation des trois exigences préparatoires existantes et de leurs cinq scénarios. Le delta `MODIFIED` les reprend mot pour mot, sans norme ajoutée, modifiée ou supprimée.

### Added Capabilities

- Aucune.

## Impact

Trois nouveaux fichiers applicatifs seulement : `src/pixs/kernel/event_registration.py`, `tests/unit/test_event_registration.py` et `tests/integration/test_event_registration_integration.py`. Les contrats, diagnostics, parseur SemVer, exports du Kernel et registre P0 existants restent inchangés. Python minimal `>=3.12`, aucune nouvelle dépendance, configuration ou opération Git.

## Validations

Trois compilations natives séparées ; tests dédiés et régressions des deux modules EventContract existants ; contrôles UTF-8/LF, périmètre et empreintes ; OpenSpec strict ciblé avant code, après tests et après cochage. L’intégration commune relève séparément le standard et le strict globaux, avec codes natifs et avertissements historiques explicites. Archivage et rapport statistique restent des mandats distincts après preuves.

## Limites

Cette représentation reste uniquement structurelle. Elle ne prouve ni admission du propriétaire, existence, résolution, légitimité ou sensibilité des références. Aucun enregistrement, abonnement, publication, livraison, payload, persistance, outbox, transaction ou bus runtime n’est livré. Le registre P0 reste fermé et B11 est préservé.
