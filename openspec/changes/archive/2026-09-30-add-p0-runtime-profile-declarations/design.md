# Design — profils déclaratifs purs

## Context

La pile de référence reste Django/PostgreSQL/TanStack ; les contrôles backend restent ready=False. Ce change ne rend pas le runtime opérationnel.

## Goals / Non-Goals

Représenter explicitement les cinq dimensions exigées par la norme. Ne lancer aucun service, ne charger aucun environnement, ne vérifier aucune disponibilité réelle et ne définir aucun profil obligatoire : les exemples de profils de la norme sont facultatifs.

## Decisions

RuntimeProfile est une dataclass frozen à cinq champs : name, guaranteed_capabilities, required_dependencies, limitations, disabled_capabilities. Le nom est str exact non vide ; les quatre collections sont des tuples exacts de str exactes non vides, sans doublons. Les tuples vides déclarent explicitement aucune entrée. Aucune conversion, trim ou valeur implicite. Une capacité ne peut être simultanément garantie et désactivée.

validate_runtime_profile exige le type exact et valide la déclaration, retourne True ; elle ne prouve ni activation, ni présence de dépendance, ni conformité de sécurité réelle. Toute entrée invalide lève ValueError avec message constant sans valeurs. Les types sont vérifiés avant hash/comparaison et les sous-types refusés. Aucun générateur de profil, service, état ready ou raccord runtime.

## Risks / Trade-offs

Une déclaration mensongère ne devient pas une preuve opérationnelle. Les imports restent stdlib uniquement, compatibles Python3.11. Les vérifications P0, secrets, persistance, HTTP, déploiement et invariants au runtime restent distincts.

## Validation

Tests de champs, immutabilité, collections vides, noms opaques, doublons, contradictions, sous-types et protocoles hostiles. Exemple docstring exécuté et sous-processus import pur sans Django ; régressions unitaires/integration séparées, AST3.11, UTF8/LF, strict OpenSpec.
