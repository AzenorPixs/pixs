## Context

B04 et ObjectMetadataV1 normatifs ; ports et annexes dans bulk-operations ; verifier et port statique UNAVAILABLE dans staging ; check_authority et resolve_governance six clés dans trusted_ports ; snapshots dans runtime_contracts ; pattern asyncio wait/close/cancel dans pg_connectivity. Aucun provider qualifié livré. B01/B02/B03 inchangés.

## Goals / Non-Goals

Composer la lecture réelle sous contrôles actuels avant worker. Snapshots en arguments non invocatoires. Aucune donnée remise avant intégrité positive ; aucune qualification production.

## Decisions

- Contrôles actuels : trusted_ports exact imposé ; server_context opaque non inspecté ; operation_reference str opaque serveur ; check EXECUTE avec resource_reference égale à object_reference attendu ; gouvernance résolue après ALLOW sur contrat ObjectMetadataV1 complet avec classification_reference, références policy_reference/policy_version opaques et SemVer ; réponse six clés strictes ; resolved_context identique à l'autorité courante ; policy/PolicyV1, profile quinze champs et obligations tuple exact capturés immuables. Types avant comportement/parsing/comparaison/I-O.
- Gouvernance liée au contrat : RESOLVED couvre réellement ObjectMetadataV1 attendu car le contrat transmis est ce metadata, pas un MappingDescriptor détourné ; aucun rapprochement avec data_asset_id/confidentiality ; six clés conservées strictement.
- Factorisation : helper privé commun d’invocation et de validation profonde complète de GovernanceResolutionV1 dans trusted_ports ; resolve_governance B01 conserve ses gardes MappingDescriptorV1 et délègue uniquement la partie commune ; méthode privée commune _resolve_governance_owned après validation et capture ObjectMetadataV1 dans le lecteur ; staging importe déjà trusted_ports donc aucun cycle ; lecteur importe les deux ; modification réalisée sous mandat CAB distinct.
- Async : API asynchrone privée, deadline UTC et asyncio.Event exacts hors payload ; asyncio.wait et attente concurrente du signal avec échéance monotone/UTC et max_runtime_seconds existant ; aucun champ PolicyV1 ni limite numérique nouvelle ; refus sur capacité incompatible sans repli synchrone.
- Qualification : résolveur serveur qualify lié instance/version, capturé statiquement puis appelé ; binding privé IMMUTABLE avec cancellation ; refus sans qualification ; contrôles metadata et flux conservés ; synthétique non productif.
- Non-remise : résultat mécanique du vérificateur uniquement, pas de copie complète ; fermeture itérateur, tâches et vérificateur sur chaque sortie dont timeout/cancellation/exception ; capacité structurelle historique reste UNAVAILABLE dans son module.
- Réutilisation et B01 : new_object_integrity_verifier exact, gardes B02, PolicyV1 existant, tenant explicite, CSV/NDJSON seuls, profils préparatoires et Record inchangés, aucune route ni seuil inventé.
- Tests : appels réels d'un provider synthétique déclaré, bornes, versions divergentes, authority/governance refusés, types hostiles, absence de fuite/effet après refus, fermeture prouvée.
- PostgreSQL : non applicable si aucun SQL ajouté ; prouvé par absence d'import ORM sous gardes positives, sans test SQL artificiel ; ne qualifie pas la production.

## Validation

Compiler les quatre Python concernés ; unitaires et intégration fraîche ; régressions regroupées bornées ; strict change/global ; périmètre/UTF-8/LF avant archive unique et STATISTIQUES distincte. Compatibilité B01 vérifiée par conservation du comportement resolve_governance MappingDescriptor, suites trusted_ports et staging rejouées, aucun champ Record modifié.

## Risks and Limits

Production indisponible sans provider et garantie réellement qualifiés. Aucune norme nouvelle requise au-delà de Frontière du contrat : signatures Python et composition du résolveur sont des choix d'implémentation sous schémas logiques ; si un reviewer exigeait un champ public nouveau, le point exact serait cité au lieu d'une promesse circulaire — aucun tel point n'est introduit ici.

## Précisions approuvées du contrat privé

La signature reçoit explicitement expected_policy, policy_reference et policy_version, références serveur validées avant I/O. Le résolveur serveur déclaré expose qualify asynchrone avec server_context, object_reference et version_reference. Son résultat privé figé porte le provider réel et les méthodes stat_private/iter_bytes capturées ; des indicateurs déclaratifs seuls ne constituent pas une qualification. Le résolveur est la frontière de qualification serveur effectivement invoquée après les contrôles actuels.

Le délai monotone restant est dérivé des échéances UTC et expirations existantes. Une horloge UTC actuelle est consultée après les I/O : le paramètre now initial ne devient pas une horloge figée. Les opérations et la fermeture respectent ces bornes et le signal asyncio.Event ; aucune valeur numérique de production n’est ajoutée. Les motifs de fermeture doivent appartenir au contrat réel du vérificateur existant.

Le helper commun réutilise toute la validation profonde existante de la réponse, après capture du contrat spécifique à chaque entrée ; il ne se limite pas à un préfixe superficiel. Aucun import inverse de staging n’est introduit. Le résultat ne contient jamais les octets lus.
