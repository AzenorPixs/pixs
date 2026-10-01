## Context

Les exigences contracts fixent sept catégories non interchangeables, une version SemVer indépendante du composant et une dépréciation/retrait encadrés. Le socle actuel valide l’identifiant et la version exacte dans les manifests et résout les contrats dans la composition, sans descripteur de contrat avec catégorie, propriétaire et garanties. Le parseur SemVer partagé est l’unique référence de versions. Aucune API existante ni aucun modèle de manifest ne doit être modifié.

## Goals / Non-Goals

Préparer une fondation pure vérifiable : descripteurs immuables à cinq champs, catégories fermées, versions indépendantes, garde de catégorie exacte, comparaison déclarée avec indicateur explicite, avis de dépréciation séparé et contrôle de retrait normal. Préserver les fondations existantes et ne créer aucune norme nouvelle.

Ne pas réaliser de registre, activation, exécution, garantie transactionnelle, persistance, détection automatique de rupture sémantique ou de schéma, chemin critique d’exception, ni suppression réelle. Ne pas présenter un descripteur comme une preuve de compatibilité globale, de conformité comportementale, d’histoire publiée ou de disponibilité de service. Ne pas confondre un statut descriptif avec une disponibilité opérationnelle.

## Decisions

- Nouveau paquet pur src/pixs/kernel/contracts, stdlib uniquement, sans I/O. Aucune API existante ni aucun modèle de manifest modifié.
- `ContractCategory` est une énumération figée des sept valeurs `SERVICE`, `COMMAND`, `QUERY`, `EVENT`, `HOOK`, `SCHEMA`, `API`. L’appartenance est vérifiée par identité stricte du membre parmi les sept membres.
- `ContractDescriptor` est une dataclass figée à cinq champs tous obligatoires : `contract_id`, `category`, `version`, `owner_component`, `guarantees_doc`. `DeprecationNotice` est un objet séparé figé à quatre champs tous obligatoires : `contract_id`, `previous_version`, `deprecated_in`, `replacement_doc`. L’immutabilité est contrôlée à la construction avec types stricts ; `contract_id` et `owner_component` sont des chaînes non vides sans comparateur validées comme identifiants nus par `parse_requirement` ; `version`, `previous_version` et `deprecated_in` sont des SemVer 2.0.0 complètes validées par `parse_version` ; `guarantees_doc` et `replacement_doc` sont des chaînes non vides sans interprétation automatique. Aucun parseur ni expression régulière divergent. Les descripteurs et `check_evolution` acceptent toute SemVer 2.0.0 valide, préversions et builds compris.
- Les fonctions publiques revalident chaque objet reçu au lieu de présumer qu’une dataclass figée n’a pas été forgée, exigent les types exacts sans conversion, ne mutent rien et réutilisent exclusivement `parse_version`, `parse_requirement` et `compare`. Un booléen n’est jamais converti depuis une valeur truthy. Toute erreur est encapsulée en `ContractDescriptorError` avec messages constants sans écho des entrées.
- Les conditions normales de validité de `DeprecationNotice` (versions stables, même majeure, augmentation de mineure, patch d’annonce nul, remplacement documenté non blanc) sont exigées dès sa construction et lors de chaque revalidation, y compris dans `check_retirement`. Un avis forgé ou incohérent ne peut donc autoriser une déclaration de retrait. `guarantees_doc` et `replacement_doc` doivent contenir au moins un caractère non blanc.
- Les refus de validation à l’intérieur des API utilisent `ContractDescriptorError` sans valeur brute. Les erreurs d’appel de signature Python (arguments obligatoires absents ou nombre d’arguments invalide) restent des `TypeError` standards ; ces fonctions ne chargent ni ne traitent de payload externe non filtré.
- Signatures exactes :

```python
class ContractDescriptorError(ValueError): ...

def require_category(descriptor: object, expected_category: object) -> ContractCategory: ...
def check_evolution(previous: object, proposed: object, *, breaking: bool) -> str: ...
def check_deprecation(descriptor: object, notice: object) -> str: ...
def check_retirement(notice: object, retired_in: object) -> str: ...
```

- `require_category` revalide le descripteur, exige que `expected_category` soit un membre `ContractCategory` par identité et impose l’égalité exacte de catégorie. Tout écart est refusé fermé. En succès, elle retourne le membre validé. La fonction n’exécute rien et ne prouve aucune garantie transactionnelle : un `EVENT` n’est jamais accepté comme `COMMAND` et un `HOOK` ne vaut jamais garantie transactionnelle.
- `check_evolution` exige `type(breaking) is bool`, jamais une valeur truthy. Elle revalide les deux descripteurs puis compare la paire explicite précédente/proposée. Une déclaration de renommage reste possible seulement comme proposition explicite avec version majeure croissante : si `contract_id` diffère, rupture inférée et `proposed.major` doit être strictement supérieur à `previous.major`. Si `category` diffère, rupture inférée avec la même exigence de majeure. Si `breaking` vaut exactement vrai, `proposed.major` doit être strictement supérieur à `previous.major`. Ces exigences de majeure valent indépendamment du build et de la préversion. Sinon, à identifiant et catégorie identiques avec `breaking` exactement faux, toute baisse est refusée : `compare(proposed.version, previous.version)` doit être supérieur ou égal à zéro. Si `compare` vaut zéro, seule la répétition des mêmes champs hors version est autorisée : version égale ou seule métadonnée de build différente, avec mêmes `contract_id`, `category`, `owner_component` et `guarantees_doc`. Tout changement de propriétaire ou de documentation à même précédence est refusé. Une version supérieure non breaking n’atteste aucune sémantique réelle. En succès, elle retourne exactement `DECLARATIVE_EVOLUTION_VALID`. Aucune comparaison sémantique, de schéma ou de garantie réelle n’est prétendue.
- `check_deprecation` reçoit le descripteur annonçant et revalide le descripteur et l’avis. Elle exige `notice.contract_id == descriptor.contract_id` et `notice.deprecated_in == descriptor.version` en identité exacte, build inclus. Elle ne valide jamais l’avis d’une autre version du même identifiant. Les annonces normales de cette fondation portent sur des versions stables seulement : `previous_version` et `deprecated_in` sans préversion ; les builds sont autorisés mais ignorés pour la précédence et ne relâchent aucune condition. `deprecated_in` doit appartenir à la même majeure que `previous_version`, avec `deprecated_in.minor` strictement supérieur, `deprecated_in.patch == 0` et `compare(deprecated_in, previous_version)` strictement supérieur à zéro. Les annonces en préversion ne sont pas supportées et sont refusées fermées, limite explicite de cette fondation. `replacement_doc` non vide est obligatoire. Une nouvelle annonce de dépréciation exige donc une évolution mineure. En succès, elle retourne exactement `DECLARATIVE_DEPRECATION_VALID`.
- `check_retirement` revalide l’avis puis exige pour `retired_in`, version contractuelle complète stable sans préversion, une majeure strictement supérieure à `deprecated_in` ; la prolongation au-delà de la majeure suivante reste possible selon TECHNICAL §10. Les builds ne modifient aucune règle. La version du composant ou de la release n’est jamais utilisée. Aucun paramètre de justification ni de contournement critique n’existe dans cette fondation : tout retrait anticipé est refusé fermé. Aucune suppression réelle n’est effectuée et la garde reste une garde de déclaration seule, sans effet ni cible opérationnelle. En succès, elle retourne exactement `DECLARATIVE_RETIREMENT_VALID`.
- Ces gardes attestent seulement la cohérence des déclarations reçues, pas une histoire publiée, pas le maintien effectif d’une majeure, pas une autorisation de retrait.
- Aucun diagnostic ne reproduit une entrée brute : messages constants nommant le champ sans écho de valeur, de clé ou de version fournie.
- Les deltas OpenSpec reprennent les exigences canoniques concernées sans nouvelle exigence normative. Les détails ci-dessus sont les décisions d’implémentation de cette fondation partielle, pas de nouvelles garanties.

## Validation

Tests purs unitaires et d’intégration avec entrées synthétiques valides et invalides, immutabilité à la construction, SemVer avec préversions et builds, category mismatch, baisse et rupture de version, indicateur `breaking` exact, idempotence à précédence égale, dépréciation et retrait normaux stables, refus des annonces en préversion, des retraits anticipés et des chemins non supportés ; syntaxe AST, UTF-8/LF, régressions du projet et validation OpenSpec stricte. Aucun résultat n’est présumé ; les commandes exactes seront soumises individuellement à CAB avec les exécutables DEVOPS. Aucune donnée réelle, I/O ou dépendance nouvelle.

## Risks / Trade-offs

Cette première fondation ne prouve ni compatibilité globale, ni conformité comportementale, ni disponibilité, ni histoire publiée. Les préversions ne portent pas d’annonce normale et les builds ne changent aucune règle. Les changements ultérieurs nécessitent leurs propres spécifications et mandats. Un registre, une activation ou une mesure réelle requiert une autorisation explicite distincte.

## Migration / Rollback

Aucune migration de données et aucune opération externe dans ce change. Les seules modifications prévues concernent le nouveau paquet descripteurs, sa documentation et ses tests ; les fondations existantes sont conservées. Un retour arrière des artefacts versionnés reste soumis aux autorisations applicables.

## Open Questions

L’implémentation et ses preuves restent à effectuer après préparation complète et validation stricte du change.
