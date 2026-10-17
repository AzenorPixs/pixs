# N06 — Kit minimal de conformité des contrats P0

## Pourquoi

`testing` #2/#3 exige un Developer Kit et des suites versionnées par contrat, ainsi que l’exclusion d’un provider dont la conformité obligatoire manque/expire/échoue. `developer-experience` exige le parcours local de l’exemple P0. Le kit actuel valide des manifests ; [validators.py](../../../src/pixs/developer_kit/validators.py) documente explicitement qu’il n’est ni kit complet ni preuve de conformité production. [example/demo.py](../../../src/pixs/example/demo.py) est une démonstration pure.

## Préparation validée

Le développeur a validé ce dossier dédié le 17 octobre 2026 dans l’audit transversal P0. [Conception, responsabilités et critères](design.md). Aucune implémentation autorisée.

## Capacités et deltas

Aucun delta normatif nouveau prévu ; réalisation du canon existant, références dans requirements.md et skip_specs explicite.

Les deltas proposés restent dans le change ; aucune synchronisation ni archive pendant cette préparation. Les paramètres encore ouverts ne sont pas réputés approuvés.

## Dépendances et intégration

Voir les responsabilités et conditions de [design.md](design.md) et le [plan global courant](../define-first-installable-pbo-profile/plan-global-preparation.md). Les producteurs précoces de contrats, les conditions d’activation et la recette finale restent distincts.

## Impact

Préparation documentaire du chemin P0 ; pas d’activation d’option extérieure au profil, d’outil installé, de serveur sélectionné implicitement, de clé réelle, de migration ou de publication. Les tâches futures nécessitent une autorisation de réalisation distincte.

## Dépendances après audit transversal P0

[C06](../add-protected-core-http-commands-and-queries/proposal.md), [C07](../activate-reference-runtime-composition/proposal.md), [C09](../add-reference-worker-scheduler-and-event-delivery/proposal.md), [C10](../enforce-core-data-governance-and-lifecycle/proposal.md), [C11](../compose-modular-frontend-with-core-api/proposal.md), [C14](../add-essential-pbo-pzt-and-dns-modules/proposal.md), [N01](../add-pbo-security-quarantine-and-revocation/proposal.md).

Les conditions d’activation et la construction des résultats sont séparées de cet ordre de préparation ; aucun cycle inverse vers la recette finale.
