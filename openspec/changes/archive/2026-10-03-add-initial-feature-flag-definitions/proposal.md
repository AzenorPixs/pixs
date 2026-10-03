# Proposition : add-initial-feature-flag-definitions

## Pourquoi

L'exigence « Définition versionnée et bornée » (R1) de la capacité `feature-flags` est non livrée : recherche ciblée dans `src/pixs` sans aucune structure de définition de fanion (grep `fanion|flag` : seuls hits non pertinents). La fondation déclarative est nécessaire avant tout mécanisme positif de fanion, et elle conditionne à terme la preuve du scénario R3 de `capabilities` (« un fanion ne remplace pas la résolution »), sans la réécrire ici.

## Ce qui change

- Une fondation déclarative purement stdlib de la définition de fanion, portée par un module unique `src/pixs/kernel/feature_flags.py` (pas de package intermédiaire) :
  - `FeatureFlagDefinition` : dataclass frozen à douze champs canoniques obligatoires (TECHNICAL 7.2) : `flag_id`, `flag_version`, `owner_component`, `purpose`, `value_schema`, `default_value`, `targeting_dimensions`, `cohort_key`, `prerequisites`, `fallback_policy`, `expires_at`, `audit_policy`. Seul `cohort_key` est explicitement éventuel en norme (valeur `None` admise) ; `expires_at` est obligatoire.
  - `validate_feature_flag_definitions(...)` : contrôle de types exacts avant toute opération, refus fermé agrégé en diagnostics `validate` sans reproduction de valeur, déterministe sous permutation.
  - Ensembles bornés déclaratifs : schémas de valeur `BOOLEAN | VARIANT` ; dimensions de ciblage canoniques `INSTALLATION`, `ENVIRONMENT`, `TENANT`, `SCOPE` (whitelist déclarative, sans ciblage effectif).
  - `expires_at` : chaîne exacte non vide représentant une date UTC sérialisée, réellement validée par analyse stdlib (`datetime.fromisoformat`), Fuseau `Z` ou `+00:00` normalisés, chaînes naïves, à décalage autre ou invalides refusées ; aucune horloge système, aucun `now`, aucune lecture d'environnement, aucune comparaison d'expiration.
- `flag_version` et `flag_id` restent des métadonnées d'identité exactes non vides (le fanion n'appartient pas à la catégorie SemVer des composants, contrats et capacités) ; `flag_id` namespacé selon la grammaire d'identifiants déclaratifs existante du noyau ; `purpose` est une prose déclarative jamais exécutée et jamais filtrée par heuristique.
- `default_value` : `bool` strictement pour `BOOLEAN` ; littéral de token borné de type identifiant pour `VARIANT`. Aucun champ « expression », « règle » ou « code » n'existe dans le modèle, et toute valeur non primitive (callable, objet étranger, séquence mal typée) est refusée en fermeture : le scénario « Règle à expression rejetée » s'éprouve par la fermeture du modèle et du validateur.
- `prerequisites`, `fallback_policy` et `audit_policy` restent des références/politiques déclaratives bornées : leur sémantique effective (ordre de priorité, évaluation d'audit, mécanisme de repli runtime) n'est pas inventée ni contrôlée ici.

## Hors périmètre

- Aucun évaluateur de fanion runtime, aucune persistance ni cache d'affectations, aucune opération administrative ni corrélation d'audit effectif (R2–R4 de `feature-flags`), aucun cycle de vie DRAFT→ACTIVE→PAUSED→EXPIRED→RETIRED, aucune comparaison d'expiration.
- Aucune réécriture de la résolution de capacités ni de la gate de disponibilité ; le lien manifestes/config/contrats n'est pas établi dans ce change.
- Le scénario R3 de `capabilities` n'est pas déclaré réalisé par ce change : la fondation R1 en est la précondition déclarative, la preuve R3 relèvera d'un change ultérieur une fois le mécanisme positif réel disponible.

## Impact

- Spécifications : MODIFIED de la seule exigence R1 « Définition versionnée et bornée » de `feature-flags`, MOTAMOT, sans scénario ajouté ; R2, R3 et R4 inchangées.
- Code : un nouveau module noyau pur stdlib ; aucune source existante modifiée.
- Tests : une suite unitaire et une intégration d'import frais sous gardes, sans I/O.
- Risque : faible — ajout isolé et borné ; aucune interaction avec la composition, les hooks ou la gate.
