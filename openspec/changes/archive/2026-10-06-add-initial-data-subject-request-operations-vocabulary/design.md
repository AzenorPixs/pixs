# Conception — Vocabulaire Enum des opérations de demande relative aux données

## Contexte

Source canonique des noms : `openspec/specs/data-governance/spec.md`, exigence « Demandes relatives aux données tracées » : accès, export, rectification, effacement, restriction. Identifiants anglais exacts fournis par TECHNICAL.md §14.6 : ACCESS, EXPORT, RECTIFY, ERASE, RESTRICT. Patron de couche : `JobState(Enum)` (`src/pixs/kernel/jobs.py`) et `data_governance.py` — Enum standard sans mixin, module stdlib pur, `__all__`, docstring de frontière. Décision CGPT : `src/pixs/kernel/data_subject_operations.py`, sans modification de façade.

## Règles livrées

- `class DataSubjectOperation(Enum)` : `ACCESS = "ACCESS"`, `EXPORT = "EXPORT"`, `RECTIFY = "RECTIFY"`, `ERASE = "ERASE"`, `RESTRICT = "RESTRICT"`, dans cet ordre ;
- `__all__ = ["DataSubjectOperation"]`, exactement cette classe ; docstring de frontière : vocabulaire interne seulement ; les noms ne constituent aucune autorisation, obligation juridique, décision de politique ou exécution ;
- Aucun membre supplémentaire, alias, valeur par défaut, constructeur, wrapper, parseur, variante, méthode, persistance, flux, runtime ni référence exporté.

## Décisions

- Enum standard sans mixin `str` ; le test unitaire porte sur l'adhésion normative des cinq noms/valeurs/ordre aux sources citées, non sur des garanties de la stdlib (vérification du contrat déclaré, sans test des garanties propres à la stdlib) ;
- Le delta MODIFIED reproduit mot pour mot l'exigence et son scénario ; effet d'archive attendu nul (+0/~0/-0/→0), toute divergence étant rapportée comme écart ; le scénario « Effacement propagé » reste non couvert par ce change et ne peut être imputable au vocabulaire ;
- Régression minimale ciblée (module isolé, sans I/O, importé par aucun module existant) : familles vocabulaire et contrats voisins, gardes de façade/pureté ; pas de régression complète par habitude ;
- La structure complète `DataSubjectRequest` (TECHNICAL §14.6, dix champs dont éventuels) reste hors périmètre : aucune sémantique d'absence ni `status` inventé.

## Validation prévue (décision technique root explicite pour CE change)

- `openspec validate` strict du change et de la spec `data-governance` : exit 0 obligatoire, avant le code puis après les tests ;
- Contrôles globaux `--specs --strict --json --report findings` et `--all --strict --json --report findings` : sorties brutes et codes réels consignés ; qualification des 19 WARNING de longueur admise pour CE change seulement si exit natif réellement 1, couverture 76 (specs) / 77 (all) complète, identité exacte des issues de la table validée de l'archive `2026-10-06-add-initial-notification-contract-representation`, zéro ERROR et aucun autre texte/emplacement, et baseline des 118 fichiers inchangée ; toute ERROR, autre WARNING, divergence d'empreinte ou couverture incomplète bloque ;
- Compilations ciblées des trois nouveaux fichiers, résultats natifs ;
- Test unitaire : couples exacts via `__members__.items()`, ordre, pas d'alias, `__all__` ;
- Test d'intégration : processus frais `-I -B`, `FIXED_ENV` réduit (`LANG=C.UTF-8`, `PATH=/usr/bin:/bin`), cwd projet, tempdir sous racine, gardes finies d'effets réutilisées à l'identique du modèle classification, contrôles positifs avant remise à zéro des compteurs, cinq couples/noms et `__all__` vérifiés sous gardes, compteurs à 0 après usage, aucun module DB chargé, marqueur `DATA_SUBJECT_OPERATIONS_SAFE_INTEGRATION_OK` seul sur stdout, les quatre assertions finales du parent hors du `with` (sonde dans le `with`) ;
- Régression minimale : `tests/unit/test_data_governance_vocabulary.py`, `tests/unit/test_data_governance_profile.py`, `tests/unit/test_job_state.py`, `tests/unit/test_notification_channel.py`, `tests/unit/test_notification_delivery_state.py`, `tests/integration/test_kernel_purity.py`, `tests/integration/test_public_api_facades.py` ;
- UTF-8/LF des trois nouveaux fichiers et empreintes des fichiers non concernés.

## Critères observables

Cinq couples `(nom, valeur)` exactement dans l'ordre canonique ; `len(DataSubjectOperation) == 5` et `len(__members__) == 5` sans alias ; `__all__` exactement `["DataSubjectOperation"]` ; import et vérification en processus frais sans effet observé sur les surfaces gardées ; façade `pixs.kernel.__all__` inchangée.

## Non-goal

Aucune exécution, file, autorisation, audit, idempotence, propagation, hold, rétention, `status`, `DataSubjectRequest`, base, runtime, consentement juridique ni immutabilité profonde revendiqués.
