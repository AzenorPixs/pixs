"""Préparation de composition par les mécanismes publics du Kernel.

Le port de preuves appartient au code serveur de confiance : il authentifie
les preuves et atteste l'exécution des suites. Il ne provient jamais d'une
requête ou d'un manifest. Aucun port de production ni attestation par défaut.
La bibliothèque contrôle structure/couverture ; elle ne certifie pas ce port.
Ce plan conserve les dimensions non évaluées et ne qualifie aucun P0,
binaire, profil de ressources, exécutant ou parcours d'installation.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Protocol

from pixs.kernel.composition import compose, discover, validate
from pixs.kernel.config.models import ConfigDeclaration, validate_config_declarations
from pixs.kernel.config.resolution import SecretReference, qualified_key, resolve_configuration
from pixs.kernel.conformity import ConformityAttestation
from pixs.kernel.registry.registries import build_registries

__all__ = ["AttestationPort", "HostPlanError", "PreparedHostPlan", "prepare_host_plan"]
_PLAN_KEY = object()
_PBO_REQUIRED = ("pixs.kernel", "pixs.core", "pixs.auth", "pixs.agent", "pixs.pzt")
_REGISTRIES = ("modules", "dependencies", "lifecycle", "services", "events", "configuration", "extensions")


class HostPlanError(ValueError):
    def __init__(self, stage, diagnostics=()):
        super().__init__("Composition hôte refusée à la phase " + stage + ".")
        self.stage = stage
        self.diagnostics = tuple(diagnostics)


class AttestationPort(Protocol):
    """Adaptateur externe sélectionné par l'appelant serveur de confiance.

    Authentifier provenance, fraîcheur et versions, puis attester les suites
    réellement exécutées relève de cette implémentation, sans manifest comme
    preuve. L'absence du port refuse l'activation ; aucun substitut implicite.
    """
    def authenticate_and_read(self, manifests: tuple) -> tuple[ConformityAttestation, ...]:
        ...


@dataclass(frozen=True, slots=True, repr=False, init=False)
class PreparedHostPlan:
    manifests: tuple
    registries: object
    configuration: object
    composition: object
    required_ids: tuple

    def __init__(self, key, *, manifests, registries, configuration, composition, required_ids):
        if key is not _PLAN_KEY:
            raise HostPlanError("construction")
        for name, value in (("manifests", manifests), ("registries", registries),
                            ("configuration", configuration), ("composition", composition),
                            ("required_ids", required_ids)):
            object.__setattr__(self, name, value)

    def __repr__(self):
        return "PreparedHostPlan(<confidentiel>)"

    @property
    def unevaluated_dimensions(self):
        return self.composition.unevaluated_dimensions


def _strings(values):
    if type(values) not in (tuple, list):
        raise HostPlanError("entrées")
    result = tuple(values)
    if any(type(value) is not str or not value for value in result):
        raise HostPlanError("entrées")
    return result


def _atom(value):
    if type(value) in (str, int) or value is None:
        return value
    if type(value) is SecretReference:
        if any(type(part) is not str or not part for part in (value.owner_id, value.entry_id, value.source)):
            raise HostPlanError("configuration")
        return SecretReference(value.owner_id, value.entry_id, value.source)
    raise HostPlanError("configuration")


def _mapping(value):
    if value is None:
        return {}
    if type(value) is not dict or any(type(key) is not str or not key for key in value):
        raise HostPlanError("configuration")
    return {key: _atom(item) for key, item in value.items()}


def _declarations(value):
    if type(value) not in (tuple, list):
        raise HostPlanError("configuration")
    result = []
    for item in tuple(value):
        if type(item) is not ConfigDeclaration:
            raise HostPlanError("configuration")
        if any(type(part) is not str or not part for part in (item.owner_id, item.entry_id, item.value_type)):
            raise HostPlanError("configuration")
        if type(item.required) is not bool or type(item.is_secret) is not bool or type(item.allowed) is not tuple:
            raise HostPlanError("configuration")
        result.append(ConfigDeclaration(item.owner_id, item.entry_id, item.value_type,
            _atom(item.default), item.required, tuple(_atom(v) for v in item.allowed), item.is_secret))
    return tuple(result)


def prepare_host_plan(*, manifest_texts, official_ids, required_ids, declarations=(),
                      configured_providers=None, schema_values=None, static=None,
                      runtime=None, secret_references=None,
                      attestation_port: AttestationPort | None = None) -> PreparedHostPlan:
    """Prépare un instantané fermé ; aucune activation de ressource ici.

    Le profil PBO exige les cinq composants dont l'identité est adoptée.
    DNS reste une obligation de qualification distincte : aucun identifiant
    absent du canon n'est inventé et ce résultat ne certifie pas le P0.
    """
    texts = _strings(manifest_texts)
    officials, required = _strings(official_ids), _strings(required_ids)
    if not set(_PBO_REQUIRED).issubset(required):
        raise HostPlanError("composants essentiels")
    providers = _mapping(configured_providers)
    if any(type(value) is not str or not value for value in providers.values()):
        raise HostPlanError("fournisseurs")
    decls = _declarations(declarations)
    layers = {name: _mapping(value) for name, value in (
        ("schema_values", schema_values), ("static", static),
        ("runtime", runtime), ("secret_references", secret_references))}
    # Le Kernel reçoit le nom opaque de source ; la frontière hôte exige
    # auparavant une référence typée liée exactement à la clé déclarée.
    references = layers["secret_references"]
    for key, reference in references.items():
        if type(reference) is not SecretReference or key != qualified_key(reference.owner_id, reference.entry_id):
            raise HostPlanError("références de secrets")
    layers["secret_references"] = {key: reference.source for key, reference in references.items()}
    manifests, diagnostics = validate(discover(texts), official_ids=officials, required_ids=required)
    if diagnostics:
        raise HostPlanError("validation", diagnostics)
    owners = {manifest.id for manifest in manifests}
    if any(declaration.owner_id not in owners for declaration in decls):
        raise HostPlanError("propriétaire de configuration")
    diagnostics = validate_config_declarations(decls)
    if diagnostics:
        raise HostPlanError("schémas de configuration", diagnostics)
    registries = build_registries(manifests)
    configuration = resolve_configuration(decls, **layers)
    if configuration.diagnostics or not configuration.complete:
        raise HostPlanError("résolution de configuration", configuration.diagnostics)
    attestations = ()
    if attestation_port is not None:
        reader = getattr(attestation_port, "authenticate_and_read", None)
        if not callable(reader):
            raise HostPlanError("port de conformité")
        attestations = reader(tuple(manifests))
        if type(attestations) is not tuple or any(type(item) is not ConformityAttestation for item in attestations):
            raise HostPlanError("attestations de conformité")
    composition = compose(texts, official_ids=officials, required_ids=required,
                          configured_providers=providers, attestations=attestations)
    if composition.diagnostics or not composition.activated:
        raise HostPlanError("composition", composition.diagnostics)
    if composition.globally_compatible is not False:
        raise HostPlanError("portée de compatibilité")
    snapshot = MappingProxyType({name: tuple(getattr(registries, name).entries) for name in _REGISTRIES})
    return PreparedHostPlan(_PLAN_KEY, manifests=tuple(manifests), registries=snapshot,
        configuration=configuration, composition=composition, required_ids=required)
