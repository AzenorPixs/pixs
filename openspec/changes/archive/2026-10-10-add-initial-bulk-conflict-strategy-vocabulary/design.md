# Conception — Stratégies de conflit en masse v1

BulkConflictStrategy utilise enum.Enum de la bibliothèque standard : REJECT, CREATE_ONLY,
UPDATE_ONLY, UPSERT, noms et valeurs identiques, dans l'ordre nommé par le canon. Il
désigne le profil structurel préparatoire ; il ne choisit aucune stratégie, ne définit
aucun défaut, aucune résolution de conflit, aucune permission, aucun effet d'import ni de
persistance.

Le module conserve intégralement et octet pour octet les quatre vocabulaires existants, le
docstring et la façade. __all__ ajoute uniquement BulkConflictStrategy en fin de liste.
Aucune façade, dépendance ou configuration nouvelle. Toute mise à jour du docstring
reste un mandat distinct.

Validation : strict du change avant code, compilation, import en processus neuf, AST et
surface exacts, mêmes suites existantes de pureté, façades, JobState et
NotificationChannel (20 tests comme au change précédent). Aucun test miroir de Enum,
aucun fichier de test modifié. Contrôles UTF-8/LF et empreintes.
