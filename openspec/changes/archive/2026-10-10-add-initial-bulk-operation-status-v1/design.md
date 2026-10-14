# Design — add-initial-bulk-operation-status-v1

## Représentation interne

@dataclass(frozen=True) BulkOperationStatus avec exactement operation_id: str et
status: BulkOperationState, dans cet ordre. Deux arguments obligatoires, aucun
défaut ni __post_init__. Le module interne n'ajoute aucune méthode métier.
__all__ = ["BulkOperationStatus", "validate_bulk_operation_status"].
Les façades, vocabulaires et autres modules existants restent inchangés.
Compatibilité Python >=3.12, aucune nouvelle dépendance.

## Validation pure

validate_bulk_operation_status(candidate: object) -> list[Diagnostic] rejette
tout type étranger ou sous-classé avant accès aux attributs. Pour un type exact,
les champs manquants sont refusés sans valeur de repli de données.
operation_id exige une str exacte non vide, opaque et sans normalisation ;
aucune contrainte UUID. status exige le type exact BulkOperationState et l’identité de l’un de ses dix
membres canoniques. Un objet forgé du même type est refusé, sans conversion,
ordre ni terminalité déduits.
Aucun hook d'objet étranger n'est invoqué.

Les diagnostics VALIDATE sont statiques, triés et dédupliqués par
(element, constraint, message), sans écho des valeurs. Chaque appel rend
une liste indépendante. Aucun I/O applicatif, environnement, réseau,
processus, DB ou autre effet. Aucune transition, progression ni garantie
de statut réel, rattachement, autorisation ou persistance.
Le profil ne remplace pas les exigences générales BulkOperation.

## Vérifications

Tests comportementaux : dix états admis, références opaques, champs obligatoires
et immuabilité, refus des types étrangers/sous-classes avant hooks, absence de
normalisation ou correction, diagnostics déterministes sans écho.
Intégration fraîche -I -B, environnement figé, timeout 10 secondes et répertoire
temporaire sous la racine projet. Gardes avec contrôles positifs : écritures,
réseau, processus, environnement et imports DB durant import/validation ;
gardes de lecture après l'import du module. Les chargements Python du module
ne sont pas présentés comme une absence universelle de lecture système.

Trois compilations séparées ; tests ciblés ; régressions Header, BulkJobLink,
SemVer, pureté, façades, JobState et NotificationChannel. Validation OpenSpec
avant/après code, aucune ERROR ; avertissements de longueur qualifiés sans
réécriture du canon. Archivage et STATISTIQUES.md restent des mandats distincts.
