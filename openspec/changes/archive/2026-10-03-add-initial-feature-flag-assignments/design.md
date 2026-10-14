# Design — affectations déclaratives

## Contrat minimal

`FeatureFlagAssignment` est une dataclass frozen à huit champs obligatoires sans défaut. La ligne `valid_from / valid_until` du cadrage donne deux champs. Un champ inconnu est refusé par le constructeur ; une valeur invalide est refusée par le validateur, pas par une validation ajoutée au constructeur.

| Champ | Représentation technique retenue par CGPT |
|---|---|
| flag_id | Référence namespacée exacte, grammaire partagée déjà utilisée en R1 |
| selector | str exact dans FLAG_TARGETING_DIMENSIONS |
| selector_value | str exact non vide, opaque |
| value | bool exact, y compris False, ou jeton str littéral selon les helpers R1 |
| valid_from, valid_until | str UTC au format déjà borné par le helper R1 ; from strictement antérieur à until |
| configuration_version | str exact non vide, opaque, sans SemVer ni comparaison |
| updated_by | str exact non vide, opaque ; aucune preuve d'identité ou grammaire de composant imposée |

Ces représentations constituent des choix techniques CGPT dans la forme déjà cadrée, pas des clauses normatives nouvelles.

## Validation en fermeture

Lot list/tuple exact avant itération, éléments FeatureFlagAssignment exacts avant attributs/eq/hash. Types exacts avant toute opération sur les valeurs ; diagnostics constants agrégés et triés, sans écho ni index dépendant de l'ordre. Réutiliser les helpers de ce même module sans duplication de grammaire. Une comparaison de deux bornes UTC déjà validées vérifie seulement la cohérence structurelle, sans now, environnement ou décision de fenêtre effective.

Aucune règle de doublon, d'unicité, de chevauchement, de correspondance avec une définition, de version ordonnée ou d'acteur authentifié n'est ajoutée. Selector est un champ unique, pas un tuple de dimensions.

## Préservation et tests

Modifications existantes limitées à la documentation nécessaire, __all__ (ajouter les deux noms sans retirer les anciens) et blocs nouveaux isolés. Conserver exactement les classes/helpers/fonctions antérieurs. Tests comportementaux : valeurs/bornes, refus hostiles sans callback, ordre d'entrée, absence d'écho, opacité des métadonnées. Import enfant frais sous gardes causales d'I/O, sans bytecode ni réseau ; regression R1.

## Limites

Ce modèle n'est ni une source persistante ni un évaluateur. Aucun flag n'est activé ou expiré et aucun acteur n'est autorisé. Aucun exemple d'affectation d'installation/production n'est embarqué comme instance globale. Le delta R4 est MOTAMOT ; son scénario de rejet au build et la source persistante ne sont pas déclarés implémentés.
