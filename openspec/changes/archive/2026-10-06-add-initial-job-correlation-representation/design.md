# Design — Représentation déclarative de corrélation des travaux

## Frontière

Le module définit une représentation interne partielle des références structurelles de corrélation des travaux. Il n'est pas le contrat `Job` de TECHNICAL.md §23. Les valeurs sont fournies par un caller trusted ou par des fixtures synthétiques ; elles ne prouvent aucune existence, légitimité, canonicité, autorisation ni sensibilité.

## Contrat technique

- Fichier : `src/pixs/kernel/job_correlation.py` ;
- exports publics exacts : `JobCorrelation`, `validate_job_correlation` — deux exports seulement ;
- `@dataclass(frozen=True) JobCorrelation` avec exactement quatre champs : `job_id: str`, `correlation_id: str`, `causation_id: str`, `perimeter_reference: str` ;
- `validate_job_correlation(candidate: object) -> list[Diagnostic]` : le type exact est vérifié avant tout accès aux attributs ; `type(candidate) is not JobCorrelation` produit le refus `corrélation de travail exacte attendue` sur l'élément `correlation` ; chaque valeur est ensuite contrôlée `type(value) is str and bool(value)` — chaîne exacte non vide, contrainte fixe `référence opaque exacte non vide attendue` ; aucune méthode n'est invoquée sur un objet non validé ;
- diagnostics : `step=VALIDATE`, élément `job_correlation.<champ>`, message fixe égal à la contrainte, sans écho d'aucune valeur ; dédoublonnés puis triés selon le motif `_pack` des modules `audit_event` et `event_contract` ;
- imports limités à `dataclasses.dataclass` et à `.diagnostics` (`VALIDATE`, `Diagnostic`) ; aucun import d'utilitaire privé d'un autre module ;
- docstring de frontière : référence opaque du périmètre distincte du `tenant_context`, sans résolution ni permission ; aucune comparaison d'identifiants ; aucun contrat `Job` complet ; aucun état, tentative, bail, horodatage, payload, SemVer, authentification, déduplication réelle, persistance, runtime, configuration ni nouvelle dépendance.

## Tests

- unitaire : corrélation valide retourne la liste vide ; type hostile (None, dict, sous-classe, conteneur) produit un seul diagnostic à message fixe sans écho ; chacun des quatre champs nullifié, non-`str` ou vide produit le diagnostic du champ nommé ; violations multiples triées et dédoublonnées ; stabilité des diagnostics sur double appel ; immuabilité gelée ; deux exports exactement ;
- intégration : import et contrôles en processus frais sous gardes d'effets, marqueur fixe dédié, adhésion stricte des deux exports, aucun effet sur disque ou réseau.
