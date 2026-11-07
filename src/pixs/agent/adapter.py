'''Adaptateur Agent v2, identite exacte et handle local par lease.'''
from __future__ import annotations
import asyncio
from pixs.agent.lifecycle import PostgresAgentLifecycleProducer
from pixs.agent.service import PostgresAgentManagementService
__all__ = ['AgentAdapterError', 'AgentFacadeHandle', 'AgentComponentAdapter']
COMPONENT_ID = 'pixs.agent'
COMPONENT_VERSION = '0.1.0'
FIXED = 'Adaptateur Agent indisponible.'
class AgentAdapterError(ValueError):
    def __init__(self, code='AGENT_ADAPTER_IMPOSSIBLE'):
        super().__init__(FIXED)
        self.code = code
        self.element = 'agent_adapter'
        self.step = 'adapt'
    def __repr__(self):
        return 'AgentAdapterError(<confidentiel>)'
    def __str__(self):
        return 'AgentAdapterError(<confidentiel>)'
def _fail(code):
    raise AgentAdapterError(code) from None
async def _shield_close(producer):
    from asgiref.sync import sync_to_async
    task = asyncio.ensure_future(sync_to_async(producer.close_sync, thread_sensitive=True)())
    cancelled = False
    while not task.done():
        try:
            await asyncio.shield(task)
        except asyncio.CancelledError:
            cancelled = True
    task.result()
    if cancelled:
        raise asyncio.CancelledError from None
    return None
class AgentFacadeHandle:
    def __init__(self, *, producer):
        if type(producer) is not PostgresAgentLifecycleProducer:
            _fail('PRODUCTEUR_INVALIDE')
        service = producer._service
        if type(service) is not PostgresAgentManagementService:
            _fail('SERVICE_INVALIDE')
        self._service = service
        self._producer = producer
        self._lease = producer._generation
        self._closed = False
    def __repr__(self):
        return 'AgentFacadeHandle(<confidentiel>)'
    def _ensure_active(self):
        if self._closed is True:
            _fail('HANDLE_INVALIDE')
        if self._lease != self._producer._generation:
            _fail('HANDLE_INVALIDE')
        if self._producer._opened is not True or self._producer._started is not True:
            _fail('HANDLE_INVALIDE')
        if self._producer.observe_lifecycle().ready is not True:
            _fail('GESTION_INDISPONIBLE')
    def persist_desired(self, *, request, context, instruction):
        self._ensure_active()
        return self._service.persist_desired(request=request, context=context, instruction=instruction)
    def append_observation(self, *, request, context, result, observed_document, observed_at, source_ref):
        self._ensure_active()
        return self._service.append_observation(request=request, context=context, result=result, observed_document=observed_document, observed_at=observed_at, source_ref=source_ref)
    def confirm_observation(self, *, request, context, result, observed_fact_id, proof_ref, postcondition_ref):
        self._ensure_active()
        return self._service.confirm_observation(request=request, context=context, result=result, observed_fact_id=observed_fact_id, proof_ref=proof_ref, postcondition_ref=postcondition_ref)
    def query_state(self, *, request, context, limit):
        self._ensure_active()
        return self._service.query_state(request=request, context=context, limit=limit)
    def dispatch(self, *, request, context, instruction):
        self._ensure_active()
        return self._service.dispatch(request=request, context=context, instruction=instruction)
class AgentComponentAdapter:
    def __init__(self, *, producer):
        if type(producer) is not PostgresAgentLifecycleProducer:
            _fail('PRODUCTEUR_INVALIDE')
        if producer._adapter_claim is not None:
            _fail('PRODUCTEUR_DEJA_LIE')
        producer._adapter_claim = object()
        self._producer = producer
        self._handle = None
        self._entering = False
    def __repr__(self):
        return 'AgentComponentAdapter(<confidentiel>)'
    @property
    def component_id(self):
        return COMPONENT_ID
    @property
    def component_version(self):
        return COMPONENT_VERSION
    def observe_capabilities(self):
        return self._producer.observe_capabilities()
    def observe_lifecycle(self):
        return self._producer.observe_lifecycle()
    def build_hooks(self):
        state = self._producer.observe_lifecycle()
        if state.ready is not True:
            return {}
        return {'configure': self._producer.configure_sync, 'start': self._producer.start_sync}
    async def __aenter__(self):
        from asgiref.sync import sync_to_async
        if self._entering or self._handle is not None or self._producer._clone is not None or self._producer._opened:
            _fail('ENTREE_INVALIDE')
        self._entering = True
        try:
            await sync_to_async(self._producer.open_sync, thread_sensitive=True)()
            handle = AgentFacadeHandle(producer=self._producer)
            self._handle = handle
            return handle
        except BaseException:
            try:
                await _shield_close(self._producer)
            except asyncio.CancelledError:
                raise
            except BaseException:
                raise AgentAdapterError('ACQUISITION_NETTOYAGE_IMPOSSIBLE') from None
            raise
        finally:
            self._entering = False
    async def __aexit__(self, exc_type, exc, tb):
        from asgiref.sync import sync_to_async
        handle = self._handle
        self._handle = None
        if handle is not None:
            handle._closed = True
        await _shield_close(self._producer)
        return False
