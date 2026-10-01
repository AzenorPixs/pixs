# Plans API — fondation déclarative pure

`ApiContractPlan` lie un `ContractDescriptor` exact de catégorie API à
une référence LOGIQUE publique de document OpenAPI (identifiant nu, ni
fichier, ni URL, ni lecture). `api_major_prefix` dérive `/api/v{major}`
de la version contractuelle complète. `check_api_evolution` délègue
l'ordre, la rupture et la précédence à la garde publique de contrat,
puis exige document distinct et coexistence documentée seulement à
majeure strictement supérieure. Retour exact
`DECLARATIVE_API_EVOLUTION_VALID`. Diagnostics constants sans écho,
`TypeError` natif si signature invalide.

Exemple synthétique via la façade (valeurs exactes) :

```python
from pixs.backend.api import (
    ApiContractPlan,
    api_major_prefix,
    check_api_evolution,
)
from pixs.kernel.contracts import ContractCategory, ContractDescriptor

first = ApiContractPlan(
    contract=ContractDescriptor(
        contract_id="pixs.contract.billing",
        category=ContractCategory.API,
        version="1.2.3",
        owner_component="pixs.backend",
        guarantees_doc="Garanties documentees.",
    ),
    openapi_document_ref="pixs.api.billing.v1",
)
assert api_major_prefix(first) == "/api/v1"

minor = ApiContractPlan(
    contract=ContractDescriptor(
        contract_id="pixs.contract.billing",
        category=ContractCategory.API,
        version="1.3.0",
        owner_component="pixs.backend",
        guarantees_doc="Garanties documentees.",
    ),
    openapi_document_ref="pixs.api.billing.v1bis",
)
assert check_api_evolution(first, minor, breaking=False, coexistence_doc=None) == "DECLARATIVE_API_EVOLUTION_VALID"

major = ApiContractPlan(
    contract=ContractDescriptor(
        contract_id="pixs.contract.billing",
        category=ContractCategory.API,
        version="2.0.0",
        owner_component="pixs.backend",
        guarantees_doc="Garanties documentees.",
    ),
    openapi_document_ref="pixs.api.billing.v2",
)
assert api_major_prefix(major) == "/api/v2"
assert check_api_evolution(minor, major, breaking=True, coexistence_doc="Coexistence v1 v2 documentee.") == "DECLARATIVE_API_EVOLUTION_VALID"
```

Les mineures acceptent `coexistence_doc` à `None`. Une rupture à même
majeure est refusée. Ces gardes ne prouvent ni publication OpenAPI
réelle, ni schéma valide, ni coexistence effective, ni transport HTTP,
ni sécurité, ni P0 achevé.

Contrôles dédiés exacts :

```text
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m unittest discover -s tests/unit -p test_api_contract_plans.py -v
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m unittest discover -s tests/integration -p test_api_contract_plans_integration.py -v
```

---

# Projection d'erreur d'infrastructure — fondation déclarative pure

`build_infrastructure_error(correlation_id, *, internal_error)`
normalise une erreur d'infrastructure vers l'enveloppe publique à
5 champs (`error_code`, `message`, `details`, `field_errors`,
`correlation_id`). `internal_error` opaque requis mais jamais
inspecté ; `correlation_id` UUID exact revalidé puis sérialisé
canoniquement (toutes versions admises, aucune norme UUIDv7).
`API_ERROR_CONTRACT_VERSION` vaut `"1.0.0"` (constante publique
séparée, jamais champ d'enveloppe). Chaque appel retourne un dict
frais ; muter un résultat ne contamine aucun appel suivant.

Exemple synthétique via la façade (valeurs exactes) :

```python
import uuid
from pixs.backend.api import (
    API_ERROR_CONTRACT_VERSION,
    build_infrastructure_error,
)

cid = uuid.UUID(int=1)
envelope = build_infrastructure_error(cid, internal_error=RuntimeError("synthetic-boom"))
assert API_ERROR_CONTRACT_VERSION == "1.0.0"
assert envelope == {
    "error_code": "INTERNAL_ERROR",
    "message": "Erreur interne du service.",
    "details": {},
    "field_errors": [],
    "correlation_id": str(cid),
}
```

Limites : ni HTTP, ni rejeu d'idempotence, ni pagination, ni tenant,
ni authentification, ni génération/validation OpenAPI, ni mapping de
statut. La requirement2 globale reste non achevée.

Contrôles dédiés exacts :

```text
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m unittest discover -s tests/unit -p test_api_error_projection.py -v
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m unittest discover -s tests/integration -p test_api_error_projection_integration.py -v
```

---

# Réponse JSON d'infrastructure — fabrique backend isolée

`build_infrastructure_response(correlation_id, *, internal_error)` appelle
d'abord la projection publique existante, exige des réglages Django déjà
configurés, puis retourne un `JsonResponse` non streaming : statut fixe
500, Content-Type exact `application/json; charset=utf-8`, corps décodé
égal à `build_infrastructure_error`, sans conversion de l'erreur interne.
Le statut 500 décrit l'erreur serveur inattendue ; aucune classification
métier n'est ajoutée. La version de l'enveloppe n'est pas modifiée.

L'import de `pixs.backend.api` et de `responses` reste sans Django. Les
imports Django sont locaux après projection. Si Django est absent, l'erreur
d'import native est propagée. Si ses réglages ne sont pas configurés,
`ImproperlyConfigured("Réglages Django non configurés.")` est levée sans
configuration automatique. Aucun `settings.configure`, `django.setup`,
fallback ou chargement d'environnement n'est effectué en production.

Cet exemple est réservé à un processus de test frais, sans réseau ni base.
Il ne constitue pas une configuration de production ou une preuve de service :

```python
import json
import uuid
from django.conf import settings
from django.apps import apps
from pixs.backend.api import build_infrastructure_error, build_infrastructure_response

assert settings.configured is False and apps.ready is False
settings.configure(DEFAULT_CHARSET="utf-8")
cid = uuid.UUID(int=1)
response = build_infrastructure_response(cid, internal_error=None)
assert response.status_code == 500 and response.streaming is False
assert response["Content-Type"] == "application/json; charset=utf-8"
assert json.loads(response.content.decode("utf-8")) == build_infrastructure_error(
    cid, internal_error=None
)
assert apps.ready is False
```

Tests dédiés, sous mandats séparés :

```text
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m unittest discover -s tests/unit -p test_api_error_response.py -v
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundation/bin/python -m unittest discover -s tests/integration -p test_api_error_response_integration.py -v
```

Limites : aucune route, serveur, middleware, authentification, tenant,
corrélation générée, header de corrélation, cache, stockage, idempotence,
pagination, schéma ou publication OpenAPI, ni activation P0. L'exigence API
complète reste partiellement réalisée.

---

# Enveloppe de succès — constructeur pur et fabrique JSON 200

`build_success_envelope(data, *, meta, links)` valide du JSON public
fini aux types exacts (`None`, `bool`, `int`, `float` fini, `str`,
`list`, `dict` à clés `str` exactes, collections `list` admises),
refuse tout sous-type et objet personnalisé sans conversion ni
inspection, copie profondément tous les conteneurs, puis retourne
`{"data":..., "meta":..., "links":...}` frais. `meta` et `links`
sont obligatoires, keyword-only, dictionnaires exacts. Les alias
acycliques sont copiés indépendamment ; les cycles, `NaN` et `±inf`
sont rejetés par `ApiSuccessEnvelopeError` constant sans écho.
`build_success_response(data, *, meta, links)` valide d'abord puis
retourne un `JsonResponse` non streaming statut 200 fixe,
Content-Type exact `application/json; charset=utf-8`, corps décodé
égal à l'enveloppe pure.

Exemple pur via la façade (valeurs exactes) :

```python
from pixs.backend.api import build_success_envelope

envelope = build_success_envelope(
    [{"label": "a-é", "tags": []}, True, 10**40],
    meta={"note": "exemple"},
    links={"next": "/suivant-synthetique"},
)
assert envelope == {
    "data": [{"label": "a-é", "tags": []}, True, 10**40],
    "meta": {"note": "exemple"},
    "links": {"next": "/suivant-synthetique"},
}
```

Exemple pur Unicode bool et grand entier :

```python
from pixs.backend.api import build_success_envelope

envelope = build_success_envelope("café-été 真", meta={}, links={})
assert envelope["data"] == "café-été 真"
assert build_success_envelope(True, meta={}, links={})["data"] is True
assert build_success_envelope(10**40, meta={}, links={})["data"] == 10**40
```

Cet exemple Django réutilise les réglages déjà configurés par
l'exemple de réponse 500 ci-dessus dans un même processus frais
d'audit ; il ne configure jamais une seconde fois et ne constitue
ni production ni preuve de service :

```python
import json
from django.conf import settings
from django.apps import apps
from pixs.backend.api import build_success_envelope, build_success_response

assert settings.configured is True and apps.ready is False
envelope = build_success_envelope("café 真", meta={}, links={})
response = build_success_response("café 真", meta={}, links={})
assert response.status_code == 200 and response.streaming is False
assert response["Content-Type"] == "application/json; charset=utf-8"
assert "café 真".encode("utf-8") in response.content
assert json.loads(response.content.decode("utf-8")) == envelope
assert apps.ready is False
```

Tests dédiés, sous mandats séparés :

```text
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/python/current/bin/python3 -m unittest discover -s tests/unit -p test_api_success_envelope.py -v
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv-backend-foundation/bin/python -m unittest discover -s tests/integration -p test_api_success_response_integration.py -v
```

Limites : aucune route, serveur, version, curseur, idempotence,
authentification, tenant, cache, statut alternatif, suivi asynchrone,
génération d'identifiant ou de date, schéma ou publication OpenAPI.
Le module appelant valide le domaine et choisit des données publiques
non sensibles ; cette fabrique n'est pas un filtre universel de
secrets. L'exigence API complète reste partiellement réalisée.
