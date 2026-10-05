# Preuve partielle honnête initiale validate/resolve

## Why
`reference-composition Preuve reproductible` exige une preuve versionnée graphe/contrats/profils/contrôles sans secret. Le pipeline `discover/validate/resolve` pur existe et est déterministe en mémoire, `compose` sans attestations refuse, mais aucune preuve sérialisée/versionnée des contrôles réellement exécutés n'est distribuée. Il s'agit d'une absence implémentable, non d'une incohérence.

## What Changes
- Helper pur `build_initial_proof` composition initiale seule, caller fournissant explicitement le tuple exact des 3 textes déclaratifs, avec `OFFICIAL_IDS/REQUIRED_IDS` existants.
- Preuve interne JSON canonique `PROOF_VERSION 0.1.0` + `COMPOSITION_VERSION` existante, résultats RÉELS `discover/validate/resolve` seuls, `partial true`, `activated false`, `globally_compatible false`, profils/conformité NON évalués.
- Refus fermés génériques sans contenu brut/hash/echo, seules données déclaratives validées `id/version/kind/graphe`.
- Aucune attestation/compose/activation/P0/readiness/DB/secret/serveur, aucune copie SDK ni modification pipeline, aucun contrat nouveau.

## Capabilities
### New Capabilities
Aucune.
### Modified Capabilities
- `reference-composition` : premier jalon strict `Preuve reproductible`, sous-ensemble preuve partielle initiale seule, reprise normative inchangée.

## Impact
Un helper pur, deux tests futurs, un append README seul. Aucune norme réécrite, aucune activation.
