# Conception journal local corrélé

## Context
errors.py grammaire UUID exacte avec nil/max, responses.py enveloppe existante, grep src sans traceparent ni trace ni W3C, source W3C trace-context consultée par CGPT. Trois manifests initiaux connus sans secret.

## Goals / Non-Goals
But : extraire contexte 00 déjà valide et correlation_id existant, émettre événement fixe localement observé. Non-buts : métriques/traces globales, propagation runtime, génération span/trace, tracestate, handler global, réseau, fichier, secret, timestamp, message libre, nouveau contrat.

## Decisions
- Parse seulement version 00 strict 55 chars, trace 32 hex minuscules nonzero, parent 16 hex minuscules nonzero, flags 00..ff avec sampled par masque 1 dont 09 valide, parent_id entrant.
- correlation_id UUID strictement identique existant y compris nil/max, errors.py non modifié.
- Événement fixe de contexte avec corrélation et composant connus uniquement, sans timestamp ni entropy ni valeur non maîtrisable.
- Retour unique write str vers sink caller explicite, StringIO réel en tests, échec ou retour partiel détecté diagnostic fixe sans brut sans relance.
- Mêmes IDs réellement émis sur trois composants connus, sans permutation arbitraire ni descripteur mélangé, parse invalide avant tout appel sink.
- Succès signifie écriture observée vers sink caller uniquement, pas livraison externe.
- Type exact avant len/encode/hash, bornes internes, déterminisme byte-identique hors sink, aucun état global.

## Files
src/pixs/backend/correlated_log.py, tests/unit/test_correlated_log.py, tests/integration/test_correlated_log_integration.py, append seul src/pixs/backend/README.md.

## Validation
Strict avant/après, subprocess isolés sans settings/setup/FS/PG/socket sauf sink caller, AST 3.11 UTF-8/LF, périmètre strict.
