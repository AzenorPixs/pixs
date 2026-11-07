# Tasks — add-p0-scope-context

## 1. Socle scope sous pixs.core (stdlib seule, hors Kernel)

- [x] 1.1 Créer `src/pixs/core/__init__.py` et façade scope — vérification : import façade seule, aucun symbole Kernel importé
- [x] 1.2 Créer `src/pixs/core/scope/__init__.py` exportant ScopeType, ScopeContext, ScopeNode, TopologySnapshot, ResourceOwnership, validate_structure, validate_context, resolve_order, check_claim, erreurs — vérification : import public borné
- [x] 1.3 Créer `src/pixs/core/scope/context.py` (ScopeType enum strict, ScopeContext frozen, validate_structure) — vérification : tests structure
- [x] 1.4 Créer `src/pixs/core/scope/topology.py` (ScopeNode, TopologySnapshot copie défensive, validate_context, resolve_order topo parent-avant-enfant tie-break lexico) — vérification : tests topologie
- [x] 1.5 Créer `src/pixs/core/scope/ownership.py` (ResourceOwnership frozen resource_id+context, contexte structurellement valide, validation topologique à la frontière avec snapshot, pas de canonical_owner wrapper) — vérification : propriétaire stable séparé droits
- [x] 1.6 Créer `src/pixs/core/scope/propagation.py` (check_claim canonical/claim=None/snapshot/on_denied, égalité stricte, callback obligatoire, échec fermé enveloppé) — vérification : tests propagation

## 2. Tests structure, types et immuabilité

- [x] 2.1 `tests/unit/test_scope_context_structure.py` : TENANT/PLATFORM, types exacts/enum strict sans conversion, immuabilité frozen, PLATFORM sans ids accepté structurellement, TENANT sans tenant refusé, PLATFORM avec ids refusé, orphelin refusé

## 3. Tests topologie

- [x] 3.1 `tests/unit/test_scope_topology.py` : références/doublons/cycles/inter-tenant refusés, deep chain, permutations d'entrée même ordre, mutation de l'entrée après snapshot sans effet, exposition immuable

## 4. Tests propriété et propagation

- [x] 4.1 `tests/unit/test_scope_ownership.py` : ResourceOwnership stable, contexte direct, partage sans changement propriétaire, séparé des droits
- [x] 4.2 `tests/integration/test_scope_propagation.py` : égalité stricte canonique+claim+snapshot, callback obligatoire et appelé à chaque refus y compris canonique invalide ou mauvais type, échec callback sans retour de contexte, diagnostics sans identifiants bruts ni fuite y compris tracebacks

## 5. Critères et validations

- [x] 5.1 Bibliothèque pure stdlib sans autorisation implicite, hors Kernel, pas de runtime prétendu — vérification : `pyproject dependencies=[]` inchangé, aucune importation ORM/HTTP
- [x] 5.2 Exécuter suite unitaire via `/usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/unit` — vérification : exit 0
- [x] 5.3 Exécuter suite intégration via `/usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/integration` — vérification : exit 0
- [x] 5.4 Syntaxe mémoire AST des six fichiers sans pyc, UTF-8/LF — vérification : parse AST et contrôle fins de ligne
- [x] 5.5 Validation OpenSpec stricte via chemin DEVOPS `/usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate --all --strict` — vérification : exit 0, scope-context passant

## Preuves de validation

- unit 228 exit 0 msg_0ed36d3b9001YeT1erytMY28Sp
- intégration 86 exit 0 msg_0ed37b370001Podw8sxEQ4eu6G
- AST 10 UTF8LF 14 msg_0ed38d2ce001OL4Z0Pge0Gea5o
- OpenSpec 77/77 exit 0 msg_0ed39b0aa001iykCgez7aSB3L7
- revue finale msg_0ed3b480d0019VXhz2wBuG7D4V

Bibliothèque partielle : persistance, PDP/PEP, audit durable, runtime et composition P0 hors périmètre.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 5. Critères et validations » ; « Preuves de validation ».

### C26-SL01 — Créer `src/pixs/core/__init__.py` et façade scope — vérification : import façade seule, aucun symbole Kernel importé

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Socle scope sous pixs.core (stdlib seule, hors Kernel) », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C26-SL02 — Créer `src/pixs/core/scope/__init__.py` exportant ScopeType, ScopeContext, ScopeNode, TopologySnapshot, ResourceOwnership, validate_structure, validate_context, resolve_order, check_claim, erreurs — vérification : import public borné

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Socle scope sous pixs.core (stdlib seule, hors Kernel) », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C26-SL03 — Créer `src/pixs/core/scope/context.py` (ScopeType enum strict, ScopeContext frozen, validate_structure) — vérification : tests structure

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Socle scope sous pixs.core (stdlib seule, hors Kernel) », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C26-SL04 — Créer `src/pixs/core/scope/topology.py` (ScopeNode, TopologySnapshot copie défensive, validate_context, resolve_order topo parent-avant-enfant tie-break lexico) — vérification : tests topologie

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Socle scope sous pixs.core (stdlib seule, hors Kernel) », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C26-SL05 — Créer `src/pixs/core/scope/ownership.py` (ResourceOwnership frozen resource_id+context, contexte structurellement valide, validation topologique à la frontière avec snapshot, pas de canonical_owner wrapper) — vérification : propriétaire stable séparé droits

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Socle scope sous pixs.core (stdlib seule, hors Kernel) », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C26-SL06 — Créer `src/pixs/core/scope/propagation.py` (check_claim canonical/claim=None/snapshot/on_denied, égalité stricte, callback obligatoire, échec fermé enveloppé) — vérification : tests propagation

- Ancien repère et tâche rattachée : tâche 1.6 ; section « 1. Socle scope sous pixs.core (stdlib seule, hors Kernel) », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C26-SL07 — `tests/unit/test_scope_context_structure.py` : TENANT/PLATFORM, types exacts/enum strict sans conversion, immuabilité frozen, PLATFORM sans ids accepté structurellement, TENANT sans tenant refusé, PLATFORM avec ids refusé, orphelin refusé

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Tests structure, types et immuabilité », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C26-SL08 — `tests/unit/test_scope_topology.py` : références/doublons/cycles/inter-tenant refusés, deep chain, permutations d'entrée même ordre, mutation de l'entrée après snapshot sans effet, exposition immuable

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Tests topologie », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C26-SL09 — `tests/unit/test_scope_ownership.py` : ResourceOwnership stable, contexte direct, partage sans changement propriétaire, séparé des droits

- Ancien repère et tâche rattachée : tâche 4.1 ; section « 4. Tests propriété et propagation », ligne 22 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C26-SL10 — `tests/integration/test_scope_propagation.py` : égalité stricte canonique+claim+snapshot, callback obligatoire et appelé à chaque refus y compris canonique invalide ou mauvais type, échec callback sans retour de contexte, diagnostics sans identifiants bruts ni fuite y compris tracebacks

- Ancien repère et tâche rattachée : tâche 4.2 ; section « 4. Tests propriété et propagation », ligne 23 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C26-SL11 — Bibliothèque pure stdlib sans autorisation implicite, hors Kernel, pas de runtime prétendu — vérification : `pyproject dependencies=[]` inchangé, aucune importation ORM/HTTP

- Ancien repère et tâche rattachée : tâche 5.1 ; section « 5. Critères et validations », ligne 27 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C26-SL12 — Exécuter suite unitaire via `/usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/unit` — vérification : exit 0

- Ancien repère et tâche rattachée : tâche 5.2 ; section « 5. Critères et validations », ligne 28 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C26-SL13 — Exécuter suite intégration via `/usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/integration` — vérification : exit 0

- Ancien repère et tâche rattachée : tâche 5.3 ; section « 5. Critères et validations », ligne 29 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C26-SL14 — Syntaxe mémoire AST des six fichiers sans pyc, UTF-8/LF — vérification : parse AST et contrôle fins de ligne

- Ancien repère et tâche rattachée : tâche 5.4 ; section « 5. Critères et validations », ligne 30 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C26-SL15 — Validation OpenSpec stricte via chemin DEVOPS `/usr/bin/env OPENSPEC_TELEMETRY=0 /home/devops/.local/npm/bin/openspec validate --all --strict` — vérification : exit 0, scope-context passant

- Ancien repère et tâche rattachée : tâche 5.5 ; section « 5. Critères et validations », ligne 31 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
