# Contrats — descripteurs déclaratifs

Fondation pure (stdlib, sans I/O) : `ContractDescriptor` cinq champs
obligatoires (`contract_id`, `category`, `version`, `owner_component`,
`guarantees_doc`), `DeprecationNotice` quatre champs obligatoires
(`contract_id`, `previous_version`, `deprecated_in`, `replacement_doc`),
`ContractCategory` sept valeurs (`SERVICE`, `COMMAND`, `QUERY`, `EVENT`,
`HOOK`, `SCHEMA`, `API`), `require_category`, `check_evolution`,
`check_deprecation`, `check_retirement`. Retours constants
`DECLARATIVE_EVOLUTION_VALID`, `DECLARATIVE_DEPRECATION_VALID`,
`DECLARATIVE_RETIREMENT_VALID`. Diagnostics constants sans écho.
`TypeError` natif si signature invalide.

Exemple synthétique via la façade (retours exacts) :

```python
from pixs.kernel.contracts import (
    ContractCategory,
    ContractDescriptor,
    DeprecationNotice,
    check_deprecation,
    check_evolution,
    check_retirement,
    require_category,
)

first = ContractDescriptor(
    contract_id="pixs.contract.order",
    category=ContractCategory.COMMAND,
    version="1.2.3",
    owner_component="pixs.kernel",
    guarantees_doc="Garanties documentees.",
)
assert require_category(first, ContractCategory.COMMAND) is ContractCategory.COMMAND

evolved = ContractDescriptor(
    contract_id="pixs.contract.order",
    category=ContractCategory.COMMAND,
    version="1.3.0",
    owner_component="pixs.kernel",
    guarantees_doc="Garanties documentees.",
)
assert check_evolution(first, evolved, breaking=False) == "DECLARATIVE_EVOLUTION_VALID"

notice = DeprecationNotice(
    contract_id="pixs.contract.order",
    previous_version="1.2.3",
    deprecated_in="1.3.0",
    replacement_doc="Remplacement documente.",
)
assert check_deprecation(evolved, notice) == "DECLARATIVE_DEPRECATION_VALID"
assert check_retirement(notice, "2.0.0") == "DECLARATIVE_RETIREMENT_VALID"
```

La version du composant reste distincte (ex. `9.9.9`) et n'autorise jamais
un retrait. L'annonce exige l'identité exacte `notice.deprecated_in ==
descriptor.version`, build inclus. L'avis normal porte sur des versions
stables, même majeure, `deprecated_in.minor` strictement supérieur
(saut permis), `deprecated_in.patch == 0`. Le retrait normal exige une
version stable en majeure strictement supérieure, prolongation permise.
`breaking` exige `type(breaking) is bool`. Objets forgés revalidés,
documentations non blanches. Ces gardes n'accordent aucune autorisation
réelle, n'effectuent aucun retrait, ne prouvent aucune histoire publiée.

Contrôles dédiés exacts :

```text
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m unittest discover -s tests/unit -p test_contract_descriptors.py -v
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m unittest discover -s tests/integration -p test_contract_descriptors_integration.py -v
```
