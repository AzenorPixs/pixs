"""Liaison privée du plan protégé C08 au challenge R01 Auth.

Construction : session et intention Auth, plan et writer C08, puis ce
raccord qui lie le challenge avant l'appel au publisher. Les confirmations
existantes sont vérifiées par le writer ; aucune n'est créée ici.
"""
from __future__ import annotations

import os
import threading

from pixs.auth.bootstrap_session import (
    AuthBootstrapSession, BootstrapDraft, BootstrapSigningChallenge)
from pixs.backend.installation.plan import (
    PlanInvalid, check_plan_facts_bind, plan_sha256)
from pixs.backend.installation.result_writer import C08TransactionalResultWriter
from pixs.core.ports import CorePortError

__all__ = ["C08AuthPlanBinding"]


class C08AuthPlanBinding:
    def __init__(self, *, writer: C08TransactionalResultWriter,
                 session: AuthBootstrapSession, draft: BootstrapDraft) -> None:
        if (type(writer) is not C08TransactionalResultWriter
                or type(session) is not AuthBootstrapSession
                or type(draft) is not BootstrapDraft
                or writer._using != session.using
                or writer._clock is not session.clock):
            raise CorePortError()
        self._writer, self._session, self._draft = writer, session, draft
        self._using, self._clock = session.using, session.clock
        self._pid, self._thread = os.getpid(), threading.get_ident()
        self._challenge = None
        session.describe(draft)
        self.resolve_challenge(draft, alias=self._using, operation_id=draft.operation_id)

    def _guard(self):
        if (os.getpid() != self._pid or threading.get_ident() != self._thread
                or self._writer._using != self._using
                or self._session.using != self._using
                or self._writer._clock is not self._clock
                or self._session.clock is not self._clock):
            raise CorePortError()

    @property
    def binding(self):
        self._guard()
        return self._using, self._session, self._draft

    def resolve_challenge(self, draft: BootstrapDraft, *, alias: str,
                          operation_id: str) -> BootstrapSigningChallenge:
        self._guard()
        if (draft is not self._draft or type(alias) is not str or alias != self._using
                or type(operation_id) is not str or operation_id != draft.operation_id):
            raise CorePortError()
        self._session.describe(draft)
        plan, _entry = self._writer._stable()
        try:
            digest = plan_sha256(plan, self._writer._store.limits)
            challenge = self._session.bind_plan(
                draft, act=self._writer._act, plan_sha256=digest,
                credential_intent_ref=plan.credential_intent_ref)
            if type(challenge) is not BootstrapSigningChallenge:
                raise CorePortError()
            check_plan_facts_bind(plan, challenge.facts, self._writer._store.limits)
        except PlanInvalid:
            raise CorePortError() from None
        if self._challenge is None:
            self._challenge = challenge
        elif challenge is not self._challenge:
            raise CorePortError()
        return challenge
