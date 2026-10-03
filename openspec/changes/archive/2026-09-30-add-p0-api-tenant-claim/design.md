## Context

Normes validées : api Requirement Périmètre canonique et autorisation à la frontière et scope-context Requirement Contexte immuable propagé avant autorisation. ScopeContext accepte des chaînes opaques exactes non vides sans normalisation ; check_claim valide la topologie puis compare strictement les contextes et livre un PropagationDiagnostic constant au callback de refus. Aucun chemin littéral tenant n’est fixé par la norme.

## Goals / Non-Goals

Résoudre le seul contexte TENANT racine à partir du tenant déjà extrait du chemin, le confronter à la déclaration client facultative. Ne pas produire de contexte enfant ou PLATFORM, extraire une URL, vérifier une appartenance, autoriser, authentifier, persister ou garantir un audit durable.

## Decisions

Signature resolve_tenant_boundary(path_tenant, claimed_tenant=None, *, snapshot, on_denied). Valeurs acceptées : str exact non vide, opaque sans strip/UUID conversion. Construire ScopeContext TENANT sans scope enfant, puis déléguer à check_claim. Pour un tenant chemin invalide, fournir à check_claim un canonique invalidant None ; pour une déclaration présente mais invalide, fournir un claim invalidant constant False. Ces signaux restent internes et ne doivent jamais accepter la valeur invalide. Les refus et diagnostics viennent uniquement du contrat public check_claim, sans lecture ou conversion des entrées hostiles. on_denied reste obligatoire conformément au contrat existant ; il n’est jamais invoqué au succès. Aucune nouvelle exception ou norme.

## Files

- src/pixs/backend/api/tenant_claim.py : module et docstring avec exemple executable.
- tests/unit/test_tenant_claim.py : exigences de canonicalité, types hostiles, topologie, diagnostic constant, absence de normalisation, callback et immutabilité.
- tests/integration/test_tenant_claim_integration.py : contrats publics réels, exemple docstring, import subprocess sans Django et compatibilité API existante.

## Validation

Préparation stricte avant code ; tests dédiés puis suites unitaires et intégration en deux commandes distinctes avec venv autorisé, PYTHONPATH=src et PYTHONDONTWRITEBYTECODE=1 ; AST3.11, UTF8/LF, exemple réel et empreintes des sources existantes ; stricte finale puis cochage et stricte du dossier coché. Archivage et STATISTIQUES.md sous mandats distincts après toutes preuves.

## Risks

L’extraction et la fiabilité du tenant chemin restent la responsabilité du contrat de route futur. La topologie est un snapshot fourni par appelant, aucune persistance. Le callback ne prouve pas un audit durable. Le helper retourne un contexte structurel, jamais une décision d’accès. Aucun Requirement global n’est déclaré satisfait.
