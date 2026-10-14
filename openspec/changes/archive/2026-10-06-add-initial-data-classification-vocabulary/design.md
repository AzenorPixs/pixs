# Conception — Vocabulaire Enum des classifications de gouvernance

## Contexte

Source canonique des noms : `openspec/specs/data-governance/spec.md`, exigence « Classification restrictive par défaut » : PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED puis NONE, PERSONAL, SENSITIVE_PERSONAL. Patron de couche : `JobState(Enum)` (`src/pixs/kernel/jobs.py`) — Enum standard sans mixin, module stdlib pur, `__all__`, docstring de frontière. Décision CGPT : `src/pixs/kernel/data_governance.py`, sans modification de façade.

## Règles livrées

- `class ConfidentialityLevel(Enum)` : `PUBLIC = "PUBLIC"`, `INTERNAL = "INTERNAL"`, `CONFIDENTIAL = "CONFIDENTIAL"`, `RESTRICTED = "RESTRICTED"`, dans cet ordre ;
- `class PersonalDataLevel(Enum)` : `NONE = "NONE"`, `PERSONAL = "PERSONAL"`, `SENSITIVE_PERSONAL = "SENSITIVE_PERSONAL"`, dans cet ordre ;
- `__all__ = ["ConfidentialityLevel", "PersonalDataLevel"]`, exactement ces deux classes ; docstring de frontière : représentation structurelle seule ;
- Aucun membre, alias, valeur par défaut, comparaison de sévérité, méthode, factory, convertisseur, validateur, persistance ni référence export ajoutés.

## Décisions

- Enum standard sans mixin `str`, comme `JobState` ; le test unitaire porte sur l'adhésion normative des sept noms/valeurs/ordre à la source citée, non sur des garanties de la stdlib ;
- Le delta MODIFIED reproduit mot pour mot l'exigence et son scénario ; effet d'archive attendu nul (+0/~0/-0/→0), toute divergence étant rapportée comme écart ;
- Régression ciblée (module isolé, sans I/O, importé par aucun module existant) : familles vocabulaire déjà prouvées et gardes de façade/pureté du Kernel ; pas de régression complète par habitude.

## Validation prévue (décision technique CGPT distincte, explicite)

- Compilations ciblées des trois nouveaux fichiers, résultats natifs ;
- Tests unitaire et d'intégration (processus frais `-I -B`, environnement réduit, gardes finies d'effets, marqueur fixe, aucune nouvelle dépendance) ;
- Régression ciblée : `tests/unit/test_job_state.py`, `tests/unit/test_notification_channel.py`, `tests/unit/test_notification_delivery_state.py` (familles vocabulaire de même patron), `tests/integration/test_kernel_purity.py` et `tests/integration/test_public_api_facades.py` (garde du caractère isolé du module et de la façade inchangée) ;
- `openspec validate` strict du change et de la spec `data-governance` : exit 0 obligatoire, avant puis après code ;
- Globals `--specs --strict` et `--all --strict --json --report findings` : sorties brutes et codes réels consignés ; qualification limitée exactement aux 19 WARNING de longueur et aux emplacements de la table validée du change archivé `2026-10-06-add-initial-notification-contract-representation`, uniquement si les 76 specs canoniques restent identiques à leurs empreintes avant code ; toute ERROR, tout autre WARNING, emplacement ou texte, toute couverture incomplète ou divergence d'empreinte bloque ; les textes normatifs et le CLI restent intacts ;
- UTF-8/LF des trois nouveaux fichiers et empreintes des fichiers non concernés.

## Critères observables

Sept couples `(nom, valeur)` exactement dans l'ordre canonique ; `len(...) == 4` et `len(...) == 3`, `__members__` sans alias ; `__all__` exactement les deux classes ; import et vérification du vocabulaire en processus frais sans aucun effet observable ; façade `pixs.kernel.__all__` inchangée.
