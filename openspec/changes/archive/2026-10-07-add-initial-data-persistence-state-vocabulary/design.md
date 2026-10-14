# Conception — Vocabulaire Enum des états de persistance

## Contexte

Source canonique des noms : `openspec/specs/data-lifecycle/spec.md`, exigence « Dimensions et états distincts » : ACTIVE, ARCHIVED, SOFT_DELETED, PURGE_PENDING, corroborée par `PROJECT.md` (« états communs de persistance ») et `TECHNICAL.md` §14.1. `PURGED` n’est pas ajouté à cette Enum ; la représentation éventuelle d’une preuve d’effacement reste hors périmètre.
Patron de couche : `ConfidentialityLevel(Enum)` et `JobState(Enum)` — Enum standard sans mixin, valeur textuelle égale au nom, `__all__`, docstring de frontière (`src/pixs/kernel/data_governance.py`, `src/pixs/kernel/jobs.py`).
Séparation à préserver : `src/pixs/kernel/lifecycle/state.py` porte le cycle mécanique des composants sans aucune notion métier ; ce change ne l'importe ni ne le modifie.
Décision CGPT : `src/pixs/kernel/data_persistence.py`, sans modification de façade.

## Règles livrées

- `class PersistenceState(Enum)` : `ACTIVE = "ACTIVE"`, `ARCHIVED = "ARCHIVED"`, `SOFT_DELETED = "SOFT_DELETED"`, `PURGE_PENDING = "PURGE_PENDING"`, dans cet ordre ;
- `__all__ = ["PersistenceState"]` ; docstring de frontière : représentation structurelle seule ;
- Aucun membre, alias, valeur par défaut, méthode, factory, convertisseur, validateur, transition, persistance, purge ni référence métier ajoutés.

## Décisions

- Enum standard sans mixin `str`, comme `JobState` ; le test unitaire porte sur l'adhésion normative des quatre couples noms/valeurs/ordre à la source citée, non sur des garanties de la stdlib ;
- Le delta MODIFIED reproduit mot pour mot l'exigence et son scénario ; effet d'archive attendu nul (+0/~0/-0/→0), toute divergence étant rapportée comme écart ;
- Tests utiles : unité — vocabulaire fermé et séparation du cycle mécanique (aucune référence à `lifecycle.state`) ; intégration — import frais à gardes positives ; pas de longue répétition miroir de l'implémentation ;
- Régression ciblée (module isolé, sans I/O, importé par aucun module existant) : famille vocabulaire voisine `test_data_governance_vocabulary.py`, gardes `tests/integration/test_kernel_purity.py` et `tests/integration/test_public_api_facades.py` ; pas de régression complète par habitude.

## Validation prévue (décisions techniques CGPT distinctes, explicites)

- Compilation ciblée des trois nouveaux fichiers via `/home/devops/python/current/bin/python3 -m py_compile`, résultats natifs ;
- `unittest` par exécutable absolu, en séquence : test unitaire du nouveau module, puis intégration, puis régression kernel purity/façades/vocabulaire voisin pertinent ; PostgreSQL et navigateur non applicables à du code pur ;
- `openspec validate` strict du change et de la spec `data-lifecycle` : exit 0 obligatoire, avant puis après code ;
- Validations globales `--specs --strict --json --report findings` et `--all --strict --json --report findings` : sorties brutes et codes réels consignés ; qualification limitée exactement aux 19 WARNING de longueur, 0 ERROR et identité des 76 specs canoniques à leurs empreintes ; contrôle de forme exact avant toute qualification ; toute ERROR, tout autre WARNING, couverture incomplète ou divergence d'empreinte bloque ;
- UTF-8/LF des trois nouveaux fichiers, identité octet par octet du bloc requirement du delta avec la source canonique, empreintes des fichiers non concernés.

## Critères observables

Quatre couples `(nom, valeur)` exactement dans l'ordre canonique ; `len(PersistenceState.__members__) == 4`, sans alias ni `PURGED` ; `__all__` exactement `["PersistenceState"]` ; import et vérifications en processus frais sans aucun effet observable et sans chargement supplémentaire de sous-modules `pixs.kernel.lifecycle` par rapport au chargement de la façade existante `pixs.kernel` ; façade `pixs.kernel.__all__` inchangée.
