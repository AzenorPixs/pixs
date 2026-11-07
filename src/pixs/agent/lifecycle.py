'''Producteur lifecycle Agent v2, ressource propre et observations reelles.'''
from __future__ import annotations
import datetime
from pathlib import Path
from tomllib import TOMLDecodeError
from django.apps import apps
from django.db import DatabaseError, InterfaceError, connections, models as db_models
from django.db.models.expressions import BaseExpression
from django.utils.connection import ConnectionDoesNotExist
from psycopg import sql
from pixs.agent import models as agent_models
from pixs.agent import _registry_support as _agent_registry
from pixs.agent.audit_adapter import AgentAuditAdapter
from pixs.agent.identifiers import new_agent_uuid7
from pixs.agent.ports import AgentOperationalProfile, AgentPortsError
from pixs.agent.service import PostgresAgentManagementService
from pixs.backend.host_plan import PreparedHostPlan
from pixs.core.audit_contracts import AuditError, AuditPolicy, apply_redactions_generic, canonical_generic_bytes, serialize_generic
from pixs.core.authz.ports import PortError
from pixs.core.ports import CorePortError
from pixs.core.scope.context import ScopeContext, ScopeStructureError, validate_structure
from pixs.kernel.audit_event import AuditEvent
from pixs.kernel.lifecycle.availability import CapabilityObservation
from pixs.kernel.lifecycle.state import LifecycleState
from pixs.kernel.manifest.models import ManifestValidationError
__all__ = ['AgentLifecycleError', 'PostgresAgentLifecycleProducer']
COMPONENT_ID = 'pixs.agent'
COMPONENT_VERSION = '0.1.0'
CAPABILITY_ID = 'agent.management'
CAPABILITY_VERSION = '1.0.0'
PROBE_ALIAS = 'pixs.agent.probe'
MIGRATION_APP = 'pixs_agent'
MIGRATION_NAME = '0001_agent_initial'
FIXED = 'Cycle de vie Agent indisponible.'
EXPECTED_TABLES = frozenset(['pixs_agent_head', 'pixs_agent_operation', 'pixs_agent_fact'])
EXPECTED_COMPONENT_DEPS = ('pixs.kernel ==0.1.0', 'pixs.core ==0.1.0')
EXPECTED_CONTRACT_DEPS = ('pixs.core.identity.query ==1.0.0', 'pixs.core.scope.query ==1.0.0', 'pixs.core.authz-data.service ==1.0.0')
EXPECTED_CONTRACTS = ('pixs.agent.management.command', 'pixs.agent.management.query', 'pixs.agent.management.service')
class AgentLifecycleError(ValueError):
    def __init__(self, code='AGENT_LIFECYCLE_IMPOSSIBLE'):
        super().__init__(FIXED)
        self.code = code
        self.element = 'agent_lifecycle'
        self.step = 'observe'
    def __repr__(self):
        return 'AgentLifecycleError(<confidentiel>)'
    def __str__(self):
        return 'AgentLifecycleError(<confidentiel>)'
def _fail(code):
    raise AgentLifecycleError(code) from None
def _check_columns(condition, model):
    columns = set()
    def field(name):
        columns.add(model._meta.get_field(name.split('__', 1)[0]).column)
    def visit(value):
        if isinstance(value, db_models.Q):
            for child in value.children:
                if type(child) is tuple:
                    field(child[0])
                    visit(child[1])
                else:
                    visit(child)
        elif isinstance(value, db_models.F):
            field(value.name)
        elif isinstance(value, BaseExpression):
            for expression in value.get_source_expressions():
                visit(expression)
    visit(condition)
    return columns
def _closed():
    return LifecycleState(installed=False, enabled=False, configured=False, healthy=False, ready=False)
class PostgresAgentLifecycleProducer:
    def __init__(self, *, service, enabled, context, plan):
        if type(service) is not PostgresAgentManagementService:
            _fail('SERVICE_INVALIDE')
        if type(enabled) is not bool:
            _fail('ACTIVATION_INVALIDE')
        if type(context) is not ScopeContext:
            _fail('CONTEXTE_INVALIDE')
        try:
            validate_structure(context)
        except ScopeStructureError:
            _fail('CONTEXTE_INVALIDE')
        if type(plan) is not PreparedHostPlan:
            _fail('PLAN_INVALIDE')
        self._service = service
        self._enabled_flag = enabled
        self._context = context
        self._plan = plan
        self._clone = None
        self._registered_alias = None
        self._opened = False
        self._configured = False
        self._started = False
        self._generation = 0
        self._adapter_claim = None
    def __repr__(self):
        return 'PostgresAgentLifecycleProducer(<confidentiel>)'
    def _server_links(self):
        alias = self._service._alias
        profile = self._service._profile
        factory = self._service._factory
        clock = self._service._clock
        audit = self._service._audit
        gov = self._service._gov
        mandate = self._service._mandate
        if type(alias) is not str or alias == '' or chr(0) in alias:
            _fail('ALIAS_INVALIDE')
        return (alias, profile, factory, clock, audit, gov, mandate)
    def _read_manifests(self):
        try:
            from pixs.kernel.manifest import load_manifest_file
            physical = load_manifest_file(Path(__file__).with_name('component.toml'))
        except (OSError, UnicodeError, ManifestValidationError, TOMLDecodeError):
            _fail('MANIFEST_ILLISIBLE')
        matches = [m for m in self._plan.manifests if m.id == COMPONENT_ID]
        if len(matches) != 1:
            _fail('MANIFEST_ABSENT')
        planned = matches[0]
        if physical != planned:
            _fail('MANIFEST_DIVERGENT')
        if (physical.schema_version, physical.id, physical.type, physical.version) != ('1', COMPONENT_ID, 'MODULE', COMPONENT_VERSION):
            _fail('MANIFEST_DIVERGENT')
        if physical.frontend is not None:
            _fail('MANIFEST_DIVERGENT')
        if tuple(physical.dependency_components) != EXPECTED_COMPONENT_DEPS:
            _fail('MANIFEST_DIVERGENT')
        if tuple(physical.dependency_capabilities) != ():
            _fail('MANIFEST_DIVERGENT')
        if tuple(physical.dependency_contracts) != EXPECTED_CONTRACT_DEPS:
            _fail('MANIFEST_DIVERGENT')
        if tuple(physical.optional_dependency_components) != ():
            _fail('MANIFEST_DIVERGENT')
        if tuple(physical.optional_dependency_capabilities) != ():
            _fail('MANIFEST_DIVERGENT')
        if tuple(physical.optional_dependency_contracts) != ():
            _fail('MANIFEST_DIVERGENT')
        if len(physical.provided_capabilities) != 1:
            _fail('MANIFEST_DIVERGENT')
        cap = physical.provided_capabilities[0]
        if cap.id != CAPABILITY_ID or cap.version != CAPABILITY_VERSION:
            _fail('MANIFEST_DIVERGENT')
        if cap.criticality != 'REQUIRED' or cap.fallback != 'none':
            _fail('MANIFEST_DIVERGENT')
        if tuple(cap.contracts) != EXPECTED_CONTRACTS:
            _fail('MANIFEST_DIVERGENT')
        impl = set((c.id, c.version) for c in physical.implemented_contracts)
        if len(physical.implemented_contracts) != 3 or impl != set((c, '1.0.0') for c in EXPECTED_CONTRACTS):
            _fail('MANIFEST_DIVERGENT')
        return (physical, planned)
    def _ports_ok(self, profile, factory, clock, audit, gov, mandate):
        if type(profile) is not AgentOperationalProfile:
            return False
        try:
            profile.__post_init__()
        except AgentPortsError:
            return False
        if not callable(getattr(factory, 'decider_for', None)):
            return False
        if not callable(getattr(factory, 'authentication_for', None)):
            return False
        if not callable(getattr(clock, 'now', None)):
            return False
        if type(audit) is not AgentAuditAdapter:
            return False
        if gov is None or mandate is None:
            return False
        for name in ('attest', 'stage_read', 'verify_staged'):
            if not callable(getattr(gov, name, None)):
                return False
        if not callable(getattr(mandate, 'verify_mandate', None)):
            return False
        return True
    def _bound_owned(self):
        found = []
        for d in self._plan.composition.capability_descriptors:
            if d.owner_component == COMPONENT_ID and d.provider_ref == COMPONENT_ID:
                found.append(d)
        return tuple(found)
    def _make_clone(self, server_alias):
        try:
            srv = connections[server_alias]
        except ConnectionDoesNotExist:
            _fail('ALIAS_INCONNU')
        if srv.in_atomic_block is True:
            _fail('TX_EXTERNE_REFUSEE')
        if srv.connection is not None:
            try:
                auto = srv.get_autocommit()
            except (DatabaseError, InterfaceError):
                _fail('TX_INDETERMINEE')
            if auto is not True:
                _fail('TX_EXTERNE_REFUSEE')
        if srv.vendor != 'postgresql':
            _fail('MOTEUR_REFUSE')
        clone = srv.copy(alias=PROBE_ALIAS + "." + new_agent_uuid7().hex)
        return clone
    def open_sync(self):
        if self._clone is not None or self._opened is True:
            _fail('OUVERTURE_REFUSEE')
        alias, profile, factory, clock, audit, gov, mandate = self._server_links()
        clone = self._make_clone(alias)
        self._clone = clone
        self._opened = True
        self._configured = False
        self._started = False
        self._generation = self._generation + 1
        try:
            # Les signaux PostgreSQL Django retrouvent ce wrapper par son alias.
            try:
                connections[clone.alias]
            except ConnectionDoesNotExist:
                connections[clone.alias] = clone
                self._registered_alias = clone.alias
            else:
                _fail('ALIAS_SONDE_OCCUPE')
            clone.ensure_connection()
        except BaseException as opening:
            try:
                self.close_sync()
            except AgentLifecycleError:
                _fail('ACQUISITION_NETTOYAGE_IMPOSSIBLE')
            if isinstance(opening, (DatabaseError, InterfaceError, ConnectionDoesNotExist)):
                _fail('SONDE_INDISPONIBLE')
            raise
        return None
    def close_sync(self):
        clone = self._clone
        self._opened = False
        self._configured = False
        self._started = False
        self._generation += 1
        if clone is None:
            return None
        try:
            if self._registered_alias is not None:
                if connections[self._registered_alias] is not clone:
                    _fail('LIAISON_SONDE_DIVERGENTE')
            clone.close()
            if self._registered_alias is not None:
                del connections[self._registered_alias]
        except (DatabaseError, InterfaceError, ConnectionDoesNotExist):
            # La reference et sa liaison restent disponibles pour une reprise.
            _fail('FERMETURE_IMPOSSIBLE')
        self._registered_alias = None
        self._clone = None
        return None
    def _installed_sync(self):
        try:
            cfg = apps.get_app_config('pixs_agent')
        except LookupError:
            return False
        if cfg.name != 'pixs.agent' or cfg.label != 'pixs_agent':
            return False
        _registered = list(cfg.get_models())
        if len({m.__name__ for m in _registered}) != len(_registered) or len({m._meta.db_table for m in _registered}) != len(_registered):
            return False
        _by_name = {m.__name__: m for m in _registered}
        for _name, _table in (('AgentHead', 'pixs_agent_head'), ('AgentOperation', 'pixs_agent_operation'), ('AgentFact', 'pixs_agent_fact')):
            _model = _by_name.get(_name)
            if _model is None or _model is not getattr(agent_models, _name, None) or _model._meta.db_table != _table:
                return False
        from django.db.migrations.loader import MigrationLoader as _RegistryLoader
        if _agent_registry.check_registry_current(apps, _by_name, agent_models, _RegistryLoader(None)) is not True:
            return False
        clone = self._clone
        if clone is None or self._opened is not True:
            return False
        try:
            if clone.vendor != 'postgresql':
                return False
            with clone.cursor() as cur:
                cur.execute('SELECT current_schema();')
                row = cur.fetchone()
                if row is None or type(row[0]) is not str or row[0] == '':
                    return False
                cur.execute('SELECT name FROM django_migrations WHERE app = %s;', [MIGRATION_APP])
                names = set(r[0] for r in cur.fetchall())
                if names != set([MIGRATION_NAME]):
                    return False
                cur.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = current_schema() AND left(table_name, %s) = %s;', [len('pixs_agent_'), 'pixs_agent_'])
                owned = set(row[0] for row in cur.fetchall())
                if owned != set(EXPECTED_TABLES):
                    return False
                by_model = {m._meta.db_table: m for m in (agent_models.AgentHead, agent_models.AgentOperation, agent_models.AgentFact)}
                for table in EXPECTED_TABLES:
                    model = by_model[table]
                    desc = clone.introspection.get_table_description(cur, table)
                    by_col = {i.name: i for i in desc}
                    for f in model._meta.local_fields:
                        if f.concrete is not True:
                            continue
                        col = f.column
                        info = by_col.get(col)
                        if info is None or type(info.null_ok) is not bool:
                            return False
                        if info.null_ok != bool(f.null):
                            return False
                        target = f
                        if f.is_relation is True and f.many_to_one is True:
                            target = f.target_field
                        expected_type = target.get_internal_type()
                        try:
                            seen_type = clone.introspection.get_field_type(info.type_code, info)
                        except KeyError:
                            return False
                        if seen_type != expected_type:
                            return False
                        sql_types = {'UUIDField': 'uuid', 'TextField': 'text', 'CharField': 'character varying', 'IntegerField': 'integer', 'BigIntegerField': 'bigint', 'DateTimeField': 'timestamp with time zone'}
                        cur.execute('SELECT data_type, character_maximum_length FROM information_schema.columns WHERE table_schema = current_schema() AND table_name = %s AND column_name = %s;', [table, col])
                        physical = cur.fetchone()
                        if physical is None or physical[0] != sql_types.get(expected_type):
                            return False
                        if expected_type == 'CharField' and physical[1] != target.max_length:
                            return False
                    cols = [i.name for i in desc]
                    probe = sql.SQL('SELECT {} FROM {} LIMIT 0;').format(sql.SQL(', ').join(sql.Identifier(c) for c in cols), sql.Identifier(table))
                    cur.execute(probe)
                for table in EXPECTED_TABLES:
                    model = by_model[table]
                    cons = clone.introspection.get_constraints(cur, table)
                    for c in model._meta.constraints:
                        entry = cons.get(c.name)
                        if entry is None:
                            return False
                        cols = set(entry.get('columns', []))
                        if isinstance(c, db_models.CheckConstraint):
                            if entry.get('check') is not True or cols != _check_columns(c.condition, model):
                                return False
                        elif isinstance(c, db_models.UniqueConstraint):
                            expected = {model._meta.get_field(name).column for name in c.fields}
                            if entry.get('unique') is not True or cols != expected:
                                return False
                        else:
                            return False
                    pk_col = model._meta.pk.column
                    if not any(e.get('primary_key') is True and set(e.get('columns', [])) == set([pk_col]) for e in cons.values()):
                        return False
                    for f in model._meta.local_fields:
                        if f.is_relation is True and f.many_to_one is True:
                            wanted = set([f.column])
                            ok = False
                            for e in cons.values():
                                fk = e.get('foreign_key')
                                if set(e.get('columns', [])) == wanted and fk is not None:
                                    if tuple(fk) == (f.target_field.model._meta.db_table, f.target_field.column):
                                        ok = True
                            if ok is not True:
                                return False
        except (DatabaseError, InterfaceError, ConnectionDoesNotExist):
            return False
        return True
    def _configured_sync(self):
        try:
            alias, profile, factory, clock, audit, gov, mandate = self._server_links()
        except AgentLifecycleError:
            return False
        if self._ports_ok(profile, factory, clock, audit, gov, mandate) is not True:
            return False
        try:
            self._read_manifests()
        except AgentLifecycleError:
            return False
        # Une capacité sans consommateur reste non liée ; cela ne désactive pas son composant.
        conf = self._plan.configuration
        if conf.complete is not True or tuple(conf.diagnostics) != ():
            return False
        return True
    def _healthy_sync(self):
        clone = self._clone
        if clone is None or self._opened is not True:
            return False
        try:
            alias, profile, factory, clock, audit, gov, mandate = self._server_links()
        except AgentLifecycleError:
            return False
        if not callable(getattr(clock, 'now', None)):
            return False
        try:
            now = clock.now()
        except (AuditError, CorePortError, PortError, DatabaseError, InterfaceError):
            return False
        if type(now) is not datetime.datetime or now.tzinfo is not datetime.timezone.utc:
            return False
        if type(audit) is not AgentAuditAdapter:
            return False
        try:
            owner = audit._owner
            policy = owner.policy(self._context, alias)
            if type(policy) is not AuditPolicy:
                return False
            policy.__post_init__()
            stamped = owner.now()
            if type(stamped) is not datetime.datetime or stamped.tzinfo is not datetime.timezone.utc:
                return False
            eid = new_agent_uuid7().hex
            occurred = stamped.strftime('%Y-%m-%dT%H:%M:%SZ')
            event = AuditEvent(eid, occurred, 'UNVERIFIED', self._context.tenant_id, 'agent.lifecycle.probe', 'agent', 'pixs.agent', 'DENIED', 'LIFECYCLE_PROBE', (eid,), (), 'pixs.agent', '0.1.0')
            payload = serialize_generic(event)
            redacted = apply_redactions_generic(payload, policy.redactions)
            raw = canonical_generic_bytes(redacted)
            if type(raw) is not bytes or len(raw) == 0 or len(raw) > policy.max_event_bytes:
                return False
            with clone.cursor() as cur:
                cur.execute('SELECT current_schema();')
                row = cur.fetchone()
                if row is None or type(row[0]) is not str or row[0] == '':
                    return False
        except (AuditError, CorePortError, PortError, DatabaseError, InterfaceError, ConnectionDoesNotExist):
            return False
        return True
    def _observe_all(self):
        try:
            self._read_manifests()
        except AgentLifecycleError:
            return _closed()
        installed = self._installed_sync()
        enabled = installed is True and self._enabled_flag is True
        configured = self._configured_sync() if installed is True else False
        healthy = self._healthy_sync() if installed is True else False
        ready = installed is True and enabled is True and configured is True and healthy is True
        return LifecycleState(installed=installed, enabled=enabled, configured=configured, healthy=healthy, ready=ready)
    def observe_lifecycle(self):
        try:
            return self._observe_all()
        except AgentLifecycleError:
            return _closed()
    def observe_capabilities(self):
        try:
            state = self._observe_all()
            owned = self._bound_owned()
        except AgentLifecycleError:
            return ()
        result = []
        for d in owned:
            if d.capability_id == CAPABILITY_ID and d.capability_version == CAPABILITY_VERSION:
                result.append(CapabilityObservation(CAPABILITY_ID, CAPABILITY_VERSION, COMPONENT_ID, state.ready is True))
        return tuple(result)
    def configure_sync(self):
        if self._opened is not True or self._clone is None:
            _fail('RESSOURCE_FERMEE')
        state = self._observe_all()
        if state.ready is not True:
            _fail('CONFIGURATION_IMPOSSIBLE')
        self._configured = True
        return None
    def start_sync(self):
        if self._opened is not True or self._configured is not True:
            _fail('DEMARRAGE_REFUSE')
        state = self._observe_all()
        if state.ready is not True:
            self._started = False
            _fail('DEMARRAGE_REFUSE')
        self._started = True
        return None
