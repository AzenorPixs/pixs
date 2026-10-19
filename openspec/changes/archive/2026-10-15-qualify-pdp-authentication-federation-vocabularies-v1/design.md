# Design — qualify-pdp-authentication-federation-vocabularies-v1

## Contexte normatif
Référence canonique : `openspec/specs/authorization-engine/spec.md`, exigence `Assurances et faits du profil PDP minimal fermé v1` et ses deux scénarios. Les deux enums exactes `AuthenticationAssurance` (`SINGLE_FACTOR | MULTI_FACTOR | PHISHING_RESISTANT`) et `FederationTrust` (`UNTRUSTED | TRUSTED | STRONGLY_BOUND`) existent déjà dans `src/pixs/core/authz/policy.py`. Ce change qualifie leur conformité, sans norme nouvelle.

## Réutilisation sans duplication
Réutilisation exclusive des classes uniques de `policy.py`, partagées via la façade `pixs.core.authz`, `decision` et `assurance_mapping`. Aucun nouvel Enum, aucune copie de valeurs, aucune façade créée ou modifiée, aucun helper de production. Séparation stricte : l'ordre sémantique existant chez les consommateurs (`decision._ORDERS`, `assurance_mapping._ORDINAL`) reste hors Enum ; les Enum restent non ordonnables (`lt/le/gt/ge` refusés). Aucun nouvel ordre introduit.

## Tests unitaires dédiés (futurs)
Un seul fichier `tests/unit/test_authentication_federation_vocab.py`, `unittest` et stdlib seule. Pour chaque Enum : ensemble exact des noms/valeurs et absence d'alias, aller-retour `Enum(name)` / `Enum[name]`, type `str` et `name == value`. Refus sans défaut : valeurs inconnues, casse, espaces, types (`None`, `int`, `bytes`), appel sans argument (`TypeError`), membres cross-dimension et enums étrangères (`ValueError`). Identité distincte des trois classes (`IdentityAssurance`, `AuthenticationAssurance`, `FederationTrust`).

## Tests d'intégration dédiés (futurs)
Un seul fichier `tests/integration/test_authentication_federation_vocab_integration.py`. Processus enfant frais via `sys.executable -B -I` avec chemin `src` explicite ; gardes installées avant imports bloquant `DB/Django`, `socket` et écriture observable. Vérification de l'identité des deux classes dans les quatre consommateurs (`policy`, façade, `mapping`, `decision`) et refus d'une valeur étrangère, sans authentification, session, audit, DB ni effet.

## Vérifications prévues (après réservation)
Compilation ciblée avec `cfile` exact `tests/unit/__pycache__/cismp3-authentication-federation.pyc` et équivalent intégration, après extension atomique. Exécution `unittest -B` avec `PYTHONPATH=src:tests/unit` via `/home/devops/datas/pixs/.venv/bin/python3`, car `test_pdp_time` importe `test_pdp_decision` comme module voisin. Cette adaptation est locale au processus, sans installation ni modification source. Preuve `cismp3-385248fa305745` : 96 tests OK, exit natif 0, après échec d'import `cismp3-b2e4427a2df440` conservé puis prévol récupéré `cismp3-fef311ebf24e44`. Régressions PDP (`policy`, `decision`, `time`, `audit`), `mapping` et `IdentityAssurance`. Empreintes production `authz` avant/après inchangées. Delta `MODIFIED` mot pour mot du canon. Validation ciblée stricte via `/home/devops/.local/npm/bin/openspec validate qualify-pdp-authentication-federation-vocabularies-v1 --strict --json` puis globale `--all --json` ; avertissements historiques tracés sans reformulation normative.

## Concurrence et fin
Deux phases : préparation OpenSpec stable avec `/ready` permettant l'intégration de CISMP1 ; tests après libération des ressources et `/extend` + `/reconcile` sur référence fraîche. Fin sous exclusion intégration : revalidation, archive avec `--skip-specs` car delta identique au canon, rapport `STATISTIQUES.md` distinct, `gate/disarm/release` puis retour au cycle parent. Aucun succès promis, aucune tâche cochée ici.
