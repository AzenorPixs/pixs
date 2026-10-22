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
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/unit -p test_api_contract_plans.py -v
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/integration -p test_api_contract_plans_integration.py -v
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

Le champ public `message` reste fixe en français (`Erreur interne du service.`).
Son externalisation dans un catalogue du composant avec canon anglais et sa
localisation restent à implémenter pour satisfaire les exigences
d'internationalisation ; cette limite concerne aussi la réponse JSON qui
réutilise cette projection.

Contrôles dédiés exacts :

```text
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/unit -p test_api_error_projection.py -v
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/integration -p test_api_error_projection_integration.py -v
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
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/unit -p test_api_error_response.py -v
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/integration -p test_api_error_response_integration.py -v
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
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/unit -p test_api_success_envelope.py -v
/usr/bin/env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python -m unittest discover -s tests/integration -p test_api_success_response_integration.py -v
```

Limites : aucune route, serveur, version, curseur, idempotence,
authentification, tenant, cache, statut alternatif, suivi asynchrone,
génération d'identifiant ou de date, schéma ou publication OpenAPI.
Le module appelant valide le domaine et choisit des données publiques
non sensibles ; cette fabrique n'est pas un filtre universel de
secrets. L'exigence API complète reste partiellement réalisée.


# Façades Core HTTP v1 — composition C06

La surface C06 publie le contrat `1.0.0` au format OpenAPI `3.1.0`.
Elle contient 156 opérations Core/Auth, indépendantes du frontend. La fabrique
`build_core_api_urls` de `../api_core_views.py` reçoit une
`CoreApiComposition` et la référence contractuelle précédemment approuvée :

```python
urlpatterns = build_core_api_urls(
    composition,
    previous_plan=approved_plan,
    previous_documents=approved_documents,
)
```

`approved_documents` est un tuple de textes JSON approuvés. Lors d'une
évolution, il représente la référence antérieure conservée ; il ne doit pas
être recalculé depuis la proposition. La fabrique calcule les différences
de chemins, méthodes, authentification, paramètres, corps, types, champs
obligatoires, enums et réponses. Une rupture conservant la majeure empêche
la construction. Une majeure suivante exige une référence documentaire
distincte et une coexistence déclarée. Cette déclaration ne prouve pas un
déploiement effectif de deux versions.

La composition fournit explicitement les alias PostgreSQL distincts, la
source et le service Auth C03, la fabrique de ports Core, l'horloge UTC,
l'hôte et l'origine HTTPS approuvés, les limites d'entrée/page/curseur, la
clé de signature et les commandes web qualifiées d'interactives. Les ports
C04 de faits, décisions, filtrage et déclarations ainsi que C05 sont réels.
C09 et C10 sont injectés ; l'absence d'un port nécessaire ferme l'opération.
La bibliothèque n'ouvre pas de serveur, ne configure pas Django, ne lit
pas de secret et ne choisit aucun fournisseur de déploiement.

## Chemins et contextes

| Racine Bearer | Contexte canonique |
| --- | --- |
| `/api/v1/platform` | PLATFORM, sans identifiants tenant/scope |
| `/api/v1/tenants/{tenant_id}` | TENANT à sa racine |
| `/api/v1/tenants/{tenant_id}/scopes/{scope_id}` | TENANT dans le scope nommé |

Pour la façade web, insérer `/web` après `/api/v1`. Les identifiants
opaques sont encodés comme segments URL ; la séparation des segments
précède leur décodage UTF-8. ASGI fournit `raw_path` ; une intégration WSGI
doit fournir le `RAW_URI` original pour prouver les contextes tenant/scope.
En l'absence de cette preuve, la route contextuelle échoue fermée.
Les en-têtes tenant/scope contradictoires sont refusés. Aucun en-tête,
corps ou privilège Super Admin ne promeut un contexte d'authentification.

Les 22 commandes du catalogue `../api_core_catalog.py` utilisent
`POST <racine>/commands/<nom>`. Les 15 collections utilisent
`GET <racine>/<collection>` selon leurs racines déclarées. L'identité,
les liens, les permissions/politiques et les registres globaux sont
administrés depuis PLATFORM ; groupes et rôles respectent leur propriétaire
réel. Le corps ne fournit ni acteur, ni décision, ni opération, ni contexte
de confiance. Les UUIDv7 et enums sont vérifiés avant appel propriétaire.

Le Super Admin reste authentifié par C03. C04 examine son binding et son
accord tenant courant : un tenant non accordé reste refusé même avec un
ALLOW ordinaire ; dans le tenant accordé, l'exception prévaut sur un DENY
ACL. Elle ne fabrique aucun niveau d'assurance, ne remplace pas le contexte
du chemin et ne rend pas un token tenant utilisable dans PLATFORM.

## Auth, cookie et Bearer

`GET /api/v1/web/auth/csrf` est le bootstrap public déclaré. Sous PLATFORM,
les opérations Auth sont `login`, `logout`, `revoke-session`,
`revoke-all`, `change-password` et `renew`. Sous tenant/scope, seules
les opérations de session `login`, `logout`, `revoke-session` et
`renew` sont publiées. `renew` est réservé à Bearer REFRESH et n'existe
pas sur la façade web. Compte et justificatif restent des ressources
globales ; leurs opérations ne sont pas promues depuis un contexte tenant.

La catégorie de session C06 est ADMIN, sélectionnée côté serveur. Les
durées et plafonds viennent des politiques C03 effectives. Le login
tenant/scope vise une référence logique Auth de création
`pixs.auth.session-intent:v1:…`, dérivée du sujet et du contexte complet.
Elle n'est ni un justificatif ni une permission. Sa propriété est reconnue
uniquement après revalidation C03 d'une vraie préparation par mot de passe,
liée à la requête, l'alias et l'opération. Le resolver des ressources Auth
existantes reste fondé sur leurs lignes et refuse cet intent. L'identité
Core conserve sa propriété globale.

La façade web utilise le cookie serveur protégé et CSRF, avec l'origine
approuvée pour les mutations. Elle ne remet pas de Bearer persistant au
navigateur. Les routes Bearer n'utilisent jamais un cookie comme substitut.
Le mélange d'une authentification Bearer et d'un cookie de session web est
refusé ; le header Authorization est également refusé sur la façade web.
La revalidation du token et de la session reste obligatoire à chaque
invocation. C03 possède l'émission et la révocation ; un rejeu d'émission
ne restitue aucun secret réutilisable et peut exiger une réauthentification.

## Résultats, pagination et rejeu

Les succès utilisent `data/meta/links` et les erreurs
`error_code/message/details/correlation_id`. Les codes publics
`pixs.core.api.v1.*` sont stables ; messages français/anglais selon
Accept-Language, anglais par défaut. Les réponses sont `no-store` ;
aucune exception, trace ou donnée d'authentification brute n'est projetée
dans les erreurs.

Les queries acceptent `limit`, `cursor` et des `ref` répétées.
C04 filtre les références avant matérialisation, puis la gouvernance,
le keyset SQL, ORDER BY et LIMIT page+1 s'appliquent avant restitution.
La ligne de réserve reste privée. Le curseur signé lie acteur, contexte
complet, collection, filtres, ordre, taille, dernière clé et snapshot.
Son expiration est bornée par la politique et la décision. Falsification,
expiration ou changement de snapshot imposent un redémarrage explicite.

Toute mutation Core exige `Idempotency-Key`. Le sérialiseur Core v1
produit l'empreinte métier canonique incluant le contexte et excluant
les identifiants de suivi renouvelés. Le participant durable C06 rejoint
la transaction Core avec C05 et les ports nécessaires. Il conserve le
résultat confirmé complet ; un rejeu autorisé restitue les identifiants
d'opération/corrélation initiaux dans `data`, tandis que `meta` décrit
l'appel courant. Un contenu divergent est refusé sans second effet.
IN_PROGRESS ne peut pas être engagé ; une issue de commit inconnue ne
réexécute pas la mutation et exige une preuve persistante réconciliée.
La migration additive est `pixs_core.0003_core_idempotence`.

## Activité interactive et documents

La liste des commandes web interactives est une politique serveur explicite.
Après un premier succès Core réellement confirmé, C06 fournit à C03 une
preuve liée à acteur/session/contexte/opération/date. C03 revalide et
dédoublonne avant toute prolongation. Renouvellement, lecture en arrière-plan
et rejeu ne créent pas d'activité nouvelle. `meta.activity` distingue
RECORDED, REPLAY_IGNORED et NOT_RECORDED. L'échec distinct de ce suivi est
explicite, avec son code public, et ne transforme pas le résultat Core déjà
confirmé en échec ni ne prolonge la session.

`/api/v1/openapi.json` publie un index OpenAPI machine-readable ; ses
`x-documents` indiquent les documents de capacités, tailles et SHA-256.
Chaque document préchargé respecte le plafond de 64 Kio du transport
commun, sans troncature ni référence externe. GET et HEAD sont disponibles ;
les autres méthodes gardent le refus borné du helper historique.

La réalisation est vérifiée par les recettes unitaires de contrat et par
PostgreSQL réel pour C03/C04/C05/Core/C06. Les recettes désignent explicitement
leurs doubles C09/C10 et leur setup C08 de binding/grant ; elles ne qualifient
ni le provisionnement R01, ni une activation P0 complète. Les requêtes Django
et ASGI s'exécutent en processus : aucun serveur ou TLS réseau n'est déployé
ou qualifié par ces tests. Le frontend n'est pas modifié.
