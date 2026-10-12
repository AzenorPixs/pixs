# Conception — États d'opération en masse v1

BulkOperationState utilise enum.Enum de la bibliothèque standard : REQUESTED, STAGED,
VALIDATING, READY, RUNNING, COMPLETED, COMPLETED_WITH_ERRORS, FAILED, CANCELLED,
EXPIRED, noms et valeurs identiques, dans l'ordre nommé par le canon. Il désigne le
profil structurel préparatoire ; il ne définit aucune transition, aucun ordre, aucune
terminalité, aucun rattachement à JobState et aucun effet d'exécution ou de persistance.

Le module conserve intégralement et octet pour octet les trois vocabulaires existants
et la façade. __all__ ajoute uniquement BulkOperationState en fin de liste. Aucune
façade, dépendance ou configuration nouvelle. Le docstring du module reste inchangé ;
toute mise à jour de sa première ligne serait un mandat distinct.

Validation : strict du change avant code, compilation, import en processus neuf, AST
et surface exacts, mêmes suites existantes de pureté, façades, JobState et
NotificationChannel (20 tests comme au change précédent). Aucun test miroir de Enum,
aucun fichier de test modifié. Contrôles UTF-8/LF et empreintes.
