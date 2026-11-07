# path: src/pixs/agent/_registry_support.py
"""Garde privee du registre Agent : 11 modeles figes, graphe strict, sans I/O DB a import.

N'accorde aucune completion future par simple presence de migrations :
noeuds pixs_agent exactement {0001,0002,0003,0004,0005}, feuille exacte 0005,
parents exacts n-1 et etats attendus. Coherence Django complete des metadonnees
installees contre project_state cible 0005 via ModelState/MigrationAutodetector
(autodetector depuis l'etat fige cible vers l'etat installe, changements
filtres pixs_agent : champs, contraintes, index, PK composite ; sans repr,
sans DB a import).
Limite : integrite/structure, pas de provenance authentifiee ni M2.
"""
from __future__ import annotations

APP_LABEL = "pixs_agent"
KNOWN_FIVE = ("AgentHead", "AgentOperation", "AgentFact", "PayloadDocument", "PayloadProvenance")
KNOWN_EIGHT = ("AgentHead", "AgentOperation", "AgentFact", "PayloadDocument", "PayloadProvenance", "PaBinding", "PaBindingRevision", "PaBindingState")
KNOWN_ELEVEN = ("AgentHead", "AgentOperation", "AgentFact", "PayloadDocument", "PayloadProvenance", "PaBinding", "PaBindingRevision", "PaBindingState", "PaOutbox", "PaAttempt", "PaDeliveryEvent")
TABLE_BY_MODEL = {
    "AgentHead": "pixs_agent_head",
    "AgentOperation": "pixs_agent_operation",
    "AgentFact": "pixs_agent_fact",
    "PayloadDocument": "pixs_agent_payload_document",
    "PayloadProvenance": "pixs_agent_payload_provenance",
    "PaBinding": "pixs_agent_pa_binding",
    "PaBindingRevision": "pixs_agent_pa_binding_revision",
    "PaBindingState": "pixs_agent_pa_binding_state",
    "PaOutbox": "pixs_agent_pa_outbox",
    "PaAttempt": "pixs_agent_pa_attempt",
    "PaDeliveryEvent": "pixs_agent_pa_delivery_event",
}
HISTORICAL_TABLES = frozenset({"pixs_agent_head", "pixs_agent_operation", "pixs_agent_fact"})
DOC_TABLES = frozenset({"pixs_agent_head", "pixs_agent_operation", "pixs_agent_fact", "pixs_agent_payload_document"})
PROV_TABLES = frozenset({"pixs_agent_head", "pixs_agent_operation", "pixs_agent_fact", "pixs_agent_payload_document", "pixs_agent_payload_provenance"})
BINDING_TABLES = frozenset({"pixs_agent_head", "pixs_agent_operation", "pixs_agent_fact", "pixs_agent_payload_document", "pixs_agent_payload_provenance", "pixs_agent_pa_binding", "pixs_agent_pa_binding_revision", "pixs_agent_pa_binding_state"})
RELAY_TABLES = frozenset({"pixs_agent_head", "pixs_agent_operation", "pixs_agent_fact", "pixs_agent_payload_document", "pixs_agent_payload_provenance", "pixs_agent_pa_binding", "pixs_agent_pa_binding_revision", "pixs_agent_pa_binding_state", "pixs_agent_pa_outbox", "pixs_agent_pa_attempt", "pixs_agent_pa_delivery_event"})
WHITELIST = ("0001_agent_initial", "0002_agent_payload_document", "0003_agent_payload_provenance", "0004_agent_pa_binding", "0005_agent_pa_relay")
STATE_TABLES = {
    "0001_agent_initial": HISTORICAL_TABLES,
    "0002_agent_payload_document": DOC_TABLES,
    "0003_agent_payload_provenance": PROV_TABLES,
    "0004_agent_pa_binding": BINDING_TABLES,
    "0005_agent_pa_relay": RELAY_TABLES,
}
EXPECTED_PARENTS = {
    "0001_agent_initial": (),
    "0002_agent_payload_document": ("0001_agent_initial",),
    "0003_agent_payload_provenance": ("0002_agent_payload_document",),
    "0004_agent_pa_binding": ("0003_agent_payload_provenance",),
    "0005_agent_pa_relay": ("0004_agent_pa_binding",),
}
__all__ = ["APP_LABEL", "KNOWN_FIVE", "KNOWN_EIGHT", "KNOWN_ELEVEN", "HISTORICAL_TABLES", "DOC_TABLES", "PROV_TABLES", "BINDING_TABLES", "RELAY_TABLES", "WHITELIST", "check_registry_current", "check_registry_five", "check_registry_eight", "check_registry_eleven", "check_frozen_states"]


def _check_identity_tables(by_name, models_module) -> bool:
    if set(by_name) != set(KNOWN_ELEVEN):
        return False
    for _name in KNOWN_ELEVEN:
        _model = by_name.get(_name)
        if _model is None or _model is not getattr(models_module, _name, None):
            return False
        if _model._meta.db_table != TABLE_BY_MODEL[_name]:
            return False
        if _model._meta.app_label != APP_LABEL:
            return False
    # Garde runtime de la PK composite, distincte de la coherence ModelState :
    # ModelState.from_model reconstruit depuis local_fields et peut ignorer
    # une substitution tardive de _meta.pk, d'ou ce controle direct.
    try:
        from django.db.models import CompositePrimaryKey as _CompositePK
    except ImportError:
        return False
    _rev_pk = by_name["PaBindingRevision"]._meta.pk
    if type(_rev_pk) is not _CompositePK:
        return False
    if tuple(getattr(_rev_pk, "field_names", ())) != ("binding_id", "revision"):
        return False
    return True


def check_frozen_states(loader) -> bool:
    _nodes = sorted(name for (app, name) in loader.graph.nodes if app == APP_LABEL)
    if tuple(_nodes) != WHITELIST:
        return False
    _leaves = sorted(name for (app, name) in loader.graph.leaf_nodes() if app == APP_LABEL)
    if _leaves != ["0005_agent_pa_relay"]:
        return False
    for _name, _parents in EXPECTED_PARENTS.items():
        _node = loader.graph.node_map[(APP_LABEL, _name)]
        _parent_keys = sorted(node.key for node in _node.parents)
        if tuple(_parent_keys) != tuple((APP_LABEL, n) for n in _parents):
            return False
    try:
        for _migration_name, _expected in STATE_TABLES.items():
            _state = loader.project_state([(APP_LABEL, _migration_name)]).apps.get_app_config(APP_LABEL)
            if {_m._meta.db_table for _m in _state.get_models()} != set(_expected):
                return False
    except (LookupError, ValueError, TypeError, KeyError):
        return False
    return True


def _check_coherent_with_target0005(apps, loader) -> bool:
    try:
        from django.db.migrations.autodetector import MigrationAutodetector
        from django.db.migrations.state import ProjectState
        _frozen = loader.project_state([(APP_LABEL, "0005_agent_pa_relay")])
        _installed = ProjectState.from_apps(apps)
        _changes = MigrationAutodetector(_frozen, _installed).changes(graph=loader.graph)
        for _app, _migrations in _changes.items():
            if _app != APP_LABEL:
                continue
            if _migrations:
                return False
        return True
    except (LookupError, ValueError, TypeError):
        return False


def check_registry_current(apps, by_name, models_module, loader) -> bool:
    if _check_identity_tables(by_name, models_module) is not True:
        return False
    if check_frozen_states(loader) is not True:
        return False
    if _check_coherent_with_target0005(apps, loader) is not True:
        return False
    return True


def check_registry_eleven(apps, by_name, models_module, loader) -> bool:
    return check_registry_current(apps, by_name, models_module, loader)


def check_registry_eight(apps, by_name, models_module, loader) -> bool:
    return check_registry_current(apps, by_name, models_module, loader)


def check_registry_five(apps, by_name, models_module, loader) -> bool:
    return check_registry_current(apps, by_name, models_module, loader)
