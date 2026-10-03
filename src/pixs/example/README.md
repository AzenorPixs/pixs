# Exemple P0 `example.hello` 1.0.0

Objectif démonstratif : provider `example.hello` 1.0.0 et consommateur
`example.client` 1.0.0 autour de la fixture `example.hello.contract`
1.0.0. Portée strictement démonstrative, jamais contrat de production.

## APIs (quatre helpers)

- `example_texts(provider_text: str) -> tuple[str, str]` : le TOML
  provider provient de `component.toml` chargé EXPLICITEMENT par
  l'appelant/test ; le consommateur est constant.
- `example_scope() -> tuple[ScopeContext, TopologySnapshot]` : fixture
  TENANT `t1` + topologie `("t1",)`.
- `example_compose(texts, attestations=()) -> CompositionResult` : la
  composition NÉCESSITE des attestations injectées ; aucune attestation
  réelle présupposée, aucun auto-PASS. Doubles `PASS`
  (`synthetic_attestations`) cantonnés aux tests.
- `example_plan(snapshot, provider, clock, audit, topology, config,
  context) -> FilterPlan` : types injectés explicites ; lot
  `s1/a1/r1+r2/c1` avec le même `context` ; catalogue injecté MUST
  déclarer sujets, actions, ressources, contextes et types d'attributs.

```python
from pathlib import Path
from pixs.example.demo import example_texts

provider_text = Path("src/pixs/example/component.toml").read_text()
provider, consumer = example_texts(provider_text)
```

Le manifest n'est JAMAIS chargé à l'import ; aucun secret de production.

## Parcours vérifiable

```bash
/usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/unit -p test_example_component.py -v
/usr/bin/env PYTHONPATH=src /home/devops/python/current/bin/python3 -B -m unittest discover -s tests/integration -p test_example_composition.py -v
```

Les tests unitaires assemblent manifests + composition déterministe +
scope + PDP/filter sur doubles ; les tests d'intégration assemblent
`compose()` + `plan_filter()` avec attestations test-only et audit
mémoire. Degrés de preuve distincts : ciblés (wiring), globaux
(régressions moteur), jamais conformité P0 globale ni Developer Kit
complet. Exclusions : backend Django, PostgreSQL, providers concrets,
persistance, audit durable, frontend, dépendances nouvelles.
