## Why

Les contrats publics exigent des catégories non interchangeables, une version SemVer indépendante et une dépréciation/retrait encadrés, tandis que le socle actuel ne contient pas encore de descripteur pur de contrat. Les manifests valident l’identifiant et la version exacte et la composition résout les contrats, sans objet testable pour les catégories ni le cycle de dépréciation/retrait. Cette évolution prépare des descripteurs immuables en pure mémoire, sans prétendre réaliser un registre, une activation ou une garantie comportementale.

## What Changes

- Préparer un descripteur immuable pur avec identifiant canonique, catégorie parmi les sept valeurs, version SemVer indépendante, composant propriétaire et garanties documentées.
- Préparer une garde pure `require_category` exigeant la catégorie exacte, notamment EVENT ne remplace jamais COMMAND et HOOK ne fournit jamais de garantie transactionnelle.
- Préparer une comparaison déclarée `check_evolution` avec indicateur explicite `breaking`, refus des ruptures sans majeure et des baisses de version, sans comparaison sémantique automatique.
- Préparer un avis séparé `DeprecationNotice` avec annonce en mineure et remplacement documenté obligatoire, puis un contrôle `check_retirement` exigeant une majeure strictement supérieure, sans suppression effective ni exception critique.
- Vérifier avec des entrées synthétiques invalides, y compris préversions et métadonnées de build SemVer, sans données réelles, I/O, secret, base ou dépendance nouvelle.
- Préserver les invariants et les fondations déjà validées. Aucune API existante ni aucun modèle de manifest n’est modifié dans ce périmètre.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- contracts : préparer la description pure des trois exigences canoniques déjà validées, sans modifier l’exigence canonique.

## Impact

Fichiers d’implémentation prévus : src/pixs/kernel/contracts/__init__.py, src/pixs/kernel/contracts/models.py, documentation ciblée si nécessaire et tests purs unitaires/integration correspondants. Aucune dépendance nouvelle ; seule la stdlib et le parseur SemVer partagé sont utilisés. Toute installation reste sans objet, aucun paquet n’est ajouté.

Exclusions : secrets réels, opération PostgreSQL, déploiement, installation, persistance, registre d’activation, résolution de provider, détection automatique sémantique ou de schéma, garanties réelles, exceptions critiques, Git, frontend, API, modèles et migrations. Les contrôles purs ne prouvent ni une compatibilité globale, ni une conformité comportementale, ni une histoire publiée. Aucun archivage ne sera autorisé avant les preuves applicables.
