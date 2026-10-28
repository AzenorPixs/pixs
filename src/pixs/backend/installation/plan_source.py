"""Port propriétaire C08 du plan R01 et de son résultat.

Ce port vérifie les liaisons de données. La vérification de signature appartient
au port C03 appelé par Core ; une structure de faits seule ne l'autorise pas.
"""
from __future__ import annotations

from pixs.backend.installation.plan import PlanInvalid, check_plan_facts_bind
from pixs.backend.installation.result_reader import C08ResultReader
from pixs.backend.installation.result_writer import C08TransactionalResultWriter
from pixs.backend.installation.act_idempotence import C08ActIdempotenceParticipant
from pixs.backend.installation.reuse_result import C08ReuseResultParticipant
from pixs.core.bootstrap_operator import BootstrapOperatorFacts
from pixs.core.dto import BootstrapActInput, BootstrapTargetSpec
from pixs.core.ports import CorePortError, StagedRef, TransactionProof

__all__ = ["C08InstallationPlanSource"]


class C08InstallationPlanSource:
    def __init__(self, *, writer: C08TransactionalResultWriter,
                 reader: C08ResultReader,
                 idempotence: C08ActIdempotenceParticipant,
                 reuse_result: C08ReuseResultParticipant | None = None) -> None:
        if (type(writer) is not C08TransactionalResultWriter
                or type(reader) is not C08ResultReader or reader._writer is not writer
                or type(idempotence) is not C08ActIdempotenceParticipant
                or idempotence._writer is not writer
                or idempotence._inspection != reader._inspection):
            raise CorePortError()
        self._writer, self._reader = writer, reader
        self._idempotence = idempotence
        writer._stable()
        reuse = writer._act.closed_effects == ("REUSE_EXISTING",)
        if reuse:
            if (type(reuse_result) is not C08ReuseResultParticipant
                    or getattr(reuse_result, "_writer", None) is not writer
                    or getattr(reader, "_idempotence", None) is not idempotence):
                raise CorePortError()
        elif reuse_result is not None:
            raise CorePortError()
        self._reuse_result = reuse_result

    def _plan(self, act, alias):
        if (type(act) is not BootstrapActInput or act != self._writer._act
                or type(alias) is not str or alias != self._writer._using):
            raise CorePortError()
        return self._writer._stable()[0]

    def verify_plan(self, act: BootstrapActInput, *, alias: str) -> None:
        self._plan(act, alias)
        return None

    def verify_operator_binding(self, act: BootstrapActInput,
                                facts: BootstrapOperatorFacts, *, alias: str) -> None:
        plan = self._plan(act, alias)
        try:
            check_plan_facts_bind(plan, facts, self._writer._store.limits)
        except PlanInvalid:
            raise CorePortError() from None
        return None

    def resolve_targets(self, act: BootstrapActInput, *, alias: str) -> BootstrapTargetSpec:
        return self._plan(act, alias).target_spec

    def get_closed_effects(self, *, plan_version: str,
                           installation_ref: str) -> tuple[str, ...]:
        plan, _ = self._writer._stable()
        if (type(plan_version) is not str or type(installation_ref) is not str
                or plan_version != plan.plan_version or installation_ref != plan.installation_ref):
            raise CorePortError()
        return plan.closed_effects

    def inspect_confirmed(self, act: BootstrapActInput) -> str | None:
        self._plan(act, self._writer._using)
        return self._idempotence.inspect_confirmed(act)

    def stage_result(self, proof: TransactionProof, *, result_ref: str,
                     transaction_token: str) -> StagedRef:
        participant = self._reuse_result if self._reuse_result is not None else self._writer
        return participant.stage_result(
            proof, result_ref=result_ref, transaction_token=transaction_token)

    def verify_staged(self, proof: TransactionProof) -> None:
        participant = self._reuse_result if self._reuse_result is not None else self._writer
        return participant.verify_staged(proof)
