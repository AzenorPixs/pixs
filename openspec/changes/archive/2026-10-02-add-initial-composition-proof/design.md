# Conception preuve partielle initiale

## Context
`composition.py` pur `discover/validate/resolve/compose`, `resolve` public `edges/order/diagnostics` seuls, `CompositionResult` sans sérialisation, `composition_initial.py` constantes seules, manifests connus sans secret, tests existants preuve mémoire seule.

## Goals / Non-Goals
But : sérialiser honnêtement les seuls contrôles `discover/validate/resolve` initiaux réellement passés. Non-buts : attestation, compose, activation, P0, conformité, profils, readiness, DB, secret, hash brut, echo payload.

## Decisions
- `build_initial_proof(manifest_texts)` exige tuple exact 3 `str`, refuse type invalide/3 requis/duplicates/extra/IDs invalides/dép manquante/non-resolve par erreur générique `cause None`.
- Appelle réellement `discover` puis `validate(texts, official_ids, required_ids)` puis `resolve(manifests)` public seul ; `warnings` et `ConformityAttestation` jamais utilisés comme preuve.
- Ne conserve que `id/version/type` validés, déclarations de capacités et contrats validées réduites à `id/version`, `order/edges` résolus réels triés. Aucun diagnostic brut (ni message, element, constraint, repr ou cause) : un refus est une erreur générique, pas une preuve réussie. La portée effectivement évaluée ne contient que components/capabilities/contracts ; conformity/profiles et les autres dimensions existantes sont explicitement non évaluées, aucune reprise trompeuse de EVALUATION_SCOPE du dataclass.
- Entrée strictement tuple de trois str exacts, chacun non vide et limité à 64 KiB UTF-8 ; identifiants exactement REQUIRED_IDS sans extra ni doublon, types initiaux KERNEL/MODULE/MODULE. Aucun accès à un fichier, aucun horodatage, aucun effet à l’import ou à l’appel ; aucun champ opaque/name/fallback retenu. La taille est une borne interne, aucune nouvelle variable de configuration.
- Résultat str JSON canonique seul, graphe/order observés et déclarations minimales triées par ID. Contrôles discover/validate/resolve réellement passés seulement ; pas de warnings inventés car API publique resolve ne les expose pas.
- JSON canonique trié `sort_keys/separators`, `PROOF_VERSION 0.1.0`, `COMPOSITION_VERSION 0.1.0`, `partial true`, `activated false`, `globally_compatible false`. Hash éventuel seulement de ce JSON filtré, jamais des textes.
- Déterminisme : deux calls identiques byte-identiques hors horodatage absent, permutation mêmes manifests ordre trié identique et contrôles équivalents.

## Files
`src/pixs/backend/composition_proof.py`, `tests/unit/test_initial_composition_proof.py`, `tests/integration/test_initial_composition_proof_integration.py`, append seul `src/pixs/backend/README.md`.

## Validation
Strict avant/après, unit subprocess isolés sans settings/setup/FS/PG/socket, intégration pipeline réel joint, AST 3.11 UTF-8/LF, périmètre strict.
