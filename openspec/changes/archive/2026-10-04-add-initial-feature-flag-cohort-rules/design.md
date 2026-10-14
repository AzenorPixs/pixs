# Design — calcul pur de cohorte

## Contrats

`FeatureFlagCohortRule` est une dataclass figée avec exactement quatre champs obligatoires sans défaut : `cohort_key: str`, `subject_dimension: str`, `threshold_basis_points: int`, `configuration_version: str`. Aucun alias ni champ arbitraire.

`FeatureFlagCohortResolution` est figée avec trois champs obligatoires : `status: str` (`MEMBER`, `NON_MEMBER`, `REFUSED`), `bucket: int | None`, `diagnostics: tuple[Diagnostic, ...]`. Le bucket est présent uniquement sur une décision valide de membership ; un refus n'expose aucune valeur ou identité. Membership n'est jamais une permission ni une valeur de fanion.

`validate_feature_flag_cohort_rule(rule)` retourne seulement les diagnostics de structure d'une règle singulière. Aucun modèle de dataset ou résolution de doublons n'est inventé.

`resolve_feature_flag_cohort(definition, rule, context, expected_configuration_version)` valide d'abord les types exacts avant tout attribut, comparaison ou hachage, puis les structures ; il vérifie la clé contre la cohorte déclarée, la dimension contre celles déclarées par le fanion, la version contre la version canonique attendue et la présence d'une identité canonique. Il refuse sans défaut implicite toute entrée inconnue, hors contrat ou incompatible. Une définition sans cohorte n'est pas un appel valide de cette primitive isolée ; son évaluation sans cohorte existante reste inchangée.

## Réutilisation et invariants

Réutiliser les modèles publics et le validateur de définitions de `feature_flags.py`, et ses helpers privés internes `_validate_context`, `_evaluation_diagnostics` et contrôles de référence/texte. Ce couplage privé du même Kernel reste documenté et couvert par régression, sans grammaire parallèle et sans changement de l'ancien module. Les diagnostics sont constants, triés, dédupliqués, sans reproduction d'identité, de clé invalide ni de version fournie.

Les modèles et leurs champs ferment les sous-classes : notamment bool n'est pas un entier de seuil, et les chaînes à hooks ne sont pas hachées ou comparées. Les définitions sont validées structurellement ; le calcul de membership ne tranche ni expiration, prérequis, repli ni autorisation. L'appelant serveur de confiance conserve la responsabilité de provenance et de cohérence du snapshot.

## Algorithme v1, choix technique CGPT

Le seed est exactement `json.dumps([cohort_key, subject_dimension, identity], ensure_ascii=True, separators=(',', ':')).encode('ascii')`. Ne normaliser ni Unicode, ni casse, ni espace des identités opaques. JSON ASCII préserve aussi les surrogates sans erreur d'encodage. Le digest SHA-256 entier de 32 octets est interprété en big-endian puis réduit modulo 10000. `MEMBER` si et seulement si `bucket < threshold_basis_points` ; sinon `NON_MEMBER`. 0 n'inclut personne, 10000 inclut tout sujet valide.

Le seed ne contient ni seuil, ni version de configuration, ni identifiant/version du fanion, ni `as_of`. À clé, dimension et identité identiques, le bucket est stable ; modifier un seuil ou une version valide ne le redistribue pas. Aucun builtin hash aléatoire, tirage, horloge ou environnement métier n'est consulté.

Vecteurs de référence précomputés par CGPT, à utiliser comme constantes : seed ASCII `["beta","TENANT","tenant-a"]` -> bucket 4599 ; `["beta","TENANT","tenant-\u00e9"]` -> 922 ; `["beta","SCOPE","scope-a"]` -> 1393. Ils ne doivent pas être régénérés dans les assertions par un miroir de l'implémentation.

## Validation et suite du cycle

Tests significatifs des quatre dimensions, des frontières et de l'égalité stricte, des versions/liaisons absentes ou incompatibles, des modèles figés et champs requis, des valeurs à hooks sans callback, de l'absence d'écho et de mutation, du Unicode/surrogate et des buckets fixes. Intégration en processus frais : finder bloquant Django/SQL/réseau et douze gardes d'E/S causales activées et éprouvées avant import, compteurs à zéro après import et usages ; les lectures physiques normales des imports via io ne sont pas présentées comme absentes. Variations PYTHONHASHSEED en environnement de test explicite vérifient la stabilité entre processus sans lire l'environnement métier.

Cette unité ne compose aucune affectation, aucun repli ni expiration. Son achèvement permet de sélectionner ensuite l'intégration de la cohorte à ces primitives existantes, après contrôle séparé des critères.
