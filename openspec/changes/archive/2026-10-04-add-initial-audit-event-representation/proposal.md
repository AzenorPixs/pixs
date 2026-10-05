# Représentation minimale d’un événement d’audit

## Why

La spécification canonique `audit` exige qu’un événement puisse représenter un contenu minimal, mais aucune représentation pure et fermée n’existe encore dans le Kernel. Ce constat bloque partiellement la suite de `feature-flags` R4, parce que les changements de configuration doivent pouvoir être audités et corrélés, sans que les normes opérationnelles correspondantes soient déjà complètement définies.

Ce change propose uniquement une capacité technique partielle : un modèle immuable et un validateur structurel capables de représenter les champs minimaux d’un événement d’audit. Il ne définit ni un wire format, ni une persistance, ni une politique de rétention, ni un panneau d’administration, ni une application aux fanions.

## What Changes

- Ajouter `src/pixs/kernel/audit_event.py` comme module pur, sans E/S applicative, sans horloge, sans réseau, sans base, sans configuration et sans nouvelle dépendance.
- Publier exactement deux exports : `AuditEvent` et `validate_audit_event`.
- Représenter un événement par un `dataclass(frozen=True)` structurel à treize champs, sans `__post_init__`, sans validation du constructeur et sans exception publique de validation.
- Fournir `validate_audit_event(event: object) -> list[Diagnostic]`, retournant une liste fraîche à chaque appel et refusant une entrée qui n’est pas exactement un `AuditEvent`, y compris une sous-classe.
- Valider les chaînes obligatoires comme références opaques de type exact `str` et non vides, sans `strip()`, normalisation, tri, troncature ni quota public.
- Autoriser `tenant_reference` et `reason_or_error` à être `None` ou une chaîne opaque exacte non vide.
- Accepter des tuples vides pour `correlation_ids` et `causation_ids` comme représentation syntaxique ; cette tolérance ne prouve pas une obligation de corrélation à l’exécution.
- Valider chaque élément présent d’un tuple comme une chaîne exacte non vide, sans imposer une grammaire ou un identifiant de corrélation.
- Valider `component_id` par `parse_requirement` public, en exigeant des contraintes vides et une cible strictement égale à l’entrée ; ne pas utiliser de fonction privée.
- Valider `component_version` par `parse_version` public SemVer, en refusant un échec par diagnostic constant sans reproduction de la valeur.
- Valider `occurred_at` par une grammaire UTC ASCII canonique injectée : `YYYY-MM-DDTHH:MM:SS[.fraction 1 à 6](Z | +00:00)`, avec calendrier réel analysé par `datetime.fromisoformat` et aucune horloge consultée.
- Produire des diagnostics bornés nommant le champ et la contrainte, sans écho d’une valeur, d’un secret, d’un identifiant brut ou d’une cause technique.
- Ajouter des tests unitaires et d’intégration sûrs pour la structure, les types, les grammaires, les tuples, l’absence d’E/S et les diagnostics.
- Ajouter trois fichiers de production et de tests exactement ; ne pas créer `tests/integration/test_audit_event.py`.

Le nombre de tests est déterminé par les comportements réellement représentés. Aucun objectif numérique arbitraire n’est fixé.

## Modified Capabilities

### audit

### Requirement: Contenu minimal d'un événement d'audit

Un événement d'audit MUST pouvoir représenter au minimum un identifiant, l'instant, l'acteur ou sa référence, le tenant pertinent, l'action, le type et l'identifiant de ressource, le résultat, la raison ou code d'erreur éventuel, les identifiants de corrélation et de causalité, et le composant avec sa version.

#### Scenario: Refus d'autorisation tracé

- **WHEN** une opération autorisée est refusée par l'évaluation d'autorisation
- **THEN** l'événement d'audit contient acteur, action, cible, résultat et corrélation sans attribut confidentiel superflu

Aucune norme nouvelle, modifiée ou supprimée n’est introduite. Le delta est recopié strictement depuis la spécification canonique `audit`.

## Impact

### Sources et fichiers

Nouveaux fichiers :

```text
src/pixs/kernel/audit_event.py
tests/unit/test_audit_event.py
tests/integration/test_audit_event_integration.py
```

Les cinquante-deux fichiers de baseline applicables restent inchangés (49 initiaux et 3 tests des dépendances). En particulier :

- aucune source ou test `feature-flags` n’est modifié ;
- aucun modèle PostgreSQL, aucune migration et aucun fichier d’intégration PG réel n’est touché ;
- aucun README backend n’est modifié ;
- aucune route, API HTTP, frontend, worker, scheduler ni configuration d’application n’est ajouté ;
- aucun package, export du package `pixs.kernel`, réglage ou dépendance nouveau n’est introduit.

### Validations prévues

- trois compilations Python natives pour les trois fichiers ajoutés ;
- tests unitaires ciblés prouvant la structure, les refus fermés, les chaînes opaques, les tuples, les grammaires de composant, l’horodatage UTC et l’absence d’écho des diagnostics ;
- intégration sûre en processus frais, avec gardes réelles contre l’E/S applicative sensible, l’horloge, le réseau et la base ;
- exécution des 192 tests sûrs actuellement acquis, sans PG réel supplémentaire ;
- validations concernées des parseurs et diagnostics :
  - `parse_requirement` public ;
  - `parse_version` public ;
  - `datetime.fromisoformat` pour le calendrier UTC ;
  - convention `Diagnostic` du Kernel ;
- strict OpenSpec du change, puis suite canonique applicable.

### Limites explicites

Ce change ne fournit ni ne prouve :

- aucun wire format JSON ou sérialisation publique ;
- aucune persistance, journalisation, stockage, intégrité ou retention ;
- aucune minimisation, redaction, anonymisation ou purge ;
- aucun panneau d’administration, route, API ou autorisation ;
- aucune obligation runtime de corrélation ou causalité ;
- aucune application aux événements de fanions ni résolution de source PostgreSQL ;
- aucune sémantique d’action, résultat, erreur ou politique d’audit ;
- aucune validation d’un secret ou d’une référence de secret.

Les références d’acteur, de tenant et les contenus restent trusted ou synthétiques au niveau structurel. Le module ne distingue pas une donnée légitime d’une donnée sensible.
