# Design — add-initial-bulk-job-link-v1

## D1 — Périmètre strict

Le module couvre uniquement le profil BulkJobLink v1 du canon `bulk-operations`.
Il ne résout aucune référence, n'établit aucune existence, légitimité,
autorisation, cardinalité globale, unicité globale, corrélation, causalité,
périmètre, déduplication ni persistance, conformément à l'exigence canonique
« Validation pure et limites de BulkJobLink v1 ».

## D2 — Représentation

`@dataclass(frozen=True)` nommée `BulkJobLink`, exactement deux champs annotés
`str` : `operation_id` puis `job_id`. Aucun champ par défaut, aucun champ de
payload, aucun champ supplémentaire, aucune méthode ajoutée, aucun `__post_init__`.
L'immuabilité est celle de `frozen=True` ; la conservation opaque des valeurs est
le comportement du dataclass, non une transformation du module.

## D3 — Exports internes

`__all__ = ["BulkJobLink", "validate_bulk_job_link"]`, dans cet ordre, comme le
precedent `job_correlation`. Aucun export intermédiaire.

## D4 — Validation : types avant comparaison

`validate_bulk_job_link(candidate: object) -> list[Diagnostic]` :

1. `type(candidate) is not BulkJobLink` → refus unique
   `bulk_job_link.link` / « lien BulkJobLink exact attendu », **avant tout accès
   aux attributs** : une sous-classe à hooks, un objet à `__getattr__` hostile et
   tout objet étranger sont écartés sans invocation de comportement étranger.
2. Contrôle champ par champ d'une référence opaque exacte :
   `type(valeur) is str and bool(valeur)` — les sous-classes de `str`, `None`,
   les nombres et la chaîne vide sont refusés ; aucun `isinstance` élargi,
   aucune normalisation, aucun `strip()`, aucun repli.
3. Contrôle de distinction **seulement si** les deux références ont passé l'étape
   2, donc jamais de `==` sur une valeur hostile : c'est l'application de
   « en contrôlant les types avant toute comparaison ». Deux références égales →
   refus unique `bulk_job_link.distinction` / « références distinctes attendues ».

Le refus de type est exclusif : il court-circuite les contrôles de champs et de
distinction, ce qui garde le diagnostic déterministe et empêche tout accès
d'attribut sur un objet étranger.

## D5 — Diagnostics statiques, sans écho

Constantes textuelles figées au module ; `Diagnostic(step=VALIDATE, element=...,
constraint=<constante>, message=<constante>)`. Aucune valeur candidate n'est
interpolée, convertie (`str()`, `repr()`, f-string), journalisée ni exposée. La
déduplication et le tri réutilisent le motif du precedent : clé
`(element, constraint, message)`, tri des clés, liste reconstruite à chaque appel
(listes fraîches et indépendantes, pas d'objet muté partagé).

## D6 — Pureté stdlib et absence d'effet

Imports du module : `dataclasses` et `.diagnostics` uniquement. Aucun I/O, aucune
variable d'environnement, aucun réseau, aucun sous-processus, aucun import de
`django`/`psycopg`/`sqlite3`, aucune dépendance nouvelle (cohérent avec la
présence de gardes de pureté `tests/integration/test_kernel_purity.py` et
l'absence de tout outil de test tiers dans `pyproject.toml`).

## D7 — Préservation de l'existant

`JobCorrelation`, `validate_job_correlation`, `diagnostics`, les façades du
noyau et tous les modules canoniques existants restent **intacts** : le nouveau
module importe seulement Diagnostic/VALIDATE depuis diagnostics et n'étend aucun de leurs contrats ; les constantes
privées du precedent (`_refusal`, `_pack`, `_is_opaque_reference`) ne sont pas
importées en travers des frontières de module, leurs motifs sont repris
localement au strict besoin.

## D8 — Tests : ciblés, pas miroirs

- Unitaires (`unittest`, fixtures synthétiques, marqueurs distinctifs) : refus
  d'égalité des deux références ; conservation opaque valide (deux références
  distinctes → aucune diagnostique et égalité des valeurs rendues) ; types et
  valeurs hostiles (`None`, nombre, vide, sous-classe `str` à hooks, objet à
  attributs/hostiles) sans rappel d'objet étranger ; sous-classe de `BulkJobLink`
  refusée avant accès aux champs ; déterminisme et indépendance des listes de
  diagnostics ; absence de toute valeur dans le rendu ; immuabilité `frozen` et
  obligation de fournir les deux champs ; exactitude de `__all__`.
- Intégration (processus frais) : même squelette de gardes que le precedent
  (`-I -B`, environnement figé, bloquages `open`/`socket`/`Popen`/`system`/
  `environ`/imports DB, **contrôles positifs** prouvant que chaque garde bloque,
  compteurs remis à zéro puis exigés à zéro) ; une seule sonde d'import
  `pixs.kernel.bulk_job_link` puis le minimum de validations caractéristiques
  (valide, type étranger, champ hostile, références égales) ; aucune duplication
  de la suite unitaire ni du precedent `job_correlation`.

## D9 — Validation OpenSpec et archivage

`openspec validate <change> --json` est attendu `valid: true`, `failed: 0`, avec
uniquement le `WARNING` de longueur déjà accepté ; aucune ERROR n'est admise et
aucun texte canon n'est reformulé. L'archivage ultérieur utilise `--skip-specs`,
justifié par l'identité stricte entre le delta et `openspec/specs/bulk-operations/spec.md`
(les deux exigences y figurent déjà mot pour mot depuis la RSMP validée).
