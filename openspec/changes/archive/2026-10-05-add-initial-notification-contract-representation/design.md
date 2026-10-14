# Conception — Représentation déclarative interne partielle du contrat de notification

## Forme livrée

Module interne séparé `src/pixs/kernel/notification_contract.py`, stdlib seule, sans I/O ni mutation. `NotificationContract` : dataclass `frozen=True` à cinq champs obligatoires dans l'ordre `contract_version: str`, `recipient_keys: frozenset[str]`, `channels: frozenset[NotificationChannel]`, `preference_reference: str`, `perimeter_reference: str`, sans défaut, sans `__post_init__`, sans méthode applicative ; le constructeur reste structurellement permissif, le validateur est le seul point fermé. `validate_notification_contract(candidate)` retourne une liste de `Diagnostic` (patron `VALIDATE` de `pixs.kernel.diagnostics`) dédupliquée et triée comme dans `src/pixs/kernel/event_contract.py`, à messages fixes sans écho des valeurs. `__all__ = ["NotificationContract", "validate_notification_contract"]`. Docstring de frontière.

## Règles de validation

- Un `candidate` dont le type exact n'est pas `NotificationContract` produit un refus unique, avant tout `getattr` et sans aucun appel des méthodes d'un objet hostile ;
- `contract_version` : `str` de type exact, non vide, accepté par le `parse_version` SemVer existant de `pixs.kernel.manifest.semver` ;
- `recipient_keys` : type exact `frozenset`, chaque élément `str` de type exact non vide ; sous-classes, `bool`, `int`, `None` refusés ; l'ensemble vide est accepté, sans obligation de destinataire inventée ;
- `channels` : type exact `frozenset`, chaque élément contrôlé comme membre réel de `NotificationChannel` par identité (`is`) selon le patron de `notification_channel_declaration.py` ; l'ensemble vide est accepté, sans obligation de canal inventée ;
- `preference_reference` et `perimeter_reference` : `str` de type exact non vide, références opaques fournies par un caller trusted ; aucune résolution, normalisation, valeur par défaut, politique de préférence, consentement, autorisation, tenant ni classification de sensibilité n'est définie ou déduite ;
- Aucune appartenance, comparaison ou message n'invoque les dunder d'une valeur non validée.

## Décisions

- Réutilisations sans modification : `NotificationChannel` de `notifications.py`, `parse_version`, `Diagnostic`/`VALIDATE` ; aucune importation de `pixs.core` — le Kernel reste générique et le périmètre n'est porté que par référence opaque, à l'image des représentations `event_contract` et `audit_event` ;
- Représentation interne et partielle : ni `ContractDescriptor` public, ni contrat enregistré, ni wire format ; les champs d'enrichissement de TECHNICAL §24 (identifiant, type, sujet, tenant, corrélation, clé de déduplication) ne sont pas canonisés et ne sont pas portés ici ;
- Sources `notifications.py`, `notification_delivery.py`, `notification_channel_declaration.py`, `notification_recipient_declaration.py`, leurs tests et les façades restent inchangés octet à octet.

## Critères observables

- Instance valide complète : liste de diagnostics vide, dans l'ordre de collecte déterministe trié ;
- Chaque refus : un `Diagnostic` par champ fautif, contraint de message fixe, sans reproduction d'aucune valeur ;
- Ensembles vides acceptés sans diagnostic ; sous-classes et éléments hétérogènes refusés avant tout contrôle d'appartenance ;
- Export : exactement `["NotificationContract", "validate_notification_contract"]` ;
- Import du module et appels du validateur sans aucun effet observable (écriture, réseau, process, environnement, base).

## Validation prévue

- `py_compile` des trois nouveaux fichiers sous mandats distincts, exits réels ;
- Tests unitaires ciblés sur les usages du validateur, les frontières ci-dessus et les effets interdits (sondes hostiles comptant `__eq__`/`__hash__`/`__str__`/`__repr__`, vérification `getattr` non atteint sur mauvais type), sans multiplier les vérifications reflétant l'implémentation sans critère normatif ; nombre de tests observé, jamais imposé ;
- Intégration en processus frais `-I -B` avec environnement réduit déclaré et gardes d'effets finies du cadre acquis, marqueur de sortie fixe unique, aucun PostgreSQL réel, réseau, horloge, Git ni secret ;
- Suites de régression notification, audit et events existantes rejouées après le nouveau lot, nombre réel relevé sans cible imposée ;
- `openspec validate --strict` du change et des specs canoniques avant le code, puis du référentiel après les tests ; cochages uniquement après preuves observables ; archivage et `STATISTIQUES.md` sous mandats distincts.
