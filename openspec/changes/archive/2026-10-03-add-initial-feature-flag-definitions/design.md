# Design : add-initial-feature-flag-definitions

## Position

Fondation déclarative purement stdlib de la définition de fanion, seule précondition normée disponible pour R1 « Définition versionnée et bornée » de `feature-flags`. Aucun évaluateur, aucune persistance, aucun cycle de vie, aucun lien avec la résolution de capacités ou la gate `availability` (inchangées) ; R3 de `capabilities` n'est pas déclaré réalisé.

## Décisions

### D1 — Modèle à douze champs canoniques, aucun défaut

`FeatureFlagDefinition` : `@dataclass(frozen=True)` dont les champs sont exactement et dans cet ordre (TECHNICAL 7.2) :

1. `flag_id : str` — identifiant namespacé (D4).
2. `flag_version : str` — métadonnée d'identité opaque exacte ; la catégorie SemVer des composants, contrats et capacités ne s'y applique pas ; aucune comparaison ni analyse de grammaire version.
3. `owner_component : str` — référence au composant propriétaire, identifiant nu (D4), non résolu ici.
4. `purpose : str` — prose déclarative non vide ; jamais exécutée, jamais filtrée par heuristique de contenu.
5. `value_schema : str` — `type(x) is str` puis appartenance exacte à `FLAG_VALUE_SCHEMAS = frozenset({"BOOLEAN", "VARIANT"})`.
6. `default_value : bool | str` — BOOLEAN : `type(...) is bool` exactement (les `int` même 0/1 sont refusés) ; VARIANT : littéral token de la grammaire d'identifiants partagée (D4).
7. `targeting_dimensions : tuple[str, ...]` — whitelist déclarative bornée `FLAG_TARGETING_DIMENSIONS = frozenset({"INSTALLATION", "ENVIRONMENT", "TENANT", "SCOPE"})` (noms canoniques TECHNICAL 7.2) ; tuple vide explicite = aucune dimension ; aucun ciblage effectif, aucune sélection.
8. `cohort_key : str | None` — seul champ dont la **valeur** explicitement fournie peut être `None` (norme : « éventuelle ») ; les douze champs restent **obligatoires à la construction, sans aucun défaut de champ** : `cohort_key` doit être passé, y compris comme `None`.
9. `prerequisites : tuple[str, ...]` — références déclaratives bornées, identifiants (D4), sans doublons ; aucune résolution, aucune précédence inventée.
10. `fallback_policy : str` — déclaration non vide identifiant une politique (D4) ; aucun interprète ni évaluateur de repli.
11. `expires_at : str` — obligatoire, jamais `None` (D5).
12. `audit_policy : str` — déclaration bornée identifiant une politique d'audit ; aucune exécution d'audit.

Aucun treizième champ, et surtout aucun champ `expression`, `rule`, `code` ou `callback` : la construction d'un objet non membre échoue par `TypeError` natif du dataclass — refus réel, non prose.

### D2 — Ordre de contrôle : identité de type exacte avant toute opération

Pour chaque valeur : `type(x) is Classe` — identité exacte partout ; aucun champ `int` n'étant requis, aucune exception `isinstance`/int n'est conservée ; `bool` exige `type(x) is bool` (les `int` 0/1 sont des `int`, donc refusés) ; la forme `type(x) in (classes)` est proscrite car elle invoquerait `métaclasse.__eq__`. Tout contrôle d'identité précède égalité, tri, hachage, appartenance à un frozenset ou analyse. Un objet hostile (callable, sous-classe non exacte, métaclass trompeuse) ne déclenche donc jamais `__eq__`, `__hash__` ni itération arbitraire.

### D3 — Validateurs en refus fermé sans écho

`validate_feature_flag_definitions(Sequence[FeatureFlagDefinition]) -> tuple[Diagnostic, ...]` :
- le conteneur d'entrée est contrôlé `type(entree) is list or type(entree) is tuple` **avant toute itération**, chaque item `type(item) is FeatureFlagDefinition` **avant tout accès d'attribut**, un item mal typé produisant un refus sans lecture d'attributs hostiles ;
- agrégation sans interruption ; diagnostics `step=VALIDATE`, `element="feature_flags.<champ>"` ou `"feature_flags.identifiants"`, `constraint` et `message` **constants** nommant champ et contrainte, ne reproduisant jamais la valeur invalide (ni identifiant fautif, ni chaîne d'expiration) ;
- tri déterministe sur `(element, constraint, message)` et dédoublonnage des messages identiques : les diagnostics ne portent **aucun index dépendant de l'ordre**, entrées permutées ⇒ tuples strictement identiques ;
- `flag_id` en double dans le lot ⇒ refus « drapeau déclaré une seule fois » même lorsque les `flag_version` diffèrent (un même drapeau ne peut coexister en double définition).

### D4 — Grammaire d'identifiants : parse_requirement partagé, aucune regex parallèle inventée

Aucune expression régulière locale ni grammaire littérale parallèle. Un identifiant **nu** est contrôlé par le parseur partagé existant `manifest.semver.parse_requirement` après `type(x) is str` exact (D2) : la valeur est admise si `parse_requirement(v)` réussit, `requirement.constraints` est vide et `requirement.target_id == v`. Nu signifie « sans comparateur », non « sans points » ; les identifiants composants existants sont namespacés et peuvent contenir tirets, majuscules et chiffres, grammaire conservée intégralement.

Champs : `flag_id` = valeur nue **et** namespacée (au moins deux segments séparés par `.` non vides, PROJECT 1374) ; `owner_component` = valeur nue (aucune confiance ni résolution ici) ; éléments de `prerequisites`, `fallback_policy`, `audit_policy`, token VARIANT de `default_value` et `cohort_key` (quand explicitement non None) = références littérales nues validées par la même grammaire partagée. `flag_version` reste hors grammaire (D1.2).

### D5 — Expiration : borne de format explicite, analyse réelle, aucune horloge

`expires_at` : après `type(x) is str`, borne **explicite du contrat** au format ASCII `YYYY-MM-DDTHH:MM:SS[.fraction](Z | +00:00)` ; la fraction est limitée à 1 à 6 chiffres pour rester dans les capacités exactes de `datetime.fromisoformat` (aucune prétention de précision conservée au-delà du format borné). La borne est vérifiée par contrôle caractère par caractère des positions et ensembles de chiffres ASCII (points fixes `-`, `T`, `:`, `.`, suffixe `Z` ou `+00:00`) — sans regex ni `in` de classes — pour refuser les représentations alternatives que `fromisoformat` accepterait sinon (séparateur espace, dates compactes, week-dates). Si la borne passe, analyse calendrier réelle par `datetime.fromisoformat` ; `ValueError` (date impossible) ⇒ refus précis ; puis UTC exigé (`utcoffset()` nul). Interdictions fermes : `datetime.now`, `time`, horloge système, lecture d'environnement, comparaison d'expiration ou décision de date courante.

### D6 — Déclarations, pas sémantique effective

`cohort_key`, `prerequisites`, `fallback_policy` et `audit_policy` ne sont que des déclarations typées/bornées : aucun choix de cohorte, aucun ordre de priorité, aucun mécanisme de repli, aucun émetteur d'audit n'est implémenté ni même nommé au-delà de l'identité.

### D7 — Surface et périmètre de fichiers

Un module unique `src/pixs/kernel/feature_flags.py` (pas de package `flags/` ni `__init__` superflu) ; deux suites nouvelles (`tests/unit/test_feature_flag_definitions.py`, `tests/integration/test_feature_flag_definitions_integration.py`) ; **zéro** source existante modifiée ; intégration sur le schéma éprouvé : enfant `-B` frais, gardes IO causales avant import, aucun I/O métier, marqueur final dédié, sans Django/PG/réseau.

### D8 — Réversibilité conceptuelle, aucune autorisation de retrait

Ce design n'autorise ni suppression, ni remplacement, ni retrait automatique du module : l'ajout est isolé (aucun consommateur), ce qui rend un futur retrait conceptuellement possible via un change distinct explicitement validé par CGPT — sans transformation de ce change en permis de détruire.

## Critères de preuve

py_compile des trois fichiers sous l'interpréteur DEVOPS ; unit et intégration verts ; régression ciblée inchangée ; baseline du présent change préservée ; delta MOTAMOT R1 seul (aucun scénario ajouté ; R2–R4 de `feature-flags` inchangés) ; strict valide pré et post-cochage ; archive et statistiques en mandats distincts.
